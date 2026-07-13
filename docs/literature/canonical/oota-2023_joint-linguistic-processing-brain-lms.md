---
title: "Joint processing of linguistic properties in brains and language models"
tags: [literature]
aliases: [oota-2023_joint-linguistic-processing-brain-lms]
---

# Joint processing of linguistic properties in brains and language models

**Authors:** Subba Reddy Oota; Manish Gupta; Mariya Toneva
**Year:** 2023
**Venue:** NeurIPS 2023
**DOI/arXiv:** 10.48550/arXiv.2212.08094
**Canonical ID:** oota-2023_joint-linguistic-processing-brain-lms

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper tests which explicit linguistic properties in LM representations are responsible for LM-fMRI alignment, using direct feature removal instead of only correlation-level probes.
2. Core insight: Removing any tested property lowers alignment, and syntactic properties (Top Constituents, Tree Depth) explain the strongest layer-trend effects, while semantic effects appear more region-specific.
3. If-wrong breakage: If residualization fails to isolate properties, then the attribution of alignment drops to specific linguistic factors is not valid.
4. Main result location: Section 5, especially Table 1 and Figure 3 (pp.6-7), Table 2-3 and Figure 4 (pp.8-9), plus conclusion synthesis (p.10).

## Source Grounding

The authors use pretrained BERT (and GPT-2 in supporting analyses) on the Narratives **"21st year" listening** fMRI dataset (18 subjects, 8,267 words, 2,226 TRs at TR=1.5s — confirmed from the authors' repo `linguistic-properties-brain-alignment` and the arXiv abstract's "listened to a story"; this is a *listening* dataset, **not** Harry Potter, which is a *reading* dataset — corrected 2026-06-10, see L009) and remove six probing properties from model representations: one surface, two syntactic, three semantic. They then re-run voxelwise encoding to measure alignment loss and correlate layerwise probing degradation with layerwise brain-alignment degradation at whole-brain, ROI, and sub-ROI levels.

## Core Claims

- `C1`: Removing each tested linguistic property causes a significant reduction in brain alignment across layers, beyond a random-vector control.
- `C2`: Syntactic properties, especially Top Constituents and Tree Depth, contribute most to the layerwise alignment trend at whole-brain and many language-ROI levels.
- `C3`: Contributions are region-specific: Top Constituents is broadly strong, Tree Depth is concentrated in temporal and frontal language regions, and semantic properties become more visible in PCC and sub-ROI analyses.

## Evidence Pointers

- `C1` evidence: Section 5.2; Figure 3 and paired significance testing with FDR correction (p.7), with probing-removal success shown in Table 1 (p.6).
- `C2` evidence: Section 5.3 whole-brain and ROI analysis; Table 2 correlations (p.8), highlighted again in Section 6 conclusion (p.10).
- `C3` evidence: Section 5.3 sub-ROI and voxelwise analysis; Table 3 and Figure 4 (pp.8-9), plus regional summary in Section 6 (p.10).

## Assumptions and Limits

The removal is linear and can also remove correlated information, so attribution is conservative but not perfectly specific. The paper also reports substantial remaining alignment after removing all tested properties, which means the investigated feature set is incomplete.

## Interpretation Notes

For reuse, this is a clean "direct intervention" complement to standard probing and pure encoding-score comparisons. It supports using feature-removal deltas as evidence when we need stronger claims about what kind of linguistic information is jointly processed in model and brain.

## Open Questions

Which additional linguistic or discourse properties account for the substantial residual alignment? How stable are these regional attribution patterns under larger models and non-English stimuli? Can nonlinear removal methods separate correlated properties more cleanly without overfitting?


## Read Date

2026-03-02


## Related
- [`status.md`](../../status.md) — the canonical status board
