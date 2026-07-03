---
title: "What Should Feature Distillation Transfer in LLMs? A Task-Tangent Geometry View"
tags: [literature]
aliases: [saadi-2026_task-tangent-feature-distillation-llms, flex-kd]
---

# What Should Feature Distillation Transfer in LLMs? A Task-Tangent Geometry View

**Authors:** Khouloud Saadi; Di Wang  
**Year:** 2025/2026  
**Venue:** arXiv preprint; OpenReview entry exists  
**DOI/arXiv:** arXiv:2507.10155  
**Canonical ID:** saadi-2026_task-tangent-feature-distillation-llms

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [ ] Full PDF read (page-by-page comprehension)
- [x] Full HTML scanned (search + targeted read)
- [ ] Extracted text only

Verified on 2026-07-03 from the arXiv abstract page and arXiv HTML v3. Targeted read covered abstract, method motivation, functional-geometry principle, Flex-KD objective, experiment summaries, appendix related-work positioning, and implications for E016. This is a scout-grade canonical note for paper-positioning and reviewer-risk, not a full `paper-digest` pass.

Comprehension self-check passed: Y, for E016 novelty pressure and design implications.

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Feature KD for LLMs often tries to match teacher and student hidden states directly, but hidden coordinates only matter through their effect on the model's outputs; the paper asks which teacher feature directions should be transferred when teacher and student hidden sizes differ.
2. Core insight: Preserve the teacher's task-dependent functional geometry: select representation directions with high output sensitivity, match a student-capacity-sized subspace, and use correlation-style alignment rather than raw MSE/cosine/full-projection matching.
3. If-wrong breakage: If raw dense feature matching is already sufficient under dimension mismatch, Flex-KD's functional subspace story weakens. For this repo, if functional geometry is the right abstraction, then any positive TRIBE dense-target effect could be reviewer-reinterpreted as generic useful-feature distillation unless the matched-information `textfeat` control is run.

---

## Source Grounding

**Task and method.** The paper frames feature-based KD as a functional problem rather than a representation-similarity problem. It estimates task-relevant directions by aggregating gradient magnitudes over the dataset, selects the top teacher dimensions, and aligns the student with that subspace through correlation-based geometry preservation. Flex-KD can be combined with logit KD and supervised task loss.

**Evaluation.** The paper evaluates classification, instruction-following, summarization, and data-scarcity settings. Reported examples include IMDB and GLUE for classification, LLaMA/GPT2/OPT instruction-following students, and a 5% Dolly low-resource condition. Tables report averages over three random seeds in the classification setup.

**Baselines.** KD, fine-tuning, projector-based hidden-state transfer, CKA-style feature distillation, MiniLLM, SeqKD, and logit objectives such as GKD/DistiLLM appear as comparison points depending on the task.

---

## Core Claims

- `C1`: Intermediate representations should not be treated as intrinsically meaningful objects during distillation; the relevant object is how hidden directions affect the teacher's input-output function.
- `C2`: Effective feature KD need not transfer the full high-dimensional teacher representation; preserving dominant function-tangent directions can be sufficient.
- `C3`: Flex-KD is parameter-free, architecture-agnostic, and designed for teacher-student hidden-size mismatch.
- `C4`: Across the reported classification/generation/low-resource evaluations, Flex-KD improves over projector and CKA-style feature-distillation baselines, especially under severe representation mismatch.

---

## Evidence Pointers

- `C1` and `C2`: arXiv HTML Sec. 1 and Sec. 2.4; the explicit "Functional Geometry Preservation" principle.
- `C3`: Sec. 3.2-3.3: gradient-based subspace selection and correlation-based alignment.
- `C4`: Sec. 4 tables for IMDB, GLUE, instruction-following, summarization, and 5% Dolly; conclusion states consistent improvements under severe mismatch and low-resource regimes.

---

## Assumptions and Limits

No brain or neural target is used. The method is task-supervised feature KD, not biological privileged-target distillation. It asks which language-model hidden directions to transfer, not whether a brain-derived target contributes anything beyond language-model features.

The functional geometry is estimated from downstream task data and teacher gradients. This differs from E016, where the TRIBE target is a synthetic neural response target over unlabeled KD text, not a teacher-output sensitivity basis.

The method is task-dependent. A geometry selected for instruction-following, classification, or summarization is not automatically the same object as a geometry useful for preserving held-out brain alignment.

---

## Interpretation Notes

This is the strongest feature-KD pressure point for E016. It makes a generic "dense intermediate targets help students" claim uninteresting unless E016 can separate brain-specific target structure from ordinary useful feature geometry.

For a positive E016 branch, the matched-information `textfeat` control is mandatory. A reviewer can reasonably say: "TRIBE helped because it supplied a dense privileged representation target, not because it is brain-like." Flex-KD supplies the modern vocabulary for that objection: functionally useful subspaces, capacity-matched feature transfer, and dimension-mismatch-aware alignment.

For a null E016 branch, this paper helps the argument: if modern task-tangent feature KD works in ordinary language tasks but synthetic neural targets fail under matched budget and permuted controls, that is evidence that brain-like target geometry is not automatically a useful KD signal.

---

## Open Questions

1. Does a TRIBE synthetic-brain target overlap with teacher functional-tangent directions, or is it mostly orthogonal to output-relevant language-model geometry?
2. If E016 is positive, does `textfeat` recover the same gain, implying generic dense-target geometry rather than brain specificity?
3. Could a future branch use a brain-weighted functional subspace instead of direct target-R2/MSE matching?

---

## Read Date

2026-07-03

## Related

- [`../../top-venue-distillation-adjacency-audit-2026-07-03.md`](../../top-venue-distillation-adjacency-audit-2026-07-03.md)
- [`../../top-venue-paper-plan-2026-07-03.md`](../../top-venue-paper-plan-2026-07-03.md)
- [`../../experiments/E016_tribe-synthetic-brain-targets.md`](../../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../../01-research-landscape.md`](../../01-research-landscape.md)
