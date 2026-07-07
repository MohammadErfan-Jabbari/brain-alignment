---
title: "S82 - E016 real-brain robustness rerun launch"
tags: [timeline, E016, work, plan]
aliases: [S82, E016-real-brain-rerun-launch]
---

# S82 - E016 real-brain robustness rerun launch

**Date:** 2026-07-07

**Stances:** `/plan` for claim-scope routing and process inspection; `/work` for the bounded rerun launch.

## What Changed

- Predeclared the bounded real-brain robustness rerun in [`../top-venue-claim-scope-review-2026-07-07.md`](../top-venue-claim-scope-review-2026-07-07.md).
- Launched only the missing TRIBE seed `0,1,2` artifact-saving rerun under the original Phase-3 protocol.
- Kept textfeat training fixed: textfeat seed `0-5` artifacts already exist, so only Tuckute scoring was needed.
- Completed textfeat seed `0-5` Tuckute scoring.
- Started a local 5-minute monitor for process/artifact status.
- Added and regression-checked `scripts/e016_analyze_tuckute_alignment.py` for the seed `0-5` real-brain handoff.

## Live State

- TRIBE rerun launcher: `outputs/E016_tribe/phase3/run_rerun_tribe_s0-2_save_20260707.sh`
- TRIBE rerun process: PID `3827100`, Python child `3827120`, GPU 1
- TRIBE rerun log: `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.log`
- textfeat seed `0-5` Tuckute output: `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.tuckute_alignment.json` (18/18 artifact rows scored, 0 missing/unusable)
- monitor: PID `3827101`, latest status `outputs/E016_tribe/phase3/rerun_realbrain_status_latest_20260707.md`

The first detached rerun attempt exited before reaching Python. Relaunching with `setsid` fixed the process-survival issue; after a one-minute stability check the rerun had entered `seed=0 arm=kd_only` and GPU 1 was active.

## Boundary

This is an active evidence-gathering state, not a result. No TRIBE rerun JSON, rerun Tuckute JSON, aligned six-seed real-brain diagnostic, final E016 verdict, brain-specific clearance, or rung change exists yet.

## Next

- Monitor the status file until the TRIBE rerun finishes.
- Score rerun TRIBE seed `0-2` on Tuckute if the launcher has not already done so.
- Combine rerun TRIBE seed `0-2` with existing TRIBE seed `3-5` diagnostics and compare against textfeat seed `0-5` using `scripts/e016_analyze_tuckute_alignment.py`.
- Choose narrowed synthetic-target/control paper versus reopened positive route using the predeclared kill criteria.

## Related

- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../top-venue-claim-scope-review-2026-07-07.md`](../top-venue-claim-scope-review-2026-07-07.md)
- [`../upspeed.md`](../upspeed.md)
- [`../ladder.md`](../ladder.md)
