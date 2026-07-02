#!/usr/bin/env python3
"""Fold-level analysis for run_brain_lever.py lambda sweeps."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


T95 = {
    2: 12.706,
    3: 4.303,
    4: 3.182,
    5: 2.776,
    6: 2.571,
    7: 2.447,
    8: 2.365,
    9: 2.306,
    10: 2.262,
}


def fold_values(rows: list[dict], value_key: str = "delta") -> dict[int, float]:
    by_fold: dict[int, list[float]] = defaultdict(list)
    for r in rows:
        if r.get(value_key) is not None:
            by_fold[int(r["fold"])].append(float(r[value_key]))
    return {f: float(np.mean(v)) for f, v in sorted(by_fold.items()) if v}


def fold_ci(values_by_fold: dict[int, float]) -> dict:
    vals = np.array(list(values_by_fold.values()), dtype=float)
    n = int(vals.size)
    mean = float(vals.mean()) if n else float("nan")
    if n <= 1:
        lo = hi = mean
    else:
        t = T95.get(n, 1.96)
        half = float(t * vals.std(ddof=1) / np.sqrt(n))
        lo, hi = mean - half, mean + half
    loo = {}
    for f in values_by_fold:
        rest = [v for k, v in values_by_fold.items() if k != f]
        loo[str(f)] = float(np.mean(rest)) if rest else float("nan")
    return {
        "n_folds": n,
        "mean": mean,
        "ci95_t": [lo, hi],
        "fold_means": {str(k): v for k, v in values_by_fold.items()},
        "loo_means": loo,
        "min_loo_mean": float(min(loo.values())) if loo else float("nan"),
        "max_loo_mean": float(max(loo.values())) if loo else float("nan"),
    }


def paired_diffs(rows: list[dict], control_rows: list[dict]) -> list[dict]:
    control_by_key: dict[tuple, list[float]] = defaultdict(list)
    for r in control_rows:
        key = (r.get("uid"), int(r["fold"]), int(r["seed"]))
        control_by_key[key].append(float(r["delta"]))

    out = []
    for r in rows:
        key = (r.get("uid"), int(r["fold"]), int(r["seed"]))
        if key not in control_by_key:
            continue
        c = float(np.mean(control_by_key[key]))
        rec = dict(r)
        rec["paired_delta"] = float(r["delta"]) - c
        out.append(rec)
    return out


def validate_lambda_grid_output(data: dict, raw: list[dict]) -> None:
    cfg = data.get("config", {})
    lambda_grid = cfg.get("lambda_grid") or []
    if len(lambda_grid) <= 1:
        return
    missing = [r["arm"] for r in raw if "null_key" not in r]
    if missing:
        raise SystemExit(
            "lambda-grid output lacks raw null_key fields; rerun with the patched run_brain_lever.py"
        )
    if any(r.get("is_perm") and "perm_draw" not in r for r in raw):
        raise SystemExit(
            "lambda-grid output lacks perm_draw fields; rerun with the patched run_brain_lever.py"
        )

    expected_draws = int(cfg.get("n_perm", 1))
    perm_cells: dict[tuple, list[dict]] = defaultdict(list)
    permuted_null_keys = {str(r["null_key"]) for r in raw if r.get("is_perm")}
    for r in raw:
        if r.get("is_perm"):
            key = (r["null_key"], r.get("uid"), int(r["fold"]), int(r["seed"]))
            perm_cells[key].append(r)

    problems = []
    for r in raw:
        if r.get("is_perm") or r["arm"] == "lm_only":
            continue
        if str(r["null_key"]) not in permuted_null_keys:
            continue
        key = (r["null_key"], r.get("uid"), int(r["fold"]), int(r["seed"]))
        ctrls = perm_cells.get(key, [])
        if len(ctrls) != expected_draws:
            problems.append(f"{r['arm']} cell {key} has {len(ctrls)} perm draws, expected {expected_draws}")
            continue
        bad_lam = [c["lambda_brain"] for c in ctrls if float(c["lambda_brain"]) != float(r["lambda_brain"])]
        if bad_lam:
            problems.append(f"{r['arm']} cell {key} has mismatched perm lambda(s) {bad_lam}")
        draws = sorted(c.get("perm_draw") for c in ctrls)
        if draws != list(range(expected_draws)):
            problems.append(f"{r['arm']} cell {key} has perm_draw ids {draws}, expected {list(range(expected_draws))}")
    if problems:
        raise SystemExit("invalid lambda-grid permuted controls:\n- " + "\n- ".join(problems[:20]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="run_brain_lever.py JSON output")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text())
    raw = data["raw"]
    validate_lambda_grid_output(data, raw)
    arms = sorted({r["arm"] for r in raw})
    lm_rows = [r for r in raw if r["arm"] == "lm_only" and not r["is_perm"]]
    perm_by_null: dict[str, list[dict]] = defaultdict(list)
    for r in raw:
        if r["is_perm"]:
            perm_by_null[str(r.get("null_key", r["kind"]))].append(r)

    analysis = {
        "source": args.input,
        "model": data.get("model"),
        "layer": data.get("layer"),
        "base_perplexity": data.get("base_perplexity"),
        "arms": {},
    }

    for arm in arms:
        rows = [r for r in raw if r["arm"] == arm]
        real = rows and not rows[0]["is_perm"]
        ent = {
            "n_rows": len(rows),
            "kind": rows[0].get("kind") if rows else None,
            "is_perm": bool(rows[0].get("is_perm")) if rows else None,
            "lambda_brain": rows[0].get("lambda_brain") if rows else None,
            "delta_fold": fold_ci(fold_values(rows, "delta")),
        }
        ppls = [r["perplexity"] for r in rows if r.get("perplexity") is not None]
        ent["perplexity_mean"] = float(np.mean(ppls)) if ppls else None
        if real:
            if arm != "lm_only" and lm_rows:
                vs_lm = paired_diffs(rows, lm_rows)
                ent["vs_lm_only_fold"] = fold_ci(fold_values(vs_lm, "paired_delta"))
            null_key = str(rows[0].get("null_key", rows[0].get("kind")))
            if arm != "lm_only" and null_key in perm_by_null:
                vs_perm = paired_diffs(rows, perm_by_null[null_key])
                ent["vs_matched_perm_fold"] = fold_ci(fold_values(vs_perm, "paired_delta"))
        analysis["arms"][arm] = ent

    out = Path(args.out) if args.out else Path(args.input).with_name(Path(args.input).stem + "_analysis.json")
    out.write_text(json.dumps(analysis, indent=2))

    print(f"wrote {out}")
    for arm, ent in analysis["arms"].items():
        if ent["is_perm"]:
            continue
        d = ent["delta_fold"]
        ppl = "NA" if ent["perplexity_mean"] is None else f"{ent['perplexity_mean']:.2f}"
        line = (f"{arm:12s} lambda={ent['lambda_brain']} ppl={ppl} "
                f"delta_fold={d['mean']:+.4f} CI[{d['ci95_t'][0]:+.4f},{d['ci95_t'][1]:+.4f}]")
        if "vs_matched_perm_fold" in ent:
            p = ent["vs_matched_perm_fold"]
            line += f"  vs_perm={p['mean']:+.4f} CI[{p['ci95_t'][0]:+.4f},{p['ci95_t'][1]:+.4f}]"
        if "vs_lm_only_fold" in ent:
            l = ent["vs_lm_only_fold"]
            line += f"  vs_lm={l['mean']:+.4f} CI[{l['ci95_t'][0]:+.4f},{l['ci95_t'][1]:+.4f}]"
        print(line)


if __name__ == "__main__":
    main()
