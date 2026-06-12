#!/usr/bin/env python3
"""I1 — merge E015-expansion shards and compute the GATED statistics (oracle HOLD→PASS).

PRIMARY: x = log bits-per-byte, y = middle-layer unique R². Robustness done on best-layer y and
per-token ppl x. The pooled Fisher CI narrows partly mechanically (scaling ladders are not independent
draws) [F3], so the headline robustness is:
  - leave-one-family-out Pearson r  (does the law ride one cluster?)
  - within-family scaling slopes      (independent direction replications: OPT, pythia ladders)
  - family-CLUSTER bootstrap CI       (resample families, not models)
Q2 (architecture beyond quality): ANCOVA y ~ log_bpb + C(family) with a common-support precondition and
n>=3 families only; plus the individual-subject law (sign must hold per-subject, else it's an L016 artifact).

Run:  uv run python scripts/merge_ppl_law.py --shards "outputs/E015_expand/shard_*.json"
"""
from __future__ import annotations
import argparse, glob, json, math
from pathlib import Path
import numpy as np

try:
    from scipy import stats as _st
except Exception:
    _st = None


def fisher_ci(r, n, z=1.96):
    if n <= 3 or abs(r) >= 1:
        return (float("nan"), float("nan"))
    zr = 0.5 * math.log((1 + r) / (1 - r)); se = 1 / math.sqrt(n - 3)
    return (math.tanh(zr - z * se), math.tanh(zr + z * se))


def pearson(x, y):
    return float(np.corrcoef(x, y)[0, 1])


def _avg_rank(a):
    a = np.asarray(a, dtype=float); order = np.argsort(a); ranks = np.empty(len(a))
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[order[j + 1]] == a[order[i]]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1  # average rank for ties
        i = j + 1
    return ranks


def spearman(x, y):
    """Tie-aware Spearman (Codex SHOULD-FIX): average ranks, not arbitrary argsort positions."""
    rx = _st.rankdata(x) if _st is not None else _avg_rank(x)
    ry = _st.rankdata(y) if _st is not None else _avg_rank(y)
    return pearson(np.asarray(rx, dtype=float), np.asarray(ry, dtype=float))


def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return beta, float(resid @ resid)


def ancova(lx, y, fams, min_n=3):
    """y ~ log_bpb (reduced) vs + C(family) (full). Family factor uses only families with >= min_n
    models (singletons would fit their own residual). Returns F, p, partial R², common-support flag."""
    fams = np.array(fams)
    counts = {f: int((fams == f).sum()) for f in set(fams)}
    big = sorted([f for f, c in counts.items() if c >= min_n])
    if len(big) < 2:  # Codex SHOULD-FIX: need >=2 families to test a family factor at all
        return {"families_used": big, "n": 0, "F": float("nan"), "p": float("nan"),
                "df": [0, 0], "partial_r2_family": float("nan"), "common_support": False,
                "note": "fewer than 2 families with n>=%d — family factor not identifiable" % min_n}
    keep = np.array([f in big for f in fams])
    lxk, yk, fk = lx[keep], y[keep], fams[keep]
    n = len(yk)
    ranges = {f: (lxk[fk == f].min(), lxk[fk == f].max()) for f in big}
    lo, hi = max(r[0] for r in ranges.values()), min(r[1] for r in ranges.values())
    common_support = hi > lo
    Xr = np.column_stack([np.ones(n), lxk])
    cats = big[1:]  # drop reference level
    D = np.column_stack([(fk == c).astype(float) for c in cats]) if cats else np.zeros((n, 0))
    Xf = np.column_stack([Xr, D])
    df1, df2 = Xf.shape[1] - Xr.shape[1], n - Xf.shape[1]
    rank_ok = np.linalg.matrix_rank(Xf) == Xf.shape[1]   # Codex SHOULD-FIX: collinearity guard
    _, rss_r = ols(Xr, yk); _, rss_f = ols(Xf, yk)
    if not rank_ok or df1 <= 0 or df2 <= 0 or rss_f <= 1e-12:  # Codex: zero-RSS / rank-deficient guard
        F = p = float("nan")
    else:
        F = ((rss_r - rss_f) / df1) / (rss_f / df2)
        p = float(_st.f.sf(F, df1, df2)) if (_st and F == F) else float("nan")
    partial_r2 = (rss_r - rss_f) / rss_r if rss_r > 1e-12 else float("nan")
    return {"families_used": big, "n": n, "F": F, "p": p, "df": [df1, df2], "rank_ok": bool(rank_ok),
            "partial_r2_family": partial_r2, "common_support": common_support,
            "support_overlap": [float(lo), float(hi)], "family_ranges": {f: [float(a), float(b)] for f, (a, b) in ranges.items()}}


def family_cluster_bootstrap(lx, y, fams, B=5000, seed=0):
    fams = np.array(fams); uniq = sorted(set(fams)); rng = np.random.default_rng(seed)
    idx_by = {f: np.where(fams == f)[0] for f in uniq}
    rs = []
    for _ in range(B):
        chosen = rng.choice(uniq, size=len(uniq), replace=True)
        ii = np.concatenate([idx_by[f] for f in chosen])
        if len(set(y[ii])) < 2 or np.std(lx[ii]) == 0:
            continue
        rs.append(pearson(lx[ii], y[ii]))
    rs = np.array([r for r in rs if np.isfinite(r)])
    if len(rs) == 0:  # Codex SHOULD-FIX: all samples degenerate
        return [float("nan"), float("nan")], float("nan")
    return [float(np.percentile(rs, 2.5)), float(np.percentile(rs, 97.5))], float(np.median(rs))


def lofo(lx, y, fams):
    fams = np.array(fams); out = {}
    for f in sorted(set(fams)):
        keep = fams != f
        if keep.sum() >= 3 and np.std(lx[keep]) > 0:
            out[f] = {"r": pearson(lx[keep], y[keep]), "n_remaining": int(keep.sum())}
    return out


def within_family(rows, xkey, ykey):
    out = {}
    by = {}
    for r in rows:
        by.setdefault(r["family"], []).append(r)
    for fam, rs in by.items():
        if len(rs) < 3:
            continue
        lx = np.array([math.log(r[xkey]) for r in rs]); y = np.array([r[ykey] for r in rs])
        lp = np.log(np.array([r["params"] for r in rs], dtype=float))
        s_x = float(np.polyfit(lx, y, 1)[0]); s_p = float(np.polyfit(lp, y, 1)[0])
        out[fam] = {"n": len(rs), "r_vs_logx": pearson(lx, y), "slope_vs_logx": s_x,
                    "r_vs_logparams": pearson(lp, y), "slope_vs_logparams": s_p}
    return out


def law(rows, xkey, ykey):
    lx = np.array([math.log(r[xkey]) for r in rows]); y = np.array([r[ykey] for r in rows])
    fams = [r["family"] for r in rows]
    r = pearson(lx, y)
    boot_ci, boot_med = family_cluster_bootstrap(lx, y, fams)
    return {"x": xkey, "y": ykey, "n_models": len(rows), "n_families": len(set(fams)),
            "pearson_r": r, "fisher_ci95_pooled": list(fisher_ci(r, len(rows))),
            "spearman_rho": spearman(lx, y), "ols_slope": float(np.polyfit(lx, y, 1)[0]),
            "family_cluster_bootstrap_ci95": boot_ci, "family_cluster_bootstrap_median_r": boot_med,
            "leave_one_family_out_r": lofo(lx, y, fams),
            "within_family": within_family(rows, xkey, ykey)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", default="outputs/E015_expand/shard_*.json")
    ap.add_argument("--out", default="outputs/E015_expand/E015_expand_merged.json")
    args = ap.parse_args()

    rows, errs = {}, []
    for f in sorted(glob.glob(args.shards)):
        for r in json.loads(Path(f).read_text())["models"]:
            if "error" in r:
                errs.append(r); continue
            if r["model"] in rows and abs(rows[r["model"]]["unique_r2_mid"] - r["unique_r2_mid"]) > 1e-9:
                print(f"  WARNING: {r['model']} appears in >1 shard with DIFFERING uR²_mid "
                      f"({rows[r['model']]['unique_r2_mid']:.5f} vs {r['unique_r2_mid']:.5f}) — keeping latest")
            rows[r["model"]] = r
    rows = list(rows.values())
    # Codex SHOULD-FIX: drop any row with non-finite x/y before headline statistics
    bad = [r["model"] for r in rows if not (np.isfinite(r["bpb"]) and np.isfinite(r["ppl_token"])
                                            and np.isfinite(r["unique_r2_mid"]) and np.isfinite(r["unique_r2_best"]))]
    if bad:
        print(f"  WARNING: dropping {len(bad)} rows with non-finite values: {bad}")
        rows = [r for r in rows if r["model"] not in bad]
    rows.sort(key=lambda r: r["bpb"])
    print(f"pooled {len(rows)} models / {len(set(r['family'] for r in rows))} families "
          f"({sorted(set(r['family'] for r in rows))}); {len(errs)} load errors\n")

    print(f"{'model':>22s} {'fam':>8s} {'vocab':>7s} {'bos':>4s} {'bpb':>6s} {'pplT':>8s} {'uR2mid':>9s} {'uR2*':>9s}")
    for r in rows:
        print(f"{r['model']:>22s} {r['family']:>8s} {r['vocab']:>7d} {r['adds_bos']:>4d} "
              f"{r['bpb']:>6.3f} {r['ppl_token']:>8.1f} {r['unique_r2_mid']:>+9.4f} {r['unique_r2_best']:>+9.4f}")

    primary = law(rows, "bpb", "unique_r2_mid")
    rob_best = law(rows, "bpb", "unique_r2_best")
    rob_ppl = law(rows, "ppl_token", "unique_r2_mid")
    anc = ancova(np.array([math.log(r["bpb"]) for r in rows]),
                 np.array([r["unique_r2_mid"] for r in rows]),
                 [r["family"] for r in rows])

    # individual-subject law (Q2 averaging guard): sign of r must hold per subject
    subj_law = {}
    uids = rows[0]["u_subj_mid"].keys()
    lx = np.array([math.log(r["bpb"]) for r in rows])
    for uid in uids:
        ys = np.array([r["u_subj_mid"][uid] for r in rows])
        subj_law[uid] = {"pearson_r": pearson(lx, ys), "mean_unique_r2": float(ys.mean())}

    P = primary
    print(f"\n=== PRIMARY law: middle-layer unique R²  vs  log bits-per-byte (n={P['n_models']} models, "
          f"{P['n_families']} families) ===")
    print(f"  Pearson r = {P['pearson_r']:+.3f}  (pooled Fisher CI {P['fisher_ci95_pooled'][0]:+.3f},"
          f"{P['fisher_ci95_pooled'][1]:+.3f} — narrows partly mechanically)")
    print(f"  family-CLUSTER bootstrap 95% CI = [{P['family_cluster_bootstrap_ci95'][0]:+.3f}, "
          f"{P['family_cluster_bootstrap_ci95'][1]:+.3f}] (median {P['family_cluster_bootstrap_median_r']:+.3f})  <- HEADLINE interval")
    print(f"  Spearman rho = {P['spearman_rho']:+.3f} (near-tautological on the scale axis)")
    print(f"  leave-one-family-out r:")
    for f, d in P["leave_one_family_out_r"].items():
        print(f"      drop {f:>9s} -> r={d['r']:+.3f} (n={d['n_remaining']})")
    print(f"  within-family scaling (independent direction replications):")
    for f, d in P["within_family"].items():
        print(f"      {f:>9s} n={d['n']}: slope(y vs log bpb)={d['slope_vs_logx']:+.4f} r={d['r_vs_logx']:+.3f};"
              f" slope(y vs log params)={d['slope_vs_logparams']:+.4f}")
    print(f"\n=== Q2 ANCOVA  y ~ log_bpb + C(family)  (family factor: {anc['families_used']}) ===")
    print(f"  common support across big families: {anc['common_support']} (overlap {anc['support_overlap']})")
    print(f"  family partial F({anc['df'][0]},{anc['df'][1]}) = {anc['F']:.2f}, p = {anc['p']:.4f}, "
          f"partial R²(family) = {anc['partial_r2_family']:+.3f}")
    print(f"  -> {'CLAIMABLE only if common_support AND p small AND survives panel' if anc['common_support'] else 'NO common support: family effect can only be BOUNDED, not claimed'}")
    print(f"\n=== Q2 individual-subject law (averaging guard, L016) ===")
    for uid, d in subj_law.items():
        print(f"      subject {uid}: r(log_bpb, unique R²) = {d['pearson_r']:+.3f}  (mean uR²={d['mean_unique_r2']:+.4f})")
    print(f"\n  robustness: best-layer y  r={rob_best['pearson_r']:+.3f} (cluster CI {rob_best['family_cluster_bootstrap_ci95']});"
          f"  per-token-ppl x  r={rob_ppl['pearson_r']:+.3f}")

    out = {"primary_bpb_mid": primary, "robustness_bpb_best": rob_best, "robustness_pplT_mid": rob_ppl,
           "ancova_family": anc, "subject_law": subj_law, "n_models": len(rows),
           "models": [{k: r[k] for k in ("model", "family", "params", "vocab", "adds_bos", "bpb",
                                         "ppl_token", "unique_r2_mid", "unique_r2_best", "mid_layer",
                                         "best_layer", "scale_T")} for r in rows]}
    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"\n  wrote {args.out}")


if __name__ == "__main__":
    main()
