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
| Privileged-information distillation for LMs | [Privileged Information Distillation for Language Models, 2026](https://arxiv.org/abs/2602.04942); [AVSD, 2026](https://arxiv.org/abs/2605.20643); [PRIDE, 2026](https://arxiv.org/abs/2606.23124) | Privileged-information KD/on-policy distillation is now an active LLM area; novelty cannot be "distillation with training-time extra signal." | These papers use model traces, tool calls, hints, answers, empathy context, or multimodal privileged views, not real or synthetic brain targets. They leave open whether neural/cognitive PI transfers to a smaller LM without becoming a text-feature proxy. |
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

## Related

- [`top-venue-claim-scope-review-2026-07-07.md`](top-venue-claim-scope-review-2026-07-07.md)
- [`e016-combined-tuckute-interpretation-gate-2026-07-07.md`](e016-combined-tuckute-interpretation-gate-2026-07-07.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
