# Experiment — E013 (the open frontier): powered per-individual brain-tuning on multi-subject naturalistic fMRI

**Created:** 2026-06-12 · **Status:** SCOPED (feasible; data path identified; heavy build — next-session unit) · **Mode:** working (design)
**Direction:** the one genuinely-open scientific door after E008/E011/E012 — does a per-individual brain-specific gain appear under a STRONGER regime (closer to Negi: full-FT / contrastive + naturalistic data) on a POWERED multi-subject cohort? The honest open frontier the manuscript (§6) flags.
**Why this is now feasible (not "blocked"):** the power sim (`scripts/sensitivity_e008.py`, L024) shows **~5 deep subjects** power a per-individual test for a δ=+0.003 effect (σ≈0.001). The **denizenslab paired read/listen dataset** (`data/paper-repos/speech-llm-brain`) has **6 subjects** with naturalistic narratives — enough. (LeBel maxes at 3 deep subjects: UTS01/02/03, acquired; denizenslab adds the count.)

## The question
Under a regime that escapes our matched-ppl light-LoRA box — full fine-tuning and/or a contrastive (NT-Xent) brain loss, on naturalistic narrative fMRI — does the per-individual brain-specific gain (vs permuted twin) appear, across ≥5 subjects? A clean per-individual positive here would qualify the thesis toward Fork-A (the null is regime-bound); a powered per-individual null would close the per-individual line decisively (n now adequate, unlike E012).

## What it requires (the honest build cost — why it's a fresh unit, not a tail-of-session rush)
1. **Data acquisition:** denizenslab fMRI timeseries (only noise-ceiling derivatives are on disk; the HDF response files download via GIN/git-annex). 6 subjects × ~11 Moth stories.
2. **A voxelwise/TR-level brain-tuning loop** — the deliberately-unbuilt "E007" pipeline (a differentiable LM-hidden→voxel readout + Lanczos/FIR TR alignment in torch + the LoRA/full-FT loop). E006/E012 deferred this; at n=6 the *power* objection is resolved but the *build* remains a multi-day pipeline.
3. **A contrastive (NT-Xent) brain-loss arm** (new `brain_loss` form) to engage Negi's objective axis, alongside the MSE readout.
4. The full protocol: per-individual inference (n≥5), permuted twin, matched-ppl read-out (the ppl-covariate intercept, since full-FT will diverge ppl — E011/L019), spatially-blocked (not per-voxel-independent) inference (E012 oracle).

## Predeclared rule
Per-individual brain-specific gap (mse/contrastive − permuted twin), n≥5 subjects, crossed subject+fold, ppl-intercept at matched ppl, spatially-blocked permutation inference. Positive (CI excludes 0, ≥k/n subjects, at matched ppl) → Fork-A-qualifying (rewrite). Null → the per-individual line closed on a powered, stronger-regime, naturalistic substrate (the strongest possible Fork-B).

## Status
SCOPED + feasible (data path: denizenslab n=6; power: sim says ≥5 suffices). **Deferred as the next-session major build** — it is the heavy E007 voxelwise-tuning pipeline on a new dataset + a contrastive-loss arm; launching it at the tail of a long session risks a rushed/buggy multi-day build (the failure mode this session's rigor avoided). It is the clear, concrete, highest-value next experiment — and the only one that can move the per-individual verdict — but it warrants a fresh session (and/or Erfan's go-ahead on the build investment). Not impossible; scoped and queued.
