---
title: "Top-venue representation-control feasibility, 2026-07-07"
tags: [plan, reference, E016, controls]
aliases: [top-venue-representation-control-feasibility-2026-07-07, representation-control-feasibility]
---

# Top-venue representation-control feasibility, 2026-07-07

**Status.** This is a `/plan` artifact originally written while the E016 seed `0-2` TRIBE artifact-saving rerun was active, then updated after the combined Tuckute gate resolved as warning/nonpositive on 2026-07-08. It is not a report, not a manuscript section, not a science verdict, and not permission to launch a new control.

## Question

The hidden-state distillation literature has moved: OPRD and PHF make representation-space and hidden-process distillation active non-brain baseline families. If E016's real-brain transfer gate becomes positive, what is the smallest next control that makes the paper stronger without changing the estimand so much that it stops answering the brain-derived target question?

## Bottom Line

Do not build `contextfeat`, OPRD-lite, or PHF-lite as the immediate next step. The combined seed `0-5` Tuckute gate is warning/nonpositive after `/interpret`, so no new representation-control compute is justified by this goal. The paper route narrows to a controlled privileged-target transfer-failure result.

An OPRD/PHF-style comparator remains a later, higher-cost burden. It requires a new on-policy runner because the supervision target is teacher hidden states or hidden transitions on student rollouts, not a precomputed per-sentence target cache. It should be opened only if all of these hold in a future goal:

1. a new predeclared endpoint/dataset or corrected evaluator reopens a positive real-brain transfer route,
2. the claim remains brain-specific after `textfeat` and real-brain transfer,
3. `contextfeat` does not explain the effect, or the intended venue claim explicitly compares against on-policy representation distillation.

## Control Options

| Option | What it tests | Fits current runner? | Cost | When to use |
|---|---|---:|---:|---|
| `textfeat` | Sentence-local frozen LM hidden-state targets, matched dimension and permuted twin. | Yes, already complete. | Paid. | Already mandatory; clears only sentence-local teacher-hidden features. |
| `contextfeat` | Frozen teacher hidden states conditioned on recovered preceding WikiText context, pooled over target sentence tokens. | Yes; cache builder exists and CPU-smoked. | Medium: build train/heldout caches, run Phase-3 arms. | Not next after the warning-route Tuckute gate; first extra non-brain control only if a future positive route reopens. |
| OPRD-lite | Teacher hidden-state MSE on student-generated/on-policy text. | No; needs new runner. | High: rollout generation, teacher/student hidden capture, layer/position policy, analyzer. | Only after positive real-brain gate plus `contextfeat` need, or if top-tier reviewers require an on-policy representation baseline. |
| PHF-lite | Teacher hidden-transition/trajectory-geometry matching on student rollouts. | No; needs new runner and transition-window design. | Very high: all OPRD-lite burdens plus transition/geometry choices. | Not a near-term E016 control; consider only for a new paper branch or a strong positive that survives simpler controls. |

## Why `contextfeat` First

`contextfeat` changes one thing relative to `textfeat`: it gives the non-brain teacher more stimulus context while keeping the Phase-3 estimand fixed. The student still trains under the same fixed KD budget, target dimension, block-permuted twin, heldout target-R2 machinery, and saved-student real-brain evaluation path.

OPRD/PHF change several things at once: they move from off-policy sentence targets to student rollouts, from fixed cache targets to dynamic teacher forwards, and from sentence-level target fitting to token/trajectory-level hidden supervision. That is a different baseline family, not a drop-in stronger `textfeat`.

## Follow-Up Pressure, 2026-07-07 22:47 UTC

A focused Firecrawl Research expansion from OPRD/PHF and PI-leakage papers added AR-OPD, EDGE-OPD, and When Context Returns as sharper positive-branch objections. Their shared lesson is that privileged supervision can fail because the privileged teacher sees information the student cannot locally support, because useful signal is localized to a subset of tokens, or because internalized context is not robust when the context is reintroduced.

This does not move OPRD-lite, PHF-lite, AR-OPD-style anchoring, or EDGE-style evidence masking ahead of the current paper planning step. Those methods are token/rollout objectives, while E016 is a fixed cache-target experiment. They become relevant only after:

1. a future positive real-brain route is positive and audit-clean,
2. independent review rules out evaluator/stat artifacts,
3. `contextfeat` fails to explain the effect, or the chosen venue requires an on-policy representation/privileged-teacher comparator.

## Predeclared Decision Rule

After the combined Tuckute gate:

- **Nonpositive or mixed:** do not build `contextfeat`, OPRD-lite, or PHF-lite. Write the paper route as a controlled transfer-failure / evaluation-ladder result if `/interpret` supports it.
- **Positive but audit or code review fails:** fix the gate first; no new controls.
- **Positive and audit-clean, but effect is fragile across seeds/PCA/protocol checks:** prioritize independent code/stat review or replication over new baselines.
- **Positive and robust:** build `contextfeat` before any on-policy hidden-state runner.
- **Positive, robust, and `contextfeat` cannot explain it:** design OPRD-lite as a separate `/precheck` item; PHF-lite remains optional and should need a venue-driven reason.

The observed 2026-07-08 branch is the first row: warning/nonpositive. No representation-control compute is the default next step.

## OPRD-Lite Sketch If It Becomes Necessary

The cleanest OPRD-lite estimand would be:

> Under the same prompts and student budget, does on-policy hidden-state supervision from a non-brain teacher explain the same real-brain transfer effect as the brain-derived target?

Minimum design burden:

- sample fixed student rollouts from the current student or KD-only checkpoint under a locked decoding policy,
- run a frozen `gpt2-medium` or matched teacher on the same rollout prefixes,
- supervise selected student layers/positions with normalized hidden-state MSE,
- include a permuted or mismatched-rollout hidden target control,
- keep perplexity and Tuckute evaluation gates identical to E016,
- require at least 3 seeds before any interpretation.

This is not a target-cache variant. It is a new training protocol and should go through `/precheck`.

## Related

- [`top-venue-literature-refresh-2026-07-07.md`](top-venue-literature-refresh-2026-07-07.md)
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md)
- [`e016-combined-tuckute-interpretation-2026-07-08.md`](e016-combined-tuckute-interpretation-2026-07-08.md)
