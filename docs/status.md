---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-07-23

**Manuscript:** `rewrite candidate share-ready; manuscript-sync-pending`. The new claim-led candidate in `docs/manuscript/rewrite/` is complete through E030, passes the strict share-ready checker and clean PDF build, and has received converged whole-manuscript review plus a 47-page visual audit. The extended manuscript and frozen public v0.9 cut remain unchanged by explicit instruction. E008's owning record now correctly names the participant median over seed--fold cells; the extended manuscript still describes within-person averaging, so it remains sync-pending even though no value or verdict changed.

**Latest frozen public cut:** [v0.9 Markdown](manuscript/public/v0.9/paper.md)

## Research state

| Rung | State | Owning evidence | Extended-manuscript location |
|---|---|---|---|
| Q0 / A2 | CONDITIONAL PASS: alignment survives controls for UTS03; no E006 participant/population inference | [E002](experiments/E002_tuckute-encoding-feasibility.md), [E006](experiments/E006_lebel-voxelwise-feasibility.md) | Methods; Results §4.1 |
| Q1 | PARTIAL: plain KD shows alignment headroom, but KD-specific shedding is not isolated from LM quality | [E003](experiments/E003_kd-alignment-preservation.md) | Results §4.2 |
| Q2 | NO DEMONSTRATED INTERVENTION EFFECT at the valid inference unit; small effects are not ruled out | [E004](experiments/E004_brain-loss-lever-test.md) | Results §4.3 |
| Q3 | NO DEMONSTRATED PARTICIPANT-GENERAL GAIN across tested ROI/objective variants; E025's direct TRIBE-minus-KD contrast is near zero. Its preregistered relative upper bound falls below the internal `+0.002` continuation threshold, but E026 shows that the saved cross-target comparator fails measured-axis comparability, so the relative contrast is not content-identifying. E030 localizes the first exact-substrate failure at target measurability under its fixed PCA-50 linear assay: aligned TRIBE above nuisance is `-0.004494`, with family-95% upper endpoint `+0.001707 < +0.002`; the frozen-twin contrast remains unresolved | [E008](experiments/E008_per-participant-f1-solidification.md), [E011](experiments/E011_strong-regime-per-individual.md), [E013](experiments/E013_open-frontier-multisubject-naturalistic.md), [E025](experiments/E025_participant-e016-biological-transfer.md), [E026](experiments/E026_tribe-textfeat-target-comparability.md), [E030](experiments/E030_exact-substrate-transport-diagnostic.md) | Results §4.4 and §4.6 through E030 |
| Q4 / A3 | BOUNDED NULL for practical payoff under tested endpoints; gaze privileged-information substrate failed its preconditions | [E009](experiments/E009_a3-practical-payoff.md), [E024](experiments/E024_zuco-lupi-sample-efficiency.md) | Results §4.5; Discussion |
| Q5 | NOT STARTED and currently moot because it depends on a Q3 benefit | No active E record | Deliberately excluded |

## Active work

- The new claim-led rewrite candidate is complete from abstract through Appendix F. It separates recorded and predicted targets, orders the argument by evidential gates, adds participant-level evidence and explicit estimator/training/provenance appendices, and preserves the scoped E001--E030 verdict. Four-skill structure and whole-paper review rounds converged; the senior-writer revision loop converged; the 16-source share-ready checker, clean 47-page build, and page-by-page visual inspection pass.
- The extended manuscript remains the current authority until Erfan approves a promotion or synchronization step. It was intentionally left untouched. Its scientific values and verdict remain unchanged, but its E008 within-person aggregation wording is stale relative to the corrected owning record and the rewrite candidate, so `manuscript-sync-pending` is active. The frozen public v0.9 cut also remains unchanged.
- E025 is complete and result-oracle clean. All language-quality, target-learning, and representation-movement gates passed. The direct TRIBE-minus-KD mean is `-0.000014`, CI95 `[-0.000739,+0.000711]`. The preregistered participant-first relative contrast is `+0.000136`, CI95 `[-0.000505,+0.000777]`, with one-sided UCB `+0.000653 < +0.002`; this relative estimand does not identify content after E026. UID 837 carries the sole clear participant positive in both views.
- E026 is complete and independently audited. The saved text-feature arm fails the frozen measured-axis conjunction: 30/55 checks fail, 24 pass, and one is unresolved. The principal mismatches are KD baseline/headroom, covariance spectrum/effective rank, low-level nuisance predictability, global parameter displacement, and layer-6 centered-Frobenius movement. This invalidates the raw cross-target proxy-gain difference as brain-specificity evidence without invalidating TRIBE's within-target learnability.
- E030 is complete, author-confirmed, independently recomputed, and synchronized into the extended manuscript. All `270/360/6,480` C1/C2/C3 rows, `748` independently recomputed load-bearing leaves, and the full provenance chain are panel-clean. The target is strongly extractable from TRIBE students (`M=+0.040725`, family-95% CI `[+0.039053,+0.042398]`), but its aligned unique participant predictivity above nuisances fails first. The frozen-twin contrast, incremental retention over KD, and all bridge contrasts remain unresolved. No post-outcome E030 variant is licensed.
- The working conference route remains a focused methodological/falsification paper built around source-target validity, target uptake, student movement, control identification, biological transfer, and utility. E028 is the primary external gate; a controlled reproduction of Xiao et al. 2026 is the lower-dependency feasibility backup. A theory-first route remains HOLD, and the positive-mechanism route is closed.
- The [E028 author-artifact request](references/e028-vaidya-artifact-request-email.md) was sent on 2026-07-22 to the corresponding author with both coauthors copied. The first response checkpoint is 2026-08-05; one concise follow-up is permitted, and 2026-08-12 is the exact-lane decision checkpoint. Silence means exact reproduction is unavailable, not that the reported result failed.
- E028's outcome-blind synthetic Stage-1 corrected-evaluator slice is implemented and independently panel-clean. Two 108-cell replays were byte-identical; schema, support, nuisance-sharing, pooled aggregation, exact sign-flip inversion, sentinels, and adversarial fixtures passed. The deliberately positive synthetic branch passed while `stage2_licensed=false` and `ready_for_endpoint_access=false`. This is plumbing evidence only. The production provider, RFC 8785 chain, factual dimensions, production-shape benchmark, exact lane, and endpoint-bundle review remain absent.
- The package strategy is recorded in [D057](decisions/decisions.md) and traces to the non-authoritative [initial Pro audit](external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md) and [corrected Pro audit](external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md).

## Conference packages

| Package | Identity | State | Next gate |
|---|---|---|---|
| A | Methodological/falsification protocol | **Strengthened default route; internal dissociation complete, external gate missing** | Run a 10-business-day E028 access/executable feasibility gate in parallel with a smallest-setting Xiao reproduction design; choose the external lane before expensive compute |
| B | Conditional theoretical boundary | **HOLD** | Generic theorems are occupied; proceed only if an observable directional certificate prospectively predicts both failure and success regimes |
| C | Positive brain-guided mechanism | **Closed; E025 continuation rule failed** | No E027: E025 failed the conjunctive participant-positive continuation rule, and direct TRIBE-minus-KD is near zero for this cohort |

## Blockers

- No writing or validation blocker remains for the rewrite candidate. Authority promotion, synchronization of the preserved extended manuscript, and any new public cut require Erfan's approval. Until then, the extended manuscript remains `manuscript-sync-pending` for the E008 estimator wording only; the numerical result and scientific verdict are unchanged.
- E028's exact lane remains blocked by author-controlled code, checkpoints, masks/folds, dataset facts, and result-regeneration artifacts. Its synthetic Stage-1 development slice is implemented, tested, and independently `PANEL-CLEAN`, but the production provider/chain/dimension benchmark and sealed endpoint-bundle review are absent; `ENDPOINT-READY: NO` remains unchanged.
- A top-AI-conference claim is not currently supported. It requires a non-inconclusive prospective external adjudication and a reusable intervention-audit implementation; the unchanged thesis should not consume a top-tier main-track cycle.

## Next actions

1. Erfan reviews the [claim-led rewrite PDF](manuscript/rewrite/main-rewrite.pdf) and decides whether to promote it as the thesis manuscript, request bounded revisions, or retain it as a candidate.
2. If promotion is approved, synchronize the manuscript authority deliberately and decide separately whether to create a new immutable public cut. Until that decision, do not overwrite the preserved extended manuscript.
3. Resolve E028's outcome-blind factual slots and exact-versus-reimplementation lane from the author response/public metadata; acquire no neural endpoint or author result before a production C1 lock. Build and benchmark the exact production Stage-1 provider only after its factual dimensions are hash-locked, and keep readiness false unless implementation, cost, RFC 8785 chain, and fresh endpoint-bundle review all clear.
4. Freeze the smallest-setting Xiao reproduction and matched-control feasibility design in parallel, without opening its result before its own precheck.
5. Inspect the E028 response state on 2026-08-05 and send one concise follow-up if needed. On 2026-08-12, run E028 Stage 1 only if complete hashable artifacts and final readiness exist; otherwise close the exact lane as unavailable and move the main allocation to Xiao. Full E028 Stages 2/3 remain forbidden unless corrected Stage 1 passes.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Extended manuscript](manuscript/extended/main-extended.tex)
- [Claim-led rewrite candidate](manuscript/rewrite/main-rewrite.tex)
- [D057 conference package decision](decisions/decisions.md)
