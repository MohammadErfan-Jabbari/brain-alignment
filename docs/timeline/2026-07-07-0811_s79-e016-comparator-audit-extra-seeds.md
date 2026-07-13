---
title: "S79 - E016 comparator audit and extra-seed launch"
tags: [timeline, work, interpret, E016]
aliases: [S79]
---

# S79 - E016 comparator audit and extra-seed launch

**Date:** 2026-07-07
**Stance:** `/interpret` audit followed by `/work` continuation
**Scope:** Continue the `/goal` top-venue paper route after S78: audit the TRIBE-vs-textfeat comparator from raw rows, decide the next evidence burden, and launch the smallest follow-up compute that strengthens the claim without over-expanding controls.

## Summary

The local `/interpret` audit recomputed the ready TRIBE-vs-textfeat comparison directly from raw run rows and wrote `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.interpret_audit.json`. The recompute matched the comparator means and gates. The prepared sentence-local textfeat control does not explain the TRIBE synthetic-target gain in the completed `0,1,2` seed set.

The interpretation is deliberately narrow. This supports the post-positive branch only: TRIBE survives the prepared textfeat control on the synthetic target endpoint. It is not a final E016 verdict, not brain-specific clearance, and not a ladder update. The limiting facts are unchanged: only 3 seeds, synthetic target-R2 endpoint, no long-context/on-policy control, no real-brain evaluation, and no saved TRIBE students from the original run.

The next evidence burden selected was extra artifact-saving seeds `3,4,5` for both TRIBE and textfeat, before any contextfeat/on-policy/real-brain escalation. Both detached jobs and a four-minute monitor were launched.

## Comparator Audit

Audit artifact:

- `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.interpret_audit.json`

Claim-intent manifest:

- expected claim: TRIBE is stronger than the prepared textfeat matched-information control, but only as a narrow post-positive synthetic-target signal.
- evidence: E016 Step 44 and `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json`.
- overturn-if: any raw-row recompute, PPL/gate audit, or seed-aligned check fails, or textfeat gains match/exceed TRIBE gains.

Result:

- all readiness, seed-alignment, PPL, and comparator-mean checks passed.
- TRIBE-minus-textfeat gain versus KD-only: mean `+0.076731`, seed values `[+0.076338, +0.075906, +0.077948]`, all positive, sign-flip `p=0.25`.
- TRIBE-minus-textfeat gain versus permuted-control gains: mean `+0.069492`, seed values `[+0.065526, +0.072959, +0.069991]`, all positive, sign-flip `p=0.25`.
- maximum observed relative PPL delta across target/permuted-vs-KD checks: `0.009220`, below the `0.05` tolerance.

Interpretation boundary:

- survives prepared sentence-local textfeat control;
- does not clear long-context/on-policy distillation;
- does not clear rich-feedback privileged-signal adjacency;
- does not show real-brain alignment or downstream utility;
- still needs stronger seed-level evidence before a top-tier positive claim.

## Extra-Seed Launch

TRIBE:

- launcher: `outputs/E016_tribe/phase3/run_extra_tribe_s3-5_20260707.sh`
- PID: `3770641`
- Python child at verification: `3770685`
- GPU: 1
- target output: `outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.json`
- target analyzer: `outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.analysis.json`
- model artifacts: `outputs/E016_tribe/phase3/model_artifacts/tribe_gpt2_n95999_s3-5_lam0.1/`

Textfeat:

- launcher: `outputs/E016_tribe/phase3/run_extra_textfeat_s3-5_20260707.sh`
- PID: `3770642`
- Python child at verification: `3770687`
- GPU: 2
- target output: `outputs/E016_tribe/phase3/phase3_extra_textfeat_gpt2_n95999_s3-5_lam0.1.json`
- target analyzer: `outputs/E016_tribe/phase3/phase3_extra_textfeat_gpt2_n95999_s3-5_lam0.1.analysis.json`
- model artifacts: `outputs/E016_tribe/phase3/model_artifacts/textfeat_gpt2_n95999_s3-5_lam0.1/`

Monitor:

- launcher: `outputs/E016_tribe/phase3/monitor_extra_seed_progress_20260707.sh`
- PID: `3770643`
- log: `outputs/E016_tribe/phase3/extra_seed_progress_monitor_20260707.log`
- interval: 240 seconds

Verification after launch:

- both launchers and both Python children were alive;
- both workers were consuming CPU and loading/running;
- textfeat had entered seed 3 `kd_only`;
- the monitor recorded process and artifact samples.

## Next

Monitor both extra-seed runs until run JSON, analyzer JSON, and readiness JSON exist. Then merge or compare seeds `0-5`, rerun the TRIBE-vs-textfeat audit, and only then decide whether the next burden is context/on-policy control, real-brain evaluation using saved artifacts, or a narrowed synthetic-target claim.

## Related

- `../ladder.md`
- `../upspeed.md`
- `../tasks.md`
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- `../top-venue-paper-plan-2026-07-03.md`
- `../top-venue-evidence-ledger-2026-07-03.md`
