#!/usr/bin/env python3
"""E025 participant-level transfer harness for saved E016 students.

This runner has three deliberately separated stages:

``manifest``
    Metadata-only preflight.  It hashes inputs, validates the complete logical
    arm/seed grid, proves the two families' KD checkpoints are byte-identical,
    audits the nine complete Tuckute participants, and freezes cache identities.
    It does not import Transformers, load model tensors, or compute an endpoint.

``extract``
    Evidence-producing representation pass.  Each unique weight bundle is
    loaded once.  One batched forward pass per corpus returns layers 6 and 7;
    the WikiText pass also accumulates direct next-token NLL and bits/byte.
    Representations and alias metadata are cached under ``outputs/E025``.

``score``
    Reads frozen caches and writes only raw participant x seed x arm x layer x
    nuisance-variant x contiguous-fold rows.  It does not aggregate contrasts,
    form confidence intervals, or flip any project/package verdict.

The stage boundary is a scientific safeguard: a successful manifest is an
artifact-integrity fact, not an E025 result.  Only explicit ``extract`` or
``score`` execution can create scientific measurements.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import sys
import tarfile
import tempfile
from typing import Any, Iterable
import zipfile

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "outputs/E025"
DEFAULT_DATA_DIR = ROOT / "data/tuckute2024"
DEFAULT_WIKITEXT = ROOT / "data/kd_corpus/wikitext103_sentences_heldout.txt"
DEFAULT_ANALYZER = ROOT / "scripts/e025_analyze_participant_transfer.py"
DEFAULT_RUN_JSONS = (
    ROOT / "outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json",
    ROOT / "outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.json",
    ROOT / "outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.json",
)

SCHEMA_VERSION = "e025-participant-transfer.v1"
SEEDS = tuple(range(6))
VALID_UIDS = (797, 837, 841, 848, 856, 865, 875, 876, 880)
EXCLUDED_UID = 853
TRAIN_UIDS = (848, 865, 875, 876)
HELDOUT_UIDS = (797, 837, 841, 856, 880)
TUCKUTE_ROIS = (
    "lang_LH_AntTemp",
    "lang_LH_IFG",
    "lang_LH_IFGorb",
    "lang_LH_MFG",
    "lang_LH_PostTemp",
)
EXPECTED_ARMS = {
    "tribe": ("kd_only", "tribe_mse", "tribe_perm"),
    "textfeat": ("kd_only", "textfeat_mse", "textfeat_perm"),
}
EXPECTED_TARGET_DIM = 20484
EXPECTED_TRAIN_ITEMS = 95999
EXPECTED_HELDOUT_ITEMS = 1999
EXPECTED_TUCKUTE_ITEMS = 1000
EXPECTED_LAMBDA = 0.1
DEFAULT_LAYERS = (6, 7)
DEFAULT_ALPHAS = (1.0, 10.0, 100.0, 1000.0, 10000.0)

NUISANCE_VARIANTS = {
    "primary": "token length + normalized item position + fixed GPT-2-medium static embeddings",
    "imageability": "primary + Tuckute imageability",
    "full_cov": "imageability + GPT-2XL and PCFG surprisal, with primary nuisance",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_path(path: str | Path) -> Path:
    p = Path(path).expanduser()
    return p if p.is_absolute() else ROOT / p


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, chunk_bytes: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_bytes)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def file_record(path: Path, hash_cache: dict[Path, str] | None = None) -> dict[str, Any]:
    path = resolve_path(path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"required file not found: {path}")
    if hash_cache is not None and path in hash_cache:
        digest = hash_cache[path]
    else:
        digest = sha256_file(path)
        if hash_cache is not None:
            hash_cache[path] = digest
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest}


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=False)
            handle.write("\n")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def atomic_write_npz(path: Path, arrays: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".npz", dir=path.parent)
    os.close(fd)
    tmp = Path(raw_tmp)
    try:
        np.savez(tmp, **arrays)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def read_nonempty_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def inspect_target_npz_metadata(path: Path, expected_rows: int) -> dict[str, Any]:
    """Validate a target cache without materializing its multi-gigabyte target matrix."""
    required_keys = {
        "targets", "texts", "item_indices", "vertex_index", "segment_counts", "metadata"
    }
    with zipfile.ZipFile(path) as archive:
        names = {name[:-4] for name in archive.namelist() if name.endswith(".npy")}
        if names != required_keys:
            raise ValueError(f"target cache keys differ for {path}: {sorted(names)}")
        with archive.open("targets.npy") as handle:
            version = np.lib.format.read_magic(handle)
            if version == (1, 0):
                shape, fortran, dtype = np.lib.format.read_array_header_1_0(handle)
            elif version == (2, 0):
                shape, fortran, dtype = np.lib.format.read_array_header_2_0(handle)
            else:
                raise ValueError(f"unsupported target NPY version {version}: {path}")
    if tuple(shape) != (expected_rows, EXPECTED_TARGET_DIM):
        raise ValueError(
            f"target matrix shape differs for {path}: {tuple(shape)} != "
            f"{(expected_rows, EXPECTED_TARGET_DIM)}"
        )
    if np.dtype(dtype) != np.dtype("float32") or fortran:
        raise ValueError(f"target matrix dtype/order differs for {path}: {dtype}, fortran={fortran}")
    with np.load(path, allow_pickle=False) as cached:
        texts = [str(value) for value in cached["texts"]]
        item_indices = np.asarray(cached["item_indices"], dtype=np.int64)
        vertex_index = np.asarray(cached["vertex_index"], dtype=np.int64)
        segment_counts = np.asarray(cached["segment_counts"])
        if len(texts) != expected_rows or item_indices.shape != (expected_rows,):
            raise ValueError(f"target cache row metadata differs for {path}")
        if vertex_index.shape != (EXPECTED_TARGET_DIM,) or segment_counts.shape != (expected_rows,):
            raise ValueError(f"target cache coordinate/segment metadata differs for {path}")
        if len(np.unique(item_indices)) != expected_rows:
            raise ValueError(f"target cache item indices are not unique: {path}")
        return {
            "keys": sorted(required_keys),
            "targets_header": {
                "shape": list(shape),
                "dtype": str(np.dtype(dtype)),
                "fortran_order": bool(fortran),
                "npy_version": list(version),
            },
            "ordered_text_sha256": ordered_text_sha(texts),
            "item_indices_sha256": sha256_bytes(item_indices.astype("<i8", copy=False).tobytes()),
            "vertex_index_sha256": sha256_bytes(vertex_index.astype("<i8", copy=False).tobytes()),
            "segment_counts_sha256": sha256_bytes(segment_counts.tobytes(order="C")),
        }


def ordered_text_sha(texts: Iterable[str]) -> str:
    return sha256_bytes(("\n".join(texts) + "\n").encode("utf-8"))


def parse_csv_ints(raw: str) -> tuple[int, ...]:
    values = tuple(int(part.strip()) for part in raw.split(",") if part.strip())
    if not values:
        raise ValueError("expected at least one comma-separated integer")
    if len(set(values)) != len(values):
        raise ValueError(f"duplicate integer in list: {raw}")
    return values


def parse_csv_floats(raw: str) -> tuple[float, ...]:
    values = tuple(float(part.strip()) for part in raw.split(",") if part.strip())
    if not values:
        raise ValueError("expected at least one comma-separated float")
    return values


def weight_files(artifact_dir: Path) -> list[Path]:
    patterns = ("model*.safetensors", "pytorch_model*.bin")
    found: set[Path] = set()
    for pattern in patterns:
        found.update(path for path in artifact_dir.glob(pattern) if path.is_file())
    paths = sorted(found, key=lambda path: path.name)
    if not paths:
        raise FileNotFoundError(f"no model weights under {artifact_dir}")
    return paths


def runtime_files(artifact_dir: Path) -> list[Path]:
    names = (
        "config.json",
        "generation_config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "vocab.json",
        "merges.txt",
    )
    return [artifact_dir / name for name in names if (artifact_dir / name).is_file()]


def bundle_digest(records: list[dict[str, Any]]) -> str:
    if len(records) == 1:
        return str(records[0]["sha256"])
    named = [{"name": Path(rec["path"]).name, "sha256": rec["sha256"]} for rec in records]
    return sha256_bytes(canonical_json(named).encode("utf-8"))


def runtime_digest(records: list[dict[str, Any]]) -> str:
    named = [{"name": Path(rec["path"]).name, "sha256": rec["sha256"]} for rec in records]
    return sha256_bytes(canonical_json(named).encode("utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected object-valued JSON: {path}")
    return payload


def _tuckute_csv_bytes(data_dir: Path) -> tuple[bytes, dict[str, Any]]:
    extracted = sorted(data_dir.rglob("brain-lang-data_participant_*.csv"))
    extracted = [path for path in extracted if "blocked" not in path.name]
    if extracted:
        path = extracted[0].resolve()
        raw = path.read_bytes()
        return raw, {
            "container": "extracted_csv",
            "path": str(path),
            "member": None,
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
        }

    archives = sorted(data_dir.glob("*.tar")) + sorted(data_dir.glob("*.tar.gz"))
    if not archives:
        raise FileNotFoundError(
            f"no extracted Tuckute participant CSV or tar archive under {data_dir}"
        )
    archive = archives[0].resolve()
    with tarfile.open(archive, "r:*") as tar:
        candidates = [
            member for member in tar.getmembers()
            if member.isfile()
            and Path(member.name).name.startswith("brain-lang-data_participant_")
            and member.name.endswith(".csv")
            and "blocked" not in Path(member.name).name
        ]
        if len(candidates) != 1:
            raise ValueError(
                f"expected one participant CSV in {archive}, found {[m.name for m in candidates]}"
            )
        member = candidates[0]
        handle = tar.extractfile(member)
        if handle is None:
            raise OSError(f"could not read {member.name} from {archive}")
        raw = handle.read()
    return raw, {
        "container": "tar_member",
        "path": str(archive),
        "container_bytes": archive.stat().st_size,
        "container_sha256": sha256_file(archive),
        "member": member.name,
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
    }


def load_tuckute_participants(
    data_dir: Path,
    condition: str,
    uids: tuple[int, ...],
    *,
    include_targets: bool,
) -> tuple[list[str], dict[int, np.ndarray], np.ndarray, dict[str, Any]]:
    """Load/order Tuckute once and prove the participant x item x ROI grid.

    ``include_targets=False`` is the manifest-only path.  Response values are
    checked only for finiteness/completeness and are not summarized or scored.
    """
    import pandas as pd

    raw, source = _tuckute_csv_bytes(data_dir)
    df = pd.read_csv(io.BytesIO(raw))
    required = {
        "cond",
        "target_UID",
        "item_id",
        "roi",
        "sentence",
        "response_target",
        "rating_imageability_mean",
        "log-prob-gpt2-xl_mean",
        "log-prob-pcfg_mean",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Tuckute CSV missing columns: {missing}")

    cond = df[df["cond"] == condition].copy()
    if cond.empty:
        raise ValueError(f"Tuckute condition {condition!r} has no rows")
    cond["target_UID"] = cond["target_UID"].astype(int)
    item_ids = sorted(int(value) for value in cond["item_id"].unique())
    if len(item_ids) != EXPECTED_TUCKUTE_ITEMS:
        raise ValueError(
            f"expected {EXPECTED_TUCKUTE_ITEMS} condition-{condition} items, found {len(item_ids)}"
        )

    sentence_counts = cond.groupby("item_id")["sentence"].nunique(dropna=False)
    if not bool((sentence_counts == 1).all()):
        bad = [int(idx) for idx in sentence_counts[sentence_counts != 1].index[:10]]
        raise ValueError(f"inconsistent sentence text for item_ids {bad}")
    sentence_map = cond.drop_duplicates("item_id").set_index("item_id")["sentence"]
    texts = [str(sentence_map.loc[item_id]) for item_id in item_ids]

    item_meta = cond.drop_duplicates("item_id").set_index("item_id")
    cov_cols = (
        "rating_imageability_mean",
        "log-prob-gpt2-xl_mean",
        "log-prob-pcfg_mean",
    )
    covariates = np.stack(
        [item_meta.loc[item_ids, col].to_numpy(dtype=np.float64) for col in cov_cols], axis=1
    )
    if not np.isfinite(covariates).all():
        counts = {col: int(np.sum(~np.isfinite(covariates[:, i]))) for i, col in enumerate(cov_cols)}
        raise ValueError(f"nonfinite Tuckute covariates: {counts}")

    targets: dict[int, np.ndarray] = {}
    participant_rows: list[dict[str, Any]] = []
    expected_cells = EXPECTED_TUCKUTE_ITEMS * len(TUCKUTE_ROIS)
    for uid in uids:
        sub = cond[(cond["target_UID"] == uid) & cond["roi"].isin(TUCKUTE_ROIS)].copy()
        grouped = sub.groupby(["item_id", "roi"], observed=True).size()
        duplicate_cells = int((grouped > 1).sum())
        pivot = sub.pivot_table(
            index="item_id", columns="roi", values="response_target", aggfunc="first", dropna=False
        ).reindex(index=item_ids, columns=list(TUCKUTE_ROIS))
        nonfinite = int(np.sum(~np.isfinite(pivot.to_numpy(dtype=np.float64))))
        exact_cells = int(len(sub)) == expected_cells and len(grouped) == expected_cells
        complete = exact_cells and duplicate_cells == 0 and nonfinite == 0
        participant_rows.append({
            "uid": uid,
            "n_source_rows": int(len(sub)),
            "n_item_roi_cells": int(len(grouped)),
            "expected_item_roi_cells": expected_cells,
            "duplicate_item_roi_cells": duplicate_cells,
            "nonfinite_responses": nonfinite,
            "complete": complete,
            "split": "train" if uid in TRAIN_UIDS else "heldout",
        })
        if not complete:
            raise ValueError(f"Tuckute UID {uid} is incomplete: {participant_rows[-1]}")
        if include_targets:
            targets[uid] = pivot.to_numpy(dtype=np.float32)

    excluded = cond[
        (cond["target_UID"] == EXCLUDED_UID) & cond["roi"].isin(TUCKUTE_ROIS)
    ].pivot_table(
        index="item_id", columns="roi", values="response_target", aggfunc="first", dropna=False
    ).reindex(index=item_ids, columns=list(TUCKUTE_ROIS))
    excluded_nonfinite = int(np.sum(~np.isfinite(excluded.to_numpy(dtype=np.float64))))

    meta = {
        "source": source,
        "condition": condition,
        "ordered_item_count": len(item_ids),
        "ordered_item_id_sha256": sha256_bytes(canonical_json(item_ids).encode("utf-8")),
        "ordered_text_sha256": ordered_text_sha(texts),
        "rois": list(TUCKUTE_ROIS),
        "valid_uids": list(uids),
        "train_uids": list(TRAIN_UIDS),
        "heldout_uids": list(HELDOUT_UIDS),
        "participants": participant_rows,
        "excluded_uid": {
            "uid": EXCLUDED_UID,
            "nonfinite_responses": excluded_nonfinite,
            "included": False,
        },
        "covariate_columns": list(cov_cols),
        "covariates_complete": True,
    }
    return texts, targets, covariates, meta


def expected_grid() -> set[tuple[str, int, str]]:
    return {
        (family, seed, arm)
        for family, arms in EXPECTED_ARMS.items()
        for seed in SEEDS
        for arm in arms
    }


def family_for_run(payload: dict[str, Any], path: Path) -> str:
    family = str(payload.get("target_label", ""))
    if family not in EXPECTED_ARMS:
        raise ValueError(f"unexpected target_label={family!r} in {path}")
    return family


def validate_artifact_metadata(
    metadata: dict[str, Any], alias: dict[str, Any], run_payload: dict[str, Any], path: Path
) -> None:
    expected = {
        "seed": alias["seed"],
        "arm": alias["arm"],
        "target_label": alias["family"],
        "student": run_payload.get("student"),
    }
    mismatches = {
        key: {"expected": value, "observed": metadata.get(key)}
        for key, value in expected.items()
        if metadata.get(key) != value
    }
    if not math.isclose(
        float(metadata.get("lambda_brain", float("nan"))),
        float(alias["lambda_brain"]),
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        mismatches["lambda_brain"] = {
            "expected": alias["lambda_brain"],
            "observed": metadata.get("lambda_brain"),
        }
    if mismatches:
        raise ValueError(f"artifact metadata mismatch in {path}: {mismatches}")


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    hash_cache: dict[Path, str] = {}
    run_paths = tuple(resolve_path(path).resolve() for path in (args.run_json or DEFAULT_RUN_JSONS))
    aliases: list[dict[str, Any]] = []
    run_records: list[dict[str, Any]] = []
    target_paths: set[Path] = set()

    for run_path in run_paths:
        run_rec = file_record(run_path, hash_cache)
        payload = load_json(run_path)
        family = family_for_run(payload, run_path)
        rows = payload.get("rows")
        if not isinstance(rows, list):
            raise ValueError(f"{run_path} has no list-valued rows")
        run_records.append({**run_rec, "family": family, "row_count": len(rows)})

        for key in ("target_cache", "heldout_target_cache"):
            raw = payload.get(key)
            if not raw:
                raise ValueError(f"{run_path} missing {key}")
            target_paths.add(resolve_path(raw).resolve())

        for row_index, row in enumerate(rows):
            if not isinstance(row, dict):
                raise ValueError(f"non-object row {row_index} in {run_path}")
            seed = int(row.get("seed"))
            arm = str(row.get("arm"))
            if arm not in EXPECTED_ARMS[family]:
                raise ValueError(f"unexpected {family} arm={arm!r} seed={seed} in {run_path}")
            expected_lambda = 0.0 if arm == "kd_only" else EXPECTED_LAMBDA
            observed_lambda = float(row.get("lambda_brain"))
            if not math.isclose(observed_lambda, expected_lambda, rel_tol=0.0, abs_tol=1e-12):
                raise ValueError(
                    f"lambda mismatch for {(family, seed, arm)}: {observed_lambda} != {expected_lambda}"
                )
            exact_shape = (
                int(row.get("target_dim")) == EXPECTED_TARGET_DIM
                and int(row.get("n_train")) == EXPECTED_TRAIN_ITEMS
                and int(row.get("n_heldout_ppl")) == EXPECTED_HELDOUT_ITEMS
            )
            if not exact_shape:
                raise ValueError(
                    f"training/target shape mismatch for {(family, seed, arm)}: "
                    f"target_dim={row.get('target_dim')} n_train={row.get('n_train')} "
                    f"n_heldout={row.get('n_heldout_ppl')}"
                )
            raw_artifact = row.get("model_artifact_dir")
            if not raw_artifact:
                raise ValueError(f"missing model_artifact_dir for {(family, seed, arm)}")
            artifact_dir = resolve_path(raw_artifact).resolve()
            if not artifact_dir.is_dir():
                raise FileNotFoundError(f"artifact directory not found: {artifact_dir}")

            metadata_path = artifact_dir / "e016_model_artifact.json"
            metadata_rec = file_record(metadata_path, hash_cache)
            alias = {
                "family": family,
                "seed": seed,
                "arm": arm,
                "lambda_brain": observed_lambda,
                "source_run_json": str(run_path),
                "source_row_index": row_index,
                "artifact_dir": str(artifact_dir),
                "artifact_metadata": metadata_rec,
            }
            validate_artifact_metadata(load_json(metadata_path), alias, payload, metadata_path)

            weight_recs = [file_record(path, hash_cache) for path in weight_files(artifact_dir)]
            runtime_recs = [file_record(path, hash_cache) for path in runtime_files(artifact_dir)]
            alias["weight_files"] = weight_recs
            alias["weight_sha256"] = bundle_digest(weight_recs)
            alias["runtime_files"] = runtime_recs
            alias["runtime_sha256"] = runtime_digest(runtime_recs)
            aliases.append(alias)

    observed_grid = {(a["family"], int(a["seed"]), a["arm"]) for a in aliases}
    if len(observed_grid) != len(aliases):
        raise ValueError("duplicate logical family/seed/arm rows across run JSON inputs")
    missing_grid = sorted(expected_grid() - observed_grid)
    extra_grid = sorted(observed_grid - expected_grid())
    if missing_grid or extra_grid:
        raise ValueError(f"logical grid mismatch: missing={missing_grid}, extra={extra_grid}")
    global_runtime_shas = {alias["runtime_sha256"] for alias in aliases}
    if len(global_runtime_shas) != 1:
        raise ValueError(
            "all E025 saved students must share one frozen GPT-2 config/tokenizer runtime bundle"
        )

    alias_by_key = {(a["family"], a["seed"], a["arm"]): a for a in aliases}
    shared_kd: list[dict[str, Any]] = []
    for seed in SEEDS:
        tribe = alias_by_key[("tribe", seed, "kd_only")]
        textfeat = alias_by_key[("textfeat", seed, "kd_only")]
        weight_identical = tribe["weight_sha256"] == textfeat["weight_sha256"]
        runtime_identical = tribe["runtime_sha256"] == textfeat["runtime_sha256"]
        row = {
            "seed": seed,
            "tribe_weight_sha256": tribe["weight_sha256"],
            "textfeat_weight_sha256": textfeat["weight_sha256"],
            "weight_identical": weight_identical,
            "runtime_identical": runtime_identical,
        }
        shared_kd.append(row)
        if not weight_identical or not runtime_identical:
            raise ValueError(f"shared KD identity failed: {row}")

    groups: dict[str, list[dict[str, Any]]] = {}
    for alias in aliases:
        groups.setdefault(alias["weight_sha256"], []).append(alias)
    unique_checkpoints: list[dict[str, Any]] = []
    for weight_sha, group in sorted(groups.items()):
        runtime_shas = {alias["runtime_sha256"] for alias in group}
        if len(runtime_shas) != 1:
            raise ValueError(
                f"byte-identical weights have different runtime/tokenizer bundles: {weight_sha}"
            )
        cache_key = f"ckpt_{weight_sha[:24]}"
        canonical = min(group, key=lambda alias: alias["artifact_dir"])
        model_config = load_json(Path(canonical["artifact_dir"]) / "config.json")
        hidden_dim = int(model_config.get("n_embd", 0))
        if hidden_dim <= 0:
            raise ValueError(f"checkpoint config lacks a positive n_embd: {canonical['artifact_dir']}")
        alias_keys = [
            {"family": a["family"], "seed": a["seed"], "arm": a["arm"]}
            for a in sorted(group, key=lambda a: (a["family"], a["seed"], a["arm"]))
        ]
        unique_checkpoints.append({
            "cache_key": cache_key,
            "weight_sha256": weight_sha,
            "runtime_sha256": next(iter(runtime_shas)),
            "hidden_dim": hidden_dim,
            "canonical_artifact_dir": canonical["artifact_dir"],
            "aliases": alias_keys,
            "planned_cache_npz": str((args.out_dir / "reps" / f"{cache_key}.npz").resolve()),
        })
        for alias in group:
            alias["cache_key"] = cache_key

    if len(unique_checkpoints) != 30:
        raise ValueError(
            f"expected 30 unique checkpoints after six shared-KD deduplications, "
            f"found {len(unique_checkpoints)}"
        )

    target_records: list[dict[str, Any]] = []
    for path in sorted(target_paths):
        split = "heldout" if "heldout_" in path.name else "train"
        family = "textfeat" if "text_feature" in str(path) else "tribe"
        expected_rows = EXPECTED_HELDOUT_ITEMS if split == "heldout" else EXPECTED_TRAIN_ITEMS
        target_records.append({
            **file_record(path, hash_cache),
            "family": family,
            "split": split,
            "metadata_preflight": inspect_target_npz_metadata(path, expected_rows),
        })
    wikitext_path = resolve_path(args.wikitext_heldout).resolve()
    wiki_all_texts = read_nonempty_lines(wikitext_path)
    if len(wiki_all_texts) < EXPECTED_HELDOUT_ITEMS:
        raise ValueError(
            f"expected at least {EXPECTED_HELDOUT_ITEMS} WikiText heldout sentences, "
            f"found {len(wiki_all_texts)}"
        )
    # E016's frozen run configuration set limit_heldout=1999.  The backing file
    # currently contains one additional nonempty line, so the scientific probe
    # is the exact ordered prefix consumed by those runs, not the whole file.
    wiki_texts = wiki_all_texts[:EXPECTED_HELDOUT_ITEMS]
    wikitext_record = {
        **file_record(wikitext_path, hash_cache),
        "source_nonempty_lines": len(wiki_all_texts),
        "scored_prefix_lines": len(wiki_texts),
        "ordered_text_sha256": ordered_text_sha(wiki_texts),
        "selection_rule": "first 1999 nonempty lines, matching every locked E016 run's limit_heldout",
    }
    for split in ("train", "heldout"):
        paired = [record for record in target_records if record["split"] == split]
        if len(paired) != 2:
            raise ValueError(f"expected two {split} target caches, found {len(paired)}")
        for identity_key in ("ordered_text_sha256", "item_indices_sha256"):
            values = {record["metadata_preflight"][identity_key] for record in paired}
            if len(values) != 1:
                raise ValueError(f"TRIBE/text-feature {split} target {identity_key} differs")
    heldout_text_hashes = {
        record["metadata_preflight"]["ordered_text_sha256"]
        for record in target_records if record["split"] == "heldout"
    }
    if heldout_text_hashes != {wikitext_record["ordered_text_sha256"]}:
        raise ValueError("heldout target-cache texts differ from the frozen WikiText prefix")

    tuckute_texts, _, _, tuckute_meta = load_tuckute_participants(
        resolve_path(args.data_dir).resolve(), args.condition, args.uids, include_targets=False
    )
    if len(tuckute_texts) != EXPECTED_TUCKUTE_ITEMS:
        raise ValueError("internal Tuckute item-count validation failure")
    scorer_validation = scoring_equivalence_selftest()
    if not scorer_validation["pass"]:
        raise RuntimeError(
            f"optimized scorer failed canonical equivalence during preflight: {scorer_validation}"
        )
    canonical_scorer = file_record((ROOT / "scripts/pilot_lib.py").resolve(), hash_cache)

    aliases.sort(key=lambda a: (a["family"], a["seed"], a["arm"]))
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "E025 metadata-only preflight manifest",
        "science_status": (
            "PRECHECK ONLY: no model tensor was loaded and no E025 endpoint, bpb, "
            "movement, contrast, interval, or verdict was computed"
        ),
        "created_at_utc": utc_now(),
        "stage": "manifest",
        "preflight_pass": True,
        "schema_description": {
            "logical_aliases": "one row per family x seed x arm; all analyzer identities live here",
            "unique_checkpoints": "one cache per unique weight SHA; aliases recover shared KD rows",
            "shared_kd_identity": "weight and runtime equality checked independently for every seed",
            "planned_cache": "NPZ keys are frozen before any model load",
        },
        "runner": file_record(Path(__file__).resolve(), hash_cache),
        "analyzer": file_record(DEFAULT_ANALYZER.resolve(), hash_cache),
        "canonical_scorer": canonical_scorer,
        "scorer_validation": scorer_validation,
        "design_lock": {
            "seeds": list(SEEDS),
            "families_and_arms": {key: list(value) for key, value in EXPECTED_ARMS.items()},
            "valid_uids": list(args.uids),
            "excluded_uid": EXCLUDED_UID,
            "layers": list(args.layers),
            "n_folds": 5,
            "pca_rank": args.n_pca,
            "ridge_alphas": list(args.ridge_alphas),
            "nuisance_variants": NUISANCE_VARIANTS,
            "representation_pooling": "attention-mask mean",
            "condition": args.condition,
            "reference_model": args.reference_model,
            "extraction_batch_size": args.batch_size,
            "max_length": args.max_length,
        },
        "checks": [
            {"name": "exact_logical_grid", "status": "PASS", "logical_rows": len(aliases)},
            {"name": "shared_kd_weight_and_runtime_identity", "status": "PASS", "seeds": len(SEEDS)},
            {"name": "unique_checkpoint_count", "status": "PASS", "unique_checkpoints": 30},
            {"name": "tuckute_participant_roi_text_completeness", "status": "PASS", "uids": len(args.uids)},
            {"name": "wikitext_order_and_count", "status": "PASS", "items": len(wiki_texts)},
            {"name": "target_cache_presence_and_hashes", "status": "PASS", "files": len(target_records)},
            {
                "name": "optimized_scorer_matches_canonical",
                "status": "PASS",
                "canonical_scorer_sha256": canonical_scorer["sha256"],
                "max_absolute_errors": scorer_validation["max_absolute_errors"],
            },
        ],
        "source_run_jsons": run_records,
        "source_targets": target_records,
        "wikitext_heldout": wikitext_record,
        "tuckute": tuckute_meta,
        "logical_aliases": aliases,
        "shared_kd_identity": {"all_seeds_identical": True, "per_seed": shared_kd},
        "unique_checkpoints": unique_checkpoints,
        "planned_cache": {
            "checkpoint_npz_keys": [
                "wikitext_layer_6",
                "wikitext_layer_7",
                "tuckute_layer_6",
                "tuckute_layer_7",
                "metadata_json",
            ],
            "nuisance_npz": str((args.out_dir / "nuisance_tuckute.npz").resolve()),
            "nuisance_npz_keys": [
                "base_scalar",
                "static_embedding",
                "imageability",
                "full_cov_extra",
                "metadata_json",
            ],
            "extraction_index_json": str(args.extraction_path.resolve()),
            "raw_score_json": str(args.score_path.resolve()),
        },
    }
    return manifest


def resolve_device(choice: str) -> str:
    if choice != "auto":
        return choice
    import torch

    return "cuda" if torch.cuda.is_available() else "cpu"


def configure_determinism() -> None:
    import torch

    np.random.seed(0)
    torch.manual_seed(0)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(0)
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False


def load_model_and_tokenizer(model_ref: str | Path, device: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    ref = str(model_ref)
    tokenizer = AutoTokenizer.from_pretrained(ref)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(ref).to(device).eval()
    return model, tokenizer


def _masked_pool(hidden, attention_mask):
    mask = attention_mask.unsqueeze(-1).to(dtype=hidden.dtype)
    return (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1.0)


def forward_corpus(
    model,
    tokenizer,
    texts: list[str],
    layers: tuple[int, ...],
    device: str,
    batch_size: int,
    max_length: int,
    *,
    compute_lm: bool,
) -> tuple[dict[int, np.ndarray], dict[str, Any] | None]:
    """One model forward per batch yields every requested layer and optional NLL."""
    import torch

    outputs: dict[int, list[np.ndarray]] = {layer: [] for layer in layers}
    nll_nats = 0.0
    n_tokens = 0
    n_bytes = 0
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            encoded = tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length,
            ).to(device)
            result = model(**encoded, output_hidden_states=True, use_cache=False)
            for layer in layers:
                if layer >= len(result.hidden_states):
                    raise ValueError(
                        f"requested hidden-state index {layer}, model exposes {len(result.hidden_states)}"
                    )
                pooled = _masked_pool(result.hidden_states[layer], encoded["attention_mask"])
                outputs[layer].append(pooled.float().cpu().numpy())

            if compute_lm:
                logits = result.logits[:, :-1, :]
                target = encoded["input_ids"][:, 1:]
                score_mask = encoded["attention_mask"][:, 1:].bool()
                log_prob = torch.log_softmax(logits.float(), dim=-1)
                selected = log_prob.gather(-1, target.unsqueeze(-1)).squeeze(-1)
                nll_nats += float((-selected[score_mask]).sum().cpu())
                n_tokens += int(score_mask.sum().cpu())
                ids_cpu = encoded["input_ids"].detach().cpu()
                lengths = encoded["attention_mask"].sum(dim=1).detach().cpu().tolist()
                for ids, length in zip(ids_cpu, lengths):
                    scored_ids = ids[1:int(length)].tolist()
                    decoded = tokenizer.decode(scored_ids, clean_up_tokenization_spaces=False)
                    n_bytes += len(decoded.encode("utf-8"))
            del result

    arrays = {layer: np.concatenate(chunks, axis=0).astype(np.float32, copy=False)
              for layer, chunks in outputs.items()}
    if not compute_lm:
        return arrays, None
    if n_tokens <= 0 or n_bytes <= 0:
        raise ValueError(f"invalid language-quality denominator: tokens={n_tokens}, bytes={n_bytes}")
    lm = {
        "nll_nats": nll_nats,
        "n_scored_tokens": n_tokens,
        "n_scored_utf8_bytes": n_bytes,
        "per_token_perplexity": math.exp(nll_nats / n_tokens),
        "bits_per_byte": nll_nats / math.log(2.0) / n_bytes,
        "definition": (
            "sum next-token NLL bits divided by UTF-8 bytes decoded from exactly the scored "
            "post-first-token IDs; padding and each sentence's first token are excluded"
        ),
    }
    return arrays, lm


def centered_relative_frobenius(base: np.ndarray, other: np.ndarray) -> float:
    x = np.asarray(base, dtype=np.float64)
    y = np.asarray(other, dtype=np.float64)
    if x.shape != y.shape:
        raise ValueError(f"representation shape mismatch: {x.shape} vs {y.shape}")
    x = x - x.mean(axis=0, keepdims=True)
    y = y - y.mean(axis=0, keepdims=True)
    return float(np.linalg.norm(y - x, ord="fro") / max(np.linalg.norm(x, ord="fro"), 1e-12))


def linear_cka_distance(base: np.ndarray, other: np.ndarray) -> float:
    x = np.asarray(base, dtype=np.float64)
    y = np.asarray(other, dtype=np.float64)
    if x.shape != y.shape:
        raise ValueError(f"representation shape mismatch: {x.shape} vs {y.shape}")
    x = x - x.mean(axis=0, keepdims=True)
    y = y - y.mean(axis=0, keepdims=True)
    cross = x.T @ y
    numerator = float(np.sum(cross * cross))
    xx = x.T @ x
    yy = y.T @ y
    denominator = math.sqrt(float(np.sum(xx * xx)) * float(np.sum(yy * yy)))
    cka = numerator / max(denominator, 1e-30)
    return float(max(0.0, min(1.0, 1.0 - cka)))


def mean_t_ci95(values: Iterable[float]) -> dict[str, Any]:
    """Two-sided Student-t interval over the explicitly supplied independent units."""
    from scipy.stats import t as student_t

    array = np.asarray(tuple(values), dtype=np.float64)
    if array.size < 2 or not np.isfinite(array).all():
        raise ValueError(f"t-CI requires at least two finite values, received {array}")
    mean = float(array.mean())
    standard_error = float(array.std(ddof=1) / math.sqrt(array.size))
    critical = float(student_t.ppf(0.975, df=array.size - 1))
    return {
        "n": int(array.size),
        "mean": mean,
        "standard_error": standard_error,
        "ci95": [mean - critical * standard_error, mean + critical * standard_error],
        "inference_unit": "training seed",
    }


def cache_metadata(npz_path: Path) -> dict[str, Any]:
    with np.load(npz_path, allow_pickle=False) as cached:
        return json.loads(str(cached["metadata_json"].item()))


def extract_static_embeddings(model, tokenizer, texts: list[str], device: str, batch_size: int) -> np.ndarray:
    import torch

    embedding = model.get_input_embeddings()
    rows: list[np.ndarray] = []
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            encoded = tokenizer(
                texts[start:start + batch_size],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(device)
            values = embedding(encoded["input_ids"])
            pooled = _masked_pool(values, encoded["attention_mask"])
            rows.append(pooled.float().cpu().numpy())
    return np.concatenate(rows, axis=0).astype(np.float32, copy=False)


def build_nuisance_cache(
    manifest: dict[str, Any], args: argparse.Namespace, texts: list[str], covariates: np.ndarray, device: str
) -> dict[str, Any]:
    cache_path = resolve_path(manifest["planned_cache"]["nuisance_npz"])
    if cache_path.exists() and not args.overwrite_cache:
        with np.load(cache_path, allow_pickle=False) as cached:
            if "metadata_json" not in cached.files:
                raise ValueError(f"nuisance cache lacks metadata_json: {cache_path}")
            metadata = json.loads(str(cached["metadata_json"].item()))
            expected_metadata = {
                "schema_version": SCHEMA_VERSION,
                "artifact_type": "E025 fixed nuisance cache",
                "reference_model": args.reference_model,
                "ordered_text_sha256": manifest["tuckute"]["ordered_text_sha256"],
                "row_count": len(texts),
                "variants": NUISANCE_VARIANTS,
            }
            for key, value in expected_metadata.items():
                if metadata.get(key) != value:
                    raise ValueError(
                        f"stale nuisance cache {cache_path}: {key}={metadata.get(key)!r} != {value!r}"
                    )
            array_keys = ("base_scalar", "static_embedding", "imageability", "full_cov_extra")
            if set(cached.files) != {*array_keys, "metadata_json"}:
                raise ValueError(f"nuisance cache key set differs: {sorted(cached.files)}")
            declared_hashes = metadata.get("array_sha256")
            if not isinstance(declared_hashes, dict):
                raise ValueError(f"nuisance cache lacks array hashes: {cache_path}")
            for key in array_keys:
                observed = sha256_bytes(np.asarray(cached[key]).tobytes(order="C"))
                if declared_hashes.get(key) != observed:
                    raise ValueError(f"nuisance cache array hash differs for {key}: {cache_path}")
        return {"path": str(cache_path), "sha256": sha256_file(cache_path), "reused": True,
                "metadata": metadata}

    model, tokenizer = load_model_and_tokenizer(args.reference_model, device)
    static = extract_static_embeddings(model, tokenizer, texts, device, args.batch_size)
    lengths = np.array(
        [len(tokenizer(text, truncation=True, max_length=512)["input_ids"]) for text in texts],
        dtype=np.float64,
    )
    position = np.arange(len(texts), dtype=np.float64) / max(len(texts) - 1, 1)
    base = np.stack([lengths, position], axis=1).astype(np.float32)
    metadata = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "E025 fixed nuisance cache",
        "reference_model": args.reference_model,
        "ordered_text_sha256": manifest["tuckute"]["ordered_text_sha256"],
        "row_count": len(texts),
        "variants": NUISANCE_VARIANTS,
        "array_sha256": {
            "base_scalar": sha256_bytes(base.tobytes(order="C")),
            "static_embedding": sha256_bytes(static.tobytes(order="C")),
            "imageability": sha256_bytes(covariates[:, :1].astype(np.float32).tobytes(order="C")),
            "full_cov_extra": sha256_bytes(covariates.astype(np.float32).tobytes(order="C")),
        },
    }
    atomic_write_npz(cache_path, {
        "base_scalar": base,
        "static_embedding": static,
        "imageability": covariates[:, :1].astype(np.float32),
        "full_cov_extra": covariates.astype(np.float32),
        "metadata_json": np.array(canonical_json(metadata)),
    })
    del model
    return {"path": str(cache_path), "sha256": sha256_file(cache_path), "reused": False,
            "metadata": metadata}


def alias_science_lookup(manifest: dict[str, Any]) -> dict[tuple[str, int, str], dict[str, Any]]:
    run_cache: dict[str, dict[str, Any]] = {}
    lookup: dict[tuple[str, int, str], dict[str, Any]] = {}
    for alias in manifest["logical_aliases"]:
        source = alias["source_run_json"]
        if source not in run_cache:
            run_cache[source] = load_json(Path(source))
        row = run_cache[source]["rows"][int(alias["source_row_index"])]
        identity = (alias["family"], int(alias["seed"]), alias["arm"])
        if (str(row.get("arm")), int(row.get("seed"))) != (alias["arm"], int(alias["seed"])):
            raise ValueError(f"source row identity changed after manifest: {identity}")
        lookup[identity] = row
    return lookup


def verify_file_record(record: dict[str, Any], label: str) -> None:
    """Require a manifest-recorded file to retain its exact size and digest."""
    path = Path(str(record.get("path", "")))
    if not path.is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    expected_bytes = int(record.get("bytes", -1))
    if path.stat().st_size != expected_bytes:
        raise ValueError(
            f"{label} byte size differs from manifest: {path.stat().st_size} != {expected_bytes}"
        )
    expected_sha = str(record.get("sha256", ""))
    if sha256_file(path) != expected_sha:
        raise ValueError(f"{label} SHA-256 differs from manifest: {path}")


def verify_manifest(manifest: dict[str, Any], args: argparse.Namespace) -> None:
    """Bind every evidence-producing stage to the metadata-only design lock."""
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported manifest schema: {manifest.get('schema_version')}")
    if manifest.get("stage") != "manifest" or manifest.get("preflight_pass") is not True:
        raise ValueError("manifest is not a passing metadata preflight")
    if len(manifest.get("logical_aliases", [])) != 36:
        raise ValueError("manifest logical alias count is not 36")
    if len(manifest.get("unique_checkpoints", [])) != 30:
        raise ValueError("manifest unique checkpoint count is not 30")
    runner = manifest.get("runner")
    if not isinstance(runner, dict) or runner.get("sha256") != sha256_file(Path(__file__).resolve()):
        raise ValueError("E025 runner differs from the preflight-frozen runner")
    analyzer = manifest.get("analyzer")
    if not isinstance(analyzer, dict) or analyzer.get("sha256") != sha256_file(DEFAULT_ANALYZER):
        raise ValueError("E025 analyzer differs from the preflight-frozen analyzer")
    canonical_scorer = manifest.get("canonical_scorer")
    canonical_path = (ROOT / "scripts/pilot_lib.py").resolve()
    if (
        not isinstance(canonical_scorer, dict)
        or canonical_scorer.get("sha256") != sha256_file(canonical_path)
    ):
        raise ValueError("canonical variance-partition scorer differs from preflight")
    scorer_validation = manifest.get("scorer_validation")
    if not isinstance(scorer_validation, dict) or scorer_validation.get("pass") is not True:
        raise ValueError("manifest lacks a passing optimized/canonical scorer equivalence proof")

    lock = manifest.get("design_lock")
    if not isinstance(lock, dict):
        raise ValueError("manifest design_lock is missing")
    current_lock = {
        "seeds": list(SEEDS),
        "families_and_arms": {key: list(value) for key, value in EXPECTED_ARMS.items()},
        "valid_uids": list(args.uids),
        "excluded_uid": EXCLUDED_UID,
        "layers": list(args.layers),
        "n_folds": 5,
        "pca_rank": args.n_pca,
        "ridge_alphas": list(args.ridge_alphas),
        "nuisance_variants": NUISANCE_VARIANTS,
        "representation_pooling": "attention-mask mean",
        "condition": args.condition,
        "reference_model": args.reference_model,
        "extraction_batch_size": args.batch_size,
        "max_length": args.max_length,
    }
    if lock != current_lock:
        raise ValueError(
            "current E025 arguments/constants differ from the preflight design lock: "
            f"current={canonical_json(current_lock)} frozen={canonical_json(lock)}"
        )
    if args.wikitext_heldout.resolve() != Path(manifest["wikitext_heldout"]["path"]).resolve():
        raise ValueError("current WikiText path differs from the preflight-frozen path")

    verify_file_record(manifest["wikitext_heldout"], "WikiText heldout source")
    verify_file_record(manifest["tuckute"]["source"], "Tuckute source")
    for index, record in enumerate(manifest.get("source_run_jsons", [])):
        verify_file_record(record, f"source run JSON {index}")
    for index, record in enumerate(manifest.get("source_targets", [])):
        verify_file_record(record, f"source target cache {index}")
    verified_paths: set[str] = set()
    for alias in manifest.get("logical_aliases", []):
        records = [alias["artifact_metadata"], *alias.get("weight_files", []), *alias.get("runtime_files", [])]
        for record in records:
            path_key = str(record.get("path"))
            if path_key in verified_paths:
                continue
            label = "checkpoint artifact file"
            verify_file_record(record, label)
            verified_paths.add(path_key)


def validate_representation_cache(
    cache_path: Path,
    checkpoint: dict[str, Any],
    manifest: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    """Reject a cache unless its complete scientific identity matches this run."""
    expected = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "E025 frozen representation cache",
        "cache_key": checkpoint["cache_key"],
        "weight_sha256": checkpoint["weight_sha256"],
        "runtime_sha256": checkpoint["runtime_sha256"],
        "canonical_artifact_dir": checkpoint["canonical_artifact_dir"],
        "aliases": checkpoint["aliases"],
        "layers": list(args.layers),
        "pooling": "attention-mask mean",
        "max_length": args.max_length,
        "wikitext_ordered_text_sha256": manifest["wikitext_heldout"]["ordered_text_sha256"],
        "tuckute_ordered_text_sha256": manifest["tuckute"]["ordered_text_sha256"],
    }
    with np.load(cache_path, allow_pickle=False) as cached:
        if "metadata_json" not in cached.files:
            raise ValueError(f"representation cache lacks metadata_json: {cache_path}")
        metadata = json.loads(str(cached["metadata_json"].item()))
        for key, value in expected.items():
            if metadata.get(key) != value:
                raise ValueError(
                    f"stale representation cache {cache_path}: {key}="
                    f"{metadata.get(key)!r} != {value!r}"
                )
        expected_keys = {"metadata_json"}
        declared_array_hashes = metadata.get("array_sha256")
        if not isinstance(declared_array_hashes, dict):
            raise ValueError(f"representation cache lacks array hashes: {cache_path}")
        for corpus, n_items in (("wikitext", EXPECTED_HELDOUT_ITEMS), ("tuckute", EXPECTED_TUCKUTE_ITEMS)):
            for layer in args.layers:
                key = f"{corpus}_layer_{layer}"
                expected_keys.add(key)
                if key not in cached.files:
                    raise ValueError(f"representation cache lacks {key}: {cache_path}")
                expected_shape = (n_items, int(checkpoint["hidden_dim"]))
                if cached[key].shape != expected_shape:
                    raise ValueError(
                        f"representation cache {key} shape {cached[key].shape} != {expected_shape}"
                    )
                observed_array_sha = sha256_bytes(np.asarray(cached[key]).tobytes(order="C"))
                if declared_array_hashes.get(key) != observed_array_sha:
                    raise ValueError(f"representation cache array hash differs for {key}: {cache_path}")
        if set(cached.files) != expected_keys:
            raise ValueError(
                f"representation cache key set differs: {sorted(cached.files)} != {sorted(expected_keys)}"
            )
    if not isinstance(metadata.get("language_quality"), dict):
        raise ValueError(f"representation cache lacks language-quality measurements: {cache_path}")
    return metadata


def run_extract(manifest: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    configure_determinism()
    device = resolve_device(args.device)
    wiki_texts = read_nonempty_lines(Path(manifest["wikitext_heldout"]["path"]))[
        :int(manifest["wikitext_heldout"]["scored_prefix_lines"])
    ]
    tuckute_texts, _, covariates, tuckute_meta = load_tuckute_participants(
        resolve_path(args.data_dir), args.condition, args.uids, include_targets=False
    )
    if ordered_text_sha(wiki_texts) != manifest["wikitext_heldout"]["ordered_text_sha256"]:
        raise ValueError("WikiText ordered text hash differs from manifest")
    if ordered_text_sha(tuckute_texts) != manifest["tuckute"]["ordered_text_sha256"]:
        raise ValueError("Tuckute ordered text hash differs from manifest")
    if tuckute_meta != manifest["tuckute"]:
        raise ValueError("Tuckute source/item/participant/covariate metadata differs from manifest")

    duplicate_group_keys = {
        checkpoint["cache_key"]
        for checkpoint in manifest["unique_checkpoints"]
        if len(checkpoint["aliases"]) > 1
        and all(alias["arm"] == "kd_only" for alias in checkpoint["aliases"])
        and any(int(alias["seed"]) == 0 for alias in checkpoint["aliases"])
    }
    cache_rows: list[dict[str, Any]] = []
    duplicate_measurements: list[dict[str, Any]] = []
    for checkpoint in manifest["unique_checkpoints"]:
        cache_path = Path(checkpoint["planned_cache_npz"])
        if cache_path.exists() and not args.overwrite_cache:
            metadata = validate_representation_cache(cache_path, checkpoint, manifest, args)
            cache_rows.append({
                "cache_key": checkpoint["cache_key"],
                "weight_sha256": checkpoint["weight_sha256"],
                "path": str(cache_path),
                "sha256": sha256_file(cache_path),
                "reused": True,
                "language_quality": metadata["language_quality"],
                "aliases": checkpoint["aliases"],
            })
            if metadata.get("duplicate_extraction_noise") is not None:
                duplicate_measurements.append(metadata["duplicate_extraction_noise"])
            continue

        artifact_dir = Path(checkpoint["canonical_artifact_dir"])
        model, tokenizer = load_model_and_tokenizer(artifact_dir, device)
        wiki_rep, language_quality = forward_corpus(
            model, tokenizer, wiki_texts, args.layers, device, args.batch_size, args.max_length,
            compute_lm=True,
        )
        tuckute_rep, _ = forward_corpus(
            model, tokenizer, tuckute_texts, args.layers, device, args.batch_size, args.max_length,
            compute_lm=False,
        )

        duplicate_noise = None
        if checkpoint["cache_key"] in duplicate_group_keys:
            n_sentinel = min(args.batch_size, len(wiki_texts))
            repeated, _ = forward_corpus(
                model,
                tokenizer,
                wiki_texts[:n_sentinel],
                args.layers,
                device,
                n_sentinel,
                args.max_length,
                compute_lm=False,
            )
            per_layer = []
            for layer in args.layers:
                original = wiki_rep[layer][:n_sentinel]
                per_layer.append({
                    "layer": layer,
                    "centered_relative_frobenius": centered_relative_frobenius(original, repeated[layer]),
                    "linear_cka_distance": linear_cka_distance(original, repeated[layer]),
                })
            duplicate_noise = {
                "cache_key": checkpoint["cache_key"],
                "sentinel_items": n_sentinel,
                "definition": "repeat deterministic extraction against the first cached WikiText batch",
                "per_layer": per_layer,
            }
            duplicate_measurements.append(duplicate_noise)

        representation_arrays: dict[str, np.ndarray] = {}
        for layer in args.layers:
            representation_arrays[f"wikitext_layer_{layer}"] = wiki_rep[layer]
            representation_arrays[f"tuckute_layer_{layer}"] = tuckute_rep[layer]
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "artifact_type": "E025 frozen representation cache",
            "created_at_utc": utc_now(),
            "cache_key": checkpoint["cache_key"],
            "weight_sha256": checkpoint["weight_sha256"],
            "runtime_sha256": checkpoint["runtime_sha256"],
            "canonical_artifact_dir": checkpoint["canonical_artifact_dir"],
            "aliases": checkpoint["aliases"],
            "layers": list(args.layers),
            "pooling": "attention-mask mean",
            "max_length": args.max_length,
            "wikitext_ordered_text_sha256": manifest["wikitext_heldout"]["ordered_text_sha256"],
            "tuckute_ordered_text_sha256": manifest["tuckute"]["ordered_text_sha256"],
            "language_quality": language_quality,
            "duplicate_extraction_noise": duplicate_noise,
            "array_sha256": {
                key: sha256_bytes(value.tobytes(order="C"))
                for key, value in representation_arrays.items()
            },
        }
        arrays: dict[str, Any] = {"metadata_json": np.array(canonical_json(metadata))}
        arrays.update(representation_arrays)
        atomic_write_npz(cache_path, arrays)
        cache_rows.append({
            "cache_key": checkpoint["cache_key"],
            "weight_sha256": checkpoint["weight_sha256"],
            "path": str(cache_path),
            "sha256": sha256_file(cache_path),
            "reused": False,
            "language_quality": language_quality,
            "aliases": checkpoint["aliases"],
        })
        del model
        try:
            import torch

            if device == "cuda":
                torch.cuda.empty_cache()
        except Exception:
            pass

    nuisance = build_nuisance_cache(manifest, args, tuckute_texts, covariates, device)
    cache_by_key = {row["cache_key"]: row for row in cache_rows}
    alias_to_cache = {
        (alias["family"], int(alias["seed"]), alias["arm"]): alias["cache_key"]
        for alias in manifest["logical_aliases"]
    }
    alias_to_weight = {
        (alias["family"], int(alias["seed"]), alias["arm"]): alias["weight_sha256"]
        for alias in manifest["logical_aliases"]
    }

    max_duplicate_cka = 0.0
    max_duplicate_fro = 0.0
    for measurement in duplicate_measurements:
        for layer_row in measurement["per_layer"]:
            if int(layer_row["layer"]) != 6:
                continue
            max_duplicate_cka = max(max_duplicate_cka, float(layer_row["linear_cka_distance"]))
            max_duplicate_fro = max(
                max_duplicate_fro, float(layer_row["centered_relative_frobenius"])
            )

    movement_rows: list[dict[str, Any]] = []
    for family, arms in EXPECTED_ARMS.items():
        for seed in SEEDS:
            kd_key = alias_to_cache[(family, seed, "kd_only")]
            kd_path = Path(cache_by_key[kd_key]["path"])
            with np.load(kd_path, allow_pickle=False) as kd_cache:
                kd_arrays = {
                    (corpus, layer): np.asarray(kd_cache[f"{corpus}_layer_{layer}"])
                    for corpus in ("wikitext", "tuckute") for layer in args.layers
                }
            for arm in arms:
                if arm == "kd_only":
                    continue
                target_key = alias_to_cache[(family, seed, arm)]
                target_path = Path(cache_by_key[target_key]["path"])
                with np.load(target_path, allow_pickle=False) as target_cache:
                    for corpus in ("wikitext", "tuckute"):
                        for layer in args.layers:
                            other = np.asarray(target_cache[f"{corpus}_layer_{layer}"])
                            fro = centered_relative_frobenius(kd_arrays[(corpus, layer)], other)
                            cka = linear_cka_distance(kd_arrays[(corpus, layer)], other)
                            threshold = max(1e-6, 10.0 * max_duplicate_cka)
                            movement_rows.append({
                                "family": family,
                                "seed": seed,
                                "arm": arm,
                                "corpus": corpus,
                                "layer": layer,
                                "weight_sha256": alias_to_weight[(family, seed, arm)],
                                "kd_weight_sha256": alias_to_weight[(family, seed, "kd_only")],
                                "centered_relative_frobenius": fro,
                                "linear_cka_distance": cka,
                                "frobenius_threshold": 1e-4,
                                "cka_threshold": threshold,
                                "meets_predeclared_movement_threshold": (
                                    fro > 1e-4 and cka > threshold
                                ) if arm.endswith("_mse") and corpus == "wikitext" and layer == 6 else None,
                            })

    science = alias_science_lookup(manifest)
    direction_rows: list[dict[str, Any]] = []
    for family in EXPECTED_ARMS:
        target_arm = f"{family}_mse"
        for seed in SEEDS:
            target_r2 = science[(family, seed, target_arm)].get("target_r2")
            kd_r2 = science[(family, seed, "kd_only")].get("target_r2")
            available = target_r2 is not None and kd_r2 is not None
            delta = float(target_r2) - float(kd_r2) if available else None
            direction_rows.append({
                "family": family,
                "seed": seed,
                "arm": target_arm,
                "source": "retained E016 held-out auxiliary-target R2 with a fresh ridge head",
                "target_r2": float(target_r2) if target_r2 is not None else None,
                "kd_r2": float(kd_r2) if kd_r2 is not None else None,
                "delta_target_minus_kd": delta,
                "available": available,
                "meets_predeclared_direction_threshold": bool(available and delta > 0.0),
            })

    bpb_rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        comparisons = (
            (("tribe", "tribe_mse"), ("textfeat", "textfeat_mse"), "tribe_vs_textfeat"),
            (("tribe", "tribe_mse"), ("tribe", "kd_only"), "tribe_vs_kd"),
            (("textfeat", "textfeat_mse"), ("textfeat", "kd_only"), "textfeat_vs_kd"),
        )
        for left, right, label in comparisons:
            left_key = alias_to_cache[(left[0], seed, left[1])]
            right_key = alias_to_cache[(right[0], seed, right[1])]
            left_bpb = float(cache_by_key[left_key]["language_quality"]["bits_per_byte"])
            right_bpb = float(cache_by_key[right_key]["language_quality"]["bits_per_byte"])
            delta = left_bpb - right_bpb
            bpb_rows.append({
                "seed": seed,
                "comparison": label,
                "left": {"family": left[0], "arm": left[1], "cache_key": left_key},
                "right": {"family": right[0], "arm": right[1], "cache_key": right_key},
                "delta_bpb": delta,
                "absolute_delta_bpb": abs(delta),
                "equivalence_margin": 0.005,
                "meets_predeclared_quality_margin": abs(delta) <= 0.005,
            })

    retained_ppl_rows: list[dict[str, Any]] = []
    for alias in manifest["logical_aliases"]:
        identity = (alias["family"], int(alias["seed"]), alias["arm"])
        retained = science[identity].get("perplexity")
        cache_key = alias_to_cache[identity]
        direct = float(cache_by_key[cache_key]["language_quality"]["per_token_perplexity"])
        available = retained is not None and float(retained) > 0.0
        retained_value = float(retained) if available else None
        absolute_log_ratio = (
            abs(math.log(direct) - math.log(retained_value)) if available else None
        )
        retained_ppl_rows.append({
            "family": alias["family"],
            "seed": int(alias["seed"]),
            "arm": alias["arm"],
            "cache_key": cache_key,
            "direct_per_token_perplexity": direct,
            "retained_per_token_perplexity": retained_value,
            "absolute_log_ratio": absolute_log_ratio,
            "absolute_log_ratio_margin": 1e-5,
            "available": available,
            "reproduces_retained_perplexity": bool(
                available and absolute_log_ratio is not None and absolute_log_ratio <= 1e-5
            ),
        })

    direction_by_family: list[dict[str, Any]] = []
    for family in EXPECTED_ARMS:
        family_rows = [row for row in direction_rows if row["family"] == family]
        available = len(family_rows) == len(SEEDS) and all(row["available"] for row in family_rows)
        stats = mean_t_ci95(row["delta_target_minus_kd"] for row in family_rows) if available else None
        direction_by_family.append({
            "family": family,
            "seed_delta_t_ci95": stats,
            "all_seed_deltas_positive": bool(
                available and all(row["meets_predeclared_direction_threshold"] for row in family_rows)
            ),
            "lower_ci_exceeds_zero": bool(available and stats is not None and stats["ci95"][0] > 0.0),
        })

    primary_movement_rows = [
        row for row in movement_rows
        if row["arm"].endswith("_mse") and row["corpus"] == "wikitext" and row["layer"] == 6
    ]
    gate_summary = {
        "quality_equivalence": {
            "pass": bool(
                bpb_rows
                and all(row["meets_predeclared_quality_margin"] for row in bpb_rows)
                and retained_ppl_rows
                and all(row["reproduces_retained_perplexity"] for row in retained_ppl_rows)
            ),
            "bpb_pair_count": len(bpb_rows),
            "all_bpb_pairs_within_0p005": bool(
                bpb_rows and all(row["meets_predeclared_quality_margin"] for row in bpb_rows)
            ),
            "all_direct_ppl_reproduces_retained": bool(
                retained_ppl_rows
                and all(row["reproduces_retained_perplexity"] for row in retained_ppl_rows)
            ),
        },
        "target_direction": {
            "pass": bool(
                direction_by_family
                and all(
                    row["all_seed_deltas_positive"] and row["lower_ci_exceeds_zero"]
                    for row in direction_by_family
                )
            ),
            "per_family": direction_by_family,
        },
        "representation_movement": {
            "pass": bool(
                len(primary_movement_rows) == len(EXPECTED_ARMS) * len(SEEDS)
                and all(row["meets_predeclared_movement_threshold"] for row in primary_movement_rows)
            ),
            "primary_rows": len(primary_movement_rows),
            "expected_primary_rows": len(EXPECTED_ARMS) * len(SEEDS),
        },
        "note": "Gate booleans summarize predeclared measurements only; they do not activate a package or flip a verdict.",
    }

    manifest_path = args.manifest_path.resolve()
    extraction = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "E025 extraction measurements and cache index",
        "science_status": (
            "MEASUREMENTS ONLY: this artifact records quality/manipulation gates and frozen "
            "representations; it does not aggregate participant endpoints or flip a verdict"
        ),
        "created_at_utc": utc_now(),
        "stage": "extract",
        "device": device,
        "manifest": {"path": str(manifest_path), "sha256": sha256_file(manifest_path)},
        "ordered_inputs": {
            "wikitext_sha256": ordered_text_sha(wiki_texts),
            "tuckute_sha256": ordered_text_sha(tuckute_texts),
            "tuckute_source": tuckute_meta["source"],
        },
        "configuration": {
            "layers": list(args.layers),
            "pooling": "attention-mask mean",
            "max_length": args.max_length,
            "batch_size": args.batch_size,
            "reference_model": args.reference_model,
        },
        "cache_rows": cache_rows,
        "nuisance_cache": nuisance,
        "gate_summary": gate_summary,
        "gate_measurements": {
            "duplicate_extraction_noise": {
                "per_shared_kd_cache": duplicate_measurements,
                "max_linear_cka_distance": max_duplicate_cka,
                "max_centered_relative_frobenius": max_duplicate_fro,
            },
            "language_quality": {
                "bpb_equivalence": bpb_rows,
                "retained_perplexity_reproduction": retained_ppl_rows,
            },
            "representation_movement": movement_rows,
            "target_direction": direction_rows,
        },
    }
    atomic_write_json(args.extraction_path, extraction)
    return extraction


def _pca_fit_transform(train: np.ndarray, test: np.ndarray, rank: int) -> tuple[np.ndarray, np.ndarray]:
    if train.shape[1] == 0 or train.shape[1] <= rank:
        return train, test
    from sklearn.decomposition import PCA

    pca = PCA(n_components=min(rank, train.shape[0] - 1, train.shape[1]), random_state=0)
    return pca.fit_transform(train), pca.transform(test)


def _ridge_r2(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    alphas: tuple[float, ...],
) -> np.ndarray:
    from sklearn.linear_model import RidgeCV
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler().fit(x_train)
    y_mean = y_train.mean(axis=0, keepdims=True)
    model = RidgeCV(alphas=list(alphas))
    model.fit(scaler.transform(x_train), y_train - y_mean)
    prediction = model.predict(scaler.transform(x_test)) + y_mean
    ss_res = np.sum((y_test - prediction) ** 2, axis=0)
    ss_tot = np.sum((y_test - y_test.mean(axis=0, keepdims=True)) ** 2, axis=0)
    return 1.0 - ss_res / np.clip(ss_tot, 1e-8, None)


def precompute_pca_folds(features: np.ndarray, n_pca: int) -> list[dict[str, Any]]:
    """Fit one train-only PCA per contiguous fold for a shared feature block."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import pilot_lib as P

    folds: list[dict[str, Any]] = []
    for fold, (train, test) in enumerate(P.contiguous_folds(len(features), 5)):
        reduced_train, reduced_test = _pca_fit_transform(features[train], features[test], n_pca)
        folds.append({
            "fold": fold,
            "train": train,
            "test": test,
            "reduced_train": reduced_train,
            "reduced_test": reduced_test,
        })
    return folds


def score_precomputed_raw_folds(
    target: np.ndarray,
    scalar: np.ndarray,
    static_folds: list[dict[str, Any]],
    contextual_folds: list[dict[str, Any]],
    *,
    alphas: tuple[float, ...],
) -> list[dict[str, Any]]:
    """Fit only participant-specific ridges; all PCA work is already frozen."""
    if len(static_folds) != len(contextual_folds):
        raise ValueError("static/contextual fold counts differ")
    rows: list[dict[str, Any]] = []
    for static_fold, contextual_fold in zip(static_folds, contextual_folds):
        train = static_fold["train"]
        test = static_fold["test"]
        if (
            int(static_fold["fold"]) != int(contextual_fold["fold"])
            or not np.array_equal(train, contextual_fold["train"])
            or not np.array_equal(test, contextual_fold["test"])
        ):
            raise ValueError("static/contextual fold identity differs")
        nuisance_train = np.concatenate(
            [scalar[train], static_fold["reduced_train"]], axis=1
        )
        nuisance_test = np.concatenate(
            [scalar[test], static_fold["reduced_test"]], axis=1
        )
        full_train = np.concatenate(
            [nuisance_train, contextual_fold["reduced_train"]], axis=1
        )
        full_test = np.concatenate(
            [nuisance_test, contextual_fold["reduced_test"]], axis=1
        )
        r2_nuisance = float(np.mean(_ridge_r2(
            nuisance_train, target[train], nuisance_test, target[test], alphas
        )))
        r2_full = float(np.mean(_ridge_r2(
            full_train, target[train], full_test, target[test], alphas
        )))
        rows.append({
            "fold": int(static_fold["fold"]),
            "train_start": int(train.min()),
            "train_count": int(len(train)),
            "test_start": int(test.min()),
            "test_stop_exclusive": int(test.max()) + 1,
            "test_count": int(len(test)),
            "r2_nuisance": r2_nuisance,
            "r2_full": r2_full,
            "unique_r2": r2_full - r2_nuisance,
        })
    return rows


def scoring_equivalence_selftest() -> dict[str, Any]:
    """Deterministic plumbing proof against the canonical variance partition."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import pilot_lib as P

    rng = np.random.default_rng(20260716)
    n_items = 80
    contextual = rng.standard_normal((n_items, 60))
    static = rng.standard_normal((n_items, 55))
    scalar = rng.standard_normal((n_items, 3))
    target = rng.standard_normal((n_items, 5))
    n_pca = 10
    alphas = DEFAULT_ALPHAS
    reference = P.variance_partition(
        contextual,
        scalar,
        static,
        target,
        k_folds=5,
        alphas=alphas,
        n_pca=n_pca,
    )
    optimized = score_precomputed_raw_folds(
        target,
        scalar,
        precompute_pca_folds(static, n_pca),
        precompute_pca_folds(contextual, n_pca),
        alphas=alphas,
    )
    optimized_nuisance = float(np.mean([row["r2_nuisance"] for row in optimized]))
    optimized_full = float(np.mean([row["r2_full"] for row in optimized]))
    optimized_unique = np.asarray([row["unique_r2"] for row in optimized])
    errors = {
        "r2_nuisance": abs(optimized_nuisance - float(reference["r2_nuisance"])),
        "r2_full": abs(optimized_full - float(reference["r2_full"])),
        "unique_r2_per_fold": float(np.max(np.abs(
            optimized_unique - np.asarray(reference["unique_r2_per_fold"], dtype=np.float64)
        ))),
    }
    tolerance = 1e-10
    return {
        "pass": all(error <= tolerance for error in errors.values()),
        "tolerance": tolerance,
        "max_absolute_errors": errors,
        "fixture": {
            "seed": 20260716,
            "n_items": n_items,
            "contextual_dim": 60,
            "static_dim": 55,
            "target_dim": 5,
            "pca_rank": n_pca,
            "folds": 5,
        },
    }


def run_score(manifest: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    scorer_validation = scoring_equivalence_selftest()
    if not scorer_validation["pass"]:
        raise RuntimeError(f"optimized scorer failed canonical equivalence: {scorer_validation}")
    extraction = load_json(args.extraction_path)
    if extraction.get("schema_version") != SCHEMA_VERSION or extraction.get("stage") != "extract":
        raise ValueError("extraction index has the wrong schema/stage")
    if extraction["manifest"]["sha256"] != sha256_file(args.manifest_path):
        raise ValueError("extraction index was produced from a different manifest")
    expected_extraction_configuration = {
        "layers": list(args.layers),
        "pooling": "attention-mask mean",
        "max_length": args.max_length,
        "batch_size": args.batch_size,
        "reference_model": args.reference_model,
    }
    if extraction.get("configuration") != expected_extraction_configuration:
        raise ValueError("extraction configuration differs from the preflight-bound score configuration")

    texts, targets, _, tuckute_meta = load_tuckute_participants(
        resolve_path(args.data_dir), args.condition, args.uids, include_targets=True
    )
    if ordered_text_sha(texts) != manifest["tuckute"]["ordered_text_sha256"]:
        raise ValueError("Tuckute ordered texts changed before score stage")
    if tuckute_meta != manifest["tuckute"]:
        raise ValueError(
            "Tuckute source/item/participant/covariate metadata differs from manifest before score stage"
        )

    nuisance_path = Path(extraction["nuisance_cache"]["path"])
    if extraction["nuisance_cache"]["sha256"] != sha256_file(nuisance_path):
        raise ValueError("nuisance cache hash mismatch")
    with np.load(nuisance_path, allow_pickle=False) as nuisance:
        base_scalar = np.asarray(nuisance["base_scalar"], dtype=np.float64)
        static_embedding = np.asarray(nuisance["static_embedding"], dtype=np.float64)
        imageability = np.asarray(nuisance["imageability"], dtype=np.float64)
        full_cov_extra = np.asarray(nuisance["full_cov_extra"], dtype=np.float64)

    variants = {
        "primary": base_scalar,
        "imageability": np.concatenate([base_scalar, imageability], axis=1),
        "full_cov": np.concatenate([base_scalar, full_cov_extra], axis=1),
    }
    static_folds = precompute_pca_folds(static_embedding, args.n_pca)
    cache_index = {row["cache_key"]: row for row in extraction["cache_rows"]}
    aliases_by_cache: dict[str, list[dict[str, Any]]] = {}
    for alias in manifest["logical_aliases"]:
        aliases_by_cache.setdefault(alias["cache_key"], []).append(alias)

    raw_rows: list[dict[str, Any]] = []
    for cache_key, aliases in sorted(aliases_by_cache.items()):
        cache_row = cache_index[cache_key]
        cache_path = Path(cache_row["path"])
        if cache_row["sha256"] != sha256_file(cache_path):
            raise ValueError(f"representation cache hash mismatch: {cache_path}")
        with np.load(cache_path, allow_pickle=False) as cached:
            metadata = json.loads(str(cached["metadata_json"].item()))
            if metadata["aliases"] != next(
                checkpoint["aliases"] for checkpoint in manifest["unique_checkpoints"]
                if checkpoint["cache_key"] == cache_key
            ):
                raise ValueError(f"cache aliases do not match manifest: {cache_key}")
            for layer in args.layers:
                contextual = np.asarray(cached[f"tuckute_layer_{layer}"], dtype=np.float64)
                if contextual.shape[0] != len(texts):
                    raise ValueError(f"cache row count mismatch: {cache_key} layer={layer}")
                contextual_folds = precompute_pca_folds(contextual, args.n_pca)
                for uid in args.uids:
                    target = targets[uid].astype(np.float64, copy=False)
                    for nuisance_variant, scalar in variants.items():
                        fold_rows = score_precomputed_raw_folds(
                            target,
                            scalar,
                            static_folds,
                            contextual_folds,
                            alphas=args.ridge_alphas,
                        )
                        for alias in aliases:
                            for fold_row in fold_rows:
                                raw_rows.append({
                                    "uid": uid,
                                    "seed": int(alias["seed"]),
                                    "family": alias["family"],
                                    "arm": alias["arm"],
                                    "layer": layer,
                                    "nuisance_variant": nuisance_variant,
                                    "fold": fold_row["fold"],
                                    "unique_r2": fold_row["unique_r2"],
                                    "r2_nuisance": fold_row["r2_nuisance"],
                                    "r2_full": fold_row["r2_full"],
                                    "weight_sha256": alias["weight_sha256"],
                                    "cache_key": cache_key,
                                    "train_count": fold_row["train_count"],
                                    "test_start": fold_row["test_start"],
                                    "test_stop_exclusive": fold_row["test_stop_exclusive"],
                                    "test_count": fold_row["test_count"],
                                })

    expected_rows = 36 * len(args.uids) * len(args.layers) * len(variants) * 5
    if len(raw_rows) != expected_rows:
        raise RuntimeError(f"raw score row count mismatch: {len(raw_rows)} != {expected_rows}")
    output = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "E025 raw participant fold scores",
        "science_status": (
            "RAW FOLD ROWS ONLY: no participant/seed/fold aggregation, uncertainty, contrast, "
            "activation decision, or project verdict is present"
        ),
        "created_at_utc": utc_now(),
        "stage": "score",
        "manifest": {"path": str(args.manifest_path), "sha256": sha256_file(args.manifest_path)},
        "extraction": {"path": str(args.extraction_path), "sha256": sha256_file(args.extraction_path)},
        "data": {
            "condition": args.condition,
            "ordered_text_sha256": ordered_text_sha(texts),
            "source": tuckute_meta["source"],
            "uids": list(args.uids),
            "rois": list(TUCKUTE_ROIS),
        },
        "scoring": {
            "layers": list(args.layers),
            "nuisance_variants": NUISANCE_VARIANTS,
            "n_folds": 5,
            "folding": "five deterministic contiguous heldout blocks",
            "pca_rank": args.n_pca,
            "pca_fit": "training fold only, separately for static and contextual blocks",
            "ridge_alphas": list(args.ridge_alphas),
            "ridge_selection": "RidgeCV fit on the training fold only",
            "target_aggregation": "mean R2 across the five fixed LH language sub-ROIs within fold",
        },
        "scorer_validation": scorer_validation,
        "raw_row_count": len(raw_rows),
        "rows": raw_rows,
    }
    atomic_write_json(args.score_path, output)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "E025 staged saved-student participant transfer harness. Run manifest first; "
            "manifest never loads model weights or computes scientific measurements."
        )
    )
    parser.add_argument("--stage", choices=("manifest", "extract", "score", "all"), default="manifest")
    parser.add_argument(
        "--run-json",
        action="append",
        type=Path,
        help="E016 run JSON; repeat three times. Defaults to the locked E025 sources.",
    )
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--manifest-path", type=Path)
    parser.add_argument("--extraction-path", type=Path)
    parser.add_argument("--score-path", type=Path)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--wikitext-heldout", type=Path, default=DEFAULT_WIKITEXT)
    parser.add_argument("--condition", default="B")
    parser.add_argument("--uids", default=",".join(map(str, VALID_UIDS)))
    parser.add_argument("--layers", default=",".join(map(str, DEFAULT_LAYERS)))
    parser.add_argument("--reference-model", default="gpt2-medium")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=64)
    parser.add_argument("--n-pca", type=int, default=50)
    parser.add_argument("--ridge-alphas", default=",".join(map(str, DEFAULT_ALPHAS)))
    parser.add_argument(
        "--overwrite-cache",
        action="store_true",
        help="Recompute representation/nuisance caches during extract. JSON indexes are always atomic.",
    )
    args = parser.parse_args()
    args.out_dir = resolve_path(args.out_dir).resolve()
    args.manifest_path = resolve_path(args.manifest_path).resolve() if args.manifest_path else (
        args.out_dir / "manifest.json"
    )
    args.extraction_path = resolve_path(args.extraction_path).resolve() if args.extraction_path else (
        args.out_dir / "extraction.json"
    )
    args.score_path = resolve_path(args.score_path).resolve() if args.score_path else (
        args.out_dir / "raw_folds.json"
    )
    args.data_dir = resolve_path(args.data_dir).resolve()
    args.wikitext_heldout = resolve_path(args.wikitext_heldout).resolve()
    args.uids = parse_csv_ints(args.uids)
    args.layers = parse_csv_ints(args.layers)
    args.ridge_alphas = parse_csv_floats(args.ridge_alphas)
    if args.uids != VALID_UIDS:
        raise ValueError(f"E025 valid UID lock is {VALID_UIDS}; received {args.uids}")
    if args.layers != DEFAULT_LAYERS:
        raise ValueError(f"E025 fixed layers are {DEFAULT_LAYERS}; received {args.layers}")
    if args.n_pca != 50:
        raise ValueError("E025 capacity-fair PCA rank is locked to 50")
    if args.batch_size < 1 or args.max_length < 2:
        raise ValueError("batch size must be positive and max length at least two")
    return args


def main() -> None:
    args = parse_args()
    manifest: dict[str, Any]
    if args.stage in ("manifest", "all"):
        manifest = build_manifest(args)
        atomic_write_json(args.manifest_path, manifest)
        print(json.dumps({
            "stage": "manifest",
            "preflight_pass": True,
            "manifest": str(args.manifest_path),
            "manifest_sha256": sha256_file(args.manifest_path),
            "logical_aliases": len(manifest["logical_aliases"]),
            "unique_checkpoints": len(manifest["unique_checkpoints"]),
            "valid_participants": len(manifest["tuckute"]["participants"]),
            "model_weights_loaded": False,
            "science_computed": False,
        }, indent=2))
    else:
        manifest = load_json(args.manifest_path)
        verify_manifest(manifest, args)

    if args.stage in ("extract", "all"):
        verify_manifest(manifest, args)
        extraction = run_extract(manifest, args)
        print(json.dumps({
            "stage": "extract",
            "extraction": str(args.extraction_path),
            "checkpoint_caches": len(extraction["cache_rows"]),
            "verdict_flipped": False,
        }, indent=2))

    if args.stage in ("score", "all"):
        verify_manifest(manifest, args)
        scored = run_score(manifest, args)
        print(json.dumps({
            "stage": "score",
            "raw_folds": str(args.score_path),
            "raw_row_count": scored["raw_row_count"],
            "aggregates_computed": False,
            "verdict_flipped": False,
        }, indent=2))


if __name__ == "__main__":
    main()
