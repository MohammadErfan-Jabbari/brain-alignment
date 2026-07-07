---
title: "Top-venue literature refresh, 2026-07-07"
tags: [scout, plan, E016, literature, top-venue]
aliases: [top-venue-literature-refresh-2026-07-07, E016-literature-refresh]
---

# Top-venue literature refresh, 2026-07-07

**Status.** This is a scout/plan artifact written while the E016 seed `0-2` real-brain rerun is active. It is not a canonical paper digest, not a report, and not a science verdict. It records what the live literature search implies for the paper route.

## Search Scope

Firecrawl Research searches were run with four framings:

- brain data / brain-tuning for language-model training;
- cognitive signals and knowledge distillation / privileged information;
- learning using privileged information and on-policy/self-distillation;
- brain-alignment confounds, model-quality controls, and prediction-score critique.

Follow-up related-paper expansion used anchors from brain-tuning, brain-misalignment, and severe-control/claim-strength critiques. A later targeted conference/proceedings pass checked the most dangerous overlap: brain data as a training signal in accepted top-venue work.

## Updated Frontier

| Area | Representative papers surfaced | What they make harder | What remains open for us |
|---|---|---|---|
| Brain-tuning / brain data as a training signal | [Schwartz et al. 2019](https://arxiv.org/abs/1911.03268); [Oota/Proietti et al. 2024](https://arxiv.org/abs/2410.09230); [Negi/Oota et al. 2025](https://doi.org/10.1101/2025.07.07.662360); [Merlin & Toneva 2026](https://arxiv.org/abs/2603.23091); [brain-tuning speech generalization 2026](https://arxiv.org/abs/2510.21520) | A broad "brain data can improve model representations or downstream behavior" claim is no longer ours. Brain-tuning papers already use random/permuted brain targets, brain-preserving controls, stimulus/text-model controls, or multilingual downstream evaluation. | Smaller-student KD/compression under matched budget/perplexity, with text-feature controls and real-brain transfer, is still a thinner cell. |
| Prediction-score and alignment robustness critiques | [L-PACT, 2026](https://arxiv.org/abs/2605.14025); [Illusions of Alignment, 2025](https://doi.org/10.1101/2025.03.09.642245); [What are LLMs mapping to in the brain?, 2024](https://arxiv.org/abs/2406.01538) | A positive neural prediction score is not enough for a top-tier brain-specific claim. The frontier now expects nuisance/severe controls, reliability bounds, relational or mechanism-specific tests, and explicit claim-strength separation. | Our matched-PPL/permuted/textfeat/real-brain-transfer ladder is valuable as a claim-strength protocol, especially if it exposes a synthetic-target positive that fails real-brain transfer. |
| Privileged-information distillation for LMs | [Privileged Information Distillation for Language Models, 2026](https://arxiv.org/abs/2602.04942); [AVSD, 2026](https://arxiv.org/abs/2605.20643); [PRIDE, 2026](https://arxiv.org/abs/2606.23124); [Rethinking On-Policy Self-Distillation for Thinking Models, 2026](https://arxiv.org/abs/2607.05184); [DemoPSD, 2026](https://arxiv.org/abs/2607.02502) | Privileged-information KD/on-policy distillation is now an active LLM area; novelty cannot be "distillation with training-time extra signal." The July 2026 PI papers also make transfer failure and privileged-information leakage first-class reviewer concerns. | These papers use model traces, tool calls, hints, answers, solution contexts, or domain demonstrations, not real or synthetic brain targets. They leave open whether neural/cognitive PI transfers to a smaller LM without becoming a text-feature proxy or a non-transferable shortcut. |
| Cognitive-signal integration reviews and adjacent signals | [Integrating Cognitive Processing Signals into Language Models, 2025](https://arxiv.org/abs/2504.06843); EEG/eye-tracking reading embeddings ([2024](https://arxiv.org/abs/2401.15681)) | "Use cognitive signals in NLP" is broad and reviewed; the paper cannot present the existence of this direction as new. | The rigorous negative/positive protocol for whether such signals survive matched controls in LM training remains publishable. |
| Model scale/compression and brain encoding | [Linguistic properties and model scale in brain encoding, 2026](https://arxiv.org/abs/2602.07547); [Scaling laws for fMRI encoding, 2023](https://arxiv.org/abs/2305.11863) | Brain alignment tracks model quality/scale in known ways; model-quality confounding is a central threat, not an afterthought. | This supports making matched perplexity/budget and text-feature controls a headline methodological contribution. |

## Verified Constraints

- Brain-tuning speech work optimizes an fMRI reconstruction objective and compares against random/permuted fMRI, BigSLM targets, stimulus tuning, and text-LM tuning. It does not test the smaller-student KD setting or matched-perplexity compression claim we are probing.
- Negi/Oota et al.'s multilingual brain-informed fine-tuning is a direct top-venue pressure point: it fine-tunes monolingual and multilingual LMs with bilingual fMRI and evaluates brain encoding plus downstream multilingual transfer, including a block-permuted brain-response control. This makes a broad "brain-informed LM fine-tuning improves downstream NLP" claim unavailable. It still does not test smaller-student KD/compression, matched-PPL student budgets, or matched non-brain privileged targets.
- Privileged Information Distillation for Language Models frames the transfer problem cleanly: training-time PI can help a teacher, but the hard question is whether the unconditioned student retains the capability at test time. Its PI sources are frontier-model trajectories/tool calls/hints, not brain or cognitive measurements.
- L-PACT explicitly separates weak predictive evidence from stronger alignment claims and treats severe controls as necessary. This is directly aligned with our caution that E016 synthetic target-R2 does not by itself imply brain-specific utility.
- Merlin & Toneva's brain-misalignment paper is a direct functional-consequence neighbor: it asks whether changing brain alignment changes linguistic competence. That makes our real-brain transfer diagnostic more important, because a synthetic-target-only result would otherwise be too easy to overread.
- Oota et al.'s scale/compression paper studies SLM scale, quantization, and pruning effects on brain encoding, and names knowledge distillation as future work. That leaves the training-time KD intervention open, but it also means a KD paper must explain why distillation is not just another compression method in the Oota taxonomy.

## Paper Route Implication

The top-venue contribution should not be framed as "brain data improves language models" or "privileged-information distillation works." Both are now occupied broad claims, and the former has direct NeurIPS-level pressure from brain-informed fine-tuning work.

The strongest open cell is narrower and more defensible:

> Does a brain-derived privileged target transfer useful information to a smaller language-model student beyond matched text-feature and permuted-target controls, and does that transfer survive evaluation on real brain alignment rather than only on the training proxy?

This yields two possible paper routes after the active rerun:

| E016 real-brain seed `0-5` outcome | Best paper route | Venue burden |
|---|---|---|
| Real-brain TRIBE-minus-textfeat remains nonpositive or mixed | Methodological/control paper: synthetic neural targets can produce a large synthetic-endpoint gain over textfeat, but the gain fails real-brain transfer; propose matched-PPL + textfeat + real-brain-transfer as a necessary evaluation ladder for neural/cognitive PI distillation. | Needs a clean `/interpret` audit, possibly context/on-policy non-brain controls if claiming brain specificity is ruled out rather than merely unsupported. This is likely a strong workshop / possible AAAI-style methodology paper, less likely ICML/ICLR/NeurIPS unless the control failure is generalized. |
| Real-brain TRIBE-minus-textfeat becomes positive and robust | Positive brain-privileged KD paper: first evidence that a synthetic brain target can improve a smaller LM's real-brain alignment beyond sentence-local teacher-hidden-state supervision under matched budget. | Needs independent implementation/stat audit, stronger non-brain/context/on-policy controls, and likely an external dataset or endpoint. This is the only plausible ICML/ICLR/NeurIPS route from E016. |

## Immediate Action

Do not widen compute while the rerun is active. The next decisive evidence is already running:

1. Finish TRIBE seed `0-2` artifact-saving rerun.
2. Score the rerun on Tuckute.
3. Run `scripts/e016_analyze_tuckute_alignment.py` over TRIBE seed `0-5` and textfeat seed `0-5`.
4. Apply [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md), then route the result through `/interpret` before narrowing or reopening the paper claim.

## Limited Follow-Up, 2026-07-07 21:59 UTC

Firecrawl Research semantic paper search was still not exposed in the Codex tool surface, and no local `firecrawl` CLI was present, so this follow-up used a small primary-source web fallback over arXiv, NeurIPS proceedings, and AAAI OJS. Treat it as a narrow pressure check, not a replacement for a canonical paper digest.

Newly checked conference pressure:

- AAAI-26 includes ["Do Large Language Models Think Like the Brain? Sentence-Level Evidences from Layer-Wise Embeddings and fMRI"](https://ojs.aaai.org/index.php/AAAI/article/view/37022/40984). It compares layer-wise embeddings from 14 LLMs against sentence-level fMRI responses and reports that model performance/instruction tuning relates to neural alignment. This reinforces that "LLM-brain alignment as an evaluation/comparison object" is now mainstream enough for AAAI; it does not occupy the training-time brain/cognitive privileged-target KD cell.

Rechecked adjacent pressure points:

- NeurIPS 2025 ["Brain-tuning Improves Generalizability and Efficiency of Brain Alignment in Speech Models"](https://proceedings.neurips.cc/paper_files/paper/2025/file/b0dfbc465fa47c7c31cbfc0f454df460-Paper-Conference.pdf) remains the strongest top-venue brain-training neighbor. It fine-tunes speech models to predict fMRI across participants and reports improved alignment/efficiency/generalization. It pressures broad "brain data improves models" claims, but still differs from fixed-student LLM KD with matched text-feature and real-brain-transfer controls.
- Oota et al. 2026 ["Linguistic properties and model scale in brain encoding"](https://arxiv.org/abs/2602.07547) keeps pressure on any scale/compression framing: the abstract reports brain predictivity saturation around 3B models and robustness to most compression methods. This supports our need to frame E016 as a training-intervention/control question, not as generic compression-neuroscience.
- Jia 2026 ["Do Language Models Align with Brains? Prediction Scores Are Not Enough"](https://arxiv.org/abs/2605.14025) strengthens the severe-control burden: prediction scores alone are insufficient, and many apparent positives can become control-explained. This aligns with our current refusal to infer brain-specific utility from synthetic target-R2.
- Penaloza et al. 2026 ["Privileged Information Distillation for Language Models"](https://arxiv.org/abs/2602.04942) keeps the PI-distillation neighbor live: training-time PI transfer to an unconditioned student is the right abstract problem, but their PI sources are agentic trajectories/actions, not brain/cognitive targets.

Net update: the narrow open cell is unchanged, but the AAAI-26 paper raises the bar for any venue framing that sounds like "LLM representations align with fMRI." The paper route should keep foregrounding the intervention question: whether a brain-derived privileged target changes a smaller KD student's behavior beyond matched non-brain targets and whether that survives real-brain transfer.

## Firecrawl Research Follow-Up, 2026-07-07 22:06 UTC

Firecrawl Research became available in the Codex tool surface during this continuation. A focused semantic search and related-paper expansion rechecked four pressure points: brain-derived PI/KD, brain-tuning, cognitive-signal PI, and severe-control brain-alignment critiques.

New PI-distillation pressure:

- [Rethinking On-Policy Self-Distillation for Thinking Models](https://arxiv.org/abs/2607.05184) was created on 2026-07-06 and updated on 2026-07-07. It reports that privileged-context distillation can degrade stronger thinking models, especially on long reasoning traces, because privileged teacher context reshapes token-level learning around high-entropy branching points. This is not about brain or cognitive signals, but it makes "privileged signal transfers cleanly" a claim reviewers will not grant for free.
- [DemoPSD: Disagreement-Modulated Policy Self-Distillation](https://arxiv.org/abs/2607.02502) was created on 2026-07-02 and updated on 2026-07-07. It explicitly frames privileged-information leakage as a failure mode where a student internalizes answer-dependent shortcuts unavailable at test time, then proposes a disagreement-weighted distillation target. Its experiments are on scientific reasoning and OOD GPQA-style generalization, not neural/cognitive targets.
- Re-reading [Privileged Information Distillation for Language Models](https://arxiv.org/abs/2602.04942) confirmed that its PI sources are frontier-model tool calls and arguments, tool-call names, and self-generated hints from successful trajectories. It does not study fMRI, EEG, eye tracking, or brain-derived cognitive measurements.

Brain-alignment control pressure:

- Firecrawl expansion from [Brain-tuning Improves Generalizability and Efficiency of Brain Alignment in Speech Models](https://arxiv.org/abs/2510.21520) re-surfaced speech/audio brain-tuning neighbors and confirmed the strongest overlap remains fMRI-supervised tuning of speech encoders, not smaller-student LLM KD.
- Re-reading [Do Language Models Align with Brains? Prediction Scores Are Not Enough](https://arxiv.org/abs/2605.14025) reinforced the severe-control standard: prediction-score positives should not be promoted to alignment claims unless they survive nuisance/severe controls, relational evidence, mechanism-stripping, reliability bounds, and replication gates.

Net update: the open cell is still not occupied, but its best framing shifts slightly. The negative/mixed E016 branch should be written, if it holds, as a **privileged-target transfer failure under strict controls**, not just as a brain-KD null. The positive branch, if reopened by the active real-brain rerun, must show not only TRIBE greater than textfeat on the synthetic endpoint but also that the privileged brain-derived target does not behave like the leakage/shortcut failure mode now foregrounded in the July PI-distillation literature.

## Firecrawl Research Follow-Up, 2026-07-07 22:20 UTC

A second focused Firecrawl Research pass checked the newer hidden-state/representation-distillation frontier against the brain-derived target cell. This matters because E016 uses a dense middle-layer target; novelty cannot rest on "hidden representations are better distillation targets" if the distillation literature already owns that move.

New close pressure:

- [Beyond representational alignment with brain-guided language models for robust reasoning](https://arxiv.org/abs/2606.11893) is now the closest brain-guided LLM training neighbor. It uses task-fMRI from deductive reasoning to derive neural activation guided representation intervention/fine-tuning, including mid-layer attention-module LoRA and a combined CE plus neural-similarity objective. It closes any broad "first brain-guided LLM improvement" framing. It does not test fixed-budget smaller-student KD, matched non-brain teacher-feature targets, or real-brain transfer after synthetic target training.
- [OPRD: On-Policy Representation Distillation](https://arxiv.org/abs/2606.06021) moves OPD supervision from output distributions into hidden-state MSE on student rollouts, with a cross-architecture bridge. It makes "representation-level distillation" a crowded algorithmic claim and names cross-modal distillation as future work. It does not use brain/fMRI/cognitive targets.
- [PHF: Privileged Hidden Flow for On-Policy Self-Distillation](https://arxiv.org/abs/2606.29340) adds privileged hidden-transition/trajectory-geometry supervision to OPSD. It strengthens the point that hidden-process targets are active in privileged distillation. It still uses model-internal privileged teachers conditioned on reference solutions, not external neural measurements.
- Re-reading [Inducing brain-relevant bias in natural language processing models](https://arxiv.org/abs/1911.03268) confirms that brain-supervised BERT fine-tuning has been known since 2019, including MEG/fMRI prediction heads and downstream NLP non-degradation checks. This remains a precursor, not a fixed-budget generative-LM KD result.

Net update: the open cell narrows again. A positive E016 route must be framed as **brain-derived privileged targets under controlled fixed-student KD**, not as hidden-state distillation, representation distillation, or brain-guided LLM improvement in general. A negative/mixed route becomes cleaner: it can say that a synthetic brain target can look strong against sentence-local hidden-state controls on the training proxy yet fail the real-brain transfer gate, under a protocol designed precisely because hidden-state and privileged-distillation baselines are now strong.

## Related

- [`top-venue-claim-scope-review-2026-07-07.md`](top-venue-claim-scope-review-2026-07-07.md)
- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
