#!/usr/bin/env python3
"""Build non-brain stimulus-derived target caches for E016 Phase-3 controls.

The cache schema matches ``tribe_predict_kd_corpus.py`` so the Phase-3 runner can
train a matched-information control by passing this file as ``--target-cache``
with ``--target-label textfeat``. Targets are frozen LM hidden states projected
to the requested dimensionality; they contain only information available from
the stimulus text, not neural recordings.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pilot_lib as P  # noqa: E402

OUT_ROOT = ROOT / "outputs/E016_tribe/kd_targets/text_feature"
CORPORA = {
    "train": ROOT / "data/kd_corpus/wikitext103_sentences_train.txt",
    "heldout": ROOT / "data/kd_corpus/wikitext103_sentences_heldout.txt",
}


def model_tag(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "--", name).strip("-")


def load_texts(path: Path, start: int, limit: int | None) -> tuple[list[str], np.ndarray]:
    lines = path.read_text(encoding="utf-8").splitlines()
    end = len(lines) if limit is None else min(len(lines), start + limit)
    keep = [(start + i, line.strip()) for i, line in enumerate(lines[start:end]) if line.strip()]
    return [text for _, text in keep], np.array([i for i, _ in keep], dtype=np.int64)


def load_lm(name: str, device: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(name).to(device).eval()
    return model, tok


def random_project(X: np.ndarray, target_dim: int, seed: int) -> tuple[np.ndarray, dict]:
    rng = np.random.default_rng(seed)
    scale = 1.0 / np.sqrt(max(1, X.shape[1]))
    proj = rng.standard_normal((X.shape[1], target_dim), dtype=np.float32) * scale
    Y = X.astype(np.float32) @ proj
    meta = {
        "projection": "gaussian_random_projection",
        "projection_seed": seed,
        "source_dim": int(X.shape[1]),
        "target_dim": int(target_dim),
        "scale": scale,
    }
    return Y.astype(np.float32), meta


def first_dims(X: np.ndarray, target_dim: int) -> tuple[np.ndarray, dict]:
    if target_dim > X.shape[1]:
        raise ValueError("first-dims projection requires --target-dim <= hidden dimension")
    meta = {
        "projection": "first_dims",
        "source_dim": int(X.shape[1]),
        "target_dim": int(target_dim),
    }
    return X[:, :target_dim].astype(np.float32), meta


def default_out(split: str, model_name: str, start: int, n_items: int, target_dim: int, layer: int) -> Path:
    return OUT_ROOT / model_tag(model_name) / f"{split}_start{start}_n{n_items}_d{target_dim}_layer{layer}.npz"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=sorted(CORPORA), default="train")
    ap.add_argument("--corpus", type=Path, default=None)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--model", default="gpt2-medium")
    ap.add_argument("--layer", type=int, default=-1, help="-1 means model middle layer")
    ap.add_argument("--pool", choices=["mean", "last"], default="mean")
    ap.add_argument("--max-length", type=int, default=64)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--target-dim", type=int, default=20484)
    ap.add_argument("--projection", choices=["random", "first-dims"], default="random")
    ap.add_argument("--projection-seed", type=int, default=0)
    ap.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if args.target_dim <= 0:
        raise ValueError("--target-dim must be positive")
    corpus = args.corpus or CORPORA[args.split]
    texts, item_indices = load_texts(corpus, args.start, args.limit)
    if not texts:
        raise SystemExit("No non-empty texts selected")

    device = P.pick_device() if args.device == "auto" else args.device
    t0 = time.time()
    model, tok = load_lm(args.model, device)
    layer = P.middle_layer_index(model) if args.layer < 0 else args.layer
    cfg = P.ExtractConfig(pool=args.pool, max_length=args.max_length, batch_size=args.batch_size)
    X = P.extract_hidden_states(model, tok, texts, cfg, device, layer=layer)
    if args.projection == "random":
        targets, projection_meta = random_project(X, args.target_dim, args.projection_seed)
    else:
        targets, projection_meta = first_dims(X, args.target_dim)

    out = args.out or default_out(args.split, args.model, args.start, len(texts), args.target_dim, layer)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise FileExistsError(f"refusing to overwrite existing cache: {out}")

    meta = {
        "experiment": "E016 matched-information non-brain target cache",
        "split": args.split,
        "corpus": str(corpus),
        "start": args.start,
        "n_items": len(texts),
        "model": args.model,
        "layer": layer,
        "pool": args.pool,
        "max_length": args.max_length,
        "batch_size": args.batch_size,
        "target_dim": int(targets.shape[1]),
        "vertex_index": "synthetic dimensions stored in npz",
        "projection": projection_meta,
        "elapsed_s": round(time.time() - t0, 3),
        "science_status": "non-brain control target cache only; not a Phase-3 result",
    }
    np.savez_compressed(
        out,
        targets=targets,
        texts=np.array(texts, dtype=str),
        item_indices=item_indices,
        vertex_index=np.arange(targets.shape[1], dtype=np.int64),
        segment_counts=np.ones(len(texts), dtype=np.int32),
        metadata=json.dumps(meta, sort_keys=True),
    )
    out.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"saved {out}")
    print(f"shape={targets.shape} elapsed_s={meta['elapsed_s']}")


if __name__ == "__main__":
    main()
