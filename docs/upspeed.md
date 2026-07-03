---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S71 - `/goal` continuation: target-control scope metadata while E016 full Phase-3 keeps training; no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

The active E016 full Phase-3 run is still in GPT-2 training. Last status check in S71: `phase=training_running_or_interrupted`; `health.status=runner_alive_log_quiet`; train cache exists with sidecar `n_items=95999`, `target_dim=20484`; heldout cache exists with sidecar `n_items=1999`, `target_dim=20484`; latest parsed marker is still `seed=1`, `arm=tribe_mse`, `lambda=0.1`; `5/9` arm markers are seen; `completed_arm_count=4`. The completed diagnostics for seed 0 plus seed 1 `kd_only` remain explicitly partial-arm diagnostics only, not Phase-3 results. The runner process is alive (`uv run python scripts/run_tribe_phase3.py` plus `.venv/bin/python3` child). The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=59` in the S71 sample), but GPU fields remain liveness context, not strict E016 attribution or evidence. There is still no Phase-3 run JSON and no analyzer JSON, so no `/interpret` result exists yet.

The top-tier contribution path is now even narrower and better defended. The literature map now includes scout-grade canonical notes for [`saadi-2026_task-tangent-feature-distillation-llms.md`](literature/canonical/saadi-2026_task-tangent-feature-distillation-llms.md), [`penaloza-2026_privileged-information-distillation-lms.md`](literature/canonical/penaloza-2026_privileged-information-distillation-lms.md), and [`wu-2026_pride-privileged-information-distillation-dialogue.md`](literature/canonical/wu-2026_pride-privileged-information-distillation-dialogue.md). The new privileged-signal adjacency audit also records that context/self-distillation, rich-feedback distillation, and gaze/cognitive supervision are active. Therefore the viable E016 cell is not generic LLM KD, feature KD, first PI distillation for LMs, first training-only PI improvement for smaller LMs, context internalization, dense feedback, or gaze/cognitive supervision. It is specifically: under a fixed smaller-student KD budget, does a synthetic brain-alignment target improve the alignment/utility frontier beyond KD-only, a permuted dense-target twin, and a matched-information non-brain privileged target?

The source-facing open-question audit is [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), the distillation-adjacency audit is [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md), the privileged-signal adjacency audit is [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), the result-contingent paper plan is [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), the claim-by-claim readiness ledger is [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), and the pre-result post-run manifest is [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md).

[`e016_branch_decision.py`](../scripts/e016_branch_decision.py) is now the safest one-command post-finalizer router. It reads the full run JSON, analyzer JSON, readiness JSON, and prepared text-feature launcher path, then prints whether to keep monitoring, run the guarded finalizer, switch to `/interpret`, launch the queued text-feature control after a resource check, or compare ready TRIBE/text-feature controls. It currently returns `status="waiting_for_run_json"` because the full run artifact is absent. [`e016_watch_finalize_phase3.py`](../scripts/e016_watch_finalize_phase3.py) remains the easiest polling handoff: it checks once by default, can poll with `--watch`, and calls [`e016_finalize_phase3.py`](../scripts/e016_finalize_phase3.py) only after the full run JSON exists. [`analyze_tribe_phase3.py`](../scripts/analyze_tribe_phase3.py) now preserves target-cache metadata; [`e016_make_readiness_packet.py`](../scripts/e016_make_readiness_packet.py) and [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) surface `target_cache_scope` / `target_scopes`, so a future textfeat comparison is explicitly scoped as sentence-local frozen-LM hidden-state supervision, not long-context/on-policy clearance. None of these helpers is a verdict engine.

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What Was Done

- Added target-control scope metadata to the analyzer/readiness/comparator handoff so post-positive comparisons can say what non-brain control actually ran.
- Updated [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md) Step 37, and [`../scripts/AGENTS.md`](../scripts/AGENTS.md).
- Verified `py_compile`, a temporary synthetic metadata-propagation smoke, `git diff --check`, changed-doc links, and the default branch-router `waiting_for_run_json` path.
- Re-checked E016 status after the tooling commit: the active run is still at seed 1 `tribe_mse`, still with no full run JSON and no analyzer JSON.
- Latest non-wrap work commit: `963f309 feat: record E016 target control scope`.

## What To Do Next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`; use the `gpu` block as a liveness clue only, not E016 attribution or evidence.
2. If the runner exits without writing `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
3. When the run JSON exists, run `uv run python scripts/e016_branch_decision.py`; if it says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
4. Switch to `/interpret` only if the analyzer/readiness gate is science-ready. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
5. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free; when both analyzer JSONs are science-ready, use [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) before any brain-specific claim.
6. If E016 is positive even after `textfeat`, state the scope precisely: textfeat is a sentence-local teacher-hidden-state control. The next reviewer-facing burden is extra seeds plus either long-context/on-policy distillation control, real-brain evaluation, or a narrower claim.
7. If E016 is null at matched PPL, use [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), and [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) to frame the controlled-negative paper branch.

## Blockers / Open Loops

- The full E016 training run is incomplete: `run_json.exists=false`, `analysis_json.exists=false`.
- The completed seed-0 plus seed-1 `kd_only` arm diagnostics are not science results and must not be used for a verdict.
- Firecrawl Research MCP/CLI tools were not exposed in this Codex surface, so the scout passes used live web search over primary or near-primary pages instead.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is training would compete for GPU and disk bandwidth.

## Key Facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Expected full TRIBE artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Latest non-wrap work commit for this continuation: `963f309 feat: record E016 target control scope`.
