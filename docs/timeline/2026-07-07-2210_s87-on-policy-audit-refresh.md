---
title: "S87 - On-policy audit refresh"
tags: [timeline, E016, scout, top-venue]
aliases: [S87, on-policy-audit-refresh]
---

# S87 - On-policy audit refresh

**Date:** 2026-07-07

**Stance:** `/work` for live-run monitoring, with a bounded `/scout` follow-up while the GPU run continued.

## What Changed

- Rechecked the active TRIBE seed `0-2` artifact-saving rerun and watcher chain.
- Used Firecrawl Research to expand around privileged-information leakage, degradation, and transfer failure in OPD/OPSD.
- Updated [`../top-venue-on-policy-context-distillation-audit-2026-07-03.md`](../top-venue-on-policy-context-distillation-audit-2026-07-03.md) with TRACE, Many Faces of OPD, AVSD, DemoPSD, and Rethinking OPSD for Thinking Models.
- Updated [`../tasks.md`](../tasks.md) and [`../upspeed.md`](../upspeed.md) to record the new literature pressure.

## Literature Note

The closest new pressure is not an exact overlap with E016. It is a failure-mode literature around privileged teacher signals: all-token privileged self-OPD can leak instance-specific information, suppress useful exploration or deliberation, shorten reasoning, and degrade OOD transfer. Several new methods respond by routing, gating, attenuating, or aggregating privileged signals instead of fitting them everywhere.

This strengthens the active E016 gate. A synthetic endpoint gain is insufficient if the trained student does not transfer to the real-brain endpoint. If the six-seed Tuckute diagnostic remains nonpositive or mixed, the route is not just a null; it is a controlled privileged-target transfer test.

## Live State

- TRIBE seed `0-2` rerun still active: runner PID `3827110`, Python child `3827120`.
- Completed arms at verification: `4/9`.
- Active arm: `seed=1`, `arm=tribe_mse`, `lambda=0.1`.
- Missing artifacts: rerun JSON, rerun Tuckute JSON, combined Tuckute analysis JSON, combined Tuckute audit JSON.

## Boundary

This was a scout/plan pressure check only. No new science number, final E016 verdict, brain-specific clearance, or rung change exists yet.

## Related

- [`../top-venue-on-policy-context-distillation-audit-2026-07-03.md`](../top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`../top-venue-literature-refresh-2026-07-07.md`](../top-venue-literature-refresh-2026-07-07.md)
- [`../top-venue-paper-plan-2026-07-03.md`](../top-venue-paper-plan-2026-07-03.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../upspeed.md`](../upspeed.md)
