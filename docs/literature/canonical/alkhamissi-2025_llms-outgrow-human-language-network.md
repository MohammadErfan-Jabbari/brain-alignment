---
title: "From Language to Cognition: How LLMs Outgrow the Human Language Network"
tags: [literature]
aliases: [alkhamissi-2025_llms-outgrow-human-language-network]
---

# From Language to Cognition: How LLMs Outgrow the Human Language Network

**Authors:** Badr AlKhamissi, Greta Tuckute, Yingtian Tang, Taha Binhuraib, Antoine Bosselut, Martin Schrimpf
**Year:** 2025
**Venue:** arXiv preprint
**DOI/arXiv:** 10.48550/arXiv.2503.01830
**Canonical ID:** alkhamissi-2025_llms-outgrow-human-language-network

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: identifies which model properties and training phases actually drive alignment with the human language network (LN), rather than treating alignment as a single final-model score.
2. Core insight: LN alignment is tied most strongly to formal linguistic competence and context integration, rises early, then saturates while functional competence continues improving.
3. If-wrong breakage: if alignment tracks functional competence or next-word prediction throughout training, the "outgrow LN" interpretation is wrong.
4. Main result location: Section 5.1-5.3, Figures 2-5 (pages 6-8), with key controls in Appendix Figures 10-12 (pages 18-19).

---

## Source Grounding

The study evaluates 34 checkpoints across training (to about 300B tokens) over multiple model sizes and five neural language benchmarks, using a standardized linear-predictivity brain-scoring protocol with cross-subject-consistency normalization. It combines architecture ablations on untrained models, competence benchmarking (formal vs functional), and longitudinal analysis of brain, language-modeling, and behavioral alignment.

## Core Claims

- `C1`: Untrained models already show substantial LN alignment, and architecture-level context integration (attention/sequence aggregation plus positional encoding) is a key driver.
- `C2`: Brain alignment peaks early in training and tracks formal linguistic competence more strongly than functional competence.
- `C3`: As training continues beyond early phases, brain alignment decouples from both next-word prediction and behavioral alignment, including late-stage weakening or reversal in larger models.

## Evidence Pointers

- `C1` evidence: Section 4.1 and 5.1 (pages 5-6), Figure 2 and Appendix Figure 6 discussion. The paper reports untrained models retaining about 50% of pretrained alignment under stricter topic-held-out generalization, and shows higher scores for sequence/context-integration architectures over token-local baselines.
- `C2` evidence: Section 5.2 (pages 6-8), Figure 3 and Figure 4. Reported trajectory: near-untrained levels until about 128M tokens, sharp rise peaking around 2B-8B tokens, then saturation. Formal-vs-functional tracking is quantified with a Wilcoxon signed-rank result (W = 0.0, p < 0.002) favoring formal competence as the stronger correlate.
- `C3` evidence: Section 5.3 (page 8), Figure 5. The paper reports strong early correlations (up to about 2B tokens) between brain alignment and both LM loss and behavioral alignment, followed by diminished significance later; in larger models, late-stage brain-vs-behavior correlations can become negative.

## Assumptions and Limits

The analysis is LN-centric and English-only, so conclusions do not directly establish how alignment behaves in other languages or non-language brain systems. Functional competence is measured by selected benchmark suites, which are informative but still an operational proxy for broader real-world language use.

## Interpretation Notes

This paper's main value is temporal decomposition: it explains when and why alignment appears, rather than just reporting which final model scores highest. For thesis framing, it supports the idea that strong LN alignment is not equivalent to broad cognitive alignment, and that post-human language performance can diverge from human-like processing signatures.

## Open Questions

- Which non-LN brain networks better track functional competence as models continue scaling?
- Can we design training interventions that improve functional competence without losing human-like behavioral alignment?
- Is the same early-saturation pattern stable across multilingual and speech-native training regimes?


## Read Date

2026-03-02


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
