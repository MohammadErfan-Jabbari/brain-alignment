#!/usr/bin/env python3
"""Evaluate saved E016 student artifacts on the real Tuckute alignment endpoint.

This is a post-hoc infrastructure helper, not a verdict engine. It reads an
E016-style run JSON, loads rows with `model_artifact_dir`, and scores each saved
student with the same contiguous-CV, nuisance-subtracted variance partition used
by the E003 KD-alignment harness.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P  # noqa: E402
from data_adapters import load_tuckute  # noqa: E402
from run_kd_alignment import layers_to_probe, verdict_layer  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data/tuckute2024"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=(
            "Score saved E016 student artifacts on Tuckute real-brain alignment. "
            "Outputs diagnostics for /interpret; it never flips a verdict."
        )
    )
    ap.add_argument("--run-json", required=True, type=Path,
                    help="E016-style run JSON containing rows with model_artifact_dir.")
    ap.add_argument("--out", type=Path,
                    help="Output JSON. Default: <run-json>.tuckute_alignment.json")
    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                    help="Tuckute data directory.")
    ap.add_argument("--condition", default="B",
                    help="Tuckute condition passed to load_tuckute.")
    ap.add_argument("--target", default="subrois",
                    help="Tuckute target passed to load_tuckute.")
    ap.add_argument("--reference-model", default="gpt2-medium",
                    help="Fixed model for scalar/static nuisance features.")
    ap.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    ap.add_argument("--limit-rows", type=int,
                    help="Score only the first N artifact-bearing rows.")
    ap.add_argument("--max-length", type=int, default=64)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--n-pca", type=int, default=50)
    ap.add_argument("--pca-robust", default="25,50,100",
                    help="Comma-separated PCA component counts at the verdict layer.")
    ap.add_argument("--require-artifacts", action="store_true",
                    help="Fail if any row lacks a readable model artifact directory.")
    ap.add_argument("--include-missing", action="store_true",
                    help="Emit skipped rows for missing artifacts instead of silently ignoring them.")
    return ap.parse_args()


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def resolve_device(choice: str) -> str:
    if choice == "auto":
        return P.pick_device()
    return choice


def parse_int_list(raw: str) -> tuple[int, ...]:
    vals = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        vals.append(int(part))
    if not vals:
        raise ValueError("--pca-robust must contain at least one integer")
    return tuple(vals)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def ensure_pad_token(tokenizer) -> None:
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token


def load_model_and_tokenizer(model_ref: str | Path, device: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_ref = str(model_ref)
    tok = AutoTokenizer.from_pretrained(model_ref)
    ensure_pad_token(tok)
    model = AutoModelForCausalLM.from_pretrained(model_ref).to(device).eval()
    return model, tok


def score_saved_model(
    model,
    tokenizer,
    texts: list[str],
    Y: np.ndarray,
    Z: np.ndarray,
    S_fixed: np.ndarray,
    device: str,
    max_length: int,
    batch_size: int,
    n_pca: int,
    pca_robust: tuple[int, ...],
) -> tuple[list[dict[str, Any]], int, dict[str, Any]]:
    ext = P.ExtractConfig(pool="mean", max_length=max_length, batch_size=batch_size)
    vl = verdict_layer(model)
    recs: list[dict[str, Any]] = []
    verdict = None
    for layer in layers_to_probe(model):
        X = P.extract_hidden_states(model, tokenizer, texts, ext, device, layer=layer)
        part = P.variance_partition(X, Z, S_fixed, Y, k_folds=5, n_pca=n_pca)
        rec: dict[str, Any] = {
            "layer": layer,
            "unique_r2": part["unique_r2"],
            "unique_r2_std": part["unique_r2_std"],
            "unique_r2_per_fold": part["unique_r2_per_fold"],
            "r2_nuisance": part["r2_nuisance"],
            "r2_full": part["r2_full"],
        }
        if layer == vl:
            rec["pca_robustness"] = {}
            for npca in pca_robust:
                p = P.variance_partition(X, Z, S_fixed, Y, k_folds=5, n_pca=npca)
                rec["pca_robustness"][str(npca)] = {
                    "unique_r2": p["unique_r2"],
                    "unique_r2_std": p["unique_r2_std"],
                }
            verdict = rec
        recs.append(rec)
    if verdict is None:
        raise RuntimeError(f"verdict layer {vl} was not scored")
    return recs, vl, verdict


def artifact_status(row: dict[str, Any]) -> tuple[str, Path | None]:
    raw = row.get("model_artifact_dir")
    if not raw:
        return "missing_model_artifact_dir", None
    artifact_dir = resolve_path(Path(raw))
    if not artifact_dir.exists():
        return "artifact_dir_not_found", artifact_dir
    if not artifact_dir.is_dir():
        return "artifact_path_not_directory", artifact_dir
    return "ready", artifact_dir


def row_identity(row: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "arm",
        "seed",
        "lambda_brain",
        "perplexity",
        "target_r2",
        "target_dim",
        "n_train",
        "n_heldout_ppl",
        "model_artifact_dir",
    )
    return {k: row.get(k) for k in keep if k in row}


def summarize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[float]] = {}
    for row in rows:
        if row.get("status") != "scored":
            continue
        arm = str(row.get("arm", "unknown"))
        grouped.setdefault(arm, []).append(float(row["verdict"]["unique_r2"]))
    summary = []
    for arm, vals in sorted(grouped.items()):
        arr = np.array(vals, dtype=np.float64)
        summary.append({
            "arm": arm,
            "n": int(arr.size),
            "verdict_unique_r2_mean": float(arr.mean()),
            "verdict_unique_r2_std": float(arr.std(ddof=1)) if arr.size > 1 else 0.0,
            "verdict_unique_r2_values": arr.tolist(),
        })
    return summary


def main() -> None:
    args = parse_args()
    t0 = time.time()
    run_json = resolve_path(args.run_json)
    out_path = resolve_path(args.out) if args.out else run_json.with_suffix(
        run_json.suffix + ".tuckute_alignment.json"
    )
    pca_robust = parse_int_list(args.pca_robust)
    device = resolve_device(args.device)

    data = load_json(run_json)
    rows = data.get("rows")
    if not isinstance(rows, list):
        raise ValueError(f"{run_json} does not contain a list-valued `rows` field")

    texts, Y, meta = load_tuckute(str(resolve_path(args.data_dir)),
                                  condition=args.condition,
                                  target=args.target)

    reference_model, reference_tok = load_model_and_tokenizer(args.reference_model, device)
    Z = P.scalar_nuisance(texts, reference_tok)
    S_fixed = P.static_embedding_features(reference_model, reference_tok, texts, device)
    del reference_model

    scored_rows: list[dict[str, Any]] = []
    artifact_rows_seen = 0
    missing_rows = 0

    for row in rows:
        status, artifact_dir = artifact_status(row)
        if status != "ready":
            missing_rows += 1
            if args.require_artifacts:
                raise FileNotFoundError(f"row artifact unavailable: {status} {artifact_dir}")
            if args.include_missing:
                skipped = row_identity(row)
                skipped.update({
                    "status": status,
                    "resolved_model_artifact_dir": str(artifact_dir) if artifact_dir else None,
                })
                scored_rows.append(skipped)
            continue
        if args.limit_rows is not None and artifact_rows_seen >= args.limit_rows:
            continue
        artifact_rows_seen += 1

        model, tok = load_model_and_tokenizer(artifact_dir, device)
        per_layer, vl, verdict = score_saved_model(
            model=model,
            tokenizer=tok,
            texts=texts,
            Y=Y,
            Z=Z,
            S_fixed=S_fixed,
            device=device,
            max_length=args.max_length,
            batch_size=args.batch_size,
            n_pca=args.n_pca,
            pca_robust=pca_robust,
        )
        result = row_identity(row)
        result.update({
            "status": "scored",
            "resolved_model_artifact_dir": str(artifact_dir),
            "verdict_layer": vl,
            "verdict": verdict,
            "per_layer": per_layer,
        })
        scored_rows.append(result)
        del model

    artifact_rows_scored = sum(1 for row in scored_rows if row.get("status") == "scored")
    output = {
        "science_status": (
            "post_hoc_real_brain_alignment_diagnostic_only; requires /interpret and "
            "does not by itself establish an E016 verdict"
        ),
        "source_run_json": str(run_json),
        "created_at_unix": time.time(),
        "elapsed_s": time.time() - t0,
        "device": device,
        "data": {
            "dataset": "tuckute2024",
            "data_dir": str(resolve_path(args.data_dir)),
            "condition": args.condition,
            "target": args.target,
            "n_items": len(texts),
            "target_shape": list(Y.shape),
            "meta_keys": sorted(meta.keys()),
            "noise_ceiling_langnetw": meta.get("noise_ceiling_langnetw"),
        },
        "reference_nuisance_model": args.reference_model,
        "scoring": {
            "protocol": (
                "contiguous 5-fold variance partition; unique contextual R2 over "
                "length, position, and fixed static embedding nuisance"
            ),
            "max_length": args.max_length,
            "batch_size": args.batch_size,
            "n_pca": args.n_pca,
            "pca_robust": list(pca_robust),
        },
        "row_counts": {
            "input_rows": len(rows),
            "missing_or_unusable_artifact_rows": missing_rows,
            "artifact_rows_considered": artifact_rows_seen,
            "artifact_rows_scored": artifact_rows_scored,
        },
        "by_arm": summarize_rows(scored_rows),
        "rows": scored_rows,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "out": str(out_path),
        "artifact_rows_scored": artifact_rows_scored,
        "missing_or_unusable_artifact_rows": missing_rows,
    }, indent=2))


if __name__ == "__main__":
    main()
