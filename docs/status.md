---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-07-13  
**Manuscript:** `manuscript-sync-pending`
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

- Reconstruct the extended manuscript as a standalone MSc thesis with complete experiment coverage and a ground-up conceptual introduction.

## Blockers

- Four theory statements require `/interpret` before expansion: the unique-$R^2$/conditional-MI relationship, the MI-generalization-bound direction, the data-processing chain, and the rate--distortion framing.
- The current manuscript omits completed secondary experiments and must not be circulated until the coverage and review gates pass again.

## Next actions

1. Reconcile theory, E-record statuses, and newly load-bearing artifact provenance.
2. Rebuild the Introduction and Methods from the concrete measurement setup upward.
3. Integrate all implemented experiments into the main causal spine or complete appendices.
4. Run deterministic, persona, and independent scientific-scope reviews.
5. Obtain Erfan's framing approval, then restore `share-ready`.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Extended manuscript](manuscript/extended/main-extended.tex)
- [Decisions](decisions/decisions.md)
