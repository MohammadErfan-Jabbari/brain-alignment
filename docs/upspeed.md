---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S52 - `/goal` continuation: paper decision tree plus E016 textfeat control launcher; `/work` + `/plan`. Active full E016 run, no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

The active E016 full Phase-3 run is still building the full train TRIBE cache. Last status check in S52: `phase=train_cache_building`; train-cache lower-bound progress `83648/95999 = 0.871342`; no train cache file yet, no heldout cache file, no Phase-3 run JSON, and no analyzer JSON. There is therefore no `/interpret` result yet.

The top-tier contribution path is now explicit: the paper cell is **brain-alignment-guided compression/distillation under fixed student budget**, not generic brain-tuning. The result-contingent paper plan is recorded in [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md). The matched-information text-feature control launcher is prepared but must not be run unless the active TRIBE Phase-3 result is positive enough to need a brain-specificity check.

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What was done

- Added [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), a result-contingent paper decision tree for null, confounded-positive, TRIBE-positive, textfeat-matched, and brain-specific-positive branches.
- Linked that decision tree from [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md).
- Added [`scripts/e016_make_textfeat_control_script.py`](../scripts/e016_make_textfeat_control_script.py), which writes the post-E016 full matched-information text-feature control launcher under `outputs/`.
- Generated `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh` and checked it with `bash -n`; it was not executed.
- Updated [`scripts/AGENTS.md`](../scripts/AGENTS.md) and [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) with the queued-control launcher.

## What to do next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`.
2. When the analyzer JSON exists, switch to `/interpret`. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
3. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free.
4. If E016 is null at matched PPL, use [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md) to frame the controlled-negative paper branch.

## Blockers / open loops

- The full E016 train cache is still building. The active process is healthy, but no result artifact exists yet.
- Firecrawl Research MCP tools were not exposed in the S51 scout turn, so the literature frontier record used web search and primary pages/PDFs.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is building would compete for GPU and disk bandwidth.

## Key facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Expected full TRIBE artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Latest non-wrap work commit for this continuation: `2922289 docs: add top-venue paper decision tree`.
