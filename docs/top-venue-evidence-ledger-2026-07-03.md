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
| Generic privileged-signal/context/gaze supervision novelty is closed. | [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), plus canonical notes for Deng 2024 and E024. | Scout-supported frontier claim. | Do not claim "PI/cognitive/gaze/context signals help models" as the contribution; use it only to motivate stricter controls. |
| Fixed-budget compression/distillation remains open. | Frontier memo plus absence of KD-only smaller-student, matched-PPL, permuted-target, matched-information controls in the scouted set. | Best current open question. | Needs E016 and, if positive, text-feature control evidence. |
| E016 null branch: dense synthetic brain targets do not move KD at matched PPL. | Full TRIBE run, analyzer, readiness packet, and independent recompute audit exist; the router did not choose the null branch. | Not current route for the TRIBE artifact. | Keep as a paper fallback only if later controls show the apparent TRIBE gain is generic or unusable. Do not rewrite this into a science verdict without `/interpret`. |
| E016 positive branch: TRIBE target improves the student beyond KD and permuted target. | `phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`, readiness packet, and independent recompute audit. Gate is `science_ready=true`; branch is `tribe_positive_needs_textfeat`; TRIBE target exceeds KD and permuted target on all 3 paired seeds at matched PPL. | Routing-supported TRIBE-positive synthetic-target branch. | This still only supports a dense TRIBE-target routing signal, not brain specificity. Finish the running text-feature control, then compare ready analyzer JSONs and run `/interpret`/stat/code review before a claim. |
| Brain-specific positive branch: TRIBE beats matched-information non-brain target. | Combined seed `0-5` TRIBE/textfeat artifacts are science-ready; `phase3_combined_tribe_vs_textfeat_s0-5_comparison.interpret_audit.json` recomputed raw-row margins: TRIBE-minus-textfeat gain is `+0.077395` versus KD-only and `+0.072531` versus permuted-control gains, all six seed margins positive, sign-flip `p=0.03125`, max relative PPL delta `0.009220`. The saved seed `3-5` real-brain diagnostic then found TRIBE-minus-textfeat Tuckute gain versus KD-only `-0.000862` and versus permuted-control gains `-0.000784`. | Synthetic-target branch held; real-brain diagnostic warning. | The sentence-local textfeat objection does not explain the synthetic target-R2 gain, but the saved-student Tuckute endpoint does not support real-brain transfer. A brain-specific top-tier claim now requires `/interpret`/code/stat review and either a predeclared robustness/rerun path or a narrowed claim. |
| Post-positive trained-student availability. | [`run_tribe_phase3.py`](../scripts/run_tribe_phase3.py) now supports opt-in `--save-model-dir`; [`e016_make_textfeat_control_script.py`](../scripts/e016_make_textfeat_control_script.py) includes it for the queued textfeat run. | Infrastructure only. | The active TRIBE full run was already running before artifact saving was added and will not save students unless rerun. Any real-brain/probe follow-up must verify whether the needed model artifacts exist before assuming post-hoc evaluation is possible. |
| Saved-student real-brain alignment follow-up. | [`e016_eval_saved_student_alignment.py`](../scripts/e016_eval_saved_student_alignment.py) scored all 18 saved seed `3-5` TRIBE/textfeat artifacts on Tuckute; paired analysis is `phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment_analysis.json`. A local raw-row audit `phase3_extra_tribe_vs_textfeat_s3-5_tuckute_alignment.interpret_audit.json` passed row/protocol/arithmetic/PCA checks and routed to `real_brain_warning_needs_claim_scope_review`. TRIBE target versus KD-only mean `-0.000735`; TRIBE target versus permuted mean `-0.001717`; TRIBE-minus-textfeat gain versus KD-only mean `-0.000862`. | Diagnostic completed and locally audited; warning for the positive branch. | Still needs claim-scope decision and, before any paper claim, code/stat review of the evaluator. It weakens the real-brain-positive route but is not a final verdict because it is post-hoc, ROI-level, and only covers saved seed `3-5`. |
| Long-context positive-branch burden. | [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md); [`e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py) exact-replay helper; [`build_context_feature_target_cache.py`](../scripts/build_context_feature_target_cache.py) CPU-smoked builder. | Feasible, not run at scale. | Build a full `contextfeat` target-cache arm only if E016 is positive and survives textfeat. This clears context-conditioned teacher-feature targets, not on-policy student-rollout supervision. |
| Six-seed real-brain robustness rerun. | [`top-venue-claim-scope-review-2026-07-07.md`](top-venue-claim-scope-review-2026-07-07.md) predeclares rerunning only missing TRIBE seed `0-2` artifacts before narrowing the paper. The stable rerun has saved the first partial arm artifact (`seed0_kd_only_lambda0`) and a detached watcher is waiting to run the combined seed `0-5` Tuckute analyzer once the rerun Tuckute JSON appears. | Active next evidence burden. | Needed because the current Tuckute warning covers saved TRIBE seed `3-5` only, while textfeat seed `0-5` artifacts already exist. Do not interpret partial arm artifacts as results. |
| Top-tier positive paper claim. | TRIBE beats the prepared sentence-local textfeat control across six paired seeds on the synthetic target endpoint, but the saved seed `3-5` Tuckute diagnostic is negative/slightly textfeat-favoring. | Brain-specific positive branch on HOLD. | Do not write a brain-specific positive claim from the current evidence. Next useful choices are: `/interpret` the diagnostic and narrow to a synthetic-target/control paper, or predeclare a robustness/rerun path that could overturn the Tuckute warning. |
| Top-tier controlled-negative/protocol paper claim. | Broader repo has a strong negative/methodology spine; E016 no longer routes to a simple null or generic-textfeat tie. | Fallback only. | Could re-enter if `/interpret` or code/stat review breaks the apparent TRIBE-vs-textfeat margin, or if the final claim must be narrowed into a control/protocol lesson. |

## Venue Burden

| Venue | What the paper must prove | Most likely branch |
|---|---|---|
| ICLR | A representation-learning/training-objective result, not just a neuroscience measurement. | Positive branch if TRIBE survives textfeat; controlled-negative only if the protocol lesson is sharp. |
| ICML | A clean estimand/control contribution around privileged biological targets in distillation. | Controlled-negative or textfeat-matched branch. |
| NeurIPS | A brain/AI bridge with strong empirical novelty and controls. | Strong positive branch, or unusually crisp field-correcting negative. |
| AAAI | A robust empirical study with a clear method/control lesson. | Controlled-negative, textfeat-matched, or positive branch. |

## Minimum Paper Packages

| Package | Core claim | Evidence that must exist before drafting | Venue realism |
|---|---|---|---|
| Synthetic-target/control paper | TRIBE-like synthetic neural targets can move a fixed-budget KD student on the synthetic neural endpoint beyond a sentence-local teacher-feature target, but this is not automatically real-brain transfer. | Six-seed synthetic TRIBE-vs-textfeat audit (already present), six-seed real-brain diagnostic showing nonpositive or mixed transfer after the active rerun, and a clean `/interpret`/code-stat audit that separates synthetic-target movement from real-brain alignment. | Most realistic AAAI or strong workshop route; ICML/ICLR only if the control/protocol lesson is generalized or unusually crisp. |
| Brain-specific positive paper | A brain-derived privileged target improves a smaller KD student beyond matched text-feature/permuted controls and transfers to real brain alignment. | Active six-seed real-brain diagnostic must reverse the current warning; then independent implementation/stat audit, evaluator review, and likely a stronger non-brain control (`contextfeat` or on-policy) or external endpoint. | Only plausible ICML/ICLR/NeurIPS route from E016, but currently on HOLD. |
| Controlled-negative/protocol paper | Strict matched-PPL, permuted-target, matched-information, and real-brain-transfer controls prevent overclaiming neural/cognitive privileged-target effects in KD. | Either the active rerun confirms the real-brain warning despite the synthetic positive, or a later code/stat audit breaks the synthetic branch; the paper must present the ladder as a protocol contribution rather than a failed method. | AAAI realistic; ICML possible if framed as an estimand/control contribution for biological privileged signals. |
| Dense privileged-target paper | Dense training-time targets help or reshape KD, but the effect is not brain-specific. | Requires a result where TRIBE and non-brain privileged targets move similarly, or a context/on-policy control that explains the synthetic TRIBE gain. Current evidence does not yet support this package. | Less attractive unless it yields a clean method insight beyond this thesis. |

## Decision Rule For The Active Run

The seed-extended synthetic comparator passed a local raw-row `/interpret` audit, and the saved seed `3-5` real-brain diagnostic has now run. The next legitimate state transition is one of:

1. **Robustness/rerun path:** rerun only missing TRIBE seed `0-2` artifacts, then evaluate the real-brain diagnostic over seed `0-5`.
2. **Claim-scope review path:** if the six-seed real-brain diagnostic stays nonpositive or mixed, narrow to synthetic brain-like target survival beyond sentence-local text features, without claiming real-brain specificity.
3. **Evaluator review path:** run code/stat review of the Tuckute evaluator before any paper claim uses the diagnostic.
4. **Stronger non-brain-control path:** build/run contextfeat or design on-policy control only after naming the estimand, and only with the real-brain warning still visible.

The analyzer's `paper_branch_hint` is only a routing aid into this ledger. It is valid only after `gate.science_ready=true`; it is not a verdict and does not replace `/interpret`.

## Related

- [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md) - literature frontier
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md) - result-contingent paper plan
- [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md) - privileged-signal/context/gaze adjacency audit
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md) - on-policy/context-distillation control burden
- [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md) - recovered-context control feasibility
- [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md) - pre-result post-run manifest
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md) - active experiment record
- [`ladder.md`](ladder.md) - canonical thesis status
- [`tasks.md`](tasks.md) - operational backlog
