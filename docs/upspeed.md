---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-02 (S51 - `/goal` top-venue frontier scout plus E016 Phase-3 support; `/work` + `/scout` + `/meta`. Active full E016 run, no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

S51 continued Erfan's autonomous `/goal`: evaluate the thesis contribution space, refresh the literature frontier, and start the best experiment path. The conclusion is sharper than before: broad "brain data improves LMs" and "brain-derived representation guidance improves LLM behavior" are no longer novel enough. The viable top-tier cell is **brain-alignment-guided compression/distillation under fixed student budget, matched perplexity, permuted targets, and matched-information non-brain controls**.

The active E016 full Phase-3 run is still building the full train TRIBE cache. Last status check: `phase=train_cache_building`; train-cache lower-bound progress `82624/95999 = 0.860676`; no train cache file yet, no heldout cache file, no Phase-3 run JSON, and no analyzer JSON. There is therefore no `/interpret` result yet.

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What was done

- Recorded the 2026 top-venue frontier in [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md): CoNLL 2026 closes generic brain-vs-stimulus text tuning; ACL 2026 ECoG tuning is a modality pivot; ICLR/MindTransformer and AAAI/ICML hits are measurement pressure; compression/KD remains open.
- Added scout-grade canonical notes for [`merlin-2026_what-brain-data-adds`](literature/canonical/merlin-2026_what-brain-data-adds.md), [`zhang-2026_temporal-precision-ecog-tuning`](literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md), and [`xiao-2026_brain-guided-llm-reasoning`](literature/canonical/xiao-2026_brain-guided-llm-reasoning.md).
- Added [`scripts/e016_phase3_status.py`](../scripts/e016_phase3_status.py), a read-only monitor for the long E016 Phase-3 run.
- Hardened [`scripts/analyze_tribe_phase3.py`](../scripts/analyze_tribe_phase3.py) so partial arm grids cannot look science-ready, then added paired seed-delta values and deterministic two-sided sign-flip p-values for the eventual `/interpret` audit.
- Added [`scripts/build_text_feature_target_cache.py`](../scripts/build_text_feature_target_cache.py), the matched-information non-brain target-cache builder for the post-CoNLL control.
- Parameterized [`scripts/run_tribe_phase3.py`](../scripts/run_tribe_phase3.py) with `--target-label`, preserving the default `tribe_mse`/`tribe_perm` arms while enabling `textfeat_mse`/`textfeat_perm`.
- Ran a tiny text-feature end-to-end smoke with `sshleifer/tiny-gpt2`; analyzer remained `science_ready=false` with the scale/seed gates closed.
- Updated [`docs/01-research-landscape.md`](01-research-landscape.md), [`docs/experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md), [`scripts/AGENTS.md`](../scripts/AGENTS.md), and [`ladder.md`](ladder.md) for the new operational state.

## What to do next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`.
2. When the analyzer JSON exists, do not declare a verdict directly. Enter `/interpret`: run the stat audit and panel, inspect the paired deltas and sign-flip p-values, and only then record a result.
3. If E016 is positive at matched PPL, the next required experiment is the matched-information non-brain target control using `build_text_feature_target_cache.py` plus `run_tribe_phase3.py --target-label textfeat`.
4. If E016 is null at matched PPL, frame the contribution as a controlled compression-frontier null: dense synthetic neural targets did not move a KD student even after removing fMRI scarcity and target-averaging excuses.

## Blockers / open loops

- The full E016 train cache is still building. The active process is healthy, but no result artifact exists yet.
- Firecrawl Research MCP tools were not exposed in this Codex turn, so the literature scout used web search and primary pages/PDFs instead.
- The ICML-facing attribution paper was found via arXiv/OpenReview plus an author acceptance notice, but no official ICML proceedings page was indexed in this scan.

## Key facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Expected full artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Latest pushed commits for this block end at `eb355dd feat: add E016 paired effect stats`.
