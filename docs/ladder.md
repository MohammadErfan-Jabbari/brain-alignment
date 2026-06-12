# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

**Last updated:** 2026-06-13 (S12 autonomous working — **I1 DONE** (E015 expanded to 22 models/6 families; cross-family law corrected to **r≈−0.78** on bits-per-byte, was an inflated −0.92; Q2 architecture-residual = underpowered hypothesis; L016 tie-in). **No rung flipped** (E015 = analysis-support). Now on **I2** (matched-ppl control; reframed to LeBel full-FT since Negi bilingual data is unavailable). Roadmap I1✅→I2(now)→I3→I4. Analysis lane frozen at R05 §9. Prior: S8 per-individual null robustified; manuscript v0.9 artifact-complete. **Analysis-lane FLAG: manuscript "r≈−0.92" → correct to ≈−0.78.**)

---

## Current position

**The honest story (post-E008 reframe).** Brain alignment is **robustly real and measurable** (L0/A2, powered at voxel scale — E006). But **optimizing it does NOT produce a per-individual brain-specific alignment gain**: E008 (per-participant, n=9, well-powered, MDE≈+0.0006) returns a clean **NULL** (mean +0.00010, CI [−0.0004,+0.0006]). E005's headline +0.0081 was a **group-averaged-target** measurement — a higher-SNR read of the *shared stimulus-evoked response*, inflated ~1.7× by averaging and ~2.4× by one outlier fold — **not** per-person brain alignment.

**The POSITIVE contribution (the paper's spine — S8 panel, do not bury it as a "null"):** a **methodological finding + a confound-clean protocol**. The finding: **cross-subject target-averaging manufactures apparent brain-specificity** — a gain measured against a group-averaged fMRI target reads as "brain-specific" (beats a permuted twin) even when *no individual subject shows it*, because averaging amplifies the shared stimulus-evoked component at an inflated noise ceiling (the +0.0081→+0.00010 ~80× collapse, E008/L016). The protocol that detects it — **matched-perplexity + per-kind permuted-twin + per-subject inference with crossed subject/fold clustering** — explains a class of overclaims in the alignment-*training* literature (Negi/Schwartz baseline against non-ppl-matched vanilla models; this is the control they lack). **Fork B = a positive method + corrected claims:** (1) A2 real & powered; (2) **the averaging-confound finding + protocol** (the positive contribution); (3) the well-powered per-subject null; (4) **A3 — practical payoff** (E009, in progress).

**→ The experimental program is CLOSED, and the per-individual null is ROBUST across every axis we could probe.** A2 holds (powered); F1 and A3 are characterized nulls; the null survived four escape attempts run + panel-bounded this session — **LoRA capacity** (E011, heavy LoRA leaves it intact), **objective** (E013b, contrastive/InfoNCE ≈ MSE, both null), **substrate** (E013, the voxelwise distillation lever fails to take hold at any λ — a mechanism failure, not a power limit), and the **measurement side** (E014, averaging the *encoding* score is legitimate-SNR/estimand, not a second confound). L4/F3 is moot. The manuscript (v0.9) is **complete as an artifact** (panel-converged, references verified, cross-refs resolve; gate = READY thesis/workshop). **We are now in the write-up phase.** The one untested door is a *different induction method* (full-FT on multi-subject naturalistic voxelwise — scoped as the next major build, §"Next session"). Details below.

> **Audit trail (S8, 2026-06-11, Erfan-confirmed):** the thinking-panel (counter-argument + premortem + first-principles, fable) caught — *before* compute — that E005's "CI excludes 0" was pseudo-replicated (15 cells over one 5-UID-averaged target) and that the planned LeBel transfer test was underpowered (`scripts/reanalyze_e005_e006.py`, L015). The pivot to a per-subject solidification (E008) then returned a well-powered null (L016), confirmed by a second panel. Rigor before compute caught an overclaim that would have been the thesis headline.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **L0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS (powered)** | **E002** (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 nuisance, story-CV. Clears the Hadidi/Feghhi 2026 bar. |
| **L2a** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **L1** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | 🟡 **PARTIAL** | **E004** — brain loss built (loss family; D010 → co-trained MSE leaning). Brain-SPECIFIC lever exists on the strong aligner (Qwen mse − its permuted twin = **+0.0032 [+0.0006,+0.0058]**), but small/fragile (fold-4 carries half) & sub-threshold on the 5-ROI screen (no arm raised Δ above base; MDE limits). `frozen`=non-specific regularizer; cka/cos worst. Co-varies w/ perplexity (L011/L012). |
| **L3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → per-individual brain-specific gain? | brain term buys ~0 alignment at matched perplexity (paired, powered) | ❌ **NULL per-subject — ROBUST across capacity/objective/substrate** (averaged-target-only artifact) | **E008** (n=9, MDE≈+0.0006): mean +0.00010, t-CI **[−0.0004,+0.0006]**, fold-clustered incl 0, the 4 E005-averaged subjects individually null. Sensitivity sim: power 1.0 at δ=+0.003 → a TRUE null. **Robust to every escape:** **E011** (heavy LoRA r64/6ep) — null holds, +0.0004 (capacity didn't move the rep; λ that does wrecks ppl, L019); **E013b** (contrastive/InfoNCE objective, n=9) — null holds, −0.0002 at matched ppl (L025); **E013** (voxelwise same-substrate, λ-sweep UTS01/02/03) — the distillation lever never improves held-out alignment over base and never beats its permuted twin, a single-subject *mechanism* failure so n≥5 is moot (L026/L027). E005's +0.0081 was a group-averaged / shared-stimulus-response artifact, NOT per-person alignment. → Fork B. **One untested door:** a *different induction method* — full-FT (not a LoRA distillation readout) on multi-subject naturalistic voxelwise (denizenslab n=6; queued as next major build). |
| **L2b · A3** | Does induced alignment *buy something practical* (OOD) at matched perplexity? | gains stay confined to the alignment metric | ❌ **bounded NULL** (E009, n=8, panel-adjudicated) | No brain-specific OOD-ppl payoff (kd_brain ≈ kd_brain_permuted ≈ textfeat ≈ kd_ppl, all within measured MDE 0.03–0.13) — AND **null-by-construction**: the fulcrum (brain-specific repr change at matched ppl) is itself ~0 (median +0.004, seed-0-outlier-driven; can't grow it without collapsing ppl). Ties to E008/L016. Negi-2025's positive is vs a non-ppl-matched baseline (L011 confound) — our matched-ppl+permuted control is the contribution. Limits: OOD-ppl is a weak proxy; perturbation/sample-eff axes not run (moot with fulcrum ~0). L017. |
| **L4 · F3** | An fMRI-free *proxy* (neighborhood-overlap / LID surrogate) that recovers most of the benefit | surrogate recovers little of the L3 benefit | ⬜ **not started** | stretch / PhD seed. LID sign is unsettled (cheng vs yu) — validate direction against real fMRI first. |

## Supporting tracks (not rungs, but gate the rungs)

| Track | Status | Note |
|---|---|---|
| Data — Tuckute 2024 | ✅ staged + in use | ROI-level screen (5 LH lang ROIs), `data/tuckute2024/` |
| Data — LeBel UTS03 voxelwise | ✅ **built + run (E006)** | adapter `scripts/lebel_adapter.py` (reuses official deep-fMRI-dataset pipeline); CC_norm voxel selection; powered A2 confirmed |
| Literature | ✅ done | R03, R04, 14 canonical notes (+ hadidi-2024 anti-confound bar; lit-fork sweep leans B) |
| Manuscript v0.9 | ✅ artifact-complete + mock-peer-reviewed | PASS thesis / borderline-PASS workshop (oracle+premortem+counter-argument, fable, L029). Power claim hardened with a real-residual bootstrap positive-control (group test power 0.92@uniform-δ=+0.002, first-principles VALID). **E015** folded in: cross-family alignment∝−ppl law (r≈−0.92, −0.929 middle / −0.917 best-layer, gpt2/pythia/Qwen) strengthens the matched-ppl control (L030). **E014** (`experiments/E014`): averaging the *encoding* brain-score is legitimate higher-SNR/estimand (per-subject positive), NOT a second confound → verified NOT-a-lift, correctly kept OUT of the paper (L028). **Open (Erfan/fresh build):** the premortem's spine reframe → matched-ppl-as-missing-control demonstrated on an external result. |
| Theory grounding | ✅ done | `06-theory-grounding.md` (MI bound, DPI, conditional-MI, rate-distortion) |
| Harness | ✅ **`$\mathcal{L}_{\text{brain}}$` built** | `brain_loss.py` (mse/cos/pearson/frozen/cka + block_permute); `run_brain_lever.py` (LoRA brain-tune); `run_lebel_encoding.py` (powered voxelwise); `distill.py` λ_brain |

Legend: ✅ done · 🟡 partial / in progress · 🔵 next (designed) · ❌ tested-negative / kill fired · ⬜ not started.

---

## Next session (what `/orient` surfaces)

**TWO PARALLEL LANES (D020) toward the dual meta-goal (D022): finish the MSc thesis AND extract ≥1 top-venue
AI paper.** The closed-rung *verdicts* (the per-individual null etc.) stand — what reopened (Erfan, 2026-06-12)
is an **implementation roadmap** that pursues the remaining *untested doors* and a new capstone, run autonomously
while Erfan studies in the analysis lane.

- **🔬 IMPLEMENTATION lane (autonomous working sessions) — an ORDERED ROADMAP, do in sequence (`tasks.md`):**
  **I1 ✅ DONE (2026-06-13)** — E015 expanded to 22 models/6 families; cross-family law corrected to **r≈−0.78**
  (bits-per-byte; v2's −0.92 was inflated by per-token-ppl + best-layer + 3-family span); operative-band ≈−0.48;
  Q2 architecture-residual = underpowered hypothesis (Llama/Mistral +0.006–0.009, n=1–2/family); L016 tie-in.
  Full oracle+panel+Codex audit; L034/L035; no rung flip (analysis-support). →
  **I2 (NOW)** the matched-ppl control on a brain-tuning gain. Negi-2025's literal multilingual pipeline is
  INFEASIBLE (no Chen-2024b bilingual fMRI) → **reframed: reproduce a brain-tuning encoding gain on LeBel
  (full-FT, vanilla baseline) + the matched-ppl/generic-finetune arm + permuted-brain twin Negi omits**
  (uses `run_lebel_tune.py`; also advances I3's full-FT door). headline/spine-call = **Erfan (STOP)** → **I3**
  full-FT multi-subject voxelwise (denizenslab n=6, blocked on git-annex) → **I4 CAPSTONE** E016 TRIBE-v2
  (P0 gate PASS; D021). After every step: thinking panel (D017) + Codex (D019) until no hole survives; record;
  **no rung flips without Erfan.**
- **📖 ANALYSIS lane (Erfan) — FROZEN at its resume point:** the get-up-to-speed walk resumes at **Layer 3 = E005**
  (apparent +0.0081 → E008 per-individual null) = R05 §9 → §14; then figures-check + manuscript read-through.
  Working sessions must NOT edit the analysis-lane docs (R05, manuscript, E005–E014 records).

**The manuscript (v0.9) is content-complete + panel-converged + artifact-complete** (`docs/manuscript/00_paper-draft-v0.md`): references verified, cross-refs resolve, gate = READY (thesis/workshop). Headline = the well-powered per-individual NULL + the averaging-confound measurement-validity result; the dose-response (E010/E010b) is hedged, not load-bearing.

**Analysis-session backlog (get-up-to-speed, in order):**
1. **Walk R03→now** — IN PROGRESS (S9): Layer 0 + Layer 1 done, captured in the new LIVING report `docs/reports/R05_thesis-narrative-from-first-principles.md` (pedagogical, course-grounded) + the new `docs/07-concepts-primer.md`. **Resume at Layer 3 = E005** (apparent +0.0081 → E008 per-individual null) → robustness escapes (E011/E013b/E013/E014) → Fork-B reframe; each becomes R05 §9–§14. Source: `docs/experiments/ENNN_*.md` + `learnings.md` L011–L030.
2. **Figures:** confirm the 4 figures (`scripts/figures/make_figures.py`) render the recorded numbers — averaging-collapse (Fig 2), powered A2 (Fig 3), A3 nulls (Fig 4), dose-response-with-caveat (Fig 1).
3. **Manuscript read-through** for thesis/workshop submission: resolve venue/length, optional §2 prose polish; the 5 reference [VERIFY] flags are now cleared (lit-scout, 2026-06-12).

**Queued next MAJOR build (item 2, a fresh WORKING session — Erfan-approved as a possible next step):** the one untested door — **full fine-tuning (not a LoRA distillation readout) on multi-subject naturalistic voxelwise targets** (denizenslab n=6; `data/paper-repos/speech-llm-brain`). Scoped in `docs/experiments/E013_*.md`. The distillation-readout lever's failure (E013) is n-independent, so the ~5-deep-subject power (L024) applies only to this full-FT route, *conditional on it first inducing an above-base improvement*. Mechanism evidence suggests likely-null, but it is the only path that could move the per-individual verdict toward Fork-A. **A multi-day build — launch fresh, not at a session tail.**

**Deferred/moot:** L4/F3 (fMRI-free proxy — moot, predicated on a null L3 benefit). **Not built:** LeBel transfer (underpowered, S8); E007 TR-lever superseded by E013's voxelwise loop.

## Doc-consistency — CLEARED (S8)
- `feghhi-2024` → `hadidi-2024` canonical redirect added (same paper). ✅
- R03/R04 checked: **no stale "E004 = headline" references** exist (0 E004 mentions). ✅

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
