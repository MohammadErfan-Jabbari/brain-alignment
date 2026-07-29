#!/usr/bin/env python3
"""Fail-closed preflight and numerical core for E032.

This executable deliberately separates acquisition integrity from neural scoring.
With the frozen configuration's authorization flags set to false, only
``selftest`` and ``manifest`` are available. The current implementation does not
claim endpoint readiness: builder, score, and analyze stop before reading neural
channels until their full nuisance and provenance pipeline has passed review.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
from scipy import linalg


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "configs/e032_kymata_cross_run_repeat_recovery.json"
IMPLEMENTED_STAGES = {"selftest", "manifest", "acquire", "integrity"}
ENDPOINT_STAGES = {"builder", "score", "analyze"}


class E032Error(RuntimeError):
    """Expected fail-closed E032 error."""


def sha256_file(path: Path, chunk_bytes: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_bytes)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def require_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise E032Error(f"CONFIG_INVALID: {name} must be an object")
    return value


def require_keys(mapping: dict[str, Any], keys: Iterable[str], name: str) -> None:
    missing = sorted(set(keys) - set(mapping))
    if missing:
        raise E032Error(f"CONFIG_INVALID: {name} missing {missing}")


def load_config(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
        config = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise E032Error(f"CONFIG_INVALID: {exc}") from exc

    require_keys(
        config,
        {
            "schema_version",
            "experiment",
            "authorization",
            "paths",
            "dataset",
            "files",
            "integrity",
            "preprocessing",
            "nuisance",
            "corrca",
            "split",
            "controls",
            "gates",
            "bootstrap",
        },
        "root",
    )
    if config["experiment"] != "E032" or config["schema_version"] != "1.0":
        raise E032Error("CONFIG_INVALID: wrong experiment or schema version")

    authorization = require_mapping(config["authorization"], "authorization")
    require_keys(
        authorization,
        {"work_e032_authorized", "participant_raw_access_allowed"},
        "authorization",
    )
    if not all(isinstance(authorization[key], bool) for key in authorization):
        raise E032Error("CONFIG_INVALID: authorization values must be booleans")

    dataset = require_mapping(config["dataset"], "dataset")
    require_keys(
        dataset,
        {
            "subject",
            "builder_runs",
            "evaluation_runs",
            "exposures_per_run",
            "event_code",
            "sampling_frequency_hz",
            "stimulus_duration_seconds",
            "expected_channels",
        },
        "dataset",
    )
    if dataset["builder_runs"] != [1, 3] or dataset["evaluation_runs"] != [2, 4]:
        raise E032Error("CONFIG_INVALID: E032 run split changed")
    if dataset["exposures_per_run"] != 2 or dataset["event_code"] != 3:
        raise E032Error("CONFIG_INVALID: E032 event contract changed")

    files = require_mapping(config["files"], "files")
    required_files = {
        *(f"run{run}_{suffix}" for run in range(1, 5) for suffix in ("channels", "events", "sidecar", "fif")),
        "coordsystem",
        "fine_calibration",
        "crosstalk",
        "stimulus_wav",
        "word_tokens",
        "word_times",
        "phoneme_tokens",
        "phoneme_times",
        "visual_frames",
    }
    require_keys(files, required_files, "files")
    for key, spec_value in files.items():
        spec = require_mapping(spec_value, f"files.{key}")
        require_keys(spec, {"stage", "path", "url", "bytes", "sha256"}, f"files.{key}")
        if not isinstance(spec["bytes"], int) or spec["bytes"] <= 0:
            raise E032Error(f"CONFIG_INVALID: files.{key}.bytes")
        if not isinstance(spec["sha256"], str) or len(spec["sha256"]) != 64:
            raise E032Error(f"CONFIG_INVALID: files.{key}.sha256")
        if not str(spec["url"]).startswith("https://"):
            raise E032Error(f"CONFIG_INVALID: files.{key}.url")
        local = Path(str(spec["path"]))
        if local.is_absolute() or ".." in local.parts:
            raise E032Error(f"CONFIG_INVALID: files.{key}.path escapes data root")

    preprocessing = require_mapping(config["preprocessing"], "preprocessing")
    require_keys(
        preprocessing,
        {
            "scale_reference",
            "minimum_median_channel_scale_ratio",
            "maximum_median_channel_scale_ratio",
            "extreme_channel_scale_ratio_lower",
            "extreme_channel_scale_ratio_upper",
            "maximum_extreme_channel_fraction",
        },
        "preprocessing",
    )
    if preprocessing["scale_reference"] != "builder_residual_channel_mad":
        raise E032Error("CONFIG_INVALID: scale reference changed")
    scale_values = [
        preprocessing["minimum_median_channel_scale_ratio"],
        preprocessing["maximum_median_channel_scale_ratio"],
        preprocessing["extreme_channel_scale_ratio_lower"],
        preprocessing["extreme_channel_scale_ratio_upper"],
        preprocessing["maximum_extreme_channel_fraction"],
    ]
    if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in scale_values):
        raise E032Error("CONFIG_INVALID: scale thresholds must be finite")
    if not (
        0 < preprocessing["extreme_channel_scale_ratio_lower"]
        <= preprocessing["minimum_median_channel_scale_ratio"]
        < preprocessing["maximum_median_channel_scale_ratio"]
        <= preprocessing["extreme_channel_scale_ratio_upper"]
    ):
        raise E032Error("CONFIG_INVALID: scale thresholds are not ordered")
    if not 0 <= preprocessing["maximum_extreme_channel_fraction"] <= 1:
        raise E032Error("CONFIG_INVALID: maximum extreme-channel fraction")

    corrca = require_mapping(config["corrca"], "corrca")
    require_keys(
        corrca,
        {
            "components",
            "shrinkage_grid",
            "tie_tolerance",
            "tie_rule",
            "dss_principal_angle_tolerance_radians",
            "dss_score_tolerance",
        },
        "corrca",
    )
    if corrca["components"] != 1 or corrca["tie_rule"] != "larger_shrinkage":
        raise E032Error("CONFIG_INVALID: component or tie rule changed")
    expected_gamma = [0.0, 0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95]
    if corrca["shrinkage_grid"] != expected_gamma:
        raise E032Error("CONFIG_INVALID: shrinkage grid changed")

    controls = require_mapping(config["controls"], "controls")
    if controls.get("shift_seconds") != [41, 53, 67, 79, 89, 101, 113, 137]:
        raise E032Error("CONFIG_INVALID: shift set changed")
    if controls.get("shifted_filter_multipliers") != [0, 1, 2, 3]:
        raise E032Error("CONFIG_INVALID: shifted-filter multipliers changed")

    bootstrap = require_mapping(config["bootstrap"], "bootstrap")
    if bootstrap.get("seeds") != [3201, 3202, 3203]:
        raise E032Error("CONFIG_INVALID: bootstrap seeds changed")

    return config, hashlib.sha256(raw).hexdigest()


def data_root(config: dict[str, Any]) -> Path:
    candidate = (REPO_ROOT / str(config["paths"]["data_root"])).resolve()
    if REPO_ROOT not in candidate.parents:
        raise E032Error("CONFIG_INVALID: data_root escapes repository")
    return candidate


def output_root(config: dict[str, Any]) -> Path:
    candidate = (REPO_ROOT / str(config["paths"]["output_root"])).resolve()
    if REPO_ROOT not in candidate.parents:
        raise E032Error("CONFIG_INVALID: output_root escapes repository")
    return candidate


def require_authorization(config: dict[str, Any], stage: str) -> None:
    authorization = config["authorization"]
    if not authorization["work_e032_authorized"]:
        raise E032Error(f"AUTHORIZATION_REQUIRED: /work E032 before {stage}")
    if not authorization["participant_raw_access_allowed"]:
        raise E032Error(f"AUTHORIZATION_REQUIRED: participant raw access before {stage}")


def local_file(config: dict[str, Any], key: str) -> Path:
    return data_root(config) / str(config["files"][key]["path"])


def verify_frozen_file(path: Path, spec: dict[str, Any]) -> dict[str, Any]:
    if not path.is_file():
        raise E032Error(f"FILE_MISSING: {path}")
    size = path.stat().st_size
    if size != spec["bytes"]:
        raise E032Error(f"FILE_SIZE_MISMATCH: {path}: {size} != {spec['bytes']}")
    digest = sha256_file(path)
    if digest != spec["sha256"]:
        raise E032Error(f"FILE_HASH_MISMATCH: {path}: {digest}")
    return {"bytes": size, "sha256": digest}


def streamed_download(url: str, destination: Path, expected_bytes: int, expected_sha256: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        verify_frozen_file(
            destination,
            {"bytes": expected_bytes, "sha256": expected_sha256},
        )
        return

    temporary = destination.with_name(f".{destination.name}.part")
    if temporary.exists():
        temporary.unlink()
    digest = hashlib.sha256()
    total = 0
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "brain-alignment-E032/1.0"})
        with urllib.request.urlopen(request, timeout=120) as response, temporary.open("xb") as handle:
            while True:
                chunk = response.read(8 * 1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
                digest.update(chunk)
                total += len(chunk)
            handle.flush()
            os.fsync(handle.fileno())
        if total != expected_bytes:
            raise E032Error(f"DOWNLOAD_SIZE_MISMATCH: {destination}: {total} != {expected_bytes}")
        if digest.hexdigest() != expected_sha256:
            raise E032Error(f"DOWNLOAD_HASH_MISMATCH: {destination}: {digest.hexdigest()}")
        os.replace(temporary, destination)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def stage_manifest(config: dict[str, Any], config_path: Path, config_hash: str) -> dict[str, Any]:
    inventory: dict[str, Any] = {}
    for key, spec in sorted(config["files"].items()):
        path = local_file(config, key)
        entry = {
            "stage": spec["stage"],
            "path": str(path.relative_to(REPO_ROOT)),
            "url": spec["url"],
            "expected_bytes": spec["bytes"],
            "expected_sha256": spec["sha256"],
            "local_exists": path.is_file(),
        }
        if path.is_file():
            entry["local_bytes"] = path.stat().st_size
            entry["local_size_matches_expected"] = entry["local_bytes"] == spec["bytes"]
        inventory[key] = entry

    payload = {
        "experiment": "E032",
        "stage": "manifest",
        "endpoint_values_accessed": False,
        "participant_raw_opened": False,
        "config_path": str(config_path.resolve().relative_to(REPO_ROOT)),
        "config_sha256": config_hash,
        "executable_sha256": sha256_file(Path(__file__).resolve()),
        "authorization": dict(config["authorization"]),
        "python": platform.python_version(),
        "files": inventory,
    }
    path = output_root(config) / "preflight_manifest.json"
    atomic_write_json(path, payload)
    payload["artifact_path"] = str(path.relative_to(REPO_ROOT))
    payload["artifact_sha256"] = sha256_file(path)
    return payload


def stage_acquire(config: dict[str, Any]) -> dict[str, Any]:
    require_authorization(config, "acquire")
    completed = []
    for key, spec in sorted(config["files"].items()):
        destination = local_file(config, key)
        streamed_download(
            str(spec["url"]),
            destination,
            int(spec["bytes"]),
            str(spec["sha256"]),
        )
        completed.append(key)
    return {
        "experiment": "E032",
        "stage": "acquire",
        "participant_raw_opened": False,
        "files_verified": completed,
    }


@dataclass(frozen=True)
class EventReconciliation:
    convention: str
    raw_relative_seconds: np.ndarray
    raw_samples: np.ndarray
    max_error_samples: float


def reconcile_events(
    raw_samples: Sequence[int],
    first_sample: int,
    sampling_frequency: float,
    tsv_onsets_seconds: Sequence[float],
    tolerance_samples: float,
) -> EventReconciliation:
    raw_samples_array = np.asarray(raw_samples, dtype=np.int64)
    tsv = np.asarray(tsv_onsets_seconds, dtype=np.float64)
    if raw_samples_array.shape != (2,) or tsv.shape != (2,):
        raise E032Error("INTEGRITY_EVENT_COUNT: exactly two code-3 events required")
    raw_relative = (raw_samples_array - first_sample) / sampling_frequency
    raw_absolute = raw_samples_array / sampling_frequency
    candidates = {
        "raw_relative": raw_relative,
        "raw_relative_plus_first_sample": raw_absolute,
    }
    passing: list[tuple[float, str]] = []
    for convention, expected in candidates.items():
        error = float(np.max(np.abs(tsv - expected)) * sampling_frequency)
        if error <= tolerance_samples + 1e-9:
            passing.append((error, convention))
    if len(passing) != 1:
        labels = [item[1] for item in passing]
        raise E032Error(f"INTEGRITY_EVENT_CONVENTION: expected one passing convention, got {labels}")
    error, convention = passing[0]
    return EventReconciliation(convention, raw_relative, raw_samples_array, error)


def require_complete_windows(
    onsets_relative_seconds: Sequence[float],
    stimulus_duration_seconds: float,
    raw_duration_seconds: float,
    tolerance_seconds: float,
) -> None:
    onsets = np.asarray(onsets_relative_seconds, dtype=np.float64)
    if np.any(onsets < -tolerance_seconds):
        raise E032Error("INTEGRITY_WINDOW: negative normalized onset")
    if np.any(onsets + stimulus_duration_seconds > raw_duration_seconds + tolerance_seconds):
        raise E032Error("INTEGRITY_WINDOW: incomplete stimulus window")


def read_tsv_code_onsets(path: Path, event_code: int) -> list[float]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if "onset" not in (reader.fieldnames or []):
            raise E032Error(f"INTEGRITY_EVENTS_TSV: onset missing in {path}")
        result = []
        for row in reader:
            tokens = [
                row.get("value"),
                row.get("trial_type"),
                row.get("event_code"),
                row.get("code"),
            ]
            matched = False
            for token in tokens:
                if token is None:
                    continue
                try:
                    matched = float(str(token).strip()) == float(event_code)
                except ValueError:
                    matched = str(token).strip() == str(event_code)
                if matched:
                    break
            if matched:
                result.append(float(row["onset"]))
    if len(result) != 2:
        raise E032Error(f"INTEGRITY_EVENTS_TSV: {path} has {len(result)} code-{event_code} events")
    return result


def channel_inventory(raw: Any) -> dict[str, int]:
    channel_types = raw.get_channel_types()
    return {
        "MEGMAG": channel_types.count("mag"),
        "MEGGRADAXIAL": channel_types.count("grad"),
        "EEG": channel_types.count("eeg"),
        "EOG": channel_types.count("eog"),
        "ECG": channel_types.count("ecg"),
        "TRIG": channel_types.count("stim"),
        "MISC": channel_types.count("misc"),
        "total": len(channel_types),
    }


def require_channel_inventory(raw: Any, expected: dict[str, int], run_number: int) -> dict[str, int]:
    inventory = channel_inventory(raw)
    if inventory != expected:
        raise E032Error(f"INTEGRITY_CHANNELS: run {run_number}: {inventory} != {expected}")
    return inventory


def missing_calibration_channels(
    raw_channel_names: Sequence[str],
    raw_channel_types: Sequence[str],
    calibration_channel_names: Sequence[str],
) -> list[str]:
    calibration_names = {str(name).replace(" ", "") for name in calibration_channel_names}
    meg_names = {
        name.replace(" ", "")
        for name, channel_type in zip(raw_channel_names, raw_channel_types)
        if channel_type in {"mag", "grad"}
    }
    return sorted(meg_names - calibration_names)


def meg_channel_names(
    raw_channel_names: Sequence[str],
    raw_channel_types: Sequence[str],
) -> list[str]:
    return [
        name
        for name, channel_type in zip(raw_channel_names, raw_channel_types)
        if channel_type in {"mag", "grad"}
    ]


def verify_calibration_compatibility(raw: Any, calibration: Path, crosstalk: Path) -> dict[str, Any]:
    import mne
    from mne.preprocessing.maxwell import _read_cross_talk

    calibration_data = mne.preprocessing.read_fine_calibration(str(calibration))
    calibration_names = {str(name).replace(" ", "") for name in calibration_data["ch_names"]}
    missing = missing_calibration_channels(
        raw.ch_names,
        raw.get_channel_types(),
        calibration_data["ch_names"],
    )
    if missing:
        raise E032Error(f"INTEGRITY_CALIBRATION: {len(missing)} MEG channels absent")
    meg_names = meg_channel_names(raw.ch_names, raw.get_channel_types())
    _read_cross_talk(str(crosstalk), meg_names)
    basis_in, basis_out = mne.preprocessing.compute_maxwell_basis(
        raw.info,
        calibration=str(calibration),
        ignore_ref=True,
        verbose="ERROR",
    )
    if basis_in.size == 0 or basis_out.size == 0:
        raise E032Error("INTEGRITY_CALIBRATION: empty Maxwell basis")
    return {
        "calibration_channels": len(calibration_names),
        "maxwell_internal_basis": list(basis_in.shape),
        "maxwell_external_basis": list(basis_out.shape),
        "crosstalk_parsed": True,
    }


def _stage_integrity_authorized(config: dict[str, Any], config_hash: str) -> dict[str, Any]:
    import mne

    for key, spec in config["files"].items():
        verify_frozen_file(local_file(config, key), spec)

    calibration = local_file(config, "fine_calibration")
    crosstalk = local_file(config, "crosstalk")
    event_code = int(config["dataset"]["event_code"])
    expected_sfreq = float(config["dataset"]["sampling_frequency_hz"])
    expected_channels = dict(config["dataset"]["expected_channels"])
    stimulus_duration = float(config["dataset"]["stimulus_duration_seconds"])
    tolerance_samples = float(config["integrity"]["event_alignment_tolerance_samples"])
    runs: dict[str, Any] = {}
    calibration_results: dict[str, Any] = {}

    for run_number in range(1, 5):
        raw_path = local_file(config, f"run{run_number}_fif")
        raw = mne.io.read_raw_fif(raw_path, preload=False, verbose="ERROR")
        try:
            if not np.isclose(raw.info["sfreq"], expected_sfreq, atol=1e-9, rtol=0):
                raise E032Error(f"INTEGRITY_SFREQ: run {run_number}: {raw.info['sfreq']}")
            inventory = require_channel_inventory(raw, expected_channels, run_number)
            if "STI101" not in raw.ch_names:
                raise E032Error(f"INTEGRITY_STI101: absent in run {run_number}")
            if not (raw.info.get("hpi_meas") or raw.info.get("hpi_subsystem")):
                raise E032Error(f"INTEGRITY_HPI: absent in run {run_number}")

            events = mne.find_events(
                raw,
                stim_channel="STI101",
                shortest_event=1,
                uint_cast=True,
                verbose="ERROR",
            )
            code_events = events[events[:, 2] == event_code]
            tsv_onsets = read_tsv_code_onsets(local_file(config, f"run{run_number}_events"), event_code)
            reconciled = reconcile_events(
                code_events[:, 0],
                int(raw.first_samp),
                float(raw.info["sfreq"]),
                tsv_onsets,
                tolerance_samples,
            )
            raw_duration = raw.n_times / float(raw.info["sfreq"])
            require_complete_windows(
                reconciled.raw_relative_seconds,
                stimulus_duration,
                raw_duration,
                tolerance_samples / expected_sfreq,
            )
            calibration_results[str(run_number)] = verify_calibration_compatibility(
                raw, calibration, crosstalk
            )
            runs[str(run_number)] = {
                "first_sample": int(raw.first_samp),
                "n_times": int(raw.n_times),
                "duration_seconds": raw_duration,
                "channel_inventory": inventory,
                "event_convention": reconciled.convention,
                "event_samples": reconciled.raw_samples.tolist(),
                "event_onsets_raw_relative_seconds": reconciled.raw_relative_seconds.tolist(),
                "maximum_alignment_error_samples": reconciled.max_error_samples,
            }
        finally:
            raw.close()

    payload = {
        "experiment": "E032",
        "stage": "integrity",
        "endpoint_values_accessed": False,
        "neural_channel_values_accessed": False,
        "trigger_channel_accessed": True,
        "config_sha256": config_hash,
        "executable_sha256": sha256_file(Path(__file__).resolve()),
        "runs": runs,
        "calibration_by_run": calibration_results,
        "classification_if_failed": "ACQUISITION/PREPROCESSING FLOOR",
    }
    artifact = output_root(config) / "acquisition_integrity.json"
    atomic_write_json(artifact, payload)
    payload["artifact_path"] = str(artifact.relative_to(REPO_ROOT))
    payload["artifact_sha256"] = sha256_file(artifact)
    return payload


def integrity_failure_payload(config_hash: str, exc: Exception) -> dict[str, Any]:
    return {
        "experiment": "E032",
        "stage": "integrity",
        "status": "FAILED",
        "classification": "ACQUISITION/PREPROCESSING FLOOR",
        "endpoint_values_accessed": False,
        "neural_channel_values_accessed": False,
        "config_sha256": config_hash,
        "executable_sha256": sha256_file(Path(__file__).resolve()),
        "error_type": type(exc).__name__,
        "error_detail": str(exc),
    }


def stage_integrity(config: dict[str, Any], config_hash: str) -> dict[str, Any]:
    # Lack of authorization is not a dataset result and must not create a
    # scientific classification. Once authorized, every integrity-path failure
    # is retained with the frozen acquisition/preprocessing-floor label.
    require_authorization(config, "integrity")
    try:
        return _stage_integrity_authorized(config, config_hash)
    except Exception as exc:
        payload = integrity_failure_payload(config_hash, exc)
        artifact = output_root(config) / "acquisition_integrity.json"
        atomic_write_json(artifact, payload)
        detail = f"{payload['error_type']}: {payload['error_detail']}"
        raise E032Error(
            f"ACQUISITION/PREPROCESSING FLOOR: {detail}; "
            f"artifact={artifact.relative_to(REPO_ROOT)}"
        ) from exc


def centered_exposures(exposures: Sequence[np.ndarray]) -> list[np.ndarray]:
    if len(exposures) < 2:
        raise E032Error("NUMERICAL_INPUT: at least two exposures required")
    shapes = [np.asarray(exposure).shape for exposure in exposures]
    if len(set(shapes)) != 1 or len(shapes[0]) != 2:
        raise E032Error(f"NUMERICAL_INPUT: unequal exposure shapes {shapes}")
    result = []
    for exposure in exposures:
        array = np.asarray(exposure, dtype=np.float64)
        if not np.all(np.isfinite(array)):
            raise E032Error("NUMERICAL_INPUT: nonfinite exposure")
        result.append(array - array.mean(axis=0, keepdims=True))
    return result


def covariance_terms(exposures: Sequence[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    centered = centered_exposures(exposures)
    within = sum(array.T @ array for array in centered)
    between = sum(
        centered[i].T @ centered[j]
        for i in range(len(centered))
        for j in range(len(centered))
        if i != j
    )
    return within, (between + between.T) / 2


def regularized_within(within: np.ndarray, gamma: float) -> np.ndarray:
    if not 0 <= gamma <= 1:
        raise E032Error("NUMERICAL_INPUT: gamma outside [0,1]")
    dimension = within.shape[0]
    target = np.trace(within) / dimension
    result = (1 - gamma) * within + gamma * target * np.eye(dimension)
    return (result + result.T) / 2


def normalize_filter(vector: np.ndarray, metric: np.ndarray) -> np.ndarray:
    norm = float(np.sqrt(vector.T @ metric @ vector))
    if not math.isfinite(norm) or norm <= 0:
        raise E032Error("NUMERICAL_FAILURE: invalid filter norm")
    result = np.asarray(vector, dtype=np.float64) / norm
    pivot = int(np.argmax(np.abs(result)))
    if result[pivot] < 0:
        result = -result
    return result


def corrca_filter(exposures: Sequence[np.ndarray], gamma: float) -> tuple[np.ndarray, float]:
    within, between = covariance_terms(exposures)
    metric = regularized_within(within, gamma)
    try:
        values, vectors = linalg.eigh(between, metric, check_finite=True)
    except linalg.LinAlgError as exc:
        raise E032Error(f"NUMERICAL_FAILURE: CorrCA eigenproblem: {exc}") from exc
    index = int(np.argmax(values))
    return normalize_filter(vectors[:, index], metric), float(values[index])


def corrca_objective(exposures: Sequence[np.ndarray], vector: np.ndarray, gamma: float) -> float:
    within, between = covariance_terms(exposures)
    metric = regularized_within(within, gamma)
    numerator = float(vector.T @ between @ vector)
    denominator = (len(exposures) - 1) * float(vector.T @ metric @ vector)
    if not math.isfinite(denominator) or denominator <= 0:
        raise E032Error("NUMERICAL_FAILURE: invalid CorrCA objective denominator")
    return numerator / denominator


def dss_filter(exposures: Sequence[np.ndarray], gamma: float) -> tuple[np.ndarray, float]:
    within, between = covariance_terms(exposures)
    metric = regularized_within(within, gamma)
    # The regularized repeat-average bias replaces the within-repeat diagonal
    # term by the same metric used for whitening. Its eigenvalues are an affine
    # transform of CorrCA's, so the eigenvectors remain identical for gamma > 0.
    bias = (metric + between) / (len(exposures) ** 2)
    try:
        values, vectors = linalg.eigh((bias + bias.T) / 2, metric, check_finite=True)
    except linalg.LinAlgError as exc:
        raise E032Error(f"NUMERICAL_FAILURE: DSS eigenproblem: {exc}") from exc
    index = int(np.argmax(values))
    return normalize_filter(vectors[:, index], metric), float(values[index])


def pca_mean_filter(exposures: Sequence[np.ndarray]) -> np.ndarray:
    centered = centered_exposures(exposures)
    mean = np.mean(np.stack(centered, axis=0), axis=0)
    _, _, right = np.linalg.svd(mean, full_matrices=False)
    vector = right[0]
    norm = np.linalg.norm(vector)
    if norm <= 0:
        raise E032Error("NUMERICAL_FAILURE: PCA zero norm")
    vector = vector / norm
    pivot = int(np.argmax(np.abs(vector)))
    return -vector if vector[pivot] < 0 else vector


def principal_angle(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    a = np.asarray(vector_a, dtype=np.float64)
    b = np.asarray(vector_b, dtype=np.float64)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    cosine = abs(float(a @ b) / denominator)
    return float(np.arccos(np.clip(cosine, -1, 1)))


def fisher_correlation(first: np.ndarray, second: np.ndarray) -> float:
    first = np.asarray(first, dtype=np.float64)
    second = np.asarray(second, dtype=np.float64)
    if first.shape != second.shape or first.ndim != 1:
        raise E032Error("NUMERICAL_INPUT: correlation shape mismatch")
    correlation = float(np.corrcoef(first, second)[0, 1])
    if not math.isfinite(correlation):
        raise E032Error("NUMERICAL_FAILURE: nonfinite correlation")
    return float(np.arctanh(np.clip(correlation, -1 + 1e-12, 1 - 1e-12)))


def circular_shift(array: np.ndarray, seconds: float, sampling_frequency: float) -> np.ndarray:
    samples = int(round(seconds * sampling_frequency))
    return np.roll(np.asarray(array), samples, axis=0)


def scale_diagnostic(
    reference_channel_mad: np.ndarray,
    heldout_channel_mad: np.ndarray,
    preprocessing: dict[str, Any],
) -> dict[str, Any]:
    reference = np.asarray(reference_channel_mad, dtype=np.float64)
    heldout = np.asarray(heldout_channel_mad, dtype=np.float64)
    if reference.shape != heldout.shape or reference.ndim != 1:
        raise E032Error("SCALE_INPUT: channel shapes differ")
    if np.any(reference <= 0) or np.any(heldout < 0):
        raise E032Error("SCALE_INPUT: invalid channel MAD")
    ratios = heldout / reference
    median_ratio = float(np.median(ratios))
    extreme = (
        (ratios < preprocessing["extreme_channel_scale_ratio_lower"])
        | (ratios > preprocessing["extreme_channel_scale_ratio_upper"])
    )
    extreme_fraction = float(np.mean(extreme))
    passed = (
        preprocessing["minimum_median_channel_scale_ratio"]
        <= median_ratio
        <= preprocessing["maximum_median_channel_scale_ratio"]
        and extreme_fraction <= preprocessing["maximum_extreme_channel_fraction"]
    )
    return {
        "median_channel_scale_ratio": median_ratio,
        "extreme_channel_fraction": extreme_fraction,
        "passed": bool(passed),
    }


def moving_block_bootstrap_mean(
    values: np.ndarray,
    block_samples: int,
    resamples: int,
    seed: int,
    confidence: float,
) -> tuple[float, float]:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or not np.all(np.isfinite(array)):
        raise E032Error("BOOTSTRAP_INPUT: expected one finite series")
    if not 1 <= block_samples <= len(array):
        raise E032Error("BOOTSTRAP_INPUT: invalid block size")
    rng = np.random.default_rng(seed)
    blocks_needed = math.ceil(len(array) / block_samples)
    maximum_start = len(array) - block_samples
    estimates = np.empty(resamples, dtype=np.float64)
    for index in range(resamples):
        starts = rng.integers(0, maximum_start + 1, size=blocks_needed)
        sample = np.concatenate([array[start : start + block_samples] for start in starts])
        estimates[index] = sample[: len(array)].mean()
    alpha = 1 - confidence
    low, high = np.quantile(estimates, [alpha / 2, 1 - alpha / 2])
    return float(low), float(high)


def stage_selftest(config: dict[str, Any]) -> dict[str, Any]:
    tests: dict[str, str] = {}

    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "identity.bin"
        path.write_bytes(b"e032")
        spec = {"bytes": 4, "sha256": hashlib.sha256(b"e032").hexdigest()}
        verify_frozen_file(path, spec)
    tests["frozen_file_identity"] = "PASS"

    reconciliation = reconcile_events(
        raw_samples=[1500, 2500],
        first_sample=1000,
        sampling_frequency=1000,
        tsv_onsets_seconds=[1.5, 2.5],
        tolerance_samples=1,
    )
    if reconciliation.convention != "raw_relative_plus_first_sample":
        raise E032Error("SELFTEST: event convention")
    tests["event_offset_reconciliation"] = "PASS"

    require_complete_windows([0.5, 1.5], 1.0, 2.5, 0.001)
    try:
        require_complete_windows([0.5, 1.6], 1.0, 2.5, 0.001)
    except E032Error:
        pass
    else:
        raise E032Error("SELFTEST: incomplete window was accepted")
    tests["complete_window_failure"] = "PASS"

    class FakeRaw:
        ch_names = ["MEG 001", "MEG 002", "EEG 001", "STI101", "MISC 001"]

        @staticmethod
        def get_channel_types() -> list[str]:
            return ["mag", "grad", "eeg", "stim", "misc"]

    expected_fake_inventory = {
        "MEGMAG": 1,
        "MEGGRADAXIAL": 1,
        "EEG": 1,
        "EOG": 0,
        "ECG": 0,
        "TRIG": 1,
        "MISC": 1,
        "total": 5,
    }
    require_channel_inventory(FakeRaw(), expected_fake_inventory, 0)
    try:
        require_channel_inventory(FakeRaw(), {**expected_fake_inventory, "EEG": 2}, 0)
    except E032Error:
        pass
    else:
        raise E032Error("SELFTEST: channel inventory mismatch was accepted")
    tests["channel_inventory_failure"] = "PASS"

    if missing_calibration_channels(
        FakeRaw.ch_names,
        FakeRaw.get_channel_types(),
        ["MEG001"],
    ) != ["MEG002"]:
        raise E032Error("SELFTEST: calibration mismatch not found")
    if missing_calibration_channels(
        FakeRaw.ch_names,
        FakeRaw.get_channel_types(),
        ["MEG001", "MEG002"],
    ):
        raise E032Error("SELFTEST: calibration match rejected")
    tests["calibration_name_mismatch"] = "PASS"

    if meg_channel_names(FakeRaw.ch_names, FakeRaw.get_channel_types()) != [
        "MEG 001",
        "MEG 002",
    ]:
        raise E032Error("SELFTEST: non-MEG channel leaked into crosstalk names")
    tests["crosstalk_meg_channel_selection"] = "PASS"

    synthetic_failure = integrity_failure_payload(
        "0" * 64,
        E032Error("synthetic integrity failure"),
    )
    if (
        synthetic_failure["classification"] != "ACQUISITION/PREPROCESSING FLOOR"
        or synthetic_failure["status"] != "FAILED"
        or synthetic_failure["endpoint_values_accessed"]
        or synthetic_failure["neural_channel_values_accessed"]
    ):
        raise E032Error("SELFTEST: integrity failure classification")
    tests["integrity_failure_classification"] = "PASS"

    rng = np.random.default_rng(3200)
    samples = 4000
    shared = rng.normal(size=samples)
    mixing = np.array([1.0, -0.5, 0.2, 0.0])
    exposures = [
        shared[:, None] * mixing[None, :] + 0.6 * rng.normal(size=(samples, 4))
        for _ in range(4)
    ]
    corr_vector, _ = corrca_filter(exposures, 0.2)
    dss_vector, _ = dss_filter(exposures, 0.2)
    angle = principal_angle(corr_vector, dss_vector)
    if angle > config["corrca"]["dss_principal_angle_tolerance_radians"]:
        raise E032Error(f"SELFTEST: CorrCA/DSS angle {angle}")
    corr_score = corrca_objective(exposures, corr_vector, 0.2)
    dss_score = corrca_objective(exposures, dss_vector, 0.2)
    if abs(corr_score - dss_score) > config["corrca"]["dss_score_tolerance"]:
        raise E032Error(f"SELFTEST: CorrCA/DSS score {corr_score} != {dss_score}")
    tests["corrca_dss_equivalence"] = "PASS"

    projected = [exposure @ corr_vector for exposure in exposures]
    aligned = np.mean(
        [fisher_correlation(projected[i], projected[j]) for i in range(4) for j in range(i)]
    )
    shifted = np.mean(
        [
            fisher_correlation(projected[i], circular_shift(projected[j], 0.137, 1000))
            for i in range(4)
            for j in range(i)
        ]
    )
    if not aligned > shifted:
        raise E032Error("SELFTEST: aligned CorrCA did not beat shift")
    tests["shifted_control"] = "PASS"

    pca_vector = pca_mean_filter(exposures)
    if pca_vector.shape != corr_vector.shape:
        raise E032Error("SELFTEST: PCA capacity mismatch")
    tests["pca_capacity"] = "PASS"

    passed = scale_diagnostic(np.ones(100), np.ones(100), config["preprocessing"])
    failed = scale_diagnostic(
        np.ones(100),
        np.r_[np.full(10, 10.0), np.ones(90)],
        config["preprocessing"],
    )
    if not passed["passed"] or failed["passed"]:
        raise E032Error("SELFTEST: scale diagnostic")
    tests["scale_diagnostic"] = "PASS"

    series = rng.normal(loc=0.1, scale=0.1, size=1000)
    first = moving_block_bootstrap_mean(series, 20, 200, 3201, 0.95)
    second = moving_block_bootstrap_mean(series, 20, 200, 3201, 0.95)
    if first != second or first[0] >= first[1]:
        raise E032Error("SELFTEST: bootstrap determinism")
    tests["moving_block_bootstrap"] = "PASS"

    unauthorized = json.loads(json.dumps(config))
    unauthorized["authorization"]["work_e032_authorized"] = False
    try:
        require_authorization(unauthorized, "builder")
    except E032Error:
        pass
    else:
        raise E032Error("SELFTEST: authorization bypass")
    tests["authorization_gate"] = "PASS"

    if not ENDPOINT_STAGES.isdisjoint(IMPLEMENTED_STAGES):
        raise E032Error("SELFTEST: endpoint stage marked implemented")
    tests["endpoint_not_implemented_gate"] = "PASS"

    return {
        "experiment": "E032",
        "stage": "selftest",
        "endpoint_values_accessed": False,
        "tests": tests,
        "test_count": len(tests),
        "status": "PASS",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--stage",
        required=True,
        choices=sorted(IMPLEMENTED_STAGES | ENDPOINT_STAGES),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    try:
        config, config_hash = load_config(config_path)
        if args.stage == "selftest":
            result = stage_selftest(config)
        elif args.stage == "manifest":
            result = stage_manifest(config, config_path, config_hash)
        elif args.stage == "acquire":
            result = stage_acquire(config)
        elif args.stage == "integrity":
            result = stage_integrity(config, config_hash)
        elif args.stage in ENDPOINT_STAGES:
            raise E032Error(
                f"NOT_IMPLEMENTED: {args.stage} is sealed before neural access; "
                "E032 remains READY-TO-RUN:NO"
            )
        else:
            raise AssertionError(args.stage)
    except E032Error as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("INTERRUPTED", file=sys.stderr)
        return 130
    except BaseException as exc:
        print(f"UNEXPECTED_FAILURE: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
