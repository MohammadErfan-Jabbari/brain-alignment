#!/usr/bin/env python3
"""E010 — the averaging DOSE-RESPONSE: does the apparent brain-specific gain grow with
the number of subjects averaged into the fMRI target? (earns/refutes the "averaging
manufactures apparent brain-specificity" claim — S8 manuscript panel, counter-argument #1.)

Mechanism under test (L016): Y_i = g + eps_i (g = shared stimulus-evoked response, eps_i
idiosyncratic+noise indep across subjects). Averaging k subjects -> Y_k = g + (1/k)Σeps,
raising the achievable noise ceiling NC_k = NC/(NC + (1-NC)/k). If the apparent
brain-specific gap (kd_brain - kd_brain_permuted, held-out unique R^2) GROWS monotonically
with k from ~0 at k=1 toward the +0.008 seen at k=5, the specificity is an averaging
artifact, not per-person alignment.

For each k in K: build the k-averaged target over the first k of a fixed UID order (nested),
KD-tune (Qwen1.5B->0.5B, LoRA) toward it + its block-permuted twin, score held-out unique R^2,
several seeds. Reports gap(k) vs the noise-ceiling prediction.

Run: export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
     CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_averaging_doseresponse.py --k 1 2 3 5 9 --seeds 0 1 2 3
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P
import brain_loss as BL
import run_brain_lever as RBL
from data_adapters import load_tuckute

# fixed UID order (nested subsets); all 9 usable (853 excluded, incomplete ROI). The
# first 5 are E005's averaged set (minus 853) so k=5 ~ E005's target.
UID_ORDER = [848, 865, 875, 876, 797, 837, 841, 856, 880]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--kd-teacher", default="Qwen/Qwen2.5-1.5B")
    ap.add_argument("--k", nargs="+", type=int, default=[1, 2, 3, 5, 9])
    ap.add_argument("--random-subsets", type=int, default=0,
                    help="if >0: for each k, draw N RANDOM size-k subsets (decouples subject-count from "
                         "subject-identity — the socratic-capstone fix for E010's nested confound). "
                         "0 = nested subsets (legacy E010).")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3])
    ap.add_argument("--lam", type=float, default=10.0)
    ap.add_argument("--n-train", type=int, default=800)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--limit-train", type=int, default=None)
    ap.add_argument("--out", default="outputs/E010_averaging_doseresponse.json")
    args = ap.parse_args()

    import torch
    device = P.pick_device()

    # per-UID targets (texts identical across UIDs)
    per_uid = {}
    texts = None
    for uid in UID_ORDER:
        t_u, Y_u, _ = load_tuckute(args.data_dir, uids=(uid,))
        if texts is None:
            texts = t_u
        else:
            assert t_u == texts
        per_uid[uid] = Y_u
    n = len(texts)
    nc = RBL.matched_nc(args.data_dir)
    n_tr = min(args.n_train, n - 100)
    tr, ev = np.arange(n_tr), np.arange(n_tr, n)
    if args.limit_train:
        tr = tr[:args.limit_train]
    texts_tr = [texts[i] for i in tr]
    texts_ev = [texts[i] for i in ev]

    teacher = RBL.load_model(args.kd_teacher, device)[0].eval()
    for p in teacher.parameters():
        p.requires_grad_(False)
    base, tok = RBL.load_model(args.model, device)
    layer = RBL.verdict_layer(base)
    Z_ev = P.scalar_nuisance(texts_ev, tok)
    S_ev = P.static_embedding_features(base, tok, texts_ev, device)
    print(f"{args.model}: L{layer}; NC={nc:.3f}; k-values={args.k}; seeds={args.seeds}; n_train={len(tr)}")

    # build subsets per k: nested (legacy) or N random size-k subsets (decouples count from identity)
    import math as _math
    subsets_by_k = {}
    rng = np.random.default_rng(20260612)
    for k in args.k:
        if args.random_subsets <= 0:
            subsets_by_k[k] = [tuple(UID_ORDER[:k])]
        else:
            n_poss = _math.comb(len(UID_ORDER), k)
            want = min(args.random_subsets, n_poss)
            seen, subs = set(), []
            while len(subs) < want:
                s = tuple(sorted(rng.choice(UID_ORDER, size=k, replace=False).tolist()))
                if s not in seen:
                    seen.add(s); subs.append(s)
            subsets_by_k[k] = subs

    results = {"model": args.model, "nc": nc, "uid_order": UID_ORDER, "config": vars(args),
               "subsets_by_k": {k: [list(s) for s in v] for k, v in subsets_by_k.items()}, "raw": []}
    t0 = time.time()
    for k in args.k:
        nc_k = nc / (nc + (1 - nc) / k)
        for si, uids_k in enumerate(subsets_by_k[k]):
            Yk = np.mean([per_uid[u] for u in uids_k], axis=0)   # k-averaged target (this subset)
            Yk_tr, Yk_ev = Yk[tr], Yk[ev]
            has875 = 875 in uids_k
            for seed in args.seeds:
                for arm in ("mse", "mse_perm"):
                    P.set_seed(seed)
                    m, _ = RBL.load_model(args.model, device)
                    Yt = Yk_tr if arm == "mse" else BL.block_permute(Yk_tr, n_blocks=10, seed=1000 + k * 17 + si * 7 + seed)
                    m = RBL.brain_tune(m, tok, texts_tr, Yt, "mse", args.lam, 1.0, layer, device,
                                       args.epochs, args.lr, args.batch_size, seed,
                                       use_lora=True, model_name=args.model, lora_r=16, teacher=teacher)
                    uR2, _ = RBL.score_unique_r2(m, tok, texts_ev, Yk_ev, Z_ev, S_ev, layer, device)
                    results["raw"].append({"k": k, "subset": si, "uids": list(uids_k), "has875": has875,
                                           "seed": seed, "arm": arm, "unique_r2": uR2, "nc_k_pred": nc_k})
                    print(f"  [k={k} sub{si}{'*' if has875 else ' '} {arm:9s} s{seed}] uR2={uR2:+.4f} (ceil {nc_k:.3f})", flush=True)
                    del m
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()

    Path(args.out).write_text(json.dumps(results, indent=2))
    # ---- summary: gap(k) = mean_seed[ uR2(mse) - uR2(mse_perm) ] ----
    print(f"\n=== AVERAGING DOSE-RESPONSE (elapsed {time.time()-t0:.0f}s; "
          f"{'RANDOM subsets' if args.random_subsets>0 else 'nested'}) ===")
    from collections import defaultdict
    bycell = defaultdict(dict)   # (k,subset,seed) -> arm -> uR2
    has875 = {}
    for r in results["raw"]:
        bycell[(r["k"], r["subset"], r["seed"])][r["arm"]] = r["unique_r2"]
        has875[(r["k"], r["subset"])] = r["has875"]
    print(f"{'k':>3s} {'gap mean':>10s} {'sd':>8s} {'n+':>6s} {'875-in':>9s} {'875-out':>9s} {'ceil':>6s}")
    for k in args.k:
        cells = [(ss, sd_) for (kk, ss, sd_) in bycell if kk == k]
        gaps = [bycell[(k, ss, sd_)]["mse"] - bycell[(k, ss, sd_)]["mse_perm"] for (ss, sd_) in cells
                if "mse" in bycell[(k, ss, sd_)] and "mse_perm" in bycell[(k, ss, sd_)]]
        g_in = [bycell[(k, ss, sd_)]["mse"] - bycell[(k, ss, sd_)]["mse_perm"] for (ss, sd_) in cells if has875.get((k, ss))]
        g_out = [bycell[(k, ss, sd_)]["mse"] - bycell[(k, ss, sd_)]["mse_perm"] for (ss, sd_) in cells if not has875.get((k, ss))]
        nc_k = nc / (nc + (1 - nc) / k)
        mi = f"{np.mean(g_in):+.4f}" if g_in else "   --   "
        mo = f"{np.mean(g_out):+.4f}" if g_out else "   --   "
        print(f"{k:>3d} {np.mean(gaps):>+10.5f} {float(np.std(gaps)):>8.5f} {sum(1 for g in gaps if g>0):>3d}/{len(gaps):<2d} {mi:>9s} {mo:>9s} {nc_k:>6.3f}")
    print("READ: if AVERAGING drives the gap, it rises with k for BOTH 875-in and 875-out subsets.")
    print("      if it's the 875 OUTLIER, 875-out subsets stay ~0 while 875-in subsets carry it.")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
