---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S77 - `/goal` continuation: full E016 TRIBE artifact reached analyzer-ready handoff, routed to `tribe_positive_needs_textfeat`, and the matched-information `textfeat` control was launched; no final verdict, no brain-specific claim, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

The full E016 TRIBE Phase-3 run is no longer training. It produced `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON. Last TRIBE status sample in S77: `checked_at_utc=2026-07-03T07:31:45.131949+00:00`; `phase=analysis_ready`; `health.status=analysis_artifact_present`; `run_json.exists=true`; `analysis_json.exists=true`; `gate.science_ready=true`; grid complete for 3 seeds x 3 arms.

The readiness packet routed the artifact to `paper_branch_hint.branch="tribe_positive_needs_textfeat"`. The independent recompute audit passed: TRIBE target exceeded the permuted target on all three paired seeds at the synthetic target endpoint (mean delta `+0.071871`; sign-flip `p=0.25`) and exceeded KD-only on all three paired seeds (mean delta `+0.077492`; sign-flip `p=0.25`), while relative PPL deltas versus KD-only stayed below the 0.05 matching tolerance. This is routing evidence for the synthetic TRIBE target branch, not a brain-specific result.

The branch router returned `status="textfeat_control_required"`, `route="run_textfeat_after_resource_check"`, and `active_runner_process_count=0` for TRIBE. The matched-information `textfeat` control was launched in a detached process on GPU 1 (`PID=3428588`) using `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`. The clean active run began at `2026-07-03T07:21:00Z`; its log also contains earlier diagnostic/trace prelude from failed supervision attempts.

The `textfeat` launcher built and validated full train and heldout caches before entering training: train `(95999, 20484)`, heldout `(1999, 20484)`, finite, `missing=0`. At the last monitored sample it had entered `scripts/run_tribe_phase3.py` for the full textfeat arms with seed 0 `kd_only` active, GPU 1 active, and no textfeat run JSON or analyzer JSON yet.

No final experiment verdict was adjudicated, no brain-specific claim was made, and no ladder rung changed.

## What Was Done

- Detected that the full TRIBE run had completed and that the analyzer JSON existed.
- Ran `uv run python scripts/e016_finalize_phase3.py` to refresh the analyzer/readiness handoff.
- Ran `uv run python scripts/e016_branch_decision.py`; it routed to `textfeat_control_required`.
- Performed an independent `/interpret` recompute audit and wrote `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.interpret_audit.json`.
- Confirmed the TRIBE runner was no longer active, inspected resources, and launched the prepared `textfeat` control on GPU 1.
- Monitored the launcher through full text-feature cache construction, validation, and entry into the first full training arm.
- Updated the E016 experiment record, top-venue plan/ledger, tasks, ladder, and timeline around the handoff.

## What To Do Next

1. Stay in `/work` and monitor the active textfeat control: process group root `3428588`, log `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.log`.
2. Do not start `contextfeat`, extra seeds, or real-brain probes while textfeat is active.
3. When `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json` appears, run the textfeat finalizer/analyzer/readiness path. The guarded finalizer supports `--run-json`; otherwise run `scripts/analyze_tribe_phase3.py` and `scripts/e016_make_readiness_packet.py` explicitly.
4. When both TRIBE and textfeat analyzer JSONs are science-ready, run `uv run python scripts/e016_compare_target_controls.py` and then switch to `/interpret`.
5. If TRIBE beats textfeat, state the scope precisely: `textfeat` is only a sentence-local teacher-hidden-state control. A top-tier brain-specific claim likely still needs extra seeds plus long-context/on-policy control, real-brain evaluation, or a narrowed claim.
6. If textfeat matches or beats TRIBE, route toward a dense privileged-target/control paper, not a brain-specific positive.

## Blockers / Open Loops

- The textfeat control is running and has no run JSON or analyzer JSON yet.
- The TRIBE-positive branch is not a brain-specific claim; it is exactly the reason textfeat is required.
- The TRIBE run did not save model artifacts because it started before `--save-model-dir`; selected TRIBE arms may require rerun if real-brain probes are needed.
- The prepared contextfeat builder is smoke-tested only. A full contextfeat cache/control is branch-gated behind E016 positive plus textfeat survival.
- The Tuckute saved-student evaluator is smoke-tested only. Full-scale use requires saved artifacts from `--save-model-dir` runs and `/interpret` before any claim.
- On-policy distillation remains a separate protocol; contextfeat and the Tuckute probe do not clear student-rollout teacher supervision.

## Key Facts

- Completed TRIBE run JSON: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`.
- Completed TRIBE analysis JSON: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Completed TRIBE readiness packet: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.readiness.json`.
- Independent recompute audit: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.interpret_audit.json`.
- Active textfeat launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Active textfeat PID at S77 wrap: `3428588`.
- Active textfeat log: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.log`.
- Active textfeat run JSON target: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`.
- Active textfeat analysis JSON target: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Saved-student Tuckute evaluator: `uv run python scripts/e016_eval_saved_student_alignment.py --run-json <artifacted-run.json> --out <alignment.json> --reference-model gpt2-medium`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Comparator command after both analyzer JSONs are ready: `uv run python scripts/e016_compare_target_controls.py <tribe-analysis.json> <textfeat-analysis.json> --out <comparison.json>`.
