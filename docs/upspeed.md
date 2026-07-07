---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-07 (S82 - `/goal` continuation: bounded seed `0-2` TRIBE artifact-saving rerun still running; rich 5-minute monitor active; hardened Python rerun Tuckute scorer watcher active; latest snapshot shows 2/9 arms completed and seed0 `tribe_perm` active; no aligned six-seed result, no final verdict, no brain-specific clearance, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

Both original E016 full-run branches are analyzer-ready. The TRIBE run produced `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`. The matched-information textfeat control also completed and produced `phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`, analyzer JSON, and readiness JSON with `gate.science_ready=true`.

The TRIBE readiness packet routed to `tribe_positive_needs_textfeat`; the textfeat readiness packet routed to `matched_information_control_ready`. The ready comparator at `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json` returned `branch_hint.branch="tribe_stronger_than_textfeat_needs_review"`.

Comparator summary at lambda 0.1: TRIBE gain versus KD-only `+0.077492`; TRIBE gain versus permuted TRIBE `+0.071871`; textfeat gain versus KD-only `+0.000761`; textfeat gain versus permuted textfeat `+0.002379`; TRIBE-minus-textfeat gain versus KD-only `+0.076731`; TRIBE-minus-textfeat gain versus permuted-control gains `+0.069492`.

The local `/interpret` audit at `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.interpret_audit.json` recomputed the comparison from raw run rows. It matched the comparator means, found all seed-aligned margins positive, and confirmed max relative PPL delta `0.009220` below the 0.05 tolerance. This supports the narrow post-positive route but not a final paper claim: `n=3` still gives sign-flip `p=0.25`, the endpoint is synthetic target-R2, and textfeat clears only sentence-local frozen-teacher hidden-state supervision.

The extra artifact-saving seeds completed cleanly. The original seed `0,1,2` and extra seed `3,4,5` artifacts were merged into combined seed `0-5` TRIBE and textfeat run JSONs. Both combined analyzers/readiness packets are science-ready. The combined comparator at `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.json` routes to `tribe_stronger_than_textfeat_needs_review`, and the independent raw-row audit at `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.interpret_audit.json` passed all checks.

Six-seed audit summary: TRIBE-minus-textfeat gain versus KD-only is mean `+0.077395`, all six seed margins positive, sign-flip `p=0.03125`; TRIBE-minus-textfeat gain versus permuted-control gains is mean `+0.072531`, all six seed margins positive, sign-flip `p=0.03125`; max relative PPL delta remains `0.009220` under the `0.05` tolerance.

The next burden was chosen and run: saved seed `3-5` TRIBE/textfeat students were scored on the real Tuckute endpoint with `scripts/e016_eval_saved_student_alignment.py`. Both branch outputs scored all 9 saved artifacts with no missing rows, and the paired analysis at `outputs/E016_tribe/phase3/phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment_analysis.json` passed readback checks.

Real-brain diagnostic summary: TRIBE target versus KD-only mean `-0.000735`; TRIBE target versus TRIBE permuted mean `-0.001717`; textfeat target versus KD-only mean `+0.000127`; TRIBE-minus-textfeat gain versus KD-only mean `-0.000862`; TRIBE-minus-textfeat gain versus permuted-control gains mean `-0.000784`. PCA robustness at `25,50,100` did not rescue the TRIBE-minus-textfeat real-brain contrast.

The local raw-row `/interpret` audit at `outputs/E016_tribe/phase3/phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment.interpret_audit.json` passed row-count, seed-arm grid, endpoint/protocol, arithmetic-match, and PCA-robustness checks. Its route is `real_brain_warning_needs_claim_scope_review`.

Local code-path review of `scripts/e016_eval_saved_student_alignment.py` found no immediate implementation blocker: it mirrors the E003 `score_model` path, uses the shared contiguous-fold variance partition, and compiles with the relevant helpers. This is not a second implementation or a publishable code audit by itself.

No final experiment verdict was adjudicated, no brain-specific claim was made, and no ladder rung changed.

S82 claim-scope decision: run the bounded real-brain robustness rerun before narrowing the paper. The selected rerun is only missing TRIBE seed `0-2` with artifact saving, because textfeat seed `0-5` artifacts already exist. If the resulting seed `0-5` Tuckute diagnostic stays nonpositive or mixed, narrow to a synthetic-target/control paper.

S82 literature refresh: [`top-venue-literature-refresh-2026-07-07.md`](top-venue-literature-refresh-2026-07-07.md) records the current scout read. Broad brain-tuning and privileged-information distillation claims are occupied; the live open cell is whether a brain-derived privileged target helps smaller-student KD beyond matched text-feature/permuted controls and survives real-brain transfer.

S82 launch status: the first detached rerun launch exited before reaching Python, so the stable launch uses `setsid`. TRIBE seed `0-2` artifact-saving rerun is active as PID `3827100` with Python child `3827120` on GPU 1, log `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.log`, and target run JSON `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json`. The first saved model artifact landed at `outputs/E016_tribe/phase3/model_artifacts/tribe_gpt2_n95999_s0-2_lam0.1_rerun/seed0_kd_only_lambda0`, and the rerun then entered `seed=0 arm=tribe_mse`. This is partial-arm progress only, not a result.

The textfeat seed `0-5` saved-student Tuckute scoring completed at `2026-07-07T20:12:13Z`, writing `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.tuckute_alignment.json` with 18/18 artifact rows scored and 0 missing/unusable rows. A 5-minute local monitor is active as PID `3827101`; latest status is written to `outputs/E016_tribe/phase3/rerun_realbrain_status_latest_20260707.md`. A postprocess watcher is active as PID `3836562`, with PID/log files `outputs/E016_tribe/phase3/combined_tuckute_analysis_watcher_20260707.pid` and `outputs/E016_tribe/phase3/combined_tuckute_analysis_watcher_20260707.log`; once the rerun Tuckute JSON appears it will run the seed `0-5` Tuckute analyzer automatically. No TRIBE rerun result JSON exists yet.

S82 audit tooling: `scripts/e016_audit_tuckute_alignment.py` now provides a reusable raw-row audit for the paired Tuckute analysis. It regression-passed against the saved seed `3-5` diagnostic with `all_checks_pass=true`, route `real_brain_warning_needs_claim_scope_review`, complete seeds `[3,4,5]`, TRIBE-minus-textfeat gain versus KD-only `-0.000861728910529826`, and versus permuted-control gains `-0.0007842046600033294`. After the combined seed `0-5` Tuckute analysis exists, run it on the rerun seed `0-2` TRIBE alignment plus existing seed `3-5` TRIBE alignment and completed seed `0-5` textfeat alignment.

S82 postprocess automation: a detached audit watcher is active as PID `3843773`, with PID/log files `outputs/E016_tribe/phase3/combined_tuckute_audit_watcher_20260707.pid` and `outputs/E016_tribe/phase3/combined_tuckute_audit_watcher_20260707.log`. It waits for `phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json`, then runs `scripts/e016_audit_tuckute_alignment.py` and writes `phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.audit.json`.

S82 interpretation gate: [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md) locks the postprocess acceptance checks and paper-route labels before the combined seed `0-5` Tuckute result exists. The gate requires complete seeds `[0,1,2,3,4,5]`, no missing artifacts, same endpoint/protocol, raw arithmetic agreement, and `all_checks_pass=true` before `/interpret`.

S82 rerun-safe status helper: `scripts/e016_phase3_status.py` now accepts explicit `--run-json`, `--analysis-json`, `--run-script`, `--train-cache`, and `--heldout-cache` paths. Use the explicit rerun command in Key Facts, not the bare default command, when checking the active seed `0-2` rerun. The explicit rerun check at `2026-07-07T21:02:22Z` reported `phase="training_running_or_interrupted"`, `health.status="runner_alive_log_quiet"`, active arm `seed=0, arm=tribe_mse`, completed-arm count `1`, and no rerun JSON/analyzer JSON.

S82 rich rerun monitor: `scripts/e016_monitor_phase3_status.py` now writes a compact latest JSON/Markdown snapshot around the rerun-safe status helper. The detached five-minute wrapper is active as PID `3850339`, with PID file `outputs/E016_tribe/phase3/rich_rerun_status_monitor_20260707.pid`, log `outputs/E016_tribe/phase3/rich_rerun_status_monitor_20260707.log`, latest JSON `outputs/E016_tribe/phase3/rerun_realbrain_rich_status_latest_20260707.json`, and latest Markdown `outputs/E016_tribe/phase3/rerun_realbrain_rich_status_latest_20260707.md`. The latest snapshot at `2026-07-07T21:10:23.298803+00:00` reported `phase="training_running_or_interrupted"`, `health.status="runner_alive_log_recent"`, completed arms `2/9`, latest completed arm `seed=0, arm=tribe_mse`, and active arm `seed=0, arm=tribe_perm`. This is progress monitoring only; no rerun JSON, rerun analyzer JSON, rerun Tuckute JSON, combined Tuckute analysis JSON, or combined Tuckute audit JSON exists yet.

S82 scorer watcher: the first ad hoc shell watcher, PID `3851658`, was retired because its `ps | grep` runner-exit check could match its own shell text after the rerun JSON appeared. The active replacement is `scripts/e016_watch_tuckute_eval.py`, PID `3853936`, PID file `outputs/E016_tribe/phase3/rerun_tuckute_eval_pywatcher_20260707.pid`, and log `outputs/E016_tribe/phase3/rerun_tuckute_eval_pywatcher_20260707.log`. It waits for the rerun JSON, polls `scripts/e016_phase3_status.py` until the selected run has `runner_process_count == 0`, then runs `scripts/e016_eval_saved_student_alignment.py` with `--require-artifacts` to write `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.tuckute_alignment.json`. This closes the handoff before the existing combined Tuckute analyzer watcher; it is postprocess automation only, not a result.

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
- Chose the real-brain diagnostic burden, smoke-tested one saved artifact, scored saved seed `3-5` TRIBE/textfeat students on Tuckute, and wrote the paired real-brain analysis.
- Recomputed the real-brain diagnostic from raw alignment rows in a local `/interpret` audit and routed it to claim-scope review.
- Reviewed the Tuckute evaluator code path against E003 scoring helpers; no immediate implementation blocker found.
- Selected and predeclared the bounded seed `0-2` TRIBE artifact-saving rerun before narrowing the paper route.
- Ran a focused Firecrawl Research literature refresh and wrote the top-venue route implications.
- Launched the rerun with `setsid` after the first detached launch died before Python; verified the stable Python child and GPU activity.
- Restarted/continued textfeat seed `0-5` Tuckute scoring, which completed cleanly with 18/18 artifact rows scored, and started the 5-minute local monitor.
- Added `scripts/e016_analyze_tuckute_alignment.py` and regression-checked it against the recorded seed `3-5` Tuckute analysis; it reproduces the load-bearing contrasts and PCA robustness means.
- Confirmed the rerun saved its first arm artifact and launched a detached postprocess watcher to run the combined seed `0-5` Tuckute analyzer after the rerun Tuckute output appears.
- Added `scripts/e016_audit_tuckute_alignment.py` and regression-checked it against the recorded seed `3-5` Tuckute diagnostic; it recomputes raw-row Tuckute contrasts and checks row/protocol/arithmetic/PCA consistency before `/interpret`.
- Launched a detached combined Tuckute audit watcher so the raw-row audit runs automatically after the combined analysis JSON appears.
- Wrote the combined Tuckute interpretation gate so a future positive/nonpositive/mixed/failed-audit result routes to the correct paper burden without creating a premature claim.
- Parameterized `scripts/e016_phase3_status.py` for explicit rerun monitoring; the default still reports the completed original full run, while the explicit rerun command correctly reports the live rerun.
- Added and launched `scripts/e016_monitor_phase3_status.py` as a rich five-minute rerun monitor; latest snapshot shows the rerun advancing through seed0 arms with 2/9 completed.
- Launched and hardened a detached rerun Tuckute scorer watcher so the saved-student real-brain evaluator runs automatically after the seed `0-2` rerun finishes.

## What To Do Next

1. Monitor `outputs/E016_tribe/phase3/rerun_realbrain_rich_status_latest_20260707.md` until the TRIBE rerun finishes.
2. Check `outputs/E016_tribe/phase3/rerun_tuckute_eval_pywatcher_20260707.log`; the Python watcher should score rerun TRIBE seed `0-2` on Tuckute after the rerun JSON lands and the training process exits.
3. Check `outputs/E016_tribe/phase3/combined_tuckute_analysis_watcher_20260707.log`; the watcher should compute the aligned seed `0-5` real-brain diagnostic against the completed textfeat seed `0-5` Tuckute output after the rerun Tuckute JSON appears.
4. If the Tuckute diagnostic becomes paper-load-bearing, run an independent second implementation or deeper code/stat review.
5. Do not claim brain-specific clearance or flip a rung from synthetic target-R2 or the post-hoc Tuckute diagnostic alone.

## Blockers / Open Loops

- The comparator route is not a final verdict and not brain-specific clearance.
- The synthetic-target comparison is now six seeds and stable against textfeat, but still not real-brain evidence.
- The saved-student Tuckute diagnostic is a warning against real-brain transfer: TRIBE does not beat KD/permuted/textfeat on the saved seed `3-5` real-brain endpoint.
- Textfeat clears only sentence-local frozen-teacher hidden-state supervision, not long-context/on-policy distillation or real-brain alignment.
- The original seed `0-2` TRIBE run did not save model artifacts; the selected replacement rerun is active but not complete.
- The prepared contextfeat builder is smoke-tested only. A full contextfeat cache/control is branch-gated behind E016 positive plus textfeat survival.
- The Tuckute saved-student evaluator has now run at full scale for saved seed `3-5`, but still requires `/interpret` before any claim.
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
- Completed extra TRIBE launcher: `outputs/E016_tribe/phase3/run_extra_tribe_s3-5_20260707.sh`, target JSON `outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.json`.
- Completed extra textfeat launcher: `outputs/E016_tribe/phase3/run_extra_textfeat_s3-5_20260707.sh`, target JSON `outputs/E016_tribe/phase3/phase3_extra_textfeat_gpt2_n95999_s3-5_lam0.1.json`.
- Completed extra-seed monitor log: `outputs/E016_tribe/phase3/extra_seed_progress_monitor_20260707.log`.
- Combined TRIBE run/analyzer/readiness: `outputs/E016_tribe/phase3/phase3_combined_tribe_gpt2_n95999_s0-5_lam0.1.json`, `.analysis.json`, `.readiness.json`.
- Combined textfeat run/analyzer/readiness: `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.json`, `.analysis.json`, `.readiness.json`.
- Combined comparator/audit: `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.json`, `.interpret_audit.json`.
- TRIBE saved-student Tuckute output: `outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.tuckute_alignment.json`.
- textfeat saved-student Tuckute output: `outputs/E016_tribe/phase3/phase3_extra_textfeat_gpt2_n95999_s3-5_lam0.1.tuckute_alignment.json`.
- Paired real-brain diagnostic analysis: `outputs/E016_tribe/phase3/phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment_analysis.json`.
- Local real-brain diagnostic `/interpret` audit: `outputs/E016_tribe/phase3/phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment.interpret_audit.json`.
- Active bounded rerun launcher: `outputs/E016_tribe/phase3/run_rerun_tribe_s0-2_save_20260707.sh`, PID `3827100`, Python child `3827120`, target JSON `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json`.
- Completed textfeat seed `0-5` Tuckute output: `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.tuckute_alignment.json` (18/18 artifact rows scored, 0 missing/unusable).
- Active rerun monitor: `outputs/E016_tribe/phase3/monitor_rerun_realbrain_20260707.sh`, PID `3827101`, latest status `outputs/E016_tribe/phase3/rerun_realbrain_status_latest_20260707.md`.
- Active rich rerun monitor: `scripts/e016_monitor_phase3_status.py`, PID `3850339`, PID file `outputs/E016_tribe/phase3/rich_rerun_status_monitor_20260707.pid`, log `outputs/E016_tribe/phase3/rich_rerun_status_monitor_20260707.log`, latest JSON `outputs/E016_tribe/phase3/rerun_realbrain_rich_status_latest_20260707.json`, latest Markdown `outputs/E016_tribe/phase3/rerun_realbrain_rich_status_latest_20260707.md`.
- Active rerun Tuckute scorer watcher: `scripts/e016_watch_tuckute_eval.py`, PID `3853936`, PID file `outputs/E016_tribe/phase3/rerun_tuckute_eval_pywatcher_20260707.pid`, log `outputs/E016_tribe/phase3/rerun_tuckute_eval_pywatcher_20260707.log`, target output `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.tuckute_alignment.json`.
- Active combined Tuckute analysis watcher: `outputs/E016_tribe/phase3/combined_tuckute_analysis_watcher_20260707.pid`, PID `3836562`, log `outputs/E016_tribe/phase3/combined_tuckute_analysis_watcher_20260707.log`.
- Active combined Tuckute audit watcher: `outputs/E016_tribe/phase3/combined_tuckute_audit_watcher_20260707.pid`, PID `3843773`, log `outputs/E016_tribe/phase3/combined_tuckute_audit_watcher_20260707.log`.
- Combined Tuckute interpretation gate: `docs/e016-combined-tuckute-interpretation-gate-2026-07-07.md`.
- Rerun-safe status command: `uv run python scripts/e016_phase3_status.py --pretty --log outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.log --run-json outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json --analysis-json outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.analysis.json --run-script outputs/E016_tribe/phase3/run_rerun_tribe_s0-2_save_20260707.sh`.
- Seed-aligned Tuckute analyzer: `uv run python scripts/e016_analyze_tuckute_alignment.py --tribe-alignment <tribe-s0-2.tuckute.json> --tribe-alignment outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.tuckute_alignment.json --textfeat-alignment outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.tuckute_alignment.json --expected-seeds 0,1,2,3,4,5 --min-seeds 6 --out outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json`.
- Seed-aligned Tuckute audit: `uv run python scripts/e016_audit_tuckute_alignment.py --tribe-alignment <tribe-s0-2.tuckute.json> --tribe-alignment outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.tuckute_alignment.json --textfeat-alignment outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.tuckute_alignment.json --analysis-json outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json --expected-seeds 0,1,2,3,4,5 --min-seeds 6 --out outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.audit.json`.
- Saved-student Tuckute evaluator: `uv run python scripts/e016_eval_saved_student_alignment.py --run-json <artifacted-run.json> --out <alignment.json> --reference-model gpt2-medium`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Comparator command after both analyzer JSONs are ready: `uv run python scripts/e016_compare_target_controls.py <tribe-analysis.json> <textfeat-analysis.json> --out <comparison.json>`.
