#!/usr/bin/env python3
"""Audit E016 saved-student Tuckute alignment analyses from raw rows.

This is a local verification helper for /interpret handoff. It recomputes the
seed-aligned real-brain contrasts from raw Tuckute alignment JSONs and checks
them against an analysis JSON written by e016_analyze_tuckute_alignment.py.
It is not a verdict engine and does not flip any rung.
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
PRIMARY_CONTRASTS = [
    "tribe_gain_vs_kd",
    "tribe_gain_vs_perm",
    "textfeat_gain_vs_kd",
    "textfeat_gain_vs_perm",
    "tribe_minus_textfeat_gain_vs_kd",
    "tribe_minus_textfeat_gain_vs_perm",
]


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return data


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


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


def load_sources(paths: list[Path], label: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    summaries = []
    data_values = []
    scoring_values = []
    counts = {
        "input_rows": 0,
        "missing_or_unusable_artifact_rows": 0,
        "artifact_rows_considered": 0,
        "artifact_rows_scored": 0,
    }
    for raw_path in paths:
        path = resolve_path(raw_path)
        data = load_json(path)
        file_rows = data.get("rows")
        if not isinstance(file_rows, list):
            raise ValueError(f"{path} does not contain a list-valued `rows` field")
        row_counts = data.get("row_counts") or {}
        counts["input_rows"] += int(row_counts.get("input_rows", len(file_rows)))
        counts["missing_or_unusable_artifact_rows"] += int(
            row_counts.get("missing_or_unusable_artifact_rows", 0)
        )
        counts["artifact_rows_considered"] += int(
            row_counts.get("artifact_rows_considered", len(file_rows))
        )
        counts["artifact_rows_scored"] += int(
            row_counts.get(
                "artifact_rows_scored",
                sum(1 for row in file_rows if row.get("status") == "scored"),
            )
        )
        rows.extend(file_rows)
        if data.get("data") is not None:
            data_values.append(data.get("data"))
        if data.get("scoring") is not None:
            scoring_values.append(data.get("scoring"))
        summaries.append({
            "path": str(path),
            "science_status": data.get("science_status"),
            "row_counts": row_counts,
        })
    return rows, {
        "label": label,
        "sources": summaries,
        "counts": counts,
        "data_values": data_values,
        "scoring_values": scoring_values,
    }


def rows_by_seed_arm(rows: list[dict[str, Any]], label: str) -> tuple[dict[tuple[int, str], dict[str, Any]], list[dict[str, Any]]]:
    out: dict[tuple[int, str], dict[str, Any]] = {}
    duplicates = []
    for row in rows:
        if row.get("status") != "scored":
            continue
        key = (int(row["seed"]), str(row["arm"]))
        if key in out:
            duplicates.append({"label": label, "seed": key[0], "arm": key[1]})
            continue
        out[key] = row
    return out, duplicates


def unique_r2(row: dict[str, Any]) -> float:
    return float(row["verdict"]["unique_r2"])


def pca_unique_r2(row: dict[str, Any], pca_key: str) -> float:
    return float(row["verdict"]["pca_robustness"][pca_key]["unique_r2"])


def parse_seed_list(seed_text: str) -> list[int]:
    return [int(x) for x in seed_text.split(",") if x.strip()]


def complete_seed_grid(
    tribe_by_key: dict[tuple[int, str], dict[str, Any]],
    text_by_key: dict[tuple[int, str], dict[str, Any]],
    args: argparse.Namespace,
) -> list[int]:
    candidates = sorted({seed for seed, _ in tribe_by_key} | {seed for seed, _ in text_by_key})
    seeds = []
    for seed in candidates:
        required = [
            (tribe_by_key, (seed, "kd_only")),
            (tribe_by_key, (seed, args.tribe_target_arm)),
            (tribe_by_key, (seed, args.tribe_perm_arm)),
            (text_by_key, (seed, "kd_only")),
            (text_by_key, (seed, args.textfeat_target_arm)),
            (text_by_key, (seed, args.textfeat_perm_arm)),
        ]
        if all(key in row_map for row_map, key in required):
            seeds.append(seed)
    return seeds


def per_seed_records(
    tribe_by_key: dict[tuple[int, str], dict[str, Any]],
    text_by_key: dict[tuple[int, str], dict[str, Any]],
    seeds: list[int],
    args: argparse.Namespace,
    value_fn,
) -> list[dict[str, Any]]:
    records = []
    for seed in seeds:
        t_kd = value_fn(tribe_by_key[(seed, "kd_only")])
        t_target = value_fn(tribe_by_key[(seed, args.tribe_target_arm)])
        t_perm = value_fn(tribe_by_key[(seed, args.tribe_perm_arm)])
        x_kd = value_fn(text_by_key[(seed, "kd_only")])
        x_target = value_fn(text_by_key[(seed, args.textfeat_target_arm)])
        x_perm = value_fn(text_by_key[(seed, args.textfeat_perm_arm)])
        tribe_gain_vs_kd = t_target - t_kd
        tribe_gain_vs_perm = t_target - t_perm
        textfeat_gain_vs_kd = x_target - x_kd
        textfeat_gain_vs_perm = x_target - x_perm
        records.append({
            "seed": seed,
            "tribe_kd_only_unique_r2": t_kd,
            f"tribe_{args.tribe_target_arm}_unique_r2": t_target,
            f"tribe_{args.tribe_perm_arm}_unique_r2": t_perm,
            "textfeat_kd_only_unique_r2": x_kd,
            f"textfeat_{args.textfeat_target_arm}_unique_r2": x_target,
            f"textfeat_{args.textfeat_perm_arm}_unique_r2": x_perm,
            "tribe_gain_vs_kd": tribe_gain_vs_kd,
            "tribe_gain_vs_perm": tribe_gain_vs_perm,
            "textfeat_gain_vs_kd": textfeat_gain_vs_kd,
            "textfeat_gain_vs_perm": textfeat_gain_vs_perm,
            "tribe_minus_textfeat_gain_vs_kd": tribe_gain_vs_kd - textfeat_gain_vs_kd,
            "tribe_minus_textfeat_gain_vs_perm": tribe_gain_vs_perm - textfeat_gain_vs_perm,
        })
    return records


def arm_summary(
    rows: dict[tuple[int, str], dict[str, Any]],
    seeds: list[int],
    arms: list[str],
) -> dict[str, Any]:
    return {
        arm: summarize([unique_r2(rows[(seed, arm)]) for seed in seeds])
        for arm in arms
    }


def contrast_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        key: summarize([float(row[key]) for row in records])
        for key in PRIMARY_CONTRASTS
    }


def available_pca_keys(by_key: dict[tuple[int, str], dict[str, Any]]) -> set[str]:
    keys = set()
    for row in by_key.values():
        robust = (((row.get("verdict") or {}).get("pca_robustness")) or {})
        keys.update(str(key) for key in robust)
    return keys


def close(a: Any, b: Any, atol: float) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) <= atol


def summary_matches(raw: dict[str, Any], recorded: dict[str, Any] | None, atol: float) -> bool:
    if not isinstance(recorded, dict):
        return False
    if int(raw["n"]) != int(recorded.get("n", -1)):
        return False
    if not close(raw["mean"], recorded.get("mean"), atol):
        return False
    raw_vals = raw.get("values") or []
    recorded_vals = recorded.get("values") or []
    if len(raw_vals) != len(recorded_vals):
        return False
    return all(close(a, b, atol) for a, b in zip(raw_vals, recorded_vals, strict=True))


def all_same(values: list[Any]) -> bool:
    if not values:
        return True
    first = canonical(values[0])
    return all(canonical(value) == first for value in values[1:])


def classify_route(all_checks_pass: bool, ready: bool, contrasts: dict[str, Any]) -> str:
    if not ready:
        return "real_brain_alignment_audit_not_ready"
    if not all_checks_pass:
        return "real_brain_alignment_audit_failed_needs_debug"
    kd = contrasts["tribe_minus_textfeat_gain_vs_kd"]
    perm = contrasts["tribe_minus_textfeat_gain_vs_perm"]
    if kd["all_positive"] and perm["all_positive"]:
        return "real_brain_positive_needs_stat_code_review"
    if kd["mean"] is not None and perm["mean"] is not None and kd["mean"] <= 0.0 and perm["mean"] <= 0.0:
        return "real_brain_warning_needs_claim_scope_review"
    return "real_brain_mixed_needs_claim_scope_review"


def audit(args: argparse.Namespace) -> dict[str, Any]:
    analysis_path = resolve_path(args.analysis_json)
    analysis = load_json(analysis_path)
    tribe_rows, tribe_meta = load_sources(args.tribe_alignment, "tribe")
    text_rows, text_meta = load_sources(args.textfeat_alignment, "textfeat")
    tribe_by_key, tribe_duplicates = rows_by_seed_arm(tribe_rows, "tribe")
    text_by_key, text_duplicates = rows_by_seed_arm(text_rows, "textfeat")
    seeds = complete_seed_grid(tribe_by_key, text_by_key, args)
    expected_seeds = parse_seed_list(args.expected_seeds) if args.expected_seeds else seeds
    missing_expected = [seed for seed in expected_seeds if seed not in seeds]

    raw_per_seed = per_seed_records(tribe_by_key, text_by_key, seeds, args, unique_r2)
    raw_contrasts = contrast_summary(raw_per_seed)
    raw_by_arm = {
        "tribe": arm_summary(
            tribe_by_key,
            seeds,
            ["kd_only", args.tribe_target_arm, args.tribe_perm_arm],
        ),
        "textfeat": arm_summary(
            text_by_key,
            seeds,
            ["kd_only", args.textfeat_target_arm, args.textfeat_perm_arm],
        ),
    }

    pca_keys = sorted(
        available_pca_keys(tribe_by_key) & available_pca_keys(text_by_key),
        key=lambda x: int(x) if x.isdigit() else x,
    )
    raw_pca = {}
    for pca_key in pca_keys:
        records = per_seed_records(
            tribe_by_key,
            text_by_key,
            seeds,
            args,
            lambda row, key=pca_key: pca_unique_r2(row, key),
        )
        raw_pca[pca_key] = contrast_summary(records)

    analysis_contrasts = analysis.get("contrasts") or {}
    analysis_by_arm = analysis.get("by_arm") or {}
    analysis_pca = analysis.get("pca_robustness") or {}

    contrast_matches = {
        key: summary_matches(raw_contrasts[key], analysis_contrasts.get(key), args.atol)
        for key in PRIMARY_CONTRASTS
    }
    by_arm_matches = {}
    for label, arms in raw_by_arm.items():
        by_arm_matches[label] = {
            arm: summary_matches(summary, ((analysis_by_arm.get(label) or {}).get(arm)), args.atol)
            for arm, summary in arms.items()
        }
    pca_matches = {
        pca_key: {
            key: summary_matches(raw_pca[pca_key][key], ((analysis_pca.get(pca_key) or {}).get(key)), args.atol)
            for key in PRIMARY_CONTRASTS
        }
        for pca_key in pca_keys
    }

    data_values = tribe_meta["data_values"] + text_meta["data_values"]
    scoring_values = tribe_meta["scoring_values"] + text_meta["scoring_values"]
    expected_row_count = len(expected_seeds) * 3 if expected_seeds else 0
    checks = {
        "source_files_exist": all(resolve_path(path).exists() for path in args.tribe_alignment + args.textfeat_alignment),
        "analysis_json_exists": analysis_path.exists(),
        "no_duplicate_seed_arm_rows": not tribe_duplicates and not text_duplicates,
        "no_missing_artifact_rows": (
            tribe_meta["counts"]["missing_or_unusable_artifact_rows"] == 0
            and text_meta["counts"]["missing_or_unusable_artifact_rows"] == 0
        ),
        "row_counts_at_least_expected_grid": (
            tribe_meta["counts"]["artifact_rows_scored"] >= expected_row_count
            and text_meta["counts"]["artifact_rows_scored"] >= expected_row_count
        ),
        "expected_seeds_complete": not missing_expected,
        "minimum_seed_count_met": len(seeds) >= args.min_seeds,
        "same_data_endpoint_across_sources": all_same(data_values),
        "same_scoring_protocol_across_sources": all_same(scoring_values),
        "analysis_seed_list_matches_raw": analysis.get("seeds") == seeds,
        "analysis_missing_expected_matches_raw": analysis.get("missing_expected_seeds", []) == missing_expected,
        "analysis_data_matches_sources": not data_values or canonical(analysis.get("data")) == canonical(data_values[0]),
        "analysis_protocol_matches_sources": not scoring_values or canonical(analysis.get("protocol")) == canonical(scoring_values[0]),
        "analysis_contrast_summaries_match_raw": all(contrast_matches.values()),
        "analysis_by_arm_summaries_match_raw": all(
            ok for label_matches in by_arm_matches.values() for ok in label_matches.values()
        ),
        "analysis_pca_summaries_match_raw": all(
            ok for pca_key_matches in pca_matches.values() for ok in pca_key_matches.values()
        ),
    }
    ready = checks["expected_seeds_complete"] and checks["minimum_seed_count_met"]
    all_checks_pass = all(checks.values())

    return {
        "science_status": "local_audit_of_real_brain_diagnostic; not a final E016 verdict or rung flip",
        "created_at_unix": time.time(),
        "sources": {
            "tribe_alignment": [str(resolve_path(path)) for path in args.tribe_alignment],
            "textfeat_alignment": [str(resolve_path(path)) for path in args.textfeat_alignment],
            "analysis_json": str(analysis_path),
        },
        "expected_seeds": expected_seeds,
        "complete_seeds": seeds,
        "missing_expected_seeds": missing_expected,
        "row_counts": {
            "tribe": tribe_meta["counts"],
            "textfeat": text_meta["counts"],
        },
        "checks": checks,
        "analysis_match": {
            "contrasts": contrast_matches,
            "by_arm": by_arm_matches,
            "pca_robustness": pca_matches,
        },
        "duplicates": {
            "tribe": tribe_duplicates,
            "textfeat": text_duplicates,
        },
        "all_checks_pass": all_checks_pass,
        "route": classify_route(all_checks_pass, ready, raw_contrasts),
        "data": data_values[0] if data_values else None,
        "scoring": scoring_values[0] if scoring_values else None,
        "per_seed": raw_per_seed,
        "contrasts": raw_contrasts,
        "pca_robustness": raw_pca,
        "interpretation_boundary": (
            "Audit checks row/protocol/arithmetic consistency only. A load-bearing result still needs "
            "/interpret, code/stat review, and Erfan-confirmed claim scope before any paper claim."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit paired E016 Tuckute alignment analysis from raw alignment rows."
    )
    parser.add_argument("--tribe-alignment", type=Path, action="append", required=True)
    parser.add_argument("--textfeat-alignment", type=Path, action="append", required=True)
    parser.add_argument("--analysis-json", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--expected-seeds", default="")
    parser.add_argument("--min-seeds", type=int, default=3)
    parser.add_argument("--tribe-target-arm", default="tribe_mse")
    parser.add_argument("--tribe-perm-arm", default="tribe_perm")
    parser.add_argument("--textfeat-target-arm", default="textfeat_mse")
    parser.add_argument("--textfeat-perm-arm", default="textfeat_perm")
    parser.add_argument("--atol", type=float, default=1e-12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = audit(args)
    out = resolve_path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(out),
        "all_checks_pass": output["all_checks_pass"],
        "route": output["route"],
        "complete_seeds": output["complete_seeds"],
        "missing_expected_seeds": output["missing_expected_seeds"],
        "tribe_minus_textfeat_gain_vs_kd_mean": output["contrasts"]["tribe_minus_textfeat_gain_vs_kd"]["mean"],
        "tribe_minus_textfeat_gain_vs_perm_mean": output["contrasts"]["tribe_minus_textfeat_gain_vs_perm"]["mean"],
    }, indent=2))


if __name__ == "__main__":
    main()
