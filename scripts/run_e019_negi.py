#!/usr/bin/env python3
"""E019 — external reproduce-and-control: a FAITHFUL Negi-2025 brain-tuning head on LeBel. (thesis venv)

Reproduce Negi's monolingual ENCODING gain (tuned LM > vanilla on held-out voxelwise encoding), then add the
controls Negi omits (perplexity-matched generic-text FT + permuted-brain twin) and measure what survives.

WHY A NEW HEAD (oracle F1): `run_lebel_tune.build_tune_pairs` trains on per-segment-MEAN BOLD — the readout-MSE
path L026/L027 proved DEGRADES held-out alignment. That is NOT Negi. The faithful Negi head keeps TR resolution:
  per-word LM feats (last verdict layer, WITH grad) -> Lanczos downsample to TR (fixed matrix, differentiable)
  -> trim -> z-score -> 4-delay FIR -> linear voxel projection -> NT-Xent (Negi's objective) at TR resolution.
The LM is FULL fine-tuned end-to-end through this head. Train uses the SAME feature pipeline as the eval
(`lebel_adapter`): faithfulness = train and eval construct features identically.

Substrate: LeBel UTS01/02/03 (D031 — deep single-subjects, 10-repeat NC story, E006-powered; denizenslab n=6
walled twice). Tractability: train per contiguous WORD-WINDOW (~WIN words ≈ tens of TRs) so backprop through the
LM is bounded; NT-Xent's contrastive set = the window's TRs.

ARMS (per subject, >=3 seeds): (a) vanilla untuned; (b) brain-tuned [reproduce]; (c) ppl-matched generic-text FT;
(d) permuted-brain twin. OUTCOME: held-out unique-R^2 (E006 metric) AND per-voxel encoding Pearson r (Negi metric):
(b-a) reproduced gain; (b-c) survival at matched ppl; (b-d) brain-specificity. Predicted (E015 law + nulls):
(b-a) collapses into the (c)+(d) band. SURVIVES controls -> Fork-A -> STOP for Erfan.
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data/paper-repos/deep-fMRI-dataset/encoding"))
import lebel_adapter as L
import brain_loss as BL
import run_brain_lever as RBL
from run_lebel_encoding import cv_unique_r2, HELDOUT_NC_STORY
from ridge_utils.interpdata import lanczosfun

VERDICT_LAYER = {12: 7, 24: 12, 28: 14}
NDELAYS = 4
TRIM = 5


def lanczos_matrix(old_times, new_times, window=3):
    """Fixed (n_new, n_old) Lanczos resampling matrix = exactly lanczosinterp2D's sincmat
    (cutoff = 1/mean(diff(new_times))). So sincmat @ word_feats == lanczosinterp2D(word_feats, ...)."""
    old_times = np.asarray(old_times, float); new_times = np.asarray(new_times, float)
    cutoff = 1.0 / np.mean(np.diff(new_times))
    M = np.zeros((len(new_times), len(old_times)), np.float64)
    for j in range(len(new_times)):
        M[j, :] = lanczosfun(cutoff, new_times[j] - old_times, window)
    return M.astype(np.float32)


def word_feats_grad(model, tok, words, layer, device, max_tokens=320):
    """Per-word LM features at `layer` WITH grad. Tokenize word-by-word (leading space), concat,
    take the LAST sub-token hidden state per word (matches lm_word_features pool='last'). Process in
    token-windows <= max_tokens to bound memory; each window forwarded WITH grad (gradient flows)."""
    import torch
    # build per-word token id lists (leading space, like GPT/Qwen BPE) and last-token offsets
    word_ids = []
    for w in words:
        ids = tok(" " + str(w), add_special_tokens=False)["input_ids"]
        if len(ids) == 0:
            ids = tok(str(w) if str(w) else " ", add_special_tokens=False)["input_ids"] or [tok.eos_token_id]
        word_ids.append(ids)
    feats = [None] * len(words)
    i = 0
    while i < len(words):
        # greedily pack words into a <=max_tokens window
        j, ntok = i, 0
        while j < len(words) and ntok + len(word_ids[j]) <= max_tokens:
            ntok += len(word_ids[j]); j += 1
        j = max(j, i + 1)  # at least one word
        flat, last_pos = [], []
        for k in range(i, j):
            flat.extend(word_ids[k]); last_pos.append(len(flat) - 1)
        ids = torch.tensor([flat], device=device)
        hs = model(ids, output_hidden_states=True).hidden_states[layer][0]   # (T, d), grad
        for k, lp in zip(range(i, j), last_pos):
            feats[k] = hs[lp]
        i = j
    return torch.stack(feats, 0)   # (n_words, d), grad


def _fir_torch(x, ndelays=NDELAYS):
    """make_delayed equivalent (delays 1..ndelays), differentiable. x (T,d) -> (T, d*ndelays)."""
    import torch
    T, d = x.shape
    outs = []
    for lag in range(1, ndelays + 1):
        z = torch.zeros_like(x)
        z[lag:] = x[:-lag]
        outs.append(z)
    return torch.cat(outs, dim=1)


def _zscore_torch(x, eps=1e-6):
    return (x - x.mean(0, keepdim=True)) / (x.std(0, keepdim=True) + eps)


def negi_tune(model, tok, tune_stories, subject, vox, layer, device, epochs, lr, seed,
              win_words=200, edge_drop=6, temp=0.07, permute=False, perm_seed=0, limit_windows=None):
    """FAITHFUL Negi head full-FT. Build per-story word-windows; each step: word feats(grad) ->
    Lanczos -> trim-edges -> zscore -> FIR -> linear voxel proj -> NT-Xent over the window's TRs."""
    import torch
    from torch import nn
    RBL.freeze_input_embeddings(model)
    model.train()
    d = model.config.hidden_size
    readout = nn.Linear(d * NDELAYS, len(vox)).to(device)
    nn.init.normal_(readout.weight, std=0.02); nn.init.zeros_(readout.bias)
    params = [p for p in model.parameters() if p.requires_grad] + list(readout.parameters())
    opt = torch.optim.AdamW(params, lr=lr)

    # ---- precompute fixed windows: (words, Lanczos matrix, BOLD target) per window ----
    wordseqs = L.get_wordseqs(tune_stories)
    windows = []
    for st in tune_stories:
        ws = wordseqs[st]
        words = [str(w) for w in list(ws.data)]
        wt = np.asarray(ws.data_times, float); trt = np.asarray(ws.tr_times, float)
        resp = L.load_response(st, subject)[:, vox]                    # (n_tr, n_vox)
        ntr = min(resp.shape[0], len(trt)); resp, trt = resp[:ntr], trt[:ntr]
        nw = min(len(words), len(wt))
        for w0 in range(0, nw, win_words):
            w1 = min(w0 + win_words, nw)
            if w1 - w0 < 20:
                continue
            tsel = np.nonzero((trt >= wt[w0]) & (trt <= wt[w1 - 1]))[0]
            if len(tsel) < 2 * edge_drop + 8:
                continue
            M = lanczos_matrix(wt[w0:w1], trt[tsel])                   # (n_tr_win, n_win_words)
            Yw = resp[tsel].astype(np.float32)
            windows.append({"story": st, "words": words[w0:w1], "M": M, "Y": Yw})
    if permute:
        # permute the BOLD<->window correspondence in contiguous blocks (brain-specificity null)
        ys = [w["Y"] for w in windows]
        order = BL.block_permute(np.arange(len(windows)).reshape(-1, 1), n_blocks=10, seed=perm_seed).ravel()
        for w, o in zip(windows, order):
            w["Y"] = ys[o][: w["M"].shape[0]] if ys[o].shape[0] >= w["M"].shape[0] else \
                     np.pad(ys[o], ((0, w["M"].shape[0] - ys[o].shape[0]), (0, 0)))
    if limit_windows:
        windows = windows[:limit_windows]

    for epoch in range(epochs):
        rng = np.random.default_rng(seed * 100 + epoch)
        for wi in rng.permutation(len(windows)):
            W = windows[wi]
            wf = word_feats_grad(model, tok, W["words"], layer, device).float()  # (nw, d) grad, fp32 head
            M = torch.tensor(W["M"], device=device)                            # (ntr, nw)
            trf = M @ wf                                                       # (ntr, d) grad
            trf = _zscore_torch(trf)
            fir = _fir_torch(trf)                                              # (ntr, d*4)
            ed = edge_drop
            pred = readout(fir)[ed:-ed]                                        # (ntr-2ed, nvox)
            tgt = torch.tensor(W["Y"], device=device)
            tgt = _zscore_torch(tgt)[ed:-ed]
            loss = BL.infonce_loss(pred, tgt, temp=temp)
            opt.zero_grad(); loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0); opt.step()
    model.eval()
    return model


def eval_unique_r2(model, tok, eval_stories, subject, vox, layer, device, eng1000, n_folds):
    d = L.build_story_data(eval_stories, model, tok, layer, subject=subject, device=device, eng1000=eng1000)
    for s in d:
        d[s]["Y"] = d[s]["Y"][:, vox]
    u = cv_unique_r2(d, eval_stories, n_folds)
    return float(u.mean())


def eval_encoding_r(model, tok, eval_stories, subject, vox, layer, device, eng1000, n_folds):
    """Negi's metric: per-voxel held-out encoding Pearson r (LM features only, ridge, story-CV), mean over vox."""
    from run_lebel_encoding import ridge_r2_per_voxel, story_folds, _pca
    d = L.build_story_data(eval_stories, model, tok, layer, subject=subject, device=device, eng1000=eng1000)
    for s in d:
        d[s]["Y"] = d[s]["Y"][:, vox]
    folds = story_folds(eval_stories, n_folds)
    rs = []
    for te in folds:
        tr = [s for s in eval_stories if s not in te]
        Xtr = np.vstack([d[s]["X"] for s in tr]); Ytr = np.vstack([d[s]["Y"] for s in tr])
        Xte = np.vstack([d[s]["X"] for s in te]); Yte = np.vstack([d[s]["Y"] for s in te])
        Xtr, Xte = _pca(Xtr, Xte, 100)
        # ridge fit, per-voxel held-out Pearson r
        from numpy.linalg import solve
        mx, my = Xtr.mean(0), Ytr.mean(0)
        Xc, Yc = Xtr - mx, Ytr - my
        B = solve(Xc.T @ Xc + 1e3 * np.eye(Xc.shape[1]), Xc.T @ Yc)
        P = (Xte - mx) @ B + my
        from scipy.stats import zscore
        r = (np.nan_to_num(zscore(P, 0)) * np.nan_to_num(zscore(Yte, 0))).mean(0)
        rs.append(r)
    return float(np.mean(np.mean(rs, 0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--subjects", nargs="+", default=["UTS01", "UTS02", "UTS03"])
    ap.add_argument("--n-tune-stories", type=int, default=14)
    ap.add_argument("--n-eval-stories", type=int, default=6)
    ap.add_argument("--reliability-thresh", type=float, default=0.5)
    ap.add_argument("--n-folds", type=int, default=3)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--lr", type=float, default=1e-5)         # gentle full-FT (E017)
    ap.add_argument("--win-words", type=int, default=200)
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--limit-windows", type=int, default=None)
    ap.add_argument("--limit-eval", type=int, default=None)
    ap.add_argument("--arms", nargs="+", default=["b", "c", "d"], help="which tuned arms to run (a=baseline always)")
    ap.add_argument("--verify-lanczos", action="store_true")
    ap.add_argument("--out", default="outputs/E019_negi/results.json")
    args = ap.parse_args()

    if args.verify_lanczos:
        _verify_lanczos(); return

    import torch
    from transformers import AutoConfig
    device = "cuda" if torch.cuda.is_available() else "cpu"
    from run_ppl_alignment_law import load_wikitext_sentences
    _wiki = load_wikitext_sentences(1200)
    ppl_probe = _wiki[:200]                 # held-out ppl probe (a/b/c all measured on THIS)
    genft_corpus = _wiki[200:]              # DISJOINT generic-text corpus for arm (c) FT (no leak)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    nlayers = AutoConfig.from_pretrained(args.model).num_hidden_layers
    layer = VERDICT_LAYER.get(nlayers, max(1, nlayers // 2))
    eng1000 = L._eng1000()
    _, tok = RBL.load_model(args.model, device)
    print(f"E019 faithful-Negi: {args.model} L{layer}, arms a+{args.arms}, lr={args.lr}", flush=True)
    results = {"model": args.model, "layer": layer, "config": vars(args), "subjects": {}}
    t0 = time.time()

    for subj in args.subjects:
        allst = [s for s in L.list_stories(subj) if s != HELDOUT_NC_STORY]
        on_disk = [s for s in allst if (Path(f"data/lebel_ds003020/preprocessed_data/{subj}") / f"{s}.hf5").exists()]
        tune_st = on_disk[:args.n_tune_stories]
        eval_st = on_disk[args.n_tune_stories:args.n_tune_stories + args.n_eval_stories]
        if args.limit_eval:
            eval_st = eval_st[:args.limit_eval]
        if len(eval_st) < 2 or len(tune_st) < 2:
            print(f"[{subj}] SKIP — stories tune {len(tune_st)} eval {len(eval_st)}"); continue
        rel = L.voxel_reliability(L.load_repeats(HELDOUT_NC_STORY, subj))
        vox = np.nonzero(rel > args.reliability_thresh)[0]
        print(f"\n=== {subj}: {len(vox)} NC voxels; tune {len(tune_st)} eval {len(eval_st)} ===", flush=True)

        # arm (a) vanilla
        base, _ = RBL.load_model(args.model, device)
        a_u = eval_unique_r2(base, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
        a_r = eval_encoding_r(base, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
        a_ppl = RBL.eval_perplexity(base, tok, ppl_probe, device)
        del base; torch.cuda.empty_cache()
        print(f"  (a) vanilla: uR2={a_u:+.4f} enc_r={a_r:+.4f} ppl={a_ppl:.1f}", flush=True)

        rows = []
        for seed in args.seeds:
            rec = {"seed": seed, "base_u": a_u, "base_r": a_r, "base_ppl": a_ppl}
            # (b) brain-tuned [reproduce], NO ppl anchor
            if "b" in args.arms:
                RBL.P.set_seed(seed); mb, _ = RBL.load_model(args.model, device)
                mb = negi_tune(mb, tok, tune_st, subj, vox, layer, device, args.epochs, args.lr, seed,
                               win_words=args.win_words, limit_windows=args.limit_windows)
                rec["b_u"] = eval_unique_r2(mb, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
                rec["b_r"] = eval_encoding_r(mb, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
                rec["b_ppl"] = RBL.eval_perplexity(mb, tok, ppl_probe, device)
                del mb; torch.cuda.empty_cache()
            # (d) permuted-brain twin
            if "d" in args.arms:
                RBL.P.set_seed(seed); md, _ = RBL.load_model(args.model, device)
                md = negi_tune(md, tok, tune_st, subj, vox, layer, device, args.epochs, args.lr, seed,
                               win_words=args.win_words, permute=True, perm_seed=1000 + seed,
                               limit_windows=args.limit_windows)
                rec["d_u"] = eval_unique_r2(md, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
                rec["d_r"] = eval_encoding_r(md, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
                del md; torch.cuda.empty_cache()
            # (c) ppl-matched generic-text FT (WikiText CE), early-stop to ~b_ppl
            if "c" in args.arms and "b" in args.arms:
                RBL.P.set_seed(seed); mc, _ = RBL.load_model(args.model, device)
                mc = _genft_to_ppl(mc, tok, genft_corpus, ppl_probe, target_ppl=rec.get("b_ppl", a_ppl),
                                   device=device, lr=args.lr, seed=seed)
                rec["c_u"] = eval_unique_r2(mc, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
                rec["c_r"] = eval_encoding_r(mc, tok, eval_st, subj, vox, layer, device, eng1000, args.n_folds)
                rec["c_ppl"] = RBL.eval_perplexity(mc, tok, ppl_probe, device)
                del mc; torch.cuda.empty_cache()
            # contrasts (encoding-r primary = Negi metric; uR2 secondary = E006 anti-confound)
            if "b" in args.arms:
                rec["gain_r_b_minus_a"] = rec["b_r"] - a_r
                rec["gain_u_b_minus_a"] = rec["b_u"] - a_u
                if "d" in args.arms:
                    rec["spec_r_b_minus_d"] = rec["b_r"] - rec["d_r"]
                    rec["spec_u_b_minus_d"] = rec["b_u"] - rec["d_u"]
                if "c" in args.arms:
                    rec["survive_r_b_minus_c"] = rec["b_r"] - rec["c_r"]
                    rec["bpb_match_ratio"] = rec.get("c_ppl", float("nan")) / rec.get("b_ppl", float("nan"))
            rows.append(rec)
            print(f"  [s{seed}] " + " ".join(f"{k}={rec[k]:+.4f}" for k in rec if isinstance(rec[k], float)
                                              and k.startswith(("gain", "spec", "survive"))), flush=True)
        results["subjects"][subj] = {"n_vox": int(len(vox)), "tune": tune_st, "eval": eval_st, "rows": rows}
        Path(args.out).write_text(json.dumps(results, indent=2))

    # summary
    def agg(key):
        vals = [r[key] for s in results["subjects"] for r in results["subjects"][s]["rows"] if key in r]
        return (round(float(np.mean(vals)), 4), round(float(np.std(vals, ddof=1)), 4), len(vals)) if vals else None
    results["summary"] = {k: agg(k) for k in ["gain_r_b_minus_a", "gain_u_b_minus_a", "spec_r_b_minus_d",
                                              "spec_u_b_minus_d", "survive_r_b_minus_c", "bpb_match_ratio"]}
    Path(args.out).write_text(json.dumps(results, indent=2))
    print(f"\n=== E019 SUMMARY ({time.time()-t0:.0f}s) ===")
    for k, v in results["summary"].items():
        print(f"  {k}: mean={v[0] if v else None} sd={v[1] if v else None} n={v[2] if v else None}")
    print(f"  wrote {args.out}")


def _genft_to_ppl(model, tok, ft_texts, ppl_probe, target_ppl, device, lr, seed, max_steps=200, bs=8):
    """Generic-text CE fine-tune on ft_texts (DISJOINT from ppl_probe), early-stopped when the held-out
    ppl_probe perplexity reaches ~target_ppl (arm b's). Arm (c) — matched-ppl by construction, no leak."""
    import torch
    RBL.freeze_input_embeddings(model); model.train()
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lr)
    texts = ft_texts
    rng = np.random.default_rng(seed)
    step = 0
    while step < max_steps:
        for start in range(0, len(texts), bs):
            batch = [texts[i] for i in rng.permutation(len(texts))[:bs]]
            enc = tok(batch, return_tensors="pt", padding=True, truncation=True, max_length=64).to(device)
            labels = enc["input_ids"].clone(); labels[enc["attention_mask"] == 0] = -100
            loss = model(**enc, labels=labels).loss
            opt.zero_grad(); loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0); opt.step()
            step += 1
            if step % 20 == 0:
                model.eval()
                cur = RBL.eval_perplexity(model, tok, ppl_probe, device); model.train()
                if cur <= target_ppl:
                    model.eval(); return model
            if step >= max_steps:
                break
    model.eval(); return model


def _verify_lanczos():
    """Verify the fixed Lanczos matrix == lanczosinterp2D on real story timing + random feats."""
    from ridge_utils.interpdata import lanczosinterp2D
    ws = L.get_wordseqs(["wheretheressmoke"])["wheretheressmoke"]
    wt, trt = np.asarray(ws.data_times, float), np.asarray(ws.tr_times, float)
    nw = len(wt); rng = np.random.default_rng(0)
    feats = rng.standard_normal((nw, 16)).astype(np.float32)
    M = lanczos_matrix(wt, trt)
    a = M @ feats
    b = lanczosinterp2D(feats, wt, trt, window=3)
    err = float(np.abs(a - b).max())
    print(f"Lanczos matrix vs lanczosinterp2D: max|Δ|={err:.2e}  shapes M{M.shape} a{a.shape} b{b.shape}")
    print("PASS" if err < 1e-4 else "FAIL")


if __name__ == "__main__":
    main()
