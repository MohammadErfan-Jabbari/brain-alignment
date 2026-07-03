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
| Brain-specific positive branch: TRIBE beats matched-information non-brain target. | Full `textfeat` control launched on 2026-07-03 after the TRIBE runner completed. The control is sentence-local frozen-LM hidden-state supervision, projected to the same target dimension; full train and heldout caches are built and validated, and training is running. | Not yet known. | Wait for the textfeat run JSON and analyzer JSON. Needs same analyzer gate, `e016_compare_target_controls.py`, and preferably more seeds or a second evaluation target. It does not clear long-context/on-policy distillation. |
| Post-positive trained-student availability. | [`run_tribe_phase3.py`](../scripts/run_tribe_phase3.py) now supports opt-in `--save-model-dir`; [`e016_make_textfeat_control_script.py`](../scripts/e016_make_textfeat_control_script.py) includes it for the queued textfeat run. | Infrastructure only. | The active TRIBE full run was already running before artifact saving was added and will not save students unless rerun. Any real-brain/probe follow-up must verify whether the needed model artifacts exist before assuming post-hoc evaluation is possible. |
| Saved-student real-brain alignment follow-up. | [`e016_eval_saved_student_alignment.py`](../scripts/e016_eval_saved_student_alignment.py) loads saved `model_artifact_dir` rows and scores them on Tuckute with the E003 contiguous-CV nuisance-subtracted protocol. Tiny CPU smoke passed on an artifact-retention smoke run. | Infrastructure only. | Full-scale use requires selected E016/textfeat/contextfeat students saved with `--save-model-dir`. The output is diagnostic and still needs `/interpret`, code/stat audit, and comparison against the synthetic-target gate before it can support a paper claim. |
| Long-context positive-branch burden. | [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md); [`e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py) exact-replay helper; [`build_context_feature_target_cache.py`](../scripts/build_context_feature_target_cache.py) CPU-smoked builder. | Feasible, not run at scale. | Build a full `contextfeat` target-cache arm only if E016 is positive and survives textfeat. This clears context-conditioned teacher-feature targets, not on-policy student-rollout supervision. |
| Top-tier positive paper claim. | No brain-specific evidence yet. The TRIBE-only branch is positive on the synthetic target endpoint, and textfeat is running. | Conditional. | Requires textfeat control passed, paired effects stable, code/stat audit clean, and likely extra seeds plus either contextfeat/on-policy control, real-brain evaluation, or a narrowed claim. The estimand split is recorded in [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md). |
| Top-tier controlled-negative/protocol paper claim. | Broader repo has a strong negative/methodology spine; full TRIBE alone no longer routes to a simple null. | Conditional. | Could still emerge if textfeat shows the gain is generic dense privileged-target supervision. Requires ready textfeat analyzer, stable paired deltas, and careful claim wording. |

## Venue Burden

| Venue | What the paper must prove | Most likely branch |
|---|---|---|
| ICLR | A representation-learning/training-objective result, not just a neuroscience measurement. | Positive branch if TRIBE survives textfeat; controlled-negative only if the protocol lesson is sharp. |
| ICML | A clean estimand/control contribution around privileged biological targets in distillation. | Controlled-negative or textfeat-matched branch. |
| NeurIPS | A brain/AI bridge with strong empirical novelty and controls. | Strong positive branch, or unusually crisp field-correcting negative. |
| AAAI | A robust empirical study with a clear method/control lesson. | Controlled-negative, textfeat-matched, or positive branch. |

## Decision Rule For The Active Run

Do not start another heavy run while the `textfeat` control is active. The next legitimate state transition is one of:

1. **Textfeat still running:** monitor the detached launcher/log; do not start contextfeat, extra seeds, or real-brain probes.
2. **Textfeat runner failure:** debug the launcher/log before interpreting anything.
3. **Textfeat run JSON without analyzer:** run the guarded finalizer on the textfeat run JSON or run the analyzer/readiness packet directly.
4. **Ready textfeat analyzer:** compare the ready TRIBE and textfeat analyzer JSONs with `scripts/e016_compare_target_controls.py`, then switch to `/interpret`.
5. **TRIBE beats textfeat:** treat it as a post-positive review branch, not brain-specific clearance; inspect the privileged-signal adjacency burden and decide whether extra seeds, context/on-policy controls, real-brain evaluation, or a narrowed claim is required.
6. **Textfeat matches or beats TRIBE:** route the paper toward dense privileged-target geometry/control findings, not a brain-specific positive.

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
