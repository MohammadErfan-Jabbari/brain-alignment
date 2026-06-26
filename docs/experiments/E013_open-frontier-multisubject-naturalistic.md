---
title: "Experiment — E013 (the open frontier): powered per-individual brain-tuning on multi-subject…"
tags: [experiment]
aliases: [E013]
---

# Experiment — E013 (the open frontier): powered per-individual brain-tuning on multi-subject naturalistic fMRI

**Created:** 2026-06-12 · **Status:** CLOSED (S25, 2026-06-19, Erfan-directed). Voxelwise distillation-readout lever RAN (no λ improves held-out alignment over base, never beats permuted twin: a single-subject *mechanism* failure → n≥5 moot; L026/L027). The full-FT (not LoRA-readout) multi-subject naturalistic route — "the one untested door" — is **NOT BUILT and assessed CLOSED, the decisive reason being DATASET SIZE: denizenslab is only n=6 subjects, too few to power the per-individual population claim** (see the S25 verdict at the bottom). · **Mode:** working (design)
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

## E013b (the tractable slice — RUNNING): the OBJECTIVE axis on data we have
Rather than wait for the heavy data+voxelwise build, test the cheaper of Negi's two axes — the **contrastive (InfoNCE/NT-Xent) objective** vs our MSE readout — on the existing **powered n=9 Tuckute per-individual** design (the E008 setup). Added `brain_loss.contrastive` (symmetric InfoNCE, `brain_loss.py`); running per-individual (9 UIDs, 2 seeds, n_perm=3, λ=1, 4-GPU split → `outputs/E013b_g{0,1,2,3}.json`). Verdict via `analyze_e008.py` (crossed inference + ppl-intercept). **Question:** does a contrastive/ranking objective produce a per-individual brain-specific gap where MSE gave ~0? **Honest caveat:** the Tuckute target is 5-ROI → low-dim contrastive space → a weaker test of the objective axis than voxelwise (the data axis still needs denizenslab); a null here would indicate the objective axis alone (at ROI granularity) doesn't rescue it, pointing the remaining hope to the data/voxelwise axis (full E013).

### E013b VERDICT (ran 2026-06-12, n=9): the contrastive objective does NOT rescue the per-individual null
Per-individual (9 UIDs, 2 seeds, n_perm=3, crossed inference): contrastive (InfoNCE) brain-specific gap = **mean −0.00019, t-CI [−0.0008,+0.0005] (incl 0), sign 4/9, fold-clustered incl 0; ppl-intercept −0.0003 at matched ppl** (slightly negative; `>perm95=False`). So switching the objective from MSE (E008) to contrastive (Negi's NT-Xent family) **does not change the per-individual verdict** — both give a well-powered ~0 at matched perplexity. **This rules out "you used the wrong loss" as the explanation for the null — at ROI granularity** (caveat: 5-ROI is low-dim for contrastive). The remaining open regime is therefore the **data/voxelwise axis** (high-dim naturalistic targets, the full E013) — NOT the objective axis. L025.

## E013 (voxelwise, n=3) — BUILT + RUNNING (Erfan-directed: build n=3, then decide n≥5)
Built the voxelwise per-individual tuning loop (`scripts/run_lebel_tune.py`, the tractable "E007": per-segment tune target [chunk words → HRF-delayed voxelwise BOLD] + `brain_tune` MSE readout/LoRA + held-out-STORY unique-R² eval via the rigorous E006 protocol + permuted twin). Smoke PASS on UTS03 (105s). Acquired `wheretheressmoke` repeats for UTS01/02 (NC-voxel selection). **Running** per-subject on UTS01/02/03 (one GPU each, 2 seeds, n_perm=2, λ=10) → `outputs/E013_UTS0{1,2,3}.json`. Verdict = per-subject brain-specific gap (real-tuned − permuted-tuned) on held-out stories; n=3 = **existence probe** (not population, L021). After: decide the powered n≥5 denizenslab version.

### E013 VERDICT v1 (n=3, ran 2026-06-12): FAILED MANIPULATION — uninformative; substrate-mismatch REMAINS OPEN (counter-argument-corrected)
Raw gaps (real-tuned − permuted-tuned, held-out story) were −0.0010/+0.0010/+0.0004, seed-flipping. **But the counter-argument panel caught that the manipulation FAILED its check:** in all 6 subject×seed runs the *real-target* tuning **REDUCED held-out alignment below the untuned base** (`real_u < base_u`): UTS01 base 0.0058 → 0.0007/−0.0017; UTS02 0.0085 → 0.0042/0.0047; UTS03 0.0077 → 0.0036/0.0031. The voxelwise tuning (~10M-param 11k-voxel readout over ~1k segments, λ=10, no KD anchor) **damaged** the general contextual features the held-out ridge depends on — it didn't instill brain-specific structure, it destroyed alignment. So the ~0 gap compares two *degraded* representations → **uninformative** (NOT "null on the powered substrate"; the L019 hollow-manipulation lesson, anti-verified). Also: ppl + spatial-blocking controls (predeclared) were omitted; perm noise (2–50× the gap) makes n=3 non-identifying. **The substrate-mismatch limitation REMAINS OPEN.** A valid test needs a regime where real-target tuning first **improves** held-out alignment over base (regularized readout / KD anchor / lower λ / fewer voxels). → E013 v2 (below).

### E013 v2 VERDICT (λ-sweep, UTS03, KD anchor + high-NC voxels): the voxelwise distillation lever DOES NOT TAKE HOLD at any λ
With the KD anchor (which fixed v1's catastrophic collapse), a λ-sweep on UTS03 (rel>0.7, 2801 voxels, base unique R²≈0.0187):
| λ | real_u | gap (real−perm) | manip_ok (real>base) |
|---|---|---|---|
| 1 | 0.0183 (≈base, neutral) | −0.0009 | ✗ |
| 3 | 0.0086 (degrades) | −0.0049 | ✗ |
| 6 | 0.0130 (degrades) | −0.0039 | ✗ |
| 10 (v1, no KD) | collapse | — | ✗ |

**At NO λ does the brain-MSE term improve held-out alignment over the untuned base** (low λ = neutral, real≈base; higher λ = monotonically degrading), **and the real arm never beats its permuted twin** (gap ≤0 throughout). The brain-MSE gradient toward voxelwise BOLD either no-ops or damages the general contextual features the held-out-story ridge depends on — even with the LM anchored by KD. v1 (no anchor, λ=10) degraded all 3 subjects; the v2 λ-sweep characterizes the mechanism on UTS03.

### Verdict: the voxelwise per-individual distillation lever FAILS to take hold (neutral-to-harmful, never brain-specific) — consistent with the per-individual null, but does not "close" substrate-mismatch in the strong sense
We could not induce an *improving* brain-tuning manipulation on the powered voxelwise substrate via distillation, so the clean "tune toward real BOLD, beat the permuted twin per-individual" test is not achievable by this route. What we observe — the lever is neutral-to-harmful at every λ and never brain-specific — is consistent with (and reinforces) the per-individual null (E008/E011/E013b), but it is honestly a **lever-failure / negative-on-method**, not a clean same-substrate null. **n≥5 is moot:** this is a per-subject *mechanism* failure (the manipulation can't be induced on a single subject across λ), not a power limit — more subjects won't change it. L027.

## Status
COMPLETE. v1 = failed manipulation (retracted). v2 λ-sweep = the voxelwise **distillation** lever doesn't take hold at any λ (neutral→degrading, never brain-specific) → consistent with the per-individual null; substrate-mismatch addressed as lever-failure (not a clean null).

**Two distinct routes — do not conflate (this is the S1 consistency fix):**
- **The voxelwise DISTILLATION-readout lever (what E013 tested): CLOSED.** n≥5 is **moot** for *this* route — it is a single-subject *mechanism* failure (the manipulation can't be induced on one subject across λ), not a power limit, so more subjects cannot rescue it. Do NOT build a powered n≥5 of the distillation lever.
- **A DIFFERENT induction method — full fine-tuning (not a LoRA distillation readout) on multi-subject naturalistic voxelwise targets: ~~still genuinely OPEN~~ → CLOSED (S25, 2026-06-19) — NOT BUILT, primarily because the dataset is too small (denizenslab n=6).** ~~This is the deferred fresh-session major build.~~ The full-FT *parameterization* was in fact already tested (E017, LeBel → null); denizenslab would only have added naturalistic data + subject count, and **n=6 cannot power the per-individual population claim** (σ unmeasured, possibly n≈8 needed). See the S25 verdict below.

---

## S25 VERDICT (2026-06-19, Erfan-directed): the full-FT n=6 route is CLOSED — NOT BUILT — primarily because the DATASET IS TOO SMALL

The "one untested door" (full fine-tuning on multi-subject naturalistic voxelwise targets, denizenslab) was driven through
the full pre-compute gate this session — the thinking panel on the Q3 verdict + `anti-confound-designer` (battery-complete
design assembled) + `oracle-reviewer` (DESIGN mode). **Verdict: KILL the build.** It was never run. Three reasons, with
dataset size the decisive one Erfan called:

1. **DATASET SIZE / POWER — the binding constraint (decisive).** denizenslab has **only n=6 subjects** (and only 6 are real
   on disk; 04/06/09 are git-annex stubs). The per-individual test is a *population* claim, so the inference unit is the
   subject (n=6, df=5). The L024 power sim's "power 1.0 at n=5 for δ=+0.003" holds **only if** between-subject σ ≈ 0.001 —
   but denizenslab's between-subject σ on the held-out-story unique-R² gap is **unmeasured**, on a different acquisition /
   stimulus / voxel space, and the oracle estimated σ could be ~2× (→ n≈8 needed). **At n=6 with unknown σ, the MDE may
   exceed the δ we seek — so even a clean run could be underpowered, and the cheap 1-subject gate could not yield a
   population verdict regardless of outcome.** The deep subjects we would need (LeBel maxes at 3; denizenslab adds 6) do
   not exist on disk; acquiring ≥more deep naturalistic-fMRI subjects is a data-acquisition decision, not a re-run.
   **The hypothesis is not what fails here — the data scale is.**

2. **The mechanism was already tested (so "untested door" was overstated).** **E017 already ran full fine-tuning** (not a
   LoRA readout) on voxelwise LeBel → NULL, manipulation mostly failing its own gate (L036). The full-FT *parameterization*
   is therefore not untested; denizenslab would have added naturalistic data + subject count, not a new mechanism.

3. **The manipulation-check gate is 0-for-5.** Across E013 v1, E013 v2 (λ-sweep), E017 gentle, E017 aggressive, and E019,
   no run ever induced an above-base, brain-specific, ppl-preserving improvement — the precondition the whole test rests
   on. A gate-fail is recorded as a lever-failure, not a per-individual null → low expected information per multi-day compute.

**Consequence:** the ladder's "one untested door" hedge is **retired** — the door is assessed closed (size/power-limited +
mechanism-already-tested + 0-for-5 gate). **Q3 stays ❌ (unchanged verdict); this only closes the open hedge.** The Fork-1
cheap single-subject gate (scoped in the S25 timeline + feasibility-confirmed: TextGrids/mapper/NC all on disk) is
**abandoned** for the same size reason — a 1-subject gate cannot move a population claim that n=6 cannot power. Forward
compute goes to the sample-efficiency line (Q4), which hits the *same* root cause from the other side (Q4 = 400 sentences).
See **L051** (data-scale is the binding constraint on the remaining brain-alignment doors).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
