---
title: "S78 - E016 textfeat completion and comparator handoff"
tags: [timeline, work, interpret, E016]
aliases: [S78]
---

# S78 - E016 textfeat completion and comparator handoff

**Date:** 2026-07-03
**Stance:** `/work` close with `/interpret` handoff
**Scope:** `/goal` continuation toward the top-venue paper branch: confirm the matched-information textfeat control finished, finalize its analyzer/readiness packet, compare it against the TRIBE branch, and record the comparator as review input rather than a verdict.

## Summary

The full E016 matched-information `textfeat` control completed. The runner wrote the full run JSON and analyzer JSON, and `scripts/e016_finalize_phase3.py` produced the readiness packet. The textfeat readiness gate is science-ready: complete for 3 seeds x 3 arms, matched PPL, full-scale train/heldout/target-dimension checks, and heldout target metrics.

With both TRIBE and textfeat analyzer JSONs ready, `scripts/e016_compare_target_controls.py` produced `outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json`. The comparator routes to `tribe_stronger_than_textfeat_needs_review`. This is a post-positive review handoff only; it does not land a final E016 verdict, clear brain-specificity, or change a ladder rung.

## Textfeat Completion

Artifacts:

- run JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json`
- analyzer JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json`
- readiness JSON: `outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.readiness.json`
- completion marker in log: `2026-07-03T11:46:44Z`

Textfeat analyzer means:

- `kd_only`: mean PPL `98.962656`; mean target R2 `0.911742`
- `textfeat_mse_lambda0.1`: mean PPL `98.524176`; mean target R2 `0.912503`
- `textfeat_perm_lambda0.1`: mean PPL `98.511881`; mean target R2 `0.910124`

Readiness route:

- `gate.science_ready=true`
- `paper_branch_hint.branch="matched_information_control_ready"`

## Comparator

Command:

```bash
uv run python scripts/e016_compare_target_controls.py --tribe-analysis outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json --textfeat-analysis outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json --out outputs/E016_tribe/phase3/phase3_full_tribe_vs_textfeat_comparison.json
```

Comparator route:

- `ready=true`
- `branch_hint.branch="tribe_stronger_than_textfeat_needs_review"`
- reason: TRIBE gains exceed text-feature gains seed-aligned, but still need `/interpret`, stats/code review, and likely extra evidence.

Lambda 0.1 comparison:

- TRIBE gain versus KD-only mean: `+0.077492`
- TRIBE gain versus permuted TRIBE mean: `+0.071871`
- textfeat gain versus KD-only mean: `+0.000761`
- textfeat gain versus permuted textfeat mean: `+0.002379`
- TRIBE-minus-textfeat gain versus KD-only mean: `+0.076731`
- TRIBE-minus-textfeat gain versus permuted-control gains: `+0.069492`

## Result Boundary

The comparator says TRIBE is stronger than the sentence-local frozen-LM hidden-state text-feature control on this synthetic-target endpoint. It does not clear long-context or on-policy distillation, dense/rich-feedback privileged-signal adjacency, or real-brain alignment. The run has only 3 seeds, so the next step is an `/interpret` audit, not a paper claim.

No final experiment verdict landed. No brain-specific clearance was granted. No ladder rung changed.

## Next

Switch to `/interpret` and audit the comparator: seed-aligned margins, PPL matching, analyzer gates, code/stat assumptions, and the post-positive evidence burden. Then choose between extra seeds, a stronger non-brain/context comparator, real-brain follow-up, or a deliberately narrowed claim.

## Related

- `../ladder.md`
- `../upspeed.md`
- `../tasks.md`
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- `../top-venue-paper-plan-2026-07-03.md`
- `../top-venue-evidence-ledger-2026-07-03.md`
