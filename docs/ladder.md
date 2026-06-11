# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

**Last updated:** 2026-06-11 (after Session 8 / thinking-panel audit + E008 per-subject null → L3/F1 reframed to Fork-B; Erfan-confirmed).

---

## Current position

**The honest story (post-E008 reframe).** Brain alignment is **robustly real and measurable** (L0/A2, powered at voxel scale — E006). But **optimizing it does NOT produce a per-individual brain-specific alignment gain**: E008 (per-participant, n=9, well-powered, MDE≈+0.0006) returns a clean **NULL** (mean +0.00010, CI [−0.0004,+0.0006]). E005's headline +0.0081 was a **group-averaged-target** measurement — a higher-SNR read of the *shared stimulus-evoked response*, inflated ~1.7× by averaging and ~2.4× by one outlier fold — **not** per-person brain alignment (the 4 subjects E005 averaged are individually null). **Fork B confirmed:** the contribution is (1) A2 real & powered, (2) a **rigorous, well-powered per-subject null** + the anti-confound characterization (literature-consistent: Hadidi/Feghhi ≤10%), and (3) **A3 — does any of this buy something practical** — now the central open question.

**→ Next step (Erfan-confirmed): A3 / E009 — does brain-tuning buy practical robustness/sample-efficiency at matched perplexity, brain-specifically?** Oracle-gate then run. Details in "Next session", bottom.

> **Audit trail (S8, 2026-06-11, Erfan-confirmed):** the thinking-panel (counter-argument + premortem + first-principles, fable) caught — *before* compute — that E005's "CI excludes 0" was pseudo-replicated (15 cells over one 5-UID-averaged target) and that the planned LeBel transfer test was underpowered (`scripts/reanalyze_e005_e006.py`, L015). The pivot to a per-subject solidification (E008) then returned a well-powered null (L016), confirmed by a second panel. Rigor before compute caught an overclaim that would have been the thesis headline.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **L0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS (powered)** | **E002** (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 nuisance, story-CV. Clears the Hadidi/Feghhi 2026 bar. |
| **L2a** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **L1** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | 🟡 **PARTIAL** | **E004** — brain loss built (loss family; D010 → co-trained MSE leaning). Brain-SPECIFIC lever exists on the strong aligner (Qwen mse − its permuted twin = **+0.0032 [+0.0006,+0.0058]**), but small/fragile (fold-4 carries half) & sub-threshold on the 5-ROI screen (no arm raised Δ above base; MDE limits). `frozen`=non-specific regularizer; cka/cos worst. Co-varies w/ perplexity (L011/L012). |
| **L3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → per-individual brain-specific gain? | brain term buys ~0 alignment at matched perplexity (paired, powered) | ❌ **NULL per-subject** (averaged-target-only trend) | **E008** (per-participant, n=9, well-powered MDE≈+0.0006, panel-adjudicated): mean +0.00010, t-CI **[−0.0004,+0.0006]**, sign 5/9, fold-clustered CI incl 0 + fails LOO-fold; the 4 E005-averaged subjects are individually null. **E005's +0.0081 was a group-averaged-target / shared-stimulus-response measurement** (~1.7× averaging + 2.4× fold-4 inflation; L015/L016), NOT per-person brain alignment. The kill criterion fired. → Fork B. (Averaged-target trend +0.003–0.004 survives only as a non-significant, confound-incomplete measurement.) |
| **L2b · A3** | Does induced alignment *buy something practical* (OOD robustness, low-data sample-efficiency) at matched perplexity? | gains stay confined to the alignment metric | 🔵 **NEXT (E009, designed+grounded)** | **the now-central contribution** (the in-domain positive is gone). Robustness-primary (pirlot/Hoak), matched-ppl + permuted-brain controls (the novel controls every A3 prior — Negi/Schwartz — lacks), MDE 2–4pp (Guo). Oracle-gate → run. |
| **L4 · F3** | An fMRI-free *proxy* (neighborhood-overlap / LID surrogate) that recovers most of the benefit | surrogate recovers little of the L3 benefit | ⬜ **not started** | stretch / PhD seed. LID sign is unsettled (cheng vs yu) — validate direction against real fMRI first. |

## Supporting tracks (not rungs, but gate the rungs)

| Track | Status | Note |
|---|---|---|
| Data — Tuckute 2024 | ✅ staged + in use | ROI-level screen (5 LH lang ROIs), `data/tuckute2024/` |
| Data — LeBel UTS03 voxelwise | ✅ **built + run (E006)** | adapter `scripts/lebel_adapter.py` (reuses official deep-fMRI-dataset pipeline); CC_norm voxel selection; powered A2 confirmed |
| Literature | ✅ done | R03, R04, 14 canonical notes (+ hadidi-2024 anti-confound bar; lit-fork sweep leans B) |
| Theory grounding | ✅ done | `06-theory-grounding.md` (MI bound, DPI, conditional-MI, rate-distortion) |
| Harness | ✅ **`$\mathcal{L}_{\text{brain}}$` built** | `brain_loss.py` (mse/cos/pearson/frozen/cka + block_permute); `run_brain_lever.py` (LoRA brain-tune); `run_lebel_encoding.py` (powered voxelwise); `distill.py` λ_brain |

Legend: ✅ done · 🟡 partial / in progress · 🔵 next (designed) · ❌ tested-negative / kill fired · ⬜ not started.

---

## Next session (what `/orient` surfaces)

**Mode:** implementation (working).
**Goal:** A3 / E009 — does brain-tuning buy anything PRACTICAL at matched perplexity (the now-central contribution; the in-domain positive is gone after E008)?

1. **A3 / E009 — practical payoff (the central question).** Does a brain-tuned student generalize / resist distribution shift / sample-efficiently better than a matched-perplexity `kd_ppl` student, **brain-specifically** (beats `kd_brain_permuted`)? Design drafted + grounded (`docs/experiments/E009_a3-practical-payoff.md`). **Oracle-gate FIRST**, then build the offline robustness harness, then run + thinking panel. Robustness-primary (pirlot/Hoak); MDE 2–4pp (Guo). **E008-informed refinement:** brain-tune toward the *averaged* target (the setting with a measurable representational change, +0.008) so the downstream test has a real change to evaluate — a null on the light-touch per-subject students would be uninformative.
2. **(Optional, Fork-B rigor) λ-sweep / multi-rate trade-off curve** on the averaged target — the genuine R(D) "how small" characterization, if A3 needs the magnitude context.

**Deferred:** L4 / F3 (fMRI-free proxy). **Not built:** LeBel transfer test (underpowered, S8); E007 TR-level lever loop (underpowered, E006).

## Doc-consistency — CLEARED (S8)
- `feghhi-2024` → `hadidi-2024` canonical redirect added (same paper). ✅
- R03/R04 checked: **no stale "E004 = headline" references** exist (0 E004 mentions). ✅

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
