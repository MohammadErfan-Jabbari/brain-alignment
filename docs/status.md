---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-07-16

**Manuscript:** `share-ready`

**Latest frozen public cut:** [v0.9 Markdown](manuscript/public/v0.9/paper.md)

## Research state

| Rung | State | Owning evidence | Extended-manuscript location |
|---|---|---|---|
| Q0 / A2 | CONDITIONAL PASS: alignment survives controls for UTS03; no E006 participant/population inference | [E002](experiments/E002_tuckute-encoding-feasibility.md), [E006](experiments/E006_lebel-voxelwise-feasibility.md) | Methods; Results §4.1 |
| Q1 | PARTIAL: plain KD shows alignment headroom, but KD-specific shedding is not isolated from LM quality | [E003](experiments/E003_kd-alignment-preservation.md) | Results §4.2 |
| Q2 | NO DEMONSTRATED LEVER at the valid inference unit; small effects are not ruled out | [E004](experiments/E004_brain-loss-lever-test.md) | Results §4.3 |
| Q3 | PER-INDIVIDUAL NULL across tested ROI/objective variants; E025 additionally excludes a `+0.002` participant-mean TRIBE transfer for the nine-participant Tuckute cohort despite successful target learning and model movement | [E008](experiments/E008_per-participant-f1-solidification.md), [E011](experiments/E011_strong-regime-per-individual.md), [E013](experiments/E013_open-frontier-multisubject-naturalistic.md), [E025](experiments/E025_participant-e016-biological-transfer.md) | Results §4.4; conference extension pending |
| Q4 / A3 | BOUNDED NULL for practical payoff under tested endpoints; gaze privileged-information substrate failed its preconditions | [E009](experiments/E009_a3-practical-payoff.md), [E024](experiments/E024_zuco-lupi-sample-efficiency.md) | Results §4.5; Discussion |
| Q5 | NOT STARTED and currently moot because it depends on a Q3 benefit | No active E record | Deliberately excluded |

## Active work

- The extended manuscript remains a share-ready MSc thesis baseline; supervisor circulation continues independently of any conference extension.
- E025 is complete and result-oracle clean. All language-quality, target-learning, and representation-movement gates passed, but participant-general biological transfer did not: mean `+0.000136`, CI95 `[-0.000505,+0.000777]`, one-sided UCB `+0.000653 < +0.002`. The direct TRIBE-minus-KD mean was `-0.000014`; UID 837 alone carried the apparent relative positive.
- The working conference route is now a focused methodological/falsification paper built around the separation between target fit, student movement, and biological transfer. E026 remains a retrospective diagnostic prerequisite; its first implementation review returned HOLD and is being repaired before any geometry outcome. A theory-first route remains conditional; the positive-mechanism route is closed and E027 is not licensed.
- The package strategy is recorded in [D057](decisions/decisions.md) and traces to the non-authoritative [initial Pro audit](external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md) and [corrected Pro audit](external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md).

## Conference packages

| Package | Identity | State | Next gate |
|---|---|---|---|
| A | Methodological/falsification protocol | **Strengthened default route** | Repair/execute E026; precheck E028 external Vaidya cross-modal falsification; obtain author artifacts or label a public-data reimplementation honestly |
| B | Conditional theoretical boundary | **HOLD** | Generic theorems are occupied; proceed only if an observable directional certificate prospectively predicts both failure and success regimes |
| C | Positive brain-guided mechanism | **Closed; E025 activation failed** | No E027: E025's powered participant upper bound excludes its `+0.002` activation threshold for this cohort |

## Blockers

- None for supervisor circulation. Public-version metadata remains a separate checkpoint decision.
- A top-AI-conference claim is not currently supported. It requires stronger biological scope and target identification, then either a prospective external demonstration or a genuinely new theoretical result.

## Next actions

1. Read and circulate the extended-manuscript PDF to supervisors.
2. Complete E026's HOLD repairs, obtain a fresh independent DESIGN PASS, then run the no-training target-geometry and trained-movement audits. Do not construct a candidate control or train E027.
3. Finish E028's metadata-only external falsification preregistration and author-artifact request. Run artifact/access and corrected-reanalysis gates before any high-cost external training matrix.
4. Route the settled E025 result into the extended manuscript as Package A conference-extension evidence without changing the frozen public thesis cut.
5. Keep Package B on HOLD unless the proposed observable directional certificate survives a prospective failure/success prediction test; do not market generic conditional-independence or deterministic-proxy arguments as a new theorem.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Extended manuscript](manuscript/extended/main-extended.tex)
- [D057 conference package decision](decisions/decisions.md)
