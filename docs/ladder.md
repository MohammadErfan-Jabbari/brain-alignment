# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

**Last updated:** 2026-06-11 (after Session 8 / thinking-panel audit + E008 per-subject null → L3/F1 reframed to Fork-B; Erfan-confirmed).

---

## Current position

**The honest story (post-E008 reframe).** Brain alignment is **robustly real and measurable** (L0/A2, powered at voxel scale — E006). But **optimizing it does NOT produce a per-individual brain-specific alignment gain**: E008 (per-participant, n=9, well-powered, MDE≈+0.0006) returns a clean **NULL** (mean +0.00010, CI [−0.0004,+0.0006]). E005's headline +0.0081 was a **group-averaged-target** measurement — a higher-SNR read of the *shared stimulus-evoked response*, inflated ~1.7× by averaging and ~2.4× by one outlier fold — **not** per-person brain alignment.

**The POSITIVE contribution (the paper's spine — S8 panel, do not bury it as a "null"):** a **methodological finding + a confound-clean protocol**. The finding: **cross-subject target-averaging manufactures apparent brain-specificity** — a gain measured against a group-averaged fMRI target reads as "brain-specific" (beats a permuted twin) even when *no individual subject shows it*, because averaging amplifies the shared stimulus-evoked component at an inflated noise ceiling (the +0.0081→+0.00010 ~80× collapse, E008/L016). The protocol that detects it — **matched-perplexity + per-kind permuted-twin + per-subject inference with crossed subject/fold clustering** — explains a class of overclaims in the alignment-*training* literature (Negi/Schwartz baseline against non-ppl-matched vanilla models; this is the control they lack). **Fork B = a positive method + corrected claims:** (1) A2 real & powered; (2) **the averaging-confound finding + protocol** (the positive contribution); (3) the well-powered per-subject null; (4) **A3 — practical payoff** (E009, in progress).

**→ The experimental ladder is essentially COMPLETE.** A2 holds (powered); F1 and A3 are characterized nulls; L4/F3 (fMRI-free proxy) is moot (it was predicated on an L3 benefit that is null). **Next step = a MODE CHANGE to write-up** (consolidate A2 + L016-method + the two nulls into the manuscript/report) — *or*, if a per-individual positive is still wanted, acquire higher-SNR data (within-subject fMRI repeats; not more averaging). Erfan's call. Details in "Next session", bottom.

> **Audit trail (S8, 2026-06-11, Erfan-confirmed):** the thinking-panel (counter-argument + premortem + first-principles, fable) caught — *before* compute — that E005's "CI excludes 0" was pseudo-replicated (15 cells over one 5-UID-averaged target) and that the planned LeBel transfer test was underpowered (`scripts/reanalyze_e005_e006.py`, L015). The pivot to a per-subject solidification (E008) then returned a well-powered null (L016), confirmed by a second panel. Rigor before compute caught an overclaim that would have been the thesis headline.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **L0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS (powered)** | **E002** (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 nuisance, story-CV. Clears the Hadidi/Feghhi 2026 bar. |
| **L2a** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **L1** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | 🟡 **PARTIAL** | **E004** — brain loss built (loss family; D010 → co-trained MSE leaning). Brain-SPECIFIC lever exists on the strong aligner (Qwen mse − its permuted twin = **+0.0032 [+0.0006,+0.0058]**), but small/fragile (fold-4 carries half) & sub-threshold on the 5-ROI screen (no arm raised Δ above base; MDE limits). `frozen`=non-specific regularizer; cka/cos worst. Co-varies w/ perplexity (L011/L012). |
| **L3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → per-individual brain-specific gain? | brain term buys ~0 alignment at matched perplexity (paired, powered) | ❌ **NULL per-subject** (averaged-target-only artifact) | **E008** (n=9, MDE≈+0.0006): mean +0.00010, t-CI **[−0.0004,+0.0006]**, fold-clustered incl 0, the 4 E005-averaged subjects individually null. **E010 dose-response** proves the mechanism: gap≈0 at k=1, *produced* by averaging (rises with k). **E011** (heavy LoRA r64/6ep) confirms the null is robust to LoRA *capacity* (+0.0004, incl 0; capacity didn't move the rep, and λ that does wrecks ppl — L019). E005's +0.0081 was a group-averaged / shared-stimulus-response artifact, NOT per-person alignment. → Fork B. Open door: Negi's loss+data regime (needs multi-subject naturalistic fMRI we lack). |
| **L2b · A3** | Does induced alignment *buy something practical* (OOD) at matched perplexity? | gains stay confined to the alignment metric | ❌ **bounded NULL** (E009, n=8, panel-adjudicated) | No brain-specific OOD-ppl payoff (kd_brain ≈ kd_brain_permuted ≈ textfeat ≈ kd_ppl, all within measured MDE 0.03–0.13) — AND **null-by-construction**: the fulcrum (brain-specific repr change at matched ppl) is itself ~0 (median +0.004, seed-0-outlier-driven; can't grow it without collapsing ppl). Ties to E008/L016. Negi-2025's positive is vs a non-ppl-matched baseline (L011 confound) — our matched-ppl+permuted control is the contribution. Limits: OOD-ppl is a weak proxy; perturbation/sample-eff axes not run (moot with fulcrum ~0). L017. |
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

**Mode:** ANALYSIS (write-up) — the experimental ladder is complete; the work now is consolidating evidence into the manuscript, not generating more.
**Goal:** turn the Fork-B story into the paper/thesis prose.

1. **Write the manuscript** (`docs/manuscript/`), structured around the **positive contribution**: *cross-subject target-averaging manufactures apparent brain-specificity, and a matched-ppl + permuted-twin + per-subject protocol detects it* (L016) — with A2 (powered-real), the F1 per-subject null (E008, the +0.0081→+0.00010 collapse), and the A3 bounded null (E009) as the supporting arc. Position vs Negi/Schwartz (the matched-ppl + permuted control is the novelty). Cite Hadidi/Feghhi (≤10% residual, consistent), Proietti, pirlot/Hoak/Guo.
2. **Figures:** the averaging-collapse (E005 avg +0.0081 → E008 per-subject +0.0001, with MDE), the E006 powered A2 voxel map, the A3 OOD/repr-gap nulls with measured MDEs.

**Decision points for Erfan (genuine forks):** (a) accept Fork-B + write up [recommended; the experimental arc is complete and honest]; (b) invest in a redesigned A3 (perturbation-robustness + sample-efficiency axes, escalated tuning) — *panel says null-by-construction unless the fulcrum can be grown, which the matched-ppl constraint blocks*; (c) pursue a per-individual positive via **new higher-SNR data** (within-subject fMRI repeats to lift the single-subject ceiling) — the only grounded path to rescue F1.

**Deferred/moot:** L4/F3 (fMRI-free proxy — moot, predicated on a null L3 benefit). **Not built:** LeBel transfer (underpowered, S8); E007 TR-lever (underpowered, E006).

## Doc-consistency — CLEARED (S8)
- `feghhi-2024` → `hadidi-2024` canonical redirect added (same paper). ✅
- R03/R04 checked: **no stale "E004 = headline" references** exist (0 E004 mentions). ✅

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
