---
title: "Beware of Calibration Data for Pruning Large Language Models"
tags: [literature]
aliases: [ji-2025_calibration-data-pruning-llms]
---

# Beware of Calibration Data for Pruning Large Language Models

**Authors:** Yixin Ji; Yang Xiang; Juntao Li; Qingrong Xia; Ping Li; Xinyu Duan; Zhefeng Wang; Min Zhang
**Year:** 2025
**Venue:** ICLR 2025
**DOI/arXiv:** 10.48550/arXiv.2410.17711
**Canonical ID:** ji-2025_calibration-data-pruning-llms

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper tests whether post-training pruning quality is limited more by pruning algorithm choice or by calibration-data choice.
2. Core insight: Calibration data distribution matters sharply at higher sparsity, and synthetic self-generated calibration data can outperform common baselines when pretraining data is unavailable.
3. If-wrong breakage: If this is wrong, calibration-data engineering is mostly wasted effort and pruning improvements should come mainly from better importance metrics.
4. Main result location: Section 3.2-3.4; Figure 1 (p.2), Figure 2 (p.4), Figure 3 (p.5), Table 2 (p.8), Table 5 (p.16).

---

## Source Grounding

The source runs controlled pruning experiments across multiple calibration corpora, sparsity settings, and pruning methods, then proposes a self-generation-plus-filtering strategy for calibration data and evaluates it on DCLM and LLaMA-family models.

## Core Claims

- `C1`: Calibration data is a first-order factor in post-training pruning quality at moderate/high sparsity, and its effect can exceed differences between pruning methods.
- `C2`: Increasing calibration sample count does not eliminate performance gaps caused by calibration-data source differences.
- `C3`: Self-generated, perplexity-filtered calibration data improves pruning performance across models/methods and remains compatible with strong pruning baselines.

## Evidence Pointers

- `C1` evidence: Section 3.2; Figure 1 (p.2) compares method vs data effects; Figure 2 (p.4) and Section 3.2 text (p.5) report widening gaps as sparsity/structure increase.
- `C2` evidence: Section 3.3; Figure 3 (p.5) shows source gaps persist across larger calibration set sizes.
- `C3` evidence: Section 3.4 and Section 5.2; Table 1 (Section 3.4, p.6), Table 2 (p.8), and Table 5 (p.16) report synthetic-data gains across settings.

## Assumptions and Limits

The evaluation focuses on selected open-source LLM families, pruning methods (e.g., Wanda/DSnoT/OWL), and commonsense reasoning/language modeling benchmarks. Similarity analysis is based on n-gram overlap heuristics, which may not capture deeper distributional properties. The self-generation pipeline depends on sampling/filtering hyperparameters and may shift behavior across domains.

## Interpretation Notes

This paper reframes calibration data from an implementation detail into a major control variable for pruning outcomes. The practical takeaway is that data-distribution alignment can buy as much or more than swapping pruning objectives, especially once sparsity is high enough to expose fragility.

## Open Questions

- How stable are these gains for multilingual, code, or instruction-heavy pretraining mixtures?
- Can a lightweight retrieval-based proxy for pretraining similarity match synthetic generation quality?
- Does synthetic calibration overfit a model's own blind spots when the model generates and is then pruned from the same distribution proxy?


## Read Date

2026-03-02


## Related
- [`status.md`](../../status.md) — the canonical status board
