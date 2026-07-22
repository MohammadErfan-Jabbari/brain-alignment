#!/usr/bin/env python3
"""Fail-closed analyzer for E028 synthetic Stage-1 raw results only."""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
from pathlib import Path
from typing import Any, Sequence

_THREAD_ENVIRONMENT_KEYS = (
    "OPENBLAS_NUM_THREADS",
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "BLIS_NUM_THREADS",
)
for _thread_key in _THREAD_ENVIRONMENT_KEYS:
    os.environ[_thread_key] = "1"

import numpy as np
from numpy.polynomial import Polynomial

from e028_vaidya_crossmodal_falsification import (
    AccessSentinel,
    DEFAULT_CONFIG,
    ProtocolError,
    assert_safe_path,
    atomic_write_json,
    build_support,
    canonical_json_bytes,
    load_config,
    sha256_bytes,
    validate_content_hash,
    with_content_hash,
)


ANALYZER_COMMANDS = ("selftest", "analyze-synthetic")


def _exact_keys(value: Any, required: Sequence[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProtocolError(f"{label} must be an object")
    expected = set(required)
    actual = set(value)
    if actual != expected:
        raise ProtocolError(
            f"{label} keys differ; missing={sorted(expected - actual)}, unknown={sorted(actual - expected)}"
        )
    return value


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProtocolError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ProtocolError(f"{label} must be finite")
    return result


def _validate_parameter_array(
    cell: dict[str, Any], key: str, allowed: Sequence[float | int], integer: bool = False
) -> None:
    values = cell[key]
    if not isinstance(values, list) or len(values) != 4:
        raise ProtocolError(f"{key} must contain four outer-fold values")
    allowed_values = {int(value) if integer else float(value) for value in allowed}
    for index, value in enumerate(values):
        numeric = _finite_number(value, f"{key}[{index}]")
        normalized = int(numeric) if integer and numeric.is_integer() else numeric
        if integer and not numeric.is_integer():
            raise ProtocolError(f"{key}[{index}] must be an integer tick")
        if normalized not in allowed_values:
            raise ProtocolError(f"{key}[{index}] is outside the development grid")


def _verify_support(config: dict[str, Any], support: dict[str, Any]) -> None:
    schema = config["raw_result_schema"]
    _exact_keys(support, schema["support_required"], "support")
    unhashed = dict(support)
    claimed = unhashed.pop("support_sha256")
    if not isinstance(claimed, str) or claimed != sha256_bytes(canonical_json_bytes(unhashed)):
        raise ProtocolError("support hash mismatch")
    replay = build_support(config)
    if canonical_json_bytes(replay) != canonical_json_bytes(support):
        raise ProtocolError("support does not byte-replay from the frozen config")
    response_ticks = support["response_ticks"]
    if not isinstance(response_ticks, list) or response_ticks != sorted(set(response_ticks)):
        raise ProtocolError("response ticks are not sorted and unique")
    lag_cfg = config["stage1"]["lag_ticks"]
    expected_lags = list(range(lag_cfg["minimum"], lag_cfg["maximum"] + 1, lag_cfg["step"]))
    lag_rows = support["lag_source_ticks"]
    if not isinstance(lag_rows, list) or len(lag_rows) != len(expected_lags):
        raise ProtocolError("lag-source tick cardinality mismatch")
    for expected_lag, row in zip(expected_lags, lag_rows):
        row = _exact_keys(row, ("lag_tick", "source_ticks"), "lag_source_ticks row")
        if row["lag_tick"] != expected_lag:
            raise ProtocolError("lag-source ticks are out of order")
        if row["source_ticks"] != [tick - expected_lag for tick in response_ticks]:
            raise ProtocolError("lag-source lookup is not absolute k-m")
    for segment in support["segments"]:
        _exact_keys(segment, schema["segment_required"], "segment")
    for fold in support["outer_folds"]:
        _exact_keys(fold, schema["outer_fold_required"], "outer fold")
        if not isinstance(fold["inner_rotations"], list) or len(fold["inner_rotations"]) != 3:
            raise ProtocolError("every outer fold must have three inner rotations")
        for rotation in fold["inner_rotations"]:
            _exact_keys(rotation, schema["inner_rotation_required"], "inner rotation")


def validate_raw(config: dict[str, Any], raw: dict[str, Any]) -> list[dict[str, Any]]:
    schema = config["raw_result_schema"]
    _exact_keys(raw, schema["top_level_required"], "raw result")
    validate_content_hash(raw)
    if raw["schema_version"] != schema["schema_version"] or raw["experiment_id"] != "E028":
        raise ProtocolError("raw result identity mismatch")
    if raw["protocol_state"] != config["protocol_state"]:
        raise ProtocolError("raw protocol-state drift")
    if raw["synthetic_only"] is not True or raw["ready_for_endpoint_access"] is not False:
        raise ProtocolError("analyzer accepts only sealed synthetic development results")
    if raw["readiness_label"] != "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY":
        raise ProtocolError("synthetic readiness label drift")
    provider = _exact_keys(raw["provider"], schema["provider_required"], "provider")
    if provider["provider_id"] != config["synthetic"]["provider_id"]:
        raise ProtocolError("unknown synthetic provider")
    parameters = _exact_keys(
        provider["parameters"], schema["provider_parameters_required"], "provider parameters"
    )
    expected_parameters = {
        key: copy.deepcopy(config["synthetic"][key])
        for key in (
            "ticks_per_contiguous_run",
            "gap_ticks",
            "electrodes_per_patient",
            "nuisance_features",
            "representation_features",
            "development_lag_ticks",
            "development_ridge_alpha",
            "development_representation_penalty_ratio",
        )
    }
    expected_parameters["patient_ids"] = config["stage1"]["patient_ids"]
    expected_parameters["source_ids"] = config["stage1"]["source_ids"]
    if canonical_json_bytes(parameters) != canonical_json_bytes(expected_parameters):
        raise ProtocolError("synthetic provider parameter drift")
    if provider["identity_sha256"] != sha256_bytes(canonical_json_bytes(parameters)):
        raise ProtocolError("synthetic provider identity mismatch")
    if provider["rng_domain"] != config["synthetic"]["rng_domain"]:
        raise ProtocolError("synthetic RNG domain drift")
    _verify_support(config, raw["support"])
    sentinel = _exact_keys(raw["sentinels"], schema["sentinels_required"], "sentinels")
    if (
        sentinel["path_network_sentinel_active"] is not True
        or sentinel["forbidden_access_attempts"] != []
        or sentinel["network_attempts"] != 0
        or sentinel["forbidden_roots"] != config["forbidden_path_components"]
        or sentinel["status"] != "PASS"
    ):
        raise ProtocolError("synthetic runner sentinel did not pass cleanly")
    cells = raw["cells"]
    if not isinstance(cells, list):
        raise ProtocolError("cells must be an array")
    patients = list(config["stage1"]["patient_ids"])
    sources = list(config["stage1"]["source_ids"])
    electrodes = [
        f"synthetic-e{index + 1:02d}"
        for index in range(int(config["synthetic"]["electrodes_per_patient"]))
    ]
    arms = list(schema["arms"])
    expected_n_test = {
        int(fold["outer_block"]): len(fold["post_embargo"]["outer_test"])
        for fold in raw["support"]["outer_folds"]
    }
    expected_keys = {
        (patient, electrode, source, arm)
        for patient in patients
        for electrode in electrodes
        for source in sources
        for arm in arms
    }
    seen: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for cell_index, cell_value in enumerate(cells):
        cell = _exact_keys(cell_value, schema["cell_required"], f"cell[{cell_index}]")
        key = (cell["patient_id"], cell["electrode_id"], cell["source_id"], cell["arm"])
        if key not in expected_keys:
            raise ProtocolError(f"unknown cell identity: {key}")
        if key in seen:
            raise ProtocolError(f"duplicate cell identity: {key}")
        _validate_parameter_array(
            cell, "selected_lag_tick", config["synthetic"]["development_lag_ticks"], integer=True
        )
        _validate_parameter_array(cell, "selected_alpha", config["synthetic"]["development_ridge_alpha"])
        _validate_parameter_array(
            cell,
            "selected_rho",
            config["synthetic"]["development_representation_penalty_ratio"],
        )
        _validate_parameter_array(
            cell, "selected_nuisance_alpha", config["synthetic"]["development_ridge_alpha"]
        )
        _validate_parameter_array(
            cell, "selected_x_only_alpha", config["synthetic"]["development_ridge_alpha"]
        )
        correlation = _finite_number(cell["x_only_pearson_r"], "x_only_pearson_r")
        if not (-1.0 < correlation < 1.0):
            raise ProtocolError("x_only_pearson_r must be strictly inside (-1,1)")
        folds = cell["fold_accumulators"]
        if not isinstance(folds, list) or len(folds) != 4:
            raise ProtocolError("each cell requires four fold accumulators")
        blocks = []
        for fold_index, accumulator in enumerate(folds):
            accumulator = _exact_keys(
                accumulator, schema["fold_accumulator_required"], f"cell[{cell_index}] fold[{fold_index}]"
            )
            block = accumulator["block"]
            if isinstance(block, bool) or not isinstance(block, int):
                raise ProtocolError("fold block must be an integer")
            blocks.append(block)
            for numeric_key in ("sse_full", "sse_nuisance", "sst"):
                value = _finite_number(accumulator[numeric_key], numeric_key)
                if value < 0 or (numeric_key == "sst" and value <= 0):
                    raise ProtocolError(f"invalid {numeric_key}")
            if isinstance(accumulator["n_test"], bool) or not isinstance(accumulator["n_test"], int) or accumulator["n_test"] < 2:
                raise ProtocolError("invalid n_test")
            if block not in expected_n_test or accumulator["n_test"] != expected_n_test[block]:
                raise ProtocolError("n_test does not match replayed post-embargo outer-test support")
        if blocks != [0, 1, 2, 3]:
            raise ProtocolError("fold accumulators must be in outer-block order 0..3")
        seen[key] = cell
    if set(seen) != expected_keys:
        missing = sorted(expected_keys - set(seen))
        raise ProtocolError(f"missing required cells: {missing[:3]} (total {len(missing)})")
    for patient in patients:
        for electrode in electrodes:
            reference_f = seen[(patient, electrode, sources[0], "F")]
            reference_payload = {
                key: value
                for key, value in reference_f.items()
                if key not in {"patient_id", "electrode_id", "source_id", "arm"}
            }
            for source in sources:
                frozen = seen[(patient, electrode, source, "F")]
                frozen_payload = {
                    key: value
                    for key, value in frozen.items()
                    if key not in {"patient_id", "electrode_id", "source_id", "arm"}
                }
                if canonical_json_bytes(frozen_payload) != canonical_json_bytes(reference_payload):
                    raise ProtocolError("F numerical payload differs across sources")
                tuned = seen[(patient, electrode, source, "B_1")]
                if tuned["selected_lag_tick"] != reference_f["selected_lag_tick"]:
                    raise ProtocolError("B_1 changed the frozen F lag")
                if tuned["selected_nuisance_alpha"] != reference_f["selected_nuisance_alpha"]:
                    raise ProtocolError("B_1 changed the shared nuisance alpha")
            for block in range(4):
                shared = None
                for source in sources:
                    for arm in arms:
                        accumulator = seen[(patient, electrode, source, arm)]["fold_accumulators"][block]
                        signature = canonical_json_bytes(
                            {
                                "block": accumulator["block"],
                                "sse_nuisance": accumulator["sse_nuisance"],
                                "sst": accumulator["sst"],
                                "n_test": accumulator["n_test"],
                            }
                        )
                        if shared is None:
                            shared = signature
                        elif signature != shared:
                            raise ProtocolError("shared nuisance/SST accumulator drift across arm or source")
    return cells


def _cell_m(cell: dict[str, Any], omit_block: int | None = None) -> float:
    folds = [row for row in cell["fold_accumulators"] if row["block"] != omit_block]
    if not folds:
        raise ProtocolError("leave-one-block removed every fold")
    sse_full = math.fsum(float(row["sse_full"]) for row in folds)
    sse_nuisance = math.fsum(float(row["sse_nuisance"]) for row in folds)
    sst = math.fsum(float(row["sst"]) for row in folds)
    if not math.isfinite(sst) or sst <= 0:
        raise ProtocolError("invalid pooled SST")
    result = (sse_nuisance - sse_full) / sst
    if not math.isfinite(result):
        raise ProtocolError("nonfinite nuisance-subtracted score")
    return result


def _patient_contrasts(
    config: dict[str, Any],
    cells: list[dict[str, Any]],
    omit_source: str | None = None,
    omit_block: int | None = None,
) -> tuple[dict[str, float], dict[str, float]]:
    patients = config["stage1"]["patient_ids"]
    sources = [source for source in config["stage1"]["source_ids"] if source != omit_source]
    if not sources:
        raise ProtocolError("no source remains")
    indexed = {
        (cell["patient_id"], cell["electrode_id"], cell["source_id"], cell["arm"]): cell
        for cell in cells
    }
    electrodes = sorted({cell["electrode_id"] for cell in cells})
    patient_values: dict[str, float] = {}
    source_values: dict[str, float] = {}
    for patient in patients:
        by_source = []
        for source in sources:
            frozen = math.fsum(
                _cell_m(indexed[(patient, electrode, source, "F")], omit_block) for electrode in electrodes
            ) / len(electrodes)
            tuned = math.fsum(
                _cell_m(indexed[(patient, electrode, source, "B_1")], omit_block) for electrode in electrodes
            ) / len(electrodes)
            by_source.append(tuned - frozen)
        patient_values[patient] = math.fsum(by_source) / len(by_source)
    for source in sources:
        values = []
        for patient in patients:
            frozen = math.fsum(
                _cell_m(indexed[(patient, electrode, source, "F")], omit_block) for electrode in electrodes
            ) / len(electrodes)
            tuned = math.fsum(
                _cell_m(indexed[(patient, electrode, source, "B_1")], omit_block) for electrode in electrodes
            ) / len(electrodes)
            values.append(tuned - frozen)
        source_values[source] = math.fsum(values) / len(values)
    return patient_values, source_values


def _fisher_contrast(config: dict[str, Any], cells: list[dict[str, Any]]) -> tuple[dict[str, float], float]:
    patients = config["stage1"]["patient_ids"]
    sources = config["stage1"]["source_ids"]
    electrodes = sorted({cell["electrode_id"] for cell in cells})
    indexed = {
        (cell["patient_id"], cell["electrode_id"], cell["source_id"], cell["arm"]): cell
        for cell in cells
    }
    patient_values = {}
    for patient in patients:
        source_values = []
        for source in sources:
            frozen = math.fsum(
                math.atanh(float(indexed[(patient, electrode, source, "F")]["x_only_pearson_r"]))
                for electrode in electrodes
            ) / len(electrodes)
            tuned = math.fsum(
                math.atanh(float(indexed[(patient, electrode, source, "B_1")]["x_only_pearson_r"]))
                for electrode in electrodes
            ) / len(electrodes)
            source_values.append(tuned - frozen)
        patient_values[patient] = math.fsum(source_values) / len(source_values)
    return patient_values, math.fsum(patient_values.values()) / len(patient_values)


def _sign_matrix(n: int) -> np.ndarray:
    if n != 9:
        raise ProtocolError("E028 sign inference is frozen to nine patients")
    return np.asarray(
        [[1.0 if mask & (1 << index) else -1.0 for index in range(n)] for mask in range(2**n)],
        dtype=np.float64,
    )


def _global_denominator_check(d: np.ndarray, floor: float) -> None:
    n = len(d)
    total = float(np.sum(d))
    square = float(d @ d)
    constant = n * square - total * total
    if not math.isfinite(constant) or constant < 0:
        raise ProtocolError("invalid sign-statistic constant")
    for signs in _sign_matrix(n):
        signed_total = float(signs @ d)
        sign_sum = float(np.sum(signs))
        if abs(sign_sum) == n:
            g_min = constant
        else:
            theta = (n * total - signed_total * sign_sum) / (n * n - sign_sum * sign_sum)
            n_zero = total - n * theta
            n_sign = signed_total - sign_sum * theta
            g_min = constant + n_zero * n_zero - n_sign * n_sign
        denominator = math.sqrt(max(g_min, 0.0)) / (n * math.sqrt(n - 1))
        if not math.isfinite(denominator) or denominator < floor:
            raise ProtocolError("a required sign-statistic denominator is below the frozen floor")


def _statistics(d: np.ndarray, theta: float, floor: float) -> np.ndarray:
    residual = d - theta
    signed = _sign_matrix(len(d)) * residual[None, :]
    denominator = np.std(signed, axis=1, ddof=1) / math.sqrt(len(d))
    if np.any(~np.isfinite(denominator)) or np.any(denominator < floor):
        raise ProtocolError("undefined sign statistic")
    statistic = np.mean(signed, axis=1) / denominator
    if np.any(~np.isfinite(statistic)):
        raise ProtocolError("nonfinite sign statistic")
    return statistic


def exact_sign_count(d: np.ndarray, theta: float, tie_tolerance: float, floor: float) -> int:
    statistic = _statistics(d, theta, floor)
    observed = statistic[-1]
    return int(np.count_nonzero(statistic >= observed - tie_tolerance))


def _direct_difference(
    normalized_d: np.ndarray, z: float, signs: np.ndarray, tie_tolerance: float
) -> float:
    return _branch_difference(normalized_d, z, signs, tie_tolerance, intended=True)


def _branch_difference(
    normalized_d: np.ndarray,
    z: float,
    signs: np.ndarray,
    tie_tolerance: float,
    intended: bool,
) -> float:
    n = len(normalized_d)
    total = float(np.sum(normalized_d))
    square = float(normalized_d @ normalized_d)
    constant = n * square - total * total
    n_zero = total - n * z
    signed_total = float(signs @ normalized_d)
    sign_sum = float(np.sum(signs))
    n_sign = signed_total - sign_sum * z
    g = constant + n_zero * n_zero - n_sign * n_sign
    if g <= 0 or constant <= 0:
        raise ProtocolError("nonpositive closed-form sign denominator")
    signed_term = n_sign / math.sqrt(g)
    comparison_term = n_zero / math.sqrt(constant) - tie_tolerance / math.sqrt(n - 1)
    return math.sqrt(n - 1) * (
        signed_term - comparison_term if intended else signed_term + comparison_term
    )


def _refine_branch_root(
    normalized_d: np.ndarray,
    signs: np.ndarray,
    candidate: float,
    tie_tolerance: float,
    intended: bool,
) -> float:
    n = len(normalized_d)
    total = float(np.sum(normalized_d))
    square = float(normalized_d @ normalized_d)
    constant = n * square - total * total
    signed_total = float(signs @ normalized_d)
    sign_sum = float(np.sum(signs))
    z = float(candidate)
    for _ in range(24):
        n_zero = total - n * z
        n_sign = signed_total - sign_sum * z
        g = constant + n_zero * n_zero - n_sign * n_sign
        if g <= 0:
            break
        g_prime = -2.0 * n * n_zero + 2.0 * sign_sum * n_sign
        signed_derivative = -sign_sum / math.sqrt(g) - 0.5 * n_sign * g_prime / (g ** 1.5)
        comparison_derivative = -n / math.sqrt(constant)
        derivative = math.sqrt(n - 1) * (
            signed_derivative - comparison_derivative
            if intended
            else signed_derivative + comparison_derivative
        )
        value = _branch_difference(normalized_d, z, signs, tie_tolerance, intended)
        if abs(value) <= 5e-13:
            return z
        if not math.isfinite(derivative) or abs(derivative) < 1e-14:
            break
        proposal = z - value / derivative
        if not math.isfinite(proposal):
            break
        z = proposal
    value = _branch_difference(normalized_d, z, signs, tie_tolerance, intended)
    if abs(value) > 5e-10:
        branch = "intended" if intended else "opposite squared"
        raise ProtocolError(f"{branch} threshold root failed unsquared verification")
    return z


def _refine_root(
    normalized_d: np.ndarray,
    signs: np.ndarray,
    candidate: float,
    tie_tolerance: float,
) -> float:
    return _refine_branch_root(normalized_d, signs, candidate, tie_tolerance, intended=True)


def _threshold_events(d: np.ndarray, tie_tolerance: float) -> list[float]:
    center = float(np.mean(d))
    scale = max(float(np.ptp(d)), float(np.std(d)), np.finfo(float).tiny)
    normalized = (d - center) / scale
    n = len(normalized)
    total = float(np.sum(normalized))
    square = float(normalized @ normalized)
    constant = n * square - total * total
    if constant <= 0 or not math.isfinite(constant):
        raise ProtocolError("observed sign denominator is undefined")
    n_zero = Polynomial([total, -float(n)])
    epsilon = tie_tolerance / math.sqrt(n - 1)
    comparison = n_zero / math.sqrt(constant) - epsilon
    events: list[float] = []
    signs_all = _sign_matrix(n)
    for signs in signs_all[:-1]:  # all-positive is an identity, not an event.
        signed_total = float(signs @ normalized)
        sign_sum = float(np.sum(signs))
        n_sign = Polynomial([signed_total, -sign_sum])
        g = Polynomial([constant]) + n_zero * n_zero - n_sign * n_sign
        polynomial = n_sign * n_sign - comparison * comparison * g
        coefficients = np.trim_zeros(np.asarray(polynomial.coef, dtype=np.float64), trim="b")
        if len(coefficients) <= 1:
            raise ProtocolError("degenerate threshold-event polynomial")
        roots = Polynomial(coefficients).roots()
        real_candidates = []
        for root in roots:
            if abs(float(np.imag(root))) <= 2e-8 * (1.0 + abs(float(np.real(root)))):
                real_candidates.append(float(np.real(root)))
        for candidate in real_candidates:
            intended_distance = abs(
                _branch_difference(normalized, candidate, signs, tie_tolerance, intended=True)
            )
            opposite_distance = abs(
                _branch_difference(normalized, candidate, signs, tie_tolerance, intended=False)
            )
            if intended_distance <= opposite_distance:
                refined = _refine_branch_root(
                    normalized, signs, candidate, tie_tolerance, intended=True
                )
                if abs(_direct_difference(normalized, refined, signs, tie_tolerance)) > 5e-10:
                    raise ProtocolError("unverified intended threshold event")
                events.append(center + scale * refined)
            else:
                extraneous = _refine_branch_root(
                    normalized, signs, candidate, tie_tolerance, intended=False
                )
                if abs(
                    _branch_difference(
                        normalized, extraneous, signs, tie_tolerance, intended=False
                    )
                ) > 5e-10:
                    raise ProtocolError("unverified opposite-branch polynomial root")
    if not events:
        raise ProtocolError("no verified threshold events")
    events.sort()
    unique = [events[0]]
    for event in events[1:]:
        tolerance = max(32 * math.ulp(max(abs(event), abs(unique[-1]), 1.0)), 1e-13 * scale)
        if abs(event - unique[-1]) > tolerance:
            unique.append(event)
    return unique


def invert_sign_bound(
    values: Sequence[float],
    family_size: int,
    tie_tolerance: float,
    denominator_floor: float,
    width_max: float,
) -> dict[str, Any]:
    d = np.asarray(values, dtype=np.float64)
    if d.shape != (9,) or not np.all(np.isfinite(d)):
        raise ProtocolError("sign inversion requires nine finite patient values")
    if family_size not in (1, 2, 3):
        raise ProtocolError("unsupported Bonferroni family size")
    minimum_count = math.floor(512 * 0.05 / family_size) + 1
    expected = {1: 26, 2: 13, 3: 9}[family_size]
    if minimum_count != expected:
        raise ProtocolError("Bonferroni accepted-count contract drift")
    _global_denominator_check(d, denominator_floor)
    if tie_tolerance == 0:
        events = sorted(
            float(np.mean(d[[index for index in range(9) if mask & (1 << index)]]))
            for mask in range(1, 512)
        )
        boundary = events[minimum_count - 2]
        unique_events = sorted(set(events))
    else:
        unique_events = _threshold_events(d, tie_tolerance)
        span = max(float(np.ptp(d)), 1.0)
        samples = [unique_events[0] - span]
        samples.extend((left + right) / 2.0 for left, right in zip(unique_events[:-1], unique_events[1:]))
        samples.append(unique_events[-1] + span)
        accepted = [
            exact_sign_count(d, sample, tie_tolerance, denominator_floor) >= minimum_count
            for sample in samples
        ]
        transitions = [index for index in range(1, len(accepted)) if not accepted[index - 1] and accepted[index]]
        if accepted[0] or not accepted[-1] or len(transitions) != 1:
            raise ProtocolError("sign-flip acceptance set is not one upper interval")
        transition = transitions[0]
        if any(accepted[:transition]) or not all(accepted[transition:]):
            raise ProtocolError("sign-flip acceptance intervals are nonmonotone")
        boundary = unique_events[transition - 1]
        root_status = [
            exact_sign_count(d, event, tie_tolerance, denominator_floor) >= minimum_count
            for event in unique_events
        ]
        if any(root_status[: transition - 1]) or not all(root_status[transition:]):
            raise ProtocolError("accepted singleton or rejected point violates upper-interval form")
    span = max(float(np.ptp(d)), 1.0)
    left = boundary - span
    right = boundary + span
    while exact_sign_count(d, left, tie_tolerance, denominator_floor) >= minimum_count:
        span *= 2.0
        left = boundary - span
        if not math.isfinite(left):
            raise ProtocolError("cannot bracket rejected lower tail")
    while exact_sign_count(d, right, tie_tolerance, denominator_floor) < minimum_count:
        span *= 2.0
        right = boundary + span
        if not math.isfinite(right):
            raise ProtocolError("cannot bracket accepted upper tail")
    for _ in range(256):
        if right - left <= width_max:
            break
        middle = (left + right) / 2.0
        if middle == left or middle == right:
            break
        if exact_sign_count(d, middle, tie_tolerance, denominator_floor) >= minimum_count:
            right = middle
        else:
            left = middle
    if right - left > width_max:
        raise ProtocolError("confidence-bound bracket exceeds frozen maximum width")
    below_count = exact_sign_count(d, left, tie_tolerance, denominator_floor)
    above_count = exact_sign_count(d, right, tie_tolerance, denominator_floor)
    if below_count >= minimum_count or above_count < minimum_count:
        raise ProtocolError("confidence-bound bracket does not straddle rejection/acceptance")
    return {
        "family_size": family_size,
        "minimum_accepted_count": minimum_count,
        "lower_bound": (left + right) / 2.0,
        "lower_bound_bracket": [left, right],
        "bracket_width": right - left,
        "sign_count_immediately_below": below_count,
        "sign_count_immediately_above": above_count,
        "verified_threshold_events": len(unique_events),
    }


def _bounds(config: dict[str, Any], values: Sequence[float], family_size: int) -> dict[str, Any]:
    stage = config["stage1"]
    lower = invert_sign_bound(
        values,
        family_size,
        float(stage["sign_tie_tolerance"]),
        float(stage["sign_denominator_floor"]),
        float(stage["boundary_width_max"]),
    )
    upper_inverted = invert_sign_bound(
        [-float(value) for value in values],
        family_size,
        float(stage["sign_tie_tolerance"]),
        float(stage["sign_denominator_floor"]),
        float(stage["boundary_width_max"]),
    )
    result = dict(lower)
    result["upper_bound"] = -float(upper_inverted["lower_bound"])
    result["upper_bound_bracket"] = [
        -float(upper_inverted["lower_bound_bracket"][1]),
        -float(upper_inverted["lower_bound_bracket"][0]),
    ]
    return result


def analyze(config: dict[str, Any], raw: dict[str, Any]) -> dict[str, Any]:
    cells = validate_raw(config, raw)
    patient_values, source_values = _patient_contrasts(config, cells)
    ordered_patients = config["stage1"]["patient_ids"]
    vector = [patient_values[patient] for patient in ordered_patients]
    fisher_patients, fisher_mean = _fisher_contrast(config, cells)
    leave_one_patient = {
        patient: math.fsum(value for other, value in patient_values.items() if other != patient) / 8.0
        for patient in ordered_patients
    }
    leave_one_source = {}
    for source in config["stage1"]["source_ids"]:
        values, _ = _patient_contrasts(config, cells, omit_source=source)
        leave_one_source[source] = math.fsum(values.values()) / len(values)
    leave_one_block = {}
    for block in range(4):
        values, _ = _patient_contrasts(config, cells, omit_block=block)
        leave_one_block[str(block)] = math.fsum(values.values()) / len(values)
    inference_error = None
    inference = None
    try:
        inference = _bounds(config, vector, family_size=1)
    except ProtocolError as exc:
        inference_error = str(exc)
    positive_patients = sum(value > 0 for value in vector)
    diagnostics_positive = (
        all(value > 0 for value in source_values.values())
        and all(value > 0 for value in leave_one_patient.values())
        and all(value > 0 for value in leave_one_source.values())
        and all(value > 0 for value in leave_one_block.values())
    )
    statistical_gate = bool(
        inference is not None
        and inference["lower_bound_bracket"][0] > 0
        and positive_patients >= 8
        and diagnostics_positive
        and fisher_mean > 0
    )
    payload = {
        "schema_version": "e028-stage1-synthetic-analysis-v1",
        "experiment_id": "E028",
        "input_content_sha256": raw["content_sha256"],
        "synthetic_only": True,
        "ready_for_endpoint_access": False,
        "readiness_label": "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY",
        "validity": {
            "raw_schema_and_hash": "PASS",
            "support_replay": "PASS",
            "cell_cardinality": len(cells),
            "shared_nuisance_and_sst": "PASS",
            "frozen_f_payload_copy": "PASS",
            "inference": "PASS" if inference is not None else "INCONCLUSIVE",
            "inference_error": inference_error,
        },
        "estimand": "equal-patient mean of b_1(u), with equal electrodes then equal sources",
        "estimates": {
            "patient_b1": patient_values,
            "mean_b1": math.fsum(vector) / len(vector),
            "source_b1": source_values,
            "fisher_z_patient_b1": fisher_patients,
            "fisher_z_mean_b1": fisher_mean,
            "leave_one_patient_mean_b1": leave_one_patient,
            "leave_one_source_mean_b1": leave_one_source,
            "leave_one_block_mean_b1": leave_one_block,
        },
        "inference": inference,
        "synthetic_statistical_gate": {
            "passed": statistical_gate,
            "positive_patients": positive_patients,
            "required_positive_patients": 8,
            "all_source_aggregates_positive": all(value > 0 for value in source_values.values()),
            "fisher_z_direction_positive": fisher_mean > 0,
            "all_leave_one_diagnostics_positive": diagnostics_positive,
        },
        "exact_lane_available_or_reimplementation_approved": False,
        "stage2_licensed": False,
        "verdict": (
            "SYNTHETIC STATISTICAL FIXTURE PASS; DEVELOPMENT SLICE ONLY; NOT READY"
            if statistical_gate
            else "SYNTHETIC STAGE-1 INCONCLUSIVE OR GATE-NEGATIVE; NOT READY"
        ),
    }
    return with_content_hash(payload)


def selftest(config: dict[str, Any]) -> dict[str, Any]:
    checks = []
    expected = {
        1: (3.25, 6.75, 26),
        2: (2.75, 7.25, 13),
        3: (2.5, 7.5, 9),
    }
    values = np.arange(1.0, 10.0)
    for family_size, (lower_expected, upper_expected, count_expected) in expected.items():
        lower = invert_sign_bound(values, family_size, 0.0, 1e-12, 1e-10)
        upper = -invert_sign_bound(-values, family_size, 0.0, 1e-12, 1e-10)["lower_bound"]
        if abs(lower["lower_bound"] - lower_expected) > 1e-9 or abs(upper - upper_expected) > 1e-9:
            raise ProtocolError(f"J={family_size} zero-tolerance bound fixture failed")
        if lower["minimum_accepted_count"] != count_expected:
            raise ProtocolError(f"J={family_size} accepted-count fixture failed")
    checks.append("bonferroni-zero-tolerance-fixtures")
    tie = float(config["stage1"]["sign_tie_tolerance"])
    scaled = 1000.0 * values
    literal = invert_sign_bound(scaled, 1, tie, 1e-12, 1e-10)
    if not (3249.999999 < literal["lower_bound"] < 3250.0):
        raise ProtocolError("literal tie-tolerance threshold-root fixture failed")
    if exact_sign_count(scaled, 3250.0 - 1e-9, tie, 1e-12) != 23:
        raise ProtocolError("literal tie-tolerance rejection count fixture failed")
    if exact_sign_count(scaled, 3250.0 - 5e-10, tie, 1e-12) != 26:
        raise ProtocolError("literal tie-tolerance acceptance count fixture failed")
    checks.append("literal-tolerance-threshold-roots")
    try:
        invert_sign_bound(np.ones(9), 1, tie, 1e-12, 1e-10)
    except ProtocolError:
        pass
    else:
        raise ProtocolError("constant-vector denominator fixture failed")
    try:
        invert_sign_bound(np.asarray([-1.0] * 4 + [1.0] * 5), 1, tie, 1e-12, 1e-10)
    except ProtocolError:
        pass
    else:
        raise ProtocolError("permuted-sign denominator fixture failed")
    checks.append("denominator-fail-closed")
    permuted = values[[8, 0, 5, 2, 7, 1, 6, 3, 4]]
    base = invert_sign_bound(values, 1, 0.0, 1e-12, 1e-10)["lower_bound"]
    if abs(invert_sign_bound(permuted, 1, 0.0, 1e-12, 1e-10)["lower_bound"] - base) > 1e-10:
        raise ProtocolError("permutation equivariance fixture failed")
    if abs(invert_sign_bound(values + 17.0, 1, 0.0, 1e-12, 1e-10)["lower_bound"] - (base + 17.0)) > 1e-9:
        raise ProtocolError("translation equivariance fixture failed")
    if abs(invert_sign_bound(values * 3.0, 1, 0.0, 1e-12, 1e-10)["lower_bound"] - 3.0 * base) > 1e-9:
        raise ProtocolError("scale equivariance fixture failed")
    checks.append("sign-inversion-equivariance")
    fold_fixture = {
        "fold_accumulators": [
            {"block": 0, "sse_full": 1.0, "sse_nuisance": 2.0, "sst": 10.0, "n_test": 2},
            {"block": 1, "sse_full": 9.0, "sse_nuisance": 10.0, "sst": 100.0, "n_test": 2},
            {"block": 2, "sse_full": 2.0, "sse_nuisance": 5.0, "sst": 20.0, "n_test": 2},
            {"block": 3, "sse_full": 18.0, "sse_nuisance": 20.0, "sst": 200.0, "n_test": 2},
        ]
    }
    pooled = _cell_m(fold_fixture)
    naive = np.mean([(2.0 - 1.0) / 10.0, (10.0 - 9.0) / 100.0, (5.0 - 2.0) / 20.0, (20.0 - 18.0) / 200.0])
    if not math.isclose(pooled, 7.0 / 330.0) or math.isclose(pooled, float(naive)):
        raise ProtocolError("four-block pooled estimator fixture failed to distinguish naive averaging")
    if not math.isclose(_cell_m(fold_fixture, 0), 6.0 / 320.0):
        raise ProtocolError("no-refit pooled leave-one-block fixture failed")
    checks.append("no-refit-pooled-aggregation")
    return {
        "status": "PASS",
        "checks": checks,
        "synthetic_only": True,
        "ready_for_endpoint_access": False,
        "readiness_label": "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY",
    }


def _load_raw(path: Path, config: dict[str, Any]) -> dict[str, Any]:
    assert_safe_path(path, config["forbidden_path_components"])
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProtocolError(f"cannot load synthetic raw result: {exc}") from exc
    if not isinstance(value, dict):
        raise ProtocolError("synthetic raw result must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=ANALYZER_COMMANDS)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if tuple(config["command_allowlists"]["analyzer"]) != ANALYZER_COMMANDS:
            raise ProtocolError("analyzer command allowlist drift")
        with AccessSentinel(config["forbidden_path_components"]) as sentinel:
            if args.command == "selftest":
                if args.input is not None or args.output is not None:
                    raise ProtocolError("selftest accepts no input or output artifact")
                result = selftest(config)
            elif args.command == "analyze-synthetic":
                if args.input is None or args.output is None:
                    raise ProtocolError("analyze-synthetic requires --input and --output")
                raw = _load_raw(args.input, config)
                result = analyze(config, raw)
                atomic_write_json(args.output, result, config["forbidden_path_components"])
            else:  # pragma: no cover
                raise ProtocolError(f"command not allowed: {args.command}")
            if sentinel.forbidden_attempts or sentinel.network_attempts:
                raise ProtocolError("sentinel observed a forbidden analyzer access")
    except ProtocolError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        return 2
    summary = {
        "status": result.get("status", "PASS"),
        "command": args.command,
        "synthetic_only": True,
        "ready_for_endpoint_access": False,
        "readiness_label": result.get("readiness_label"),
        "content_sha256": result.get("content_sha256"),
    }
    if args.command == "selftest":
        summary["checks"] = result["checks"]
    else:
        summary["verdict"] = result["verdict"]
        summary["synthetic_statistical_gate_passed"] = result["synthetic_statistical_gate"]["passed"]
        summary["stage2_licensed"] = False
    print(json.dumps(summary, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
