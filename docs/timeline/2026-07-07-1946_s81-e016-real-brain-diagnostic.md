---
title: "S81 - E016 saved-student real-brain diagnostic"
tags: [timeline, E016, work, interpret]
aliases: [S81, E016-real-brain-diagnostic]
---

# S81 - E016 saved-student real-brain diagnostic

**Date:** 2026-07-07

**Stances:** `/work` to produce the Tuckute diagnostic; local `/interpret` boundary while recording it.

## What Changed

- Chose the real-brain evaluation burden after the combined six-seed synthetic comparator held.
- Verified that both extra seed `3-5` run JSONs had all 9 saved model artifacts.
- Ran `scripts/e016_eval_saved_student_alignment.py` on the saved TRIBE and textfeat students with `--require-artifacts`.
- Wrote the paired diagnostic analysis artifact: `outputs/E016_tribe/phase3/phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment_analysis.json`.
- Wrote the local raw-row audit artifact: `outputs/E016_tribe/phase3/phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment.interpret_audit.json`.

## Result

The diagnostic moved against the brain-specific positive branch. On Tuckute sub-ROI unique-R2:

- TRIBE target versus KD-only: mean `-0.000735`, seed values `[-0.002065, -0.000638, +0.000498]`.
- TRIBE target versus TRIBE permuted: mean `-0.001717`, seed values `[-0.002131, -0.001670, -0.001348]`.
- TRIBE-minus-textfeat gain versus KD-only: mean `-0.000862`, seed values `[-0.002114, -0.000189, -0.000282]`.
- TRIBE-minus-textfeat gain versus permuted-control gains: mean `-0.000784`, seed values `[-0.002100, -0.000382, +0.000130]`.

PCA robustness did not rescue the branch: TRIBE-minus-textfeat gain versus KD-only stayed negative at PCA `25`, `50`, and `100`.

The local audit passed row-count, seed-arm grid, endpoint/protocol, arithmetic-match, and PCA-robustness checks. Its route is `real_brain_warning_needs_claim_scope_review`.

## Boundary

This is a diagnostic, not a final E016 verdict: it is post-hoc, ROI-level Tuckute, and only saved seed `3-5` because the original TRIBE seed `0-2` students were not saved. It is still a serious warning. The six-seed synthetic target-R2 branch survives textfeat, but the saved-student real-brain endpoint does not support a brain-specific positive claim.

## Next

- Decide whether the paper route narrows to a synthetic-target/control contribution or whether a predeclared real-brain robustness/rerun is worth the compute.
- Run code review of the evaluator before any paper claim uses the Tuckute diagnostic.

## Verification

- One-row smoke of the Tuckute evaluator on a saved TRIBE artifact passed.
- Full TRIBE Tuckute evaluation scored 9/9 artifacts with 0 missing rows.
- Full textfeat Tuckute evaluation scored 9/9 artifacts with 0 missing rows.
- Independent analysis readback checked row counts, seeds, arithmetic identities, and contrast means.

## Related

- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md)
- [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`../ladder.md`](../ladder.md)
