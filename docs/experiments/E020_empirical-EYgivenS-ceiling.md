# Experiment E020 — the empirical-E[Y|S] ceiling (TRIBE-free): does the LM align to brain signal beyond the stimulus-predictable part?

**Created:** 2026-06-14 (S13) · **Status:** **DESIGNED — NEXT to run (F1-close).** Replaces the walled TRIBE
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
