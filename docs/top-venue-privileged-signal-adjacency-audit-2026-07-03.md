---
title: "Top-venue privileged-signal adjacency audit, 2026-07-03"
tags: [reference]
aliases: [top-venue-privileged-signal-adjacency-audit-2026-07-03, privileged-signal-adjacency-audit]
---

# Top-venue privileged-signal adjacency audit, 2026-07-03

**Status.** This is a `/scout` audit memo, not a canonical paper note, not a report, and not a science verdict. It checks whether adjacent work on context/self-distillation, privileged information, and gaze/cognitive supervision changes the active E016 paper cell while the full run trains. A focused follow-up on the on-policy/context-distillation control burden is [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md).

## Search method and fallback

The intended Firecrawl Research route was checked first, but no `firecrawl` CLI/MCP tool was exposed in this Codex tool surface. I therefore used live web search over primary or near-primary sources: arXiv, ACL Anthology, OpenReview search snippets where the page itself was browser-gated, and public paper/project pages. Treat this as a frontier audit; any paper that becomes load-bearing in manuscript prose should still receive a canonical note.

## Bottom line

The adjacent literature has widened fast enough that the paper must avoid a second overbroad claim: **training-time privileged signals, context, feedback, and gaze can already improve LMs or VLMs in several settings.** The open cell is not "privileged information helps language models" or "human gaze/cognition can supervise models." The open cell is narrower:

> Under a fixed smaller-student text-KD budget, does a synthetic brain-alignment target add anything beyond KD-only, a permuted dense target, and a matched-information non-brain privileged target?

This does not invalidate E016. It makes the matched-information control and branch-specific framing even more central. A TRIBE-only positive is not a brain-specific result; it is at most a dense privileged-target result until it beats non-brain controls.

## Adjacent-source matrix

| Source | What it establishes | Pressure on our claim | Remaining open cell |
|---|---|---|---|
| [Zhao et al., 2026, "Self-Distilled Reasoner"](https://arxiv.org/abs/2601.18734) | On-policy self-distillation lets one model act as teacher/student under different information contexts; the teacher sees privileged reasoning traces or answers, and the student sees only the question. | Privileged self-teaching for LLM reasoning is active; do not claim same-model or train-only privileged distillation novelty. | Reasoning/post-training, not neural targets, not fixed-budget brain-alignment KD, and not a biological-vs-nonbiological privileged-target comparison. |
| [Hübotter et al., 2026, "Reinforcement Learning via Self-Distillation"](https://arxiv.org/abs/2601.20802) | Rich feedback can be converted into dense token-level self-distillation without an external teacher or reward model. | "Dense feedback improves sample efficiency" is crowded. | The feedback is environment/textual, not brain/neural, and the task is RLVR rather than compression of a smaller text student. |
| [Ye et al., 2026, "On-Policy Context Distillation for Language Models"](https://arxiv.org/abs/2602.12275) | A context-conditioned teacher can be distilled into a context-free model on the student's own trajectories; the abstract reports cross-size distillation and OOD-preservation benefits. | Context distillation is the closest algorithmic pressure: a reviewer can ask whether any privileged context/feature target would work. | Does not compare biological/neural targets against matched non-brain targets; does not test brain alignment; does not answer fixed-student KD under matched PPL. |
| [Ding, 2026, "HDPO"](https://arxiv.org/abs/2603.23871) | Privileged self-distillation targets "cliff" prompts where RL gradients vanish by giving the same model ground-truth information. | Ground-truth-conditioned privileged distillation is now a recognizable training pattern, not an exotic idea. | It is same-model reasoning RL, not cross-model student compression and not a neural privileged target. |
| [Pani and Yang, 2025/2026, "Gaze-VLM"](https://arxiv.org/abs/2510.21356) | Gaze can regularize VLM attention for egocentric understanding. A public repository describes it as a NeurIPS 2025 paper, but this audit only relies on the arXiv record. | Gaze-as-supervision for multimodal models is active; do not claim cognitive/gaze supervision novelty. | VLM attention/egocentric vision, not text-LM KD, not brain alignment, and not train-only neural targets for smaller language students. |
| [Zhang et al., 2026, "Thinking with Gaze"](https://arxiv.org/abs/2603.06697) | Sequential radiologist gaze supervises dedicated visual evidence tokens in medical VLMs and reports in-domain/OOD gains. | Strong evidence that gaze can be useful supervision when it is task-causal and high-SNR. | Medical VLM visual search is not natural-language KD; it does not test whether text fMRI-like targets add beyond text features. |
| [EACL 2026, "Controlling Reading Ease with Gaze-Guided Text Generation"](https://aclanthology.org/2026.eacl-long.107/) | A gaze-prediction model can steer generated text toward desired reading behavior, with human eye-tracking evaluation. | Gaze is a live controllable-objective signal in NLP-adjacent generation. | It is generation control via predicted gaze, not train-only supervision improving a smaller student's task or brain alignment. |
| [Deng et al., 2024](literature/canonical/deng-2024_gaze-supervised-finetuning.md) | Synthetic scanpath supervision can help BERT/RoBERTa on low-resource GLUE, but the canonical note shows the gaze-order-specific increment is small and untested. | Low-resource gaze-supervised text fine-tuning is already published. | Encoder GLUE fine-tuning, no LLM KD, no matched-information target-control battery, and no neural/brain target. |
| [E024](experiments/E024_zuco-lupi-sample-efficiency.md) | In this repo, ZuCo normal-reading gaze is reliable but orthogonal to the relation-label task; task-directed gaze carries relation information and is therefore a leak. | Our own cognitive-PI path already produced a controlled negative for one text task. | Does not answer E016's synthetic fMRI-like target under KD; it does warn that reliable privileged signals can be non-portable or label-leaky. |

## Claim update

The paper pitch should now be fenced at three levels:

1. **Not novel:** train-only privileged information for LMs; context distillation; on-policy/self-distillation; dense feedback improving reasoning/post-training; gaze as supervision for VLMs or low-resource encoder fine-tuning.
2. **Still open:** a controlled biological/synthetic-neural privileged target under fixed-budget text-LM KD, with matched-PPL/utility, permuted-target, and matched-information non-brain controls.
3. **Most dangerous reviewer reinterpretation:** a positive TRIBE result may be just another privileged-context/dense-target effect. The text-feature control is the minimum answer and should be named precisely: sentence-local frozen-LM hidden-state supervision, not long-context or on-policy distillation. A top-tier positive may also need an on-policy/context-distillation baseline or a real-brain evaluation, depending on the analyzer branch.

## Design implications for E016

- Do not add any new GPU job while the active full E016 run is alive.
- If E016 is null, this audit strengthens the controlled-negative branch: adjacent PI/gaze methods can work elsewhere, so a null says something specific about synthetic brain-alignment targets under fixed text-KD controls.
- If E016 is positive before textfeat, call it a TRIBE-target effect only.
- If TRIBE and textfeat both help similarly, frame the paper as privileged target geometry under KD, not brain specificity.
- If TRIBE beats textfeat, the next burden is not only extra seeds; it is also explaining why the effect is not a generic on-policy/context-distillation artifact. The prepared textfeat arm covers a teacher-hidden-state baseline; the unresolved follow-up is long-context/on-policy distillation or real-brain evaluation.

## Follow-up digest queue

- Full canonical notes for OPCD/OPSD/SDPO/HDPO are only needed if the E016 positive branch survives, because they would then shape the methods/comparison section.
- Full canonical notes for Gaze-VLM/Thinking-with-Gaze are only needed if we revive a cognitive/gaze-supervision route; for the current E016 paper they are boundary-setting sources.
- The active manuscript should cite the already canonical [Deng et al., 2024](literature/canonical/deng-2024_gaze-supervised-finetuning.md) and [E024](experiments/E024_zuco-lupi-sample-efficiency.md) only if it discusses the abandoned cognitive-PI branch.

## Related

- [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md)
- [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md)
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
- [`experiments/E024_zuco-lupi-sample-efficiency.md`](experiments/E024_zuco-lupi-sample-efficiency.md)
