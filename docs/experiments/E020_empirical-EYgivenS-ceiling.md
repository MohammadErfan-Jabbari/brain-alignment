---
title: "Experiment E020 — the empirical-E[Y|S] ceiling (TRIBE-free): does the LM align to brain signal…"
tags: [experiment]
aliases: [E020]
---

# Experiment E020 — the empirical-E[Y|S] ceiling (TRIBE-free): does the LM align to brain signal beyond the stimulus-predictable part?

**Created:** 2026-06-14 (S13) · **Status:** **COMPLETE — the apparent residual was explained by reference unreliability and leakage/autocorrelation; the clean controlled residual was bounded, but this failed instrument does not close the general ceiling question.** Replaces the walled TRIBE
stimulus-subtraction ceiling (E016 Phase 2 / Step 9) per **D028**. · **Mode:** working (design→run→judge)
**Origin:** E016 Phase-2 hit a wall — TRIBE estimates E[Y|S] at only ~7% of per-vertex real-BOLD variance on
story-listening, too weak to subtract (L038). The fix (Erfan-agreed): use the **ground-truth empirical E[Y|S]**
(the cross-subject + cross-repeat average of real fMRI) as the ceiling reference — it *is* the stimulus-evoked
expectation by definition, and is strictly stronger than any model estimate where many subjects heard the same
stimulus. denizenslab gives exactly this (n=6 subjects, story_11 has 2 repeats).

## 1. The question (the spine, made measurable without TRIBE)
Markov chain θ\*→S→R(S)→Y, with **Y ⊥ θ\* | S** (assumption). Decompose Y_subj = E[Y|S] + ε_subj. By Y⊥θ\*|S, the
residual ε_subj is θ\*-independent given S. The LM rep R(S) is a deterministic function of S (via θ\*). **Predicted:
the LM aligns to E[Y|S] (the A2 signal) but NOT to ε_subj → the ceiling on brain-guided training is the
stimulus-predictable part.** This is the cleanest, ground-truth statement of the ceiling and the unifying spine
(subsumes E008 per-individual null + L016 averaging confound + the E015 quality law + the induction nulls).

## 2. Design (LOCKED skeleton — oracle-gate before running)
Substrate: denizenslab, fsaverage5 (reuse `scripts/fsaverage_mapping.py`), n=6 (01/02/03/05/07/08). Use stories
with the alignment signal; story_11 (2 repeats → noise ceiling) is primary, ≥2 train stories for replication.
LM: trained Qwen2.5-0.5B verdict layer (+ ≥3 untrained-seed floor) — reuse `run_tribe_ceiling.lm_grid` /
`lebel_adapter.lm_word_features`. Encoding via the Phase-1 ridge machinery (`run_tribe_fidelity.ridge_cv_pred`,
contiguous-block CV, per-fold centering).
- **E[Y|S] estimate:** mean of real fMRI over subjects (+ over the 2 repeats for story_11), in fsa5. The
  leave-one-subject-out average (E[Y|S] from the OTHER 5 subjects) avoids leakage when testing subject s.
- **Residual:** ε_s = Y_s − E[Y|S]_{-s} (leave-one-out, so ε_s is not trivially anti-correlated with the estimate).
- **Two alignments (NC-normalized, higher-language ROIs):** A_shared = LM→E[Y|S]; A_resid = LM→ε_s. Decision:
  A_resid ≈ 0 (within MDE) while A_shared > 0 ⇒ ceiling = E[Y|S] ⇒ **Fork-B.** A_resid > 0 surviving the controls
  ⇒ **Fork-A → STOP for Erfan.**

## 3. The subtlety that MUST be handled (oracle Q1/Q4 carry-forward — the reason not to rush this)
ε_s = subject-specific **stimulus-evoked deviation** + subject noise. The first part is still *stimulus-driven* —
a stimulus-locked LM could align to it WITHOUT it being "non-stimulus" signal. So a naive A_resid > 0 is NOT
automatically Fork-A. Required controls:
1. **Untrained-LM floor** (≥3 seeds): the verdict is **(trained A_resid − untrained A_resid)** — absorbs capacity
   bias + any architectural/low-level stimulus-locked alignment to ε.
2. **Pre-registered MDE** (fold-variance; E006 machinery). A single story → a residual *bound*, not a clean null;
   ≥2-3 stories to break the n=1-stimulus pseudo-replication.
3. **Noise-ceiling bound:** A_resid is capped by ε's own reliability — report A_resid relative to the NC of ε.
4. **Asymmetric Fork-A bar:** trained−untrained A_resid excludes 0, survives the NC bound, replicates across
   stories — anything less = Fork-B/HOLD, not a STOP. (Same discipline that correctly caught the TRIBE false Fork-A.)

## 4. Why this is the right F1-close (not more TRIBE grinding)
The empirical E[Y|S] is the ceiling reference TRIBE was approximating, available here at ground truth and far
stronger. Closing the ceiling this way is cheap (data + machinery already built S13), TRIBE-free, and airtight.
TRIBE's irreplaceable use (Phase 3: synthetic targets for the no-fMRI KD corpus) is a separate, optional Fork-B
booster (E016 §5 Phase 3). **After E020 closes F1 → F2 (E019), the paper-critical experiment.** (D028.)
**Reuse map:** `fsaverage_mapping.py` (voxel→fsa5 + ROIs), `run_tribe_fidelity.py` (load_real+NC, ridge_cv_pred,
ROI groups, NC-norm), `run_tribe_ceiling.py` (lm_grid, untrained-seed loop, the verdict/MDE scaffolding — adapt the
targets from {real,TRIBE} to {E[Y|S]_LOO, ε_s}).

---

## v2 — HARDENED after oracle HOLD (S14, 2026-06-14). Supersedes §2–§3 controls; §1 question stands.
The oracle gate returned **HOLD** with three fatal gaps + confound list + a power KILL-branch. Addressing all of
them before any compute (D029). The estimand is sound *in spirit* and a clear improvement over the walled TRIBE
subtraction, but the locked skeleton had a double-spend of the repeats, a noisy reference, and a Fork-A rule that
fires on a point statistic. Fixes:

### Reframe — the claim is a RATIO, not a femto-null (the senior-researcher correction)
A_resid is expected tiny (this program's per-individual effects live at +0.0001–+0.001). A femto-precise null is
not achievable at n=6 / ~3 stories and is **not what the ceiling claim needs.** The publishable, defensible claim
is **A_resid ≪ A_shared**: the LM's brain alignment is *almost entirely* to the stimulus-predictable part. On
denizenslab A_shared = LM→E[Y|S] is large (A2 reconfirmed S13: trained Qwen NC-align ≈0.355 in higher-language,
untrained ≈0). So even a **loose bound** A_resid ≲ 0.02 means A_resid/A_shared ≲ ~6% ⇒ >94% of alignment is to
E[Y|S] ⇒ Fork-B, informatively. **Primary statistic: the ratio ρ = (trained A_resid) / (trained A_shared), with a
bound from the across-story spread.** This is the cleanest non-arbitrary scale and it sidesteps the "is +0.003
small?" ambiguity.

### G1 (FATAL) — stop double-spending story_11's 2 repeats; pre-register the repeat split.
`load_real` collapses both repeats into one mean, leaving no within-subject replicate ⇒ ε's noise ceiling (the §3.3
NC-bound control) is **uncomputable as locked.** Fix: read the raw `(2, T, n_vox)` array directly, project each
repeat to fsa5 separately. Use **repeat-1 of all 6 subjects** to build E[Y|S]^{(1)} and ε_s^{(1)}; validate the
trained A_resid against **ε_s^{(2)}** (repeat-2) as a leave-repeat-out reliability check + to estimate ε's NC. A
residual alignment that does not survive repeat-2 is noise.

### G2 (FATAL) — the LOO reference is noisy at n=5; gate on its reliability.
E[Y|S]_{-s} is a 5-subject mean; at per-subject NC≈0.49 it carries ~17% estimation noise, which can spuriously
*zero out* A_resid (false Fork-B) as easily as inflate it. Fix: **jackknife the reliability of E[Y|S]_{-s}** (split
the 5 into subsets, correlate the two means) and report it. Pre-register: A_resid is only interpretable where the
reference reliability clears a threshold (the L038 vacuity gate, applied to the *reference's stability*, not just
its absolute alignment). Restrict the verdict to NC-mask vertices (`ncgroup > NC_MIN`) — already excludes
zero-support vertices.

### G3 (FATAL) — the replication unit is the STORY, coded in the script, not the seed/fold.
The coded MDE = spread of 3 untrained seeds on n=1 story = the E005/E008 pseudo-replication trap. Fix: run **≥3
stories** (story_11 + train stories 01–10, which exist on disk), compute per-story A_resid, and make the Fork-A
flag require an **across-story** test (paired sign/t across stories), hard-coded in `run_eys_ceiling.py`. The MDE
printed by the runner is the **across-story** MDE, not the untrained-seed spread.

### Confound controls (each with its neutralizer)
- **C1 (L035 carry-forward):** trained−untrained alone under-controls the *lexical-semantic* stimulus-locked path
  (untrained nets lack eng1000 structure). Add the **strong nuisance floor** (rate+articulatory+eng1000-PCA, already
  `F.lowlevel_design(strong=True)`) as a *second* floor: A_resid must exceed trained−untrained AND exceed what the
  nuisance encoder explains of ε_s.
- **C2:** drop the `NDELAYS` TRs straddling each contiguous train/test fold cut (HRF autocorrelation leak).
- **C3:** fit the lag on E[Y|S]_{-s} (or AC on the LOO mean), **never on Y_s** — no cross-subject leak into subject s.
- **C4:** only story_11 carries the NC/repeat bound; train stories (1 repeat) contribute the **point estimate only**
  to the across-story replication. An off-story positive (unceilable) cannot by itself fire Fork-A.

### Power gate / KILL branch (run this FIRST — cheapest decisive)
Compute the across-story MDE empirically (point A_resid on story_11 + ≥3 train stories → between-story sd → MDE).
- **If ρ's bound is informative** (A_resid bound ≲ small fraction of A_shared≈0.355) ⇒ proceed; a bounded null = Fork-B.
- **KILL:** if the across-story MDE on A_resid exceeds the largest plausible non-stimulus signal (≈ the A2
  trained−untrained real magnitude on the *same NC-normalized scale*), E020 cannot separate "ceiling holds" from
  "underpowered." Then **concede the ceiling as bounded-not-closed** (the honest L021 move), record it, and go
  straight to **F2 (E019)** — which does not depend on resolving this residual. Do not spend a fourth compute cycle
  below the instrument floor.

**Decision rule (final, asymmetric):** trained−untrained A_resid (a) excludes 0 on the across-story test, (b)
exceeds the strong-nuisance floor, (c) survives the repeat-2 reliability check, (d) clears the reference-reliability
gate ⇒ **Fork-A → STOP for Erfan.** Anything less ⇒ Fork-B (ceiling holds, bounded by ρ) or HOLD (underpowered →
concede + F2). All four gates **coded in the runner**, matching the discipline that caught the TRIBE false Fork-A.

## VERDICT (S14, 2026-06-14) — NO FORK-A; ceiling BOUNDED-NOT-CLOSED → invoke KILL → F2. (panel-survived)

**Run:** story_11, denizenslab n=6 (01/02/03/05/07/08), Qwen2.5-0.5B layer-12, higher-language ROIs, NC-masked,
linear ridge encoding. `outputs/E020_eys/eys_story11_results.json`, `eys_diagnose.json`, `eys_diagnose2.json`.

**Headline numbers (raw per-vertex Pearson r, HL, one scale):**
A_shared (LM→E[Y|S]) = **+0.176**, A_total (LM→Y_s) = **+0.108**, A_resid (LM→ε_s) = **+0.090**;
ρ vs A_shared = 0.51, ρ vs A_total = 0.84; untrained A_resid +0.033 (untrained A_shared ≈0);
ε split-half NC = **0.174**, LOO reference reliability = **0.33**.

The naive flag fired (A_resid positive). **It is a confirmed ARTIFACT, NOT escalated** — proven by the diagnostics:
- **(A) reference-scaling:** A_resid flat/rising k=1→5 (+0.071→+0.090); the n≤5 reference never gets reliable
  (0.16→0.33) — the η-leak never clears (matches the predeclared "too-noisy reference" regime).
- **(D) symmetric partial (decisive):** the eng1000 partial collapses A_resid +0.090→−0.008 BUT ALSO A_shared
  +0.176→+0.033 ⇒ the nuisance-partial control (B/C1) is **partly vacuous** (eng1000 spans the LM's own semantic
  subspace) — so it CANNOT by itself prove "leaked stimulus." A_shared keeps an 18% non-eng1000 component; A_resid keeps none.
- **(E) low-level-only partial:** A_resid +0.090→+0.034 (the residual alignment lives in the *semantic* subspace).
- **(F) permuted-eng1000 partial:** A_resid +0.038 (NOT killed) ⇒ the collapse is **not** a DOF/overfit artifact;
  temporally-*aligned* stimulus content does the work — what is removed is genuine leaked stimulus.
- **(G) gapped + eng1000-partial (cleanest):** after controlling BOTH HRF-autocorrelation (fold-gaps) AND stimulus
  structure, trained−untrained residual gap = **−0.018 ≈ 0** ⇒ **no brain-specific non-stimulus residual alignment.**

**Conclusion (panel-survived: oracle + socratic + first-principles + counter-argument + premortem):**
1. **NO FORK-A.** The +0.090 A_resid = leaked stimulus (imperfect n=5 reference) + autocorrelation, both controlled
   away. No non-stimulus brain signal the shared LM aligns to. The Fork-A guard worked; nothing escalates to Erfan.
2. **Ceiling BOUNDED-NOT-CLOSED, not closed.** The empirical n=6 LOO E[Y|S] is too noisy (ref-rel 0.33, ε-NC 0.17 —
   the oracle's predeclared KILL regime) and the nuisance-partial is partly vacuous (D), so E020 cannot bound ρ
   cleanly. This is the SECOND ceiling instrument to wall at n=6 denizenslab (after TRIBE — same disease: the
   instrument can't estimate E[Y|S] reliably enough to interpret a residual).
3. **E020 is CONVERGENT CORROBORATION, not proof.** The universal Fork-B (the brain's training-useful signal is its
   stimulus-predictable part) rests on the POWERED per-individual nulls **E008/E011/E017**, per L039/L040. E020 adds:
   (a) the mechanism — no non-stimulus residual signal for a shared stimulus rep to grab; (b) a successful Fork-A guard.
4. **Action: invoke the oracle KILL branch → F2 (E019).** Do not spend a fourth compute cycle below the instrument
   floor (more stories can't fix ref-rel 0.33 — it's a subject-count limit, not a per-story-noise limit; an across-story
   run would re-confirm "no Fork-A" at real cost/timing-bug risk). F2 is paper-critical and ceiling-independent.

**Honest one-sentence claim for the manuscript (analysis lane — Erfan's framing call):** *On denizenslab story_11, the
group-LM's linear-ridge alignment to per-subject fMRI is dominated by the stimulus-predictable component; after
controlling autocorrelation and stimulus structure, no per-subject-residual alignment survives — consistent with the
ceiling, though the empirical reference is too noisy to bound ρ tightly, so the universal claim rests on convergence
with E008/E011/E017.*  **No rung flip.** Q3/F1 stays ❌ (robust per-individual null).

### v2.1 — panel corrections (socratic + first-principles, opus, S14). Sharpen the claim; do not change the run.
The pre-lock thinking panel exposed three things the v2 text over-claimed. Corrected here (the experiment is sound
with these; see L039):

**(i) What E020 establishes — scoped honestly (NOT the universal spine).** A_resid uses a SHARED group LM R(S),
identical across subjects. By construction ε_s = Y_s − E[Y|S]_{-s} removes everything shared across subjects, and a
shared R(S) cannot track genuinely *idiosyncratic* deviation — so **A_resid ≈ 0 is the EXPECTED, theory-consistent
result** (it is also what the DPI predicts for any deterministic function of S: note 2, [`06-theory-grounding.md`](../06-theory-grounding.md)).
E020 therefore **confirms + bounds + guards**, it does not independently *prove* a universal ceiling. Its real
contribution: it is the **mechanistic ceiling that explains E008's per-individual null** — E008 showed you cannot
*train* to induce per-subject alignment; E020 shows there is little per-subject-residual signal a *shared stimulus
representation* can linearly grab in the first place (the "why" behind the null). Scope the manuscript claim to:
"*the group-LM's linear-ridge-detectable alignment to per-subject fMRI is carried almost entirely by the
stimulus-predictable component E[Y|S]; the per-subject residual carries little linearly-alignable signal.*" The
universal Fork-B is supported by the **convergence** of E020 + E008 + E011 + E017, not E020 alone.

**(ii) §1's null is over-attributed.** Cov(R(S), ε) = 0 follows from the **conditional-mean projection** (ε ⟂ any
function of S), not specifically from Y⊥θ\*|S — and only for the *true* mean. Against the *empirical* LOO mean,
ε̂_s = ε_s − η carries estimation noise η that is itself stimulus-structured, so the measurable A_resid is a
**positively-biased bound**, and the bias IS the L016 averaging-confound displaced into the residual. ⇒ **G2 guards
BOTH directions:** a noisy reference can spuriously *zero* A_resid (false Fork-B) AND spuriously *inflate* it (false
Fork-A via leaked stimulus signal). A surviving positive must beat the reference-reliability gate AND the eng1000
floor precisely to rule out η-leak.

**(iii) The ratio must be commensurable.** Do NOT divide an ε-NC-normalized numerator by a group-NC-normalized
denominator (bakes in an arbitrary NC ratio). **Report all three alignments on ONE scale** (raw per-vertex Pearson
r, NC-context reported separately): A_total = LM→Y_s (raw per-subject), A_shared = LM→E[Y|S]_{-s}, A_resid = LM→ε_s.
Primary ratio ρ = raw A_resid / raw A_shared (same normalization on both). Also report whether A_total ≈ A_shared
(the decomposition sanity check — if the LM's alignment to raw Y is carried by the shared part, that IS the ceiling
statement, arithmetically not just rhetorically).


## Retained load-bearing artifacts

| Artifact | SHA-256 |
|---|---|
| `outputs/E020_eys/eys_story11_results.json` | `d16d6f94f2f8f389db3178262bb399c93a8f973321684e1246bf1009f063acab` |
| `outputs/E020_eys/eys_diagnose.json` | `e8fab13e0fed3840a94fb9605d2ca4868ddc6e78d6cc975cede6f7f03b8579b0` |
| `outputs/E020_eys/eys_diagnose2.json` | `84d268dc4a6211e7775cc5bbeca84e5d64eb52fbd8af963799011014eacb1879` |

## Related
- [`status.md`](../status.md) — the canonical status board
