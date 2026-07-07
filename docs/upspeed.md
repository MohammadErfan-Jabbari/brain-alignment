---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-07 (S79 - `/goal` continuation: comparator `/interpret` audit held locally and extra artifact-saving seeds `3,4,5` were launched for TRIBE and textfeat; no final verdict, no brain-specific clearance, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

Both original E016 full-run branches are analyzer-ready. The TRIBE run produced `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`. The matched-information textfeat control also completed and produced `phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`.

The TRIBE readiness packet routed to `tribe_positive_needs_textfeat`; the textfeat readiness packet routed to `matched_information_control_ready`. The ready comparator at `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json` returned `branch_hint.branch="tribe_stronger_than_textfeat_needs_review"`.

Comparator summary at lambda 0.1: TRIBE gain versus KD-only `+0.077492`; TRIBE gain versus permuted TRIBE `+0.071871`; textfeat gain versus KD-only `+0.000761`; textfeat gain versus permuted textfeat `+0.002379`; TRIBE-minus-textfeat gain versus KD-only `+0.076731`; TRIBE-minus-textfeat gain versus permuted-control gains `+0.069492`.

The local `/interpret` audit at `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.interpret_audit.json` recomputed the comparison from raw run rows. It matched the comparator means, found all seed-aligned margins positive, and confirmed max relative PPL delta `0.009220` below the 0.05 tolerance. This supports the narrow post-positive route but not a final paper claim: `n=3` still gives sign-flip `p=0.25`, the endpoint is synthetic target-R2, and textfeat clears only sentence-local frozen-teacher hidden-state supervision.

The selected next evidence step is extra artifact-saving seeds. TRIBE extra seeds `3,4,5` are running detached on GPU 1 with launcher PID `3770641` and Python child `3770685`. Textfeat extra seeds `3,4,5` are running detached on GPU 2 with launcher PID `3770642` and Python child `3770687`. A four-minute monitor is running as PID `3770643` and appends to `outputs/E016_tribe/phase3/extra_seed_progress_monitor_20260707.log`.

No final experiment verdict was adjudicated, no brain-specific claim was made, and no ladder rung changed.

## What Was Done

- Detected that the full TRIBE run had completed and that the analyzer JSON existed.
- Ran `uv run python scripts/e016_finalize_phase3.py` to refresh the analyzer/readiness handoff.
- Ran `uv run python scripts/e016_branch_decision.py`; it routed to `textfeat_control_required`.
- Performed an independent `/interpret` recompute audit and wrote `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.interpret_audit.json`.
- Confirmed the TRIBE runner was no longer active, inspected resources, and launched the prepared `textfeat` control on GPU 1.
- Monitored the launcher through full text-feature cache construction, validation, and entry into the first full training arm.
- Updated the E016 experiment record, top-venue plan/ledger, tasks, ladder, and timeline around the handoff.
- Detected textfeat completion, generated the textfeat readiness packet, and ran `scripts/e016_compare_target_controls.py`.
- Recorded the completed-control/comparator handoff in the E016 experiment record, top-venue plan/ledger, tasks, ladder, and timeline.
- Recomputed the TRIBE-vs-textfeat comparison from raw rows and wrote the local `/interpret` audit artifact.
- Chose extra artifact-saving seeds as the next evidence burden and launched matched TRIBE/textfeat seed `3,4,5` runs.

## What To Do Next

1. Monitor the extra-seed runs with `tail -f outputs/E016_tribe/phase3/extra_seed_progress_monitor_20260707.log` or direct log tails.
2. When both extra run JSONs and analyzer/readiness JSONs exist, merge or compare seeds `0-5` and rerun the TRIBE-vs-textfeat audit.
3. Do not launch contextfeat, on-policy distillation, or real-brain probes until the seed-extended comparison is interpreted.
4. If the extended margin holds, choose the next burden: context/on-policy control, real-brain evaluation with saved artifacts, or a deliberately narrowed synthetic-target claim.

## Blockers / Open Loops

- The comparator route is not a final verdict and not brain-specific clearance.
- The current interpreted comparison still has only three completed seeds; sign-flip resolution is weak for a top-tier positive.
- Extra seeds are running and may fail, drift, or reduce the margin.
- Textfeat clears only sentence-local frozen-teacher hidden-state supervision, not long-context/on-policy distillation or real-brain alignment.
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
- Active textfeat log: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.log`.
- Completed textfeat run JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`.
- Completed textfeat analysis JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Completed textfeat readiness packet: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.readiness.json`.
- Ready comparator JSON: `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json`.
- Local comparator `/interpret` audit: `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.interpret_audit.json`.
- Active extra TRIBE launcher: `outputs/E016_tribe/phase3/run_extra_tribe_s3-5_20260707.sh`, PID `3770641`, target JSON `outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.json`.
- Active extra textfeat launcher: `outputs/E016_tribe/phase3/run_extra_textfeat_s3-5_20260707.sh`, PID `3770642`, target JSON `outputs/E016_tribe/phase3/phase3_extra_textfeat_gpt2_n95999_s3-5_lam0.1.json`.
- Active monitor: `outputs/E016_tribe/phase3/monitor_extra_seed_progress_20260707.sh`, PID `3770643`, log `outputs/E016_tribe/phase3/extra_seed_progress_monitor_20260707.log`.
- Saved-student Tuckute evaluator: `uv run python scripts/e016_eval_saved_student_alignment.py --run-json <artifacted-run.json> --out <alignment.json> --reference-model gpt2-medium`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Comparator command after both analyzer JSONs are ready: `uv run python scripts/e016_compare_target_controls.py <tribe-analysis.json> <textfeat-analysis.json> --out <comparison.json>`.
