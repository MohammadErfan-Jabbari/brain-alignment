#!/usr/bin/env python3
"""E009 A3 PILOT — does brain-tuning buy practical (OOD) value at matched perplexity,
brain-specifically? (the oracle-gated HOLD->PASS pilot, S8/D018.)

This is the cheap green-light/kill pilot the E009 oracle review mandated. It:
  1. Trains 4 arms by KD (Qwen2.5-1.5B -> 0.5B, LoRA, KL retention) on ALL of an
     800-sentence Tuckute TRAIN split toward the GROUP-AVERAGED target (the setting
     with a real representational change, per E008/L016):
       lm_only   = KD only                       (kd_ppl, the matched-ppl baseline)
       mse       = + MSE -> averaged REAL BOLD    (kd_brain)            [lambda-sweep]
       mse_perm  = + MSE -> block-permuted BOLD   (kd_brain_permuted; brain-specificity null)
       textfeat  = + MSE -> TEXT-FEATURE-predicted BOLD (kd_textfeat; the oracle's
                   control separating "brain-derived" from "any smooth text-correlated
                   regressor" — ridge(imageability,surprisal x2 -> BOLD) predictions)
  2. Measures, per arm x seed x lambda:
       - in-domain ppl (WikiText heldout)
       - OOD ppl on Pereira sentences + LeBel spoken transcript -> OOD/in-domain RATIO
       - brain-specific representational gap: held-out (200-sentence) Tuckute unique_r2
  3. Reports: (a) is the brain-specific repr gap (mse - mse_perm) nonzero in all-data
     students? (b) the MEASURED MDE from seed SD of the OOD ratio (NOT Guo's borrowed
     2-4pp). (c) does the repr gap grow with lambda at matched ppl? (d) the downstream
     contrasts mse vs {lm_only, mse_perm, textfeat}.

Run: export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
     CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_a3_pilot.py --seeds 0 1 2 --lambda-grid 10 30
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P
import brain_loss as BL
import run_brain_lever as RBL
from data_adapters import load_tuckute, TUCKUTE_TRAIN_UIDS

ROOT = Path(__file__).resolve().parents[1]
KD_HELDOUT = ROOT / "data/kd_corpus/wikitext103_sentences_heldout.txt"


def load_lines(path, n):
    if not Path(path).exists():
        return []
    return [l.strip() for l in Path(path).read_text().splitlines() if l.strip()][:n]


def pereira_ood(n=400):
    sents = []
    for f in ["stimuli_384sentences.txt", "stimuli_243sentences.txt"]:
        p = ROOT / "data/pereira/Pereira_Materials" / f
        if p.exists():
            sents += [l.strip() for l in p.read_text().splitlines() if l.strip()]
    return sents[:n]


def lebel_ood(n=400, n_stories=3, chunk=20):
    """A few LeBel spoken-narrative transcripts -> ~20-word pseudo-sentences (OOD: spoken)."""
    try:
        ws = RBL.__dict__  # noqa  (keep import side-effect-free)
        from lebel_adapter import get_wordseqs, list_stories
        stories = list_stories()[:n_stories]
        seqs = get_wordseqs(stories)
        out = []
        for st in stories:
            words = [str(w) for w in list(seqs[st].data)]
            for i in range(0, len(words), chunk):
                seg = " ".join(words[i:i + chunk]).strip()
                if len(seg.split()) >= 5:
                    out.append(seg)
        return out[:n]
    except Exception as e:
        print(f"  [lebel_ood] skipped ({type(e).__name__}: {e})")
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--kd-teacher", default="Qwen/Qwen2.5-1.5B")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--lambda-grid", nargs="+", type=float, default=[10.0, 30.0])
    ap.add_argument("--n-train", type=int, default=800)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--limit-train", type=int, default=None, help="smoke: cap train sentences")
    ap.add_argument("--ood-n", type=int, default=400)
    ap.add_argument("--out", default="outputs/E009_a3_pilot.json")
    args = ap.parse_args()

    import torch
    device = P.pick_device()

    # ---- data: averaged target, contiguous 800/200 split ----
    texts, Y, meta = load_tuckute(args.data_dir)  # averaged over 5 train UIDs
    n = len(texts)
    nc = RBL.matched_nc(args.data_dir)
    cov = RBL.load_covariates(args.data_dir, n)            # [imageability, gpt2xl_surprisal, pcfg_surprisal]
    n_tr = min(args.n_train, n - 100)
    tr, ev = np.arange(n_tr), np.arange(n_tr, n)
    if args.limit_train:
        tr = tr[:args.limit_train]
    texts_tr = [texts[i] for i in tr]; texts_ev = [texts[i] for i in ev]
    Y_tr, Y_ev = Y[tr], Y[ev]

    # ---- text-feature pseudo-target: ridge(cov -> BOLD) fit on train, predicted everywhere ----
    Xc = np.concatenate([cov, np.ones((n, 1))], axis=1)            # +bias
    Xtr = Xc[tr]
    A = Xtr.T @ Xtr + 10.0 * np.eye(Xtr.shape[1])
    W = np.linalg.solve(A, Xtr.T @ Y_tr)                          # (4, n_roi)
    Y_textfeat = Xc @ W                                           # text-derived pseudo-BOLD
    r2_tf = 1 - ((Y_ev - Y_textfeat[ev]) ** 2).sum() / ((Y_ev - Y_ev.mean(0)) ** 2).sum()
    print(f"text-feature target: ridge(cov->BOLD) held-out R2={r2_tf:+.3f} (how much of BOLD is text-feature-explainable)")

    # ---- corpora ----
    indomain = load_lines(KD_HELDOUT, 1000)
    ood = {"pereira": pereira_ood(args.ood_n), "lebel_spoken": lebel_ood(args.ood_n)}
    ood = {k: v for k, v in ood.items() if v}
    print(f"corpora: in-domain(wikitext)={len(indomain)}  " + "  ".join(f"OOD/{k}={len(v)}" for k, v in ood.items()))

    # ---- models ----
    teacher = RBL.load_model(args.kd_teacher, device)[0].eval()
    for p in teacher.parameters():
        p.requires_grad_(False)
    base, tok = RBL.load_model(args.model, device)
    layer = RBL.verdict_layer(base)
    base_ppl_id = RBL.eval_perplexity(base, tok, indomain, device)
    base_ppl_ood = {k: RBL.eval_perplexity(base, tok, v, device) for k, v in ood.items()}
    print(f"{args.model}: L{layer}; base in-domain ppl={base_ppl_id:.1f}  OOD={ {k: round(v,1) for k,v in base_ppl_ood.items()} }")
    # fixed nuisance for the repr-gap unique_r2 (from UNTUNED base, on the eval split)
    Z_ev = P.scalar_nuisance(texts_ev, tok)
    S_ev = P.static_embedding_features(base, tok, texts_ev, device)
    base_uR2, _ = RBL.score_unique_r2(base, tok, texts_ev, Y_ev, Z_ev, S_ev, layer, device)
    print(f"base held-out unique_r2={base_uR2:+.4f}")

    # ---- conditions: (tag, kind, lambda, target) ----
    conds = [("lm_only", None, 0.0, None)]
    for lam in args.lambda_grid:
        conds.append((f"mse_l{lam:g}", "mse", lam, Y))
    lam0 = args.lambda_grid[0]
    conds.append((f"mse_perm_l{lam0:g}", "mse", lam0, "PERM"))
    conds.append((f"textfeat_l{lam0:g}", "mse", lam0, Y_textfeat))
    print("conditions:", [c[0] for c in conds])

    results = {"model": args.model, "kd_teacher": args.kd_teacher, "layer": layer, "nc": nc,
               "base_ppl_indomain": base_ppl_id, "base_ppl_ood": base_ppl_ood,
               "base_heldout_unique_r2": base_uR2, "textfeat_target_r2": float(r2_tf),
               "config": vars(args), "raw": []}
    t0 = time.time()
    for seed in args.seeds:
        for tag, kind, lam, target in conds:
            P.set_seed(seed)
            m, _ = RBL.load_model(args.model, device)
            if target is None:
                Yt = Y_tr
            elif isinstance(target, str) and target == "PERM":
                Yt = BL.block_permute(Y_tr, n_blocks=10, seed=1000 + seed)
            else:
                Yt = target[tr]
            m = RBL.brain_tune(m, tok, texts_tr, Yt, kind, lam, 1.0, layer, device,
                               args.epochs, args.lr, args.batch_size, seed,
                               use_lora=True, model_name=args.model, lora_r=16, teacher=teacher)
            ppl_id = RBL.eval_perplexity(m, tok, indomain, device)
            ppl_ood = {k: RBL.eval_perplexity(m, tok, v, device) for k, v in ood.items()}
            uR2, _ = RBL.score_unique_r2(m, tok, texts_ev, Y_ev, Z_ev, S_ev, layer, device)
            row = {"seed": seed, "arm": tag, "kind": kind, "lambda": lam,
                   "ppl_indomain": ppl_id, "ppl_ood": ppl_ood,
                   "ood_ratio": {k: ppl_ood[k] / ppl_id for k in ppl_ood},
                   "heldout_unique_r2": uR2}
            results["raw"].append(row)
            ratios = "  ".join(f"{k} {row['ood_ratio'][k]:.3f}" for k in ppl_ood)
            print(f"  [{tag:14s} s{seed}] ppl_id={ppl_id:.1f}  OODratio[{ratios}]  uR2={uR2:+.4f}", flush=True)
            del m
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(results, indent=2))
    print(f"\nwrote {args.out} (elapsed {time.time()-t0:.0f}s)")
    print("Run scripts/analyze_a3_pilot.py for the contrasts + measured MDE.")


if __name__ == "__main__":
    main()
