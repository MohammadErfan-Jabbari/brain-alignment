#!/usr/bin/env python3
"""Frozen aggregation and mechanical classification for E030.

The normal path reads only the frozen E030 raw fold-score JSON.  ``--selftest``
constructs and analyzes a synthetic fixture without opening any E030 outcome or
participant-response artifact.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import os
import resource
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import scipy
import sklearn
from scipy import optimize, stats


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_CONFIG = ROOT / "configs/e030_exact_substrate_transport.json"
ANALYSIS_SCHEMA = "e030-exact-substrate-analysis.v2"
RAW_SCHEMA = "e030-exact-substrate-raw.v2"
RUNNER_PATH = "scripts/e030_exact_substrate_transport.py"
ANALYZER_PATH = "scripts/e030_analyze_exact_substrate.py"
E_RECORD_PATH = "docs/experiments/E030_exact-substrate-transport-diagnostic.md"
FLOAT_ATOL = 1e-12
FLOAT_RTOL = 1e-10
SHA256_HEX_LEN = 64
VALIDITY_KEYS = {
    "inputs_hash_valid",
    "inputs_finite",
    "participant_grid_valid",
    "c1_grid_complete",
    "c2_grid_complete",
    "c3_grid_complete",
    "bridge_contributions_finite",
    "target_pca_basis_reuse_valid",
    "student_pca_basis_reuse_valid",
    "coordinate_floor_valid",
    "inherited_gates_valid",
    "all_pass",
}


class ProtocolError(ValueError):
    """Raised when a frozen protocol identity or data invariant fails."""


def sha256_file(path: Path, chunk_bytes: int = 16 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_bytes)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_array(value: np.ndarray) -> str:
    return sha256_bytes(np.ascontiguousarray(value).tobytes(order="C"))


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("utf-8")


def strict_json_load(path: Path) -> dict[str, Any]:
    def reject_constant(value: str) -> None:
        raise ProtocolError(f"non-finite JSON constant in {path}: {value}")

    try:
        payload = json.loads(path.read_text(), parse_constant=reject_constant)
    except (OSError, json.JSONDecodeError) as exc:
        raise ProtocolError(f"cannot read strict JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ProtocolError(f"top-level JSON must be an object: {path}")
    return payload


def atomic_json_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def pretty_json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def directory_regular_file_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(
        int(candidate.stat().st_size)
        for candidate in path.rglob("*")
        if candidate.is_file() and not candidate.is_symlink()
    )


def retained_storage_limit_bytes(config: Mapping[str, Any]) -> int:
    return int(float(config["compute_ceiling"]["retained_storage_gb"]) * 1024**3)


def enforce_retained_storage(
    config: Mapping[str, Any], *, projected_extra_bytes: int = 0
) -> int:
    output_dir = resolve_repo_path(
        config["paths"]["output_dir"], "config.paths.output_dir"
    )
    observed = directory_regular_file_bytes(output_dir)
    projected = observed + int(projected_extra_bytes)
    ceiling = retained_storage_limit_bytes(config)
    if projected > ceiling:
        raise ProtocolError(
            f"retained-output ceiling exceeded: {projected} > {ceiling} bytes"
        )
    return observed


def process_cpu_seconds() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return float(usage.ru_utime + usage.ru_stime)


def current_rss_kib() -> int:
    status = Path("/proc/self/status")
    if not status.is_file():
        raise ProtocolError(
            "Linux /proc/self/status is required for RSS enforcement"
        )
    for line in status.read_text(encoding="utf-8").splitlines():
        if line.startswith("VmRSS:"):
            fields = line.split()
            if len(fields) == 3 and fields[2] == "kB":
                return int(fields[1])
            break
    raise ProtocolError("cannot parse VmRSS from /proc/self/status")


def start_rss_watchdog(
    limit_kib: int, poll_seconds: float,
) -> tuple[threading.Event, threading.Thread]:
    initial_rss = current_rss_kib()
    if initial_rss > limit_kib:
        raise ProtocolError(
            f"analysis RSS already exceeds ceiling: {initial_rss} > {limit_kib} KiB"
        )
    stop = threading.Event()

    def monitor() -> None:
        while not stop.wait(poll_seconds):
            observed = current_rss_kib()
            if observed > limit_kib:
                message = (
                    f"E030 analysis RSS watchdog exceeded: {observed} > "
                    f"{limit_kib} KiB\n"
                ).encode("utf-8")
                os.write(2, message)
                os._exit(97)

    thread = threading.Thread(
        target=monitor, name="e030-analysis-rss-watchdog", daemon=True
    )
    thread.start()
    return stop, thread


def apply_analysis_resource_limits(config: Mapping[str, Any]) -> dict[str, Any]:
    ceiling = config["compute_ceiling"]
    cpu_budget_seconds = max(
        1, int(math.floor(float(ceiling["analysis_cpu_hours"]) * 3600.0))
    )
    cpu_soft = max(1, int(math.ceil(process_cpu_seconds())) + cpu_budget_seconds)
    _, cpu_hard = resource.getrlimit(resource.RLIMIT_CPU)
    if cpu_hard != resource.RLIM_INFINITY:
        cpu_soft = min(cpu_soft, int(cpu_hard))
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_soft, cpu_hard))
    address_space_bytes = int(float(ceiling["analysis_ram_gb"]) * 1024**3)
    _, as_hard = resource.getrlimit(resource.RLIMIT_AS)
    if as_hard != resource.RLIM_INFINITY:
        address_space_bytes = min(address_space_bytes, int(as_hard))
    resource.setrlimit(resource.RLIMIT_AS, (address_space_bytes, as_hard))
    return {
        "stage": "analysis",
        "cpu_budget_seconds": int(cpu_budget_seconds),
        "rlimit_cpu_soft_seconds": int(cpu_soft),
        "address_space_limit_bytes": int(address_space_bytes),
        "peak_rss_limit_kib": int(
            float(ceiling["analysis_ram_gb"]) * 1024 * 1024
        ),
        "retained_storage_limit_bytes": retained_storage_limit_bytes(config),
        "cpu_limit_mechanism": ceiling["cpu_limit_mechanism"],
        "memory_limit_mechanism": ceiling["memory_limit_mechanism"],
        "rss_watchdog_poll_seconds": float(
            ceiling["rss_watchdog_poll_seconds"]
        ),
        "retained_storage_scope": ceiling["retained_storage_scope"],
    }


def measured_analysis_resource_use(
    limits: Mapping[str, Any], *, started_wall: float, started_cpu: float
) -> dict[str, Any]:
    peak_rss_kib = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if peak_rss_kib > int(limits["peak_rss_limit_kib"]):
        raise ProtocolError(
            f"analysis peak RSS exceeded ceiling: {peak_rss_kib} > "
            f"{limits['peak_rss_limit_kib']} KiB"
        )
    return {
        **limits,
        "elapsed_wall_seconds": float(time.perf_counter() - started_wall),
        "elapsed_cpu_seconds": float(process_cpu_seconds() - started_cpu),
        "peak_rss_kib": peak_rss_kib,
    }


def expect_exact_keys(value: Mapping[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ProtocolError(f"{context} key mismatch; missing={missing}, extra={extra}")


def require_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProtocolError(f"{context} must be an object")
    return value


def require_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise ProtocolError(f"{context} must be a list")
    return value


def require_str(value: Any, context: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        raise ProtocolError(f"{context} must be a{' nonempty' if nonempty else ''} string")
    return value


def require_bool(value: Any, context: str) -> bool:
    if type(value) is not bool:
        raise ProtocolError(f"{context} must be boolean")
    return value


def require_int(value: Any, context: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ProtocolError(f"{context} must be an integer")
    return value


def require_float(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProtocolError(f"{context} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ProtocolError(f"{context} must be finite")
    return result


def require_sha256(value: Any, context: str) -> str:
    text = require_str(value, context)
    if len(text) != SHA256_HEX_LEN or any(ch not in "0123456789abcdef" for ch in text):
        raise ProtocolError(f"{context} must be a lowercase SHA-256 hex digest")
    return text


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=FLOAT_RTOL, abs_tol=FLOAT_ATOL)


def require_close(left: float, right: float, context: str) -> None:
    if not close(left, right):
        raise ProtocolError(f"{context} mismatch: observed={left:.17g}, expected={right:.17g}")


def require_array_close(left: Sequence[float], right: Sequence[float], context: str) -> None:
    a = np.asarray(left, dtype=np.float64)
    b = np.asarray(right, dtype=np.float64)
    if a.shape != b.shape or not np.allclose(a, b, rtol=FLOAT_RTOL, atol=FLOAT_ATOL):
        raise ProtocolError(f"{context} array mismatch")


def repo_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise ProtocolError(f"path escapes repository: {path}") from exc


def resolve_repo_path(path_text: str, context: str) -> Path:
    path = Path(path_text)
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ProtocolError(f"{context} escapes repository: {path_text}") from exc
    return resolved


def validate_timestamp(value: Any) -> str:
    text = require_str(value, "created_at_utc")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProtocolError(f"created_at_utc is not ISO-8601: {text}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ProtocolError("created_at_utc must carry a UTC offset")
    return text


def validate_config(config: Mapping[str, Any]) -> None:
    if config.get("experiment") != "E030":
        raise ProtocolError("config experiment must be E030")
    if config.get("protocol_version") != "e030-exact-substrate-transport.v2":
        raise ProtocolError("unexpected config protocol_version")
    substrate = require_mapping(config.get("substrate"), "config.substrate")
    estimator = require_mapping(config.get("estimator"), "config.estimator")
    inference = require_mapping(config.get("inference"), "config.inference")
    folds = require_mapping(config.get("folds"), "config.folds")
    target = require_mapping(config.get("target"), "config.target")
    bridge = require_mapping(config.get("bridge"), "config.bridge")
    compute = require_mapping(config.get("compute_ceiling"), "config.compute_ceiling")
    expect_exact_keys(
        compute,
        {
            "target_gpu",
            "target_gpu_hours",
            "scoring_cpu_hours",
            "scoring_ram_gb",
            "analysis_cpu_hours",
            "analysis_ram_gb",
            "retained_storage_gb",
            "blas_threads",
            "target_timeout_rule",
            "cpu_limit_mechanism",
            "memory_limit_mechanism",
            "rss_watchdog_poll_seconds",
            "retained_storage_scope",
        },
        "config.compute_ceiling",
    )
    if (
        any(
            not isinstance(compute[key], (int, float))
            or isinstance(compute[key], bool)
            or float(compute[key]) <= 0
            for key in (
                "target_gpu_hours",
                "scoring_cpu_hours",
                "scoring_ram_gb",
                "analysis_cpu_hours",
                "analysis_ram_gb",
                "retained_storage_gb",
                "blas_threads",
                "rss_watchdog_poll_seconds",
            )
        )
        or compute["target_timeout_rule"]
        != "target_gpu_hours * 3600 wall-clock seconds"
        or compute["cpu_limit_mechanism"] != "POSIX RLIMIT_CPU"
        or compute["memory_limit_mechanism"]
        != "Linux /proc/self/status RSS watchdog plus POSIX RLIMIT_AS"
        or compute["retained_storage_scope"]
        != "recursive regular-file bytes below paths.output_dir"
    ):
        raise ProtocolError("config resource ceilings or mechanisms changed")
    if substrate.get("n_items") != 1000 or len(substrate.get("valid_uids", [])) != 9:
        raise ProtocolError("config must freeze 1,000 items and nine participants")
    if estimator.get("pca_rank") != 50:
        raise ProtocolError("config estimator.pca_rank must be 50")
    if estimator.get("primary_layer") != 6 or estimator.get("sensitivity_layer") != 7:
        raise ProtocolError("config layers must be primary 6 and sensitivity 7")
    if estimator.get("seeds") != [0, 1, 2, 3, 4, 5]:
        raise ProtocolError("config must freeze seeds 0 through 5")
    if target.get("target_dim") != 20484:
        raise ProtocolError("config target_dim must be 20,484")
    if folds.get("method") != "contiguous" or folds.get("count") != 5:
        raise ProtocolError("config must freeze five contiguous folds")
    blocks = folds.get("test_blocks")
    if blocks != [[0, 200], [200, 400], [400, 600], [600, 800], [800, 1000]]:
        raise ProtocolError("config contiguous test blocks changed")
    if inference.get("alpha") != 0.05 or inference.get("significance_test") != "two-sided":
        raise ProtocolError("config inference must freeze two-sided alpha 0.05")
    if inference.get("sign_flip_enumeration") != 2 ** len(estimator["seeds"]):
        raise ProtocolError("config sign-flip enumeration does not equal 2^n_seeds")
    if (
        inference.get("c3_seed_stability_metrics") != ["D", "J"]
        or inference.get("terminal_endpoint_order")
        != ["A", "Q", "M", "B", "O", "D", "J"]
        or inference.get("terminal_family_sizes")
        != {"C1": 2, "C2": 2, "C3": 3}
    ):
        raise ProtocolError("config inference multiplicity or endpoint order changed")
    expect_exact_keys(
        bridge,
        {
            "target_pca_rank",
            "student_pca_rank",
            "target_pca_basis",
            "student_pca_basis",
            "static_pca_basis",
            "alignments",
            "absolute_arm",
            "comparator_arm",
            "metrics",
            "response_model",
            "target_model",
            "composition",
            "score",
            "claim_boundary",
        },
        "config.bridge",
    )
    if (
        bridge["target_pca_rank"] != estimator["pca_rank"]
        or bridge["student_pca_rank"] != estimator["pca_rank"]
        or bridge["alignments"] != ["aligned", "twin"]
        or bridge["absolute_arm"] != "tribe_mse"
        or bridge["comparator_arm"] != "kd_only"
        or bridge["metrics"] != ["O", "D", "J"]
    ):
        raise ProtocolError("config bridge design differs from the frozen C3 contract")


def validate_design(design: Mapping[str, Any], config: Mapping[str, Any]) -> None:
    expected_keys = {
        "uids",
        "train_uids",
        "heldout_uids",
        "rois",
        "test_blocks",
        "nuisance_variants",
        "primary_nuisance",
        "layers",
        "primary_layer",
        "sensitivity_layer",
        "arms",
        "seeds",
        "pca_rank",
        "ridge_alphas",
        "coordinate_sst_floor",
        "target_dim",
        "bridge",
    }
    expect_exact_keys(design, expected_keys, "design")
    substrate = config["substrate"]
    estimator = config["estimator"]
    expected = {
        "uids": substrate["valid_uids"],
        "train_uids": substrate["train_uids"],
        "heldout_uids": substrate["heldout_uids"],
        "rois": substrate["rois"],
        "test_blocks": config["folds"]["test_blocks"],
        "nuisance_variants": list(estimator["nuisance_variants"]),
        "primary_nuisance": estimator["primary_nuisance"],
        "layers": [estimator["primary_layer"], estimator["sensitivity_layer"]],
        "primary_layer": estimator["primary_layer"],
        "sensitivity_layer": estimator["sensitivity_layer"],
        "arms": estimator["arms"],
        "seeds": estimator["seeds"],
        "pca_rank": estimator["pca_rank"],
        "ridge_alphas": estimator["ridge_alphas"],
        "coordinate_sst_floor": estimator["coordinate_sst_floor"],
        "target_dim": config["target"]["target_dim"],
        "bridge": config["bridge"],
    }
    for key, expected_value in expected.items():
        if design.get(key) != expected_value:
            raise ProtocolError(f"design.{key} does not match canonical config")


def validate_path_hash_record(
    record: Any,
    context: str,
    expected_path: str,
    expected_sha256: str | None,
    verify_files: bool,
) -> dict[str, Any]:
    value = require_mapping(record, context)
    expect_exact_keys(value, {"path", "sha256"}, context)
    path_text = require_str(value["path"], f"{context}.path")
    observed_path = resolve_repo_path(path_text, f"{context}.path")
    canonical_path = resolve_repo_path(expected_path, f"{context}.expected_path")
    if observed_path != canonical_path:
        raise ProtocolError(f"{context}.path changed: {path_text} != {expected_path}")
    digest = require_sha256(value["sha256"], f"{context}.sha256")
    if expected_sha256 is not None and digest != expected_sha256:
        raise ProtocolError(f"{context}.sha256 does not match canonical config")
    if verify_files:
        if not observed_path.is_file():
            raise ProtocolError(f"{context}.path is not a file: {observed_path}")
        observed = sha256_file(observed_path)
        if observed != digest:
            raise ProtocolError(f"{context} file hash mismatch")
    return value


def validate_identity(
    identity: Mapping[str, Any],
    config: Mapping[str, Any],
    config_path: Path,
    verify_files: bool,
) -> None:
    expected_keys = {
        "protocol_version",
        "config",
        "readiness",
        "bundle",
        "design_manifest",
        "acquisition_manifest",
        "runner",
        "analyzer",
        "tuckute_csv",
        "e025_manifest",
        "e025_extraction",
        "e025_analysis",
        "e025_nuisance",
        "e025_participant_loader",
        "target",
        "standardization",
        "twin_permutation",
        "ordered_item_sha256",
        "ordered_text_sha256",
        "vertex_index_sha256",
        "tribe_runtime",
        "scoring_runtime",
    }
    expect_exact_keys(identity, expected_keys, "identity")
    if identity["protocol_version"] != config["protocol_version"]:
        raise ProtocolError("identity.protocol_version mismatch")

    config_rel = repo_relative(config_path)
    validate_path_hash_record(
        identity["config"], "identity.config", config_rel, sha256_file(config_path), verify_files
    )
    validate_path_hash_record(
        identity["readiness"],
        "identity.readiness",
        config["paths"]["readiness"],
        None,
        verify_files,
    )
    bundle = require_mapping(identity["bundle"], "identity.bundle")
    expect_exact_keys(bundle, {"path", "sha256", "bundle_sha256"}, "identity.bundle")
    require_sha256(bundle["bundle_sha256"], "identity.bundle.bundle_sha256")
    validate_path_hash_record(
        {"path": bundle["path"], "sha256": bundle["sha256"]},
        "identity.bundle",
        config["paths"]["bundle_manifest"],
        None,
        verify_files,
    )
    validate_path_hash_record(
        identity["design_manifest"],
        "identity.design_manifest",
        config["paths"]["design_manifest"],
        None,
        verify_files,
    )
    validate_path_hash_record(
        identity["acquisition_manifest"],
        "identity.acquisition_manifest",
        config["paths"]["acquisition_manifest"],
        None,
        verify_files,
    )
    validate_path_hash_record(identity["runner"], "identity.runner", RUNNER_PATH, None, verify_files)
    validate_path_hash_record(identity["analyzer"], "identity.analyzer", ANALYZER_PATH, None, verify_files)
    if identity["analyzer"]["sha256"] != sha256_file(Path(__file__).resolve()):
        raise ProtocolError("identity.analyzer.sha256 does not match the executing analyzer")

    for key in (
        "tuckute_csv",
        "e025_manifest",
        "e025_extraction",
        "e025_analysis",
        "e025_nuisance",
        "e025_participant_loader",
    ):
        source = config["sources"][key]
        validate_path_hash_record(identity[key], f"identity.{key}", source["path"], source["sha256"], verify_files)

    target = require_mapping(identity["target"], "identity.target")
    expect_exact_keys(target, {"path", "sha256", "targets_array_sha256"}, "identity.target")
    require_sha256(target["targets_array_sha256"], "identity.target.targets_array_sha256")
    validate_path_hash_record(
        {"path": target["path"], "sha256": target["sha256"]},
        "identity.target",
        config["paths"]["target"],
        None,
        verify_files,
    )

    standardization = require_mapping(identity["standardization"], "identity.standardization")
    expect_exact_keys(
        standardization,
        {"npz_path", "npz_sha256", "manifest_path", "manifest_sha256"},
        "identity.standardization",
    )
    validate_path_hash_record(
        {"path": standardization["npz_path"], "sha256": standardization["npz_sha256"]},
        "identity.standardization.npz",
        config["paths"]["standardization"],
        None,
        verify_files,
    )
    validate_path_hash_record(
        {"path": standardization["manifest_path"], "sha256": standardization["manifest_sha256"]},
        "identity.standardization.manifest",
        config["paths"]["standardization_manifest"],
        None,
        verify_files,
    )

    twin = require_mapping(identity["twin_permutation"], "identity.twin_permutation")
    expect_exact_keys(twin, {"path", "sha256", "array_sha256"}, "identity.twin_permutation")
    require_sha256(twin["array_sha256"], "identity.twin_permutation.array_sha256")
    validate_path_hash_record(
        {"path": twin["path"], "sha256": twin["sha256"]},
        "identity.twin_permutation",
        config["paths"]["twin_permutation"],
        None,
        verify_files,
    )

    if require_sha256(identity["ordered_item_sha256"], "identity.ordered_item_sha256") != config["substrate"]["ordered_item_sha256"]:
        raise ProtocolError("identity ordered-item hash mismatch")
    if require_sha256(identity["ordered_text_sha256"], "identity.ordered_text_sha256") != config["substrate"]["ordered_text_sha256"]:
        raise ProtocolError("identity ordered-text hash mismatch")
    expected_vertex = config["sources"]["e016_heldout_target"]["vertex_index_sha256"]
    if require_sha256(identity["vertex_index_sha256"], "identity.vertex_index_sha256") != expected_vertex:
        raise ProtocolError("identity vertex-index hash mismatch")
    validate_scoring_runtime_identity(
        require_mapping(identity["scoring_runtime"], "identity.scoring_runtime"),
        config,
        verify_files,
    )
    validate_tribe_runtime_identity(
        identity["tribe_runtime"], config, verify_live=verify_files
    )
    if verify_files:
        validate_sealed_identity_chain(identity, config, config_path)


def validate_scoring_runtime_identity(
    runtime: Mapping[str, Any], config: Mapping[str, Any], verify_files: bool
) -> None:
    expect_exact_keys(
        runtime,
        {"launcher", "versions", "pyproject", "uv_lock", "blas_threads"},
        "identity.scoring_runtime",
    )
    frozen = config["scoring_runtime"]
    if runtime["launcher"] != frozen["launcher"]:
        raise ProtocolError("scoring runtime launcher mismatch")
    versions = require_mapping(runtime["versions"], "identity.scoring_runtime.versions")
    expect_exact_keys(
        versions,
        {"python", "numpy", "scipy", "scikit_learn"},
        "identity.scoring_runtime.versions",
    )
    expected_versions = {
        "python": frozen["python_version"],
        "numpy": frozen["numpy_version"],
        "scipy": frozen["scipy_version"],
        "scikit_learn": frozen["scikit_learn_version"],
    }
    current_versions = {
        "python": ".".join(map(str, sys.version_info[:3])),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
    }
    if versions != expected_versions or current_versions != expected_versions:
        raise ProtocolError(
            f"scoring runtime version mismatch: raw={versions}, current={current_versions}, expected={expected_versions}"
        )
    validate_path_hash_record(
        runtime["pyproject"],
        "identity.scoring_runtime.pyproject",
        frozen["pyproject"]["path"],
        frozen["pyproject"]["sha256"],
        verify_files,
    )
    validate_path_hash_record(
        runtime["uv_lock"],
        "identity.scoring_runtime.uv_lock",
        frozen["uv_lock"]["path"],
        frozen["uv_lock"]["sha256"],
        verify_files,
    )
    if require_int(runtime["blas_threads"], "identity.scoring_runtime.blas_threads") != int(
        config["compute_ceiling"]["blas_threads"]
    ):
        raise ProtocolError("scoring runtime BLAS-thread count mismatch")


def frozen_tribe_runtime_identity(
    config: Mapping[str, Any], *, verify_live: bool
) -> dict[str, Any]:
    frozen = config["runtime"]
    checkout_value = Path(frozen["tribe_checkout"])
    checkout = (
        checkout_value
        if checkout_value.is_absolute()
        else ROOT / checkout_value
    ).absolute()
    python_value = Path(frozen["python"])
    python = (
        python_value if python_value.is_absolute() else ROOT / python_value
    ).absolute()
    for path, context in (
        (checkout, "config.runtime.tribe_checkout"),
        (python, "config.runtime.python"),
    ):
        try:
            path.relative_to(ROOT)
        except ValueError as exc:
            raise ProtocolError(f"{context} escapes repository: {path}") from exc
    if verify_live:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=checkout, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ).stdout.strip()
        diff = subprocess.run(
            ["git", "diff", "--binary", "--", "tribev2/grids/defaults.py"],
            cwd=checkout, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout
        status = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=checkout, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout
        version = subprocess.run(
            [str(python), "--version"], check=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True,
        ).stdout.strip()
        freeze = subprocess.run(
            [str(python), *frozen["sorted_pip_freeze_command"]], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ).stdout
        freeze_lines = sorted(
            line.strip() for line in freeze.splitlines() if line.strip()
        )
        freeze_bytes = ("\n".join(freeze_lines) + "\n").encode("utf-8")
        if (
            head != frozen["tribe_git_head"]
            or sha256_bytes(diff) != frozen["tribe_tracked_diff_sha256"]
            or sha256_bytes(status) != frozen["tribe_status_sha256"]
            or version != f"Python {frozen['python_version']}"
            or len(freeze_lines) != int(frozen["sorted_pip_freeze_line_count"])
            or sha256_bytes(freeze_bytes) != frozen["sorted_pip_freeze_sha256"]
        ):
            raise ProtocolError("live TRIBE code or environment provenance changed")
    else:
        head = frozen["tribe_git_head"]
        diff = b""
        status = b""
        version = f"Python {frozen['python_version']}"
        freeze_lines = [""] * int(frozen["sorted_pip_freeze_line_count"])

    def frozen_file_record(
        record: Mapping[str, Any], context: str
    ) -> dict[str, Any]:
        path = Path(record["path"]).absolute()
        if not path.is_file():
            raise ProtocolError(f"{context} is missing: {path}")
        digest = sha256_file(path) if verify_live else record["sha256"]
        if digest != record["sha256"]:
            raise ProtocolError(f"{context} hash differs from frozen config")
        return {
            "path": str(path),
            "size_bytes": int(path.stat().st_size),
            "sha256": digest,
        }

    identity = {
        "tribe_checkout": str(checkout),
        "git_head": head,
        "tracked_diff_sha256": (
            sha256_bytes(diff) if verify_live else frozen["tribe_tracked_diff_sha256"]
        ),
        "status_sha256": (
            sha256_bytes(status) if verify_live else frozen["tribe_status_sha256"]
        ),
        "python": str(python),
        "python_version": version,
        "sorted_pip_freeze_sha256": frozen["sorted_pip_freeze_sha256"],
        "sorted_pip_freeze_line_count": len(freeze_lines),
        "hf_home": frozen["hf_home"],
        "tribe_snapshot": frozen["tribe_snapshot"],
        "tribe_checkpoint": frozen_file_record(
            frozen["tribe_checkpoint"], "TRIBE checkpoint"
        ),
        "llama_snapshot": frozen["llama_snapshot"],
        "llama_shards": [
            frozen_file_record(record, f"Llama shard {index}")
            for index, record in enumerate(frozen["llama_shards"])
        ],
    }
    return {
        "schema_version": "e030-tribe-runtime.v1",
        "identity": identity,
        "semantic_sha256": sha256_bytes(canonical_json_bytes(identity)),
    }


def validate_tribe_runtime_identity(
    runtime: Any, config: Mapping[str, Any], *, verify_live: bool
) -> dict[str, Any]:
    value = require_mapping(runtime, "identity.tribe_runtime")
    expect_exact_keys(
        value, {"schema_version", "identity", "semantic_sha256"},
        "identity.tribe_runtime",
    )
    if value["schema_version"] != "e030-tribe-runtime.v1":
        raise ProtocolError("TRIBE runtime schema mismatch")
    identity = require_mapping(value["identity"], "identity.tribe_runtime.identity")
    expect_exact_keys(
        identity,
        {
            "tribe_checkout", "git_head", "tracked_diff_sha256", "status_sha256",
            "python", "python_version", "sorted_pip_freeze_sha256",
            "sorted_pip_freeze_line_count", "hf_home", "tribe_snapshot",
            "tribe_checkpoint", "llama_snapshot", "llama_shards",
        },
        "identity.tribe_runtime.identity",
    )
    declared = require_sha256(
        value["semantic_sha256"], "identity.tribe_runtime.semantic_sha256"
    )
    if declared != sha256_bytes(canonical_json_bytes(identity)):
        raise ProtocolError("TRIBE runtime semantic digest mismatch")
    expected = frozen_tribe_runtime_identity(config, verify_live=verify_live)
    if value != expected:
        raise ProtocolError("TRIBE runtime identity differs from frozen provenance")
    return value


def validate_file_record_against(
    record: Any, expected_path: str, expected_sha256: str, context: str
) -> None:
    value = require_mapping(record, context)
    if set(value) not in ({"path", "sha256"}, {"path", "sha256", "size_bytes"}):
        raise ProtocolError(f"{context} has unexpected file-record keys")
    path = resolve_repo_path(require_str(value["path"], f"{context}.path"), f"{context}.path")
    expected = resolve_repo_path(expected_path, f"{context}.expected_path")
    if path != expected or require_sha256(value["sha256"], f"{context}.sha256") != expected_sha256:
        raise ProtocolError(f"{context} path/hash mismatch")
    if "size_bytes" in value and require_int(value["size_bytes"], f"{context}.size_bytes") != path.stat().st_size:
        raise ProtocolError(f"{context} size mismatch")


def validate_bundle_payload(
    bundle: Mapping[str, Any], identity: Mapping[str, Any], config_path: Path
) -> None:
    expect_exact_keys(bundle, {"schema_version", "files", "bundle_sha256"}, "bundle manifest")
    if bundle["schema_version"] != "e030-bundle.v1":
        raise ProtocolError("unexpected bundle-manifest schema")
    files = require_mapping(bundle["files"], "bundle manifest.files")
    expect_exact_keys(files, {"config", "e_record", "runner", "analyzer"}, "bundle manifest.files")
    expected_paths = {
        "config": repo_relative(config_path),
        "e_record": E_RECORD_PATH,
        "runner": RUNNER_PATH,
        "analyzer": ANALYZER_PATH,
    }
    file_hashes: dict[str, str] = {}
    for name, expected_path in expected_paths.items():
        record = require_mapping(files[name], f"bundle manifest.files.{name}")
        expect_exact_keys(record, {"path", "sha256", "size_bytes"}, f"bundle manifest.files.{name}")
        actual_path = resolve_repo_path(record["path"], f"bundle manifest.files.{name}.path")
        if actual_path != resolve_repo_path(expected_path, f"bundle expected {name}"):
            raise ProtocolError(f"bundle {name} path mismatch")
        digest = require_sha256(record["sha256"], f"bundle manifest.files.{name}.sha256")
        if sha256_file(actual_path) != digest or actual_path.stat().st_size != require_int(
            record["size_bytes"], f"bundle manifest.files.{name}.size_bytes"
        ):
            raise ProtocolError(f"bundle {name} file identity is stale")
        file_hashes[name] = digest
    computed = sha256_bytes(canonical_json_bytes(file_hashes))
    declared = require_sha256(bundle["bundle_sha256"], "bundle manifest.bundle_sha256")
    if declared != computed or declared != identity["bundle"]["bundle_sha256"]:
        raise ProtocolError("bundle semantic digest mismatch")
    for name, identity_key in (("config", "config"), ("runner", "runner"), ("analyzer", "analyzer")):
        if identity[identity_key]["sha256"] != file_hashes[name]:
            raise ProtocolError(f"raw {identity_key} hash differs from approved bundle")


def validate_seal_payloads(
    identity: Mapping[str, Any],
    config: Mapping[str, Any],
    bundle: Mapping[str, Any],
    readiness: Mapping[str, Any],
    design: Mapping[str, Any],
    acquisition: Mapping[str, Any],
    oracle: Mapping[str, Any],
) -> None:
    bundle_sha = require_sha256(bundle.get("bundle_sha256"), "bundle.bundle_sha256")
    expect_exact_keys(
        readiness,
        {
            "schema_version",
            "verdict",
            "ready",
            "bundle",
            "bundle_manifest",
            "design_manifest",
            "selftest_report",
            "benchmark_report",
            "smoke_report",
            "standardization_manifest",
            "standardization_artifact",
            "oracle_report",
            "all_pre_result_gates_pass",
        },
        "readiness",
    )
    if (
        readiness.get("schema_version") != "e030-readiness.v2"
        or readiness.get("ready") is not True
        or readiness.get("verdict") != "DESIGN PASS / READY-TO-RUN: YES"
        or readiness.get("all_pre_result_gates_pass") is not True
        or readiness.get("bundle") != bundle
        or readiness.get("design_manifest", {}).get("sha256")
        != identity["design_manifest"]["sha256"]
    ):
        raise ProtocolError("readiness seal is stale or incomplete")
    if design.get("schema_version") != "e030-design-manifest.v1":
        raise ProtocolError("design manifest schema mismatch")
    if design.get("config", {}).get("sha256") != identity["config"]["sha256"]:
        raise ProtocolError("design manifest does not bind the raw config")
    substrate = design.get("substrate", {})
    if (
        substrate.get("ordered_item_sha256") != identity["ordered_item_sha256"]
        or substrate.get("ordered_text_sha256") != identity["ordered_text_sha256"]
    ):
        raise ProtocolError("design manifest substrate identity mismatch")
    design_tuckute = design.get("sources", {}).get("tuckute_csv", {})
    if design_tuckute.get("sha256") != identity["tuckute_csv"]["sha256"]:
        raise ProtocolError("design manifest Tuckute source mismatch")
    design_twin = design.get("twin", {})
    if (
        design_twin.get("zero_fixed_points") is not True
        or design_twin.get("semantic_sha256") != identity["twin_permutation"]["array_sha256"]
        or design_twin.get("artifact", {}).get("sha256") != identity["twin_permutation"]["sha256"]
    ):
        raise ProtocolError("design manifest twin identity mismatch")
    if (
        oracle.get("schema_version") != "e030-oracle-review.v1"
        or oracle.get("approved") is not True
        or oracle.get("bundle_sha256") != bundle_sha
    ):
        raise ProtocolError("oracle review does not approve the current bundle")
    expect_exact_keys(
        acquisition,
        {
            "schema_version",
            "science_status",
            "bundle_sha256",
            "config_sha256",
            "readiness_sha256",
            "design_manifest_sha256",
            "target_manifest",
            "target",
            "semantic_sha256",
            "runtime",
            "resource_use",
        },
        "acquisition",
    )
    if (
        acquisition.get("schema_version") != "e030-acquisition-manifest.v2"
        or acquisition.get("bundle_sha256") != bundle_sha
        or acquisition.get("config_sha256") != identity["config"]["sha256"]
        or acquisition.get("readiness_sha256") != identity["readiness"]["sha256"]
        or acquisition.get("design_manifest_sha256") != identity["design_manifest"]["sha256"]
        or acquisition.get("target", {}).get("sha256") != identity["target"]["sha256"]
        or acquisition.get("semantic_sha256", {}).get("targets")
        != identity["target"]["targets_array_sha256"]
        or acquisition.get("semantic_sha256", {}).get("vertex_index")
        != identity["vertex_index_sha256"]
    ):
        raise ProtocolError("acquisition seal does not bind the approved design and target")
    if acquisition.get("runtime") != identity["tribe_runtime"]:
        raise ProtocolError("acquisition runtime differs from raw runtime identity")
    target_resources = require_mapping(
        acquisition.get("resource_use"), "acquisition.resource_use"
    )
    expect_exact_keys(
        target_resources,
        {
            "timeout_seconds",
            "elapsed_wall_seconds",
            "elapsed_cpu_seconds",
            "parent_peak_rss_kib",
            "retained_output_dir_bytes_before",
            "retained_output_dir_bytes_projected_after_seal",
            "retained_storage_limit_bytes",
        },
        "acquisition.resource_use",
    )
    if (
        require_float(
            target_resources["timeout_seconds"],
            "acquisition.resource_use.timeout_seconds",
        )
        != float(config["compute_ceiling"]["target_gpu_hours"]) * 3600.0
        or require_int(
            target_resources["retained_storage_limit_bytes"],
            "acquisition.resource_use.retained_storage_limit_bytes",
        )
        != retained_storage_limit_bytes(config)
        or require_int(
            target_resources["retained_output_dir_bytes_projected_after_seal"],
            "acquisition.resource_use.retained_output_dir_bytes_projected_after_seal",
        )
        > retained_storage_limit_bytes(config)
    ):
        raise ProtocolError("acquisition resource policy differs from config")
    if (
        require_int(
            target_resources["retained_output_dir_bytes_projected_after_seal"],
            "acquisition.resource_use.retained_output_dir_bytes_projected_after_seal",
        )
        < require_int(
            target_resources["retained_output_dir_bytes_before"],
            "acquisition.resource_use.retained_output_dir_bytes_before",
        )
    ):
        raise ProtocolError("acquisition projected storage precedes its baseline")


def validate_target_and_twin_semantics(
    identity: Mapping[str, Any], config: Mapping[str, Any], acquisition: Mapping[str, Any]
) -> None:
    twin_path = resolve_repo_path(identity["twin_permutation"]["path"], "identity.twin_permutation.path")
    twin = np.load(twin_path, allow_pickle=False)
    n_items = int(config["substrate"]["n_items"])
    if twin.shape != (n_items,) or not np.issubdtype(twin.dtype, np.integer):
        raise ProtocolError("twin permutation shape/dtype mismatch")
    twin_i64 = twin.astype("<i8", copy=False)
    if sha256_array(twin_i64) != identity["twin_permutation"]["array_sha256"]:
        raise ProtocolError("twin permutation semantic hash mismatch")
    if not np.array_equal(np.sort(twin_i64), np.arange(n_items, dtype=np.int64)):
        raise ProtocolError("twin permutation is not bijective")
    if np.any(twin_i64 == np.arange(n_items, dtype=np.int64)):
        raise ProtocolError("twin permutation has fixed points")
    for start, stop in config["folds"]["test_blocks"]:
        block = twin_i64[start:stop]
        if np.any(block < start) or np.any(block >= stop):
            raise ProtocolError("twin permutation leaves a frozen fold block")

    target_path = resolve_repo_path(identity["target"]["path"], "identity.target.path")
    with np.load(target_path, allow_pickle=False) as cache:
        required = {"targets", "texts", "item_indices", "vertex_index", "segment_counts", "metadata_json"}
        if set(cache.files) != required:
            raise ProtocolError("target cache member set mismatch")
        targets = cache["targets"]
        texts = [str(value) for value in cache["texts"].tolist()]
        item_indices = cache["item_indices"]
        vertex_index = cache["vertex_index"]
        counts = cache["segment_counts"]
        metadata = json.loads(str(cache["metadata_json"].item()))
        metadata = require_mapping(metadata, "target metadata")
        expect_exact_keys(
            metadata,
            {
                "schema_version",
                "experiment",
                "science_status",
                "config_sha256",
                "design_manifest_sha256",
                "readiness_sha256",
                "bundle_sha256",
                "runtime_semantic_sha256",
                "generator",
                "generator_settings_sha256",
                "corpus",
                "condition",
                "n_items",
                "batch_items",
                "features",
                "text_model",
                "event_mode",
                "target_dim",
                "tr",
                "word_duration",
                "word_gap",
                "min_duration",
                "config_update",
                "ordered_item_sha256",
                "ordered_text_sha256",
                "item_mapping",
                "elapsed_seconds",
                "worker_resource_use",
            },
            "target metadata",
        )
        if metadata["schema_version"] != "e030-target-cache.v2":
            raise ProtocolError("target metadata schema mismatch")
        if targets.shape != (n_items, int(config["target"]["target_dim"])) or targets.dtype != np.float32:
            raise ProtocolError("target cache shape/dtype mismatch")
        if (
            not np.isfinite(targets).all()
            or counts.shape != (n_items,)
            or np.any(counts <= 0)
            or item_indices.shape != (n_items,)
            or not np.issubdtype(item_indices.dtype, np.integer)
            or not np.issubdtype(vertex_index.dtype, np.integer)
        ):
            raise ProtocolError("target cache contains invalid values or segment counts")
        if sha256_array(targets) != identity["target"]["targets_array_sha256"]:
            raise ProtocolError("target array semantic hash mismatch")
        if sha256_array(vertex_index.astype("<i8", copy=False)) != identity["vertex_index_sha256"]:
            raise ProtocolError("target vertex semantic hash mismatch")
        if not np.array_equal(item_indices, np.arange(n_items, dtype=item_indices.dtype)):
            raise ProtocolError("target item indices are reordered")
        text_hash = sha256_bytes(("\n".join(texts) + "\n").encode("utf-8"))
        if text_hash != identity["ordered_text_sha256"]:
            raise ProtocolError("target ordered-text hash mismatch")
        if metadata.get("ordered_item_sha256") != identity["ordered_item_sha256"]:
            raise ProtocolError("target ordered-item hash mismatch")
        target_settings = {
            "features": config["target"]["features"],
            "text_model": config["target"]["text_model"],
            "event_mode": config["target"]["event_mode"],
            "target_dim": int(config["target"]["target_dim"]),
            "tr": float(config["target"]["tr"]),
            "word_duration": float(config["target"]["word_duration"]),
            "word_gap": float(config["target"]["word_gap"]),
            "min_duration": float(config["target"]["min_duration"]),
            "batch_items": int(config["target"]["batch_items"]),
        }
        expected_metadata = {
            "experiment": "E030 exact-substrate TRIBE target acquisition",
            "science_status": "target-cache artifact only; no participant response was opened",
            "config_sha256": identity["config"]["sha256"],
            "design_manifest_sha256": identity["design_manifest"]["sha256"],
            "readiness_sha256": identity["readiness"]["sha256"],
            "bundle_sha256": identity["bundle"]["bundle_sha256"],
            "runtime_semantic_sha256": identity["tribe_runtime"][
                "semantic_sha256"
            ],
            "generator_settings_sha256": sha256_bytes(
                canonical_json_bytes(target_settings)
            ),
            "condition": config["substrate"]["condition"],
            "n_items": n_items,
            **target_settings,
            "ordered_item_sha256": identity["ordered_item_sha256"],
            "ordered_text_sha256": identity["ordered_text_sha256"],
            "item_mapping": "item_id = item_index + 1",
        }
        for key, expected in expected_metadata.items():
            if metadata[key] != expected:
                raise ProtocolError(f"target metadata/config mismatch: {key}")
        validate_file_record_against(
            metadata["generator"],
            config["sources"]["target_generator"]["path"],
            config["sources"]["target_generator"]["sha256"],
            "target metadata.generator",
        )
        validate_file_record_against(
            metadata["corpus"],
            config["paths"]["corpus"],
            identity["ordered_text_sha256"],
            "target metadata.corpus",
        )
        smoke = strict_json_load(
            resolve_repo_path(config["paths"]["smoke_report"], "smoke report")
        )
        if metadata["config_update"] != smoke.get("stable_metadata", {}).get(
            "config_update"
        ):
            raise ProtocolError("target config_update differs from frozen smoke")
        worker_resource = require_mapping(
            metadata["worker_resource_use"], "target metadata.worker_resource_use"
        )
        expect_exact_keys(
            worker_resource,
            {
                "elapsed_wall_seconds",
                "elapsed_cpu_seconds",
                "peak_rss_kib",
                "retained_output_dir_bytes_before_write",
                "retained_storage_limit_bytes",
                "target_timeout_seconds",
            },
            "target metadata.worker_resource_use",
        )
        if (
            require_int(
                worker_resource["retained_storage_limit_bytes"],
                "target worker retained-storage limit",
            )
            != retained_storage_limit_bytes(config)
            or any(
                require_float(worker_resource[key], f"target worker {key}") < 0
                for key in (
                    "elapsed_wall_seconds",
                    "elapsed_cpu_seconds",
                    "target_timeout_seconds",
                )
            )
            or require_float(
                worker_resource["target_timeout_seconds"],
                "target worker target_timeout_seconds",
            )
            != float(config["compute_ceiling"]["target_gpu_hours"]) * 3600.0
        ):
            raise ProtocolError("target worker resource policy mismatch")
    semantic = acquisition.get("semantic_sha256", {})
    expected_semantic = {
        "targets": sha256_array(targets),
        "texts": identity["ordered_text_sha256"],
        "item_indices": sha256_array(item_indices.astype("<i8", copy=False)),
        "vertex_index": sha256_array(vertex_index.astype("<i8", copy=False)),
        "segment_counts": sha256_array(counts),
    }
    if semantic != expected_semantic:
        raise ProtocolError("acquisition target semantic identity mismatch")
    target_manifest_path = resolve_repo_path(
        acquisition["target_manifest"]["path"], "acquisition.target_manifest.path"
    )
    target_manifest = strict_json_load(target_manifest_path)
    if target_manifest.get("metadata") != metadata:
        raise ProtocolError("target-manifest metadata differs from target cache")


def validate_standardization_semantics(
    identity: Mapping[str, Any], config: Mapping[str, Any]
) -> None:
    manifest_path = resolve_repo_path(
        identity["standardization"]["manifest_path"], "identity.standardization.manifest_path"
    )
    manifest = strict_json_load(manifest_path)
    if (
        manifest.get("schema_version") != "e030-standardization.v1"
        or manifest.get("design_manifest_sha256") != identity["design_manifest"]["sha256"]
        or manifest.get("runner_sha256") != identity["runner"]["sha256"]
        or manifest.get("source", {}).get("sha256")
        != config["sources"]["e016_train_target"]["sha256"]
        or manifest.get("artifact", {}).get("sha256")
        != identity["standardization"]["npz_sha256"]
    ):
        raise ProtocolError("standardization manifest identity mismatch")
    npz_path = resolve_repo_path(
        identity["standardization"]["npz_path"], "identity.standardization.npz_path"
    )
    with np.load(npz_path, allow_pickle=False) as cache:
        if set(cache.files) != {"mean", "std", "metadata_json"}:
            raise ProtocolError("standardization NPZ member set mismatch")
        mean = cache["mean"]
        std = cache["std"]
        if not np.isfinite(mean).all() or not np.isfinite(std).all() or np.any(std <= 0):
            raise ProtocolError("standardization arrays are invalid")
        if sha256_array(mean) != manifest.get("mean_sha256") or sha256_array(std) != manifest.get("std_sha256"):
            raise ProtocolError("standardization semantic hash mismatch")


def validate_sealed_identity_chain(
    identity: Mapping[str, Any], config: Mapping[str, Any], config_path: Path
) -> None:
    bundle = strict_json_load(resolve_repo_path(identity["bundle"]["path"], "identity.bundle.path"))
    readiness = strict_json_load(resolve_repo_path(identity["readiness"]["path"], "identity.readiness.path"))
    design = strict_json_load(resolve_repo_path(identity["design_manifest"]["path"], "identity.design_manifest.path"))
    acquisition = strict_json_load(
        resolve_repo_path(identity["acquisition_manifest"]["path"], "identity.acquisition_manifest.path")
    )
    oracle_record = require_mapping(readiness.get("oracle_report"), "readiness.oracle_report")
    expect_exact_keys(
        oracle_record,
        {"path", "size_bytes", "sha256"},
        "readiness.oracle_report",
    )
    oracle_path = resolve_repo_path(oracle_record.get("path"), "readiness.oracle_report.path")
    if oracle_path != resolve_repo_path(config["paths"]["oracle_report"], "config.paths.oracle_report"):
        raise ProtocolError("readiness oracle-report path mismatch")
    oracle_hash = require_sha256(oracle_record.get("sha256"), "readiness.oracle_report.sha256")
    if not oracle_path.is_file() or sha256_file(oracle_path) != oracle_hash:
        raise ProtocolError("readiness oracle-report hash mismatch")
    oracle = strict_json_load(oracle_path)
    validate_bundle_payload(bundle, identity, config_path)
    validate_seal_payloads(identity, config, bundle, readiness, design, acquisition, oracle)

    report_specs = (
        "bundle_manifest",
        "design_manifest",
        "selftest_report",
        "benchmark_report",
        "smoke_report",
        "standardization_manifest",
        "standardization_artifact",
    )
    path_key_by_record = {
        "bundle_manifest": "bundle_manifest",
        "design_manifest": "design_manifest",
        "selftest_report": "selftest_report",
        "benchmark_report": "benchmark_report",
        "smoke_report": "smoke_report",
        "standardization_manifest": "standardization_manifest",
        "standardization_artifact": "standardization",
    }
    for readiness_key in report_specs:
        path_key = path_key_by_record[readiness_key]
        path = resolve_repo_path(config["paths"][path_key], f"config.paths.{path_key}")
        record = require_mapping(readiness.get(readiness_key), f"readiness.{readiness_key}")
        expect_exact_keys(
            record,
            {"path", "size_bytes", "sha256"},
            f"readiness.{readiness_key}",
        )
        if (
            resolve_repo_path(record["path"], f"readiness.{readiness_key}.path")
            != path
            or not path.is_file()
            or sha256_file(path) != record.get("sha256")
            or path.stat().st_size != require_int(
                record.get("size_bytes"), f"readiness.{readiness_key}.size_bytes"
            )
        ):
            raise ProtocolError(f"readiness prerequisite report is stale: {path_key}")
    selftest_report = strict_json_load(
        resolve_repo_path(config["paths"]["selftest_report"], "selftest report")
    )
    benchmark_report = strict_json_load(
        resolve_repo_path(config["paths"]["benchmark_report"], "benchmark report")
    )
    smoke_report = strict_json_load(
        resolve_repo_path(config["paths"]["smoke_report"], "smoke report")
    )
    for label, report, schema in (
        ("selftest", selftest_report, "e030-selftest.v2"),
        ("benchmark", benchmark_report, "e030-benchmark.v3"),
    ):
        if (
            report.get("schema_version") != schema
            or report.get("pass") is not True
            or report.get("config_sha256") != identity["config"]["sha256"]
            or report.get("design_manifest_sha256")
            != identity["design_manifest"]["sha256"]
            or report.get("runner_sha256") != identity["runner"]["sha256"]
            or report.get("analyzer_sha256") != identity["analyzer"]["sha256"]
        ):
            raise ProtocolError(f"readiness {label} report identity is stale")
    if (
        smoke_report.get("schema_version") != "e030-smoke-replay.v1"
        or smoke_report.get("pass") is not True
        or smoke_report.get("config_sha256") != identity["config"]["sha256"]
        or smoke_report.get("design_manifest_sha256")
        != identity["design_manifest"]["sha256"]
        or smoke_report.get("runner_sha256") != identity["runner"]["sha256"]
        or smoke_report.get("runtime") != identity["tribe_runtime"]
    ):
        raise ProtocolError("readiness smoke report identity is stale")
    target_manifest_record = require_mapping(
        acquisition.get("target_manifest"), "acquisition.target_manifest"
    )
    target_manifest_path = resolve_repo_path(
        target_manifest_record.get("path"), "acquisition.target_manifest.path"
    )
    if (
        target_manifest_path != resolve_repo_path(config["paths"]["target_manifest"], "config.paths.target_manifest")
        or not target_manifest_path.is_file()
        or sha256_file(target_manifest_path)
        != require_sha256(target_manifest_record.get("sha256"), "acquisition.target_manifest.sha256")
    ):
        raise ProtocolError("acquisition target-manifest identity mismatch")
    target_manifest = strict_json_load(target_manifest_path)
    expect_exact_keys(
        target_manifest,
        {
            "schema_version",
            "science_status",
            "config_sha256",
            "design_manifest_sha256",
            "readiness_sha256",
            "bundle_sha256",
            "runtime_semantic_sha256",
            "target",
            "shape",
            "dtype",
            "finite",
            "all_segment_counts_positive",
            "semantic_sha256",
            "metadata",
            "runtime",
            "elapsed_seconds",
            "gpu_selector",
            "log",
            "resource_use",
        },
        "target manifest",
    )
    if (
        target_manifest.get("schema_version") != "e030-target-manifest.v2"
        or target_manifest.get("config_sha256") != identity["config"]["sha256"]
        or target_manifest.get("design_manifest_sha256")
        != identity["design_manifest"]["sha256"]
        or target_manifest.get("readiness_sha256")
        != identity["readiness"]["sha256"]
        or target_manifest.get("bundle_sha256")
        != identity["bundle"]["bundle_sha256"]
        or target_manifest.get("target", {}).get("sha256") != identity["target"]["sha256"]
        or target_manifest.get("semantic_sha256") != acquisition.get("semantic_sha256")
        or target_manifest.get("runtime") != identity["tribe_runtime"]
        or target_manifest.get("runtime_semantic_sha256")
        != identity["tribe_runtime"]["semantic_sha256"]
        or target_manifest.get("resource_use") != acquisition.get("resource_use")
    ):
        raise ProtocolError("target manifest does not match acquisition seal")
    validate_target_and_twin_semantics(identity, config, acquisition)
    validate_standardization_semantics(identity, config)


def validate_validity(value: Any) -> dict[str, bool]:
    validity = require_mapping(value, "validity")
    expect_exact_keys(validity, VALIDITY_KEYS, "validity")
    parsed = {key: require_bool(flag, f"validity.{key}") for key, flag in validity.items()}
    conjunction = all(flag for key, flag in parsed.items() if key != "all_pass")
    if parsed["all_pass"] != conjunction:
        raise ProtocolError("validity.all_pass does not equal the component-check conjunction")
    return parsed


def validate_scoring_resource_use(
    value: Any, config: Mapping[str, Any]
) -> dict[str, Any]:
    resources = require_mapping(value, "resource_use")
    expected_keys = {
        "stage",
        "cpu_budget_seconds",
        "rlimit_cpu_soft_seconds",
        "address_space_limit_bytes",
        "peak_rss_limit_kib",
        "retained_storage_limit_bytes",
        "cpu_limit_mechanism",
        "memory_limit_mechanism",
        "rss_watchdog_poll_seconds",
        "retained_storage_scope",
        "elapsed_wall_seconds",
        "elapsed_cpu_seconds",
        "peak_rss_kib",
        "retained_output_dir_bytes_before_write",
        "retained_output_dir_bytes_projected_after_write",
    }
    expect_exact_keys(resources, expected_keys, "resource_use")
    ceiling = config["compute_ceiling"]
    cpu_budget = int(float(ceiling["scoring_cpu_hours"]) * 3600.0)
    rss_limit = int(float(ceiling["scoring_ram_gb"]) * 1024 * 1024)
    address_limit = int(float(ceiling["scoring_ram_gb"]) * 1024**3)
    storage_limit = retained_storage_limit_bytes(config)
    if (
        resources["stage"] != "scoring"
        or require_int(resources["cpu_budget_seconds"], "resource_use.cpu_budget_seconds")
        != cpu_budget
        or require_int(
            resources["rlimit_cpu_soft_seconds"],
            "resource_use.rlimit_cpu_soft_seconds",
        )
        < cpu_budget
        or require_int(
            resources["address_space_limit_bytes"],
            "resource_use.address_space_limit_bytes",
        )
        != address_limit
        or require_int(
            resources["peak_rss_limit_kib"], "resource_use.peak_rss_limit_kib"
        )
        != rss_limit
        or require_int(
            resources["retained_storage_limit_bytes"],
            "resource_use.retained_storage_limit_bytes",
        )
        != storage_limit
        or resources["cpu_limit_mechanism"] != ceiling["cpu_limit_mechanism"]
        or resources["memory_limit_mechanism"]
        != ceiling["memory_limit_mechanism"]
        or require_float(
            resources["rss_watchdog_poll_seconds"],
            "resource_use.rss_watchdog_poll_seconds",
        )
        != float(ceiling["rss_watchdog_poll_seconds"])
        or resources["retained_storage_scope"]
        != ceiling["retained_storage_scope"]
    ):
        raise ProtocolError("scoring resource policy differs from frozen config")
    wall = require_float(resources["elapsed_wall_seconds"], "resource_use.elapsed_wall_seconds")
    cpu = require_float(resources["elapsed_cpu_seconds"], "resource_use.elapsed_cpu_seconds")
    peak = require_int(resources["peak_rss_kib"], "resource_use.peak_rss_kib")
    before = require_int(
        resources["retained_output_dir_bytes_before_write"],
        "resource_use.retained_output_dir_bytes_before_write",
    )
    projected = require_int(
        resources["retained_output_dir_bytes_projected_after_write"],
        "resource_use.retained_output_dir_bytes_projected_after_write",
    )
    if (
        wall < 0
        or cpu < 0
        or cpu > cpu_budget
        or peak < 0
        or peak > rss_limit
        or before < 0
        or projected < before
        or projected > storage_limit
    ):
        raise ProtocolError("scoring resource use exceeds a frozen ceiling")
    return dict(resources)


def validate_inherited_gates(value: Any, config: Mapping[str, Any]) -> dict[str, Any]:
    gates = require_mapping(value, "inherited_gates")
    expect_exact_keys(
        gates,
        {"quality_equivalence", "target_direction", "representation_movement", "source_extraction_sha256"},
        "inherited_gates",
    )
    result: dict[str, Any] = {
        key: require_bool(gates[key], f"inherited_gates.{key}")
        for key in ("quality_equivalence", "target_direction", "representation_movement")
    }
    source_hash = require_sha256(gates["source_extraction_sha256"], "inherited_gates.source_extraction_sha256")
    if source_hash != config["sources"]["e025_extraction"]["sha256"]:
        raise ProtocolError("inherited gate extraction hash mismatch")
    result["source_extraction_sha256"] = source_hash
    result["all_pass"] = all(result[key] for key in ("quality_equivalence", "target_direction", "representation_movement"))
    return result


def parse_float_vector(value: Any, length: int, context: str) -> list[float]:
    items = require_list(value, context)
    if len(items) != length:
        raise ProtocolError(f"{context} must contain exactly {length} values")
    return [require_float(item, f"{context}[{index}]") for index, item in enumerate(items)]


def validate_alpha(value: Any, alphas: Sequence[float], context: str) -> float:
    alpha = require_float(value, context)
    if not any(close(alpha, float(candidate)) for candidate in alphas):
        raise ProtocolError(f"{context} is outside the frozen ridge grid")
    return alpha


C1_ROW_KEYS = {
    "uid",
    "participant_split",
    "nuisance_variant",
    "fold",
    "test_start",
    "test_stop_exclusive",
    "test_count",
    "representation",
    "target_pca_basis_sha256",
    "static_pca_basis_sha256",
    "alpha_nuisance",
    "alpha_full",
    "r2_nuisance_by_roi",
    "r2_full_by_roi",
    "unique_r2_by_roi",
    "r2_nuisance",
    "r2_full",
    "unique_r2",
}


def validate_c1_rows(rows_value: Any, config: Mapping[str, Any]) -> dict[tuple[int, str, int, str], dict[str, Any]]:
    rows = require_list(rows_value, "c1_rows")
    uids = config["substrate"]["valid_uids"]
    train = set(config["substrate"]["train_uids"])
    heldout = set(config["substrate"]["heldout_uids"])
    nuisances = list(config["estimator"]["nuisance_variants"])
    blocks = config["folds"]["test_blocks"]
    alphas = config["estimator"]["ridge_alphas"]
    roi_count = len(config["substrate"]["rois"])
    expected_count = len(uids) * len(nuisances) * len(blocks) * 2
    if len(rows) != expected_count:
        raise ProtocolError(f"c1_rows count {len(rows)} != frozen {expected_count}")

    index: dict[tuple[int, str, int, str], dict[str, Any]] = {}
    for row_index, raw in enumerate(rows):
        row = require_mapping(raw, f"c1_rows[{row_index}]")
        expect_exact_keys(row, C1_ROW_KEYS, f"c1_rows[{row_index}]")
        uid = require_int(row["uid"], f"c1_rows[{row_index}].uid")
        if uid not in uids:
            raise ProtocolError(f"unknown C1 uid: {uid}")
        split = require_str(row["participant_split"], f"c1_rows[{row_index}].participant_split")
        expected_split = "train" if uid in train else "heldout" if uid in heldout else None
        if split != expected_split:
            raise ProtocolError(f"C1 participant split mismatch for uid {uid}")
        nuisance = require_str(row["nuisance_variant"], f"c1_rows[{row_index}].nuisance_variant")
        if nuisance not in nuisances:
            raise ProtocolError(f"unknown C1 nuisance variant: {nuisance}")
        fold = require_int(row["fold"], f"c1_rows[{row_index}].fold")
        if fold not in range(len(blocks)):
            raise ProtocolError(f"unknown C1 fold: {fold}")
        start, stop = blocks[fold]
        if row["test_start"] != start or row["test_stop_exclusive"] != stop or row["test_count"] != stop - start:
            raise ProtocolError(f"C1 fold bounds mismatch at row {row_index}")
        representation = require_str(row["representation"], f"c1_rows[{row_index}].representation")
        if representation not in {"aligned", "twin"}:
            raise ProtocolError(f"unknown C1 representation: {representation}")
        require_sha256(
            row["target_pca_basis_sha256"],
            f"c1_rows[{row_index}].target_pca_basis_sha256",
        )
        require_sha256(
            row["static_pca_basis_sha256"],
            f"c1_rows[{row_index}].static_pca_basis_sha256",
        )
        alpha_nuisance = validate_alpha(row["alpha_nuisance"], alphas, f"c1_rows[{row_index}].alpha_nuisance")
        alpha_full = validate_alpha(row["alpha_full"], alphas, f"c1_rows[{row_index}].alpha_full")
        nuisance_roi = parse_float_vector(row["r2_nuisance_by_roi"], roi_count, f"c1_rows[{row_index}].r2_nuisance_by_roi")
        full_roi = parse_float_vector(row["r2_full_by_roi"], roi_count, f"c1_rows[{row_index}].r2_full_by_roi")
        unique_roi = parse_float_vector(row["unique_r2_by_roi"], roi_count, f"c1_rows[{row_index}].unique_r2_by_roi")
        require_array_close(unique_roi, np.asarray(full_roi) - np.asarray(nuisance_roi), f"C1 ROI unique arithmetic row {row_index}")
        nuisance_mean = require_float(row["r2_nuisance"], f"c1_rows[{row_index}].r2_nuisance")
        full_mean = require_float(row["r2_full"], f"c1_rows[{row_index}].r2_full")
        unique_mean = require_float(row["unique_r2"], f"c1_rows[{row_index}].unique_r2")
        require_close(nuisance_mean, float(np.mean(nuisance_roi)), f"C1 nuisance ROI mean row {row_index}")
        require_close(full_mean, float(np.mean(full_roi)), f"C1 full ROI mean row {row_index}")
        require_close(unique_mean, float(np.mean(unique_roi)), f"C1 unique ROI mean row {row_index}")
        require_close(unique_mean, full_mean - nuisance_mean, f"C1 aggregate unique arithmetic row {row_index}")
        key = (uid, nuisance, fold, representation)
        if key in index:
            raise ProtocolError(f"duplicate C1 cell: {key}")
        normalized = dict(row)
        normalized.update(
            {
                "alpha_nuisance": alpha_nuisance,
                "alpha_full": alpha_full,
                "r2_nuisance_by_roi": nuisance_roi,
                "r2_full_by_roi": full_roi,
                "unique_r2_by_roi": unique_roi,
                "r2_nuisance": nuisance_mean,
                "r2_full": full_mean,
                "unique_r2": unique_mean,
            }
        )
        index[key] = normalized

    expected_keys = set(itertools.product(uids, nuisances, range(len(blocks)), ("aligned", "twin")))
    if set(index) != expected_keys:
        raise ProtocolError("C1 cell grid is incomplete or contains unexpected cells")
    for uid, nuisance, fold in itertools.product(uids, nuisances, range(len(blocks))):
        aligned = index[(uid, nuisance, fold, "aligned")]
        twin = index[(uid, nuisance, fold, "twin")]
        require_close(aligned["alpha_nuisance"], twin["alpha_nuisance"], "C1 paired nuisance alpha")
        require_close(aligned["r2_nuisance"], twin["r2_nuisance"], "C1 paired nuisance R2")
        require_array_close(aligned["r2_nuisance_by_roi"], twin["r2_nuisance_by_roi"], "C1 paired nuisance ROI R2")
        if (
            aligned["target_pca_basis_sha256"]
            != twin["target_pca_basis_sha256"]
        ):
            raise ProtocolError("C1 aligned/twin target PCA bases differ")
        if (
            aligned["static_pca_basis_sha256"]
            != twin["static_pca_basis_sha256"]
        ):
            raise ProtocolError("C1 aligned/twin static PCA bases differ")
    for fold in range(len(blocks)):
        target_hashes = {
            index[(uid, nuisance, fold, representation)][
                "target_pca_basis_sha256"
            ]
            for uid, nuisance, representation in itertools.product(
                uids, nuisances, ("aligned", "twin")
            )
        }
        static_hashes = {
            index[(uid, nuisance, fold, representation)][
                "static_pca_basis_sha256"
            ]
            for uid, nuisance, representation in itertools.product(
                uids, nuisances, ("aligned", "twin")
            )
        }
        if len(target_hashes) != 1 or len(static_hashes) != 1:
            raise ProtocolError("C1 fold-specific PCA basis identity is not shared")
    return index


C2_ROW_KEYS = {
    "seed",
    "arm",
    "layer",
    "nuisance_variant",
    "fold",
    "test_start",
    "test_stop_exclusive",
    "test_count",
    "cache_key",
    "weight_sha256",
    "representation_cache_sha256",
    "student_pca_basis_sha256",
    "coordinate_count",
    "coordinate_sst_min",
    "coordinate_sst_floor",
    "coordinates_below_floor",
    "alpha_nuisance",
    "alpha_full",
    "nuisance_sse_total",
    "full_sse_total",
    "sst_total",
    "r2_nuisance_total",
    "r2_full_total",
    "unique_r2_total",
    "r2_nuisance_equal_coordinate",
    "r2_full_equal_coordinate",
    "unique_r2_equal_coordinate",
}


def expected_representation_identities(
    config: Mapping[str, Any], extraction: Mapping[str, Any]
) -> dict[tuple[int, str], tuple[str, str, str]]:
    rows = require_list(extraction.get("cache_rows"), "E025 extraction.cache_rows")
    wanted = {
        (int(seed), str(arm))
        for seed in config["estimator"]["seeds"]
        for arm in config["estimator"]["arms"]
    }
    mapping: dict[tuple[int, str], tuple[str, str, str]] = {}
    for row_index, raw in enumerate(rows):
        row = require_mapping(raw, f"E025 extraction.cache_rows[{row_index}]")
        cache_key = require_str(row.get("cache_key"), f"E025 extraction.cache_rows[{row_index}].cache_key")
        cache_hash = require_sha256(row.get("sha256"), f"E025 extraction.cache_rows[{row_index}].sha256")
        weight_hash = require_sha256(row.get("weight_sha256"), f"E025 extraction.cache_rows[{row_index}].weight_sha256")
        aliases = require_list(row.get("aliases"), f"E025 extraction.cache_rows[{row_index}].aliases")
        for alias_index, raw_alias in enumerate(aliases):
            alias = require_mapping(raw_alias, f"E025 extraction.cache_rows[{row_index}].aliases[{alias_index}]")
            if alias.get("family") != "tribe":
                continue
            seed = alias.get("seed")
            arm = alias.get("arm")
            if isinstance(seed, bool) or not isinstance(seed, int) or not isinstance(arm, str):
                continue
            key = (seed, arm)
            if key not in wanted:
                continue
            if key in mapping:
                raise ProtocolError(f"duplicate fixed E025 representation alias: {key}")
            mapping[key] = (cache_key, weight_hash, cache_hash)
    if set(mapping) != wanted:
        raise ProtocolError(f"fixed E025 representation aliases are incomplete: {sorted(wanted - set(mapping))}")
    return mapping


def validate_c2_rows(
    rows_value: Any,
    config: Mapping[str, Any],
    fixed_cache_identities: Mapping[tuple[int, str], tuple[str, str, str]],
) -> dict[tuple[int, str, int, str, int], dict[str, Any]]:
    rows = require_list(rows_value, "c2_rows")
    seeds = config["estimator"]["seeds"]
    arms = config["estimator"]["arms"]
    layers = [config["estimator"]["primary_layer"], config["estimator"]["sensitivity_layer"]]
    nuisances = list(config["estimator"]["nuisance_variants"])
    blocks = config["folds"]["test_blocks"]
    alphas = config["estimator"]["ridge_alphas"]
    coordinate_floor = float(config["estimator"]["coordinate_sst_floor"])
    coordinate_count = int(config["target"]["target_dim"])
    expected_count = len(seeds) * len(arms) * len(layers) * len(nuisances) * len(blocks)
    if len(rows) != expected_count:
        raise ProtocolError(f"c2_rows count {len(rows)} != frozen {expected_count}")

    index: dict[tuple[int, str, int, str, int], dict[str, Any]] = {}
    cache_identity: dict[tuple[int, str], tuple[str, str, str]] = {}
    for row_index, raw in enumerate(rows):
        row = require_mapping(raw, f"c2_rows[{row_index}]")
        expect_exact_keys(row, C2_ROW_KEYS, f"c2_rows[{row_index}]")
        seed = require_int(row["seed"], f"c2_rows[{row_index}].seed")
        arm = require_str(row["arm"], f"c2_rows[{row_index}].arm")
        layer = require_int(row["layer"], f"c2_rows[{row_index}].layer")
        nuisance = require_str(row["nuisance_variant"], f"c2_rows[{row_index}].nuisance_variant")
        fold = require_int(row["fold"], f"c2_rows[{row_index}].fold")
        if seed not in seeds or arm not in arms or layer not in layers or nuisance not in nuisances or fold not in range(len(blocks)):
            raise ProtocolError(f"unknown C2 cell identity at row {row_index}")
        start, stop = blocks[fold]
        if row["test_start"] != start or row["test_stop_exclusive"] != stop or row["test_count"] != stop - start:
            raise ProtocolError(f"C2 fold bounds mismatch at row {row_index}")
        cache_key = require_str(row["cache_key"], f"c2_rows[{row_index}].cache_key")
        weight_hash = require_sha256(row["weight_sha256"], f"c2_rows[{row_index}].weight_sha256")
        cache_hash = require_sha256(row["representation_cache_sha256"], f"c2_rows[{row_index}].representation_cache_sha256")
        student_basis_hash = require_sha256(
            row["student_pca_basis_sha256"],
            f"c2_rows[{row_index}].student_pca_basis_sha256",
        )
        cache_tuple = (cache_key, weight_hash, cache_hash)
        arm_seed = (seed, arm)
        if arm_seed in cache_identity and cache_identity[arm_seed] != cache_tuple:
            raise ProtocolError(f"C2 cache identity changes within arm/seed {arm_seed}")
        cache_identity[arm_seed] = cache_tuple
        if arm_seed not in fixed_cache_identities or fixed_cache_identities[arm_seed] != cache_tuple:
            raise ProtocolError(f"C2 cache identity differs from frozen E025 extraction for {arm_seed}")
        if require_int(row["coordinate_count"], f"c2_rows[{row_index}].coordinate_count") != coordinate_count:
            raise ProtocolError(f"C2 coordinate count mismatch at row {row_index}")
        observed_floor = require_float(row["coordinate_sst_floor"], f"c2_rows[{row_index}].coordinate_sst_floor")
        require_close(observed_floor, coordinate_floor, f"C2 coordinate floor row {row_index}")
        sst_min = require_float(row["coordinate_sst_min"], f"c2_rows[{row_index}].coordinate_sst_min")
        if sst_min <= coordinate_floor:
            raise ProtocolError(f"C2 coordinate SST at or below frozen floor at row {row_index}")
        if require_int(row["coordinates_below_floor"], f"c2_rows[{row_index}].coordinates_below_floor") != 0:
            raise ProtocolError(f"C2 has coordinates below the denominator floor at row {row_index}")
        alpha_nuisance = validate_alpha(row["alpha_nuisance"], alphas, f"c2_rows[{row_index}].alpha_nuisance")
        alpha_full = validate_alpha(row["alpha_full"], alphas, f"c2_rows[{row_index}].alpha_full")
        nuisance_sse = require_float(row["nuisance_sse_total"], f"c2_rows[{row_index}].nuisance_sse_total")
        full_sse = require_float(row["full_sse_total"], f"c2_rows[{row_index}].full_sse_total")
        sst_total = require_float(row["sst_total"], f"c2_rows[{row_index}].sst_total")
        if nuisance_sse < 0 or full_sse < 0 or sst_total <= 0:
            raise ProtocolError(f"C2 SSE/SST must be nonnegative with positive SST at row {row_index}")
        r2_nuisance = require_float(row["r2_nuisance_total"], f"c2_rows[{row_index}].r2_nuisance_total")
        r2_full = require_float(row["r2_full_total"], f"c2_rows[{row_index}].r2_full_total")
        unique_total = require_float(row["unique_r2_total"], f"c2_rows[{row_index}].unique_r2_total")
        require_close(r2_nuisance, 1.0 - nuisance_sse / sst_total, f"C2 nuisance total R2 row {row_index}")
        require_close(r2_full, 1.0 - full_sse / sst_total, f"C2 full total R2 row {row_index}")
        require_close(unique_total, r2_full - r2_nuisance, f"C2 total unique R2 row {row_index}")
        eq_nuisance = require_float(row["r2_nuisance_equal_coordinate"], f"c2_rows[{row_index}].r2_nuisance_equal_coordinate")
        eq_full = require_float(row["r2_full_equal_coordinate"], f"c2_rows[{row_index}].r2_full_equal_coordinate")
        eq_unique = require_float(row["unique_r2_equal_coordinate"], f"c2_rows[{row_index}].unique_r2_equal_coordinate")
        require_close(eq_unique, eq_full - eq_nuisance, f"C2 equal-coordinate unique R2 row {row_index}")
        key = (seed, arm, layer, nuisance, fold)
        if key in index:
            raise ProtocolError(f"duplicate C2 cell: {key}")
        normalized = dict(row)
        normalized.update(
            {
                "alpha_nuisance": alpha_nuisance,
                "alpha_full": alpha_full,
                "nuisance_sse_total": nuisance_sse,
                "full_sse_total": full_sse,
                "sst_total": sst_total,
                "r2_nuisance_total": r2_nuisance,
                "r2_full_total": r2_full,
                "unique_r2_total": unique_total,
                "r2_nuisance_equal_coordinate": eq_nuisance,
                "r2_full_equal_coordinate": eq_full,
                "unique_r2_equal_coordinate": eq_unique,
                "coordinate_sst_min": sst_min,
                "student_pca_basis_sha256": student_basis_hash,
            }
        )
        index[key] = normalized

    expected_keys = set(itertools.product(seeds, arms, layers, nuisances, range(len(blocks))))
    if set(index) != expected_keys:
        raise ProtocolError("C2 cell grid is incomplete or contains unexpected cells")

    nuisance_fields = (
        "alpha_nuisance",
        "nuisance_sse_total",
        "sst_total",
        "r2_nuisance_total",
        "r2_nuisance_equal_coordinate",
        "coordinate_sst_min",
        "coordinate_sst_floor",
        "coordinates_below_floor",
        "coordinate_count",
    )
    for nuisance, fold in itertools.product(nuisances, range(len(blocks))):
        group = [index[(seed, arm, layer, nuisance, fold)] for seed, arm, layer in itertools.product(seeds, arms, layers)]
        reference = group[0]
        for row in group[1:]:
            for field in nuisance_fields:
                require_close(float(row[field]), float(reference[field]), f"C2 repeated nuisance field {field} for {nuisance}/fold{fold}")
    denominator_fields = (
        "sst_total",
        "coordinate_sst_min",
        "coordinate_sst_floor",
        "coordinates_below_floor",
        "coordinate_count",
    )
    for fold in range(len(blocks)):
        group = [
            index[(seed, arm, layer, nuisance, fold)]
            for seed, arm, layer, nuisance in itertools.product(seeds, arms, layers, nuisances)
        ]
        reference = group[0]
        for row in group[1:]:
            for field in denominator_fields:
                require_close(float(row[field]), float(reference[field]), f"C2 denominator field {field} across nuisance variants at fold{fold}")
    for seed, arm, layer, fold in itertools.product(
        seeds, arms, layers, range(len(blocks))
    ):
        basis_hashes = {
            index[(seed, arm, layer, nuisance, fold)][
                "student_pca_basis_sha256"
            ]
            for nuisance in nuisances
        }
        if len(basis_hashes) != 1:
            raise ProtocolError(
                "C2 student PCA basis changes across nuisance variants for "
                f"{(seed, arm, layer, fold)}"
            )
    return index


C3_ROW_KEYS = {
    "uid",
    "participant_split",
    "seed",
    "arm",
    "layer",
    "nuisance_variant",
    "fold",
    "representation",
    "test_start",
    "test_stop_exclusive",
    "test_count",
    "target_pca_basis_sha256",
    "student_pca_basis_sha256",
    "static_pca_basis_sha256",
    "cache_key",
    "weight_sha256",
    "representation_cache_sha256",
    "target_component_count",
    "student_component_count",
    "alpha_response_nuisance",
    "alpha_response_full",
    "alpha_target_full",
    "r2_base_by_roi",
    "r2_bridge_by_roi",
    "bridge_unique_r2_by_roi",
    "r2_base",
    "r2_bridge",
    "bridge_unique_r2",
    "response_target_coefficient_l2",
    "student_target_coefficient_l2",
    "target_pc_contribution_l2",
    "composed_contribution_l2",
}


def validate_c3_rows(
    rows_value: Any,
    config: Mapping[str, Any],
    fixed_cache_identities: Mapping[tuple[int, str], tuple[str, str, str]],
    c1_index: Mapping[tuple[int, str, int, str], Mapping[str, Any]],
    c2_index: Mapping[tuple[int, str, int, str, int], Mapping[str, Any]],
) -> dict[tuple[int, int, str, int, str, int, str], dict[str, Any]]:
    rows = require_list(rows_value, "c3_rows")
    uids = config["substrate"]["valid_uids"]
    train = set(config["substrate"]["train_uids"])
    heldout = set(config["substrate"]["heldout_uids"])
    seeds = config["estimator"]["seeds"]
    arms = config["estimator"]["arms"]
    layers = [
        config["estimator"]["primary_layer"],
        config["estimator"]["sensitivity_layer"],
    ]
    nuisances = list(config["estimator"]["nuisance_variants"])
    alignments = list(config["bridge"]["alignments"])
    blocks = config["folds"]["test_blocks"]
    alphas = config["estimator"]["ridge_alphas"]
    roi_count = len(config["substrate"]["rois"])
    target_components = int(config["bridge"]["target_pca_rank"])
    student_components = int(config["bridge"]["student_pca_rank"])
    expected_count = (
        len(uids)
        * len(seeds)
        * len(arms)
        * len(layers)
        * len(nuisances)
        * len(blocks)
        * len(alignments)
    )
    if len(rows) != expected_count:
        raise ProtocolError(f"c3_rows count {len(rows)} != frozen {expected_count}")

    index: dict[tuple[int, int, str, int, str, int, str], dict[str, Any]] = {}
    for row_index, raw in enumerate(rows):
        row = require_mapping(raw, f"c3_rows[{row_index}]")
        expect_exact_keys(row, C3_ROW_KEYS, f"c3_rows[{row_index}]")
        uid = require_int(row["uid"], f"c3_rows[{row_index}].uid")
        seed = require_int(row["seed"], f"c3_rows[{row_index}].seed")
        arm = require_str(row["arm"], f"c3_rows[{row_index}].arm")
        layer = require_int(row["layer"], f"c3_rows[{row_index}].layer")
        nuisance = require_str(
            row["nuisance_variant"], f"c3_rows[{row_index}].nuisance_variant"
        )
        fold = require_int(row["fold"], f"c3_rows[{row_index}].fold")
        alignment = require_str(
            row["representation"], f"c3_rows[{row_index}].representation"
        )
        if (
            uid not in uids
            or seed not in seeds
            or arm not in arms
            or layer not in layers
            or nuisance not in nuisances
            or fold not in range(len(blocks))
            or alignment not in alignments
        ):
            raise ProtocolError(f"unknown C3 cell identity at row {row_index}")
        split = require_str(
            row["participant_split"], f"c3_rows[{row_index}].participant_split"
        )
        expected_split = "train" if uid in train else "heldout" if uid in heldout else None
        if split != expected_split:
            raise ProtocolError(f"C3 participant split mismatch for uid {uid}")
        start, stop = blocks[fold]
        if (
            row["test_start"] != start
            or row["test_stop_exclusive"] != stop
            or row["test_count"] != stop - start
        ):
            raise ProtocolError(f"C3 fold bounds mismatch at row {row_index}")
        target_basis_hash = require_sha256(
            row["target_pca_basis_sha256"],
            f"c3_rows[{row_index}].target_pca_basis_sha256",
        )
        student_basis_hash = require_sha256(
            row["student_pca_basis_sha256"],
            f"c3_rows[{row_index}].student_pca_basis_sha256",
        )
        static_basis_hash = require_sha256(
            row["static_pca_basis_sha256"],
            f"c3_rows[{row_index}].static_pca_basis_sha256",
        )

        cache_tuple = (
            require_str(row["cache_key"], f"c3_rows[{row_index}].cache_key"),
            require_sha256(
                row["weight_sha256"], f"c3_rows[{row_index}].weight_sha256"
            ),
            require_sha256(
                row["representation_cache_sha256"],
                f"c3_rows[{row_index}].representation_cache_sha256",
            ),
        )
        if fixed_cache_identities.get((seed, arm)) != cache_tuple:
            raise ProtocolError(
                f"C3 cache identity differs from frozen E025 extraction for {(seed, arm)}"
            )
        if (
            require_int(
                row["target_component_count"],
                f"c3_rows[{row_index}].target_component_count",
            )
            != target_components
            or require_int(
                row["student_component_count"],
                f"c3_rows[{row_index}].student_component_count",
            )
            != student_components
        ):
            raise ProtocolError(f"C3 component count mismatch at row {row_index}")

        alpha_response_nuisance = validate_alpha(
            row["alpha_response_nuisance"],
            alphas,
            f"c3_rows[{row_index}].alpha_response_nuisance",
        )
        alpha_response_full = validate_alpha(
            row["alpha_response_full"],
            alphas,
            f"c3_rows[{row_index}].alpha_response_full",
        )
        alpha_target_full = validate_alpha(
            row["alpha_target_full"],
            alphas,
            f"c3_rows[{row_index}].alpha_target_full",
        )
        base_roi = parse_float_vector(
            row["r2_base_by_roi"], roi_count, f"c3_rows[{row_index}].r2_base_by_roi"
        )
        bridge_roi = parse_float_vector(
            row["r2_bridge_by_roi"],
            roi_count,
            f"c3_rows[{row_index}].r2_bridge_by_roi",
        )
        unique_roi = parse_float_vector(
            row["bridge_unique_r2_by_roi"],
            roi_count,
            f"c3_rows[{row_index}].bridge_unique_r2_by_roi",
        )
        require_array_close(
            unique_roi,
            np.asarray(bridge_roi) - np.asarray(base_roi),
            f"C3 ROI bridge arithmetic row {row_index}",
        )
        base_mean = require_float(row["r2_base"], f"c3_rows[{row_index}].r2_base")
        bridge_mean = require_float(
            row["r2_bridge"], f"c3_rows[{row_index}].r2_bridge"
        )
        unique_mean = require_float(
            row["bridge_unique_r2"], f"c3_rows[{row_index}].bridge_unique_r2"
        )
        require_close(base_mean, float(np.mean(base_roi)), f"C3 base ROI mean row {row_index}")
        require_close(
            bridge_mean, float(np.mean(bridge_roi)), f"C3 bridge ROI mean row {row_index}"
        )
        require_close(
            unique_mean, float(np.mean(unique_roi)), f"C3 unique ROI mean row {row_index}"
        )
        require_close(
            unique_mean, bridge_mean - base_mean, f"C3 aggregate bridge arithmetic row {row_index}"
        )
        norms = {
            field: require_float(row[field], f"c3_rows[{row_index}].{field}")
            for field in (
                "response_target_coefficient_l2",
                "student_target_coefficient_l2",
                "target_pc_contribution_l2",
                "composed_contribution_l2",
            )
        }
        if any(value < 0 for value in norms.values()):
            raise ProtocolError(f"C3 coefficient/contribution norm is negative at row {row_index}")

        c1 = c1_index[(uid, nuisance, fold, alignment)]
        require_close(
            alpha_response_nuisance,
            float(c1["alpha_nuisance"]),
            f"C3/C1 nuisance alpha row {row_index}",
        )
        require_close(
            alpha_response_full,
            float(c1["alpha_full"]),
            f"C3/C1 full alpha row {row_index}",
        )
        require_array_close(
            base_roi,
            c1["r2_nuisance_by_roi"],
            f"C3/C1 nuisance ROI score row {row_index}",
        )
        require_close(
            base_mean,
            float(c1["r2_nuisance"]),
            f"C3/C1 nuisance score row {row_index}",
        )
        if target_basis_hash != c1["target_pca_basis_sha256"]:
            raise ProtocolError(f"C3/C1 target PCA basis mismatch at row {row_index}")
        if static_basis_hash != c1["static_pca_basis_sha256"]:
            raise ProtocolError(f"C3/C1 static PCA basis mismatch at row {row_index}")
        c2 = c2_index[(seed, arm, layer, nuisance, fold)]
        if student_basis_hash != c2["student_pca_basis_sha256"]:
            raise ProtocolError(f"C3/C2 student PCA basis mismatch at row {row_index}")

        key = (uid, seed, arm, layer, nuisance, fold, alignment)
        if key in index:
            raise ProtocolError(f"duplicate C3 cell: {key}")
        normalized = dict(row)
        normalized.update(
            {
                "alpha_response_nuisance": alpha_response_nuisance,
                "alpha_response_full": alpha_response_full,
                "alpha_target_full": alpha_target_full,
                "r2_base_by_roi": base_roi,
                "r2_bridge_by_roi": bridge_roi,
                "bridge_unique_r2_by_roi": unique_roi,
                "r2_base": base_mean,
                "r2_bridge": bridge_mean,
                "bridge_unique_r2": unique_mean,
                **norms,
            }
        )
        index[key] = normalized

    expected_keys = set(
        itertools.product(
            uids,
            seeds,
            arms,
            layers,
            nuisances,
            range(len(blocks)),
            alignments,
        )
    )
    if set(index) != expected_keys:
        raise ProtocolError("C3 cell grid is incomplete or contains unexpected cells")

    for uid, nuisance, fold, alignment in itertools.product(
        uids, nuisances, range(len(blocks)), alignments
    ):
        group = [
            index[(uid, seed, arm, layer, nuisance, fold, alignment)]
            for seed, arm, layer in itertools.product(seeds, arms, layers)
        ]
        reference = group[0]
        for row in group[1:]:
            for field in (
                "alpha_response_nuisance",
                "alpha_response_full",
                "r2_base",
                "response_target_coefficient_l2",
            ):
                require_close(
                    float(row[field]),
                    float(reference[field]),
                    f"C3 repeated participant field {field}",
                )
            require_array_close(
                row["r2_base_by_roi"],
                reference["r2_base_by_roi"],
                "C3 repeated participant base ROI score",
            )
            if (
                row["target_pca_basis_sha256"]
                != reference["target_pca_basis_sha256"]
                or row["static_pca_basis_sha256"]
                != reference["static_pca_basis_sha256"]
            ):
                raise ProtocolError("C3 participant cell PCA basis identity changed")

    for seed, arm, layer, nuisance, fold, alignment in itertools.product(
        seeds, arms, layers, nuisances, range(len(blocks)), alignments
    ):
        group = [
            index[(uid, seed, arm, layer, nuisance, fold, alignment)]
            for uid in uids
        ]
        reference = group[0]
        for row in group[1:]:
            for field in (
                "alpha_target_full",
                "student_target_coefficient_l2",
                "target_pc_contribution_l2",
            ):
                require_close(
                    float(row[field]),
                    float(reference[field]),
                    f"C3 repeated student-target field {field}",
                )
            if (
                row["student_pca_basis_sha256"]
                != reference["student_pca_basis_sha256"]
                or row["target_pca_basis_sha256"]
                != reference["target_pca_basis_sha256"]
                or row["static_pca_basis_sha256"]
                != reference["static_pca_basis_sha256"]
            ):
                raise ProtocolError("C3 alignment-shared PCA basis identity changed")
    for uid, seed, arm, layer, nuisance, fold in itertools.product(
        uids, seeds, arms, layers, nuisances, range(len(blocks))
    ):
        aligned = index[(uid, seed, arm, layer, nuisance, fold, "aligned")]
        twin = index[(uid, seed, arm, layer, nuisance, fold, "twin")]
        for field in (
            "target_pca_basis_sha256",
            "student_pca_basis_sha256",
            "static_pca_basis_sha256",
        ):
            if aligned[field] != twin[field]:
                raise ProtocolError(
                    f"C3 aligned/twin {field} identity differs"
                )
    for seed, arm, layer, fold in itertools.product(
        seeds, arms, layers, range(len(blocks))
    ):
        c3_basis_hashes = {
            index[(uid, seed, arm, layer, nuisance, fold, alignment)][
                "student_pca_basis_sha256"
            ]
            for uid, nuisance, alignment in itertools.product(
                uids, nuisances, alignments
            )
        }
        c2_basis_hashes = {
            c2_index[(seed, arm, layer, nuisance, fold)][
                "student_pca_basis_sha256"
            ]
            for nuisance in nuisances
        }
        if len(c3_basis_hashes) != 1 or c3_basis_hashes != c2_basis_hashes:
            raise ProtocolError(
                "C2/C3 student PCA basis is not shared across nuisances for "
                f"{(seed, arm, layer, fold)}"
            )
    return index


def exact_sign_test(values: Iterable[float]) -> dict[str, Any]:
    x = np.asarray(list(values), dtype=np.float64)
    if x.ndim != 1 or x.size == 0 or not np.isfinite(x).all():
        raise ProtocolError("exact sign test requires a nonempty finite vector")
    nonzero = x[x != 0]
    positive = int(np.sum(nonzero > 0))
    pvalue = float(stats.binomtest(positive, int(nonzero.size), 0.5, alternative="two-sided").pvalue) if nonzero.size else 1.0
    return {
        "positive": positive,
        "negative": int(np.sum(nonzero < 0)),
        "zero": int(np.sum(x == 0)),
        "n_nonzero": int(nonzero.size),
        "two_sided_p": pvalue,
    }


def wilcoxon_test(values: Iterable[float]) -> dict[str, Any]:
    x = np.asarray(list(values), dtype=np.float64)
    if x.ndim != 1 or x.size == 0 or not np.isfinite(x).all():
        raise ProtocolError("Wilcoxon test requires a nonempty finite vector")
    if np.all(x == 0):
        return {"status": "unavailable_all_zero", "statistic": None, "two_sided_p": None}
    try:
        result = stats.wilcoxon(x, alternative="two-sided", zero_method="wilcox", method="auto")
    except ValueError as exc:
        return {"status": f"unavailable: {exc}", "statistic": None, "two_sided_p": None}
    return {"status": "ok", "statistic": float(result.statistic), "two_sided_p": float(result.pvalue)}


def noncentral_power(delta: float, sd: float, n: int, alpha: float) -> float:
    if sd <= 0:
        return 1.0 if delta != 0 else alpha
    critical = float(stats.t.ppf(1.0 - alpha / 2.0, n - 1))
    ncp = abs(delta) / (sd / math.sqrt(n))
    power = float(stats.nct.sf(critical, n - 1, ncp) + stats.nct.cdf(-critical, n - 1, ncp))
    return float(min(1.0, max(0.0, power)))


def mde_for_power(sd: float, n: int, alpha: float, desired_power: float = 0.80) -> float:
    if sd <= 0:
        return 0.0
    objective = lambda delta: noncentral_power(delta, sd, n, alpha) - desired_power
    upper = sd / math.sqrt(n)
    while objective(upper) < 0 and upper < 100.0 * sd:
        upper *= 2.0
    if objective(upper) < 0:
        raise ProtocolError("could not bracket observed-variance MDE")
    return float(optimize.brentq(objective, 0.0, upper))


def summarize_values(values: Sequence[float], alpha: float, reference: float | None = None) -> dict[str, Any]:
    x = np.asarray(values, dtype=np.float64)
    if x.ndim != 1 or x.size < 2 or not np.isfinite(x).all():
        raise ProtocolError("summary requires at least two finite values")
    mean = float(np.mean(x))
    median = float(np.median(x))
    sd = float(np.std(x, ddof=1))
    se = sd / math.sqrt(x.size)
    two_sided_q = float(stats.t.ppf(1.0 - alpha / 2.0, x.size - 1))
    one_sided_q = float(stats.t.ppf(1.0 - alpha, x.size - 1))
    output: dict[str, Any] = {
        "n": int(x.size),
        "values": [float(value) for value in x],
        "mean": mean,
        "median": median,
        "sd": sd,
        "se": se,
        "two_sided_t_ci95": [mean - two_sided_q * se, mean + two_sided_q * se],
        "one_sided_t_lower95": mean - one_sided_q * se,
        "one_sided_t_upper95": mean + one_sided_q * se,
        "exact_sign_test": exact_sign_test(x),
        "wilcoxon_signed_rank": wilcoxon_test(x),
    }
    if reference is not None:
        output["observed_variance_sensitivity"] = {
            "reference": float(reference),
            "mde80_two_sided_t": mde_for_power(sd, int(x.size), alpha),
            "power_at_reference_two_sided_t": noncentral_power(reference, sd, int(x.size), alpha),
        }
    return output


def add_simultaneous_family_upper(
    summary: dict[str, Any], alpha: float, family_size: int
) -> dict[str, Any]:
    statistics = summary["statistics"]
    endpoint_alpha = alpha / family_size
    quantile = float(
        stats.t.ppf(1.0 - endpoint_alpha, int(statistics["n"]) - 1)
    )
    upper = float(statistics["mean"] + quantile * statistics["se"])
    statistics["simultaneous_family_one_sided_t_upper95"] = upper
    statistics["simultaneous_family_size"] = family_size
    statistics["bonferroni_endpoint_alpha"] = endpoint_alpha
    return summary


def exact_magnitude_sign_flip(values: Sequence[float]) -> dict[str, Any]:
    x = np.asarray(values, dtype=np.float64)
    if x.shape != (6,) or not np.isfinite(x).all():
        raise ProtocolError("E030 exact sign-flip requires exactly six finite seed contrasts")
    observed = abs(float(np.mean(x)))
    statistics: list[float] = []
    for signs in itertools.product((-1.0, 1.0), repeat=x.size):
        statistics.append(abs(float(np.mean(x * np.asarray(signs, dtype=np.float64)))))
    tolerance = 1e-15 + 1e-12 * observed
    extreme = sum(value >= observed - tolerance for value in statistics)
    return {
        "test": "exact_2^6_magnitude_preserving_two_sided_sign_flip",
        "statistic_abs_mean": observed,
        "enumeration_count": len(statistics),
        "extreme_count": int(extreme),
        "two_sided_p": float(extreme / len(statistics)),
    }


def summarize_unit_fold(
    unit_order: Sequence[int],
    fold_values: Mapping[int, Mapping[int, float]],
    alpha: float,
    reference: float | None = None,
    subgroups: Mapping[str, Sequence[int]] | None = None,
) -> dict[str, Any]:
    folds = sorted(next(iter(fold_values.values())))
    if any(sorted(fold_values[unit]) != folds for unit in unit_order):
        raise ProtocolError("unit/fold summary grid is incomplete")
    by_unit = {str(unit): float(np.mean([fold_values[unit][fold] for fold in folds])) for unit in unit_order}
    values = [by_unit[str(unit)] for unit in unit_order]
    by_block = {
        str(fold): float(np.mean([fold_values[unit][fold] for unit in unit_order]))
        for fold in folds
    }
    leave_unit = {
        str(unit): float(np.mean([by_unit[str(other)] for other in unit_order if other != unit]))
        for unit in unit_order
    }
    leave_block = {
        str(fold): float(
            np.mean(
                [fold_values[unit][other_fold] for unit in unit_order for other_fold in folds if other_fold != fold]
            )
        )
        for fold in folds
    }
    output: dict[str, Any] = {
        "unit_order": list(unit_order),
        "by_unit": by_unit,
        "statistics": summarize_values(values, alpha, reference),
        "by_block": by_block,
        "leave_one_unit_out_means": leave_unit,
        "leave_one_block_out_means": leave_block,
    }
    if subgroups is not None:
        output["subgroups"] = {
            name: {
                "units": list(members),
                "values": [by_unit[str(unit)] for unit in members],
                "mean": float(np.mean([by_unit[str(unit)] for unit in members])),
            }
            for name, members in subgroups.items()
        }
    return output


def analyze_c1(index: Mapping[tuple[int, str, int, str], Mapping[str, Any]], config: Mapping[str, Any]) -> dict[str, Any]:
    uids = config["substrate"]["valid_uids"]
    folds = range(config["folds"]["count"])
    alpha = float(config["inference"]["alpha"])
    reference = float(config["inference"]["practical_reference_unique_r2"])
    subgroups = {
        "train4": config["substrate"]["train_uids"],
        "heldout5": config["substrate"]["heldout_uids"],
    }
    cells: dict[str, Any] = {}
    for nuisance in config["estimator"]["nuisance_variants"]:
        a_fold = {
            uid: {fold: float(index[(uid, nuisance, fold, "aligned")]["unique_r2"]) for fold in folds}
            for uid in uids
        }
        q_fold = {
            uid: {
                fold: float(index[(uid, nuisance, fold, "aligned")]["unique_r2"])
                - float(index[(uid, nuisance, fold, "twin")]["unique_r2"])
                for fold in folds
            }
            for uid in uids
        }
        family_size = int(config["inference"]["terminal_family_sizes"]["C1"])
        a_summary = add_simultaneous_family_upper(
            summarize_unit_fold(uids, a_fold, alpha, reference, subgroups),
            alpha,
            family_size,
        )
        q_summary = add_simultaneous_family_upper(
            summarize_unit_fold(uids, q_fold, alpha, reference, subgroups),
            alpha,
            family_size,
        )
        cells[nuisance] = {
            "A_aligned_above_nuisance": a_summary,
            "Q_aligned_minus_twin": q_summary,
        }
    return {
        "inference_unit": "participant",
        "participants_are_biological_units": True,
        "folds_and_rois_are_not_inference_units": True,
        "primary_nuisance": config["estimator"]["primary_nuisance"],
        "cells": cells,
    }


def analyze_c2(index: Mapping[tuple[int, str, int, str, int], Mapping[str, Any]], config: Mapping[str, Any]) -> dict[str, Any]:
    seeds = config["estimator"]["seeds"]
    folds = range(config["folds"]["count"])
    alpha = float(config["inference"]["alpha"])
    kd_arm, tribe_arm = config["estimator"]["arms"]
    cells: dict[str, Any] = {}
    for layer in (config["estimator"]["primary_layer"], config["estimator"]["sensitivity_layer"]):
        layer_cells: dict[str, Any] = {}
        for nuisance in config["estimator"]["nuisance_variants"]:
            aggregation_cells: dict[str, Any] = {}
            for label, field in (
                ("variance_weighted_total", "unique_r2_total"),
                ("equal_coordinate_continuity", "unique_r2_equal_coordinate"),
            ):
                m_fold = {
                    seed: {fold: float(index[(seed, tribe_arm, layer, nuisance, fold)][field]) for fold in folds}
                    for seed in seeds
                }
                b_fold = {
                    seed: {
                        fold: float(index[(seed, tribe_arm, layer, nuisance, fold)][field])
                        - float(index[(seed, kd_arm, layer, nuisance, fold)][field])
                        for fold in folds
                    }
                    for seed in seeds
                }
                m_summary = summarize_unit_fold(seeds, m_fold, alpha)
                b_summary = summarize_unit_fold(seeds, b_fold, alpha)
                family_size = int(
                    config["inference"]["terminal_family_sizes"]["C2"]
                )
                add_simultaneous_family_upper(
                    m_summary, alpha, family_size
                )
                add_simultaneous_family_upper(
                    b_summary, alpha, family_size
                )
                b_summary["exact_magnitude_sign_flip"] = exact_magnitude_sign_flip(
                    [b_summary["by_unit"][str(seed)] for seed in seeds]
                )
                aggregation_cells[label] = {
                    "M_absolute_tribe_extractability": m_summary,
                    "B_tribe_minus_kd_increment": b_summary,
                }
            layer_cells[nuisance] = aggregation_cells
        cells[f"layer{layer}"] = layer_cells
    return {
        "inference_unit": "paired_seed_technical_realization",
        "seeds_are_not_biological_replications": True,
        "coordinates_folds_and_layers_are_not_inference_units": True,
        "primary_layer": config["estimator"]["primary_layer"],
        "sensitivity_layer": config["estimator"]["sensitivity_layer"],
        "primary_nuisance": config["estimator"]["primary_nuisance"],
        "primary_aggregation": "variance_weighted_total",
        "cells": cells,
    }


def seed_sensitivity_summary(
    uids: Sequence[int],
    seeds: Sequence[int],
    folds: Sequence[int],
    values: Mapping[int, Mapping[int, Mapping[int, float]]],
) -> dict[str, Any]:
    by_seed = {
        str(seed): float(
            np.mean([values[uid][seed][fold] for uid in uids for fold in folds])
        )
        for seed in seeds
    }
    leave_one_seed = {
        str(seed): float(
            np.mean(
                [
                    values[uid][other_seed][fold]
                    for uid in uids
                    for other_seed in seeds
                    if other_seed != seed
                    for fold in folds
                ]
            )
        )
        for seed in seeds
    }
    return {
        "seed_order": list(seeds),
        "by_seed_grand_mean": by_seed,
        "leave_one_seed_out_grand_means": leave_one_seed,
    }


def analyze_c3(
    index: Mapping[
        tuple[int, int, str, int, str, int, str], Mapping[str, Any]
    ],
    config: Mapping[str, Any],
) -> dict[str, Any]:
    uids = config["substrate"]["valid_uids"]
    seeds = config["estimator"]["seeds"]
    folds = list(range(config["folds"]["count"]))
    alpha = float(config["inference"]["alpha"])
    tribe_arm = config["bridge"]["absolute_arm"]
    kd_arm = config["bridge"]["comparator_arm"]
    subgroups = {
        "train4": config["substrate"]["train_uids"],
        "heldout5": config["substrate"]["heldout_uids"],
    }
    cells: dict[str, Any] = {}
    for layer in (
        config["estimator"]["primary_layer"],
        config["estimator"]["sensitivity_layer"],
    ):
        layer_cells: dict[str, Any] = {}
        for nuisance in config["estimator"]["nuisance_variants"]:
            g = lambda uid, seed, arm, fold, alignment: float(
                index[(uid, seed, arm, layer, nuisance, fold, alignment)][
                    "bridge_unique_r2"
                ]
            )
            o_values = {
                uid: {
                    seed: {
                        fold: g(uid, seed, tribe_arm, fold, "aligned")
                        for fold in folds
                    }
                    for seed in seeds
                }
                for uid in uids
            }
            d_values = {
                uid: {
                    seed: {
                        fold: g(uid, seed, tribe_arm, fold, "aligned")
                        - g(uid, seed, kd_arm, fold, "aligned")
                        for fold in folds
                    }
                    for seed in seeds
                }
                for uid in uids
            }
            j_values = {
                uid: {
                    seed: {
                        fold: (
                            g(uid, seed, tribe_arm, fold, "aligned")
                            - g(uid, seed, kd_arm, fold, "aligned")
                            - g(uid, seed, tribe_arm, fold, "twin")
                            + g(uid, seed, kd_arm, fold, "twin")
                        )
                        for fold in folds
                    }
                    for seed in seeds
                }
                for uid in uids
            }
            summaries: dict[str, Any] = {}
            for label, values in (
                ("O_absolute_tribe_bridge", o_values),
                ("D_tribe_minus_kd_bridge", d_values),
                ("J_aligned_minus_twin_increment", j_values),
            ):
                fold_values = {
                    uid: {
                        fold: float(
                            np.mean([values[uid][seed][fold] for seed in seeds])
                        )
                        for fold in folds
                    }
                    for uid in uids
                }
                summary = summarize_unit_fold(
                    uids, fold_values, alpha, subgroups=subgroups
                )
                add_simultaneous_family_upper(
                    summary,
                    alpha,
                    int(
                        config["inference"]["terminal_family_sizes"]["C3"]
                    ),
                )
                seed_sensitivity = seed_sensitivity_summary(
                    uids, seeds, folds, values
                )
                if label.startswith(("D_", "J_")):
                    seed_sensitivity["exact_magnitude_sign_flip"] = (
                        exact_magnitude_sign_flip(
                            [
                                seed_sensitivity["by_seed_grand_mean"][
                                    str(seed)
                                ]
                                for seed in seeds
                            ]
                        )
                    )
                summary["seed_sensitivity"] = seed_sensitivity
                summaries[label] = summary
            layer_cells[nuisance] = summaries
        cells[f"layer{layer}"] = layer_cells
    return {
        "inference_unit": "participant",
        "seeds_and_folds_are_averaged_within_participant": True,
        "seeds_folds_rois_layers_and_nuisance_variants_are_not_inference_units": True,
        "path_product_is_predictive_not_causal_mediation": True,
        "participant_claims_are_conditional_on_paired_seed_stability": True,
        "seed_gates_support_technical_realization_stability_only": True,
        "primary_layer": config["estimator"]["primary_layer"],
        "sensitivity_layer": config["estimator"]["sensitivity_layer"],
        "primary_nuisance": config["estimator"]["primary_nuisance"],
        "cells": cells,
    }


def all_positive(values: Iterable[float]) -> bool:
    return all(float(value) > 0 for value in values)


def c1_pass_checks(c1: Mapping[str, Any], validity_all: bool, config: Mapping[str, Any]) -> dict[str, bool]:
    cell = c1["cells"][config["estimator"]["primary_nuisance"]]
    a = cell["A_aligned_above_nuisance"]
    q = cell["Q_aligned_minus_twin"]
    minimum = int(config["inference"]["participant_min_positive"])
    checks = {
        "all_validity_checks_pass": validity_all,
        "A_two_sided_t_ci95_lower_above_zero": a["statistics"]["two_sided_t_ci95"][0] > 0,
        "Q_two_sided_t_ci95_lower_above_zero": q["statistics"]["two_sided_t_ci95"][0] > 0,
        "A_at_least_8_of_9_positive": a["statistics"]["exact_sign_test"]["positive"] >= minimum,
        "Q_at_least_8_of_9_positive": q["statistics"]["exact_sign_test"]["positive"] >= minimum,
        "A_exact_sign_two_sided_p_at_most_0_05": a["statistics"]["exact_sign_test"]["two_sided_p"] <= config["inference"]["alpha"],
        "Q_exact_sign_two_sided_p_at_most_0_05": q["statistics"]["exact_sign_test"]["two_sided_p"] <= config["inference"]["alpha"],
        "A_heldout5_mean_positive": a["subgroups"]["heldout5"]["mean"] > 0,
        "Q_heldout5_mean_positive": q["subgroups"]["heldout5"]["mean"] > 0,
        "A_all_leave_one_participant_means_positive": all_positive(a["leave_one_unit_out_means"].values()),
        "Q_all_leave_one_participant_means_positive": all_positive(q["leave_one_unit_out_means"].values()),
        "A_all_leave_one_block_means_positive": all_positive(a["leave_one_block_out_means"].values()),
        "Q_all_leave_one_block_means_positive": all_positive(q["leave_one_block_out_means"].values()),
    }
    checks["A_endpoint_pass"] = all(
        value for key, value in checks.items() if key.startswith("A_")
    )
    checks["Q_endpoint_pass"] = all(
        value for key, value in checks.items() if key.startswith("Q_")
    )
    checks["pass"] = bool(
        validity_all
        and checks["A_endpoint_pass"]
        and checks["Q_endpoint_pass"]
    )
    return checks


def c2_pass_checks(c2: Mapping[str, Any], validity_all: bool, inherited_all: bool, config: Mapping[str, Any]) -> dict[str, bool]:
    primary = c2["cells"][f"layer{config['estimator']['primary_layer']}"][config["estimator"]["primary_nuisance"]]["variance_weighted_total"]
    m = primary["M_absolute_tribe_extractability"]
    b = primary["B_tribe_minus_kd_increment"]
    checks = {
        "all_validity_checks_pass": validity_all,
        "all_inherited_quality_target_movement_gates_pass": inherited_all,
        "all_six_M_values_positive": all_positive(m["by_unit"].values()),
        "all_six_B_values_positive": all_positive(b["by_unit"].values()),
        "M_two_sided_t_ci95_lower_above_zero": m["statistics"]["two_sided_t_ci95"][0] > 0,
        "B_two_sided_t_ci95_lower_above_zero": b["statistics"]["two_sided_t_ci95"][0] > 0,
        "B_exact_sign_flip_two_sided_p_at_most_0_05": b["exact_magnitude_sign_flip"]["two_sided_p"] <= config["inference"]["alpha"],
        "M_all_leave_one_seed_means_positive": all_positive(m["leave_one_unit_out_means"].values()),
        "B_all_leave_one_seed_means_positive": all_positive(b["leave_one_unit_out_means"].values()),
        "M_all_leave_one_block_means_positive": all_positive(m["leave_one_block_out_means"].values()),
        "B_all_leave_one_block_means_positive": all_positive(b["leave_one_block_out_means"].values()),
    }
    checks["M_endpoint_pass"] = all(
        value
        for key, value in checks.items()
        if key.startswith("M_") or key == "all_six_M_values_positive"
    )
    checks["B_endpoint_pass"] = all(
        value
        for key, value in checks.items()
        if key.startswith("B_") or key == "all_six_B_values_positive"
    )
    checks["pass"] = bool(
        validity_all
        and inherited_all
        and checks["M_endpoint_pass"]
        and checks["B_endpoint_pass"]
    )
    return checks


def c3_pass_checks(
    c3: Mapping[str, Any],
    validity_all: bool,
    c1_pass: bool,
    c2_pass: bool,
    config: Mapping[str, Any],
) -> dict[str, bool]:
    primary = c3["cells"][f"layer{config['estimator']['primary_layer']}"][
        config["estimator"]["primary_nuisance"]
    ]
    minimum = int(config["inference"]["participant_min_positive"])
    alpha = float(config["inference"]["alpha"])
    metrics = {
        "O": primary["O_absolute_tribe_bridge"],
        "D": primary["D_tribe_minus_kd_bridge"],
        "J": primary["J_aligned_minus_twin_increment"],
    }
    checks: dict[str, bool] = {
        "all_validity_checks_pass": validity_all,
        "C1_primary_rules_pass": c1_pass,
        "C2_primary_rules_pass": c2_pass,
    }
    for label, summary in metrics.items():
        checks[f"{label}_two_sided_t_ci95_lower_above_zero"] = (
            summary["statistics"]["two_sided_t_ci95"][0] > 0
        )
        checks[f"{label}_at_least_8_of_9_positive"] = (
            summary["statistics"]["exact_sign_test"]["positive"] >= minimum
        )
        checks[f"{label}_exact_sign_two_sided_p_at_most_0_05"] = (
            summary["statistics"]["exact_sign_test"]["two_sided_p"] <= alpha
        )
        checks[f"{label}_heldout5_mean_positive"] = (
            summary["subgroups"]["heldout5"]["mean"] > 0
        )
        checks[f"{label}_all_leave_one_participant_means_positive"] = all_positive(
            summary["leave_one_unit_out_means"].values()
        )
        checks[f"{label}_all_leave_one_block_means_positive"] = all_positive(
            summary["leave_one_block_out_means"].values()
        )
    for label in ("D", "J"):
        seed_sensitivity = metrics[label]["seed_sensitivity"]
        checks[f"{label}_all_six_seed_grand_means_positive"] = all_positive(
            seed_sensitivity["by_seed_grand_mean"].values()
        )
        checks[
            f"{label}_exact_seed_sign_flip_two_sided_p_at_most_0_05"
        ] = (
            seed_sensitivity["exact_magnitude_sign_flip"]["two_sided_p"]
            <= alpha
        )
        checks[f"{label}_all_leave_one_seed_grand_means_positive"] = all_positive(
            seed_sensitivity[
                "leave_one_seed_out_grand_means"
            ].values()
        )
    for label in ("O", "D", "J"):
        checks[f"{label}_endpoint_pass"] = all(
            value
            for key, value in checks.items()
            if key.startswith(f"{label}_") and key != f"{label}_endpoint_pass"
        )
    checks["pass"] = bool(
        validity_all
        and c1_pass
        and c2_pass
        and checks["O_endpoint_pass"]
        and checks["D_endpoint_pass"]
        and checks["J_endpoint_pass"]
    )
    return checks


def interval_evidence_status(
    summary: Mapping[str, Any],
    exclusion_threshold: float | None,
    *,
    inclusive: bool,
) -> dict[str, Any]:
    statistics = summary["statistics"]
    lower, upper = statistics["two_sided_t_ci95"]
    marginal_one_sided_upper = statistics["one_sided_t_upper95"]
    simultaneous_one_sided_upper = statistics[
        "simultaneous_family_one_sided_t_upper95"
    ]
    excludes_threshold: bool | None
    if exclusion_threshold is None:
        excludes_threshold = None
    elif inclusive:
        excludes_threshold = simultaneous_one_sided_upper <= exclusion_threshold
    else:
        excludes_threshold = simultaneous_one_sided_upper < exclusion_threshold
    statuses: list[str] = []
    if lower > 0:
        statuses.append("supported_positive_interval")
    if upper < 0:
        statuses.append("contradicts_positive_effect")
    if excludes_threshold:
        statuses.append("simultaneous_family_upper_excludes_threshold")
    if not statuses:
        statuses.append("unresolved")
    return {
        "statuses": statuses,
        "two_sided_t_ci95": list(statistics["two_sided_t_ci95"]),
        "marginal_one_sided_t_upper95": marginal_one_sided_upper,
        "simultaneous_family_one_sided_t_upper95": (
            simultaneous_one_sided_upper
        ),
        "simultaneous_family_size": statistics["simultaneous_family_size"],
        "bonferroni_endpoint_alpha": statistics["bonferroni_endpoint_alpha"],
        "exclusion_threshold": exclusion_threshold,
        "exclusion_is_inclusive": inclusive,
        "simultaneous_family_upper_excludes_threshold": excludes_threshold,
    }


def primary_evidence_diagnostics(
    c1: Mapping[str, Any],
    c2: Mapping[str, Any],
    c3: Mapping[str, Any],
    config: Mapping[str, Any],
) -> dict[str, Any]:
    nuisance = config["estimator"]["primary_nuisance"]
    c1_primary = c1["cells"][nuisance]
    c2_primary = c2["cells"][f"layer{config['estimator']['primary_layer']}"][
        nuisance
    ]["variance_weighted_total"]
    c3_primary = c3["cells"][f"layer{config['estimator']['primary_layer']}"][
        nuisance
    ]
    reference = float(config["inference"]["practical_reference_unique_r2"])
    return {
        "C1": {
            "inherited_reference_is_sensitivity_not_pass_threshold": reference,
            "A": interval_evidence_status(
                c1_primary["A_aligned_above_nuisance"],
                reference,
                inclusive=False,
            ),
            "Q": interval_evidence_status(
                c1_primary["Q_aligned_minus_twin"],
                reference,
                inclusive=False,
            ),
        },
        "C2": {
            "positivity_exclusion_threshold": 0.0,
            "M": interval_evidence_status(
                c2_primary["M_absolute_tribe_extractability"],
                0.0,
                inclusive=True,
            ),
            "B": interval_evidence_status(
                c2_primary["B_tribe_minus_kd_increment"],
                0.0,
                inclusive=True,
            ),
        },
        "C3": {
            "positivity_exclusion_threshold": 0.0,
            "O": interval_evidence_status(
                c3_primary["O_absolute_tribe_bridge"],
                0.0,
                inclusive=True,
            ),
            "D": interval_evidence_status(
                c3_primary["D_tribe_minus_kd_bridge"],
                0.0,
                inclusive=True,
            ),
            "J": interval_evidence_status(
                c3_primary["J_aligned_minus_twin_increment"],
                0.0,
                inclusive=True,
            ),
        },
    }


def classify_terminal(
    c1: Mapping[str, Any],
    c2: Mapping[str, Any],
    c3: Mapping[str, Any],
    c1_checks: Mapping[str, bool],
    c2_checks: Mapping[str, bool],
    c3_checks: Mapping[str, bool],
    validity_all: bool,
    inherited_all: bool,
    config: Mapping[str, Any],
) -> tuple[str, str, list[str]]:
    if not validity_all:
        label = "INCONCLUSIVE"
        return label, "one or more raw validity gates failed", [label]
    primary_nuisance = config["estimator"]["primary_nuisance"]
    c1_cell = c1["cells"][primary_nuisance]
    reference = float(config["inference"]["practical_reference_unique_r2"])
    if not c1_checks["A_endpoint_pass"]:
        if (
            c1_cell["A_aligned_above_nuisance"]["statistics"][
                "simultaneous_family_one_sided_t_upper95"
            ]
            < reference
        ):
            label = "NO PRACTICALLY RELEVANT LINEAR MEASURABILITY"
            return (
                label,
                "A does not pass and its simultaneous C1-family upper bound excludes +0.002",
                [label],
            )
        label = "INCONCLUSIVE"
        return label, "A does not pass and its familywise upper bound is unresolved", [label]
    if not c1_checks["Q_endpoint_pass"]:
        if (
            c1_cell["Q_aligned_minus_twin"]["statistics"][
                "simultaneous_family_one_sided_t_upper95"
            ]
            < reference
        ):
            label = "NO PRACTICALLY RELEVANT ADVANTAGE OVER THE FROZEN TWIN"
            return (
                label,
                "A passes; Q does not pass and its simultaneous C1-family upper bound excludes +0.002",
                [label],
            )
        label = "INCONCLUSIVE"
        return label, "A passes; Q does not pass and its familywise upper bound is unresolved", [label]
    if not inherited_all:
        label = "INCONCLUSIVE"
        return (
            label,
            "a required inherited E025 quality, target-direction, or movement gate failed",
            [label],
        )
    primary = c2["cells"][f"layer{config['estimator']['primary_layer']}"][primary_nuisance]["variance_weighted_total"]
    if not c2_checks["M_endpoint_pass"]:
        if (
            primary["M_absolute_tribe_extractability"]["statistics"][
                "simultaneous_family_one_sided_t_upper95"
            ]
            <= 0
        ):
            label = "NO MEASURABLE ABSOLUTE RETENTION"
            return (
                label,
                "M does not pass and its simultaneous C2-family upper bound excludes a positive value",
                [label],
            )
        label = "INCONCLUSIVE"
        return label, "M does not pass and its familywise upper bound is unresolved", [label]
    if not c2_checks["B_endpoint_pass"]:
        if (
            primary["B_tribe_minus_kd_increment"]["statistics"][
                "simultaneous_family_one_sided_t_upper95"
            ]
            <= 0
        ):
            label = "NO INCREMENTAL RETENTION OVER KD"
            return (
                label,
                "M passes; B does not pass and its simultaneous C2-family upper bound excludes a positive value",
                [label],
            )
        label = "INCONCLUSIVE"
        return label, "M passes; B does not pass and its familywise upper bound is unresolved", [label]
    primary_c3 = c3["cells"][f"layer{config['estimator']['primary_layer']}"][
        primary_nuisance
    ]
    for short, name in (
        ("O", "O_absolute_tribe_bridge"),
        ("D", "D_tribe_minus_kd_bridge"),
        ("J", "J_aligned_minus_twin_increment"),
    ):
        if c3_checks[f"{short}_endpoint_pass"]:
            continue
        if (
            primary_c3[name]["statistics"][
                "simultaneous_family_one_sided_t_upper95"
            ]
            <= 0
        ):
            label = {
                "O": "NO MEASURABLE ABSOLUTE PREDICTIVE OVERLAP",
                "D": "NO INCREMENTAL PREDICTIVE OVERLAP OVER KD",
                "J": "NO ALIGNED-ROW ADVANTAGE OVER THE FROZEN TWIN",
            }[short]
            return (
                label,
                f"all upstream endpoints pass; {short} does not pass and its simultaneous C3-family upper bound excludes a positive predictive bridge",
                [label],
            )
        label = "INCONCLUSIVE"
        return (
            label,
            f"all upstream endpoints pass; {short} does not pass and its familywise upper bound is unresolved",
            [label],
        )
    if not c3_checks["pass"]:
        raise ProtocolError("C3 global pass disagrees with ordered endpoint passes")
    label = "JOINT PASS / predictive overlap supported"
    return (
        label,
        "C1, C2, and C3 satisfy every frozen primary predictive rule",
        [label],
    )


def analyze_payload(
    payload: Mapping[str, Any],
    config: Mapping[str, Any],
    config_path: Path,
    raw_source: str,
    raw_sha256: str,
    *,
    verify_identity_files: bool,
    fixed_cache_identities: Mapping[tuple[int, str], tuple[str, str, str]],
) -> dict[str, Any]:
    expected_top = {
        "schema_version",
        "stage",
        "science_status",
        "created_at_utc",
        "identity",
        "design",
        "validity",
        "inherited_gates",
        "c1_rows",
        "c2_rows",
        "c3_rows",
        "resource_use",
    }
    expect_exact_keys(payload, expected_top, "raw payload")
    if payload["schema_version"] != RAW_SCHEMA:
        raise ProtocolError(f"raw schema must be {RAW_SCHEMA}")
    if payload["stage"] != "score" or payload["science_status"] != "RAW FOLD ROWS ONLY":
        raise ProtocolError("raw stage/science_status mismatch")
    created_at = validate_timestamp(payload["created_at_utc"])
    identity = require_mapping(payload["identity"], "identity")
    validate_identity(identity, config, config_path, verify_identity_files)
    validate_design(require_mapping(payload["design"], "design"), config)
    scoring_resource_use = validate_scoring_resource_use(
        payload["resource_use"], config
    )
    validity = validate_validity(payload["validity"])
    inherited = validate_inherited_gates(payload["inherited_gates"], config)
    c1_index = validate_c1_rows(payload["c1_rows"], config)
    c2_index = validate_c2_rows(payload["c2_rows"], config, fixed_cache_identities)
    c3_index = validate_c3_rows(
        payload["c3_rows"],
        config,
        fixed_cache_identities,
        c1_index,
        c2_index,
    )
    c1 = analyze_c1(c1_index, config)
    c2 = analyze_c2(c2_index, config)
    c3 = analyze_c3(c3_index, config)
    c1_checks = c1_pass_checks(c1, validity["all_pass"], config)
    c2_checks = c2_pass_checks(c2, validity["all_pass"], inherited["all_pass"], config)
    c3_checks = c3_pass_checks(
        c3,
        validity["all_pass"],
        c1_checks["pass"],
        c2_checks["pass"],
        config,
    )
    evidence_diagnostics = primary_evidence_diagnostics(c1, c2, c3, config)
    classification, reason, terminal_labels = classify_terminal(
        c1,
        c2,
        c3,
        c1_checks,
        c2_checks,
        c3_checks,
        validity["all_pass"],
        inherited["all_pass"],
        config,
    )
    return {
        "schema_version": ANALYSIS_SCHEMA,
        "experiment": "E030",
        "protocol_version": config["protocol_version"],
        "science_status": "mechanical frozen analysis; requires independent /interpret recomputation and Erfan confirmation before any changed verdict",
        "raw_created_at_utc": created_at,
        "source": {
            "raw_scores": raw_source,
            "raw_scores_sha256": raw_sha256,
            "config": repo_relative(config_path),
            "config_sha256": sha256_file(config_path),
            "analyzer": ANALYZER_PATH,
            "analyzer_sha256": sha256_file(Path(__file__).resolve()),
        },
        "validated_identity": copy.deepcopy(identity),
        "validity": validity,
        "scoring_resource_use": scoring_resource_use,
        "inherited_gates": inherited,
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "primary_pass_checks": {
            "C1": c1_checks,
            "C2": c2_checks,
            "C3": c3_checks,
        },
        "primary_evidence_diagnostics": evidence_diagnostics,
        "mechanical_terminal_classification": classification,
        "mechanical_terminal_labels": terminal_labels,
        "classification_reason": reason,
        "inferential_status": "enabled" if validity["all_pass"] else "suppressed_by_validity_gate_failure",
        "claim_boundary": (
            "A joint pass supports only cross-validated predictive overlap on the frozen E030 substrate. The composed "
            "coefficient path is not causal mediation, brain specificity, population generality, Package C reopening, "
            "or authority to retrain. Participant-level C3 claims are conditional on paired-seed D/J gates that support "
            "technical-realization stability, not biological replication. Layer 7, non-primary nuisance variants, and "
            "equal-coordinate summaries cannot rescue a primary layer-6 imageability-conditioned nonpass."
        ),
    }


def synthetic_digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def synthetic_fixed_cache_identities(
    config: Mapping[str, Any],
) -> dict[tuple[int, str], tuple[str, str, str]]:
    return {
        (int(seed), str(arm)): (
            f"{arm}:seed{seed}",
            synthetic_digest(f"weight:{arm}:{seed}"),
            synthetic_digest(f"cache:{arm}:{seed}"),
        )
        for seed in config["estimator"]["seeds"]
        for arm in config["estimator"]["arms"]
    }


def synthetic_design(config: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "uids": config["substrate"]["valid_uids"],
        "train_uids": config["substrate"]["train_uids"],
        "heldout_uids": config["substrate"]["heldout_uids"],
        "rois": config["substrate"]["rois"],
        "test_blocks": config["folds"]["test_blocks"],
        "nuisance_variants": list(config["estimator"]["nuisance_variants"]),
        "primary_nuisance": config["estimator"]["primary_nuisance"],
        "layers": [config["estimator"]["primary_layer"], config["estimator"]["sensitivity_layer"]],
        "primary_layer": config["estimator"]["primary_layer"],
        "sensitivity_layer": config["estimator"]["sensitivity_layer"],
        "arms": config["estimator"]["arms"],
        "seeds": config["estimator"]["seeds"],
        "pca_rank": config["estimator"]["pca_rank"],
        "ridge_alphas": config["estimator"]["ridge_alphas"],
        "coordinate_sst_floor": config["estimator"]["coordinate_sst_floor"],
        "target_dim": config["target"]["target_dim"],
        "bridge": copy.deepcopy(config["bridge"]),
    }


def synthetic_identity(config: Mapping[str, Any], config_path: Path) -> dict[str, Any]:
    source_record = lambda key: {
        "path": config["sources"][key]["path"],
        "sha256": config["sources"][key]["sha256"],
    }
    return {
        "protocol_version": config["protocol_version"],
        "config": {"path": repo_relative(config_path), "sha256": sha256_file(config_path)},
        "readiness": {"path": config["paths"]["readiness"], "sha256": synthetic_digest("readiness")},
        "bundle": {
            "path": config["paths"]["bundle_manifest"],
            "sha256": synthetic_digest("bundle-file"),
            "bundle_sha256": synthetic_digest("bundle-semantic"),
        },
        "design_manifest": {
            "path": config["paths"]["design_manifest"],
            "sha256": synthetic_digest("design-manifest"),
        },
        "acquisition_manifest": {"path": config["paths"]["acquisition_manifest"], "sha256": synthetic_digest("acquisition")},
        "runner": {"path": RUNNER_PATH, "sha256": synthetic_digest("runner")},
        "analyzer": {"path": ANALYZER_PATH, "sha256": sha256_file(Path(__file__).resolve())},
        "tuckute_csv": source_record("tuckute_csv"),
        "e025_manifest": source_record("e025_manifest"),
        "e025_extraction": source_record("e025_extraction"),
        "e025_analysis": source_record("e025_analysis"),
        "e025_nuisance": source_record("e025_nuisance"),
        "e025_participant_loader": source_record("e025_participant_loader"),
        "target": {
            "path": config["paths"]["target"],
            "sha256": synthetic_digest("synthetic-target-file"),
            "targets_array_sha256": synthetic_digest("synthetic-target-array"),
        },
        "standardization": {
            "npz_path": config["paths"]["standardization"],
            "npz_sha256": synthetic_digest("synthetic-standardization-file"),
            "manifest_path": config["paths"]["standardization_manifest"],
            "manifest_sha256": synthetic_digest("synthetic-standardization-manifest"),
        },
        "twin_permutation": {
            "path": config["paths"]["twin_permutation"],
            "sha256": synthetic_digest("synthetic-twin-file"),
            "array_sha256": synthetic_digest("synthetic-twin-array"),
        },
        "ordered_item_sha256": config["substrate"]["ordered_item_sha256"],
        "ordered_text_sha256": config["substrate"]["ordered_text_sha256"],
        "vertex_index_sha256": config["sources"]["e016_heldout_target"]["vertex_index_sha256"],
        "tribe_runtime": frozen_tribe_runtime_identity(
            config, verify_live=False
        ),
        "scoring_runtime": {
            "launcher": config["scoring_runtime"]["launcher"],
            "versions": {
                "python": config["scoring_runtime"]["python_version"],
                "numpy": config["scoring_runtime"]["numpy_version"],
                "scipy": config["scoring_runtime"]["scipy_version"],
                "scikit_learn": config["scoring_runtime"]["scikit_learn_version"],
            },
            "pyproject": copy.deepcopy(config["scoring_runtime"]["pyproject"]),
            "uv_lock": copy.deepcopy(config["scoring_runtime"]["uv_lock"]),
            "blas_threads": config["compute_ceiling"]["blas_threads"],
        },
    }


def make_synthetic_payload(
    config: Mapping[str, Any],
    config_path: Path,
    *,
    c1_aligned: float = 0.020,
    c1_twin: float = 0.004,
    c2_tribe: float = 0.030,
    c2_kd: float = 0.008,
    c3_tribe_aligned: float = 0.040,
    c3_kd_aligned: float = 0.010,
    c3_tribe_twin: float = 0.012,
    c3_kd_twin: float = 0.008,
) -> dict[str, Any]:
    c1_rows: list[dict[str, Any]] = []
    roi_offsets = np.asarray([-2, -1, 0, 1, 2], dtype=np.float64) * 1e-6
    train = set(config["substrate"]["train_uids"])
    for uid_index, uid in enumerate(config["substrate"]["valid_uids"]):
        for nuisance_index, nuisance in enumerate(config["estimator"]["nuisance_variants"]):
            for fold, (start, stop) in enumerate(config["folds"]["test_blocks"]):
                nuisance_value = 0.010 + nuisance_index * 0.001 + fold * 1e-5
                nuisance_roi = nuisance_value + roi_offsets
                variation = uid_index * 2e-5 + fold * 1e-6
                for representation, base_unique in (("aligned", c1_aligned), ("twin", c1_twin)):
                    unique_roi = base_unique + variation + roi_offsets * 0.1
                    full_roi = nuisance_roi + unique_roi
                    c1_rows.append(
                        {
                            "uid": uid,
                            "participant_split": "train" if uid in train else "heldout",
                            "nuisance_variant": nuisance,
                            "fold": fold,
                            "test_start": start,
                            "test_stop_exclusive": stop,
                            "test_count": stop - start,
                            "representation": representation,
                            "target_pca_basis_sha256": synthetic_digest(
                                f"target-pca-basis:{fold}"
                            ),
                            "static_pca_basis_sha256": synthetic_digest(
                                f"static-pca-basis:{fold}"
                            ),
                            "alpha_nuisance": 10.0,
                            "alpha_full": 100.0,
                            "r2_nuisance_by_roi": nuisance_roi.tolist(),
                            "r2_full_by_roi": full_roi.tolist(),
                            "unique_r2_by_roi": unique_roi.tolist(),
                            "r2_nuisance": float(np.mean(nuisance_roi)),
                            "r2_full": float(np.mean(full_roi)),
                            "unique_r2": float(np.mean(unique_roi)),
                        }
                    )

    c2_rows: list[dict[str, Any]] = []
    for seed in config["estimator"]["seeds"]:
        for arm in config["estimator"]["arms"]:
            for layer in (config["estimator"]["primary_layer"], config["estimator"]["sensitivity_layer"]):
                for nuisance_index, nuisance in enumerate(config["estimator"]["nuisance_variants"]):
                    for fold, (start, stop) in enumerate(config["folds"]["test_blocks"]):
                        nuisance_r2 = 0.015 + nuisance_index * 0.001 + fold * 1e-5
                        base_v = c2_tribe if arm == "tribe_mse" else c2_kd
                        unique = base_v + seed * 2e-5 + fold * 1e-6 + (layer - 6) * 1e-5
                        full_r2 = nuisance_r2 + unique
                        sst_total = 1000.0 + fold
                        eq_nuisance = nuisance_r2 * 0.9
                        eq_unique = unique * 0.9
                        c2_rows.append(
                            {
                                "seed": seed,
                                "arm": arm,
                                "layer": layer,
                                "nuisance_variant": nuisance,
                                "fold": fold,
                                "test_start": start,
                                "test_stop_exclusive": stop,
                                "test_count": stop - start,
                                "cache_key": f"{arm}:seed{seed}",
                                "weight_sha256": synthetic_digest(f"weight:{arm}:{seed}"),
                                "representation_cache_sha256": synthetic_digest(f"cache:{arm}:{seed}"),
                                "student_pca_basis_sha256": synthetic_digest(
                                    f"student-pca-basis:{seed}:{arm}:{layer}:{fold}"
                                ),
                                "coordinate_count": config["target"]["target_dim"],
                                "coordinate_sst_min": 1.0 + fold * 0.01,
                                "coordinate_sst_floor": config["estimator"]["coordinate_sst_floor"],
                                "coordinates_below_floor": 0,
                                "alpha_nuisance": 10.0,
                                "alpha_full": 100.0,
                                "nuisance_sse_total": (1.0 - nuisance_r2) * sst_total,
                                "full_sse_total": (1.0 - full_r2) * sst_total,
                                "sst_total": sst_total,
                                "r2_nuisance_total": nuisance_r2,
                                "r2_full_total": full_r2,
                                "unique_r2_total": unique,
                                "r2_nuisance_equal_coordinate": eq_nuisance,
                                "r2_full_equal_coordinate": eq_nuisance + eq_unique,
                                "unique_r2_equal_coordinate": eq_unique,
                            }
                        )
    c3_rows: list[dict[str, Any]] = []
    for uid_index, uid in enumerate(config["substrate"]["valid_uids"]):
        for seed in config["estimator"]["seeds"]:
            for arm in config["estimator"]["arms"]:
                for layer in (
                    config["estimator"]["primary_layer"],
                    config["estimator"]["sensitivity_layer"],
                ):
                    for nuisance_index, nuisance in enumerate(
                        config["estimator"]["nuisance_variants"]
                    ):
                        for fold, (start, stop) in enumerate(
                            config["folds"]["test_blocks"]
                        ):
                            nuisance_value = (
                                0.010 + nuisance_index * 0.001 + fold * 1e-5
                            )
                            base_roi = nuisance_value + roi_offsets
                            for alignment in config["bridge"]["alignments"]:
                                lookup = {
                                    ("tribe_mse", "aligned"): c3_tribe_aligned,
                                    ("kd_only", "aligned"): c3_kd_aligned,
                                    ("tribe_mse", "twin"): c3_tribe_twin,
                                    ("kd_only", "twin"): c3_kd_twin,
                                }
                                bridge_value = (
                                    lookup[(arm, alignment)]
                                    + uid_index * 2e-5
                                    + seed * 2e-6
                                    + fold * 1e-7
                                )
                                unique_roi = (
                                    bridge_value + roi_offsets * 0.1
                                )
                                bridge_roi = base_roi + unique_roi
                                c3_rows.append(
                                    {
                                        "uid": uid,
                                        "participant_split": (
                                            "train" if uid in train else "heldout"
                                        ),
                                        "seed": seed,
                                        "arm": arm,
                                        "layer": layer,
                                        "nuisance_variant": nuisance,
                                        "fold": fold,
                                        "representation": alignment,
                                        "test_start": start,
                                        "test_stop_exclusive": stop,
                                        "test_count": stop - start,
                                        "target_pca_basis_sha256": synthetic_digest(
                                            f"target-pca-basis:{fold}"
                                        ),
                                        "student_pca_basis_sha256": synthetic_digest(
                                            f"student-pca-basis:{seed}:{arm}:{layer}:{fold}"
                                        ),
                                        "static_pca_basis_sha256": synthetic_digest(
                                            f"static-pca-basis:{fold}"
                                        ),
                                        "cache_key": f"{arm}:seed{seed}",
                                        "weight_sha256": synthetic_digest(
                                            f"weight:{arm}:{seed}"
                                        ),
                                        "representation_cache_sha256": synthetic_digest(
                                            f"cache:{arm}:{seed}"
                                        ),
                                        "target_component_count": config[
                                            "bridge"
                                        ]["target_pca_rank"],
                                        "student_component_count": config[
                                            "bridge"
                                        ]["student_pca_rank"],
                                        "alpha_response_nuisance": 10.0,
                                        "alpha_response_full": 100.0,
                                        "alpha_target_full": 1000.0,
                                        "r2_base_by_roi": base_roi.tolist(),
                                        "r2_bridge_by_roi": bridge_roi.tolist(),
                                        "bridge_unique_r2_by_roi": unique_roi.tolist(),
                                        "r2_base": float(np.mean(base_roi)),
                                        "r2_bridge": float(np.mean(bridge_roi)),
                                        "bridge_unique_r2": float(
                                            np.mean(unique_roi)
                                        ),
                                        "response_target_coefficient_l2": (
                                            1.0
                                            + uid_index * 0.01
                                            + nuisance_index * 0.001
                                            + fold * 0.0001
                                            + (0.00001 if alignment == "twin" else 0.0)
                                        ),
                                        "student_target_coefficient_l2": (
                                            2.0
                                            + seed * 0.01
                                            + (0.1 if arm == "tribe_mse" else 0.0)
                                            + layer * 0.001
                                            + nuisance_index * 0.0001
                                            + fold * 0.00001
                                            + (0.000001 if alignment == "twin" else 0.0)
                                        ),
                                        "target_pc_contribution_l2": (
                                            3.0
                                            + seed * 0.01
                                            + (0.1 if arm == "tribe_mse" else 0.0)
                                            + layer * 0.001
                                            + nuisance_index * 0.0001
                                            + fold * 0.00001
                                            + (0.000001 if alignment == "twin" else 0.0)
                                        ),
                                        "composed_contribution_l2": (
                                            4.0 + uid_index * 0.01 + seed * 0.001
                                        ),
                                    }
                                )
    return {
        "schema_version": RAW_SCHEMA,
        "stage": "score",
        "science_status": "RAW FOLD ROWS ONLY",
        "created_at_utc": "2026-07-21T00:00:00Z",
        "identity": synthetic_identity(config, config_path),
        "design": synthetic_design(config),
        "validity": {
            "inputs_hash_valid": True,
            "inputs_finite": True,
            "participant_grid_valid": True,
            "c1_grid_complete": True,
            "c2_grid_complete": True,
            "c3_grid_complete": True,
            "bridge_contributions_finite": True,
            "target_pca_basis_reuse_valid": True,
            "student_pca_basis_reuse_valid": True,
            "coordinate_floor_valid": True,
            "inherited_gates_valid": True,
            "all_pass": True,
        },
        "inherited_gates": {
            "quality_equivalence": True,
            "target_direction": True,
            "representation_movement": True,
            "source_extraction_sha256": config["sources"]["e025_extraction"]["sha256"],
        },
        "c1_rows": c1_rows,
        "c2_rows": c2_rows,
        "c3_rows": c3_rows,
        "resource_use": {
            "stage": "scoring",
            "cpu_budget_seconds": int(
                float(config["compute_ceiling"]["scoring_cpu_hours"]) * 3600
            ),
            "rlimit_cpu_soft_seconds": int(
                float(config["compute_ceiling"]["scoring_cpu_hours"]) * 3600
            ),
            "address_space_limit_bytes": int(
                float(config["compute_ceiling"]["scoring_ram_gb"]) * 1024**3
            ),
            "peak_rss_limit_kib": int(
                float(config["compute_ceiling"]["scoring_ram_gb"])
                * 1024
                * 1024
            ),
            "retained_storage_limit_bytes": retained_storage_limit_bytes(config),
            "cpu_limit_mechanism": config["compute_ceiling"][
                "cpu_limit_mechanism"
            ],
            "memory_limit_mechanism": config["compute_ceiling"][
                "memory_limit_mechanism"
            ],
            "rss_watchdog_poll_seconds": config["compute_ceiling"][
                "rss_watchdog_poll_seconds"
            ],
            "retained_storage_scope": config["compute_ceiling"][
                "retained_storage_scope"
            ],
            "elapsed_wall_seconds": 1.0,
            "elapsed_cpu_seconds": 1.0,
            "peak_rss_kib": 1,
            "retained_output_dir_bytes_before_write": 0,
            "retained_output_dir_bytes_projected_after_write": 1,
        },
    }


def expect_protocol_error(function: Any, label: str) -> None:
    try:
        function()
    except ProtocolError:
        return
    raise AssertionError(f"selftest expected ProtocolError: {label}")


def run_selftest(config: Mapping[str, Any], config_path: Path, fixture_path: Path | None) -> dict[str, Any]:
    fixture = make_synthetic_payload(config, config_path)
    cache_identities = synthetic_fixed_cache_identities(config)
    temporary_directory: tempfile.TemporaryDirectory[str] | None = None
    if fixture_path is None:
        temporary_directory = tempfile.TemporaryDirectory(prefix="e030-analyzer-selftest-")
        target = Path(temporary_directory.name) / "synthetic_raw_scores.json"
    else:
        target = fixture_path.resolve()
        for forbidden in (ROOT / config["paths"]["raw_scores"], ROOT / config["paths"]["analysis"]):
            if target == forbidden.resolve():
                raise ProtocolError("selftest fixture may not overwrite a configured E030 outcome path")
    try:
        atomic_json_write(target, fixture)
        loaded = strict_json_load(target)
        joint = analyze_payload(
            loaded,
            config,
            config_path,
            str(target),
            sha256_file(target),
            verify_identity_files=False,
            fixed_cache_identities=cache_identities,
        )
        if (
            joint["mechanical_terminal_classification"]
            != "JOINT PASS / predictive overlap supported"
        ):
            raise AssertionError("synthetic positive fixture did not produce JOINT PASS")
        if not joint["primary_pass_checks"]["C3"]["pass"]:
            raise AssertionError("synthetic positive fixture did not pass C3")
        sign_flip = joint["c2"]["cells"]["layer6"][config["estimator"]["primary_nuisance"]]["variance_weighted_total"]["B_tribe_minus_kd_increment"]["exact_magnitude_sign_flip"]
        if sign_flip["enumeration_count"] != 64 or not close(sign_flip["two_sided_p"], 2 / 64):
            raise AssertionError("exact 2^6 sign-flip selftest failed")
        positive_checks = joint["primary_pass_checks"]
        if not all(
            positive_checks[stage][f"{endpoint}_endpoint_pass"]
            for stage, endpoints in (
                ("C1", ("A", "Q")),
                ("C2", ("M", "B")),
                ("C3", ("O", "D", "J")),
            )
            for endpoint in endpoints
        ):
            raise AssertionError("positive fixture did not pass every ordered endpoint subset")
        c3_primary_positive = joint["c3"]["cells"][
            f"layer{config['estimator']['primary_layer']}"
        ][config["estimator"]["primary_nuisance"]]
        for metric_name in (
            "D_tribe_minus_kd_bridge",
            "J_aligned_minus_twin_increment",
        ):
            seed_stability = c3_primary_positive[metric_name]["seed_sensitivity"]
            seed_flip = seed_stability["exact_magnitude_sign_flip"]
            if (
                len(seed_stability["by_seed_grand_mean"]) != 6
                or not all_positive(seed_stability["by_seed_grand_mean"].values())
                or seed_flip["enumeration_count"] != 64
                or not close(seed_flip["two_sided_p"], 2 / 64)
            ):
                raise AssertionError("C3 paired-seed D/J stability gate failed")

        boundary_c1 = copy.deepcopy(joint["c1"])
        boundary_c2 = copy.deepcopy(joint["c2"])
        boundary_c3 = copy.deepcopy(joint["c3"])
        boundary_c1_checks = copy.deepcopy(joint["primary_pass_checks"]["C1"])
        boundary_c2_checks = copy.deepcopy(joint["primary_pass_checks"]["C2"])
        boundary_c3_checks = copy.deepcopy(joint["primary_pass_checks"]["C3"])
        boundary_c1_checks["pass"] = False
        boundary_c1_checks["A_endpoint_pass"] = False
        primary_c1 = boundary_c1["cells"][config["estimator"]["primary_nuisance"]]
        primary_c1["A_aligned_above_nuisance"]["statistics"]["two_sided_t_ci95"] = [-0.001, 0.0015]
        primary_c1["A_aligned_above_nuisance"]["statistics"]["one_sided_t_upper95"] = 0.001
        primary_c1["A_aligned_above_nuisance"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = 0.0015
        primary_c1["Q_aligned_minus_twin"]["statistics"]["two_sided_t_ci95"] = [-0.005, 0.012]
        primary_c1["Q_aligned_minus_twin"]["statistics"]["one_sided_t_upper95"] = 0.010
        boundary_class, _, boundary_labels = classify_terminal(
            boundary_c1,
            boundary_c2,
            boundary_c3,
            boundary_c1_checks,
            boundary_c2_checks,
            boundary_c3_checks,
            True,
            True,
            config,
        )
        if boundary_labels != ["NO PRACTICALLY RELEVANT LINEAR MEASURABILITY"]:
            raise AssertionError("C1-A boundary did not retain its separate terminal label")

        positive_nonpass_c1 = copy.deepcopy(joint["primary_pass_checks"]["C1"])
        positive_nonpass_c1["pass"] = False
        positive_nonpass_c1["A_endpoint_pass"] = False
        positive_nonpass_class, _, _ = classify_terminal(
            joint["c1"],
            joint["c2"],
            joint["c3"],
            positive_nonpass_c1,
            joint["primary_pass_checks"]["C2"],
            joint["primary_pass_checks"]["C3"],
            True,
            True,
            config,
        )
        if positive_nonpass_class != "INCONCLUSIVE":
            raise AssertionError("C1 rule nonpass without exclusion did not remain INCONCLUSIVE")

        boundary_c2_checks["pass"] = False
        boundary_c2_checks["M_endpoint_pass"] = False
        primary_c2 = boundary_c2["cells"][f"layer{config['estimator']['primary_layer']}"][
            config["estimator"]["primary_nuisance"]
        ]["variance_weighted_total"]
        primary_c2["M_absolute_tribe_extractability"]["statistics"]["two_sided_t_ci95"] = [-0.002, 0.001]
        primary_c2["M_absolute_tribe_extractability"]["statistics"]["one_sided_t_upper95"] = -0.001
        primary_c2["M_absolute_tribe_extractability"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = -0.0005
        primary_c2["B_tribe_minus_kd_increment"]["statistics"]["two_sided_t_ci95"] = [-0.010, 0.020]
        primary_c2["B_tribe_minus_kd_increment"]["statistics"]["one_sided_t_upper95"] = 0.010
        boundary_class, _, boundary_labels = classify_terminal(
            joint["c1"],
            boundary_c2,
            boundary_c3,
            joint["primary_pass_checks"]["C1"],
            boundary_c2_checks,
            boundary_c3_checks,
            True,
            True,
            config,
        )
        if boundary_labels != ["NO MEASURABLE ABSOLUTE RETENTION"]:
            raise AssertionError("C2-M boundary did not retain its separate terminal label")

        positive_nonpass_c2 = copy.deepcopy(joint["primary_pass_checks"]["C2"])
        positive_nonpass_c2["pass"] = False
        positive_nonpass_c2["M_endpoint_pass"] = False
        positive_nonpass_class, _, _ = classify_terminal(
            joint["c1"],
            joint["c2"],
            joint["c3"],
            joint["primary_pass_checks"]["C1"],
            positive_nonpass_c2,
            joint["primary_pass_checks"]["C3"],
            True,
            True,
            config,
        )
        if positive_nonpass_class != "INCONCLUSIVE":
            raise AssertionError("C2 rule nonpass without exclusion did not remain INCONCLUSIVE")

        q_only_c1 = copy.deepcopy(joint["c1"])
        q_only_checks = copy.deepcopy(joint["primary_pass_checks"]["C1"])
        q_only_checks["pass"] = False
        q_only_checks["Q_endpoint_pass"] = False
        q_only_c1["cells"][config["estimator"]["primary_nuisance"]][
            "Q_aligned_minus_twin"
        ]["statistics"]["simultaneous_family_one_sided_t_upper95"] = 0.001
        _, _, q_only_labels = classify_terminal(
            q_only_c1,
            joint["c2"],
            joint["c3"],
            q_only_checks,
            joint["primary_pass_checks"]["C2"],
            joint["primary_pass_checks"]["C3"],
            True,
            True,
            config,
        )
        if q_only_labels != [
            "NO PRACTICALLY RELEVANT ADVANTAGE OVER THE FROZEN TWIN"
        ]:
            raise AssertionError("C1-Q did not retain its separate terminal label")

        b_only_c2 = copy.deepcopy(joint["c2"])
        b_only_checks = copy.deepcopy(joint["primary_pass_checks"]["C2"])
        b_only_checks["pass"] = False
        b_only_checks["B_endpoint_pass"] = False
        b_only_c2["cells"][f"layer{config['estimator']['primary_layer']}"][
            config["estimator"]["primary_nuisance"]
        ]["variance_weighted_total"]["B_tribe_minus_kd_increment"][
            "statistics"
        ]["simultaneous_family_one_sided_t_upper95"] = -0.001
        _, _, b_only_labels = classify_terminal(
            joint["c1"],
            b_only_c2,
            joint["c3"],
            joint["primary_pass_checks"]["C1"],
            b_only_checks,
            joint["primary_pass_checks"]["C3"],
            True,
            True,
            config,
        )
        if b_only_labels != ["NO INCREMENTAL RETENTION OVER KD"]:
            raise AssertionError("C2-B did not retain its separate terminal label")

        c3_names = {
            "O": "O_absolute_tribe_bridge",
            "D": "D_tribe_minus_kd_bridge",
            "J": "J_aligned_minus_twin_increment",
        }
        for short, metric_name in c3_names.items():
            component_c3 = copy.deepcopy(joint["c3"])
            component_checks = copy.deepcopy(joint["primary_pass_checks"]["C3"])
            component_checks["pass"] = False
            component_checks[f"{short}_endpoint_pass"] = False
            component_c3["cells"][
                f"layer{config['estimator']['primary_layer']}"
            ][config["estimator"]["primary_nuisance"]][metric_name][
                "statistics"
            ]["simultaneous_family_one_sided_t_upper95"] = -0.001
            _, _, component_labels = classify_terminal(
                joint["c1"],
                joint["c2"],
                component_c3,
                joint["primary_pass_checks"]["C1"],
                joint["primary_pass_checks"]["C2"],
                component_checks,
                True,
                True,
                config,
            )
            expected_label = [
                {
                    "O": "NO MEASURABLE ABSOLUTE PREDICTIVE OVERLAP",
                    "D": "NO INCREMENTAL PREDICTIVE OVERLAP OVER KD",
                    "J": "NO ALIGNED-ROW ADVANTAGE OVER THE FROZEN TWIN",
                }[short]
            ]
            if component_labels != expected_label:
                raise AssertionError(
                    f"C3-{short} did not retain its separate terminal label"
                )

        positive_nonpass_c3 = copy.deepcopy(joint["primary_pass_checks"]["C3"])
        positive_nonpass_c3["pass"] = False
        positive_nonpass_c3["O_endpoint_pass"] = False
        positive_nonpass_class, _, _ = classify_terminal(
            joint["c1"],
            joint["c2"],
            joint["c3"],
            joint["primary_pass_checks"]["C1"],
            joint["primary_pass_checks"]["C2"],
            positive_nonpass_c3,
            True,
            True,
            config,
        )
        if positive_nonpass_class != "INCONCLUSIVE":
            raise AssertionError("C3 rule nonpass without exclusion did not remain INCONCLUSIVE")

        diagnostic_families = joint["primary_evidence_diagnostics"]
        for stage, endpoints in (
            ("C1", ("A", "Q")),
            ("C2", ("M", "B")),
            ("C3", ("O", "D", "J")),
        ):
            for endpoint in endpoints:
                diagnostic = diagnostic_families[stage][endpoint]
                if (
                    diagnostic["simultaneous_family_size"]
                    != config["inference"]["terminal_family_sizes"][stage]
                    or diagnostic["simultaneous_family_one_sided_t_upper95"]
                    < diagnostic["marginal_one_sided_t_upper95"]
                ):
                    raise AssertionError("familywise upper-bound diagnostic is invalid")

        marginal_only_c1 = copy.deepcopy(joint["c1"])
        marginal_only_c1_checks = copy.deepcopy(
            joint["primary_pass_checks"]["C1"]
        )
        marginal_only_c1_checks["pass"] = False
        marginal_only_c1_checks["A_endpoint_pass"] = False
        a_statistics = marginal_only_c1["cells"][
            config["estimator"]["primary_nuisance"]
        ]["A_aligned_above_nuisance"]["statistics"]
        a_statistics["one_sided_t_upper95"] = 0.001
        a_statistics["simultaneous_family_one_sided_t_upper95"] = 0.003
        marginal_only_class, _, _ = classify_terminal(
            marginal_only_c1,
            joint["c2"],
            joint["c3"],
            marginal_only_c1_checks,
            joint["primary_pass_checks"]["C2"],
            joint["primary_pass_checks"]["C3"],
            True,
            True,
            config,
        )
        if marginal_only_class != "INCONCLUSIVE":
            raise AssertionError("marginal C1 bound incorrectly issued a terminal label")

        ordered_c1 = copy.deepcopy(marginal_only_c1)
        ordered_c1_checks = copy.deepcopy(marginal_only_c1_checks)
        ordered_c1_checks["Q_endpoint_pass"] = False
        ordered_c1["cells"][config["estimator"]["primary_nuisance"]][
            "Q_aligned_minus_twin"
        ]["statistics"]["simultaneous_family_one_sided_t_upper95"] = 0.001
        ordered_class, _, _ = classify_terminal(
            ordered_c1,
            joint["c2"],
            joint["c3"],
            ordered_c1_checks,
            joint["primary_pass_checks"]["C2"],
            joint["primary_pass_checks"]["C3"],
            True,
            True,
            config,
        )
        if ordered_class != "INCONCLUSIVE":
            raise AssertionError("Q was labeled before unresolved A")

        ordered_c2 = copy.deepcopy(joint["c2"])
        ordered_c2_checks = copy.deepcopy(joint["primary_pass_checks"]["C2"])
        ordered_c2_checks["pass"] = False
        ordered_c2_checks["M_endpoint_pass"] = False
        ordered_c2_checks["B_endpoint_pass"] = False
        ordered_c2_primary = ordered_c2["cells"][
            f"layer{config['estimator']['primary_layer']}"
        ][config["estimator"]["primary_nuisance"]]["variance_weighted_total"]
        ordered_c2_primary["M_absolute_tribe_extractability"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = 0.001
        ordered_c2_primary["B_tribe_minus_kd_increment"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = -0.001
        ordered_class, _, _ = classify_terminal(
            joint["c1"],
            ordered_c2,
            joint["c3"],
            joint["primary_pass_checks"]["C1"],
            ordered_c2_checks,
            joint["primary_pass_checks"]["C3"],
            True,
            True,
            config,
        )
        if ordered_class != "INCONCLUSIVE":
            raise AssertionError("B was labeled before unresolved M")

        ordered_c3 = copy.deepcopy(joint["c3"])
        ordered_c3_checks = copy.deepcopy(joint["primary_pass_checks"]["C3"])
        ordered_c3_checks["pass"] = False
        ordered_c3_checks["O_endpoint_pass"] = False
        ordered_c3_checks["D_endpoint_pass"] = False
        ordered_c3_checks["J_endpoint_pass"] = False
        ordered_c3_primary = ordered_c3["cells"][
            f"layer{config['estimator']['primary_layer']}"
        ][config["estimator"]["primary_nuisance"]]
        ordered_c3_primary["O_absolute_tribe_bridge"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = 0.001
        ordered_c3_primary["D_tribe_minus_kd_bridge"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = -0.001
        ordered_c3_primary["J_aligned_minus_twin_increment"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = -0.001
        ordered_class, _, _ = classify_terminal(
            joint["c1"],
            joint["c2"],
            ordered_c3,
            joint["primary_pass_checks"]["C1"],
            joint["primary_pass_checks"]["C2"],
            ordered_c3_checks,
            True,
            True,
            config,
        )
        if ordered_class != "INCONCLUSIVE":
            raise AssertionError("D/J were labeled before unresolved O")

        ordered_c3_checks["O_endpoint_pass"] = True
        ordered_c3_primary["O_absolute_tribe_bridge"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = 0.01
        ordered_c3_primary["D_tribe_minus_kd_bridge"]["statistics"][
            "simultaneous_family_one_sided_t_upper95"
        ] = 0.001
        ordered_class, _, _ = classify_terminal(
            joint["c1"],
            joint["c2"],
            ordered_c3,
            joint["primary_pass_checks"]["C1"],
            joint["primary_pass_checks"]["C2"],
            ordered_c3_checks,
            True,
            True,
            config,
        )
        if ordered_class != "INCONCLUSIVE":
            raise AssertionError("J was labeled before unresolved D")

        proxy_fixture = make_synthetic_payload(config, config_path, c1_aligned=-0.003, c1_twin=0.001)
        proxy = analyze_payload(proxy_fixture, config, config_path, "synthetic-proxy", synthetic_digest("proxy"), verify_identity_files=False, fixed_cache_identities=cache_identities)
        if proxy["mechanical_terminal_labels"] != [
            "NO PRACTICALLY RELEVANT LINEAR MEASURABILITY"
        ]:
            raise AssertionError("synthetic C1 failure did not stop at A")

        retention_fixture = make_synthetic_payload(config, config_path, c2_tribe=-0.003, c2_kd=0.002)
        retention = analyze_payload(retention_fixture, config, config_path, "synthetic-retention", synthetic_digest("retention"), verify_identity_files=False, fixed_cache_identities=cache_identities)
        if retention["mechanical_terminal_labels"] != [
            "NO MEASURABLE ABSOLUTE RETENTION"
        ]:
            raise AssertionError("synthetic C2 failure did not stop at M")

        invalid_fixture = copy.deepcopy(fixture)
        invalid_fixture["validity"]["inputs_finite"] = False
        invalid_fixture["validity"]["all_pass"] = False
        invalid = analyze_payload(invalid_fixture, config, config_path, "synthetic-invalid", synthetic_digest("invalid"), verify_identity_files=False, fixed_cache_identities=cache_identities)
        if (
            invalid["mechanical_terminal_classification"]
            != "INCONCLUSIVE"
        ):
            raise AssertionError("failed validity gate did not classify as INCONCLUSIVE")

        missing_row = copy.deepcopy(fixture)
        missing_row["c1_rows"].pop()
        expect_protocol_error(
            lambda: analyze_payload(missing_row, config, config_path, "synthetic-missing", synthetic_digest("missing"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "missing C1 cell",
        )
        arithmetic = copy.deepcopy(fixture)
        arithmetic["c2_rows"][0]["unique_r2_total"] += 0.01
        expect_protocol_error(
            lambda: analyze_payload(arithmetic, config, config_path, "synthetic-arithmetic", synthetic_digest("arithmetic"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "C2 arithmetic mismatch",
        )
        missing_c3 = copy.deepcopy(fixture)
        missing_c3["c3_rows"].pop()
        expect_protocol_error(
            lambda: analyze_payload(missing_c3, config, config_path, "synthetic-missing-c3", synthetic_digest("missing-c3"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "missing C3 cell",
        )
        bridge_arithmetic = copy.deepcopy(fixture)
        bridge_arithmetic["c3_rows"][0]["bridge_unique_r2"] += 0.01
        expect_protocol_error(
            lambda: analyze_payload(bridge_arithmetic, config, config_path, "synthetic-bridge-arithmetic", synthetic_digest("bridge-arithmetic"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "C3 arithmetic mismatch",
        )
        basis_identity = copy.deepcopy(fixture)
        basis_identity["c3_rows"][0]["student_pca_basis_sha256"] = (
            synthetic_digest("wrong-student-pca-basis")
        )
        expect_protocol_error(
            lambda: analyze_payload(basis_identity, config, config_path, "synthetic-basis-identity", synthetic_digest("basis-identity"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "alignment-shared PCA basis identity mismatch",
        )
        c2_nuisance_basis = copy.deepcopy(fixture)
        reference_c2 = c2_nuisance_basis["c2_rows"][0]
        matching_c2 = next(
            row
            for row in c2_nuisance_basis["c2_rows"][1:]
            if (
                row["seed"],
                row["arm"],
                row["layer"],
                row["fold"],
            )
            == (
                reference_c2["seed"],
                reference_c2["arm"],
                reference_c2["layer"],
                reference_c2["fold"],
            )
            and row["nuisance_variant"]
            != reference_c2["nuisance_variant"]
        )
        matching_c2["student_pca_basis_sha256"] = synthetic_digest(
            "wrong-c2-nuisance-student-basis"
        )
        expect_protocol_error(
            lambda: analyze_payload(c2_nuisance_basis, config, config_path, "synthetic-c2-nuisance-basis", synthetic_digest("c2-nuisance-basis"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "C2 student PCA basis differs across nuisances",
        )
        c2_c3_basis = copy.deepcopy(fixture)
        for row in c2_c3_basis["c3_rows"]:
            if (
                row["seed"],
                row["arm"],
                row["layer"],
                row["fold"],
            ) == (0, config["estimator"]["arms"][0], config["estimator"]["primary_layer"], 0):
                row["student_pca_basis_sha256"] = synthetic_digest(
                    "wrong-c3-student-basis"
                )
        expect_protocol_error(
            lambda: analyze_payload(c2_c3_basis, config, config_path, "synthetic-c2-c3-basis", synthetic_digest("c2-c3-basis"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "C2/C3 student PCA basis mismatch",
        )
        resource_ceiling = copy.deepcopy(fixture)
        resource_ceiling["resource_use"][
            "retained_output_dir_bytes_projected_after_write"
        ] = retained_storage_limit_bytes(config) + 1
        expect_protocol_error(
            lambda: analyze_payload(resource_ceiling, config, config_path, "synthetic-resource-ceiling", synthetic_digest("resource-ceiling"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "scoring retained-storage ceiling fail closed",
        )
        runtime_digest = copy.deepcopy(fixture)
        runtime_digest["identity"]["tribe_runtime"]["identity"][
            "git_head"
        ] = synthetic_digest("wrong-runtime-head")[:40]
        expect_protocol_error(
            lambda: analyze_payload(runtime_digest, config, config_path, "synthetic-runtime-digest", synthetic_digest("runtime-digest"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "TRIBE runtime semantic digest fail closed",
        )
        identity = copy.deepcopy(fixture)
        identity["identity"]["ordered_text_sha256"] = synthetic_digest("wrong text")
        expect_protocol_error(
            lambda: analyze_payload(identity, config, config_path, "synthetic-identity", synthetic_digest("identity"), verify_identity_files=False, fixed_cache_identities=cache_identities),
            "identity mismatch",
        )
        return {
            "status": "PASS",
            "fixture": str(target),
            "fixture_persisted": fixture_path is not None,
            "tests": [
                "strict synthetic JSON round trip",
                "joint positive recovery",
                "exact 2^6 magnitude-preserving two-sided sign-flip",
                "C3 paired-seed D/J exact stability gates",
                "ordered A/Q/M/B/O/D/J endpoint subsets",
                "Bonferroni simultaneous family bounds dominate marginals",
                "marginal-only exclusion cannot issue a terminal label",
                "unresolved upstream endpoint blocks downstream labels",
                "C1 one-excluded/one-unresolved boundary classification",
                "C1 positive-bound rule nonpass remains inconclusive",
                "C2 one-excluded/one-unresolved boundary classification",
                "C2 positive-bound rule nonpass remains inconclusive",
                "separate C1-A and C1-Q terminal labels",
                "separate C2-M and C2-B terminal labels",
                "separate C3-O, C3-D, and C3-J terminal labels",
                "C3 positive-bound rule nonpass remains inconclusive",
                "synthetic C1 component classification",
                "synthetic C2 component classification",
                "validity-gate inconclusive classification",
                "missing-grid fail closed",
                "arithmetic fail closed",
                "missing-C3-grid fail closed",
                "C3 arithmetic fail closed",
                "alignment-shared PCA basis identity fail closed",
                "C2 nuisance-shared student PCA basis identity fail closed",
                "C2/C3 student PCA basis identity fail closed",
                "scoring resource ceiling fail closed",
                "TRIBE runtime semantic digest fail closed",
                "identity fail closed",
            ],
        }
    finally:
        if temporary_directory is not None:
            temporary_directory.cleanup()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CANONICAL_CONFIG)
    parser.add_argument("--raw", type=Path, help="Frozen raw score JSON; must equal the configured path")
    parser.add_argument("--out", type=Path, help="Analysis JSON; must equal the configured path")
    parser.add_argument("--selftest", action="store_true", help="Analyze synthetic fixtures only; never reads --raw")
    parser.add_argument("--selftest-fixture", type=Path, help="Optional path at which to retain the synthetic raw fixture")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = args.config.resolve()
    if config_path != CANONICAL_CONFIG.resolve():
        raise ProtocolError(f"only the canonical config is allowed: {CANONICAL_CONFIG}")
    config = strict_json_load(config_path)
    validate_config(config)
    if args.selftest:
        report = run_selftest(config, config_path, args.selftest_fixture)
        print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
        return
    if args.selftest_fixture is not None:
        raise ProtocolError("--selftest-fixture requires --selftest")
    raw_path = (args.raw or (ROOT / config["paths"]["raw_scores"])).resolve()
    out_path = (args.out or (ROOT / config["paths"]["analysis"])).resolve()
    if raw_path != (ROOT / config["paths"]["raw_scores"]).resolve():
        raise ProtocolError("--raw must equal the canonical configured raw-score path")
    if out_path != (ROOT / config["paths"]["analysis"]).resolve():
        raise ProtocolError("--out must equal the canonical configured analysis path")
    if out_path.exists():
        raise ProtocolError(f"frozen analyzer output already exists; refusing a second analysis: {out_path}")
    stage_started_wall = time.perf_counter()
    stage_started_cpu = process_cpu_seconds()
    analysis_limits = apply_analysis_resource_limits(config)
    rss_stop, rss_thread = start_rss_watchdog(
        int(analysis_limits["peak_rss_limit_kib"]),
        float(analysis_limits["rss_watchdog_poll_seconds"]),
    )
    storage_before = enforce_retained_storage(config)
    payload = strict_json_load(raw_path)
    extraction_path = resolve_repo_path(
        config["sources"]["e025_extraction"]["path"],
        "config.sources.e025_extraction.path",
    )
    cache_identities = expected_representation_identities(
        config, strict_json_load(extraction_path)
    )
    analysis = analyze_payload(
        payload,
        config,
        config_path,
        repo_relative(raw_path),
        sha256_file(raw_path),
        verify_identity_files=True,
        fixed_cache_identities=cache_identities,
    )
    analysis["resource_use"] = {
        **measured_analysis_resource_use(
            analysis_limits,
            started_wall=stage_started_wall,
            started_cpu=stage_started_cpu,
        ),
        "retained_output_dir_bytes_before_write": int(storage_before),
        "retained_output_dir_bytes_projected_after_write": 0,
    }
    for _ in range(8):
        projected = int(storage_before + len(pretty_json_bytes(analysis)))
        if (
            analysis["resource_use"][
                "retained_output_dir_bytes_projected_after_write"
            ]
            == projected
        ):
            break
        analysis["resource_use"][
            "retained_output_dir_bytes_projected_after_write"
        ] = projected
    enforce_retained_storage(
        config, projected_extra_bytes=len(pretty_json_bytes(analysis))
    )
    atomic_json_write(out_path, analysis)
    retained_after = enforce_retained_storage(config)
    rss_stop.set()
    rss_thread.join(timeout=1.0)
    print(
        json.dumps(
            {
                "out": repo_relative(out_path),
                "out_sha256": sha256_file(out_path),
                "mechanical_terminal_classification": analysis["mechanical_terminal_classification"],
                "science_status": analysis["science_status"],
                "retained_output_dir_bytes_after_write": int(retained_after),
            },
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
