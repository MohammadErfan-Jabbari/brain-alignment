---
title: "Top-venue paper plan, 2026-07-03"
tags: [reference]
aliases: [top-venue-paper-plan-2026-07-03, compression-paper-plan]
---

# Top-venue paper plan, 2026-07-03

**Status.** This is a `/plan` artifact built from the S51 `/scout` and `/work` state. It is not a report, not a manuscript section, and not a science verdict. It exists so the active E016 run has a clear decision tree when results arrive. The claim-by-claim proof ledger is [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), the pre-result interpretation manifest is [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), the follow-up venue audit is [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), the distillation-adjacency audit is [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md), the privileged-signal adjacency audit is [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md), the on-policy/context-distillation audit is [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md), the long-context control feasibility memo is [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md), the representation-control feasibility memo is [`top-venue-representation-control-feasibility-2026-07-07.md`](top-venue-representation-control-feasibility-2026-07-07.md), and the venue-specific readiness matrix is [`top-venue-readiness-matrix-2026-07-07.md`](top-venue-readiness-matrix-2026-07-07.md).

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

Current route as of the 2026-07-08 `/interpret` closeout: the full TRIBE artifact passed the analyzer/readiness gate, the matched-information `textfeat` control completed, extra artifact-saving seeds `3,4,5` completed for both TRIBE and textfeat, and the combined seed `0-5` synthetic comparator held. A local raw-row `/interpret` audit reproduced all synthetic target-R2 seed-aligned margins: TRIBE-minus-textfeat gain is `+0.077395` versus KD-only and `+0.072531` versus permuted-control gains, all six margins positive. The bounded real-brain robustness rerun then completed the missing TRIBE seed `0-2` artifacts, and the combined seed `0-5` Tuckute diagnostic moved against the brain-specific positive branch: TRIBE-minus-textfeat real-brain gain versus KD-only is `-0.001213`, CI `[-0.001846, -0.000580]`, all six margins negative; versus permuted-control gains it is `-0.001005`, CI `[-0.001643, -0.000368]`. This supports a synthetic-target/control plus real-brain transfer-failure route, not a brain-specific positive route.

Literature pressure update as of 2026-07-07 22:20 UTC: newer PI/on-policy self-distillation papers now explicitly treat privileged-context degradation and privileged-information leakage as live failure modes, while OPRD and PHF make hidden-state/hidden-flow distillation active non-brain baseline families. This does not occupy the brain-derived KD cell, but it changes the rhetoric of the narrow branch. A negative or mixed E016 real-brain-transfer result should be positioned as a controlled test of whether a privileged neural target transfers, rather than as a generic brain-KD failure. A positive result must answer the leakage/shortcut objection and must not rely on novelty of representation-level distillation; it needs the textfeat/permuted controls plus real-brain transfer, and likely a stronger on-policy hidden-state/hidden-flow comparator before a top-tier brain-specific claim.

## Experiment matrix

| Arm | Purpose | Status |
|---|---|---|
| KD-only | Fixed-budget student baseline. | Full TRIBE run complete and analyzer-ready for the TRIBE branch. Textfeat control is running its matched KD-only baseline. |
| TRIBE target | Synthetic brain target under the same KD budget. | Full TRIBE run complete; analyzer gate `science_ready=true`; route `tribe_positive_needs_textfeat`. |
| TRIBE block-permuted | Dense target/statistics control with stimulus alignment broken. | Full TRIBE run complete; analyzer gate `science_ready=true`; used in the TRIBE-positive route. |
| Text-feature target | Matched-information non-brain privileged target: sentence-local frozen `gpt2-medium` hidden states, projected to the same target dimension. | Full textfeat run complete; analyzer gate `science_ready=true`; use as a sentence-local teacher-hidden-state control only. |
| Text-feature block-permuted | Dense non-brain target-statistics twin. | Full textfeat run complete; analyzer gate `science_ready=true`. |
| TRIBE-vs-textfeat comparator | Read-only post-positive analyzer comparison. | Combined seed `0-5` comparator `phase3_combined_tribe_vs_textfeat_s0-5_comparison.json` is ready and routes to `tribe_stronger_than_textfeat_needs_review`; the independent audit reproduced the raw-row margins with sign-flip `p=0.03125`. |
| Trained student artifacts | Keeps positive-branch students available for post-hoc probes or real-brain evaluation instead of forcing a rerun. | [`run_tribe_phase3.py`](../scripts/run_tribe_phase3.py) now has opt-in `--save-model-dir`; the queued textfeat launcher uses it. The active TRIBE full run was already in flight before this option existed, so any real-brain follow-up for that exact branch may still require rerunning selected arms with artifact saving. |
| Saved-student real-brain alignment probe | Scores saved E016/textfeat/contextfeat students on the real Tuckute endpoint using the E003 contiguous-CV nuisance-subtracted protocol. | Complete for combined seed `0-5` TRIBE/textfeat artifacts after the bounded TRIBE seed `0-2` artifact-saving rerun. [`e016-combined-tuckute-interpretation-2026-07-08.md`](e016-combined-tuckute-interpretation-2026-07-08.md) records the warning-route verdict. |
| Extra seeds | Inference-strengthening if the positive branch survives. | Complete for seeds `3,4,5`; merged with original seeds into combined `0-5` artifacts. The seed-extended comparison held. |
| Long-context non-brain control (`contextfeat`) | Separates synthetic-brain specificity from generic context-conditioned teacher-feature effects. | Builder prepared and CPU-smoked only: [`e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py) exactly recovers WikiText row/header context, and [`build_context_feature_target_cache.py`](../scripts/build_context_feature_target_cache.py) writes context-conditioned teacher-feature caches. Full cache/run waits until E016 and textfeat justify it. See [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md). |
| On-policy non-brain control | Separates synthetic-brain specificity from generic teacher supervision on the student's own trajectories. | Not built. This remains a new runner protocol, not a target-cache variant. [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md) records the estimand split. |
| On-policy representation control (`OPRD-lite` / `PHF-lite`) | Separates a brain-derived target from generic on-policy hidden-state or hidden-flow distillation. | Not built and not immediate. After the warning-route Tuckute interpretation, [`top-venue-representation-control-feasibility-2026-07-07.md`](top-venue-representation-control-feasibility-2026-07-07.md) says no representation-control compute is next by default; OPRD/PHF-style controls require a future reopened positive route and a new `/precheck`. |
| Real-brain evaluation | Separates synthetic-target fit from real brain alignment. | Combined seed `0-5` Tuckute diagnostic completed, passed audit, and was interpreted in [`e016-combined-tuckute-interpretation-2026-07-08.md`](e016-combined-tuckute-interpretation-2026-07-08.md). It does not support the brain-specific positive branch. |
| Real-brain robustness rerun | Closes the missing-saved-artifact hole in the Tuckute diagnostic. | Complete. The predeclared seed `0-2` TRIBE artifact-saving rerun finished, Tuckute scoring completed, the combined seed `0-5` analyzer/audit passed, and the warning route held. |

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

The venue-specific readiness matrix is [`top-venue-readiness-matrix-2026-07-07.md`](top-venue-readiness-matrix-2026-07-07.md). The short version is: AAAI is the default route after the combined real-brain gate interpreted as warning/nonpositive; ICML becomes plausible only for a crisp estimand/control paper. ICLR/NeurIPS are not the default because the robust positive route did not open.

| Venue | Best-fit angle | Risk |
|---|---|---|
| ICLR | Representation learning and training-objective question. | Not the default after the real-brain transfer gate failed; would need a broader representation lesson. |
| ICML | Estimation/control protocol for privileged biological targets in distillation. | Needs clean method framing and enough statistical strength. |
| NeurIPS | Brain/AI bridge plus compression and careful controls. | Hard without a positive real-brain transfer result or broader field-correcting negative. |
| AAAI | Robust empirical study with clear negative or bounded positive. | May be less ideal if the final contribution is mainly methodology. |

## Must-not-claim

- Do not claim first brain-guided LLM improvement.
- Do not claim first brain data beyond stimulus text.
- Do not claim first privileged-information distillation for language models.
- Do not claim first hidden-state, representation-space, or hidden-process distillation for language models.
- Do not claim first training-only privileged information improvement for smaller language models.
- Do not claim first context/self-distillation, dense-feedback distillation, or gaze/cognitive supervision for modern LMs/VLMs.
- Do not assume a privileged training signal transfers cleanly to the unprivileged student; recent PI/on-policy distillation work treats leakage, shortcut learning, and degraded transfer as expected failure modes.
- Do not treat `textfeat` as clearing long-context or on-policy distillation; it clears a sentence-local frozen-teacher hidden-state target.
- Do not claim brain-specificity from TRIBE or from TRIBE beating textfeat on synthetic target-R2; the combined Tuckute `/interpret` gate moved against real-brain transfer.
- Do not claim that a positive TRIBE synthetic result is more than a synthetic-endpoint dense privileged-target effect; it beat a sentence-local teacher-hidden-state control on the synthetic endpoint, then failed the real-brain Tuckute transfer gate.
- Do not claim a final submitted-paper result from the Tuckute diagnostic without independent code/stat review if the diagnostic becomes load-bearing.
- Do not use synthetic target-R2 as a substitute for real-brain utility unless explicitly framed as a synthetic-target result.

## Related

- [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md) - source frontier memo
- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md) - combined Tuckute acceptance and route gate
- [`e016-combined-tuckute-interpretation-2026-07-08.md`](e016-combined-tuckute-interpretation-2026-07-08.md) - combined Tuckute verdict and paper-route closeout
- [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md) - source-facing venue/open-question audit
- [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md) - KD/privileged-information adjacency audit
- [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md) - context/self-distillation and gaze/cognitive-supervision adjacency audit
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md) - focused on-policy/context-distillation control burden
- [`top-venue-long-context-control-feasibility-2026-07-03.md`](top-venue-long-context-control-feasibility-2026-07-03.md) - recovered WikiText context metadata for a possible contextfeat control
- [`top-venue-representation-control-feasibility-2026-07-07.md`](top-venue-representation-control-feasibility-2026-07-07.md) - ranks contextfeat versus OPRD/PHF-style controls after the hidden-state distillation literature update
- [`top-venue-readiness-matrix-2026-07-07.md`](top-venue-readiness-matrix-2026-07-07.md) - venue-specific burden map for AAAI, ICML, ICLR, and NeurIPS
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) - claim/readiness ledger
- [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md) - pre-result post-run manifest
- [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) - active Phase-3 experiment
- [`01-research-landscape.md`](01-research-landscape.md) - literature map
- [`ladder.md`](ladder.md) - canonical status board
