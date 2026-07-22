#!/usr/bin/env python3
"""Prospective E030 exact-substrate transport diagnostic.

The executable is deliberately staged. Manifest, selftest, benchmark,
smoke-replay, and standardizer do not open new E030 outcomes. Target requires
the frozen readiness seal but still cannot read participant responses. Score
is the only stage allowed to open participant responses, and it writes raw
fold-level values without a scientific classification.

The target-worker entry point exists only because TRIBE uses an isolated
environment. Invoke it through the guarded target stage.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import resource
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable

FROZEN_BLAS_THREADS = "8"
for _thread_variable in (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ[_thread_variable] = FROZEN_BLAS_THREADS

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/e030_exact_substrate_transport.json"
E_RECORD = ROOT / "docs/experiments/E030_exact-substrate-transport-diagnostic.md"
ANALYZER = ROOT / "scripts/e030_analyze_exact_substrate.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path, chunk_bytes: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_bytes), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_array(value: np.ndarray) -> str:
    return sha256_bytes(np.ascontiguousarray(value).tobytes(order="C"))


def ordered_text_sha(texts: Iterable[str]) -> str:
    return sha256_bytes(("\n".join(texts) + "\n").encode("utf-8"))


def ordered_item_sha(item_ids: np.ndarray) -> str:
    payload = json.dumps(
        np.asarray(item_ids, dtype=np.int64).tolist(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256_bytes(payload)


def resolve(path_value: str | Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_config(path: Path) -> tuple[dict[str, Any], str]:
    path = path.resolve()
    config = load_json(path)
    if config.get("experiment") != "E030":
        raise ValueError(f"not an E030 config: {path}")
    if config.get("protocol_version") != "e030-exact-substrate-transport.v2":
        raise ValueError("unexpected E030 protocol version")
    return config, sha256_file(path)


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(canonical_json_bytes(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def atomic_write_npy(path: Path, value: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            np.save(handle, value, allow_pickle=False)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def atomic_write_npz(path: Path, **arrays: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".npz", dir=path.parent
    )
    os.close(fd)
    try:
        np.savez_compressed(temporary, **arrays)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def file_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "size_bytes": int(path.stat().st_size),
        "sha256": sha256_file(path),
    }


def require_exact_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{label} key mismatch: missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )


def require_current_file_record(
    record: Any, expected_path: Path, label: str
) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError(f"{label} must be a file-record object")
    require_exact_keys(record, {"path", "size_bytes", "sha256"}, label)
    expected = expected_path.resolve()
    observed = resolve(str(record["path"])).resolve()
    if observed != expected:
        raise ValueError(f"{label} path mismatch: {observed} != {expected}")
    if not observed.is_file():
        raise FileNotFoundError(f"{label} is missing: {observed}")
    current = file_record(observed)
    if current != {**record, "path": str(observed)}:
        raise ValueError(f"{label} file identity is stale")
    return current


def directory_regular_file_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    total = 0
    for candidate in path.rglob("*"):
        if candidate.is_file() and not candidate.is_symlink():
            total += int(candidate.stat().st_size)
    return total


def retained_storage_limit_bytes(config: dict[str, Any]) -> int:
    return int(float(config["compute_ceiling"]["retained_storage_gb"]) * 1024**3)


def enforce_retained_storage(
    config: dict[str, Any], *, projected_extra_bytes: int = 0
) -> int:
    output_dir = path_for(config, "output_dir")
    observed = directory_regular_file_bytes(output_dir)
    projected = observed + int(projected_extra_bytes)
    ceiling = retained_storage_limit_bytes(config)
    if projected > ceiling:
        raise RuntimeError(
            f"E030 retained-output ceiling exceeded: {projected} > {ceiling} bytes"
        )
    return observed


def process_cpu_seconds() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return float(usage.ru_utime + usage.ru_stime)


def current_rss_kib() -> int:
    status = Path("/proc/self/status")
    if not status.is_file():
        raise RuntimeError("Linux /proc/self/status is required for RSS enforcement")
    for line in status.read_text(encoding="utf-8").splitlines():
        if line.startswith("VmRSS:"):
            fields = line.split()
            if len(fields) != 3 or fields[2] != "kB":
                break
            return int(fields[1])
    raise RuntimeError("cannot parse VmRSS from /proc/self/status")


def start_rss_watchdog(
    limit_kib: int, poll_seconds: float,
) -> tuple[threading.Event, threading.Thread]:
    initial_rss = current_rss_kib()
    if initial_rss > limit_kib:
        raise RuntimeError(
            f"E030 RSS already exceeds ceiling: {initial_rss} > {limit_kib} KiB"
        )
    stop = threading.Event()

    def monitor() -> None:
        while not stop.wait(poll_seconds):
            observed = current_rss_kib()
            if observed > limit_kib:
                message = (
                    f"E030 RSS watchdog exceeded: {observed} > {limit_kib} KiB\n"
                ).encode("utf-8")
                os.write(2, message)
                os._exit(97)

    thread = threading.Thread(
        target=monitor, name="e030-rss-watchdog", daemon=True
    )
    thread.start()
    return stop, thread


def apply_stage_resource_limits(
    config: dict[str, Any], stage: str
) -> dict[str, Any]:
    if stage not in {"scoring", "analysis"}:
        raise ValueError(f"unknown resource-limited E030 stage: {stage}")
    ceiling = config["compute_ceiling"]
    cpu_hours = float(ceiling[f"{stage}_cpu_hours"])
    ram_gb = float(ceiling[f"{stage}_ram_gb"])
    if float(ceiling["rss_watchdog_poll_seconds"]) <= 0:
        raise ValueError("RSS watchdog polling interval must be positive")
    cpu_budget_seconds = max(1, int(math.floor(cpu_hours * 3600.0)))
    cpu_soft = max(1, int(math.ceil(process_cpu_seconds())) + cpu_budget_seconds)
    current_soft, current_hard = resource.getrlimit(resource.RLIMIT_CPU)
    if current_hard != resource.RLIM_INFINITY:
        cpu_soft = min(cpu_soft, int(current_hard))
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_soft, current_hard))

    address_space_bytes = int(ram_gb * 1024**3)
    as_soft, as_hard = resource.getrlimit(resource.RLIMIT_AS)
    if as_hard != resource.RLIM_INFINITY:
        address_space_bytes = min(address_space_bytes, int(as_hard))
    resource.setrlimit(resource.RLIMIT_AS, (address_space_bytes, as_hard))
    return {
        "stage": stage,
        "cpu_budget_seconds": cpu_budget_seconds,
        "rlimit_cpu_soft_seconds": int(cpu_soft),
        "address_space_limit_bytes": int(address_space_bytes),
        "peak_rss_limit_kib": int(ram_gb * 1024 * 1024),
        "retained_storage_limit_bytes": retained_storage_limit_bytes(config),
        "cpu_limit_mechanism": ceiling["cpu_limit_mechanism"],
        "memory_limit_mechanism": ceiling["memory_limit_mechanism"],
        "rss_watchdog_poll_seconds": float(
            ceiling["rss_watchdog_poll_seconds"]
        ),
        "retained_storage_scope": ceiling["retained_storage_scope"],
    }


def measured_resource_use(
    limits: dict[str, Any], *, started_wall: float, started_cpu: float
) -> dict[str, Any]:
    peak_rss_kib = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if peak_rss_kib > int(limits["peak_rss_limit_kib"]):
        raise RuntimeError(
            f"E030 {limits['stage']} peak RSS exceeded its ceiling: "
            f"{peak_rss_kib} > {limits['peak_rss_limit_kib']} KiB"
        )
    return {
        **limits,
        "elapsed_wall_seconds": float(time.perf_counter() - started_wall),
        "elapsed_cpu_seconds": float(process_cpu_seconds() - started_cpu),
        "peak_rss_kib": peak_rss_kib,
    }


def require_hash(path: Path, expected: str, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"{label} missing: {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(
            f"{label} SHA-256 mismatch: expected {expected}, got {actual}"
        )
    return {
        "path": str(path),
        "size_bytes": int(path.stat().st_size),
        "sha256": actual,
    }


def source_record(config: dict[str, Any], name: str) -> dict[str, Any]:
    record = config["sources"][name]
    return require_hash(resolve(record["path"]), record["sha256"], name)


def require_current_frozen_source_record(
    record: dict[str, Any], frozen: dict[str, Any], label: str
) -> dict[str, Any]:
    require_exact_keys(
        record,
        {"path", "size_bytes", "sha256"},
        f"{label} record",
    )
    live_record = require_hash(
        resolve(frozen["path"]), frozen["sha256"], label
    )
    if record != live_record:
        raise ValueError(f"{label} identity is stale")
    return live_record


def path_for(config: dict[str, Any], name: str) -> Path:
    return resolve(config["paths"][name])


def configure_threads(config: dict[str, Any]) -> None:
    count = str(int(config["compute_ceiling"]["blas_threads"]))
    if count != FROZEN_BLAS_THREADS:
        raise ValueError(
            "config BLAS thread count differs from pre-import frozen value"
        )
    for key in (
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        os.environ[key] = count


def validate_scoring_runtime(config: dict[str, Any]) -> dict[str, Any]:
    import scipy
    import sklearn

    runtime = config["scoring_runtime"]
    versions = {
        "python": ".".join(map(str, sys.version_info[:3])),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
    }
    expected = {
        "python": runtime["python_version"],
        "numpy": runtime["numpy_version"],
        "scipy": runtime["scipy_version"],
        "scikit_learn": runtime["scikit_learn_version"],
    }
    if versions != expected:
        raise ValueError(f"scoring runtime mismatch: {versions} != {expected}")
    project = require_hash(
        resolve(runtime["pyproject"]["path"]),
        runtime["pyproject"]["sha256"],
        "pyproject",
    )
    lock = require_hash(
        resolve(runtime["uv_lock"]["path"]),
        runtime["uv_lock"]["sha256"],
        "uv.lock",
    )
    return {
        "launcher": runtime["launcher"],
        "versions": versions,
        "pyproject": {
            "path": project["path"],
            "sha256": project["sha256"],
        },
        "uv_lock": {
            "path": lock["path"],
            "sha256": lock["sha256"],
        },
        "blas_threads": int(config["compute_ceiling"]["blas_threads"]),
    }


def bundle_manifest(config_path: Path) -> dict[str, Any]:
    files = {
        "config": config_path.resolve(),
        "e_record": E_RECORD,
        "runner": Path(__file__).resolve(),
        "analyzer": ANALYZER,
    }
    missing = [name for name, path in files.items() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"bundle files missing: {missing}")
    records = {
        name: {
            "path": str(path),
            "sha256": sha256_file(path),
            "size_bytes": int(path.stat().st_size),
        }
        for name, path in sorted(files.items())
    }
    digest = sha256_bytes(
        canonical_json_bytes(
            {name: record["sha256"] for name, record in records.items()}
        )
    )
    return {
        "schema_version": "e030-bundle.v1",
        "files": records,
        "bundle_sha256": digest,
    }


def contiguous_folds(config: dict[str, Any]) -> list[tuple[np.ndarray, np.ndarray]]:
    n_items = int(config["substrate"]["n_items"])
    blocks = config["folds"]["test_blocks"]
    folds: list[tuple[np.ndarray, np.ndarray]] = []
    all_indices = np.arange(n_items, dtype=np.int64)
    coverage = np.zeros(n_items, dtype=np.int64)
    for expected_fold, block in enumerate(blocks):
        if len(block) != 2:
            raise ValueError(f"invalid test block {expected_fold}: {block}")
        start, stop = (int(block[0]), int(block[1]))
        test = np.arange(start, stop, dtype=np.int64)
        train = np.concatenate((all_indices[:start], all_indices[stop:]))
        coverage[test] += 1
        folds.append((train, test))
    if len(folds) != int(config["folds"]["count"]):
        raise ValueError("fold count differs from config")
    if not np.array_equal(coverage, np.ones(n_items, dtype=np.int64)):
        raise ValueError("test blocks do not partition the item rows exactly")
    return folds


def sattolo_permutation(
    config: dict[str, Any],
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    n_items = int(config["substrate"]["n_items"])
    text_hash = config["substrate"]["ordered_text_sha256"]
    key = config["twin"]["key"]
    permutation = np.full(n_items, -1, dtype=np.int64)
    block_records: list[dict[str, Any]] = []
    for fold, (_, test) in enumerate(contiguous_folds(config)):
        seed_material = f"{key}|text={text_hash}|block={fold}".encode("utf-8")
        seed_hex = sha256_bytes(seed_material)
        seed = int.from_bytes(bytes.fromhex(seed_hex)[:8], "little")
        rng = np.random.Generator(np.random.PCG64(seed))
        local = test.copy()
        for index in range(len(local) - 1, 0, -1):
            swap = int(rng.integers(0, index))
            local[index], local[swap] = local[swap], local[index]
        if np.any(local == test):
            raise AssertionError(f"Sattolo fixed point in block {fold}")
        if not np.array_equal(np.sort(local), test):
            raise AssertionError(f"Sattolo row multiset changed in block {fold}")
        permutation[test] = local
        block_records.append(
            {
                "fold": fold,
                "start": int(test[0]),
                "stop_exclusive": int(test[-1]) + 1,
                "seed_sha256": seed_hex,
                "permutation_sha256": sha256_array(local.astype("<i8")),
            }
        )
    if np.any(permutation < 0) or np.any(
        permutation == np.arange(n_items, dtype=np.int64)
    ):
        raise AssertionError("invalid whole-dataset Sattolo permutation")
    return permutation, block_records


def stimulus_table(config: dict[str, Any]) -> tuple[np.ndarray, list[str]]:
    import pandas as pd

    csv_path = resolve(config["sources"]["tuckute_csv"]["path"])
    frame = pd.read_csv(csv_path, usecols=["cond", "item_id", "sentence"])
    selected = frame.loc[
        frame["cond"].astype(str) == str(config["substrate"]["condition"]),
        ["item_id", "sentence"],
    ].copy()
    if selected.empty:
        raise ValueError("no rows found for the frozen Tuckute condition")
    selected["item_id"] = selected["item_id"].astype(np.int64)
    per_item = selected.groupby("item_id", sort=True, dropna=False)["sentence"]
    if (per_item.nunique(dropna=False) != 1).any():
        raise ValueError("a Tuckute item has nonunique sentence identity")
    ordered = (
        selected.drop_duplicates(subset=["item_id"], keep="first")
        .sort_values("item_id")
        .reset_index(drop=True)
    )
    item_ids = ordered["item_id"].to_numpy(dtype=np.int64)
    texts = [str(value) for value in ordered["sentence"].tolist()]
    expected = np.arange(
        int(config["substrate"]["item_id_start"]),
        int(config["substrate"]["item_id_stop_exclusive"]),
        dtype=np.int64,
    )
    if not np.array_equal(item_ids, expected):
        raise ValueError("Tuckute item IDs are not the frozen contiguous range")
    if len(set(texts)) != len(texts):
        raise ValueError("Tuckute texts are not unique")
    for index, text in enumerate(texts):
        if not text or text != text.strip() or "\n" in text or "\r" in text:
            raise ValueError(f"unsafe newline-corpus text at row {index}")
    if ordered_item_sha(item_ids) != config["substrate"]["ordered_item_sha256"]:
        raise ValueError("ordered Tuckute item hash mismatch")
    if ordered_text_sha(texts) != config["substrate"]["ordered_text_sha256"]:
        raise ValueError("ordered Tuckute text hash mismatch")
    return item_ids, texts


def run_manifest(config_path: Path) -> dict[str, Any]:
    config, config_hash = load_config(config_path)
    source_names = (
        "tuckute_csv",
        "e025_manifest",
        "e025_extraction",
        "e025_analysis",
        "e025_nuisance",
        "e025_participant_loader",
        "e016_train_target",
        "e016_heldout_target",
        "target_generator",
    )
    sources = {name: source_record(config, name) for name in source_names}
    item_ids, texts = stimulus_table(config)
    folds = contiguous_folds(config)
    permutation, block_records = sattolo_permutation(config)

    corpus_path = path_for(config, "corpus")
    atomic_write_text(corpus_path, "\n".join(texts) + "\n")
    if sha256_file(corpus_path) != config["substrate"]["ordered_text_sha256"]:
        raise AssertionError("written corpus hash differs from frozen text hash")

    fold_arrays: dict[str, np.ndarray] = {}
    fold_records: list[dict[str, Any]] = []
    for fold, (train, test) in enumerate(folds):
        fold_arrays[f"fold_{fold}_train"] = train
        fold_arrays[f"fold_{fold}_test"] = test
        fold_records.append(
            {
                "fold": fold,
                "train_count": int(len(train)),
                "test_count": int(len(test)),
                "train_sha256": sha256_array(train.astype("<i8")),
                "test_sha256": sha256_array(test.astype("<i8")),
            }
        )
    folds_path = path_for(config, "folds")
    atomic_write_npz(folds_path, **fold_arrays)
    twin_path = path_for(config, "twin_permutation")
    atomic_write_npy(twin_path, permutation)

    manifest = {
        "schema_version": "e030-design-manifest.v1",
        "science_status": (
            "OUTCOME SEALED: stimulus identity only; response_target was not "
            "selected, parsed, summarized, or scored"
        ),
        "config": {"path": str(config_path.resolve()), "sha256": config_hash},
        "scoring_runtime": validate_scoring_runtime(config),
        "csv_usecols": ["cond", "item_id", "sentence"],
        "participant_loader_called": False,
        "sources": sources,
        "substrate": {
            "condition": config["substrate"]["condition"],
            "n_items": int(len(texts)),
            "item_id_start": int(item_ids[0]),
            "item_id_stop_exclusive": int(item_ids[-1]) + 1,
            "ordered_item_sha256": ordered_item_sha(item_ids),
            "ordered_text_sha256": ordered_text_sha(texts),
            "generator_item_mapping": "item_id = item_index + 1",
        },
        "folds": {
            "method": "contiguous",
            "records": fold_records,
            "artifact": file_record(folds_path),
        },
        "twin": {
            "algorithm": config["twin"]["algorithm"],
            "key": config["twin"]["key"],
            "zero_fixed_points": bool(
                np.all(permutation != np.arange(len(permutation)))
            ),
            "blocks": block_records,
            "semantic_sha256": sha256_array(permutation.astype("<i8")),
            "artifact": file_record(twin_path),
        },
        "corpus": file_record(corpus_path),
    }
    manifest_path = path_for(config, "design_manifest")
    atomic_write_json(manifest_path, manifest)
    return manifest


def validate_design_manifest(
    config_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    config, config_hash = load_config(config_path)
    path = path_for(config, "design_manifest")
    manifest = load_json(path)
    require_exact_keys(
        manifest,
        {
            "schema_version",
            "science_status",
            "config",
            "scoring_runtime",
            "csv_usecols",
            "participant_loader_called",
            "sources",
            "substrate",
            "folds",
            "twin",
            "corpus",
        },
        "E030 design manifest",
    )
    if manifest.get("schema_version") != "e030-design-manifest.v1":
        raise ValueError("unexpected E030 design-manifest version")
    require_exact_keys(manifest["config"], {"path", "sha256"}, "design config")
    if (
        resolve(manifest["config"]["path"]).resolve() != config_path.resolve()
        or manifest["config"]["sha256"] != config_hash
    ):
        raise ValueError("design manifest config identity mismatch")
    frozen_scoring = config["scoring_runtime"]
    frozen_project = require_hash(
        resolve(frozen_scoring["pyproject"]["path"]),
        frozen_scoring["pyproject"]["sha256"],
        "design scoring-runtime pyproject",
    )
    frozen_lock = require_hash(
        resolve(frozen_scoring["uv_lock"]["path"]),
        frozen_scoring["uv_lock"]["sha256"],
        "design scoring-runtime uv.lock",
    )
    expected_scoring_runtime = {
        "launcher": frozen_scoring["launcher"],
        "versions": {
            "python": frozen_scoring["python_version"],
            "numpy": frozen_scoring["numpy_version"],
            "scipy": frozen_scoring["scipy_version"],
            "scikit_learn": frozen_scoring["scikit_learn_version"],
        },
        "pyproject": {
            "path": frozen_project["path"],
            "sha256": frozen_project["sha256"],
        },
        "uv_lock": {
            "path": frozen_lock["path"],
            "sha256": frozen_lock["sha256"],
        },
        "blas_threads": int(config["compute_ceiling"]["blas_threads"]),
    }
    if manifest["scoring_runtime"] != expected_scoring_runtime:
        raise ValueError("design manifest scoring-runtime identity mismatch")
    if manifest["csv_usecols"] != ["cond", "item_id", "sentence"]:
        raise ValueError("design manifest CSV projection changed")
    if manifest["participant_loader_called"] is not False:
        raise ValueError("design manifest opened participant responses")
    expected_source_names = {
        "tuckute_csv",
        "e025_manifest",
        "e025_extraction",
        "e025_analysis",
        "e025_nuisance",
        "e025_participant_loader",
        "e016_train_target",
        "e016_heldout_target",
        "target_generator",
    }
    require_exact_keys(manifest["sources"], expected_source_names, "design sources")
    for name in expected_source_names:
        require_current_frozen_source_record(
            manifest["sources"][name],
            config["sources"][name],
            f"design source {name}",
        )
    expected_substrate = {
        "condition": config["substrate"]["condition"],
        "n_items": int(config["substrate"]["n_items"]),
        "item_id_start": int(config["substrate"]["item_id_start"]),
        "item_id_stop_exclusive": int(
            config["substrate"]["item_id_stop_exclusive"]
        ),
        "ordered_item_sha256": config["substrate"]["ordered_item_sha256"],
        "ordered_text_sha256": config["substrate"]["ordered_text_sha256"],
        "generator_item_mapping": "item_id = item_index + 1",
    }
    if manifest["substrate"] != expected_substrate:
        raise ValueError("design manifest substrate identity mismatch")
    require_hash(
        path_for(config, "corpus"),
        config["substrate"]["ordered_text_sha256"],
        "E030 corpus",
    )
    require_current_file_record(
        manifest["corpus"], path_for(config, "corpus"), "design corpus"
    )
    folds_manifest = manifest["folds"]
    require_exact_keys(folds_manifest, {"method", "records", "artifact"}, "design folds")
    if folds_manifest["method"] != config["folds"]["method"]:
        raise ValueError("design fold method mismatch")
    require_current_file_record(
        folds_manifest["artifact"], path_for(config, "folds"), "design folds artifact"
    )
    expected_folds = contiguous_folds(config)
    expected_fold_records = []
    with np.load(path_for(config, "folds"), allow_pickle=False) as cache:
        expected_members = {
            f"fold_{fold}_{split}"
            for fold in range(len(expected_folds))
            for split in ("train", "test")
        }
        if set(cache.files) != expected_members:
            raise ValueError("stored fold artifact member set mismatch")
        for fold, (train, test) in enumerate(expected_folds):
            if not np.array_equal(cache[f"fold_{fold}_train"], train) or not np.array_equal(
                cache[f"fold_{fold}_test"], test
            ):
                raise ValueError(f"stored fold artifact differs at fold {fold}")
            expected_fold_records.append(
                {
                    "fold": fold,
                    "train_count": int(len(train)),
                    "test_count": int(len(test)),
                    "train_sha256": sha256_array(train.astype("<i8")),
                    "test_sha256": sha256_array(test.astype("<i8")),
                }
            )
    if folds_manifest["records"] != expected_fold_records:
        raise ValueError("design fold records differ from frozen folds")
    twin_manifest = manifest["twin"]
    require_exact_keys(
        twin_manifest,
        {"algorithm", "key", "zero_fixed_points", "blocks", "semantic_sha256", "artifact"},
        "design twin",
    )
    require_current_file_record(
        twin_manifest["artifact"],
        path_for(config, "twin_permutation"),
        "design twin artifact",
    )
    permutation = np.load(path_for(config, "twin_permutation"), allow_pickle=False)
    expected, expected_blocks = sattolo_permutation(config)
    if not np.array_equal(permutation, expected):
        raise ValueError("stored Sattolo twin differs from frozen algorithm")
    if twin_manifest != {
        "algorithm": config["twin"]["algorithm"],
        "key": config["twin"]["key"],
        "zero_fixed_points": True,
        "blocks": expected_blocks,
        "semantic_sha256": sha256_array(expected.astype("<i8")),
        "artifact": twin_manifest["artifact"],
    }:
        raise ValueError("design twin metadata differs from frozen algorithm")
    return config, manifest, sha256_file(path)


def runtime_manifest(config: dict[str, Any]) -> dict[str, Any]:
    runtime = config["runtime"]
    checkout = resolve(runtime["tribe_checkout"])
    python = resolve(runtime["python"])
    if not checkout.is_dir() or not python.is_file():
        raise FileNotFoundError("TRIBE checkout or isolated Python is missing")

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()
    if head != runtime["tribe_git_head"]:
        raise ValueError(f"TRIBE HEAD mismatch: {head}")

    diff = subprocess.run(
        ["git", "diff", "--binary", "--", "tribev2/grids/defaults.py"],
        cwd=checkout,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    diff_hash = sha256_bytes(diff)
    if diff_hash != runtime["tribe_tracked_diff_sha256"]:
        raise ValueError("TRIBE tracked runtime diff mismatch")

    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=checkout,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    status_hash = sha256_bytes(status)
    if status_hash != runtime["tribe_status_sha256"]:
        raise ValueError("TRIBE checkout status differs from frozen status")

    version = subprocess.run(
        [str(python), "--version"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ).stdout.strip()
    if version != f"Python {runtime['python_version']}":
        raise ValueError(f"TRIBE Python mismatch: {version}")

    freeze = subprocess.run(
        [str(python), *runtime["sorted_pip_freeze_command"]],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout
    freeze_lines = sorted(line.strip() for line in freeze.splitlines() if line.strip())
    freeze_bytes = ("\n".join(freeze_lines) + "\n").encode("utf-8")
    if len(freeze_lines) != int(runtime["sorted_pip_freeze_line_count"]):
        raise ValueError("TRIBE environment package count mismatch")
    if sha256_bytes(freeze_bytes) != runtime["sorted_pip_freeze_sha256"]:
        raise ValueError("TRIBE environment freeze mismatch")

    checkpoint = require_hash(
        Path(runtime["tribe_checkpoint"]["path"]),
        runtime["tribe_checkpoint"]["sha256"],
        "TRIBE checkpoint",
    )
    shards = [
        require_hash(Path(row["path"]), row["sha256"], f"Llama shard {index}")
        for index, row in enumerate(runtime["llama_shards"])
    ]
    identity = {
        "tribe_checkout": str(checkout),
        "git_head": head,
        "tracked_diff_sha256": diff_hash,
        "status_sha256": status_hash,
        "python": str(python),
        "python_version": version,
        "sorted_pip_freeze_sha256": sha256_bytes(freeze_bytes),
        "sorted_pip_freeze_line_count": len(freeze_lines),
        "hf_home": runtime["hf_home"],
        "tribe_snapshot": runtime["tribe_snapshot"],
        "tribe_checkpoint": checkpoint,
        "llama_snapshot": runtime["llama_snapshot"],
        "llama_shards": shards,
    }
    return {
        "schema_version": "e030-tribe-runtime.v1",
        "identity": identity,
        "semantic_sha256": sha256_bytes(canonical_json_bytes(identity)),
    }


def semantic_target_hashes(path: Path, allow_pickle: bool) -> dict[str, str]:
    with np.load(path, allow_pickle=allow_pickle) as cache:
        texts = [str(value) for value in cache["texts"].tolist()]
        return {
            "targets": sha256_array(cache["targets"]),
            "texts": ordered_text_sha(texts),
            "item_indices": sha256_array(
                cache["item_indices"].astype("<i8", copy=False)
            ),
            "vertex_index": sha256_array(
                cache["vertex_index"].astype("<i8", copy=False)
            ),
            "segment_counts": sha256_array(cache["segment_counts"]),
        }


def read_target_metadata(path: Path, allow_pickle: bool = False) -> dict[str, Any]:
    with np.load(path, allow_pickle=allow_pickle) as cache:
        key = "metadata_json" if "metadata_json" in cache.files else "metadata"
        return json.loads(str(cache[key].item()))


def run_smoke_replay(config_path: Path, gpu: str) -> dict[str, Any]:
    config, design, design_hash = validate_design_manifest(config_path)
    config_hash = design["config"]["sha256"]
    runtime = runtime_manifest(config)
    smoke = config["smoke_replay"]
    reference = require_hash(
        resolve(smoke["reference_npz"]["path"]),
        smoke["reference_npz"]["sha256"],
        "E016 retained smoke NPZ",
    )
    reference_sidecar = require_hash(
        resolve(smoke["reference_sidecar"]["path"]),
        smoke["reference_sidecar"]["sha256"],
        "E016 retained smoke sidecar",
    )
    corpus = require_hash(
        resolve(smoke["corpus"]["path"]),
        smoke["corpus"]["sha256"],
        "E016 smoke corpus",
    )
    generator = source_record(config, "target_generator")
    expected_hashes = smoke["semantic_sha256"]
    retained_hashes = semantic_target_hashes(
        Path(reference["path"]), allow_pickle=True
    )
    if retained_hashes != expected_hashes:
        raise ValueError("retained E016 smoke semantic hashes changed")

    replay_path = path_for(config, "smoke_replay")
    replay_path.parent.mkdir(parents=True, exist_ok=True)
    log_path = replay_path.with_suffix(".log")
    checkout = resolve(config["runtime"]["tribe_checkout"])
    python = resolve(config["runtime"]["python"])
    with tempfile.TemporaryDirectory(
        prefix=".e030-smoke.", dir=replay_path.parent
    ) as temporary:
        temporary_path = Path(temporary) / "replay.npz"
        command = [
            str(python),
            str(resolve(config["sources"]["target_generator"]["path"])),
            "--split",
            "heldout",
            "--corpus",
            str(resolve(smoke["corpus"]["path"])),
            "--start",
            "0",
            "--limit",
            str(smoke["n_items"]),
            "--batch-items",
            str(smoke["batch_items"]),
            "--features",
            "text",
            "--event-mode",
            "synthetic-text",
            "--target-dim",
            str(smoke["target_dim"]),
            "--word-duration",
            str(config["target"]["word_duration"]),
            "--word-gap",
            str(config["target"]["word_gap"]),
            "--min-duration",
            str(config["target"]["min_duration"]),
            "--out",
            str(temporary_path),
        ]
        environment = os.environ.copy()
        environment.update(
            {
                "CUDA_VISIBLE_DEVICES": str(gpu),
                "HF_HOME": config["runtime"]["hf_home"],
                "HF_HUB_OFFLINE": "1",
                "TRANSFORMERS_OFFLINE": "1",
            }
        )
        started = time.perf_counter()
        with log_path.open("wb") as log:
            subprocess.run(
                command,
                cwd=checkout,
                env=environment,
                check=True,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
        elapsed = time.perf_counter() - started
        actual_hashes = semantic_target_hashes(
            temporary_path, allow_pickle=False
        )
        if actual_hashes != expected_hashes:
            raise ValueError(
                f"TRIBE smoke semantic mismatch: {actual_hashes}"
            )
        retained_metadata = read_target_metadata(
            Path(reference["path"]), allow_pickle=True
        )
        replay_metadata = read_target_metadata(temporary_path)
        stable_keys = (
            "split",
            "start",
            "n_items",
            "features",
            "event_mode",
            "target_dim",
            "tr",
            "word_duration",
            "word_gap",
            "min_duration",
            "config_update",
        )
        stable_retained = {
            key: retained_metadata[key] for key in stable_keys
        }
        stable_replay = {key: replay_metadata[key] for key in stable_keys}
        if stable_retained != stable_replay:
            raise ValueError("TRIBE smoke stable metadata mismatch")
        os.replace(temporary_path, replay_path)

    report = {
        "schema_version": "e030-smoke-replay.v1",
        "science_status": (
            "OUTCOME SEALED: WikiText runtime-identity replay only; no "
            "Tuckute file or participant response was opened"
        ),
        "pass": True,
        "config_sha256": config_hash,
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "design_manifest_sha256": design_hash,
        "runtime": runtime,
        "generator": generator,
        "reference": reference,
        "reference_sidecar": reference_sidecar,
        "corpus": corpus,
        "semantic_sha256": actual_hashes,
        "stable_metadata": stable_replay,
        "replay": file_record(replay_path),
        "log": file_record(log_path),
        "elapsed_seconds": float(elapsed),
        "gpu_selector": str(gpu),
    }
    atomic_write_json(path_for(config, "smoke_report"), report)
    return report


def run_standardizer(config_path: Path) -> dict[str, Any]:
    config, _, design_hash = validate_design_manifest(config_path)
    validate_scoring_runtime(config)
    source = source_record(config, "e016_train_target")
    source_path = Path(source["path"])
    expected_shape = tuple(config["sources"]["e016_train_target"]["shape"])
    epsilon = np.float32(config["target"]["standardization"]["epsilon"])
    started = time.perf_counter()
    started_cpu = process_cpu_seconds()
    with np.load(source_path, allow_pickle=False) as cache:
        targets = cache["targets"]
        if targets.shape != expected_shape or targets.dtype != np.float32:
            raise ValueError(
                f"E016 target shape/dtype mismatch: {targets.shape} {targets.dtype}"
            )
        if not np.isfinite(targets).all():
            raise ValueError("E016 training target contains nonfinite values")
        mean = targets.mean(axis=0, keepdims=True).astype(np.float32)
        std = (targets.std(axis=0, keepdims=True) + epsilon).astype(np.float32)
    if not np.isfinite(mean).all() or not np.isfinite(std).all():
        raise ValueError("E016 target standardizer is nonfinite")
    if np.any(std <= 0):
        raise ValueError("E016 target standardizer has nonpositive scale")

    metadata = {
        "schema_version": "e030-standardization.v1",
        "science_status": (
            "OUTCOME SEALED: exact E016 training-cache standardizer only; "
            "the E030 Tuckute target was not opened"
        ),
        "algorithm": config["target"]["standardization"]["algorithm"],
        "population_ddof": config["target"]["standardization"][
            "population_ddof"
        ],
        "epsilon": float(epsilon),
        "source": source,
        "design_manifest_sha256": design_hash,
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "shape": list(expected_shape),
        "mean_shape": list(mean.shape),
        "std_shape": list(std.shape),
        "mean_dtype": str(mean.dtype),
        "std_dtype": str(std.dtype),
        "mean_sha256": sha256_array(mean),
        "std_sha256": sha256_array(std),
        "elapsed_seconds": float(time.perf_counter() - started),
        "peak_rss_kib": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }
    output = path_for(config, "standardization")
    atomic_write_npz(
        output,
        mean=mean,
        std=std,
        metadata_json=np.array(
            json.dumps(metadata, sort_keys=True), dtype=np.str_
        ),
    )
    metadata["artifact"] = file_record(output)
    atomic_write_json(path_for(config, "standardization_manifest"), metadata)
    return metadata


def require_report_pass(path: Path, schema: str) -> tuple[dict[str, Any], str]:
    report = load_json(path)
    if report.get("schema_version") != schema or report.get("pass") is not True:
        raise ValueError(f"required report did not pass: {path}")
    return report, sha256_file(path)


def validate_runtime_payload(
    payload: Any, config: dict[str, Any], label: str
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be an object")
    require_exact_keys(
        payload,
        {"schema_version", "identity", "semantic_sha256"},
        label,
    )
    if payload["schema_version"] != "e030-tribe-runtime.v1":
        raise ValueError(f"{label} schema mismatch")
    identity = payload["identity"]
    require_exact_keys(
        identity,
        {
            "tribe_checkout",
            "git_head",
            "tracked_diff_sha256",
            "status_sha256",
            "python",
            "python_version",
            "sorted_pip_freeze_sha256",
            "sorted_pip_freeze_line_count",
            "hf_home",
            "tribe_snapshot",
            "tribe_checkpoint",
            "llama_snapshot",
            "llama_shards",
        },
        f"{label}.identity",
    )
    semantic = sha256_bytes(canonical_json_bytes(identity))
    if payload["semantic_sha256"] != semantic:
        raise ValueError(f"{label} semantic digest mismatch")
    frozen = config["runtime"]
    expected_scalars = {
        "tribe_checkout": str(resolve(frozen["tribe_checkout"])),
        "git_head": frozen["tribe_git_head"],
        "tracked_diff_sha256": frozen["tribe_tracked_diff_sha256"],
        "status_sha256": frozen["tribe_status_sha256"],
        "python": str(resolve(frozen["python"])),
        "python_version": f"Python {frozen['python_version']}",
        "sorted_pip_freeze_sha256": frozen["sorted_pip_freeze_sha256"],
        "sorted_pip_freeze_line_count": int(
            frozen["sorted_pip_freeze_line_count"]
        ),
        "hf_home": frozen["hf_home"],
        "tribe_snapshot": frozen["tribe_snapshot"],
        "llama_snapshot": frozen["llama_snapshot"],
    }
    for key, expected in expected_scalars.items():
        if identity[key] != expected:
            raise ValueError(f"{label} frozen runtime field mismatch: {key}")
    checkpoint = identity["tribe_checkpoint"]
    require_exact_keys(
        checkpoint, {"path", "size_bytes", "sha256"}, f"{label}.tribe_checkpoint"
    )
    if (
        Path(checkpoint["path"]).resolve()
        != Path(frozen["tribe_checkpoint"]["path"]).resolve()
        or checkpoint["sha256"] != frozen["tribe_checkpoint"]["sha256"]
    ):
        raise ValueError(f"{label} checkpoint identity mismatch")
    shards = identity["llama_shards"]
    if not isinstance(shards, list) or len(shards) != len(frozen["llama_shards"]):
        raise ValueError(f"{label} Llama shard grid mismatch")
    for index, (observed, expected) in enumerate(zip(shards, frozen["llama_shards"])):
        require_exact_keys(
            observed,
            {"path", "size_bytes", "sha256"},
            f"{label}.llama_shards[{index}]",
        )
        if (
            Path(observed["path"]).resolve() != Path(expected["path"]).resolve()
            or observed["sha256"] != expected["sha256"]
        ):
            raise ValueError(f"{label} Llama shard identity mismatch at {index}")
    return payload


def readiness_inputs(
    config_path: Path, *, write_bundle: bool
) -> tuple[dict[str, Any], dict[str, Any]]:
    config, _, design_hash = validate_design_manifest(config_path)
    config_hash = sha256_file(config_path.resolve())
    bundle = bundle_manifest(config_path)
    bundle_path = path_for(config, "bundle_manifest")
    if write_bundle:
        atomic_write_json(bundle_path, bundle)
    stored_bundle = load_json(bundle_path)
    require_exact_keys(
        stored_bundle, {"schema_version", "files", "bundle_sha256"}, "stored bundle"
    )
    if stored_bundle != bundle:
        raise ValueError("stored bundle is stale for the current files")
    selftest, selftest_hash = require_report_pass(
        path_for(config, "selftest_report"), "e030-selftest.v2"
    )
    benchmark, benchmark_hash = require_report_pass(
        path_for(config, "benchmark_report"), "e030-benchmark.v3"
    )
    smoke, smoke_hash = require_report_pass(
        path_for(config, "smoke_report"), "e030-smoke-replay.v1"
    )
    standardizer = load_json(path_for(config, "standardization_manifest"))
    if standardizer.get("schema_version") != "e030-standardization.v1":
        raise ValueError("standardization manifest is missing or invalid")
    standardizer_hash = sha256_file(
        path_for(config, "standardization_manifest")
    )
    for label, report in (("selftest", selftest), ("benchmark", benchmark)):
        if (
            report.get("config_sha256") != config_hash
            or report.get("design_manifest_sha256") != design_hash
        ):
            raise ValueError(f"{label} report is stale for the current design")
    if (
        smoke.get("config_sha256") != config_hash
        or smoke.get("design_manifest_sha256") != design_hash
    ):
        raise ValueError("smoke report is stale for the current design")
    if standardizer.get("design_manifest_sha256") != design_hash:
        raise ValueError("standardizer is stale for the current design")
    current_runner_hash = bundle["files"]["runner"]["sha256"]
    for label, report in (
        ("selftest", selftest),
        ("benchmark", benchmark),
        ("smoke", smoke),
        ("standardizer", standardizer),
    ):
        if report.get("runner_sha256") != current_runner_hash:
            raise ValueError(f"{label} report is stale for the current runner")
    if (
        selftest.get("analyzer_sha256")
        != bundle["files"]["analyzer"]["sha256"]
        or benchmark.get("analyzer_sha256")
        != bundle["files"]["analyzer"]["sha256"]
    ):
        raise ValueError("selftest or benchmark is stale for the current analyzer")
    validate_runtime_payload(smoke.get("runtime"), config, "smoke runtime")
    standardization_path = path_for(config, "standardization")
    require_current_file_record(
        standardizer.get("artifact"),
        standardization_path,
        "standardization artifact",
    )
    standardizer_source = standardizer.get("source")
    if not isinstance(standardizer_source, dict):
        raise ValueError("standardizer source record is missing")
    frozen_standardizer_source = config["sources"]["e016_train_target"]
    require_current_frozen_source_record(
        standardizer_source,
        frozen_standardizer_source,
        "standardizer frozen source",
    )
    oracle_path = path_for(config, "oracle_report")
    oracle = load_json(oracle_path)
    if (
        oracle.get("schema_version") != "e030-oracle-review.v1"
        or oracle.get("approved") is not True
        or oracle.get("bundle_sha256") != bundle["bundle_sha256"]
    ):
        raise ValueError("oracle report does not approve the current bundle")
    records = {
        "bundle": bundle,
        "bundle_manifest": file_record(bundle_path),
        "design_manifest": file_record(path_for(config, "design_manifest")),
        "selftest_report": file_record(path_for(config, "selftest_report")),
        "benchmark_report": file_record(path_for(config, "benchmark_report")),
        "smoke_report": file_record(path_for(config, "smoke_report")),
        "standardization_manifest": file_record(
            path_for(config, "standardization_manifest")
        ),
        "standardization_artifact": file_record(standardization_path),
        "oracle_report": file_record(oracle_path),
    }
    expected_hashes = {
        "design_manifest": design_hash,
        "selftest_report": selftest_hash,
        "benchmark_report": benchmark_hash,
        "smoke_report": smoke_hash,
        "standardization_manifest": standardizer_hash,
    }
    for name, expected_hash in expected_hashes.items():
        if records[name]["sha256"] != expected_hash:
            raise AssertionError(f"readiness input hash drifted: {name}")
    return config, records


def seal_readiness(config_path: Path) -> dict[str, Any]:
    config, records = readiness_inputs(config_path, write_bundle=True)
    readiness = {
        "schema_version": "e030-readiness.v2",
        "verdict": "DESIGN PASS / READY-TO-RUN: YES",
        "ready": True,
        **records,
        "all_pre_result_gates_pass": True,
    }
    atomic_write_json(path_for(config, "readiness"), readiness)
    return readiness


def require_readiness(
    config_path: Path, config: dict[str, Any]
) -> tuple[dict[str, Any], str]:
    path = path_for(config, "readiness")
    readiness = load_json(path)
    require_exact_keys(
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
        "E030 readiness seal",
    )
    current_config, records = readiness_inputs(config_path, write_bundle=False)
    if current_config != config:
        raise ValueError("readiness config object differs from caller config")
    if (
        readiness.get("schema_version") != "e030-readiness.v2"
        or readiness.get("ready") is not True
        or readiness.get("verdict") != "DESIGN PASS / READY-TO-RUN: YES"
        or readiness.get("all_pre_result_gates_pass") is not True
        or any(readiness.get(key) != value for key, value in records.items())
    ):
        raise ValueError("E030 readiness seal is missing, stale, or invalid")
    return readiness, sha256_file(path)


def load_generator_module(path: Path):
    specification = importlib.util.spec_from_file_location(
        "e030_bound_tribe_generator", path
    )
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load target generator: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def load_participant_module(path: Path):
    specification = importlib.util.spec_from_file_location(
        "e030_bound_e025_participant_loader", path
    )
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load participant loader: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def target_generator_settings(config: dict[str, Any]) -> dict[str, Any]:
    target = config["target"]
    return {
        "features": target["features"],
        "text_model": target["text_model"],
        "event_mode": target["event_mode"],
        "target_dim": int(target["target_dim"]),
        "tr": float(target["tr"]),
        "word_duration": float(target["word_duration"]),
        "word_gap": float(target["word_gap"]),
        "min_duration": float(target["min_duration"]),
        "batch_items": int(target["batch_items"]),
    }


def target_prediction_args(config: dict[str, Any]) -> SimpleNamespace:
    target_config = config["target"]
    return SimpleNamespace(
        word_duration=float(target_config["word_duration"]),
        word_gap=float(target_config["word_gap"]),
        min_duration=float(target_config["min_duration"]),
        quiet=True,
    )


def run_target_worker(config_path: Path, output: Path) -> None:
    started_wall = time.perf_counter()
    started_cpu = process_cpu_seconds()
    config, _ = load_config(config_path)
    timeout_seconds = float(config["compute_ceiling"]["target_gpu_hours"]) * 3600.0
    if (
        timeout_seconds <= 0
        or config["compute_ceiling"]["target_timeout_rule"]
        != "target_gpu_hours * 3600 wall-clock seconds"
    ):
        raise ValueError("E030 target-worker timeout policy is invalid")

    def target_worker_timeout(_signum: int, _frame: Any) -> None:
        raise TimeoutError("E030 target-worker exceeded target_gpu_hours")

    signal.signal(signal.SIGALRM, target_worker_timeout)
    signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
    config, _, design_hash = validate_design_manifest(config_path)
    config_hash = sha256_file(config_path.resolve())
    readiness, readiness_hash = require_readiness(config_path, config)
    runtime = runtime_manifest(config)
    storage_before = enforce_retained_storage(config)
    checkout = resolve(config["runtime"]["tribe_checkout"]).resolve()
    if Path.cwd().resolve() != checkout:
        raise ValueError("target-worker must run from the frozen TRIBE checkout")
    generator_identity = source_record(config, "target_generator")
    corpus_path = path_for(config, "corpus")
    require_hash(
        corpus_path,
        config["substrate"]["ordered_text_sha256"],
        "E030 target corpus",
    )
    texts = corpus_path.read_text(encoding="utf-8").splitlines()
    if len(texts) != int(config["substrate"]["n_items"]):
        raise ValueError("E030 target corpus row count mismatch")
    if ordered_text_sha(texts) != config["substrate"]["ordered_text_sha256"]:
        raise ValueError("E030 target corpus order mismatch")
    item_indices = np.arange(len(texts), dtype=np.int64)
    generator = load_generator_module(
        resolve(config["sources"]["target_generator"]["path"])
    )
    target_config = config["target"]
    vertex_index = generator.vertex_index(target_config["target_dim"])
    model, config_update = generator.load_model(target_config["features"])
    if (
        config_update.get("data.text_feature.model_name")
        != target_config["text_model"]
        or config_update.get("data.features_to_use") != target_config["features"]
    ):
        raise ValueError("TRIBE target-worker model/features config mismatch")
    if float(model.data.TR) != float(target_config["tr"]):
        raise ValueError("TRIBE target-worker TR mismatch")
    args = target_prediction_args(config)
    all_targets: list[np.ndarray] = []
    all_counts: list[np.ndarray] = []
    started = time.perf_counter()
    batch_items = int(target_config["batch_items"])
    for start in range(0, len(texts), batch_items):
        stop = min(start + batch_items, len(texts))
        print(f"E030 target batch {start}:{stop}", flush=True)
        batch_targets, batch_counts, _ = generator.predict_synthetic(
            model,
            texts[start:stop],
            item_indices[start:stop],
            args,
            vertex_index,
        )
        all_targets.append(batch_targets)
        all_counts.append(batch_counts)
    targets = np.concatenate(all_targets, axis=0).astype(np.float32)
    counts = np.concatenate(all_counts, axis=0).astype(np.int32)
    if targets.shape != (
        int(config["substrate"]["n_items"]),
        int(target_config["target_dim"]),
    ):
        raise ValueError(f"target-worker shape mismatch: {targets.shape}")
    if not np.isfinite(targets).all() or np.any(counts <= 0):
        raise ValueError("target-worker produced invalid values or segments")
    worker_resource_use = {
        "elapsed_wall_seconds": float(time.perf_counter() - started_wall),
        "elapsed_cpu_seconds": float(process_cpu_seconds() - started_cpu),
        "peak_rss_kib": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "retained_output_dir_bytes_before_write": int(storage_before),
        "retained_storage_limit_bytes": retained_storage_limit_bytes(config),
        "target_timeout_seconds": float(timeout_seconds),
    }
    metadata = {
        "schema_version": "e030-target-cache.v2",
        "experiment": "E030 exact-substrate TRIBE target acquisition",
        "science_status": (
            "target-cache artifact only; no participant response was opened"
        ),
        "config_sha256": config_hash,
        "design_manifest_sha256": design_hash,
        "readiness_sha256": readiness_hash,
        "bundle_sha256": readiness["bundle"]["bundle_sha256"],
        "runtime_semantic_sha256": runtime["semantic_sha256"],
        "generator": generator_identity,
        "generator_settings_sha256": sha256_bytes(
            canonical_json_bytes(target_generator_settings(config))
        ),
        "corpus": file_record(corpus_path),
        "condition": config["substrate"]["condition"],
        "n_items": len(texts),
        "batch_items": batch_items,
        "features": target_config["features"],
        "text_model": target_config["text_model"],
        "event_mode": target_config["event_mode"],
        "target_dim": int(targets.shape[1]),
        "tr": float(model.data.TR),
        "word_duration": float(target_config["word_duration"]),
        "word_gap": float(target_config["word_gap"]),
        "min_duration": float(target_config["min_duration"]),
        "config_update": config_update,
        "ordered_item_sha256": config["substrate"]["ordered_item_sha256"],
        "ordered_text_sha256": ordered_text_sha(texts),
        "item_mapping": "item_id = item_index + 1",
        "elapsed_seconds": float(time.perf_counter() - started),
        "worker_resource_use": worker_resource_use,
    }
    if output.exists():
        raise FileExistsError(f"target-worker refuses overwrite: {output}")
    atomic_write_npz(
        output,
        targets=targets,
        texts=np.asarray(texts, dtype=np.str_),
        item_indices=item_indices,
        vertex_index=vertex_index.astype(np.int64),
        segment_counts=counts,
        metadata_json=np.array(
            json.dumps(metadata, sort_keys=True), dtype=np.str_
        ),
    )
    enforce_retained_storage(config)
    signal.setitimer(signal.ITIMER_REAL, 0.0)


def validate_target_cache(
    config_path: Path,
    config: dict[str, Any],
    path: Path,
    *,
    design_hash: str,
    readiness: dict[str, Any],
    readiness_hash: str,
    runtime: dict[str, Any],
) -> dict[str, Any]:
    validate_runtime_payload(runtime, config, "current target runtime")
    with np.load(path, allow_pickle=False) as cache:
        required = {
            "targets",
            "texts",
            "item_indices",
            "vertex_index",
            "segment_counts",
            "metadata_json",
        }
        if set(cache.files) != required:
            raise ValueError(f"E030 target keys differ: {cache.files}")
        targets = cache["targets"]
        texts = [str(value) for value in cache["texts"].tolist()]
        item_indices = cache["item_indices"].astype(np.int64, copy=False)
        vertex_index = cache["vertex_index"].astype(np.int64, copy=False)
        counts = cache["segment_counts"]
        metadata = json.loads(str(cache["metadata_json"].item()))
        if not isinstance(metadata, dict):
            raise ValueError("E030 target metadata must be an object")
        require_exact_keys(
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
            "E030 target metadata",
        )
        if metadata["schema_version"] != "e030-target-cache.v2":
            raise ValueError("E030 target metadata schema mismatch")
        expected_shape = (
            int(config["substrate"]["n_items"]),
            int(config["target"]["target_dim"]),
        )
        if targets.shape != expected_shape or targets.dtype != np.float32:
            raise ValueError(
                f"E030 target shape/dtype mismatch: {targets.shape} {targets.dtype}"
            )
        if not np.isfinite(targets).all():
            raise ValueError("E030 target contains nonfinite values")
        if counts.shape != (expected_shape[0],) or np.any(counts <= 0):
            raise ValueError("E030 target segment counts are invalid")
        if not np.array_equal(
            item_indices, np.arange(expected_shape[0], dtype=np.int64)
        ):
            raise ValueError("E030 target generator indices are reordered")
        if ordered_text_sha(texts) != config["substrate"]["ordered_text_sha256"]:
            raise ValueError("E030 target text order mismatch")
        expected_metadata = {
            "experiment": "E030 exact-substrate TRIBE target acquisition",
            "science_status": (
                "target-cache artifact only; no participant response was opened"
            ),
            "config_sha256": sha256_file(config_path.resolve()),
            "design_manifest_sha256": design_hash,
            "readiness_sha256": readiness_hash,
            "bundle_sha256": readiness["bundle"]["bundle_sha256"],
            "runtime_semantic_sha256": runtime["semantic_sha256"],
            "generator_settings_sha256": sha256_bytes(
                canonical_json_bytes(target_generator_settings(config))
            ),
            "condition": config["substrate"]["condition"],
            "n_items": int(config["substrate"]["n_items"]),
            "batch_items": int(config["target"]["batch_items"]),
            "features": config["target"]["features"],
            "text_model": config["target"]["text_model"],
            "event_mode": config["target"]["event_mode"],
            "target_dim": int(config["target"]["target_dim"]),
            "tr": float(config["target"]["tr"]),
            "word_duration": float(config["target"]["word_duration"]),
            "word_gap": float(config["target"]["word_gap"]),
            "min_duration": float(config["target"]["min_duration"]),
            "ordered_item_sha256": config["substrate"]["ordered_item_sha256"],
            "ordered_text_sha256": config["substrate"]["ordered_text_sha256"],
            "item_mapping": "item_id = item_index + 1",
        }
        for key, expected in expected_metadata.items():
            if metadata[key] != expected:
                raise ValueError(f"E030 target metadata mismatch: {key}")
        if metadata["generator"] != source_record(config, "target_generator"):
            raise ValueError("E030 target generator identity mismatch")
        if metadata["corpus"] != file_record(path_for(config, "corpus")):
            raise ValueError("E030 target corpus identity mismatch")
        smoke = load_json(path_for(config, "smoke_report"))
        if metadata["config_update"] != smoke.get("stable_metadata", {}).get(
            "config_update"
        ):
            raise ValueError("E030 target generator config update differs from smoke")
        elapsed = metadata["elapsed_seconds"]
        if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)) or not math.isfinite(float(elapsed)) or float(elapsed) < 0:
            raise ValueError("E030 target elapsed time is invalid")
        worker_resource = metadata["worker_resource_use"]
        if not isinstance(worker_resource, dict):
            raise ValueError("E030 target worker resource record is invalid")
        require_exact_keys(
            worker_resource,
            {
                "elapsed_wall_seconds",
                "elapsed_cpu_seconds",
                "peak_rss_kib",
                "retained_output_dir_bytes_before_write",
                "retained_storage_limit_bytes",
                "target_timeout_seconds",
            },
            "E030 target worker resources",
        )
        for key in (
            "elapsed_wall_seconds",
            "elapsed_cpu_seconds",
            "target_timeout_seconds",
        ):
            value = worker_resource[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) or float(value) < 0:
                raise ValueError(f"E030 target worker resource is invalid: {key}")
        if float(worker_resource["target_timeout_seconds"]) != (
            float(config["compute_ceiling"]["target_gpu_hours"]) * 3600.0
        ):
            raise ValueError("E030 target worker timeout ceiling mismatch")
        for key in (
            "peak_rss_kib",
            "retained_output_dir_bytes_before_write",
            "retained_storage_limit_bytes",
        ):
            if isinstance(worker_resource[key], bool) or not isinstance(worker_resource[key], int) or worker_resource[key] < 0:
                raise ValueError(f"E030 target worker resource is invalid: {key}")
        if worker_resource["retained_storage_limit_bytes"] != retained_storage_limit_bytes(config):
            raise ValueError("E030 target worker storage ceiling mismatch")
        semantic = {
            "targets": sha256_array(targets),
            "texts": ordered_text_sha(texts),
            "item_indices": sha256_array(item_indices.astype("<i8")),
            "vertex_index": sha256_array(vertex_index.astype("<i8")),
            "segment_counts": sha256_array(counts),
        }
    heldout = resolve(config["sources"]["e016_heldout_target"]["path"])
    with np.load(heldout, allow_pickle=False) as cache:
        expected_vertex = cache["vertex_index"].astype(np.int64, copy=False)
    if not np.array_equal(vertex_index, expected_vertex):
        raise ValueError("E030 target vertex identity differs from E016")
    if semantic["vertex_index"] != config["sources"]["e016_heldout_target"][
        "vertex_index_sha256"
    ]:
        raise ValueError("E030 target vertex hash differs from E016")
    return {
        "schema_version": "e030-target-manifest.v2",
        "science_status": (
            "OUTCOME SEALED: target schema, order, finiteness, and identity "
            "only; no target geometry or participant score was inspected"
        ),
        "config_sha256": sha256_file(config_path.resolve()),
        "design_manifest_sha256": design_hash,
        "readiness_sha256": readiness_hash,
        "bundle_sha256": readiness["bundle"]["bundle_sha256"],
        "runtime_semantic_sha256": runtime["semantic_sha256"],
        "target": file_record(path),
        "shape": list(expected_shape),
        "dtype": "float32",
        "finite": True,
        "all_segment_counts_positive": True,
        "semantic_sha256": semantic,
        "metadata": metadata,
    }


def run_target(config_path: Path, gpu: str) -> dict[str, Any]:
    stage_started_wall = time.perf_counter()
    stage_started_cpu = process_cpu_seconds()
    config, _, design_hash = validate_design_manifest(config_path)
    readiness, readiness_hash = require_readiness(config_path, config)
    runtime = runtime_manifest(config)
    storage_before = enforce_retained_storage(config)
    timeout_seconds = float(config["compute_ceiling"]["target_gpu_hours"]) * 3600.0
    if timeout_seconds <= 0 or config["compute_ceiling"]["target_timeout_rule"] != (
        "target_gpu_hours * 3600 wall-clock seconds"
    ):
        raise ValueError("E030 target timeout policy is invalid")
    target_path = path_for(config, "target")
    if target_path.exists() or path_for(config, "acquisition_manifest").exists():
        raise FileExistsError(
            "E030 acquisition is single-use; target or acquisition seal exists"
        )
    target_path.parent.mkdir(parents=True, exist_ok=True)
    log_path = target_path.with_suffix(".log")
    checkout = resolve(config["runtime"]["tribe_checkout"])
    python = resolve(config["runtime"]["python"])
    with tempfile.TemporaryDirectory(
        prefix=".e030-target.", dir=target_path.parent
    ) as temporary:
        temporary_path = Path(temporary) / "target.npz"
        command = [
            str(python),
            str(Path(__file__).resolve()),
            "--config",
            str(config_path.resolve()),
            "target-worker",
            "--out",
            str(temporary_path),
        ]
        environment = os.environ.copy()
        environment.update(
            {
                "CUDA_VISIBLE_DEVICES": str(gpu),
                "HF_HOME": config["runtime"]["hf_home"],
                "HF_HUB_OFFLINE": "1",
                "TRANSFORMERS_OFFLINE": "1",
            }
        )
        started = time.perf_counter()
        with log_path.open("wb") as log:
            subprocess.run(
                command,
                cwd=checkout,
                env=environment,
                check=True,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout_seconds,
            )
        elapsed = time.perf_counter() - started
        target_manifest = validate_target_cache(
            config_path,
            config,
            temporary_path,
            design_hash=design_hash,
            readiness=readiness,
            readiness_hash=readiness_hash,
            runtime=runtime,
        )
        os.replace(temporary_path, target_path)
    target_manifest["target"] = file_record(target_path)
    target_manifest["runtime"] = runtime
    target_manifest["elapsed_seconds"] = float(elapsed)
    target_manifest["gpu_selector"] = str(gpu)
    target_manifest["log"] = file_record(log_path)
    target_resource_use = {
        "timeout_seconds": float(timeout_seconds),
        "elapsed_wall_seconds": float(time.perf_counter() - stage_started_wall),
        "elapsed_cpu_seconds": float(process_cpu_seconds() - stage_started_cpu),
        "parent_peak_rss_kib": int(
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        ),
        "retained_output_dir_bytes_before": int(storage_before),
        "retained_output_dir_bytes_projected_after_seal": 0,
        "retained_storage_limit_bytes": retained_storage_limit_bytes(config),
    }
    target_manifest["resource_use"] = target_resource_use
    target_manifest_path = path_for(config, "target_manifest")
    base_storage_after_target = enforce_retained_storage(config)
    acquisition: dict[str, Any] = {}
    for _ in range(8):
        target_manifest_bytes = canonical_json_bytes(target_manifest)
        target_manifest_record = {
            "path": str(target_manifest_path),
            "size_bytes": len(target_manifest_bytes),
            "sha256": sha256_bytes(target_manifest_bytes),
        }
        acquisition = {
            "schema_version": "e030-acquisition-manifest.v2",
            "science_status": (
                "OUTCOME SEALED: exact target identity is frozen; no target "
                "geometry or participant response score was inspected"
            ),
            "bundle_sha256": readiness["bundle"]["bundle_sha256"],
            "config_sha256": sha256_file(config_path.resolve()),
            "readiness_sha256": readiness_hash,
            "design_manifest_sha256": design_hash,
            "target_manifest": target_manifest_record,
            "target": file_record(target_path),
            "semantic_sha256": target_manifest["semantic_sha256"],
            "runtime": runtime,
            "resource_use": target_resource_use,
        }
        projected = int(
            base_storage_after_target
            + len(target_manifest_bytes)
            + len(canonical_json_bytes(acquisition))
        )
        if (
            target_resource_use[
                "retained_output_dir_bytes_projected_after_seal"
            ]
            == projected
        ):
            break
        target_resource_use[
            "retained_output_dir_bytes_projected_after_seal"
        ] = projected
    if projected > retained_storage_limit_bytes(config):
        raise RuntimeError("E030 target seal would exceed retained-storage ceiling")
    atomic_write_json(target_manifest_path, target_manifest)
    if file_record(target_manifest_path) != acquisition["target_manifest"]:
        raise AssertionError("target-manifest in-memory identity drifted on write")
    atomic_write_json(path_for(config, "acquisition_manifest"), acquisition)
    enforce_retained_storage(config)
    return acquisition


def pca_folds(
    features: np.ndarray,
    folds: list[tuple[np.ndarray, np.ndarray]],
    rank: int,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    from sklearn.decomposition import PCA

    output: list[dict[str, Any]] = []
    for fold, (train, test) in enumerate(folds):
        components = min(rank, len(train) - 1, features.shape[1])
        model = PCA(
            n_components=components,
            svd_solver=config["estimator"]["pca_svd_solver"],
            whiten=bool(config["estimator"]["pca_whiten"]),
            random_state=int(config["estimator"]["pca_random_state"]),
        )
        reduced_train = model.fit_transform(features[train])
        reduced_test = model.transform(features[test])
        output.append(
            {
                "fold": fold,
                "train": train,
                "test": test,
                "reduced_train": reduced_train,
                "reduced_test": reduced_test,
                "basis_sha256": sha256_array(
                    np.asarray(model.components_)
                ),
            }
        )
    return output


def paired_target_pca_folds(
    aligned: np.ndarray,
    twin: np.ndarray,
    folds: list[tuple[np.ndarray, np.ndarray]],
    rank: int,
    config: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    from sklearn.decomposition import PCA

    if aligned.shape != twin.shape:
        raise ValueError("aligned/twin target shapes differ")
    output: dict[str, list[dict[str, Any]]] = {
        "aligned": [],
        "twin": [],
    }
    for fold, (train, test) in enumerate(folds):
        components = min(rank, len(train) - 1, aligned.shape[1])
        model = PCA(
            n_components=components,
            svd_solver=config["estimator"]["pca_svd_solver"],
            whiten=bool(config["estimator"]["pca_whiten"]),
            random_state=int(config["estimator"]["pca_random_state"]),
        )
        model.fit(aligned[train])
        basis_sha256 = sha256_array(np.asarray(model.components_))
        for alignment, values in (("aligned", aligned), ("twin", twin)):
            output[alignment].append(
                {
                    "fold": fold,
                    "train": train,
                    "test": test,
                    "reduced_train": model.transform(values[train]),
                    "reduced_test": model.transform(values[test]),
                    "basis_sha256": basis_sha256,
                    "basis_fit_arm": "aligned",
                }
            )
    return output


def ridge_fit_details(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    config: dict[str, Any],
) -> dict[str, Any]:
    from sklearn.linear_model import RidgeCV
    from sklearn.preprocessing import StandardScaler

    estimator = config["estimator"]
    scaler = StandardScaler(
        with_mean=bool(estimator["standard_scaler_with_mean"]),
        with_std=bool(estimator["standard_scaler_with_std"]),
    ).fit(x_train)
    y_mean = y_train.mean(axis=0, keepdims=True)
    model = RidgeCV(
        alphas=[float(value) for value in estimator["ridge_alphas"]],
        cv=estimator["ridge_cv"],
        scoring=estimator["ridge_scoring"],
        gcv_mode=estimator["ridge_gcv_mode"],
        fit_intercept=bool(estimator["ridge_fit_intercept"]),
        alpha_per_target=bool(estimator["ridge_alpha_per_target"]),
    )
    standardized_train = scaler.transform(x_train)
    standardized_test = scaler.transform(x_test)
    model.fit(standardized_train, y_train - y_mean)
    if np.ndim(model.alpha_) != 0:
        raise ValueError("RidgeCV selected a non-scalar alpha")
    coefficients = np.asarray(model.coef_)
    if coefficients.ndim != 2 or coefficients.shape != (
        y_train.shape[1],
        x_train.shape[1],
    ):
        raise ValueError("unexpected multi-output ridge coefficient shape")
    intercept = np.asarray(model.intercept_).reshape(1, -1)
    prediction = model.predict(standardized_test) + y_mean
    reconstructed = (
        standardized_test @ coefficients.T + intercept + y_mean
    )
    if not np.allclose(prediction, reconstructed, rtol=1e-6, atol=1e-7):
        raise AssertionError("ridge coefficient reconstruction failed")
    return {
        "prediction": prediction,
        "alpha": float(model.alpha_),
        "feature_mean": np.asarray(scaler.mean_),
        "feature_scale": np.asarray(scaler.scale_),
        "coefficients": coefficients,
        "intercept": intercept,
        "y_mean": y_mean,
        "standardized_test": standardized_test,
    }


def ridge_predictions(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    config: dict[str, Any],
) -> tuple[np.ndarray, float]:
    details = ridge_fit_details(x_train, y_train, x_test, config)
    return details["prediction"], details["alpha"]


def linear_feature_contribution(
    details: dict[str, Any],
    start: int,
    stop: int,
) -> np.ndarray:
    standardized = np.asarray(details["standardized_test"])
    coefficients = np.asarray(details["coefficients"])
    if not (0 <= start < stop <= standardized.shape[1]):
        raise ValueError("invalid ridge feature-contribution slice")
    if coefficients.shape[1] != standardized.shape[1]:
        raise ValueError("ridge contribution coefficient width mismatch")
    contribution = standardized[:, start:stop] @ coefficients[:, start:stop].T
    if not np.isfinite(contribution).all():
        raise ValueError("ridge feature contribution is nonfinite")
    return contribution


def linear_delta_contribution(
    delta_features: np.ndarray,
    feature_scale: np.ndarray,
    coefficients: np.ndarray,
) -> np.ndarray:
    delta = np.asarray(delta_features)
    scale = np.asarray(feature_scale).reshape(-1)
    coefficient_matrix = np.asarray(coefficients)
    if (
        delta.ndim != 2
        or scale.shape != (delta.shape[1],)
        or coefficient_matrix.ndim != 2
        or coefficient_matrix.shape[1] != delta.shape[1]
        or np.any(scale <= 0)
    ):
        raise ValueError("invalid standardized ridge delta composition")
    contribution = (delta / scale) @ coefficient_matrix.T
    if not np.isfinite(contribution).all():
        raise ValueError("composed ridge delta contribution is nonfinite")
    return contribution


def c1_prediction_r2(
    y_test: np.ndarray,
    prediction: np.ndarray,
) -> dict[str, np.ndarray]:
    sse = np.sum((y_test - prediction) ** 2, axis=0)
    centered = y_test - y_test.mean(axis=0, keepdims=True)
    sst = np.sum(centered**2, axis=0)
    r2 = 1.0 - sse / np.clip(sst, 1e-8, None)
    if not np.isfinite(r2).all():
        raise ValueError("nonfinite C1 ROI score")
    return {"r2": r2, "sse": sse, "sst": sst}


def per_output_r2(
    y_test: np.ndarray,
    prediction: np.ndarray,
    floor: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    residual = np.asarray(y_test, dtype=np.float64) - np.asarray(
        prediction, dtype=np.float64
    )
    centered = np.asarray(y_test, dtype=np.float64) - np.asarray(
        y_test, dtype=np.float64
    ).mean(axis=0, keepdims=True)
    sse = np.sum(residual * residual, axis=0, dtype=np.float64)
    sst = np.sum(centered * centered, axis=0, dtype=np.float64)
    if not np.isfinite(sse).all() or not np.isfinite(sst).all():
        raise ValueError("nonfinite SSE/SST")
    if np.any(sst <= floor):
        raise ValueError(
            f"held-out target coordinate SST at or below floor {floor}"
        )
    return 1.0 - sse / sst, sse, sst


def ridge_per_output(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    config: dict[str, Any],
) -> dict[str, Any]:
    prediction, alpha = ridge_predictions(
        x_train, y_train, x_test, config
    )
    r2, sse, sst = per_output_r2(
        y_test,
        prediction,
        float(config["estimator"]["coordinate_sst_floor"]),
    )
    return {
        "alpha": alpha,
        "r2": r2,
        "sse": sse,
        "sst": sst,
    }


def ridge_c1_per_output(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Reproduce E025's float32 ROI-wise held-out R2 semantics exactly."""
    details = ridge_fit_details(x_train, y_train, x_test, config)
    score = c1_prediction_r2(y_test, details["prediction"])
    return {
        **details,
        **score,
    }


def ridge_multioutput(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    config: dict[str, Any],
) -> dict[str, Any]:
    result = ridge_per_output(
        x_train, y_train, x_test, y_test, config
    )
    sse = result["sse"]
    sst = result["sst"]
    total_sse = float(np.sum(sse, dtype=np.float64))
    total_sst = float(np.sum(sst, dtype=np.float64))
    if not math.isfinite(total_sse) or not math.isfinite(total_sst):
        raise ValueError("nonfinite multi-output SSE/SST")
    if total_sst <= 0:
        raise ValueError("nonpositive multi-output total SST")
    return {
        "alpha": result["alpha"],
        "total_sse": total_sse,
        "total_sst": total_sst,
        "total_r2": 1.0 - total_sse / total_sst,
        "equal_coordinate_r2": float(
            np.mean(result["r2"], dtype=np.float64)
        ),
        "min_coordinate_sst": float(np.min(sst)),
        "max_coordinate_sst": float(np.max(sst)),
        "n_coordinates": int(len(sst)),
    }


def nuisance_arrays(
    config: dict[str, Any],
) -> tuple[dict[str, np.ndarray], np.ndarray, dict[str, Any]]:
    record = source_record(config, "e025_nuisance")
    path = Path(record["path"])
    with np.load(path, allow_pickle=False) as cache:
        required = {
            "base_scalar",
            "static_embedding",
            "imageability",
            "full_cov_extra",
            "metadata_json",
        }
        if set(cache.files) != required:
            raise ValueError("E025 nuisance cache keys changed")
        base = cache["base_scalar"].astype(np.float32)
        static = cache["static_embedding"].astype(np.float32)
        imageability = cache["imageability"].astype(np.float32)
        full_extra = cache["full_cov_extra"].astype(np.float32)
        metadata = json.loads(str(cache["metadata_json"].item()))
    if metadata["ordered_text_sha256"] != config["substrate"][
        "ordered_text_sha256"
    ]:
        raise ValueError("E025 nuisance text identity mismatch")
    n_items = int(config["substrate"]["n_items"])
    if (
        base.shape != (n_items, 2)
        or static.shape[0] != n_items
        or imageability.shape != (n_items, 1)
        or full_extra.shape != (n_items, 3)
    ):
        raise ValueError("E025 nuisance shapes changed")
    variants = {
        "base_continuity": base,
        "imageability_primary": np.concatenate(
            (base, imageability), axis=1
        ),
        "full_cov_stress": np.concatenate(
            (base, full_extra), axis=1
        ),
    }
    if set(variants) != set(config["estimator"]["nuisance_variants"]):
        raise ValueError("nuisance variants differ from config")
    return variants, static, {"artifact": record, "metadata": metadata}


def inherited_gates(config: dict[str, Any]) -> dict[str, Any]:
    analysis_record = source_record(config, "e025_analysis")
    extraction_record = source_record(config, "e025_extraction")
    analysis = load_json(Path(analysis_record["path"]))
    extraction = load_json(Path(extraction_record["path"]))
    gates = analysis.get("pre_scoring_gates", {})
    expected = {
        "quality_equivalence": True,
        "representation_movement": True,
        "target_direction": True,
    }
    if gates != expected:
        raise ValueError(f"E025 inherited gates are not all satisfied: {gates}")
    if analysis.get("source", {}).get("gates_sha256") != extraction_record[
        "sha256"
    ]:
        raise ValueError("E025 analysis does not bind the frozen extraction")
    return {
        "all_pass": True,
        "gates": gates,
        "analysis": analysis_record,
        "extraction": extraction_record,
        "extraction_gate_summary": extraction.get("gate_summary"),
    }


def representation_aliases(
    config: dict[str, Any],
) -> tuple[dict[tuple[int, str], dict[str, Any]], dict[str, Any]]:
    extraction_record = source_record(config, "e025_extraction")
    extraction = load_json(Path(extraction_record["path"]))
    wanted = {
        (int(seed), arm)
        for seed in config["estimator"]["seeds"]
        for arm in config["estimator"]["arms"]
    }
    mapping: dict[tuple[int, str], dict[str, Any]] = {}
    for row in extraction["cache_rows"]:
        for alias in row.get("aliases", []):
            key = (int(alias["seed"]), str(alias["arm"]))
            if alias["family"] == "tribe" and key in wanted:
                if key in mapping:
                    raise ValueError(f"duplicate E025 representation alias: {key}")
                mapping[key] = row
    if set(mapping) != wanted:
        raise ValueError(
            f"E025 representation aliases incomplete: {set(mapping) ^ wanted}"
        )
    return mapping, extraction_record


def load_representation(
    config: dict[str, Any],
    row: dict[str, Any],
    seed: int,
    arm: str,
) -> tuple[dict[int, np.ndarray], dict[str, Any]]:
    path = Path(row["path"])
    require_hash(path, row["sha256"], f"representation {seed}/{arm}")
    with np.load(path, allow_pickle=False) as cache:
        metadata = json.loads(str(cache["metadata_json"].item()))
        if metadata["tuckute_ordered_text_sha256"] != config["substrate"][
            "ordered_text_sha256"
        ]:
            raise ValueError("representation Tuckute text identity mismatch")
        aliases = {
            (int(value["seed"]), str(value["arm"]))
            for value in metadata["aliases"]
            if value["family"] == "tribe"
        }
        if (seed, arm) not in aliases:
            raise ValueError("representation metadata alias mismatch")
        layers = {
            layer: cache[f"tuckute_layer_{layer}"].astype(np.float32)
            for layer in (
                int(config["estimator"]["primary_layer"]),
                int(config["estimator"]["sensitivity_layer"]),
            )
        }
    expected_shape = (
        int(config["substrate"]["n_items"]),
        768,
    )
    if any(value.shape != expected_shape for value in layers.values()):
        raise ValueError("representation shape changed")
    if any(not np.isfinite(value).all() for value in layers.values()):
        raise ValueError("representation contains nonfinite values")
    identity = {
        "path": str(path),
        "sha256": row["sha256"],
        "cache_key": row["cache_key"],
        "weight_sha256": row["weight_sha256"],
    }
    return layers, identity


def validate_acquisition_chain(
    config_path: Path,
    config: dict[str, Any],
    *,
    design_hash: str,
    readiness: dict[str, Any],
    readiness_hash: str,
    runtime: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    acquisition_path = path_for(config, "acquisition_manifest")
    acquisition = load_json(acquisition_path)
    require_exact_keys(
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
        "E030 acquisition manifest",
    )
    if (
        acquisition["schema_version"] != "e030-acquisition-manifest.v2"
        or acquisition["config_sha256"] != sha256_file(config_path.resolve())
        or acquisition["bundle_sha256"] != readiness["bundle"]["bundle_sha256"]
        or acquisition["readiness_sha256"] != readiness_hash
        or acquisition["design_manifest_sha256"] != design_hash
    ):
        raise ValueError("E030 acquisition manifest is missing or stale")
    validate_runtime_payload(acquisition["runtime"], config, "acquisition runtime")
    if acquisition["runtime"] != runtime:
        raise ValueError("E030 acquisition runtime differs from current runtime")

    target_path = path_for(config, "target")
    target_record = require_current_file_record(
        acquisition["target"], target_path, "acquisition target"
    )
    target_manifest_path = path_for(config, "target_manifest")
    require_current_file_record(
        acquisition["target_manifest"],
        target_manifest_path,
        "acquisition target manifest",
    )
    target_manifest = load_json(target_manifest_path)
    require_exact_keys(
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
        "E030 target manifest",
    )
    current_target_manifest = validate_target_cache(
        config_path,
        config,
        target_path,
        design_hash=design_hash,
        readiness=readiness,
        readiness_hash=readiness_hash,
        runtime=runtime,
    )
    for key, expected in current_target_manifest.items():
        if target_manifest.get(key) != expected:
            raise ValueError(f"E030 target manifest is stale: {key}")
    if (
        target_manifest["runtime"] != runtime
        or target_manifest["runtime_semantic_sha256"]
        != runtime["semantic_sha256"]
        or target_manifest["target"] != target_record
        or target_manifest["target"] != acquisition["target"]
        or target_manifest["semantic_sha256"] != acquisition["semantic_sha256"]
        or target_manifest["resource_use"] != acquisition["resource_use"]
    ):
        raise ValueError("target-manifest/acquisition identity disagreement")
    require_current_file_record(
        target_manifest["log"],
        target_path.with_suffix(".log"),
        "target log",
    )
    target_elapsed = target_manifest["elapsed_seconds"]
    if isinstance(target_elapsed, bool) or not isinstance(target_elapsed, (int, float)) or not math.isfinite(float(target_elapsed)) or float(target_elapsed) < 0:
        raise ValueError("target manifest elapsed time is invalid")
    resource_use = acquisition["resource_use"]
    if not isinstance(resource_use, dict):
        raise ValueError("target resource-use record is invalid")
    require_exact_keys(
        resource_use,
        {
            "timeout_seconds",
            "elapsed_wall_seconds",
            "elapsed_cpu_seconds",
            "parent_peak_rss_kib",
            "retained_output_dir_bytes_before",
            "retained_output_dir_bytes_projected_after_seal",
            "retained_storage_limit_bytes",
        },
        "target resource use",
    )
    expected_timeout = float(config["compute_ceiling"]["target_gpu_hours"]) * 3600.0
    if (
        float(resource_use["timeout_seconds"]) != expected_timeout
        or int(resource_use["retained_storage_limit_bytes"])
        != retained_storage_limit_bytes(config)
    ):
        raise ValueError("target resource policy differs from current config")
    for key in ("elapsed_wall_seconds", "elapsed_cpu_seconds"):
        if not math.isfinite(float(resource_use[key])) or float(resource_use[key]) < 0:
            raise ValueError(f"target resource value is invalid: {key}")
    for key in (
        "parent_peak_rss_kib",
        "retained_output_dir_bytes_before",
        "retained_output_dir_bytes_projected_after_seal",
        "retained_storage_limit_bytes",
    ):
        if isinstance(resource_use[key], bool) or not isinstance(resource_use[key], int) or resource_use[key] < 0:
            raise ValueError(f"target resource value is invalid: {key}")
    if (
        resource_use["retained_output_dir_bytes_projected_after_seal"]
        < resource_use["retained_output_dir_bytes_before"]
        or resource_use["retained_output_dir_bytes_projected_after_seal"]
        > resource_use["retained_storage_limit_bytes"]
    ):
        raise ValueError("target projected retained storage is invalid")
    return acquisition, target_manifest


def load_external_target(
    config: dict[str, Any], acquisition: dict[str, Any]
) -> tuple[np.ndarray, dict[str, Any]]:
    target_path = path_for(config, "target")
    acquisition_path = path_for(config, "acquisition_manifest")
    standardization_path = path_for(config, "standardization")
    standardization_manifest = load_json(
        path_for(config, "standardization_manifest")
    )
    if standardization_manifest["artifact"]["sha256"] != sha256_file(
        standardization_path
    ):
        raise ValueError("E016 standardizer differs from frozen manifest")
    with np.load(standardization_path, allow_pickle=False) as cache:
        mean = cache["mean"].astype(np.float32, copy=False)
        std = cache["std"].astype(np.float32, copy=False)
        if sha256_array(mean) != standardization_manifest["mean_sha256"]:
            raise ValueError("E016 target mean hash mismatch")
        if sha256_array(std) != standardization_manifest["std_sha256"]:
            raise ValueError("E016 target std hash mismatch")
    with np.load(target_path, allow_pickle=False) as cache:
        target = cache["targets"].astype(np.float32)
    if mean.shape != (1, target.shape[1]) or std.shape != mean.shape:
        raise ValueError("external standardizer shape mismatch")
    standardized = ((target - mean) / std).astype(np.float32)
    if not np.isfinite(standardized).all():
        raise ValueError("externally standardized E030 target is nonfinite")
    return standardized, {
        "acquisition": file_record(acquisition_path),
        "target": file_record(target_path),
        "standardization": file_record(standardization_path),
        "standardization_manifest": file_record(
            path_for(config, "standardization_manifest")
        ),
    }


def fold_design(
    scalar: np.ndarray,
    static_fold: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray]:
    train = static_fold["train"]
    test = static_fold["test"]
    return (
        np.concatenate(
            (scalar[train], static_fold["reduced_train"]), axis=1
        ),
        np.concatenate(
            (scalar[test], static_fold["reduced_test"]), axis=1
        ),
    )


def participant_split(config: dict[str, Any], uid: int) -> str:
    if uid in config["substrate"]["train_uids"]:
        return "train"
    if uid in config["substrate"]["heldout_uids"]:
        return "heldout"
    raise ValueError(f"participant {uid} is outside frozen split")


def run_score(config_path: Path) -> dict[str, Any]:
    stage_started_wall = time.perf_counter()
    stage_started_cpu = process_cpu_seconds()
    config, design_manifest, design_hash = validate_design_manifest(config_path)
    config_hash = design_manifest["config"]["sha256"]
    configure_threads(config)
    resource_limits = apply_stage_resource_limits(config, "scoring")
    rss_stop, rss_thread = start_rss_watchdog(
        int(resource_limits["peak_rss_limit_kib"]),
        float(resource_limits["rss_watchdog_poll_seconds"]),
    )
    storage_before = enforce_retained_storage(config)
    scoring_runtime = validate_scoring_runtime(config)
    readiness, readiness_hash = require_readiness(config_path, config)
    raw_path = path_for(config, "raw_scores")
    if raw_path.exists():
        raise FileExistsError(
            f"E030 scorer is single-use and refuses overwrite: {raw_path}"
        )
    runtime = runtime_manifest(config)
    acquisition, _ = validate_acquisition_chain(
        config_path,
        config,
        design_hash=design_hash,
        readiness=readiness,
        readiness_hash=readiness_hash,
        runtime=runtime,
    )
    acquisition_path = path_for(config, "acquisition_manifest")

    target, target_identity = load_external_target(config, acquisition)
    folds = contiguous_folds(config)
    permutation = np.load(
        path_for(config, "twin_permutation"), allow_pickle=False
    ).astype(np.int64)
    twin = target[permutation]
    nuisance_variants, static, nuisance_identity = nuisance_arrays(config)
    rank = int(config["estimator"]["pca_rank"])
    bridge_target_rank = int(config["bridge"]["target_pca_rank"])
    bridge_student_rank = int(config["bridge"]["student_pca_rank"])
    if bridge_target_rank != rank or bridge_student_rank != rank:
        raise ValueError("E030 C1/C2/C3 PCA ranks must remain identical")
    static_folds = pca_folds(static, folds, rank, config)
    target_folds = paired_target_pca_folds(
        target, twin, folds, bridge_target_rank, config
    )

    participant_loader = source_record(config, "e025_participant_loader")
    e025 = load_participant_module(Path(participant_loader["path"]))
    texts, participant_targets, _, participant_summary = (
        e025.load_tuckute_participants(
            ROOT / "data/tuckute2024",
            str(config["substrate"]["condition"]),
            tuple(config["substrate"]["valid_uids"]),
            include_targets=True,
        )
    )
    if ordered_text_sha(texts) != config["substrate"]["ordered_text_sha256"]:
        raise ValueError("scoring participant text identity mismatch")
    if (
        participant_summary.get("ordered_item_id_sha256")
        != config["substrate"]["ordered_item_sha256"]
    ):
        raise ValueError("scoring participant item identity mismatch")
    e025_manifest = load_json(Path(source_record(config, "e025_manifest")["path"]))
    if participant_summary != e025_manifest.get("tuckute"):
        raise ValueError("scoring participant metadata differs from frozen E025")
    if set(participant_targets) != set(config["substrate"]["valid_uids"]):
        raise ValueError("scoring participant grid differs from design")

    c1_rows: list[dict[str, Any]] = []
    c1_bridge_models: dict[
        tuple[int, str, int, str], dict[str, Any]
    ] = {}
    for uid in config["substrate"]["valid_uids"]:
        responses = participant_targets[int(uid)].astype(np.float32)
        for nuisance_name, scalar in nuisance_variants.items():
            for fold, static_fold in enumerate(static_folds):
                train = static_fold["train"]
                test = static_fold["test"]
                nuisance_train, nuisance_test = fold_design(
                    scalar, static_fold
                )
                nuisance_score = ridge_c1_per_output(
                    nuisance_train,
                    responses[train],
                    nuisance_test,
                    responses[test],
                    config,
                )
                for alignment in ("aligned", "twin"):
                    contextual = target_folds[alignment][fold]
                    full_train = np.concatenate(
                        (
                            nuisance_train,
                            contextual["reduced_train"],
                        ),
                        axis=1,
                    )
                    full_test = np.concatenate(
                        (
                            nuisance_test,
                            contextual["reduced_test"],
                        ),
                        axis=1,
                    )
                    full_score = ridge_c1_per_output(
                        full_train,
                        responses[train],
                        full_test,
                        responses[test],
                        config,
                    )
                    target_start = nuisance_train.shape[1]
                    target_stop = full_train.shape[1]
                    target_scale = np.asarray(
                        full_score["feature_scale"][target_start:target_stop]
                    )
                    target_coefficients = np.asarray(
                        full_score["coefficients"][:, target_start:target_stop]
                    )
                    if target_scale.shape != (bridge_target_rank,) or (
                        target_coefficients.shape
                        != (responses.shape[1], bridge_target_rank)
                    ):
                        raise ValueError("C1 target coefficient block shape changed")
                    c1_bridge_models[
                        (int(uid), nuisance_name, fold, alignment)
                    ] = {
                        "base_prediction": nuisance_score["prediction"],
                        "base_r2": nuisance_score["r2"],
                        "alpha_nuisance": nuisance_score["alpha"],
                        "alpha_full": full_score["alpha"],
                        "target_scale": target_scale,
                        "target_coefficients": target_coefficients,
                    }
                    nuisance_mean = float(
                        np.mean(nuisance_score["r2"], dtype=np.float64)
                    )
                    full_mean = float(
                        np.mean(full_score["r2"], dtype=np.float64)
                    )
                    c1_rows.append(
                        {
                            "uid": int(uid),
                            "participant_split": participant_split(
                                config, int(uid)
                            ),
                            "nuisance_variant": nuisance_name,
                            "fold": fold,
                            "representation": alignment,
                            "test_start": int(test[0]),
                            "test_stop_exclusive": int(test[-1]) + 1,
                            "test_count": int(len(test)),
                            "target_pca_basis_sha256": contextual[
                                "basis_sha256"
                            ],
                            "static_pca_basis_sha256": static_fold[
                                "basis_sha256"
                            ],
                            "alpha_nuisance": nuisance_score["alpha"],
                            "alpha_full": full_score["alpha"],
                            "r2_nuisance_by_roi": nuisance_score[
                                "r2"
                            ].tolist(),
                            "r2_full_by_roi": full_score["r2"].tolist(),
                            "unique_r2_by_roi": (
                                full_score["r2"] - nuisance_score["r2"]
                            ).tolist(),
                            "r2_nuisance": nuisance_mean,
                            "r2_full": full_mean,
                            "unique_r2": full_mean - nuisance_mean,
                        }
                    )

    alias_rows, extraction_identity = representation_aliases(config)
    c2_rows: list[dict[str, Any]] = []
    representation_folds_cache: dict[
        tuple[int, str, int], list[dict[str, Any]]
    ] = {}
    representation_identity_cache: dict[
        tuple[int, str], dict[str, Any]
    ] = {}
    nuisance_baselines: dict[tuple[str, int], dict[str, Any]] = {}
    for nuisance_name, scalar in nuisance_variants.items():
        for fold, static_fold in enumerate(static_folds):
            train = static_fold["train"]
            test = static_fold["test"]
            nuisance_train, nuisance_test = fold_design(
                scalar, static_fold
            )
            nuisance_baselines[(nuisance_name, fold)] = ridge_multioutput(
                nuisance_train,
                target[train],
                nuisance_test,
                target[test],
                config,
            )

    for seed in config["estimator"]["seeds"]:
        for arm in config["estimator"]["arms"]:
            representations, representation_identity = load_representation(
                config,
                alias_rows[(int(seed), arm)],
                int(seed),
                arm,
            )
            representation_identity_cache[(int(seed), arm)] = (
                representation_identity
            )
            for layer, features in representations.items():
                representation_folds = pca_folds(
                    features, folds, rank, config
                )
                representation_folds_cache[
                    (int(seed), arm, int(layer))
                ] = representation_folds
                for nuisance_name, scalar in nuisance_variants.items():
                    for fold, static_fold in enumerate(static_folds):
                        train = static_fold["train"]
                        test = static_fold["test"]
                        nuisance_train, nuisance_test = fold_design(
                            scalar, static_fold
                        )
                        representation_fold = representation_folds[fold]
                        full_train = np.concatenate(
                            (
                                nuisance_train,
                                representation_fold["reduced_train"],
                            ),
                            axis=1,
                        )
                        full_test = np.concatenate(
                            (
                                nuisance_test,
                                representation_fold["reduced_test"],
                            ),
                            axis=1,
                        )
                        full = ridge_multioutput(
                            full_train,
                            target[train],
                            full_test,
                            target[test],
                            config,
                        )
                        nuisance = nuisance_baselines[
                            (nuisance_name, fold)
                        ]
                        if not math.isclose(
                            nuisance["total_sst"],
                            full["total_sst"],
                            rel_tol=0.0,
                            abs_tol=0.0,
                        ):
                            raise AssertionError(
                                "C2 nuisance/full target SST differs"
                            )
                        c2_rows.append(
                            {
                                "seed": int(seed),
                                "arm": arm,
                                "layer": int(layer),
                                "nuisance_variant": nuisance_name,
                                "fold": fold,
                                "test_start": int(test[0]),
                                "test_stop_exclusive": int(test[-1]) + 1,
                                "test_count": int(len(test)),
                                "cache_key": representation_identity[
                                    "cache_key"
                                ],
                                "weight_sha256": representation_identity[
                                    "weight_sha256"
                                ],
                                "representation_cache_sha256": (
                                    representation_identity["sha256"]
                                ),
                                "student_pca_basis_sha256": (
                                    representation_fold["basis_sha256"]
                                ),
                                "coordinate_count": full["n_coordinates"],
                                "coordinate_sst_min": full[
                                    "min_coordinate_sst"
                                ],
                                "coordinate_sst_floor": config[
                                    "estimator"
                                ]["coordinate_sst_floor"],
                                "coordinates_below_floor": 0,
                                "alpha_nuisance": nuisance["alpha"],
                                "alpha_full": full["alpha"],
                                "nuisance_sse_total": nuisance[
                                    "total_sse"
                                ],
                                "full_sse_total": full["total_sse"],
                                "sst_total": full["total_sst"],
                                "r2_nuisance_total": nuisance["total_r2"],
                                "r2_full_total": full["total_r2"],
                                "unique_r2_total": (
                                    full["total_r2"]
                                    - nuisance["total_r2"]
                                ),
                                "r2_nuisance_equal_coordinate": nuisance[
                                    "equal_coordinate_r2"
                                ],
                                "r2_full_equal_coordinate": full[
                                    "equal_coordinate_r2"
                                ],
                                "unique_r2_equal_coordinate": (
                                    full["equal_coordinate_r2"]
                                    - nuisance["equal_coordinate_r2"]
                                ),
                            }
                        )

    c3_rows: list[dict[str, Any]] = []
    bridge_alignments = tuple(config["bridge"]["alignments"])
    for seed in config["estimator"]["seeds"]:
        for arm in config["estimator"]["arms"]:
            representation_identity = representation_identity_cache[
                (int(seed), arm)
            ]
            for layer in (
                int(config["estimator"]["primary_layer"]),
                int(config["estimator"]["sensitivity_layer"]),
            ):
                representation_folds = representation_folds_cache[
                    (int(seed), arm, layer)
                ]
                for nuisance_name, scalar in nuisance_variants.items():
                    for fold, static_fold in enumerate(static_folds):
                        train = static_fold["train"]
                        test = static_fold["test"]
                        nuisance_train, nuisance_test = fold_design(
                            scalar, static_fold
                        )
                        representation_fold = representation_folds[fold]
                        retention_train = np.concatenate(
                            (
                                nuisance_train,
                                representation_fold["reduced_train"],
                            ),
                            axis=1,
                        )
                        retention_test = np.concatenate(
                            (
                                nuisance_test,
                                representation_fold["reduced_test"],
                            ),
                            axis=1,
                        )
                        student_start = nuisance_train.shape[1]
                        student_stop = retention_train.shape[1]
                        for alignment in bridge_alignments:
                            contextual = target_folds[alignment][fold]
                            retention = ridge_fit_details(
                                retention_train,
                                contextual["reduced_train"],
                                retention_test,
                                config,
                            )
                            target_pc_contribution = (
                                linear_feature_contribution(
                                    retention,
                                    student_start,
                                    student_stop,
                                )
                            )
                            if target_pc_contribution.shape != (
                                len(test),
                                bridge_target_rank,
                            ):
                                raise ValueError(
                                    "C3 student-to-target contribution shape changed"
                                )
                            student_coefficients = np.asarray(
                                retention["coefficients"][
                                    :, student_start:student_stop
                                ]
                            )
                            for uid in config["substrate"]["valid_uids"]:
                                responses = participant_targets[int(uid)].astype(
                                    np.float32, copy=False
                                )
                                response_model = c1_bridge_models[
                                    (
                                        int(uid),
                                        nuisance_name,
                                        fold,
                                        alignment,
                                    )
                                ]
                                composed = linear_delta_contribution(
                                    target_pc_contribution,
                                    response_model["target_scale"],
                                    response_model["target_coefficients"],
                                )
                                base_prediction = response_model[
                                    "base_prediction"
                                ]
                                base_score = c1_prediction_r2(
                                    responses[test], base_prediction
                                )
                                if not np.array_equal(
                                    base_score["r2"],
                                    response_model["base_r2"],
                                ):
                                    raise AssertionError(
                                        "C3 base score differs from C1 nuisance score"
                                    )
                                bridge_score = c1_prediction_r2(
                                    responses[test],
                                    base_prediction + composed,
                                )
                                bridge_unique = (
                                    bridge_score["r2"] - base_score["r2"]
                                )
                                base_mean = float(
                                    np.mean(
                                        base_score["r2"], dtype=np.float64
                                    )
                                )
                                bridge_mean = float(
                                    np.mean(
                                        bridge_score["r2"], dtype=np.float64
                                    )
                                )
                                c3_rows.append(
                                    {
                                        "uid": int(uid),
                                        "participant_split": participant_split(
                                            config, int(uid)
                                        ),
                                        "seed": int(seed),
                                        "arm": arm,
                                        "layer": layer,
                                        "nuisance_variant": nuisance_name,
                                        "fold": fold,
                                        "representation": alignment,
                                        "test_start": int(test[0]),
                                        "test_stop_exclusive": int(test[-1])
                                        + 1,
                                        "test_count": int(len(test)),
                                        "target_pca_basis_sha256": contextual[
                                            "basis_sha256"
                                        ],
                                        "student_pca_basis_sha256": (
                                            representation_fold[
                                                "basis_sha256"
                                            ]
                                        ),
                                        "static_pca_basis_sha256": (
                                            static_fold["basis_sha256"]
                                        ),
                                        "cache_key": representation_identity[
                                            "cache_key"
                                        ],
                                        "weight_sha256": (
                                            representation_identity[
                                                "weight_sha256"
                                            ]
                                        ),
                                        "representation_cache_sha256": (
                                            representation_identity["sha256"]
                                        ),
                                        "target_component_count": (
                                            bridge_target_rank
                                        ),
                                        "student_component_count": (
                                            bridge_student_rank
                                        ),
                                        "alpha_response_nuisance": (
                                            response_model["alpha_nuisance"]
                                        ),
                                        "alpha_response_full": (
                                            response_model["alpha_full"]
                                        ),
                                        "alpha_target_full": retention["alpha"],
                                        "r2_base_by_roi": base_score[
                                            "r2"
                                        ].tolist(),
                                        "r2_bridge_by_roi": bridge_score[
                                            "r2"
                                        ].tolist(),
                                        "bridge_unique_r2_by_roi": (
                                            bridge_unique.tolist()
                                        ),
                                        "r2_base": base_mean,
                                        "r2_bridge": bridge_mean,
                                        "bridge_unique_r2": (
                                            bridge_mean - base_mean
                                        ),
                                        "response_target_coefficient_l2": float(
                                            np.linalg.norm(
                                                response_model[
                                                    "target_coefficients"
                                                ]
                                            )
                                        ),
                                        "student_target_coefficient_l2": float(
                                            np.linalg.norm(
                                                student_coefficients
                                            )
                                        ),
                                        "target_pc_contribution_l2": float(
                                            np.linalg.norm(
                                                target_pc_contribution
                                            )
                                        ),
                                        "composed_contribution_l2": float(
                                            np.linalg.norm(composed)
                                        ),
                                    }
                                )

    expected_c1 = (
        len(config["substrate"]["valid_uids"])
        * len(nuisance_variants)
        * len(folds)
        * 2
    )
    expected_c2 = (
        len(config["estimator"]["seeds"])
        * len(config["estimator"]["arms"])
        * 2
        * len(nuisance_variants)
        * len(folds)
    )
    expected_c3 = (
        len(config["substrate"]["valid_uids"])
        * len(config["estimator"]["seeds"])
        * len(config["estimator"]["arms"])
        * 2
        * len(nuisance_variants)
        * len(folds)
        * len(bridge_alignments)
    )
    if (
        len(c1_rows) != expected_c1
        or len(c2_rows) != expected_c2
        or len(c3_rows) != expected_c3
    ):
        raise AssertionError("raw score grid is incomplete")
    gates = inherited_gates(config)
    twin_path = path_for(config, "twin_permutation")
    standardization_path = path_for(config, "standardization")
    standardization_manifest_path = path_for(
        config, "standardization_manifest"
    )
    source_identities = {
        name: source_record(config, name)
        for name in (
            "tuckute_csv",
            "e025_manifest",
            "e025_extraction",
            "e025_analysis",
            "e025_nuisance",
            "e025_participant_loader",
        )
    }
    validity = {
        "inputs_hash_valid": True,
        "inputs_finite": True,
        "participant_grid_valid": True,
        "c1_grid_complete": len(c1_rows) == expected_c1,
        "c2_grid_complete": len(c2_rows) == expected_c2,
        "c3_grid_complete": len(c3_rows) == expected_c3,
        "bridge_contributions_finite": all(
            math.isfinite(float(row["bridge_unique_r2"]))
            and math.isfinite(float(row["composed_contribution_l2"]))
            for row in c3_rows
        ),
        "target_pca_basis_reuse_valid": all(
            target_folds["aligned"][fold]["basis_sha256"]
            == target_folds["twin"][fold]["basis_sha256"]
            for fold in range(len(folds))
        ),
        "student_pca_basis_reuse_valid": all(
            len(
                {
                    row["student_pca_basis_sha256"]
                    for row in c2_rows
                    if (
                        int(row["seed"]),
                        row["arm"],
                        int(row["layer"]),
                        int(row["fold"]),
                    )
                    == (int(seed), arm, int(layer), int(fold))
                }
            )
            == 1
            and {
                row["student_pca_basis_sha256"]
                for row in c2_rows
                if (
                    int(row["seed"]),
                    row["arm"],
                    int(row["layer"]),
                    int(row["fold"]),
                )
                == (int(seed), arm, int(layer), int(fold))
            }
            == {
                row["student_pca_basis_sha256"]
                for row in c3_rows
                if (
                    int(row["seed"]),
                    row["arm"],
                    int(row["layer"]),
                    int(row["fold"]),
                )
                == (int(seed), arm, int(layer), int(fold))
            }
            for seed, arm, layer, fold in itertools.product(
                config["estimator"]["seeds"],
                config["estimator"]["arms"],
                (
                    config["estimator"]["primary_layer"],
                    config["estimator"]["sensitivity_layer"],
                ),
                range(len(folds)),
            )
        ),
        "coordinate_floor_valid": all(
            int(row["coordinates_below_floor"]) == 0
            and float(row["coordinate_sst_min"])
            > float(row["coordinate_sst_floor"])
            for row in c2_rows
        ),
        "inherited_gates_valid": bool(gates["all_pass"]),
    }
    validity["all_pass"] = bool(all(validity.values()))
    raw = {
        "schema_version": "e030-exact-substrate-raw.v2",
        "stage": "score",
        "science_status": "RAW FOLD ROWS ONLY",
        "created_at_utc": utc_now(),
        "identity": {
            "protocol_version": config["protocol_version"],
            "config": {
                "path": str(config_path.resolve()),
                "sha256": config_hash,
            },
            "readiness": {
                "path": str(path_for(config, "readiness")),
                "sha256": readiness_hash,
            },
            "bundle": {
                "path": str(path_for(config, "bundle_manifest")),
                "sha256": sha256_file(path_for(config, "bundle_manifest")),
                "bundle_sha256": readiness["bundle"]["bundle_sha256"],
            },
            "design_manifest": {
                "path": str(path_for(config, "design_manifest")),
                "sha256": design_hash,
            },
            "acquisition_manifest": {
                "path": str(acquisition_path),
                "sha256": sha256_file(acquisition_path),
            },
            "runner": {
                "path": str(Path(__file__).resolve()),
                "sha256": sha256_file(Path(__file__).resolve()),
            },
            "analyzer": {
                "path": str(ANALYZER),
                "sha256": sha256_file(ANALYZER),
            },
            "tuckute_csv": {
                "path": source_identities["tuckute_csv"]["path"],
                "sha256": source_identities["tuckute_csv"]["sha256"],
            },
            "e025_manifest": {
                "path": source_identities["e025_manifest"]["path"],
                "sha256": source_identities["e025_manifest"]["sha256"],
            },
            "e025_extraction": {
                "path": source_identities["e025_extraction"]["path"],
                "sha256": source_identities["e025_extraction"]["sha256"],
            },
            "e025_analysis": {
                "path": source_identities["e025_analysis"]["path"],
                "sha256": source_identities["e025_analysis"]["sha256"],
            },
            "e025_nuisance": {
                "path": source_identities["e025_nuisance"]["path"],
                "sha256": source_identities["e025_nuisance"]["sha256"],
            },
            "e025_participant_loader": {
                "path": source_identities["e025_participant_loader"]["path"],
                "sha256": source_identities["e025_participant_loader"]["sha256"],
            },
            "target": {
                "path": target_identity["target"]["path"],
                "sha256": target_identity["target"]["sha256"],
                "targets_array_sha256": acquisition["semantic_sha256"][
                    "targets"
                ],
            },
            "standardization": {
                "npz_path": str(standardization_path),
                "npz_sha256": sha256_file(standardization_path),
                "manifest_path": str(standardization_manifest_path),
                "manifest_sha256": sha256_file(
                    standardization_manifest_path
                ),
            },
            "twin_permutation": {
                "path": str(twin_path),
                "sha256": sha256_file(twin_path),
                "array_sha256": sha256_array(
                    permutation.astype("<i8", copy=False)
                ),
            },
            "ordered_item_sha256": config["substrate"][
                "ordered_item_sha256"
            ],
            "ordered_text_sha256": config["substrate"][
                "ordered_text_sha256"
            ],
            "vertex_index_sha256": acquisition["semantic_sha256"][
                "vertex_index"
            ],
            "tribe_runtime": runtime,
            "scoring_runtime": scoring_runtime,
        },
        "design": {
            "uids": config["substrate"]["valid_uids"],
            "train_uids": config["substrate"]["train_uids"],
            "heldout_uids": config["substrate"]["heldout_uids"],
            "rois": config["substrate"]["rois"],
            "test_blocks": config["folds"]["test_blocks"],
            "nuisance_variants": list(nuisance_variants),
            "primary_nuisance": config["estimator"]["primary_nuisance"],
            "layers": [
                config["estimator"]["primary_layer"],
                config["estimator"]["sensitivity_layer"],
            ],
            "primary_layer": config["estimator"]["primary_layer"],
            "sensitivity_layer": config["estimator"]["sensitivity_layer"],
            "arms": config["estimator"]["arms"],
            "seeds": config["estimator"]["seeds"],
            "pca_rank": rank,
            "ridge_alphas": config["estimator"]["ridge_alphas"],
            "coordinate_sst_floor": config["estimator"][
                "coordinate_sst_floor"
            ],
            "target_dim": config["target"]["target_dim"],
            "bridge": config["bridge"],
        },
        "validity": validity,
        "inherited_gates": {
            **gates["gates"],
            "source_extraction_sha256": gates["extraction"]["sha256"],
        },
        "c1_rows": c1_rows,
        "c2_rows": c2_rows,
        "c3_rows": c3_rows,
    }
    raw["resource_use"] = {
        **measured_resource_use(
            resource_limits,
            started_wall=stage_started_wall,
            started_cpu=stage_started_cpu,
        ),
        "retained_output_dir_bytes_before_write": int(storage_before),
        "retained_output_dir_bytes_projected_after_write": 0,
    }
    for _ in range(8):
        projected = int(storage_before + len(canonical_json_bytes(raw)))
        if (
            raw["resource_use"][
                "retained_output_dir_bytes_projected_after_write"
            ]
            == projected
        ):
            break
        raw["resource_use"][
            "retained_output_dir_bytes_projected_after_write"
        ] = projected
    enforce_retained_storage(
        config, projected_extra_bytes=len(canonical_json_bytes(raw))
    )
    atomic_write_json(raw_path, raw)
    retained_after = enforce_retained_storage(config)
    rss_stop.set()
    rss_thread.join(timeout=1.0)
    return {
        "path": str(raw_path),
        "sha256": sha256_file(raw_path),
        "c1_rows": len(c1_rows),
        "c2_rows": len(c2_rows),
        "c3_rows": len(c3_rows),
        "retained_output_dir_bytes_after_write": int(retained_after),
    }


def synthetic_folds(n_items: int) -> list[tuple[np.ndarray, np.ndarray]]:
    if n_items % 5:
        raise ValueError("synthetic fixture item count must divide into five folds")
    width = n_items // 5
    indices = np.arange(n_items, dtype=np.int64)
    output: list[tuple[np.ndarray, np.ndarray]] = []
    for fold in range(5):
        start = fold * width
        stop = start + width
        output.append(
            (
                np.concatenate((indices[:start], indices[stop:])),
                indices[start:stop],
            )
        )
    return output


def synthetic_twin(n_items: int, key: str) -> np.ndarray:
    permutation = np.full(n_items, -1, dtype=np.int64)
    for fold, (_, test) in enumerate(synthetic_folds(n_items)):
        seed = int.from_bytes(
            hashlib.sha256(f"{key}|{fold}".encode("utf-8")).digest()[:8],
            "little",
        )
        rng = np.random.Generator(np.random.PCG64(seed))
        local = test.copy()
        for index in range(len(local) - 1, 0, -1):
            swap = int(rng.integers(0, index))
            local[index], local[swap] = local[swap], local[index]
        permutation[test] = local
    if np.any(permutation == np.arange(n_items)):
        raise AssertionError("synthetic Sattolo twin has fixed points")
    return permutation


def synthetic_bridge_dataset(
    *, n_items: int, seed: int
) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    predictive = rng.normal(size=(n_items, 4)).astype(np.float32)
    disjoint = rng.normal(size=(n_items, 4)).astype(np.float32)
    scalar = rng.normal(size=(n_items, 3)).astype(np.float32)
    static = rng.normal(size=(n_items, 16)).astype(np.float32)
    predictive_target = (
        predictive
        @ rng.normal(size=(4, 8)).astype(np.float32)
        + rng.normal(scale=0.03, size=(n_items, 8)).astype(np.float32)
    )
    disjoint_target = (
        disjoint
        @ rng.normal(size=(4, 8)).astype(np.float32)
        + rng.normal(scale=0.03, size=(n_items, 8)).astype(np.float32)
    )
    target = np.concatenate((predictive_target, disjoint_target), axis=1)
    target = (
        (target - target.mean(axis=0, keepdims=True))
        / (target.std(axis=0, keepdims=True) + np.float32(1e-6))
    ).astype(np.float32)
    response = (
        predictive @ rng.normal(size=(4, 5)).astype(np.float32)
        + scalar @ rng.normal(scale=0.15, size=(3, 5)).astype(np.float32)
        + rng.normal(scale=0.08, size=(n_items, 5)).astype(np.float32)
    ).astype(np.float32)
    shared_representation = (
        predictive @ rng.normal(size=(4, 48)).astype(np.float32)
        + rng.normal(scale=0.05, size=(n_items, 48)).astype(np.float32)
    ).astype(np.float32)
    disjoint_representation = (
        disjoint @ rng.normal(size=(4, 48)).astype(np.float32)
        + rng.normal(scale=0.05, size=(n_items, 48)).astype(np.float32)
    ).astype(np.float32)
    return {
        "target": target,
        "response": response,
        "scalar": scalar,
        "static": static,
        "shared_representation": shared_representation,
        "disjoint_representation": disjoint_representation,
    }


def synthetic_bridge_fold_score(
    config: dict[str, Any],
    dataset: dict[str, np.ndarray],
    representation_key: str,
    fold: int,
) -> dict[str, Any]:
    target = dataset["target"]
    response = dataset["response"]
    scalar = dataset["scalar"]
    static = dataset["static"]
    representation = dataset[representation_key]
    folds = synthetic_folds(len(target))
    rank = int(config["estimator"]["pca_rank"])
    static_fold = pca_folds(static, folds, rank, config)[fold]
    target_fold = pca_folds(target, folds, rank, config)[fold]
    representation_fold = pca_folds(
        representation, folds, rank, config
    )[fold]
    train = static_fold["train"]
    test = static_fold["test"]
    nuisance_train, nuisance_test = fold_design(scalar, static_fold)
    base = ridge_c1_per_output(
        nuisance_train,
        response[train],
        nuisance_test,
        response[test],
        config,
    )
    response_train = np.concatenate(
        (nuisance_train, target_fold["reduced_train"]), axis=1
    )
    response_test = np.concatenate(
        (nuisance_test, target_fold["reduced_test"]), axis=1
    )
    response_full = ridge_fit_details(
        response_train, response[train], response_test, config
    )
    target_start = nuisance_train.shape[1]
    target_stop = response_train.shape[1]
    retention_train = np.concatenate(
        (nuisance_train, representation_fold["reduced_train"]), axis=1
    )
    retention_test = np.concatenate(
        (nuisance_test, representation_fold["reduced_test"]), axis=1
    )
    retention = ridge_fit_details(
        retention_train,
        target_fold["reduced_train"],
        retention_test,
        config,
    )
    student_start = nuisance_train.shape[1]
    student_stop = retention_train.shape[1]
    target_pc_contribution = linear_feature_contribution(
        retention, student_start, student_stop
    )
    composed = linear_delta_contribution(
        target_pc_contribution,
        response_full["feature_scale"][target_start:target_stop],
        response_full["coefficients"][:, target_start:target_stop],
    )
    bridge = c1_prediction_r2(
        response[test], base["prediction"] + composed
    )
    score = float(
        np.mean(bridge["r2"] - base["r2"], dtype=np.float64)
    )
    fit_signature = {
        "target_train_scores": sha256_array(
            np.asarray(target_fold["reduced_train"])
        ),
        "student_train_scores": sha256_array(
            np.asarray(representation_fold["reduced_train"])
        ),
        "response_coefficients": sha256_array(
            np.asarray(response_full["coefficients"])
        ),
        "response_scale": sha256_array(
            np.asarray(response_full["feature_scale"])
        ),
        "retention_coefficients": sha256_array(
            np.asarray(retention["coefficients"])
        ),
        "retention_scale": sha256_array(
            np.asarray(retention["feature_scale"])
        ),
        "response_alpha": response_full["alpha"],
        "retention_alpha": retention["alpha"],
    }
    return {
        "score": score,
        "fit_signature": fit_signature,
        "composed_sha256": sha256_array(np.asarray(composed)),
    }


def synthetic_fixture(
    config: dict[str, Any],
    *,
    n_items: int,
    target_dim: int,
    n_participants: int,
    n_seeds: int,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    folds = synthetic_folds(n_items)
    latent_dim = 8
    representation_dim = 64
    latent = rng.normal(size=(n_items, latent_dim)).astype(np.float32)
    scalar = rng.normal(size=(n_items, 3)).astype(np.float32)
    static = rng.normal(size=(n_items, 24)).astype(np.float32)
    target_weights = rng.normal(
        scale=0.7, size=(latent_dim, target_dim)
    ).astype(np.float32)
    target = (
        latent @ target_weights
        + rng.normal(scale=0.08, size=(n_items, target_dim))
    ).astype(np.float32)
    target = (
        (target - target.mean(axis=0, keepdims=True))
        / (target.std(axis=0, keepdims=True) + np.float32(1e-6))
    ).astype(np.float32)
    permutation = synthetic_twin(n_items, f"E030-fixture-{seed}")
    twin = target[permutation]
    rank = min(
        int(config["estimator"]["pca_rank"]),
        n_items - n_items // 5 - 1,
    )
    static_folds = pca_folds(static, folds, rank, config)
    paired_target_folds = paired_target_pca_folds(
        target, twin, folds, rank, config
    )
    target_folds = paired_target_folds["aligned"]
    twin_folds = paired_target_folds["twin"]

    participant_a: list[float] = []
    participant_q: list[float] = []
    null_a: list[float] = []
    for _ in range(n_participants):
        response_weights = rng.normal(
            scale=0.8, size=(latent_dim, 5)
        ).astype(np.float32)
        nuisance_weights = rng.normal(
            scale=0.2, size=(3, 5)
        ).astype(np.float32)
        response = (
            latent @ response_weights
            + scalar @ nuisance_weights
            + rng.normal(scale=0.25, size=(n_items, 5))
        ).astype(np.float32)
        null_response = rng.normal(size=(n_items, 5)).astype(np.float32)
        aligned_values: list[float] = []
        twin_values: list[float] = []
        null_values: list[float] = []
        for fold, static_fold in enumerate(static_folds):
            train = static_fold["train"]
            test = static_fold["test"]
            nuisance_train, nuisance_test = fold_design(
                scalar, static_fold
            )
            nuisance = ridge_c1_per_output(
                nuisance_train,
                response[train],
                nuisance_test,
                response[test],
                config,
            )
            null_nuisance = ridge_c1_per_output(
                nuisance_train,
                null_response[train],
                nuisance_test,
                null_response[test],
                config,
            )
            for contextual, destination, response_score in (
                (target_folds[fold], aligned_values, nuisance),
                (twin_folds[fold], twin_values, nuisance),
            ):
                full = ridge_c1_per_output(
                    np.concatenate(
                        (nuisance_train, contextual["reduced_train"]),
                        axis=1,
                    ),
                    response[train],
                    np.concatenate(
                        (nuisance_test, contextual["reduced_test"]),
                        axis=1,
                    ),
                    response[test],
                    config,
                )
                destination.append(
                    float(
                        np.mean(full["r2"] - response_score["r2"])
                    )
                )
            null_full = ridge_c1_per_output(
                np.concatenate(
                    (
                        nuisance_train,
                        target_folds[fold]["reduced_train"],
                    ),
                    axis=1,
                ),
                null_response[train],
                np.concatenate(
                    (
                        nuisance_test,
                        target_folds[fold]["reduced_test"],
                    ),
                    axis=1,
                ),
                null_response[test],
                config,
            )
            null_values.append(
                float(np.mean(null_full["r2"] - null_nuisance["r2"]))
            )
        participant_a.append(float(np.mean(aligned_values)))
        participant_q.append(
            float(np.mean(np.asarray(aligned_values) - np.asarray(twin_values)))
        )
        null_a.append(float(np.mean(null_values)))

    seed_m: list[float] = []
    seed_b: list[float] = []
    for _ in range(n_seeds):
        projection = rng.normal(
            size=(latent_dim, representation_dim)
        ).astype(np.float32)
        kd = (
            0.15 * (latent @ projection)
            + rng.normal(
                scale=1.0, size=(n_items, representation_dim)
            )
        ).astype(np.float32)
        trained = (
            latent @ projection
            + rng.normal(
                scale=0.12, size=(n_items, representation_dim)
            )
        ).astype(np.float32)
        arm_values: dict[str, list[float]] = {"kd_only": [], "tribe_mse": []}
        for arm, representation in (
            ("kd_only", kd),
            ("tribe_mse", trained),
        ):
            representation_folds = pca_folds(
                representation, folds, rank, config
            )
            for fold, static_fold in enumerate(static_folds):
                train = static_fold["train"]
                test = static_fold["test"]
                nuisance_train, nuisance_test = fold_design(
                    scalar, static_fold
                )
                nuisance = ridge_multioutput(
                    nuisance_train,
                    target[train],
                    nuisance_test,
                    target[test],
                    config,
                )
                full = ridge_multioutput(
                    np.concatenate(
                        (
                            nuisance_train,
                            representation_folds[fold]["reduced_train"],
                        ),
                        axis=1,
                    ),
                    target[train],
                    np.concatenate(
                        (
                            nuisance_test,
                            representation_folds[fold]["reduced_test"],
                        ),
                        axis=1,
                    ),
                    target[test],
                    config,
                )
                arm_values[arm].append(
                    full["total_r2"] - nuisance["total_r2"]
                )
        mse = float(np.mean(arm_values["tribe_mse"]))
        kd_value = float(np.mean(arm_values["kd_only"]))
        seed_m.append(mse)
        seed_b.append(mse - kd_value)
    return {
        "A": participant_a,
        "Q": participant_q,
        "null_A": null_a,
        "M": seed_m,
        "B": seed_b,
    }


def run_selftest(config_path: Path) -> dict[str, Any]:
    config, config_hash = load_config(config_path)
    design_hash = sha256_file(path_for(config, "design_manifest"))
    configure_threads(config)
    validate_scoring_runtime(config)
    tests: dict[str, dict[str, Any]] = {}

    first_permutation, _ = sattolo_permutation(config)
    second_permutation, _ = sattolo_permutation(config)
    tests["sattolo"] = {
        "pass": bool(
            np.array_equal(first_permutation, second_permutation)
            and np.all(
                first_permutation
                != np.arange(len(first_permutation), dtype=np.int64)
            )
            and np.array_equal(
                np.sort(first_permutation),
                np.arange(len(first_permutation), dtype=np.int64),
            )
        ),
        "semantic_sha256": sha256_array(first_permutation.astype("<i8")),
    }

    with tempfile.TemporaryDirectory(prefix="e030-source-identity-") as temporary:
        source_path = Path(temporary) / "source.bin"
        original_bytes = b"frozen-source-v1"
        mutated_bytes = b"frozen-source-v2"
        if len(original_bytes) != len(mutated_bytes):
            raise AssertionError("source identity fixture must preserve size")
        source_path.write_bytes(original_bytes)
        frozen_source = {
            "path": str(source_path),
            "sha256": sha256_bytes(original_bytes),
        }
        current_record = require_hash(
            source_path, frozen_source["sha256"], "synthetic frozen source"
        )
        accepted_current = bool(
            require_current_frozen_source_record(
                current_record,
                frozen_source,
                "synthetic frozen source",
            )
            == current_record
        )
        source_path.write_bytes(mutated_bytes)
        same_size_mutation_rejected = False
        try:
            require_current_frozen_source_record(
                current_record,
                frozen_source,
                "synthetic frozen source",
            )
        except ValueError as error:
            same_size_mutation_rejected = "SHA-256 mismatch" in str(error)
        source_path.write_bytes(original_bytes)
        nonexact_record = dict(current_record)
        nonexact_record["path"] = str(source_path.with_name("alias.bin"))
        nonexact_record_rejected = False
        try:
            require_current_frozen_source_record(
                nonexact_record,
                frozen_source,
                "synthetic frozen source",
            )
        except ValueError as error:
            nonexact_record_rejected = "identity is stale" in str(error)
    tests["live_source_rehash"] = {
        "pass": bool(
            accepted_current
            and same_size_mutation_rejected
            and nonexact_record_rejected
        ),
        "accepted_current": accepted_current,
        "same_size_mutation_rejected": same_size_mutation_rejected,
        "nonexact_record_rejected": nonexact_record_rejected,
    }

    rng = np.random.default_rng(30031)
    x_train = rng.normal(size=(80, 12)).astype(np.float32)
    x_test = rng.normal(size=(20, 12)).astype(np.float32)
    y_train = rng.normal(size=(80, 5)).astype(np.float32)
    y_test = rng.normal(size=(20, 5)).astype(np.float32)
    ours = ridge_c1_per_output(
        x_train, y_train, x_test, y_test, config
    )
    sys.path.insert(0, str(ROOT / "scripts"))
    import e025_participant_transfer as e025

    expected = e025._ridge_r2(
        x_train,
        y_train,
        x_test,
        y_test,
        tuple(float(value) for value in config["estimator"]["ridge_alphas"]),
    )
    tests["e025_ridge_equivalence"] = {
        "pass": bool(np.array_equal(ours["r2"], expected)),
        "max_abs_error": float(np.max(np.abs(ours["r2"] - expected))),
        "scalar_alpha": bool(np.ndim(ours["alpha"]) == 0),
    }

    coefficient_fit = ridge_fit_details(
        x_train, y_train, x_test, config
    )
    feature_split = 5
    first_contribution = linear_feature_contribution(
        coefficient_fit, 0, feature_split
    )
    second_contribution = linear_feature_contribution(
        coefficient_fit, feature_split, x_train.shape[1]
    )
    constant = (
        coefficient_fit["intercept"] + coefficient_fit["y_mean"]
    )
    reconstructed = constant + first_contribution + second_contribution
    delta = rng.normal(scale=0.2, size=(len(x_test), feature_split)).astype(
        np.float32
    )
    perturbed = x_test.copy()
    perturbed[:, :feature_split] += delta
    perturbed_standardized = (
        (perturbed - coefficient_fit["feature_mean"])
        / coefficient_fit["feature_scale"]
    )
    perturbed_prediction = (
        perturbed_standardized @ coefficient_fit["coefficients"].T
        + constant
    )
    delta_prediction = linear_delta_contribution(
        delta,
        coefficient_fit["feature_scale"][:feature_split],
        coefficient_fit["coefficients"][:, :feature_split],
    )
    tests["coefficient_contributions"] = {
        "pass": bool(
            np.allclose(
                reconstructed,
                coefficient_fit["prediction"],
                rtol=1e-6,
                atol=1e-7,
            )
            and np.allclose(
                perturbed_prediction - coefficient_fit["prediction"],
                delta_prediction,
                rtol=1e-6,
                atol=1e-7,
            )
        ),
        "isolated_block_reconstruction_max_abs_error": float(
            np.max(np.abs(reconstructed - coefficient_fit["prediction"]))
        ),
        "delta_composition_max_abs_error": float(
            np.max(
                np.abs(
                    perturbed_prediction
                    - coefficient_fit["prediction"]
                    - delta_prediction
                )
            )
        ),
    }

    features = rng.normal(size=(100, 20)).astype(np.float32)
    folds = synthetic_folds(100)
    original = pca_folds(features, folds, 10, config)
    modified_features = features.copy()
    modified_features[folds[0][1]] += np.float32(1000.0)
    modified = pca_folds(modified_features, folds, 10, config)
    tests["train_only_pca"] = {
        "pass": bool(
            np.allclose(
                original[0]["reduced_train"],
                modified[0]["reduced_train"],
                atol=0,
                rtol=0,
            )
            and not np.allclose(
                original[0]["reduced_test"],
                modified[0]["reduced_test"],
            )
        )
    }

    paired_features = rng.normal(size=(100, 64)).astype(np.float32)
    paired_permutation = synthetic_twin(100, "E030-basis-reuse-selftest")
    paired_twin = paired_features[paired_permutation]
    paired = paired_target_pca_folds(
        paired_features, paired_twin, folds, 10, config
    )
    independent_aligned = pca_folds(
        paired_features, folds, 10, config
    )
    row_multiset = lambda value: sorted(
        sha256_bytes(np.ascontiguousarray(row).tobytes())
        for row in np.asarray(value)
    )
    same_basis = all(
        paired["aligned"][fold]["basis_sha256"]
        == paired["twin"][fold]["basis_sha256"]
        == independent_aligned[fold]["basis_sha256"]
        for fold in range(5)
    )
    same_multiset_scores = all(
        row_multiset(paired["aligned"][fold]["reduced_train"])
        == row_multiset(paired["twin"][fold]["reduced_train"])
        for fold in range(5)
    )
    perturbed_twin = paired_twin.copy()
    perturbed_twin += np.float32(500.0)
    paired_perturbed = paired_target_pca_folds(
        paired_features, perturbed_twin, folds, 10, config
    )
    twin_cannot_change_basis = all(
        paired["aligned"][fold]["basis_sha256"]
        == paired_perturbed["aligned"][fold]["basis_sha256"]
        and np.array_equal(
            paired["aligned"][fold]["reduced_train"],
            paired_perturbed["aligned"][fold]["reduced_train"],
        )
        and np.array_equal(
            paired["aligned"][fold]["reduced_test"],
            paired_perturbed["aligned"][fold]["reduced_test"],
        )
        for fold in range(5)
    )
    tests["paired_target_pca_basis_reuse"] = {
        "pass": bool(
            same_basis and same_multiset_scores and twin_cannot_change_basis
        ),
        "same_basis_hash": same_basis,
        "same_multiset_train_scores": same_multiset_scores,
        "twin_perturbation_cannot_change_aligned_basis": (
            twin_cannot_change_basis
        ),
    }

    reference = rng.normal(size=(200, 16)).astype(np.float32)
    evaluation_a = rng.normal(size=(20, 16)).astype(np.float32)
    evaluation_b = evaluation_a + np.float32(100.0)
    mean = reference.mean(axis=0, keepdims=True).astype(np.float32)
    std = (
        reference.std(axis=0, keepdims=True) + np.float32(1e-6)
    ).astype(np.float32)
    import run_tribe_phase3 as phase3

    _, e016_mean, e016_std = phase3.standardize_train(reference)
    mean_hash = sha256_array(mean)
    _ = ((evaluation_a - mean) / std).astype(np.float32)
    _ = ((evaluation_b - mean) / std).astype(np.float32)
    tests["external_standardization"] = {
        "pass": bool(
            mean_hash == sha256_array(mean)
            and np.array_equal(mean, e016_mean)
            and np.array_equal(std, e016_std)
            and sha256_array(std)
            == sha256_array(
                (
                    reference.std(axis=0, keepdims=True)
                    + np.float32(1e-6)
                ).astype(np.float32)
            )
        )
    }

    prediction_args = target_prediction_args(config)
    tests["target_generator_argument_contract"] = {
        "pass": bool(
            vars(prediction_args)
            == {
                "word_duration": float(config["target"]["word_duration"]),
                "word_gap": float(config["target"]["word_gap"]),
                "min_duration": float(config["target"]["min_duration"]),
                "quiet": True,
            }
        ),
        "required_fields": sorted(vars(prediction_args)),
    }

    bridge_dataset = synthetic_bridge_dataset(n_items=100, seed=30033)
    shared_scores = [
        synthetic_bridge_fold_score(
            config, bridge_dataset, "shared_representation", fold
        )["score"]
        for fold in range(5)
    ]
    disjoint_scores = [
        synthetic_bridge_fold_score(
            config, bridge_dataset, "disjoint_representation", fold
        )["score"]
        for fold in range(5)
    ]
    shared_mean = float(np.mean(shared_scores))
    disjoint_mean = float(np.mean(disjoint_scores))
    tests["shared_subspace_bridge"] = {
        "pass": bool(shared_mean > 0.05),
        "fold_scores": shared_scores,
        "mean": shared_mean,
    }
    tests["disjoint_subspace_control"] = {
        "pass": bool(shared_mean > disjoint_mean + 0.05),
        "fold_scores": disjoint_scores,
        "mean": disjoint_mean,
        "shared_minus_disjoint": shared_mean - disjoint_mean,
    }

    original_bridge = synthetic_bridge_fold_score(
        config, bridge_dataset, "shared_representation", 0
    )
    perturbed_dataset = {
        key: value.copy() for key, value in bridge_dataset.items()
    }
    heldout = synthetic_folds(100)[0][1]
    perturbed_dataset["target"][heldout] += np.float32(100.0)
    perturbed_dataset["response"][heldout] -= np.float32(50.0)
    perturbed_dataset["shared_representation"][heldout] += np.float32(
        200.0
    )
    perturbed_bridge = synthetic_bridge_fold_score(
        config, perturbed_dataset, "shared_representation", 0
    )
    tests["bridge_train_only_no_leakage"] = {
        "pass": bool(
            original_bridge["fit_signature"]
            == perturbed_bridge["fit_signature"]
            and original_bridge["composed_sha256"]
            != perturbed_bridge["composed_sha256"]
            and not math.isclose(
                original_bridge["score"],
                perturbed_bridge["score"],
                rel_tol=0.0,
                abs_tol=0.0,
            )
        ),
        "fit_signature_unchanged": bool(
            original_bridge["fit_signature"]
            == perturbed_bridge["fit_signature"]
        ),
        "heldout_contribution_changed": bool(
            original_bridge["composed_sha256"]
            != perturbed_bridge["composed_sha256"]
        ),
    }

    fixture_one = synthetic_fixture(
        config,
        n_items=100,
        target_dim=64,
        n_participants=3,
        n_seeds=2,
        seed=30032,
    )
    fixture_two = synthetic_fixture(
        config,
        n_items=100,
        target_dim=64,
        n_participants=3,
        n_seeds=2,
        seed=30032,
    )
    deterministic = canonical_json_bytes(fixture_one) == canonical_json_bytes(
        fixture_two
    )
    directional = bool(
        min(fixture_one["A"]) > 0
        and min(fixture_one["Q"]) > 0
        and min(fixture_one["M"]) > 0
        and min(fixture_one["B"]) > 0
        and np.mean(fixture_one["A"])
        > np.mean(fixture_one["null_A"])
    )
    tests["synthetic_recovery"] = {
        "pass": bool(deterministic and directional),
        "deterministic": deterministic,
        "directional": directional,
        "fixture_sha256": sha256_bytes(canonical_json_bytes(fixture_one)),
        "summary": {
            key: float(np.mean(value))
            for key, value in fixture_one.items()
        },
    }

    report = {
        "schema_version": "e030-selftest.v2",
        "science_status": "SYNTHETIC ONLY: no E030 target or response was opened",
        "config_sha256": config_hash,
        "design_manifest_sha256": design_hash,
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "analyzer_sha256": sha256_file(ANALYZER),
        "pass": bool(all(value["pass"] for value in tests.values())),
        "tests": tests,
        "peak_rss_kib": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }
    atomic_write_json(path_for(config, "selftest_report"), report)
    if not report["pass"]:
        raise AssertionError("E030 selftest failed")
    return report


def run_benchmark(config_path: Path) -> dict[str, Any]:
    config, config_hash = load_config(config_path)
    design_hash = sha256_file(path_for(config, "design_manifest"))
    configure_threads(config)
    validate_scoring_runtime(config)
    benchmark = config["benchmark"]
    started = time.perf_counter()
    started_cpu = process_cpu_seconds()
    fixture = synthetic_fixture(
        config,
        n_items=int(benchmark["n_items"]),
        target_dim=int(benchmark["target_dim"]),
        n_participants=int(benchmark["n_participants"]),
        n_seeds=int(benchmark["n_seeds"]),
        seed=int(benchmark["seed"]),
    )
    fixture_elapsed = time.perf_counter() - started
    fixture_cpu = process_cpu_seconds() - started_cpu
    directional = bool(
        min(fixture["A"]) > 0
        and min(fixture["Q"]) > 0
        and min(fixture["M"]) > 0
        and min(fixture["B"]) > 0
    )
    bridge_started = time.perf_counter()
    bridge_started_cpu = process_cpu_seconds()
    bridge_dataset = synthetic_bridge_dataset(
        n_items=int(benchmark["n_items"]),
        seed=int(benchmark["seed"]) + 2,
    )
    shared_bridge = [
        synthetic_bridge_fold_score(
            config, bridge_dataset, "shared_representation", fold
        )["score"]
        for fold in range(5)
    ]
    disjoint_bridge = [
        synthetic_bridge_fold_score(
            config, bridge_dataset, "disjoint_representation", fold
        )["score"]
        for fold in range(5)
    ]
    bridge_elapsed = time.perf_counter() - bridge_started
    bridge_cpu = process_cpu_seconds() - bridge_started_cpu
    bridge_shared_mean = float(np.mean(shared_bridge))
    bridge_disjoint_mean = float(np.mean(disjoint_bridge))
    bridge_directional = bool(
        bridge_shared_mean > 0.05
        and bridge_shared_mean > bridge_disjoint_mean + 0.05
    )

    full = benchmark["full_shape_single_fit"]
    rng = np.random.default_rng(int(benchmark["seed"]) + 1)
    n_items = int(full["n_items"])
    target_dim = int(full["target_dim"])
    predictor_dim = int(full["predictor_dim"])
    latent = rng.normal(size=(n_items, 12)).astype(np.float32)
    predictors = rng.normal(
        size=(n_items, predictor_dim)
    ).astype(np.float32)
    weights = rng.normal(
        scale=0.2, size=(12, target_dim)
    ).astype(np.float32)
    targets = (
        latent @ weights
        + rng.normal(scale=0.5, size=(n_items, target_dim))
    ).astype(np.float32)
    train, test = synthetic_folds(n_items)[0]
    full_started = time.perf_counter()
    full_started_cpu = process_cpu_seconds()
    full_result = ridge_multioutput(
        predictors[train],
        targets[train],
        predictors[test],
        targets[test],
        config,
    )
    full_elapsed = time.perf_counter() - full_started
    full_cpu = process_cpu_seconds() - full_started_cpu

    response_targets = rng.normal(size=(n_items, 5)).astype(np.float32)
    c1_started = time.perf_counter()
    c1_started_cpu = process_cpu_seconds()
    c1_result = ridge_c1_per_output(
        predictors[train],
        response_targets[train],
        predictors[test],
        response_targets[test],
        config,
    )
    c1_wall = time.perf_counter() - c1_started
    c1_cpu = process_cpu_seconds() - c1_started_cpu

    bridge_rank = int(config["bridge"]["target_pca_rank"])
    bridge_targets = rng.normal(size=(n_items, bridge_rank)).astype(np.float32)
    retention_started = time.perf_counter()
    retention_started_cpu = process_cpu_seconds()
    retention_result = ridge_fit_details(
        predictors[train],
        bridge_targets[train],
        predictors[test],
        config,
    )
    retention_wall = time.perf_counter() - retention_started
    retention_cpu = process_cpu_seconds() - retention_started_cpu

    from sklearn.decomposition import PCA

    pca_model = PCA(
        n_components=int(config["estimator"]["pca_rank"]),
        svd_solver=config["estimator"]["pca_svd_solver"],
        whiten=bool(config["estimator"]["pca_whiten"]),
        random_state=int(config["estimator"]["pca_random_state"]),
    )
    pca_started = time.perf_counter()
    pca_started_cpu = process_cpu_seconds()
    pca_train = pca_model.fit_transform(targets[train])
    pca_test = pca_model.transform(targets[test])
    pca_wall = time.perf_counter() - pca_started
    pca_cpu = process_cpu_seconds() - pca_started_cpu

    composition_repetitions = int(benchmark["composition_repetitions"])
    composition_delta = rng.normal(size=(len(test), bridge_rank)).astype(
        np.float32
    )
    composition_scale = np.maximum(
        rng.lognormal(size=bridge_rank).astype(np.float32), np.float32(1e-4)
    )
    composition_coefficients = rng.normal(size=(5, bridge_rank)).astype(
        np.float32
    )
    composition_response = rng.normal(size=(len(test), 5)).astype(np.float32)
    composition_base = rng.normal(size=(len(test), 5)).astype(np.float32)
    composition_started = time.perf_counter()
    composition_started_cpu = process_cpu_seconds()
    composition_score: dict[str, Any] | None = None
    for _ in range(composition_repetitions):
        composition = linear_delta_contribution(
            composition_delta, composition_scale, composition_coefficients
        )
        composition_score = c1_prediction_r2(
            composition_response, composition_base + composition
        )
    composition_wall_total = time.perf_counter() - composition_started
    composition_cpu_total = process_cpu_seconds() - composition_started_cpu
    composition_wall = composition_wall_total / composition_repetitions
    composition_cpu = composition_cpu_total / composition_repetitions

    grid_started = time.perf_counter()
    grid_started_cpu = process_cpu_seconds()
    uids = config["substrate"]["valid_uids"]
    nuisances = config["estimator"]["nuisance_variants"]
    folds = range(int(config["folds"]["count"]))
    seeds = config["estimator"]["seeds"]
    arms = config["estimator"]["arms"]
    layers = (
        config["estimator"]["primary_layer"],
        config["estimator"]["sensitivity_layer"],
    )
    alignments = config["bridge"]["alignments"]
    c1_grid = list(itertools.product(uids, nuisances, folds, alignments))
    c2_grid = list(itertools.product(seeds, arms, layers, nuisances, folds))
    c3_grid = list(
        itertools.product(
            uids, seeds, arms, layers, nuisances, folds, alignments
        )
    )
    exact_counts = {
        "c1_rows": len(c1_grid),
        "c2_rows": len(c2_grid),
        "c3_rows": len(c3_grid),
        "c1_model_fits": len(uids) * len(nuisances) * len(folds) * 3,
        "c2_model_fits": len(nuisances) * len(folds) + len(c2_grid),
        "c3_retention_fits": (
            len(seeds)
            * len(arms)
            * len(layers)
            * len(nuisances)
            * len(folds)
            * len(alignments)
        ),
        "c3_composition_scores": len(c3_grid),
        "pca_fits": (
            len(folds)
            + len(folds)
            + len(seeds) * len(arms) * len(layers) * len(folds)
        ),
    }
    expected_counts = benchmark["exact_v2_grid"]
    grid_complete = bool(
        exact_counts == expected_counts
        and len(c1_grid) == len(set(c1_grid))
        and len(c2_grid) == len(set(c2_grid))
        and len(c3_grid) == len(set(c3_grid))
    )
    grid_elapsed = time.perf_counter() - grid_started
    grid_cpu = process_cpu_seconds() - grid_started_cpu
    primitive_measurements = {
        "c1_model_fits": {
            "count": int(exact_counts["c1_model_fits"]),
            "cpu_seconds_per_operation": float(c1_cpu),
            "wall_seconds_per_operation": float(c1_wall),
            "measurement": "one production-shape 103-predictor, five-output ridge fit",
        },
        "full_target_fits": {
            "count": int(exact_counts["c2_model_fits"]),
            "cpu_seconds_per_operation": float(full_cpu),
            "wall_seconds_per_operation": float(full_elapsed),
            "measurement": "one production-shape 103-predictor, 20,484-output ridge fit",
        },
        "bridge_retention_fits": {
            "count": int(exact_counts["c3_retention_fits"]),
            "cpu_seconds_per_operation": float(retention_cpu),
            "wall_seconds_per_operation": float(retention_wall),
            "measurement": "one production-shape 103-predictor, 50-target-PC ridge fit",
        },
        "composition_scores": {
            "count": int(exact_counts["c3_composition_scores"]),
            "cpu_seconds_per_operation": float(composition_cpu),
            "wall_seconds_per_operation": float(composition_wall),
            "measurement": (
                "mean of repeated production-fold 50-PC to five-ROI "
                "compositions plus response scoring"
            ),
            "measurement_repetitions": composition_repetitions,
        },
        "pca_fits": {
            "count": int(exact_counts["pca_fits"]),
            "cpu_seconds_per_operation": float(pca_cpu),
            "wall_seconds_per_operation": float(pca_wall),
            "measurement": (
                "one worst-case production-shape 20,484-coordinate train-fit "
                "and heldout transform"
            ),
        },
    }
    for measurement in primitive_measurements.values():
        measurement["projected_cpu_seconds"] = float(
            measurement["count"] * measurement["cpu_seconds_per_operation"]
        )
        measurement["projected_wall_seconds"] = float(
            measurement["count"] * measurement["wall_seconds_per_operation"]
        )
    conservative_projected_cpu_seconds = float(
        sum(
            row["projected_cpu_seconds"]
            for row in primitive_measurements.values()
        )
    )
    conservative_projected_wall_seconds = float(
        sum(
            row["projected_wall_seconds"]
            for row in primitive_measurements.values()
        )
    )
    scoring_cpu_ceiling_seconds = (
        float(config["compute_ceiling"]["scoring_cpu_hours"]) * 3600.0
    )
    primitive_measurements_valid = bool(
        all(
            math.isfinite(float(row[field])) and float(row[field]) > 0
            for row in primitive_measurements.values()
            for field in (
                "cpu_seconds_per_operation",
                "wall_seconds_per_operation",
                "projected_cpu_seconds",
                "projected_wall_seconds",
            )
        )
        and np.isfinite(c1_result["r2"]).all()
        and np.isfinite(retention_result["prediction"]).all()
        and np.isfinite(pca_train).all()
        and np.isfinite(pca_test).all()
        and composition_score is not None
        and np.isfinite(composition_score["r2"]).all()
    )
    peak_kib = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    ram_ceiling_kib = int(
        float(config["compute_ceiling"]["scoring_ram_gb"]) * 1024 * 1024
    )
    report = {
        "schema_version": "e030-benchmark.v3",
        "science_status": "SYNTHETIC ONLY: no E030 target or response was opened",
        "config_sha256": config_hash,
        "design_manifest_sha256": design_hash,
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "analyzer_sha256": sha256_file(ANALYZER),
        "pass": bool(
            directional
            and bridge_directional
            and np.isfinite(full_result["total_r2"])
            and peak_kib < ram_ceiling_kib
            and grid_complete
            and primitive_measurements_valid
            and conservative_projected_cpu_seconds
            <= scoring_cpu_ceiling_seconds
        ),
        "fixture": {
            "n_items": int(benchmark["n_items"]),
            "target_dim": int(benchmark["target_dim"]),
            "n_participants": int(benchmark["n_participants"]),
            "n_seeds": int(benchmark["n_seeds"]),
            "wall_seconds": float(fixture_elapsed),
            "cpu_seconds": float(fixture_cpu),
            "deterministic_sha256": sha256_bytes(
                canonical_json_bytes(fixture)
            ),
            "directional_recovery": directional,
        },
        "bridge_fixture": {
            "n_items": int(benchmark["n_items"]),
            "wall_seconds": float(bridge_elapsed),
            "cpu_seconds": float(bridge_cpu),
            "shared_fold_scores": shared_bridge,
            "disjoint_fold_scores": disjoint_bridge,
            "shared_mean": bridge_shared_mean,
            "disjoint_mean": bridge_disjoint_mean,
            "shared_minus_disjoint": (
                bridge_shared_mean - bridge_disjoint_mean
            ),
            "directional_recovery": bridge_directional,
        },
        "full_shape_single_fit": {
            "n_items": n_items,
            "target_dim": target_dim,
            "predictor_dim": predictor_dim,
            "wall_seconds": float(full_elapsed),
            "cpu_seconds": float(full_cpu),
            "selected_alpha": full_result["alpha"],
            "finite": bool(np.isfinite(full_result["total_r2"])),
        },
        "exact_v2_factor_grid": {
            "claim": benchmark["claim"],
            "benchmark_n_items": int(benchmark["n_items"]),
            "benchmark_target_dim": int(benchmark["target_dim"]),
            "counts": exact_counts,
            "expected_counts": expected_counts,
            "unique_and_complete": grid_complete,
            "enumeration_wall_seconds": float(grid_elapsed),
            "enumeration_cpu_seconds": float(grid_cpu),
            "c1_grid_sha256": sha256_bytes(canonical_json_bytes(c1_grid)),
            "c2_grid_sha256": sha256_bytes(canonical_json_bytes(c2_grid)),
            "c3_grid_sha256": sha256_bytes(canonical_json_bytes(c3_grid)),
        },
        "conservative_production_projection": {
            "claim_boundary": (
                "not a timed full-grid run; each exact production operation "
                "category is charged its separately measured conservative "
                "production-shape CPU and wall primitive"
            ),
            "primitive_measurements": primitive_measurements,
            "primitive_measurements_valid": primitive_measurements_valid,
            "projected_cpu_seconds": float(
                conservative_projected_cpu_seconds
            ),
            "projected_wall_seconds": float(
                conservative_projected_wall_seconds
            ),
            "scoring_cpu_ceiling_seconds": float(
                scoring_cpu_ceiling_seconds
            ),
            "within_ceiling": bool(
                conservative_projected_cpu_seconds
                <= scoring_cpu_ceiling_seconds
            ),
        },
        "peak_rss_kib": peak_kib,
        "ram_ceiling_kib": ram_ceiling_kib,
    }
    atomic_write_json(path_for(config, "benchmark_report"), report)
    if not report["pass"]:
        raise AssertionError("E030 benchmark failed")
    return report


def write_bundle(config_path: Path) -> dict[str, Any]:
    config, _ = load_config(config_path)
    bundle = bundle_manifest(config_path)
    atomic_write_json(path_for(config, "bundle_manifest"), bundle)
    return bundle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("manifest")
    subparsers.add_parser("selftest")
    subparsers.add_parser("benchmark")
    smoke = subparsers.add_parser("smoke-replay")
    smoke.add_argument("--gpu", default="1")
    subparsers.add_parser("standardizer")
    subparsers.add_parser("bundle")
    subparsers.add_parser("seal-readiness")
    target = subparsers.add_parser("target")
    target.add_argument("--gpu", default="1")
    worker = subparsers.add_parser("target-worker")
    worker.add_argument("--out", type=Path, required=True)
    subparsers.add_parser("score")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = args.config.resolve()
    if args.command == "manifest":
        run_manifest(config_path)
        config, _ = load_config(config_path)
        output = path_for(config, "design_manifest")
    elif args.command == "selftest":
        run_selftest(config_path)
        config, _ = load_config(config_path)
        output = path_for(config, "selftest_report")
    elif args.command == "benchmark":
        run_benchmark(config_path)
        config, _ = load_config(config_path)
        output = path_for(config, "benchmark_report")
    elif args.command == "smoke-replay":
        run_smoke_replay(config_path, args.gpu)
        config, _ = load_config(config_path)
        output = path_for(config, "smoke_report")
    elif args.command == "standardizer":
        run_standardizer(config_path)
        config, _ = load_config(config_path)
        output = path_for(config, "standardization_manifest")
    elif args.command == "bundle":
        write_bundle(config_path)
        config, _ = load_config(config_path)
        output = path_for(config, "bundle_manifest")
    elif args.command == "seal-readiness":
        seal_readiness(config_path)
        config, _ = load_config(config_path)
        output = path_for(config, "readiness")
    elif args.command == "target":
        run_target(config_path, args.gpu)
        config, _ = load_config(config_path)
        output = path_for(config, "acquisition_manifest")
    elif args.command == "target-worker":
        run_target_worker(config_path, args.out.resolve())
        return
    elif args.command == "score":
        run_score(config_path)
        config, _ = load_config(config_path)
        output = path_for(config, "raw_scores")
    else:
        raise AssertionError(args.command)
    print(f"saved {output} sha256={sha256_file(output)}", flush=True)


if __name__ == "__main__":
    main()
