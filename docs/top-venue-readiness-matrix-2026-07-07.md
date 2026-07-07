---
title: "Top-venue readiness matrix, 2026-07-07"
tags: [plan, E016, top-venue]
aliases: [top-venue-readiness-matrix-2026-07-07, venue-readiness-matrix]
---

# Top-venue readiness matrix, 2026-07-07

**Status.** This is a `/plan` artifact written while the bounded E016 TRIBE seed `0-2` artifact-saving rerun is active. It is not a report, not a manuscript section, not a science verdict, and not a ladder update. It converts the current literature/evidence state into a venue-specific burden map for AAAI, ICML, ICLR, and NeurIPS.

## Current Evidence State

The current candidate contribution is not broad brain-guided LLM improvement, generic privileged-information distillation, or hidden-state distillation. Those neighboring cells are already occupied by the literature summarized in [`top-venue-literature-refresh-2026-07-07.md`](top-venue-literature-refresh-2026-07-07.md), [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md), and [`top-venue-representation-control-feasibility-2026-07-07.md`](top-venue-representation-control-feasibility-2026-07-07.md).

The live open cell is narrower: under a fixed smaller-student KD budget, does a brain-derived privileged target beat KD-only, permuted dense-target controls, and matched non-brain text-feature controls, and does any gain transfer to real-brain alignment rather than only to the synthetic training proxy?

As of the latest recorded state, the six-seed synthetic TRIBE-vs-textfeat comparator is positive and locally audited, but the saved seed `3-5` Tuckute diagnostic is a warning against real-brain transfer. The decisive combined seed `0-5` real-brain gate is still pending because the rerun JSON, rerun Tuckute output, combined Tuckute analysis, and combined audit are absent. See [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md) for the exact required files and acceptance checks.

## Recommendation Before The Gate Resolves

Do not launch `contextfeat`, OPRD-lite, PHF-lite, or a new dataset while the combined Tuckute gate is incomplete. The next evidence is already running, and widening compute before that result would blur the estimand.

The strongest near-term paper route is contingent:

| Combined seed `0-5` Tuckute route | Best immediate paper package | Next action |
|---|---|---|
| `real_brain_warning_needs_claim_scope_review` or `real_brain_mixed_needs_claim_scope_review` | Synthetic-target/control plus privileged-target transfer-failure paper. | Run `/interpret`, code/stat review if load-bearing, then write the control ladder: synthetic proxy gains can survive textfeat yet fail the real-brain transfer gate. Do not launch new representation controls. |
| `real_brain_positive_needs_stat_code_review` | Brain-derived privileged-KD positive paper, still provisional. | Run independent code/stat review first, then build `contextfeat`; open OPRD-lite only if the positive survives and the venue claim needs an on-policy hidden-state comparator. |
| `real_brain_alignment_audit_failed_needs_debug` | No paper claim. | Debug evaluator, row identity, protocol mismatch, or arithmetic before interpreting. |
| `real_brain_alignment_audit_not_ready` | No paper claim. | Keep monitoring and do not interpret partial artifacts. |

## Venue Matrix

| Venue | Nonpositive or mixed real-brain gate | Positive and audit-clean real-brain gate | What would make it credible |
|---|---|---|---|
| AAAI | Most realistic main-track route if the controlled transfer-failure story is clean: a robust empirical study and evaluation ladder for neural/cognitive privileged targets in KD. | Viable but less distinctive than ICML/ICLR/NeurIPS if it becomes a methods-heavy positive. | Clean `/interpret` gate, readable control lesson, no overclaiming brain specificity, and a clear account of why matched textfeat plus real-brain transfer matters. |
| ICML | Possible if framed as an estimand/control contribution for biological privileged information in distillation, not as a neuroscience result. | Plausible if the positive survives independent audit and the control story is methodologically tight. | Precise estimand, matched budget/perplexity, seed-aligned paired statistics, and at least `contextfeat` if claiming more than sentence-local text-feature specificity. |
| ICLR | Weak unless the transfer-failure result yields a representation-learning lesson beyond one brain proxy. | Plausible if E016 becomes a training-objective result: brain-derived target improves the student and survives stronger non-brain controls. | Mechanistic representation framing, stronger non-brain comparator, and evidence that the effect is not hidden-state distillation, shortcut transfer, or synthetic-target overfitting. |
| NeurIPS | Hardest route for the nonpositive/mixed branch; needs a field-correcting story broad enough to matter beyond one dataset/proxy. | Best fit for a strong brain/AI bridge positive, but only after the largest burden clears. | Real-brain positive route, independent audit, stronger non-brain controls or external endpoint, and a conservative claim that respects the crowded brain-tuning and PI-distillation frontier. |

## Kill Gates

No paper package should proceed unless the combined Tuckute audit reports complete seeds `[0,1,2,3,4,5]`, no missing artifacts, protocol identity across alignment files, raw arithmetic agreement, and `all_checks_pass=true`.

If the gate is nonpositive or mixed, the next compute is not another representation control. The next work is interpretation and claim-scope tightening: preserve the six-seed synthetic-target result as synthetic-target evidence, and use the Tuckute result to test transfer.

If the gate is positive but fragile across seeds, PCA settings, or protocol checks, replication and audit beat new baselines.

If the gate is positive, robust, and audit-clean, the next control is `contextfeat`, because it stays inside the current cache-based estimand. OPRD-lite and PHF-lite are new-runner protocols and require a separate `/precheck`.

## One-Line Submission Strategy

The default submission target should be AAAI unless the combined real-brain gate becomes positive and survives code/stat review. ICML becomes plausible for either a crisp estimand/control paper or a positive with `contextfeat`. ICLR/NeurIPS require the positive route plus stronger controls or a broader field-correcting negative; they should not be treated as reachable from the current pending evidence alone.

## Related

- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-literature-refresh-2026-07-07.md`](top-venue-literature-refresh-2026-07-07.md)
- [`top-venue-representation-control-feasibility-2026-07-07.md`](top-venue-representation-control-feasibility-2026-07-07.md)
- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
