---
title: "Multi-Granularity Structural Knowledge Distillation for Language Model Compression"
tags: [literature]
aliases: [liu-2022_multi-granularity-structural-kd]
---

# Multi-Granularity Structural Knowledge Distillation for Language Model Compression

**Authors:** Chang Liu; Chongyang Tao; Jiazhan Feng; Dongyan Zhao
**Year:** 2022
**Venue:** ACL 2022 (Long Papers)
**DOI/arXiv:** 10.18653/v1/2022.acl-long.71
**Canonical ID:** liu-2022_multi-granularity-structural-kd

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper addresses the limitation of mono-granularity KD by distilling richer structural knowledge across token, span, and sample granularities.
2. Core insight: Distilling pair-wise and triplet-wise structural relations from multi-granularity representations, with hierarchical layer assignment, yields stronger small-student transfer.
3. If-wrong breakage: If multi-granularity structure is not genuinely informative, a 14M student should not beat strong matched-setting baselines like MiniLMv2/CKD on most GLUE tasks.
4. Main result location: Method in Section 3 (pp. 3-5), primary benchmark in Table 1 (p. 6), and ablation/discussion in Table 3 and Figure 3 (pp. 7-8).

---

## Source Grounding

The source reframes KD around three questions: which granularity to transfer, what form the knowledge should take, and how to place that transfer across student depth. MGSKD answers with multi-granularity representations (tokens/spans/samples), relation-based structural knowledge (pair-wise interactions and triplet angles), and hierarchical layer routing (lower layers for token/span, upper layers for sample).

## Core Claims

- `C1`: Under matched task-specific settings, Student+MGSKD (14M) outperforms Student+MiniLMv2 and Student+CKD on most GLUE tasks (7/8 reported in text).
- `C2`: MGSKD enables a 14M student to approach or match BERT-base behavior on many GLUE tasks while keeping substantial speedup (reported as about 9.4x).
- `C3`: Sample-level knowledge and hierarchical placement are the most influential design choices in the method's ablations.

## Evidence Pointers

- `C1` evidence: Main Results narrative (Section 4.4, p. 7) and Table 1 quantitative comparison (p. 6).
- `C2` evidence: Table 1 model-size/speed columns and task metrics (p. 6), plus Main Results discussion on performance-vs-size tradeoff (p. 7).
- `C3` evidence: Table 3 ablation over token/span/sample removal and relation forms (p. 7), and "Choice of boundary layer M" with Figure 3 (p. 8).

## Assumptions and Limits

The evaluation is task-specific GLUE distillation with a particular teacher/student setup (ELECTRA-base teacher, TinyBERT-initialized student, data augmentation). The method introduces additional relation-head and angle-hyperparameter complexity. Performance on CoLA lags several baselines, which the authors attribute to stronger syntactic emphasis than sample-level semantics.

## Interpretation Notes

This paper argues that "what to transfer" in KD should be structural and multi-level, not just local hidden-state imitation. For compression pipelines, it offers a reusable pattern: semantic granularity routing across depth can matter as much as loss type.

## Open Questions

- How sensitive are MGSKD gains to span-construction heuristics and language morphology?
- Can hierarchical multi-granularity transfer scale to decoder-only LLM distillation?
- What is the best compute-accuracy frontier when relation-head count and angle sampling are jointly optimized?


## Read Date

2026-03-02


## Related
- [`status.md`](../../status.md) — the canonical status board
