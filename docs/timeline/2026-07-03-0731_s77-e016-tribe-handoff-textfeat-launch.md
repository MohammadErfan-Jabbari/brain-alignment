---
title: "S77 - E016 TRIBE handoff and textfeat launch"
tags: [timeline, work, interpret, E016]
aliases: [S77]
---

# S77 - E016 TRIBE handoff and textfeat launch

**Date:** 2026-07-03
**Stance:** `/interpret` with a `/work` continuation for the branch-required control
**Scope:** `/goal` continuation toward the top-venue paper branch: finalize the completed TRIBE artifact to a guarded handoff, audit it without over-claiming, and launch the matched-information control required by the branch router.

## Summary

The full E016 TRIBE Phase-3 run completed after S76 and produced the full run JSON, analyzer JSON, and readiness packet. The analyzer gate is science-ready, complete for 3 seeds x 3 arms, matched PPL, full train/heldout/target-dimension checks, and heldout target metrics. The readiness route is `tribe_positive_needs_textfeat`: a synthetic-target TRIBE branch that requires the matched-information text-feature control before any brain-specific interpretation.

An independent recompute audit matched the analyzer on grid completeness, paired target-R2 deltas, and PPL matching. This audit supports the branch handoff only; it is not a final E016 verdict and cannot flip a rung.

After confirming the TRIBE runner was complete and resources were free, the prepared `textfeat` control was launched detached on GPU 1. The launcher built and validated full text-feature train and heldout caches, then entered the full `scripts/run_tribe_phase3.py` training arms. No textfeat run JSON or analyzer JSON exists yet.

## TRIBE Handoff

Artifacts:

- run JSON: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`
- analyzer JSON: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`
- readiness JSON: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.readiness.json`
- independent audit: `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.interpret_audit.json`

Gate:

- `science_ready=true`
- `arm_seed_grid_complete=true`
- `all_paired_common_seeds=true`
- `ppl_matched_all_lambdas=true`
- `has_heldout_target_metric=true`
- `train_size_ready=true`
- `heldout_size_ready=true`
- `target_dim_ready=true`
- `paper_branch_hint.branch="tribe_positive_needs_textfeat"`

Audit highlights:

- TRIBE target minus permuted target mean synthetic target-R2 delta: `+0.071871`, values `[+0.067040, +0.075710, +0.072863]`, sign-flip `p=0.25`.
- TRIBE target minus KD-only mean synthetic target-R2 delta: `+0.077492`, values `[+0.077134, +0.076934, +0.078409]`, sign-flip `p=0.25`.
- Mean relative PPL deltas versus KD-only: `0.004973` for TRIBE target and `0.004875` for TRIBE permuted; all per-seed deltas stayed below the 0.05 matching tolerance.

## Branch Router

`uv run python scripts/e016_branch_decision.py` returned:

- `status="textfeat_control_required"`
- `route="run_textfeat_after_resource_check"`
- `active_runner_process_count=0`
- reason: TRIBE-only positive cannot support brain specificity; matched-information control is required.

## Textfeat Control

Launcher:

- script: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`
- detached process root: PID `3428588`
- GPU: `GPU=1`
- log: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.log`
- target run JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`
- target analyzer JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json`
- saved-student artifact root: `outputs/E016_tribe/phase3/model_artifacts/textfeat_gpt2_n95999_s0-1-2_lam0.1/`

State at close:

- clean active launch began at `2026-07-03T07:21:00Z`
- train text-feature cache saved: shape `(95999, 20484)`, `elapsed_s=176.718`, finite, `missing=0`
- heldout text-feature cache saved: shape `(1999, 20484)`, `elapsed_s=9.014`, finite, `missing=0`
- launcher entered the full GPT-2 textfeat arms at `2026-07-03T07:29:40Z`
- latest monitored arm: seed 0 `kd_only`
- no textfeat run JSON or analyzer JSON yet

## Result Boundary

No final E016 verdict landed. The TRIBE artifact is analyzer-ready and routes to the textfeat control, but it does not support a brain-specific claim. The textfeat control is running and has not produced evidence yet. No ladder rung changed.

## Next

Monitor the textfeat log and process. When the textfeat run JSON appears, run the finalizer/analyzer/readiness path for that run. When both analyzer JSONs are science-ready, run `scripts/e016_compare_target_controls.py`, then switch to `/interpret` for the comparison and reviewer-burden audit. Do not run contextfeat, extra seeds, or real-brain probes while textfeat is active.

## Related

- [`../ladder.md`](../ladder.md)
- [`../upspeed.md`](../upspeed.md)
- [`../tasks.md`](../tasks.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`../top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md)
