---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S76 - `/goal` continuation: bounded E016 monitoring; run advanced to 7/9 completed arms but still has no full run JSON or analyzer; no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

The active E016 full Phase-3 run is still training. Last status check in S76: `checked_at_utc=2026-07-03T05:02:44.843177+00:00`; `phase=training_running_or_interrupted`; `health.status=runner_alive_log_quiet`; runner processes are alive (`bash run_full_phase3_20260702.sh`, `uv run python scripts/run_tribe_phase3.py`, and the `.venv/bin/python3` child); `run_json.exists=false`; `analysis_json.exists=false`. Full train and heldout target caches remain present and validated as target-cache artifacts only: train `n_items=95999`, `target_dim=20484`; heldout `n_items=1999`, `target_dim=20484`.

Training advanced during S76 from 6/9 completed arms to 7/9 completed arms. The latest parsed marker is `seed=2`, `arm=tribe_mse`, `lambda=0.1`; `arm_markers_seen=8`; `completed_arm_count=7`; `arms_expected=9`. The latest completed arm is seed 2 `kd_only` with `ppl=98.120` and `target_r2=0.5932`, but this is explicitly a partial-arm diagnostic only, not a Phase-3 result. The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=75` in the S76 sample), but GPU fields remain liveness context, not strict E016 attribution or evidence.

Two bounded watcher runs were executed. The first watcher (`--max-wait-s 720`) reached its cap with no run JSON, then the status sample showed the run had advanced to seed 2 `tribe_mse`. The second watcher (`--max-wait-s 1200`) also reached its cap with no run JSON. Since the runner is still alive and the active arm is still training, there is no failure to debug and no result to interpret yet.

The positive-branch control ladder remains as of S75: future control runs can preserve trained students with `--save-model-dir`, and [`e016_eval_saved_student_alignment.py`](../scripts/e016_eval_saved_student_alignment.py) can score artifacted students on Tuckute as a diagnostic input to `/interpret`. The active TRIBE full run started before artifact saving existed, so it should still be treated as metrics-only unless selected arms are rerun with `--save-model-dir`.

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What Was Done

- Rechecked the current worktree and active E016 status.
- Ran `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 120 --max-wait-s 720`; it exited waiting for the full run JSON.
- Took a status sample that showed the run advanced from 6/9 to 7/9 completed arms: seed 2 `kd_only` completed; seed 2 `tribe_mse` became active.
- Ran `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 120 --max-wait-s 1200`; it also exited waiting for the full run JSON.
- Took a close-state status sample showing the runner still alive, seed 2 `tribe_mse` active, no run JSON, and no analyzer JSON.

## What To Do Next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`; use the `gpu` block as a liveness clue only, not evidence.
2. If the runner exits without writing `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
3. When the run JSON exists, run `uv run python scripts/e016_branch_decision.py`; if it says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
4. Switch to `/interpret` only if the analyzer/readiness gate is science-ready. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
5. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free; when both analyzer JSONs are science-ready, use [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) before any brain-specific claim.
6. If E016 is positive even after `textfeat`, state the scope precisely: `textfeat` is a sentence-local teacher-hidden-state control. The prepared `contextfeat` path can test a context-conditioned teacher-feature control, and the saved-student Tuckute evaluator can probe real-brain alignment for artifacted students, but both are branch-gated follow-ups.

## Blockers / Open Loops

- The full E016 training run is incomplete: `run_json.exists=false`, `analysis_json.exists=false`.
- The completed arm diagnostics are not science results and must not be used for a verdict.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is training would compete for GPU and disk bandwidth.
- The prepared contextfeat builder is smoke-tested only. A full contextfeat cache/control is branch-gated behind E016 positive plus textfeat survival.
- The Tuckute saved-student evaluator is smoke-tested only. Full-scale use requires saved artifacts from `--save-model-dir` runs and `/interpret` before any claim.
- On-policy distillation remains a separate protocol; contextfeat and the Tuckute probe do not clear student-rollout teacher supervision.
- The active TRIBE full run is metrics-only with respect to model artifacts because it started before `--save-model-dir` existed.

## Key Facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Active run JSON target: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`.
- Active analysis JSON target: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Current active arm at S76 close: seed 2 `tribe_mse`, `lambda=0.1`.
- Completed arms at S76 close: 7/9, latest seed 2 `kd_only`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Saved-student Tuckute evaluator: `uv run python scripts/e016_eval_saved_student_alignment.py --run-json <artifacted-run.json> --out <alignment.json> --reference-model gpt2-medium`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Latest committed work before this monitor-only continuation: `478cd53 docs: wrap E016 real-brain probe`.
