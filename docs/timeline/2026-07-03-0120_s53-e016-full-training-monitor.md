---
title: "S53 - E016 full training monitor"
tags: [timeline, session]
---

# S53 - E016 full training monitor

## Purpose

Continue the active autonomous `/goal` while the full E016 run advances from target-cache generation into training. Keep the evidence boundary clean: improve monitoring and record artifact status without interpreting a result before the analyzer exists.

## Stances

Dominant stance: `/work`.

## What happened

- Verified and extended [`e016_phase3_status.py`](../../scripts/e016_phase3_status.py) with ETA fields for the train-cache build.
- Fixed the status helper to parse train and heldout cache-builder sections separately, so heldout batches use the `1999`-item denominator instead of the `95999`-item train denominator.
- Confirmed the full train target cache materialized at `2026-07-03T00:42:59.151237+00:00` with sidecar `n_items=95999`, `target_dim=20484`, and target-cache-only science status.
- Confirmed the full heldout target cache materialized at `2026-07-03T01:00:04.768769+00:00` with sidecar `n_items=1999`, `target_dim=20484`, and target-cache-only science status.
- Confirmed launcher validation printed finite train and heldout target arrays with `missing=0`.
- Extended the status helper to report training-arm markers (`seed`, `arm`, `lambda`, marker count) and to discover the active `run_tribe_phase3.py` runner process.
- Recorded these support changes as E016 Steps 21-24 in [`E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md).

## Current truth

The full E016 Phase-3 run is alive in training. Last status check in S53: `phase=training_running_or_interrupted`; parent launcher plus `uv run python scripts/run_tribe_phase3.py` and its `.venv/bin/python3` child were present; latest parsed training marker was `seed=0`, `arm=kd_only`, `lambda=0.0`, with `1/9` arm markers seen.

No Phase-3 run JSON exists yet. No analyzer JSON exists yet. No experiment verdict, science claim, or ladder rung change exists yet.

## Checks run

- `uv run python -m py_compile scripts/e016_phase3_status.py`
- `uv run python scripts/e016_phase3_status.py --pretty`
- `git diff --check`
- `ps -eo pid=,etime=,stat=,cmd= | rg 'run_tribe_phase3|run_full_phase3|python scripts/run_tribe'`
- `nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits`

## Next session

- Continue monitoring E016 with `uv run python scripts/e016_phase3_status.py --pretty`.
- If the runner exits without writing `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
- When `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json` exists, switch to `/interpret` and inspect gate completeness, all paired seeds, PPL matching, paired deltas, and sign-flip P-values before recording any result.
- Run the prepared text-feature control only if the TRIBE result is positive enough to require a brain-specificity control and resources are free.

## Related

- [`../upspeed.md`](../upspeed.md)
- [`../ladder.md`](../ladder.md)
- [`../tasks.md`](../tasks.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../../scripts/e016_phase3_status.py`](../../scripts/e016_phase3_status.py)
