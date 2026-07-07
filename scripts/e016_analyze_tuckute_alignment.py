#!/usr/bin/env python3
"""Analyze paired E016 saved-student Tuckute alignment outputs.

This is a post-hoc diagnostic helper, not a verdict engine. It reads one or
more TRIBE and textfeat Tuckute alignment JSONs, aligns seeds with complete arm
grids, and writes the real-brain contrasts needed for /interpret.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return data


def sign_flip_p_two_sided(vals: list[float]) -> float | None:
    arr = np.asarray(vals, dtype=np.float64)
    if arr.size == 0 or np.any(arr == 0):
        return None
    if not (np.all(arr > 0) or np.all(arr < 0)):
        return None
    if arr.size > 30:
        return None
    return float(2.0 * (0.5 ** int(arr.size)))


def summarize(vals: list[float]) -> dict[str, Any]:
    arr = np.asarray(vals, dtype=np.float64)
    if arr.size == 0:
        return {
            "n": 0,
            "mean": None,
            "std": None,
            "ci95_normal": None,
            "values": [],
            "all_positive": False,
            "all_negative": False,
            "sign_flip_p_two_sided": None,
        }
    mean = float(arr.mean())
    std = float(arr.std(ddof=1)) if arr.size > 1 else 0.0
    half_width = 1.96 * std / math.sqrt(float(arr.size)) if arr.size > 1 else 0.0
    values = [float(v) for v in arr.tolist()]
    return {
        "n": int(arr.size),
        "mean": mean,
        "std": std,
        "ci95_normal": [mean - half_width, mean + half_width],
        "values": values,
        "all_positive": bool(values) and all(v > 0.0 for v in values),
        "all_negative": bool(values) and all(v < 0.0 for v in values),
        "sign_flip_p_two_sided": sign_flip_p_two_sided(values),
    }


def load_alignment_rows(paths: list[Path], label: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_summaries = []
    data_meta = None
    scoring_meta = None
    input_rows = 0
    missing = 0
    considered = 0
    scored = 0
    for raw_path in paths:
        path = resolve_path(raw_path)
        data = load_json(path)
        file_rows = data.get("rows")
        if not isinstance(file_rows, list):
            raise ValueError(f"{path} does not contain a list-valued `rows` field")
        counts = data.get("row_counts") or {}
        input_rows += int(counts.get("input_rows", len(file_rows)))
        missing += int(counts.get("missing_or_unusable_artifact_rows", 0))
        considered += int(counts.get("artifact_rows_considered", len(file_rows)))
        scored += int(counts.get("artifact_rows_scored", sum(1 for r in file_rows if r.get("status") == "scored")))
        rows.extend(file_rows)
        data_meta = data_meta or data.get("data")
        scoring_meta = scoring_meta or data.get("scoring")
        source_summaries.append({
            "path": str(path),
            "row_counts": counts,
            "science_status": data.get("science_status"),
        })
    return rows, {
        "label": label,
        "sources": source_summaries,
        "input_rows": input_rows,
        "missing_or_unusable_artifact_rows": missing,
        "artifact_rows_considered": considered,
        "artifact_rows_scored": scored,
        "data": data_meta,
        "scoring": scoring_meta,
    }


def unique_scored_rows(rows: list[dict[str, Any]], label: str) -> dict[tuple[int, str], dict[str, Any]]:
    out: dict[tuple[int, str], dict[str, Any]] = {}
    duplicates: list[dict[str, Any]] = []
    for row in rows:
        if row.get("status") != "scored":
            continue
        key = (int(row["seed"]), str(row["arm"]))
        if key in out:
            duplicates.append({"seed": key[0], "arm": key[1], "label": label})
        out[key] = row
    if duplicates:
        raise ValueError(f"duplicate scored rows: {duplicates}")
    return out


def verdict_unique_r2(row: dict[str, Any]) -> float:
    return float(row["verdict"]["unique_r2"])


def pca_unique_r2(row: dict[str, Any], pca_key: str) -> float:
    return float(row["verdict"]["pca_robustness"][pca_key]["unique_r2"])


def complete_seeds(
    tribe_by_key: dict[tuple[int, str], dict[str, Any]],
    text_by_key: dict[tuple[int, str], dict[str, Any]],
    tribe_target_arm: str,
    tribe_perm_arm: str,
    text_target_arm: str,
    text_perm_arm: str,
) -> list[int]:
    seed_candidates = sorted({seed for seed, _ in tribe_by_key} | {seed for seed, _ in text_by_key})
    required = (
        ("tribe", "kd_only"),
        ("tribe", tribe_target_arm),
        ("tribe", tribe_perm_arm),
        ("textfeat", "kd_only"),
        ("textfeat", text_target_arm),
        ("textfeat", text_perm_arm),
    )
    ok = []
    for seed in seed_candidates:
        present = {
            ("tribe", arm): (seed, arm) in tribe_by_key
            for arm in ("kd_only", tribe_target_arm, tribe_perm_arm)
        }
        present.update({
            ("textfeat", arm): (seed, arm) in text_by_key
            for arm in ("kd_only", text_target_arm, text_perm_arm)
        })
        if all(present.get(req, False) for req in required):
            ok.append(seed)
    return ok


def arm_summary(by_key: dict[tuple[int, str], dict[str, Any]], seeds: list[int], arms: list[str]) -> dict[str, Any]:
    out = {}
    for arm in arms:
        out[arm] = summarize([verdict_unique_r2(by_key[(seed, arm)]) for seed in seeds])
    return out


def per_seed_records(
    tribe_by_key: dict[tuple[int, str], dict[str, Any]],
    text_by_key: dict[tuple[int, str], dict[str, Any]],
    seeds: list[int],
    tribe_target_arm: str,
    tribe_perm_arm: str,
    text_target_arm: str,
    text_perm_arm: str,
    value_fn,
) -> list[dict[str, Any]]:
    records = []
    for seed in seeds:
        t_kd = value_fn(tribe_by_key[(seed, "kd_only")])
        t_target = value_fn(tribe_by_key[(seed, tribe_target_arm)])
        t_perm = value_fn(tribe_by_key[(seed, tribe_perm_arm)])
        x_kd = value_fn(text_by_key[(seed, "kd_only")])
        x_target = value_fn(text_by_key[(seed, text_target_arm)])
        x_perm = value_fn(text_by_key[(seed, text_perm_arm)])
        tribe_gain_vs_kd = t_target - t_kd
        tribe_gain_vs_perm = t_target - t_perm
        text_gain_vs_kd = x_target - x_kd
        text_gain_vs_perm = x_target - x_perm
        records.append({
            "seed": seed,
            "tribe_kd_only_unique_r2": t_kd,
            f"tribe_{tribe_target_arm}_unique_r2": t_target,
            f"tribe_{tribe_perm_arm}_unique_r2": t_perm,
            "textfeat_kd_only_unique_r2": x_kd,
            f"textfeat_{text_target_arm}_unique_r2": x_target,
            f"textfeat_{text_perm_arm}_unique_r2": x_perm,
            "tribe_gain_vs_kd": tribe_gain_vs_kd,
            "tribe_gain_vs_perm": tribe_gain_vs_perm,
            "textfeat_gain_vs_kd": text_gain_vs_kd,
            "textfeat_gain_vs_perm": text_gain_vs_perm,
            "tribe_minus_textfeat_gain_vs_kd": tribe_gain_vs_kd - text_gain_vs_kd,
            "tribe_minus_textfeat_gain_vs_perm": tribe_gain_vs_perm - text_gain_vs_perm,
            "tribe_mse_minus_textfeat_mse_absolute": t_target - x_target,
            "tribe_kd_minus_textfeat_kd_absolute": t_kd - x_kd,
        })
    return records


def contrast_summary(per_seed: list[dict[str, Any]]) -> dict[str, Any]:
    keys = [
        "tribe_gain_vs_kd",
        "tribe_gain_vs_perm",
        "textfeat_gain_vs_kd",
        "textfeat_gain_vs_perm",
        "tribe_minus_textfeat_gain_vs_kd",
        "tribe_minus_textfeat_gain_vs_perm",
        "tribe_mse_minus_textfeat_mse_absolute",
        "tribe_kd_minus_textfeat_kd_absolute",
    ]
    return {key: summarize([float(row[key]) for row in per_seed]) for key in keys}


def available_pca_keys(rows_by_key: dict[tuple[int, str], dict[str, Any]]) -> list[str]:
    keys: set[str] = set()
    for row in rows_by_key.values():
        robust = (((row.get("verdict") or {}).get("pca_robustness")) or {})
        keys.update(str(k) for k in robust)
    return sorted(keys, key=lambda x: int(x) if x.isdigit() else x)


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    tribe_rows, tribe_meta = load_alignment_rows(args.tribe_alignment, "tribe")
    text_rows, text_meta = load_alignment_rows(args.textfeat_alignment, "textfeat")
    tribe_by_key = unique_scored_rows(tribe_rows, "tribe")
    text_by_key = unique_scored_rows(text_rows, "textfeat")
    seeds = complete_seeds(
        tribe_by_key,
        text_by_key,
        args.tribe_target_arm,
        args.tribe_perm_arm,
        args.textfeat_target_arm,
        args.textfeat_perm_arm,
    )
    expected_seeds = [int(x) for x in args.expected_seeds.split(",") if x.strip()] if args.expected_seeds else seeds
    missing_expected = [seed for seed in expected_seeds if seed not in seeds]
    per_seed = per_seed_records(
        tribe_by_key,
        text_by_key,
        seeds,
        args.tribe_target_arm,
        args.tribe_perm_arm,
        args.textfeat_target_arm,
        args.textfeat_perm_arm,
        verdict_unique_r2,
    )
    pca_keys = sorted(
        set(available_pca_keys(tribe_by_key)) & set(available_pca_keys(text_by_key)),
        key=lambda x: int(x) if x.isdigit() else x,
    )
    pca_robustness = {}
    for pca_key in pca_keys:
        robust_seed = per_seed_records(
            tribe_by_key,
            text_by_key,
            seeds,
            args.tribe_target_arm,
            args.tribe_perm_arm,
            args.textfeat_target_arm,
            args.textfeat_perm_arm,
            lambda row, k=pca_key: pca_unique_r2(row, k),
        )
        pca_robustness[pca_key] = contrast_summary(robust_seed)

    return {
        "science_status": "post_hoc_real_brain_alignment_diagnostic_only; not an E016 verdict or rung flip",
        "created_at_unix": time.time(),
        "source_outputs": {
            "tribe": [str(resolve_path(p)) for p in args.tribe_alignment],
            "textfeat": [str(resolve_path(p)) for p in args.textfeat_alignment],
        },
        "row_counts": {
            "tribe": {
                "input_rows": tribe_meta["input_rows"],
                "missing_or_unusable_artifact_rows": tribe_meta["missing_or_unusable_artifact_rows"],
                "artifact_rows_considered": tribe_meta["artifact_rows_considered"],
                "artifact_rows_scored": tribe_meta["artifact_rows_scored"],
            },
            "textfeat": {
                "input_rows": text_meta["input_rows"],
                "missing_or_unusable_artifact_rows": text_meta["missing_or_unusable_artifact_rows"],
                "artifact_rows_considered": text_meta["artifact_rows_considered"],
                "artifact_rows_scored": text_meta["artifact_rows_scored"],
            },
        },
        "seeds": seeds,
        "expected_seeds": expected_seeds,
        "missing_expected_seeds": missing_expected,
        "data": tribe_meta.get("data") or text_meta.get("data"),
        "protocol": tribe_meta.get("scoring") or text_meta.get("scoring"),
        "arms": {
            "tribe_target_arm": args.tribe_target_arm,
            "tribe_perm_arm": args.tribe_perm_arm,
            "textfeat_target_arm": args.textfeat_target_arm,
            "textfeat_perm_arm": args.textfeat_perm_arm,
        },
        "by_arm": {
            "tribe": arm_summary(tribe_by_key, seeds, ["kd_only", args.tribe_target_arm, args.tribe_perm_arm]),
            "textfeat": arm_summary(text_by_key, seeds, ["kd_only", args.textfeat_target_arm, args.textfeat_perm_arm]),
        },
        "per_seed": per_seed,
        "contrasts": contrast_summary(per_seed),
        "pca_robustness": pca_robustness,
        "readiness": {
            "complete_seed_count": len(seeds),
            "expected_seed_count": len(expected_seeds),
            "has_missing_expected_seeds": bool(missing_expected),
            "ready_for_interpret": not missing_expected and len(seeds) >= args.min_seeds,
            "min_seeds": args.min_seeds,
        },
        "interpretation_boundary": (
            "diagnostic real-brain endpoint on saved artifacts; post-hoc; requires /interpret/stat/code review "
            "before any claim"
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze paired E016 Tuckute saved-student alignment outputs."
    )
    parser.add_argument("--tribe-alignment", type=Path, action="append", required=True)
    parser.add_argument("--textfeat-alignment", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--expected-seeds", default="")
    parser.add_argument("--min-seeds", type=int, default=3)
    parser.add_argument("--tribe-target-arm", default="tribe_mse")
    parser.add_argument("--tribe-perm-arm", default="tribe_perm")
    parser.add_argument("--textfeat-target-arm", default="textfeat_mse")
    parser.add_argument("--textfeat-perm-arm", default="textfeat_perm")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = analyze(args)
    out = resolve_path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(out),
        "seeds": output["seeds"],
        "ready_for_interpret": output["readiness"]["ready_for_interpret"],
        "tribe_minus_textfeat_gain_vs_kd_mean": output["contrasts"]["tribe_minus_textfeat_gain_vs_kd"]["mean"],
        "tribe_minus_textfeat_gain_vs_perm_mean": output["contrasts"]["tribe_minus_textfeat_gain_vs_perm"]["mean"],
    }, indent=2))


if __name__ == "__main__":
    main()
