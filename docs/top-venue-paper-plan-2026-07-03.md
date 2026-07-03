---
title: "Top-venue paper plan, 2026-07-03"
tags: [reference]
aliases: [top-venue-paper-plan-2026-07-03, compression-paper-plan]
---

# Top-venue paper plan, 2026-07-03

**Status.** This is a `/plan` artifact built from the S51 `/scout` and `/work` state. It is not a report, not a manuscript section, and not a science verdict. It exists so the active E016 run has a clear decision tree when results arrive. The claim-by-claim proof ledger is [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), the pre-result interpretation manifest is [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), the follow-up venue audit is [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), the distillation-adjacency audit is [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md), the privileged-signal adjacency audit is [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), the on-policy/context-distillation audit is [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), and the long-context control feasibility memo is [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md).

## Claim cell

The thesis-native paper cell is **brain-alignment-guided compression/distillation under fixed student budget**.

The broad cells are now closed or too crowded:

- [Merlin et al., 2026](literature/canonical/merlin-2026_what-brain-data-adds.md) directly tests brain data beyond stimulus text for text-LM LoRA fine-tuning.
- [Xiao et al., 2026](literature/canonical/xiao-2026_brain-guided-llm-reasoning.md) shows task-fMRI-derived representation guidance can improve LLM reasoning.
- [Zhang et al., 2026](literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md) makes ECoG-tuning a credible positive speech-model branch.
- Measurement and attribution papers sharpen how to score alignment, but do not test fixed-budget compression.
- The distillation-adjacency, privileged-signal, and on-policy/context-distillation audits show that LLM KD, feature-level KD, generic privileged-information distillation for LMs, context/self-distillation, rich-feedback distillation, gaze supervision, and task-specific PI-enhanced KD into smaller LMs are active. The paper therefore must not claim novelty for privileged-information KD itself, training-only PI improving smaller LMs, context internalization, dense feedback, on-policy teacher supervision, or gaze/cognitive supervision. The open cell is biological/synthetic-brain privileged targets under the fixed-budget KD protocol.

So the paper must not be framed as "brain data helps LMs." It must be framed as:

> When the deployment target is a smaller KD student, does a brain-alignment target change the utility/alignment frontier beyond KD-only, permuted-target, and matched-information non-brain controls?

## Result-contingent paper branches

| E016 outcome | Claim shape | Required next action |
|---|---|---|
| `tribe_mse` does not beat `kd_only` or `tribe_perm` at matched PPL | Controlled negative: dense synthetic neural targets do not improve fixed-budget KD even after removing fMRI scarcity and averaging confounds. | `/interpret` audit, then write as a frontier/protocol paper if the analyzer gate is complete and the null is stable across seeds. |
| `tribe_mse` beats `tribe_perm` and `kd_only`, but PPL is not matched | Not a brain-alignment result; it is a quality/regularization confound. | Tune lambda or abandon the positive interpretation. |
| `tribe_mse` beats `tribe_perm` and `kd_only` at matched PPL | Promising compression signal, but not yet brain-specific. | Run the matched-information `textfeat` control. A brain-specific claim requires beating `textfeat_mse` and `textfeat_perm` under the same budget. |
| `tribe_mse` and `textfeat_mse` both beat KD/permuted similarly | Dense privileged targets help KD, but brain specificity is not supported. | Paper becomes a control finding about privileged target geometry, not a brain-specific paper. |
| `tribe_mse` beats `textfeat_mse`, `tribe_perm`, and KD at matched PPL | Strongest current positive branch, but only against a sentence-local teacher-hidden-state control. | Add seeds plus either long-context/on-policy distillation control, real-brain evaluation, or a narrowed claim before a top-tier brain-specific submission. See [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md). |

## Experiment matrix

| Arm | Purpose | Status |
|---|---|---|
| KD-only | Fixed-budget student baseline. | Active full E016 run will produce this. |
| TRIBE target | Synthetic brain target under the same KD budget. | Active full E016 run will produce this. |
| TRIBE block-permuted | Dense target/statistics control with stimulus alignment broken. | Active full E016 run will produce this. |
| Text-feature target | Matched-information non-brain privileged target: sentence-local frozen `gpt2-medium` hidden states, projected to the same target dimension. | Launcher prepared by [`e016_make_textfeat_control_script.py`](../scripts/e016_make_textfeat_control_script.py), not run. It clears the teacher-hidden-state/dense-feature alternative, not long-context or on-policy privileged distillation. |
| Text-feature block-permuted | Dense non-brain target-statistics twin. | Launcher prepared, not run. |
| TRIBE-vs-textfeat comparator | Read-only post-positive analyzer comparison. | [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) prepared; use only after both analyzer JSONs are science-ready. |
| Extra seeds | Inference-strengthening if the positive branch survives. | Do only after E016 and textfeat justify it. |
| Long-context non-brain control (`contextfeat`) | Separates synthetic-brain specificity from generic context-conditioned teacher-feature effects. | Not yet built, but mechanically feasible: [`e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py) exactly recovers WikiText row/header context and writes joinable metadata. Build only after E016 and textfeat justify it. See [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md). |
| On-policy non-brain control | Separates synthetic-brain specificity from generic teacher supervision on the student's own trajectories. | Not built. This remains a new runner protocol, not a target-cache variant. [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md) records the estimand split. |
| Real-brain evaluation | Separates synthetic-target fit from real brain alignment. | Optional but likely needed for a top-tier positive claim. |

## Analyzer gates

The E016 analyzer must be treated as a gate, not a verdict engine. A result is not ready for interpretation unless it has:

- complete expected arm grid,
- at least three expected seeds,
- heldout target metrics present,
- full-scale train/heldout/target-dimension thresholds satisfied,
- PPL matched for every target/permuted arm at the predeclared tolerance,
- paired target-vs-permuted and target-vs-KD deltas available for audit.

For a positive paper, the paired effect must be inspected seed-by-seed. With only three seeds, an exact sign-flip test is useful as a sanity check but cannot by itself carry a strong inferential claim. A top-tier positive likely needs more seeds, a second dataset/evaluation target, or both.

## Paper skeleton

1. **Problem.** Brain-alignment scores and brain-tuning positives exist, but fixed-budget compression is the deployment-relevant cell left open.
2. **Method.** KD-only versus brain-guided KD under matched budget, with permuted target and matched-information non-brain target controls.
3. **Result branch.** Report either the controlled null or the positive branch after the above gates.
4. **Control interpretation.** Separate brain-specific signal from dense-target regularization, text-derived privileged information, and PPL movement.
5. **Contribution.** A strict protocol plus an empirical answer for whether brain-alignment guidance transfers into compressed students.

## Venue fit

| Venue | Best-fit angle | Risk |
|---|---|---|
| ICLR | Representation learning and training-objective question. | Positive branch needs stronger inference or extra target evaluation. |
| ICML | Estimation/control protocol for privileged biological targets in distillation. | Needs clean method framing and enough statistical strength. |
| NeurIPS | Brain/AI bridge plus compression and careful controls. | Broad brain-tuning novelty is gone; the fixed-budget cell must be foregrounded. |
| AAAI | Robust empirical study with clear negative or bounded positive. | May be less ideal if the final contribution is mainly methodology. |

## Must-not-claim

- Do not claim first brain-guided LLM improvement.
- Do not claim first brain data beyond stimulus text.
- Do not claim first privileged-information distillation for language models.
- Do not claim first training-only privileged information improvement for smaller language models.
- Do not claim first context/self-distillation, dense-feedback distillation, or gaze/cognitive supervision for modern LMs/VLMs.
- Do not treat `textfeat` as clearing long-context or on-policy distillation; it clears a sentence-local frozen-teacher hidden-state target.
- Do not claim brain-specificity from TRIBE alone if `textfeat` is not run.
- Do not claim that a positive TRIBE result is more than a dense privileged-target effect until it beats matched non-brain targets; if it beats `textfeat`, say exactly that it beat a sentence-local teacher-hidden-state control and expect reviewers to ask about long-context/on-policy distillation variants or real-brain evaluation.
- Do not claim a science null or positive before the active full E016 run produces an analyzer JSON and passes `/interpret`.
- Do not use synthetic target-R2 as a substitute for real-brain utility unless explicitly framed as a synthetic-target result.

## Related

- [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md) - source frontier memo
- [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md) - source-facing venue/open-question audit
- [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md) - KD/privileged-information adjacency audit
- [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md) - context/self-distillation and gaze/cognitive-supervision adjacency audit
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md) - focused on-policy/context-distillation control burden
- [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md) - recovered WikiText context metadata for a possible contextfeat control
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) - claim/readiness ledger
- [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md) - pre-result post-run manifest
- [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) - active Phase-3 experiment
- [`01-research-landscape.md`](01-research-landscape.md) - literature map
- [`ladder.md`](ladder.md) - canonical status board
