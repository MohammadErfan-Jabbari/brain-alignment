---
title: "Top-venue distillation adjacency audit, 2026-07-03"
tags: [reference]
aliases: [top-venue-distillation-adjacency-audit-2026-07-03, distillation-adjacency-audit]
---

# Top-venue distillation adjacency audit, 2026-07-03

**Status.** This is a `/scout` audit memo, not a canonical paper note, not a report, and not a science verdict. It checks the nearest LLM-distillation and privileged-information literature around the active E016 paper cell while the full E016 run trains. Firecrawl Research was the intended paper-retrieval route, but no Firecrawl MCP/CLI tool was exposed in this Codex surface; sources below were checked through live web search over primary pages where possible.

## Bottom line

The narrower literature check strengthens, but also narrows, the paper claim. **LLM distillation is crowded, feature-level distillation is crowded, and generic privileged-information distillation for language models is now active.** The open cell is therefore not "privileged information improves LMs" or "feature targets help KD." The defensible cell is:

> Under a fixed smaller-student KD budget, does a synthetic brain-alignment target improve the alignment/utility frontier beyond KD-only, a permuted dense-target twin, and a matched-information non-brain privileged target?

This makes the prepared `textfeat` control more central, not optional. If TRIBE and text-feature targets both help, the contribution is a dense privileged-target/control result rather than brain specificity.

## Adjacent-source matrix

| Source | What it establishes | Pressure on our claim | Remaining open cell |
|---|---|---|---|
| [Lopez-Paz et al., 2016, "Unifying distillation and privileged information"](https://arxiv.org/abs/1511.03643) | Generalized distillation unifies distillation and privileged information; the arXiv record lists ICLR 2016. | We cannot claim to introduce privileged-information distillation as a concept. | Biological/synthetic-brain privileged targets under modern LLM KD remain untested here. |
| [MiniLLM, ICLR 2024 / arXiv:2306.08543](https://arxiv.org/abs/2306.08543) | On-policy/reverse-KL style KD compresses generative LLMs into smaller students; the arXiv record says it was published at ICLR 2024. | "LLM KD under smaller-student budget" is not novel. | No brain/neural target, no matched-information biological-control question. |
| [Huang et al., NeurIPS 2023, "Feature Correlation Distillation"](https://proceedings.neurips.cc/paper_files/paper/2023/hash/34260a400e39a802961470b3d3de99cc-Abstract-Conference.html) | Feature-level relation/correlation distillation is a top-venue PLM-compression method. | Feature matching as a KD idea is not novel, and reviewers may compare TRIBE target fitting to feature KD. | Does not use neural targets or ask whether a biological target adds anything beyond language-model features. |
| [Saadi and Wang, 2025/2026, "What Should Feature Distillation Transfer in LLMs?"](https://arxiv.org/abs/2507.10155) | Modern feature KD asks which teacher hidden-state directions are functionally relevant, especially under teacher-student dimension mismatch. | Our target-control comparison must distinguish "useful dense target geometry" from "brain-specific signal." | No brain data; no matched biological-vs-nonbiological privileged target. |
| [Hsieh et al., ACL Findings 2023, "Distilling Step-by-Step"](https://aclanthology.org/2023.findings-acl.507/) | Rationales serve as extra supervision for smaller models with less training data. | Extra training-time side information for small students is already a known recipe. | Rationales are language-derived; no neural target and no brain-specificity control. |
| [Penaloza et al., 2026, "Privileged Information Distillation for Language Models"](https://arxiv.org/abs/2602.04942) | PI distillation for language models is now explicit, with PI-conditioned teacher/student objectives for agentic environments. | We must not claim the first PI-distillation-for-LMs paper. | Their PI is action/agentic information, not synthetic brain alignment, and not the fixed-KD compression protocol here. |
| [Oota et al., 2026, "from small to compressed language models"](literature/canonical/oota-2026_brain-encoding-scale-compression.md) | Brain alignment can survive quantization/pruning; KD is explicitly absent in our canonical read. | "Compression destroys brain alignment by default" is too broad. | Whether KD-trained students preserve or gain brain alignment, and whether a brain target helps KD, remains open. |

## Claim update

The paper pitch should be:

1. **Not novel:** KD for LLM compression; feature-level KD; distillation with privileged information; measuring brain alignment of compressed models.
2. **Potentially novel:** a controlled biological/synthetic-brain privileged target in fixed-budget LLM distillation, with matched-PPL/utility, permuted-target, and matched-information non-brain controls.
3. **Most reviewer-facing risk:** any positive TRIBE effect can be reinterpreted as dense privileged-target regularization unless it beats `textfeat` under the same gate.

## Design implications

- E016's three-arm TRIBE run is necessary but not sufficient for a brain-specific positive.
- The text-feature matched-information control becomes mandatory for any positive branch.
- The controlled-null branch remains credible if E016 is null: it would say that even a dense synthetic neural target does not improve fixed-budget KD after removing scarcity and target-statistics excuses.
- If E016 is positive but textfeat is equally positive, the paper should pivot to "privileged target geometry in KD" and explicitly avoid a brain-specific claim.

## Follow-up digest queue

- Full canonical digest for [Penaloza et al., 2026](https://arxiv.org/abs/2602.04942) if the E016 positive branch survives; it is the closest generic PI-distillation threat.
- Full canonical digest for [Saadi and Wang, 2025/2026](https://arxiv.org/abs/2507.10155) if reviewers push the feature-KD interpretation.
- No immediate digest needed for MiniLLM/FCD unless the methods section foregrounds KD baselines beyond KD-only/logit KD.

## Related

- [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
