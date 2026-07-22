#!/usr/bin/env python3
"""Outcome-blind synthetic Stage-1 reference slice for E028.

This executable deliberately has no production provider, endpoint command, model
training path, or network path.  It exercises the corrected evaluator contract on
deterministic synthetic data and emits development-only artifacts.
"""

from __future__ import annotations

import argparse
import builtins
import copy
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import resource
import socket
import tempfile
import time
from typing import Any, Iterable, Sequence

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


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "e028_vaidya_crossmodal_falsification.json"
RUNNER_COMMANDS = ("manifest", "synthetic-replay", "selftest", "benchmark", "bundle")
FORBIDDEN_COMPONENTS = (
    "data",
    "outputs",
    "hf-cache",
    "huggingface",
    "transformers",
    "author-results",
    "author_results",
    "neural-payload",
    "neural_payload",
    "endpoint-payload",
    "endpoint_payload",
)
DEVELOPMENT_MANIFEST_FILES = (
    "configs/e028_vaidya_crossmodal_falsification.json",
    "scripts/e028_vaidya_crossmodal_falsification.py",
    "scripts/e028_analyze_vaidya_stage1.py",
    "scripts/e028_acquisition_manifest.py",
    "docs/experiments/E028_vaidya-crossmodal-intervention-falsification.md",
    "docs/decisions/decisions.md",
    "pyproject.toml",
    "uv.lock",
)
CONFIG_KEYS = {
    "schema_version",
    "experiment_id",
    "protocol_state",
    "development_scope",
    "synthetic_only",
    "author_facts_complete",
    "exact_lane",
    "production_provider",
    "ready_for_endpoint_access",
    "readiness_label",
    "endpoint_access_authorized",
    "author_result_access_authorized",
    "training_authorized",
    "network_access_authorized",
    "development_canonicalization",
    "command_allowlists",
    "author_facts",
    "chain",
    "stage1",
    "synthetic",
    "raw_result_schema",
    "development_gaps",
    "forbidden_path_components",
}


class ProtocolError(RuntimeError):
    """Fail-closed protocol violation."""


def canonical_json_bytes(value: Any) -> bytes:
    """Canonical bytes for the explicitly development-only JSON profile."""
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ProtocolError(f"value is not canonical-development-JSON encodable: {exc}") from exc


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def with_content_hash(payload: dict[str, Any]) -> dict[str, Any]:
    if "content_sha256" in payload:
        raise ProtocolError("content_sha256 must be absent before hashing")
    result = copy.deepcopy(payload)
    result["content_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    return result


def validate_content_hash(payload: dict[str, Any]) -> None:
    claimed = payload.get("content_sha256")
    if not isinstance(claimed, str) or len(claimed) != 64:
        raise ProtocolError("missing or malformed content_sha256")
    unhashed = dict(payload)
    del unhashed["content_sha256"]
    actual = sha256_bytes(canonical_json_bytes(unhashed))
    if actual != claimed:
        raise ProtocolError(f"content hash mismatch: expected {claimed}, computed {actual}")


def _relative_forbidden_parts(path: Path, forbidden: set[str]) -> set[str]:
    resolved = path.resolve(strict=False)
    try:
        relative = resolved.relative_to(ROOT)
        parts = {part.casefold() for part in relative.parts}
    except ValueError:
        # The repository itself lives below a parent named ``data``.  Broad names
        # are therefore meaningful only relative to ROOT; payload-specific names
        # remain forbidden everywhere.
        broad = {"data", "outputs"}
        parts = {part.casefold() for part in resolved.parts}
        forbidden = forbidden - broad
    return parts & forbidden


def assert_safe_path(path: Path, forbidden_components: Sequence[str]) -> None:
    forbidden = {str(item).casefold() for item in forbidden_components}
    hits = _relative_forbidden_parts(path, forbidden)
    if hits:
        raise ProtocolError(f"forbidden path component(s): {sorted(hits)}")
    probe = path if path.exists() else path.parent
    while probe != probe.parent:
        if probe.is_symlink():
            raise ProtocolError(f"symlink path is forbidden: {probe}")
        probe = probe.parent


class AccessSentinel:
    """Block forbidden file roots and all socket creation during dev commands."""

    def __init__(self, forbidden_components: Sequence[str]) -> None:
        self.forbidden_components = tuple(forbidden_components)
        self.forbidden_attempts: list[str] = []
        self.network_attempts = 0
        self._open = builtins.open
        self._io_open = io.open
        self._socket = socket.socket
        self._create_connection = socket.create_connection
        self._getaddrinfo = socket.getaddrinfo

    def check_path(self, path: Any) -> None:
        if isinstance(path, int):
            return
        try:
            candidate = Path(os.fspath(path))
        except TypeError:
            return
        try:
            assert_safe_path(candidate, self.forbidden_components)
        except ProtocolError:
            self.forbidden_attempts.append(str(candidate))
            raise

    def _guarded_open(self, file: Any, *args: Any, **kwargs: Any) -> Any:
        self.check_path(file)
        return self._open(file, *args, **kwargs)

    def _guarded_io_open(self, file: Any, *args: Any, **kwargs: Any) -> Any:
        self.check_path(file)
        return self._io_open(file, *args, **kwargs)

    def _blocked_network(self, *args: Any, **kwargs: Any) -> Any:
        self.network_attempts += 1
        raise ProtocolError("network access is forbidden in E028 synthetic development")

    def __enter__(self) -> "AccessSentinel":
        builtins.open = self._guarded_open
        io.open = self._guarded_io_open
        socket.socket = self._blocked_network  # type: ignore[assignment]
        socket.create_connection = self._blocked_network  # type: ignore[assignment]
        socket.getaddrinfo = self._blocked_network  # type: ignore[assignment]
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        builtins.open = self._open
        io.open = self._io_open
        socket.socket = self._socket
        socket.create_connection = self._create_connection
        socket.getaddrinfo = self._getaddrinfo

    def summary(self) -> dict[str, Any]:
        return {
            "path_network_sentinel_active": True,
            "forbidden_access_attempts": list(self.forbidden_attempts),
            "network_attempts": self.network_attempts,
            "forbidden_roots": list(self.forbidden_components),
            "status": "PASS" if not self.forbidden_attempts and self.network_attempts == 0 else "FAIL",
        }


def load_config(path: Path) -> dict[str, Any]:
    try:
        resolved = path.resolve(strict=True)
        canonical = DEFAULT_CONFIG.resolve(strict=True)
    except OSError as exc:
        raise ProtocolError(f"cannot resolve canonical config: {exc}") from exc
    if resolved != canonical or path.is_symlink() or DEFAULT_CONFIG.is_symlink():
        raise ProtocolError("only the canonical non-symlinked E028 config is accepted")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProtocolError(f"cannot load config {path}: {exc}") from exc
    if set(config) != CONFIG_KEYS:
        raise ProtocolError(
            f"config keys differ; missing={sorted(CONFIG_KEYS - set(config))}, "
            f"unknown={sorted(set(config) - CONFIG_KEYS)}"
        )
    exact_identity = {
        "schema_version": "e028-outcome-blind-development-v1",
        "experiment_id": "E028",
        "protocol_state": "outcome-blind-development",
        "development_scope": "synthetic Stage-1 corrected-evaluator slice only",
        "readiness_label": "NOT READY",
        "author_facts_complete": False,
        "exact_lane": None,
        "production_provider": None,
    }
    for key, expected in exact_identity.items():
        if config[key] != expected:
            raise ProtocolError(f"frozen config identity changed: {key}")
    frozen_false = (
        "ready_for_endpoint_access",
        "endpoint_access_authorized",
        "author_result_access_authorized",
        "training_authorized",
        "network_access_authorized",
    )
    if config["synthetic_only"] is not True or any(config[key] is not False for key in frozen_false):
        raise ProtocolError("synthetic development safety flags changed")
    if tuple(config["command_allowlists"]["runner"]) != RUNNER_COMMANDS:
        raise ProtocolError("runner command allowlist drift")
    if tuple(config["command_allowlists"]["analyzer"]) != ("selftest", "analyze-synthetic"):
        raise ProtocolError("analyzer command allowlist drift")
    if tuple(config["forbidden_path_components"]) != FORBIDDEN_COMPONENTS:
        raise ProtocolError("forbidden path component list drift")
    if tuple(config["chain"]["development_manifest_files"]) != DEVELOPMENT_MANIFEST_FILES:
        raise ProtocolError("development manifest file list drift")
    canon = config["development_canonicalization"]
    if canon.get("production_rfc8785_chain_satisfied") is not False:
        raise ProtocolError("development canonicalization cannot claim production RFC8785")
    stage = config["stage1"]
    exact = {
        "tick_seconds": 0.05,
        "response_origin_seconds": 4,
        "outer_blocks": 4,
        "embargo_ticks": 120,
        "minimum_role_rows": 2,
        "standardization_ddof": 0,
        "drop_sd_below": 1e-8,
        "solver_residual_tolerance": 1e-10,
        "tie_tolerance": 1e-12,
        "sign_patterns": 512,
        "sign_tie_tolerance": 1e-12,
        "sign_denominator_floor": 1e-12,
        "family_alpha": 0.05,
        "boundary_width_max": 1e-10,
    }
    for key, expected in exact.items():
        if stage.get(key) != expected:
            raise ProtocolError(f"frozen Stage-1 value changed: {key}")
    if stage.get("lag_ticks") != {"minimum": -40, "maximum": 40, "step": 1}:
        raise ProtocolError("frozen lag grid changed")
    if stage.get("ridge_alpha") != [10.0**power for power in range(-6, 9)]:
        raise ProtocolError("frozen ridge-alpha grid changed")
    if stage.get("representation_penalty_ratio") != [1e-4, 1e-2, 1.0, 1e2, 1e4]:
        raise ProtocolError("frozen representation-penalty grid changed")
    patient_ids = stage.get("patient_ids", [])
    source_ids = stage.get("source_ids", [])
    if len(patient_ids) != 9 or len(source_ids) != 3:
        raise ProtocolError("synthetic inference cardinality must be 9 patients x 3 sources")
    if patient_ids != sorted(set(patient_ids)) or source_ids != sorted(set(source_ids)):
        raise ProtocolError("patient and source IDs must be unique and lexicographically sorted")
    return config


def atomic_write_json(path: Path, payload: dict[str, Any], forbidden: Sequence[str]) -> None:
    assert_safe_path(path, forbidden)
    if path.exists():
        raise ProtocolError(f"refusing to overwrite existing artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_json_bytes(payload) + b"\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _validate_manifest_path(text_path: str) -> Path:
    pure = PurePosixPath(text_path)
    if pure.is_absolute() or ".." in pure.parts or str(pure) != text_path:
        raise ProtocolError(f"noncanonical manifest path: {text_path}")
    candidate = ROOT.joinpath(*pure.parts)
    if not candidate.is_file() or candidate.is_symlink():
        raise ProtocolError(f"manifest input missing, non-file, or symlink: {text_path}")
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(ROOT):
        raise ProtocolError(f"manifest path escapes repository: {text_path}")
    return candidate


def development_manifest(config: dict[str, Any]) -> dict[str, Any]:
    paths = config["chain"]["development_manifest_files"]
    if not isinstance(paths, list) or not paths:
        raise ProtocolError("empty development manifest")
    normalized = [str(PurePosixPath(item)) for item in paths]
    if len(set(normalized)) != len(normalized) or normalized != paths:
        raise ProtocolError("manifest contains duplicate or non-normalized paths")
    entries = []
    for relative in sorted(paths):
        path = _validate_manifest_path(relative)
        entries.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    payload = {
        "schema_version": "e028-development-manifest-v1",
        "experiment_id": "E028",
        "development_only": True,
        "not_production_c0": True,
        "protocol_state": config["protocol_state"],
        "scope": config["development_scope"],
        "canonicalization_profile": config["development_canonicalization"]["profile"],
        "production_rfc8785_chain_satisfied": False,
        "files": entries,
        "files_sha256": sha256_bytes(canonical_json_bytes(entries)),
    }
    return with_content_hash(payload)


def maximal_segments(ticks: Sequence[int]) -> list[dict[str, int]]:
    ordered = [int(value) for value in ticks]
    if ordered != sorted(set(ordered)) or not ordered:
        raise ProtocolError("ticks must be nonempty, sorted, and unique")
    starts = [0]
    for index in range(1, len(ordered)):
        if ordered[index] != ordered[index - 1] + 1:
            starts.append(index)
    starts.append(len(ordered))
    result = []
    for segment_id, (lo, hi) in enumerate(zip(starts[:-1], starts[1:])):
        part = ordered[lo:hi]
        result.append(
            {
                "segment_id": segment_id,
                "start_tick": part[0],
                "end_tick": part[-1],
                "n_ticks": len(part),
            }
        )
    return result


def _role_arrays(
    ticks: Sequence[int], labels: dict[int, str], embargo_ticks: int
) -> tuple[dict[str, list[int]], dict[str, list[int]], list[float]]:
    ordered = [int(value) for value in ticks]
    if set(ordered) != set(labels):
        raise ProtocolError("role map does not cover support exactly")
    roles = sorted(set(labels.values()))
    pre = {role: [tick for tick in ordered if labels[tick] == role] for role in roles}
    boundaries = [
        (left + right) / 2.0
        for left, right in zip(ordered[:-1], ordered[1:])
        if labels[left] != labels[right]
    ]
    keep = {
        tick
        for tick in ordered
        if all(abs(tick - boundary) >= embargo_ticks for boundary in boundaries)
    }
    post = {role: [tick for tick in pre[role] if tick in keep] for role in roles}
    return pre, post, boundaries


def build_support(config: dict[str, Any]) -> dict[str, Any]:
    synthetic = config["synthetic"]
    run_length = int(synthetic["ticks_per_contiguous_run"])
    gaps = [int(value) for value in synthetic["gap_ticks"]]
    if run_length < 1 or len(gaps) != 2 or any(value < 1 for value in gaps):
        raise ProtocolError("synthetic support requires three positive-length runs")
    response_ticks: list[int] = []
    cursor = 0
    for run_index in range(3):
        response_ticks.extend(range(cursor, cursor + run_length))
        cursor += run_length
        if run_index < len(gaps):
            cursor += gaps[run_index]
    blocks = [array.astype(np.int64).tolist() for array in np.array_split(response_ticks, 4)]
    if any(not block for block in blocks):
        raise ProtocolError("empty outer block")
    embargo = int(config["stage1"]["embargo_ticks"])
    minimum = int(config["stage1"]["minimum_role_rows"])
    outer_folds: list[dict[str, Any]] = []
    all_ticks = set(response_ticks)
    for outer_block in range(4):
        outer_labels = {
            tick: ("outer_test" if tick in set(blocks[outer_block]) else "outer_train")
            for tick in response_ticks
        }
        outer_pre, outer_post, outer_boundaries = _role_arrays(response_ticks, outer_labels, embargo)
        rotations = []
        for inner_validation_block in range(4):
            if inner_validation_block == outer_block:
                continue
            validation = set(blocks[inner_validation_block])
            test = set(blocks[outer_block])
            labels = {
                tick: (
                    "outer_test"
                    if tick in test
                    else "inner_validation"
                    if tick in validation
                    else "inner_train"
                )
                for tick in response_ticks
            }
            pre, post, boundaries = _role_arrays(response_ticks, labels, embargo)
            for role in ("outer_test", "inner_validation", "inner_train"):
                if len(post[role]) < minimum:
                    raise ProtocolError(f"undersized {role} in outer fold {outer_block}")
            if set(post["outer_test"]) & (set(post["inner_train"]) | set(post["inner_validation"])):
                raise ProtocolError("outer-test leakage into inner fitting")
            if set().union(*(set(values) for values in post.values())) - all_ticks:
                raise ProtocolError("role map introduced unsupported ticks")
            rotations.append(
                {
                    "inner_validation_block": inner_validation_block,
                    "pre_embargo": pre,
                    "post_embargo": post,
                    "boundaries": boundaries,
                }
            )
        for role in ("outer_train", "outer_test"):
            if len(outer_post[role]) < minimum:
                raise ProtocolError(f"undersized {role} in outer fold {outer_block}")
        outer_folds.append(
            {
                "outer_block": outer_block,
                "pre_embargo": outer_pre,
                "post_embargo": outer_post,
                "boundaries": outer_boundaries,
                "inner_rotations": rotations,
            }
        )
    lag_cfg = config["stage1"]["lag_ticks"]
    lag_grid = list(range(int(lag_cfg["minimum"]), int(lag_cfg["maximum"]) + 1, int(lag_cfg["step"])))
    lag_source_ticks = [
        {"lag_tick": lag, "source_ticks": [tick - lag for tick in response_ticks]}
        for lag in lag_grid
    ]
    payload = {
        "response_ticks": response_ticks,
        "lag_source_ticks": lag_source_ticks,
        "segments": maximal_segments(response_ticks),
        "outer_folds": outer_folds,
    }
    payload["support_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    return payload


def _rng(config: dict[str, Any], *labels: str) -> np.random.Generator:
    domain = config["synthetic"]["rng_domain"].encode("utf-8")
    identity = canonical_json_bytes([str(label) for label in labels])
    seed = int.from_bytes(hashlib.sha256(domain + identity).digest()[:16], "big")
    return np.random.Generator(np.random.PCG64(seed))


def _rows(indices: dict[int, int], ticks: Sequence[int]) -> np.ndarray:
    try:
        return np.asarray([indices[int(tick)] for tick in ticks], dtype=np.int64)
    except KeyError as exc:
        raise ProtocolError(f"tick is outside frozen support: {exc}") from exc


def _standardize_group(
    train: np.ndarray, evaluations: Sequence[np.ndarray], floor: float
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray]:
    train = np.asarray(train, dtype=np.float64)
    if train.ndim != 2 or not np.all(np.isfinite(train)):
        raise ProtocolError("nonfinite or malformed training predictors")
    mean = train.mean(axis=0)
    sd = train.std(axis=0, ddof=0)
    mask = sd >= floor
    train_z = (train[:, mask] - mean[mask]) / sd[mask]
    eval_z = []
    for value in evaluations:
        array = np.asarray(value, dtype=np.float64)
        if array.ndim != 2 or array.shape[1] != train.shape[1] or not np.all(np.isfinite(array)):
            raise ProtocolError("nonfinite or incompatible evaluation predictors")
        eval_z.append((array[:, mask] - mean[mask]) / sd[mask])
    return train_z, eval_z, mask


def grouped_ridge_predict(
    nuisance_train: np.ndarray,
    representation_train: np.ndarray,
    target_train: np.ndarray,
    nuisance_eval: np.ndarray,
    representation_eval: np.ndarray,
    alpha: float,
    rho: float,
    sd_floor: float,
    residual_tolerance: float,
) -> tuple[np.ndarray, float]:
    n_train = np.asarray(nuisance_train, dtype=np.float64)
    x_train = np.asarray(representation_train, dtype=np.float64)
    y_train = np.asarray(target_train, dtype=np.float64).reshape(-1)
    n_eval = np.asarray(nuisance_eval, dtype=np.float64)
    x_eval = np.asarray(representation_eval, dtype=np.float64)
    if n_train.ndim != 2 or x_train.ndim != 2 or len(y_train) != len(n_train) or len(y_train) != len(x_train):
        raise ProtocolError("incompatible ridge training shapes")
    if len(y_train) < 2 or not np.all(np.isfinite(y_train)) or float(np.var(y_train)) <= 0:
        raise ProtocolError("invalid ridge target")
    if not (math.isfinite(alpha) and math.isfinite(rho) and alpha > 0 and rho > 0):
        raise ProtocolError("invalid ridge penalty")
    if not math.isfinite(residual_tolerance) or residual_tolerance < 0:
        raise ProtocolError("invalid ridge residual tolerance")
    n_z, [n_eval_z], _ = _standardize_group(n_train, [n_eval], sd_floor)
    x_z, [x_eval_z], _ = _standardize_group(x_train, [x_eval], sd_floor)
    design = np.column_stack([np.ones(len(y_train)), n_z, x_z]).astype(np.float64, copy=False)
    eval_design = np.column_stack([np.ones(len(n_eval_z)), n_eval_z, x_eval_z]).astype(np.float64, copy=False)
    penalties = np.concatenate(
        [np.zeros(1), np.full(n_z.shape[1], alpha), np.full(x_z.shape[1], alpha * rho)]
    )
    gram = design.T @ design / len(y_train) + np.diag(penalties)
    rhs = design.T @ y_train / len(y_train)
    if not np.all(np.isfinite(gram)) or not np.all(np.isfinite(rhs)):
        raise ProtocolError("nonfinite ridge system")
    try:
        chol = np.linalg.cholesky(gram)
        coefficient = np.linalg.solve(chol.T, np.linalg.solve(chol, rhs))
    except np.linalg.LinAlgError as exc:
        raise ProtocolError("ridge Cholesky failed; no fallback is allowed") from exc
    denominator = np.linalg.norm(gram) * np.linalg.norm(coefficient) + np.linalg.norm(rhs)
    relative_residual = float(np.linalg.norm(gram @ coefficient - rhs) / max(denominator, np.finfo(float).tiny))
    if not math.isfinite(relative_residual) or relative_residual > residual_tolerance:
        raise ProtocolError(f"ridge residual {relative_residual} exceeds tolerance")
    prediction = eval_design @ coefficient
    if not np.all(np.isfinite(prediction)):
        raise ProtocolError("nonfinite ridge prediction")
    return prediction, relative_residual


def _score(y_train: np.ndarray, y_eval: np.ndarray, prediction: np.ndarray) -> tuple[float, float, float]:
    y_train = np.asarray(y_train, dtype=np.float64).reshape(-1)
    y_eval = np.asarray(y_eval, dtype=np.float64).reshape(-1)
    prediction = np.asarray(prediction, dtype=np.float64).reshape(-1)
    if (
        len(y_train) < 2
        or len(y_eval) < 2
        or len(y_eval) != len(prediction)
        or not np.all(np.isfinite(y_train))
        or not np.all(np.isfinite(y_eval))
        or not np.all(np.isfinite(prediction))
        or float(np.var(y_eval, ddof=0)) <= 0
    ):
        raise ProtocolError("invalid or zero-variance score target")
    sse = float(np.sum((y_eval - prediction) ** 2))
    sst = float(np.sum((y_eval - float(np.mean(y_train))) ** 2))
    if not math.isfinite(sse) or not math.isfinite(sst) or sst <= 0:
        raise ProtocolError("invalid SSE/SST")
    return 1.0 - sse / sst, sse, sst


def _pearson(y: np.ndarray, prediction: np.ndarray) -> float:
    y = np.asarray(y, dtype=np.float64)
    prediction = np.asarray(prediction, dtype=np.float64)
    if len(y) < 2 or float(np.std(y)) == 0 or float(np.std(prediction)) == 0:
        raise ProtocolError("undefined Pearson correlation")
    value = float(np.corrcoef(y, prediction)[0, 1])
    if not math.isfinite(value):
        raise ProtocolError("nonfinite Pearson correlation")
    return float(np.clip(value, -1.0 + 1e-7, 1.0 - 1e-7))


def _lookup_representation(
    values: dict[int, np.ndarray], response_ticks: Sequence[int], lag_tick: int
) -> np.ndarray:
    try:
        return np.vstack([values[int(tick) - int(lag_tick)] for tick in response_ticks]).astype(np.float64)
    except KeyError as exc:
        raise ProtocolError(f"missing absolute lag-source tick: {exc}") from exc


def _best(candidates: Iterable[tuple[float, tuple[Any, ...], Any]], tolerance: float) -> Any:
    materialized = list(candidates)
    if not materialized:
        raise ProtocolError("empty hyperparameter search")
    highest = max(item[0] for item in materialized)
    tied = [item for item in materialized if highest - item[0] <= tolerance]
    return min(tied, key=lambda item: item[1])[2]


def _synthetic_arrays(
    config: dict[str, Any], response_ticks: list[int], patient: str, electrode: str
) -> tuple[np.ndarray, np.ndarray, dict[int, np.ndarray], dict[str, dict[int, np.ndarray]]]:
    synthetic = config["synthetic"]
    n_features = int(synthetic["nuisance_features"])
    x_features = int(synthetic["representation_features"])
    lag_min = int(config["stage1"]["lag_ticks"]["minimum"])
    lag_max = int(config["stage1"]["lag_ticks"]["maximum"])
    source_ticks = range(min(response_ticks) - lag_max, max(response_ticks) - lag_min + 1)
    all_ticks = np.asarray(list(source_ticks), dtype=np.float64)
    phase = (_rng(config, patient, electrode, "phase").uniform(-math.pi, math.pi))
    latent_all = np.sin(0.031 * all_ticks + phase) + 0.55 * np.cos(0.013 * all_ticks - 0.4 * phase)
    response_array = np.asarray(response_ticks, dtype=np.float64)
    latent_response = np.sin(0.031 * response_array + phase) + 0.55 * np.cos(0.013 * response_array - 0.4 * phase)
    nuisance_rng = _rng(config, patient, electrode, "nuisance")
    nuisance_columns = [
        np.sin((0.005 + 0.002 * j) * response_array + 0.3 * j)
        + 0.2 * nuisance_rng.normal(size=len(response_array))
        for j in range(n_features)
    ]
    nuisance = np.column_stack(nuisance_columns).astype(np.float64)
    target_rng = _rng(config, patient, electrode, "target")
    nuisance_weight = np.linspace(0.15, -0.08, n_features)
    patient_scale = 1.0 + 0.04 * int(patient[-2:])
    target = nuisance @ nuisance_weight + patient_scale * latent_response + 0.16 * target_rng.normal(size=len(response_array))
    f_rng = _rng(config, patient, electrode, "F")
    f_matrix = f_rng.normal(size=(len(all_ticks), x_features))
    f_matrix[:, 0] += 0.08 * latent_all
    frozen = {int(tick): f_matrix[index].copy() for index, tick in enumerate(all_ticks.astype(np.int64))}
    tuned: dict[str, dict[int, np.ndarray]] = {}
    for source in config["stage1"]["source_ids"]:
        source_rng = _rng(config, patient, electrode, source, "B_1")
        matrix = 0.22 * source_rng.normal(size=(len(all_ticks), x_features))
        matrix[:, 0] += latent_all
        if x_features > 1:
            matrix[:, 1] += 0.65 * latent_all + 0.25 * np.sin(0.071 * all_ticks)
        tuned[source] = {int(tick): matrix[index].copy() for index, tick in enumerate(all_ticks.astype(np.int64))}
    return nuisance, target.astype(np.float64), frozen, tuned


def _fit_cell(
    config: dict[str, Any],
    support: dict[str, Any],
    nuisance: np.ndarray,
    target: np.ndarray,
    representation: dict[int, np.ndarray],
    frozen_lags: list[int] | None,
    shared_nuisance: list[dict[str, Any]] | None,
) -> tuple[dict[str, Any], list[int], list[dict[str, Any]]]:
    stage = config["stage1"]
    synthetic = config["synthetic"]
    response_ticks = support["response_ticks"]
    tick_to_row = {tick: index for index, tick in enumerate(response_ticks)}
    lags = [int(value) for value in synthetic["development_lag_ticks"]]
    alphas = [float(value) for value in synthetic["development_ridge_alpha"]]
    rhos = [float(value) for value in synthetic["development_representation_penalty_ratio"]]
    tie = float(stage["tie_tolerance"])
    sd_floor = float(stage["drop_sd_below"])
    residual_tolerance = float(stage["solver_residual_tolerance"])
    empty_train = np.empty((len(target), 0), dtype=np.float64)
    selected_lag: list[int] = []
    selected_alpha: list[float] = []
    selected_rho: list[float] = []
    selected_nuisance_alpha: list[float] = []
    selected_x_only_alpha: list[float] = []
    accumulators: list[dict[str, Any]] = []
    nuisance_state: list[dict[str, Any]] = []
    x_targets: list[np.ndarray] = []
    x_predictions: list[np.ndarray] = []
    for fold in support["outer_folds"]:
        outer_block = int(fold["outer_block"])
        inner_cache = []
        for rotation in fold["inner_rotations"]:
            train_rows = _rows(tick_to_row, rotation["post_embargo"]["inner_train"])
            validation_rows = _rows(tick_to_row, rotation["post_embargo"]["inner_validation"])
            inner_cache.append((rotation, train_rows, validation_rows))
        if shared_nuisance is None:
            nuisance_candidates = []
            for alpha in alphas:
                scores = []
                for _, train_rows, validation_rows in inner_cache:
                    prediction, _ = grouped_ridge_predict(
                        nuisance[train_rows], empty_train[train_rows], target[train_rows],
                        nuisance[validation_rows], empty_train[validation_rows], alpha, 1.0,
                        sd_floor, residual_tolerance,
                    )
                    score, _, _ = _score(target[train_rows], target[validation_rows], prediction)
                    scores.append(score)
                nuisance_candidates.append((float(np.mean(scores)), (alpha,), alpha))
            nuisance_alpha = float(_best(nuisance_candidates, tie))
            nuisance_inner_scores = []
            for _, train_rows, validation_rows in inner_cache:
                prediction, _ = grouped_ridge_predict(
                    nuisance[train_rows], empty_train[train_rows], target[train_rows],
                    nuisance[validation_rows], empty_train[validation_rows], nuisance_alpha, 1.0,
                    sd_floor, residual_tolerance,
                )
                score, _, _ = _score(target[train_rows], target[validation_rows], prediction)
                nuisance_inner_scores.append(score)
        else:
            if len(shared_nuisance) != 4 or int(shared_nuisance[outer_block]["block"]) != outer_block:
                raise ProtocolError("shared nuisance state is incomplete or out of order")
            nuisance_alpha = float(shared_nuisance[outer_block]["selected_alpha"])
            nuisance_inner_scores = [float(value) for value in shared_nuisance[outer_block]["inner_scores"]]
            if len(nuisance_inner_scores) != 3:
                raise ProtocolError("shared nuisance state has wrong inner cardinality")
        selected_nuisance_alpha.append(nuisance_alpha)
        candidate_lags = [int(frozen_lags[outer_block])] if frozen_lags is not None else lags
        full_candidates = []
        for lag in candidate_lags:
            full_representation = _lookup_representation(representation, response_ticks, lag)
            for alpha in alphas:
                for rho in rhos:
                    unique_scores = []
                    for rotation_index, (_, train_rows, validation_rows) in enumerate(inner_cache):
                        prediction, _ = grouped_ridge_predict(
                            nuisance[train_rows], full_representation[train_rows], target[train_rows],
                            nuisance[validation_rows], full_representation[validation_rows], alpha, rho,
                            sd_floor, residual_tolerance,
                        )
                        score, _, _ = _score(target[train_rows], target[validation_rows], prediction)
                        unique_scores.append(score - nuisance_inner_scores[rotation_index])
                    key = (abs(lag), lag, alpha, rho)
                    full_candidates.append((float(np.mean(unique_scores)), key, (lag, alpha, rho)))
        lag, alpha, rho = _best(full_candidates, tie)
        if frozen_lags is not None and int(lag) != int(frozen_lags[outer_block]):
            raise ProtocolError("arm changed frozen pretrained lag")
        selected_lag.append(int(lag))
        selected_alpha.append(float(alpha))
        selected_rho.append(float(rho))
        full_representation = _lookup_representation(representation, response_ticks, int(lag))
        x_candidates = []
        for x_alpha in alphas:
            fisher_scores = []
            for _, train_rows, validation_rows in inner_cache:
                prediction, _ = grouped_ridge_predict(
                    empty_train[train_rows], full_representation[train_rows], target[train_rows],
                    empty_train[validation_rows], full_representation[validation_rows], x_alpha, 1.0,
                    sd_floor, residual_tolerance,
                )
                fisher_scores.append(float(np.arctanh(_pearson(target[validation_rows], prediction))))
            x_candidates.append((float(np.mean(fisher_scores)), (x_alpha,), x_alpha))
        x_alpha = float(_best(x_candidates, tie))
        selected_x_only_alpha.append(x_alpha)
        train_rows = _rows(tick_to_row, fold["post_embargo"]["outer_train"])
        test_rows = _rows(tick_to_row, fold["post_embargo"]["outer_test"])
        if shared_nuisance is None:
            nuisance_prediction, _ = grouped_ridge_predict(
                nuisance[train_rows], empty_train[train_rows], target[train_rows],
                nuisance[test_rows], empty_train[test_rows], nuisance_alpha, 1.0,
                sd_floor, residual_tolerance,
            )
            _, nuisance_sse, sst = _score(target[train_rows], target[test_rows], nuisance_prediction)
        else:
            nuisance_sse = float(shared_nuisance[outer_block]["sse_nuisance"])
            sst = float(shared_nuisance[outer_block]["sst"])
            if int(shared_nuisance[outer_block]["n_test"]) != len(test_rows):
                raise ProtocolError("shared nuisance test cardinality drift")
        full_prediction, _ = grouped_ridge_predict(
            nuisance[train_rows], full_representation[train_rows], target[train_rows],
            nuisance[test_rows], full_representation[test_rows], float(alpha), float(rho),
            sd_floor, residual_tolerance,
        )
        _, full_sse, full_sst = _score(target[train_rows], target[test_rows], full_prediction)
        if full_sst != sst:
            raise ProtocolError("SST drift between shared outer fits")
        x_prediction, _ = grouped_ridge_predict(
            empty_train[train_rows], full_representation[train_rows], target[train_rows],
            empty_train[test_rows], full_representation[test_rows], x_alpha, 1.0,
            sd_floor, residual_tolerance,
        )
        x_targets.append(target[test_rows].copy())
        x_predictions.append(x_prediction.copy())
        accumulators.append(
            {
                "block": outer_block,
                "sse_full": full_sse,
                "sse_nuisance": nuisance_sse,
                "sst": sst,
                "n_test": int(len(test_rows)),
            }
        )
        nuisance_state.append(
            {
                "block": outer_block,
                "selected_alpha": nuisance_alpha,
                "inner_scores": nuisance_inner_scores,
                "sse_nuisance": nuisance_sse,
                "sst": sst,
                "n_test": int(len(test_rows)),
            }
        )
    cell_payload = {
        "selected_lag_tick": selected_lag,
        "selected_alpha": selected_alpha,
        "selected_rho": selected_rho,
        "selected_nuisance_alpha": selected_nuisance_alpha,
        "selected_x_only_alpha": selected_x_only_alpha,
        "x_only_pearson_r": _pearson(np.concatenate(x_targets), np.concatenate(x_predictions)),
        "fold_accumulators": accumulators,
    }
    return cell_payload, selected_lag, nuisance_state


def build_synthetic_raw(config: dict[str, Any], sentinel: AccessSentinel) -> dict[str, Any]:
    support = build_support(config)
    cells: list[dict[str, Any]] = []
    patient_ids = config["stage1"]["patient_ids"]
    source_ids = config["stage1"]["source_ids"]
    electrodes = [f"synthetic-e{index + 1:02d}" for index in range(int(config["synthetic"]["electrodes_per_patient"]))]
    for patient in patient_ids:
        for electrode in electrodes:
            nuisance, target, frozen_values, tuned_values = _synthetic_arrays(
                config, support["response_ticks"], patient, electrode
            )
            frozen_payload, frozen_lags, shared_nuisance = _fit_cell(
                config, support, nuisance, target, frozen_values, frozen_lags=None,
                shared_nuisance=None,
            )
            for source in source_ids:
                frozen_cell = {
                    "patient_id": patient,
                    "electrode_id": electrode,
                    "source_id": source,
                    "arm": "F",
                    **copy.deepcopy(frozen_payload),
                }
                cells.append(frozen_cell)
                tuned_payload, returned_lags, _ = _fit_cell(
                    config, support, nuisance, target, tuned_values[source], frozen_lags=frozen_lags,
                    shared_nuisance=shared_nuisance,
                )
                if returned_lags != frozen_lags:
                    raise ProtocolError("B_1 did not preserve F lag")
                tuned_cell = {
                    "patient_id": patient,
                    "electrode_id": electrode,
                    "source_id": source,
                    "arm": "B_1",
                    **tuned_payload,
                }
                cells.append(tuned_cell)
    expected = len(patient_ids) * len(electrodes) * len(source_ids) * 2
    if len(cells) != expected:
        raise ProtocolError(f"wrong synthetic cell cardinality: {len(cells)} != {expected}")
    parameters = {
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
    parameters["patient_ids"] = list(patient_ids)
    parameters["source_ids"] = list(source_ids)
    provider = {
        "provider_id": config["synthetic"]["provider_id"],
        "identity_sha256": sha256_bytes(canonical_json_bytes(parameters)),
        "rng_domain": config["synthetic"]["rng_domain"],
        "parameters": parameters,
    }
    payload = {
        "schema_version": config["raw_result_schema"]["schema_version"],
        "experiment_id": "E028",
        "protocol_state": config["protocol_state"],
        "synthetic_only": True,
        "ready_for_endpoint_access": False,
        "readiness_label": "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY",
        "provider": provider,
        "support": support,
        "cells": cells,
        "sentinels": sentinel.summary(),
    }
    return with_content_hash(payload)


def run_benchmark(config: dict[str, Any]) -> dict[str, Any]:
    spec = config["synthetic"]["benchmark"]
    rows = int(spec["rows"])
    n_features = int(spec["nuisance_features"])
    x_features = int(spec["representation_features"])
    targets = int(spec["targets"])
    repetitions = int(spec["repetitions"])
    rng = _rng(config, "benchmark")
    nuisance = rng.normal(size=(rows, n_features)).astype(np.float64)
    representation = rng.normal(size=(rows, x_features)).astype(np.float64)
    weights_n = rng.normal(scale=0.15, size=(n_features, targets))
    weights_x = rng.normal(scale=0.08, size=(x_features, targets))
    response = nuisance @ weights_n + representation @ weights_x + rng.normal(scale=0.2, size=(rows, targets))
    split = rows * 3 // 4
    start = time.perf_counter()
    hashes: list[str] = []
    residuals: list[float] = []
    for repetition in range(repetitions):
        for target in range(targets):
            prediction, residual = grouped_ridge_predict(
                nuisance[:split], representation[:split], response[:split, target],
                nuisance[split:], representation[split:], 1.0, 1.0,
                float(config["stage1"]["drop_sd_below"]),
                float(config["stage1"]["solver_residual_tolerance"]),
            )
            residuals.append(residual)
            hashes.append(sha256_bytes(prediction.astype("<f8", copy=False).tobytes()))
    for target in range(targets):
        if len(set(hashes[target::targets])) != 1:
            raise ProtocolError("benchmark prediction replay is not deterministic")
    wall = time.perf_counter() - start
    peak_kib = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    payload = {
        "schema_version": "e028-development-kernel-benchmark-v1",
        "experiment_id": "E028",
        "synthetic_only": True,
        "production_shape": False,
        "ready_for_endpoint_access": False,
        "readiness_label": "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY",
        "shape": {
            "rows": rows,
            "nuisance_features": n_features,
            "representation_features": x_features,
            "targets": targets,
            "repetitions": repetitions,
        },
        "dtype": "float64",
        "wall_seconds": wall,
        "peak_rss_kib_process": peak_kib,
        "peak_vram_bytes": 0,
        "maximum_relative_linear_residual": max(residuals),
        "one_thread_environment": {
            key: os.environ[key] for key in _THREAD_ENVIRONMENT_KEYS
        },
        "prediction_hashes_sha256": sha256_bytes(canonical_json_bytes(hashes)),
        "limitation": "Local regression-kernel benchmark only; not the protocol production-shape benchmark.",
    }
    return with_content_hash(payload)


def selftest(config: dict[str, Any]) -> dict[str, Any]:
    checks: list[str] = []
    support_a = build_support(config)
    support_b = build_support(config)
    if canonical_json_bytes(support_a) != canonical_json_bytes(support_b):
        raise ProtocolError("support replay is not deterministic")
    checks.append("support-deterministic")
    ticks = support_a["response_ticks"]
    if [segment["n_ticks"] for segment in support_a["segments"]] != [420, 420, 420]:
        raise ProtocolError("gap-preserving segment fixture failed")
    lag_two = next(item for item in support_a["lag_source_ticks"] if item["lag_tick"] == 2)
    if any(source != response - 2 for source, response in zip(lag_two["source_ticks"], ticks)):
        raise ProtocolError("absolute lag lookup fixture failed")
    checks.append("absolute-tick-gap-lag")
    short_ticks = list(range(600))
    labels = {tick: ("left" if tick < 300 else "right") for tick in short_ticks}
    _, post, _ = _role_arrays(short_ticks, labels, 120)
    if len(post["left"]) != 180 or len(post["right"]) != 180:
        raise ProtocolError("strict 120-tick in-segment embargo fixture failed")
    long_gap_ticks = list(range(200)) + list(range(500, 700))
    long_labels = {tick: ("left" if tick < 200 else "right") for tick in long_gap_ticks}
    _, long_post, _ = _role_arrays(long_gap_ticks, long_labels, 120)
    if len(long_post["left"]) != 200 or len(long_post["right"]) != 200:
        raise ProtocolError("gap-absorbed embargo fixture failed")
    checks.append("simultaneous-embargo")
    train = np.asarray([[1.0, 7.0], [2.0, 7.0], [3.0, 7.0]])
    eval_array = np.asarray([[4.0, 100.0]])
    train_z, [eval_z], mask = _standardize_group(train, [eval_array], 1e-8)
    if mask.tolist() != [True, False] or not np.allclose(train_z.mean(axis=0), 0) or not np.allclose(eval_z, [[2.449489742783178]]):
        raise ProtocolError("training-only standardization fixture failed")
    checks.append("train-only-standardization")
    rng = _rng(config, "ridge-fixture")
    n = rng.normal(size=(64, 3))
    x = rng.normal(size=(64, 4))
    y = 0.4 + n @ np.asarray([0.2, -0.1, 0.3]) + x @ np.asarray([0.4, 0.0, -0.2, 0.1])
    prediction, residual = grouped_ridge_predict(n[:48], x[:48], y[:48], n[48:], x[48:], 0.1, 2.0, 1e-8, 1e-10)
    if prediction.shape != (16,) or residual > 1e-10:
        raise ProtocolError("ridge fixture failed")
    n_train = n[:48]
    x_train = x[:48]
    n_mean, n_sd = n_train.mean(axis=0), n_train.std(axis=0, ddof=0)
    x_mean, x_sd = x_train.mean(axis=0), x_train.std(axis=0, ddof=0)
    design = np.column_stack(
        [np.ones(48), (n_train - n_mean) / n_sd, (x_train - x_mean) / x_sd]
    )
    eval_design = np.column_stack(
        [np.ones(16), (n[48:] - n_mean) / n_sd, (x[48:] - x_mean) / x_sd]
    )
    penalty = np.diag(np.concatenate([np.zeros(1), np.full(3, 0.1), np.full(4, 0.2)]))
    closed_form = np.linalg.solve(design.T @ design / 48 + penalty, design.T @ y[:48] / 48)
    if not np.allclose(prediction, eval_design @ closed_form, rtol=0.0, atol=1e-12):
        raise ProtocolError("ridge Cholesky does not match independent mean-MSE closed form")
    original_cholesky = np.linalg.cholesky
    try:
        def _forced_factorization_failure(matrix: np.ndarray) -> np.ndarray:
            raise np.linalg.LinAlgError("synthetic singular fixture")

        np.linalg.cholesky = _forced_factorization_failure  # type: ignore[assignment]
        try:
            grouped_ridge_predict(
                n[:48], x[:48], y[:48], n[48:], x[48:], 0.1, 2.0, 1e-8, 1e-10
            )
        except ProtocolError:
            pass
        else:
            raise ProtocolError("ridge factorization-failure fixture failed")
    finally:
        np.linalg.cholesky = original_cholesky  # type: ignore[assignment]
    try:
        grouped_ridge_predict(
            n[:48], x[:48], y[:48], n[48:], x[48:], 0.1, 2.0, 1e-8,
            np.nextafter(0.0, 1.0),
        )
    except ProtocolError:
        pass
    else:
        raise ProtocolError("ridge residual-rejection fixture failed")
    support_before_nan = support_a["support_sha256"]
    x_bad = x.copy()
    x_bad[0, 0] = np.nan
    try:
        grouped_ridge_predict(
            n[:48], x_bad[:48], y[:48], n[48:], x_bad[48:], 0.1, 2.0, 1e-8, 1e-10
        )
    except ProtocolError:
        pass
    else:
        raise ProtocolError("arm-specific NaN fixture failed")
    if build_support(config)["support_sha256"] != support_before_nan:
        raise ProtocolError("arm-specific NaN altered frozen support")
    checks.append("float64-cholesky-ridge")
    checks.append("arm-nan-fail-closed")
    if any(os.environ.get(key) != "1" for key in _THREAD_ENVIRONMENT_KEYS):
        raise ProtocolError("one-thread numerical environment fixture failed")
    checks.append("one-thread-environment")
    r2, sse, sst = _score(np.asarray([0.0, 2.0]), np.asarray([1.0, 3.0]), np.asarray([1.0, 2.0]))
    if not np.isclose(r2, 0.75) or not np.isclose(sse, 1.0) or not np.isclose(sst, 4.0):
        raise ProtocolError("pooled SSE/SST fixture failed")
    try:
        _score(np.asarray([0.0, 1.0]), np.asarray([2.0, 2.0]), np.asarray([2.0, 2.0]))
    except ProtocolError:
        pass
    else:
        raise ProtocolError("zero-variance evaluation target fixture failed")
    checks.append("pooled-sse-sst")
    fixed_rng_outputs = {
        ("benchmark",): [0.07124584220241248, 0.32447112346146645, 0.5590319665022763, 0.6445863240115381],
        ("ridge-fixture",): [0.5317866423563055, 0.7541877950662648, 0.38237953784806733, 0.19188161684218863],
        ("synthetic-p01", "synthetic-e01", "phase"): [0.4628434152639086, 0.5788369006959299, 0.58788545280149, 0.8020740328202259],
        ("synthetic-p01", "synthetic-e01", "nuisance"): [0.12459755236729797, 0.9586238963960174, 0.9346589881667637, 0.8560485211725215],
        ("synthetic-p01", "synthetic-e01", "target"): [0.43224952751389856, 0.03256131065695611, 0.031165179864768855, 0.5516700683860868],
        ("synthetic-p01", "synthetic-e01", "F"): [0.7790113134334956, 0.7840335548065377, 0.24654349840167222, 0.049320926234895035],
        ("synthetic-p01", "synthetic-e01", "synthetic-q01", "B_1"): [0.8942118920046208, 0.9352387112976024, 0.28322044309235817, 0.9303801366003127],
    }
    for labels, expected_values in fixed_rng_outputs.items():
        if _rng(config, *labels).random(4).tolist() != expected_values:
            raise ProtocolError(f"stored RNG fixture changed for {labels}")
    base_labels = ("patient", "electrode", "source", "arm")
    base_values = _rng(config, *base_labels).random(4).tolist()
    for index in range(len(base_labels)):
        changed = list(base_labels)
        changed[index] += "-changed"
        if _rng(config, *changed).random(4).tolist() == base_values:
            raise ProtocolError(f"RNG key perturbation failed at position {index}")
    checks.append("rng-domain-replay")
    isolated = AccessSentinel(config["forbidden_path_components"])
    try:
        isolated.check_path(ROOT / "data" / "forbidden.bin")
    except ProtocolError:
        pass
    else:
        raise ProtocolError("path sentinel fixture failed")
    try:
        isolated._blocked_network()
    except ProtocolError:
        pass
    else:
        raise ProtocolError("network sentinel fixture failed")
    if len(isolated.forbidden_attempts) != 1 or isolated.network_attempts != 1:
        raise ProtocolError("sentinel counters failed")
    checks.append("path-network-sentinel")
    manifest = development_manifest(config)
    validate_content_hash(manifest)
    mutated = copy.deepcopy(manifest)
    mutated["scope"] += "x"
    try:
        validate_content_hash(mutated)
    except ProtocolError:
        pass
    else:
        raise ProtocolError("one-byte manifest mutation fixture failed")
    checks.append("development-manifest-hash")
    return {
        "status": "PASS",
        "checks": checks,
        "synthetic_only": True,
        "ready_for_endpoint_access": False,
        "readiness_label": "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY",
    }


def build_bundle(config: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "e028-development-bundle-v1",
        "experiment_id": "E028",
        "synthetic_only": True,
        "development_manifest": development_manifest(config),
        "ready_for_endpoint_access": False,
        "stage2_licensed": False,
        "verdict": "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY",
        "neural_files_opened": [],
        "author_results_parsed": False,
        "production_provider_present": False,
        "production_rfc8785_chain_satisfied": False,
        "unresolved": list(config["development_gaps"]),
    }
    return with_content_hash(payload)


def _output_required(command: str, output: Path | None) -> Path:
    if output is None:
        raise ProtocolError(f"{command} requires --output")
    return output


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=RUNNER_COMMANDS)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        forbidden = config["forbidden_path_components"]
        with AccessSentinel(forbidden) as sentinel:
            if args.command == "selftest":
                result = selftest(config)
            elif args.command == "manifest":
                output = _output_required(args.command, args.output)
                result = development_manifest(config)
                atomic_write_json(output, result, forbidden)
            elif args.command == "synthetic-replay":
                output = _output_required(args.command, args.output)
                result = build_synthetic_raw(config, sentinel)
                atomic_write_json(output, result, forbidden)
            elif args.command == "benchmark":
                output = _output_required(args.command, args.output)
                result = run_benchmark(config)
                atomic_write_json(output, result, forbidden)
            elif args.command == "bundle":
                output = _output_required(args.command, args.output)
                result = build_bundle(config)
                atomic_write_json(output, result, forbidden)
            else:  # pragma: no cover - argparse and config both deny this path.
                raise ProtocolError(f"command not allowed: {args.command}")
            if sentinel.forbidden_attempts or sentinel.network_attempts:
                raise ProtocolError("sentinel observed a forbidden access")
    except ProtocolError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        return 2
    summary = {
        "status": result.get("status", "PASS"),
        "command": args.command,
        "synthetic_only": True,
        "ready_for_endpoint_access": False,
        "readiness_label": result.get(
            "readiness_label", result.get("verdict", "SYNTHETIC DEVELOPMENT SLICE ONLY; NOT READY")
        ),
        "content_sha256": result.get("content_sha256"),
    }
    if args.command == "selftest":
        summary["checks"] = result["checks"]
    print(json.dumps(summary, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
