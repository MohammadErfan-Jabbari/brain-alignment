#!/usr/bin/env python3
"""Independent arithmetic and binding audit for the retained E026 result.

This checker deliberately does not import ``e026_audit_target_comparability``.
It consumes the single retained E026 audit JSON, recomputes the 55 frozen
mechanical checks from lower-level fields, verifies the embedded frozen
manifest and its current dependencies, and exits nonzero on any mismatch.

It is a verification artifact, not a scientific verdict engine. Target
coordinates are not replication units and the six seeds are technical
training realizations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
from scipy.stats import t


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT = ROOT / "outputs/E026/e026_audit.json"
DEFAULT_OUTPUT = ROOT / "outputs/E026/e026_independent_result_audit.json"
EXPECTED_LAGS = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)
EXPECTED_MASS_CUTS = (1, 8, 32, 128, 512)
RTOL = 1e-12
ATOL = 1e-12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve(path: str | Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else ROOT / value


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"expected a JSON object: {path}")
    return value


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def sha256_file(path: Path, chunk_bytes: int = 32 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk_bytes), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_int64(values: Sequence[int]) -> str:
    array = np.asarray(values, dtype="<i8")
    return hashlib.sha256(array.tobytes(order="C")).hexdigest()


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float, np.integer, np.floating)) and not isinstance(
        value, (bool, np.bool_)
    )


def close(left: Any, right: Any) -> bool:
    return bool(
        is_number(left)
        and is_number(right)
        and math.isclose(float(left), float(right), rel_tol=RTOL, abs_tol=ATOL)
    )


def compare_expected(
    expected: Any, observed: Any, label: str, mismatches: list[dict[str, Any]]
) -> None:
    """Compare a recomputed structure against a reported one with float tolerance."""
    if is_number(expected):
        if not close(expected, observed):
            mismatches.append({"check": label, "expected": expected, "observed": observed})
        return
    if isinstance(expected, Mapping):
        if not isinstance(observed, Mapping):
            mismatches.append({"check": label, "expected_type": "object", "observed": observed})
            return
        for key, value in expected.items():
            if key not in observed:
                mismatches.append({"check": f"{label}.{key}", "error": "missing reported key"})
            else:
                compare_expected(value, observed[key], f"{label}.{key}", mismatches)
        return
    if isinstance(expected, Sequence) and not isinstance(expected, (str, bytes, bytearray)):
        if not isinstance(observed, Sequence) or isinstance(observed, (str, bytes, bytearray)):
            mismatches.append({"check": label, "expected_type": "array", "observed": observed})
            return
        if len(expected) != len(observed):
            mismatches.append(
                {"check": label, "expected_length": len(expected), "observed_length": len(observed)}
            )
            return
        for index, (left, right) in enumerate(zip(expected, observed, strict=True)):
            compare_expected(left, right, f"{label}[{index}]", mismatches)
        return
    if expected != observed:
        mismatches.append({"check": label, "expected": expected, "observed": observed})


def exact_sign_flip_p(values: Sequence[float]) -> float | None:
    array = np.asarray(values, dtype=np.float64)
    if len(array) > 20:
        return None
    observed = abs(float(array.mean()))
    tolerance = 1e-15 * max(1.0, observed)
    extreme = 0
    for mask in range(1 << len(array)):
        signs = np.asarray(
            [1.0 if mask & (1 << index) else -1.0 for index in range(len(array))],
            dtype=np.float64,
        )
        if abs(float(np.mean(signs * array))) >= observed - tolerance:
            extreme += 1
    return float(extreme / (1 << len(array)))


def summary_stats(values: Sequence[float]) -> dict[str, Any]:
    array = np.asarray(values, dtype=np.float64)
    if not len(array):
        return {"n": 0, "values": []}
    mean = float(array.mean())
    if len(array) > 1:
        sd = float(array.std(ddof=1))
        half = float(t.ppf(0.975, len(array) - 1) * sd / math.sqrt(len(array)))
        interval: list[float] | None = [mean - half, mean + half]
    else:
        sd = None
        interval = None
    nonzero = array[array != 0]
    return {
        "n": int(len(array)),
        "values": array.tolist(),
        "mean": mean,
        "median": float(np.median(array)),
        "sd": sd,
        "t_ci95": interval,
        "positive_count": int(np.count_nonzero(nonzero > 0)),
        "nonzero_count_for_sign_test": int(len(nonzero)),
        "exact_paired_sign_flip_two_sided_p": exact_sign_flip_p(array),
        "sign_flip_assignments": 1 << len(array),
        "sign_flip_identifying_assumption": (
            "paired seed contrasts are exchangeable under independent sign reversal under the sharp null"
        ),
    }


def margin_check(
    name: str,
    value: float | None,
    margin: float | Sequence[float],
    *,
    reason: str | None = None,
) -> dict[str, Any]:
    if value is None:
        state = "UNRESOLVED"
    elif isinstance(margin, Sequence) and not isinstance(margin, (str, bytes, bytearray)):
        state = "PASS" if float(margin[0]) <= value <= float(margin[1]) else "FAIL"
    else:
        state = "PASS" if value <= float(margin) else "FAIL"
    return {"name": name, "state": state, "value": value, "margin": margin, "reason": reason}


def conjunction(checks: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    states = [str(check["state"]) for check in checks]
    state = "FAIL" if "FAIL" in states else ("PASS" if states and set(states) == {"PASS"} else "UNRESOLVED")
    return {
        "state": state,
        "n_checks": len(states),
        "pass_count": states.count("PASS"),
        "fail_count": states.count("FAIL"),
        "unresolved_count": states.count("UNRESOLVED"),
    }


def jensen_shannon(left_values: Sequence[float], right_values: Sequence[float]) -> float:
    left = np.asarray(left_values, dtype=np.float64)
    right = np.asarray(right_values, dtype=np.float64)
    if left.shape != right.shape or left.sum() <= 0 or right.sum() <= 0:
        raise ValueError("invalid power arrays for Jensen-Shannon divergence")
    left /= left.sum()
    right /= right.sum()
    middle = 0.5 * (left + right)
    kl_left = np.sum(np.where(left > 0, left * np.log(left / np.maximum(middle, 1e-300)), 0))
    kl_right = np.sum(
        np.where(right > 0, right * np.log(right / np.maximum(middle, 1e-300)), 0)
    )
    return float(0.5 * (kl_left + kl_right))


def recompute_geometry(
    audit: Mapping[str, Any], margins: Mapping[str, Any], mismatches: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    geometry = audit["geometry"]
    families = geometry["families"]
    checks: list[dict[str, Any]] = []
    samples: dict[str, Any] = {}
    for sample in ("A", "B"):
        tribe_record = families["tribe"]["samples"][sample]["training_standardized_primary"]
        text_record = families["textfeat"]["samples"][sample]["training_standardized_primary"]
        tribe = tribe_record["svd"]
        textfeat = text_record["svd"]
        left = np.asarray(tribe["normalized_covariance_eigenvalues_top512"], dtype=np.float64)
        right = np.asarray(textfeat["normalized_covariance_eigenvalues_top512"], dtype=np.float64)
        if left.shape != (512,) or right.shape != (512,):
            raise ValueError(f"{sample}: expected two 512-value normalized spectra")
        valid = (left > left[0] * 1e-8) & (right > right[0] * 1e-8)
        log_rms = (
            float(np.sqrt(np.mean(np.square(np.log(left[valid]) - np.log(right[valid])))))
            if valid.any()
            else None
        )
        stable_log = abs(
            math.log(float(tribe["sample_stable_rank"]) / float(textfeat["sample_stable_rank"]))
        )
        left_pre = tribe_record["pre_center_global_moments"]
        right_pre = text_record["pre_center_global_moments"]
        mean_difference = abs(float(left_pre["mean"]) - float(right_pre["mean"]))
        right_sd = float(right_pre["population_sd"])
        sd_ratio = float(left_pre["population_sd"]) / right_sd if right_sd > 0 else None
        sample_checks = [
            margin_check(
                f"{sample}:standardized_global_mean",
                mean_difference,
                margins["sample_global_mean_abs_difference"],
            ),
            margin_check(
                f"{sample}:standardized_global_sd_ratio",
                sd_ratio,
                margins["sample_global_sd_ratio"],
                reason="zero text-feature sample SD" if sd_ratio is None else None,
            ),
            margin_check(
                f"{sample}:normalized_covariance_spectrum",
                log_rms,
                margins["normalized_covariance_log_eigen_rms"],
                reason="no common eigenvalues above floor" if log_rms is None else None,
            ),
            margin_check(
                f"{sample}:sample_stable_rank",
                stable_log,
                margins["sample_stable_rank_abs_log_ratio"],
            ),
        ]
        mass_differences: dict[str, float] = {}
        for cut in EXPECTED_MASS_CUTS:
            key = str(cut)
            difference = abs(float(tribe["variance_mass"][key]) - float(textfeat["variance_mass"][key]))
            mass_differences[key] = difference
            sample_checks.append(
                margin_check(
                    f"{sample}:variance_mass@{cut}",
                    difference,
                    margins["variance_mass_abs_difference"],
                )
            )
        checks.extend(sample_checks)
        samples[sample] = {
            "standardized_global_mean_absolute_difference": mean_difference,
            "standardized_global_sd_ratio": sd_ratio,
            "top512_normalized_covariance_log_eigen_rms_difference": log_rms,
            "top512_values_excluded_below_1e-8_leading": int(len(left) - np.count_nonzero(valid)),
            "tribe_sample_stable_rank": tribe["sample_stable_rank"],
            "textfeat_sample_stable_rank": textfeat["sample_stable_rank"],
            "sample_stable_rank_abs_log_ratio": stable_log,
            "variance_mass_absolute_differences": mass_differences,
            "checks": sample_checks,
        }

    order: dict[str, Any] = {"trace_autocorrelation": {}}
    trace_checks: list[dict[str, Any]] = []
    for lag in EXPECTED_LAGS:
        key = str(lag)
        left = families["tribe"]["order"]["trace_autocorrelation_all_coordinates"][key]["rho_trace"]
        right = families["textfeat"]["order"]["trace_autocorrelation_all_coordinates"][key]["rho_trace"]
        difference = None if left is None or right is None else abs(float(left) - float(right))
        check = margin_check(
            f"trace_autocorrelation@{lag}",
            difference,
            margins["trace_autocorrelation_abs_difference"],
            reason="no valid within-document pairs at this lag" if difference is None else None,
        )
        trace_checks.append(check)
        order["trace_autocorrelation"][key] = {
            "tribe": left,
            "textfeat": right,
            "absolute_difference": difference,
        }
    checks.extend(trace_checks)
    order["power_js_nats"] = {}
    for sample in ("A", "B"):
        left = families["tribe"]["order"]["coordinate_samples"][sample]["welch_trace_power"][
            "normalized_power"
        ]
        right = families["textfeat"]["order"]["coordinate_samples"][sample]["welch_trace_power"][
            "normalized_power"
        ]
        value = jensen_shannon(left, right)
        check = margin_check(
            f"coordinate_sample_{sample}:power_js_nats",
            value,
            margins["power_spectrum_js_nats"],
        )
        checks.append(check)
        order["power_js_nats"][sample] = value

    nuisance = geometry["nuisance_target_predictability"]
    nuisance_summary: dict[str, Any] = {
        "selected_alpha": nuisance["selected_alpha"],
        "inner_alpha_aggregate_r2": nuisance["inner_alpha_aggregate_r2"],
        "samples": {},
    }
    nuisance_checks: list[dict[str, Any]] = []
    for sample in ("A", "B"):
        tribe = nuisance["heldout_records"]["tribe"][sample]
        textfeat = nuisance["heldout_records"]["textfeat"][sample]
        low_difference = abs(
            float(tribe["low_level_only_variance_weighted_r2"])
            - float(textfeat["low_level_only_variance_weighted_r2"])
        )
        unique_difference = abs(
            float(tribe["static_unique_delta_r2"]) - float(textfeat["static_unique_delta_r2"])
        )
        sample_checks = [
            margin_check(
                f"{sample}:low_level_target_r2",
                low_difference,
                margins["low_level_target_r2_abs_difference"],
            ),
            margin_check(
                f"{sample}:static_unique_target_r2",
                unique_difference,
                margins["static_unique_target_r2_abs_difference"],
            ),
        ]
        nuisance_checks.extend(sample_checks)
        nuisance_summary["samples"][sample] = {
            "tribe": tribe,
            "textfeat": textfeat,
            "low_level_r2_absolute_difference": low_difference,
            "static_unique_r2_absolute_difference": unique_difference,
        }
    checks.extend(nuisance_checks)

    compare_expected(
        checks,
        geometry["component_comparison"]["checks"],
        "geometry.reported_checks",
        mismatches,
    )
    compare_expected(
        conjunction(checks),
        geometry["component_comparison"]["mechanical_conjunction"],
        "geometry.reported_conjunction",
        mismatches,
    )
    compare_expected(
        nuisance_checks,
        nuisance["checks"],
        "geometry.reported_nuisance_checks",
        mismatches,
    )
    return checks, {"samples": samples, "order": order, "nuisance": nuisance_summary}


def recompute_target_learning(
    audit: Mapping[str, Any], margins: Mapping[str, Any], mismatches: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trained = audit["trained"]
    learning = trained["target_learning_and_loss"]
    normalized: dict[str, list[Mapping[str, Any]]] = {}
    family_summaries: dict[str, Any] = {}
    for family in ("tribe", "textfeat"):
        rows = sorted(learning[family]["seed_rows"], key=lambda row: int(row["seed"]))
        if [int(row["seed"]) for row in rows] != list(range(6)):
            raise ValueError(f"{family}: expected exactly seeds 0..5")
        target_deltas: list[float] = []
        permuted_deltas: list[float] = []
        for row in rows:
            kd = float(row["kd_target_r2"])
            target_delta = float(row["target_arm_target_r2"]) - kd
            permuted_delta = float(row["permuted_arm_target_r2"]) - kd
            headroom = 1.0 - kd
            compare_expected(
                {
                    "target_minus_kd_delta_r2": target_delta,
                    "permuted_minus_kd_delta_r2": permuted_delta,
                    "remaining_headroom": headroom,
                    "target_headroom_closed": target_delta / headroom if headroom >= 0.05 else None,
                    "headroom_ratio_suppressed": headroom < 0.05,
                },
                row,
                f"trained.{family}.seed{row['seed']}",
                mismatches,
            )
            target_deltas.append(target_delta)
            permuted_deltas.append(permuted_delta)
        target_summary = summary_stats(target_deltas)
        permuted_summary = summary_stats(permuted_deltas)
        compare_expected(
            target_summary,
            learning[family]["target_minus_kd_delta_r2"],
            f"trained.{family}.reported_target_summary",
            mismatches,
        )
        compare_expected(
            permuted_summary,
            learning[family]["permuted_minus_kd_delta_r2"],
            f"trained.{family}.reported_permuted_summary",
            mismatches,
        )
        normalized[family] = rows
        family_summaries[family] = {
            "mean_kd_target_r2": float(np.mean([float(row["kd_target_r2"]) for row in rows])),
            "mean_target_arm_r2": float(
                np.mean([float(row["target_arm_target_r2"]) for row in rows])
            ),
            "mean_remaining_headroom": float(
                np.mean([float(row["remaining_headroom"]) for row in rows])
            ),
            "target_minus_kd": target_summary,
            "permuted_minus_kd": permuted_summary,
        }

    tribe = normalized["tribe"]
    textfeat = normalized["textfeat"]
    baseline = [
        float(left["kd_target_r2"]) - float(right["kd_target_r2"])
        for left, right in zip(tribe, textfeat, strict=True)
    ]
    target_gain = [
        (float(left["target_arm_target_r2"]) - float(left["kd_target_r2"]))
        - (float(right["target_arm_target_r2"]) - float(right["kd_target_r2"]))
        for left, right in zip(tribe, textfeat, strict=True)
    ]
    tribe_headroom = float(np.mean([float(row["remaining_headroom"]) for row in tribe]))
    text_headroom = float(np.mean([float(row["remaining_headroom"]) for row in textfeat]))
    headroom_ratio = (
        tribe_headroom / text_headroom
        if tribe_headroom >= 0.05 and text_headroom >= 0.05
        else None
    )
    checks = [
        margin_check(
            "kd_target_r2_abs_paired_mean_difference",
            abs(float(np.mean(baseline))),
            margins["kd_target_r2_abs_paired_mean_difference"],
        ),
        margin_check(
            "remaining_headroom_mean_ratio",
            headroom_ratio,
            margins["remaining_headroom_mean_ratio"],
            reason="mean remaining headroom below 0.05" if headroom_ratio is None else None,
        ),
    ]
    comparison = trained["target_learning_comparison"]
    compare_expected(checks, comparison["checks"], "trained.reported_target_checks", mismatches)
    compare_expected(
        conjunction(checks),
        comparison["mechanical_conjunction"],
        "trained.reported_target_conjunction",
        mismatches,
    )
    baseline_summary = summary_stats(baseline)
    target_gain_summary = summary_stats(target_gain)
    compare_expected(
        baseline_summary,
        comparison["baseline_predictability_tribe_minus_textfeat"],
        "trained.reported_baseline_summary",
        mismatches,
    )
    compare_expected(
        target_gain_summary,
        comparison["target_gain_tribe_minus_textfeat"],
        "trained.reported_target_gain_summary",
        mismatches,
    )
    compare_expected(
        headroom_ratio,
        comparison["mean_remaining_headroom_ratio_tribe_over_textfeat"],
        "trained.reported_headroom_ratio",
        mismatches,
    )
    return checks, {
        "families": family_summaries,
        "baseline_predictability_tribe_minus_textfeat": baseline_summary,
        "target_gain_tribe_minus_textfeat": target_gain_summary,
        "mean_remaining_headroom_ratio_tribe_over_textfeat": headroom_ratio,
        "checks": checks,
    }


def recompute_parameter_movement(
    audit: Mapping[str, Any], manifest: Mapping[str, Any], margins: Mapping[str, Any], mismatches: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trained = audit["trained"]
    raw = trained["parameter_update_norms"]
    lookup: dict[tuple[str, int, str], Mapping[str, Any]] = {}
    for family, records in raw.items():
        for row in records:
            key = (str(family), int(row["seed"]), str(row["arm"]))
            if key in lookup:
                raise ValueError(f"duplicate parameter-movement row: {key}")
            lookup[key] = row
    checks: list[dict[str, Any]] = []
    differences: list[float] = []
    ratios: list[float] = []
    for seed in range(6):
        left = lookup[("tribe", seed, str(manifest["runs"]["tribe"]["target_arm"]))]["blocks"][
            "global"
        ]["relative_update_l2"]
        right = lookup[
            ("textfeat", seed, str(manifest["runs"]["textfeat"]["target_arm"]))
        ]["blocks"]["global"]["relative_update_l2"]
        left = float(left)
        right = float(right)
        differences.append(left - right)
        ratios.append(left / right)
        if left > float(margins["parameter_update_absolute_floor"]) and right > float(
            margins["parameter_update_absolute_floor"]
        ):
            value = abs(math.log(left / right))
            margin = margins["parameter_update_abs_log_ratio"]
            route = "absolute_log_ratio"
        else:
            value = abs(left - right)
            margin = margins["parameter_update_absolute_floor"]
            route = "absolute_difference_below_floor"
        checks.append(
            {
                "seed": seed,
                "tribe_relative_update_l2": left,
                "textfeat_relative_update_l2": right,
                "route": route,
                "value": value,
                "margin": margin,
                "state": "PASS" if value <= float(margin) else "FAIL",
            }
        )
    comparison = trained["parameter_update_comparison"]
    compare_expected(checks, comparison["checks"], "trained.reported_parameter_checks", mismatches)
    compare_expected(
        checks,
        comparison["blocks"]["global"]["seed_rows"],
        "trained.reported_parameter_global_rows",
        mismatches,
    )
    movement_summary = summary_stats(differences)
    compare_expected(
        movement_summary,
        comparison["blocks"]["global"]["paired_signed_difference"],
        "trained.reported_parameter_summary",
        mismatches,
    )
    compare_expected(
        conjunction(checks),
        comparison["mechanical_conjunction"],
        "trained.reported_parameter_conjunction",
        mismatches,
    )
    return checks, {
        "mean_tribe_relative_update_l2": float(
            np.mean([row["tribe_relative_update_l2"] for row in checks])
        ),
        "mean_textfeat_relative_update_l2": float(
            np.mean([row["textfeat_relative_update_l2"] for row in checks])
        ),
        "tribe_over_textfeat_ratios": ratios,
        "paired_signed_difference": movement_summary,
        "checks": checks,
    }


def recompute_representation_movement(
    audit: Mapping[str, Any], margins: Mapping[str, Any], mismatches: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trained = audit["trained"]
    movement = trained["representation_movement"]
    if movement.get("status") != "available" or movement.get("errors"):
        raise ValueError(f"representation movement unavailable: {movement.get('errors')}")
    if len(movement["records"]) != 96:
        raise ValueError(f"expected 96 representation records, found {len(movement['records'])}")
    primary = [row for row in movement["records"] if row.get("role") == "wikitext_layer6_primary"]
    if len(primary) != 12:
        raise ValueError(f"expected 12 primary representation rows, found {len(primary)}")
    lookup = {(str(row["family"]), int(row["seed"])): row for row in primary}
    if len(lookup) != 12:
        raise ValueError("duplicate primary representation rows")
    noise = movement["duplicate_extraction_noise"]
    duplicate_fro = float(noise["max_centered_relative_frobenius"])
    duplicate_cka = float(noise["max_linear_cka_distance"])
    if not math.isfinite(duplicate_fro) or duplicate_fro < 0:
        raise ValueError("invalid duplicate Frobenius noise")
    if not math.isfinite(duplicate_cka) or duplicate_cka < 0:
        raise ValueError("invalid duplicate CKA noise")
    fro_floor = max(
        1e-12, float(margins["representation_duplicate_noise_multiplier"]) * duplicate_fro
    )
    compare_expected(
        fro_floor,
        noise["centered_relative_frobenius_ratio_floor"],
        "trained.reported_duplicate_fro_floor",
        mismatches,
    )
    checks: list[dict[str, Any]] = []
    seed_rows: list[dict[str, Any]] = []
    cka_signed: list[float] = []
    fro_signed: list[float] = []
    for seed in range(6):
        left = lookup[("tribe", seed)]
        right = lookup[("textfeat", seed)]
        left_cka = float(left["linear_cka_distance"])
        right_cka = float(right["linear_cka_distance"])
        cka_signed.append(left_cka - right_cka)
        cka = margin_check(
            f"seed{seed}:cka_distance",
            abs(left_cka - right_cka),
            margins["representation_cka_distance_abs_difference"],
        )
        left_fro = float(left["centered_relative_frobenius_change"])
        right_fro = float(right["centered_relative_frobenius_change"])
        fro_signed.append(left_fro - right_fro)
        if left_fro > fro_floor and right_fro > fro_floor:
            value = abs(math.log(left_fro / right_fro))
            margin = margins["representation_centered_relative_fro_abs_log_ratio"]
            route = "absolute_log_ratio"
        else:
            value = abs(left_fro - right_fro)
            margin = margins["representation_centered_relative_fro_absolute_floor"]
            route = "absolute_difference_at_or_below_duplicate_floor"
        fro = margin_check(f"seed{seed}:centered_relative_frobenius", value, margin)
        fro["route"] = route
        checks.extend((cka, fro))
        seed_rows.append(
            {
                "seed": seed,
                "tribe": {
                    "cka_distance": left_cka,
                    "centered_relative_frobenius": left_fro,
                },
                "textfeat": {
                    "cka_distance": right_cka,
                    "centered_relative_frobenius": right_fro,
                },
                "checks": [cka, fro],
            }
        )
    comparison = trained["representation_movement_comparison"]
    compare_expected(checks, comparison["checks"], "trained.reported_representation_checks", mismatches)
    compare_expected(seed_rows, comparison["seed_rows"], "trained.reported_representation_rows", mismatches)
    cka_summary = summary_stats(cka_signed)
    fro_summary = summary_stats(fro_signed)
    compare_expected(
        cka_summary,
        comparison["paired_cka_distance_difference"],
        "trained.reported_cka_summary",
        mismatches,
    )
    compare_expected(
        fro_summary,
        comparison["paired_centered_relative_frobenius_difference"],
        "trained.reported_fro_summary",
        mismatches,
    )
    compare_expected(
        conjunction(checks),
        comparison["mechanical_conjunction"],
        "trained.reported_representation_conjunction",
        mismatches,
    )
    return checks, {
        "mean_tribe_cka_distance": float(
            np.mean([row["tribe"]["cka_distance"] for row in seed_rows])
        ),
        "mean_textfeat_cka_distance": float(
            np.mean([row["textfeat"]["cka_distance"] for row in seed_rows])
        ),
        "mean_tribe_centered_relative_frobenius": float(
            np.mean([row["tribe"]["centered_relative_frobenius"] for row in seed_rows])
        ),
        "mean_textfeat_centered_relative_frobenius": float(
            np.mean([row["textfeat"]["centered_relative_frobenius"] for row in seed_rows])
        ),
        "paired_cka_distance_difference": cka_summary,
        "paired_centered_relative_frobenius_difference": fro_summary,
        "duplicate_noise": noise,
        "checks": checks,
    }


def add_dependency(
    dependencies: dict[Path, dict[str, Any]],
    path: str | Path | None,
    expected_sha256: str | None,
    label: str,
    mismatches: list[dict[str, Any]],
) -> None:
    if not path or not expected_sha256:
        mismatches.append({"check": f"dependency.{label}", "error": "missing path or SHA-256"})
        return
    resolved = resolve(path).resolve()
    previous = dependencies.get(resolved)
    if previous and previous["expected_sha256"] != expected_sha256:
        mismatches.append(
            {
                "check": f"dependency.{label}",
                "error": "same path has inconsistent frozen hashes",
                "path": display_path(resolved),
            }
        )
        return
    if previous:
        previous["labels"].append(label)
    else:
        dependencies[resolved] = {"expected_sha256": expected_sha256, "labels": [label]}


def collect_dependencies(
    manifest: Mapping[str, Any], mismatches: list[dict[str, Any]]
) -> dict[Path, dict[str, Any]]:
    dependencies: dict[Path, dict[str, Any]] = {}
    for key in ("audit_script", "owning_e_record"):
        record = manifest[key]
        add_dependency(dependencies, record.get("path"), record.get("sha256"), key, mismatches)
    for record in manifest["runtime_environment"]["environment_files"]:
        add_dependency(dependencies, record.get("path"), record.get("sha256"), "environment", mismatches)
    for family in ("tribe", "textfeat"):
        for split in ("train", "heldout"):
            cache = manifest["target_caches"][family][split]
            add_dependency(
                dependencies, cache.get("path"), cache.get("sha256"), f"target:{family}:{split}", mismatches
            )
            sidecar = cache["sidecar"]
            add_dependency(
                dependencies,
                sidecar.get("path"),
                sidecar.get("sha256"),
                f"sidecar:{family}:{split}",
                mismatches,
            )
        for source in manifest["runs"][family]["sources"]:
            add_dependency(
                dependencies, source.get("path"), source.get("sha256"), f"run:{family}", mismatches
            )
        for row in manifest["runs"][family]["rows"]:
            label = f"{family}:seed{row['seed']}:{row['arm']}"
            add_dependency(
                dependencies,
                row.get("model_weights"),
                row.get("model_weights_sha256"),
                f"weight:{label}",
                mismatches,
            )
            add_dependency(
                dependencies,
                row.get("artifact_manifest"),
                row.get("artifact_manifest_sha256"),
                f"artifact_manifest:{label}",
                mismatches,
            )
    for key in ("nuisance_static_model_provenance", "nuisance_static_tokenizer_provenance"):
        for record in manifest[key]["files"]:
            add_dependency(
                dependencies, record.get("path"), record.get("sha256"), key, mismatches
            )
    context = manifest["context_provenance"]
    add_dependency(dependencies, context.get("path"), context.get("sha256"), "context", mismatches)
    e025 = manifest["e025_representation_provenance"]
    add_dependency(dependencies, e025.get("path"), e025.get("sha256"), "e025_extraction", mismatches)
    base = e025["base_manifest"]
    add_dependency(dependencies, base.get("path"), base.get("sha256"), "e025_manifest", mismatches)
    for record in e025["cache_rows"]:
        add_dependency(
            dependencies,
            record.get("path"),
            record.get("recomputed_sha256"),
            f"e025_representation:{record.get('cache_key')}",
            mismatches,
        )
    for record in base["source_run_jsons"]:
        add_dependency(
            dependencies, record.get("path"), record.get("sha256"), "e025_source_run", mismatches
        )
    for record in base["source_targets"]:
        add_dependency(
            dependencies, record.get("path"), record.get("sha256"), "e025_source_target", mismatches
        )
    return dependencies


def verify_bindings(
    audit: Mapping[str, Any], audit_path: Path, mismatches: list[dict[str, Any]]
) -> dict[str, Any]:
    manifest = audit["manifest"]
    geometry_path = resolve(audit["geometry"]["manifest_path"]).resolve()
    trained_path = resolve(audit["trained"]["manifest_path"]).resolve()
    if geometry_path != trained_path:
        mismatches.append(
            {"check": "binding.manifest_paths", "geometry": str(geometry_path), "trained": str(trained_path)}
        )
    manifest_path = geometry_path
    manifest_sha256 = sha256_file(manifest_path)
    compare_expected(
        manifest_sha256,
        audit["geometry"]["manifest_sha256"],
        "binding.geometry_manifest_sha256",
        mismatches,
    )
    compare_expected(
        manifest_sha256,
        audit["trained"]["manifest_sha256"],
        "binding.trained_manifest_sha256",
        mismatches,
    )
    compare_expected(manifest, load_json(manifest_path), "binding.embedded_manifest", mismatches)

    integrity = manifest["integrity"]
    if integrity.get("errors") or integrity.get("warnings"):
        mismatches.append({"check": "binding.manifest_integrity", "observed": integrity})
    for field in (
        "full_target_hashes_frozen",
        "geometry_sources_ready",
        "target_manifest_valid",
        "trained_representation_sources_ready",
    ):
        if integrity.get(field) is not True:
            mismatches.append({"check": f"binding.integrity.{field}", "observed": integrity.get(field)})

    selftests = manifest["numerical_selftests"]["checks"]
    if len(selftests) != 13 or not all(record.get("pass") is True for record in selftests):
        mismatches.append(
            {"check": "binding.numerical_selftests", "count": len(selftests), "records": selftests}
        )
    for group in ("row_samples", "coordinate_samples"):
        sets: list[set[int]] = []
        for sample in ("A", "B"):
            record = manifest[group][sample]
            ids = [int(value) for value in record["item_ids_sorted"]]
            positions = [int(value) for value in record["row_positions_for_sorted_item_ids"]]
            compare_expected(
                record["item_ids_sha256_int64_le"],
                sha256_int64(ids),
                f"binding.{group}.{sample}.item_hash",
                mismatches,
            )
            compare_expected(
                record["row_positions_sha256_int64_le"],
                sha256_int64(positions),
                f"binding.{group}.{sample}.position_hash",
                mismatches,
            )
            if len(ids) != len(set(ids)) or ids != sorted(ids):
                mismatches.append({"check": f"binding.{group}.{sample}.uniqueness_or_order"})
            sets.append(set(ids))
        if not sets[0].isdisjoint(sets[1]):
            mismatches.append({"check": f"binding.{group}.disjointness"})

    parity_fields = (
        "seed_matched_kd_weights",
        "six_seed_arm_grid",
        "train_and_heldout_item_text_order",
        "train_and_heldout_target_shape",
        "training_budget_and_standardization_metadata",
    )
    for field in parity_fields:
        if manifest["parity_checks"].get(field) is not True:
            mismatches.append({"check": f"binding.parity.{field}"})
    for family in ("tribe", "textfeat"):
        run = manifest["runs"][family]
        expected_grid = {
            (seed, arm)
            for seed in range(6)
            for arm in ("kd_only", str(run["target_arm"]), str(run["permuted_arm"]))
        }
        observed_grid = Counter(
            (int(row["seed"]), str(row["arm"])) for row in manifest["runs"][family]["rows"]
        )
        if set(observed_grid) != expected_grid or any(count != 1 for count in observed_grid.values()):
            mismatches.append(
                {
                    "check": f"binding.arm_seed_grid.{family}",
                    "expected": sorted(expected_grid),
                    "observed": [
                        {"seed": seed, "arm": arm, "count": count}
                        for (seed, arm), count in sorted(observed_grid.items())
                    ],
                }
            )
    identity_fields = (
        "item_indices_sha256_int64_le",
        "texts_sha256_len_prefixed_utf8",
        "vertex_index_sha256_int64_le",
    )
    for split in ("train", "heldout"):
        tribe = manifest["target_caches"]["tribe"][split]
        textfeat = manifest["target_caches"]["textfeat"][split]
        compare_expected(
            tribe["members"]["targets"]["shape"],
            textfeat["members"]["targets"]["shape"],
            f"binding.target_shape.{split}",
            mismatches,
        )
        for field in identity_fields:
            compare_expected(
                tribe["content_identity"][field],
                textfeat["content_identity"][field],
                f"binding.target_identity.{split}.{field}",
                mismatches,
            )
        for family, record in (("tribe", tribe), ("textfeat", textfeat)):
            if record["sidecar"]["semantic_validation"].get("status") != "valid":
                mismatches.append(
                    {"check": f"binding.sidecar_semantics.{family}.{split}", "observed": record["sidecar"]}
                )
    for seed, record in manifest["seed_matched_kd_weight_identity"].items():
        hashes = [family_record["sha256"] for family_record in record["families"].values()]
        if record.get("byte_identical") is not True or len(set(hashes)) != 1:
            mismatches.append({"check": f"binding.seed_matched_kd.{seed}", "observed": record})

    dependencies = collect_dependencies(manifest, mismatches)
    dependency_rows: list[dict[str, Any]] = []
    total_bytes = 0
    bad_count = 0
    for path, record in dependencies.items():
        if not path.exists():
            actual = None
            size = None
            state = "FAIL"
        else:
            size = path.stat().st_size
            total_bytes += size
            actual = sha256_file(path)
            state = "PASS" if actual == record["expected_sha256"] else "FAIL"
        if state != "PASS":
            bad_count += 1
            mismatches.append(
                {
                    "check": "binding.dependency_sha256",
                    "path": display_path(path),
                    "expected": record["expected_sha256"],
                    "observed": actual,
                }
            )
        dependency_rows.append(
            {
                "path": display_path(path),
                "labels": record["labels"],
                "size_bytes": size,
                "expected_sha256": record["expected_sha256"],
                "recomputed_sha256": actual,
                "state": state,
            }
        )
    return {
        "input_audit": {
            "path": display_path(audit_path),
            "sha256": sha256_file(audit_path),
        },
        "manifest": {
            "path": display_path(manifest_path),
            "sha256": manifest_sha256,
            "embedded_object_equals_file": manifest == load_json(manifest_path),
        },
        "main_runner": manifest["audit_script"],
        "owning_e_record": manifest["owning_e_record"],
        "dependency_verification": {
            "state": "PASS" if bad_count == 0 else "FAIL",
            "file_count": len(dependency_rows),
            "total_bytes": total_bytes,
            "failure_count": bad_count,
            "files": sorted(dependency_rows, key=lambda row: row["path"]),
        },
    }


def run_audit(audit_path: Path) -> dict[str, Any]:
    audit = load_json(audit_path)
    if audit.get("schema_version") != "e026-target-comparability-v2" or audit.get("stage") != "all":
        raise ValueError("input is not the retained E026 all-stage audit")
    manifest = audit["manifest"]
    margins = manifest["design_lock"]["margins"]
    mismatches: list[dict[str, Any]] = []

    bindings = verify_bindings(audit, audit_path, mismatches)
    geometry_checks, geometry_summary = recompute_geometry(audit, margins, mismatches)
    target_checks, target_summary = recompute_target_learning(audit, margins, mismatches)
    parameter_checks, parameter_summary = recompute_parameter_movement(
        audit, manifest, margins, mismatches
    )
    representation_checks, representation_summary = recompute_representation_movement(
        audit, margins, mismatches
    )
    trained_checks = target_checks + parameter_checks + representation_checks
    all_checks = geometry_checks + trained_checks
    if len(geometry_checks) != 35 or len(trained_checks) != 20 or len(all_checks) != 55:
        mismatches.append(
            {
                "check": "mechanical_check_count",
                "expected": {"geometry": 35, "trained": 20, "all": 55},
                "observed": {
                    "geometry": len(geometry_checks),
                    "trained": len(trained_checks),
                    "all": len(all_checks),
                },
            }
        )
    compare_expected(
        trained_checks,
        audit["trained"]["mechanical_measured_axis_checks"],
        "trained.reported_combined_checks",
        mismatches,
    )
    compare_expected(
        conjunction(trained_checks),
        audit["trained"]["mechanical_measured_axis_conjunction"],
        "trained.reported_combined_conjunction",
        mismatches,
    )
    overall = conjunction(all_checks)
    expected_top = {
        **overall,
        "classification": (
            "AT_LEAST_ONE_MEASURED_AXIS_FAILS"
            if overall["state"] == "FAIL"
            else ("ALL_MEASURED_AXES_PASS" if overall["state"] == "PASS" else "UNRESOLVED")
        ),
        "initial_gradient_comparability": "UNKNOWN_NOT_RETAINED",
    }
    compare_expected(
        expected_top,
        audit["mechanical_measured_axis_summary"],
        "reported_overall_summary",
        mismatches,
    )
    states = Counter(check["state"] for check in all_checks)
    if states != Counter({"FAIL": 30, "PASS": 24, "UNRESOLVED": 1}):
        mismatches.append(
            {
                "check": "expected_retained_state_counts",
                "expected": {"PASS": 24, "FAIL": 30, "UNRESOLVED": 1},
                "observed": dict(states),
            }
        )

    return {
        "schema_version": "e026-independent-result-audit-v1",
        "experiment": "E026",
        "created_at_utc": utc_now(),
        "science_status": (
            "independent arithmetic and binding verification only; this checker does not settle a scientific verdict"
        ),
        "checker": {
            "path": display_path(Path(__file__)),
            "sha256": sha256_file(Path(__file__)),
            "imports_main_e026_runner": False,
        },
        "verification_state": "PASS" if not mismatches else "FAIL",
        "bindings": bindings,
        "recomputed": {
            "geometry": geometry_summary,
            "target_learning": target_summary,
            "parameter_movement": parameter_summary,
            "representation_movement": representation_summary,
            "mechanical_checks": all_checks,
            "mechanical_summary": {
                **overall,
                "classification": expected_top["classification"],
                "initial_gradient_comparability": "UNKNOWN_NOT_RETAINED",
            },
        },
        "caveats": [
            "The engineering margins are not formal population-equivalence tests.",
            "The six seeds are technical training realizations; target coordinates are not replication units.",
            "Initial standardized auxiliary-loss and gradient comparability was not retained.",
            "The 1024-lag order diagnostic is unresolved because there are no valid within-document pairs.",
            "The selected nuisance ridge alpha is the upper edge of the frozen candidate grid.",
        ],
        "mismatches": mismatches,
    }


def main() -> int:
    args = parse_args()
    audit_path = resolve(args.audit_json).resolve()
    output_path = resolve(args.out).resolve()
    if output_path == audit_path:
        raise ValueError("output must not alias the retained E026 audit JSON")
    try:
        report = run_audit(audit_path)
    except Exception as exc:  # Preserve a machine-readable failure artifact.
        report = {
            "schema_version": "e026-independent-result-audit-v1",
            "experiment": "E026",
            "created_at_utc": utc_now(),
            "science_status": "independent verification failed before completion",
            "checker": {
                "path": display_path(Path(__file__)),
                "sha256": sha256_file(Path(__file__)),
                "imports_main_e026_runner": False,
            },
            "verification_state": "FAIL",
            "mismatches": [{"check": "fatal_exception", "error": f"{type(exc).__name__}: {exc}"}],
        }
    write_json(output_path, report)
    print(
        json.dumps(
            {
                "verification_state": report["verification_state"],
                "mismatch_count": len(report.get("mismatches") or []),
                "output": display_path(output_path),
            },
            sort_keys=True,
        )
    )
    return 0 if report["verification_state"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
