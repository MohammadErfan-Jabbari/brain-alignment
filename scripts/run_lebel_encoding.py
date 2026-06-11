#!/usr/bin/env python3
"""E006 — LeBel UTS03 voxelwise A2-feasibility (powered substrate validation).

Does a TRAINED LM's middle-layer representation predict UTS03 BOLD *beyond
nuisance* (low-level phone-tier rates/durations/length/log-freq + eng1000 static
lexical-semantic), under contiguous STORY-level CV, materially above an UNTRAINED
same-arch control? The E002/A2 question at voxel scale — the kill-gate before the
TR-level lever re-test (E007).

Design locked in docs/experiments/E006_*.md (oracle HOLD resolved). Load-bearing:
  * verdict = TRAINED − UNTRAINED gap (not trained absolute; untrained can score
    positive on naturalistic timeseries via rate structure). Identical nuisance both arms.
  * voxel selection on the HELD-OUT repeated story (wheretheressmoke 10 repeats) ->
    no double-dipping; ridge restricted to NC-reliable voxels (also cuts compute).
  * unique R^2 = R^2([nuisance, LM]) - R^2([nuisance]), per voxel, story-grouped CV.
  * EMPIRICAL E007-LEVER MDE from fold-level variance of unique R^2 on NC voxels —
    this licenses (or refuses) E007: if MDE > +0.003 even here, the lever line is
    structurally underpowered (stop it, don't build the TR loop).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lebel_adapter as L  # noqa: E402

# A pinned story set (alphabetical first N with both response + textgrid), excluding
# the held-out repeated noise-ceiling story. Pinned for reproducibility.
HELDOUT_NC_STORY = "wheretheressmoke"


def ridge_r2_per_voxel(Xtr, Ytr, Xte, Yte, alphas=(1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7)):
    """Standardize X (fit on train), RidgeCV (one GCV alpha across voxels), per-voxel R^2 on test."""
    from sklearn.linear_model import RidgeCV
    from sklearn.preprocessing import StandardScaler
    xs = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = xs.transform(Xtr), xs.transform(Xte)
    ym = Ytr.mean(0, keepdims=True)
    model = RidgeCV(alphas=list(alphas))
    model.fit(Xtr_s, Ytr - ym)
    pred = model.predict(Xte_s) + ym
    ss_res = ((Yte - pred) ** 2).sum(0)
    ss_tot = ((Yte - Yte.mean(0, keepdims=True)) ** 2).sum(0)
    return 1.0 - ss_res / np.clip(ss_tot, 1e-8, None)        # (n_vox,)


def story_folds(stories, n_folds):
    """Contiguous story-grouped folds (whole stories held out)."""
    stories = list(stories)
    bounds = np.linspace(0, len(stories), n_folds + 1).astype(int)
    return [stories[bounds[i]:bounds[i + 1]] for i in range(n_folds)]


def _pca(Xtr, Xte, k):
    """Capacity-fair PCA, fit on TRAIN only (the L004/E002 fix for p>>n)."""
    if Xtr.shape[1] <= k:
        return Xtr, Xte
    from sklearn.decomposition import PCA
    p = PCA(n_components=min(k, Xtr.shape[0] - 1, Xtr.shape[1])).fit(Xtr)
    return p.transform(Xtr), p.transform(Xte)


def cv_unique_r2(data, stories, n_folds, pca_rank=100):
    """Per-fold per-voxel unique R^2 = R^2([low, PCA(eng), PCA(LM)]) - R^2([low, PCA(eng)]);
    story-grouped CV with capacity-fair PCA on the LM and eng1000 blocks (equal rank, train-fit;
    low-level kept raw). Returns (n_folds, n_vox)."""
    folds = story_folds(stories, n_folds)
    out = []
    for test in folds:
        train = [s for s in stories if s not in test]
        def cat(key, ss): return np.vstack([data[s][key] for s in ss])
        low_tr, low_te = cat("N_low", train), cat("N_low", test)
        Etr, Ete = _pca(cat("N_eng", train), cat("N_eng", test), pca_rank)
        Xtr, Xte = _pca(cat("X", train), cat("X", test), pca_rank)   # capacity-fair (same rank)
        Ytr, Yte = cat("Y", train), cat("Y", test)
        nuis_tr = np.hstack([low_tr, Etr]); nuis_te = np.hstack([low_te, Ete])
        full_tr = np.hstack([nuis_tr, Xtr]); full_te = np.hstack([nuis_te, Xte])
        r2_n = ridge_r2_per_voxel(nuis_tr, Ytr, nuis_te, Yte)
        r2_f = ridge_r2_per_voxel(full_tr, Ytr, full_te, Yte)
        out.append(r2_f - r2_n)
    return np.array(out)                                     # (n_folds, n_vox)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--subject", default="UTS03")
    ap.add_argument("--n-stories", type=int, default=12)
    ap.add_argument("--untrained-seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--reliability-thresh", type=float, default=0.5)
    ap.add_argument("--n-folds", type=int, default=4)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    device = L.pick_device() if hasattr(L, "pick_device") else ("cuda" if __import__("torch").cuda.is_available() else "cpu")

    allst = [s for s in L.list_stories(args.subject) if s != HELDOUT_NC_STORY]
    stories = allst[:args.n_stories]
    layer = L.verdict_layer(AutoConfig.from_pretrained(args.model).num_hidden_layers) \
        if hasattr(L, "verdict_layer") else None
    # verdict_layer takes a model; resolve via num layers map
    nlayers = AutoConfig.from_pretrained(args.model).num_hidden_layers
    layer = {12: 7, 24: 12, 28: 14}.get(nlayers, max(1, nlayers // 2))
    print(f"{args.model}: L{layer}/{nlayers}; {len(stories)} stories: {stories}")

    # --- NC-reliable voxel selection on the HELD-OUT repeated story (no double-dip) ---
    rel = L.voxel_reliability(L.load_repeats(HELDOUT_NC_STORY, args.subject))
    vox = np.nonzero(rel > args.reliability_thresh)[0]
    print(f"NC-reliable voxels (rel>{args.reliability_thresh}): {len(vox)}/{len(rel)}  "
          f"(mean rel {rel[vox].mean():.3f})")

    eng1000 = L._eng1000()
    tok = AutoTokenizer.from_pretrained(args.model); tok.pad_token = tok.pad_token or tok.eos_token

    def build(model):
        d = L.build_story_data(stories, model, tok, layer, subject=args.subject,
                               device=device, eng1000=eng1000)
        for s in d:                                          # restrict Y to reliable voxels
            d[s]["Y"] = d[s]["Y"][:, vox]
        return d

    results = {"model": args.model, "layer": layer, "subject": args.subject, "stories": stories,
               "n_reliable_vox": int(len(vox)), "reliability_thresh": args.reliability_thresh,
               "config": vars(args)}
    t0 = time.time()

    print("== trained ==", flush=True)
    mt = AutoModelForCausalLM.from_pretrained(args.model).to(device).eval()
    dtr = build(mt); del mt; torch.cuda.empty_cache()
    u_trained = cv_unique_r2(dtr, stories, args.n_folds)     # (folds, vox)
    del dtr; torch.cuda.empty_cache()
    print(f"  trained unique R^2 (mean over folds,vox) = {u_trained.mean():+.4f}", flush=True)

    u_untr = []
    for s in args.untrained_seeds:
        print(f"== untrained seed {s} ==", flush=True)
        L.set_seed(s) if hasattr(L, "set_seed") else __import__("torch").manual_seed(s)
        cfg = AutoConfig.from_pretrained(args.model); __import__("torch").manual_seed(s)
        mu = AutoModelForCausalLM.from_config(cfg).to(device).eval()
        du = build(mu); del mu; torch.cuda.empty_cache()
        u = cv_unique_r2(du, stories, args.n_folds); del du; torch.cuda.empty_cache()
        u_untr.append(u)
        print(f"  untrained s{s} unique R^2 = {u.mean():+.4f}", flush=True)
    u_untr = np.array(u_untr)                                # (seeds, folds, vox)

    # --- aggregate: trained − untrained gap on reliable voxels ---
    trained_vox = u_trained.mean(0)                          # (vox,) mean over folds
    untr_vox = u_untr.mean((0, 1))                           # (vox,) mean over seeds,folds
    gap_vox = trained_vox - untr_vox
    # bootstrap CI of the mean gap over voxels
    rng = np.random.default_rng(0)
    bs = rng.choice(gap_vox, size=(10000, len(gap_vox)), replace=True).mean(1)
    gap_mean, gap_lo, gap_hi = float(gap_vox.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
    # E007-lever MDE: fold-level variance of the unique-R^2 *mean over voxels* (the statistic E007 will track)
    trained_fold_means = u_trained.mean(1)                   # (folds,)
    untr_fold_means = u_untr.mean(2).reshape(-1)             # (seeds*folds,)
    sd_fold = float(np.std(np.concatenate([trained_fold_means, untr_fold_means]), ddof=1))
    se = sd_fold / np.sqrt(args.n_folds)
    mde80 = float(2.49 * se)                                 # ~80% power, two-sided 0.05 (z .975 + z .80)

    results.update({
        "trained_unique_r2_mean": float(trained_vox.mean()),
        "untrained_unique_r2_mean": float(untr_vox.mean()),
        "gap_mean": gap_mean, "gap_ci": [gap_lo, gap_hi],
        "frac_voxels_gap_positive": float((gap_vox > 0).mean()),
        "trained_fold_means": trained_fold_means.tolist(),
        "untrained_fold_means": untr_fold_means.tolist(),
        "fold_sd": sd_fold, "E007_lever_mde80": mde80,
        "elapsed_s": time.time() - t0,
    })
    out = args.out or f"outputs/E006_lebel_{args.model.replace('/', '_')}.json"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(results, indent=2))
    print(f"\n=== E006 SUMMARY {args.model} ({results['elapsed_s']:.0f}s) ===")
    print(f"  trained unique R^2 = {trained_vox.mean():+.4f} | untrained = {untr_vox.mean():+.4f}")
    print(f"  GAP = {gap_mean:+.4f}  CI[{gap_lo:+.4f},{gap_hi:+.4f}]  ({100*results['frac_voxels_gap_positive']:.0f}% voxels positive)")
    print(f"  E007-lever MDE(80%) = {mde80:+.4f}  -> {'CAN' if mde80 < 0.003 else 'CANNOT'} resolve a +0.003 lever")
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
