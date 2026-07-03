---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S78 - `/goal` continuation: full textfeat control completed, readiness is science-ready, and the TRIBE-vs-textfeat comparator routes to `tribe_stronger_than_textfeat_needs_review`; no final verdict, no brain-specific clearance, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

Both E016 full-run branches are now analyzer-ready. The TRIBE run produced `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`. The matched-information textfeat control also completed and produced `phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`.

The TRIBE readiness packet routed to `tribe_positive_needs_textfeat`; the textfeat readiness packet routed to `matched_information_control_ready`. The ready comparator at `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json` returned `branch_hint.branch="tribe_stronger_than_textfeat_needs_review"`.

Comparator summary at lambda 0.1: TRIBE gain versus KD-only `+0.077492`; TRIBE gain versus permuted TRIBE `+0.071871`; textfeat gain versus KD-only `+0.000761`; textfeat gain versus permuted textfeat `+0.002379`; TRIBE-minus-textfeat gain versus KD-only `+0.076731`; TRIBE-minus-textfeat gain versus permuted-control gains `+0.069492`.

The comparator is a handoff, not a verdict. Its own burden says TRIBE stronger than textfeat clears only a sentence-local frozen-LM hidden-state target. It does not clear long-context/on-policy distillation, rich-feedback privileged-signal adjacency, or real-brain alignment. The next step is `/interpret`, including seed-aligned margin audit, PPL/gate/code/stat review, and a decision about extra seeds, context/on-policy control, real-brain evaluation, or narrowed claim.

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

## What To Do Next

1. Switch to `/interpret`; do not record a verdict from the comparator alone.
2. Audit seed-aligned TRIBE-minus-textfeat margins, PPL matching, analyzer gates, and code/stat assumptions.
3. Inspect [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md) before choosing positive paper framing.
4. Choose the next evidence burden: extra seeds, stronger non-brain/context comparator, real-brain follow-up, or controlled scoping of the claim.

## Blockers / Open Loops

- The comparator route is not a final verdict and not brain-specific clearance.
- The run has only three seeds; sign-flip resolution is weak for a top-tier positive.
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
- Saved-student Tuckute evaluator: `uv run python scripts/e016_eval_saved_student_alignment.py --run-json <artifacted-run.json> --out <alignment.json> --reference-model gpt2-medium`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Comparator command after both analyzer JSONs are ready: `uv run python scripts/e016_compare_target_controls.py <tribe-analysis.json> <textfeat-analysis.json> --out <comparison.json>`.
