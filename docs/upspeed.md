---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S72 - `/goal` continuation: on-policy/context-distillation control-burden audit while E016 full Phase-3 keeps training; no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

The active E016 full Phase-3 run is still training. Last status check in S72: `checked_at_utc=2026-07-03T03:43:55.868994+00:00`; `phase=training_running_or_interrupted`; `health.status=runner_alive_log_recent`; runner processes are alive (`bash run_full_phase3_20260702.sh`, `uv run python scripts/run_tribe_phase3.py`, and the `.venv/bin/python3` child); `run_json.exists=false`; `analysis_json.exists=false`. Full train and heldout target caches remain present and validated as target-cache artifacts only: train `n_items=95999`, `target_dim=20484`; heldout `n_items=1999`, `target_dim=20484`.

Training has advanced since S71 but still has no result artifact. The latest parsed marker is `seed=1`, `arm=tribe_perm`, `lambda=0.1`; `arm_markers_seen=6`; `completed_arm_count=5`; `arms_expected=9`. The completed diagnostics through seed 1 `tribe_mse` remain explicitly partial-arm diagnostics only, not Phase-3 results. The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=60` in the S72 sample), but GPU fields remain liveness context, not strict E016 attribution or evidence.

The top-tier paper route is now sharper: on-policy/context/self-distillation is an active 2026 LLM field, so the prepared `textfeat` control must not be treated as a full context-distillation comparator. The new `/scout` memo [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md) records that `textfeat` clears a sentence-local frozen-teacher hidden-state target only. If E016 is positive and later beats `textfeat`, a top-tier brain-specific positive still needs extra seeds plus either a long-context/on-policy non-brain control, a real-brain evaluation, or a narrowed claim.

The current source-facing planning bundle is: [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md), [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), and [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md).

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What Was Done

- Added [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), a focused `/scout` memo over 2026 on-policy/context/self-/privileged-information distillation sources: OPD survey, OPCD, OPSD, PI distillation, GATES, SDPO, HDPO, and OEL.
- Updated [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), and [`01-research-landscape.md`](01-research-landscape.md) so they distinguish the sentence-local `textfeat` control from long-context/on-policy distillation.
- Verified `git diff --check` and a changed-doc relative-link check.
- Committed the scout slice as `ce3f107 docs: audit on-policy distillation burden`.

## What To Do Next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`; use the `gpu` block as a liveness clue only, not evidence.
2. If the runner exits without writing `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
3. When the run JSON exists, run `uv run python scripts/e016_branch_decision.py`; if it says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
4. Switch to `/interpret` only if the analyzer/readiness gate is science-ready. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
5. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free; when both analyzer JSONs are science-ready, use [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) before any brain-specific claim.
6. If E016 is positive even after `textfeat`, state the scope precisely: `textfeat` is a sentence-local teacher-hidden-state control. The next reviewer-facing burden is extra seeds plus either long-context/on-policy distillation control, real-brain evaluation, or a narrower claim.
7. If E016 is null at matched PPL, use [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), and [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) to frame the controlled-negative paper branch.

## Blockers / Open Loops

- The full E016 training run is incomplete: `run_json.exists=false`, `analysis_json.exists=false`.
- The completed arm diagnostics are not science results and must not be used for a verdict.
- Firecrawl Research MCP/CLI tools were not exposed in this Codex surface, so the scout passes used live web search over primary or near-primary pages instead.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is training would compete for GPU and disk bandwidth.

## Key Facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Expected full TRIBE artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Latest non-wrap work commit for this continuation: `ce3f107 docs: audit on-policy distillation burden`.
