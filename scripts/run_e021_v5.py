#!/usr/bin/env python
"""E021 v5 — the panel's decisive controls, run at the SAME 10 seeds as v4.

Both opus panels killed the v4 "positive" with one structural gap: no control was
simultaneously (real-difficulty OR RT-marginal) AND temporally smooth AND non-cognitive.
v5 fills that cell with three controls (see e021_targets_v5.py):
  shape_matched   — phase-randomized residual: residual's FULL autocorrelation + marginal,
                    zero content. RT beating this = content; RT tying it = shape artifact.
  surp_smoothed   — Qwen surprisal EWMA-smoothed to RT's lag-1 AC: real-difficulty + smooth,
                    non-cognitive. RT beating this = not mere smoothness.
  rt_hat_nuisance — nonlinear (GBM) out-of-fold reconstruction of RT from nuisances only:
                    RT's nuisance-explainable component. RT beating this = beyond freq/len/surp.

Reuses the v4/v3 harness verbatim (frozen-probe AULC, all fixes, per-seed aux-MSE). Runs
arms [residual, raw, shape_matched, rt_hat_nuisance, surp_smoothed] so residual/raw are
re-measured at the same seeds (paired with the new controls AND a reproduction check vs v4).
Sharded by seed; combine with --mode combine (merges v4 + v5 arms, recomputes the verdict).

Usage:
  CUDA_VISIBLE_DEVICES=1 HF_HOME=... uv run python scripts/run_e021_v5.py --mode arms --seeds 0 1 2 3 4 --tag g1
  CUDA_VISIBLE_DEVICES=2 ...                                              --seeds 5 6 7 8 9 --tag g2
  uv run python scripts/run_e021_v5.py --mode combine
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import e021_targets_v5 as T
from run_e021_arms import (
    BASE, DEVICE, OUT, LAMBDA_AUX, BYWORD, TRAIN_ITEMS,
    load_ns_stories, load_wiki_tokens,
)
from run_e021_v3 import frozen_probe_aulc, paired_ci
from run_e021_v4 import stage_a_aux_arm, NONCOG_CONTROLS as V4_NONCOG

V5_ARMS = ["residual", "raw", "shape_matched", "rt_hat_nuisance", "surp_smoothed"]
# the panel-requested non-cognitive controls (added to the v4 non-cog set for the trend)
V5_NONCOG = ["shape_matched", "surp_smoothed", "rt_hat_nuisance"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["arms", "combine"], required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(10)))
    ap.add_argument("--tag", default="all")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    if args.mode == "combine":
        return combine()

    tokenizer = AutoTokenizer.from_pretrained(BASE)
    tokenizer.pad_token = tokenizer.eos_token
    stories = load_ns_stories()
    wiki_train, wiki_eval = load_wiki_tokens(tokenizer)
    m0 = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32)
    d, vocab = m0.config.hidden_size, m0.config.vocab_size
    base_wte = m0.state_dict()["transformer.wte.weight"].detach().clone().to(DEVICE)
    del m0
    print(f"[{args.tag}] seeds={args.seeds} dev={os.environ.get('CUDA_VISIBLE_DEVICES','?')}", flush=True)

    rows = []
    for seed in args.seeds:
        targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=seed)
        if seed == args.seeds[0] and args.tag in ("all", "g1"):
            targ.to_csv(f"{OUT}/aux_targets_v5.csv", index=False)
        arm_target = {a: ({(r.item, r.zone): getattr(r, a) for r in targ.itertuples()}, LAMBDA_AUX)
                      for a in V5_ARMS}
        for arm in V5_ARMS:
            tmap, lam = arm_target[arm]
            state, a_logs, n_aux, aux_mse = stage_a_aux_arm(tmap, lam, tokenizer, stories, seed)
            aulc, ppls = frozen_probe_aulc(state, base_wte, wiki_train, wiki_eval, seed, d, vocab)
            del state
            torch.cuda.empty_cache() if DEVICE == "cuda" else None
            rows.append({"arm": arm, "seed": seed, "aulc": aulc, "aux_mse": aux_mse,
                         "ppls": ppls, "n_aux_examples": n_aux})
            print(f"[{args.tag} seed {seed}] {arm:16s} AULC={aulc:.2f}  aux_mse={aux_mse:.4f}", flush=True)

    path = f"{OUT}/arms_v5_shard_{args.tag}.json"
    json.dump({"mode": "arms_shard_v5", "tag": args.tag, "rows": rows}, open(path, "w"), indent=2)
    print(f"[{args.tag}] wrote {path} ({len(rows)} arm-runs)")


def combine():
    # v5 shards (new controls + re-measured residual/raw)
    v5_rows = []
    for s in sorted(glob.glob(f"{OUT}/arms_v5_shard_*.json")):
        v5_rows += json.load(open(s))["rows"]
    # v4 shards (the original arms incl. the non-cog learnability controls)
    v4_rows = []
    for s in sorted(glob.glob(f"{OUT}/arms_v4_shard_*.json")):
        v4_rows += json.load(open(s))["rows"]

    seen = {}
    # v5 residual/raw OVERRIDE v4's (same harness, re-measured at same seeds; use the v5 batch
    # so the new controls are paired against residual/raw from the SAME run)
    for r in v4_rows:
        seen[(r["arm"], r["seed"])] = r
    for r in v5_rows:
        seen[(r["arm"], r["seed"])] = r
    rows = list(seen.values())
    seeds = sorted({r["seed"] for r in rows})
    n = len(seeds)
    arms = sorted({r["arm"] for r in rows})

    def series(arm, key):
        dd = {r["seed"]: r[key] for r in rows if r["arm"] == arm and key in r}
        return [dd[s] for s in seeds if s in dd]

    aulc = {a: series(a, "aulc") for a in arms}
    auxmse = {a: series(a, "aux_mse") for a in arms}
    means = {a: float(np.mean(aulc[a])) for a in arms}
    sems = {a: float(np.std(aulc[a], ddof=1) / math.sqrt(len(aulc[a]))) for a in arms}
    auxmse_mean = {a: (float(np.nanmean(auxmse[a])) if auxmse[a] else float("nan")) for a in arms}

    def contrast(x, y):
        if not aulc[x] or not aulc[y]:
            return None
        m, lo, hi = paired_ci(aulc[x], aulc[y])
        return {"mean": m, "ci": [lo, hi], "excludes_0": bool(hi < 0 or lo > 0),
                "favors_x_lower": bool(hi < 0)}

    # the decisive contrasts: residual/raw vs each panel control
    decisive = {}
    for test in ["residual", "raw"]:
        for ctrl in ["shape_matched", "surp_smoothed", "rt_hat_nuisance"]:
            decisive[f"{test}_minus_{ctrl}"] = contrast(test, ctrl)
    # per-cap decomposition of residual - shape_matched (counter-argument's cap-3000 worry)
    caps = [100, 300, 1000, 3000]
    def cap_series(arm, cap):
        dd = {r["seed"]: r["ppls"][str(cap)] for r in rows if r["arm"] == arm and "ppls" in r}
        return [dd[s] for s in seeds if s in dd]
    per_cap = {}
    for ctrl in ["shape_matched", "surp_smoothed", "rt_hat_nuisance"]:
        per_cap[f"residual_minus_{ctrl}"] = {}
        for cap in caps:
            a = cap_series("residual", cap); b = cap_series(ctrl, cap)
            if a and b:
                m, lo, hi = paired_ci(a, b)
                per_cap[f"residual_minus_{ctrl}"][cap] = {"mean": m, "ci": [lo, hi], "excludes_0": bool(hi < 0 or lo > 0)}

    # verdict: a CLEAN POSITIVE needs residual to beat shape_matched AND surp_smoothed AND
    # rt_hat_nuisance (CIs exclude 0, residual lower). Otherwise the v4 edge was shape/
    # smoothness/nuisance, i.e. NULL on cognition.
    beats = {c: (decisive[f"residual_minus_{c}"] and decisive[f"residual_minus_{c}"]["favors_x_lower"])
             for c in ["shape_matched", "surp_smoothed", "rt_hat_nuisance"]}
    ties = {c: (decisive[f"residual_minus_{c}"] and not decisive[f"residual_minus_{c}"]["excludes_0"])
            for c in ["shape_matched", "surp_smoothed", "rt_hat_nuisance"]}
    if all(beats.values()):
        verdict = ("CLEAN POSITIVE — RT-residual beats the phase-randomized shape control, the "
                   "smoothed-real-difficulty control, AND the nonlinear-nuisance reconstruction "
                   "(all CIs exclude 0, residual lower). The advantage is NOT explained by signal "
                   "shape, smoothness of a real-difficulty signal, or nonlinear nuisance content. "
                   "First real evidence of RT-specific trainable structure. ESCALATE: Erfan; flip nothing.")
    elif any(ties.values()):
        tied = [c for c, v in ties.items() if v]
        verdict = (f"CLEAN NULL on cognition — RT-residual TIES at least one neutralizing control "
                   f"({', '.join(tied)}): the v4 below-trend edge is explained by signal shape / "
                   f"smoothness-of-real-difficulty / nonlinear nuisance, NOT cognition-specific content. "
                   f"raw~residual already killed surprisal-orthogonality. The defensible claim is the "
                   f"NARROW negative: surprisal-residualization buys nothing AND the RT edge over the "
                   f"v4 controls is a signal-shape regularization effect, not cognition.")
    else:
        verdict = ("MIXED — residual beats some neutralizing controls but the picture is not uniform; "
                   "report each contrast and let Erfan adjudicate.")

    out = {"mode": "v5_combined", "n_seeds": n, "seeds": seeds, "arms": arms,
           "arm_aulc_mean": means, "arm_aulc_sem": sems, "arm_aux_mse_mean": auxmse_mean,
           "arm_aulc_per_seed": aulc, "arm_aux_mse_per_seed": auxmse,
           "decisive_contrasts": decisive, "per_cap_residual_minus_control": per_cap,
           "residual_beats": beats, "residual_ties": ties, "verdict": verdict}
    json.dump(out, open(f"{OUT}/arms_v5_results.json", "w"), indent=2)

    print(f"\n=== E021 v5 (panel controls)  n={n} ===")
    print(f"{'arm':18s} {'AULC mean±sem':>20s} {'aux_mse':>10s}")
    for a in arms:
        am = f"{auxmse_mean[a]:.4f}" if not math.isnan(auxmse_mean[a]) else "  n/a"
        print(f"  {a:16s} {means[a]:8.2f} ± {sems[a]:5.2f}   {am:>8s}")
    print("\n-- DECISIVE contrasts (residual/raw - panel control; lower=better; *** = CI excludes 0) --")
    for k, v in decisive.items():
        if v is None:
            continue
        flag = "***" if v["excludes_0"] else "TIE"
        print(f"  {k:34s} {v['mean']:+8.2f}  CI[{v['ci'][0]:+8.2f},{v['ci'][1]:+8.2f}] {flag}")
    print("\n-- per-cap residual - shape_matched (cap-3000 dominance check) --")
    for ctrl, caps_d in per_cap.items():
        if ctrl != "residual_minus_shape_matched":
            continue
        for cap, v in caps_d.items():
            print(f"  cap {cap:5d}: {v['mean']:+8.2f}  CI[{v['ci'][0]:+8.2f},{v['ci'][1]:+8.2f}]  {'***' if v['excludes_0'] else 'TIE'}")
    print(f"\nVERDICT: {verdict}")
    print(f"Wrote {OUT}/arms_v5_results.json")


if __name__ == "__main__":
    main()
