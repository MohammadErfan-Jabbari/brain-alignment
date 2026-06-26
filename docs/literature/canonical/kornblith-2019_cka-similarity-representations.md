---
title: "Similarity of Neural Network Representations Revisited"
tags: [literature]
aliases: [kornblith-2019_cka-similarity-representations]
---

# Similarity of Neural Network Representations Revisited

**Authors:** Simon Kornblith, Mohammad Norouzi, Honglak Lee, Geoffrey Hinton
**Year:** 2019
**Venue:** ICML 2019
**DOI/arXiv:** arXiv:1905.00414
**Canonical ID:** kornblith-2019_cka-similarity-representations

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper clarifies when popular representation-similarity metrics fail and proposes a more reliable default for neural representation comparison.
2. Core insight: Metrics invariant to arbitrary invertible linear transforms are too permissive in high dimension; CKA keeps useful invariances while preserving discriminative power.
3. If-wrong breakage: If CKA does not avoid the invertible-invariance failure mode, layer correspondence and architecture-level conclusions drawn from it are not trustworthy.
4. Main result location: Section 2.1 Theorem 1 (failure mode), Section 6.1 Figure 2 and Table 2 (sanity check), and Section 6.2 Figure 3/Figure 6 (architecture analysis), pp.2 and 6-7.

---

## Source Grounding

The source analyzes invariance requirements for representational similarity, proves a limitation for invertible-invariant metrics in high-dimensional regimes, and motivates CKA as a kernel-alignment approach tied to representational similarity matrices. It then benchmarks CKA against CCA-family and regression baselines on correspondence checks and architectural analyses.

## Core Claims

- `C1`: Any similarity index invariant to invertible linear transforms cannot provide meaningful discrimination once representation width exceeds available sample rank (`p >= n` regime).
- `C2`: CKA (linear and tuned RBF variants) reliably recovers corresponding layers across independently initialized but architecturally identical CNNs, while CCA/SVCCA/PWCCA/regression perform much worse in the same sanity check.
- `C3`: CKA reveals architecture effects that match functional diagnostics, including depth pathology (layer collapse in very deep plain nets) and width-driven convergence where early layers saturate sooner.

## Evidence Pointers

- `C1` evidence: Section 2.1 Theorem 1, p.2; invariance summary context in Table 1, p.4.
- `C2` evidence: Section 6.1, Figure 2 and Table 2, p.6 (layer correspondence accuracies: CKA near 99%, CCA-family much lower).
- `C3` evidence: Section 6.2, Figure 3, p.7 (depth pathology and probe accuracy agreement); Section 6.2, Figure 6, p.7 (width increases similarity with earlier-layer saturation).

## Assumptions and Limits

CKA still measures representational geometry rather than direct causal function. Kernel and bandwidth choices matter (especially for RBF CKA). The method is more robust than CCA-family metrics in tested settings, but it is not a universal substitute for task-conditioned functional tests.

## Interpretation Notes

This paper is the key argument for separating "useful invariance" from "too much invariance." CKA is compelling because it preserves rotation/scaling robustness without collapsing distinctions in high-dimensional activations.

## Open Questions

Which kernels beyond linear and RBF improve interpretability for modern transformer-scale models?
How often does strong CKA alignment fail to predict stitchability or transfer performance?
Can CKA be integrated with intervention-based probes to separate shared geometry from shared computation?


## Read Date

2026-03-03


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
