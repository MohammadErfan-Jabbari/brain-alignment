#!/usr/bin/env python3
"""Numerically honest E026 TRIBE/text-feature target comparability audit.

This script is an evidence helper, not a verdict engine.  It has five stages:

``selftest``
    Run synthetic-only numerical, sample-freezing, and tamper-rejection
    fixtures.  This stage never reads scientific target values.

``manifest``
    Verify artifact provenance and freeze deterministic row/coordinate samples
    without loading ``targets`` values from the large NPZ caches.
``geometry``
    Stream/extract the frozen caches, compute full float64 moments, sample-based
    randomized-SVD geometry, descriptive 2NN, and within-document order
    diagnostics.  Top-512 quantities are always labelled as sample/truncated.
``trained``
    Summarize retained E016 target learning/losses, effective parameter-update
    norms, and CKA/RMS movement from a validated E025 representation manifest.
``all``
    Consume an already reviewed frozen manifest, then run ``geometry`` and
    ``trained``.  This stage never creates or overwrites its manifest.

Only JSON audit summaries are emitted.  Heavy extracted NPY files are scratch
artifacts under the gitignored output directory.  No stage changes an E-record
or scientific verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
import time
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

import numpy as np

# This must be set before the first Torch/CUDA import.  ``choose_device`` queries
# CUDA, so setting it inside the SVD routine is too late to make the contract
# auditable.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

REPO = Path(".") if (Path("scripts") / "AGENTS.md").exists() else Path(__file__).resolve().parents[1]
OUT_DIR = Path("outputs/E026")
SCHEMA_VERSION = "e026-target-comparability-v2"
E025_SCHEMA_VERSION = "e025-participant-transfer.v1"
E026_RECORD = Path("docs/experiments/E026_tribe-textfeat-target-comparability.md")
SCIENCE_STATUS = (
    "audit_diagnostic_only; component estimates require interpretation; "
    "this file never flips an E016/E025/E026 verdict"
)

TRAIN_N = 95_999
HELDOUT_N = 1_999
TARGET_D = 20_484
SAMPLE_N = 4_096
COORD_SAMPLE_N = 256
ROW_SAMPLE_KEYS = {
    "A": "E026-A-20260716",
    "B": "E026-B-20260716",
}
COORD_SAMPLE_KEYS = {
    "A": "E026-COORD-A-20260716",
    "B": "E026-COORD-B-20260716",
}
SVD_SEED = 20_260_716
SVD_K = 512
SVD_OVERSAMPLE = 64
SVD_POWER_ITERS = 4
SVD_MASS_CUTS = (1, 8, 32, 128, 512)
ID_RANKS = (32, 64, 128, 256, 512)
ORDER_LAGS = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)
STD_EPS = 1e-6  # E016 formula: (Y - population mean) / (population SD + 1e-6)
STANDARDIZATION_EXTREMA_RTOL = 1e-5
SVD_ORTHOGONALITY_MAX = 5e-3
SVD_ENERGY_TOL = 1e-4
NUISANCE_MODEL = "gpt2-medium"
NUISANCE_TOKENIZER = "gpt2"
NUISANCE_MAX_LENGTH = 64
NUISANCE_PCA_RANK = 50
NUISANCE_INNER_FOLDS = 5
NUISANCE_POSITION_BLOCKS = 10
NUISANCE_RIDGE_ALPHAS = (0.1, 1.0, 10.0, 100.0, 1000.0)
NUISANCE_TARGET_CHUNK = 128
ROW_CHUNK = 512
STATIC_BATCH_SIZE = 64
DERIVED_SCRATCH_REUSE = False
ENVIRONMENT_FILES = (Path("pyproject.toml"), Path("uv.lock"))

# These are engineering margins, not population-equivalence tests.  They are
# frozen into the metadata manifest and emitted beside every mechanical check.
MARGINS: dict[str, Any] = {
    "sample_global_mean_abs_difference": 0.01,
    "sample_global_sd_ratio": [0.99, 1.01],
    "normalized_covariance_log_eigen_rms": 0.10,
    "sample_stable_rank_abs_log_ratio": 0.10,
    "variance_mass_abs_difference": 0.02,
    "trace_autocorrelation_abs_difference": 0.05,
    "power_spectrum_js_nats": 0.05,
    "kd_target_r2_abs_paired_mean_difference": 0.02,
    "remaining_headroom_mean_ratio": [0.90, 1.10],
    "low_level_target_r2_abs_difference": 0.02,
    "static_unique_target_r2_abs_difference": 0.02,
    "parameter_update_abs_log_ratio": 0.10,
    "parameter_update_absolute_floor": 1e-6,
    "representation_cka_distance_abs_difference": 0.002,
    "representation_centered_relative_fro_abs_log_ratio": 0.10,
    "representation_centered_relative_fro_absolute_floor": 1e-6,
    "representation_duplicate_noise_multiplier": 10.0,
}

ALGEBRAIC_RANK_CAP = {
    # Mean pooling gives a 1,024-dimensional source and the fixed Gaussian
    # projection plus coordinatewise affine standardization cannot increase
    # centered matrix rank.
    "textfeat": 1_024,
    # TRIBE is nonlinear in its upstream representation.  Only the centered
    # fixed-sample cap is asserted.
    "tribe": SAMPLE_N - 1,
}

TARGET_SOURCES: dict[str, dict[str, Any]] = {
    "tribe": {
        "train_cache": Path("outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz"),
        "heldout_cache": Path("outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz"),
        "train_sidecar": Path("outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.json"),
        "heldout_sidecar": Path("outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.json"),
        "run_jsons": (
            Path("outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json"),
            Path("outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.json"),
        ),
        "target_arm": "tribe_mse",
        "permuted_arm": "tribe_perm",
    },
    "textfeat": {
        "train_cache": Path(
            "outputs/E016_tribe/kd_targets/text_feature/gpt2-medium/"
            "train_start0_n95999_d20484_full.npz"
        ),
        "heldout_cache": Path(
            "outputs/E016_tribe/kd_targets/text_feature/gpt2-medium/"
            "heldout_start0_n1999_d20484_full.npz"
        ),
        "train_sidecar": Path(
            "outputs/E016_tribe/kd_targets/text_feature/gpt2-medium/"
            "train_start0_n95999_d20484_full.json"
        ),
        "heldout_sidecar": Path(
            "outputs/E016_tribe/kd_targets/text_feature/gpt2-medium/"
            "heldout_start0_n1999_d20484_full.json"
        ),
        "run_jsons": (
            Path(
                "outputs/E016_tribe/phase3/"
                "phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.json"
            ),
        ),
        "target_arm": "textfeat_mse",
        "permuted_arm": "textfeat_perm",
    },
}

CORPUS_PATHS = {
    "train": Path("data/kd_corpus/wikitext103_sentences_train.txt"),
    "heldout": Path("data/kd_corpus/wikitext103_sentences_heldout.txt"),
}

CONTEXT_META = Path(
    "outputs/E016_tribe/kd_context_metadata/wikitext103_train_context_meta.jsonl"
)
CONTEXT_SUMMARY = Path(
    "outputs/E016_tribe/kd_context_metadata/wikitext103_context_meta_summary.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        required=True,
        choices=("selftest", "manifest", "geometry", "trained", "all"),
    )
    parser.add_argument("--out", type=Path, help="JSON output path; a stage-specific default is used.")
    parser.add_argument(
        "--manifest-in",
        type=Path,
        default=OUT_DIR / "e026_manifest.json",
        help="Frozen manifest consumed by geometry/trained stages.",
    )
    parser.add_argument(
        "--e025-manifest",
        type=Path,
        help=(
            "E025 representation-cache manifest. If omitted, known manifest paths under "
            "outputs/E025 are checked; absence is recorded, not silently substituted."
        ),
    )
    parser.add_argument("--scratch-dir", type=Path, default=OUT_DIR / "scratch_npy")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--row-chunk", type=int, default=ROW_CHUNK)
    parser.add_argument("--feature-chunk", type=int, default=NUISANCE_TARGET_CHUNK)
    parser.add_argument("--static-batch-size", type=int, default=STATIC_BATCH_SIZE)
    parser.add_argument(
        "--skip-full-cache-sha256",
        action="store_true",
        help="Record ZIP CRC/size provenance without recomputing whole-cache SHA-256.",
    )
    parser.add_argument(
        "--keep-extracted",
        action="store_true",
        help="Keep extracted target NPY scratch files after geometry completes.",
    )
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def repo_path(path: str | Path) -> Path:
    """Return a path usable from the open checkout even when ancestors deny traversal."""
    p = Path(path)
    if not p.is_absolute():
        return p
    marker = "/brain-alignment/"
    raw = str(p)
    if marker in raw and (REPO / raw.split(marker, 1)[1]).exists():
        return REPO / raw.split(marker, 1)[1]
    return p


def output_path(args: argparse.Namespace, stage: str) -> Path:
    if args.out is not None:
        return repo_path(args.out)
    names = {
        "selftest": "e026_selftest.json",
        "manifest": "e026_manifest.json",
        "geometry": "e026_geometry.json",
        "trained": "e026_trained.json",
        "all": "e026_audit.json",
    }
    return OUT_DIR / names[stage]


def json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.ndarray):
        return json_safe(value.tolist())
    if isinstance(value, np.generic):
        return json_safe(value.item())
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    text = json.dumps(json_safe(payload), indent=2, sort_keys=True, allow_nan=False) + "\n"
    temp.write_text(text, encoding="utf-8")
    os.replace(temp, path)


def load_json(path: str | Path) -> dict[str, Any]:
    p = repo_path(path)
    value = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{p} must contain a JSON object")
    return value


def expected_generator_sidecar(family: str, split: str) -> dict[str, Any]:
    """Return the load-bearing cache-generator semantics frozen by E026."""
    if split not in CORPUS_PATHS:
        raise ValueError(f"unknown target-cache split: {split}")
    n_items = TRAIN_N if split == "train" else HELDOUT_N
    common = {
        "split": split,
        "corpus": str((REPO / CORPUS_PATHS[split]).resolve()),
        "start": 0,
        "n_items": n_items,
        "target_dim": TARGET_D,
    }
    if family == "tribe":
        return {
            **common,
            "experiment": "E016 Phase 3 KD-corpus TRIBE target cache",
            "batch_items": 32,
            "features": ["text"],
            "event_mode": "synthetic-text",
            "vertex_index": "stored in npz",
            "tr": 1.0,
            "word_duration": 0.35,
            "word_gap": 0.05,
            "min_duration": 1.0,
            "config_update": {
                "data.text_feature.model_name": "unsloth/Llama-3.2-3B",
                "data.features_to_use": ["text"],
            },
        }
    if family == "textfeat":
        return {
            **common,
            "experiment": "E016 matched-information non-brain target cache",
            "batch_size": 16,
            "model": "gpt2-medium",
            "layer": 12,
            "pool": "mean",
            "max_length": 64,
            "target_dim": TARGET_D,
            "vertex_index": "synthetic dimensions stored in npz",
            "projection": {
                "projection": "gaussian_random_projection",
                "projection_seed": 0,
                "source_dim": 1_024,
                "target_dim": TARGET_D,
                "scale": 0.03125,
            },
        }
    raise ValueError(f"unknown target-cache family: {family}")


def validate_generator_sidecar(
    family: str, split: str, metadata: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate exact generator fields while allowing nonsemantic timing metadata."""
    expected = expected_generator_sidecar(family, split)
    errors: list[str] = []

    def visit(observed: Any, wanted: Any, field: str) -> None:
        if isinstance(wanted, Mapping):
            if not isinstance(observed, Mapping):
                errors.append(f"{field}: expected object, observed {type(observed).__name__}")
                return
            for key, value in wanted.items():
                if key not in observed:
                    errors.append(f"{field}.{key}: missing")
                else:
                    visit(observed[key], value, f"{field}.{key}")
            return
        if observed != wanted:
            errors.append(f"{field}: observed={observed!r}, expected={wanted!r}")

    visit(metadata, expected, f"{family}/{split}")
    return {
        "status": "valid" if not errors else "invalid",
        "expected_load_bearing_fields": expected,
        "errors": errors,
    }


def sha256_file(path: str | Path, chunk_bytes: int = 16 << 20) -> str:
    p = repo_path(path)
    digest = hashlib.sha256()
    with p.open("rb") as handle:
        while True:
            block = handle.read(chunk_bytes)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def sha256_int64(values: Sequence[int] | np.ndarray) -> str:
    arr = np.asarray(values, dtype="<i8")
    return hashlib.sha256(arr.tobytes(order="C")).hexdigest()


def sha256_strings(values: Sequence[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = str(value).encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "little", signed=False))
        digest.update(encoded)
    return digest.hexdigest()


def sha256_newline_texts(values: Sequence[str]) -> str:
    """Match E025's frozen ordered-text identity exactly."""
    return hashlib.sha256(("\n".join(map(str, values)) + "\n").encode("utf-8")).hexdigest()


def sha256_array(values: np.ndarray, row_chunk: int = 4096) -> str:
    """Hash a C-order array without requiring a second full-size byte copy."""
    array = np.asarray(values)
    digest = hashlib.sha256()
    if array.ndim == 0:
        digest.update(array.tobytes(order="C"))
    else:
        for start in range(0, len(array), row_chunk):
            digest.update(np.ascontiguousarray(array[start : start + row_chunk]).tobytes(order="C"))
    return digest.hexdigest()


def npy_header(handle: Any) -> dict[str, Any]:
    version = np.lib.format.read_magic(handle)
    if version == (1, 0):
        shape, fortran, dtype = np.lib.format.read_array_header_1_0(handle)
    elif version == (2, 0):
        shape, fortran, dtype = np.lib.format.read_array_header_2_0(handle)
    else:
        shape, fortran, dtype = np.lib.format._read_array_header(handle, version)  # noqa: SLF001
    return {
        "npy_version": list(version),
        "shape": [int(x) for x in shape],
        "fortran_order": bool(fortran),
        "dtype": str(np.dtype(dtype)),
    }


def inspect_npz(path: str | Path, full_sha256: bool) -> dict[str, Any]:
    p = repo_path(path)
    stat = p.stat()
    members: dict[str, Any] = {}
    with zipfile.ZipFile(p) as archive:
        for info in archive.infolist():
            with archive.open(info) as member:
                header = npy_header(member)
            members[info.filename.removesuffix(".npy")] = {
                **header,
                "member": info.filename,
                "file_size": int(info.file_size),
                "compressed_size": int(info.compress_size),
                "compression": int(info.compress_type),
                "zip_crc32": f"{info.CRC:08x}",
            }
    return {
        "path": str(p),
        "size_bytes": int(stat.st_size),
        "mtime_ns": int(stat.st_mtime_ns),
        "sha256": sha256_file(p) if full_sha256 else None,
        "sha256_recomputed": bool(full_sha256),
        "members": members,
    }


def inspect_local_hf_snapshot(
    model_name: str, *, require_model: bool, require_tokenizer: bool
) -> tuple[dict[str, Any], list[str]]:
    """Freeze an exact local model or tokenizer snapshot without loading tensors."""
    errors: list[str] = []
    try:
        from huggingface_hub import snapshot_download

        snapshot = Path(snapshot_download(repo_id=model_name, local_files_only=True)).resolve()
    except Exception as exc:
        return {"model": model_name, "status": "unavailable"}, [
            f"local Hugging Face snapshot unavailable for {model_name}: {type(exc).__name__}: {exc}"
        ]
    relevant_names: list[str] = ["config.json"]
    if require_model:
        relevant_names.extend(("generation_config.json", "model.safetensors", "pytorch_model.bin"))
    if require_tokenizer:
        relevant_names.extend(
            (
                "tokenizer.json",
                "tokenizer_config.json",
                "vocab.json",
                "merges.txt",
                "special_tokens_map.json",
            )
        )
    files: list[dict[str, Any]] = []
    for name in relevant_names:
        path = snapshot / name
        if path.exists():
            files.append(
                {
                    "name": name,
                    "path": str(path),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    if require_model and not any(
        row["name"] in {"model.safetensors", "pytorch_model.bin"} for row in files
    ):
        errors.append(f"{snapshot}: no supported model-weight file")
    if require_tokenizer and not any(
        row["name"] in {"tokenizer.json", "vocab.json"} for row in files
    ):
        errors.append(f"{snapshot}: no tokenizer vocabulary file")
    return {
        "model": model_name,
        "status": "valid" if not errors else "invalid",
        "snapshot_path": str(snapshot),
        "snapshot_revision": snapshot.name,
        "requirements": {
            "model_weights": require_model,
            "tokenizer_vocabulary": require_tokenizer,
        },
        "files": files,
    }, errors


def inspect_runtime_environment(device: str) -> tuple[dict[str, Any], list[str]]:
    """Freeze the numerical software lock and selected accelerator class."""
    import importlib.metadata
    import platform

    errors: list[str] = []
    files: list[dict[str, Any]] = []
    for raw_path in ENVIRONMENT_FILES:
        path = repo_path(raw_path)
        if not path.exists():
            errors.append(f"missing numerical environment file: {path}")
            continue
        files.append(
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    packages: dict[str, str] = {}
    for distribution in (
        "numpy",
        "scipy",
        "scikit-learn",
        "torch",
        "transformers",
        "safetensors",
        "huggingface-hub",
    ):
        try:
            packages[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            errors.append(f"missing numerical package: {distribution}")
    accelerator: dict[str, Any] = {"selected_device": device}
    if device == "cuda":
        import torch

        if not torch.cuda.is_available():
            errors.append("CUDA was selected for the frozen design but is unavailable")
        else:
            accelerator.update(
                {
                    "device_name": torch.cuda.get_device_name(0),
                    "compute_capability": list(torch.cuda.get_device_capability(0)),
                    "torch_cuda_version": torch.version.cuda,
                    "cudnn_version": torch.backends.cudnn.version(),
                }
            )
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "packages": packages,
        "environment_files": files,
        "accelerator": accelerator,
        "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
    }, errors


def load_npz_member(path: str | Path, key: str) -> np.ndarray:
    p = repo_path(path)
    with zipfile.ZipFile(p) as archive, archive.open(f"{key}.npy") as member:
        return np.load(member, allow_pickle=False)


def keyed_u64(identifier: int, key: str) -> int:
    digest = hashlib.blake2b(digest_size=8, key=key.encode("utf-8"))
    digest.update(int(identifier).to_bytes(8, "little", signed=False))
    return int.from_bytes(digest.digest(), "little", signed=False)


def freeze_sample(
    identifiers: Sequence[int] | np.ndarray,
    key: str,
    n: int,
    excluded: Iterable[int] = (),
) -> dict[str, Any]:
    ids = np.asarray(identifiers, dtype=np.int64)
    if len(np.unique(ids)) != len(ids):
        raise ValueError("canonical identifiers must be unique before hash sampling")
    excluded_set = {int(x) for x in excluded}
    candidates = [
        (keyed_u64(int(identifier), key), int(identifier), int(position))
        for position, identifier in enumerate(ids)
        if int(identifier) not in excluded_set
    ]
    if len(candidates) < n:
        raise ValueError(f"sample size {n} exceeds {len(candidates)} eligible identifiers")
    selected = sorted(candidates, key=lambda row: (row[0], row[1]))[:n]
    selected_by_id = sorted(selected, key=lambda row: row[1])
    item_ids = [row[1] for row in selected_by_id]
    row_positions = [row[2] for row in selected_by_id]
    return {
        "key": key,
        "selection": "smallest unsigned BLAKE2b-64 keyed hash; tie-break canonical identifier",
        "n": n,
        "item_ids_sorted": item_ids,
        "row_positions_for_sorted_item_ids": row_positions,
        "item_ids_sha256_int64_le": sha256_int64(item_ids),
        "row_positions_sha256_int64_le": sha256_int64(row_positions),
    }


def artifact_model_path(directory: str | Path | None) -> Path | None:
    if not directory:
        return None
    base = repo_path(directory)
    for name in ("model.safetensors", "pytorch_model.bin"):
        candidate = base / name
        if candidate.exists():
            return candidate
    return None


def normalize_run_rows(
    family: str,
    source: Mapping[str, Any],
    path: Path,
    weight_sha_cache: dict[str, str],
) -> list[dict[str, Any]]:
    rows = source.get("rows")
    if not isinstance(rows, list):
        raise ValueError(f"{path}: missing list-valued rows")
    normalized: list[dict[str, Any]] = []
    for raw in rows:
        if not isinstance(raw, Mapping):
            continue
        artifact_dir = repo_path(raw["model_artifact_dir"]) if raw.get("model_artifact_dir") else None
        artifact_manifest = artifact_dir / "e016_model_artifact.json" if artifact_dir else None
        model_path = artifact_model_path(artifact_dir)
        artifact_metadata: dict[str, Any] | None = None
        if artifact_manifest and artifact_manifest.exists():
            artifact_metadata = load_json(artifact_manifest)
        model_sha = None
        if model_path is not None:
            model_key = str(model_path)
            if model_key not in weight_sha_cache:
                weight_sha_cache[model_key] = sha256_file(model_path)
            model_sha = weight_sha_cache[model_key]
        normalized.append(
            {
                "family": family,
                "source_run": str(path),
                "seed": int(raw["seed"]),
                "arm": str(raw["arm"]),
                "lambda_brain": raw.get("lambda_brain"),
                "steps": raw.get("steps"),
                "target_dim": raw.get("target_dim"),
                "n_train": raw.get("n_train"),
                "perplexity": raw.get("perplexity"),
                "target_r2": raw.get("target_r2"),
                "final_loss": raw.get("final_loss"),
                "final_kd": raw.get("final_kd"),
                "final_brain": raw.get("final_brain"),
                "model_artifact_dir": str(artifact_dir) if artifact_dir else None,
                "artifact_manifest": str(artifact_manifest) if artifact_manifest else None,
                "artifact_manifest_sha256": (
                    sha256_file(artifact_manifest) if artifact_manifest and artifact_manifest.exists() else None
                ),
                "artifact_metadata_identity": (
                    {
                        "seed": artifact_metadata.get("seed"),
                        "arm": artifact_metadata.get("arm"),
                        "lambda_brain": artifact_metadata.get("lambda_brain"),
                        "target_label": artifact_metadata.get("target_label"),
                        "target_cache": artifact_metadata.get("target_cache"),
                        "heldout_target_cache": artifact_metadata.get("heldout_target_cache"),
                    }
                    if artifact_metadata is not None
                    else None
                ),
                "model_weights": str(model_path) if model_path else None,
                "model_weights_size": model_path.stat().st_size if model_path else None,
                "model_weights_sha256": model_sha,
            }
        )
    return normalized


def collect_run_manifest(
    family: str,
    spec: Mapping[str, Any],
    weight_sha_cache: dict[str, str],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    rows_by_key: dict[tuple[int, str], dict[str, Any]] = {}
    sources: list[dict[str, Any]] = []
    for raw_path in spec["run_jsons"]:
        path = repo_path(raw_path)
        if not path.exists():
            errors.append(f"missing run JSON: {path}")
            continue
        data = load_json(path)
        if data.get("target_label") != family:
            errors.append(f"{path}: target_label={data.get('target_label')!r}, expected {family!r}")
        for field, expected in (
            ("target_cache", repo_path(spec["train_cache"])),
            ("heldout_target_cache", repo_path(spec["heldout_cache"])),
        ):
            recorded = repo_path(data.get(field, ""))
            if str(recorded) != str(expected):
                errors.append(f"{path}: {field}={recorded}, expected {expected}")
        config = data.get("config") if isinstance(data.get("config"), Mapping) else {}
        expected_config = {
            "teacher": "gpt2-medium",
            "student": "gpt2",
            "epochs": 1,
            "lr": 5e-5,
            "batch_size": 4,
            "max_length": 64,
            "limit_train": None,
            "limit_heldout": HELDOUT_N,
            "perm_blocks": 10,
        }
        for field, expected in expected_config.items():
            if config.get(field) != expected:
                errors.append(
                    f"{path}: config {field}={config.get(field)!r}, expected {expected!r}"
                )
        if str(config.get("lambda_brain_grid")) != "0.1":
            errors.append(f"{path}: lambda_brain_grid is not the locked 0.1")
        standardization = data.get("target_standardization")
        if not isinstance(standardization, Mapping):
            errors.append(f"{path}: missing target_standardization metadata")
        elif standardization.get("mean_shape") != [1, TARGET_D] or standardization.get(
            "std_shape"
        ) != [1, TARGET_D]:
            errors.append(f"{path}: target standardization shapes differ from [1, {TARGET_D}]")
        source_rows = normalize_run_rows(family, data, path, weight_sha_cache)
        sources.append(
            {
                "path": str(path),
                "sha256": sha256_file(path),
                "config": data.get("config"),
                "target_standardization": data.get("target_standardization"),
            }
        )
        for row in source_rows:
            expected_lambda = 0.0 if row["arm"] == "kd_only" else 0.1
            for field, expected in (
                ("lambda_brain", expected_lambda),
                ("steps", 24_000),
                ("target_dim", TARGET_D),
                ("n_train", TRAIN_N),
            ):
                if row.get(field) != expected:
                    errors.append(
                        f"{path}: seed={row['seed']} arm={row['arm']} {field}="
                        f"{row.get(field)!r}, expected {expected!r}"
                    )
            if row.get("target_r2") is None or not math.isfinite(float(row["target_r2"])):
                errors.append(f"{path}: seed={row['seed']} arm={row['arm']} target_r2 unavailable")
            if not row.get("model_weights_sha256"):
                errors.append(f"{path}: seed={row['seed']} arm={row['arm']} model weights unavailable")
            elif Path(str(row.get("model_weights"))).suffix != ".safetensors":
                errors.append(
                    f"{path}: seed={row['seed']} arm={row['arm']} parameter audit requires safetensors"
                )
            artifact_identity = row.get("artifact_metadata_identity")
            if not isinstance(artifact_identity, Mapping):
                errors.append(f"{path}: seed={row['seed']} arm={row['arm']} artifact metadata missing")
            else:
                for field, expected in (
                    ("seed", row["seed"]),
                    ("arm", row["arm"]),
                    ("lambda_brain", expected_lambda),
                    ("target_label", family),
                ):
                    if artifact_identity.get(field) != expected:
                        errors.append(
                            f"{path}: artifact seed={row['seed']} arm={row['arm']} "
                            f"{field}={artifact_identity.get(field)!r}, expected {expected!r}"
                        )
                for field, expected in (
                    ("target_cache", repo_path(spec["train_cache"])),
                    ("heldout_target_cache", repo_path(spec["heldout_cache"])),
                ):
                    observed_path = repo_path(str(artifact_identity.get(field, "")))
                    if str(observed_path) != str(expected):
                        errors.append(
                            f"{path}: artifact seed={row['seed']} arm={row['arm']} "
                            f"{field}={observed_path}, expected {expected}"
                        )
            key = (row["seed"], row["arm"])
            prior = rows_by_key.get(key)
            if prior is not None and any(
                prior.get(field) != row.get(field)
                for field in ("target_r2", "final_loss", "model_artifact_dir")
            ):
                errors.append(f"conflicting duplicate run row for {family} seed/arm={key}")
            rows_by_key[key] = row
    expected_arms = {"kd_only", str(spec["target_arm"]), str(spec["permuted_arm"])}
    for seed in range(6):
        got = {arm for (row_seed, arm) in rows_by_key if row_seed == seed}
        if got != expected_arms:
            errors.append(f"{family} seed {seed}: arms={sorted(got)}, expected={sorted(expected_arms)}")
    return {
        "target_label": family,
        "target_arm": spec["target_arm"],
        "permuted_arm": spec["permuted_arm"],
        "sources": sources,
        "rows": [rows_by_key[key] for key in sorted(rows_by_key)],
    }, errors


def verify_seed_matched_kd_identity(run_reports: Mapping[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Verify the alleged shared baselines using manifest-frozen weight hashes."""
    errors: list[str] = []
    output: dict[str, Any] = {}
    for seed in range(6):
        rows: dict[str, Mapping[str, Any]] = {}
        for family in ("tribe", "textfeat"):
            matches = [
                row
                for row in run_reports[family]["rows"]
                if int(row["seed"]) == seed and row["arm"] == "kd_only"
            ]
            if len(matches) != 1:
                errors.append(f"{family} seed {seed}: expected one KD row, found {len(matches)}")
                continue
            rows[family] = matches[0]
        if len(rows) != 2:
            continue
        record: dict[str, Any] = {"seed": seed, "families": {}}
        hashes: dict[str, str] = {}
        for family, row in rows.items():
            raw = row.get("model_weights")
            path = repo_path(raw) if raw else None
            if path is None or not path.exists():
                errors.append(f"{family} seed {seed}: KD model weights unavailable: {path}")
                continue
            hashes[family] = str(row.get("model_weights_sha256") or "")
            if not hashes[family]:
                errors.append(f"{family} seed {seed}: KD weight hash unavailable")
                continue
            record["families"][family] = {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": hashes[family],
            }
        record["byte_identical"] = len(hashes) == 2 and len(set(hashes.values())) == 1
        if len(hashes) == 2 and not record["byte_identical"]:
            errors.append(f"seed {seed}: TRIBE/textfeat KD model weights are not byte-identical")
        output[str(seed)] = record
    return output, errors


def locate_e025_manifest(explicit: Path | None) -> Path | None:
    if explicit is not None:
        return repo_path(explicit)
    candidates = (
        Path("outputs/E025/extraction.json"),
        Path("outputs/E025/manifest.json"),
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def canonical_e025_aliases(raw: Any, context: str) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        raise ValueError(f"{context}: aliases must be a list")
    aliases: list[dict[str, Any]] = []
    for index, value in enumerate(raw):
        if not isinstance(value, Mapping):
            raise ValueError(f"{context}: alias {index} is not an object")
        try:
            aliases.append(
                {
                    "family": str(value["family"]),
                    "seed": int(value["seed"]),
                    "arm": str(value["arm"]),
                }
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"{context}: malformed alias {index}: {exc}") from exc
    aliases.sort(key=lambda row: (row["family"], row["seed"], row["arm"]))
    identities = [(row["family"], row["seed"], row["arm"]) for row in aliases]
    if len(set(identities)) != len(identities):
        raise ValueError(f"{context}: duplicate aliases")
    return aliases


def inspect_e025_base_manifest(
    path: Path, data: Mapping[str, Any]
) -> tuple[dict[str, Any], list[str], dict[tuple[str, int, str], Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    """Validate E025's frozen metadata preflight without loading representation values."""
    errors: list[str] = []
    if data.get("schema_version") != E025_SCHEMA_VERSION:
        errors.append(
            f"E025 base schema={data.get('schema_version')!r}, expected {E025_SCHEMA_VERSION!r}"
        )
    if data.get("stage") != "manifest":
        errors.append(f"E025 base stage={data.get('stage')!r}, expected 'manifest'")
    if data.get("preflight_pass") is not True:
        errors.append("E025 base preflight_pass is not true")

    design = data.get("design_lock") if isinstance(data.get("design_lock"), Mapping) else {}
    if list(design.get("layers") or []) != [6, 7]:
        errors.append(f"E025 design layers={design.get('layers')!r}, expected [6, 7]")
    if design.get("representation_pooling") != "attention-mask mean":
        errors.append("E025 representation pooling is not attention-mask mean")
    if int(design.get("max_length", -1)) != 64:
        errors.append(f"E025 max_length={design.get('max_length')!r}, expected 64")

    planned = data.get("planned_cache") if isinstance(data.get("planned_cache"), Mapping) else {}
    required_keys = {
        "wikitext_layer_6",
        "wikitext_layer_7",
        "tuckute_layer_6",
        "tuckute_layer_7",
        "metadata_json",
    }
    if set(planned.get("checkpoint_npz_keys") or []) != required_keys:
        errors.append("E025 planned checkpoint NPZ keys differ from the locked layer-6/7 contract")

    logical_raw = data.get("logical_aliases")
    logical_rows = logical_raw if isinstance(logical_raw, list) else []
    if not isinstance(logical_raw, list):
        errors.append("E025 logical_aliases must be a list")
    if len(logical_rows) != 36:
        errors.append(f"E025 logical alias count={len(logical_rows)}, expected 36")
    alias_lookup: dict[tuple[str, int, str], Mapping[str, Any]] = {}
    for index, alias in enumerate(logical_rows):
        if not isinstance(alias, Mapping):
            errors.append(f"E025 logical alias {index} is not an object")
            continue
        try:
            identity = (str(alias["family"]), int(alias["seed"]), str(alias["arm"]))
            if identity in alias_lookup:
                errors.append(f"E025 duplicate logical alias: {identity}")
            alias_lookup[identity] = alias
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"E025 malformed logical alias {index}: {exc}")
    expected_identities = {
        (family, seed, arm)
        for family, arms in {
            "tribe": ("kd_only", "tribe_mse", "tribe_perm"),
            "textfeat": ("kd_only", "textfeat_mse", "textfeat_perm"),
        }.items()
        for seed in range(6)
        for arm in arms
    }
    if set(alias_lookup) != expected_identities:
        missing = sorted(expected_identities - set(alias_lookup))
        extra = sorted(set(alias_lookup) - expected_identities)
        errors.append(f"E025 logical grid mismatch; missing={missing}, extra={extra}")

    checkpoints_raw = data.get("unique_checkpoints")
    checkpoint_rows = checkpoints_raw if isinstance(checkpoints_raw, list) else []
    if not isinstance(checkpoints_raw, list):
        errors.append("E025 unique_checkpoints must be a list")
    if len(checkpoint_rows) != 30:
        errors.append(f"E025 unique checkpoint count={len(checkpoint_rows)}, expected 30")
    checkpoint_lookup: dict[str, Mapping[str, Any]] = {}
    for index, checkpoint in enumerate(checkpoint_rows):
        if not isinstance(checkpoint, Mapping):
            errors.append(f"E025 unique checkpoint {index} is not an object")
            continue
        key = str(checkpoint.get("cache_key", ""))
        if not key or key in checkpoint_lookup:
            errors.append(f"E025 invalid/duplicate checkpoint cache_key={key!r}")
            continue
        checkpoint_lookup[key] = checkpoint
    alias_cache_keys = {str(row.get("cache_key", "")) for row in alias_lookup.values()}
    if alias_cache_keys != set(checkpoint_lookup):
        errors.append(
            "E025 cache keys referenced by logical aliases differ from unique_checkpoints"
        )
    for cache_key, checkpoint in checkpoint_lookup.items():
        try:
            checkpoint_aliases = canonical_e025_aliases(
                checkpoint.get("aliases"), f"E025 checkpoint {cache_key}"
            )
        except ValueError as exc:
            errors.append(str(exc))
            checkpoint_aliases = []
        logical_for_cache = []
        for identity, alias in alias_lookup.items():
            if str(alias.get("cache_key", "")) == cache_key:
                logical_for_cache.append(
                    {"family": identity[0], "seed": identity[1], "arm": identity[2]}
                )
                if alias.get("weight_sha256") != checkpoint.get("weight_sha256"):
                    errors.append(f"E025 {identity}: weight hash differs from checkpoint {cache_key}")
                if alias.get("runtime_sha256") != checkpoint.get("runtime_sha256"):
                    errors.append(f"E025 {identity}: runtime hash differs from checkpoint {cache_key}")
        logical_for_cache.sort(key=lambda row: (row["family"], row["seed"], row["arm"]))
        if checkpoint_aliases != logical_for_cache:
            errors.append(f"E025 checkpoint {cache_key}: aliases differ from logical grid")
        planned_path = checkpoint.get("planned_cache_npz")
        if not planned_path or repo_path(str(planned_path)).suffix != ".npz":
            errors.append(f"E025 checkpoint {cache_key}: invalid planned cache path")

    checks = data.get("checks") if isinstance(data.get("checks"), list) else []
    required_checks = {
        "exact_logical_grid",
        "shared_kd_weight_and_runtime_identity",
        "unique_checkpoint_count",
        "tuckute_participant_roi_text_completeness",
        "wikitext_order_and_count",
        "target_cache_presence_and_hashes",
    }
    passed_checks = {
        str(row.get("name"))
        for row in checks
        if isinstance(row, Mapping) and row.get("status") == "PASS"
    }
    if not required_checks.issubset(passed_checks):
        errors.append(f"E025 required preflight checks not passing: {sorted(required_checks - passed_checks)}")

    wiki = data.get("wikitext_heldout") if isinstance(data.get("wikitext_heldout"), Mapping) else {}
    tuckute = data.get("tuckute") if isinstance(data.get("tuckute"), Mapping) else {}
    if int(wiki.get("scored_prefix_lines", -1)) != HELDOUT_N:
        errors.append("E025 WikiText scored-prefix count is not 1,999")
    if int(tuckute.get("ordered_item_count", -1)) != 1_000:
        errors.append("E025 Tuckute ordered item count is not 1,000")

    public = {
        "path": str(path),
        "sha256": sha256_file(path),
        "schema_version": data.get("schema_version"),
        "stage": data.get("stage"),
        "preflight_pass": data.get("preflight_pass"),
        "logical_alias_count": len(logical_rows),
        "unique_checkpoint_count": len(checkpoint_rows),
        "ordered_inputs": {
            "wikitext_n": wiki.get("scored_prefix_lines"),
            "wikitext_sha256": wiki.get("ordered_text_sha256"),
            "tuckute_n": tuckute.get("ordered_item_count"),
            "tuckute_sha256": tuckute.get("ordered_text_sha256"),
            "tuckute_item_id_sha256": tuckute.get("ordered_item_id_sha256"),
        },
        "configuration": {
            "layers": design.get("layers"),
            "pooling": design.get("representation_pooling"),
            "max_length": design.get("max_length"),
        },
        "source_targets": data.get("source_targets"),
        "source_run_jsons": data.get("source_run_jsons"),
        "extraction_expected_path": planned.get("extraction_index_json"),
        "logical_aliases": [
            {
                "family": identity[0],
                "seed": identity[1],
                "arm": identity[2],
                "cache_key": alias.get("cache_key"),
                "weight_sha256": alias.get("weight_sha256"),
                "runtime_sha256": alias.get("runtime_sha256"),
            }
            for identity, alias in sorted(alias_lookup.items())
        ],
        "unique_checkpoints": [
            {
                "cache_key": key,
                "weight_sha256": checkpoint.get("weight_sha256"),
                "runtime_sha256": checkpoint.get("runtime_sha256"),
                "aliases": checkpoint.get("aliases"),
                "planned_cache_npz": checkpoint.get("planned_cache_npz"),
            }
            for key, checkpoint in sorted(checkpoint_lookup.items())
        ],
    }
    return public, errors, alias_lookup, checkpoint_lookup


def inspect_e025_manifest(path: Path | None) -> dict[str, Any]:
    """Inspect either E025 extraction.json or its preflight-only manifest.json."""
    if path is None:
        return {
            "status": "unavailable",
            "reason": "no E025 manifest/extraction found; trained CKA/RMS must remain unavailable",
            "errors": [],
        }
    path = repo_path(path)
    if not path.exists():
        return {"status": "invalid", "path": str(path), "errors": [f"file not found: {path}"]}
    try:
        data = load_json(path)
    except Exception as exc:
        return {"status": "invalid", "path": str(path), "errors": [str(exc)]}

    if data.get("stage") == "manifest":
        base, errors, _, _ = inspect_e025_base_manifest(path, data)
        return {
            "status": "preflight_only" if not errors else "invalid",
            "kind": "manifest",
            "path": str(path),
            "sha256": base["sha256"],
            "base_manifest": base,
            "reason": (
                "passing E025 metadata preflight found, but extraction.json is not present; "
                "trained CKA/RMS remain unavailable"
            ),
            "errors": errors,
        }
    if data.get("stage") != "extract" or data.get("schema_version") != E025_SCHEMA_VERSION:
        return {
            "status": "invalid",
            "path": str(path),
            "sha256": sha256_file(path),
            "errors": ["E025 file is neither the v1 manifest nor the v1 extraction index"],
        }

    errors: list[str] = []
    manifest_link = data.get("manifest") if isinstance(data.get("manifest"), Mapping) else {}
    base_path_raw = manifest_link.get("path")
    if not base_path_raw:
        return {
            "status": "invalid",
            "kind": "extraction",
            "path": str(path),
            "sha256": sha256_file(path),
            "errors": ["E025 extraction does not declare its base-manifest path"],
        }
    base_path = repo_path(str(base_path_raw))
    if not base_path.exists():
        return {
            "status": "invalid",
            "kind": "extraction",
            "path": str(path),
            "sha256": sha256_file(path),
            "errors": [f"E025 extraction base manifest not found: {base_path}"],
        }
    base_data = load_json(base_path)
    base, base_errors, alias_lookup, checkpoint_lookup = inspect_e025_base_manifest(
        base_path, base_data
    )
    errors.extend(base_errors)
    if manifest_link.get("sha256") != base["sha256"]:
        errors.append("E025 extraction -> base-manifest SHA-256 mismatch")

    configuration = data.get("configuration") if isinstance(data.get("configuration"), Mapping) else {}
    if list(configuration.get("layers") or []) != [6, 7]:
        errors.append("E025 extraction layers are not exactly [6, 7]")
    if configuration.get("pooling") != "attention-mask mean":
        errors.append("E025 extraction pooling is not attention-mask mean")
    if int(configuration.get("max_length", -1)) != 64:
        errors.append("E025 extraction max_length is not 64")
    ordered = data.get("ordered_inputs") if isinstance(data.get("ordered_inputs"), Mapping) else {}
    if ordered.get("wikitext_sha256") != base["ordered_inputs"]["wikitext_sha256"]:
        errors.append("E025 extraction WikiText order hash differs from base manifest")
    if ordered.get("tuckute_sha256") != base["ordered_inputs"]["tuckute_sha256"]:
        errors.append("E025 extraction Tuckute order hash differs from base manifest")

    cache_rows_raw = data.get("cache_rows")
    cache_rows = cache_rows_raw if isinstance(cache_rows_raw, list) else []
    if not isinstance(cache_rows_raw, list):
        errors.append("E025 extraction cache_rows must be a list")
    cache_reports: list[dict[str, Any]] = []
    observed_cache_keys: list[str] = []
    expected_arrays = {
        "wikitext_layer_6": HELDOUT_N,
        "wikitext_layer_7": HELDOUT_N,
        "tuckute_layer_6": 1_000,
        "tuckute_layer_7": 1_000,
    }
    for index, row in enumerate(cache_rows):
        if not isinstance(row, Mapping):
            errors.append(f"E025 extraction cache row {index} is not an object")
            continue
        cache_key = str(row.get("cache_key", ""))
        observed_cache_keys.append(cache_key)
        checkpoint = checkpoint_lookup.get(cache_key)
        if checkpoint is None:
            errors.append(f"E025 extraction has unknown cache key {cache_key!r}")
            continue
        cache_path = repo_path(str(row.get("path", "")))
        if not cache_path.exists():
            errors.append(f"E025 representation cache is missing: {cache_path}")
            continue
        try:
            actual_sha = sha256_file(cache_path)
            if row.get("sha256") != actual_sha:
                errors.append(f"E025 cache {cache_key}: extraction-index SHA-256 mismatch")
            if row.get("weight_sha256") != checkpoint.get("weight_sha256"):
                errors.append(f"E025 cache {cache_key}: weight hash differs from base manifest")
            try:
                row_aliases = canonical_e025_aliases(row.get("aliases"), f"E025 cache row {cache_key}")
                checkpoint_aliases = canonical_e025_aliases(
                    checkpoint.get("aliases"), f"E025 checkpoint {cache_key}"
                )
                if row_aliases != checkpoint_aliases:
                    errors.append(f"E025 cache {cache_key}: aliases differ from base manifest")
            except ValueError as exc:
                errors.append(str(exc))
                row_aliases = []

            archive = inspect_npz(cache_path, full_sha256=False)
            members = archive["members"]
            if set(members) != set(expected_arrays) | {"metadata_json"}:
                errors.append(f"E025 cache {cache_key}: NPZ keys differ from frozen contract")
            hidden_dims: set[int] = set()
            headers: dict[str, Any] = {}
            for array_key, expected_rows in expected_arrays.items():
                header = members.get(array_key)
                if header is None:
                    continue
                headers[array_key] = header
                shape = header.get("shape") or []
                if len(shape) != 2 or int(shape[0]) != expected_rows or int(shape[1]) <= 0:
                    errors.append(
                        f"E025 cache {cache_key}:{array_key}: shape={shape}, "
                        f"expected [{expected_rows}, hidden_dim]"
                    )
                elif len(shape) == 2:
                    hidden_dims.add(int(shape[1]))
                if header.get("dtype") != "float32":
                    errors.append(
                        f"E025 cache {cache_key}:{array_key}: dtype={header.get('dtype')}, expected float32"
                    )
            if len(hidden_dims) > 1:
                errors.append(f"E025 cache {cache_key}: hidden dimensions differ across arrays")

            metadata_raw = load_npz_member(cache_path, "metadata_json")
            if metadata_raw.shape != ():
                raise ValueError(f"metadata_json shape={metadata_raw.shape}, expected scalar")
            metadata = json.loads(str(metadata_raw.item()))
            metadata_checks = {
                "schema_version": E025_SCHEMA_VERSION,
                "cache_key": cache_key,
                "weight_sha256": checkpoint.get("weight_sha256"),
                "runtime_sha256": checkpoint.get("runtime_sha256"),
                "pooling": "attention-mask mean",
                "max_length": 64,
                "wikitext_ordered_text_sha256": base["ordered_inputs"]["wikitext_sha256"],
                "tuckute_ordered_text_sha256": base["ordered_inputs"]["tuckute_sha256"],
            }
            for field, expected in metadata_checks.items():
                if metadata.get(field) != expected:
                    errors.append(
                        f"E025 cache {cache_key}: metadata {field}={metadata.get(field)!r}, expected {expected!r}"
                    )
            if list(metadata.get("layers") or []) != [6, 7]:
                errors.append(f"E025 cache {cache_key}: metadata layers are not [6, 7]")
            try:
                metadata_aliases = canonical_e025_aliases(
                    metadata.get("aliases"), f"E025 cache metadata {cache_key}"
                )
                if metadata_aliases != row_aliases:
                    errors.append(f"E025 cache {cache_key}: metadata aliases differ from cache row")
            except ValueError as exc:
                errors.append(str(exc))
            cache_reports.append(
                {
                    "cache_key": cache_key,
                    "path": str(cache_path),
                    "declared_sha256": row.get("sha256"),
                    "recomputed_sha256": actual_sha,
                    "weight_sha256": row.get("weight_sha256"),
                    "aliases": row_aliases,
                    "headers": headers,
                }
            )
        except Exception as exc:
            errors.append(f"E025 cache {cache_key}: {type(exc).__name__}: {exc}")

    if len(observed_cache_keys) != 30 or len(set(observed_cache_keys)) != 30:
        errors.append(
            f"E025 extraction cache row count/uniqueness invalid: "
            f"rows={len(observed_cache_keys)}, unique={len(set(observed_cache_keys))}"
        )
    if set(observed_cache_keys) != set(checkpoint_lookup):
        errors.append("E025 extraction cache keys differ from base unique_checkpoints")
    return {
        "status": "valid" if not errors else "invalid",
        "kind": "extraction",
        "path": str(path),
        "sha256": sha256_file(path),
        "base_manifest": base,
        "ordered_inputs": dict(ordered),
        "configuration": dict(configuration),
        "cache_rows": cache_reports,
        "errors": errors,
    }


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    started = time.time()
    numerical_selftests = run_numerical_selftests()
    errors: list[str] = []
    warnings: list[str] = []
    cache_reports: dict[str, Any] = {}
    small_arrays: dict[tuple[str, str], dict[str, np.ndarray]] = {}
    for family, spec in TARGET_SOURCES.items():
        cache_reports[family] = {}
        for split, expected_n in (("train", TRAIN_N), ("heldout", HELDOUT_N)):
            cache_path = repo_path(spec[f"{split}_cache"])
            sidecar_path = repo_path(spec[f"{split}_sidecar"])
            try:
                report = inspect_npz(cache_path, full_sha256=not args.skip_full_cache_sha256)
                target = report["members"].get("targets") or {}
                if target.get("shape") != [expected_n, TARGET_D]:
                    errors.append(
                        f"{family}/{split}: target shape {target.get('shape')} != {[expected_n, TARGET_D]}"
                    )
                if target.get("dtype") != "float32":
                    errors.append(f"{family}/{split}: target dtype {target.get('dtype')} != float32")
                arrays = {
                    key: load_npz_member(cache_path, key)
                    for key in ("texts", "item_indices", "vertex_index", "segment_counts", "metadata")
                }
                small_arrays[(family, split)] = arrays
                report["content_identity"] = {
                    "texts_sha256_len_prefixed_utf8": sha256_strings(arrays["texts"].tolist()),
                    "item_indices_sha256_int64_le": sha256_int64(arrays["item_indices"]),
                    "vertex_index_sha256_int64_le": sha256_int64(arrays["vertex_index"]),
                    "segment_counts_sha256_int64_le": sha256_int64(arrays["segment_counts"]),
                }
                if len(arrays["item_indices"]) != expected_n:
                    errors.append(f"{family}/{split}: item_indices length mismatch")
                if len(np.unique(arrays["item_indices"])) != expected_n:
                    errors.append(f"{family}/{split}: item_indices are not unique")
                if sidecar_path.exists():
                    sidecar_metadata = load_json(sidecar_path)
                    sidecar_validation = validate_generator_sidecar(
                        family, split, sidecar_metadata
                    )
                    report["sidecar"] = {
                        "path": str(sidecar_path),
                        "sha256": sha256_file(sidecar_path),
                        "metadata": sidecar_metadata,
                        "semantic_validation": sidecar_validation,
                    }
                    errors.extend(sidecar_validation["errors"])
                else:
                    errors.append(f"missing sidecar: {sidecar_path}")
                cache_reports[family][split] = report
            except Exception as exc:
                errors.append(f"{family}/{split}: {type(exc).__name__}: {exc}")
    for split in ("train", "heldout"):
        if ("tribe", split) not in small_arrays or ("textfeat", split) not in small_arrays:
            continue
        left = small_arrays[("tribe", split)]
        right = small_arrays[("textfeat", split)]
        for key in ("texts", "item_indices", "vertex_index"):
            if not np.array_equal(left[key], right[key]):
                errors.append(f"{split}: TRIBE/textfeat {key} differ")
    row_samples: dict[str, Any] = {}
    coord_samples: dict[str, Any] = {}
    if ("tribe", "train") in small_arrays:
        canonical_ids = small_arrays[("tribe", "train")]["item_indices"]
        sample_a = freeze_sample(canonical_ids, ROW_SAMPLE_KEYS["A"], SAMPLE_N)
        sample_b = freeze_sample(
            canonical_ids,
            ROW_SAMPLE_KEYS["B"],
            SAMPLE_N,
            excluded=sample_a["item_ids_sorted"],
        )
        row_samples = {"A": sample_a, "B": sample_b}
        if set(sample_a["item_ids_sorted"]) & set(sample_b["item_ids_sorted"]):
            errors.append("row samples A and B overlap")
    coordinates = np.arange(TARGET_D, dtype=np.int64)
    coord_a = freeze_sample(coordinates, COORD_SAMPLE_KEYS["A"], COORD_SAMPLE_N)
    coord_b = freeze_sample(
        coordinates,
        COORD_SAMPLE_KEYS["B"],
        COORD_SAMPLE_N,
        excluded=coord_a["item_ids_sorted"],
    )
    coord_samples = {"A": coord_a, "B": coord_b}
    run_reports: dict[str, Any] = {}
    weight_sha_cache: dict[str, str] = {}
    for family, spec in TARGET_SOURCES.items():
        report, run_errors = collect_run_manifest(family, spec, weight_sha_cache)
        run_reports[family] = report
        errors.extend(run_errors)
    kd_identity, kd_errors = verify_seed_matched_kd_identity(run_reports)
    errors.extend(kd_errors)
    nuisance_model, nuisance_model_errors = inspect_local_hf_snapshot(
        NUISANCE_MODEL, require_model=True, require_tokenizer=False
    )
    errors.extend(nuisance_model_errors)
    nuisance_tokenizer, nuisance_tokenizer_errors = inspect_local_hf_snapshot(
        NUISANCE_TOKENIZER, require_model=False, require_tokenizer=True
    )
    errors.extend(nuisance_tokenizer_errors)
    execution_device = choose_device(args.device)
    runtime_environment, runtime_errors = inspect_runtime_environment(execution_device)
    errors.extend(runtime_errors)
    context_report: dict[str, Any] = {"path": str(CONTEXT_META), "available": CONTEXT_META.exists()}
    if CONTEXT_META.exists():
        context_report.update({"sha256": sha256_file(CONTEXT_META), "size_bytes": CONTEXT_META.stat().st_size})
    else:
        warnings.append("context metadata absent; order diagnostics must remain unresolved")
    if CONTEXT_SUMMARY.exists():
        context_report["summary"] = load_json(CONTEXT_SUMMARY)
        context_report["summary_sha256"] = sha256_file(CONTEXT_SUMMARY)
    e025 = inspect_e025_manifest(locate_e025_manifest(args.e025_manifest))
    if e025.get("status") in {"valid", "preflight_only"}:
        e025_errors = list(e025.get("errors") or [])
        base = e025.get("base_manifest") if isinstance(e025.get("base_manifest"), Mapping) else {}
        frozen_inputs = base.get("ordered_inputs") if isinstance(base.get("ordered_inputs"), Mapping) else {}
        heldout_texts = small_arrays.get(("tribe", "heldout"), {}).get("texts")
        cross_checks: dict[str, Any] = {}
        if heldout_texts is not None:
            current_wikitext_hash = sha256_newline_texts(heldout_texts.tolist())
            expected_wikitext_hash = frozen_inputs.get("wikitext_sha256")
            cross_checks["wikitext_heldout_order"] = {
                "e016_cache_sha256": current_wikitext_hash,
                "e025_sha256": expected_wikitext_hash,
                "match": current_wikitext_hash == expected_wikitext_hash,
            }
            if current_wikitext_hash != expected_wikitext_hash:
                e025_errors.append("E025 WikiText order/text hash differs from E016 heldout cache")

        current_targets = {
            str(repo_path(report["path"])): report
            for family_reports in cache_reports.values()
            for report in family_reports.values()
            if isinstance(report, Mapping) and report.get("path")
        }
        target_cross_checks: list[dict[str, Any]] = []
        for source in base.get("source_targets") or []:
            if not isinstance(source, Mapping):
                e025_errors.append("E025 source_targets contains a non-object record")
                continue
            normalized_path = str(repo_path(str(source.get("path", ""))))
            current = current_targets.get(normalized_path)
            match = bool(
                current
                and int(source.get("bytes", -1)) == int(current.get("size_bytes", -2))
                and (
                    current.get("sha256") is None
                    or source.get("sha256") == current.get("sha256")
                )
            )
            target_cross_checks.append(
                {
                    "path": normalized_path,
                    "e025_sha256": source.get("sha256"),
                    "e026_recomputed_sha256": current.get("sha256") if current else None,
                    "match": match,
                }
            )
            if not match:
                e025_errors.append(f"E025 source-target provenance mismatch: {normalized_path}")
        cross_checks["source_targets"] = target_cross_checks

        current_runs = {
            str(repo_path(source["path"])): source
            for report in run_reports.values()
            for source in report.get("sources") or []
            if isinstance(source, Mapping) and source.get("path")
        }
        run_cross_checks: list[dict[str, Any]] = []
        for source in base.get("source_run_jsons") or []:
            if not isinstance(source, Mapping):
                e025_errors.append("E025 source_run_jsons contains a non-object record")
                continue
            normalized_path = str(repo_path(str(source.get("path", ""))))
            current = current_runs.get(normalized_path)
            match = bool(current and source.get("sha256") == current.get("sha256"))
            run_cross_checks.append(
                {
                    "path": normalized_path,
                    "e025_sha256": source.get("sha256"),
                    "e026_recomputed_sha256": current.get("sha256") if current else None,
                    "match": match,
                }
            )
            if not match:
                e025_errors.append(f"E025 source-run provenance mismatch: {normalized_path}")
        cross_checks["source_run_jsons"] = run_cross_checks

        e025_alias_hashes = {
            (str(row["family"]), int(row["seed"]), str(row["arm"])): row.get("weight_sha256")
            for row in base.get("logical_aliases") or []
            if isinstance(row, Mapping)
        }
        weight_cross_checks: list[dict[str, Any]] = []
        for family, report in run_reports.items():
            for row in report.get("rows") or []:
                identity = (family, int(row["seed"]), str(row["arm"]))
                expected = e025_alias_hashes.get(identity)
                observed = row.get("model_weights_sha256")
                match = bool(expected and observed and expected == observed)
                weight_cross_checks.append(
                    {
                        "family": identity[0],
                        "seed": identity[1],
                        "arm": identity[2],
                        "e025_weight_sha256": expected,
                        "e026_weight_sha256": observed,
                        "match": match,
                    }
                )
                if not match:
                    e025_errors.append(f"E025/E026 model-weight mismatch: {identity}")
        cross_checks["model_weights"] = weight_cross_checks
        e025["cross_checks_against_e016"] = cross_checks
        e025["errors"] = e025_errors
        if e025_errors:
            e025["status"] = "invalid"
    if e025["status"] == "invalid":
        warnings.append("E025 representation provenance is invalid; CKA/RMS will be unavailable")
    elif e025["status"] in {"unavailable", "preflight_only"}:
        warnings.append(str(e025["reason"]))
    if args.skip_full_cache_sha256:
        warnings.append(
            "full target-cache SHA-256 was skipped; this is a smoke manifest and cannot authorize geometry"
        )
    if not numerical_selftests.get("pass"):
        errors.append("synthetic numerical selftests failed")
    parity_checks = {
        "train_and_heldout_target_shape": not any("target shape" in value for value in errors),
        "train_and_heldout_item_text_order": not any(
            "TRIBE/textfeat" in value and "differ" in value for value in errors
        ),
        "six_seed_arm_grid": not any("arms=" in value for value in errors),
        "training_budget_and_standardization_metadata": not any(
            "config " in value or "standardization" in value or "steps=" in value
            for value in errors
        ),
        "seed_matched_kd_weights": len(kd_identity) == 6
        and all(record.get("byte_identical") is True for record in kd_identity.values()),
    }
    full_hashes_frozen = not args.skip_full_cache_sha256 and all(
        bool(report.get("sha256"))
        for family_reports in cache_reports.values()
        for report in family_reports.values()
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "experiment": "E026",
        "stage": "manifest",
        "science_status": SCIENCE_STATUS,
        "created_at_utc": utc_now(),
        "elapsed_s": time.time() - started,
        "audit_script": {
            "path": str(repo_path(Path(__file__).resolve())),
            "sha256": sha256_file(repo_path(Path(__file__).resolve())),
        },
        "owning_e_record": {
            "path": str(E026_RECORD),
            "sha256": sha256_file(E026_RECORD),
        },
        "numerical_selftests": numerical_selftests,
        "design_lock": {
            "training_standardization": "(Y - full_train_population_mean) / (full_train_population_std + 1e-6)",
            "standardization_extrema_relative_tolerance": STANDARDIZATION_EXTREMA_RTOL,
            "row_sample_n": SAMPLE_N,
            "coordinate_sample_n": COORD_SAMPLE_N,
            "svd": {
                "seed": SVD_SEED,
                "top_k": SVD_K,
                "oversample": SVD_OVERSAMPLE,
                "power_iterations": SVD_POWER_ITERS,
                "orthogonality_max": SVD_ORTHOGONALITY_MAX,
                "captured_energy_tolerance": SVD_ENERGY_TOL,
            },
            "algebraic_centered_rank_caps": ALGEBRAIC_RANK_CAP,
            "nuisance_predictability": {
                "model": NUISANCE_MODEL,
                "tokenizer": NUISANCE_TOKENIZER,
                "max_length": NUISANCE_MAX_LENGTH,
                "static_pca_rank": NUISANCE_PCA_RANK,
                "inner_contiguous_folds": NUISANCE_INNER_FOLDS,
                "position_blocks": NUISANCE_POSITION_BLOCKS,
                "ridge_alphas": list(NUISANCE_RIDGE_ALPHAS),
                "target_coordinate_chunk": NUISANCE_TARGET_CHUNK,
            },
            "execution_chunks": {
                "row_chunk": ROW_CHUNK,
                "static_batch_size": STATIC_BATCH_SIZE,
                "target_coordinate_chunk": NUISANCE_TARGET_CHUNK,
            },
            "derived_scratch_reuse": DERIVED_SCRATCH_REUSE,
            "execution_device": execution_device,
            "margins": MARGINS,
            "mechanical_logic": "FAIL if any required observed margin fails; PASS only if all pass; otherwise UNRESOLVED",
            "target_coordinates_are_replication_units": False,
        },
        "parity_checks": parity_checks,
        "target_caches": cache_reports,
        "row_samples": row_samples,
        "coordinate_samples": coord_samples,
        "context_provenance": context_report,
        "runs": run_reports,
        "seed_matched_kd_weight_identity": kd_identity,
        "nuisance_static_model_provenance": nuisance_model,
        "nuisance_static_tokenizer_provenance": nuisance_tokenizer,
        "runtime_environment": runtime_environment,
        "e025_representation_provenance": e025,
        "integrity": {
            "target_manifest_valid": not errors,
            "full_target_hashes_frozen": full_hashes_frozen,
            "geometry_sources_ready": not errors and full_hashes_frozen,
            "trained_representation_sources_ready": e025.get("status") == "valid",
            "errors": errors,
            "warnings": warnings,
        },
    }


def validate_frozen_sample_records(manifest: Mapping[str, Any]) -> None:
    row_sets: dict[str, set[int]] = {}
    for label, key in ROW_SAMPLE_KEYS.items():
        record = manifest["row_samples"][label]
        if record.get("key") != key:
            raise ValueError(f"row sample {label} key drift")
        if sha256_int64(record["item_ids_sorted"]) != record["item_ids_sha256_int64_le"]:
            raise ValueError(f"row sample {label} item hash mismatch")
        if sha256_int64(record["row_positions_for_sorted_item_ids"]) != record[
            "row_positions_sha256_int64_le"
        ]:
            raise ValueError(f"row sample {label} position hash mismatch")
        if len(record["item_ids_sorted"]) != SAMPLE_N:
            raise ValueError(f"row sample {label} count drift")
        row_sets[label] = {int(value) for value in record["item_ids_sorted"]}
    if row_sets["A"] & row_sets["B"]:
        raise ValueError("row samples A/B overlap")
    coordinate_sets: dict[str, set[int]] = {}
    for label, key in COORD_SAMPLE_KEYS.items():
        record = manifest["coordinate_samples"][label]
        if record.get("key") != key:
            raise ValueError(f"coordinate sample {label} key drift")
        if sha256_int64(record["item_ids_sorted"]) != record["item_ids_sha256_int64_le"]:
            raise ValueError(f"coordinate sample {label} item hash mismatch")
        if sha256_int64(record["row_positions_for_sorted_item_ids"]) != record[
            "row_positions_sha256_int64_le"
        ]:
            raise ValueError(f"coordinate sample {label} position hash mismatch")
        if len(record["item_ids_sorted"]) != COORD_SAMPLE_N:
            raise ValueError(f"coordinate sample {label} count drift")
        coordinate_sets[label] = {int(value) for value in record["item_ids_sorted"]}
    if coordinate_sets["A"] & coordinate_sets["B"]:
        raise ValueError("coordinate samples A/B overlap")


def load_frozen_manifest(path: Path) -> dict[str, Any]:
    path = repo_path(path)
    manifest = load_json(path)
    if manifest.get("schema_version") != SCHEMA_VERSION or manifest.get("stage") != "manifest":
        raise ValueError(f"{path} is not a {SCHEMA_VERSION} manifest")
    if not (manifest.get("integrity") or {}).get("geometry_sources_ready"):
        raise ValueError(f"{path} has manifest integrity errors")
    script = repo_path(Path(__file__).resolve())
    if manifest.get("audit_script", {}).get("sha256") != sha256_file(script):
        raise ValueError("audit script changed after manifest freeze")
    record_path = repo_path(str(manifest.get("owning_e_record", {}).get("path", "")))
    if not record_path.exists() or manifest.get("owning_e_record", {}).get("sha256") != sha256_file(
        record_path
    ):
        raise ValueError("E026 design record changed after manifest freeze")
    if manifest.get("design_lock", {}).get("margins") != MARGINS:
        raise ValueError("manifest-frozen margins differ from code")
    expected_chunks = {
        "row_chunk": ROW_CHUNK,
        "static_batch_size": STATIC_BATCH_SIZE,
        "target_coordinate_chunk": NUISANCE_TARGET_CHUNK,
    }
    if manifest.get("design_lock", {}).get("execution_chunks") != expected_chunks:
        raise ValueError("manifest-frozen execution chunks differ from code")
    if manifest.get("design_lock", {}).get("derived_scratch_reuse") is not False:
        raise ValueError("manifest does not forbid mutable derived-scratch reuse")
    execution_device = str(manifest.get("design_lock", {}).get("execution_device", ""))
    if execution_device not in {"cpu", "cuda"}:
        raise ValueError("manifest has no valid frozen execution device")
    current_runtime, runtime_errors = inspect_runtime_environment(execution_device)
    if runtime_errors or current_runtime != manifest.get("runtime_environment"):
        raise ValueError(
            f"numerical runtime changed after manifest freeze: {runtime_errors or 'identity mismatch'}"
        )
    selftests = manifest.get("numerical_selftests") or {}
    if selftests.get("pass") is not True:
        raise ValueError("manifest numerical selftests did not pass")
    current_selftests = run_numerical_selftests()
    if current_selftests.get("pass") is not True:
        raise ValueError("current synthetic numerical selftests do not pass")
    validate_frozen_sample_records(manifest)

    # Revalidate every external input rather than trusting paths and mtimes.
    for family, reports in manifest["target_caches"].items():
        for split, report in reports.items():
            cache = repo_path(report["path"])
            if not report.get("sha256"):
                raise ValueError(f"{family}/{split}: full target-cache SHA-256 was not frozen")
            if sha256_file(cache) != report["sha256"]:
                raise ValueError(f"{family}/{split}: target cache changed after manifest freeze")
            sidecar = report.get("sidecar") or {}
            sidecar_path = repo_path(str(sidecar.get("path", "")))
            if not sidecar_path.exists() or sha256_file(sidecar_path) != sidecar.get("sha256"):
                raise ValueError(f"{family}/{split}: target sidecar changed after manifest freeze")
            current_sidecar = load_json(sidecar_path)
            semantic = validate_generator_sidecar(family, split, current_sidecar)
            if semantic.get("status") != "valid":
                raise ValueError(
                    f"{family}/{split}: target generator semantics invalid: "
                    f"{semantic.get('errors')}"
                )
    current_ids = load_npz_member(TARGET_SOURCES["tribe"]["train_cache"], "item_indices")
    expected_row_a = freeze_sample(current_ids, ROW_SAMPLE_KEYS["A"], SAMPLE_N)
    expected_row_b = freeze_sample(
        current_ids,
        ROW_SAMPLE_KEYS["B"],
        SAMPLE_N,
        excluded=expected_row_a["item_ids_sorted"],
    )
    if manifest["row_samples"] != {"A": expected_row_a, "B": expected_row_b}:
        raise ValueError("row samples differ from the deterministic keyed-hash selection")
    coordinate_domain = np.arange(TARGET_D, dtype=np.int64)
    expected_coord_a = freeze_sample(
        coordinate_domain, COORD_SAMPLE_KEYS["A"], COORD_SAMPLE_N
    )
    expected_coord_b = freeze_sample(
        coordinate_domain,
        COORD_SAMPLE_KEYS["B"],
        COORD_SAMPLE_N,
        excluded=expected_coord_a["item_ids_sorted"],
    )
    if manifest["coordinate_samples"] != {"A": expected_coord_a, "B": expected_coord_b}:
        raise ValueError("coordinate samples differ from the deterministic keyed-hash selection")
    for label, record in manifest["row_samples"].items():
        positions = np.asarray(record["row_positions_for_sorted_item_ids"], dtype=np.int64)
        if not np.array_equal(
            current_ids[positions], np.asarray(record["item_ids_sorted"], dtype=np.int64)
        ):
            raise ValueError(f"row sample {label}: frozen item-to-position mapping drifted")
    current_weight_hashes: dict[str, str] = {}
    for report in manifest["runs"].values():
        for source in report.get("sources") or []:
            source_path = repo_path(source["path"])
            if sha256_file(source_path) != source["sha256"]:
                raise ValueError(f"run JSON changed after manifest freeze: {source_path}")
        for row in report.get("rows") or []:
            model_path = repo_path(str(row.get("model_weights", "")))
            model_key = str(model_path)
            if model_path.exists() and model_key not in current_weight_hashes:
                current_weight_hashes[model_key] = sha256_file(model_path)
            if not model_path.exists() or current_weight_hashes.get(model_key) != row.get(
                "model_weights_sha256"
            ):
                raise ValueError(
                    f"model weights changed after manifest freeze: {row.get('family')}/"
                    f"{row.get('seed')}/{row.get('arm')}"
                )
            artifact_path = repo_path(str(row.get("artifact_manifest", "")))
            if not artifact_path.exists() or sha256_file(artifact_path) != row.get(
                "artifact_manifest_sha256"
            ):
                raise ValueError(f"model artifact metadata changed after manifest freeze: {artifact_path}")
    context = manifest.get("context_provenance") or {}
    context_path = repo_path(str(context.get("path", "")))
    if context.get("available") and sha256_file(context_path) != context.get("sha256"):
        raise ValueError("context metadata changed after manifest freeze")
    if context.get("summary_sha256"):
        if not CONTEXT_SUMMARY.exists() or sha256_file(CONTEXT_SUMMARY) != context.get(
            "summary_sha256"
        ):
            raise ValueError("context summary changed after manifest freeze")
    for provenance_key, label in (
        ("nuisance_static_model_provenance", "model"),
        ("nuisance_static_tokenizer_provenance", "tokenizer"),
    ):
        nuisance_source = manifest.get(provenance_key) or {}
        if nuisance_source.get("status") != "valid":
            raise ValueError(f"frozen nuisance static {label} is unavailable")
        for record in nuisance_source.get("files") or []:
            source_file = Path(str(record.get("path", "")))
            if not source_file.exists() or sha256_file(source_file) != record.get("sha256"):
                raise ValueError(
                    f"nuisance static-{label} file changed after manifest freeze: {source_file}"
                )
    e025 = manifest.get("e025_representation_provenance") or {}
    if e025.get("status") == "valid":
        e025_path = repo_path(str(e025.get("path", "")))
        current = inspect_e025_manifest(e025_path)
        if current.get("status") != "valid" or current.get("sha256") != e025.get("sha256"):
            raise ValueError("E025 extraction provenance changed after manifest freeze")
    return manifest


def ensure_target_npy(cache: Path, cache_record: Mapping[str, Any], scratch: Path) -> Path:
    target_info = cache_record["members"]["targets"]
    identity = cache_record.get("sha256") or (
        f"{cache_record['size_bytes']}-{target_info['zip_crc32']}-{cache_record['mtime_ns']}"
    )
    digest = hashlib.sha256(str(identity).encode("utf-8")).hexdigest()[:16]
    destination = scratch / f"{cache.stem}.{digest}.targets.npy"
    metadata_path = destination.with_suffix(destination.suffix + ".source.json")
    # Evidence runs never trust a mutable derived cache. Re-extract from the
    # full-SHA-validated NPZ on every invocation; retaining scratch only helps
    # inspection and cannot alter a retry.
    if DERIVED_SCRATCH_REUSE:
        raise RuntimeError("derived target-cache reuse is forbidden by the E026 design lock")
    scratch.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(scratch).free
    required = int(target_info["file_size"]) + (1 << 30)
    if free < required:
        raise OSError(f"not enough scratch space for {cache}: free={free}, required={required}")
    temp = destination.with_suffix(destination.suffix + ".tmp")
    log(f"extracting {cache}:targets -> {destination}")
    with zipfile.ZipFile(cache) as archive, archive.open(target_info["member"]) as source, temp.open("wb") as sink:
        shutil.copyfileobj(source, sink, length=16 << 20)
        sink.flush()
        os.fsync(sink.fileno())
    os.replace(temp, destination)
    with destination.open("rb") as handle:
        header = npy_header(handle)
    if header["shape"] != target_info["shape"] or header["dtype"] != target_info["dtype"]:
        destination.unlink(missing_ok=True)
        raise ValueError(f"extracted target header mismatch for {cache}")
    derived_sha256 = sha256_file(destination)
    write_json(
        metadata_path,
        {
            "source_cache": str(cache),
            "source_identity": identity,
            "source_targets_member": target_info,
            "derived_npy_sha256_for_audit": derived_sha256,
            "reuse_policy": "forbidden; regenerated from full-SHA-validated NPZ every invocation",
            "created_at_utc": utc_now(),
        },
    )
    return destination


def quantiles(values: np.ndarray, probs: Sequence[float] = (0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1)) -> dict[str, float]:
    arr = np.asarray(values, dtype=np.float64)
    out = np.quantile(arr, probs)
    return {f"q{int(round(100 * p)):02d}": float(v) for p, v in zip(probs, out, strict=True)}


def full_moments(array: np.ndarray, row_chunk: int) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
    n_total, width = array.shape
    count = 0
    mean = np.zeros(width, dtype=np.float64)
    m2 = np.zeros(width, dtype=np.float64)
    row_norms = np.empty(n_total, dtype=np.float64)
    nonfinite = 0
    for start in range(0, n_total, row_chunk):
        stop = min(n_total, start + row_chunk)
        block = np.asarray(array[start:stop], dtype=np.float64)
        finite = np.isfinite(block)
        nonfinite += int(block.size - np.count_nonzero(finite))
        if not finite.all():
            raise ValueError(f"target cache contains {nonfinite} nonfinite values by row {stop}")
        block_n = stop - start
        block_mean = block.mean(axis=0, dtype=np.float64)
        centered = block - block_mean
        block_m2 = np.einsum("ij,ij->j", centered, centered, dtype=np.float64)
        delta = block_mean - mean
        combined = count + block_n
        mean += delta * (block_n / combined)
        m2 += block_m2 + delta * delta * (count * block_n / combined)
        count = combined
        row_norms[start:stop] = np.sqrt(np.einsum("ij,ij->i", block, block, dtype=np.float64))
    # E016 used NumPy's default population SD (ddof=0).  We accumulate in
    # float64 for numerical stability and cast the reconstructed transform to
    # float32 at application time.  Retained E016 denominator extrema are
    # checked separately before this view is allowed to carry evidence.
    std = np.sqrt(m2 / max(1, count))
    near_threshold = max(1e-12, 1e-8 * float(np.median(std)))
    report = {
        "n": count,
        "d": width,
        "nonfinite_count": nonfinite,
        "mean_quantiles": quantiles(mean),
        "std_quantiles": quantiles(std),
        "std_definition": "population SD (ddof=0), matching E016's Y.std(axis=0)",
        "near_constant_threshold": near_threshold,
        "near_constant_count": int(np.count_nonzero(std <= near_threshold)),
        "item_l2_norm_quantiles": quantiles(row_norms),
        "centered_frobenius_sq": float(m2.sum(dtype=np.float64)),
        "trace_covariance": float(m2.sum(dtype=np.float64) / max(1, count - 1)),
    }
    return report, mean, std


def standardization_extrema_validation(
    family: str, std: np.ndarray, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    denominator = std.astype(np.float32) + np.float32(STD_EPS)
    observed = {"std_min": float(denominator.min()), "std_max": float(denominator.max())}
    source_checks: list[dict[str, Any]] = []
    for source in manifest["runs"][family]["sources"]:
        retained = source.get("target_standardization") or {}
        checks = {}
        for field in ("std_min", "std_max"):
            expected = retained.get(field)
            value = observed[field]
            passed = bool(
                expected is not None
                and math.isclose(
                    value,
                    float(expected),
                    rel_tol=STANDARDIZATION_EXTREMA_RTOL,
                    abs_tol=1e-8,
                )
            )
            checks[field] = {
                "reconstructed": value,
                "retained_e016": expected,
                "relative_tolerance": STANDARDIZATION_EXTREMA_RTOL,
                "pass": passed,
            }
        source_checks.append(
            {
                "source_run": source["path"],
                "checks": checks,
                "pass": all(check["pass"] for check in checks.values()),
            }
        )
    passed = bool(source_checks and all(row["pass"] for row in source_checks))
    if not passed:
        raise RuntimeError(f"{family}: reconstructed E016 standardization extrema failed validation")
    return {
        "pass": passed,
        "formula": "(Y - population_mean) / (population_sd + 1e-6)",
        "reconstruction": (
            "float64 streaming population moments, cast to float32 at transform application"
        ),
        "observed_denominator_extrema": observed,
        "source_checks": source_checks,
    }


def choose_device(choice: str) -> str:
    if choice != "auto":
        return choice
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def sample_view(
    array: np.ndarray,
    row_positions: Sequence[int],
    mean: np.ndarray,
    std: np.ndarray,
    view: str,
) -> tuple[np.ndarray, dict[str, Any]]:
    values = np.asarray(array[np.asarray(row_positions, dtype=np.int64)], dtype=np.float32)
    if view == "training_standardized_primary":
        values = (values - mean.astype(np.float32)) / (std.astype(np.float32) + np.float32(STD_EPS))
    elif view == "raw_centered_sensitivity":
        values = values - mean.astype(np.float32)
    else:
        raise ValueError(view)
    pre_center = np.asarray(values, dtype=np.float64)
    global_mean = float(pre_center.mean(dtype=np.float64))
    global_sd = float(pre_center.std(ddof=0, dtype=np.float64))
    # The load-bearing spectrum is a covariance spectrum.  Sample centering is
    # therefore mandatory after applying the frozen full-training transform.
    values = values - values.mean(axis=0, keepdims=True, dtype=np.float64).astype(np.float32)
    return np.ascontiguousarray(values, dtype=np.float32), {
        "mean": global_mean,
        "population_sd": global_sd,
        "sample_column_centered_before_covariance_svd": True,
    }


def entropy_rank_tail_sensitivity(
    singular_values: np.ndarray, frobenius_sq: float, matrix_rank_cap: int
) -> dict[str, Any]:
    """Descriptive tail-allocation sensitivity, deliberately not a certified bound.

    Randomized Ritz values do not provide interval-certified eigenvalues.  Calling
    the old adversarial/uniform allocation a rigorous bound was therefore too
    strong.  This diagnostic is retained for description and excluded from the
    mechanical equivalence conjunction.
    """
    energy = np.square(np.asarray(singular_values, dtype=np.float64))
    p = energy / max(frobenius_sq, np.finfo(np.float64).tiny)
    captured = float(p.sum())
    tail = max(0.0, 1.0 - captured)
    positive = p[p > 0]
    top_entropy = float(-np.sum(positive * np.log(positive)))
    min_tail_entropy = 0.0 if tail == 0 else float(-tail * math.log(tail))
    tail_slots = max(1, matrix_rank_cap - len(p))
    max_tail_entropy = 0.0 if tail == 0 else float(-tail * math.log(tail / tail_slots))
    normalized = p / max(captured, np.finfo(np.float64).tiny)
    normalized = normalized[normalized > 0]
    conditional_entropy = float(-np.sum(normalized * np.log(normalized)))
    return {
        "captured_fraction": captured,
        "tail_fraction": tail,
        "conditional_top512_effective_rank": float(math.exp(conditional_entropy)),
        "concentrated_tail_effective_rank": float(math.exp(top_entropy + min_tail_entropy)),
        "uniform_tail_effective_rank": float(math.exp(top_entropy + max_tail_entropy)),
        "rank_cap_used": int(matrix_rank_cap),
        "load_bearing": False,
        "note": (
            "Tail allocations condition on approximate randomized Ritz values and are not certified "
            "bounds. They are descriptive only and are excluded from equivalence."
        ),
    }


def randomized_svd_geometry(
    x: np.ndarray,
    device: str,
    *,
    top_k: int = SVD_K,
    oversample: int = SVD_OVERSAMPLE,
    power_iterations: int = SVD_POWER_ITERS,
    seed: int = SVD_SEED,
    rank_cap: int | None = None,
    enforce_production_shape: bool = True,
) -> tuple[dict[str, Any], np.ndarray]:
    import torch

    if enforce_production_shape and (x.shape[0] != SAMPLE_N or x.shape[1] != TARGET_D):
        raise ValueError(f"unexpected SVD sample shape {x.shape}")
    if top_k <= 0 or top_k >= min(x.shape):
        raise ValueError(f"top_k={top_k} must lie in [1, min(shape)-1] for shape={x.shape}")
    use_device = torch.device(device)
    if use_device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision("highest")
    torch.use_deterministic_algorithms(True)
    l = min(min(x.shape), top_k + oversample)
    rng = np.random.default_rng(seed)
    omega = rng.standard_normal((x.shape[1], l), dtype=np.float32)
    tx = torch.from_numpy(x).to(use_device)
    tomega = torch.from_numpy(omega).to(use_device)
    with torch.no_grad():
        q, _ = torch.linalg.qr(tx @ tomega, mode="reduced")
        for _ in range(power_iterations):
            z, _ = torch.linalg.qr(tx.T @ q, mode="reduced")
            q, _ = torch.linalg.qr(tx @ z, mode="reduced")
        orth_error = torch.linalg.matrix_norm(q.T @ q - torch.eye(l, device=use_device), ord="fro")
        b = q.T @ tx
        ub, singular, vh = torch.linalg.svd(b, full_matrices=False)
        scores = (q @ ub[:, :top_k]) * singular[:top_k]
        singular_np = singular[:top_k].detach().cpu().numpy().astype(np.float64)
        scores_np = scores.detach().cpu().numpy().astype(np.float32)
        orth = float(orth_error.detach().cpu())
        projected_frobenius_sq = float(
            torch.sum(b.to(dtype=torch.float64) * b.to(dtype=torch.float64)).detach().cpu()
        )
    x64 = x.astype(np.float64)
    frobenius_sq = float(np.einsum("ij,ij->", x64, x64, dtype=np.float64))
    del x64
    cuts = tuple(cut for cut in SVD_MASS_CUTS if cut <= top_k)
    masses = {
        str(cut): float(np.square(singular_np[:cut]).sum(dtype=np.float64) / frobenius_sq)
        for cut in cuts
    }
    captured = float(np.square(singular_np).sum(dtype=np.float64) / frobenius_sq)
    if rank_cap is None:
        rank_cap = min(x.shape) - 1
    tail_sensitivity = entropy_rank_tail_sensitivity(singular_np, frobenius_sq, rank_cap)
    normalized_eigenvalues = np.square(singular_np) / max(
        frobenius_sq, np.finfo(np.float64).tiny
    )
    finite = bool(np.isfinite(singular_np).all() and np.isfinite(scores_np).all())
    monotone = bool(np.all(np.diff(singular_np) <= max(1e-7, singular_np[0] * 1e-6)))
    energy_valid = bool(captured <= 1.0 + SVD_ENERGY_TOL)
    orth_valid = bool(orth <= SVD_ORTHOGONALITY_MAX)
    validation_pass = finite and monotone and energy_valid and orth_valid
    report = {
        "estimator_scope": (
            f"{x.shape[0]}-row fixed sample; randomized top-{top_k}; not full-cache SVD"
        ),
        "seed": seed,
        "top_k": top_k,
        "oversample": oversample,
        "power_iterations": power_iterations,
        "qr_after_each_multiply": True,
        "tf32_disabled": True,
        "device": str(use_device),
        "sample_frobenius_sq_float64": frobenius_sq,
        "projected_subspace_frobenius_sq_float64": projected_frobenius_sq,
        "projection_residual_fraction": max(
            0.0, 1.0 - projected_frobenius_sq / max(frobenius_sq, np.finfo(float).tiny)
        ),
        "q_orthogonality_frobenius_error": orth,
        "validation": {
            "pass": validation_pass,
            "finite": finite,
            "singular_values_nonincreasing": monotone,
            "captured_energy_not_above_one": energy_valid,
            "orthogonality_within_threshold": orth_valid,
            "orthogonality_max": SVD_ORTHOGONALITY_MAX,
            "captured_energy_tolerance": SVD_ENERGY_TOL,
        },
        "singular_values_top512": singular_np.tolist(),
        "normalized_covariance_eigenvalues_top512": normalized_eigenvalues.tolist(),
        "leading_singular_values": singular_np[:32].tolist(),
        "sigma_512": float(singular_np[-1]),
        "sample_stable_rank": float(frobenius_sq / max(singular_np[0] ** 2, np.finfo(float).tiny)),
        "variance_mass": masses,
        "entropy_rank_tail_allocation_sensitivity": tail_sensitivity,
    }
    del tx, tomega, q, b, ub, singular, vh, scores
    if use_device.type == "cuda":
        torch.cuda.empty_cache()
    if not validation_pass:
        raise RuntimeError(f"randomized SVD validation failed: {report['validation']}")
    return report, scores_np


def descriptive_2nn(scores: np.ndarray) -> dict[str, Any]:
    from scipy.stats import chi2
    from sklearn.neighbors import NearestNeighbors

    output: dict[str, Any] = {
        "status": "descriptive_only",
        "assumption": "local homogeneous-Poisson approximation; rows are not independent population replicates",
        "ranks": {},
    }
    for rank in ID_RANKS:
        x = np.ascontiguousarray(scores[:, :rank], dtype=np.float32)
        nn = NearestNeighbors(n_neighbors=4, algorithm="brute", metric="euclidean", n_jobs=-1)
        distances, neighbor_indices = nn.fit(x).kneighbors(x, return_distance=True)
        scale = float(np.median(distances[:, -1]))
        tol = max(np.finfo(np.float32).eps * max(scale, 1.0) * 16, 1e-12)
        first = np.full(len(x), np.nan, dtype=np.float64)
        second = np.full(len(x), np.nan, dtype=np.float64)
        duplicate_flags = np.zeros(len(x), dtype=bool)
        exact_duplicate_flags = np.zeros(len(x), dtype=bool)
        for i, (row, indices) in enumerate(zip(distances, neighbor_indices, strict=True)):
            # Remove the query row by identity, not by assuming the first zero
            # distance is self. Exact duplicate observations can otherwise be
            # silently discarded as if they were the self-neighbor.
            self_matches = np.flatnonzero(indices == i)
            if len(self_matches) > 1:
                duplicate_flags[i] = True
                continue
            nonself = row[indices != i]
            if np.any(nonself <= tol):
                duplicate_flags[i] = True
                exact_duplicate_flags[i] = True
            elif len(self_matches) == 0:
                # A nonduplicate query must be its own unique closest neighbor.
                duplicate_flags[i] = True
                continue
            positive = nonself[nonself > tol]
            if len(positive) < 2:
                duplicate_flags[i] = True
                continue
            first[i], second[i] = float(positive[0]), float(positive[1])
        valid = (
            ~duplicate_flags
            & np.isfinite(first)
            & np.isfinite(second)
            & (second >= first)
            & (first > 0)
        )
        logs = np.log(second[valid] / first[valid])
        logs = logs[np.isfinite(logs) & (logs > 0)]
        rec: dict[str, Any] = {
            "embedding_rank": rank,
            "n_rows": len(x),
            "n_valid": int(len(logs)),
            "exact_duplicate_rows": int(np.count_nonzero(exact_duplicate_flags)),
            "duplicate_or_unresolved_rows": int(
                np.count_nonzero(duplicate_flags | ~valid)
            ),
        }
        if len(logs) < 10 or float(logs.sum()) <= 0:
            rec.update({"status": "unresolved", "reason": "insufficient positive 2NN log-ratios"})
        else:
            estimate = float((len(logs) - 1) / logs.sum())
            lower = float(chi2.ppf(0.025, 2 * len(logs)) / (2 * logs.sum()))
            upper = float(chi2.ppf(0.975, 2 * len(logs)) / (2 * logs.sum()))
            censor_at = rank / 2
            if estimate > censor_at:
                rec.update(
                    {
                        "status": "right_censored",
                        "right_censored_lower_bound": censor_at,
                        "unclipped_model_estimate": estimate,
                        "model_interval_unclipped": [lower, upper],
                    }
                )
            else:
                rec.update(
                    {
                        "status": "estimated_descriptive",
                        "estimate": estimate,
                        "model_interval": [lower, upper],
                    }
                )
        output["ranks"][str(rank)] = rec
    return output


def load_context_segments(item_ids: Sequence[int], expected_texts: Sequence[str]) -> tuple[list[tuple[int, int]], dict[str, Any]]:
    if not CONTEXT_META.exists():
        return [], {"status": "unavailable", "reason": f"missing {CONTEXT_META}"}
    wanted = {int(item): pos for pos, item in enumerate(item_ids)}
    records: list[dict[str, Any] | None] = [None] * len(item_ids)
    duplicate_split_indices: list[int] = []
    with CONTEXT_META.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            item = int(row["split_index"])
            pos = wanted.get(item)
            if pos is not None:
                if records[pos] is not None:
                    duplicate_split_indices.append(item)
                records[pos] = row
    if duplicate_split_indices:
        return [], {
            "status": "invalid",
            "reason": f"duplicate context split indices: {duplicate_split_indices[:10]}",
        }
    missing = [i for i, row in enumerate(records) if row is None]
    if missing:
        return [], {"status": "invalid", "reason": f"context metadata missing {len(missing)} cache rows"}
    text_mismatches = sum(
        str(records[i]["text"]) != str(expected_texts[i])  # type: ignore[index]
        for i in range(len(records))
    )
    if text_mismatches:
        return [], {"status": "invalid", "reason": f"{text_mismatches} context/cache text mismatches"}
    invalid_split = sum(str(row.get("split")) != "train" for row in records if row is not None)
    if invalid_split:
        return [], {"status": "invalid", "reason": f"{invalid_split} non-train context records"}
    segments: list[tuple[int, int]] = []
    start = 0
    for pos in range(1, len(records)):
        prior = records[pos - 1]
        current = records[pos]
        contiguous = (
            prior is not None
            and current is not None
            and current.get("doc_title") == prior.get("doc_title")
            and int(current["split_index"]) == int(prior["split_index"]) + 1
            and current.get("previous_same_doc_global_index") == prior.get("global_accepted_index")
        )
        if not contiguous:
            segments.append((start, pos))
            start = pos
    segments.append((start, len(records)))
    lengths = np.asarray([end - begin for begin, end in segments], dtype=np.int64)
    usable_for_power = int(np.count_nonzero(lengths >= 4))
    return segments, {
        "status": "valid",
        "n_segments": len(segments),
        "length_quantiles": quantiles(lengths),
        "text_mismatches": 0,
        "cross_boundary_pairs_excluded": True,
        "boundary_rule": (
            "same doc_title, consecutive split_index, and explicit previous_same_doc_global_index "
            "link to prior global_accepted_index"
        ),
        "segments_length_ge_4": usable_for_power,
    }


def transform_block(block: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (np.asarray(block, dtype=np.float64) - mean) / (std + STD_EPS)


def trace_autocorrelation(
    array: np.ndarray,
    mean: np.ndarray,
    std: np.ndarray,
    segments: Sequence[tuple[int, int]],
    row_chunk: int,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for lag in ORDER_LAGS:
        numerator = np.float64(0.0)
        left_energy = np.float64(0.0)
        right_energy = np.float64(0.0)
        pair_rows = 0
        for begin, end in segments:
            pair_end = end - lag
            if pair_end <= begin:
                continue
            for start in range(begin, pair_end, row_chunk):
                stop = min(pair_end, start + row_chunk)
                left = transform_block(array[start:stop], mean, std)
                right = transform_block(array[start + lag : stop + lag], mean, std)
                numerator += np.einsum("ij,ij->", left, right, dtype=np.float64)
                left_energy += np.einsum("ij,ij->", left, left, dtype=np.float64)
                right_energy += np.einsum("ij,ij->", right, right, dtype=np.float64)
                pair_rows += stop - start
        denominator = math.sqrt(float(left_energy * right_energy))
        result[str(lag)] = {
            "rho_trace": float(numerator / denominator) if denominator > 0 else None,
            "valid_pair_rows": pair_rows,
        }
    return result


def coordinate_order_diagnostics(
    array: np.ndarray,
    mean: np.ndarray,
    std: np.ndarray,
    coordinates: Sequence[int],
    segments: Sequence[tuple[int, int]],
    row_chunk: int,
) -> dict[str, Any]:
    from scipy.signal import welch

    coords = np.asarray(coordinates, dtype=np.int64)
    values = np.empty((array.shape[0], len(coords)), dtype=np.float32)
    for start in range(0, array.shape[0], row_chunk):
        stop = min(array.shape[0], start + row_chunk)
        raw = np.asarray(array[start:stop][:, coords], dtype=np.float64)
        values[start:stop] = ((raw - mean[coords]) / (std[coords] + STD_EPS)).astype(np.float32)
    lag_records: dict[str, Any] = {}
    for lag in ORDER_LAGS:
        num = np.zeros(len(coords), dtype=np.float64)
        le = np.zeros(len(coords), dtype=np.float64)
        re = np.zeros(len(coords), dtype=np.float64)
        pairs = 0
        for begin, end in segments:
            if end - begin <= lag:
                continue
            left = values[begin : end - lag].astype(np.float64)
            right = values[begin + lag : end].astype(np.float64)
            num += np.einsum("ij,ij->j", left, right, dtype=np.float64)
            le += np.einsum("ij,ij->j", left, left, dtype=np.float64)
            re += np.einsum("ij,ij->j", right, right, dtype=np.float64)
            pairs += len(left)
        denom = np.sqrt(le * re)
        valid = denom > 0
        rho = np.full(len(coords), np.nan, dtype=np.float64)
        rho[valid] = num[valid] / denom[valid]
        lag_records[str(lag)] = {
            "valid_pair_rows": pairs,
            "feature_rho_quantiles": quantiles(rho[np.isfinite(rho)]) if np.any(np.isfinite(rho)) else {},
        }
    nfft = 128
    power = np.zeros(nfft // 2 + 1, dtype=np.float64)
    weight_total = 0.0
    covered_rows = 0
    for begin, end in segments:
        length = end - begin
        if length < 4:
            continue
        nperseg = min(64, length)
        noverlap = nperseg // 2
        frequency, segment_power = welch(
            values[begin:end].astype(np.float64),
            fs=1.0,
            window="hann",
            nperseg=nperseg,
            noverlap=noverlap,
            nfft=nfft,
            detrend="constant",
            return_onesided=True,
            scaling="spectrum",
            axis=0,
        )
        windows = max(1, 1 + (length - nperseg) // max(1, nperseg - noverlap))
        power += segment_power.sum(axis=1, dtype=np.float64) * windows
        weight_total += len(coords) * windows
        covered_rows += length
    if covered_rows == 0:
        return {
            "status": "unresolved",
            "reason": "no recovered within-document segment has at least four rows",
            "coordinate_count": len(coords),
            "lags": lag_records,
        }
    normalized = power / power.sum() if power.sum() > 0 else power
    positive = normalized[normalized > 0]
    spectral_entropy = float(-np.sum(positive * np.log(positive))) if len(positive) else None
    bands = ((0.0, 1 / 64), (1 / 64, 1 / 16), (1 / 16, 1 / 4), (1 / 4, 0.5000001))
    band_mass = {
        f"[{lo:.8g},{hi:.8g})": float(normalized[(frequency >= lo) & (frequency < hi)].sum())
        for lo, hi in bands
    }
    return {
        "coordinate_count": len(coords),
        "lags": lag_records,
        "welch_trace_power": {
            "scope": "all canonical rows within documents; fixed coordinate sample only",
            "nfft": nfft,
            "frequency": frequency.tolist(),
            "normalized_power": normalized.tolist(),
            "spectral_entropy": spectral_entropy,
            "fixed_band_mass": band_mass,
            "weight_total": weight_total,
            "rows_in_segments_length_ge_4": covered_rows,
        },
    }


def jensen_shannon(p: Sequence[float], q: Sequence[float]) -> float | None:
    left = np.asarray(p, dtype=np.float64)
    right = np.asarray(q, dtype=np.float64)
    if left.shape != right.shape or left.sum() <= 0 or right.sum() <= 0:
        return None
    left /= left.sum()
    right /= right.sum()
    middle = 0.5 * (left + right)
    kl_left = np.sum(np.where(left > 0, left * np.log(left / np.maximum(middle, 1e-300)), 0))
    kl_right = np.sum(np.where(right > 0, right * np.log(right / np.maximum(middle, 1e-300)), 0))
    return float(0.5 * (kl_left + kl_right))


def margin_check(
    name: str,
    value: Any,
    margin: Any,
    passed: bool | None,
    *,
    reason: str | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "state": "UNRESOLVED" if passed is None else ("PASS" if passed else "FAIL"),
        "value": value,
        "margin": margin,
        "reason": reason,
    }


def mechanical_conjunction(checks: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    states = [str(check.get("state")) for check in checks]
    if "FAIL" in states:
        state = "FAIL"
    elif states and all(value == "PASS" for value in states):
        state = "PASS"
    else:
        state = "UNRESOLVED"
    return {
        "state": state,
        "n_checks": len(states),
        "pass_count": states.count("PASS"),
        "fail_count": states.count("FAIL"),
        "unresolved_count": states.count("UNRESOLVED"),
        "boundary": (
            "Mechanical three-state conjunction over frozen engineering margins; this is not a "
            "scientific verdict or claim of information equivalence."
        ),
    }


def _hash_embedding_weight(weight: Any) -> str:
    array = weight.detach().cpu().numpy()
    return sha256_array(array)


def extract_static_embedding_features(
    split_texts: Mapping[str, Sequence[str]],
    scratch: Path,
    device: str,
    batch_size: int,
    model_snapshot: Path,
    tokenizer_snapshot: Path,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], dict[str, Any], list[Path]]:
    """Extract frozen GPT-2-medium mean input embeddings for nuisance analysis."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_snapshot, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_snapshot, local_files_only=True)
    embedding = model.get_input_embeddings()
    if len(tokenizer) != int(embedding.weight.shape[0]):
        raise ValueError(
            f"tokenizer/model vocabulary mismatch: {len(tokenizer)} != {embedding.weight.shape[0]}"
        )
    weight_sha = _hash_embedding_weight(embedding.weight)
    embedding = embedding.to(device)
    width = int(embedding.weight.shape[1])
    scratch.mkdir(parents=True, exist_ok=True)
    features: dict[str, np.ndarray] = {}
    lengths: dict[str, np.ndarray] = {}
    derived: list[Path] = []
    split_reports: dict[str, Any] = {}
    for split, texts in split_texts.items():
        text_hash = sha256_strings([str(value) for value in texts])
        identity = hashlib.sha256(
            (
                f"{model_snapshot}|{tokenizer_snapshot}|{weight_sha}|"
                f"{text_hash}|{NUISANCE_MAX_LENGTH}"
            ).encode("utf-8")
        ).hexdigest()[:16]
        feature_path = scratch / f"nuisance_static_{split}.{identity}.npy"
        length_path = scratch / f"nuisance_lengths_{split}.{identity}.npy"
        meta_path = scratch / f"nuisance_static_{split}.{identity}.json"
        expected_meta = {
            "model": NUISANCE_MODEL,
            "snapshot_path": str(model_snapshot),
            "tokenizer": NUISANCE_TOKENIZER,
            "tokenizer_snapshot_path": str(tokenizer_snapshot),
            "embedding_weight_sha256": weight_sha,
            "ordered_text_sha256_len_prefixed_utf8": text_hash,
            "max_length": NUISANCE_MAX_LENGTH,
            "n": len(texts),
            "d": width,
            "pooling": "attention-mask mean of frozen input-token embeddings",
        }
        if DERIVED_SCRATCH_REUSE:
            raise RuntimeError("derived nuisance-cache reuse is forbidden by the E026 design lock")
        feature_mm = np.lib.format.open_memmap(
            feature_path, mode="w+", dtype=np.float32, shape=(len(texts), width)
        )
        length_mm = np.lib.format.open_memmap(
            length_path, mode="w+", dtype=np.int32, shape=(len(texts),)
        )
        with torch.inference_mode():
            for start in range(0, len(texts), batch_size):
                batch = [str(value) for value in texts[start : start + batch_size]]
                encoded = tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=NUISANCE_MAX_LENGTH,
                    return_tensors="pt",
                )
                ids = encoded["input_ids"].to(device)
                mask = encoded["attention_mask"].to(device)
                token_embeddings = embedding(ids)
                denom = mask.sum(dim=1, keepdim=True).clamp_min(1)
                pooled = (token_embeddings * mask.unsqueeze(-1)).sum(dim=1) / denom
                stop = start + len(batch)
                feature_mm[start:stop] = pooled.detach().cpu().float().numpy()
                length_mm[start:stop] = mask.sum(dim=1).detach().cpu().numpy().astype(np.int32)
        feature_mm.flush()
        length_mm.flush()
        del feature_mm, length_mm
        feature_sha256 = sha256_file(feature_path)
        length_sha256 = sha256_file(length_path)
        write_json(
            meta_path,
            {
                **expected_meta,
                "feature_npy_sha256_for_audit": feature_sha256,
                "length_npy_sha256_for_audit": length_sha256,
                "reuse_policy": "forbidden; regenerated from frozen model/text every invocation",
                "created_at_utc": utc_now(),
            },
        )
        feature_array = np.load(feature_path, mmap_mode="r", allow_pickle=False)
        length_array = np.load(length_path, mmap_mode="r", allow_pickle=False)
        features[split] = feature_array
        lengths[split] = length_array
        derived.extend((feature_path, length_path, meta_path))
        split_reports[split] = {
            **expected_meta,
            "feature_path": str(feature_path),
            "length_path": str(length_path),
            "feature_npy_sha256_for_audit": feature_sha256,
            "length_npy_sha256_for_audit": length_sha256,
            "reused": False,
            "reuse_policy": "forbidden",
        }
    del model, embedding
    if str(device).startswith("cuda"):
        torch.cuda.empty_cache()
    return features, lengths, {
        "model": NUISANCE_MODEL,
        "snapshot_path": str(model_snapshot),
        "tokenizer": NUISANCE_TOKENIZER,
        "tokenizer_snapshot_path": str(tokenizer_snapshot),
        "tokenizer_class": type(tokenizer).__name__,
        "tokenizer_vocab_size": len(tokenizer),
        "embedding_weight_sha256": weight_sha,
        "splits": split_reports,
    }, derived


def low_level_nuisance_design(lengths: np.ndarray) -> np.ndarray:
    n = len(lengths)
    if n < 2:
        raise ValueError("nuisance design requires at least two rows")
    position = np.linspace(-1.0, 1.0, n, dtype=np.float64)
    block = np.minimum(
        NUISANCE_POSITION_BLOCKS - 1,
        (np.arange(n, dtype=np.int64) * NUISANCE_POSITION_BLOCKS) // n,
    )
    one_hot = np.eye(NUISANCE_POSITION_BLOCKS, dtype=np.float64)[block, :-1]
    return np.column_stack((np.asarray(lengths, dtype=np.float64), position, one_hot))


def fit_scale(train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = train.mean(axis=0, dtype=np.float64)
    std = train.std(axis=0, ddof=0, dtype=np.float64)
    std = np.where(std > 1e-12, std, 1.0)
    return (train - mean) / std, (test - mean) / std


def ridge_sse_sst(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    alpha: float,
    target_chunk: int | None = None,
) -> tuple[float, float]:
    xtr = np.asarray(x_train, dtype=np.float64)
    xte = np.asarray(x_test, dtype=np.float64)
    ytr = np.asarray(y_train, dtype=np.float64)
    yte = np.asarray(y_test, dtype=np.float64)
    if target_chunk is not None and ytr.shape[1] > target_chunk:
        sse_total = 0.0
        sst_total = 0.0
        for start in range(0, ytr.shape[1], target_chunk):
            sse, sst = ridge_sse_sst(
                xtr,
                ytr[:, start : start + target_chunk],
                xte,
                yte[:, start : start + target_chunk],
                alpha,
                target_chunk=None,
            )
            sse_total += sse
            sst_total += sst
        return sse_total, sst_total
    x_mean = xtr.mean(axis=0, keepdims=True)
    y_mean = ytr.mean(axis=0, keepdims=True)
    xc = xtr - x_mean
    yc = ytr - y_mean
    gram = xc.T @ xc
    gram.flat[:: len(gram) + 1] += float(alpha)
    weights = np.linalg.solve(gram, xc.T @ yc)
    prediction = (xte - x_mean) @ weights + y_mean
    residual = yte - prediction
    centered = yte - yte.mean(axis=0, keepdims=True)
    sse = float(np.einsum("ij,ij->", residual, residual, dtype=np.float64))
    sst = float(np.einsum("ij,ij->", centered, centered, dtype=np.float64))
    return sse, sst


def standardized_coordinate_targets(
    array: np.ndarray,
    coordinates: Sequence[int],
    mean: np.ndarray,
    std: np.ndarray,
) -> np.ndarray:
    coords = np.asarray(coordinates, dtype=np.int64)
    raw = np.asarray(array[:, coords], dtype=np.float32)
    return np.ascontiguousarray(
        (raw - mean[coords].astype(np.float32))
        / (std[coords].astype(np.float32) + np.float32(STD_EPS)),
        dtype=np.float32,
    )


def nuisance_target_predictability(
    train_arrays: Mapping[str, np.ndarray],
    heldout_arrays: Mapping[str, np.ndarray],
    moments: Mapping[str, tuple[np.ndarray, np.ndarray]],
    split_texts: Mapping[str, Sequence[str]],
    manifest: Mapping[str, Any],
    scratch: Path,
    device: str,
    batch_size: int,
    target_chunk: int,
) -> tuple[dict[str, Any], list[Path]]:
    """Held-out, variance-weighted target R2 under a frozen nuisance protocol."""
    from sklearn.decomposition import PCA

    static, token_lengths, provenance, derived = extract_static_embedding_features(
        split_texts,
        scratch,
        device,
        batch_size,
        Path(str(manifest["nuisance_static_model_provenance"]["snapshot_path"])),
        Path(str(manifest["nuisance_static_tokenizer_provenance"]["snapshot_path"])),
    )
    low_train = low_level_nuisance_design(token_lengths["train"])
    low_heldout = low_level_nuisance_design(token_lengths["heldout"])
    tasks: dict[tuple[str, str], tuple[np.ndarray, np.ndarray]] = {}
    for family in ("tribe", "textfeat"):
        mean, std = moments[family]
        for sample, frozen in manifest["coordinate_samples"].items():
            coords = frozen["item_ids_sorted"]
            tasks[(family, sample)] = (
                standardized_coordinate_targets(train_arrays[family], coords, mean, std),
                standardized_coordinate_targets(heldout_arrays[family], coords, mean, std),
            )

    alpha_totals = {float(alpha): {"sse": 0.0, "sst": 0.0} for alpha in NUISANCE_RIDGE_ALPHAS}
    fold_records: list[dict[str, Any]] = []
    n = len(low_train)
    bounds = np.linspace(0, n, NUISANCE_INNER_FOLDS + 1, dtype=int)
    all_indices = np.arange(n, dtype=np.int64)
    for fold in range(NUISANCE_INNER_FOLDS):
        begin, end = int(bounds[fold]), int(bounds[fold + 1])
        validation = np.arange(begin, end, dtype=np.int64)
        training = np.concatenate((all_indices[:begin], all_indices[end:]))
        pca = PCA(
            n_components=NUISANCE_PCA_RANK,
            svd_solver="randomized",
            random_state=SVD_SEED + fold,
        )
        static_train = pca.fit_transform(np.asarray(static["train"][training], dtype=np.float32))
        static_validation = pca.transform(np.asarray(static["train"][validation], dtype=np.float32))
        low_tr, low_va = fit_scale(low_train[training], low_train[validation])
        full_tr, full_va = fit_scale(
            np.column_stack((low_train[training], static_train)),
            np.column_stack((low_train[validation], static_validation)),
        )
        fold_alpha = {float(alpha): {"sse": 0.0, "sst": 0.0} for alpha in NUISANCE_RIDGE_ALPHAS}
        # Alpha selection uses only the static-augmented tier, aggregated over
        # both target families and both frozen coordinate samples.
        for y_train, _ in tasks.values():
            ytr = y_train[training]
            yva = y_train[validation]
            for alpha in NUISANCE_RIDGE_ALPHAS:
                sse, sst = ridge_sse_sst(
                    full_tr, ytr, full_va, yva, alpha, target_chunk=target_chunk
                )
                fold_alpha[float(alpha)]["sse"] += sse
                fold_alpha[float(alpha)]["sst"] += sst
                alpha_totals[float(alpha)]["sse"] += sse
                alpha_totals[float(alpha)]["sst"] += sst
        fold_records.append(
            {
                "fold": fold,
                "validation_slice": [begin, end],
                "alpha_aggregate_r2": {
                    str(alpha): 1.0 - values["sse"] / max(values["sst"], 1e-12)
                    for alpha, values in fold_alpha.items()
                },
            }
        )
    alpha_scores = {
        alpha: 1.0 - values["sse"] / max(values["sst"], 1e-12)
        for alpha, values in alpha_totals.items()
    }
    selected_alpha = max(sorted(alpha_scores), key=lambda alpha: alpha_scores[alpha])

    pca = PCA(
        n_components=NUISANCE_PCA_RANK,
        svd_solver="randomized",
        random_state=SVD_SEED,
    )
    static_train_full = pca.fit_transform(np.asarray(static["train"], dtype=np.float32))
    static_heldout = pca.transform(np.asarray(static["heldout"], dtype=np.float32))
    low_tr, low_te = fit_scale(low_train, low_heldout)
    full_tr, full_te = fit_scale(
        np.column_stack((low_train, static_train_full)),
        np.column_stack((low_heldout, static_heldout)),
    )
    records: dict[str, Any] = {family: {} for family in ("tribe", "textfeat")}
    for (family, sample), (y_train, y_heldout) in tasks.items():
        low_sse, low_sst = ridge_sse_sst(
            low_tr, y_train, low_te, y_heldout, selected_alpha, target_chunk=target_chunk
        )
        full_sse, full_sst = ridge_sse_sst(
            full_tr, y_train, full_te, y_heldout, selected_alpha, target_chunk=target_chunk
        )
        if abs(low_sst - full_sst) > max(1e-8, 1e-10 * low_sst):
            raise ValueError("nuisance tiers produced inconsistent held-out target SST")
        low_r2 = 1.0 - low_sse / max(low_sst, 1e-12)
        full_r2 = 1.0 - full_sse / max(full_sst, 1e-12)
        records[family][sample] = {
            "coordinate_count": len(manifest["coordinate_samples"][sample]["item_ids_sorted"]),
            "low_level_only_variance_weighted_r2": low_r2,
            "static_augmented_variance_weighted_r2": full_r2,
            "static_unique_delta_r2": full_r2 - low_r2,
            "heldout_sst": low_sst,
        }
    checks: list[dict[str, Any]] = []
    comparisons: dict[str, Any] = {}
    for sample in ("A", "B"):
        left = records["tribe"][sample]
        right = records["textfeat"][sample]
        low_diff = abs(
            left["low_level_only_variance_weighted_r2"]
            - right["low_level_only_variance_weighted_r2"]
        )
        unique_diff = abs(left["static_unique_delta_r2"] - right["static_unique_delta_r2"])
        sample_checks = [
            margin_check(
                f"{sample}:low_level_target_r2",
                low_diff,
                MARGINS["low_level_target_r2_abs_difference"],
                low_diff <= MARGINS["low_level_target_r2_abs_difference"],
            ),
            margin_check(
                f"{sample}:static_unique_target_r2",
                unique_diff,
                MARGINS["static_unique_target_r2_abs_difference"],
                unique_diff <= MARGINS["static_unique_target_r2_abs_difference"],
            ),
        ]
        checks.extend(sample_checks)
        comparisons[sample] = {"checks": sample_checks}
    return {
        "protocol": {
            "static_model": NUISANCE_MODEL,
            "static_pooling": "attention-mask mean input embeddings",
            "max_length": NUISANCE_MAX_LENGTH,
            "low_level_columns": (
                "token length, normalized corpus position, and nine reference-coded contiguous-decile indicators"
            ),
            "static_pca_rank": NUISANCE_PCA_RANK,
            "inner_folds": NUISANCE_INNER_FOLDS,
            "inner_split": "five contiguous validation blocks; every transform fit on complement only",
            "ridge_alphas": list(NUISANCE_RIDGE_ALPHAS),
            "alpha_selection": (
                "single alpha maximizing aggregate static-augmented validation R2 over both families "
                "and both frozen coordinate samples"
            ),
            "target_transform": (
                "historically frozen E016 full-training population standardization; ridge intercept "
                "and every predictor transform fit on the current training side only"
            ),
            "aggregation": "variance-weighted aggregate SSE/SST; target coordinates are not replicates",
            "target_coordinate_chunk": target_chunk,
        },
        "static_feature_provenance": provenance,
        "selected_alpha": selected_alpha,
        "inner_alpha_aggregate_r2": {str(key): value for key, value in alpha_scores.items()},
        "inner_fold_records": fold_records,
        "heldout_records": records,
        "comparisons": comparisons,
        "checks": checks,
        "mechanical_conjunction": mechanical_conjunction(checks),
    }, derived


def geometry_comparison(
    families: Mapping[str, Any], nuisance: Mapping[str, Any]
) -> dict[str, Any]:
    output: dict[str, Any] = {
        "scope": (
            "mechanical component checks against manifest-frozen engineering margins; no scientific "
            "verdict or information-equivalence claim is computed"
        ),
        "samples": {},
        "order": {},
        "checks": [],
    }
    for sample in ("A", "B"):
        left_record = families["tribe"]["samples"][sample]["training_standardized_primary"]
        right_record = families["textfeat"]["samples"][sample]["training_standardized_primary"]
        left = left_record["svd"]
        right = right_record["svd"]
        ls = np.asarray(left["normalized_covariance_eigenvalues_top512"], dtype=np.float64)
        rs = np.asarray(right["normalized_covariance_eigenvalues_top512"], dtype=np.float64)
        valid = (ls > ls[0] * 1e-8) & (rs > rs[0] * 1e-8)
        log_rms = (
            float(np.sqrt(np.mean(np.square(np.log(ls[valid]) - np.log(rs[valid])))))
            if valid.any()
            else None
        )
        stable_log = float(math.log(left["sample_stable_rank"] / right["sample_stable_rank"]))
        mean_diff = abs(
            float(left_record["pre_center_global_moments"]["mean"])
            - float(right_record["pre_center_global_moments"]["mean"])
        )
        left_sd = float(left_record["pre_center_global_moments"]["population_sd"])
        right_sd = float(right_record["pre_center_global_moments"]["population_sd"])
        sd_ratio = left_sd / right_sd if right_sd > 0 else None
        mass_differences = {
            cut: abs(left["variance_mass"][cut] - right["variance_mass"][cut])
            for cut in left["variance_mass"]
        }
        checks = [
            margin_check(
                f"{sample}:standardized_global_mean",
                mean_diff,
                MARGINS["sample_global_mean_abs_difference"],
                mean_diff <= MARGINS["sample_global_mean_abs_difference"],
            ),
            margin_check(
                f"{sample}:standardized_global_sd_ratio",
                sd_ratio,
                MARGINS["sample_global_sd_ratio"],
                (
                    MARGINS["sample_global_sd_ratio"][0]
                    <= sd_ratio
                    <= MARGINS["sample_global_sd_ratio"][1]
                )
                if sd_ratio is not None
                else None,
                reason="zero text-feature sample SD" if sd_ratio is None else None,
            ),
            margin_check(
                f"{sample}:normalized_covariance_spectrum",
                log_rms,
                MARGINS["normalized_covariance_log_eigen_rms"],
                log_rms <= MARGINS["normalized_covariance_log_eigen_rms"]
                if log_rms is not None
                else None,
                reason="no common eigenvalues above floor" if log_rms is None else None,
            ),
            margin_check(
                f"{sample}:sample_stable_rank",
                abs(stable_log),
                MARGINS["sample_stable_rank_abs_log_ratio"],
                abs(stable_log) <= MARGINS["sample_stable_rank_abs_log_ratio"],
            ),
        ]
        for cut, difference in mass_differences.items():
            checks.append(
                margin_check(
                    f"{sample}:variance_mass@{cut}",
                    difference,
                    MARGINS["variance_mass_abs_difference"],
                    difference <= MARGINS["variance_mass_abs_difference"],
                )
            )
        output["checks"].extend(checks)
        output["samples"][sample] = {
            "top512_normalized_covariance_log_eigen_rms_difference": log_rms,
            "top512_values_excluded_below_1e-8_leading": int(len(ls) - np.count_nonzero(valid)),
            "sample_stable_rank_log_ratio": stable_log,
            "standardized_global_mean_absolute_difference": mean_diff,
            "standardized_global_sd_ratio": sd_ratio,
            "variance_mass_absolute_differences": mass_differences,
            "checks": checks,
            "note": (
                "Paired fixed-sample, sample-centered, trace-normalized top-512 covariance diagnostic; "
                "it is not a full-cache covariance spectrum."
            ),
        }
    if all("coordinate_samples" in families[name]["order"] for name in ("tribe", "textfeat")):
        trace_checks: list[dict[str, Any]] = []
        for lag in map(str, ORDER_LAGS):
            left_rho = families["tribe"]["order"]["trace_autocorrelation_all_coordinates"][lag][
                "rho_trace"
            ]
            right_rho = families["textfeat"]["order"]["trace_autocorrelation_all_coordinates"][lag][
                "rho_trace"
            ]
            difference = (
                abs(float(left_rho) - float(right_rho))
                if left_rho is not None and right_rho is not None
                else None
            )
            trace_checks.append(
                margin_check(
                    f"trace_autocorrelation@{lag}",
                    difference,
                    MARGINS["trace_autocorrelation_abs_difference"],
                    difference <= MARGINS["trace_autocorrelation_abs_difference"]
                    if difference is not None
                    else None,
                    reason="no valid within-document pairs at this lag" if difference is None else None,
                )
            )
        output["checks"].extend(trace_checks)
        output["order"]["trace_autocorrelation_checks"] = trace_checks
        for coordinate_sample in ("A", "B"):
            left_coordinate = families["tribe"]["order"]["coordinate_samples"][coordinate_sample]
            right_coordinate = families["textfeat"]["order"]["coordinate_samples"][coordinate_sample]
            if "welch_trace_power" not in left_coordinate or "welch_trace_power" not in right_coordinate:
                js = None
            else:
                lp = left_coordinate["welch_trace_power"]
                rp = right_coordinate["welch_trace_power"]
                js = jensen_shannon(lp["normalized_power"], rp["normalized_power"])
            check = margin_check(
                f"coordinate_sample_{coordinate_sample}:power_js_nats",
                js,
                MARGINS["power_spectrum_js_nats"],
                js <= MARGINS["power_spectrum_js_nats"] if js is not None else None,
                reason="within-document power unavailable" if js is None else None,
            )
            output["checks"].append(check)
            output["order"][coordinate_sample] = {
                "coordinate_sample_power_js_divergence_nats": js,
                "check": check,
            }
    else:
        output["order"] = {"status": "unresolved_due_to_context_metadata"}
        output["checks"].append(
            margin_check(
                "order_structure",
                None,
                {
                    "trace_autocorrelation": MARGINS["trace_autocorrelation_abs_difference"],
                    "power_js_nats": MARGINS["power_spectrum_js_nats"],
                },
                None,
                reason="valid context boundaries unavailable",
            )
        )
    output["checks"].extend(list(nuisance.get("checks") or []))
    output["mechanical_conjunction"] = mechanical_conjunction(output["checks"])
    return output


def run_geometry(args: argparse.Namespace, manifest: Mapping[str, Any]) -> dict[str, Any]:
    started = time.time()
    scratch = repo_path(args.scratch_dir)
    families: dict[str, Any] = {}
    extracted: list[Path] = []
    train_arrays: dict[str, np.ndarray] = {}
    heldout_arrays: dict[str, np.ndarray] = {}
    moments: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    train_ids = load_npz_member(TARGET_SOURCES["tribe"]["train_cache"], "item_indices")
    train_texts = load_npz_member(TARGET_SOURCES["tribe"]["train_cache"], "texts")
    segments, context_status = load_context_segments(train_ids.tolist(), train_texts.tolist())
    if context_status.get("status") != "valid":
        log(f"order diagnostics unresolved: {context_status}")
    device = choose_device(args.device)
    if device != manifest["design_lock"]["execution_device"]:
        raise ValueError(
            f"geometry device={device} differs from manifest-frozen "
            f"device={manifest['design_lock']['execution_device']}"
        )
    for family, spec in TARGET_SOURCES.items():
        families[family] = {"cache_moments": {}, "samples": {}, "order": {}}
        arrays: dict[str, np.ndarray] = {}
        for split in ("train", "heldout"):
            cache = repo_path(spec[f"{split}_cache"])
            record = manifest["target_caches"][family][split]
            npy = ensure_target_npy(cache, record, scratch)
            extracted.append(npy)
            array = np.load(npy, mmap_mode="r", allow_pickle=False)
            arrays[split] = array
            report, mean, std = full_moments(array, args.row_chunk)
            families[family]["cache_moments"][split] = report
            if split == "train":
                train_arrays[family] = array
                moments[family] = (mean, std)
                standardization_validation = standardization_extrema_validation(
                    family, std, manifest
                )
                families[family]["training_standardized_moment_identity"] = {
                    "transform": "(Y - full_train_mean) / (full_train_std + 1e-6)",
                    "std_ddof": 0,
                    "expected_feature_mean": 0.0,
                    "feature_sd_quantiles": quantiles(std / (std + STD_EPS)),
                    "retained_e016_extrema_validation": standardization_validation,
                }
            else:
                heldout_arrays[family] = array
                train_mean, train_std = moments[family]
                families[family]["heldout_shift_in_training_standardized_units"] = {
                    "mean_shift_quantiles": quantiles((mean - train_mean) / (train_std + STD_EPS)),
                    "sd_ratio_quantiles": quantiles(std / (train_std + STD_EPS)),
                }
        mean, std = moments[family]
        for sample_label, frozen in manifest["row_samples"].items():
            families[family]["samples"][sample_label] = {}
            positions = frozen["row_positions_for_sorted_item_ids"]
            for view in ("training_standardized_primary", "raw_centered_sensitivity"):
                x, pre_center = sample_view(arrays["train"], positions, mean, std, view)
                svd, scores = randomized_svd_geometry(
                    x,
                    device,
                    rank_cap=ALGEBRAIC_RANK_CAP[family],
                )
                families[family]["samples"][sample_label][view] = {
                    "pre_center_global_moments": pre_center,
                    "svd": svd,
                    "intrinsic_dimension_2nn": descriptive_2nn(scores),
                }
        if context_status.get("status") == "valid":
            families[family]["order"] = {
                "scope": "exact E016 training-standardized targets; all pairs stay within recovered documents",
                "trace_autocorrelation_all_coordinates": trace_autocorrelation(
                    arrays["train"], mean, std, segments, args.row_chunk
                ),
                "coordinate_samples": {
                    label: coordinate_order_diagnostics(
                        arrays["train"],
                        mean,
                        std,
                        frozen["item_ids_sorted"],
                        segments,
                        args.row_chunk,
                    )
                    for label, frozen in manifest["coordinate_samples"].items()
                },
            }
        else:
            families[family]["order"] = {"status": "unresolved", "context": context_status}
    heldout_texts = load_npz_member(TARGET_SOURCES["tribe"]["heldout_cache"], "texts").tolist()
    nuisance, nuisance_derived = nuisance_target_predictability(
        train_arrays,
        heldout_arrays,
        moments,
        {"train": train_texts.tolist(), "heldout": heldout_texts},
        manifest,
        scratch,
        device,
        args.static_batch_size,
        args.feature_chunk,
    )
    extracted.extend(nuisance_derived)
    result = {
        "schema_version": SCHEMA_VERSION,
        "experiment": "E026",
        "stage": "geometry",
        "science_status": SCIENCE_STATUS,
        "created_at_utc": utc_now(),
        "elapsed_s": time.time() - started,
        "manifest_path": str(repo_path(args.manifest_in)),
        "manifest_sha256": sha256_file(repo_path(args.manifest_in)),
        "primary_view": (
            "E016-formula training-standardized targets: (Y-population_mean)/(population_std+1e-6); "
            "reconstructed extrema must reproduce retained E016 metadata"
        ),
        "raw_centered_view": "sensitivity only",
        "context": context_status,
        "families": families,
        "nuisance_target_predictability": nuisance,
        "component_comparison": geometry_comparison(families, nuisance),
        "inference_boundary": (
            "Geometry is deterministic on two frozen row samples. A/B disagreement is sample sensitivity; "
            "coordinates are features, not replication units; no p-values or confidence intervals are produced."
        ),
    }
    if not args.keep_extracted:
        for path in extracted:
            path.unlink(missing_ok=True)
            path.with_suffix(path.suffix + ".source.json").unlink(missing_ok=True)
    return result


def summary_stats(values: Sequence[float]) -> dict[str, Any]:
    from scipy.stats import t

    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return {"n": 0, "values": []}
    mean = float(arr.mean())
    if arr.size > 1:
        sd = float(arr.std(ddof=1))
        half = float(t.ppf(0.975, arr.size - 1) * sd / math.sqrt(arr.size))
        interval = [mean - half, mean + half]
    else:
        sd = None
        interval = None
    nonzero = arr[arr != 0]
    positives = int(np.count_nonzero(nonzero > 0))
    # Exact paired randomization sign-flip test on the mean statistic.  With
    # six seeds this enumerates only 64 assignments and retains magnitudes;
    # a binomial sign test is not the same test.
    if arr.size <= 20:
        observed = abs(float(arr.mean()))
        assignments = 1 << int(arr.size)
        extreme = 0
        tolerance = 1e-15 * max(1.0, observed)
        for mask in range(assignments):
            signs = np.asarray(
                [1.0 if mask & (1 << index) else -1.0 for index in range(arr.size)],
                dtype=np.float64,
            )
            if abs(float(np.mean(signs * arr))) >= observed - tolerance:
                extreme += 1
        exact_two_sided = float(extreme / assignments)
    else:
        exact_two_sided = None
    return {
        "n": int(arr.size),
        "values": arr.tolist(),
        "mean": mean,
        "median": float(np.median(arr)),
        "sd": sd,
        "t_ci95": interval,
        "positive_count": positives,
        "nonzero_count_for_sign_test": int(len(nonzero)),
        "exact_paired_sign_flip_two_sided_p": exact_two_sided,
        "sign_flip_assignments": (1 << int(arr.size)) if arr.size <= 20 else None,
        "sign_flip_identifying_assumption": (
            "paired seed contrasts are exchangeable under independent sign reversal under the sharp null"
        ),
    }


def rows_from_manifest(manifest: Mapping[str, Any], family: str) -> list[dict[str, Any]]:
    return [dict(row) for row in manifest["runs"][family]["rows"]]


def target_learning_summary(manifest: Mapping[str, Any], family: str) -> dict[str, Any]:
    run = manifest["runs"][family]
    target_arm = run["target_arm"]
    permuted_arm = run["permuted_arm"]
    by_seed: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows_from_manifest(manifest, family):
        by_seed[int(row["seed"])][str(row["arm"])] = row
    seed_rows: list[dict[str, Any]] = []
    target_deltas: list[float] = []
    perm_deltas: list[float] = []
    for seed in sorted(by_seed):
        kd = by_seed[seed]["kd_only"]
        target = by_seed[seed][target_arm]
        permuted = by_seed[seed][permuted_arm]
        kd_r2 = float(kd["target_r2"])
        headroom = 1.0 - kd_r2
        target_delta = float(target["target_r2"]) - kd_r2
        perm_delta = float(permuted["target_r2"]) - kd_r2
        target_deltas.append(target_delta)
        perm_deltas.append(perm_delta)
        seed_rows.append(
            {
                "seed": seed,
                "kd_target_r2": kd_r2,
                "target_arm_target_r2": target["target_r2"],
                "permuted_arm_target_r2": permuted["target_r2"],
                "target_minus_kd_delta_r2": target_delta,
                "permuted_minus_kd_delta_r2": perm_delta,
                "remaining_headroom": headroom,
                "target_headroom_closed": target_delta / headroom if headroom >= 0.05 else None,
                "headroom_ratio_suppressed": headroom < 0.05,
                "last_minibatch_diagnostics": {
                    "kd_final_loss": kd.get("final_loss"),
                    "target_final_loss": target.get("final_loss"),
                    "target_final_auxiliary_loss": target.get("final_brain"),
                    "permuted_final_loss": permuted.get("final_loss"),
                    "permuted_final_auxiliary_loss": permuted.get("final_brain"),
                },
            }
        )
    return {
        "family": family,
        "seed_rows": seed_rows,
        "target_minus_kd_delta_r2": summary_stats(target_deltas),
        "permuted_minus_kd_delta_r2": summary_stats(perm_deltas),
        "loss_scope": "retained last-minibatch diagnostics only; not an optimization-trajectory estimate",
        "initial_gradient_scale": "unknown_not_retained",
    }


def parameter_block(name: str) -> str:
    if ".wte." in f".{name}." or ".wpe." in f".{name}.":
        return "embeddings"
    if ".attn." in name:
        return "attention"
    if ".mlp." in name:
        return "mlp"
    if ".ln_" in name or ".ln_f." in f".{name}.":
        return "normalization"
    if name.startswith("lm_head"):
        return "output"
    return "other"


def parameter_update_norms(kd_path: Path, arm_path: Path) -> dict[str, Any]:
    from safetensors import safe_open

    if kd_path.suffix != ".safetensors" or arm_path.suffix != ".safetensors":
        raise ValueError("parameter audit currently requires safetensors model weights")
    accum: dict[str, dict[str, float]] = defaultdict(lambda: {"base_sq": 0.0, "delta_sq": 0.0})
    with safe_open(kd_path, framework="pt", device="cpu") as kd, safe_open(
        arm_path, framework="pt", device="cpu"
    ) as arm:
        kd_keys = list(kd.keys())
        arm_keys = list(arm.keys())
        if kd_keys != arm_keys:
            raise ValueError("KD/arm safetensor keys differ")
        for name in kd_keys:
            left = kd.get_tensor(name).detach().to(dtype=__import__("torch").float64)
            right = arm.get_tensor(name).detach().to(dtype=__import__("torch").float64)
            delta = right - left
            block = parameter_block(name)
            base_sq = float(__import__("torch").sum(left * left).item())
            delta_sq = float(__import__("torch").sum(delta * delta).item())
            accum[block]["base_sq"] += base_sq
            accum[block]["delta_sq"] += delta_sq
            accum["global"]["base_sq"] += base_sq
            accum["global"]["delta_sq"] += delta_sq
    output: dict[str, Any] = {}
    for block, values in sorted(accum.items()):
        base = math.sqrt(values["base_sq"])
        delta = math.sqrt(values["delta_sq"])
        output[block] = {
            "base_l2": base,
            "update_l2": delta,
            "relative_update_l2": delta / base if base > 0 else None,
        }
    return {
        "kd_weights": str(kd_path),
        "arm_weights": str(arm_path),
        "parameterization": "full saved GPT-2 tensors; auxiliary head absent",
        "blocks": output,
    }


def trained_parameter_summaries(manifest: Mapping[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for family in ("tribe", "textfeat"):
        run = manifest["runs"][family]
        target_arm = run["target_arm"]
        permuted_arm = run["permuted_arm"]
        by_seed: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
        for row in rows_from_manifest(manifest, family):
            by_seed[int(row["seed"])][str(row["arm"])] = row
        records: list[dict[str, Any]] = []
        for seed in sorted(by_seed):
            kd = repo_path(by_seed[seed]["kd_only"]["model_weights"])
            for arm_name in (target_arm, permuted_arm):
                arm_path = repo_path(by_seed[seed][arm_name]["model_weights"])
                rec = parameter_update_norms(kd, arm_path)
                rec.update({"seed": seed, "arm": arm_name})
                records.append(rec)
        output[family] = records
    return output


def linear_cka_rms(x: np.ndarray, y: np.ndarray, row_chunk: int) -> dict[str, Any]:
    if x.shape != y.shape or x.ndim != 2:
        raise ValueError(f"CKA/RMS arrays must have equal 2D shape, got {x.shape}, {y.shape}")
    n, dx = x.shape
    sx = np.zeros(dx, dtype=np.float64)
    sy = np.zeros(dx, dtype=np.float64)
    xtx = np.zeros((dx, dx), dtype=np.float64)
    yty = np.zeros((dx, dx), dtype=np.float64)
    xty = np.zeros((dx, dx), dtype=np.float64)
    delta_sq = np.float64(0.0)
    for start in range(0, n, row_chunk):
        stop = min(n, start + row_chunk)
        xb = np.asarray(x[start:stop], dtype=np.float64)
        yb = np.asarray(y[start:stop], dtype=np.float64)
        sx += xb.sum(axis=0, dtype=np.float64)
        sy += yb.sum(axis=0, dtype=np.float64)
        xtx += xb.T @ xb
        yty += yb.T @ yb
        xty += xb.T @ yb
        delta = xb - yb
        delta_sq += np.einsum("ij,ij->", delta, delta, dtype=np.float64)
    sxx = xtx - np.outer(sx, sx) / n
    syy = yty - np.outer(sy, sy) / n
    sxy = xty - np.outer(sx, sy) / n
    numerator = float(np.einsum("ij,ij->", sxy, sxy, dtype=np.float64))
    left = float(np.einsum("ij,ij->", sxx, sxx, dtype=np.float64))
    right = float(np.einsum("ij,ij->", syy, syy, dtype=np.float64))
    denominator = math.sqrt(left * right)
    # Center the *difference* before RMS/Frobenius movement.  Otherwise a
    # constant activation offset is incorrectly called representation change
    # despite centered CKA being invariant to it.
    delta_sum = sx - sy
    centered_delta_sq = max(0.0, float(delta_sq) - float(delta_sum @ delta_sum) / n)
    kd_centered_sq = float(np.trace(syy))
    rms = math.sqrt(centered_delta_sq / (n * dx))
    relative = math.sqrt(centered_delta_sq / kd_centered_sq) if kd_centered_sq > 1e-12 else None
    cka = numerator / denominator if denominator > 0 else None
    if cka is not None:
        if cka < -1e-8 or cka > 1.0 + 1e-8:
            raise ValueError(f"linear CKA outside numerical tolerance: {cka}")
        cka = min(1.0, max(0.0, cka))
    return {
        "n_items": n,
        "hidden_dim": dx,
        "linear_cka": cka,
        "linear_cka_distance": 1.0 - cka if cka is not None else None,
        "centered_activation_rms_change": rms,
        "centered_relative_frobenius_change": relative,
        "cka_scope": "biased feature-space linear CKA; rows are fixed stimuli, not inference units",
    }


def representation_movement(
    e025_path: Path | None, expected_extraction_sha256: str | None, row_chunk: int
) -> dict[str, Any]:
    if e025_path is None or not e025_path.exists():
        return {"status": "unavailable", "reason": "valid E025 extraction index is absent"}
    actual_extraction_sha256 = sha256_file(e025_path)
    if expected_extraction_sha256 and actual_extraction_sha256 != expected_extraction_sha256:
        return {
            "status": "invalid",
            "reason": "E025 extraction index changed after the E026 manifest was frozen",
            "expected_sha256": expected_extraction_sha256,
            "actual_sha256": actual_extraction_sha256,
        }
    provenance = inspect_e025_manifest(e025_path)
    if provenance.get("status") != "valid" or provenance.get("kind") != "extraction":
        return {
            "status": "invalid",
            "reason": "E025 extraction provenance failed revalidation at trained-stage execution",
            "errors": provenance.get("errors") or [],
        }

    extraction = load_json(e025_path)
    manifest_path = repo_path(str(extraction["manifest"]["path"]))
    base = load_json(manifest_path)
    cache_by_key = {
        str(row["cache_key"]): row
        for row in extraction.get("cache_rows") or []
        if isinstance(row, Mapping) and row.get("cache_key")
    }
    alias_to_cache = {
        (str(alias["family"]), int(alias["seed"]), str(alias["arm"])): str(alias["cache_key"])
        for alias in base.get("logical_aliases") or []
        if isinstance(alias, Mapping)
    }
    duplicate_record = (
        extraction.get("gate_measurements", {}).get("duplicate_extraction_noise", {})
        if isinstance(extraction.get("gate_measurements"), Mapping)
        else {}
    )
    duplicate_values: dict[str, float] = {}
    for field in ("max_centered_relative_frobenius", "max_linear_cka_distance"):
        raw_value = duplicate_record.get(field)
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            return {
                "status": "invalid",
                "reason": f"E025 duplicate-extraction noise field {field!r} is absent or nonnumeric",
                "observed": raw_value,
            }
        if not math.isfinite(value) or value < 0:
            return {
                "status": "invalid",
                "reason": f"E025 duplicate-extraction noise field {field!r} is nonfinite or negative",
                "observed": raw_value,
            }
        duplicate_values[field] = value
    duplicate_fro = duplicate_values["max_centered_relative_frobenius"]
    duplicate_cka = duplicate_values["max_linear_cka_distance"]
    relative_fro_floor = max(
        1e-12, MARGINS["representation_duplicate_noise_multiplier"] * duplicate_fro
    )
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for family, arms in (
        ("tribe", ("tribe_mse", "tribe_perm")),
        ("textfeat", ("textfeat_mse", "textfeat_perm")),
    ):
        for seed in range(6):
            for arm in arms:
                try:
                    target_key = alias_to_cache[(family, seed, arm)]
                    kd_key = alias_to_cache[(family, seed, "kd_only")]
                    target_row = cache_by_key[target_key]
                    kd_row = cache_by_key[kd_key]
                    target_path = repo_path(str(target_row["path"]))
                    kd_path = repo_path(str(kd_row["path"]))
                    with np.load(target_path, allow_pickle=False) as target_cache, np.load(
                        kd_path, allow_pickle=False
                    ) as kd_cache:
                        for corpus in ("wikitext", "tuckute"):
                            for layer in (6, 7):
                                array_key = f"{corpus}_layer_{layer}"
                                target_array = np.asarray(target_cache[array_key])
                                kd_array = np.asarray(kd_cache[array_key])
                                metrics = linear_cka_rms(target_array, kd_array, row_chunk)
                                role = (
                                    "wikitext_layer6_primary"
                                    if arm.endswith("_mse") and corpus == "wikitext" and layer == 6
                                    else "sensitivity"
                                )
                                records.append(
                                    {
                                        "family": family,
                                        "arm": arm,
                                        "seed": seed,
                                        "target_cache_key": target_key,
                                        "kd_cache_key": kd_key,
                                        "corpus": corpus,
                                        "layer": layer,
                                        "role": role,
                                        **metrics,
                                    }
                                )
                except Exception as exc:
                    errors.append(f"{family}/seed{seed}/{arm}: {type(exc).__name__}: {exc}")
    return {
        "status": (
            "available"
            if len(records) == 96 and not errors
            else ("partial" if records else "unavailable")
        ),
        "extraction_index": str(e025_path),
        "extraction_index_sha256": actual_extraction_sha256,
        "base_manifest": str(manifest_path),
        "base_manifest_sha256": sha256_file(manifest_path),
        "records": records,
        "errors": errors,
        "duplicate_extraction_noise": {
            "max_linear_cka_distance": duplicate_cka,
            "max_centered_relative_frobenius": duplicate_fro,
            "centered_relative_frobenius_ratio_floor": relative_fro_floor,
            "multiplier": MARGINS["representation_duplicate_noise_multiplier"],
        },
        "primary_rule": (
            "WikiText heldout layer 6 is primary; WikiText layer 7 and both Tuckute layers "
            "are sensitivity diagnostics only"
        ),
    }


def compare_parameter_movement(parameter_norms: Mapping[str, Any]) -> dict[str, Any]:
    lookup: dict[tuple[str, int, str], Mapping[str, Any]] = {}
    for family, records in parameter_norms.items():
        for row in records:
            lookup[(family, int(row["seed"]), str(row["arm"]))] = row
    blocks = sorted(
        {
            block
            for row in lookup.values()
            for block in (row.get("blocks") or {}).keys()
        }
    )
    output: dict[str, Any] = {"blocks": {}, "checks": []}
    for block in blocks:
        seed_rows: list[dict[str, Any]] = []
        signed_differences: list[float] = []
        for seed in range(6):
            left = lookup.get(("tribe", seed, "tribe_mse"), {}).get("blocks", {}).get(block)
            right = lookup.get(("textfeat", seed, "textfeat_mse"), {}).get("blocks", {}).get(block)
            if not isinstance(left, Mapping) or not isinstance(right, Mapping):
                seed_rows.append({"seed": seed, "state": "UNRESOLVED", "reason": "block absent"})
                continue
            lv = left.get("relative_update_l2")
            rv = right.get("relative_update_l2")
            if lv is None or rv is None:
                seed_rows.append({"seed": seed, "state": "UNRESOLVED", "reason": "zero base norm"})
                continue
            lv, rv = float(lv), float(rv)
            signed_differences.append(lv - rv)
            if lv > MARGINS["parameter_update_absolute_floor"] and rv > MARGINS[
                "parameter_update_absolute_floor"
            ]:
                value = abs(math.log(lv / rv))
                margin = MARGINS["parameter_update_abs_log_ratio"]
                route = "absolute_log_ratio"
            else:
                value = abs(lv - rv)
                margin = MARGINS["parameter_update_absolute_floor"]
                route = "absolute_difference_below_floor"
            seed_rows.append(
                {
                    "seed": seed,
                    "tribe_relative_update_l2": lv,
                    "textfeat_relative_update_l2": rv,
                    "route": route,
                    "value": value,
                    "margin": margin,
                    "state": "PASS" if value <= margin else "FAIL",
                }
            )
        block_state = mechanical_conjunction(seed_rows)
        output["blocks"][block] = {
            "seed_rows": seed_rows,
            "paired_signed_difference": summary_stats(signed_differences),
            "mechanical_conjunction": block_state,
            "load_bearing": block == "global",
        }
        if block == "global":
            output["checks"].extend(seed_rows)
    output["mechanical_conjunction"] = mechanical_conjunction(output["checks"])
    return output


def compare_representation_movement(movement: Mapping[str, Any]) -> dict[str, Any]:
    if movement.get("status") != "available":
        check = margin_check(
            "representation_movement",
            None,
            {
                "cka": MARGINS["representation_cka_distance_abs_difference"],
                "fro_log_ratio": MARGINS[
                    "representation_centered_relative_fro_abs_log_ratio"
                ],
            },
            None,
            reason=str(movement.get("reason") or movement.get("errors") or "unavailable"),
        )
        return {"checks": [check], "mechanical_conjunction": mechanical_conjunction([check])}
    lookup = {
        (str(row["family"]), int(row["seed"])): row
        for row in movement.get("records") or []
        if row.get("role") == "wikitext_layer6_primary"
    }
    noise = movement.get("duplicate_extraction_noise") or {}
    fro_floor = float(noise.get("centered_relative_frobenius_ratio_floor") or 1e-12)
    checks: list[dict[str, Any]] = []
    seed_rows: list[dict[str, Any]] = []
    cka_signed: list[float] = []
    fro_signed: list[float] = []
    for seed in range(6):
        left = lookup.get(("tribe", seed))
        right = lookup.get(("textfeat", seed))
        if left is None or right is None:
            unresolved = margin_check(
                f"seed{seed}:representation_movement", None, None, None, reason="missing primary row"
            )
            checks.append(unresolved)
            seed_rows.append(unresolved)
            continue
        left_cka = float(left["linear_cka_distance"])
        right_cka = float(right["linear_cka_distance"])
        cka_diff = abs(left_cka - right_cka)
        cka_signed.append(left_cka - right_cka)
        cka_check = margin_check(
            f"seed{seed}:cka_distance",
            cka_diff,
            MARGINS["representation_cka_distance_abs_difference"],
            cka_diff <= MARGINS["representation_cka_distance_abs_difference"],
        )
        left_fro = float(left["centered_relative_frobenius_change"])
        right_fro = float(right["centered_relative_frobenius_change"])
        fro_signed.append(left_fro - right_fro)
        if left_fro > fro_floor and right_fro > fro_floor:
            fro_value = abs(math.log(left_fro / right_fro))
            fro_margin = MARGINS["representation_centered_relative_fro_abs_log_ratio"]
            fro_route = "absolute_log_ratio"
        else:
            fro_value = abs(left_fro - right_fro)
            fro_margin = MARGINS["representation_centered_relative_fro_absolute_floor"]
            fro_route = "absolute_difference_at_or_below_duplicate_floor"
        fro_check = margin_check(
            f"seed{seed}:centered_relative_frobenius",
            fro_value,
            fro_margin,
            fro_value <= fro_margin,
        )
        fro_check["route"] = fro_route
        checks.extend((cka_check, fro_check))
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
                "checks": [cka_check, fro_check],
            }
        )
    return {
        "primary": "MSE arm minus seed-matched KD on WikiText heldout layer 6",
        "duplicate_noise_floor": noise,
        "seed_rows": seed_rows,
        "paired_cka_distance_difference": summary_stats(cka_signed),
        "paired_centered_relative_frobenius_difference": summary_stats(fro_signed),
        "checks": checks,
        "mechanical_conjunction": mechanical_conjunction(checks),
    }


def compare_target_learning(learning: Mapping[str, Any]) -> dict[str, Any]:
    tribe = learning["tribe"]["seed_rows"]
    textfeat = learning["textfeat"]["seed_rows"]
    if len(tribe) != 6 or len(textfeat) != 6:
        check = margin_check(
            "target_learning_grid", None, None, None, reason="six paired seeds unavailable"
        )
        return {"checks": [check], "mechanical_conjunction": mechanical_conjunction([check])}
    baseline_delta = [
        float(left["kd_target_r2"]) - float(right["kd_target_r2"])
        for left, right in zip(tribe, textfeat, strict=True)
    ]
    target_gain_delta = [
        float(left["target_minus_kd_delta_r2"])
        - float(right["target_minus_kd_delta_r2"])
        for left, right in zip(tribe, textfeat, strict=True)
    ]
    tribe_headroom = np.asarray([row["remaining_headroom"] for row in tribe], dtype=np.float64)
    text_headroom = np.asarray([row["remaining_headroom"] for row in textfeat], dtype=np.float64)
    baseline_abs_mean = abs(float(np.mean(baseline_delta)))
    headroom_ratio = (
        float(tribe_headroom.mean() / text_headroom.mean())
        if float(text_headroom.mean()) >= 0.05 and float(tribe_headroom.mean()) >= 0.05
        else None
    )
    checks = [
        margin_check(
            "kd_target_r2_abs_paired_mean_difference",
            baseline_abs_mean,
            MARGINS["kd_target_r2_abs_paired_mean_difference"],
            baseline_abs_mean <= MARGINS["kd_target_r2_abs_paired_mean_difference"],
        ),
        margin_check(
            "remaining_headroom_mean_ratio",
            headroom_ratio,
            MARGINS["remaining_headroom_mean_ratio"],
            (
                MARGINS["remaining_headroom_mean_ratio"][0]
                <= headroom_ratio
                <= MARGINS["remaining_headroom_mean_ratio"][1]
            )
            if headroom_ratio is not None
            else None,
            reason="mean remaining headroom below 0.05" if headroom_ratio is None else None,
        ),
    ]
    return {
        "baseline_predictability_tribe_minus_textfeat": summary_stats(baseline_delta),
        "target_gain_tribe_minus_textfeat": summary_stats(target_gain_delta),
        "mean_remaining_headroom_ratio_tribe_over_textfeat": headroom_ratio,
        "checks": checks,
        "mechanical_conjunction": mechanical_conjunction(checks),
    }


def run_trained(args: argparse.Namespace, manifest: Mapping[str, Any]) -> dict[str, Any]:
    started = time.time()
    e025_record = manifest.get("e025_representation_provenance") or {}
    e025_path = (
        repo_path(e025_record["path"])
        if e025_record.get("status") == "valid" and e025_record.get("kind") == "extraction"
        else None
    )
    learning = {family: target_learning_summary(manifest, family) for family in ("tribe", "textfeat")}
    learning_comparison = compare_target_learning(learning)
    parameter_norms = trained_parameter_summaries(manifest)
    parameter_comparison = compare_parameter_movement(parameter_norms)
    movement = representation_movement(e025_path, e025_record.get("sha256"), args.row_chunk)
    movement_comparison = compare_representation_movement(movement)
    trained_checks = (
        list(learning_comparison.get("checks") or [])
        + list(parameter_comparison.get("checks") or [])
        + list(movement_comparison.get("checks") or [])
    )
    result = {
        "schema_version": SCHEMA_VERSION,
        "experiment": "E026",
        "stage": "trained",
        "science_status": SCIENCE_STATUS,
        "created_at_utc": utc_now(),
        "manifest_path": str(repo_path(args.manifest_in)),
        "manifest_sha256": sha256_file(repo_path(args.manifest_in)),
        "target_learning_and_loss": learning,
        "target_learning_comparison": learning_comparison,
        "initial_gradient_comparability": {
            "status": "unknown",
            "reason": "initial standardized auxiliary loss/gradient norms were not retained in E016",
        },
        "parameter_update_norms": parameter_norms,
        "parameter_update_comparison": parameter_comparison,
        "representation_movement": movement,
        "representation_movement_comparison": movement_comparison,
        "mechanical_measured_axis_checks": trained_checks,
        "mechanical_measured_axis_conjunction": mechanical_conjunction(trained_checks),
        "inference_boundary": (
            "Seeds are technical training realizations for these trained-model summaries. Target coordinates "
            "and parameters are not replication units. Last-minibatch losses and movement norms are diagnostics."
        ),
    }
    result["elapsed_s"] = time.time() - started
    return result


def run_numerical_selftests() -> dict[str, Any]:
    """Synthetic-only acceptance suite for the load-bearing numerical helpers."""
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: Any) -> None:
        checks.append({"name": name, "pass": bool(passed), "detail": json_safe(detail)})

    try:
        fixture = np.asarray([[0.0], [1.0], [2.0]], dtype=np.float32)
        _, _, std = full_moments(fixture, row_chunk=2)
        expected = float(fixture.std(axis=0, ddof=0)[0])
        record("e016_population_sd", math.isclose(float(std[0]), expected, rel_tol=1e-7), {
            "observed": float(std[0]), "expected": expected
        })

        ids = np.arange(10_000, dtype=np.int64)
        row_a = freeze_sample(ids, ROW_SAMPLE_KEYS["A"], SAMPLE_N)
        row_b = freeze_sample(ids, ROW_SAMPLE_KEYS["B"], SAMPLE_N, row_a["item_ids_sorted"])
        coords = np.arange(TARGET_D, dtype=np.int64)
        coord_a = freeze_sample(coords, COORD_SAMPLE_KEYS["A"], COORD_SAMPLE_N)
        coord_b = freeze_sample(
            coords, COORD_SAMPLE_KEYS["B"], COORD_SAMPLE_N, coord_a["item_ids_sorted"]
        )
        frozen = {
            "row_samples": {"A": row_a, "B": row_b},
            "coordinate_samples": {"A": coord_a, "B": coord_b},
        }
        validate_frozen_sample_records(frozen)
        repeat = freeze_sample(ids, ROW_SAMPLE_KEYS["A"], SAMPLE_N)
        record(
            "sample_freeze_repeat_and_disjoint",
            repeat == row_a
            and not (set(row_a["item_ids_sorted"]) & set(row_b["item_ids_sorted"]))
            and not (set(coord_a["item_ids_sorted"]) & set(coord_b["item_ids_sorted"])),
            {"row_a_hash": row_a["item_ids_sha256_int64_le"]},
        )
        tampered = json.loads(json.dumps(frozen))
        tampered["coordinate_samples"]["A"]["item_ids_sha256_int64_le"] = "0" * 64
        rejected = False
        try:
            validate_frozen_sample_records(tampered)
        except ValueError:
            rejected = True
        record("sample_manifest_tamper_rejected", rejected, {})

        with tempfile.TemporaryDirectory(prefix="e026-derived-cache-selftest-") as raw_tmp:
            tmp = Path(raw_tmp)
            source = tmp / "fixture.npz"
            original_targets = np.arange(24, dtype=np.float32).reshape(6, 4)
            np.savez(source, targets=original_targets)
            source_record = inspect_npz(source, full_sha256=True)
            derived = ensure_target_npy(source, source_record, tmp / "scratch")
            tampered_target = np.load(derived, mmap_mode="r+", allow_pickle=False)
            tampered_target[0, 0] = -999.0
            tampered_target.flush()
            del tampered_target
            restored = ensure_target_npy(source, source_record, tmp / "scratch")
            restored_array = np.load(restored, allow_pickle=False)
            restored_meta = load_json(restored.with_suffix(restored.suffix + ".source.json"))
            record(
                "derived_target_tamper_overwritten_from_source",
                np.array_equal(restored_array, original_targets)
                and restored_meta.get("derived_npy_sha256_for_audit") == sha256_file(restored),
                {
                    "derived_sha256": sha256_file(restored),
                    "source_sha256": source_record["sha256"],
                },
            )
        record(
            "derived_static_cache_reuse_disabled",
            DERIVED_SCRATCH_REUSE is False,
            {"derived_scratch_reuse": DERIVED_SCRATCH_REUSE},
        )

        unequal = [10.0, -1.0, -1.0, -1.0, -1.0, -1.0]
        sign_p = summary_stats(unequal)["exact_paired_sign_flip_two_sided_p"]
        record("paired_sign_flip_retains_magnitude", sign_p == 1.0, {"p": sign_p})

        x = np.arange(24, dtype=np.float32).reshape(6, 4)
        movement = linear_cka_rms(x + 5.0, x, row_chunk=2)
        record(
            "centered_movement_constant_offset",
            abs(float(movement["centered_activation_rms_change"])) <= 1e-12
            and abs(float(movement["centered_relative_frobenius_change"])) <= 1e-12,
            movement,
        )

        rng = np.random.default_rng(91)
        matrix = rng.standard_normal((48, 20), dtype=np.float32)
        matrix -= matrix.mean(axis=0, keepdims=True)
        kwargs = {
            "top_k": 8,
            "oversample": 10,
            "power_iterations": 4,
            "seed": 123,
            "rank_cap": 20,
            "enforce_production_shape": False,
        }
        first, scores_first = randomized_svd_geometry(matrix, "cpu", **kwargs)
        second, scores_second = randomized_svd_geometry(matrix, "cpu", **kwargs)
        exact = np.linalg.svd(matrix.astype(np.float64), full_matrices=False, compute_uv=False)[:8]
        exact_normalized = np.square(exact) / np.square(exact).sum(dtype=np.float64)
        # Normalize the exact top-eight shape for a shape-only agreement check.
        approx = np.asarray(first["normalized_covariance_eigenvalues_top512"], dtype=np.float64)
        approx_shape = approx / approx.sum()
        relative_shape_error = float(
            np.max(np.abs(approx_shape - exact_normalized) / np.maximum(exact_normalized, 1e-12))
        )
        record(
            "randomized_svd_exact_small_fixture",
            relative_shape_error <= 2e-3,
            {"max_relative_normalized_topk_error": relative_shape_error},
        )
        record(
            "randomized_svd_repeat_determinism",
            np.array_equal(
                np.asarray(first["singular_values_top512"]),
                np.asarray(second["singular_values_top512"]),
            )
            and np.array_equal(scores_first, scores_second),
            {},
        )
        scaled, _ = randomized_svd_geometry(matrix * 3.0, "cpu", **kwargs)
        scale_diff = float(
            np.max(
                np.abs(
                    np.asarray(first["normalized_covariance_eigenvalues_top512"])
                    - np.asarray(scaled["normalized_covariance_eigenvalues_top512"])
                )
            )
        )
        record("normalized_spectrum_scale_invariance", scale_diff <= 2e-6, {"max_abs": scale_diff})

        duplicate_fixture = rng.standard_normal((16, 12), dtype=np.float32)
        duplicate_fixture[-5:] = duplicate_fixture[0]
        duplicate_report = descriptive_2nn(duplicate_fixture)
        duplicate_counts = {
            rank: int(report["exact_duplicate_rows"])
            for rank, report in duplicate_report["ranks"].items()
        }
        record(
            "descriptive_2nn_exact_duplicate_detection",
            all(count == 6 for count in duplicate_counts.values()),
            {"exact_duplicate_rows_by_rank": duplicate_counts},
        )

        train = np.asarray([[0.0], [1.0], [2.0]])
        transformed_a, _ = fit_scale(train, np.asarray([[3.0]]))
        transformed_b, _ = fit_scale(train, np.asarray([[3_000.0]]))
        record(
            "predictor_transform_heldout_invariance",
            np.array_equal(transformed_a, transformed_b),
            {},
        )
        x_train = np.arange(30, dtype=np.float64).reshape(-1, 1)
        x_test = np.arange(30, 40, dtype=np.float64).reshape(-1, 1)
        y_train = np.column_stack((2.0 * x_train[:, 0] + 3.0, -x_train[:, 0] + 1.0))
        y_test = np.column_stack((2.0 * x_test[:, 0] + 3.0, -x_test[:, 0] + 1.0))
        sse_full, sst_full = ridge_sse_sst(x_train, y_train, x_test, y_test, 1e-8)
        sse_chunk, sst_chunk = ridge_sse_sst(
            x_train, y_train, x_test, y_test, 1e-8, target_chunk=1
        )
        record(
            "ridge_target_chunk_equivalence",
            math.isclose(sse_full, sse_chunk, rel_tol=1e-10, abs_tol=1e-12)
            and math.isclose(sst_full, sst_chunk, rel_tol=1e-12, abs_tol=1e-12)
            and 1.0 - sse_full / sst_full > 0.999999,
            {"full_sse": sse_full, "chunk_sse": sse_chunk},
        )
    except Exception as exc:
        record("selftest_unhandled_exception", False, {"type": type(exc).__name__, "message": str(exc)})
    return {
        "scope": "synthetic fixtures only; no E016/E025 target or endpoint values loaded",
        "checks": checks,
        "pass": bool(checks and all(check["pass"] for check in checks)),
    }


def main() -> None:
    args = parse_args()
    out = output_path(args, args.stage)
    if args.stage in {"geometry", "trained", "all"}:
        manifest_path = repo_path(args.manifest_in).resolve()
        if repo_path(out).resolve() == manifest_path:
            raise ValueError(
                "evidence-stage --out must differ from --manifest-in; the reviewed manifest is immutable"
            )
    if args.row_chunk <= 0 or args.feature_chunk <= 0 or args.static_batch_size <= 0:
        raise ValueError("chunk sizes must be positive")
    if args.row_chunk != ROW_CHUNK:
        raise ValueError(
            f"--row-chunk is design-locked at {ROW_CHUNK}; changing it requires a new frozen manifest"
        )
    if args.feature_chunk != NUISANCE_TARGET_CHUNK:
        raise ValueError(
            "--feature-chunk is design-locked at "
            f"{NUISANCE_TARGET_CHUNK}; changing it requires a new frozen manifest"
        )
    if args.static_batch_size != STATIC_BATCH_SIZE:
        raise ValueError(
            "--static-batch-size is design-locked at "
            f"{STATIC_BATCH_SIZE}; changing it requires a new frozen manifest"
        )
    if DERIVED_SCRATCH_REUSE:
        raise RuntimeError("E026 evidence execution forbids derived-scratch reuse")
    if args.stage == "selftest":
        result = {
            "schema_version": SCHEMA_VERSION,
            "experiment": "E026",
            "stage": "selftest",
            "science_status": "synthetic plumbing only; never a scientific result",
            "created_at_utc": utc_now(),
            **run_numerical_selftests(),
        }
    elif args.stage == "manifest":
        result = build_manifest(args)
    elif args.stage == "geometry":
        manifest = load_frozen_manifest(repo_path(args.manifest_in))
        result = run_geometry(args, manifest)
    elif args.stage == "trained":
        manifest = load_frozen_manifest(repo_path(args.manifest_in))
        result = run_trained(args, manifest)
    else:
        manifest = load_frozen_manifest(repo_path(args.manifest_in))
        geometry = run_geometry(args, manifest)
        trained = run_trained(args, manifest)
        all_checks = (
            list(geometry.get("component_comparison", {}).get("checks") or [])
            + list(trained.get("mechanical_measured_axis_checks") or [])
        )
        combined = mechanical_conjunction(all_checks)
        if combined["state"] == "PASS":
            classification = "MEASURED_AXES_PASS__INITIAL_GRADIENT_UNRESOLVED"
        elif combined["state"] == "FAIL":
            classification = "AT_LEAST_ONE_MEASURED_AXIS_FAILS"
        else:
            classification = "MEASURED_AXIS_AUDIT_UNRESOLVED"
        result = {
            "schema_version": SCHEMA_VERSION,
            "experiment": "E026",
            "stage": "all",
            "science_status": SCIENCE_STATUS,
            "created_at_utc": utc_now(),
            "manifest": manifest,
            "geometry": geometry,
            "trained": trained,
            "mechanical_measured_axis_summary": {
                **combined,
                "classification": classification,
                "initial_gradient_comparability": "UNKNOWN_NOT_RETAINED",
                "not_a_scientific_verdict": True,
            },
        }
    write_json(out, result)
    print(
        json.dumps(
            {
                "stage": args.stage,
                "output_json": str(out),
                "science_status": result["science_status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
