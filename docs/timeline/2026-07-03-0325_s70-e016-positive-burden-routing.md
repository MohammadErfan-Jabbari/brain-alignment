---
title: "S70 - E016 positive burden routing"
tags: [timeline, session]
---

# S70 - E016 Positive Burden Routing

## Purpose

Continue the autonomous `/goal` while E016 trains by converting the privileged-signal adjacency audit into executable handoff safeguards.

## Stances

Dominant stance: `/work`.

Supporting stance: `/meta`.

## What Happened

- Checked the active E016 full Phase-3 run and confirmed it still has no full run JSON and no analyzer JSON.
- Hardened [`../../scripts/e016_compare_target_controls.py`](../../scripts/e016_compare_target_controls.py) so the `tribe_stronger_than_textfeat_needs_review` branch carries explicit post-positive reviewer-burden metadata and next actions.
- Hardened [`../../scripts/e016_make_readiness_packet.py`](../../scripts/e016_make_readiness_packet.py) and [`../../scripts/e016_branch_decision.py`](../../scripts/e016_branch_decision.py) so their `must_not_claim`, burden, and route metadata do not treat TRIBE > textfeat as brain-specific clearance.
- Updated [`../../scripts/AGENTS.md`](../../scripts/AGENTS.md) with the new helper semantics.
- Recorded the tooling change as Step 36 in [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md).
- Updated the close records: [`../upspeed.md`](../upspeed.md), [`../ladder.md`](../ladder.md), and [`../tasks.md`](../tasks.md).

## Current Truth

The active full E016 Phase-3 run is still alive in training. Last status in S70: `phase=training_running_or_interrupted`, `health.status=runner_alive_log_quiet`, latest parsed marker `seed=1`, `arm=tribe_mse`, `lambda=0.1`, with `5/9` arm markers seen and `completed_arm_count=4`.

The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=67`). GPU fields remain liveness context only, not strict E016 attribution and not experiment evidence.

No run JSON exists yet. No analyzer JSON exists yet. The completed seed-0 plus seed-1 `kd_only` arm diagnostics are explicitly partial-arm diagnostics only. No experiment verdict, science claim, or ladder rung change exists yet.

## Checks Run

- `uv run python -m py_compile scripts/e016_compare_target_controls.py scripts/e016_make_readiness_packet.py scripts/e016_branch_decision.py`
- In-memory smoke over the post-positive comparator metadata, readiness burden metadata, and router comparison metadata.
- `uv run python scripts/e016_branch_decision.py` -> `status="waiting_for_run_json"`
- `uv run python scripts/e016_phase3_status.py --pretty`
- `git diff --check`
- Modified-doc relative-link check, excluding known old `docs/tasks.md` link debt to `references/codex-usage.md`

## Next Session

- Continue monitoring with `uv run python scripts/e016_phase3_status.py --pretty`.
- When the full run JSON exists, run `uv run python scripts/e016_branch_decision.py`.
- If the router says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
- If the readiness packet reports `gate.science_ready=true`, switch to `/interpret` before recording any E016 result.
- If E016 is positive at matched PPL, run the queued text-feature control only after confirming resources are free.
- If TRIBE beats textfeat, treat that as a review input, not clearance: clear the post-positive reviewer burden before any brain-specific top-venue claim.

## Related

- [`../upspeed.md`](../upspeed.md)
- [`../ladder.md`](../ladder.md)
- [`../tasks.md`](../tasks.md)
- [`../top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](../top-venue-privileged-signal-adjacency-audit-2026-07-03.md)
- [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
