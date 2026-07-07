---
title: "E016 combined Tuckute interpretation gate, 2026-07-07"
tags: [plan, E016, top-venue]
aliases: [E016-combined-Tuckute-gate, real-brain-transfer-gate]
---

# E016 combined Tuckute interpretation gate, 2026-07-07

**Status.** This is a `/plan`/`/work` handoff artifact for the active E016 real-brain rerun. It is not a report, not a manuscript section, not a verdict, and not a rung update. It exists so the combined seed `0-5` Tuckute result is interpreted only after the required files and audit checks exist.

## Gate Question

After the bounded TRIBE seed `0-2` artifact-saving rerun finishes, does the seed-aligned real-brain Tuckute diagnostic support, weaken, or fail to adjudicate the brain-specific positive paper route?

The estimand is narrow: TRIBE target training versus sentence-local text-feature target training, compared by seed-aligned real-brain unique-R2 gains over KD-only and over the corresponding permuted-target control, using the saved-student Tuckute evaluator and the same contiguous nuisance-subtracted protocol already used for the seed `3-5` diagnostic.

## Required Files

The gate is not open until all of these exist and are non-empty:

| File | Role |
|---|---|
| `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json` | Rerun TRIBE seed `0-2` run rows with saved artifact paths. |
| `outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.tuckute_alignment.json` | Real-brain scoring for rerun TRIBE seed `0-2`. |
| `outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.tuckute_alignment.json` | Existing real-brain scoring for TRIBE seed `3-5`. |
| `outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.tuckute_alignment.json` | Completed real-brain scoring for textfeat seed `0-5`. |
| `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json` | Seed-aligned combined analysis from `scripts/e016_analyze_tuckute_alignment.py`. |
| `outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.audit.json` | Raw-row audit from `scripts/e016_audit_tuckute_alignment.py`. |

## Acceptance Checks

The combined diagnostic is eligible for `/interpret` only if the audit JSON reports:

| Check | Required condition |
|---|---|
| complete seeds | `complete_seeds == [0,1,2,3,4,5]` and `missing_expected_seeds == []` |
| row grid | KD-only, target, and permuted arms exist for every seed on both TRIBE and textfeat sides |
| artifacts | no missing or unusable artifact rows |
| protocol identity | same Tuckute endpoint and scoring protocol across all alignment sources |
| arithmetic | analysis contrasts, by-arm summaries, and PCA robustness summaries match raw-row recomputation |
| audit status | `all_checks_pass == true` |

If any acceptance check fails, the result is not paper-load-bearing. The next action is debugging or evaluator/code review, not claim selection.

## Route Labels

Use the audit `route` and then confirm the underlying per-seed pattern in `/interpret`.

| Route | Meaning | Paper consequence |
|---|---|---|
| `real_brain_positive_needs_stat_code_review` | TRIBE-minus-textfeat gains are positive versus KD-only and versus permuted-control gains after row/protocol/arithmetic checks. | Reopens the brain-specific positive route only. It still requires independent code/stat review, likely a stronger non-brain control or external endpoint, and a clean `/interpret` verdict before any ICML/ICLR/NeurIPS-style claim. |
| `real_brain_warning_needs_claim_scope_review` | The mean TRIBE-minus-textfeat real-brain gains are nonpositive on the key contrasts after checks pass. | Narrow toward the synthetic-target/control paper: synthetic target movement can survive textfeat on the synthetic endpoint, but it does not transfer to this real-brain endpoint. |
| `real_brain_mixed_needs_claim_scope_review` | The combined diagnostic is neither clean positive nor clean nonpositive. | Treat as insufficient for a brain-specific positive paper. Inspect seed pattern and uncertainty before deciding whether the paper narrows or another predeclared check is justified. |
| `real_brain_alignment_audit_failed_needs_debug` | Files exist, but integrity or arithmetic checks fail. | No claim. Debug evaluator, row identity, protocol mismatch, or analysis code. |
| `real_brain_alignment_audit_not_ready` | Required seeds/files are incomplete. | No claim. Continue monitoring or repair missing postprocess. |

## Non-Negotiables

- Do not interpret partial arm artifacts, partial Tuckute rows, or analysis JSON without the audit JSON.
- Do not use synthetic target-R2 as a substitute for real-brain transfer.
- Do not flip a ladder rung from this gate; any verdict still needs `/interpret` and Erfan confirmation.
- Do not write a brain-specific positive paper claim unless the real-brain route is positive and then survives code/stat review.
- If the result is nonpositive or mixed, preserve the positive synthetic-target finding as synthetic-target evidence only; do not rewrite it into a failure of all privileged-target training.

## Related

- [`top-venue-claim-scope-review-2026-07-07.md`](top-venue-claim-scope-review-2026-07-07.md)
- [`top-venue-literature-refresh-2026-07-07.md`](top-venue-literature-refresh-2026-07-07.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
