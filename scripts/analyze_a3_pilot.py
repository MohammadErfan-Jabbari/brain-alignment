"""E009 A3 pilot analysis — the contrasts + the MEASURED MDE (oracle gate #2).

Answers: (a) is the brain-specific representational gap (mse - mse_perm) nonzero in
all-data students? (b) the measured MDE from seed SD of the OOD ratio. (c) does the
gap grow with lambda at matched ppl? (d) downstream OOD contrasts mse vs {lm_only,
mse_perm, textfeat} — is any OOD gain brain-specific (survives the permuted + text-feature
controls)?

Run: uv run python scripts/analyze_a3_pilot.py [outputs/E009_a3_pilot.json]
"""
import json, math, sys
from collections import defaultdict
from statistics import mean, stdev

T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571}


def agg(vals):
    n = len(vals)
    m = mean(vals)
    sd = stdev(vals) if n > 1 else float("nan")
    se = sd / math.sqrt(n) if n > 1 else float("nan")
    mde = (T975.get(n - 1, 2.0) + 0.84) * se if n > 1 else float("nan")  # ~MDE80 two-sided
    return m, sd, se, mde


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "outputs/E009_a3_pilot.json"
    d = json.load(open(path))
    raw = d["raw"]
    ood_domains = list(raw[0]["ood_ratio"].keys())
    arms = []
    for r in raw:
        if r["arm"] not in arms:
            arms.append(r["arm"])

    by_arm = defaultdict(list)
    for r in raw:
        by_arm[r["arm"]].append(r)

    print("=" * 80)
    print(f"E009 A3 PILOT — {path}")
    print(f"base in-domain ppl={d['base_ppl_indomain']:.1f}  base OOD={ {k: round(v,1) for k,v in d['base_ppl_ood'].items()} }")
    print(f"base held-out unique_r2={d['base_heldout_unique_r2']:+.4f}  | text-feature target R2={d['textfeat_target_r2']:+.3f}")
    print("=" * 80)

    # per-arm table
    print(f"\n{'arm':16s} {'ppl_id':>7s} {'uR2(heldout)':>13s}  " + "  ".join(f"OODr/{k}" for k in ood_domains))
    arm_uR2, arm_ratio = {}, defaultdict(dict)
    for a in arms:
        rs = by_arm[a]
        ppl = mean(r["ppl_indomain"] for r in rs)
        uR2v = [r["heldout_unique_r2"] for r in rs]
        arm_uR2[a] = uR2v
        cells = f"{a:16s} {ppl:7.1f} {mean(uR2v):+13.4f}  "
        for k in ood_domains:
            rr = [r["ood_ratio"][k] for r in rs]
            arm_ratio[a][k] = rr
            cells += f"{mean(rr):7.3f}  "
        print(cells)

    # (a) brain-specific representational gap (mse vs mse_perm) at matched lambda
    mse_arm = next((a for a in arms if a.startswith("mse_l")), None)
    perm_arm = next((a for a in arms if a.startswith("mse_perm")), None)
    tf_arm = next((a for a in arms if a.startswith("textfeat")), None)
    lm_arm = "lm_only" if "lm_only" in arms else None
    print("\n--- (a) brain-specific REPRESENTATIONAL gap (held-out Tuckute unique_r2) ---")
    if mse_arm and perm_arm:
        diff = [a - b for a, b in zip(arm_uR2[mse_arm], arm_uR2[perm_arm])]
        m, sd, se, mde = agg(diff)
        print(f"  uR2({mse_arm}) - uR2({perm_arm}) = {m:+.5f}  (seed SD {sd:.5f}, MDE80 {mde:.5f})  "
              f"-> {'NONZERO-ish' if abs(m) > (mde or 9) else 'within noise'}")
    if mse_arm and lm_arm:
        diff = [a - b for a, b in zip(arm_uR2[mse_arm], arm_uR2[lm_arm])]
        print(f"  uR2({mse_arm}) - uR2({lm_arm}) = {mean(diff):+.5f}")

    # (b)+(d) downstream OOD contrasts + MEASURED MDE
    print("\n--- (b)+(d) downstream OOD-ratio contrasts (LOWER ratio = better OOD generalization) ---")
    for k in ood_domains:
        print(f"  [{k}]")
        for other in [lm_arm, perm_arm, tf_arm]:
            if other and mse_arm:
                paired = [a - b for a, b in zip(arm_ratio[mse_arm][k], arm_ratio[other][k])]
                m, sd, se, mde = agg(paired)
                verdict = "mse BETTER" if m < -mde else ("mse WORSE" if m > mde else "~equal (within measured MDE)")
                print(f"    {mse_arm} - {other}: Δratio={m:+.4f}  measured-MDE80={mde:.4f}  -> {verdict}")

    # (c) lambda-sweep: repr gap vs lambda at matched ppl
    mse_lams = sorted([a for a in arms if a.startswith("mse_l")], key=lambda s: float(s.split("_l")[1]))
    if len(mse_lams) > 1 and perm_arm:
        print("\n--- (c) λ-sweep: brain-specific repr gap + ppl by λ ---")
        for a in mse_lams:
            gap = mean(arm_uR2[a]) - mean(arm_uR2[perm_arm])
            ppl = mean(r["ppl_indomain"] for r in by_arm[a])
            print(f"    {a}: uR2={mean(arm_uR2[a]):+.4f}  gap-vs-perm={gap:+.5f}  ppl_id={ppl:.1f}")

    print("\n" + "=" * 80)
    print("READ: A3 has a fulcrum iff (a) the repr gap is nonzero AND (d) the OOD gain is mse-BETTER")
    print("vs BOTH the permuted twin AND the text-feature control beyond the MEASURED MDE. Else Fork-B null.")
    print("=" * 80)


if __name__ == "__main__":
    main()
