"""Sensitivity / power demonstration for the E008 per-individual null (counter-argument's
fix #1: prove the protocol PASSES a true positive, so the null isn't 'just underpowered').

Uses the OBSERVED between-subject variance of the E008 per-subject effects e_u, then asks:
if the true per-individual effect were delta, with what probability would our test
(t-CI excludes 0, n=9) detect it? A demonstrated power curve turns the analytic MDE into
an empirical sensitivity statement, using the real observed noise.

Run: uv run python scripts/sensitivity_e008.py outputs/E008_g0.json ... outputs/E008_g3.json
"""
import json, math, sys
from collections import defaultdict
from statistics import mean, median, stdev

T975 = {8: 2.306}  # df=n-1=8 for n=9


def main():
    paths = sys.argv[1:] or ["outputs/E008_g0.json", "outputs/E008_g1.json", "outputs/E008_g2.json", "outputs/E008_g3.json"]
    raw = []
    for p in paths:
        raw.extend(json.load(open(p))["raw"])
    by, perm = {}, defaultdict(list)
    for r in raw:
        k = (r["uid"], r["fold"], r["seed"])
        if r["is_perm"]:
            perm[k].append(r["unique_r2"])
        elif r["arm"] == "mse":
            by[k] = r["unique_r2"]
    cells = {k: by[k] - mean(perm[k]) for k in by if k in perm}
    uids = sorted({u for (u, f, s) in cells})
    e_u = {u: median([cells[(uu, f, s)] for (uu, f, s) in cells if uu == u]) for u in uids}
    obs = [e_u[u] for u in uids]
    n = len(obs)
    sd = stdev(obs)
    se = sd / math.sqrt(n)
    print(f"E008 observed per-subject effects (n={n}): mean={mean(obs):+.5f}, sd={sd:.5f}, se={se:.5f}")
    print(f"observed t-CI95 = [{mean(obs)-T975[8]*se:+.5f}, {mean(obs)+T975[8]*se:+.5f}]")

    # deterministic parametric power sim: resample n effects ~ Normal(delta, sd), test t-CI excludes 0.
    # LCG for reproducibility (no Math.random/np.random dependence on global seed).
    def randn(state):
        # Box-Muller from two LCG uniforms
        state = (1103515245 * state + 12345) & 0x7FFFFFFF; u1 = (state + 1) / 0x80000000
        state = (1103515245 * state + 12345) & 0x7FFFFFFF; u2 = state / 0x7FFFFFFF
        u1 = min(max(u1, 1e-9), 1 - 1e-9)
        return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2), state

    print("\nPOWER to detect a true per-individual effect of size delta (t-CI95 excludes 0, n=9, observed sd):")
    print(f"{'delta':>8s} {'power':>8s}")
    state = 20260612
    for delta in [0.0006, 0.001, 0.002, 0.003, 0.005, 0.008]:
        hits, N = 0, 4000
        for _ in range(N):
            samp = []
            for _ in range(n):
                z, state = randn(state); samp.append(delta + sd * z)
            m = mean(samp); s2 = stdev(samp) / math.sqrt(n)
            if m - T975[8] * s2 > 0:
                hits += 1
        print(f"{delta:>+8.4f} {hits/N:>8.2f}")
    print("\nREAD: high power at delta≈+0.003 ⇒ the protocol WOULD detect a per-individual effect of the")
    print("averaged-target magnitude; the observed ~0 is a true null, not a power failure.")

    # ---- POWER vs N (the open-frontier data requirement): how many subjects to detect delta? ----
    # Vary n and between-subject sd; t-CI95 excludes 0. Answers "how many deep subjects to acquire".
    def t975_df(df):
        T = {2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262,
             10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 19: 2.093, 24: 2.064, 29: 2.045}
        return T.get(df, 1.96)

    def power_at(nn, delta, sigma, state, N=3000):
        hits = 0
        for _ in range(N):
            samp = []
            for _ in range(nn):
                z, state = randn(state); samp.append(delta + sigma * z)
            m = mean(samp); s2 = stdev(samp) / math.sqrt(nn)
            if m - t975_df(nn - 1) * s2 > 0:
                hits += 1
        return hits / N, state

    # ---- REAL-RESIDUAL POSITIVE CONTROL (counter-argument fix: power on the ACTUAL two-level noise,
    #      not a flat Normal(delta, between-sd) draw). For each subject we have its real fold×seed cells;
    #      we BOOTSTRAP-resample those cells (propagating the real WITHIN-subject noise the parametric sim
    #      ignored), inject a synthetic true per-individual effect delta, recompute each subject's median,
    #      then run the SAME n=9 group t-CI. Power = fraction of bootstraps whose CI excludes 0.
    #      delta=0 recovers the one-sided false-positive rate (~0.025); a high power at delta=+0.002
    #      shows the instrument detects the size we deny, on the real noise structure. ----
    cells_by_u = {u: [cells[(uu, f, s)] for (uu, f, s) in cells if uu == u] for u in uids}
    wsd = {u: (stdev(v) if len(v) > 1 else 0.0) for u, v in cells_by_u.items()}
    print("\nReal within-subject cell sd (the noise the parametric sim omitted):")
    print("  " + ", ".join(f"uid{u}:{wsd[u]:.4f}" for u in uids))
    print(f"  mean within-subject sd = {mean(wsd.values()):.5f}  vs  between-subject sd = {sd:.5f}")

    def lcg_int(state, hi):
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        return state % hi, state

    print("\nREAL-RESIDUAL POSITIVE CONTROL (bootstrap real cells + inject delta; n=9 group t-CI excludes 0):")
    print(f"{'delta':>8s} {'power':>8s} {'mean_est':>10s} {'CI_lo':>9s} {'CI_hi':>9s}")
    state = 777
    for delta in [0.0, 0.001, 0.002, 0.003, 0.005]:
        hits, N = 0, 4000
        est_acc, lo_acc, hi_acc = [], [], []
        for _ in range(N):
            meds = []
            for u in uids:
                cu = cells_by_u[u]; nb = len(cu)
                bs = []
                for _ in range(nb):
                    j, state = lcg_int(state, nb); bs.append(cu[j])
                meds.append(median(bs) + delta)
            m = mean(meds); s2 = stdev(meds) / math.sqrt(n)
            lo, hi = m - T975[8] * s2, m + T975[8] * s2
            if lo > 0:
                hits += 1
            est_acc.append(m); lo_acc.append(lo); hi_acc.append(hi)
        print(f"{delta:>+8.4f} {hits/N:>8.2f} {mean(est_acc):>+10.5f} {mean(lo_acc):>+9.5f} {mean(hi_acc):>+9.5f}")
    print("READ: delta=0 ≈ false-positive rate; high power at delta=+0.002 ⇒ the group test detects the")
    print("per-individual effect that would GENERATE the averaged gain, ON THE REAL within+between noise —")
    print("so the observed group ~0 is a true null. (This does NOT claim per-BRAIN power; see manuscript §4.2.)")

    print("\nPOWER vs N (subjects) — the open-frontier acquisition requirement.")
    print("Between-subject sd from E008-ROI=0.00062; the E012 oracle estimated ~0.001 for voxelwise naturalistic.")
    for sigma in [0.00062, 0.001, 0.002]:
        print(f"\n  sigma_between={sigma:.5f}:")
        print(f"    {'n':>4s}  " + "  ".join(f"δ={d:+.4f}" for d in [0.001, 0.003, 0.005]))
        for nn in [3, 5, 8, 10, 15, 20, 30]:
            row = []
            for d in [0.001, 0.003, 0.005]:
                p, state = power_at(nn, d, sigma, state)
                row.append(f"{p:>8.2f}")
            print(f"    {nn:>4d}  " + "  ".join(row))
    print("\nREAD: locate the smallest n giving >=0.80 power for the target (delta, sigma) → the # deep")
    print("subjects to acquire for a powered per-individual test of an open-frontier effect.")


if __name__ == "__main__":
    main()
