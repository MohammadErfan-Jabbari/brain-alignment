# Linguistic properties and model scale in brain encoding: from small to compressed language models

**Authors:** Subba Reddy Oota; Vijay Rowtula; Satya Sai Srinath Namburi; Khushbu Pahwa; Anant Khandelwal; Manish Gupta; Tanmoy Chakraborty; Bapi S. Raju
**Year:** 2026
**Venue:** arXiv preprint
**DOI/arXiv:** arXiv:2602.07547
**Canonical ID:** oota-2026_brain-encoding-scale-compression

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper tests how much language-model scale is actually needed for brain alignment and how compression changes that alignment.
2. Core insight: Brain alignment saturates around 3B scale across families, is mostly robust to quantization/moderate pruning, and is not tightly coupled to all linguistic benchmark changes.
3. If-wrong breakage: If these findings fail, conclusions about compact brain-aligned models are overstated and compression may be distorting neural conclusions.
4. Main result location: Section 4 RQ1-RQ3; Figure 2 (p.6), Table 2 (p.7), RQ2 analysis (p.8), Table 5 (p.9), Figure 5 (p.10), Tables 7-8 (appendix pages p.23, p.29).

---

## Source Grounding

The source evaluates multiple model families (small and large, plus compressed variants) on fMRI encoding/decoding and on FlashHolmes probing, then compares scale and compression effects on normalized brain alignment and linguistic competence.

## Core Claims

- `C1`: Across tested families, ~3B models achieve brain alignment comparable to larger 7B-14B models, while ~1B-1.5B models show consistent degradation.
- `C2`: Most quantization methods and moderate pruning preserve brain alignment, but GPTQ and aggressive compression in smaller models show clearer degradation.
- `C3`: Linguistic competence drops under some compressions do not always translate into proportional brain-alignment drops, indicating partial dissociation.

## Evidence Pointers

- `C1` evidence: Section 4 [RQ1]; Figure 2 (p.6) and Table 2 pairwise tests (p.7).
- `C2` evidence: Section 4 [RQ2] (p.8); Table 5 quantization/pruning comparison (p.9); Figure 4 voxel-wise change map (p.9).
- `C3` evidence: Section 4 [RQ3] and Figure 5 tradeoff analysis (p.10); FlashHolmes breakdown tables (Table 7 p.23, Table 8 p.29).

## Assumptions and Limits

The study uses a specific naturalistic fMRI dataset (nine participants) and selected model families, so generalization to other modalities/languages/tasks is not automatic. Quantized/pruned models are evaluated without retraining, which isolates compression effects but may understate recoverable performance. Linguistic probing via linear classifiers captures accessible features, not full causal competence.

## Interpretation Notes

This paper supports an efficiency-first view of brain-aligned modeling: beyond a moderate capacity threshold, extra scale may buy little neural alignment, and many compression choices preserve brain-relevant geometry. It also warns against treating benchmark competence and neural predictivity as interchangeable objectives.

## Open Questions

- Does the ~3B saturation point hold across additional brain datasets, languages, and interaction settings?
- Why does GPTQ show comparatively stronger neural degradation than AWQ/SmoothQuant in this setup?
- Can compression-aware fine-tuning recover linguistic deficits while preserving the same brain-alignment regime?


## Read Date

2026-03-02
