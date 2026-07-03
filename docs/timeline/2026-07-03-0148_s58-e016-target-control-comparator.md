---
title: "S58 - E016 target-control comparator"
tags: [timeline, session]
aliases: [S58]
---

# S58 - E016 target-control comparator

## Purpose

Continue the active autonomous `/goal` while E016 trains by preparing the later TRIBE-vs-textfeat comparison required for any brain-specific positive branch.

## Stances

Dominant stance: `/work`.

Also used: `/plan` for the post-positive branch-routing logic.

## What happened

- Checked the active E016 run: the full run is alive in training, with no run JSON and no analyzer JSON.
- Added [`e016_compare_target_controls.py`](../../scripts/e016_compare_target_controls.py), a read-only comparator for science-ready TRIBE and text-feature analyzer JSONs.
- Updated [`scripts/AGENTS.md`](../../scripts/AGENTS.md), [`E016`](../experiments/E016_tribe-synthetic-brain-targets.md), [`e016-interpretation-protocol-2026-07-03.md`](../e016-interpretation-protocol-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md), and [`tasks.md`](../tasks.md).

## Current truth

E016 remains unadjudicated. Last status in S58: `phase=training_running_or_interrupted`, `health.status=runner_alive_log_recent`, latest parsed marker `seed=0`, `arm=tribe_mse`, `lambda=0.1`, with `2/9` arm markers seen.

No run JSON exists yet. No analyzer JSON exists yet. No experiment verdict, science claim, or ladder rung change exists yet.

## Checks run

- `uv run python -m py_compile scripts/e016_compare_target_controls.py`
- Comparator refusal test on existing smoke/incomplete analyzer JSONs (`ready=false`, `branch_hint.branch="not_ready"`)
- Temporary ready-analysis fixture tests for `tribe_stronger_than_textfeat_needs_review`, `dense_privileged_target_generic`, and `tribe_not_positive`
- `git diff --check`
- Modified-doc relative Markdown link check, excluding the known old `tasks.md` `references/codex-usage.md` debt
- `uv run python scripts/e016_phase3_status.py --pretty`

## Next session

- Continue monitoring E016 with `uv run python scripts/e016_phase3_status.py --pretty`.
- If the analyzer JSON appears, switch to `/interpret` and use [`e016-interpretation-protocol-2026-07-03.md`](../e016-interpretation-protocol-2026-07-03.md) as the manifest before recording any result.
- If E016 is positive and the text-feature control later runs, use [`e016_compare_target_controls.py`](../../scripts/e016_compare_target_controls.py) only after both analyzer JSONs are science-ready.
- If the runner exits without a run JSON, debug the runner/log before interpreting anything.

## Related

- [`e016-interpretation-protocol-2026-07-03.md`](../e016-interpretation-protocol-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
