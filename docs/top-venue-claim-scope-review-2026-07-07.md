---
title: "Top-venue claim-scope review, 2026-07-07"
tags: [plan, E016, top-venue]
aliases: [top-venue-claim-scope-review-2026-07-07, E016-claim-scope-review]
---

# Top-venue claim-scope review, 2026-07-07

**Status.** This is a `/plan` artifact after the E016 saved-student Tuckute diagnostic. It chooses the next evidence burden. It is not a report, not a manuscript section, and not a science verdict.

## Current fork

The synthetic target endpoint and real-brain endpoint now disagree:

- Synthetic target-R2: combined seed `0-5` TRIBE beats sentence-local textfeat. TRIBE-minus-textfeat gain is `+0.077395` versus KD-only and `+0.072531` versus permuted-control gains, all six seed margins positive.
- Real-brain Tuckute diagnostic: saved seed `3-5` TRIBE does not beat KD, permuted TRIBE, or textfeat. TRIBE-minus-textfeat gain is `-0.000862` versus KD-only and `-0.000784` versus permuted-control gains.

This makes a direct brain-specific positive claim unsafe. The remaining paper routes are:

| Route | What it would claim | Why not choose it immediately |
|---|---|---|
| Narrow synthetic-target/control paper | TRIBE-like synthetic neural targets can move a KD student on the synthetic target endpoint beyond a sentence-local text-feature target, but the effect does not automatically transfer to real-brain alignment. | Plausible, but we should first close the only obvious diagnostic hole: real-brain scoring currently covers TRIBE seeds `3-5`, not `0-5`. |
| Real-brain robustness/rerun | Re-score the real-brain endpoint after saving the missing TRIBE seed `0-2` students. | This is the smallest evidence step that can fairly overturn or confirm the Tuckute warning. |
| Contextfeat/on-policy control | Test stronger non-brain context or on-policy teacher supervision. | Not next. These controls address non-brain privilege confounds on the synthetic target branch; they do not answer whether the trained students transfer to real brain. |

## Decision

Run the bounded real-brain robustness/rerun path before narrowing the paper.

The run is deliberately limited:

1. Rerun only TRIBE seeds `0,1,2` with `--save-model-dir`, using the same Phase-3 target cache, heldout target cache, model pair, seed set, lambda, epoch count, learning rate, batch size, and heldout limit as the original TRIBE run.
2. Do not rerun textfeat training: textfeat seeds `0-5` already have saved artifacts.
3. After the rerun completes, score TRIBE seed `0-2` and textfeat seed `0-5` on Tuckute, then combine with the existing TRIBE seed `3-5` diagnostic.
4. Judge the six-seed real-brain diagnostic with seed-aligned TRIBE-minus-textfeat gains versus KD-only and versus permuted-control gains.

## Kill Criteria

The brain-specific positive route stays on HOLD unless the six-seed real-brain diagnostic reverses the warning.

- If six-seed TRIBE-minus-textfeat real-brain gain versus KD-only is nonpositive, mixed without a convincing positive seed pattern, or smaller than the current diagnostic uncertainty, narrow the paper to a synthetic-target/control contribution.
- If six-seed TRIBE-minus-textfeat real-brain gain versus permuted-control gains is nonpositive, narrow the paper.
- If the rerun fails readiness, PPL matching, artifact saving, or row identity checks, do not use it for a claim.
- If the six-seed diagnostic turns positive, it still only reopens the positive route. It does not establish a final claim without independent code/stat review and a clean `/interpret` verdict.

## Why This Beats Contextfeat Now

The contextfeat control is mechanically feasible and still relevant if the paper claims that TRIBE is specifically better than text-derived privileged targets. But the current blocking fact is different: saved TRIBE students did not improve real-brain Tuckute alignment. A stronger non-brain synthetic control cannot repair a negative real-brain transfer diagnostic.

So the order is:

1. close the missing TRIBE seed `0-2` real-brain diagnostic,
2. then choose narrow synthetic/control paper versus reopened positive route,
3. only then decide whether contextfeat/on-policy controls are worth compute.

## Related

- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md)
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
