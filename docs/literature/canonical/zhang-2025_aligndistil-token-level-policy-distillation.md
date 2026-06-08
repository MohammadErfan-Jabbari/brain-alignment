# AlignDistil: Token-Level Language Model Alignment as Adaptive Policy Distillation

**Authors:** Songming Zhang; Xue Zhang; Tong Zhang; Bojie Hu; Yufeng Chen; Jinan Xu
**Year:** 2025
**Venue:** ACL 2025 (Long Papers)
**DOI/arXiv:** 10.18653/v1/2025.acl-long.972
**Canonical ID:** zhang-2025_aligndistil-token-level-policy-distillation

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper addresses coarse response-level alignment signals that mis-credit tokens and slow optimization.
2. Core insight: RLHF with DPO-style reward can be rewritten as token-level policy distillation, then improved with contrastive reward construction and token-adaptive logit extrapolation.
3. If-wrong breakage: If the equivalence and adaptive-teacher design are weak, AlignDistil becomes a heavier variant of existing preference-optimization methods without reliable gain.
4. Main result location: Theorem 1 (p.3); Section 4.1-4.2 (p.4); Table 1 (p.6), Table 2-3 (p.7), Figure 2 (p.8).

---

## Source Grounding

The source derives a theoretical bridge from RLHF under DPO reward to a token-level KL-distillation form, then implements AlignDistil with two design additions (contrastive DPO reward and token-adaptive extrapolation) and evaluates on common alignment benchmarks.

## Core Claims

- `C1`: Under DPO reward parameterization, the RLHF objective is theoretically equivalent to a token-level policy distillation objective.
- `C2`: AlignDistil (on-policy and off-policy) improves alignment benchmark performance over major baselines, including DPO/PPO-family methods.
- `C3`: Token-level distributional reward optimization in AlignDistil converges faster than sentence-level and token-scalar alternatives.

## Evidence Pointers

- `C1` evidence: Section 3 theorem statement and derivation, including Theorem 1 and associated equations (p.3).
- `C2` evidence: Section 5 main results; Table 1 benchmark comparison (p.6), with supporting ablations in Table 2 and Table 3 (p.7).
- `C3` evidence: Section 6.4 convergence analysis and Figure 2 curves (p.8).

## Assumptions and Limits

The method depends on reward quality from DPO/reverse-DPO models and on the stability of adaptive extrapolation weights. Reported experiments focus on specific model scales/datasets and judge-based benchmarks that may shift with evaluator choice. Training efficiency and gains may vary across larger models or different preference distributions.

## Interpretation Notes

AlignDistil's key move is to treat alignment as teacher-distribution shaping at token granularity instead of scalar response reward pushing. This reframing explains both the claimed convergence benefit and why reward-construction details matter more than a single objective label.

## Open Questions

- How does token-adaptive extrapolation behave for much larger policy models under the same data budget?
- Can the method preserve its gains when preference labels are noisier or less pairwise-consistent?
- What is the best off-policy data construction strategy for AlignDistil without sacrificing safety-alignment behavior?


## Read Date

2026-03-02
