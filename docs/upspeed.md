---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S73 - `/goal` continuation: recovered WikiText context metadata and CPU-smoked a future `contextfeat` control builder while E016 full Phase-3 keeps training; no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current State

The active E016 full Phase-3 run is still training. Last status check in S73: `checked_at_utc=2026-07-03T04:03:04.350959+00:00`; `phase=training_running_or_interrupted`; `health.status=runner_alive_log_quiet`; runner processes are alive (`bash run_full_phase3_20260702.sh`, `uv run python scripts/run_tribe_phase3.py`, and the `.venv/bin/python3` child); `run_json.exists=false`; `analysis_json.exists=false`. Full train and heldout target caches remain present and validated as target-cache artifacts only: train `n_items=95999`, `target_dim=20484`; heldout `n_items=1999`, `target_dim=20484`.

Training has not produced a new result artifact. The latest parsed marker remains `seed=1`, `arm=tribe_perm`, `lambda=0.1`; `arm_markers_seen=6`; `completed_arm_count=5`; `arms_expected=9`. The completed diagnostics through seed 1 `tribe_mse` remain explicitly partial-arm diagnostics only, not Phase-3 results. The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=66` in the S73 sample), but GPU fields remain liveness context, not strict E016 attribution or evidence.

The positive-branch control ladder is now more concrete. [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md) records that the original WikiText row/header context can be replayed exactly from the E003 corpus extraction. [`e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py) writes joinable context metadata under `outputs/E016_tribe/kd_context_metadata/`, and [`build_context_feature_target_cache.py`](../scripts/build_context_feature_target_cache.py) can build a long-context `contextfeat` target cache. A CPU smoke with `sshleifer/tiny-gpt2`, four train sentences, and 16 dimensions passed. This is plumbing only: no full contextfeat cache or training should run until E016 is positive and survives the prepared sentence-local `textfeat` control.

The current source-facing planning bundle is: [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md), [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), and [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md).

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What Was Done

- Added [`../scripts/e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py), a CPU-only helper that replays the original WikiText extraction and verifies exact equality against the cached KD corpus.
- Ran `HF_HOME=/home/centcom/data/hf-cache uv run python scripts/e016_recover_kd_context_metadata.py --overwrite`; it returned `corpus_replay="exact_match"` and wrote gitignored metadata for 96,000 train and 2,000 heldout rows.
- Added [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md), documenting that a recovered-context `contextfeat` control is mechanically feasible while on-policy remains a separate runner protocol.
- Added [`../scripts/build_context_feature_target_cache.py`](../scripts/build_context_feature_target_cache.py), a possible post-positive long-context non-brain target builder that conditions a frozen LM on recovered context and pools target-sentence hidden states.
- CPU-smoked `build_context_feature_target_cache.py` with `sshleifer/tiny-gpt2`, 4 train items, target dim 16, `--device cpu`; it saved `outputs/E016_tribe/kd_targets/context_feature/smoke_train_contextfeat_d16.npz` with `shape=(4, 16)` and `context_items_with_previous=3`.
- Updated [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md) Steps 38-39, and [`../scripts/AGENTS.md`](../scripts/AGENTS.md).
- Verified `py_compile`, exact corpus replay, the contextfeat CPU smoke, `git diff --check`, and changed-doc relative links.
- Latest non-wrap work commits: `c142f61 feat: recover E016 context metadata`; `19be346 feat: add E016 contextfeat target builder`.

## What To Do Next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`; use the `gpu` block as a liveness clue only, not evidence.
2. If the runner exits without writing `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
3. When the run JSON exists, run `uv run python scripts/e016_branch_decision.py`; if it says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
4. Switch to `/interpret` only if the analyzer/readiness gate is science-ready. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
5. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free; when both analyzer JSONs are science-ready, use [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) before any brain-specific claim.
6. If E016 is positive even after `textfeat`, state the scope precisely: `textfeat` is a sentence-local teacher-hidden-state control. The now-prepared `contextfeat` path can test a context-conditioned teacher-feature control, but the full cache/training should wait for that branch.
7. If E016 is null at matched PPL, use [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), and [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) to frame the controlled-negative paper branch.

## Blockers / Open Loops

- The full E016 training run is incomplete: `run_json.exists=false`, `analysis_json.exists=false`.
- The completed arm diagnostics are not science results and must not be used for a verdict.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is training would compete for GPU and disk bandwidth.
- The prepared contextfeat builder is smoke-tested only. A full contextfeat cache/control is branch-gated behind E016 positive plus textfeat survival.
- On-policy distillation remains a separate protocol; contextfeat does not clear student-rollout teacher supervision.

## Key Facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Context metadata summary: `outputs/E016_tribe/kd_context_metadata/wikitext103_context_meta_summary.json`.
- Contextfeat smoke artifact: `outputs/E016_tribe/kd_targets/context_feature/smoke_train_contextfeat_d16.npz`.
- Expected full TRIBE artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Watch-finalize command: `uv run python scripts/e016_watch_finalize_phase3.py --watch --interval-s 300`.
- Branch router command: `uv run python scripts/e016_branch_decision.py`.
- Latest non-wrap work commits for this continuation: `c142f61 feat: recover E016 context metadata`; `19be346 feat: add E016 contextfeat target builder`.
