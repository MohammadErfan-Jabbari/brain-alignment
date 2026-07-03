---
title: "S72 - On-policy context-distillation audit"
tags: [timeline, session]
---

# S72 - On-Policy Context-Distillation Audit

## Purpose

Continue the autonomous `/goal` while E016 trains by checking whether the 2026 on-policy/context/self-distillation frontier changes the top-venue control burden.

## Stances

Dominant stance: `/scout`.

Supporting stance: `/work`.

## What Happened

- Checked the active E016 full Phase-3 run and confirmed it still has no full run JSON and no analyzer JSON.
- Searched 2026 on-policy/context/self-/privileged-information distillation sources and found that OPD/OPCD/OPSD/PI-distillation/GATES/SDPO/HDPO/OEL-style work makes privileged context and on-policy teacher supervision an active LLM field.
- Added [`../top-venue-on-policy-context-distillation-audit-2026-07-03.md`](../top-venue-on-policy-context-distillation-audit-2026-07-03.md), a focused `/scout` memo that distinguishes the prepared sentence-local `textfeat` target from unresolved long-context/on-policy comparators.
- Updated [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md), [`../top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md), [`../top-venue-open-question-audit-2026-07-03.md`](../top-venue-open-question-audit-2026-07-03.md), [`../top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](../top-venue-privileged-signal-adjacency-audit-2026-07-03.md), and [`../01-research-landscape.md`](../01-research-landscape.md) so they do not treat `textfeat` as clearing long-context/on-policy distillation.
- Updated the close records: [`../upspeed.md`](../upspeed.md), [`../ladder.md`](../ladder.md), and [`../tasks.md`](../tasks.md).

## Current Truth

The active full E016 Phase-3 run is still alive in training. Last status in S72: `checked_at_utc=2026-07-03T03:43:55.868994+00:00`, `phase=training_running_or_interrupted`, `health.status=runner_alive_log_recent`, latest parsed marker `seed=1`, `arm=tribe_perm`, `lambda=0.1`, with `6/9` arm markers seen and `completed_arm_count=5`.

The status helper reports node-level GPU activity (`gpu.available=true`, `active_gpu_count=2`, instantaneous `max_utilization_gpu_pct=60`). GPU fields remain liveness context only, not strict E016 attribution and not experiment evidence.

No run JSON exists yet. No analyzer JSON exists yet. The completed-arm diagnostics are explicitly partial-arm diagnostics only. No experiment verdict, science claim, or ladder rung change exists yet.

## Checks Run

- `uv run python scripts/e016_phase3_status.py --pretty`
- `git diff --check`
- Changed-doc relative-link check over the six scout/planning docs

## Next Session

- Continue monitoring with `uv run python scripts/e016_phase3_status.py --pretty`.
- When the full run JSON exists, run `uv run python scripts/e016_branch_decision.py`.
- If the router says `needs_finalizer`, run `uv run python scripts/e016_watch_finalize_phase3.py` or `uv run python scripts/e016_finalize_phase3.py`.
- If the readiness packet reports `gate.science_ready=true`, switch to `/interpret` before recording any E016 result.
- If E016 is positive at matched PPL, run the queued text-feature control only after confirming resources are free.
- If TRIBE beats textfeat, state the scope precisely: textfeat is a sentence-local teacher-hidden-state control, not long-context/on-policy or real-brain clearance.

## Related

- [`../upspeed.md`](../upspeed.md)
- [`../ladder.md`](../ladder.md)
- [`../tasks.md`](../tasks.md)
- [`../top-venue-on-policy-context-distillation-audit-2026-07-03.md`](../top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`../top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
