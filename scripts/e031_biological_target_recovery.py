#!/usr/bin/env python3
"""Outcome-blind preflight for E031 biological target information recovery.

Only ``selftest`` and ``manifest`` are implemented while the experiment is on
DESIGN HOLD. The biological stages fail closed. The manifest hashes inputs and
reads container metadata, but never indexes or reduces biological response
values.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import wave
import zipfile
from pathlib import Path
from typing import Any, Iterable

import h5py
import numpy as np
from numpy.lib import format as npy_format


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "configs/e031_biological_target_information_recovery.json"
BLOCKED_STAGES = {"c1", "c2-build", "c2-score", "analyze"}


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


def load_config(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("experiment") != "E031":
        raise ValueError("configuration is not E031")
    if payload.get("science_status") != "DESIGN_HOLD":
        raise ValueError("preflight requires science_status=DESIGN_HOLD")
    if payload.get("authorization", {}).get("endpoint_compute_allowed") is not False:
        raise ValueError("preflight configuration must forbid endpoint computation")
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
        set(seal["data_hashes"]),
        {"response_hdf", "textgrid", "audio", "eng1000", "adapter"},
        "builder data hashes",
    )


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
        "endpoint_compute_allowed": False,
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
            "allocation_constants_pending_user_acceptance": {
                "builder_floor": c2["builder_floor"],
                "response_fraction": c2["response_fraction"],
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    config = load_config(config_path)
    if args.stage in BLOCKED_STAGES:
        print(
            canonical_json(
                {
                    "experiment": "E031",
                    "stage": args.stage,
                    "status": "BLOCKED_BY_DESIGN_HOLD",
                    "endpoint_values_accessed": False,
                    "requires": [
                        "independent oracle review",
                        "Erfan acceptance of C2 builder_floor=0.01",
                        "Erfan acceptance of C2 response_fraction=0.10",
                        "explicit /work E031",
                    ],
                }
            ),
            file=sys.stderr,
        )
        return 2
    payload = run_selftest(config) if args.stage == "selftest" else run_manifest(config, config_path)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
