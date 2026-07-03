#!/usr/bin/env python3
"""Recover WikiText provenance/context metadata for the E016 KD corpus.

E016's active target caches store sentence text and split-local item indices, but
not the original WikiText row/header context. This helper replays the original
E003 corpus extraction exactly, verifies that the replayed sentences match the
cached train/heldout text files, and writes JSONL metadata under ``outputs/``.

This is CPU-only provenance plumbing. It is not a target builder, not a training
launcher, and not an experiment result.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from data_adapters import load_tuckute  # noqa: E402

CORPUS_DIR = ROOT / "data/kd_corpus"
TRAIN_FILE = CORPUS_DIR / "wikitext103_sentences_train.txt"
HELDOUT_FILE = CORPUS_DIR / "wikitext103_sentences_heldout.txt"
OUT_DIR = ROOT / "outputs/E016_tribe/kd_context_metadata"
SPLITTER = re.compile(r"(?<=[.!?])\s+")


def read_sentences(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def heading_info(line: str) -> tuple[int, str] | None:
    """Return (level, text) for WikiText headings such as '= Title ='."""
    parts = line.strip().split()
    if not parts or not all(ch == "=" for ch in parts[0]):
        return None
    lead = 0
    while lead < len(parts) and all(ch == "=" for ch in parts[lead]):
        lead += 1
    trail = 0
    while trail < len(parts) - lead and all(ch == "=" for ch in parts[len(parts) - 1 - trail]):
        trail += 1
    if lead == 0 or trail == 0 or lead + trail >= len(parts):
        return None
    level = min(lead, trail)
    text = " ".join(parts[lead : len(parts) - trail]).strip()
    return level, text


def update_heading_stack(stack: list[str], level: int, text: str) -> list[str]:
    if level <= 0:
        return stack
    if len(stack) < level:
        stack = stack + [""] * (level - len(stack))
    stack[level - 1] = text
    return stack[:level]


def extract_banned(tuckute_dir: Path) -> set[str]:
    texts, _, _ = load_tuckute(str(tuckute_dir))
    return {text.strip().lower() for text in texts}


def replay_wikitext(total: int, tuckute_dir: Path) -> list[dict[str, Any]]:
    from datasets import load_dataset

    banned = extract_banned(tuckute_dir)
    ds = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="train")
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    heading_stack: list[str] = []
    previous_in_doc: dict[str, int] = {}

    for row_index, row in enumerate(ds):
        line = row["text"].strip()
        if not line:
            continue
        heading = heading_info(line)
        if heading:
            heading_stack = update_heading_stack(heading_stack, heading[0], heading[1])
        if line.startswith("="):
            # The original E003 extractor skipped every leading-equals row, not
            # only balanced headings; formula rows can start with "=" too.
            continue
        row_sentence_indices: list[int] = []
        for sentence_in_row, sentence in enumerate(SPLITTER.split(line)):
            sentence = sentence.strip()
            words = sentence.split()
            if not (4 <= len(words) <= 45):
                continue
            key = sentence.lower()
            if key in banned or key in seen:
                continue
            seen.add(key)
            doc_title = heading_stack[0] if heading_stack else None
            doc_key = doc_title or f"unknown-before-row-{row_index}"
            prev_same_doc = previous_in_doc.get(doc_key)
            prev_same_row = row_sentence_indices[-1] if row_sentence_indices else None
            record = {
                "global_accepted_index": len(records),
                "text": sentence,
                "wikitext_row_index": row_index,
                "sentence_in_wikitext_row": sentence_in_row,
                "doc_title": doc_title,
                "heading_path": heading_stack,
                "previous_same_row_global_index": prev_same_row,
                "previous_same_doc_global_index": prev_same_doc,
                "word_count": len(words),
            }
            records.append(record)
            row_sentence_indices.append(record["global_accepted_index"])
            previous_in_doc[doc_key] = record["global_accepted_index"]
            if len(records) >= total:
                return records
    raise RuntimeError(f"replayed only {len(records)} sentences; need {total}")


def attach_split(records: list[dict[str, Any]], split: str, split_start: int) -> list[dict[str, Any]]:
    out = []
    for split_index, rec in enumerate(records):
        item = dict(rec)
        item["split"] = split
        item["split_index"] = split_index
        item["split_start_global_accepted_index"] = split_start
        out.append(item)
    return out


def write_jsonl(path: Path, rows: list[dict[str, Any]], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite {path}; pass --overwrite")
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def availability(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    return {
        "n_items": n,
        "same_row_previous_available": int(sum(r["previous_same_row_global_index"] is not None for r in rows)),
        "same_doc_previous_available": int(sum(r["previous_same_doc_global_index"] is not None for r in rows)),
        "doc_title_available": int(sum(r["doc_title"] is not None for r in rows)),
        "unique_doc_titles": int(len({r["doc_title"] for r in rows if r["doc_title"] is not None})),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-file", type=Path, default=TRAIN_FILE)
    ap.add_argument("--heldout-file", type=Path, default=HELDOUT_FILE)
    ap.add_argument("--tuckute-dir", type=Path, default=ROOT / "data/tuckute2024")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    train = read_sentences(args.train_file)
    heldout = read_sentences(args.heldout_file)
    total = len(train) + len(heldout)
    records = replay_wikitext(total, args.tuckute_dir)
    replay_train = [r["text"] for r in records[: len(train)]]
    replay_heldout = [r["text"] for r in records[len(train) : total]]
    if replay_train != train:
        for i, (a, b) in enumerate(zip(replay_train, train, strict=True)):
            if a != b:
                raise SystemExit(f"train mismatch at {i}: replay={a!r} cached={b!r}")
    if replay_heldout != heldout:
        for i, (a, b) in enumerate(zip(replay_heldout, heldout, strict=True)):
            if a != b:
                raise SystemExit(f"heldout mismatch at {i}: replay={a!r} cached={b!r}")

    train_rows = attach_split(records[: len(train)], "train", 0)
    heldout_rows = attach_split(records[len(train) : total], "heldout", len(train))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    train_out = args.out_dir / "wikitext103_train_context_meta.jsonl"
    heldout_out = args.out_dir / "wikitext103_heldout_context_meta.jsonl"
    summary_out = args.out_dir / "wikitext103_context_meta_summary.json"
    write_jsonl(train_out, train_rows, args.overwrite)
    write_jsonl(heldout_out, heldout_rows, args.overwrite)

    summary = {
        "science_status": "context metadata recovery only; not an experiment result",
        "corpus_replay": "exact_match",
        "train_file": str(args.train_file),
        "heldout_file": str(args.heldout_file),
        "train_items": len(train_rows),
        "heldout_items": len(heldout_rows),
        "train_metadata": str(train_out),
        "heldout_metadata": str(heldout_out),
        "train_context_availability": availability(train_rows),
        "heldout_context_availability": availability(heldout_rows),
        "join_key_for_active_target_caches": "split_index equals target-cache item_indices for the prefix selected by the launcher",
        "active_e016_launcher_prefix": {
            "train_items": 95999,
            "heldout_items": 1999,
        },
    }
    summary_out.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
