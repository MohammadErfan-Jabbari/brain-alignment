---
title: "E016 combined Tuckute interpretation, 2026-07-08"
tags: [interpret, E016, top-venue]
aliases: [E016-combined-Tuckute-interpretation, real-brain-transfer-interpretation]
---

# E016 combined Tuckute interpretation, 2026-07-08

**Status.** This is the `/interpret` closeout for the E016 combined seed `0-5` Tuckute gate. It adjudicates already-recorded artifacts; it is not a new experiment, not a report, not a manuscript section, and not a ladder rung flip.

## Claim-Intent Manifest

**Claim.** E016 supports a synthetic-target/control plus real-brain transfer-failure paper route: the TRIBE synthetic target beats the sentence-local text-feature control on the synthetic endpoint, but the saved-student real-brain Tuckute gate does not support a brain-specific positive KD claim.

**Evidence.** The synthetic endpoint evidence is the combined seed `0-5` TRIBE-vs-textfeat audit recorded in [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md) Step 54 and the real-brain transfer gate is `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json` plus `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.audit.json`.

**Overturn-if.** The claim would fail if the row-level recompute showed complete seed `0-5` TRIBE-minus-textfeat real-brain gains positive versus KD-only and versus permuted-control gains, or if the audit failed row identity, protocol identity, artifact, arithmetic, or readiness checks.

## SCR Prediction And Recompute

**Prediction before recompute.** The expected route was the warning route: the synthetic target-R2 result should remain a separate positive, while the real-brain Tuckute transfer contrast should stay nonpositive after seed-aligned comparison with textfeat.

**Independent recompute.** A local `/interpret` recompute rebuilt the paired contrasts from the raw alignment JSON rows, not from the analysis summary, and wrote `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.interpret_recompute.json`. It found complete seeds `[0,1,2,3,4,5]`, no missing seed-arm cells, no duplicate scored seed-arm cells, and exact agreement with the recorded analysis/audit summaries for the primary contrasts.

**Audit readback.** The official audit reports `all_checks_pass=true`, complete seeds `[0,1,2,3,4,5]`, no missing expected seeds, and route `real_brain_warning_needs_claim_scope_review`.

## Load-Bearing Contrasts

| Contrast | Mean | 95% normal CI | Seed pattern | Interpretation |
|---|---:|---:|---|---|
| TRIBE-minus-textfeat gain versus KD-only | `-0.001213` | `[-0.001846, -0.000580]` | all six seed margins negative; sign-flip `p=0.03125` | Kills the real-brain positive route for this gate. |
| TRIBE-minus-textfeat gain versus permuted-control gains | `-0.001005` | `[-0.001643, -0.000368]` | five negative margins and one tiny positive margin | Does not rescue a positive route; mean and CI are negative. |
| TRIBE gain versus permuted TRIBE | `-0.001786` | `[-0.002166, -0.001407]` | all six seed margins negative; sign-flip `p=0.03125` | The TRIBE target itself does not beat its permuted twin on real-brain Tuckute. |

The PCA robustness summaries at `25`, `50`, and `100` components do not reverse the route: the TRIBE-minus-textfeat real-brain means remain negative across the recorded PCA settings.

## Verdict

**Verdict.** The E016 positive branch is synthetic-endpoint only. It survives the matched textfeat control on synthetic target-R2, but it fails the real-brain Tuckute transfer gate. The paper route should narrow to a controlled study of neural/cognitive privileged targets in KD: synthetic proxy gains can survive matched non-brain text-feature controls and still fail to transfer to this real-brain endpoint.

**Not supported.** E016 does not support a brain-specific positive claim, a real-brain-alignment improvement claim, or a new `contextfeat`/OPRD/PHF compute launch as an automatic next step.

**Supported.** E016 supports a paper route centered on estimand/control discipline: KD-only, permuted target, matched-information non-brain target, seed-aligned paired inference, and a real-brain transfer gate that prevents synthetic-target gains from being overclaimed as brain alignment gains.

## Review Limits

This Codex surface did not spawn the repo's subagent panel because the current multi-agent tool requires explicit user delegation. The local replacement was a direct row-level recompute plus an adversarial check of the main escape hatches: incomplete grid, analysis/audit mismatch, PCA rescue, permuted-control rescue, and overclaiming synthetic target-R2 as real-brain transfer. If this diagnostic becomes central in a submitted paper, run an independent code/stat review of the saved-student Tuckute evaluator before drafting the final results section.

## Paper Consequence

The default route is now AAAI-style unless a later writing/planning pass finds a broader ICML-worthy estimand/control lesson. ICLR/NeurIPS are not the default from this evidence because the real-brain positive route did not open and the current negative route is one controlled transfer gate, not yet a broad field-correcting result.

## Related

- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-readiness-matrix-2026-07-07.md`](top-venue-readiness-matrix-2026-07-07.md)
- [`ladder.md`](ladder.md)
