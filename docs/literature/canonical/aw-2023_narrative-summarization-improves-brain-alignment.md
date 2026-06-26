---
title: "Training language models to summarize narratives improves brain alignment"
tags: [literature]
aliases: [aw-2023_narrative-summarization-improves-brain-alignment]
---

# Training language models to summarize narratives improves brain alignment

**Authors:** Khai Loong Aw; Mariya Toneva
**Year:** 2023
**Venue:** ICLR 2023
**DOI/arXiv:** 10.48550/arXiv.2212.10898
**Canonical ID:** aw-2023_narrative-summarization-improves-brain-alignment

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper tests whether training for long-form narrative summarization produces language representations that align better with human brain activity than standard next-word-pretrained baselines.
2. Core insight: Fine-tuning long-context models on BookSum improves brain alignment broadly, and the gain is linked to deeper discourse-sensitive processing rather than just better next-word prediction.
3. If-wrong breakage: If these gains were only artifacts of language-model loss, domain overlap, or architecture quirks, the claim that summarization training adds brain-relevant understanding would fail.
4. Main result location: Sections 4-6, especially Figure 1 (p.5), Figure 2 (p.7), Figure 3 (p.8), and Figure 4 (p.9).

## Source Grounding

The study compares four base long-context language models with BookSum-finetuned counterparts and aligns each model's representations to Harry Potter fMRI recordings using voxelwise ridge encoding. It evaluates both 20v20 classification and Pearson correlation, then runs controls around context length, language-model loss, brain-region specificity, and discourse-feature subsets (characters, emotions, motions).

## Core Claims

- `C1`: Across four model families, BookSum-finetuned models achieve significantly higher brain alignment than their base counterparts.
- `C2`: The alignment improvement is not reducible to improved next-word modeling performance, because most finetuned models improve brain alignment without better LM loss.
- `C3`: The gain is strongest in conditions tied to deeper context use, including long input windows and discourse-feature analyses where character-related samples show the largest alignment advantage.

## Evidence Pointers

- `C1` evidence: Section 4; Figure 1 (p.5); paired tests with FDR correction reported in Section 4 and appendix references.
- `C2` evidence: Section 5; Figure 2 left panel (p.7), where BigBird and LED show better brain alignment but worse LM loss, and BART shows better alignment without LM-loss gain.
- `C3` evidence: Section 4 context-length analysis (p.6, peak around ~500 words and no benefit at very short contexts); Section 6 discourse analysis with Figure 3 (p.8) and Figure 4 (p.9).

## Assumptions and Limits

The evidence comes from one narrative fMRI dataset (Harry Potter) and linear encoding models, so generalization to other genres, languages, and nonlinear mappings is not guaranteed. The paper argues against several confounds, but causal attribution to "deeper understanding" still depends on how complete those controls are.

## Interpretation Notes

This paper is best read as evidence that training objectives requiring long-range narrative compression can inject brain-relevant structure beyond plain LM pretraining. For thesis use, its strongest reusable contribution is methodological: pair brain alignment with explicit controls on LM performance and context-window effects before claiming cognitive relevance.

## Open Questions

How much of the observed gain transfers to non-narrative stimuli and non-English data? Which specific discourse computations beyond character tracking drive the residual gain? Would the same pattern hold with stronger modern base models that already encode longer contexts well?


## Read Date

2026-03-02


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
