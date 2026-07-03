---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S56 - `/goal` continuation: E016 analyzer paper-branch hint; `/work` + `/plan`. Full target caches built and validated; training arm 1/9 running; no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

The active E016 full Phase-3 run has moved past target-cache generation into GPT-2 training. Last status check in S56: `phase=training_running_or_interrupted`; `health.status=runner_alive_log_quiet`; train cache exists with sidecar `n_items=95999`, `target_dim=20484`; heldout cache exists with sidecar `n_items=1999`, `target_dim=20484`; launcher validation printed finite targets and `missing=0` for both caches. Training began at `2026-07-03T01:01:14Z`; latest parsed training marker is `seed=0`, `arm=kd_only`, `lambda=0.0`, with `1/9` arm markers seen. The runner process is alive (`uv run python scripts/run_tribe_phase3.py` plus `.venv/bin/python3` child). There is still no Phase-3 run JSON and no analyzer JSON, so no `/interpret` result exists yet.

The top-tier contribution path is now explicit: the paper cell is **brain-alignment-guided compression/distillation under fixed student budget**, not generic brain-tuning. The result-contingent paper plan is recorded in [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), and the claim-by-claim readiness ledger is [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md). The matched-information text-feature control launcher is prepared but must not be run unless the active TRIBE Phase-3 result is positive enough to need a brain-specificity check.

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What was done

- Added and hardened [`scripts/e016_phase3_status.py`](../scripts/e016_phase3_status.py) so it reports cache-stage progress, ETA fields, heldout-vs-train denominators, training-arm markers, the active `run_tribe_phase3.py` runner processes, and a `health` block for quiet-but-live training.
- Recorded E016 Steps 21-25 in [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md): ETA monitor, stage-aware cache progress, full cache validation/training start, runner-process discovery, and quiet-training health status.
- Added [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), mapping each possible paper claim to current evidence, missing proof, and venue burden.
- Added `paper_branch_hint` to [`scripts/analyze_tribe_phase3.py`](../scripts/analyze_tribe_phase3.py). It stays `not_ready` unless `gate.science_ready=true`; once ready, it routes to the predeclared paper branches (`controlled_null_candidate`, `tribe_positive_needs_textfeat`, or matched-information control comparison).
- Confirmed the full train and heldout target caches exist and validated, then left the full Phase-3 launcher running on training arm 1/9.
- Latest non-wrap paper-planning/tooling commit: `ea3ba18 feat: add E016 paper branch hint`.

## What to do next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`.
2. If the runner exits without writing `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
3. When the analyzer JSON exists, switch to `/interpret`. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
4. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free.
5. If E016 is null at matched PPL, use [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md) and [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) to frame the controlled-negative paper branch.

## Blockers / open loops

- The full E016 training run is still on the first parsed arm marker (`seed=0`, `kd_only`). Full-arm training may be long; do not treat quiet log mtime as failure unless the runner process exits or GPU/process state changes.
- Firecrawl Research MCP tools were not exposed in the S51 scout turn, so the literature frontier record used web search and primary pages/PDFs.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is building would compete for GPU and disk bandwidth.

## Key facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Expected full TRIBE artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Latest non-wrap work commit for this continuation: `ea3ba18 feat: add E016 paper branch hint`.
