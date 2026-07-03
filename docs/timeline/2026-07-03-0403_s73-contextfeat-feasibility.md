---
title: "S73 - Contextfeat feasibility"
tags: [timeline, session]
---

# S73 - Contextfeat Feasibility

## Purpose

Continue the autonomous `/goal` while E016 trains by making the next positive-branch control burden concrete without starting another GPU run.

## Stances

Dominant stance: `/work`.

Supporting stance: `/scout`.

## What Happened

- Checked the active E016 full Phase-3 run and confirmed it still has no full run JSON and no analyzer JSON.
- Added [`../../scripts/e016_recover_kd_context_metadata.py`](../../scripts/e016_recover_kd_context_metadata.py), a CPU-only helper that replays the original E003 WikiText extraction, verifies exact equality against the cached KD corpus, and writes joinable context metadata under `outputs/E016_tribe/kd_context_metadata/`.
- Ran the context recovery helper with `--overwrite`; it returned `corpus_replay="exact_match"` for 96,000 train rows and 2,000 heldout rows.
- Added [`../top-venue-long-context-control-feasibility-2026-07-03.md`](../top-venue-long-context-control-feasibility-2026-07-03.md), recording that a recovered-context `contextfeat` control is mechanically feasible while on-policy distillation remains a separate runner protocol.
- Added [`../../scripts/build_context_feature_target_cache.py`](../../scripts/build_context_feature_target_cache.py), a possible post-positive target-cache builder that conditions a frozen LM on recovered same-document context and pools target-sentence hidden states into the Phase-3 target-cache schema.
- CPU-smoked the `contextfeat` builder with `sshleifer/tiny-gpt2`, 4 train items, target dim 16, `--device cpu`; it saved `outputs/E016_tribe/kd_targets/context_feature/smoke_train_contextfeat_d16.npz` with `shape=(4, 16)` and `context_items_with_previous=3`.
- Updated [`../../scripts/AGENTS.md`](../../scripts/AGENTS.md), [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md), [`../top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md), [`../top-venue-on-policy-context-distillation-audit-2026-07-03.md`](../top-venue-on-policy-context-distillation-audit-2026-07-03.md), and [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md).
- Updated the close records: [`../upspeed.md`](../upspeed.md), [`../ladder.md`](../ladder.md), and [`../tasks.md`](../tasks.md).

## Current Truth

The active full E016 Phase-3 run is still alive in training. Last status in S73: `checked_at_utc=2026-07-03T04:03:04.350959+00:00`, `phase=training_running_or_interrupted`, `health.status=runner_alive_log_quiet`, latest parsed marker `seed=1`, `arm=tribe_perm`, `lambda=0.1`, with `6/9` arm markers seen and `completed_arm_count=5`.

The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=66`). GPU fields remain liveness context only, not strict E016 attribution and not experiment evidence.

No run JSON exists yet. No analyzer JSON exists yet. The completed-arm diagnostics are explicitly partial-arm diagnostics only. No experiment verdict, science claim, or ladder rung change exists yet.

The `contextfeat` path is plumbing only. It must not be promoted to a full cache/training run unless E016 is positive and survives the prepared sentence-local `textfeat` control.

## Checks Run

- `uv run python -m py_compile scripts/e016_recover_kd_context_metadata.py`
- `HF_HOME=/home/centcom/data/hf-cache uv run python scripts/e016_recover_kd_context_metadata.py --overwrite`
- `uv run python -m py_compile scripts/build_context_feature_target_cache.py scripts/e016_recover_kd_context_metadata.py`
- `HF_HOME=/home/centcom/data/hf-cache uv run python scripts/build_context_feature_target_cache.py --split train --start 0 --limit 4 --model sshleifer/tiny-gpt2 --target-dim 16 --max-length 64 --batch-size 2 --device cpu --out outputs/E016_tribe/kd_targets/context_feature/smoke_train_contextfeat_d16.npz --overwrite`
- `uv run python scripts/e016_phase3_status.py --pretty`
- `git diff --check`
- Changed-doc relative-link check

## Next Session

- Continue monitoring with `uv run python scripts/e016_phase3_status.py --pretty`.
- When the full run JSON exists, run `uv run python scripts/e016_branch_decision.py`.
- If the router says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
- If the readiness packet reports `gate.science_ready=true`, switch to `/interpret` before recording any E016 result.
- If E016 is positive at matched PPL, run the queued text-feature control only after confirming resources are free.
- If E016 is positive even after `textfeat`, use the recovered context metadata and `contextfeat` builder as the next non-brain control candidate; do not treat it as on-policy/student-rollout clearance.

## Related

- [`../upspeed.md`](../upspeed.md)
- [`../ladder.md`](../ladder.md)
- [`../tasks.md`](../tasks.md)
- [`../top-venue-long-context-control-feasibility-2026-07-03.md`](../top-venue-long-context-control-feasibility-2026-07-03.md)
- [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`../top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
