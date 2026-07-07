---
title: "S95 - Tuckute gate progress summary"
tags: [timeline, work, E016, S95]
aliases: [S95, E016-tuckute-gate-progress-summary]
---

# S95 - Tuckute gate progress summary

## Stance

`/work`

## What happened

- Continued the active top-venue goal by checking whether the E016 combined Tuckute gate had resolved.
- `uv run scripts/e016_tuckute_gate_status.py --markdown` still reported `phase="waiting_for_rerun_run_json"`, `ready_for_interpret=false`, and missing `run_json`, `rerun_tuckute`, `analysis_json`, and `audit_json`.
- The selected rerun remained alive with completed arms `5/9`, active arm `seed=1 arm=tribe_perm lambda=0.1`, and all selected postprocess watcher groups alive.
- Extended `scripts/e016_tuckute_gate_status.py` so the same command also embeds compact rerun progress/ETA from `scripts/e016_phase3_status.py`.
- Updated `scripts/AGENTS.md` to record the helper's expanded status scope.

## Verification

- `uv run python -m py_compile scripts/e016_tuckute_gate_status.py`
- `uv run scripts/e016_tuckute_gate_status.py --markdown`
- `uv run scripts/e016_tuckute_gate_status.py --pretty`

## Result status

Monitoring/handoff utility only. No rerun JSON, no rerun Tuckute JSON, no combined Tuckute analysis JSON, no combined Tuckute audit JSON, no six-seed real-brain result, no final E016 verdict, no brain-specific clearance, and no ladder change.

## Related

- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../tasks.md`](../tasks.md)
- [`../upspeed.md`](../upspeed.md)
