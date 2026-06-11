"""Re-analysis of E005 (in-domain F1) and E006 (transfer feasibility) prompted by the
Session-8 thinking-panel audit (counter-argument + premortem, 2026-06-11).

Pure re-analysis of EXISTING outputs — no GPU, no training, no new evidence. It answers
two questions the panel raised:

  (Q1) Does E005's in-domain brain-specific gain (paired mse - mse_perm) survive HONEST
       inference at the fold level (the legitimate independent unit), instead of the
       15-cell (3 seeds x 5 folds, one subject-average) flat bootstrap that treats
       correlated re-randomizations as i.i.d.?  Plus leave-each-fold-out + sign test.

  (Q2) What is the *paired-contrast* MDE on the LeBel voxelwise axis (the transfer test's
       statistic), derived from E006's fold-level variance under a range of arm-to-arm
       correlations rho?  E006 only published the UNPAIRED mean-over-voxels MDE
       (+0.013/+0.015); the paired MDE is the number that decides whether a transfer test
       is even runnable.

Run:  uv run python scripts/reanalyze_e005_e006.py
"""
import json
import math
from statistics import mean, stdev

# Student-t 0.975 critical values (two-sided 95%) by df, for small-n fold inference.
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
        8: 2.306, 9: 2.262, 10: 2.228, 14: 2.145}


def t975(df):
    return T975.get(df, 1.96)


def fold_level_paired(raw, arm_a="mse", arm_b="mse_perm"):
    """Pair arm_a vs arm_b on matched (fold, seed); aggregate to fold means.

    Returns per-cell diffs, per-fold means (averaging over seeds), and the
    fold-level t-interval (df = n_folds-1) — the honest unit, since the 5 folds
    are the only mutually-disjoint eval partitions; the 3 seeds reuse the same data.
    """
    # index by (fold,seed,is_perm) using the chosen kind for the permuted arm
    def key(r):
        return (r["fold"], r["seed"])
    a = {key(r): r for r in raw if r["arm"] == "mse" and not r["is_perm"]} if arm_a == "mse" else None
    if arm_b == "mse_perm":
        b = {key(r): r for r in raw if r["is_perm"]}
    elif arm_b == "lm_only":
        b = {key(r): r for r in raw if r["arm"] == "lm_only"}
    else:
        raise ValueError(arm_b)
    if arm_a == "lm_only":
        a = {key(r): r for r in raw if r["arm"] == "lm_only"}

    cells = {}  # (fold,seed) -> paired diff in unique_r2 (delta cancels base, identical)
    for k in a:
        if k in b:
            cells[k] = a[k]["unique_r2"] - b[k]["unique_r2"]
    folds = sorted({f for (f, s) in cells})
    fold_means = []
    per_fold = {}
    for f in folds:
        vals = [cells[(f, s)] for (ff, s) in cells if ff == f]
        per_fold[f] = vals
        fold_means.append(mean(vals))
    n = len(fold_means)
    m = mean(fold_means)
    sd = stdev(fold_means) if n > 1 else float("nan")
    se = sd / math.sqrt(n)
    ci = (m - t975(n - 1) * se, m + t975(n - 1) * se)
    all_cells = list(cells.values())
    return {
        "cells": cells, "per_fold": per_fold, "fold_means": fold_means,
        "n_folds": n, "mean_of_fold_means": m, "sd_fold": sd, "se_fold": se,
        "t_ci95": ci, "n_cells": len(all_cells),
        "cell_mean": mean(all_cells), "cell_median": sorted(all_cells)[len(all_cells)//2],
        "frac_cells_pos": sum(1 for v in all_cells if v > 0) / len(all_cells),
        "frac_folds_pos": sum(1 for v in fold_means if v > 0) / n,
    }


def leave_one_fold_out(res):
    fm = res["fold_means"]
    out = {}
    for i in range(len(fm)):
        rest = fm[:i] + fm[i+1:]
        out[i] = mean(rest)
    return out


def cluster_bootstrap_folds(res, n_boot=20000, seed=0):
    """Resample folds (with replacement); within each draw average its seed cells.
    Deterministic LCG so the result is reproducible without numpy."""
    fm = res["fold_means"]
    n = len(fm)
    state = seed * 2654435761 + 12345
    means = []
    for _ in range(n_boot):
        acc = 0.0
        for _ in range(n):
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            acc += fm[state % n]
        means.append(acc / n)
    means.sort()
    lo = means[int(0.025 * n_boot)]
    hi = means[int(0.975 * n_boot)]
    p_le0 = sum(1 for x in means if x <= 0) / n_boot
    return {"ci95": (lo, hi), "boot_mean": mean(means), "p(mean<=0)": p_le0}


def paired_mde_sensitivity(fold_sd, n_folds, rho_grid=(0.0, 0.3, 0.5, 0.7, 0.9, 0.95)):
    """MDE80 (one-sided 0.05) for a PAIRED two-arm contrast on the LeBel mean-over-voxels
    statistic. var(a-b) = var(a)+var(b)-2 rho sqrt(var(a)var(b)); assume equal arm
    variances ~ fold_sd^2, so sd_diff = fold_sd * sqrt(2(1-rho)). MDE = 2.487 * sd_diff/sqrt(n)
    (matches E006's published unpaired MDE constant)."""
    se_unpaired = fold_sd / math.sqrt(n_folds)
    mde_unpaired = 2.487 * se_unpaired
    rows = []
    for rho in rho_grid:
        sd_diff = fold_sd * math.sqrt(2 * (1 - rho))
        mde = 2.487 * sd_diff / math.sqrt(n_folds)
        rows.append((rho, mde))
    return mde_unpaired, rows


def main():
    e5 = json.load(open("outputs/E005_Qwen.json"))
    raw = e5["raw"]

    print("=" * 78)
    print("Q1 — E005 in-domain, HONEST fold-level inference (Qwen-0.5B<-1.5B, lambda=10)")
    print("=" * 78)
    for a, b, label in [("mse", "mse_perm", "BRAIN-SPECIFIC: mse - mse_perm (matched ppl)"),
                        ("mse", "lm_only", "BEYOND-KD: mse - lm_only (UNmatched ppl)")]:
        r = fold_level_paired(raw, a, b)
        print(f"\n--- {label} ---")
        print(f"  per-fold means : {[round(x,5) for x in r['fold_means']]}")
        print(f"  n_cells={r['n_cells']}  cell_mean={r['cell_mean']:+.5f}  cell_median={r['cell_median']:+.5f}")
        print(f"  frac cells>0={r['frac_cells_pos']:.0%}  frac folds>0={r['frac_folds_pos']:.0%}")
        print(f"  FOLD-LEVEL (n={r['n_folds']}): mean={r['mean_of_fold_means']:+.5f}  sd={r['sd_fold']:.5f}  se={r['se_fold']:.5f}")
        print(f"  FOLD-LEVEL t-CI95 = [{r['t_ci95'][0]:+.5f}, {r['t_ci95'][1]:+.5f}]  -> {'EXCLUDES 0' if r['t_ci95'][0]>0 else 'INCLUDES 0'}")
        loo = leave_one_fold_out(r)
        print(f"  leave-each-fold-out: " + "  ".join(f"drop f{i}={v:+.5f}" for i, v in loo.items()))
        boot = cluster_bootstrap_folds(r)
        print(f"  cluster-bootstrap-folds CI95 = [{boot['ci95'][0]:+.5f}, {boot['ci95'][1]:+.5f}]  p(mean<=0)={boot['p(mean<=0)']:.3f}")

    print("\n" + "=" * 78)
    print("Q2 — Paired-contrast MDE on LeBel voxelwise axis (transfer-test feasibility)")
    print("=" * 78)
    in_domain_effect = 0.0081
    in_domain_loo = 0.0042
    for tag, path in [("Qwen-0.5B", "outputs/E006_lebel_Qwen.json"),
                      ("gpt2", "outputs/E006_lebel_gpt2.json")]:
        d = json.load(open(path))
        fold_sd = d["fold_sd"]; nf = d["config"]["n_folds"]
        mde_unp, rows = paired_mde_sensitivity(fold_sd, nf)
        print(f"\n--- {tag}: fold_sd={fold_sd:.5f}, n_folds={nf} ---")
        print(f"  UNPAIRED MDE80 (published) = {mde_unp:+.5f}  (json says {d['E007_lever_mde80']:+.5f})")
        print(f"  PAIRED MDE80 by assumed arm-correlation rho:")
        for rho, mde in rows:
            flag_eff = "detectable" if mde < in_domain_effect else "BELOW NOISE"
            flag_loo = "detectable" if mde < in_domain_loo else "BELOW NOISE"
            print(f"    rho={rho:>4}: MDE={mde:+.5f}   vs +0.0081(full)->{flag_eff:11}  vs +0.0042(loo)->{flag_loo}")
    print("\nReference: in-domain effect +0.0081 (full) / +0.0042 (leave-fold-4-out).")
    print("A transfer test is only runnable where the paired MDE sits BELOW the (attenuated) effect.")


if __name__ == "__main__":
    main()
