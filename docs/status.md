---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-07-22

**Manuscript:** `share-ready through E030`; the extended manuscript carries the author-confirmed scoped E030 framing and has passed the strict checker, PDF rebuild, and fresh independent review. The frozen public v0.9 cut remains unchanged.

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

- The extended manuscript is share-ready through E030 after author confirmation, the 12-source manuscript checker, a successful Tectonic PDF rebuild, and a fresh independent scientific-scope review. It reports every E030 primary diagnostic and its inference unit. The frozen public v0.9 cut remains unchanged.
- E025 is complete and result-oracle clean. All language-quality, target-learning, and representation-movement gates passed. The direct TRIBE-minus-KD mean is `-0.000014`, CI95 `[-0.000739,+0.000711]`. The preregistered participant-first relative contrast is `+0.000136`, CI95 `[-0.000505,+0.000777]`, with one-sided UCB `+0.000653 < +0.002`; this relative estimand does not identify content after E026. UID 837 carries the sole clear participant positive in both views.
- E026 is complete and independently audited. The saved text-feature arm fails the frozen measured-axis conjunction: 30/55 checks fail, 24 pass, and one is unresolved. The principal mismatches are KD baseline/headroom, covariance spectrum/effective rank, low-level nuisance predictability, global parameter displacement, and layer-6 centered-Frobenius movement. This invalidates the raw cross-target proxy-gain difference as brain-specificity evidence without invalidating TRIBE's within-target learnability.
- E030 is complete, author-confirmed, independently recomputed, and synchronized into the extended manuscript. All `270/360/6,480` C1/C2/C3 rows, `748` independently recomputed load-bearing leaves, and the full provenance chain are panel-clean. The target is strongly extractable from TRIBE students (`M=+0.040725`, family-95% CI `[+0.039053,+0.042398]`), but its aligned unique participant predictivity above nuisances fails first. The frozen-twin contrast, incremental retention over KD, and all bridge contrasts remain unresolved. No post-outcome E030 variant is licensed.
- The working conference route remains a focused methodological/falsification paper built around source-target validity, target uptake, student movement, control identification, biological transfer, and utility. E028 is the primary external gate; a controlled reproduction of Xiao et al. 2026 is the lower-dependency feasibility backup. A theory-first route remains HOLD, and the positive-mechanism route is closed.
- The [E028 author-artifact request](references/e028-vaidya-artifact-request-email.md) was sent on 2026-07-22 to the corresponding author with both coauthors copied. The first response checkpoint is 2026-08-05; one concise follow-up is permitted, and 2026-08-12 is the exact-lane decision checkpoint. Silence means exact reproduction is unavailable, not that the reported result failed.
- The package strategy is recorded in [D057](decisions/decisions.md) and traces to the non-authoritative [initial Pro audit](external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md) and [corrected Pro audit](external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md).

## Conference packages

| Package | Identity | State | Next gate |
|---|---|---|---|
| A | Methodological/falsification protocol | **Strengthened default route; internal dissociation complete, external gate missing** | Run a 10-business-day E028 access/executable feasibility gate in parallel with a smallest-setting Xiao reproduction design; choose the external lane before expensive compute |
| B | Conditional theoretical boundary | **HOLD** | Generic theorems are occupied; proceed only if an observable directional certificate prospectively predicts both failure and success regimes |
| C | Positive brain-guided mechanism | **Closed; E025 continuation rule failed** | No E027: E025 failed the conjunctive participant-positive continuation rule, and direct TRIBE-minus-KD is near zero for this cohort |

## Blockers

- None for circulation of the E030-synchronized thesis. Public-version metadata remains a separate checkpoint decision.
- E028's exact lane remains blocked by author-controlled code, checkpoints, masks/folds, dataset facts, and result-regeneration artifacts. Outcome-blind review also found four local protocol-definition blockers that must be repaired and prechecked before the synthetic Stage-1 slice can honestly claim executable scope.
- A top-AI-conference claim is not currently supported. It requires a non-inconclusive prospective external adjudication and a reusable intervention-audit implementation; the unchanged thesis should not consume a top-tier main-track cycle.

## Next actions

1. Circulate the E030-synchronized extended-manuscript PDF now as publication insurance. Do not create a new public cut without explicit request.
2. Resolve E028's four outcome-blind protocol-definition blockers, then pass anti-confound and oracle precheck before implementing only the fail-closed synthetic Stage-1 corrected-evaluator slice. Open no neural endpoint or author result.
3. Benchmark the exact Stage-1 evaluator bottleneck at production shape and keep readiness false unless the implementation, cost, hash chain, and author facts all clear their frozen gates.
4. Freeze the smallest-setting Xiao reproduction and matched-control feasibility design in parallel, without opening its result before its own precheck.
5. Inspect the E028 response state on 2026-08-05 and send one concise follow-up if needed. On 2026-08-12, run E028 Stage 1 only if complete hashable artifacts and final readiness exist; otherwise close the exact lane as unavailable and move the main allocation to Xiao. Full E028 Stages 2/3 remain forbidden unless corrected Stage 1 passes.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Extended manuscript](manuscript/extended/main-extended.tex)
- [D057 conference package decision](decisions/decisions.md)
