# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

**Last updated:** 2026-06-11 (after Session 7 / E004 lever + E006 powered A2 + E005 F1-confirmed; Erfan-confirmed).

---

## Current position

We have climbed **Layer 0 (A2, powered/voxelwise — E006)**, **Layer 2a (E003)**, **Layer 1 (lever, E004, PARTIAL)**, and now **Layer 3 / F1 (E005, in-domain PARTIAL-PASS)**. The full story: brain alignment is **robustly real and measurable** (A2 powerful at voxel scale); **optimizing** it gives a **small but real, brain-specific, perplexity-independent gain** — confirmed in distillation at matched perplexity (E005: +0.0081, CI excludes 0, robust) — **the dissociation E003/E004 couldn't establish**. The effect is small (~1.6% NC), so the headline is an **A+B synthesis**: F1 confirmed (alignment-guided KD recovers alignment beyond perplexity) *and* the rigorous characterization of how small it is (the rate–distortion trade-off curve). `$\mathcal{L}_{\text{brain}}$` built; D010 → co-trained MSE.

**→ Next step: (1) LeBel voxelwise TRANSFER test** (does E005's in-domain gain generalize? — needs a *powered* statistic, design+oracle-gate first) **and (2) the λ-sweep / multi-rate trade-off curve**. Details in "Next session", bottom.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **L0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS (powered)** | **E002** (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 nuisance, story-CV. Clears the Hadidi/Feghhi 2026 bar. |
| **L2a** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **L1** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | 🟡 **PARTIAL** | **E004** — brain loss built (loss family; D010 → co-trained MSE leaning). Brain-SPECIFIC lever exists on the strong aligner (Qwen mse − its permuted twin = **+0.0032 [+0.0006,+0.0058]**), but small/fragile (fold-4 carries half) & sub-threshold on the 5-ROI screen (no arm raised Δ above base; MDE limits). `frozen`=non-specific regularizer; cka/cos worst. Co-varies w/ perplexity (L011/L012). |
| **L3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → rate-distortion trade-off curve | brain term buys ~0 alignment at matched perplexity (paired, powered) | 🟡 **PARTIAL-PASS** | **E005** (Qwen2.5-1.5B→0.5B KD, LoRA): alignment-guided KD beats perplexity-only **at matched perplexity**, brain-specifically — paired (kd_brain − kd_brain_permuted) = **+0.0081 [+0.0023, +0.0171]**, CI excludes 0, 4/5 folds + (leave-fold-4-out +0.0042), gain holds despite slightly-worse ppl (rules out L011). The dissociation E003/E004 couldn't show. **But small** (~1.6% NC) = A+B synthesis. **In-domain (Tuckute) confirmed; voxelwise TRANSFER + full trade-off curve pending.** |
| **L2b · A3** | Does preserved/induced alignment *buy something practical* (OOD, low-data sample-efficiency)? | gains stay confined to the alignment metric | ⬜ **not started** | the untested assumption — **the real thesis risk**. Run the matched non-brain control the precedents skipped (R04). |
| **L4 · F3** | An fMRI-free *proxy* (neighborhood-overlap / LID surrogate) that recovers most of the benefit | surrogate recovers little of the L3 benefit | ⬜ **not started** | stretch / PhD seed. LID sign is unsettled (cheng vs yu) — validate direction against real fMRI first. |

## Supporting tracks (not rungs, but gate the rungs)

| Track | Status | Note |
|---|---|---|
| Data — Tuckute 2024 | ✅ staged + in use | ROI-level screen (5 LH lang ROIs), `data/tuckute2024/` |
| Data — LeBel UTS03 voxelwise | ✅ **built + run (E006)** | adapter `scripts/lebel_adapter.py` (reuses official deep-fMRI-dataset pipeline); CC_norm voxel selection; powered A2 confirmed |
| Literature | ✅ done | R03, R04, 14 canonical notes (+ hadidi-2024 anti-confound bar; lit-fork sweep leans B) |
| Theory grounding | ✅ done | `06-theory-grounding.md` (MI bound, DPI, conditional-MI, rate-distortion) |
| Harness | ✅ **`$\mathcal{L}_{\text{brain}}$` built** | `brain_loss.py` (mse/cos/pearson/frozen/cka + block_permute); `run_brain_lever.py` (LoRA brain-tune); `run_lebel_encoding.py` (powered voxelwise); `distill.py` λ_brain |

Legend: ✅ done · 🟡 partial / in progress · ⬜ not started.

---

## Next session (what `/orient` surfaces)

**Mode:** implementation (working).
**Goal:** confirm E005's in-domain F1 generalizes + trace the full trade-off curve.

1. **LeBel voxelwise TRANSFER test (the next gate).** Does E005's in-domain (Tuckute) F1 gain (+0.0081) generalize to the powered LeBel voxelwise benchmark? **Design + oracle-gate FIRST** — the mean-over-voxels statistic is underpowered (E006 MDE +0.013 ≫ the effect), so the transfer test needs a *powered* statistic (per-voxel paired, or LH-language-region-restricted). Measure each E005 KD student (kd_brain vs kd_brain_permuted) on the E006 LeBel protocol. A positive = cross-dataset/granularity generalization (strong); a powered null after an in-domain positive = "real but doesn't transfer" (still honest).
2. **λ-sweep / multi-rate trade-off curve.** Trace kd_brain & kd_ppl frontiers across λ_brain and ≥2 compression rates → the rate–distortion curve (the Fork-B-rigor framing / the "how small" characterization). In-domain Tuckute first (powered), then LeBel.
3. **Doc-consistency (wrap carry-over):** dedup feghhi-2024 / hadidi-2024 (same paper); sweep R03/R04/upspeed for stale "E004 = headline" (now E005) references.

**Deferred:** L2b / A3 (does alignment buy OOD/sample-efficiency), L4 / F3 (fMRI-free proxy). **E007 (TR-level LeBel lever loop) NOT built** (structurally underpowered, E006).

## Doc-consistency notes (for the wrap)
- `feghhi-2024` and `hadidi-2024` canonical notes are the **same paper** (arXiv-first-author vs NatComms-first-author) — dedup/redirect at wrap.
- The headline experiment was renamed **E004 → E005**; E004 is now the lever test. References in older docs (R03/R04/upspeed) may still say "E004 = headline" — fix at wrap.

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
