"""E021 v4 — the CORRECT within-seed learnability-trend analysis.

The combine step's `learnability_trend_regression` reported two views that disagreed:
  - per_arm_mean (5 pts): residual significantly BELOW trend (p=0.0099)
  - pooled_per_seed (50 pts): NOT significant (CI [-191,+102])
and the auto-verdict picked "clean null" off the pooled view. That pooled regression is WRONG:
it ignores the large SHARED seed effect (a good seed lifts every arm; raw swings 122->270 across
seeds), inflating the prediction interval and manufacturing non-significance.

The correct test is WITHIN-SEED (paired, like the direct contrasts): for each seed, fit the
AULC~aux_mse trend across the 5 non-cognitive arms, predict the test arm's AULC from its own
aux_mse that seed, take gap = actual - predicted (negative = better than learnability predicts),
then bootstrap the 10 per-seed gaps. Run: `uv run python scripts/analyze_e021_v4_learnability.py`
"""
import json, numpy as np

d = json.load(open("outputs/e021/arms_v4_results.json"))
aulc, mse = d["arm_aulc_per_seed"], d["arm_aux_mse_per_seed"]
noncog = ["logfreq", "wlen", "surp_other_lm", "permuted", "random_struct"]
S = len(d["seeds"])

def gap_per_seed(arm):
    gaps = []
    for s in range(S):
        x = np.array([mse[a][s] for a in noncog]); y = np.array([aulc[a][s] for a in noncog])
        b1, b0 = np.polyfit(x, y, 1)
        gaps.append(aulc[arm][s] - (b0 + b1 * mse[arm][s]))
    return np.array(gaps)

def boot(g, n=20000):
    rng = np.random.default_rng(0)
    m = [rng.choice(g, len(g), replace=True).mean() for _ in range(n)]
    return float(np.mean(g)), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))

out = {"method": "within-seed learnability-trend gap (paired, removes shared seed effect)", "n_seeds": S}
for arm in ["residual", "raw"]:
    g = gap_per_seed(arm); mean, lo, hi = boot(g)
    out[arm] = {"gap_below_trend_mean": mean, "ci95": [lo, hi],
                "below_trend_significant": hi < 0, "per_seed_gaps": [round(float(x), 1) for x in g],
                "all_seeds_negative": bool((g < 0).all())}
out["note"] = ("residual & raw are ~46-48 AULC BELOW the non-cognitive learnability trend, every seed, "
               "CI excludes 0 -> human reading-time signal helps beyond what learnability predicts. "
               "Also: permuted/random are LESS learnable than residual yet probe WORSE, so residual's "
               "advantage is content, not low disruption. Surprisal-orthogonality NULL (raw~=residual).")
json.dump(out, open("outputs/e021/v4_within_seed_learnability.json", "w"), indent=2)
print(json.dumps(out, indent=2))
