---
title: "Experiment — E014: does cross-subject averaging inflate the ENCODING brain-score (the measurement,…"
tags: [experiment]
aliases: [E014]
---

# Experiment — E014: does cross-subject averaging inflate the ENCODING brain-score (the measurement, not just our distillation)?

**Created:** 2026-06-12 · **Status:** COMPLETE — NOT a main-track lift (panel-deflated) · **Mode:** working (analysis-support)
**Question:** E005-vs-E008 showed averaging inflates apparent brain-specificity *in our distillation pipeline*. The "main-track lift" hoped to show the same confound on the field's **standard measurement** — the encoding brain-score (ridge LM→fMRI unique R²) on a cross-subject-averaged target. If averaging inflated the *encoding* score the way it inflated our optimization gain, the averaging-confound finding would generalize from "our pipeline" to "the published benchmark metric."

## Design
Pure encoding (no LM training): extract Qwen2.5-0.5B verdict-layer features once for the 1000 Tuckute sentences, compute unique R² (E006 protocol: contiguous folds, length/position/static nuisance, n_pca=50) against (a) each individual subject's ROI target, (b) k-averaged targets (random size-k subsets, k∈{1,2,3,5,9}), (c) the standard 5-UID-averaged target. Track the noise-ceiling prediction NC_k = NC/(NC+(1−NC)/k). `scripts/run_averaging_encoding.py` → `outputs/E014_averaging_encoding_seeded.json`.

## Result (seeded run)
- **Per-subject mean unique R² = +0.0069** (7/9 positive, range −0.003 to +0.023).
- Dose-response (k=1/2/3/5/9): **+0.0039 / +0.0162 / +0.0324 / +0.0444 / +0.0702** (NC_k pred 0.491→0.897).
- Standard 5-UID-averaged target: **+0.0357** → inflation **5.15×** vs the per-subject mean (unseeded run gave 4.8×; ratio stable).

## VERDICT: NOT a main-track confound-lift — it is legitimate higher-SNR + estimand-shift (panel-deflated)
The thinking panel (counter-argument + first-principles, fable) rejected the "averaging manufactures the encoding score 5×" reading:
1. **Per-subject scores are POSITIVE (7/9), not a well-powered zero.** So the E008 logic ("averaging manufactures a gap absent per-person") does NOT transfer to the encoding side — on the measurement, the per-individual signal is *present*; averaging just measures it with less noise. The "manufactures/artifactual" framing fails here.
2. **The ~5× is mostly legitimate.** ~1.7× is the noise-ceiling rise (NC 0.49→0.83 at k=5; Lage-Castellanos 2019 / Nili 2014); the residual is the ridge estimator approaching the higher ceiling as target SNR rises + a near-zero per-subject denominator (the L016/L019 divide-by-noise-floor pathology). The averaged score measures a *different estimand* (alignment to the shared component g), not a 5×-biased per-individual estimate.
3. **Found + fixed a real bug:** `pilot_lib` PCA was unseeded (randomized SVD) → nondeterministic unique R² (jitter ±0.005–0.01, larger than the small per-subject scores). Seeded it (`random_state=0`). Headline results (E006 A2, E008 null) are robust — they aggregate over many folds/voxels/seeds so PCA jitter averages out; E014's single-shot scores were the exposed ones (seeded re-run 5.15× vs unseeded 4.8× — ratio stable, finding survives).
4. **Process WIN:** verified with the panel BEFORE folding into the manuscript → the paper is correctly UNCHANGED (contrast E013 v1, claimed-then-retracted). L028.

## Status
COMPLETE. **E014 is a legitimate-SNR / estimand-shift effect, NOT a second confound; it does not strengthen the paper and is NOT added to it.** The averaging-confound headline stays on E005-vs-E008 (well-powered per-individual ZERO on the *optimization* side, where the per-individual reality is genuinely null). Recorded in L028; PCA-seed fix in `pilot_lib.py`.


## Related
- [`status.md`](../status.md) — the canonical status board
