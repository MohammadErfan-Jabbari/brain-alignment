#!/usr/bin/env python3
"""Analyze/gate an E016 Phase 3 runner output.

The gate is intentionally conservative. It reports summaries but refuses a
science verdict unless the run has >=3 seeds, the brain/permuted arms are
perplexity-matched to KD-only, and heldout target metrics are present.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def mean_ci(vals: list[float]) -> dict:
    arr = np.asarray(vals, dtype=float)
    if len(arr) == 0:
        return {"mean": None, "ci95": None, "n": 0}
    if len(arr) == 1:
        return {"mean": float(arr[0]), "ci95": [float(arr[0]), float(arr[0])], "n": 1}
    m = float(arr.mean())
    se = float(arr.std(ddof=1) / np.sqrt(len(arr)))
    return {"mean": m, "ci95": [m - 1.96 * se, m + 1.96 * se], "n": int(len(arr))}


def by_seed(rows: list[dict], arm: str, lam: float | None = None) -> dict[int, dict]:
    out = {}
    for row in rows:
        if row["arm"] != arm:
            continue
        if lam is not None and float(row["lambda_brain"]) != float(lam):
            continue
        out[int(row["seed"])] = row
    return out


def parse_int_csv(spec: object) -> list[int]:
    if spec is None:
        return []
    return [int(x) for x in str(spec).split(",") if x.strip()]


def parse_float_csv(spec: object) -> list[float]:
    if spec is None:
        return []
    return [float(x) for x in str(spec).split(",") if x.strip()]


def rel_delta(a: float, b: float) -> float:
    return abs(a - b) / max(abs(b), 1e-8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_json", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--ppl-rel-tolerance", type=float, default=0.05)
    ap.add_argument("--min-train-science", type=int, default=50000)
    ap.add_argument("--min-heldout-science", type=int, default=1000)
    ap.add_argument("--min-target-dim-science", type=int, default=20484)
    args = ap.parse_args()

    data = json.loads(args.run_json.read_text(encoding="utf-8"))
    rows = data["rows"]
    seeds = sorted({int(r["seed"]) for r in rows})
    lams = sorted({float(r["lambda_brain"]) for r in rows if r["arm"] != "kd_only"})
    config = data.get("config", {})
    expected_seeds = parse_int_csv(config.get("seeds")) or seeds
    expected_lams = parse_float_csv(config.get("lambda_brain_grid")) or lams
    kd = by_seed(rows, "kd_only")

    summary = {
        "run": str(args.run_json),
        "n_seeds": len(seeds),
        "expected_seeds": expected_seeds,
        "observed_seeds": seeds,
        "expected_lambdas": expected_lams,
        "observed_lambdas": lams,
        "expected_rows": len(expected_seeds) * (1 + 2 * len(expected_lams)),
        "observed_rows": len(rows),
        "target_dim": rows[0].get("target_dim") if rows else None,
        "n_train": rows[0].get("n_train") if rows else None,
        "n_heldout_ppl": rows[0].get("n_heldout_ppl") if rows else None,
        "ppl_rel_tolerance": args.ppl_rel_tolerance,
        "min_train_science": args.min_train_science,
        "min_heldout_science": args.min_heldout_science,
        "min_target_dim_science": args.min_target_dim_science,
        "arms": {},
        "paired": {},
        "gate": {},
    }

    seen = set()
    duplicate_rows = []
    for row in rows:
        key = (int(row["seed"]), row["arm"], float(row["lambda_brain"]))
        if key in seen:
            duplicate_rows.append({"seed": key[0], "arm": key[1], "lambda_brain": key[2]})
        seen.add(key)

    expected_grid = [(seed, "kd_only", 0.0) for seed in expected_seeds]
    for seed in expected_seeds:
        for lam in expected_lams:
            expected_grid.append((seed, "tribe_mse", float(lam)))
            expected_grid.append((seed, "tribe_perm", float(lam)))
    missing_rows = [
        {"seed": seed, "arm": arm, "lambda_brain": lam}
        for seed, arm, lam in expected_grid
        if (seed, arm, lam) not in seen
    ]
    extra_rows = [
        {"seed": seed, "arm": arm, "lambda_brain": lam}
        for seed, arm, lam in sorted(seen)
        if (seed, arm, lam) not in set(expected_grid)
    ]
    arm_seed_grid_complete = not missing_rows and not duplicate_rows and not extra_rows
    summary["grid"] = {
        "complete": bool(arm_seed_grid_complete),
        "missing_rows": missing_rows,
        "duplicate_rows": duplicate_rows,
        "extra_rows": extra_rows,
    }

    grouped = defaultdict(list)
    for row in rows:
        key = (row["arm"], float(row["lambda_brain"]))
        grouped[key].append(row)
    for (arm, lam), vals in grouped.items():
        name = arm if arm == "kd_only" else f"{arm}_lambda{lam:g}"
        summary["arms"][name] = {
            "perplexity": mean_ci([v["perplexity"] for v in vals]),
            "target_r2": mean_ci([v["target_r2"] for v in vals if v.get("target_r2") is not None]),
            "final_brain": mean_ci([v["final_brain"] for v in vals]),
            "n": len(vals),
        }

    matched_all = True
    all_paired_common_seeds = True
    has_target_metric = bool(rows) and all(r.get("target_r2") is not None for r in rows)
    for lam in expected_lams:
        real = by_seed(rows, "tribe_mse", lam)
        perm = by_seed(rows, "tribe_perm", lam)
        common = sorted(set(kd) & set(real) & set(perm))
        common_complete = common == expected_seeds
        all_paired_common_seeds = all_paired_common_seeds and common_complete
        ppl_real, ppl_perm = [], []
        r2_real_perm, r2_real_kd = [], []
        for seed in common:
            ppl_real.append(rel_delta(real[seed]["perplexity"], kd[seed]["perplexity"]))
            ppl_perm.append(rel_delta(perm[seed]["perplexity"], kd[seed]["perplexity"]))
            if real[seed].get("target_r2") is not None and perm[seed].get("target_r2") is not None:
                r2_real_perm.append(real[seed]["target_r2"] - perm[seed]["target_r2"])
                r2_real_kd.append(real[seed]["target_r2"] - kd[seed]["target_r2"])
        lam_key = f"lambda{lam:g}"
        ppl_ok = (
            common_complete
            and max(ppl_real or [float("inf")]) <= args.ppl_rel_tolerance
            and max(ppl_perm or [float("inf")]) <= args.ppl_rel_tolerance
        )
        matched_all = matched_all and ppl_ok
        summary["paired"][lam_key] = {
            "common_seeds": common,
            "common_seeds_complete": bool(common_complete),
            "ppl_rel_delta_real_vs_kd": mean_ci(ppl_real),
            "ppl_rel_delta_perm_vs_kd": mean_ci(ppl_perm),
            "ppl_matched": ppl_ok,
            "target_r2_real_minus_perm": mean_ci(r2_real_perm),
            "target_r2_real_minus_kd": mean_ci(r2_real_kd),
        }

    n_train = int(summary["n_train"] or 0)
    n_heldout = int(summary["n_heldout_ppl"] or 0)
    target_dim = int(summary["target_dim"] or 0)
    scale_ready = (
        n_train >= args.min_train_science
        and n_heldout >= args.min_heldout_science
        and target_dim >= args.min_target_dim_science
    )
    enough_expected_seeds = len(expected_seeds) >= 3 and seeds == expected_seeds
    has_lambda_grid = len(expected_lams) > 0
    science_ready = (
        enough_expected_seeds
        and has_lambda_grid
        and arm_seed_grid_complete
        and all_paired_common_seeds
        and matched_all
        and has_target_metric
        and scale_ready
    )
    summary["gate"] = {
        "science_ready": bool(science_ready),
        "enough_seeds": bool(enough_expected_seeds),
        "has_lambda_grid": bool(has_lambda_grid),
        "arm_seed_grid_complete": bool(arm_seed_grid_complete),
        "all_paired_common_seeds": bool(all_paired_common_seeds),
        "ppl_matched_all_lambdas": bool(matched_all),
        "has_heldout_target_metric": bool(has_target_metric),
        "scale_ready": bool(scale_ready),
        "train_size_ready": n_train >= args.min_train_science,
        "heldout_size_ready": n_heldout >= args.min_heldout_science,
        "target_dim_ready": target_dim >= args.min_target_dim_science,
        "interpretation": (
            "READY_FOR_INTERPRETATION_GATE"
            if science_ready
            else "SMOKE_OR_INCOMPLETE_DO_NOT_INTERPRET_AS_PHASE3_RESULT"
        ),
    }

    out = args.out or args.run_json.with_suffix(".analysis.json")
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["gate"], indent=2))
    for name, rec in summary["arms"].items():
        ppl = rec["perplexity"]["mean"]
        r2 = rec["target_r2"]["mean"]
        print(f"{name:22s} ppl={ppl if ppl is not None else 'NA'} target_r2={r2 if r2 is not None else 'NA'}")
    print(f"saved {out}")


if __name__ == "__main__":
    main()
