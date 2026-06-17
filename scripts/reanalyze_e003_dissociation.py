"""Re-derive and archive E003's dissociation statistics (provenance repair, 2026-06-17).

WHY: E003.md and L011 lean on a dissociation analysis that lived only as prose: the
log-perplexity fit (Pearson r=-0.88; align = 0.050 - 0.0079*ln ppl), the per-point
residuals, two bootstrap dissociation P-values (P(gpt2<=kd_warm)=0.092,
P(lmft<=kd_warm)=0.085), and "one fold carries ~44% of the signal." None of it was archived,
so the guard that holds the strong claim back was less reproducible than the claim. This
script re-derives it from the per-fold/per-seed alignment arrays in the run JSONs plus the
recomputed reference ppls, and writes outputs/E003_dissociation.json.

HONESTY NOTES (these shape what this script does and does NOT claim):
  1. The ORIGINAL bootstrap P-value estimator (resample unit, seed, fold-source) was never
     recorded. This script PINS one documented construction (below) and reports what it
     yields. The acceptance test is the QUALITATIVE claim — the objective-specific
     dissociations are NOT clean significant effects — not third-decimal reproduction of
     0.092/0.085. A re-derived P-value near ~0.1 (or a construction-sensitive spread)
     confirms the qualitative claim; it does not "reproduce the original number."
  2. The regression part (r, slope, intercept, residuals, 44%-fold) IS reproducible and is
     archived with a bootstrap CI and a leave-one-out table so its INSTABILITY is visible.
  3. E015 retired the within-family r as layer-unstable noise: r here is the within-gpt2
     coupling whose ONLY job is to hedge against the strong "shed beyond ppl" claim. It is
     archived as that hedge, NOT promoted to a standalone result. See the forward-pointer.

PROVENANCE-ONLY: no alignment number, verdict, or rung changes.

Run:  uv run python scripts/reanalyze_e003_dissociation.py
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
COLD = REPO / "outputs/E003_cold.json"
WARM = REPO / "outputs/E003_warm.json"
PPL = REPO / "outputs/E003_perplexity.json"
OUT = REPO / "outputs/E003_dissociation.json"

# The fit spans the five trained/distilled points (teacher and untrained floor excluded).
# Same-file sourcing: warm.json for everything it carries, cold.json only for kd_cold.
FIT_POINTS = ["gpt2", "distilgpt2", "kd_warm", "lmft_warm", "kd_cold"]
BOOT_SEED = 0
N_BOOT = 100_000


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return "unknown"


def _seed_mean_folds(entries: list[dict]) -> np.ndarray:
    """Mean over seeds of the verdict-layer per-fold unique-R^2 -> one vector of length n_fold."""
    arrs = [np.asarray(e["verdict"]["unique_r2_per_fold"], float) for e in entries]
    return np.mean(np.stack(arrs, 0), axis=0)


def main() -> None:
    cold = json.loads(COLD.read_text())
    warm = json.loads(WARM.read_text())
    ppl_side = json.loads(PPL.read_text())["reference_perplexities"]

    # Per-point seed-mean fold vectors (alignment), sourced as documented.
    src = {p: warm for p in FIT_POINTS}
    src["kd_cold"] = cold
    folds = {p: _seed_mean_folds(src[p]["models"][p]) for p in FIT_POINTS}
    align = {p: float(folds[p].mean()) for p in FIT_POINTS}

    # Perplexity per point: references from the sidecar, trained arms from the run summary.
    ppl = {
        "gpt2": ppl_side["gpt2"]["perplexity"],
        "distilgpt2": ppl_side["distilgpt2"]["perplexity"],
        "kd_warm": warm["summary"]["arms"]["kd_warm"]["mean_perplexity"],
        "lmft_warm": warm["summary"]["arms"]["lmft_warm"]["mean_perplexity"],
        "kd_cold": cold["summary"]["arms"]["kd_cold"]["mean_perplexity"],
    }

    # --- log-ppl fit -------------------------------------------------------
    x = np.array([np.log(ppl[p]) for p in FIT_POINTS])
    y = np.array([align[p] for p in FIT_POINTS])
    r = float(np.corrcoef(x, y)[0, 1])
    slope, intercept = (float(v) for v in np.polyfit(x, y, 1))
    residuals = {p: float(y[i] - (slope * x[i] + intercept)) for i, p in enumerate(FIT_POINTS)}

    # leave-one-out r (the instability the verdict actually rests on)
    loo = {}
    for i, p in enumerate(FIT_POINTS):
        xs = np.delete(x, i)
        ys = np.delete(y, i)
        loo[f"drop_{p}"] = float(np.corrcoef(xs, ys)[0, 1])

    # bootstrap CI on r (resample the 5 points with replacement)
    rng = np.random.default_rng(BOOT_SEED)
    r_boot = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, len(x), len(x))
        if np.ptp(x[idx]) == 0 or np.ptp(y[idx]) == 0:
            continue
        r_boot.append(np.corrcoef(x[idx], y[idx])[0, 1])
    r_ci = [float(np.percentile(r_boot, 2.5)), float(np.percentile(r_boot, 97.5))]

    # --- dissociation P-values (TWO documented constructions) --------------
    # The original estimator was never archived; the P-value is construction-sensitive, so
    # we report TWO defensible constructions rather than tune one to the prose value:
    #   (a) fold-only: resample the 5 CV folds (seed-mean per fold). Discards seed variance.
    #   (b) fold x seed: resample the pooled (fold,seed) cells of each arm independently.
    #       Retains seed variance; wider, more conservative; ~matches the prose ~0.09.
    def _cells(tag: str) -> np.ndarray:
        return np.concatenate(
            [np.asarray(e["verdict"]["unique_r2_per_fold"], float)
             for e in src[tag]["models"][tag]]
        )

    def p_le_fold(left: str, right: str) -> float:
        fl, fr = folds[left], folds[right]
        rng2 = np.random.default_rng(BOOT_SEED)
        n = len(fl)
        hits = sum(int(fl[(ix := rng2.integers(0, n, n))].mean() <= fr[ix].mean())
                   for _ in range(N_BOOT))
        return hits / N_BOOT

    def p_le_cell(left: str, right: str) -> float:
        cl, cr = _cells(left), _cells(right)
        rng2 = np.random.default_rng(BOOT_SEED)
        hits = sum(int(cl[rng2.integers(0, len(cl), len(cl))].mean()
                       <= cr[rng2.integers(0, len(cr), len(cr))].mean())
                   for _ in range(N_BOOT))
        return hits / N_BOOT

    p_gpt2_fold = p_le_fold("gpt2", "kd_warm")
    p_lmft_fold = p_le_fold("lmft_warm", "kd_warm")
    p_gpt2_cell = p_le_cell("gpt2", "kd_warm")
    p_lmft_cell = p_le_cell("lmft_warm", "kd_warm")

    # --- "~44% of the signal in one fold" ---------------------------------
    delta_folds = folds["gpt2"] - folds["kd_warm"]
    frac = (delta_folds / delta_folds.sum()).tolist()
    max_fold = int(np.argmax(delta_folds))

    payload = {
        "provenance": {
            "what": "E003 dissociation statistics, re-derived for provenance.",
            "recomputed_on": "2026-06-17",
            "git_sha": _git_sha(),
            "inputs": {
                "alignment_folds": "outputs/E003_{warm,cold}.json "
                                   "models[arm][seed].verdict.unique_r2_per_fold, seed-averaged",
                "reference_ppls": "outputs/E003_perplexity.json",
                "trained_arm_ppls": "outputs/E003_{warm,cold}.json summary.arms[*].mean_perplexity",
            },
            "fit_points": FIT_POINTS,
            "fold_source": "warm.json for gpt2/distilgpt2/kd_warm/lmft_warm (same run/GPU as "
                           "kd_warm, which is warm-only); cold.json for kd_cold.",
            "bootstrap": {"seed": BOOT_SEED, "n_boot": N_BOOT,
                          "units": "two constructions reported: (a) fold-only seed-mean folds; "
                                   "(b) fold x seed pooled cells, per-arm independent resample"},
            "P_value_caveat": "The ORIGINAL P-value estimator was never archived, and the P-value "
                              "is CONSTRUCTION-SENSITIVE: a fold-only bootstrap gives ~0.00 "
                              "(seed variance discarded -> overstates significance), while a "
                              "fold x seed cell bootstrap gives ~0.1 (matches the prose 0.092/0.085). "
                              "The fold x seed construction is the more honest (it retains the seed "
                              "variability the 3-seed design generated). The QUALITATIVE claim stands "
                              "on it: neither dissociation is a clean significant effect. This "
                              "construction-sensitivity is itself why E003 alone cannot attribute the "
                              "gradient to the objective (L011). Flagged, not tuned.",
            "r_caveat": "Within-gpt2-family r; E015 retired the standalone within-family law as "
                        "layer-unstable noise. Archived here ONLY as the hedge against 'shed beyond "
                        "ppl', NOT as a standalone result. Forward-pointer: see E015.",
            "scope": "PROVENANCE-ONLY: no alignment number, verdict, or rung changes.",
        },
        "log_ppl_fit": {
            "pearson_r": round(r, 4),
            "pearson_r_bootstrap_ci": [round(c, 4) for c in r_ci],
            "slope": round(slope, 5),
            "intercept": round(intercept, 5),
            "residuals": {p: round(v, 5) for p, v in residuals.items()},
            "leave_one_out_r": {k: round(v, 4) for k, v in loo.items()},
            "alignment_per_point": {p: round(align[p], 5) for p in FIT_POINTS},
            "ppl_per_point": {p: round(ppl[p], 2) for p in FIT_POINTS},
        },
        "dissociation_p_values": {
            "fold_only": {"P_gpt2_le_kd_warm": round(p_gpt2_fold, 4),
                          "P_lmft_le_kd_warm": round(p_lmft_fold, 4)},
            "fold_x_seed": {"P_gpt2_le_kd_warm": round(p_gpt2_cell, 4),
                            "P_lmft_le_kd_warm": round(p_lmft_cell, 4)},
            "qualitative": "neither dissociation is a clean significant effect under the "
                           "fold x seed construction (the prose's ~0.09); fold-only is sensitive.",
        },
        "one_fold_dominance": {
            "gpt2_minus_kd_warm_per_fold": [round(v, 5) for v in delta_folds.tolist()],
            "fraction_per_fold": [round(f, 3) for f in frac],
            "max_fold_index": max_fold,
            "max_fold_fraction": round(frac[max_fold], 3),
        },
    }
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"r={r:.4f} CI={r_ci}  slope={slope:.5f} intercept={intercept:.5f}")
    print(f"residuals: kd_warm={residuals['kd_warm']:+.5f}  gpt2={residuals['gpt2']:+.5f}")
    print(f"LOO r: {payload['log_ppl_fit']['leave_one_out_r']}")
    print(f"fold-only:   P(gpt2<=kd_warm)={p_gpt2_fold:.4f}  P(lmft<=kd_warm)={p_lmft_fold:.4f}")
    print(f"fold x seed: P(gpt2<=kd_warm)={p_gpt2_cell:.4f}  P(lmft<=kd_warm)={p_lmft_cell:.4f}")
    print(f"max-fold dominance: fold {max_fold} = {frac[max_fold]*100:.1f}% of the gpt2-kd_warm delta")
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
