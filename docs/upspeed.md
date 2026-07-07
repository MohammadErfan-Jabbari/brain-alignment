---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-07 (S80 - `/goal` continuation: extra seeds completed, combined seed `0-5` TRIBE-vs-textfeat comparator/audit held, no final verdict, no brain-specific clearance, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

Both original E016 full-run branches are analyzer-ready. The TRIBE run produced `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`. The matched-information textfeat control also completed and produced `phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`.

The TRIBE readiness packet routed to `tribe_positive_needs_textfeat`; the textfeat readiness packet routed to `matched_information_control_ready`. The ready comparator at `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json` returned `branch_hint.branch="tribe_stronger_than_textfeat_needs_review"`.

Comparator summary at lambda 0.1: TRIBE gain versus KD-only `+0.077492`; TRIBE gain versus permuted TRIBE `+0.071871`; textfeat gain versus KD-only `+0.000761`; textfeat gain versus permuted textfeat `+0.002379`; TRIBE-minus-textfeat gain versus KD-only `+0.076731`; TRIBE-minus-textfeat gain versus permuted-control gains `+0.069492`.

The local `/interpret` audit at `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.interpret_audit.json` recomputed the comparison from raw run rows. It matched the comparator means, found all seed-aligned margins positive, and confirmed max relative PPL delta `0.009220` below the 0.05 tolerance. This supports the narrow post-positive route but not a final paper claim: `n=3` still gives sign-flip `p=0.25`, the endpoint is synthetic target-R2, and textfeat clears only sentence-local frozen-teacher hidden-state supervision.

The extra artifact-saving seeds completed cleanly. The original seed `0,1,2` and extra seed `3,4,5` artifacts were merged into combined seed `0-5` TRIBE and textfeat run JSONs. Both combined analyzers/readiness packets are science-ready. The combined comparator at `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.json` routes to `tribe_stronger_than_textfeat_needs_review`, and the independent raw-row audit at `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.interpret_audit.json` passed all checks.

Six-seed audit summary: TRIBE-minus-textfeat gain versus KD-only is mean `+0.077395`, all six seed margins positive, sign-flip `p=0.03125`; TRIBE-minus-textfeat gain versus permuted-control gains is mean `+0.072531`, all six seed margins positive, sign-flip `p=0.03125`; max relative PPL delta remains `0.009220` under the `0.05` tolerance.

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
- Detected extra-seed completion, merged seeds `0-5`, reran analyzers/readiness/comparator, and wrote the six-seed independent audit.

## What To Do Next

1. Choose the next burden deliberately: real-brain evaluation on saved seed `3-5` artifacts, stronger context/on-policy non-brain control, or narrowed synthetic-target claim.
2. If choosing real-brain evaluation, use `scripts/e016_eval_saved_student_alignment.py` on the artifacted extra-seed TRIBE/textfeat runs and treat the output as diagnostic, not a verdict.
3. If choosing stronger non-brain control, define the estimand before launching contextfeat/on-policy compute.
4. Do not claim brain-specific clearance or flip a rung from synthetic target-R2 alone.

## Blockers / Open Loops

- The comparator route is not a final verdict and not brain-specific clearance.
- The synthetic-target comparison is now six seeds and stable against textfeat, but still not real-brain evidence.
- Textfeat clears only sentence-local frozen-teacher hidden-state supervision, not long-context/on-policy distillation or real-brain alignment.
- The original seed `0-2` TRIBE run did not save model artifacts; real-brain evaluation can currently use the saved seed `3-5` artifacts unless selected original arms are rerun.
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
- Combined TRIBE run/analyzer/readiness: `outputs/E016_tribe/phase3/phase3_combined_tribe_gpt2_n95999_s0-5_lam0.1.json`, `.analysis.json`, `.readiness.json`.
- Combined textfeat run/analyzer/readiness: `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.json`, `.analysis.json`, `.readiness.json`.
- Combined comparator/audit: `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.json`, `.interpret_audit.json`.
- Saved-student Tuckute evaluator: `uv run python scripts/e016_eval_saved_student_alignment.py --run-json <artifacted-run.json> --out <alignment.json> --reference-model gpt2-medium`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Comparator command after both analyzer JSONs are ready: `uv run python scripts/e016_compare_target_controls.py <tribe-analysis.json> <textfeat-analysis.json> --out <comparison.json>`.
