---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S74 - `/goal` continuation: added opt-in E016 trained-student artifact retention for future control/probe runs while E016 full Phase-3 keeps training; no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

The active E016 full Phase-3 run is still training. Last status check in S74: `checked_at_utc=2026-07-03T04:14:42.369947+00:00`; `phase=training_running_or_interrupted`; `health.status=runner_alive_log_recent`; runner processes are alive (`bash run_full_phase3_20260702.sh`, `uv run python scripts/run_tribe_phase3.py`, and the `.venv/bin/python3` child); `run_json.exists=false`; `analysis_json.exists=false`. Full train and heldout target caches remain present and validated as target-cache artifacts only: train `n_items=95999`, `target_dim=20484`; heldout `n_items=1999`, `target_dim=20484`.

Training has not produced a new result artifact. The latest parsed marker is now `seed=2`, `arm=kd_only`, `lambda=0.0`; `arm_markers_seen=7`; `completed_arm_count=6`; `arms_expected=9`. The completed diagnostics through seed 1 `tribe_perm` remain explicitly partial-arm diagnostics only, not Phase-3 results. The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=55` in the S74 sample), but GPU fields remain liveness context, not strict E016 attribution or evidence.

The positive-branch control ladder is now more concrete. [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md) records that the original WikiText row/header context can be replayed exactly from the E003 corpus extraction. [`e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py) writes joinable context metadata under `outputs/E016_tribe/kd_context_metadata/`, and [`build_context_feature_target_cache.py`](../scripts/build_context_feature_target_cache.py) can build a long-context `contextfeat` target cache. A CPU smoke with `sshleifer/tiny-gpt2`, four train sentences, and 16 dimensions passed. S74 also added opt-in `--save-model-dir` support to [`run_tribe_phase3.py`](../scripts/run_tribe_phase3.py), and regenerated the queued textfeat launcher so future textfeat controls save trained students for possible post-hoc probes or real-brain evaluation. This is plumbing only: no full textfeat/contextfeat cache or training should run until E016 justifies it.

The current source-facing planning bundle is: [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md), [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), and [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md).

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What Was Done

- Added opt-in trained-student artifact retention to [`../scripts/run_tribe_phase3.py`](../scripts/run_tribe_phase3.py): `--save-model-dir` saves each per-arm student with tokenizer plus an `e016_model_artifact.json` sidecar, and each row records `model_artifact_dir`.
- Updated [`../scripts/e016_make_textfeat_control_script.py`](../scripts/e016_make_textfeat_control_script.py), then regenerated `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`; the queued textfeat control will save trained students if it is ever launched.
- Updated [`../scripts/AGENTS.md`](../scripts/AGENTS.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), and [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md) Step 40.
- Verified `py_compile`, `git diff --check`, changed-doc relative links, regenerated launcher syntax, and a tiny CPU smoke that saved all three expected two-item arm artifacts with non-null `model_artifact_dir` fields.
- Latest non-wrap work commit: `cfd1399 feat: retain E016 control student artifacts`.

## What To Do Next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`; use the `gpu` block as a liveness clue only, not evidence.
2. If the runner exits without writing `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
3. When the run JSON exists, run `uv run python scripts/e016_branch_decision.py`; if it says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
4. Switch to `/interpret` only if the analyzer/readiness gate is science-ready. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
5. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free; when both analyzer JSONs are science-ready, use [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) before any brain-specific claim.
6. If E016 is positive even after `textfeat`, state the scope precisely: `textfeat` is a sentence-local teacher-hidden-state control. The now-prepared `contextfeat` path can test a context-conditioned teacher-feature control, but the full cache/training should wait for that branch.
7. If a positive branch needs post-hoc probes or real-brain evaluation, first check whether the needed `model_artifact_dir` entries exist. The active TRIBE full run started before artifact saving existed, so selected TRIBE arms may need rerunning with `--save-model-dir`.
8. If E016 is null at matched PPL, use [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), and [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) to frame the controlled-negative paper branch.

## Blockers / Open Loops

- The full E016 training run is incomplete: `run_json.exists=false`, `analysis_json.exists=false`.
- The completed arm diagnostics are not science results and must not be used for a verdict.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is training would compete for GPU and disk bandwidth.
- The prepared contextfeat builder is smoke-tested only. A full contextfeat cache/control is branch-gated behind E016 positive plus textfeat survival.
- On-policy distillation remains a separate protocol; contextfeat does not clear student-rollout teacher supervision.
- The active TRIBE full run is metrics-only with respect to model artifacts because it started before `--save-model-dir` existed.

## Key Facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Prepared textfeat model-artifact directory: `outputs/E016_tribe/phase3/model_artifacts/textfeat_gpt2_n95999_s0-1-2_lam0.1/` if the launcher is eventually run.
- Artifact-retention smoke output: `outputs/E016_tribe/phase3/phase3_smoke_save_model_test.json` and `outputs/E016_tribe/phase3/model_artifacts/smoke_save_model_test/`.
- Context metadata summary: `outputs/E016_tribe/kd_context_metadata/wikitext103_context_meta_summary.json`.
- Contextfeat smoke artifact: `outputs/E016_tribe/kd_targets/context_feature/smoke_train_contextfeat_d16.npz`.
- Expected full TRIBE artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Latest non-wrap work commit for this continuation: `cfd1399 feat: retain E016 control student artifacts`.
