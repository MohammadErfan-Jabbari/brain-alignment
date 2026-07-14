---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-07-14

**Manuscript:** `share-ready`

**Latest frozen public cut:** [v0.9 Markdown](manuscript/public/v0.9/paper.md)

## Research state

| Rung | State | Owning evidence | Extended-manuscript location |
|---|---|---|---|
| Q0 / A2 | CONDITIONAL PASS: alignment survives controls for UTS03; no E006 participant/population inference | [E002](experiments/E002_tuckute-encoding-feasibility.md), [E006](experiments/E006_lebel-voxelwise-feasibility.md) | Methods; Results §4.1 |
| Q1 | PARTIAL: plain KD shows alignment headroom, but KD-specific shedding is not isolated from LM quality | [E003](experiments/E003_kd-alignment-preservation.md) | Results §4.2 |
| Q2 | NO DEMONSTRATED LEVER at the valid inference unit; small effects are not ruled out | [E004](experiments/E004_brain-loss-lever-test.md) | Results §4.3 |
| Q3 | PER-INDIVIDUAL NULL across tested ROI capacity/objective variants; averaged-target gain changed estimand; voxelwise route separately failed to create a lever | [E008](experiments/E008_per-participant-f1-solidification.md), [E011](experiments/E011_strong-regime-per-individual.md), [E013](experiments/E013_open-frontier-multisubject-naturalistic.md) | Results §4.4 |
| Q4 / A3 | BOUNDED NULL for practical payoff under tested endpoints; gaze privileged-information substrate failed its preconditions | [E009](experiments/E009_a3-practical-payoff.md), [E024](experiments/E024_zuco-lupi-sample-efficiency.md) | Results §4.5; Discussion |
| Q5 | NOT STARTED and currently moot because it depends on a Q3 benefit | No active E record | Deliberately excluded |

## Active work

- The extended manuscript remains a share-ready MSc thesis baseline; supervisor circulation continues independently of any conference extension.
- Conference-extension work has resumed. The working route is a focused methodological/falsification paper built around the intervention-to-biological-transfer boundary. A theory-first route remains conditional on deriving a nontrivial finite-sample result; the tested positive-mechanism route remains closed.
- Two external ChatGPT Pro audits are retained as non-authoritative provenance in [`external-reviews/chatgpt-pro/`](external-reviews/chatgpt-pro/). Their proposals do not change a scientific verdict until they pass the repository evidence transaction.

## Blockers

- None for supervisor circulation. Public-version metadata remains a separate checkpoint decision.
- A top-AI-conference claim is not currently supported. It requires stronger biological scope and target identification, then either a prospective external demonstration or a genuinely new theoretical result.

## Next actions

1. Read and circulate the extended-manuscript PDF to supervisors.
2. In `/work`, precheck and lock E025: extend the saved-student evaluator without retraining, exclude incomplete UID 853 as in E008, score the nine complete participants for all six seeds, use layer 7 as primary and layer 6 as a mechanistic sensitivity, and retain participant and fold inference without flattening participant-by-seed cells.
3. In `/work`, precheck and lock E026: run a no-training TRIBE-versus-text-feature target-comparability audit focused on effective rank and spectrum, scale, baseline/head learnability, loss and gradient scale if retained, and representation movement.
4. Use the E025/E026 gates to choose exactly one branch: train one geometry- and learnability-matched non-brain control if the comparison is identifiable, otherwise close the E016 positive branch without another local sweep.
5. Finish the novelty synthesis from the canonical full-text notes, then choose the conference package: Package A by default, Package B only with a nontrivial theorem, and no high-cost biological or faithful-reproduction study until the cheap gates justify it.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Extended manuscript](manuscript/extended/main-extended.tex)
- [Decisions](decisions/decisions.md)
