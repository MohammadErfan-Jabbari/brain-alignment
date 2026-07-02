#!/usr/bin/env python3
"""E016 Phase 3 target builder: TRIBE-v2 predictions for the KD corpus.

Run this from the isolated TRIBE checkout, not the thesis uv environment:

    cd /home/centcom/data/brain-alignment/data/paper-repos/tribev2
    CUDA_VISIBLE_DEVICES=1 .venv-tribe/bin/python \
        /home/centcom/data/brain-alignment/scripts/tribe_predict_kd_corpus.py \
        --split train --start 0 --limit 8 --target-dim 64

The cache path is ``--event-mode synthetic-text``. It bypasses gTTS/ASR by
constructing timed Word events directly and running TRIBE with
``features_to_use=["text"]``. The slower ``tts-single`` mode is retained only as
a fidelity/debug fallback against TRIBE's public text_path route.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

THESIS = Path("/home/centcom/data/brain-alignment")
TRIBE_CACHE = "/home/centcom/data/tribe_cache"
OUT_ROOT = THESIS / "outputs/E016_tribe/kd_targets"
CORPORA = {
    "train": THESIS / "data/kd_corpus/wikitext103_sentences_train.txt",
    "heldout": THESIS / "data/kd_corpus/wikitext103_sentences_heldout.txt",
}
N_VERTICES = 20484


def load_texts(path: Path, start: int, limit: int | None) -> tuple[list[str], np.ndarray]:
    lines = path.read_text(encoding="utf-8").splitlines()
    end = len(lines) if limit is None else min(len(lines), start + limit)
    texts = [line.strip() for line in lines[start:end]]
    keep = [(start + i, text) for i, text in enumerate(texts) if text]
    return [text for _, text in keep], np.array([i for i, _ in keep], dtype=np.int64)


def words(text: str) -> list[str]:
    toks = re.findall(r"\w+(?:[-@.]\w+)*|[^\w\s]", text, flags=re.UNICODE)
    return toks or [text.strip() or "."]


def context_for(words_: list[str], idx: int, max_chars: int = 4096) -> str:
    ctx = " ".join(words_[: idx + 1]).strip()
    return ctx[-max_chars:] if len(ctx) > max_chars else ctx


def synthetic_word_events(
    texts: list[str],
    item_indices: np.ndarray,
    *,
    word_duration: float,
    word_gap: float,
    min_duration: float,
) -> tuple[pd.DataFrame, dict[str, int]]:
    rows: list[dict] = []
    timeline_to_item: dict[str, int] = {}
    for local_i, (global_i, text) in enumerate(zip(item_indices, texts, strict=True)):
        timeline = f"item_{int(global_i):08d}"
        timeline_to_item[timeline] = local_i
        start = 0.0
        toks = words(text)
        for j, tok in enumerate(toks):
            rows.append(
                {
                    "type": "Word",
                    "text": tok,
                    "context": context_for(toks, j),
                    "sentence": text,
                    "sequence_id": int(global_i),
                    "item_index": int(global_i),
                    "start": start,
                    "duration": word_duration,
                    "timeline": timeline,
                    "subject": "default",
                }
            )
            start += word_duration + word_gap
        if start < min_duration:
            rows[-1]["duration"] += min_duration - start
    return pd.DataFrame(rows), timeline_to_item


def vertex_index(target_dim: int | None) -> np.ndarray:
    if target_dim is None or target_dim >= N_VERTICES:
        return np.arange(N_VERTICES, dtype=np.int64)
    if target_dim <= 0:
        raise ValueError("--target-dim must be positive")
    return np.unique(np.linspace(0, N_VERTICES - 1, target_dim).round().astype(np.int64))


def load_model(features: list[str]):
    sys.path.insert(0, ".")
    from tribev2.demo_utils import TribeModel

    cfg = {
        "data.text_feature.model_name": "unsloth/Llama-3.2-3B",
        "data.features_to_use": features,
    }
    print(f"=== loading facebook/tribev2 features={features} ===", flush=True)
    model = TribeModel.from_pretrained(
        "facebook/tribev2",
        cache_folder=TRIBE_CACHE,
        config_update=cfg,
    )
    return model, cfg


def pool_by_timeline(
    preds: np.ndarray,
    segments: list,
    timeline_to_item: dict[str, int],
    n_items: int,
    vindex: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    targets = np.zeros((n_items, len(vindex)), dtype=np.float32)
    counts = np.zeros(n_items, dtype=np.int32)
    for row, seg in zip(preds, segments, strict=True):
        timeline = getattr(seg, "timeline", None)
        if timeline not in timeline_to_item:
            continue
        item = timeline_to_item[timeline]
        targets[item] += row[vindex].astype(np.float32)
        counts[item] += 1
    missing = np.where(counts == 0)[0]
    if len(missing):
        raise RuntimeError(f"TRIBE produced no kept segments for local item(s): {missing.tolist()}")
    targets /= counts[:, None]
    return targets, counts


def predict_synthetic(model, texts: list[str], item_indices: np.ndarray, args, vindex: np.ndarray):
    events, timeline_to_item = synthetic_word_events(
        texts,
        item_indices,
        word_duration=args.word_duration,
        word_gap=args.word_gap,
        min_duration=args.min_duration,
    )
    preds, segments = model.predict(events, verbose=not args.quiet)
    if preds.ndim != 2 or preds.shape[1] != N_VERTICES:
        raise RuntimeError(f"expected TRIBE cortical preds (T,{N_VERTICES}); got {preds.shape}")
    targets, counts = pool_by_timeline(preds, segments, timeline_to_item, len(texts), vindex)
    return targets, counts, events


def predict_tts_single(model, texts: list[str], args, vindex: np.ndarray):
    if args.batch_items != 1:
        raise ValueError("tts-single requires --batch-items 1")
    targets, counts = [], []
    all_events = []
    for text in texts:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as tmp:
            tmp.write(text)
            tmp.flush()
            events = model.get_events_dataframe(text_path=tmp.name)
        preds, segments = model.predict(events, verbose=not args.quiet)
        if preds.ndim != 2 or preds.shape[1] != N_VERTICES:
            raise RuntimeError(f"expected TRIBE cortical preds (T,{N_VERTICES}); got {preds.shape}")
        targets.append(preds[:, vindex].mean(axis=0).astype(np.float32))
        counts.append(len(segments))
        all_events.append(events)
    return np.stack(targets), np.array(counts, dtype=np.int32), pd.concat(all_events, ignore_index=True)


def default_out(split: str, features: list[str], start: int, n: int, target_dim: int | None) -> Path:
    tag = "+".join(features)
    dim = "full" if target_dim is None else f"d{target_dim}"
    return OUT_ROOT / tag / f"{split}_start{start}_n{n}_{dim}.npz"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=sorted(CORPORA), default="train")
    ap.add_argument("--corpus", type=Path, default=None)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--batch-items", type=int, default=8)
    ap.add_argument("--features", default="text", help="comma list, default text")
    ap.add_argument("--event-mode", choices=["synthetic-text", "tts-single"], default="synthetic-text")
    ap.add_argument("--target-dim", type=int, default=None, help="evenly spaced fsaverage5 vertices; default all")
    ap.add_argument("--word-duration", type=float, default=0.35)
    ap.add_argument("--word-gap", type=float, default=0.05)
    ap.add_argument("--min-duration", type=float, default=1.0)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--save-events", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    corpus = args.corpus or CORPORA[args.split]
    texts, item_indices = load_texts(corpus, args.start, args.limit)
    if not texts:
        raise SystemExit("No non-empty texts selected")
    features = [f.strip() for f in args.features.split(",") if f.strip()]
    if args.event_mode == "synthetic-text" and features != ["text"]:
        raise ValueError("synthetic-text is valid only with --features text")
    out = args.out or default_out(args.split, features, args.start, len(texts), args.target_dim)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise FileExistsError(f"refusing to overwrite existing cache: {out}")

    vindex = vertex_index(args.target_dim)
    model, cfg = load_model(features)
    tr = float(model.data.TR)
    all_targets, all_counts, events_parts = [], [], []
    t0 = time.time()
    for start in range(0, len(texts), args.batch_items):
        batch_texts = texts[start : start + args.batch_items]
        batch_idx = item_indices[start : start + args.batch_items]
        print(f"=== batch {start}:{start + len(batch_texts)} ===", flush=True)
        if args.event_mode == "synthetic-text":
            targets, counts, events = predict_synthetic(model, batch_texts, batch_idx, args, vindex)
        else:
            targets, counts, events = predict_tts_single(model, batch_texts, args, vindex)
        all_targets.append(targets)
        all_counts.append(counts)
        if args.save_events:
            events_parts.append(events)

    targets = np.concatenate(all_targets, axis=0).astype(np.float32)
    counts = np.concatenate(all_counts, axis=0).astype(np.int32)
    meta = {
        "experiment": "E016 Phase 3 KD-corpus TRIBE target cache",
        "split": args.split,
        "corpus": str(corpus),
        "start": args.start,
        "n_items": len(texts),
        "features": features,
        "event_mode": args.event_mode,
        "target_dim": int(targets.shape[1]),
        "vertex_index": "stored in npz",
        "tr": tr,
        "word_duration": args.word_duration,
        "word_gap": args.word_gap,
        "min_duration": args.min_duration,
        "config_update": cfg,
        "elapsed_s": round(time.time() - t0, 3),
        "science_status": "target-cache artifact only; not a Phase-3 result",
    }
    np.savez_compressed(
        out,
        targets=targets,
        texts=np.array(texts, dtype=str),
        item_indices=item_indices,
        vertex_index=vindex,
        segment_counts=counts,
        metadata=json.dumps(meta, sort_keys=True),
    )
    out.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    if args.save_events:
        pd.concat(events_parts, ignore_index=True).to_csv(out.with_suffix(".events.csv"), index=False)
    print(f"saved {out} targets={targets.shape} segment_counts={counts.tolist()}", flush=True)


if __name__ == "__main__":
    main()
