"""Recompute E003's reference-arm held-out perplexities (provenance repair, 2026-06-17).

WHY: E003's headline table quotes teacher 74 / gpt2 105 / distilgpt2 169 / untrained
~50000, but the original run recorded ``perplexity: null`` for every reference arm
(``record()`` was called without a ``ppl=`` argument for the references — only the three
trained arms carried a measured ppl). The four reference numbers were therefore never in
the output JSONs. This script measures them on the EXACT cached held-out slice the run
used, with the run's OWN estimator (imported, not reimplemented), so the table values are
traceable to an artifact.

PROVENANCE-ONLY. This touches no alignment number, no verdict, no rung. It writes a sidecar
``outputs/E003_perplexity.json`` and leaves the raw run JSONs immutable.

ESTIMATOR NOTE: ``eval_perplexity`` is a single-window, max_length=64, micro-averaged
token-level perplexity with NO sliding-window stride. This is NOT the canonical
sliding-window WikiText perplexity; it is the estimator E003's trained arms were measured
with, and cross-arm ratios / the log-ppl fit are only coherent if every arm uses it. Do not
substitute a stride-1 estimator here.

Run:
    export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
    uv run python scripts/recompute_e003_reference_ppl.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch
from transformers import AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_kd_alignment import (  # noqa: E402  (import the run's own estimator + builders)
    eval_perplexity,
    load_pretrained,
    make_random_gpt2,
)

REPO = Path(__file__).resolve().parent.parent
SLICE = REPO / "data/kd_corpus/wikitext103_sentences_heldout.txt"
OUT = REPO / "outputs/E003_perplexity.json"

# What E003.md's table currently asserts, for a recompute-vs-recorded comparison.
RECORDED = {"teacher": 74.0, "gpt2": 105.0, "distilgpt2": 169.0, "untrained": 50000.0}
UNTRAINED_SEEDS = [0, 1, 2]  # the floor arm was scored over these seeds in the run


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return "unknown"


def main() -> None:
    if not SLICE.exists():
        raise FileNotFoundError(f"cached held-out slice missing: {SLICE}")
    texts = [ln for ln in SLICE.read_text().splitlines() if ln.strip()]
    slice_md5 = hashlib.md5(SLICE.read_bytes()).hexdigest()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained("gpt2")
    tok.pad_token = tok.eos_token

    results: dict = {}

    # Deterministic single-instance reference arms.
    for tag, name in [("teacher", "gpt2-medium"), ("gpt2", "gpt2"), ("distilgpt2", "distilgpt2")]:
        m = load_pretrained(name, dev)
        ppl = eval_perplexity(m, tok, texts, dev)
        results[tag] = {"model": name, "perplexity": round(ppl, 4), "seeds": None}
        print(f"{tag:11s} ({name:11s}) ppl={ppl:8.3f}  recorded={RECORDED[tag]}")
        del m
        torch.cuda.empty_cache()

    # Untrained floor: random-init gpt2 over the run's seeds.
    per_seed = []
    for s in UNTRAINED_SEEDS:
        m = make_random_gpt2(dev, s)
        per_seed.append(eval_perplexity(m, tok, texts, dev))
        del m
        torch.cuda.empty_cache()
    untr_mean = float(np.mean(per_seed))
    results["untrained"] = {
        "model": "gpt2 (random init)",
        "perplexity": round(untr_mean, 1),
        "per_seed": [round(p, 1) for p in per_seed],
        "seeds": UNTRAINED_SEEDS,
        "label": "order-of-magnitude only — a random-init net's ppl is large and seed-variable, "
                 "near the BPE vocab scale (|V|=50257); not a stable converged-LM measurement.",
    }
    print(f"untrained   (random gpt2) ppl={untr_mean:8.1f}  per-seed={results['untrained']['per_seed']}")

    payload = {
        "provenance": {
            "what": "E003 reference-arm held-out perplexities, recomputed for provenance.",
            "recomputed_on": "2026-06-17",
            "git_sha": _git_sha(),
            "slice": str(SLICE.relative_to(REPO)),
            "slice_md5": slice_md5,
            "slice_n_sentences": len(texts),
            "estimator": "scripts/run_kd_alignment.py:eval_perplexity — single-window, "
                         "max_length=64, batch_size=32, NO sliding-window stride, "
                         "token-level micro-averaged NLL, gpt2 BPE tokenizer (pad=eos). "
                         "Matched to the trained arms; NOT canonical sliding-window WikiText ppl.",
            "source_note": "These reference ppls were NOT stored in the original run "
                           "(record() passed ppl=None for reference arms); they are recomputed "
                           "on the original cached slice with the original estimator. "
                           "Trained-arm ppls (kd_cold/kd_warm/lmft_warm) remain sourced from "
                           "outputs/E003_{cold,warm}.json.",
            "scope": "PROVENANCE-ONLY: no alignment number, verdict, or rung changes.",
        },
        "reference_perplexities": results,
        "recompute_vs_recorded": {
            tag: {
                "recomputed": results[tag]["perplexity"],
                "recorded": RECORDED[tag],
                "matches_within_rounding": (
                    tag != "untrained"
                    and abs(results[tag]["perplexity"] - RECORDED[tag]) <= 0.5
                ),
            }
            for tag in results
        },
    }
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"\nwrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
