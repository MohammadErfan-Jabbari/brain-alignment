---
title: "S80 - E016 six-seed TRIBE-vs-textfeat comparison"
tags: [timeline, interpret, E016]
aliases: [S80]
---

# S80 - E016 six-seed TRIBE-vs-textfeat comparison

**Date:** 2026-07-07
**Stance:** `/interpret`
**Scope:** After the extra seed `3,4,5` runs completed, merge original and extra E016 artifacts, rerun analyzers/readiness/comparator, independently audit the six-seed TRIBE-vs-textfeat contrast, and record the boundary.

## Summary

The extra TRIBE and textfeat seed `3,4,5` runs completed cleanly. Their run JSONs, analyzer JSONs, and readiness packets exist and are science-ready. The original seed `0,1,2` artifacts and extra seed `3,4,5` artifacts were merged into combined seed `0-5` TRIBE and textfeat run JSONs, each with 18 rows and complete arm grids.

Both combined analyzers passed the science gate. The combined comparator routed to `tribe_stronger_than_textfeat_needs_review`. The independent raw-row audit matched the comparator means and found all six seed-aligned margins positive.

This materially strengthens the narrow post-positive route. It still does not land a final E016 verdict, clear brain-specificity, or flip a rung. The endpoint is synthetic target-R2; textfeat clears only sentence-local frozen-teacher hidden-state supervision; long-context/on-policy distillation, rich-feedback privileged-signal adjacency, real-brain alignment, and downstream utility remain unresolved.

## Artifacts

- combined TRIBE run: `outputs/E016_tribe/phase3/phase3_combined_tribe_gpt2_n95999_s0-5_lam0.1.json`
- combined TRIBE analyzer: `outputs/E016_tribe/phase3/phase3_combined_tribe_gpt2_n95999_s0-5_lam0.1.analysis.json`
- combined TRIBE readiness: `outputs/E016_tribe/phase3/phase3_combined_tribe_gpt2_n95999_s0-5_lam0.1.readiness.json`
- combined textfeat run: `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.json`
- combined textfeat analyzer: `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.analysis.json`
- combined textfeat readiness: `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.readiness.json`
- combined comparator: `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.json`
- independent audit: `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_comparison.interpret_audit.json`

## Gate

Both combined analyzers:

- `science_ready=true`
- complete expected seed `0-5` x arm grid
- all paired common seeds present
- PPL matched under the `0.05` relative tolerance
- full train/heldout/target-dimension scale gates true
- heldout target metrics present

## Six-Seed Contrast

Combined analyzer means at lambda 0.1:

- TRIBE branch: KD-only PPL `99.133957`, target-R2 `0.595327`; TRIBE target PPL `98.811351`, target-R2 `0.673624`; TRIBE permuted PPL `98.803784`, target-R2 `0.598818`.
- textfeat branch: KD-only PPL `99.133957`, target-R2 `0.911687`; textfeat target PPL `98.766267`, target-R2 `0.912590`; textfeat permuted PPL `98.818684`, target-R2 `0.910313`.

Combined comparator at lambda 0.1:

- TRIBE gain versus KD-only: `+0.078298`
- TRIBE gain versus permuted TRIBE: `+0.074807`
- textfeat gain versus KD-only: `+0.000903`
- textfeat gain versus permuted textfeat: `+0.002276`
- TRIBE-minus-textfeat gain versus KD-only: `+0.077395`
- TRIBE-minus-textfeat gain versus permuted-control gains: `+0.072531`

Independent raw-row audit:

- gain versus KD-only values: `[+0.076338, +0.075906, +0.077948, +0.078325, +0.078158, +0.077694]`, all positive, sign-flip `p=0.03125`.
- gain versus permuted-control-gain values: `[+0.065526, +0.072959, +0.069991, +0.076589, +0.074926, +0.075194]`, all positive, sign-flip `p=0.03125`.
- max relative PPL delta: `0.009220`.

## Boundary

The seed-extended result supports the claim that TRIBE survives the prepared sentence-local textfeat control on the synthetic target endpoint. It does not support a brain-specific top-tier claim by itself.

The next decision is the burden choice:

- real-brain evaluation on saved seed `3-5` TRIBE/textfeat artifacts,
- stronger context/on-policy non-brain control,
- or a deliberately narrowed synthetic-target paper claim.

## Related

- [`../ladder.md`](../ladder.md)
- [`../upspeed.md`](../upspeed.md)
- [`../tasks.md`](../tasks.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`../top-venue-evidence-ledger-2026-07-03.md`](../top-venue-evidence-ledger-2026-07-03.md)
