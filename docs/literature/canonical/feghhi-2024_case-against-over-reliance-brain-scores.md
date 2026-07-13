---
title: "What Are Large Language Models Mapping to in the Brain? A Case Against Over-Reliance on Brain Scores"
tags: [literature]
aliases: [feghhi-2024_case-against-over-reliance-brain-scores]
---

# What Are Large Language Models Mapping to in the Brain? A Case Against Over-Reliance on Brain Scores

> **⚠ DUPLICATE — same paper as [`hadidi-2024_case-against-brainscore-reliance`](hadidi-2024_case-against-brainscore-reliance.md), which is the CANONICAL note.** This is the earlier arXiv-version digest (first author Feghhi); `hadidi-2024` is the fuller Nature Communications 2026 digest (the * = equal-contribution author list is randomized, so the same paper appears under both first authors). The anti-confound bar (residual ≤10%, contiguous splits, shuffled-split inflation) lives in `hadidi-2024`. Kept as a redirect so existing `feghhi-2024` references resolve; cite `hadidi-2024` going forward. (Dedup logged in ladder/tasks, S8 2026-06-11.)

**Authors:** Ebrahim Feghhi*, Nima Hadidi*, Bryan Song, Idan A. Blank, Jonathan C. Kao (* equal contrib)
**Year:** 2024 (arXiv) / 2026 (Nature Communications)
**Venue:** arXiv preprint → Nature Communications 2026
**DOI/arXiv:** 10.48550/arXiv.2406.01538
**Canonical ID:** feghhi-2024_case-against-over-reliance-brain-scores

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper tests whether high LLM brain scores on standard benchmarks genuinely reflect language-like computation, or whether simple confounds explain much of the signal.
2. Core insight: A large share of reported neural predictivity can be recovered by simple temporal/positional/statistical features, and shuffled train-test splits seriously inflate interpretability of brain scores.
3. If-wrong breakage: If the confound analyses are incorrect, then the paper's central warning against strong brain-score-based claims about LLM-brain similarity collapses.
4. Main result location: Sections 3-5, especially Figure 1 (p.6), Figure 2 (p.7), Figure 3 plus Tables 2-3 (pp.8-9), Figure 4 (p.10).

## Source Grounding

The study re-analyzes three datasets (Pereira fMRI, Fedorenko ECoG, Blank fMRI) with contiguous splits, explicit autocorrelation baselines, and layered feature-space decompositions. It quantifies how much GPT2-XL performance is explainable by simple features such as sentence length/position, static embeddings, and positional signals, then compares this to contextual features like sense and syntax.

## Core Claims

- `C1`: On Pereira, shuffled train-test splits are heavily contaminated by temporal autocorrelation and can produce misleading model-layer conclusions.
- `C2`: Untrained GPT2-XL performance on Pereira is fully explained by sentence length and sentence position, with no reliable additional variance after correction.
- `C3`: For trained GPT2-XL, most explainable variance is captured by simple non-contextual features; richer contextual features add only modest increments, and cross-dataset checks show similar cautionary patterns.

## Evidence Pointers

- `C1` evidence: Section 3.1; Figure 1a-b (pp.5-6), including strong anti-correlation between shuffled vs contiguous layer profiles and high OASM overlap.
- `C2` evidence: Section 3.2; Figure 2 (pp.6-7), including voxelwise tests where added untrained GPT2-XL contribution vanishes after FDR correction.
- `C3` evidence: Section 3.3 with Table 2 and Table 3 plus Figure 3 (pp.8-9), Section 4.2 on Fedorenko (pp.9-10), and Section 5.1 on Blank chance-level results (p.10).

## Assumptions and Limits

The decomposition depends on chosen feature sets and linear banded regression, so omitted feature spaces could shift attribution percentages. The authors also note scalability limits as feature spaces grow and potential bias from noise and sample size in neural recordings.

## Interpretation Notes

For thesis use, this paper is a methodological brake pedal: high encoding scores are not enough. It supports a workflow where every headline brain score is paired with split sanity checks and feature-space deconstruction before making claims about shared computation.

## Open Questions

Would the same deconstruction on larger, higher-sample neural datasets leave more unique LLM signal? How stable are these attribution percentages across newer architectures beyond GPT2-XL and RoBERTa-Large? Which controlled features are still "simple" versus already linguistically substantive in practice?


## Read Date

2026-03-02


## Related
- [`status.md`](../../status.md) — the canonical status board
