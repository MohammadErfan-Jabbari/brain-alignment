#!/usr/bin/env python3
"""Build long-context non-brain target caches for a possible E016 control.

This is the context-conditioned counterpart to ``build_text_feature_target_cache``.
It conditions a frozen LM on recovered preceding WikiText context, then pools the
hidden states over the target sentence tokens and projects them into the same
target-cache schema used by ``run_tribe_phase3.py``.

Use only after E016 and the sentence-local textfeat control justify the extra
burden. Smoke tests with ``--device cpu`` are safe; full caches are not launched
by this helper automatically.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pilot_lib as P  # noqa: E402

OUT_ROOT = ROOT / "outputs/E016_tribe/kd_targets/context_feature"
CORPORA = {
    "train": ROOT / "data/kd_corpus/wikitext103_sentences_train.txt",
    "heldout": ROOT / "data/kd_corpus/wikitext103_sentences_heldout.txt",
}
META_FILES = {
    "train": ROOT / "outputs/E016_tribe/kd_context_metadata/wikitext103_train_context_meta.jsonl",
    "heldout": ROOT / "outputs/E016_tribe/kd_context_metadata/wikitext103_heldout_context_meta.jsonl",
}


def model_tag(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "--", name).strip("-")


def read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} missing; run scripts/e016_recover_kd_context_metadata.py first"
        )
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_metadata() -> tuple[dict[str, list[dict[str, Any]]], dict[int, dict[str, Any]]]:
    by_split: dict[str, list[dict[str, Any]]] = {}
    by_global: dict[int, dict[str, Any]] = {}
    for split, path in META_FILES.items():
        rows = load_jsonl(path)
        by_split[split] = rows
        for row in rows:
            by_global[int(row["global_accepted_index"])] = row
    return by_split, by_global


def load_selected(split: str, corpus: Path, start: int, limit: int | None) -> tuple[list[str], np.ndarray]:
    lines = read_lines(corpus)
    end = len(lines) if limit is None else min(len(lines), start + limit)
    keep = [(i, lines[i]) for i in range(start, end) if lines[i].strip()]
    return [text for _, text in keep], np.array([i for i, _ in keep], dtype=np.int64)


def context_indices(
    row: dict[str, Any],
    by_global: dict[int, dict[str, Any]],
    max_sentences: int,
) -> list[int]:
    out: list[int] = []
    prev = row.get("previous_same_doc_global_index")
    while prev is not None and len(out) < max_sentences:
        prev = int(prev)
        if prev not in by_global:
            break
        out.append(prev)
        prev = by_global[prev].get("previous_same_doc_global_index")
    return list(reversed(out))


def context_text(
    row: dict[str, Any],
    by_global: dict[int, dict[str, Any]],
    max_sentences: int,
    max_chars: int,
) -> tuple[str, list[int]]:
    idxs = context_indices(row, by_global, max_sentences)
    pieces = [by_global[i]["text"] for i in idxs]
    text = " ".join(pieces).strip()
    if len(text) > max_chars:
        text = text[-max_chars:]
    return text, idxs


def load_lm(name: str, device: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(name).to(device).eval()
    for param in model.parameters():
        param.requires_grad_(False)
    return model, tok


def build_ids(tok, context: str, target: str, max_length: int) -> tuple[list[int], int]:
    target_ids = tok(target, add_special_tokens=False).input_ids
    if not target_ids:
        target_ids = tok(tok.eos_token, add_special_tokens=False).input_ids
    if len(target_ids) >= max_length:
        ids = target_ids[-max_length:]
        return ids, 0
    context_ids = tok(context, add_special_tokens=False).input_ids if context else []
    sep_ids = tok("\n\n", add_special_tokens=False).input_ids if context_ids else []
    room = max_length - len(target_ids)
    prefix = (context_ids + sep_ids)[-room:] if room > 0 else []
    ids = prefix + target_ids
    return ids, len(prefix)


def extract_contextual_features(
    model,
    tok,
    texts: list[str],
    contexts: list[str],
    *,
    layer: int,
    max_length: int,
    batch_size: int,
    pool: str,
    device: str,
) -> np.ndarray:
    feats: list[np.ndarray] = []
    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start : start + batch_size]
        batch_contexts = contexts[start : start + batch_size]
        encoded = [build_ids(tok, ctx, txt, max_length) for ctx, txt in zip(batch_contexts, batch_texts, strict=True)]
        lengths = [len(ids) for ids, _ in encoded]
        max_len = max(lengths)
        pad_id = tok.pad_token_id
        input_ids = torch.full((len(encoded), max_len), pad_id, dtype=torch.long, device=device)
        attn = torch.zeros((len(encoded), max_len), dtype=torch.long, device=device)
        for i, (ids, _) in enumerate(encoded):
            input_ids[i, : len(ids)] = torch.tensor(ids, dtype=torch.long, device=device)
            attn[i, : len(ids)] = 1
        with torch.no_grad():
            out = model(input_ids=input_ids, attention_mask=attn, output_hidden_states=True)
            hidden = out.hidden_states[layer].detach().cpu().numpy()
        for i, ((_, target_start), seq_len) in enumerate(zip(encoded, lengths, strict=True)):
            target_hidden = hidden[i, target_start:seq_len]
            if pool == "mean":
                feats.append(target_hidden.mean(axis=0).astype(np.float32))
            elif pool == "last":
                feats.append(target_hidden[-1].astype(np.float32))
            else:
                raise ValueError(f"unknown pool: {pool}")
    return np.stack(feats).astype(np.float32)


def random_project(X: np.ndarray, target_dim: int, seed: int) -> tuple[np.ndarray, dict[str, Any]]:
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


def first_dims(X: np.ndarray, target_dim: int) -> tuple[np.ndarray, dict[str, Any]]:
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
    ap.add_argument("--max-length", type=int, default=128)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--context-sentences", type=int, default=4)
    ap.add_argument("--max-context-chars", type=int, default=4096)
    ap.add_argument("--target-dim", type=int, default=20484)
    ap.add_argument("--projection", choices=["random", "first-dims"], default="random")
    ap.add_argument("--projection-seed", type=int, default=0)
    ap.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    if args.target_dim <= 0:
        raise ValueError("--target-dim must be positive")
    if args.context_sentences < 0:
        raise ValueError("--context-sentences must be non-negative")

    corpus = args.corpus or CORPORA[args.split]
    texts, item_indices = load_selected(args.split, corpus, args.start, args.limit)
    if not texts:
        raise SystemExit("No non-empty texts selected")
    by_split, by_global = load_metadata()
    split_rows = by_split[args.split]
    rows = [split_rows[int(i)] for i in item_indices]
    for text, row in zip(texts, rows, strict=True):
        if text != row["text"]:
            raise SystemExit(
                f"context metadata mismatch at split_index={row['split_index']}: {text!r} != {row['text']!r}"
            )
    contexts, context_ids = [], []
    for row in rows:
        ctx, ids = context_text(row, by_global, args.context_sentences, args.max_context_chars)
        contexts.append(ctx)
        context_ids.append(ids)

    device = P.pick_device() if args.device == "auto" else args.device
    t0 = time.time()
    model, tok = load_lm(args.model, device)
    layer = P.middle_layer_index(model) if args.layer < 0 else args.layer
    X = extract_contextual_features(
        model,
        tok,
        texts,
        contexts,
        layer=layer,
        max_length=args.max_length,
        batch_size=args.batch_size,
        pool=args.pool,
        device=device,
    )
    if args.projection == "random":
        targets, projection_meta = random_project(X, args.target_dim, args.projection_seed)
    else:
        targets, projection_meta = first_dims(X, args.target_dim)

    out = args.out or default_out(args.split, args.model, args.start, len(texts), args.target_dim, layer)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not args.overwrite:
        raise FileExistsError(f"refusing to overwrite existing cache: {out}; pass --overwrite")

    context_counts = np.array([len(ids) for ids in context_ids], dtype=np.int32)
    source_global_indices = np.array([int(r["global_accepted_index"]) for r in rows], dtype=np.int64)
    meta = {
        "experiment": "E016 long-context non-brain target cache",
        "science_status": "non-brain context-feature target cache only; not a Phase-3 result",
        "split": args.split,
        "corpus": str(corpus),
        "start": args.start,
        "n_items": len(texts),
        "model": args.model,
        "layer": layer,
        "pool": args.pool,
        "max_length": args.max_length,
        "batch_size": args.batch_size,
        "context_sentences": args.context_sentences,
        "max_context_chars": args.max_context_chars,
        "context_metadata": str(META_FILES[args.split]),
        "target_dim": int(targets.shape[1]),
        "vertex_index": "synthetic dimensions stored in npz",
        "projection": projection_meta,
        "context_items_with_previous": int((context_counts > 0).sum()),
        "elapsed_s": round(time.time() - t0, 3),
    }
    np.savez_compressed(
        out,
        targets=targets,
        texts=np.array(texts, dtype=str),
        item_indices=item_indices,
        source_global_indices=source_global_indices,
        context_counts=context_counts,
        vertex_index=np.arange(targets.shape[1], dtype=np.int64),
        segment_counts=np.ones(len(texts), dtype=np.int32),
        metadata=json.dumps(meta, sort_keys=True),
    )
    out.with_suffix(".json").write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    print(f"saved {out}")
    print(f"shape={targets.shape} context_items_with_previous={meta['context_items_with_previous']} elapsed_s={meta['elapsed_s']}")


if __name__ == "__main__":
    main()
