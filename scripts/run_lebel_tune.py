#!/usr/bin/env python3
"""E013 (n=3 existence probe) — per-individual VOXELWISE brain-tuning on LeBel naturalistic data.

The deferred "E007" tuning loop, built tractably: tune the LM (LoRA) so its verdict-layer
features better predict a subject's voxelwise BOLD, then measure HELD-OUT-STORY unique R^2
(the rigorous E006 protocol) vs a block-permuted twin. Per individual (UTS01/02/03).

Tractable architecture (avoids a differentiable Lanczos/FIR loop):
  * TUNE on per-segment pairs: chunk each tune-story's words into CHUNK-word segments;
    target = mean voxelwise BOLD over the TRs spanning the segment's time + HRF delay.
    Reuse `brain_tune` (pooled-segment feature -> MSE readout -> voxelwise BOLD, LoRA).
  * EVAL on HELD-OUT stories with the E006 pipeline (build_story_data + cv_unique_r2):
    Lanczos->TR->FIR contextual features, phone-tier+eng1000 nuisance, story-CV ridge,
    unique R^2 on NC-reliable voxels. Compare real-tuned vs permuted-tuned vs untuned.

POWER CAVEAT (oracle, L021): n=3 deep subjects -> a per-SUBJECT existence probe, NOT a
population claim; per-voxel inference is spatially-autocorrelated, so we report the
per-subject mean-over-voxels gap (tuned-real - tuned-permuted) and treat the 3 subjects as
an existence demonstration. A powered population test needs n>=5 (L024 -> denizenslab).

Run: export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
  CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_lebel_tune.py --subjects UTS01 UTS02 UTS03
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lebel_adapter as L
import brain_loss as BL
import run_brain_lever as RBL
from run_lebel_encoding import cv_unique_r2, HELDOUT_NC_STORY

VERDICT_LAYER = {12: 7, 24: 12, 28: 14}


def build_tune_pairs(stories, subject, vox, chunk_words, hrf_delay_s):
    """Per-segment (text, voxelwise-BOLD) training pairs from tune stories.
    Each segment = CHUNK consecutive words; target = mean BOLD over TRs in the segment's
    time-span shifted by the HRF delay. Returns (texts, Y[n_seg, n_vox])."""
    wordseqs = L.get_wordseqs(stories)
    texts, Ys = [], []
    for st in stories:
        ws = wordseqs[st]
        words = [str(w) for w in list(ws.data)]
        wt = np.asarray(ws.data_times, dtype=np.float64)
        trt = np.asarray(ws.tr_times, dtype=np.float64)
        resp = L.load_response(st, subject)[:, vox]            # (n_tr, n_vox)
        n_tr = min(resp.shape[0], len(trt))
        resp, trt = resp[:n_tr], trt[:n_tr]
        nw = min(len(words), len(wt))
        for i0 in range(0, nw, chunk_words):
            i1 = min(i0 + chunk_words, nw)
            t0, t1 = wt[i0], wt[i1 - 1]
            sel = np.nonzero((trt >= t0 + hrf_delay_s) & (trt <= t1 + hrf_delay_s))[0]
            if len(sel) == 0:                                  # nearest TR to segment midpoint+delay
                sel = [int(np.argmin(np.abs(trt - ((t0 + t1) / 2 + hrf_delay_s))))]
            texts.append(" ".join(words[i0:i1]))
            Ys.append(resp[sel].mean(0))
    Y = np.asarray(Ys, dtype=np.float32)
    # z-score the voxelwise target columns (match the eval's zscored BOLD scale)
    Y = (Y - Y.mean(0, keepdims=True)) / (Y.std(0, keepdims=True) + 1e-6)
    return texts, Y


def eval_unique_r2(model, tok, eval_stories, subject, vox, layer, device, eng1000, n_folds):
    d = L.build_story_data(eval_stories, model, tok, layer, subject=subject, device=device, eng1000=eng1000)
    for s in d:
        d[s]["Y"] = d[s]["Y"][:, vox]
    u = cv_unique_r2(d, eval_stories, n_folds)                 # (folds, n_vox)
    return float(u.mean()), u.mean(0)                          # mean scalar, per-voxel mean-over-folds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--subjects", nargs="+", default=["UTS01", "UTS02", "UTS03"])
    ap.add_argument("--n-tune-stories", type=int, default=14)
    ap.add_argument("--n-eval-stories", type=int, default=6)
    ap.add_argument("--chunk-words", type=int, default=25)
    ap.add_argument("--hrf-delay", type=float, default=4.0)
    ap.add_argument("--reliability-thresh", type=float, default=0.5)
    ap.add_argument("--n-folds", type=int, default=3)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--lambda-brain", type=float, default=10.0)
    ap.add_argument("--lora-r", type=int, default=16)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--n-perm", type=int, default=1)
    ap.add_argument("--seeds", nargs="+", type=int, default=[0])
    ap.add_argument("--limit-tune", type=int, default=None, help="smoke: cap tune segments")
    ap.add_argument("--out", default="outputs/E013_lebel_tune.json")
    args = ap.parse_args()

    import torch
    from transformers import AutoConfig
    device = "cuda" if torch.cuda.is_available() else "cpu"
    nlayers = AutoConfig.from_pretrained(args.model).num_hidden_layers
    layer = VERDICT_LAYER.get(nlayers, max(1, nlayers // 2))
    eng1000 = L._eng1000()
    base0, tok = RBL.load_model(args.model, device)
    del base0
    results = {"model": args.model, "layer": layer, "config": vars(args), "subjects": {}}
    t0 = time.time()

    for subj in args.subjects:
        allst = [s for s in L.list_stories(subj) if s != HELDOUT_NC_STORY]
        on_disk = [s for s in allst if (Path(f"data/lebel_ds003020/preprocessed_data/{subj}") / f"{s}.hf5").exists()]
        tune_st = on_disk[:args.n_tune_stories]
        eval_st = on_disk[args.n_tune_stories:args.n_tune_stories + args.n_eval_stories]
        if len(eval_st) < 2 or len(tune_st) < 2:
            print(f"[{subj}] SKIP — insufficient stories on disk (tune {len(tune_st)}, eval {len(eval_st)})")
            continue
        rel = L.voxel_reliability(L.load_repeats(HELDOUT_NC_STORY, subj))
        vox = np.nonzero(rel > args.reliability_thresh)[0]
        print(f"\n=== {subj}: {len(vox)} NC voxels; tune {len(tune_st)} stories, eval {len(eval_st)} ===", flush=True)
        texts_tune, Y_tune = build_tune_pairs(tune_st, subj, vox, args.chunk_words, args.hrf_delay)
        if args.limit_tune:
            texts_tune, Y_tune = texts_tune[:args.limit_tune], Y_tune[:args.limit_tune]
        print(f"  {len(texts_tune)} tune segments; Y {Y_tune.shape}", flush=True)

        # untuned baseline unique R^2 on eval stories
        base, _ = RBL.load_model(args.model, device)
        base_u, _ = eval_unique_r2(base, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
        del base; torch.cuda.empty_cache()
        print(f"  untuned eval unique R^2 = {base_u:+.4f}", flush=True)

        rows = []
        for seed in args.seeds:
            # real-tuned
            RBL.P.set_seed(seed)
            m, _ = RBL.load_model(args.model, device)
            m = RBL.brain_tune(m, tok, texts_tune, Y_tune, "mse", args.lambda_brain, 1.0, layer, device,
                               args.epochs, args.lr, args.batch_size, seed, use_lora=True,
                               model_name=args.model, lora_r=args.lora_r, teacher=None)
            real_u, _ = eval_unique_r2(m, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
            del m; torch.cuda.empty_cache()
            # permuted twins
            perm_us = []
            for p in range(args.n_perm):
                RBL.P.set_seed(seed)
                mp, _ = RBL.load_model(args.model, device)
                Yperm = BL.block_permute(Y_tune, n_blocks=10, seed=1000 + seed * 10 + p)
                mp = RBL.brain_tune(mp, tok, texts_tune, Yperm, "mse", args.lambda_brain, 1.0, layer, device,
                                    args.epochs, args.lr, args.batch_size, seed, use_lora=True,
                                    model_name=args.model, lora_r=args.lora_r, teacher=None)
                pu, _ = eval_unique_r2(mp, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
                perm_us.append(pu); del mp; torch.cuda.empty_cache()
            gap = real_u - float(np.mean(perm_us))
            rows.append({"seed": seed, "real_u": real_u, "perm_u_mean": float(np.mean(perm_us)),
                         "perm_us": perm_us, "gap": gap, "base_u": base_u})
            print(f"  [s{seed}] real={real_u:+.4f} perm={np.mean(perm_us):+.4f} GAP={gap:+.4f}", flush=True)
        results["subjects"][subj] = {"n_vox": int(len(vox)), "tune_stories": tune_st, "eval_stories": eval_st,
                                     "base_u": base_u, "rows": rows,
                                     "gap_mean": float(np.mean([r["gap"] for r in rows]))}
        Path(args.out).write_text(json.dumps(results, indent=2))   # checkpoint per subject

    # ---- across-subject existence-probe summary ----
    subj_gaps = {s: results["subjects"][s]["gap_mean"] for s in results["subjects"]}
    results["across_subject"] = {"per_subject_gap": subj_gaps,
                                 "mean": float(np.mean(list(subj_gaps.values()))) if subj_gaps else None,
                                 "n": len(subj_gaps), "n_positive": sum(1 for g in subj_gaps.values() if g > 0)}
    Path(args.out).write_text(json.dumps(results, indent=2))
    print(f"\n=== E013 (n=3 existence probe) SUMMARY ({time.time()-t0:.0f}s) ===")
    for s, g in subj_gaps.items():
        print(f"  {s}: brain-specific gap (real-tuned − permuted-tuned) = {g:+.4f}")
    print(f"  across {len(subj_gaps)} subjects: mean {results['across_subject']['mean']}, "
          f"{results['across_subject']['n_positive']}/{len(subj_gaps)} positive")
    print("  POWER CAVEAT: per-subject existence probe (n=3); not a population claim (L021/L024).")
    print(f"  wrote {args.out}")


if __name__ == "__main__":
    main()
