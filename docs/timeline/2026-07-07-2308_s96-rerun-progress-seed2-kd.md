---
title: "S96 - Rerun progressed to seed2 KD"
tags: [timeline, work, E016, S96]
aliases: [S96, E016-rerun-progress-seed2-kd]
---

# S96 - Rerun progressed to seed2 KD

## Stance

`/work`

## What happened

- Continued the active top-venue goal by checking whether the E016 combined Tuckute gate had resolved.
- Ran a bounded 5-minute watch using `scripts/e016_tuckute_gate_status.py` once per minute.
- The first five checks stayed at completed arms `5/9`, active `seed=1 arm=tribe_perm lambda=0.1`.
- The final/follow-up status showed the sixth saved model artifact landed and the rerun entered `seed=2 arm=kd_only lambda=0.0`.

## Latest status

- `phase="waiting_for_rerun_run_json"`;
- `ready_for_interpret=false`;
- completed arms `6/9`;
- latest completed partial diagnostic: `seed=1 arm=tribe_perm lambda=0.1 ppl=99.333 target_r2=0.5971`;
- active arm: `seed=2 arm=kd_only lambda=0.0`;
- all selected watcher groups alive;
- missing `run_json`, `rerun_tuckute`, `analysis_json`, and `audit_json`.

## Result status

Partial-arm progress only. No rerun JSON, no rerun Tuckute JSON, no combined Tuckute analysis JSON, no combined Tuckute audit JSON, no six-seed real-brain result, no final E016 verdict, no brain-specific clearance, and no ladder change.

## Related

- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../tasks.md`](../tasks.md)
- [`../upspeed.md`](../upspeed.md)
