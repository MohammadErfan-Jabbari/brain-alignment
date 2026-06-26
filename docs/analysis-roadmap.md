---
title: "Analysis-Week Roadmap — resume the analysis lane, get current, and write the paper"
tags: [methodology]
---

# Analysis-Week Roadmap — resume the analysis lane, get current, and write the paper

**Created:** 2026-06-14 (S14 close, by the agent, for Erfan's heavy analysis week starting 2026-06-15).
**Purpose:** a sequenced, pedagogical plan to (1) **resume** the frozen analysis lane (R05 was paused at end of
Q2; §9 = E005 is next), (2) **get current** on everything the implementation lane produced since (E015, E017,
E020, E019, and the S14 idea-refinement), (3) **learn alongside** — deepen the information-theory math while you narrate
it, and (4) **produce** the manuscript v1.0 with the S14 scope correction and refocused headline baked in.

> **⚠️ UPDATE (S16, 2026-06-16) — the OUTPUT layer changed; the reading/concepts/self-checks below are still valid.**
> **R05 is retired** (D036). The per-session deliverable is no longer "an R05 section" but a **finding-report**
> (`reports/R<NN>_*.md`): one Q-tagged claim per file, current-truth-only, each 1:1 with a manuscript Results section.
> Write them in the reading order of [`reports/README.md`](reports/README.md), through the `sci-write-v2` pipeline. Where a session below
> says "Produce: R05 §N", read it as "write/extend the corresponding finding-report":
>
> | This roadmap's session | Finding-report (output) | Status |
> |---|---|---|
> | (Q0/A2, was R05 §0–§8) | **R06** — signal real beyond confounds | ✅ written (S16) |
> | (Q1, was R05 §0–§8) | **R07** — plain KD does not preserve alignment | ⬜ **NEXT** |
> | (Q2, was R05 §0–§8) | **R08** — the lever is real but weak / ppl-confounded | ⬜ |
> | **Session A** (E005→E008) | **R09** — no per-individual gain; the averaging confound (parked `_pending-Q3_*.md`) | ⬜ |
> | **Session C** (E017 + convergence) | **R10** — the null is method-general | ⬜ |
> | **Session B** (E015 quality law) | **R11** — the quality law; matched-ppl is the missing control | ⬜ |
> | **Session D** (E020 ceiling — keystone) | **R12** — the ceiling, scoped honestly | ⬜ |
> | **Session E** (E019 reproduction) | **R13** — external reproduction corroborates | ⬜ |
> | (Q4/A3, E009) | **R14** — no practical payoff | ⬜ |
> | **Session F** (synthesis) | extended manuscript checkpoint (D035; on Erfan's call) | ⬜ |
> | **Session G** (adversarial review + figures) | review pass + figures | ⬜ |
>
> Reading order across the *finding-reports* is by Q-rung climb order (Q0→Q4); the session ordering below is the
> *pedagogical* order (the conceptual core, Session D, deliberately late). Both are fine — pick reports in the README's
> reading order, use the matching session below for the deep read + self-checks.

> **How to use this.** Each "Analysis Session" below is a self-contained chunk: a **goal**, what to **read** (in order),
> the **concepts to master** (with the course-note tie-in), what to **produce** (a concrete R05 section or manuscript
> edit), and a **self-check** (quiz / derivation) to confirm you actually understand it before moving on. Do them in
> order — each builds on the last. Pace is deliberately slow + math-grounded (your stated preference). The canonical
> status is always [`ladder.md`](ladder.md); this roadmap is the *plan*, the ladder is the *truth*.
>
> **Hard rule (D011, unchanged):** the analysis lane may only report numbers a working session actually recorded in
> `docs/`/`outputs/`. Every number below traces to an `experiments/` doc or an `outputs/` file — never invent or
> round-trip a number you can't point to. If a figure needs a number that isn't recorded, that's a gap to flag, not to fill.

---

## 0. Where we are — the one-screen status (read first)

**The result is in, and it is a well-powered, honest NEGATIVE — reframed into a positive methodological paper.**

- **A2 (is the signal real?) — ✅ PASS, powered.** A trained LM's middle layer predicts real fMRI beyond the full
  nuisance floor: trained−untrained unique-R² gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels,
  95–99% positive, contiguous splits (E006). The signal is real.
- **F1/Q3 (does optimizing brain-alignment buy a per-individual gain at matched perplexity?) — ❌ NULL, robust.**
  E005's apparent **+0.0081** headline collapsed to a per-individual **null** (E008: mean **+0.00010**, 95% CI
  **[−0.0004,+0.0006]**, n=9, MDE≈+0.0006) once measured per-subject instead of against a group-averaged target. The
  null survived every escape: capacity (E011), objective (E013b), substrate (E013), full-FT (E017, n=9, p=0.27), and
  was corroborated S14 by a faithful Negi reproduction (E019).
- **The positive contribution (the paper's spine):** a **measurement-validity finding + a control protocol.**
  Cross-subject target-averaging *manufactures apparent brain-specificity* (L016); the missing controls are
  **matched-perplexity + a per-kind permuted-brain twin**; and the reason is the **stimulus-predictability ceiling** —
  an LM aligns (almost) only to the stimulus-predictable part E[Y|S] of brain activity (E020, bounded; E015's
  quality-law is the mechanism).
- **S14 scope correction (the thing to internalize this week):** the spine's *operational* claim ("no brain-specific
  gain is **inducible** beyond perplexity via the readouts we tried") is what the evidence supports. The stronger
  *information-theoretic* statement ("the residual is task-independent noise") rests on **Y⊥θ\*|S as an assumption**,
  not a result. One genuine hole remains open and must be stated as such: a **DPI selection/regularization side-channel**
  (brain-as-prior improving generalization without moving the alignment metric) — argued-shut by E009's ~0 fulcrum,
  not measured-shut.

**The analysis lane was frozen at R05 §7 (end of Q2).** Everything from E005 onward — the would-be headline, its
collapse, the robustness escapes, the quality law, the ceiling, the reproduction, and the scope correction — is
**not yet narrated** in R05 and **not yet reframed** in the manuscript. That is this week's work.

---

## 1. The refocused thesis, in one paragraph (the destination)

> **"Brain-tuning gains in language models are an LM-quality / fine-tuning-regime artifact, not per-individual brain
> signal. We supply the two controls the brain-tuning literature omits — perplexity-matched fine-tuning and a
> permuted-brain twin — and show: (a) a well-powered per-individual null where cross-subject averaging manufactures
> apparent brain-specificity; (b) that an LM aligns essentially only to the stimulus-predictable part E[Y|S] of brain
> activity (a stimulus-predictability ceiling); (c) that this is the same quality-dependence that makes 'brain-specific'
> gains track perplexity (the cross-family bits-per-byte law). A faithful reimplementation of a published brain-tuning
> positive corroborates the failure."**

This replaces the dead "brain-guided distillation works" framing (the nulls killed it). The lit scan (S14) confirms it
is **not scooped**: the published critiques (Hadidi/Feghhi Nature-Comms 2026; Jia L-PACT 2026) attack *frozen-model
encoding scores*, not *brain-tuning*, and none use a perplexity-matched control or identify the averaging confound.

---

## 2. The session sequence (do in order)

### ▶ Analysis Session A — Resume the narrative: the headline that wasn't (E005 → E008 → Fork-B)
**This is the frozen resume point. R05 §9 onward.**
- **Goal:** narrate *the* turn of the thesis — E005's apparent +0.0081 brain-specific gain, and why it collapsed to a
  per-individual null. Understand the **averaging confound** deeply; it is the paper's most defensible result.
- **Read (in order):** `docs/reports/R05_*.md` §7–§8 (re-read the resume point) → `experiments/E005_*.md` (the apparent
  headline) → `experiments/E008_*.md` (the per-individual solidification → null) → [`learnings.md`](learnings.md) L014, **L016** (the
  averaging confound, the heart of it), L015 (the pseudo-replication catch) → `docs/literature/canonical/
  lage-castellanos-2019_fmri-noise-ceiling.md` (the noise-ceiling-of-an-average math).
- **Concepts to master:**
  - *Why a group-averaged target inflates apparent specificity.* Averaging k subjects raises the noise ceiling toward
    the shared (stimulus-evoked) component; a "brain-specific" gain measured against that average reads as real (it beats
    a permuted twin) even when *no individual subject shows it*. The +0.0081→+0.00010 ~80× collapse is the signature.
  - *Pseudo-replication* (L015): 15 cells over one 5-UID-averaged target is **not** n=15; the legitimate replication
    unit is the independent subject/stimulus. This burned the program repeatedly (L015/L016/L018/L020) — know it cold.
  - **Course tie-in:** conditional MI = unique R² ([`06-theory-grounding.md`](06-theory-grounding.md) §3, info-theory lecture 4) — what "unique
    variance beyond nuisance" *means* information-theoretically.
- **Produce:** R05 **§9 (E005)** + **§10 (E008, the collapse)** — the living narrative, in your slow math-grounded
  voice. Mark §11–§14 placeholders for the robustness escapes.
- **Self-check (answer before moving on):**
  1. In one sentence: *why* does cross-subject averaging make a non-existent per-individual effect look brain-specific?
  2. E008's CI is [−0.0004,+0.0006] with MDE≈+0.0006. Explain why that makes it a *true* null and not an
     underpowered one (what would an underpowered null's CI look like instead?).
  3. Open-ended: if a reviewer says "but 7/9 subjects had positive *encoding* scores (L028), so the per-individual
     signal IS there" — reconcile that with E008's null. (Hint: REAL ≠ MOVABLE ≠ USEFUL; R05 §7.)

### ▶ Analysis Session B — The quality law: why "brain-specific" gains track perplexity (E015 / I1)
- **Goal:** understand the cross-family **alignment ∝ −bits-per-byte** law and why it is the *mechanism* behind
  "matched-perplexity is the missing control." Internalize the r≈−0.92 → −0.78 correction.
- **Read:** `experiments/E015_*.md` → [`learnings.md`](learnings.md) **L034** (the −0.78 correction; bpb not per-token-ppl + the
  single-model scoring bug) and **L035** (unique-R² over a low-level nuisance can't separate "matches brain computation"
  from "encodes the stimulus") → `docs/literature/canonical/antonello-2023_*.md`, `gao-2024_*.md` (scaling anchors) →
  the new `raugel`/King NeurIPS-spotlight note if digested (size+context vs our bpb framing).
- **Concepts to master:**
  - *Why bits-per-byte, not per-token perplexity* (L034): per-token NLL is tokenizer-confounded across families — it
    misranks capability. bpb normalizes by bytes → a fair cross-family quality axis.
  - *The deep point (L035):* if a better LM encodes the *stimulus* better, then alignment-to-an-averaged-target rises
    with quality **without any "brain-matching"** — so a "brain-specific gain" that isn't perplexity-matched is
    confounded with quality. This is *why* the control is necessary, stated as a property of the measure itself.
  - **Course tie-in:** rate–distortion (`06` §4, lecture 1) — quality as the rate axis; the alignment-quality coupling.
- **Produce:** R05 **§(new) — the quality law** + the **manuscript correction**: every "r≈−0.92" → the 3-part argument
  (full-range −0.78 / scale-controlled partial −0.675 / operative capable-band ≈−0.48 with CI incl. 0). Drop any
  standalone in-band claim.
- **Self-check:**
  1. Why would a "brain-specific alignment gain" measured against a vanilla (non-ppl-matched) baseline be misleading,
     in terms of the quality law?
  2. The capable-band coupling CI includes 0. What is the honest claim the law supports, and what is the over-claim?

### ▶ Analysis Session C — The induction null is method-general (E017 + the convergence)
- **Goal:** see that the per-individual null is not one experiment but a *convergence* across every axis — capacity,
  objective, substrate, parameterization (LoRA/full-FT). Understand the DPI argument for why.
- **Read:** `experiments/E017_*.md` (full-FT, n=9) → `learnings.md` **L036** (method-general lever failure + the
  catastrophic-forgetting trap: a gentle-LR n=1 flip washed out when powered) → re-skim E011/E013/E013b records →
  [`06-theory-grounding.md`](06-theory-grounding.md) §2 (DPI) + info-theory lecture 6 (`6_..._DPI_SourceCodingI_study.md`).
- **Concepts to master:**
  - *Data-processing inequality:* along θ\*→S→R(S)→Y, I(θ\*;Y) ≤ I(θ\*;S) — brain-as-data cannot carry more about the
    optimal parameters than the stimulus already does. This is the spine's theoretical backbone (and its limit — see Session D).
  - *Catastrophic forgetting as a confounder of induction tests* (L036): an aggressive full-FT can both *mask* a real
    signal and *mimic* one; always match perplexity AND check the permuted twin AND power it before believing a flip.
- **Produce:** R05 **§(new) — the robustness escapes + convergence**; the manuscript's "the null survives every door" subsection.
- **Self-check:**
  1. List the axes the null survived (capacity / objective / substrate / parameterization) and the experiment for each.
  2. What single result would have *broken* the null (a Fork-A)? Why didn't any appear?
  3. Derive (informally) why DPI says brain-as-data can't beat stimulus-as-data — and name the one channel DPI does NOT
     close (Session D).

### ▶ Analysis Session D — The ceiling and its honest scope (E020 + the S14 scope correction) — THE conceptual core
- **Goal:** understand the E[Y|S] stimulus-predictability ceiling, why it came back *bounded-not-closed*, and the scope
  correction that keeps the whole thesis honest. **This is the most important conceptual session of the week.**
- **Read:** `experiments/E020_*.md` IN FULL (§1, §v2, §v2.1, the VERDICT) → `learnings.md` **L039** (a shared-LM probe
  of a leave-one-subject-out residual is ~0 *by construction*), **L040** (a content-laden eng1000 nuisance-partial can
  *vacuously* collapse any LM alignment — test with the symmetric partial), **L041** (the scope correction + the DPI
  side-channel + Negi-passes-permuted) → [`decisions/decisions.md`](decisions/decisions.md) **D029/D030/D034** → `06-theory-grounding.md` §2–§3.
- **Concepts to master:**
  - *The decomposition* Y_subj = E[Y|S] + ε_subj, and why, for the *true* conditional mean, Cov(R(S),ε)=0 follows from
    the **conditional-mean projection** (ε ⟂ any function of S) — *not* specifically from Y⊥θ\*|S. Against the *empirical*
    leave-one-out mean, A_resid is a **positively-biased bound** whose bias is leaked stimulus (the L016 confound
    displaced into the residual) — which is exactly the +0.090 artifact E020 caught.
  - *Why A_resid≈0 is expected by construction* (L039): a *shared* LM R(S) cannot track *idiosyncratic* per-subject
    deviation; the LOO subtraction removes everything shared. So E020 **confirms + bounds + guards**, it does not prove.
  - *The operational vs information-theoretic claim (L041):* what we measured = "not inducible via these readouts";
    what Y⊥θ\*|S would assert = "the residual is θ\*-noise." State the assumption as an assumption.
  - *The DPI selection side-channel (the open hole):* DPI bounds the *information* channel; it does NOT bound a
    *selection/regularization* channel (a brain prior that improves generalization — lecture-26 I(W;Z^n), a different MI
    object — without moving the alignment metric). Argued-shut by E009 (fulcrum ~0), not measured-shut.
  - *Why the ceiling is instrument-limited on ALL substrates (D034):* TRIBE too weak (L038), denizenslab n=6 walled
    (ref-rel 0.33, L040), LeBel n=3 worse (n_ref=2) + no cross-subject mapper. It rests as bounded corroboration.
  - **Course tie-in:** conditional-mean projection / L²(σ(S)) geometry; DPI (lecture 6); the generalization bound (lecture 26).
- **Produce:** R05 **§(new) — the ceiling, scoped honestly**; and the **keystone manuscript edit**: restate the spine
  as the operational/inducibility claim, name Y⊥θ\*|S as an assumption, and add a short paragraph carving out the
  unmeasured DPI selection side-channel. (This is the single highest-value analysis-lane fix — a `first-principles`
  reviewer catches the over-claim otherwise.)
- **Self-check:**
  1. Why is A_resid≈0 the *expected* result for a shared-LM probe of a LOO residual — independent of whether Y⊥θ\*|S
     is true? What, then, does E020 actually contribute?
  2. The eng1000 nuisance-partial collapsed A_resid +0.090→−0.008 — why was that NOT clean evidence, and what did the
     *symmetric* partial (it also collapsed A_shared +0.176→+0.033) reveal?
  3. State the operational claim and the information-theoretic claim in your own words, and the exact gap between them.
  4. Name the one channel the DPI does not close, and the experiment (E009) that argued — but didn't measure — it shut.

### ▶ Analysis Session E — The external reproduction + the literature gap (E019 + related work)
- **Goal:** understand what E019 establishes (and, crucially, what it does *not*), and lock the related-work positioning.
- **Read:** `experiments/E019_*.md` (all versions + the VERDICT) → `learnings.md` **L042** (corroboration not clincher;
  the raw-mean-r ruler is quality-blind) → `decisions/decisions.md` **D031/D032** → the new canonical note
  [`docs/literature/canonical/jia-2026_lpact-prediction-scores-not-enough.md`](literature/canonical/jia-2026_lpact-prediction-scores-not-enough.md) → [`01-research-landscape.md`](01-research-landscape.md) (the Jia row
  + Hadidi→Nature-Comms cite) → `negi-2025_*.md` (the reproduction target; note Negi *passes* the permuted twin Δr=0.133
  on encoding, so our encoding clincher must be matched-ppl, not permuted — L041).
- **Concepts to master:**
  - *Why E019 is corroboration, not the clincher:* no positive gain reproduced at any lr (gentle = no representational
    movement, Δppl≈0; stronger = catastrophic forgetting), AND the raw-mean-r metric is quality-insensitive (eval
    positive-control: enc_r 0.5B +0.150 ≈ 3B +0.143 — `outputs/E019_negi/eval_posctrl.json`), AND decoder≠Negi's BERT.
    So it converges with the E008/E011/E017 lever-failure spine without claiming "Negi is wrong."
  - *The metric-validity point:* raw encoding scores hide the quality dependence that unique-R² reveals — this is *why*
    the project uses unique-R² (ties L035 + Hadidi + Jia-L-PACT's "scores aren't enough").
- **Produce:** R05 **§(new) — the external reproduction**; the manuscript's **Related Work** (frozen-encoding critiques
  are the foundation to build on; we extend the rigor from *measuring* alignment to *training on* it) + the honest E019
  paragraph (scoped to "our faithful-as-feasible reimplementation on a 0.5B decoder").
- **Self-check:**
  1. State the *defensible* one-sentence claim E019 supports, and the *over-claim* it does not.
  2. Why is matched-perplexity (not the permuted twin) the load-bearing control for Negi's encoding gain specifically?
  3. How do we stay distinct from Jia-L-PACT and Hadidi/Feghhi (name the three differentiators)?

### ▶ Analysis Session F — The synthesis: manuscript v1.0 reframe (the capstone)
- **Goal:** assemble the refocused paper. Apply the scope correction throughout; make the powered nulls the spine and
  E019/E020 the corroboration.
- **Read:** [`docs/manuscript/00_paper-draft-v0.md`](manuscript/00_paper-draft-v0.md) IN FULL → this roadmap §1 (the headline) → [`ladder.md`](ladder.md) (the spine
  wording, post-S14) → the framing note `brain-alignment-thesis-framing-s14` (gbrain) if reachable.
- **Produce (manuscript edits — this is the analysis lane's main output):**
  - **Abstract + Intro:** reframe to the control-protocol + per-individual-null + E[Y|S]-ceiling headline.
  - **Spine statement:** operational claim; Y⊥θ\*|S as assumption; the DPI side-channel paragraph (Session D output).
  - **Results spine:** A2 (E006) → the averaging confound + per-individual null (E005→E008, L016) → the convergence
    (E011/E013/E017) → the quality law (E015) → the bounded ceiling (E020) → the reproduction corroboration (E019).
  - **Numbers audit:** every figure/number traces to an `outputs/` file (D011). Fix the r≈−0.92→−0.78 throughout.
- **Self-check:** can you state, for each results section, the exact number-with-uncertainty and the `outputs/` file it
  comes from? (If any floats free, it's a gap to flag.)

### ▶ Analysis Session G — Adversarial self-review + figures (harden before it lands)
- **Goal:** stress-test the draft and confirm the figures render the recorded numbers.
- **Do:**
  - Run the thinking panel on the manuscript draft (counter-argument + premortem + first-principles, opus) — find the
    holes a reviewer would, address until none survive. (This mirrors how E020/E019 were hardened.)
  - **Figures** (`scripts/figures/make_figures.py`): confirm the 4 render the recorded numbers — averaging-collapse
    (Fig 2), powered A2 (Fig 3), A3 nulls (Fig 4), dose-response-with-caveat (Fig 1). Add a 5th if the ceiling/quality-law
    deserves one.
  - **Venue/length** decision (thesis chapter + workshop/conference cut).
- **Produce:** manuscript v1.0, mock-review-hardened; a short "open questions" box (the DPI side-channel; the
  instrument-limited ceiling; the architecture-residual Q2).
- **Self-check:** would the draft survive the three differentiators being challenged? Is every caveat *in* the claim
  sentence (the E019/E020 lesson) rather than buried?

---

## 3. The "learn-alongside" thread (deepen the math while you narrate)

Each session above has a course tie-in; here is the spine of it, so you build the information-theory backbone as you go.
Source notes live under `data/course-material/info-theory-course/` (the `*_study.md` notes; mapped in `06-theory-grounding.md`).

| Concept | Where it bites in the thesis | Course note | Master it well enough to… |
|---|---|---|---|
| **Conditional MI = unique R²** | the whole alignment measure (A2, the nulls) | lecture 4 (`4_..._RelativeEntropy_MI_Jensen_study.md`) | …explain what "unique variance beyond nuisance" means as an MI quantity |
| **Data-processing inequality** | the E[Y|S] ceiling; "brain can't beat the stimulus" | lecture 6 (`6_..._DPI_SourceCodingI_study.md`) | …state the ceiling AND its one loophole (the selection side-channel) |
| **MI generalization bound** | the selection/regularization side-channel | lecture 26 (`26_generalization_error_bounds_OCR.md`) | …explain how a prior could help OOD via I(W;Z^n) without moving alignment |
| **Rate–distortion** | the quality law; the F1 trade-off framing | lecture 1 (`1_InfTh_Intro_study.md`) | …frame quality (rate) vs alignment (distortion) — and NOT over-apply it to E020 (which is a DPI/conditional-mean statement, not R-D) |
| **Noise ceiling of an average** | the averaging confound (L016) | `lage-castellanos-2019_*.md` (canonical) | …derive why k-subject averaging inflates the apparent ceiling |

**Quiz cadence (your stated preference):** at the end of each session, do the self-check; for the math, re-derive the
relevant bound from the course note *without looking*, then check. Vary it — sometimes a hard MCQ, sometimes
"explain it to a skeptic." If a derivation won't come, that's the gap to close before narrating that section.

---

## 4. The honest open questions to hold in mind (don't paper over these)

1. **Y⊥θ\*|S is an assumption.** The ceiling/spine rests on it. State it as an assumption; the powered nulls
   (E008/E011/E017) are the *empirical* leg, the assumption is the *interpretive* leg.
2. **The DPI selection side-channel is argued-shut, not measured-shut.** A brain-as-regularizer improving OOD without
   moving the alignment metric is the one door the linear-ridge/encoding experiments don't measure (E009 aimed at it
   but was null-by-construction — fulcrum ~0). Name it as a limitation; it's also the most honest "future work."
3. **The E[Y|S] ceiling is instrument-limited** (bounded-not-closed on all substrates, D034). The clean version needs
   ≥3 more deep LeBel subjects with the 10-repeat story (data acquisition, not a re-run). Frame the ceiling as
   *convergent corroboration* of the nulls, not a standalone closed result.
4. **E019 reproduction is faithful-as-feasible, not identical** (Qwen decoder vs Negi's BERT; window-TR vs batch
   NT-Xent). Own these caveats *in* the claim; do not claim "Negi doesn't reproduce" full-stop.
5. **The architecture-residual Q2 (E015)** is underpowered (p=0.20). Either bury it or flag it as future work — don't
   lean on it.

---

## 5. Working-lane items parked (for reference; NOT this week's analysis work)
- **F3 (denizenslab n=6 full-FT)** — superseded/moot (D033); run only for literal 100%-rule coverage.
- **F4 (E015 Q2 extension)** — add Llama/Mistral sizes at matched bpb; an extension, not decisive.
- **Ceiling closure** — needs deep-LeBel-subject acquisition (D034); a data decision.
- **TRIBE Phase 3** — optional synthetic-target Fork-B booster (E016 §5).
None of these block the paper; the spine is fully supported by powered evidence already recorded.

---

**Bottom line:** the experiments are done and honest; this week is about *understanding* the arc deeply enough to write
it, *correcting* the over-claims (the scope correction is the keystone), and *producing* a manuscript whose every
caveat is in the claim. Resume at R05 §9 (Session A); the keystone conceptual session is D (the ceiling + scope
correction); the capstone is F (the manuscript reframe). Learn the five bounds in §3 as you go.


## Related
- [`ladder.md`](./ladder.md) — the canonical status board
- [`map.md`](./map.md) — code system (Q/E/A/D/L) & journey map
