---
title: "Top-venue representation-control feasibility, 2026-07-07"
tags: [plan, reference, E016, controls]
aliases: [top-venue-representation-control-feasibility-2026-07-07, representation-control-feasibility]
---

# Top-venue representation-control feasibility, 2026-07-07

**Status.** This is a `/plan` artifact written while the E016 seed `0-2` TRIBE artifact-saving rerun is active. It is not a report, not a manuscript section, not a science verdict, and not permission to launch a new control before the combined Tuckute gate resolves.

## Question

The hidden-state distillation literature has moved: OPRD and PHF make representation-space and hidden-process distillation active non-brain baseline families. If E016's real-brain transfer gate becomes positive, what is the smallest next control that makes the paper stronger without changing the estimand so much that it stops answering the brain-derived target question?

## Bottom Line

Do not build an OPRD/PHF-style control as the immediate next step. If the combined seed `0-5` Tuckute gate is nonpositive or mixed, no new representation-control compute is justified; the paper route narrows to a controlled privileged-target transfer-failure result. If the gate is positive and audit-clean, the next non-brain control should be `contextfeat` first, because it is already mechanically feasible in the current cache-based Phase-3 runner and tests a cleaner nearby objection: whether a context-conditioned frozen teacher hidden target explains the TRIBE gain.

An OPRD/PHF-style comparator is a later, higher-cost burden. It requires a new on-policy runner because the supervision target is teacher hidden states or hidden transitions on student rollouts, not a precomputed per-sentence target cache. It should be opened only if all of these hold:

1. combined Tuckute seed `0-5` is positive and audit-clean,
2. the claim remains brain-specific after `textfeat` and real-brain transfer,
3. `contextfeat` does not explain the effect, or the intended venue claim explicitly compares against on-policy representation distillation.

## Control Options

| Option | What it tests | Fits current runner? | Cost | When to use |
|---|---|---:|---:|---|
| `textfeat` | Sentence-local frozen LM hidden-state targets, matched dimension and permuted twin. | Yes, already complete. | Paid. | Already mandatory; clears only sentence-local teacher-hidden features. |
| `contextfeat` | Frozen teacher hidden states conditioned on recovered preceding WikiText context, pooled over target sentence tokens. | Yes; cache builder exists and CPU-smoked. | Medium: build train/heldout caches, run Phase-3 arms. | First extra non-brain control if E016 real-brain gate is positive. |
| OPRD-lite | Teacher hidden-state MSE on student-generated/on-policy text. | No; needs new runner. | High: rollout generation, teacher/student hidden capture, layer/position policy, analyzer. | Only after positive real-brain gate plus `contextfeat` need, or if top-tier reviewers require an on-policy representation baseline. |
| PHF-lite | Teacher hidden-transition/trajectory-geometry matching on student rollouts. | No; needs new runner and transition-window design. | Very high: all OPRD-lite burdens plus transition/geometry choices. | Not a near-term E016 control; consider only for a new paper branch or a strong positive that survives simpler controls. |

## Why `contextfeat` First

`contextfeat` changes one thing relative to `textfeat`: it gives the non-brain teacher more stimulus context while keeping the Phase-3 estimand fixed. The student still trains under the same fixed KD budget, target dimension, block-permuted twin, heldout target-R2 machinery, and saved-student real-brain evaluation path.

OPRD/PHF change several things at once: they move from off-policy sentence targets to student rollouts, from fixed cache targets to dynamic teacher forwards, and from sentence-level target fitting to token/trajectory-level hidden supervision. That is a different baseline family, not a drop-in stronger `textfeat`.

## Predeclared Decision Rule

After the combined Tuckute gate:

- **Nonpositive or mixed:** do not build `contextfeat`, OPRD-lite, or PHF-lite. Write the paper route as a controlled transfer-failure / evaluation-ladder result if `/interpret` supports it.
- **Positive but audit or code review fails:** fix the gate first; no new controls.
- **Positive and audit-clean, but effect is fragile across seeds/PCA/protocol checks:** prioritize independent code/stat review or replication over new baselines.
- **Positive and robust:** build `contextfeat` before any on-policy hidden-state runner.
- **Positive, robust, and `contextfeat` cannot explain it:** design OPRD-lite as a separate `/precheck` item; PHF-lite remains optional and should need a venue-driven reason.

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
