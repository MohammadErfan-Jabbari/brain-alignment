---
title: "Language models and brains align due to more than next-word prediction and word-level information"
tags: [literature]
aliases: [merlin-2024_beyond-next-word-brain-alignment]
---

# Language models and brains align due to more than next-word prediction and word-level information

**Authors:** Gabriele Merlin; Mariya Toneva
**Year:** 2024
**Venue:** EMNLP 2024
**DOI/arXiv:** 10.18653/v1/2024.emnlp-main.1024
**Canonical ID:** merlin-2024_beyond-next-word-brain-alignment

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper tests whether brain alignment of GPT-2 models can be reduced to next-word prediction and word-level information, or whether additional information is required.
2. Core insight: A two-perturbation contrast framework (stimulus-tuning plus input scrambling) leaves residual alignment in language regions even after controlling for next-word prediction and word-level information.
3. If-wrong breakage: If the contrast does not actually control the targeted factors, then the residual signal cannot support claims about additional brain-relevant information.
4. Main result location: Methods contrast formulation (Section 2.5, Eq. 5, pp.4-5) and Results Section 3 with Figures 2-5 (pp.6-7).

## Source Grounding

The authors evaluate GPT-2-small, medium, and distilled on one naturalistic fMRI narrative dataset. They introduce two perturbations: scrambling input word order at inference to preserve word identities while disrupting context structure, and stimulus-tuning on held-out narrative text to modulate prediction behavior. They compare baseline and perturbed models under ROI-level brain-alignment analysis, then build a second-level contrast to control both word-level and next-word effects.

## Core Claims

- `C1`: Stimulus-tuning improves both next-word prediction and brain alignment, with stronger gains in language-related ROIs than in non-language regions.
- `C2`: Scrambling decreases alignment but does not eliminate it, implying that word-level information alone is insufficient to explain alignment patterns.
- `C3`: After controlling for both word-level information and next-word prediction in the cross-perturbation contrast, residual positive alignment remains in IFG and AG.

## Evidence Pointers

- `C1` evidence: Section 3.1-3.2; Figure 2A and 2D plus Figure 3 and Figure 4 (pp.5-7).
- `C2` evidence: Section 3.2; Figure 2E-F and associated discussion (p.6), with persistence of alignment in language ROIs.
- `C3` evidence: Section 3.3 and Eq. 5 setup (pp.5-7); Figure 5 (p.7) with residual effects in IFG and AG across model variants.

## Assumptions and Limits

The inference relies on one dataset, GPT-2 family models, and a specific scrambling design. The paper explicitly notes high subject variability and limited statistical power for some ROI effects, so the residual interpretation should be treated as supported but not exhaustive.

## Interpretation Notes

This paper contributes a reusable causal-style evaluation pattern for brain alignment: do not only compare raw model scores, compare controlled contrasts that remove candidate mechanisms. In thesis terms, it is a bridge between "next-word prediction matters" and "next-word prediction is the whole story," and argues for the middle ground.

## Open Questions

How robust is the IFG/AG residual across other architectures and larger datasets? Would alternative perturbations that disrupt compositional structure differently produce the same residual pattern? Which explicit multi-word representations best account for the residual term?


## Read Date

2026-03-02


## Related
- [`status.md`](../../status.md) — the canonical status board
