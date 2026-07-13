---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-07-13  
**Manuscript:** `manuscript-sync-pending`  
**Latest frozen public cut:** v0.9 Markdown artifact; migration to `manuscript/public/v0.9/` is pending in this cutover.

## Research state

| Rung | State | Owning evidence | Extended-manuscript location |
|---|---|---|---|
| Q0 / A2 | CONDITIONAL PASS: alignment survives controls for UTS03; no E006 participant/population inference | [E002](experiments/E002_tuckute-encoding-feasibility.md), [E006](experiments/E006_lebel-voxelwise-feasibility.md) | Methods; Results §4.1, correction pending |
| Q1 | PARTIAL: plain KD shows alignment headroom, but KD-specific shedding is not isolated from LM quality | [E003](experiments/E003_kd-alignment-preservation.md) | Results §4.2 |
| Q2 | NO DEMONSTRATED LEVER at the valid inference unit; small effects are not ruled out | [E004](experiments/E004_brain-loss-lever-test.md) | Results §4.3, pending synchronization |
| Q3 | ROBUST NULL for per-individual gain across tested capacity, objective, and substrate; averaged-target gain was an artifact | [E008](experiments/E008_per-participant-f1-solidification.md), [E011](experiments/E011_strong-regime-per-individual.md), [E013](experiments/E013_open-frontier-multisubject-naturalistic.md) | Results, pending synchronization |
| Q4 / A3 | BOUNDED NULL for practical payoff under tested endpoints; gaze privileged-information substrate also failed its precondition | [E009](experiments/E009_a3-practical-payoff.md), [E024](experiments/E024_zuco-lupi-sample-efficiency.md) | Results/Discussion, pending synchronization |
| Q5 | NOT STARTED and currently moot because it depends on a Q3 benefit | No active E record | Deliberately excluded |

## Active work

- Complete the source-of-truth cutover without launching experiments or creating replacement apparatus.
- Bring settled Q2–Q4 and the scoped E016 result into the extended manuscript.

## Blockers

- E006 is resolved: retain the UTS03 point result and 5/5 fold-block sensitivity; remove invalid voxel-bootstrap intervals, “powered” language, and the E007 MDE claim from the manuscript.
- E016 is on HOLD for manuscript wording: the transfer-failure arithmetic is verified, but the block-permuted control and dimension-matched text control must not be over-described.
- The extended manuscript still contains report-era dependencies and incomplete Q2–Q4/E016 sections.

## Next actions

1. Synchronize the E006 correction and Q2 directly into the extended manuscript.
2. Integrate Q3 and Q4 directly into the extended manuscript.
3. Integrate E016 with the independently verified narrow synthetic-endpoint and real-brain transfer-failure scope.
4. Remove migrated reports, boards, stale plans, routine timelines, and retired tooling; repair links.
5. Run provenance, number, citation, link, and LaTeX checks plus one fresh manuscript review; set `share-ready` only after Erfan approves the load-bearing framing.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Extended manuscript](manuscript/extended/main-extended.tex)
- [Experiment records](experiments/AGENTS.md)
- [Decisions](decisions/decisions.md)
