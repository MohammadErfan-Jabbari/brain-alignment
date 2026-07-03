---
title: "Top-venue open-question audit, 2026-07-03"
tags: [reference]
aliases: [top-venue-open-question-audit-2026-07-03, venue-open-question-audit]
---

# Top-venue open-question audit, 2026-07-03

**Status.** This is a `/scout` + `/plan` audit memo, not a literature canonical note, not a report, and not a science verdict. It updates the source-facing burden of proof for the active AAAI/ICML/ICLR/NeurIPS paper goal while the E016 full run trains.

## Search method and fallback

The intended Firecrawl Research route was checked first, but no `firecrawl` CLI/MCP tool was exposed in this Codex tool surface. I therefore used live web search over primary or near-primary sources: arXiv, OpenReview, AAAI OJS, NeurIPS proceedings, ACL Anthology/CoNLL, and public project pages. Treat this as a fresh frontier audit, not a paper digest. Papers that become load-bearing should still get canonical notes through the normal digest route.

## Bottom line

The live search strengthens the S51 conclusion: the broad novelty cells are crowded or closed, but **fixed-student-budget brain-alignment-guided distillation/compression remains open** in the sources checked.

The field has now covered measurement, attribution, multilingual alignment, brain-informed training, speech-model brain-tuning, brain-vs-stimulus comparisons, and reasoning-time/fine-tuning brain guidance. I did not find a primary-source paper that tests the exact deployment-relevant cell we can still contribute: **KD-only smaller student vs brain-guided KD under matched PPL/utility, with a permuted target and a matched-information non-brain privileged target.**

The follow-up privileged-signal and on-policy/context-distillation audits add one more boundary: context/self-distillation, on-policy teacher supervision, rich-feedback distillation, and gaze/cognitive supervision are active too. So the contribution cannot be "privileged or cognitive signal helps a model"; it must be the controlled biological/synthetic-neural target comparison under fixed-budget text-KD.

## Venue/open-question matrix

| Venue/source cell | Fresh source pressure | What it closes | What remains open for us |
|---|---|---|---|
| AAAI 2026 measurement | [Lei et al., "Do Large Language Models Think like the Brain?"](https://ojs.aaai.org/index.php/AAAI/article/view/37022) compares layer-wise LLM embeddings and fMRI at sentence level. | Brain-LLM layerwise measurement is no longer a novelty angle. | No training intervention, no KD student, no matched-budget control. |
| ICLR 2026 brain-informed training | [Bilgin et al., OpenReview](https://openreview.net/forum?id=07S1CPoQYP) is explicitly "Brain-Informed Language Model Training..." | Text-LM brain-informed training itself is not ours as a generic claim. | Need compression/KD, matched PPL, permuted and matched-information controls. |
| ICLR 2026 measurement/readout | [The Mind's Transformer, OpenReview](https://openreview.net/forum?id=PgIlCCNxdB) and public author pages place measurement inside transformer state structure. | Alignment readout choice is a live reviewer concern. | Does not test whether neural supervision helps a smaller student. |
| ICML 2026 mechanism/measurement | [Cheng et al., arXiv:2602.04081](https://arxiv.org/abs/2602.04081) links abstraction/intrinsic dimension to brain alignment; the arXiv record carries `Journal-ref: ICML 2026`. | Mechanistic explanations of why middle layers align are active. | It informs target/readout interpretation, not fixed-budget distillation. |
| ICML-facing attribution | [Proietti et al., arXiv:2510.12355](https://arxiv.org/abs/2510.12355) and [OpenReview](https://openreview.net/forum?id=8JgaMrEw52) analyze which input words drive brain-LLM alignment; an author post reports ICML 2026 acceptance, but I did not find an official proceedings page in this audit. | Attribution and BA-vs-NWP feature reliance are crowded. | It does not train or compress models. |
| NeurIPS 2025 brain-tuning | [Moussa and Toneva, arXiv:2510.21520](https://arxiv.org/abs/2510.21520), [NeurIPS/OpenReview](https://openreview.net/forum?id=4jgsUhWWaF), and the NeurIPS PDF report multi-participant speech brain-tuning. | Brain-tuning can improve generalizability/efficiency in speech-model settings. | No fixed smaller text student and no KD-only compression frontier. |
| NeurIPS 2025 multilingual brain tuning | [Negi et al., OpenReview](https://openreview.net/forum?id=JPogehP8By) covers brain-informed fine-tuning for multilingual understanding. | Broad "brain-informed fine-tuning improves downstream tasks" is not novel. | Missing matched-PPL/matched-information compression controls remain the opening. |
| CoNLL 2026 brain-vs-stimulus | [Merlin et al., OpenReview](https://openreview.net/forum?id=DnBd2X3G5Y) and the [CoNLL 2026 program](https://conll.org/) cover "What Brain Data Adds to Language Model Training." | Brain data beyond stimulus text has been directly tested for text-LM fine-tuning. | It does not test KD-only smaller students or fixed-budget compression. |
| ACL 2026 ECoG tuning | [Zhang et al., ACL Anthology](https://aclanthology.org/2026.acl-long.1911/) introduces ECoG-tuning with millisecond neural signals. | Speech brain-tuning and temporal precision are credible positive branches. | It is modality/data pivot work, not our immediate text-KD compression cell. |
| arXiv 2026 brain-guided reasoning | [Xiao et al., arXiv:2606.11893](https://arxiv.org/abs/2606.11893) reports fMRI-derived directions improving reasoning. | Broad "brain signals can guide LLM behavior" is no longer safe as a novelty claim. | No compression, no KD-only student, no matched-information privileged-target control. |
| arXiv 2026 multilingual alignment | [Guo et al., arXiv:2605.23032](https://arxiv.org/abs/2605.23032) links cross-lingual brain-LLM alignment to training-language dominance and typology. | Measurement generalization across languages is active and data-rich. | It is a measurement/frontier-pressure paper, not an intervention or compression result. |

## What this changes

The paper pitch must be even narrower than "brain data helps language models." The defensible contribution is one of:

1. **Controlled-negative compression paper:** dense synthetic neural targets do not improve fixed-budget KD after scarcity, target-averaging, PPL, and dense-target-statistics confounds are controlled.
2. **Dense privileged-target paper:** if TRIBE and text-feature targets both help similarly, the finding is about privileged target geometry under KD, not brain specificity.
3. **Brain-specific compression paper:** only if TRIBE beats KD, TRIBE-permuted, textfeat, and textfeat-permuted under matched PPL, and then likely with extra seeds or real-brain evaluation.

The active E016 path is still the right next experiment because it is the first repo-native test that removes the biggest reviewer objection to the current null spine: "maybe fMRI scarcity/noise hid the effect."

## Immediate implications for E016

- A TRIBE-only positive is not enough; the text-feature control is non-optional after the current frontier check.
- A TRIBE positive that only beats KD/permuted targets is still vulnerable to a generic privileged-target/context-distillation interpretation; if it beats textfeat, the likely next reviewer demand is extra seeds plus either a stronger non-brain privileged-target control or real-brain evaluation.
- A null is still publishable only if the analyzer gate is complete and the paired seed-level audit survives `/interpret`.
- A positive branch must be described as synthetic-target compression until the matched-information control and extra inference strength are in hand.
- The final paper introduction should concede generic brain-guided LLM utility as prior work, then move straight to the smaller-student/KD deployment question.

## Gaps to revisit before submission

- Re-run this audit near submission, especially over official ICML 2026 proceedings once available.
- Digest [Guo et al., 2026](https://arxiv.org/abs/2605.23032) if cross-lingual alignment becomes part of the motivation or limitations.
- Digest [Cheng et al., 2026](https://arxiv.org/abs/2602.04081) if intrinsic dimension or readout-state choice becomes part of the method defense.
- Use primary proceedings pages, not author social posts, for any venue-placement claim in the manuscript.

## Related

- [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`top-venue-privileged-signal-adjacency-audit-2026-07-03.md`](top-venue-privileged-signal-adjacency-audit-2026-07-03.md)
- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
