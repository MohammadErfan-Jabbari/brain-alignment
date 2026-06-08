# MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers

**Authors:** Wenhui Wang; Furu Wei; Li Dong; Hangbo Bao; Nan Yang; Ming Zhou
**Year:** 2020
**Venue:** arXiv preprint
**DOI/arXiv:** 10.48550/arXiv.2002.10957
**Canonical ID:** wang-2020_minilm-self-attention-distillation

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper compresses pretrained transformers in a task-agnostic way without rigid layer mapping constraints from teacher to student.
2. Core insight: Distilling last-layer self-attention distributions plus value-relation matrices transfers behavior effectively across different student depths and hidden sizes, with teacher assistant helping smaller students.
3. If-wrong breakage: If last-layer/value-relation transfer is not the right signal, MiniLM should not consistently beat soft-label and layer-to-layer alternatives under matched settings.
4. Main result location: Method in Section 3 (pp. 3-4), primary comparisons in Tables 2-4 (pp. 5-6), and ablations in Tables 5-7 (pp. 7-8).

---

## Source Grounding

The source proposes deep self-attention distillation as a simpler transfer target than full layer-to-layer imitation. It keeps the student focused on the teacher's last-layer attention behavior, adds value-relation transfer to avoid hidden-dimension coupling, and optionally uses a teacher-assistant stage to bridge large teacher-small student gaps.

## Core Claims

- `C1`: MiniLM with a 6-layer 768 student outperforms prior task-agnostic distilled baselines on major benchmarks while remaining close to BERT-base quality and faster at inference.
- `C2`: Value-relation transfer is a meaningful contributor across student sizes, improving results beyond attention-distribution-only variants.
- `C3`: Distilling only the teacher's last layer and adding a teacher assistant for small students improves outcomes relative to layer-to-layer transfer and direct small-student distillation.

## Evidence Pointers

- `C1` evidence: Table 2 benchmark comparison for 6-layer 768 models (p. 5) and Section 4.3 Main Results text including speed/retention statement (p. 6); Table 4 inference-time scaling (p. 6).
- `C2` evidence: Table 5 ablation with and without value-relation transfer and Table 6 value-relation vs value-MSE (p. 7).
- `C3` evidence: Section 3.3 teacher assistant rationale (p. 4), Table 3 results with/without TA for smaller architectures (p. 6), and Table 7 comparison against layer-to-layer distillation (p. 8).

## Assumptions and Limits

Core evidence is mostly from QA and GLUE dev-style evaluations under the paper's pretraining/distillation setup. Teacher assistant improves quality but increases training complexity. The framework is empirically strong, but the paper does not establish formal guarantees for when last-layer-only transfer should dominate full-layer matching.

## Interpretation Notes

MiniLM's main durable idea is relation-space distillation: comparing scaled dot-product relations instead of raw hidden vectors makes student design more flexible. This is especially useful when compression targets need arbitrary hidden sizes or layer counts.

## Open Questions

- How much of MiniLM's gain survives when distilling modern decoder-only instruction-tuned LLMs instead of BERT-style encoders?
- Can teacher-assistant benefits be reproduced with lower training overhead using curriculum or progressive depth schedules?
- Which transfer target is most robust under domain shift: attention maps, value relations, or mixed objectives?


## Read Date

2026-03-02
