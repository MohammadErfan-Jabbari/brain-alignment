#!/usr/bin/env python3
"""E031 biological-target information recovery.

``selftest`` and ``manifest`` are outcome-blind. Biological stages remain
fail-closed until the locked configuration explicitly enables endpoint compute.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import sys
import tempfile
import wave
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import h5py
import numpy as np
from numpy.lib import format as npy_format


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "configs/e031_biological_target_information_recovery.json"
BLOCKED_STAGES = {"c1", "c2-build", "c2-score", "analyze"}
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_array(values: np.ndarray) -> str:
    array = np.ascontiguousarray(values)
    payload = (
        canonical_json({"dtype": str(array.dtype), "shape": list(array.shape)}).encode("utf-8")
        + b"\0"
        + array.tobytes(order="C")
    )
    return sha256_bytes(payload)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def atomic_savez(path: Path, arrays: dict[str, np.ndarray]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".npz", dir=path.parent)
    os.close(handle)
    try:
        np.savez_compressed(temporary, **arrays)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load_config(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("experiment") != "E031":
        raise ValueError("configuration is not E031")
    allowed_statuses = {"DESIGN_HOLD", "IMPLEMENTATION_AUTHORIZED", "READY_TO_RUN"}
    if payload.get("science_status") not in allowed_statuses:
        raise ValueError(f"unrecognized E031 science_status: {payload.get('science_status')!r}")
    endpoint_allowed = payload.get("authorization", {}).get("endpoint_compute_allowed")
    if endpoint_allowed not in {True, False}:
        raise ValueError("authorization.endpoint_compute_allowed must be boolean")
    if endpoint_allowed and payload.get("science_status") != "READY_TO_RUN":
        raise ValueError("endpoint computation requires science_status=READY_TO_RUN")
    return payload


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def require_equal(observed: Any, expected: Any, label: str) -> None:
    if observed != expected:
        raise ValueError(f"{label}: observed {observed!r}, expected {expected!r}")


def file_record(spec: dict[str, Any]) -> dict[str, Any]:
    path = resolve_path(spec["path"])
    if not path.is_file():
        raise FileNotFoundError(path)
    observed_size = path.stat().st_size
    observed_hash = sha256_file(path)
    if "bytes" in spec:
        require_equal(observed_size, int(spec["bytes"]), f"{path} byte count")
    require_equal(observed_hash, spec["sha256"], f"{path} SHA-256")
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "bytes": observed_size,
        "sha256": observed_hash,
    }


def npz_headers(path: Path) -> dict[str, dict[str, Any]]:
    """Read NPY headers inside an NPZ without loading array payloads."""
    records: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(path) as archive:
        for member in sorted(archive.namelist()):
            if not member.endswith(".npy"):
                continue
            with archive.open(member) as handle:
                version = npy_format.read_magic(handle)
                if version == (1, 0):
                    shape, fortran, dtype = npy_format.read_array_header_1_0(handle)
                elif version in {(2, 0), (3, 0)}:
                    shape, fortran, dtype = npy_format.read_array_header_2_0(handle)
                else:
                    raise ValueError(f"unsupported NPY version {version} in {path}")
            records[member[:-4]] = {
                "shape": list(shape),
                "dtype": str(dtype),
                "fortran_order": bool(fortran),
            }
    return records


def representation_metadata(path: Path) -> dict[str, Any]:
    """Read only the small JSON metadata scalar from a representation cache."""
    with np.load(path, allow_pickle=False) as cached:
        if "metadata_json" not in cached.files:
            raise ValueError(f"{path} lacks metadata_json")
        return json.loads(str(cached["metadata_json"].item()))


def validate_c1_biological_inputs(config: dict[str, Any]) -> dict[str, Any]:
    """Bind C1 response, participant/ROI, nuisance, and loader identities."""
    c1 = config["c1"]
    specs = c1["biological_inputs"]
    records = {
        name: file_record(specs[name])
        for name in ("e025_manifest", "response_csv", "nuisance_cache", "loader")
    }
    e025 = json.loads(resolve_path(specs["e025_manifest"]["path"]).read_text(encoding="utf-8"))
    tuckute = e025.get("tuckute", {})
    require_equal(
        str(Path(tuckute.get("source", {}).get("path", "")).resolve().relative_to(REPO_ROOT)),
        specs["response_csv"]["path"],
        "Tuckute response path in E025 manifest",
    )
    require_equal(tuckute.get("source", {}).get("sha256"), specs["response_csv"]["sha256"], "response hash")
    for key in (
        "condition",
        "ordered_item_count",
        "ordered_item_id_sha256",
        "rois",
        "covariate_columns",
    ):
        expected_key = "valid_participants" if key == "valid_uids" else key
        require_equal(tuckute.get(key), specs[expected_key], f"Tuckute {key}")
    require_equal(tuckute.get("ordered_text_sha256"), c1["ordered_text_sha256"], "Tuckute text order")
    require_equal(tuckute.get("valid_uids"), specs["valid_participants"], "Tuckute valid participants")
    require_equal(tuckute.get("excluded_uid", {}).get("uid"), c1["excluded_participant"], "excluded UID")
    require_equal(tuckute.get("excluded_uid", {}).get("included"), False, "excluded UID flag")
    require_equal(tuckute.get("covariates_complete"), True, "Tuckute covariate completeness")

    expected_source = set(c1["source_participants"])
    expected_evaluation = set(c1["evaluation_participants"])
    participant_records = tuckute.get("participants", [])
    require_equal(
        {int(row["uid"]) for row in participant_records},
        set(specs["valid_participants"]),
        "participant identity set",
    )
    for row in participant_records:
        uid = int(row["uid"])
        expected_split = "train" if uid in expected_source else "heldout"
        if uid not in expected_source | expected_evaluation:
            raise ValueError(f"unexpected C1 participant {uid}")
        require_equal(row.get("split"), expected_split, f"participant {uid} split")
        require_equal(row.get("complete"), True, f"participant {uid} completeness")
        require_equal(row.get("n_source_rows"), 5000, f"participant {uid} source rows")
        require_equal(row.get("n_item_roi_cells"), 5000, f"participant {uid} item/ROI cells")
        require_equal(row.get("duplicate_item_roi_cells"), 0, f"participant {uid} duplicate cells")
        require_equal(row.get("nonfinite_responses"), 0, f"participant {uid} nonfinite responses")

    nuisance_path = resolve_path(specs["nuisance_cache"]["path"])
    nuisance_headers = npz_headers(nuisance_path)
    nuisance_metadata = representation_metadata(nuisance_path)
    expected_keys = set(specs["nuisance_arrays"]) | {"metadata_json"}
    require_equal(set(nuisance_headers), expected_keys, "nuisance cache keys")
    for key, expected in specs["nuisance_arrays"].items():
        require_equal(nuisance_headers[key]["shape"], expected["shape"], f"nuisance {key} shape")
        require_equal(nuisance_headers[key]["dtype"], expected["dtype"], f"nuisance {key} dtype")
        require_equal(
            nuisance_metadata.get("array_sha256", {}).get(key),
            expected["sha256"],
            f"nuisance {key} declared hash",
        )
    require_equal(
        nuisance_metadata.get("ordered_text_sha256"),
        c1["ordered_text_sha256"],
        "nuisance ordered text",
    )
    require_equal(nuisance_metadata.get("row_count"), c1["rows"], "nuisance row count")
    require_equal(nuisance_metadata.get("reference_model"), "gpt2-medium", "nuisance model")

    return {
        "files": records,
        "condition": tuckute["condition"],
        "ordered_item_count": tuckute["ordered_item_count"],
        "ordered_item_id_sha256": tuckute["ordered_item_id_sha256"],
        "ordered_text_sha256": tuckute["ordered_text_sha256"],
        "rois": tuckute["rois"],
        "valid_participants": tuckute["valid_uids"],
        "excluded_participant": tuckute["excluded_uid"],
        "covariate_columns": tuckute["covariate_columns"],
        "participants": participant_records,
        "nuisance_headers": nuisance_headers,
        "nuisance_metadata": nuisance_metadata,
    }


def validate_cache_aliases(
    extraction_path: Path, cache_specs: list[dict[str, Any]]
) -> dict[int, dict[str, Any]]:
    extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
    require_equal(
        extraction.get("manifest", {}).get("sha256"),
        extraction_spec_manifest_sha256(cache_specs),
        "E025 manifest hash recorded by extraction",
    )
    observed: dict[int, dict[str, Any]] = {}
    for row in extraction.get("cache_rows", []):
        aliases = row.get("aliases", [])
        for alias in aliases:
            if alias.get("arm") != "kd_only":
                continue
            seed = int(alias["seed"])
            candidate = {
                "path": str(Path(row["path"]).resolve().relative_to(REPO_ROOT)),
                "sha256": row["sha256"],
                "cache_key": row["cache_key"],
            }
            previous = observed.get(seed)
            if previous is not None and previous != candidate:
                raise ValueError(f"seed {seed} has conflicting kd_only aliases")
            observed[seed] = candidate
    require_equal(sorted(observed), [0, 1, 2, 3, 4, 5], "kd_only seed aliases")
    for spec in cache_specs:
        seed = int(spec["seed"])
        require_equal(observed[seed]["path"], spec["path"], f"seed {seed} cache path")
        require_equal(observed[seed]["sha256"], spec["sha256"], f"seed {seed} cache hash")
    return observed


def extraction_spec_manifest_sha256(cache_specs: list[dict[str, Any]]) -> str:
    """Obtain the shared frozen E025 manifest hash attached by the caller."""
    values = {
        str(spec["_e025_manifest_sha256"])
        for spec in cache_specs
        if "_e025_manifest_sha256" in spec
    }
    if len(values) != 1:
        raise ValueError("cache specifications do not bind one E025 manifest hash")
    return values.pop()


def hdf_metadata(path: Path) -> dict[str, Any]:
    """Inspect HDF structure only. Dataset values are never indexed."""
    result: dict[str, Any] = {}
    with h5py.File(path, "r") as handle:
        def visit(name: str, item: h5py.Dataset | h5py.Group) -> None:
            if isinstance(item, h5py.Dataset):
                result[name] = {
                    "shape": list(item.shape),
                    "dtype": str(item.dtype),
                    "chunks": None if item.chunks is None else list(item.chunks),
                    "compression": item.compression,
                }

        handle.visititems(visit)
    return result


def wav_metadata(path: Path) -> dict[str, Any]:
    with wave.open(str(path), "rb") as handle:
        return {
            "channels": handle.getnchannels(),
            "sample_width_bytes": handle.getsampwidth(),
            "sample_rate_hz": handle.getframerate(),
            "frames": handle.getnframes(),
            "compression": handle.getcomptype(),
        }


def stable_hash(payload: Any) -> str:
    return sha256_bytes(canonical_json(payload).encode("utf-8"))


def validate_payload_hash(
    payload: dict[str, Any], field: str, label: str
) -> None:
    if field not in payload:
        raise ValueError(f"{label} lacks {field}")
    observed = str(payload[field])
    unhashed = {key: value for key, value in payload.items() if key != field}
    require_equal(observed, stable_hash(unhashed), f"{label} payload hash")


def validate_c1_result_artifact(
    config: dict[str, Any], config_path: Path
) -> dict[str, Any]:
    path = resolve_path(config["outputs"]["c1_result"])
    result = json.loads(path.read_text(encoding="utf-8"))
    require_equal(result.get("experiment"), "E031", "C1 result experiment")
    require_equal(result.get("stage"), "c1", "C1 result stage")
    require_equal(result.get("status"), "SEALED", "C1 result status")
    require_equal(
        result.get("configuration", {}).get("sha256"),
        sha256_file(config_path),
        "C1 current configuration hash",
    )
    require_equal(
        result.get("executable", {}).get("sha256"),
        sha256_file(Path(__file__).resolve()),
        "C1 current executable hash",
    )
    arrays = result.get("array_artifact", {})
    arrays_path = resolve_path(str(arrays.get("path", "")))
    require_equal(
        sha256_file(arrays_path),
        arrays.get("sha256"),
        "C1 array artifact hash",
    )
    validate_payload_hash(result, "result_payload_sha256", "C1 result")
    return result


def consensus_weights(fold_agreements: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    fold_agreements = np.asarray(fold_agreements, dtype=np.float64)
    if fold_agreements.ndim != 2 or fold_agreements.shape[0] < 2:
        raise ValueError("fold_agreements must be participant by inner-fold")
    clip = float(config["correlation_clip"])
    minimum = float(config["minimum_weight_sum"])
    shrinkage = float(config["shrinkage_to_uniform"])
    clipped = np.clip(fold_agreements, -clip, clip)
    fisher_means = np.arctanh(clipped).mean(axis=1)
    scores = np.maximum(np.tanh(fisher_means), 0.0)
    uniform = np.full(fold_agreements.shape[0], 1.0 / fold_agreements.shape[0], dtype=np.float64)
    if float(scores.sum()) <= minimum:
        learned = uniform
    else:
        learned = scores / scores.sum()
    return shrinkage * uniform + (1.0 - shrinkage) * learned


def geometry_match(
    text_scores_train: np.ndarray,
    biological_train: np.ndarray,
    text_scores_apply: np.ndarray,
    relative_floor: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Whiten text scores and recolor them to biological train covariance."""
    x = np.asarray(text_scores_train, dtype=np.float64)
    y = np.asarray(biological_train, dtype=np.float64)
    z = np.asarray(text_scores_apply, dtype=np.float64)
    if x.shape[1] != y.shape[1] or z.shape[1] != x.shape[1]:
        raise ValueError("geometry matching requires equal dimensions")
    x_mean = x.mean(axis=0)
    y_mean = y.mean(axis=0)
    x_centered = x - x_mean
    y_centered = y - y_mean
    x_cov = np.cov(x_centered, rowvar=False, ddof=1)
    y_cov = np.cov(y_centered, rowvar=False, ddof=1)
    x_eval, x_vec = np.linalg.eigh(x_cov)
    y_eval, y_vec = np.linalg.eigh(y_cov)
    if float(x_eval.min()) < -1e-10 or float(y_eval.min()) < -1e-10:
        raise ValueError("covariance has a materially negative eigenvalue")
    x_eval = np.maximum(x_eval, 0.0)
    y_eval = np.maximum(y_eval, 0.0)
    x_floor = relative_floor * max(float(x_eval.max()), np.finfo(np.float64).tiny)
    whiten = x_vec @ np.diag(1.0 / np.sqrt(np.maximum(x_eval, x_floor))) @ x_vec.T
    recolor = y_vec @ np.diag(np.sqrt(y_eval)) @ y_vec.T
    transform = whiten @ recolor
    return (x_centered @ transform + y_mean, (z - x_mean) @ transform + y_mean)


def block_local_shift(indices: Iterable[int]) -> np.ndarray:
    values = np.asarray(list(indices), dtype=np.int64)
    if values.ndim != 1 or values.size < 2:
        raise ValueError("shift segment must be one-dimensional and nontrivial")
    return np.roll(values, values.size // 2)


def unique_r2(
    observed: np.ndarray, nuisance_prediction: np.ndarray, full_prediction: np.ndarray
) -> np.ndarray:
    observed = np.asarray(observed, dtype=np.float64)
    nuisance_prediction = np.asarray(nuisance_prediction, dtype=np.float64)
    full_prediction = np.asarray(full_prediction, dtype=np.float64)
    if observed.shape != nuisance_prediction.shape or observed.shape != full_prediction.shape:
        raise ValueError("unique R2 inputs must have identical shape")
    if observed.ndim == 1:
        observed = observed[:, None]
        nuisance_prediction = nuisance_prediction[:, None]
        full_prediction = full_prediction[:, None]
    sse_nuisance = np.square(observed - nuisance_prediction).sum(axis=0)
    sse_full = np.square(observed - full_prediction).sum(axis=0)
    sst = np.square(observed - observed.mean(axis=0, keepdims=True)).sum(axis=0)
    if np.any(sst <= 1e-12):
        raise ValueError("SST is at or below the frozen floor")
    return (sse_nuisance - sse_full) / sst


def fit_standardizer(
    train: np.ndarray, apply: np.ndarray, floor: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    train64 = np.asarray(train, dtype=np.float64)
    apply64 = np.asarray(apply, dtype=np.float64)
    mean = train64.mean(axis=0)
    scale = train64.std(axis=0, ddof=0)
    scale = np.maximum(scale, float(floor))
    return (train64 - mean) / scale, (apply64 - mean) / scale, mean, scale


def fit_pca_svd(
    train: np.ndarray, apply: np.ndarray, rank: int
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    train64 = np.asarray(train, dtype=np.float64)
    apply64 = np.asarray(apply, dtype=np.float64)
    if train64.ndim != 2 or apply64.ndim != 2 or train64.shape[1] != apply64.shape[1]:
        raise ValueError("PCA train/apply matrices are incompatible")
    mean = train64.mean(axis=0)
    centered = train64 - mean
    _, singular, right = np.linalg.svd(centered, full_matrices=False)
    tolerance = (
        max(centered.shape)
        * np.finfo(np.float64).eps
        * (float(singular[0]) if singular.size else 0.0)
    )
    finite_rank = int(np.sum(singular > tolerance))
    if finite_rank < int(rank):
        raise ValueError(f"PCA rank {finite_rank} is below required rank {rank}")
    components = right[: int(rank)].copy()
    for index in range(components.shape[0]):
        pivot = int(np.argmax(np.abs(components[index])))
        if components[index, pivot] < 0:
            components[index] *= -1.0
    train_scores = centered @ components.T
    apply_scores = (apply64 - mean) @ components.T
    return train_scores, apply_scores, {
        "rank": int(rank),
        "finite_rank": finite_rank,
        "mean_sha256": sha256_array(mean),
        "components_sha256": sha256_array(components),
        "singular_values": singular[: int(rank)].tolist(),
    }


def c1_blocks(config: dict[str, Any]) -> list[np.ndarray]:
    return [
        np.arange(int(start), int(stop), dtype=np.int64)
        for start, stop in config["c1"]["outer_folds"]
    ]


def c1_nuisance_design(
    nuisance: dict[str, np.ndarray],
    train: np.ndarray,
    apply: np.ndarray,
    config: dict[str, Any],
    variant: str,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    c1 = config["c1"]
    floor = float(c1["standard_deviation_floor"])
    base_train, base_apply, _, _ = fit_standardizer(
        nuisance["base_scalar"][train], nuisance["base_scalar"][apply], floor
    )
    embed_train, embed_apply, _, _ = fit_standardizer(
        nuisance["static_embedding"][train], nuisance["static_embedding"][apply], floor
    )
    embed_train, embed_apply, pca = fit_pca_svd(
        embed_train, embed_apply, int(c1["nuisance_pca_rank"])
    )
    train_parts = [base_train, embed_train]
    apply_parts = [base_apply, embed_apply]
    if variant == "expanded_imageability":
        extra_key = "imageability"
    elif variant == "full_covariate_stress":
        extra_key = "full_cov_extra"
    elif variant == "primary":
        extra_key = None
    else:
        raise ValueError(f"unknown C1 nuisance variant {variant!r}")
    if extra_key is not None:
        extra_train, extra_apply, _, _ = fit_standardizer(
            nuisance[extra_key][train], nuisance[extra_key][apply], floor
        )
        train_parts.append(extra_train)
        apply_parts.append(extra_apply)
    design_train = np.concatenate(train_parts, axis=1)
    design_apply = np.concatenate(apply_parts, axis=1)
    if not np.isfinite(design_train).all() or not np.isfinite(design_apply).all():
        raise ValueError("C1 nuisance design contains nonfinite values")
    return design_train, design_apply, {
        "variant": variant,
        "columns": int(design_train.shape[1]),
        "embedding_pca": pca,
    }


def residualize_source_responses(
    responses: np.ndarray,
    train: np.ndarray,
    apply: np.ndarray,
    nuisance_train: np.ndarray,
    nuisance_apply: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(responses, dtype=np.float64)
    if values.ndim != 3:
        raise ValueError("source responses must be participant by row by ROI")
    train_values = values[:, train, :]
    apply_values = values[:, apply, :]
    train_residual = np.empty_like(train_values)
    apply_residual = np.empty_like(apply_values)
    for participant in range(values.shape[0]):
        mean = train_values[participant].mean(axis=0)
        centered_train = train_values[participant] - mean
        coefficient = np.linalg.lstsq(nuisance_train, centered_train, rcond=None)[0]
        train_residual[participant] = centered_train - nuisance_train @ coefficient
        apply_residual[participant] = (
            apply_values[participant] - mean - nuisance_apply @ coefficient
        )
    return train_residual, apply_residual


def normalize_target(
    train: np.ndarray, apply: np.ndarray, floor: float
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    train_scaled, apply_scaled, mean, scale = fit_standardizer(train, apply, floor)
    return train_scaled, apply_scaled, {
        "mean": mean.tolist(),
        "scale": scale.tolist(),
    }


def c1_consensus_weight_matrix(
    source_responses: np.ndarray,
    outer_test_index: int,
    nuisance: dict[str, np.ndarray],
    config: dict[str, Any],
    variant: str,
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    blocks = c1_blocks(config)
    inner_blocks = [block for index, block in enumerate(blocks) if index != outer_test_index]
    participant_count = source_responses.shape[0]
    roi_count = source_responses.shape[2]
    agreements = np.zeros((roi_count, participant_count, len(inner_blocks)), dtype=np.float64)
    diagnostics: list[dict[str, Any]] = []
    for inner_index, validation in enumerate(inner_blocks):
        inner_train = np.concatenate(
            [block for index, block in enumerate(inner_blocks) if index != inner_index]
        )
        nuisance_train, nuisance_validation, nuisance_meta = c1_nuisance_design(
            nuisance, inner_train, validation, config, variant
        )
        _, residual_validation = residualize_source_responses(
            source_responses,
            inner_train,
            validation,
            nuisance_train,
            nuisance_validation,
        )
        for roi in range(roi_count):
            for participant in range(participant_count):
                peer_indices = [index for index in range(participant_count) if index != participant]
                peer_mean = residual_validation[peer_indices, :, roi].mean(axis=0)
                candidate = residual_validation[participant, :, roi]
                if (
                    float(np.var(candidate, ddof=0)) <= 1e-12
                    or float(np.var(peer_mean, ddof=0)) <= 1e-12
                ):
                    agreement = 0.0
                else:
                    agreement = float(np.corrcoef(candidate, peer_mean)[0, 1])
                agreements[roi, participant, inner_index] = agreement
        diagnostics.append(
            {
                "inner_index": inner_index,
                "validation_rows": [int(validation[0]), int(validation[-1]) + 1],
                "nuisance": nuisance_meta,
            }
        )
    weights = np.stack(
        [
            consensus_weights(agreements[roi], config["c1"]["consensus"])
            for roi in range(roi_count)
        ],
        axis=1,
    )
    return weights, diagnostics


def load_c1_text_features(config: dict[str, Any]) -> tuple[np.ndarray, list[dict[str, Any]]]:
    c1 = config["c1"]
    cache_specs = sorted(
        [
            {
                **row,
                "_e025_manifest_sha256": c1["extraction"]["manifest_sha256"],
            }
            for row in c1["representation_caches"]
        ],
        key=lambda row: int(row["seed"]),
    )
    file_record(c1["extraction"])
    validate_cache_aliases(resolve_path(c1["extraction"]["path"]), cache_specs)
    layers: dict[int, list[np.ndarray]] = {
        int(layer): [] for layer in c1["text_control"]["layers"]
    }
    records: list[dict[str, Any]] = []
    for spec in cache_specs:
        record = file_record(spec)
        path = resolve_path(spec["path"])
        headers = npz_headers(path)
        metadata = representation_metadata(path)
        require_equal(
            metadata.get("tuckute_ordered_text_sha256"),
            c1["ordered_text_sha256"],
            f"seed {spec['seed']} text order",
        )
        require_equal(metadata.get("pooling"), "attention-mask mean", "C1 cache pooling")
        require_equal(
            metadata.get("layers"),
            c1["text_control"]["layers"],
            "C1 cache layers",
        )
        if {
            "family": "textfeat",
            "seed": int(spec["seed"]),
            "arm": "kd_only",
        } not in metadata.get("aliases", []):
            raise ValueError(f"seed {spec['seed']} cache lacks its textfeat kd_only alias")
        for layer in layers:
            key = f"tuckute_layer_{layer}"
            require_equal(headers[key]["shape"], [c1["rows"], 768], f"{key} shape")
            require_equal(headers[key]["dtype"], "float32", f"{key} dtype")
        with np.load(path, allow_pickle=False) as cached:
            for layer in layers:
                layers[layer].append(np.asarray(cached[f"tuckute_layer_{layer}"], dtype=np.float64))
        records.append({"seed": int(spec["seed"]), **record})
    means = [
        np.mean(np.stack(layers[layer], axis=0), axis=0, dtype=np.float64)
        for layer in c1["text_control"]["layers"]
    ]
    features = np.concatenate(means, axis=1)
    if features.shape != (int(c1["rows"]), 1536) or not np.isfinite(features).all():
        raise ValueError(f"unexpected C1 text feature matrix {features.shape}")
    return features, records


def residualized_text_pca(
    raw_text: np.ndarray,
    train: np.ndarray,
    apply: np.ndarray,
    nuisance_train: np.ndarray,
    nuisance_apply: np.ndarray,
    rank: int,
    floor: float,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    text_train = np.asarray(raw_text[train], dtype=np.float64)
    text_apply = np.asarray(raw_text[apply], dtype=np.float64)
    mean = text_train.mean(axis=0)
    coefficient = np.linalg.lstsq(nuisance_train, text_train - mean, rcond=None)[0]
    residual_train = text_train - mean - nuisance_train @ coefficient
    residual_apply = text_apply - mean - nuisance_apply @ coefficient
    residual_train, residual_apply, _, _ = fit_standardizer(
        residual_train, residual_apply, floor
    )
    return fit_pca_svd(residual_train, residual_apply, rank)


def c1_text_crossfit(
    raw_text: np.ndarray,
    consensus_full: np.ndarray,
    outer_test_index: int,
    nuisance: dict[str, np.ndarray],
    config: dict[str, Any],
    variant: str,
) -> tuple[np.ndarray, dict[str, Any]]:
    from sklearn.linear_model import Ridge

    c1 = config["c1"]
    blocks = c1_blocks(config)
    outer_test = blocks[outer_test_index]
    outer_train_blocks = [block for index, block in enumerate(blocks) if index != outer_test_index]
    outer_train = np.concatenate(outer_train_blocks)
    rank = int(c1["text_control"]["feature_pca_rank"])
    alpha = float(c1["text_control"]["fixed_crossfit_ridge_alpha"])
    floor = float(c1["standard_deviation_floor"])
    predicted = np.full_like(consensus_full, np.nan, dtype=np.float64)
    inner_records: list[dict[str, Any]] = []
    for inner_index, validation in enumerate(outer_train_blocks):
        inner_train = np.concatenate(
            [block for index, block in enumerate(outer_train_blocks) if index != inner_index]
        )
        nuisance_train, nuisance_validation, _ = c1_nuisance_design(
            nuisance, inner_train, validation, config, variant
        )
        scores_train, scores_validation, pca = residualized_text_pca(
            raw_text,
            inner_train,
            validation,
            nuisance_train,
            nuisance_validation,
            rank,
            floor,
        )
        model = Ridge(alpha=alpha, solver="svd", fit_intercept=False)
        model.fit(scores_train, consensus_full[inner_train])
        predicted[validation] = model.predict(scores_validation)
        inner_records.append(
            {
                "inner_index": inner_index,
                "validation_rows": [int(validation[0]), int(validation[-1]) + 1],
                "pca": pca,
            }
        )
    nuisance_train, nuisance_test, _ = c1_nuisance_design(
        nuisance, outer_train, outer_test, config, variant
    )
    scores_train, scores_test, pca = residualized_text_pca(
        raw_text,
        outer_train,
        outer_test,
        nuisance_train,
        nuisance_test,
        rank,
        floor,
    )
    model = Ridge(alpha=alpha, solver="svd", fit_intercept=False)
    model.fit(scores_train, consensus_full[outer_train])
    predicted[outer_test] = model.predict(scores_test)
    if not np.isfinite(predicted).all():
        raise ValueError("C1 text-to-consensus crossfit has uncovered rows")
    return predicted, {"inner": inner_records, "outer_refit_pca": pca}


def build_c1_targets(
    source_responses: np.ndarray,
    raw_text: np.ndarray,
    nuisance: dict[str, np.ndarray],
    outer_test_index: int,
    config: dict[str, Any],
    variant: str,
) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    c1 = config["c1"]
    blocks = c1_blocks(config)
    test = blocks[outer_test_index]
    train = np.concatenate([block for index, block in enumerate(blocks) if index != outer_test_index])
    nuisance_train, nuisance_test, nuisance_meta = c1_nuisance_design(
        nuisance, train, test, config, variant
    )
    residual_train, residual_test = residualize_source_responses(
        source_responses, train, test, nuisance_train, nuisance_test
    )
    uniform_weights = np.asarray(c1["uniform_weights"], dtype=np.float64)
    uniform_train_raw = np.einsum("p,ptr->tr", uniform_weights, residual_train)
    uniform_test_raw = np.einsum("p,ptr->tr", uniform_weights, residual_test)
    uniform_train, uniform_test, uniform_norm = normalize_target(
        uniform_train_raw,
        uniform_test_raw,
        float(c1["standard_deviation_floor"]),
    )
    weights, consensus_inner = c1_consensus_weight_matrix(
        source_responses, outer_test_index, nuisance, config, variant
    )
    consensus_train_raw = np.einsum("pr,ptr->tr", weights, residual_train)
    consensus_test_raw = np.einsum("pr,ptr->tr", weights, residual_test)
    consensus_train, consensus_test, consensus_norm = normalize_target(
        consensus_train_raw,
        consensus_test_raw,
        float(c1["standard_deviation_floor"]),
    )
    consensus_full = np.empty((int(c1["rows"]), int(c1["target_dimension"])), dtype=np.float64)
    consensus_full[train] = consensus_train
    consensus_full[test] = consensus_test

    text_train, text_test, text_pca = residualized_text_pca(
        raw_text,
        train,
        test,
        nuisance_train,
        nuisance_test,
        int(c1["text_control"]["geometry_rank"]),
        float(c1["standard_deviation_floor"]),
    )
    text_train, text_test = geometry_match(
        text_train,
        consensus_train,
        text_test,
        float(c1["text_control"]["whitening_relative_floor"]),
    )
    biological_covariance = np.cov(consensus_train, rowvar=False, ddof=1)
    text_covariance = np.cov(text_train, rowvar=False, ddof=1)
    covariance_error = float(
        np.linalg.norm(text_covariance - biological_covariance, ord="fro")
        / max(float(np.linalg.norm(biological_covariance, ord="fro")), 1e-12)
    )
    biological_eigenvalues = np.linalg.eigvalsh(biological_covariance)[::-1]
    text_eigenvalues = np.linalg.eigvalsh(text_covariance)[::-1]
    eigenvalue_error = float(
        np.max(np.abs(text_eigenvalues - biological_eigenvalues))
        / max(float(biological_eigenvalues[0]), 1e-12)
    )
    mean_error = float(np.max(np.abs(text_train.mean(axis=0) - consensus_train.mean(axis=0))))
    geometry_pass = (
        text_train.shape[1] == int(c1["target_dimension"])
        and covariance_error
        <= float(c1["text_control"]["covariance_relative_frobenius_tolerance"])
        and eigenvalue_error <= float(c1["text_control"]["eigenvalue_relative_tolerance"])
        and mean_error <= float(c1["text_control"]["mean_absolute_tolerance"])
    )
    if not geometry_pass:
        raise ValueError(
            "C1 geometry-match gate failed: "
            f"covariance={covariance_error}, eigenvalue={eigenvalue_error}, mean={mean_error}"
        )
    text_full = np.empty_like(consensus_full)
    text_full[train] = text_train
    text_full[test] = text_test
    text_crossfit, crossfit_meta = c1_text_crossfit(
        raw_text,
        consensus_full,
        outer_test_index,
        nuisance,
        config,
        variant,
    )
    shifted_full = np.empty_like(consensus_full)
    shift_records: list[dict[str, Any]] = []
    for segment_index, block in enumerate(blocks):
        row_map = np.roll(block, int(c1["block_shift"]))
        shifted_full[block] = consensus_full[row_map]
        shift_records.append(
            {
                "segment": segment_index,
                "start": int(block[0]),
                "stop": int(block[-1]) + 1,
                "offset": int(c1["block_shift"]),
                "row_map_sha256": sha256_array(row_map.astype("<i8")),
            }
        )
    uniform_full = np.empty_like(consensus_full)
    uniform_full[train] = uniform_train
    uniform_full[test] = uniform_test
    source_mean_raw = source_responses.mean(axis=0)
    targets = {
        "source_mean_raw": source_mean_raw,
        "uniform_residual": uniform_full,
        "consensus_weighted": consensus_full,
        "text_surrogate_geometry_matched": text_full,
        "text_to_consensus_crossfit": text_crossfit,
        "cw_shifted": shifted_full,
    }
    return targets, {
        "outer_test_index": outer_test_index,
        "train_rows": int(len(train)),
        "test_rows": [int(test[0]), int(test[-1]) + 1],
        "nuisance": nuisance_meta,
        "uniform_normalization": uniform_norm,
        "consensus_normalization": consensus_norm,
        "consensus_weights_by_participant_roi": weights.tolist(),
        "consensus_inner": consensus_inner,
        "geometry": {
            "dimension": int(text_train.shape[1]),
            "covariance_relative_frobenius_error": covariance_error,
            "eigenvalue_relative_error": eigenvalue_error,
            "mean_absolute_error": mean_error,
            "status": "PASS",
            "pca": text_pca,
        },
        "text_crossfit": crossfit_meta,
        "shift_maps": shift_records,
    }


def select_nested_ridge_prediction(
    train: np.ndarray,
    test: np.ndarray,
    inner_blocks: list[np.ndarray],
    predictors: np.ndarray,
    outcome: np.ndarray,
    config: dict[str, Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    from sklearn.linear_model import Ridge

    c1 = config["c1"]
    floor = float(c1["standard_deviation_floor"])
    x_train, x_test, _, _ = fit_standardizer(
        predictors[train], predictors[test], floor
    )
    y_train, _, y_mean, y_scale = fit_standardizer(outcome[train], outcome[test], floor)
    location = {int(row): index for index, row in enumerate(train.tolist())}
    inner_local = [
        np.asarray([location[int(row)] for row in block], dtype=np.int64)
        for block in inner_blocks
    ]
    all_local = np.arange(len(train), dtype=np.int64)
    losses: dict[float, float] = {}
    for alpha_value in c1["ridge_alphas"]:
        alpha = float(alpha_value)
        squared_error = 0.0
        count = 0
        for validation in inner_local:
            fit = np.setdiff1d(all_local, validation, assume_unique=True)
            model = Ridge(alpha=alpha, solver="svd", fit_intercept=False)
            model.fit(x_train[fit], y_train[fit])
            prediction = model.predict(x_train[validation])
            squared_error += float(np.square(y_train[validation] - prediction).sum())
            count += int(np.prod(prediction.shape))
        losses[alpha] = squared_error / count
    tolerance = float(c1["ridge_tie_tolerance"])
    best_alpha: float | None = None
    best_loss = np.inf
    for alpha in sorted(losses):
        loss = losses[alpha]
        if loss < best_loss - tolerance or (
            abs(loss - best_loss) <= tolerance
            and (best_alpha is None or alpha > best_alpha)
        ):
            best_alpha = alpha
            best_loss = loss
    if best_alpha is None:
        raise RuntimeError("ridge selection did not choose an alpha")
    model = Ridge(alpha=best_alpha, solver="svd", fit_intercept=False)
    model.fit(x_train, y_train)
    prediction = model.predict(x_test) * y_scale + y_mean
    return prediction, {
        "alpha": best_alpha,
        "inner_mean_mse": {str(alpha): losses[alpha] for alpha in sorted(losses)},
    }


def c1_contrast_summary(values: np.ndarray) -> dict[str, Any]:
    from scipy import stats

    array = np.asarray(values, dtype=np.float64)
    n = int(array.size)
    mean = float(array.mean())
    median = float(np.median(array))
    standard_error = float(array.std(ddof=1) / np.sqrt(n))
    ci_critical = float(stats.t.ppf(0.975, n - 1))
    lower_critical = float(stats.t.ppf(1.0 - 0.0125, n - 1))
    nonzero = array[array != 0.0]
    if nonzero.size:
        sign_p = float(
            stats.binomtest(
                int(np.sum(nonzero > 0.0)),
                int(nonzero.size),
                p=0.5,
                alternative="greater",
            ).pvalue
        )
    else:
        sign_p = None
    return {
        "values": array.tolist(),
        "mean": mean,
        "median": median,
        "t_ci95": [
            mean - ci_critical * standard_error,
            mean + ci_critical * standard_error,
        ],
        "one_sided_bonferroni_t_lower_bound": mean - lower_critical * standard_error,
        "positive_count": int(np.sum(array > 0.0)),
        "zero_count": int(np.sum(array == 0.0)),
        "one_sided_exact_sign_p": sign_p,
        "leave_one_participant_out_means": [
            float(np.delete(array, index).mean()) for index in range(n)
        ],
    }


def run_c1(config: dict[str, Any], config_path: Path) -> dict[str, Any]:
    from scripts.e025_participant_transfer import load_tuckute_participants

    c1 = config["c1"]
    validation = validate_c1_biological_inputs(config)
    response_path = resolve_path(c1["biological_inputs"]["response_csv"]["path"])
    all_participants = tuple(
        int(value)
        for value in c1["source_participants"] + c1["evaluation_participants"]
    )
    texts, targets_by_uid, _, loaded_meta = load_tuckute_participants(
        response_path.parents[1],
        str(c1["biological_inputs"]["condition"]),
        all_participants,
        include_targets=True,
    )
    require_equal(loaded_meta["ordered_text_sha256"], c1["ordered_text_sha256"], "C1 loaded text")
    require_equal(len(texts), int(c1["rows"]), "C1 loaded rows")
    source_responses = np.stack(
        [
            np.asarray(targets_by_uid[int(uid)], dtype=np.float64)
            for uid in c1["source_participants"]
        ],
        axis=0,
    )
    evaluation_responses = {
        int(uid): np.asarray(targets_by_uid[int(uid)], dtype=np.float64)
        for uid in c1["evaluation_participants"]
    }
    nuisance_path = resolve_path(c1["biological_inputs"]["nuisance_cache"]["path"])
    with np.load(nuisance_path, allow_pickle=False) as cached:
        nuisance = {
            key: np.asarray(cached[key], dtype=np.float64)
            for key in c1["biological_inputs"]["nuisance_arrays"]
        }
    raw_text, cache_records = load_c1_text_features(config)
    variants = ["primary", "expanded_imageability", "full_covariate_stress"]
    blocks = c1_blocks(config)
    array_artifact: dict[str, np.ndarray] = {}
    variant_results: dict[str, Any] = {}
    for variant in variants:
        fold_targets: list[dict[str, np.ndarray]] = []
        builder_records: list[dict[str, Any]] = []
        for outer_test_index in range(len(blocks)):
            built, record = build_c1_targets(
                source_responses,
                raw_text,
                nuisance,
                outer_test_index,
                config,
                variant,
            )
            fold_targets.append(built)
            builder_records.append(record)
        participant_u: dict[int, dict[str, float]] = {}
        participant_b: dict[int, float] = {}
        selection_records: dict[str, Any] = {}
        fold_descriptives: dict[str, Any] = {}
        for uid, outcome in evaluation_responses.items():
            predictions = {
                name: np.full_like(outcome, np.nan, dtype=np.float64)
                for name in (
                    "nuisance",
                    "uniform_residual",
                    "consensus_weighted",
                    "text_surrogate_geometry_matched",
                    "text_to_consensus_crossfit",
                    "cw_shifted",
                    "text_plus_cw",
                )
            }
            selection_records[str(uid)] = {}
            fold_descriptives[str(uid)] = {}
            for outer_test_index, test in enumerate(blocks):
                train_blocks = [
                    block for index, block in enumerate(blocks) if index != outer_test_index
                ]
                train = np.concatenate(train_blocks)
                nuisance_train, nuisance_test, _ = c1_nuisance_design(
                    nuisance, train, test, config, variant
                )
                nuisance_full = np.empty(
                    (int(c1["rows"]), nuisance_train.shape[1]), dtype=np.float64
                )
                nuisance_full[train] = nuisance_train
                nuisance_full[test] = nuisance_test
                fold_selection: dict[str, Any] = {}
                prediction, record = select_nested_ridge_prediction(
                    train, test, train_blocks, nuisance_full, outcome, config
                )
                predictions["nuisance"][test] = prediction
                fold_selection["nuisance"] = record
                for arm in (
                    "uniform_residual",
                    "consensus_weighted",
                    "text_surrogate_geometry_matched",
                    "text_to_consensus_crossfit",
                    "cw_shifted",
                ):
                    predictors = np.concatenate(
                        [nuisance_full, fold_targets[outer_test_index][arm]], axis=1
                    )
                    prediction, record = select_nested_ridge_prediction(
                        train, test, train_blocks, predictors, outcome, config
                    )
                    predictions[arm][test] = prediction
                    fold_selection[arm] = record
                text_plus_cw = np.concatenate(
                    [
                        nuisance_full,
                        fold_targets[outer_test_index]["text_to_consensus_crossfit"],
                        fold_targets[outer_test_index]["consensus_weighted"],
                    ],
                    axis=1,
                )
                prediction, record = select_nested_ridge_prediction(
                    train, test, train_blocks, text_plus_cw, outcome, config
                )
                predictions["text_plus_cw"][test] = prediction
                fold_selection["text_plus_cw"] = record
                selection_records[str(uid)][str(outer_test_index)] = fold_selection
                fold_descriptives[str(uid)][str(outer_test_index)] = {
                    arm: float(
                        np.mean(
                            unique_r2(
                                outcome[test],
                                predictions["nuisance"][test],
                                predictions[arm][test],
                            )
                        )
                    )
                    for arm in (
                        "uniform_residual",
                        "consensus_weighted",
                        "text_surrogate_geometry_matched",
                        "cw_shifted",
                    )
                }
            if any(not np.isfinite(values).all() for values in predictions.values()):
                raise ValueError(f"C1 predictions are incomplete for participant {uid}")
            u_values = {
                arm: float(
                    np.mean(unique_r2(outcome, predictions["nuisance"], predictions[arm]))
                )
                for arm in (
                    "uniform_residual",
                    "consensus_weighted",
                    "text_surrogate_geometry_matched",
                    "text_to_consensus_crossfit",
                    "cw_shifted",
                )
            }
            participant_u[uid] = u_values
            participant_b[uid] = float(
                np.mean(
                    unique_r2(
                        outcome,
                        predictions["text_to_consensus_crossfit"],
                        predictions["text_plus_cw"],
                    )
                )
            )
            array_artifact[f"{variant}__observed__{uid}"] = outcome.astype(np.float64)
            for arm, values in predictions.items():
                array_artifact[f"{variant}__prediction__{uid}__{arm}"] = values.astype(
                    np.float64
                )
        ordered_uids = [int(uid) for uid in c1["evaluation_participants"]]
        contrasts = {
            "A_cw": np.asarray(
                [participant_u[uid]["consensus_weighted"] for uid in ordered_uids]
            ),
            "D_cw_minus_uniform": np.asarray(
                [
                    participant_u[uid]["consensus_weighted"]
                    - participant_u[uid]["uniform_residual"]
                    for uid in ordered_uids
                ]
            ),
            "S_cw": np.asarray(
                [
                    participant_u[uid]["consensus_weighted"]
                    - participant_u[uid]["cw_shifted"]
                    for uid in ordered_uids
                ]
            ),
            "B_cw_given_text": np.asarray([participant_b[uid] for uid in ordered_uids]),
            "T_cw_minus_text": np.asarray(
                [
                    participant_u[uid]["consensus_weighted"]
                    - participant_u[uid]["text_surrogate_geometry_matched"]
                    for uid in ordered_uids
                ]
            ),
        }
        summaries = {
            name: c1_contrast_summary(values) for name, values in contrasts.items()
        }
        gate_spec = c1["fixed_cohort_gate"]
        confirmatory = (
            summaries["A_cw"]["mean"] >= float(gate_spec["absolute_minimum"])
            and summaries["D_cw_minus_uniform"]["mean"]
            >= float(gate_spec["increment_minimum"])
            and summaries["S_cw"]["mean"] > 0.0
            and summaries["B_cw_given_text"]["mean"] > 0.0
            and all(
                summaries[name]["positive_count"]
                >= int(gate_spec["minimum_positive_participants"])
                for name in (
                    "A_cw",
                    "D_cw_minus_uniform",
                    "S_cw",
                    "B_cw_given_text",
                )
            )
        )
        variant_results[variant] = {
            "participant_u": {
                str(uid): participant_u[uid] for uid in ordered_uids
            },
            "participant_b_cw_given_text": {
                str(uid): participant_b[uid] for uid in ordered_uids
            },
            "contrasts": summaries,
            "fixed_cohort_gate": "PASS" if confirmatory else "FAIL",
            "scope": "fixed_named_participant_cohort_only",
            "builder_records": builder_records,
            "ridge_selection": selection_records,
            "fold_descriptives": fold_descriptives,
        }
    arrays_path = resolve_path(config["outputs"]["c1_arrays"])
    atomic_savez(arrays_path, array_artifact)
    result = {
        "schema_version": "1.0",
        "experiment": "E031",
        "stage": "c1",
        "created_at_utc": utc_now(),
        "configuration": {
            "path": str(config_path.relative_to(REPO_ROOT)),
            "sha256": sha256_file(config_path),
        },
        "executable": {
            "path": str(Path(__file__).resolve().relative_to(REPO_ROOT)),
            "sha256": sha256_file(Path(__file__).resolve()),
        },
        "input_validation": validation,
        "representation_caches": cache_records,
        "participants": {
            "source": c1["source_participants"],
            "evaluation": c1["evaluation_participants"],
        },
        "variants": variant_results,
        "array_artifact": {
            "path": str(arrays_path.relative_to(REPO_ROOT)),
            "sha256": sha256_file(arrays_path),
            "keys": sorted(array_artifact),
        },
        "primary_gate": variant_results["primary"]["fixed_cohort_gate"],
        "population_claim_permitted": False,
        "status": "SEALED",
    }
    result["result_payload_sha256"] = stable_hash(result)
    atomic_write_json(resolve_path(config["outputs"]["c1_result"]), result)
    return result


def make_delayed_features(values: np.ndarray, delays: list[int]) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 2:
        raise ValueError("delayed feature input must be two-dimensional")
    delayed: list[np.ndarray] = []
    for delay in delays:
        shifted = np.zeros_like(array)
        if delay > 0:
            shifted[delay:] = array[:-delay]
        elif delay < 0:
            shifted[:delay] = array[-delay:]
        else:
            shifted = array.copy()
        delayed.append(shifted)
    return np.concatenate(delayed, axis=1)


def c2_audio_features(config: dict[str, Any], tr_times: np.ndarray) -> np.ndarray:
    from ridge_utils.interpdata import lanczosinterp2D

    c2 = config["c2"]
    acoustic = c2["acoustic"]
    audio_path = resolve_path(c2["files"]["audio"]["path"])
    with wave.open(str(audio_path), "rb") as stream:
        channels = stream.getnchannels()
        sample_width = stream.getsampwidth()
        sample_rate = stream.getframerate()
        frame_count = stream.getnframes()
        raw = stream.readframes(frame_count)
    require_equal(channels, int(acoustic["channels"]), "C2 audio channels")
    require_equal(sample_width, int(acoustic["sample_width_bytes"]), "C2 audio width")
    require_equal(sample_rate, int(acoustic["sample_rate_hz"]), "C2 audio rate")
    require_equal(frame_count, int(acoustic["frames"]), "C2 audio frames")
    waveform = np.frombuffer(raw, dtype="<i2").reshape(-1, channels)
    mono = waveform.astype(np.float64).mean(axis=1) / float(acoustic["scale_divisor"])
    window_samples = int(acoustic["window_samples"])
    hop_samples = int(acoustic["hop_samples"])
    fft_size = int(acoustic["fft_size"])
    starts = np.arange(
        0, len(mono) - window_samples + 1, hop_samples, dtype=np.int64
    )
    periodic_hann = np.hanning(window_samples + 1)[:-1].astype(np.float64)
    fft_frequencies = np.fft.rfftfreq(fft_size, d=1.0 / sample_rate)
    htk = lambda frequency: 2595.0 * np.log10(1.0 + frequency / 700.0)
    inverse_htk = lambda value: 700.0 * (np.power(10.0, value / 2595.0) - 1.0)
    edge_mels = np.linspace(
        htk(float(acoustic["minimum_hz"])),
        htk(float(acoustic["maximum_hz"])),
        int(acoustic["mel_edges"]),
    )
    edges = inverse_htk(edge_mels)
    filters = np.zeros(
        (int(acoustic["mel_bands"]), len(fft_frequencies)), dtype=np.float64
    )
    for band in range(filters.shape[0]):
        left, center, right = edges[band : band + 3]
        rising = (fft_frequencies - left) / (center - left)
        falling = (right - fft_frequencies) / (right - center)
        weights = np.maximum(np.minimum(rising, falling), 0.0)
        weight_sum = float(weights.sum())
        if weight_sum <= 0.0:
            raise ValueError(f"C2 mel filter {band} has no FFT support")
        filters[band] = weights / weight_sum
    log_energy = np.empty((len(starts), filters.shape[0]), dtype=np.float64)
    batch_size = 4096
    offsets = np.arange(window_samples, dtype=np.int64)
    for start in range(0, len(starts), batch_size):
        stop = min(start + batch_size, len(starts))
        frames = mono[starts[start:stop, None] + offsets[None, :]]
        spectrum = np.fft.rfft(frames * periodic_hann, n=fft_size, axis=1)
        power = np.square(np.abs(spectrum))
        energy = power @ filters.T
        log_energy[start:stop] = np.log(
            np.maximum(energy, float(acoustic["energy_floor"]))
        )
    difference = np.vstack(
        [np.zeros((1, log_energy.shape[1]), dtype=np.float64), np.diff(log_energy, axis=0)]
    )
    frame_features = np.concatenate([log_energy, difference], axis=1)
    frame_times = (starts + window_samples / 2.0) / sample_rate
    resampled = lanczosinterp2D(
        frame_features,
        frame_times,
        np.asarray(tr_times, dtype=np.float64),
        window=int(acoustic["lanczos_window"]),
    )
    trimmed = resampled[
        int(acoustic["trim_start"]) : -int(acoustic["trim_stop_from_end"])
    ]
    delayed = make_delayed_features(trimmed, [int(value) for value in acoustic["fir_delays"]])
    require_equal(delayed.shape[0], int(c2["time_rows"]), "C2 acoustic time rows")
    if not np.isfinite(delayed).all():
        raise ValueError("C2 acoustic block contains nonfinite values")
    return delayed


def build_c2_nuisance(config: dict[str, Any]) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    from scripts import lebel_adapter

    c2 = config["c2"]
    story = "wheretheressmoke"
    word_sequence = lebel_adapter.get_wordseqs([story])[story]
    low, eng = lebel_adapter.nuisance_features(story, word_sequence)
    acoustic = c2["acoustic"]
    trim_start = int(acoustic["trim_start"])
    trim_stop = int(acoustic["trim_stop_from_end"])
    delays = [int(value) for value in acoustic["fir_delays"]]
    low_trimmed = np.asarray(low[trim_start:-trim_stop], dtype=np.float64)
    eng_trimmed = np.asarray(eng[trim_start:-trim_stop], dtype=np.float64)
    low_delayed = make_delayed_features(low_trimmed, delays)
    eng_delayed = make_delayed_features(eng_trimmed, delays)
    audio_delayed = c2_audio_features(config, np.asarray(word_sequence.tr_times))
    for label, values in (
        ("low", low_delayed),
        ("eng1000", eng_delayed),
        ("acoustic", audio_delayed),
    ):
        require_equal(values.shape[0], int(c2["time_rows"]), f"C2 {label} rows")
        if not np.isfinite(values).all():
            raise ValueError(f"C2 {label} nuisance contains nonfinite values")
    arrays = {
        "low": low_delayed.astype(np.float32),
        "eng1000": eng_delayed.astype(np.float32),
        "acoustic": audio_delayed.astype(np.float32),
    }
    metadata = {
        "schema_version": "1.0",
        "created_at_utc": utc_now(),
        "rows": int(c2["time_rows"]),
        "delays": delays,
        "trim": [trim_start, -trim_stop],
        "array_sha256": {
            key: sha256_array(values) for key, values in arrays.items()
        },
        "input_hashes": {
            name: c2["files"][name]["sha256"]
            for name in ("textgrid", "audio", "eng1000", "adapter")
        },
        "configuration_payload_sha256": stable_hash(config),
        "executable_sha256": sha256_file(Path(__file__).resolve()),
        "c2_nuisance_spec_sha256": stable_hash(
            {
                "time_rows": c2["time_rows"],
                "acoustic": c2["acoustic"],
                "input_hashes": {
                    name: c2["files"][name]["sha256"]
                    for name in ("textgrid", "audio", "eng1000", "adapter")
                },
            }
        ),
    }
    cache_arrays = dict(arrays)
    cache_arrays["metadata_json"] = np.asarray(canonical_json(metadata))
    atomic_savez(resolve_path(config["outputs"]["c2_nuisance"]), cache_arrays)
    return {key: np.asarray(value, dtype=np.float64) for key, value in arrays.items()}, metadata


def load_or_build_c2_nuisance(
    config: dict[str, Any],
) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    path = resolve_path(config["outputs"]["c2_nuisance"])
    if path.is_file():
        with np.load(path, allow_pickle=False) as cached:
            metadata = json.loads(str(cached["metadata_json"].item()))
            expected_hashes = {
                name: config["c2"]["files"][name]["sha256"]
                for name in ("textgrid", "audio", "eng1000", "adapter")
            }
            expected_spec_hash = stable_hash(
                {
                    "time_rows": config["c2"]["time_rows"],
                    "acoustic": config["c2"]["acoustic"],
                    "input_hashes": expected_hashes,
                }
            )
            current = (
                metadata.get("input_hashes") == expected_hashes
                and metadata.get("configuration_payload_sha256") == stable_hash(config)
                and metadata.get("executable_sha256")
                == sha256_file(Path(__file__).resolve())
                and metadata.get("c2_nuisance_spec_sha256") == expected_spec_hash
                and metadata.get("rows") == int(config["c2"]["time_rows"])
            )
            if not current:
                return build_c2_nuisance(config)
            arrays = {
                key: np.asarray(cached[key], dtype=np.float64)
                for key in ("low", "eng1000", "acoustic")
            }
        for key, values in arrays.items():
            require_equal(
                sha256_array(values.astype(np.float32)),
                metadata["array_sha256"][key],
                f"C2 cached {key} hash",
            )
        return arrays, metadata
    return build_c2_nuisance(config)


def c2_time_blocks(config: dict[str, Any]) -> tuple[list[np.ndarray], list[np.ndarray]]:
    blocks = [
        np.asarray(block, dtype=np.int64)
        for block in np.array_split(np.arange(int(config["c2"]["time_rows"])), 5)
    ]
    require_equal(
        [len(block) for block in blocks],
        config["c2"]["outer_block_lengths"],
        "C2 block lengths",
    )
    purge = int(config["c2"]["boundary_purge_trs"])
    retained = [block[purge:-purge] for block in blocks]
    if any(len(block) // 2 <= purge for block in retained):
        raise ValueError("C2 retained shift offset is not wider than the purge")
    return blocks, retained


def c2_shift_map(config: dict[str, Any]) -> tuple[np.ndarray, list[dict[str, Any]]]:
    _, retained = c2_time_blocks(config)
    mapping = np.arange(int(config["c2"]["time_rows"]), dtype=np.int64)
    records: list[dict[str, Any]] = []
    for segment, rows in enumerate(retained):
        shifted = block_local_shift(rows)
        mapping[rows] = shifted
        records.append(
            {
                "segment": segment,
                "offset": int(len(rows) // 2),
                "row_map_sha256": sha256_bytes(shifted.astype("<i8").tobytes()),
            }
        )
    return mapping, records


def c2_nuisance_design(
    raw: dict[str, np.ndarray],
    train: np.ndarray,
    apply: np.ndarray,
    config: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    floor = float(config["c2"]["builder_variance_floor"])
    low_train, low_apply, _, _ = fit_standardizer(raw["low"][train], raw["low"][apply], floor)
    acoustic_train, acoustic_apply, _, _ = fit_standardizer(
        raw["acoustic"][train], raw["acoustic"][apply], floor
    )
    eng_train, eng_apply, _, _ = fit_standardizer(
        raw["eng1000"][train], raw["eng1000"][apply], floor
    )
    eng_train, eng_apply, pca = fit_pca_svd(
        eng_train,
        eng_apply,
        int(config["c2"]["eng1000_pca_rank"]),
    )
    nuisance_train = np.concatenate([low_train, eng_train, acoustic_train], axis=1)
    nuisance_apply = np.concatenate([low_apply, eng_apply, acoustic_apply], axis=1)
    nuisance_train, nuisance_apply, _, _ = fit_standardizer(
        nuisance_train, nuisance_apply, floor
    )
    return nuisance_train, nuisance_apply, {
        "columns": int(nuisance_train.shape[1]),
        "eng1000_pca": pca,
    }


def c2_builder_mask(
    response_path: Path,
    builder_repeats: list[int],
    retained_rows: np.ndarray,
    config: dict[str, Any],
) -> np.ndarray:
    voxel_count = int(config["c2"]["voxel_count"])
    mask = np.ones(voxel_count, dtype=bool)
    chunk = 4096
    with h5py.File(response_path, "r") as handle:
        dataset = handle["individual_repeats"]
        _, retained_blocks = c2_time_blocks(config)
        retained_lookup = {
            int(row): index
            for index, row in enumerate(retained_rows.tolist())
        }
        outer_train_local = [
            np.asarray(
                [
                    retained_lookup[int(row)]
                    for block_index, block in enumerate(retained_blocks)
                    if block_index != outer_test
                    for row in block
                ],
                dtype=np.int64,
            )
            for outer_test in range(len(retained_blocks))
        ]
        subsets = [
            subset
            for size_subsets in repeat_subsets(builder_repeats).values()
            for subset in size_subsets
        ]
        repeat_locations = {
            int(repeat): index for index, repeat in enumerate(builder_repeats)
        }
        for start in range(0, voxel_count, chunk):
            stop = min(start + chunk, voxel_count)
            values = np.stack(
                [
                    np.asarray(dataset[int(repeat), retained_rows, start:stop], dtype=np.float64)
                    for repeat in builder_repeats
                ],
                axis=0,
            )
            finite = np.isfinite(values).all(axis=(0, 1))
            variance = np.var(values, axis=(0, 1), ddof=0)
            valid = finite & (variance > float(config["c2"]["builder_variance_floor"]))
            for subset in subsets:
                locations = [repeat_locations[int(repeat)] for repeat in subset]
                target = values[locations].mean(axis=0)
                for train_local in outer_train_local:
                    valid &= (
                        np.std(target[train_local], axis=0, ddof=0)
                        > float(config["c2"]["builder_variance_floor"])
                    )
            mask[start:stop] = valid
    if not np.any(mask):
        raise ValueError("C2 builder mask is empty")
    return mask


def load_c2_repeat_mean(
    response_path: Path,
    repeats: list[int] | tuple[int, ...],
    mask: np.ndarray,
) -> np.ndarray:
    indices = np.flatnonzero(mask)
    positions = np.full(mask.size, -1, dtype=np.int64)
    positions[indices] = np.arange(len(indices), dtype=np.int64)
    with h5py.File(response_path, "r") as handle:
        dataset = handle["individual_repeats"]
        accumulator = np.zeros((dataset.shape[1], len(indices)), dtype=np.float64)
        chunk = 4096
        for start in range(0, mask.size, chunk):
            stop = min(start + chunk, mask.size)
            local = mask[start:stop]
            if not np.any(local):
                continue
            selected_positions = positions[start:stop][local]
            values = np.stack(
                [
                    np.asarray(dataset[int(repeat), :, start:stop], dtype=np.float64)[
                        :, local
                    ]
                    for repeat in repeats
                ],
                axis=0,
            )
            accumulator[:, selected_positions] = values.mean(axis=0)
    return accumulator


def choose_alpha_from_losses(
    losses: dict[float, float], tolerance: float
) -> float:
    best_alpha: float | None = None
    best_loss = np.inf
    for alpha in sorted(losses):
        loss = float(losses[alpha])
        if loss < best_loss - tolerance or (
            abs(loss - best_loss) <= tolerance
            and (best_alpha is None or alpha > best_alpha)
        ):
            best_alpha = float(alpha)
            best_loss = loss
    if best_alpha is None:
        raise RuntimeError("C2 alpha selection did not choose an alpha")
    return best_alpha


def c2_torch_predictions(
    nuisance_train: Any,
    nuisance_test: Any,
    outcome_train: Any,
    aligned_train: Any | None,
    aligned_test: Any | None,
    shifted_train: Any | None,
    shifted_test: Any | None,
    alpha: float,
) -> tuple[Any, Any | None, Any | None]:
    import torch

    gram = nuisance_train @ nuisance_train.T
    identity = torch.eye(
        gram.shape[0], dtype=gram.dtype, device=gram.device
    )
    factor = torch.linalg.cholesky(gram + float(alpha) * identity)
    solved_outcome = torch.cholesky_solve(outcome_train, factor)
    cross = nuisance_test @ nuisance_train.T
    nuisance_prediction = cross @ solved_outcome
    if aligned_train is None:
        return nuisance_prediction, None, None
    if (
        aligned_test is None
        or shifted_train is None
        or shifted_test is None
    ):
        raise ValueError("C2 full prediction requires aligned and shifted targets")
    stacked = torch.cat([aligned_train, shifted_train], dim=1)
    solved_targets = torch.cholesky_solve(stacked, factor)
    fitted_outcome_train = gram @ solved_outcome
    fitted_targets_train = gram @ solved_targets
    voxel_count = aligned_train.shape[1]
    aligned_fitted = fitted_targets_train[:, :voxel_count]
    shifted_fitted = fitted_targets_train[:, voxel_count:]
    aligned_solved = solved_targets[:, :voxel_count]
    shifted_solved = solved_targets[:, voxel_count:]
    outcome_residual = outcome_train - fitted_outcome_train
    aligned_denominator = float(alpha) + torch.sum(
        aligned_train * (aligned_train - aligned_fitted), dim=0
    )
    shifted_denominator = float(alpha) + torch.sum(
        shifted_train * (shifted_train - shifted_fitted), dim=0
    )
    if bool(torch.any(aligned_denominator <= 0.0)) or bool(
        torch.any(shifted_denominator <= 0.0)
    ):
        raise ValueError("C2 ridge Schur complement is nonpositive")
    aligned_coefficient = torch.sum(
        aligned_train * outcome_residual, dim=0
    ) / aligned_denominator
    shifted_coefficient = torch.sum(
        shifted_train * outcome_residual, dim=0
    ) / shifted_denominator
    aligned_residual_test = aligned_test - cross @ aligned_solved
    shifted_residual_test = shifted_test - cross @ shifted_solved
    aligned_prediction = (
        nuisance_prediction
        + aligned_residual_test * aligned_coefficient[None, :]
    )
    shifted_prediction = (
        nuisance_prediction
        + shifted_residual_test * shifted_coefficient[None, :]
    )
    return nuisance_prediction, aligned_prediction, shifted_prediction


def c2_evaluate_target(
    predictor: np.ndarray,
    outcome: np.ndarray,
    nuisance_raw: dict[str, np.ndarray],
    config: dict[str, Any],
    device: str,
) -> dict[str, Any]:
    import torch

    c2 = config["c2"]
    if predictor.shape != outcome.shape or predictor.ndim != 2:
        raise ValueError("C2 predictor/outcome matrices are incompatible")
    _, retained_blocks = c2_time_blocks(config)
    retained_rows = np.concatenate(retained_blocks)
    shift_map, _ = c2_shift_map(config)
    if not np.isfinite(predictor).all() or not np.isfinite(outcome).all():
        raise ValueError("C2 target or outcome has nonfinite values")
    torch_device = torch.device(device)
    predictor_tensor = torch.as_tensor(
        predictor, dtype=torch.float64, device=torch_device
    )
    outcome_tensor = torch.as_tensor(
        outcome, dtype=torch.float64, device=torch_device
    )
    shift_tensor = torch.as_tensor(shift_map, dtype=torch.long, device=torch_device)
    shifted_tensor = predictor_tensor.index_select(0, shift_tensor)
    voxel_count = predictor.shape[1]
    sse_nuisance = torch.zeros(voxel_count, dtype=torch.float64, device=torch_device)
    sse_aligned = torch.zeros_like(sse_nuisance)
    sse_shifted = torch.zeros_like(sse_nuisance)
    fold_records: list[dict[str, Any]] = []
    tolerance = float(c2["ridge_tie_tolerance"])
    for outer_test_index, test_rows in enumerate(retained_blocks):
        train_blocks = [
            block for index, block in enumerate(retained_blocks)
            if index != outer_test_index
        ]
        train_rows = np.concatenate(train_blocks)
        nuisance_train_np, nuisance_all_np, nuisance_meta = c2_nuisance_design(
            nuisance_raw, train_rows, retained_rows, config
        )
        nuisance_full_np = np.zeros(
            (int(c2["time_rows"]), nuisance_all_np.shape[1]), dtype=np.float64
        )
        nuisance_full_np[retained_rows] = nuisance_all_np
        nuisance_full = torch.as_tensor(
            nuisance_full_np, dtype=torch.float64, device=torch_device
        )
        train_index = torch.as_tensor(train_rows, dtype=torch.long, device=torch_device)
        test_index = torch.as_tensor(test_rows, dtype=torch.long, device=torch_device)
        predictor_mean = predictor_tensor.index_select(0, train_index).mean(dim=0)
        predictor_scale = predictor_tensor.index_select(0, train_index).std(
            dim=0, correction=0
        )
        outcome_mean = outcome_tensor.index_select(0, train_index).mean(dim=0)
        outcome_scale = outcome_tensor.index_select(0, train_index).std(
            dim=0, correction=0
        )
        if bool(torch.any(predictor_scale <= float(c2["builder_variance_floor"]))):
            raise ValueError("C2 predictor training variance fell below the sealed floor")
        if bool(torch.any(outcome_scale <= float(c2["evaluation_sst_floor"]))):
            raise ValueError("C2 outcome training variance fell below the frozen floor")
        predictor_z = (predictor_tensor - predictor_mean) / predictor_scale
        shifted_z = (shifted_tensor - predictor_mean) / predictor_scale
        outcome_z = (outcome_tensor - outcome_mean) / outcome_scale
        losses = {
            "nuisance": {float(alpha): 0.0 for alpha in c2["ridge_alphas"]},
            "aligned": {float(alpha): 0.0 for alpha in c2["ridge_alphas"]},
            "shifted": {float(alpha): 0.0 for alpha in c2["ridge_alphas"]},
        }
        count = 0
        for validation_rows in train_blocks:
            fit_rows = np.concatenate(
                [block for block in train_blocks if not np.array_equal(block, validation_rows)]
            )
            fit_index = torch.as_tensor(fit_rows, dtype=torch.long, device=torch_device)
            validation_index = torch.as_tensor(
                validation_rows, dtype=torch.long, device=torch_device
            )
            for alpha_value in c2["ridge_alphas"]:
                alpha = float(alpha_value)
                nuisance_prediction, aligned_prediction, shifted_prediction = (
                    c2_torch_predictions(
                        nuisance_full.index_select(0, fit_index),
                        nuisance_full.index_select(0, validation_index),
                        outcome_z.index_select(0, fit_index),
                        predictor_z.index_select(0, fit_index),
                        predictor_z.index_select(0, validation_index),
                        shifted_z.index_select(0, fit_index),
                        shifted_z.index_select(0, validation_index),
                        alpha,
                    )
                )
                observed = outcome_z.index_select(0, validation_index)
                losses["nuisance"][alpha] += float(
                    torch.sum(torch.square(observed - nuisance_prediction)).item()
                )
                losses["aligned"][alpha] += float(
                    torch.sum(torch.square(observed - aligned_prediction)).item()
                )
                losses["shifted"][alpha] += float(
                    torch.sum(torch.square(observed - shifted_prediction)).item()
                )
            count += int(len(validation_rows) * voxel_count)
        mean_losses = {
            arm: {alpha: value / count for alpha, value in arm_losses.items()}
            for arm, arm_losses in losses.items()
        }
        selected = {
            arm: choose_alpha_from_losses(arm_losses, tolerance)
            for arm, arm_losses in mean_losses.items()
        }
        predictions_by_alpha: dict[float, tuple[Any, Any, Any]] = {}
        for alpha in sorted(set(selected.values())):
            predictions_by_alpha[alpha] = c2_torch_predictions(
                nuisance_full.index_select(0, train_index),
                nuisance_full.index_select(0, test_index),
                outcome_z.index_select(0, train_index),
                predictor_z.index_select(0, train_index),
                predictor_z.index_select(0, test_index),
                shifted_z.index_select(0, train_index),
                shifted_z.index_select(0, test_index),
                alpha,
            )
        nuisance_prediction = predictions_by_alpha[selected["nuisance"]][0]
        aligned_prediction = predictions_by_alpha[selected["aligned"]][1]
        shifted_prediction = predictions_by_alpha[selected["shifted"]][2]
        observed_raw = outcome_tensor.index_select(0, test_index)
        nuisance_raw_prediction = nuisance_prediction * outcome_scale + outcome_mean
        aligned_raw_prediction = aligned_prediction * outcome_scale + outcome_mean
        shifted_raw_prediction = shifted_prediction * outcome_scale + outcome_mean
        sse_nuisance += torch.sum(
            torch.square(observed_raw - nuisance_raw_prediction), dim=0
        )
        sse_aligned += torch.sum(
            torch.square(observed_raw - aligned_raw_prediction), dim=0
        )
        sse_shifted += torch.sum(
            torch.square(observed_raw - shifted_raw_prediction), dim=0
        )
        fold_sst = torch.sum(
            torch.square(observed_raw - observed_raw.mean(dim=0)), dim=0
        )
        valid_fold = fold_sst > float(c2["evaluation_sst_floor"])
        fold_contrast = torch.full_like(fold_sst, torch.nan)
        fold_contrast[valid_fold] = (
            torch.sum(
                torch.square(observed_raw - shifted_raw_prediction)
                - torch.square(observed_raw - aligned_raw_prediction),
                dim=0,
            )[valid_fold]
            / fold_sst[valid_fold]
        )
        fold_records.append(
            {
                "outer_test_index": outer_test_index,
                "test_rows": test_rows.tolist(),
                "train_rows": int(len(train_rows)),
                "nuisance": nuisance_meta,
                "selected_alphas": selected,
                "inner_mean_mse": {
                    arm: {str(alpha): value for alpha, value in values.items()}
                    for arm, values in mean_losses.items()
                },
                "median_aligned_minus_shifted_fold_unique_r2": float(
                    torch.nanmedian(fold_contrast).item()
                ),
            }
        )
        del (
            nuisance_full,
            predictor_z,
            shifted_z,
            outcome_z,
            predictions_by_alpha,
        )
        if torch_device.type == "cuda":
            torch.cuda.empty_cache()
    retained_index = torch.as_tensor(
        retained_rows, dtype=torch.long, device=torch_device
    )
    retained_outcome = outcome_tensor.index_select(0, retained_index)
    sst = torch.sum(
        torch.square(retained_outcome - retained_outcome.mean(dim=0)), dim=0
    )
    if bool(torch.any(sst <= float(c2["evaluation_sst_floor"]))):
        raise ValueError("C2 concatenated outcome SST is at or below the frozen floor")
    aligned_unique = (sse_nuisance - sse_aligned) / sst
    shifted_unique = (sse_nuisance - sse_shifted) / sst
    if not bool(torch.isfinite(aligned_unique).all()) or not bool(
        torch.isfinite(shifted_unique).all()
    ):
        raise ValueError("C2 unique R2 contains nonfinite values")
    return {
        "aligned_unique_r2": aligned_unique.detach().cpu().numpy(),
        "shifted_unique_r2": shifted_unique.detach().cpu().numpy(),
        "folds": fold_records,
    }


def c2_data_hashes(config: dict[str, Any]) -> dict[str, str]:
    return {
        name: str(config["c2"]["files"][name]["sha256"])
        for name in ("response_hdf", "textgrid", "audio", "eng1000", "adapter")
    }


def validate_builder_seal_against_config(
    seal: dict[str, Any],
    config: dict[str, Any],
    config_path: Path,
) -> None:
    c2 = config["c2"]
    builder_repeats = [int(value) for value in c2["builder_repeats"]]
    validate_builder_seal_structure(seal, builder_repeats)
    require_equal(
        float(seal["delta_c2"]),
        float(c2["response_fraction"]) * float(seal["r_builder"]),
        "C2 builder delta arithmetic",
    )
    blocks, _ = c2_time_blocks(config)
    require_equal(
        seal["folds"],
        [block.tolist() for block in blocks],
        "C2 builder folds",
    )
    _, shift_records = c2_shift_map(config)
    require_equal(seal["shift_maps"], shift_records, "C2 builder shift maps")
    require_equal(seal["data_hashes"], c2_data_hashes(config), "C2 builder data hashes")
    require_equal(
        seal["nuisance_cache_sha256"],
        sha256_file(resolve_path(config["outputs"]["c2_nuisance"])),
        "C2 builder nuisance-cache hash",
    )
    c1_result = validate_c1_result_artifact(config, config_path)
    require_equal(
        seal["c1_result_payload_sha256"],
        c1_result["result_payload_sha256"],
        "C2 builder C1-result binding",
    )
    require_equal(
        seal["configuration_sha256"],
        sha256_file(config_path),
        "C2 builder configuration hash",
    )
    require_equal(
        seal["executable_sha256"],
        sha256_file(Path(__file__).resolve()),
        "C2 builder executable hash",
    )


def validate_builder_arrays_against_seal(
    seal: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, np.ndarray]:
    path = resolve_path(config["outputs"]["builder_arrays"])
    require_equal(
        sha256_file(path),
        seal["builder_arrays_sha256"],
        "C2 builder array artifact hash",
    )
    with np.load(path, allow_pickle=False) as cached:
        require_equal(
            set(cached.files),
            {
                "primary_voxel_indices",
                "direction_aligned_unique_r2",
                "direction_shifted_unique_r2",
            },
            "C2 builder array keys",
        )
        indices = np.asarray(cached["primary_voxel_indices"], dtype="<i8")
        aligned = np.asarray(cached["direction_aligned_unique_r2"], dtype=np.float64)
        shifted = np.asarray(cached["direction_shifted_unique_r2"], dtype=np.float64)
    if (
        indices.ndim != 1
        or aligned.shape != shifted.shape
        or aligned.shape != (20, len(indices))
        or not np.array_equal(indices, np.unique(indices))
        or (indices.size and (indices[0] < 0 or indices[-1] >= int(config["c2"]["voxel_count"])))
    ):
        raise ValueError("C2 builder array shapes or voxel identities are invalid")
    if not np.isfinite(aligned).all() or not np.isfinite(shifted).all():
        raise ValueError("C2 builder arrays contain nonfinite values")
    require_equal(
        sha256_bytes(indices.astype("<i8").tobytes()),
        seal["primary_mask_sha256"],
        "C2 builder array mask hash",
    )
    direction_values = np.median(aligned - shifted, axis=1).astype("<f8")
    require_equal(
        sha256_array(direction_values),
        seal["direction_values_sha256"],
        "C2 builder direction-value hash",
    )
    require_equal(
        float(np.mean(direction_values, dtype=np.float64)),
        float(seal["r_builder"]),
        "C2 builder R arithmetic from arrays",
    )
    return {
        "primary_voxel_indices": indices,
        "direction_aligned_unique_r2": aligned,
        "direction_shifted_unique_r2": shifted,
    }


def c2_mask_sha256(mask: np.ndarray) -> str:
    return sha256_bytes(np.flatnonzero(mask).astype("<i8").tobytes())


def c2_load_repeat_stack(
    response_path: Path,
    repeats: list[int],
    mask: np.ndarray,
) -> np.ndarray:
    return np.stack(
        [load_c2_repeat_mean(response_path, [repeat], mask) for repeat in repeats],
        axis=0,
    )


def run_c2_build(
    config: dict[str, Any],
    config_path: Path,
    device: str,
) -> dict[str, Any]:
    c1_result = validate_c1_result_artifact(config, config_path)
    c2 = config["c2"]
    file_records = {
        name: file_record(c2["files"][name])
        for name in ("response_hdf", "textgrid", "audio", "eng1000", "adapter")
    }
    nuisance, nuisance_metadata = load_or_build_c2_nuisance(config)
    response_path = resolve_path(c2["files"]["response_hdf"]["path"])
    _, retained_blocks = c2_time_blocks(config)
    retained_rows = np.concatenate(retained_blocks)
    builder_repeats = [int(value) for value in c2["builder_repeats"]]
    mask = c2_builder_mask(
        response_path, builder_repeats, retained_rows, config
    )
    repeat_stack = c2_load_repeat_stack(response_path, builder_repeats, mask)
    repeat_locations = {
        repeat: index for index, repeat in enumerate(builder_repeats)
    }
    directions = expected_builder_directions(builder_repeats)
    direction_records: list[dict[str, Any]] = []
    aligned_rows: list[np.ndarray] = []
    shifted_rows: list[np.ndarray] = []
    directed_values: list[float] = []
    for direction_index, direction in enumerate(directions):
        predictor_locations = [
            repeat_locations[int(repeat)]
            for repeat in direction["predictor_repeats"]
        ]
        outcome_locations = [
            repeat_locations[int(repeat)]
            for repeat in direction["outcome_repeats"]
        ]
        predictor = repeat_stack[predictor_locations].mean(axis=0)
        outcome = repeat_stack[outcome_locations].mean(axis=0)
        evaluated = c2_evaluate_target(
            predictor, outcome, nuisance, config, device
        )
        aligned = np.asarray(evaluated["aligned_unique_r2"], dtype=np.float64)
        shifted = np.asarray(evaluated["shifted_unique_r2"], dtype=np.float64)
        contrast = aligned - shifted
        directed_value = float(np.median(contrast))
        directed_values.append(directed_value)
        aligned_rows.append(aligned.astype(np.float64))
        shifted_rows.append(shifted.astype(np.float64))
        direction_records.append(
            {
                "direction_index": direction_index,
                **direction,
                "median_aligned_minus_shifted_unique_r2": directed_value,
                "mean_aligned_minus_shifted_unique_r2": float(np.mean(contrast)),
                "positive_voxel_fraction": float(np.mean(contrast > 0.0)),
                "folds": evaluated["folds"],
            }
        )
    r_builder = float(np.mean(np.asarray(directed_values, dtype=np.float64)))
    delta_c2 = float(c2["response_fraction"]) * r_builder
    blocks, _ = c2_time_blocks(config)
    _, shift_records = c2_shift_map(config)
    arrays = {
        "primary_voxel_indices": np.flatnonzero(mask).astype("<i8"),
        "direction_aligned_unique_r2": np.stack(aligned_rows, axis=0),
        "direction_shifted_unique_r2": np.stack(shifted_rows, axis=0),
    }
    arrays_path = resolve_path(config["outputs"]["builder_arrays"])
    atomic_savez(arrays_path, arrays)
    arrays_sha256 = sha256_file(arrays_path)
    direction_values_array = np.asarray(directed_values, dtype="<f8")
    seal = {
        "r_builder": r_builder,
        "delta_c2": delta_c2,
        "partitions": [
            {
                "left": list(left),
                "right": sorted(set(builder_repeats) - set(left)),
            }
            for left in itertools.combinations(builder_repeats, 2)
        ],
        "directions": directions,
        "folds": [block.tolist() for block in blocks],
        "shift_maps": shift_records,
        "primary_mask_sha256": c2_mask_sha256(mask),
        "builder_arrays_sha256": arrays_sha256,
        "direction_values_sha256": sha256_array(direction_values_array),
        "nuisance_cache_sha256": sha256_file(
            resolve_path(config["outputs"]["c2_nuisance"])
        ),
        "c1_result_payload_sha256": c1_result["result_payload_sha256"],
        "aggregation_constants": {
            "partition_reduction": "mean_within_voxel",
            "voxel_reduction": "median",
            "direction_reduction": "equal_mean_20",
        },
        "data_hashes": c2_data_hashes(config),
        "configuration_sha256": sha256_file(config_path),
        "executable_sha256": sha256_file(Path(__file__).resolve()),
    }
    validate_builder_seal_against_config(seal, config, config_path)
    seal_path = resolve_path(config["outputs"]["builder_seal"])
    atomic_write_json(seal_path, seal)
    seal_file_sha256 = sha256_file(seal_path)
    result = {
        "schema_version": "1.0",
        "experiment": "E031",
        "stage": "c2-build",
        "created_at_utc": utc_now(),
        "status": "SEALED",
        "classification": (
            "BUILDER INSTRUMENT FLOOR"
            if r_builder < float(c2["builder_floor"])
            else "BUILDER ADEQUATE"
        ),
        "evaluation_repeats_accessed": False,
        "r_builder": r_builder,
        "delta_c2": delta_c2,
        "builder_floor": float(c2["builder_floor"]),
        "primary_voxel_count": int(mask.sum()),
        "primary_mask_sha256": c2_mask_sha256(mask),
        "directions": direction_records,
        "seal": {
            "path": str(seal_path.relative_to(REPO_ROOT)),
            "sha256": seal_file_sha256,
            "payload_sha256": stable_hash(seal),
        },
        "arrays": {
            "path": str(arrays_path.relative_to(REPO_ROOT)),
            "sha256": arrays_sha256,
            "keys": sorted(arrays),
        },
        "nuisance": {
            "path": config["outputs"]["c2_nuisance"],
            "sha256": sha256_file(resolve_path(config["outputs"]["c2_nuisance"])),
            "metadata": nuisance_metadata,
        },
        "inputs": file_records,
        "c1_result_payload_sha256": c1_result["result_payload_sha256"],
    }
    result["result_payload_sha256"] = stable_hash(result)
    build_result_path = resolve_path(config["outputs"]["directory"]) / "c2_builder_result.json"
    atomic_write_json(build_result_path, result)
    return result


def c2_curve_from_subset_rows(
    aligned_rows: list[np.ndarray],
    shifted_rows: list[np.ndarray],
    subset_sizes: list[int],
) -> tuple[dict[str, Any], dict[int, np.ndarray]]:
    curve: dict[str, Any] = {}
    contrasts: dict[int, np.ndarray] = {}
    for size in sorted(set(subset_sizes)):
        selected = [index for index, value in enumerate(subset_sizes) if value == size]
        aligned_mean = np.mean(
            np.stack([aligned_rows[index] for index in selected], axis=0),
            axis=0,
            dtype=np.float64,
        )
        shifted_mean = np.mean(
            np.stack([shifted_rows[index] for index in selected], axis=0),
            axis=0,
            dtype=np.float64,
        )
        contrast = aligned_mean - shifted_mean
        contrasts[size] = contrast
        curve[str(size)] = {
            "subset_count": len(selected),
            "median_aligned_minus_shifted_unique_r2": float(np.median(contrast)),
            "mean_aligned_minus_shifted_unique_r2": float(np.mean(contrast)),
            "positive_voxel_fraction": float(np.mean(contrast > 0.0)),
            "aligned_unique_r2_median": float(np.median(aligned_mean)),
            "aligned_unique_r2_mean": float(np.mean(aligned_mean)),
            "shifted_unique_r2_median": float(np.median(shifted_mean)),
            "shifted_unique_r2_mean": float(np.mean(shifted_mean)),
        }
    return curve, contrasts


def c2_score_assignment(
    builder_repeat_indices: list[int],
    outcome_repeat_indices: list[int],
    response_path: Path,
    mask: np.ndarray,
    nuisance: dict[str, np.ndarray],
    config: dict[str, Any],
    device: str,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    builder_stack = c2_load_repeat_stack(response_path, builder_repeat_indices, mask)
    outcome = load_c2_repeat_mean(response_path, outcome_repeat_indices, mask)
    if not np.isfinite(outcome).all():
        raise ValueError("C2 evaluation outcome contains nonfinite values in the sealed mask")
    subsets = repeat_subsets(builder_repeat_indices)
    subset_records: list[dict[str, Any]] = []
    subset_sizes: list[int] = []
    aligned_rows: list[np.ndarray] = []
    shifted_rows: list[np.ndarray] = []
    locations = {
        repeat: index for index, repeat in enumerate(builder_repeat_indices)
    }
    for size in sorted(subsets):
        for subset_index, subset in enumerate(subsets[size]):
            predictor = builder_stack[
                [locations[int(repeat)] for repeat in subset]
            ].mean(axis=0)
            evaluated = c2_evaluate_target(
                predictor, outcome, nuisance, config, device
            )
            aligned = np.asarray(evaluated["aligned_unique_r2"], dtype=np.float64)
            shifted = np.asarray(evaluated["shifted_unique_r2"], dtype=np.float64)
            contrast = aligned - shifted
            aligned_rows.append(aligned.astype(np.float64))
            shifted_rows.append(shifted.astype(np.float64))
            subset_sizes.append(int(size))
            subset_records.append(
                {
                    "repeat_count": int(size),
                    "subset_index": subset_index,
                    "builder_repeats": list(subset),
                    "aligned_unique_r2_median": float(np.median(aligned)),
                    "aligned_unique_r2_mean": float(np.mean(aligned)),
                    "median_aligned_minus_shifted_unique_r2": float(
                        np.median(contrast)
                    ),
                    "folds": evaluated["folds"],
                }
            )
    curve, contrasts = c2_curve_from_subset_rows(
        aligned_rows, shifted_rows, subset_sizes
    )
    points = np.asarray(
        [
            curve[str(size)]["median_aligned_minus_shifted_unique_r2"]
            for size in range(1, 6)
        ],
        dtype=np.float64,
    )
    scale = 1.0 - 1.0 / np.arange(1, 6, dtype=np.float64)
    slope = float(np.linalg.lstsq(
        np.column_stack([np.ones(5), scale]), points, rcond=None
    )[0][1])
    t_value = float(points[-1] - points[0])
    arrays = {
        "subset_sizes": np.asarray(subset_sizes, dtype=np.int8),
        "aligned_unique_r2": np.stack(aligned_rows, axis=0),
        "shifted_unique_r2": np.stack(shifted_rows, axis=0),
    }
    result = {
        "builder_repeats": builder_repeat_indices,
        "outcome_repeats": outcome_repeat_indices,
        "subset_records": subset_records,
        "curve": curve,
        "t_k5_minus_k1": t_value,
        "slope_against_one_minus_inverse_k": slope,
    }
    return result, arrays


def run_c2_score(
    config: dict[str, Any],
    config_path: Path,
    expected_seal_sha256: str,
    device: str,
) -> dict[str, Any]:
    c2 = config["c2"]
    seal_path = resolve_path(config["outputs"]["builder_seal"])
    observed_seal_sha256 = sha256_file(seal_path)
    require_equal(
        observed_seal_sha256,
        expected_seal_sha256,
        "C2 builder seal file SHA-256",
    )
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    validate_builder_seal_against_config(seal, config, config_path)
    validate_builder_arrays_against_seal(seal, config)
    if float(seal["r_builder"]) < float(c2["builder_floor"]):
        return {
            "experiment": "E031",
            "stage": "c2-score",
            "status": "NOT_OPENED",
            "classification": "BUILDER INSTRUMENT FLOOR",
            "evaluation_repeats_accessed": False,
            "r_builder": float(seal["r_builder"]),
        }
    nuisance, nuisance_metadata = load_or_build_c2_nuisance(config)
    response_path = resolve_path(c2["files"]["response_hdf"]["path"])
    _, retained_blocks = c2_time_blocks(config)
    retained_rows = np.concatenate(retained_blocks)
    builder_repeats = [int(value) for value in c2["builder_repeats"]]
    evaluation_repeats = [int(value) for value in c2["evaluation_repeats"]]
    primary_mask = c2_builder_mask(
        response_path, builder_repeats, retained_rows, config
    )
    require_equal(
        c2_mask_sha256(primary_mask),
        seal["primary_mask_sha256"],
        "C2 recomputed primary mask",
    )
    primary, primary_arrays = c2_score_assignment(
        builder_repeats,
        evaluation_repeats,
        response_path,
        primary_mask,
        nuisance,
        config,
        device,
    )
    t_value = float(primary["t_k5_minus_k1"])
    slope = float(primary["slope_against_one_minus_inverse_k"])
    delta_c2 = float(seal["delta_c2"])
    primary_pass = t_value >= delta_c2 and slope > 0.0

    reverse_mask = c2_builder_mask(
        response_path, evaluation_repeats, retained_rows, config
    )
    reverse, reverse_arrays = c2_score_assignment(
        evaluation_repeats,
        builder_repeats,
        response_path,
        reverse_mask,
        nuisance,
        config,
        device,
    )
    arrays = {
        "primary_voxel_indices": np.flatnonzero(primary_mask).astype("<i8"),
        "primary_subset_sizes": primary_arrays["subset_sizes"],
        "primary_aligned_unique_r2": primary_arrays["aligned_unique_r2"],
        "primary_shifted_unique_r2": primary_arrays["shifted_unique_r2"],
        "reverse_voxel_indices": np.flatnonzero(reverse_mask).astype("<i8"),
        "reverse_subset_sizes": reverse_arrays["subset_sizes"],
        "reverse_aligned_unique_r2": reverse_arrays["aligned_unique_r2"],
        "reverse_shifted_unique_r2": reverse_arrays["shifted_unique_r2"],
    }
    arrays_path = resolve_path(config["outputs"]["c2_arrays"])
    atomic_savez(arrays_path, arrays)
    result = {
        "schema_version": "1.0",
        "experiment": "E031",
        "stage": "c2-score",
        "created_at_utc": utc_now(),
        "status": "SEALED",
        "classification": (
            "FIXED-CONTENT REPEAT-INFORMATION RESPONSE"
            if primary_pass
            else "REPEAT-INFORMATION INADEQUATE"
        ),
        "scope": "one_fixed_story_one_participant_no_population_claim",
        "builder_seal": {
            "path": str(seal_path.relative_to(REPO_ROOT)),
            "sha256": observed_seal_sha256,
            "r_builder": float(seal["r_builder"]),
            "delta_c2": delta_c2,
        },
        "primary": primary,
        "primary_gate": {
            "t_k5_minus_k1": t_value,
            "required_delta_c2": delta_c2,
            "slope": slope,
            "t_pass": t_value >= delta_c2,
            "slope_pass": slope > 0.0,
            "status": "PASS" if primary_pass else "FAIL",
        },
        "reverse_assignment_sensitivity": reverse,
        "voxel_masks": {
            "primary_count": int(primary_mask.sum()),
            "primary_sha256": c2_mask_sha256(primary_mask),
            "reverse_count": int(reverse_mask.sum()),
            "reverse_sha256": c2_mask_sha256(reverse_mask),
        },
        "arrays": {
            "path": str(arrays_path.relative_to(REPO_ROOT)),
            "sha256": sha256_file(arrays_path),
            "keys": sorted(arrays),
        },
        "nuisance": {
            "path": config["outputs"]["c2_nuisance"],
            "sha256": sha256_file(resolve_path(config["outputs"]["c2_nuisance"])),
            "metadata": nuisance_metadata,
        },
        "configuration_sha256": sha256_file(config_path),
        "executable_sha256": sha256_file(Path(__file__).resolve()),
        "population_claim_permitted": False,
    }
    result["result_payload_sha256"] = stable_hash(result)
    atomic_write_json(resolve_path(config["outputs"]["c2_result"]), result)
    return result


def validate_c2_builder_result_artifact(
    config: dict[str, Any],
    config_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    result_path = resolve_path(config["outputs"]["directory"]) / "c2_builder_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    require_equal(result.get("experiment"), "E031", "C2 builder result experiment")
    require_equal(result.get("stage"), "c2-build", "C2 builder result stage")
    require_equal(result.get("status"), "SEALED", "C2 builder result status")
    require_equal(
        result.get("evaluation_repeats_accessed"),
        False,
        "C2 builder evaluation-access flag",
    )
    validate_payload_hash(result, "result_payload_sha256", "C2 builder result")
    seal_path = resolve_path(config["outputs"]["builder_seal"])
    require_equal(
        result.get("seal", {}).get("sha256"),
        sha256_file(seal_path),
        "C2 builder result seal hash",
    )
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    require_equal(
        result.get("seal", {}).get("payload_sha256"),
        stable_hash(seal),
        "C2 builder result seal payload hash",
    )
    validate_builder_seal_against_config(seal, config, config_path)
    validate_builder_arrays_against_seal(seal, config)
    require_equal(
        float(result["r_builder"]),
        float(seal["r_builder"]),
        "C2 builder result R",
    )
    require_equal(
        float(result["delta_c2"]),
        float(seal["delta_c2"]),
        "C2 builder result delta",
    )
    expected_classification = (
        "BUILDER INSTRUMENT FLOOR"
        if float(seal["r_builder"]) < float(config["c2"]["builder_floor"])
        else "BUILDER ADEQUATE"
    )
    require_equal(
        result["classification"],
        expected_classification,
        "C2 builder result classification",
    )
    return result, seal


def validate_c2_result_artifact(
    config: dict[str, Any],
    config_path: Path,
    seal: dict[str, Any],
) -> dict[str, Any]:
    path = resolve_path(config["outputs"]["c2_result"])
    result = json.loads(path.read_text(encoding="utf-8"))
    require_equal(result.get("experiment"), "E031", "C2 result experiment")
    require_equal(result.get("stage"), "c2-score", "C2 result stage")
    require_equal(result.get("status"), "SEALED", "C2 result status")
    require_equal(
        result.get("configuration_sha256"),
        sha256_file(config_path),
        "C2 result configuration hash",
    )
    require_equal(
        result.get("executable_sha256"),
        sha256_file(Path(__file__).resolve()),
        "C2 result executable hash",
    )
    require_equal(
        result.get("builder_seal", {}).get("sha256"),
        sha256_file(resolve_path(config["outputs"]["builder_seal"])),
        "C2 result builder seal hash",
    )
    require_equal(
        float(result.get("builder_seal", {}).get("r_builder")),
        float(seal["r_builder"]),
        "C2 result builder R",
    )
    require_equal(
        float(result.get("builder_seal", {}).get("delta_c2")),
        float(seal["delta_c2"]),
        "C2 result builder delta",
    )
    arrays = result.get("arrays", {})
    require_equal(
        sha256_file(resolve_path(str(arrays.get("path", "")))),
        arrays.get("sha256"),
        "C2 result array artifact hash",
    )
    validate_payload_hash(result, "result_payload_sha256", "C2 result")
    gate_pass = result.get("primary_gate", {}).get("status") == "PASS"
    expected_classification = (
        "FIXED-CONTENT REPEAT-INFORMATION RESPONSE"
        if gate_pass
        else "REPEAT-INFORMATION INADEQUATE"
    )
    require_equal(
        result.get("classification"),
        expected_classification,
        "C2 result classification",
    )
    return result


def run_analysis(config: dict[str, Any], config_path: Path) -> dict[str, Any]:
    c1_path = resolve_path(config["outputs"]["c1_result"])
    c2_path = resolve_path(config["outputs"]["c2_result"])
    builder_result_path = resolve_path(config["outputs"]["directory"]) / "c2_builder_result.json"
    c1 = validate_c1_result_artifact(config, config_path)
    builder, seal = validate_c2_builder_result_artifact(config, config_path)
    builder_floor = float(seal["r_builder"]) < float(config["c2"]["builder_floor"])
    if builder_floor:
        if c2_path.is_file():
            raise ValueError(
                "stale C2 result exists after a builder instrument-floor classification"
            )
        c2 = None
        c2_classification = "BUILDER INSTRUMENT FLOOR"
    else:
        if not c2_path.is_file():
            raise FileNotFoundError("adequate C2 builder requires a sealed C2 score artifact")
        c2 = validate_c2_result_artifact(config, config_path, seal)
        c2_classification = c2["classification"]
    primary = c1["variants"]["primary"]
    summaries = primary["contrasts"]
    a_pass = (
        summaries["A_cw"]["mean"]
        >= float(config["c1"]["fixed_cohort_gate"]["absolute_minimum"])
        and summaries["A_cw"]["positive_count"]
        >= int(config["c1"]["fixed_cohort_gate"]["minimum_positive_participants"])
    )
    d_pass = (
        summaries["D_cw_minus_uniform"]["mean"]
        >= float(config["c1"]["fixed_cohort_gate"]["increment_minimum"])
        and summaries["D_cw_minus_uniform"]["positive_count"]
        >= int(config["c1"]["fixed_cohort_gate"]["minimum_positive_participants"])
    )
    specificity_pass = (
        summaries["S_cw"]["mean"] > 0.0
        and summaries["B_cw_given_text"]["mean"] > 0.0
        and summaries["S_cw"]["positive_count"]
        >= int(config["c1"]["fixed_cohort_gate"]["minimum_positive_participants"])
        and summaries["B_cw_given_text"]["positive_count"]
        >= int(config["c1"]["fixed_cohort_gate"]["minimum_positive_participants"])
    )
    if not a_pass:
        c1_classification = "FIXED-COHORT TARGET FAILURE"
    elif not d_pass:
        c1_classification = "NO CONSENSUS INCREMENT"
    elif not specificity_pass:
        c1_classification = "SHARED-SEMANTICS FAILURE"
    else:
        c1_classification = "CONSENSUS-TRANSFER PASS"
    analysis = {
        "schema_version": "1.0",
        "experiment": "E031",
        "stage": "analysis",
        "created_at_utc": utc_now(),
        "status": "AGGREGATED_AWAITING_INTERPRETATION",
        "c1_classification": c1_classification,
        "c2_classification": c2_classification,
        "licenses": {
            "tuckute_target_gradient_gate": c1_classification
            == "CONSENSUS-TRANSFER PASS",
            "repeat_aware_lebel_target_work": c2_classification
            == "FIXED-CONTENT REPEAT-INFORMATION RESPONSE",
            "student_training": False,
        },
        "c1_result_sha256": sha256_file(c1_path),
        "c2_builder_result_sha256": sha256_file(builder_result_path),
        "c2_result_sha256": sha256_file(c2_path) if c2 is not None else None,
        "configuration_sha256": sha256_file(config_path),
        "executable_sha256": sha256_file(Path(__file__).resolve()),
    }
    analysis["analysis_payload_sha256"] = stable_hash(analysis)
    atomic_write_json(resolve_path(config["outputs"]["analysis"]), analysis)
    return analysis


def repeat_subsets(builder_repeats: list[int]) -> dict[int, list[tuple[int, ...]]]:
    return {
        size: list(itertools.combinations(builder_repeats, size))
        for size in range(1, len(builder_repeats) + 1)
    }


def expected_builder_directions(builder_repeats: list[int]) -> list[dict[str, Any]]:
    directions: list[dict[str, Any]] = []
    universe = set(builder_repeats)
    for partition_index, left_tuple in enumerate(itertools.combinations(builder_repeats, 2)):
        left = list(left_tuple)
        right = sorted(universe - set(left))
        directions.extend(
            [
                {
                    "partition_index": partition_index,
                    "predictor_repeats": left,
                    "outcome_repeats": right,
                },
                {
                    "partition_index": partition_index,
                    "predictor_repeats": right,
                    "outcome_repeats": left,
                },
            ]
        )
    return directions


def validate_builder_seal_structure(seal: dict[str, Any], builder_repeats: list[int]) -> None:
    required = {
        "r_builder",
        "delta_c2",
        "partitions",
        "directions",
        "folds",
        "shift_maps",
        "primary_mask_sha256",
        "builder_arrays_sha256",
        "direction_values_sha256",
        "nuisance_cache_sha256",
        "c1_result_payload_sha256",
        "aggregation_constants",
        "data_hashes",
        "configuration_sha256",
        "executable_sha256",
    }
    require_equal(set(seal), required, "builder seal fields")
    expected_partitions = [
        {"left": list(left), "right": sorted(set(builder_repeats) - set(left))}
        for left in itertools.combinations(builder_repeats, 2)
    ]
    require_equal(seal["partitions"], expected_partitions, "builder partition identities")
    require_equal(
        seal["directions"],
        expected_builder_directions(builder_repeats),
        "builder direction identities",
    )
    require_equal(len(seal["directions"]), 20, "builder directed comparisons")
    if not seal["folds"] or not seal["shift_maps"]:
        raise ValueError("builder seal requires folds and shift maps")
    for shift in seal["shift_maps"]:
        if set(shift) != {"segment", "offset", "row_map_sha256"}:
            raise ValueError("builder shift map has incomplete identity")
    require_equal(
        set(seal["aggregation_constants"]),
        {"partition_reduction", "voxel_reduction", "direction_reduction"},
        "builder aggregation constants",
    )
    require_equal(
        seal["aggregation_constants"],
        {
            "partition_reduction": "mean_within_voxel",
            "voxel_reduction": "median",
            "direction_reduction": "equal_mean_20",
        },
        "builder aggregation values",
    )
    require_equal(
        set(seal["data_hashes"]),
        {"response_hdf", "textgrid", "audio", "eng1000", "adapter"},
        "builder data hashes",
    )
    for key in (
        "r_builder",
        "delta_c2",
        "primary_mask_sha256",
        "builder_arrays_sha256",
        "direction_values_sha256",
        "nuisance_cache_sha256",
        "c1_result_payload_sha256",
        "configuration_sha256",
        "executable_sha256",
    ):
        value = seal[key]
        if isinstance(value, float) and not np.isfinite(value):
            raise ValueError(f"builder seal {key} is nonfinite")
        if isinstance(value, str) and not value:
            raise ValueError(f"builder seal {key} is empty")


def run_selftest(config: dict[str, Any]) -> dict[str, Any]:
    rng = np.random.default_rng(31031)
    tests: dict[str, Any] = {}

    folds = config["c1"]["outer_folds"]
    concatenated = np.concatenate([np.arange(start, stop) for start, stop in folds])
    require_equal(concatenated.tolist(), list(range(config["c1"]["rows"])), "C1 folds")
    tests["c1_contiguous_folds"] = "PASS"

    cw = config["c1"]["consensus"]
    zero_agreements = np.zeros((4, 4), dtype=np.float64)
    require_equal(
        consensus_weights(zero_agreements, cw).tolist(),
        [0.25, 0.25, 0.25, 0.25],
        "zero-agreement consensus fallback",
    )
    agreements = np.repeat(np.array([[0.8], [0.4], [-0.2], [0.0]]), 4, axis=1)
    weights = consensus_weights(agreements, cw)
    expected_weights = np.array([11 / 24, 7 / 24, 1 / 8, 1 / 8], dtype=np.float64)
    if not np.allclose(weights, expected_weights, rtol=0.0, atol=1e-15):
        raise AssertionError(
            f"consensus Fisher-average/back-transform mismatch: {weights} != {expected_weights}"
        )
    tests["c1_consensus_weights"] = "PASS"

    x_train = rng.normal(size=(600, 5)) @ np.diag([2.0, 1.5, 1.0, 0.7, 0.4])
    y_train = rng.normal(size=(600, 5)) @ np.array(
        [[1.4, 0.3, 0.0, 0.0, 0.0],
         [0.0, 1.1, 0.2, 0.0, 0.0],
         [0.1, 0.0, 0.9, 0.2, 0.0],
         [0.0, 0.0, 0.0, 0.7, 0.1],
         [0.0, 0.0, 0.0, 0.0, 0.5]]
    )
    matched, _ = geometry_match(x_train, y_train, x_train[:20], 1e-8)
    covariance_error = np.linalg.norm(
        np.cov(matched, rowvar=False, ddof=1) - np.cov(y_train, rowvar=False, ddof=1),
        ord="fro",
    ) / np.linalg.norm(np.cov(y_train, rowvar=False, ddof=1), ord="fro")
    if covariance_error > 1e-10 or np.max(np.abs(matched.mean(0) - y_train.mean(0))) > 1e-10:
        raise AssertionError("geometry matching invariant failed")
    tests["c1_geometry_match"] = "PASS"

    all_outer_blocks = [np.arange(start, stop) for start, stop in folds]
    for outer_test in range(len(all_outer_blocks)):
        inner_blocks = [
            block for index, block in enumerate(all_outer_blocks) if index != outer_test
        ]
        seen = []
        for heldout, block in enumerate(inner_blocks):
            train = np.concatenate(
                [part for index, part in enumerate(inner_blocks) if index != heldout]
            )
            if np.intersect1d(train, block).size:
                raise AssertionError("inner crossfit leakage")
            if np.intersect1d(train, all_outer_blocks[outer_test]).size:
                raise AssertionError("outer-test leakage into text crossfit")
            seen.append(block)
        expected = np.concatenate(inner_blocks)
        require_equal(
            np.sort(np.concatenate(seen)).tolist(),
            np.sort(expected).tolist(),
            f"inner OOF coverage for outer fold {outer_test}",
        )
    tests["c1_text_crossfit_locality"] = "PASS"

    synthetic_config = json.loads(json.dumps(config))
    synthetic_config["c1"]["rows"] = 100
    synthetic_config["c1"]["outer_folds"] = [
        [0, 20],
        [20, 40],
        [40, 60],
        [60, 80],
        [80, 100],
    ]
    synthetic_config["c1"]["nuisance_pca_rank"] = 5
    synthetic_config["c1"]["text_control"]["feature_pca_rank"] = 8
    synthetic_config["c1"]["block_shift"] = 10
    synthetic_nuisance = {
        "base_scalar": rng.normal(size=(100, 2)),
        "static_embedding": rng.normal(size=(100, 12)),
        "imageability": rng.normal(size=(100, 1)),
        "full_cov_extra": rng.normal(size=(100, 3)),
    }
    shared_signal = rng.normal(size=(100, 5))
    synthetic_source = np.stack(
        [
            shared_signal + 0.4 * rng.normal(size=(100, 5))
            for _ in range(4)
        ],
        axis=0,
    )
    synthetic_text = np.concatenate(
        [shared_signal + 0.2 * rng.normal(size=(100, 5)), rng.normal(size=(100, 15))],
        axis=1,
    )
    synthetic_targets, synthetic_builder = build_c1_targets(
        synthetic_source,
        synthetic_text,
        synthetic_nuisance,
        0,
        synthetic_config,
        "primary",
    )
    require_equal(
        set(synthetic_targets),
        {
            "source_mean_raw",
            "uniform_residual",
            "consensus_weighted",
            "text_surrogate_geometry_matched",
            "text_to_consensus_crossfit",
            "cw_shifted",
        },
        "synthetic C1 target arms",
    )
    if any(
        values.shape != (100, 5) or not np.isfinite(values).all()
        for values in synthetic_targets.values()
    ):
        raise AssertionError("synthetic C1 target construction failed")
    require_equal(synthetic_builder["geometry"]["status"], "PASS", "synthetic geometry")
    tests["c1_full_target_builder"] = "PASS"

    for start, stop in folds:
        source = np.arange(start, stop)
        shifted = block_local_shift(source)
        if set(source) != set(shifted) or np.any(shifted == source):
            raise AssertionError("C1 shift escaped a block or left fixed rows")
    tests["c1_segment_local_shift"] = "PASS"

    observed = np.arange(20, dtype=np.float64)
    nuisance = np.zeros(20, dtype=np.float64)
    full = observed.copy()
    full[:10] += 2.0
    concatenated_u = float(unique_r2(observed, nuisance, full)[0])
    fold_u = np.mean(
        [
            float(unique_r2(observed[:10], nuisance[:10], full[:10])[0]),
            float(unique_r2(observed[10:], nuisance[10:], full[10:])[0]),
        ]
    )
    if np.isclose(concatenated_u, fold_u):
        raise AssertionError("U selftest does not distinguish concatenation from fold averaging")
    tests["concatenated_unique_r2"] = "PASS"

    builder = config["c2"]["builder_repeats"]
    evaluation = config["c2"]["evaluation_repeats"]
    if set(builder) & set(evaluation) or sorted(builder + evaluation) != list(range(10)):
        raise AssertionError("C2 repeat split is not disjoint and exhaustive")
    subsets = repeat_subsets(builder)
    require_equal([len(subsets[k]) for k in range(1, 6)], [5, 10, 10, 5, 1], "C2 subsets")
    partitions = list(itertools.combinations(builder, 2))
    require_equal(len(partitions), 10, "C2 unordered 2-versus-3 partitions")
    require_equal(2 * len(partitions), 20, "C2 directed builder comparisons")
    tests["c2_repeat_split_and_subsets"] = "PASS"

    time_blocks = np.array_split(np.arange(config["c2"]["time_rows"]), 5)
    require_equal([len(block) for block in time_blocks], config["c2"]["outer_block_lengths"], "C2 blocks")
    for block in time_blocks:
        purge = int(config["c2"]["boundary_purge_trs"])
        retained = block[purge:-purge]
        shifted = block_local_shift(retained)
        if len(retained) // 2 <= purge:
            raise AssertionError("C2 retained-segment shift does not exceed purge width")
        if set(retained) != set(shifted):
            raise AssertionError("C2 shift escaped a retained segment")
        raw_support = {
            int(row): set(range(int(row) - purge, int(row) + 4))
            for row in retained
        }
        outside = set(range(config["c2"]["time_rows"])) - set(block)
        if any(support & outside for support in raw_support.values()):
            raise AssertionError("purged retained row shares support across a fold boundary")
    tests["c2_time_blocks_and_shifts"] = "PASS"

    delayed_source = np.arange(12, dtype=np.float64).reshape(6, 2)
    delayed = make_delayed_features(delayed_source, [1, 2])
    expected_delayed = np.concatenate(
        [
            np.vstack([np.zeros((1, 2)), delayed_source[:-1]]),
            np.vstack([np.zeros((2, 2)), delayed_source[:-2]]),
        ],
        axis=1,
    )
    if not np.array_equal(delayed, expected_delayed):
        raise AssertionError("C2 FIR delay construction mismatch")
    tests["c2_delayed_features"] = "PASS"

    import torch
    from sklearn.linear_model import Ridge

    nuisance_train = rng.normal(size=(24, 7))
    nuisance_test = rng.normal(size=(9, 7))
    outcome_train = rng.normal(size=(24, 4))
    aligned_train = rng.normal(size=(24, 4))
    aligned_test = rng.normal(size=(9, 4))
    shifted_train = rng.normal(size=(24, 4))
    shifted_test = rng.normal(size=(9, 4))
    alpha = 10.0
    torch_predictions = c2_torch_predictions(
        torch.as_tensor(nuisance_train, dtype=torch.float64),
        torch.as_tensor(nuisance_test, dtype=torch.float64),
        torch.as_tensor(outcome_train, dtype=torch.float64),
        torch.as_tensor(aligned_train, dtype=torch.float64),
        torch.as_tensor(aligned_test, dtype=torch.float64),
        torch.as_tensor(shifted_train, dtype=torch.float64),
        torch.as_tensor(shifted_test, dtype=torch.float64),
        alpha,
    )
    nuisance_reference = Ridge(alpha=alpha, solver="svd", fit_intercept=False).fit(
        nuisance_train, outcome_train
    ).predict(nuisance_test)
    aligned_reference = np.column_stack(
        [
            Ridge(alpha=alpha, solver="svd", fit_intercept=False)
            .fit(
                np.column_stack([nuisance_train, aligned_train[:, voxel]]),
                outcome_train[:, voxel],
            )
            .predict(np.column_stack([nuisance_test, aligned_test[:, voxel]]))
            for voxel in range(outcome_train.shape[1])
        ]
    )
    shifted_reference = np.column_stack(
        [
            Ridge(alpha=alpha, solver="svd", fit_intercept=False)
            .fit(
                np.column_stack([nuisance_train, shifted_train[:, voxel]]),
                outcome_train[:, voxel],
            )
            .predict(np.column_stack([nuisance_test, shifted_test[:, voxel]]))
            for voxel in range(outcome_train.shape[1])
        ]
    )
    for observed_prediction, reference_prediction in zip(
        torch_predictions,
        (nuisance_reference, aligned_reference, shifted_reference),
    ):
        if observed_prediction is None or not np.allclose(
            observed_prediction.detach().cpu().numpy(),
            reference_prediction,
            rtol=1e-10,
            atol=1e-10,
        ):
            raise AssertionError("C2 block-ridge formula disagrees with sklearn Ridge(svd)")
    tests["c2_block_ridge_sklearn_equivalence"] = "PASS"

    synthetic_c2_config = json.loads(json.dumps(config))
    synthetic_c2_config["c2"]["time_rows"] = 100
    synthetic_c2_config["c2"]["outer_block_lengths"] = [20, 20, 20, 20, 20]
    synthetic_c2_config["c2"]["boundary_purge_trs"] = 2
    synthetic_c2_config["c2"]["eng1000_pca_rank"] = 5
    synthetic_c2_config["c2"]["ridge_alphas"] = [1, 10]
    synthetic_c2_nuisance = {
        "low": rng.normal(size=(100, 3)),
        "eng1000": rng.normal(size=(100, 15)),
        "acoustic": rng.normal(size=(100, 4)),
    }
    synthetic_predictor = rng.normal(size=(100, 6))
    synthetic_outcome = (
        0.35 * synthetic_predictor + rng.normal(scale=0.8, size=(100, 6))
    )
    synthetic_evaluation = c2_evaluate_target(
        synthetic_predictor,
        synthetic_outcome,
        synthetic_c2_nuisance,
        synthetic_c2_config,
        "cpu",
    )
    require_equal(len(synthetic_evaluation["folds"]), 5, "synthetic C2 folds")
    for key in ("aligned_unique_r2", "shifted_unique_r2"):
        values = synthetic_evaluation[key]
        if values.shape != (6,) or not np.isfinite(values).all():
            raise AssertionError(f"synthetic C2 evaluation failed for {key}")
    tests["c2_full_nested_evaluation"] = "PASS"

    partitions = [
        {"left": list(left), "right": sorted(set(builder) - set(left))}
        for left in itertools.combinations(builder, 2)
    ]
    seal = {
        "r_builder": 0.02,
        "delta_c2": 0.002,
        "partitions": partitions,
        "directions": expected_builder_directions(builder),
        "folds": [block.tolist() for block in time_blocks],
        "shift_maps": [
            {
                "segment": index,
                "offset": len(block[7:-7]) // 2,
                "row_map_sha256": sha256_bytes(
                    block_local_shift(block[7:-7]).astype("<i8").tobytes()
                ),
            }
            for index, block in enumerate(time_blocks)
        ],
        "primary_mask_sha256": "synthetic-mask",
        "builder_arrays_sha256": "synthetic-arrays",
        "direction_values_sha256": "synthetic-directions",
        "nuisance_cache_sha256": "synthetic-nuisance",
        "c1_result_payload_sha256": "synthetic-c1",
        "aggregation_constants": {
            "partition_reduction": "mean_within_voxel",
            "voxel_reduction": "median",
            "direction_reduction": "equal_mean_20",
        },
        "data_hashes": {
            "response_hdf": "synthetic-response",
            "textgrid": "synthetic-textgrid",
            "audio": "synthetic-audio",
            "eng1000": "synthetic-eng1000",
            "adapter": "synthetic-adapter",
        },
        "configuration_sha256": "synthetic-config",
        "executable_sha256": "synthetic-executable",
    }
    validate_builder_seal_structure(seal, builder)
    changed = dict(seal)
    changed["delta_c2"] = 0.0020000000001
    if stable_hash(seal) == stable_hash(changed):
        raise AssertionError("builder seal hash ignored a scientific field")
    for field in seal:
        incomplete = {key: value for key, value in seal.items() if key != field}
        try:
            validate_builder_seal_structure(incomplete, builder)
        except ValueError:
            pass
        else:
            raise AssertionError(f"builder seal accepted missing field {field}")
    bad_directions = json.loads(json.dumps(seal))
    bad_directions["directions"][0]["predictor_repeats"] = [builder[0], builder[2]]
    try:
        validate_builder_seal_structure(bad_directions, builder)
    except ValueError:
        pass
    else:
        raise AssertionError("builder seal accepted a changed direction identity")
    tests["c2_builder_seal_hash"] = "PASS"

    return {
        "experiment": "E031",
        "stage": "selftest",
        "science_status": "SYNTHETIC_ONLY",
        "endpoint_values_accessed": False,
        "tests": tests,
        "status": "PASS",
    }


def run_manifest(config: dict[str, Any], config_path: Path) -> dict[str, Any]:
    c1 = config["c1"]
    c2 = config["c2"]
    c1_biological_inputs = validate_c1_biological_inputs(config)
    extraction_spec = c1["extraction"]
    extraction_record = file_record(extraction_spec)
    extraction_path = resolve_path(extraction_spec["path"])
    cache_specs = [
        {**spec, "_e025_manifest_sha256": extraction_spec["manifest_sha256"]}
        for spec in c1["representation_caches"]
    ]
    aliases = validate_cache_aliases(extraction_path, cache_specs)

    cache_records = []
    for spec in cache_specs:
        record = file_record(spec)
        headers = npz_headers(resolve_path(spec["path"]))
        for key in ("tuckute_layer_6", "tuckute_layer_7"):
            if key not in headers:
                raise ValueError(f"{spec['path']} lacks {key}")
            require_equal(headers[key]["shape"], [1000, 768], f"{spec['path']} {key} shape")
            require_equal(headers[key]["dtype"], "float32", f"{spec['path']} {key} dtype")
        if "metadata_json" not in headers:
            raise ValueError(f"{spec['path']} lacks metadata_json")
        metadata = representation_metadata(resolve_path(spec["path"]))
        require_equal(
            metadata.get("pooling"),
            "attention-mask mean",
            f"{spec['path']} pooling",
        )
        require_equal(metadata.get("layers"), c1["text_control"]["layers"], f"{spec['path']} layers")
        require_equal(
            metadata.get("tuckute_ordered_text_sha256"),
            c1["ordered_text_sha256"],
            f"{spec['path']} ordered text",
        )
        expected_alias = {"arm": "kd_only", "seed": int(spec["seed"])}
        if not any(
            alias.get("arm") == expected_alias["arm"]
            and int(alias.get("seed", -1)) == expected_alias["seed"]
            for alias in metadata.get("aliases", [])
        ):
            raise ValueError(f"{spec['path']} metadata lacks its kd_only seed alias")
        cache_records.append(
            {
                "seed": spec["seed"],
                **record,
                "arrays": {
                    key: headers[key]
                    for key in ("tuckute_layer_6", "tuckute_layer_7", "metadata_json")
                },
                "alias_cache_key": aliases[int(spec["seed"])]["cache_key"],
                "metadata_identity": {
                    "pooling": metadata["pooling"],
                    "layers": metadata["layers"],
                    "tuckute_ordered_text_sha256": metadata[
                        "tuckute_ordered_text_sha256"
                    ],
                    "aliases": metadata["aliases"],
                },
            }
        )

    c2_file_records: dict[str, Any] = {}
    for name, spec in c2["files"].items():
        c2_file_records[name] = file_record(spec)

    response_path = resolve_path(c2["files"]["response_hdf"]["path"])
    response_metadata = hdf_metadata(response_path)
    expected_datasets = c2["files"]["response_hdf"]["datasets"]
    for key, shape in expected_datasets.items():
        if key not in response_metadata:
            raise ValueError(f"response HDF lacks dataset {key}")
        require_equal(response_metadata[key]["shape"], shape, f"response HDF {key} shape")
        require_equal(response_metadata[key]["dtype"], "float64", f"response HDF {key} dtype")

    audio_metadata = wav_metadata(resolve_path(c2["files"]["audio"]["path"]))
    acoustic = c2["acoustic"]
    for key in ("channels", "sample_width_bytes", "sample_rate_hz", "frames"):
        require_equal(audio_metadata[key], acoustic[key], f"audio {key}")

    voxel_index = np.arange(c2["voxel_count"], dtype="<i8")
    require_equal(
        sha256_bytes(voxel_index.tobytes()),
        c2["voxel_index_sha256"],
        "primary voxel index hash",
    )
    blocks = np.array_split(np.arange(c2["time_rows"]), 5)
    block_lengths = [len(block) for block in blocks]
    require_equal(block_lengths, c2["outer_block_lengths"], "C2 block lengths")

    manifest = {
        "schema_version": "1.0",
        "artifact_type": "E031 metadata-only preflight manifest",
        "experiment": "E031",
        "stage": "manifest",
        "science_status": "METADATA_ONLY",
        "endpoint_values_accessed": False,
        "endpoint_compute_allowed": bool(
            config["authorization"]["endpoint_compute_allowed"]
        ),
        "configuration": {
            "path": str(config_path.resolve().relative_to(REPO_ROOT)),
            "sha256": sha256_file(config_path),
        },
        "executable": {
            "path": str(Path(__file__).resolve().relative_to(REPO_ROOT)),
            "sha256": sha256_file(Path(__file__).resolve()),
        },
        "c1": {
            "source_participants": c1["source_participants"],
            "evaluation_participants": c1["evaluation_participants"],
            "outer_folds": c1["outer_folds"],
            "extraction": extraction_record,
            "representation_caches": cache_records,
            "ordered_text_sha256": c1["ordered_text_sha256"],
            "biological_inputs": c1_biological_inputs,
        },
        "c2": {
            "builder_repeats": c2["builder_repeats"],
            "evaluation_repeat_values_accessed": False,
            "evaluation_repeat_indices_recorded_only": c2["evaluation_repeats"],
            "outer_block_lengths": block_lengths,
            "voxel_index_sha256": c2["voxel_index_sha256"],
            "files": c2_file_records,
            "response_container_metadata": response_metadata,
            "audio_container_metadata": audio_metadata,
            "allocation_constants": {
                "builder_floor": c2["builder_floor"],
                "response_fraction": c2["response_fraction"],
                "accepted": bool(
                    config["authorization"].get("c2_allocation_accepted", False)
                ),
            },
        },
        "status": "PASS",
    }
    manifest["manifest_payload_sha256"] = stable_hash(manifest)
    output_path = resolve_path(config["outputs"]["preflight_manifest"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=["selftest", "manifest", "c1", "c2-build", "c2-score", "analyze"],
        required=True,
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--builder-seal-sha256")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    config = load_config(config_path)
    endpoint_allowed = bool(config["authorization"]["endpoint_compute_allowed"])
    if args.stage in BLOCKED_STAGES and not endpoint_allowed:
        print(
            canonical_json(
                {
                    "experiment": "E031",
                    "stage": args.stage,
                    "status": "BLOCKED_BY_PREFLIGHT_HOLD",
                    "endpoint_values_accessed": False,
                    "requires": [
                        "fresh anti-confound review of implemented endpoint stages",
                        "fresh independent oracle PASS",
                        "science_status=READY_TO_RUN",
                        "authorization.endpoint_compute_allowed=true",
                    ],
                }
            ),
            file=sys.stderr,
        )
        return 2
    if args.stage == "selftest":
        payload = run_selftest(config)
    elif args.stage == "manifest":
        payload = run_manifest(config, config_path)
    elif args.stage == "c1":
        payload = run_c1(config, config_path)
    elif args.stage == "c2-build":
        payload = run_c2_build(config, config_path, args.device)
    elif args.stage == "c2-score":
        if not args.builder_seal_sha256:
            raise ValueError("c2-score requires --builder-seal-sha256")
        payload = run_c2_score(
            config,
            config_path,
            args.builder_seal_sha256,
            args.device,
        )
    elif args.stage == "analyze":
        payload = run_analysis(config, config_path)
    else:
        print(
            canonical_json(
                {
                    "experiment": "E031",
                    "stage": args.stage,
                    "status": "BLOCKED_BY_UNIMPLEMENTED_STAGE",
                    "endpoint_values_accessed": False,
                }
            ),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
