# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

**Last updated:** 2026-06-11 (after Session 7 / E004 lever + E006 powered A2; Erfan-confirmed).

---

## Current position

We have climbed **Layer 0 (A2)** — now with a **powered voxelwise confirmation** (E006) — **Layer 2a**, and **Layer 1** (the lever, E004, PARTIAL). `$\mathcal{L}_{\text{brain}}$` is now **built** (`scripts/brain_loss.py`, loss family; D010 leaning to co-trained MSE, unconfirmed). The signal is **robustly real and measurable** (A2 powerful at voxel scale), but **optimizing** it gives only a **small, fragile, brain-specific gain** (+0.0032, near the noise floor; co-varies with perplexity). The thesis is at its **headline fork**: E005 (alignment-guided vs perplexity-only KD **at matched perplexity**) decides Fork A ("alignment-guided distillation wins") vs Fork B ("alignment is real but hard to optimize → compete on the rate–distortion trade-off curve / measurement rigor"). Evidence + literature (Hadidi/Feghhi 2026 residual ≤10%) lean B; E005 settles it on evidence.

**→ Next step: run E005 in-domain** (reordered per oracle: Tuckute paired permuted-twin, LoRA, matched-ppl frontier; powered, MDE +0.0035). Details in "Next session", bottom.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **L0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS (powered)** | **E002** (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 nuisance, story-CV. Clears the Hadidi/Feghhi 2026 bar. |
| **L2a** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **L1** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | 🟡 **PARTIAL** | **E004** — brain loss built (loss family; D010 → co-trained MSE leaning). Brain-SPECIFIC lever exists on the strong aligner (Qwen mse − its permuted twin = **+0.0032 [+0.0006,+0.0058]**), but small/fragile (fold-4 carries half) & sub-threshold on the 5-ROI screen (no arm raised Δ above base; MDE limits). `frozen`=non-specific regularizer; cka/cos worst. Co-varies w/ perplexity (L011/L012). |
| **L3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → rate-distortion trade-off curve | brain term buys ~0 alignment at matched perplexity (paired, powered) | ⬜ **next (E005)** | the **headline thesis experiment** (**E005**, renamed from E004). Decides Fork A (win) vs Fork B (honest trade-off curve). Run **in-domain on Tuckute** (paired permuted-twin, powered MDE +0.0035) first; LeBel transfer second. Must control perplexity, not budget (L011). |
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
**Goal:** run E005 (the headline) and settle the Fork A / Fork B framing on evidence.

1. **E005 — the headline (L3 / F1), in-domain first.** Alignment-guided (co-trained-MSE) vs perplexity-only KD (gpt2-medium→gpt2, LoRA) compared **at matched perplexity** (L011), on **Tuckute in-domain** with the **paired permuted-twin** contrast (powered, MDE +0.0035) — then LeBel voxelwise transfer if in-domain positive. Oracle-vetted (HOLD→fixes: in-domain-primary, LoRA, permuted-twin, frontier-dominance, match-ppl-on-eval-domain-text, λ/gradient calibration). Positive = Fork A confirmed; powered null = Fork B (the honest trade-off curve). **Make-or-break for the headline framing.**
2. **Fork B write-up path (if E005 null):** the powered A2 PASS (E006) + the rate–distortion trade-off curve (from kd_ppl + the sweep) + alignment-tracks-perplexity (L011/L012) + the anti-confound rigor (Hadidi/Feghhi bar) is a coherent, publishable thesis without a positive lever.
3. **E007 (the TR-level LeBel lever loop) is NOT built** — E006 showed the mean-over-voxels lever statistic is structurally underpowered (MDE +0.013 ≫ +0.003). Do not build it unless E005 in-domain is clearly positive.

**Deferred:** L2b / A3 (does alignment buy OOD/sample-efficiency), L4 / F3 (fMRI-free proxy).

## Doc-consistency notes (for the wrap)
- `feghhi-2024` and `hadidi-2024` canonical notes are the **same paper** (arXiv-first-author vs NatComms-first-author) — dedup/redirect at wrap.
- The headline experiment was renamed **E004 → E005**; E004 is now the lever test. References in older docs (R03/R04/upspeed) may still say "E004 = headline" — fix at wrap.

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
