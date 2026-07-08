---
title: "Top-venue evidence ledger, 2026-07-03"
tags: [reference]
aliases: [top-venue-evidence-ledger-2026-07-03, compression-evidence-ledger]
---

# Top-venue evidence ledger, 2026-07-03

**Status.** This is a `/plan` and `/work` coordination artifact. It is not a report, not a manuscript section, and not a science verdict. It exists to keep the active top-venue goal honest while E016 trains. The pre-result post-run interpretation manifest is [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md).

## Purpose

The current candidate paper cell is **brain-alignment-guided compression/distillation under fixed student budget**. The broad "brain data helps language models" pitch is no longer defensible as our contribution because recent work has already tested brain-tuning, brain-data-vs-stimulus comparisons, and brain-guided reasoning. The remaining paper must be a controlled answer to a narrower question:

> At fixed student budget, matched perplexity, and with permuted plus matched-information twins, does brain-alignment guidance change the KD student's alignment/utility frontier?

This ledger separates what is already supported, what is only a literature/open-question claim, and what still needs evidence before it can become an AAAI/ICML/ICLR/NeurIPS paper.

## Claim Ledger

| Candidate claim | Current evidence | Status | Missing proof before paper claim |
|---|---|---|---|
| The LM-brain alignment signal is real enough to use as an experimental object. | [`ladder.md`](ladder.md) Q0/A2; E002 and E006. | Recorded thesis result. | No new proof needed for the compression paper's motivation, but cite the recorded caveats and the E006 CI-unit audit if reopened. |
| Plain KD does not obviously preserve the teacher's alignment. | [`ladder.md`](ladder.md) Q1; E003. | Recorded partial result. | Do not overclaim KD-specific shedding; frame it as headroom plus quality entanglement. |
| Existing brain-alignment optimization did not give a robust per-individual gain in this repo. | [`ladder.md`](ladder.md) Q2-Q4; E004/E008/E009/E011/E013/E017/E024. | Recorded negative/methodology spine. | This motivates the strict controls; it is not enough by itself for the new top-tier paper. |
| Generic brain-tuning novelty is closed. | [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md), canonical notes for Moussa, Merlin/CoNLL, Zhang, Xiao, Bilgin, Oota, Jia. | Scout-supported frontier claim. | Keep fresh before submission; do not turn this into a result claim. |
| Generic privileged-signal/context/gaze supervision novelty is closed. | [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), plus canonical notes for Deng 2024 and E024. The 2026-07-07 Firecrawl Research follow-up in [`top-venue-literature-refresh-2026-07-07.md`](top-venue-literature-refresh-2026-07-07.md) adds July 2026 PI/on-policy papers that foreground privileged-context degradation and leakage. | Scout-supported frontier claim. | Do not claim "PI/cognitive/gaze/context signals help models" as the contribution; use it only to motivate stricter controls. If E016 is negative/mixed on real-brain transfer, frame the lesson as controlled privileged-target transfer failure, not merely "brain target did not help." |
| Fixed-budget compression/distillation remains open. | Frontier memo plus absence of KD-only smaller-student, matched-PPL, permuted-target, matched-information controls in the scouted set. E016 now supplies the controlled synthetic-target plus real-brain transfer-failure case. | Best current paper question, narrowed. | Needs paper planning/writing, plus independent code/stat review only if the Tuckute diagnostic becomes publication-load-bearing. |
| E016 null branch: dense synthetic brain targets do not move KD at matched PPL. | Full TRIBE run, analyzer, readiness packet, and independent recompute audit exist; the router did not choose the null branch. | Not current route for the TRIBE artifact. | Keep as a paper fallback only if later controls show the apparent TRIBE gain is generic or unusable. Do not rewrite this into a science verdict without `/interpret`. |
| E016 positive branch: TRIBE target improves the student beyond KD and permuted target. | `phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`, readiness packet, and independent recompute audit. Gate is `science_ready=true`; branch is `tribe_positive_needs_textfeat`; TRIBE target exceeds KD and permuted target on all 3 paired seeds at matched PPL. The later combined seed `0-5` TRIBE-vs-textfeat synthetic comparator also held. | Synthetic-target branch supported. | This supports dense TRIBE-target movement on the synthetic endpoint, not brain specificity. The textfeat control and real-brain Tuckute transfer gate are now complete; the transfer gate prevents a brain-specific positive claim. |
| Brain-specific positive branch: TRIBE beats matched-information non-brain target. | Combined seed `0-5` TRIBE/textfeat artifacts are science-ready; `phase3_combined_tribe_vs_textfeat_s0-5_comparison.interpret_audit.json` recomputed raw-row margins: TRIBE-minus-textfeat gain is `+0.077395` versus KD-only and `+0.072531` versus permuted-control gains, all six seed margins positive, sign-flip `p=0.03125`, max relative PPL delta `0.009220`. The combined seed `0-5` Tuckute diagnostic then found TRIBE-minus-textfeat real-brain gain versus KD-only `-0.001213`, CI `[-0.001846, -0.000580]`, all six margins negative; versus permuted-control gains it found `-0.001005`, CI `[-0.001643, -0.000368]`. | Synthetic-target branch held; real-brain positive branch not supported. | The sentence-local textfeat objection does not explain the synthetic target-R2 gain, but the saved-student Tuckute endpoint rejects a real-brain-transfer claim for this goal. The paper route narrows to synthetic-target/control plus transfer failure. |
| Post-positive trained-student availability. | [`run_tribe_phase3.py`](../scripts/run_tribe_phase3.py) now supports opt-in `--save-model-dir`; [`e016_make_textfeat_control_script.py`](../scripts/e016_make_textfeat_control_script.py) includes it for the queued textfeat run. | Infrastructure only. | The active TRIBE full run was already running before artifact saving was added and will not save students unless rerun. Any real-brain/probe follow-up must verify whether the needed model artifacts exist before assuming post-hoc evaluation is possible. |
| Saved-student real-brain alignment follow-up. | [`e016_eval_saved_student_alignment.py`](../scripts/e016_eval_saved_student_alignment.py) scored the saved seed `3-5` TRIBE/textfeat artifacts and, after the bounded rerun, the combined seed `0-5` TRIBE/textfeat artifacts on Tuckute. The combined paired analysis is `phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json`; the audit `phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.audit.json` passed row/protocol/arithmetic/PCA checks and routed to `real_brain_warning_needs_claim_scope_review`. The `/interpret` recompute `phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.interpret_recompute.json` matched the recorded analysis/audit. | Diagnostic completed, locally audited, and interpreted as warning/nonpositive. | Use it for claim-scope routing now. If it becomes a submitted-paper load-bearing result, run an independent evaluator/stat review before drafting the final result. |
| Long-context positive-branch burden. | [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md); [`e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py) exact-replay helper; [`build_context_feature_target_cache.py`](../scripts/build_context_feature_target_cache.py) CPU-smoked builder. | Feasible, not run at scale. | Build a full `contextfeat` target-cache arm only if E016 is positive and survives textfeat. This clears context-conditioned teacher-feature targets, not on-policy student-rollout supervision. |
| Six-seed real-brain robustness rerun. | [`top-venue-claim-scope-review-2026-07-07.md`](top-venue-claim-scope-review-2026-07-07.md) predeclared rerunning only missing TRIBE seed `0-2` artifacts before narrowing the paper, and [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md) locked the postprocess acceptance/route criteria. The rerun, Tuckute scoring, combined analyzer, audit, and `/interpret` recompute are now complete. | Completed evidence burden. | The result confirms the warning route, so no further robustness rerun is owed for this goal. |
| Top-tier positive paper claim. | TRIBE beats the prepared sentence-local textfeat control across six paired seeds on the synthetic target endpoint, but the combined seed `0-5` Tuckute diagnostic is negative/nonpositive for real-brain transfer. | Brain-specific positive branch closed for this goal. | Do not write a brain-specific positive claim from E016. Reopening requires a new predeclared endpoint/dataset or a new goal, not more interpretation of these artifacts. |
| Top-tier controlled-negative/protocol paper claim. | Broader repo has a strong negative/methodology spine; E016 no longer routes to a simple null or generic-textfeat tie. The July 2026 PI/on-policy papers make leakage, shortcut transfer, and OOD degradation an external reason to value a real-brain-transfer gate. | Selected E016 paper route for this goal. | Frame as controlled transfer failure: synthetic privileged-target gains can survive matched textfeat on their own endpoint while failing the real-brain transfer test. |

## Venue Burden

| Venue | What the paper must prove | Most likely branch |
|---|---|---|
| ICLR | A representation-learning/training-objective result, not just a neuroscience measurement. | Not default after the real-brain transfer gate failed; possible only if the protocol lesson becomes broader than this one gate. |
| ICML | A clean estimand/control contribution around privileged biological targets in distillation. | Controlled-negative or textfeat-matched branch. |
| NeurIPS | A brain/AI bridge with strong empirical novelty and controls. | Hard after the positive route failed; requires unusually crisp field-correcting negative evidence. |
| AAAI | A robust empirical study with a clear method/control lesson. | Controlled-negative, textfeat-matched, or positive branch. |

## Minimum Paper Packages

| Package | Core claim | Evidence that must exist before drafting | Venue realism |
|---|---|---|---|
| Synthetic-target/control paper | TRIBE-like synthetic neural targets can move a fixed-budget KD student on the synthetic neural endpoint beyond a sentence-local teacher-feature target, but this is not automatically real-brain transfer. | Six-seed synthetic TRIBE-vs-textfeat audit, six-seed real-brain diagnostic showing negative/nonpositive transfer, and a clean `/interpret` recompute that separates synthetic-target movement from real-brain alignment. | Most realistic AAAI route; ICML possible only if the control/protocol lesson is generalized or unusually crisp. |
| Brain-specific positive paper | A brain-derived privileged target improves a smaller KD student beyond matched text-feature/permuted controls and transfers to real brain alignment. | Not supported by E016 after the combined seed `0-5` Tuckute interpretation. | Not the route for this goal. |
| Controlled-negative/protocol paper | Strict matched-PPL, permuted-target, matched-information, and real-brain-transfer controls prevent overclaiming neural/cognitive privileged-target effects in KD. | The completed robustness rerun confirmed the real-brain warning despite the synthetic positive. The paper must present the ladder as a protocol/estimand contribution rather than a failed method. | AAAI realistic; ICML possible if framed as an estimand/control contribution for biological privileged signals. |
| Dense privileged-target paper | Dense training-time targets help or reshape KD, but the effect is not brain-specific. | Requires a result where TRIBE and non-brain privileged targets move similarly, or a context/on-policy control that explains the synthetic TRIBE gain. Current evidence does not yet support this package. | Less attractive unless it yields a clean method insight beyond this thesis. |

## Decision Rule For The Active Run

The seed-extended synthetic comparator passed a local raw-row `/interpret` audit, and the combined seed `0-5` real-brain diagnostic has now been interpreted. The next legitimate state transition is one of:

1. **Paper planning path:** outline the synthetic-target/control plus real-brain transfer-failure paper.
2. **Evaluator review path:** run code/stat review of the Tuckute evaluator before any submitted-paper claim uses the diagnostic as load-bearing evidence.
3. **Stronger non-brain-control path:** build/run contextfeat or design on-policy control only after a new `/plan` names a reason that survives the real-brain warning; it is not the default next action.

The analyzer's `paper_branch_hint` is only a routing aid into this ledger. It is valid only after `gate.science_ready=true`; it is not a verdict and does not replace `/interpret`.

## Related

- [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md) - literature frontier
- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md) - combined Tuckute acceptance and route gate
- [`e016-combined-tuckute-interpretation-2026-07-08.md`](e016-combined-tuckute-interpretation-2026-07-08.md) - combined Tuckute verdict and paper-route closeout
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md) - result-contingent paper plan
- [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md) - privileged-signal/context/gaze adjacency audit
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md) - on-policy/context-distillation control burden
- [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md) - recovered-context control feasibility
- [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md) - pre-result post-run manifest
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md) - active experiment record
- [`ladder.md`](ladder.md) - canonical thesis status
- [`tasks.md`](tasks.md) - operational backlog
