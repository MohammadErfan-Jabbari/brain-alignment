---
title: "Top-venue on-policy/context-distillation audit, 2026-07-03"
tags: [reference]
aliases: [top-venue-on-policy-context-distillation-audit-2026-07-03, on-policy-context-distillation-audit]
---

# Top-venue on-policy/context-distillation audit, 2026-07-03

**Status.** This is a `/scout` audit memo, not a canonical paper note, not a report, and not a science verdict. It sharpens the control burden around E016 after a focused search on 2026 on-policy, context, self-, and privileged-information distillation for language models.

## Search method and fallback

The intended Firecrawl Research route was checked first in this session, but no callable Firecrawl tool was exposed in the Codex tool surface. I therefore used live web search over primary or near-primary sources, mostly arXiv pages. Treat this memo as a frontier audit. Any paper that becomes load-bearing in manuscript prose still needs a canonical note.

## Bottom line

On-policy/context/self-distillation for LLMs is now a fast-moving adjacent field, not a niche baseline family. The current `textfeat` control is still necessary because it asks whether TRIBE beats a matched-dimension, sentence-local frozen-LM hidden-state target. But it is not the same as a long-context or on-policy privileged teacher.

That distinction changes only the positive branch. If E016 is null, the paper can still argue that dense synthetic neural targets failed under fixed-budget KD after the local target/statistics confounds were controlled. If E016 is positive and later beats `textfeat`, the paper must still choose one of three honest paths before a top-tier brain-specific claim:

1. add a long-context or on-policy non-brain control,
2. add a real-brain evaluation,
3. narrow the claim to exactly what was cleared: TRIBE beat a sentence-local frozen-teacher hidden-state target under the fixed KD protocol.

Starting a long-context/on-policy control before E016 and `textfeat` justify it would be premature. The active KD corpus is sentence-split; a clean context control would require reconstructing document context or designing a new on-policy teacher/student protocol rather than bolting a context label onto the existing target cache.

## Source matrix

| Source | What it establishes | Pressure on E016 | What remains open for us |
|---|---|---|---|
| [Song and Zheng, 2026, "A Survey of On-Policy Distillation for Large Language Models"](https://arxiv.org/abs/2604.00626) | OPD for LLMs is mature enough to have a dedicated survey organized by feedback signal, teacher access, and loss granularity. | A reviewer can plausibly ask why a positive TRIBE result is not just one more privileged/on-policy distillation effect. | The survey is not about neural targets or biological-vs-nonbiological matched controls under fixed-budget text KD. |
| [Ye et al., 2026, "On-Policy Context Distillation for Language Models"](https://arxiv.org/abs/2602.12275) | OPCD trains on student-generated trajectories while matching a context-conditioned teacher, and reports cross-size distillation plus OOD-preservation benefits. | This is the closest algorithmic comparator to a "privileged context internalized into a smaller student" story. | It uses text/context privileges, not brain targets, and does not compare biological targets with matched non-brain targets. |
| [Zhao et al., 2026, "Self-Distilled Reasoner"](https://arxiv.org/abs/2601.18734) | OPSD lets the same model act as teacher and student under different contexts; the teacher sees privileged reasoning traces or answers while the student sees the question. | Same-model, training-only PI with dense token-level supervision is active. | It targets reasoning/post-training, not synthetic neural supervision for smaller-student KD. |
| [Penaloza et al., 2026, "Privileged Information Distillation for Language Models"](https://arxiv.org/abs/2602.04942) | PI-conditioned teacher/student objectives for agentic environments can transfer action-only privileged information to unconditioned policies. | Generic PI distillation for LMs is not a novelty cell. | Their PI is agentic/action information, not biological or synthetic-brain targets under the E016 compression protocol. |
| [Stein et al., 2026, "GATES"](https://arxiv.org/abs/2602.20574) | A document-conditioned tutor can distill into a document-free student when consensus gates unreliable self-supervision. | Asymmetric context distillation with no test-time context is active. | It is document-grounded QA, not brain-alignment-guided KD, and not a target-specific brain-vs-text control. |
| [Hübotter et al., 2026, "Reinforcement Learning via Self-Distillation"](https://arxiv.org/abs/2601.20802) | SDPO converts rich textual feedback into dense self-distillation signals without an external teacher or reward model. | Dense feedback and token-level self-teaching are crowded ideas. | Feedback is environment/textual, not neural, and the objective is RLVR rather than smaller-student compression. |
| [Ding, 2026, "HDPO"](https://arxiv.org/abs/2603.23871) | Privileged ground-truth-conditioned rollouts can rescue prompts where standard RL gradients vanish. | Privileged self-distillation is becoming a recognizable post-training pattern. | It is same-model reasoning RL, not fixed-budget cross-model KD with biological controls. |
| [Ye et al., 2026, "Online Experiential Learning"](https://arxiv.org/abs/2603.16856) | Deployment trajectories can be converted into experiential knowledge and consolidated through on-policy context distillation. | "Experience/context can be internalized into parameters" is already an active claim family. | It does not test neural targets or the matched-information biological specificity question. |

## Control interpretation

`textfeat` answers one precise reviewer objection: maybe any high-dimensional teacher-hidden-state target would regularize KD as well as TRIBE. It does so by using sentence-local frozen `gpt2-medium` hidden states, projected to the same target dimension and paired with a permuted twin.

It does not answer these distinct objections:

- maybe a long-context teacher would transfer discourse information better than a sentence-local target,
- maybe an on-policy context-conditioned teacher would work because it supervises the student's own trajectories,
- maybe the synthetic target is useful only because it encodes text-derived context rather than brain-like structure,
- maybe a real-brain evaluation is needed because synthetic-target fit does not guarantee biological utility.

So the post-positive burden should be ordered, not expanded blindly:

1. E016 full run must finish and pass the analyzer gate.
2. If positive at matched PPL, run `textfeat`.
3. If TRIBE does not beat `textfeat`, stop the brain-specific claim.
4. If TRIBE beats `textfeat`, decide between extra seeds plus a long-context/on-policy control, extra seeds plus real-brain evaluation, or a deliberately narrowed claim.

## Design note

A clean long-context/on-policy comparator is not just a new target cache over the current sentence list. It needs an estimand:

- **Context-distillation estimand:** does a student internalize teacher predictions conditioned on preceding document context or retrieved context better than it internalizes sentence-local features?
- **On-policy estimand:** does teacher supervision on the student's own generations change the KD frontier differently from off-policy sentence KD?
- **Brain-specificity estimand:** after non-brain context/on-policy privileges are matched, does the neural target add anything?

Those are adjacent but not identical. The current active path should not pay that complexity until E016 and `textfeat` force it.

## Related

- [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md)
- [`top-venue-distillation-adjacency-audit-2026-07-03.md`](top-venue-distillation-adjacency-audit-2026-07-03.md)
- [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
