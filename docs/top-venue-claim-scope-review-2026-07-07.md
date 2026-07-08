---
title: "Top-venue claim-scope review, 2026-07-07"
tags: [plan, E016, top-venue]
aliases: [top-venue-claim-scope-review-2026-07-07, E016-claim-scope-review]
---

# Top-venue claim-scope review, 2026-07-07

**Status.** This is a `/plan` artifact after the E016 saved-student Tuckute diagnostic. It chose the bounded real-brain robustness rerun; the 2026-07-08 `/interpret` closeout below records how that rerun resolved. It is not a report, not a manuscript section, and not a ladder update.

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

## Resolution After Rerun

The bounded robustness path completed on 2026-07-08 and is interpreted in [`e016-combined-tuckute-interpretation-2026-07-08.md`](e016-combined-tuckute-interpretation-2026-07-08.md). The combined seed `0-5` Tuckute audit passed with complete seeds `[0,1,2,3,4,5]`, no missing expected seeds, and route `real_brain_warning_needs_claim_scope_review`.

The kill criteria fired for the brain-specific positive route: TRIBE-minus-textfeat real-brain gain versus KD-only is mean `-0.001213`, CI `[-0.001846, -0.000580]`, `n=6`, with all six margins negative; TRIBE-minus-textfeat gain versus permuted-control gains is mean `-0.001005`, CI `[-0.001643, -0.000368]`. The paper route now narrows to a synthetic-target/control plus real-brain transfer-failure package.

**Resolved order:** the missing TRIBE seed `0-2` real-brain diagnostic is closed; the narrow synthetic/control route is selected for this goal; `contextfeat` and on-policy controls are not next by default.

## Related

- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md)
- [`e016-combined-tuckute-interpretation-2026-07-08.md`](e016-combined-tuckute-interpretation-2026-07-08.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md)
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
