# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

**Last updated:** 2026-06-10 (after Session 6 / E003).

---

## Current position

We have climbed **Layer 0 (A2)** and **Layer 2a**, plus all the supporting groundwork (data, literature, theory, harness). **We have not yet built or run the brain-alignment loss itself** — every experiment so far *measures* alignment; none *optimizes* it. The keystone (`$\mathcal{L}_{\text{brain}}$`, decision D010) is still unbuilt.

**→ Next step: an IMPLEMENTATION session — build `$\mathcal{L}_{\text{brain}}$` (resolve D010) and run the Layer-1 lever test, then the Layer-3 / F1 headline at matched perplexity.** Details in "Next session", bottom.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **L0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS** | **E002** — trained mid-layer unique R² +0.020 (gpt2) … +0.036 (Qwen2.5-0.5B), NC-norm 5–10%; untrained controls negative (3 seeds) |
| **L2a** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **L1** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | ⬜ **not started** | requires building the loss (D010). Blocks everything below. |
| **L3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → rate-distortion trade-off curve | does not beat perplexity-only KD by ≥ +0.05 unique R² at matched ppl/budget (H001) | ⬜ **not started** | the **headline thesis experiment** (E004). Depends on L1. Must control perplexity, not just budget (L011). |
| **L2b · A3** | Does preserved/induced alignment *buy something practical* (OOD, low-data sample-efficiency)? | gains stay confined to the alignment metric | ⬜ **not started** | the untested assumption — **the real thesis risk**. Run the matched non-brain control the precedents skipped (R04). |
| **L4 · F3** | An fMRI-free *proxy* (neighborhood-overlap / LID surrogate) that recovers most of the benefit | surrogate recovers little of the L3 benefit | ⬜ **not started** | stretch / PhD seed. LID sign is unsettled (cheng vs yu) — validate direction against real fMRI first. |

## Supporting tracks (not rungs, but gate the rungs)

| Track | Status | Note |
|---|---|---|
| Data — Tuckute 2024 | ✅ staged + in use | ROI-level screen (5 LH lang ROIs), `data/tuckute2024/` |
| Data — LeBel UTS03 voxelwise | 🟡 staged, **adapter not built** | powered confirmation (thousands of voxels); FIR/lag + contiguous-story loader is real work, not a config swap |
| Literature | ✅ done | R03 (first-principles), R04 (gap analysis), 12 canonical notes |
| Theory grounding | ✅ done | `06-theory-grounding.md` (MI bound, DPI, conditional-MI, rate-distortion) |
| Harness | 🟡 partial | E001/E002 anti-confound built; `distill.py` supports λ_brain>0; **the `$\mathcal{L}_{\text{brain}}$` form (D010) is unbuilt** |

Legend: ✅ done · 🟡 partial / in progress · ⬜ not started.

---

## Next session (what `/orient` surfaces)

**Mode:** implementation (working).
**Goal:** build the keystone and run the lever test, then the headline.

1. **Build `$\mathcal{L}_{\text{brain}}$` (resolve D010) + run L1.** Frozen encoding-map loss (fit ridge on Tuckute train, freeze, penalize the student so it predicts held-out BOLD); a CKA/RDM variant optional. Verify on real data that turning it on *raises* held-out unique R² under the full anti-confound protocol. New experiment doc. Cheap, unblocks F1.
2. **E004 — the headline (L3 / F1).** Alignment-guided KD vs perplexity-only KD **at matched perplexity** (L011). Make-or-break. Depends on step 1.
3. **Converged cold arm** (cheap cleanup of E003's under-training confound — re-run cold-KD to matched perplexity).
4. **LeBel voxelwise adapter** when a powered confirmation of the ~0.005 gaps is needed.

**Deferred until F1 shows the signal is movable + preservable:** L2b / A3 (does it buy anything), L4 / F3 (fMRI-free proxy).

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
