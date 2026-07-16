---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-07-17

**Manuscript:** `manuscript-sync-pending` — E025/E026 conference-extension framing is integrated, independently reviewed, and revised; author approval is required before restoring `share-ready`

**Latest frozen public cut:** [v0.9 Markdown](manuscript/public/v0.9/paper.md)

## Research state

| Rung | State | Owning evidence | Extended-manuscript location |
|---|---|---|---|
| Q0 / A2 | CONDITIONAL PASS: alignment survives controls for UTS03; no E006 participant/population inference | [E002](experiments/E002_tuckute-encoding-feasibility.md), [E006](experiments/E006_lebel-voxelwise-feasibility.md) | Methods; Results §4.1 |
| Q1 | PARTIAL: plain KD shows alignment headroom, but KD-specific shedding is not isolated from LM quality | [E003](experiments/E003_kd-alignment-preservation.md) | Results §4.2 |
| Q2 | NO DEMONSTRATED LEVER at the valid inference unit; small effects are not ruled out | [E004](experiments/E004_brain-loss-lever-test.md) | Results §4.3 |
| Q3 | NO PREDECLARED-MEANINGFUL PARTICIPANT-GENERAL GAIN across tested ROI/objective variants; E025's primary TRIBE-minus-textfeat upper bound excludes `+0.002` for the nine-participant Tuckute cohort, while direct TRIBE-minus-KD is near zero; E026 shows that the saved cross-target comparator fails measured-axis comparability | [E008](experiments/E008_per-participant-f1-solidification.md), [E011](experiments/E011_strong-regime-per-individual.md), [E013](experiments/E013_open-frontier-multisubject-naturalistic.md), [E025](experiments/E025_participant-e016-biological-transfer.md), [E026](experiments/E026_tribe-textfeat-target-comparability.md) | Results §4.4 and §4.6; extension integrated, approval pending |
| Q4 / A3 | BOUNDED NULL for practical payoff under tested endpoints; gaze privileged-information substrate failed its preconditions | [E009](experiments/E009_a3-practical-payoff.md), [E024](experiments/E024_zuco-lupi-sample-efficiency.md) | Results §4.5; Discussion |
| Q5 | NOT STARTED and currently moot because it depends on a Q3 benefit | No active E record | Deliberately excluded |

## Active work

- The frozen public thesis cut remains available for supervisor circulation. The live extended manuscript now includes independently reviewed E025/E026 framing and is intentionally not marked share-ready until it receives author approval.
- E025 is complete and result-oracle clean. All language-quality, target-learning, and representation-movement gates passed. Its primary participant-first TRIBE-minus-textfeat activation contrast is `+0.000136`, CI95 `[-0.000505,+0.000777]`, with one-sided UCB `+0.000653 < +0.002`; this relative estimand does not identify content after E026. The direct TRIBE-minus-KD mean is `-0.000014`, CI95 `[-0.000739,+0.000711]`; UID 837 carries the sole clear participant positive in both views.
- E026 is complete and independently audited. The saved text-feature arm fails the frozen measured-axis conjunction: 30/55 checks fail, 24 pass, and one is unresolved. The principal mismatches are KD baseline/headroom, covariance spectrum/effective rank, low-level nuisance predictability, global parameter displacement, and layer-6 centered-Frobenius movement. This invalidates the raw cross-target proxy-gain difference as brain-specificity evidence without invalidating TRIBE's within-target learnability.
- The working conference route is a focused methodological/falsification paper built around the separation among target fit, student movement, control identification, and biological transfer. A theory-first route remains HOLD because the generic theorem is occupied and no prospective directional certificate exists; the positive-mechanism route is closed and E027 is not licensed.
- The package strategy is recorded in [D057](decisions/decisions.md) and traces to the non-authoritative [initial Pro audit](external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md) and [corrected Pro audit](external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md).

## Conference packages

| Package | Identity | State | Next gate |
|---|---|---|---|
| A | Methodological/falsification protocol | **Strengthened default route; internal dissociation complete** | Complete E028's executable and artifact gates, reproduce the external positive faithfully, then apply the frozen participant-level and matched-control falsification |
| B | Conditional theoretical boundary | **HOLD** | Generic theorems are occupied; proceed only if an observable directional certificate prospectively predicts both failure and success regimes |
| C | Positive brain-guided mechanism | **Closed; E025 activation failed** | No E027: E025's primary relative upper bound excludes its `+0.002` activation threshold, and direct TRIBE-minus-KD is near zero for this cohort |

## Blockers

- None for supervisor circulation. Public-version metadata remains a separate checkpoint decision.
- A top-AI-conference claim is not currently supported. It requires stronger biological scope and target identification, then either a prospective external demonstration or a genuinely new theoretical result.

## Next actions

1. Obtain author approval for the independently reviewed E025/E026 manuscript framing; do not alter the frozen public thesis cut.
2. Predeclare an exact-substrate transport diagnostic: participant-first Tuckute predictivity of text-only TRIBE above the existing nuisance baseline, and retained TRIBE-target predictivity of the saved students on the same 1,000 sentences.
3. Complete E028's executable runner/analyzer/config hashes, dimension-scale synthetic benchmark, author-artifact access, and final anti-confound/oracle gates. Send the prepared author email only with explicit approval.
4. If E028 passes access and reproduction, run its corrected patient-level reanalysis before any expensive training matrix; the reproduced positive must survive before matched phase/audio controls activate.
5. Keep Package B on HOLD unless the observable directional certificate prospectively distinguishes positive, null, and harmful regimes; do not market the generic target-only insufficiency result as a new theorem.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Extended manuscript](manuscript/extended/main-extended.tex)
- [D057 conference package decision](decisions/decisions.md)
