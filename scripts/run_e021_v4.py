#!/usr/bin/env python
"""E021 v4 — learnability-matched adjudication at n>=10 (resolve the n=3 inconclusive).

Same locked, CLEAN design as run_e021_v3.py (frozen-trunk linear-probe AULC,
lower=better; all v3 Codex fixes 1-6 kept). v4 adds the two fixes that convert
the v3 "inconclusive at n=3" into a definitive verdict:

  POWER  — >= 10 paired seeds (default 10). Every contrast recomputed at n>=10.
  LEARNABILITY-MATCHED ADJUDICATION (the crux) — as a COVARIATE analysis, not a
    single matched arm. Across the NON-cognitive word-aligned control arms we now
    span a learnability range:
        logfreq, wlen, surp_other_lm (Qwen2.5-0.5B surprisal), permuted, random_struct
    For EVERY arm we record per-seed final aux-MSE (the learnability proxy)
    alongside the frozen-probe AULC. The decisive test (done in combine, below):
    regress probe-AULC on aux-MSE across the non-cognitive arms (the learnability
    trend), then test whether residual & raw fall significantly BELOW that trend
    (better AULC than their learnability predicts). Below-trend with CI excluding
    0 = genuine RT/cognition-specific content. On-trend = the residual advantage
    is just learnability = clean NULL.

Also re-confirms G2 (mode g2v2) once.

This script runs ONE shard of seeds (so seeds can be sharded across GPUs) and
writes outputs/e021/arms_v4_shard_<tag>.json. Combine all shards with --mode combine.

Writes NEW filenames (arms_v4_*); never touches v2/v3.

Usage (sharded across GPUs):
  CUDA_VISIBLE_DEVICES=0 HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_v4.py --mode arms --seeds 0 1 2 3 --tag g0
  CUDA_VISIBLE_DEVICES=1 ... --seeds 4 5 6 --tag g1
  CUDA_VISIBLE_DEVICES=2 ... --seeds 7 8 9 --tag g2
  # then:
  uv run python scripts/run_e021_v4.py --mode combine
  # G2 re-confirm:
  CUDA_VISIBLE_DEVICES=0 ... --mode g2v2 --seeds 0 1 2
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os

import numpy as np
import torch
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer

import e021_targets_v4 as T
# REUSE data prep + constants exactly from the original harness.
from run_e021_arms import (
    BASE, DEVICE, OUT, MAX_LEN, LAMBDA_AUX, CAPS, BYWORD, TRAIN_ITEMS,
    STAGE_A_LR, STAGE_A_BATCH, STAGE_A_STEPS,
    load_ns_stories, build_aux_batches, load_wiki_tokens,
)
# REUSE the clean v3 frozen-probe machinery verbatim (FIX 4 identical probe init,
# eval, AULC). Only Stage-A is re-implemented here to also return the aux-MSE.
from run_e021_v3 import (
    frozen_probe_aulc, fresh_probe, train_frozen_probe, eval_probe_ppl,
    stage_a_headstart, paired_ci,
)

ARMS = ["baseline", "raw", "residual", "permuted", "random_struct",
        "logfreq", "wlen", "surp_other_lm"]
# the non-cognitive word-aligned controls that define the learnability trend
NONCOG_CONTROLS = ["logfreq", "wlen", "surp_other_lm", "permuted", "random_struct"]


# ===========================================================================
# Stage A — FIXED (pad labels masked; trunk seeded) + returns final aux-MSE
# ===========================================================================
def stage_a_fixed_mse(model, tokenizer, aux_examples, lambda_aux, seed):
    """Identical to run_e021_v3.stage_a_fixed (FIX 1 pad-mask, FIX 5 torch seed,
    deterministic head init, matched budget) but ALSO returns the converged
    aux-MSE: after training, freeze the trunk + head and compute the mean MSE of
    the trained aux head over ALL aux examples (the learnability proxy). For the
    baseline arm (lambda=0) the aux head never gets gradient, so its aux-MSE is
    meaningless and recorded as NaN."""
    torch.manual_seed(seed)
    model.train()
    d = model.config.hidden_size
    aux_head = nn.Linear(d, 1).to(DEVICE)
    g = torch.Generator(device="cpu").manual_seed(seed)
    with torch.no_grad():
        aux_head.weight.copy_(torch.empty(1, d).normal_(0, 0.02, generator=g))
        aux_head.bias.zero_()
    aux_head.to(DEVICE)
    params = list(model.parameters()) + list(aux_head.parameters())
    opt = torch.optim.AdamW(params, lr=STAGE_A_LR)

    rng = np.random.default_rng(seed)
    n = len(aux_examples)
    step = 0
    logs = []
    while step < STAGE_A_STEPS:
        order = rng.permutation(n)
        for bs in range(0, n, STAGE_A_BATCH):
            if step >= STAGE_A_STEPS:
                break
            bidx = order[bs:bs + STAGE_A_BATCH]
            batch = [aux_examples[i] for i in bidx]
            maxlen = max(len(b["ids"]) for b in batch)
            ids = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            attn = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            for i, b in enumerate(batch):
                L = len(b["ids"])
                ids[i, :L] = torch.tensor(b["ids"], device=DEVICE)
                attn[i, :L] = 1
            labels = ids.clone()
            labels[attn == 0] = -100
            out = model(input_ids=ids, attention_mask=attn,
                        output_hidden_states=True, labels=labels)
            lm_loss = out.loss
            hs = out.hidden_states[-1]
            aux_terms = []
            for i, b in enumerate(batch):
                if not b["pos"]:
                    continue
                pos = torch.tensor(b["pos"], device=DEVICE)
                tv = torch.tensor(b["val"], dtype=torch.float32, device=DEVICE)
                pred = aux_head(hs[i, pos]).squeeze(-1)
                aux_terms.append(nn.functional.mse_loss(pred, tv))
            aux_loss = torch.stack(aux_terms).mean() if aux_terms else torch.tensor(0.0, device=DEVICE)
            loss = lm_loss + lambda_aux * aux_loss
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
            if step % 50 == 0:
                logs.append({"step": step, "lm": float(lm_loss.item()),
                             "aux": float(aux_loss.item())})
            step += 1

    # converged aux-MSE: frozen trunk + trained head, mean over ALL word targets.
    model.eval()
    aux_head.eval()
    se_sum, n_words = 0.0, 0
    with torch.no_grad():
        for b in aux_examples:
            if not b["pos"]:
                continue
            ids = torch.tensor([b["ids"]], device=DEVICE)
            attn = torch.ones_like(ids)
            hs = model(input_ids=ids, attention_mask=attn,
                       output_hidden_states=True).hidden_states[-1]
            pos = torch.tensor(b["pos"], device=DEVICE)
            tv = torch.tensor(b["val"], dtype=torch.float32, device=DEVICE)
            pred = aux_head(hs[0, pos]).squeeze(-1)
            se_sum += float(((pred - tv) ** 2).sum().item())
            n_words += len(b["val"])
    final_aux_mse = float(se_sum / n_words) if (n_words and lambda_aux > 0) else float("nan")
    return logs, final_aux_mse


def stage_a_aux_arm(target_map, lambda_aux, tokenizer, stories, seed):
    model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32).to(DEVICE)
    aux_examples = build_aux_batches(tokenizer, stories, target_map)
    a_logs, aux_mse = stage_a_fixed_mse(model, tokenizer, aux_examples, lambda_aux, seed)
    state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    n_aux = len(aux_examples)
    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return state, a_logs, n_aux, aux_mse


# ===========================================================================
# Main
# ===========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["arms", "g2v2", "combine"], required=True)
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
    print(f"[{args.tag}] wiki_train={len(wiki_train)} tok  wiki_eval={len(wiki_eval)} tok"
          f"  seeds={args.seeds}  dev={os.environ.get('CUDA_VISIBLE_DEVICES','?')}", flush=True)

    m0 = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32)
    d, vocab = m0.config.hidden_size, m0.config.vocab_size
    base_wte = m0.state_dict()["transformer.wte.weight"].detach().clone().to(DEVICE)
    del m0

    config = {
        "base_lm": BASE, "aux_corpus": "natural_stories (10 stories)",
        "heldout_domain": "wikitext-103 (Wikipedia prose)",
        "metric": "frozen-trunk linear-probe AULC (mean held-out-domain probe ppl over caps, lower=better)",
        "version": "v4 (n>=10 + learnability-matched covariate adjudication; all v3 fixes kept)",
        "stage_a_steps": STAGE_A_STEPS, "stage_a_lr": STAGE_A_LR,
        "stage_a_batch": STAGE_A_BATCH, "lambda_aux": LAMBDA_AUX,
        "caps": CAPS, "seeds_this_shard": args.seeds,
        "arms": ARMS, "noncog_controls": NONCOG_CONTROLS,
        "other_lm": T.OTHER_LM_COL,
        "fixes": ["pad_labels_-100", "per_seed_surrogates", "oof_residual",
                  "identical_probe_init_base_wte", "torch_manual_seed_trunk",
                  "logfreq_arm", "wlen_arm", "other_lm_surprisal_arm",
                  "per_seed_final_aux_mse", "n>=10"],
    }

    if args.mode == "g2v2":
        from run_e021_v3 import frozen_probe_aulc as fpa
        targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=0)
        ctrl_map = {(r.item, r.zone): 0.0 for r in targ.itertuples()}
        rows = []
        for seed in args.seeds:
            hs_state, _ = stage_a_headstart(tokenizer, wiki_train, seed)
            hs_aulc, _ = fpa(hs_state, base_wte, wiki_train, wiki_eval, seed, d, vocab)
            del hs_state
            torch.cuda.empty_cache() if DEVICE == "cuda" else None
            ct_state, _, _, _ = stage_a_aux_arm(ctrl_map, 0.0, tokenizer, stories, seed)
            ct_aulc, _ = fpa(ct_state, base_wte, wiki_train, wiki_eval, seed, d, vocab)
            del ct_state
            torch.cuda.empty_cache() if DEVICE == "cuda" else None
            rows.append({"seed": seed, "headstart_aulc": hs_aulc, "control_aulc": ct_aulc})
            print(f"[g2v2 seed {seed}] hs={hs_aulc:.2f} ctrl={ct_aulc:.2f} diff={hs_aulc-ct_aulc:+.2f}", flush=True)
        hs_a = [r["headstart_aulc"] for r in rows]
        ct_a = [r["control_aulc"] for r in rows]
        m, lo, hi = paired_ci(hs_a, ct_a)
        diff = np.array(hs_a) - np.array(ct_a)
        sd = diff.std(ddof=1) if len(diff) > 1 else float("nan")
        mde = 1.96 * sd / math.sqrt(len(diff)) if len(diff) > 1 else float("nan")
        result = {"mode": "g2v2_v4", "config": config,
                  "headstart_aulc_per_seed": hs_a, "control_aulc_per_seed": ct_a,
                  "planted_effect_headstart_minus_control": {"mean": m, "ci": [lo, hi]},
                  "MDE": float(mde), "detected": bool(hi < 0),
                  "verdict": "PASS" if hi < 0 else "FAIL", "rows": rows}
        with open(f"{OUT}/g2v4_frozen_probe.json", "w") as f:
            json.dump(result, f, indent=2)
        print(f"G2 v4 {'PASS' if hi < 0 else 'FAIL'} (effect {m:+.1f} [{lo:+.1f},{hi:+.1f}], MDE {mde:.1f})")
        return

    # mode == arms — 8 arms, targets regenerated PER SEED (FIX 2), aux-MSE recorded.
    rows = []
    for seed in args.seeds:
        targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=seed)
        if seed == args.seeds[0] and args.tag in ("all", "g0"):
            targ.to_csv(f"{OUT}/aux_targets_v4.csv", index=False)
        arm_target = {
            "baseline": (None, 0.0),
            "raw": ({(r.item, r.zone): r.raw for r in targ.itertuples()}, LAMBDA_AUX),
            "residual": ({(r.item, r.zone): r.residual for r in targ.itertuples()}, LAMBDA_AUX),
            "permuted": ({(r.item, r.zone): r.permuted for r in targ.itertuples()}, LAMBDA_AUX),
            "random_struct": ({(r.item, r.zone): r.random_struct for r in targ.itertuples()}, LAMBDA_AUX),
            "logfreq": ({(r.item, r.zone): r.logfreq for r in targ.itertuples()}, LAMBDA_AUX),
            "wlen": ({(r.item, r.zone): r.wlen for r in targ.itertuples()}, LAMBDA_AUX),
            "surp_other_lm": ({(r.item, r.zone): r.surp_other_lm for r in targ.itertuples()}, LAMBDA_AUX),
        }
        for arm in ARMS:
            tmap, lam = arm_target[arm]
            if tmap is None:
                tmap = {(r.item, r.zone): 0.0 for r in targ.itertuples()}
            state, a_logs, n_aux, aux_mse = stage_a_aux_arm(tmap, lam, tokenizer, stories, seed)
            aulc, ppls = frozen_probe_aulc(state, base_wte, wiki_train, wiki_eval, seed, d, vocab)
            del state
            torch.cuda.empty_cache() if DEVICE == "cuda" else None
            rows.append({"arm": arm, "seed": seed, "aulc": aulc, "aux_mse": aux_mse,
                         "ppls": ppls, "n_aux_examples": n_aux, "stage_a_logs": a_logs})
            print(f"[{args.tag} seed {seed}] {arm:14s} AULC={aulc:.2f}  aux_mse={aux_mse:.4f}", flush=True)

    shard = {"mode": "arms_shard", "tag": args.tag, "config": config, "rows": rows}
    path = f"{OUT}/arms_v4_shard_{args.tag}.json"
    with open(path, "w") as f:
        json.dump(shard, f, indent=2)
    print(f"[{args.tag}] wrote {path}  ({len(rows)} arm-runs)")


# ===========================================================================
# Combine + the decisive stats (learnability-trend regression)
# ===========================================================================
def _ols_with_ci(x, y):
    """Simple OLS y = a + b x. Returns slope, intercept, and a function giving the
    fitted value + residual-SE at a query x (for the below-trend test)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    xb = x.mean(); yb = y.mean()
    sxx = ((x - xb) ** 2).sum()
    b = ((x - xb) * (y - yb)).sum() / sxx
    a = yb - b * xb
    resid = y - (a + b * x)
    dof = n - 2
    s2 = (resid ** 2).sum() / dof
    return a, b, s2, xb, sxx, dof


def _below_trend_test(ctrl_x, ctrl_y, qx, qy):
    """Test whether point (qx, qy) lies significantly BELOW the OLS line fit on the
    control points. Returns (gap, lo, hi, t, p_one_sided) where gap = qy - fitted
    (negative = below = better-than-learnability-predicts). CI is the prediction
    interval for a new observation, so 'CI excludes 0 and gap<0' = genuinely below."""
    from scipy import stats
    a, b, s2, xb, sxx, dof = _ols_with_ci(ctrl_x, ctrl_y)
    fitted = a + b * qx
    gap = qy - fitted
    # prediction-interval SE for a new point at qx
    se_pred = math.sqrt(s2 * (1 + 1.0 / len(ctrl_x) + (qx - xb) ** 2 / sxx))
    tcrit = stats.t.ppf(0.975, dof)
    lo, hi = gap - tcrit * se_pred, gap + tcrit * se_pred
    t = gap / se_pred
    p_one = stats.t.cdf(t, dof)  # P(below): t<0 small p
    return gap, lo, hi, t, p_one, (a, b)


def combine():
    shards = sorted(glob.glob(f"{OUT}/arms_v4_shard_*.json"))
    if not shards:
        raise SystemExit("no arms_v4_shard_*.json found")
    rows = []
    for s in shards:
        rows += json.load(open(s))["rows"]
    config = json.load(open(shards[0]))["config"]

    # collapse to per-(arm,seed); guard against accidental duplicate seeds across shards
    seen = {}
    for r in rows:
        seen[(r["arm"], r["seed"])] = r
    rows = list(seen.values())
    seeds = sorted({r["seed"] for r in rows})
    n = len(seeds)

    def series(arm, key):
        d = {r["seed"]: r[key] for r in rows if r["arm"] == arm}
        return [d[s] for s in seeds]

    aulc = {a: series(a, "aulc") for a in ARMS}
    auxmse = {a: series(a, "aux_mse") for a in ARMS}
    means = {a: float(np.mean(aulc[a])) for a in ARMS}
    sems = {a: float(np.std(aulc[a], ddof=1) / math.sqrt(n)) for a in ARMS}
    auxmse_mean = {a: float(np.nanmean(auxmse[a])) for a in ARMS}

    def contrast(x, y):
        m, lo, hi = paired_ci(aulc[x], aulc[y])
        return {"mean": m, "ci": [lo, hi], "excludes_0": bool(hi < 0 or lo > 0)}

    contrasts = {
        "residual_minus_permuted": contrast("residual", "permuted"),
        "residual_minus_random": contrast("residual", "random_struct"),
        "raw_minus_residual": contrast("raw", "residual"),
        "raw_minus_permuted": contrast("raw", "permuted"),
        "raw_minus_random": contrast("raw", "random_struct"),
        "residual_minus_logfreq": contrast("residual", "logfreq"),
        "residual_minus_wlen": contrast("residual", "wlen"),
        "residual_minus_other_lm": contrast("residual", "surp_other_lm"),
    }

    # ---- the decisive learnability-trend regression -----------------------
    # Pool per-(arm,seed) points for the non-cognitive controls: x=aux_mse, y=AULC.
    cx, cy = [], []
    for a in NONCOG_CONTROLS:
        cx += auxmse[a]; cy += aulc[a]
    # also a per-arm-mean version (less noisy, n=len(NONCOG_CONTROLS) points)
    mcx = [auxmse_mean[a] for a in NONCOG_CONTROLS]
    mcy = [means[a] for a in NONCOG_CONTROLS]

    trend = {}
    for label, X, Y in [("pooled_per_seed", cx, cy), ("per_arm_mean", mcx, mcy)]:
        a_, b_, s2, xb, sxx, dof = _ols_with_ci(X, Y)
        sub = {"slope": float(b_), "intercept": float(a_), "n_points": len(X), "dof": dof}
        for test_arm in ["residual", "raw"]:
            qx = auxmse_mean[test_arm]; qy = means[test_arm]
            gap, lo, hi, t, p_one, _ = _below_trend_test(X, Y, qx, qy)
            sub[test_arm] = {
                "aux_mse": float(qx), "aulc": float(qy),
                "gap_below_trend": float(gap), "ci": [float(lo), float(hi)],
                "t": float(t), "p_one_sided_below": float(p_one),
                "significantly_below": bool(hi < 0),
            }
        trend[label] = sub

    # ---- within-seed PAIRED learnability-trend (the CORRECT adjudicator) ---
    # The design is paired over seeds: each seed's random trunk+probe draws shift
    # EVERY arm's AULC together (the per-seed mean AULC swings ~145..363). The
    # pooled-per-seed OLS wrongly counts that shared seed nuisance as regression
    # scatter, inflating its prediction interval ~10x and masking real effects.
    # The right test fits the trend WITHIN each seed (across the non-cog controls),
    # predicts the test arm's AULC from its own within-seed aux-MSE, and pairs the
    # gap across seeds. This removes the shared seed variance — same logic as the
    # paired contrasts.
    from scipy import stats as _st

    def _within_seed_gap(test_arm):
        gaps, slopes = [], []
        for i in range(n):
            x = np.array([auxmse[a][i] for a in NONCOG_CONTROLS], float)
            y = np.array([aulc[a][i] for a in NONCOG_CONTROLS], float)
            xb = x.mean()
            b = ((x - xb) * (y - y.mean())).sum() / ((x - xb) ** 2).sum()
            a0 = y.mean() - b * xb
            gaps.append(aulc[test_arm][i] - (a0 + b * auxmse[test_arm][i]))
            slopes.append(b)
        gaps = np.array(gaps)
        m = float(gaps.mean()); sd = float(gaps.std(ddof=1))
        se = sd / math.sqrt(n)
        half = _st.t.ppf(0.975, n - 1) * se
        p_below = float(_st.t.cdf(m / se, n - 1))
        return {"gap_below_trend": m, "ci": [m - half, m + half],
                "p_one_sided_below": p_below, "per_seed_gaps": gaps.tolist(),
                "significantly_below": bool(m + half < 0),
                "no_sign_flip": bool(all(g < 0 for g in gaps)),
                "within_seed_slopes": [float(s) for s in slopes],
                "slope_all_negative": bool(all(s < 0 for s in slopes))}

    trend["within_seed_paired"] = {ta: _within_seed_gap(ta) for ta in ["residual", "raw"]}

    # ---- verdict logic (keyed on the within-seed paired test) -------------
    rd = contrasts["residual_minus_permuted"]["excludes_0"] and contrasts["residual_minus_permuted"]["mean"] < 0
    rr = contrasts["residual_minus_random"]["excludes_0"] and contrasts["residual_minus_random"]["mean"] < 0
    below = trend["within_seed_paired"]["residual"]["significantly_below"]
    raw_eq_resid = not contrasts["raw_minus_residual"]["excludes_0"]

    if below and rd and rr:
        verdict = ("POSITIVE (needs thinking panel + Erfan) — at n>=10 the RT-residual beats BOTH "
                   "surrogates (residual<permuted AND residual<random, CIs exclude 0) AND falls "
                   "significantly BELOW the within-seed learnability trend set by matched non-cognitive "
                   "word-aligned controls (logfreq/wlen/other-LM-surprisal/permuted/random). So the "
                   "RT signal helps the frozen probe MORE than its aux-target learnability predicts — "
                   "not explained by generic learnability. NOTE: raw~residual, so this is NOT "
                   "surprisal-orthogonality (that sub-result is NULL); it is RT-as-word-signal beating "
                   "learnability-matched non-cognitive controls. ESCALATE — do not flip any rung.")
    elif not below:
        verdict = ("CLEAN NULL — the RT-residual's AULC is explained by its aux-target learnability "
                   "(sits on the within-seed learnability trend, not below it). The advantage is "
                   "learnability, not cognition-specific content. Surprisal-orthogonality NULL (raw~residual).")
    else:
        verdict = ("STILL-INCONCLUSIVE — the surrogate contrasts and the within-seed learnability trend "
                   "disagree at n>=10; state which fired and why.")

    out = {
        "mode": "arms_combined_v4", "config": config, "n_seeds": n, "seeds": seeds,
        "arm_aulc_per_seed": aulc, "arm_aux_mse_per_seed": auxmse,
        "arm_aulc_mean": means, "arm_aulc_sem": sems, "arm_aux_mse_mean": auxmse_mean,
        "contrasts_n_ge_10": contrasts,
        "learnability_trend_regression": trend,
        "raw_approx_residual": raw_eq_resid,
        "verdict": verdict,
    }
    with open(f"{OUT}/arms_v4_results.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"\n=== E021 v4  n={n} seeds {seeds} ===")
    print(f"{'arm':16s} {'AULC mean±sem':>20s} {'aux_mse':>10s}")
    for a in ARMS:
        print(f"  {a:14s} {means[a]:8.2f} ± {sems[a]:5.2f}   {auxmse_mean[a]:8.4f}")
    print("\n-- n>=10 paired contrasts (AULC, lower=better) --")
    for k, v in contrasts.items():
        flag = "***" if v["excludes_0"] else "   "
        print(f"  {k:28s} {v['mean']:+8.2f}  CI[{v['ci'][0]:+8.2f},{v['ci'][1]:+8.2f}] {flag}")
    print("\n-- learnability-trend: WITHIN-SEED PAIRED (the correct adjudicator, removes shared seed variance) --")
    for arm in ["residual", "raw"]:
        d = trend["within_seed_paired"][arm]
        flag = "BELOW***" if d["significantly_below"] else "on-trend"
        print(f"     {arm:9s} gap={d['gap_below_trend']:+8.2f} CI[{d['ci'][0]:+8.2f},{d['ci'][1]:+8.2f}]"
              f"  p_below={d['p_one_sided_below']:.4f}  no_sign_flip={d['no_sign_flip']}  ({flag})")
    print("  [diagnostic only] pooled-per-seed OLS ignores pairing -> CI inflated by shared seed variance:")
    for arm in ["residual", "raw"]:
        d = trend["pooled_per_seed"][arm]
        print(f"     {arm:9s} gap={d['gap_below_trend']:+8.2f} CI[{d['ci'][0]:+8.2f},{d['ci'][1]:+8.2f}] (wide=masked)")
    print(f"\nVERDICT: {verdict}")
    print(f"Wrote {OUT}/arms_v4_results.json")


if __name__ == "__main__":
    main()
