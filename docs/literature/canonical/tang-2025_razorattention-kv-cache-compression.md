# RazorAttention: Efficient KV Cache Compression Through Retrieval Heads

**Authors:** Hanlin Tang; Yang Lin; Jing Lin; Qingsen Han; Shikuan Hong; Yiwu Yao; Gongyi Wang
**Year:** 2024
**Venue:** arXiv preprint
**DOI/arXiv:** arXiv:2407.15891
**Canonical ID:** tang-2025_razorattention-kv-cache-compression

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper targets long-context inference bottlenecks by reducing KV-cache memory without collapsing retrieval quality.
2. Core insight: Preserve full KV only for retrieval heads, aggressively compress non-retrieval heads, and recover dropped information with a compensation token.
3. If-wrong breakage: If retrieval-head separation is not stable, compression will silently remove needed long-range evidence and fail on multi-query contexts.
4. Main result location: Section 3.1-3.2; Theorem 1 (p.4), Table 1 (p.5), Table 2-3 (p.6), Figure 4 (p.7).

---

## Source Grounding

The source first analyzes head-level attention behavior in long-context transformers, then introduces a training-free head-wise KV strategy plus compensation token and benchmarks it on long-context tasks across several LLM families.

## Core Claims

- `C1`: Attention heads are functionally asymmetric: a small subset of retrieval heads carries most long-range retrieval load, while many heads are effectively local.
- `C2`: RazorAttention can cut KV cache by about 70% (around 3x compression) with near-baseline task quality and competitive/better performance than prior KV-compression methods.
- `C3`: The method is practical for deployment because its head-wise criterion is compatible with FlashAttention and avoids expensive retraining.

## Evidence Pointers

- `C1` evidence: Section 3.1-3.2 and Theorem 1 (p.4); Table 1 protected-head ablation (p.5).
- `C2` evidence: Abstract and Figure 1 (p.1); Table 2 compression setting (p.6); Table 3 and Figure 4 long-context benchmark results (p.6-7).
- `C3` evidence: Introduction/design rationale discussing FlashAttention compatibility (p.1-2) and contribution summary on implementation overhead (p.3).

## Assumptions and Limits

The method assumes retrieval-head identification remains valid across prompts/tasks and model families. Reported outcomes focus on long-context benchmarks and may not transfer uniformly to all generation regimes. Compression benefits also depend on serving stack details and attention-kernel implementation.

## Interpretation Notes

RazorAttention is best read as an interpretability-driven systems method: it turns a head-role hypothesis into a concrete memory policy. Its edge over token-importance eviction is that it preserves query-time optionality instead of betting on one static notion of token importance.

## Open Questions

- How stable are retrieval-head assignments across domains and multi-turn chat sessions?
- Can this head-wise policy be combined cleanly with KV quantization for further memory cuts?
- What are the failure boundaries at context lengths beyond those evaluated in the paper?


## Read Date

2026-03-02
