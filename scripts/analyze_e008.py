"""E008 crossed-inference analysis — the verdict statistic for the per-participant
in-domain F1 solidification. Implements exactly what the oracle HOLD required:

  - per-cell paired diff d[uid,fold,seed] = uR2(mse) - mean_p uR2(mse_perm_p)
  - per-subject robust estimate e_u = median over (fold,seed)
  - SUBJECT-axis inference (n=#uid): mean(e_u), t-CI(df=n-1), sign test, LOO-subject
  - FOLD-axis inference (n=#folds, the CONSERVATIVE headline): f_k = mean over (uid,seed),
    t-CI(df=#folds-1), cluster-bootstrap over folds, LOO-fold
  - report the MORE CONSERVATIVE of subject-CI and fold-CI as the headline
  - train-5 (E005's own subjects) vs held-out-5 (genuine OOS) split
  - SNR control: Spearman(e_u, per-subject baseline uR2)
  - null-stability: per-cell perm SE

Run: uv run python scripts/analyze_e008.py [outputs/E008_per_participant_Qwen.json]
"""
import json
import math
import sys
from collections import defaultdict
from statistics import mean, median, stdev

T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
        8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 14: 2.145, 19: 2.093}
TRAIN5 = {848, 865, 875, 876}        # E005-averaged UIDs (data reuse); 853 excluded (incomplete ROI, 60 NaNs)
HELD5 = {797, 837, 841, 856, 880}    # genuine out-of-sample brains


def t975(df):
    return T975.get(df, 1.96)


def t_ci(vals):
    n = len(vals)
    if n < 2:
        return (mean(vals), float("nan"), float("nan"))
    m = mean(vals); se = stdev(vals) / math.sqrt(n)
    return m, m - t975(n - 1) * se, m + t975(n - 1) * se


def cluster_bootstrap(vals, n_boot=20000, seed=1):
    n = len(vals); state = seed * 2654435761 + 12345; out = []
    for _ in range(n_boot):
        acc = 0.0
        for _ in range(n):
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            acc += vals[state % n]
        out.append(acc / n)
    out.sort()
    return out[int(0.025 * n_boot)], out[int(0.975 * n_boot)], sum(1 for x in out if x <= 0) / n_boot


def binom_sign_p(k, n):
    """One-sided binomial P(X>=k | p=0.5)."""
    from math import comb
    return sum(comb(n, i) for i in range(k, n + 1)) / (2 ** n)


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for rk, i in enumerate(order):
            r[i] = rk
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - 6 * d2 / (n * (n * n - 1)) if n > 2 else float("nan")


def main():
    paths = sys.argv[1:] if len(sys.argv) > 1 else ["outputs/E008_per_participant_Qwen.json"]
    # merge raw rows + folds across shards (the 4-GPU split writes one json per shard)
    raw, folds_merged, nc = [], {}, None
    for p in paths:
        dj = json.load(open(p))
        raw.extend(dj["raw"])
        folds_merged.update(dj.get("folds", {}))
        nc = dj["nc_matched"]
    d = {"raw": raw, "folds": folds_merged, "nc_matched": nc}
    print(f"merged {len(paths)} shard(s): {paths}")

    # index unique_r2 by (uid,fold,seed,arm)
    by = {}
    perm_by_cell = defaultdict(list)
    for r in raw:
        u, f, s = r["uid"], r["fold"], r["seed"]
        if r["is_perm"]:
            perm_by_cell[(u, f, s)].append(r["unique_r2"])
        else:
            by[(u, f, s, r["arm"])] = r["unique_r2"]

    # per-cell paired diff d = mse - mean(perm)
    cells = {}            # (uid,fold,seed) -> d
    perm_se_list = []
    for (u, f, s, arm), v in by.items():
        if arm != "mse":
            continue
        perms = perm_by_cell.get((u, f, s), [])
        if not perms:
            continue
        cells[(u, f, s)] = v - mean(perms)
        if len(perms) > 1:
            perm_se_list.append(stdev(perms) / math.sqrt(len(perms)))

    uids = sorted({u for (u, f, s) in cells})
    folds = sorted({f for (u, f, s) in cells})
    print("=" * 78)
    print(f"E008 crossed inference — {paths}")
    print(f"uids={uids}  folds={folds}  cells={len(cells)}  NC={nc:.3f}")
    print("=" * 78)

    # per-subject e_u (median robust + mean)
    e_u_med, e_u_mean = {}, {}
    for u in uids:
        vals = [cells[(uu, f, s)] for (uu, f, s) in cells if uu == u]
        e_u_med[u] = median(vals); e_u_mean[u] = mean(vals)
    print("\nPer-subject e_u (median | mean), NC-norm of median:")
    for u in uids:
        grp = "train" if u in TRAIN5 else ("held " if u in HELD5 else "?")
        print(f"  uid {u} [{grp}]: median={e_u_med[u]:+.5f}  mean={e_u_mean[u]:+.5f}  (NC {e_u_med[u]/nc:+.3f})")

    # ---- SUBJECT-axis ----
    em = [e_u_med[u] for u in uids]
    m, lo, hi = t_ci(em)
    npos = sum(1 for x in em if x > 0)
    print(f"\n[SUBJECT axis, n={len(uids)}]  mean(e_u median) = {m:+.5f}  t-CI95=[{lo:+.5f},{hi:+.5f}] "
          f"-> {'excl 0' if lo > 0 else 'INCL 0'}")
    print(f"  sign: {npos}/{len(uids)} positive (one-sided binom p={binom_sign_p(npos, len(uids)):.3f})")
    loo_sub = [mean([e_u_med[v] for v in uids if v != u]) for u in uids]
    print(f"  LOO-subject mean range: [{min(loo_sub):+.5f}, {max(loo_sub):+.5f}]  "
          f"(sign stays + : {all(x > 0 for x in loo_sub)})")

    # ---- FOLD-axis (conservative) ----
    f_k = []
    for f in folds:
        vals = [cells[(u, ff, s)] for (u, ff, s) in cells if ff == f]
        f_k.append(mean(vals))
    fm, flo, fhi = t_ci(f_k)
    blo, bhi, bp = cluster_bootstrap(f_k)
    print(f"\n[FOLD axis, n={len(folds)} — CONSERVATIVE]  per-fold f_k={[round(x,5) for x in f_k]}")
    print(f"  mean={fm:+.5f}  t-CI95(df={len(folds)-1})=[{flo:+.5f},{fhi:+.5f}] -> {'excl 0' if flo > 0 else 'INCL 0'}")
    print(f"  cluster-bootstrap CI95=[{blo:+.5f},{bhi:+.5f}]  p(mean<=0)={bp:.3f}")
    loo_fold = []
    for f in folds:
        rest = [cells[(u, ff, s)] for (u, ff, s) in cells if ff != f]
        # recompute fold-clustered mean over remaining folds
        fks = [mean([cells[(u, ff, s)] for (u, ff, s) in cells if ff == g]) for g in folds if g != f]
        _, l2, h2 = t_ci(fks)
        loo_fold.append((f, mean(rest), l2, h2))
    print("  LOO-fold (drop f -> remaining fold-clustered t-CI):")
    for f, mr, l2, h2 in loo_fold:
        print(f"    drop f{f}: mean={mr:+.5f}  CI=[{l2:+.5f},{h2:+.5f}] -> {'excl 0' if l2 > 0 else 'INCL 0'}")

    # ---- train vs held-out ----
    for label, grp in [("train-5 (data reuse)", TRAIN5), ("held-out-5 (genuine OOS)", HELD5)]:
        g = [e_u_med[u] for u in uids if u in grp]
        if g:
            gm, glo, ghi = t_ci(g)
            print(f"\n[{label}] n={len(g)}  mean(e_u)={gm:+.5f}  t-CI95=[{glo:+.5f},{ghi:+.5f}] "
                  f"-> {'excl 0' if glo > 0 else 'INCL 0'}  ({sum(1 for x in g if x>0)}/{len(g)} +)")

    # ---- SNR control ----
    base_u = {}
    for fk, fv in d["folds"].items():
        # key like "uid848:3"
        if ":" in str(fk) and str(fk).startswith("uid"):
            u = int(str(fk).split(":")[0][3:])
            base_u.setdefault(u, []).append(fv["base_unique_r2"])
    if base_u:
        snr = [mean(base_u[u]) for u in uids]
        rho = spearman(snr, em)
        print(f"\n[SNR control] Spearman(e_u, per-subject baseline uR²) = {rho:+.3f}")
        # drop top-2 SNR subjects, recompute subject mean
        topk = sorted(uids, key=lambda u: mean(base_u[u]))[-2:]
        rest = [e_u_med[u] for u in uids if u not in topk]
        if rest:
            print(f"  drop top-2 SNR subjects {topk}: mean(e_u)={mean(rest):+.5f} (was {m:+.5f})")

    if perm_se_list:
        print(f"\n[null stability] mean per-cell perm SE = {mean(perm_se_list):.5f} "
              f"(want << |effect| {abs(m):.5f})")

    # ---- ppl-confound read-out (E011 oracle fix): is the gap brain-specific at MATCHED ppl? ----
    # per cell: ΔuR²(real−perm) vs Δlog-ppl(real−perm); regress, report intercept (effect at Δppl=0).
    ppl_mse = {}
    ppl_perm = defaultdict(list)
    for r in raw:
        u, f, s = r["uid"], r["fold"], r["seed"]
        if r.get("perplexity") is None:
            continue
        if r["is_perm"]:
            ppl_perm[(u, f, s)].append(r["perplexity"])
        elif r["arm"] == "mse":
            ppl_mse[(u, f, s)] = r["perplexity"]
    pairs = []  # (d_logppl, d_uR2)
    for key, d_uR2 in cells.items():
        if key in ppl_mse and ppl_perm.get(key):
            dlp = math.log(ppl_mse[key]) - mean(math.log(p) for p in ppl_perm[key])
            pairs.append((dlp, d_uR2))
    if pairs and len(pairs) > 2:
        xs = [p[0] for p in pairs]; ys = [p[1] for p in pairs]
        mx, my = mean(xs), mean(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx > 1e-12 else float("nan")
        intercept = my - slope * mx
        dlp_mean = mx
        print("\n[ppl-confound read-out — E011] per-cell Δlog-ppl(real−perm) vs ΔuR²(real−perm):")
        print(f"  mean Δlog-ppl(real−perm) = {dlp_mean:+.4f}  (>0 ⇒ real arm has WORSE ppl; ~0 ⇒ matched)")
        print(f"  regression: ΔuR² = {slope:+.5f}·Δlogppl + {intercept:+.5f}")
        print(f"  INTERCEPT (brain-specific gap at MATCHED ppl) = {intercept:+.5f}  "
              f"[raw mean gap = {my:+.5f}]")
        print("  → if intercept ≈ 0 while raw mean > 0, the gap is L011 (ppl-driven), not brain-specific.")

    # ---- headline ----
    print("\n" + "=" * 78)
    conservative_excl0 = (flo > 0)
    loo_fold_ok = all(l2 > 0 for _, _, l2, _ in loo_fold)
    held = [e_u_med[u] for u in uids if u in HELD5]
    held_pos = (t_ci(held)[0] > 0) if held else None
    print(f"HEADLINE (conservative = fold-clustered): mean={fm:+.5f}, CI excl 0 = {conservative_excl0}, "
          f"LOO-fold all excl 0 = {loo_fold_ok}, held-out-5 mean>0 = {held_pos}, "
          f"sign {npos}/{len(uids)}")
    print("CONFIRMED iff: fold-CI excl 0 AND LOO-fold robust AND >=8/10 sign AND held-out-5>0 AND not-SNR.")
    print("=" * 78)


if __name__ == "__main__":
    main()
