---
title: "S98 - Combined Tuckute gate ready"
tags: [timeline, work, E016, S98]
aliases: [S98, E016-combined-tuckute-gate-ready]
---

# S98 - Combined Tuckute gate ready

## Stance

`/work`

## What happened

- Checked the active E016 combined Tuckute gate after the detached monitors ran.
- The selected TRIBE seed `0-2` artifact-saving rerun completed all `9/9` arms.
- The rerun Tuckute scoring, combined seed `0-5` Tuckute analysis, and raw-row audit artifacts are present.
- `uv run scripts/e016_tuckute_gate_status.py --markdown` reported `phase="audit_ready_for_interpret"` and `ready_for_interpret=true`.

## Evidence

- Combined analysis: `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json`.
- Combined audit: `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.audit.json`.
- Audit status: `all_checks_pass=true`, complete seeds `[0,1,2,3,4,5]`, no missing expected seeds.
- Audit route: `real_brain_warning_needs_claim_scope_review`.

Key combined real-brain contrasts:

- TRIBE-minus-textfeat gain versus KD-only: mean `-0.001213`, 95% normal CI `[-0.001846, -0.000580]`, `n=6`, all seed margins negative, sign-flip `p=0.03125`.
- TRIBE-minus-textfeat gain versus permuted-control gains: mean `-0.001005`, 95% normal CI `[-0.001643, -0.000368]`, `n=6`.
- TRIBE gain versus permuted TRIBE: mean `-0.001786`, 95% normal CI `[-0.002166, -0.001407]`, `n=6`, all seed margins negative, sign-flip `p=0.03125`.

## Result status

Artifact-complete real-brain transfer diagnostic ready for `/interpret`. No final E016 verdict, no brain-specific clearance, no manuscript claim, and no ladder change.

## Related

- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../tasks.md`](../tasks.md)
- [`../upspeed.md`](../upspeed.md)
