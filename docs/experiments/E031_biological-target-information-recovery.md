---
title: "Experiment - E031: biological-target information recovery"
tags: [experiment, complete]
aliases: [E031]
---

# Experiment - E031: biological-target information recovery

**Created:** 2026-07-28 · **Status:** COMPLETE - independently audited; author confirmation of the scoped classifications is pending · **Mode:** interpreted
**Hypothesis:** [`H002`](../hypotheses/H002_repeat-stable-biological-supervision.md)
**Direction:** Test whether existing fMRI measurements contain recoverable, repeat-stable and participant-preserving target information before changing the LM loss or opening a new modality.

## Objective and claim boundary

Test two upstream claims required by the proposed denoising direction:

> A cross-fitted source-consensus target retains more information about target-construction-held-out participants than an otherwise identical uniform source target, and fixed-content repeat averaging increases independent biological information within the repeated LeBel story.

Cross-participant consensus is not measurement reliability. It mixes measurement noise with stable participant-specific biology. C1 therefore tests consensus transfer, while C2 tests a fixed-content repeat-information response. Each can justify only its same-substrate follow-on. Their conjunction cannot establish that measurement noise caused C1 behavior or any prior intervention failure.

E031 does not train or score a student, select a loss layer, establish biological specificity unless its matched controls pass, compare downstream utility, or change the thesis verdict.

`READY-TO-RUN: YES`

## Why this experiment comes first

The repository already shows that target uptake is not sufficient:

- [`E025`](E025_participant-e016-biological-transfer.md) found target learning and representation movement without participant-general biological transfer.
- [`E030`](E030_exact-substrate-transport-diagnostic.md) localized the first observed failure to unique linear measurability of the target in recorded fMRI, before student-to-brain overlap.
- [`E014`](E014_averaging-encoding-confound.md) showed that participant averaging can raise apparent reliability while changing the estimand.
- [`E020`](E020_empirical-EYgivenS-ceiling.md) showed that a noisy leave-one-subject-out reference can hit an instrument floor.

Running an autoencoder, a broad layer sweep, or a new-modality training job before a target-information gate would not distinguish noise reduction from target mismatch, estimand substitution, semantic leakage, or generic optimization.

## Claims under test

### C1: held-out-participant target recovery

A target built only from source participants and outer-training stimuli adds held-out predictivity of each evaluation participant's five-ROI Tuckute response beyond the locked nuisance model.

The source-consensus candidate must also exceed:

1. an otherwise byte-identical uniformly weighted residual mean;
2. its own capacity- and structure-matched block-shifted twin; and
3. positive information conditional on the frozen contextual-text family before any source-response-specific interpretation.

### C2: fixed-content repeat-information response

For one participant hearing the same LeBel story ten times, increasing the number of independent repeats used to construct a target increases its unique predictivity of a disjoint repeat average beyond the frozen text and acquisition nuisance model by a predeclared practical amount and in the direction expected under \(1/k\) independent-noise averaging.

C2 tests whether repeat averaging increases independently recoverable information at fixed participant and content. It does not support participant or stimulus generalization and does not by itself identify a binding noise bottleneck.

### C3: follow-on readiness

C1 and C2 provide separate evidence about participant transfer and fixed-content measurement reliability. They do not share an estimand, are not combined numerically, and do not license the same follow-on.

A C1 pass can license a Tuckute target-gradient gate. A C2 pass can license repeat-aware LeBel target work. Their conjunction is convergent evidence only: a C2 pass does not transfer its effect size or required repeat count to Tuckute, and it does not show that LeBel repeat noise caused the earlier Tuckute failure.

## Competing explanations

1. **Fixed-content repeat-information response:** repeat count and held-out-view information rise together within LeBel.
2. **Estimand substitution:** participant pooling helps only for a shared average and does not improve target-construction-held-out individual responses.
3. **Shared semantics:** the candidate target predicts held-out biology only through information already present in the text or nuisance model.
4. **Target simplification:** the candidate wins because it has easier scale, spectrum, rank, or headroom rather than better biological content.
5. **Participant-specific biology:** a shared target discards the individual structure required for transfer.
6. **Linear-assay limit:** repeat reliability is adequate, but only a nested nonlinear map finds held-out biological information.
7. **Optimization limit:** the target is valid, but a later gradient gate shows that the readout or attachment layer does not transmit content-specific pressure to the LM.

E031 can separate explanations 1-5 only within their named substrates. Explanations 6-7 remain conditional follow-ons. Identifying measurement noise as binding for an intervention requires a later same-substrate SNR manipulation measured first on a target-construction-held-out biological view and then on the trunk gradient or student.

## Outcome seal and authorized order

No E031 endpoint is computed during design, implementation self-tests, manifest construction, power calibration, or precheck.

The authorized order is:

1. freeze the design, data identities, nuisance sets, splits, target builders, estimands, thresholds, and terminal classifications;
2. implement a synthetic-only self-test and a metadata-only manifest;
3. run `anti-confound-designer`;
4. obtain an independent oracle `PASS`;
5. obtain explicit `/work` authorization for E031;
6. run C1;
7. open C1 only after its artifact is sealed;
8. run C2 only under its already frozen repeat split and estimands;
9. open C2, compute the separate C1 and C2 continuation gates, and route aggregated results to independent statistical audit;
10. adjudicate only under `/interpret`.

C1 cannot alter C2's split, voxel scope, nuisance model, repeat-count grid, or decision rule.

## Fixed sources

### Tuckute C1

- Tuckute condition B, 1,000 ordered sentences, five left-hemisphere language sub-ROIs.
- Exclude UID `853` under the [`E025`](E025_participant-e016-biological-transfer.md) incomplete-ROI rule.
- Source participants are the original valid training subset: `848, 865, 875, 876`.
- Evaluation participants are target-construction-held-out for E031, not project-naive: `797, 837, 841, 856, 880`.
- The primary inference unit is evaluation participant (`n=5`).
- A leave-one-participant-out analysis over all nine valid participants is a dependence-aware descriptive sensitivity, not a second population test.
- Reuse the ordered text, participant-response, covariate, and identity checks from `scripts/e025_participant_transfer.py`.

### LeBel C2

- Participant `UTS03`, story `wheretheressmoke`.
- `individual_repeats` has verified shape `(10, 291, 95556)` in [`E006`](E006_lebel-voxelwise-feasibility.md).
- Reuse the official TextGrid, word sequence, Lanczos, FIR, low-level covariate, and `eng1000` stimulus-feature path through `scripts/lebel_adapter.py`.
- The primary C2 voxel scope is the fixed released cortical column space intersected only with builder-side finite and nonzero-variance checks before evaluation access. No response-reliability mask is run in E031 v1.
- C2 generalizes only to this participant, story, acquisition, and preprocessing path.

Every source path, ordered stimulus identifier, participant or repeat index, response array, covariate array, and executable dependency must be hash-bound in the E031 manifest.

## C1 design: participant-preserving target recovery

### Outer split and nuisance rules

- Use the five contiguous Tuckute stimulus folds from E025.
- Fit response centering, scaling, nuisance regression, target construction, functional alignment, rank choice, covariance estimation, and ridge regularization on the outer training complement only.
- The primary nuisance set is sentence token length, normalized stimulus position, and the fixed GPT-2-medium static-embedding block with fold-only PCA.
- Add imageability as the predeclared expanded-nuisance sensitivity.
- Add GPT-2XL and PCFG surprisal symmetrically only as the non-primary stress test inherited from E025.
- Never shuffle sentences for model selection or choose a target builder, rank, nuisance set, or participant subset from C1 outcomes.

### Target arms

1. **`source_mean_raw`:** unweighted mean of the four source-participant response vectors in common ROI coordinates. This is descriptive only.
2. **`uniform_residual`:** fit the locked centering, scaling, and nuisance model separately to each source participant on the outer training fold, average the fold-residual response vectors with weights exactly `0.25`, then center and scale each ROI target coordinate from the outer training fold only.
3. **`consensus_weighted`:** use byte-identical transforms and output normalization to `uniform_residual`, changing only the source-participant weights. For each outer fold, participant, and ROI, the four existing outer-training blocks become four inner validation folds. In each inner fold, fit transforms on the other three blocks and compute Pearson agreement between that participant's residual and the uniform mean of the other three participants. If either validation vector has variance at most `1e-12`, set that fold agreement to zero. Otherwise clip the correlation to `[-0.999999, 0.999999]`, Fisher-transform it, average the four values with equal fold weights, transform back, and set negative values to zero. If the four non-negative participant scores sum above `1e-6`, normalize them and shrink halfway to uniform, `w = 0.5 * w_normalized + 0.5 * 0.25`; otherwise use four weights of `0.25`. Apply the frozen participant-by-ROI weights to the outer-train and held-out source residuals. This is a source-consensus estimator, not a measurement-reliability estimator.
4. **`text_surrogate_geometry_matched`:** a five-dimensional contextual text predictor constructed without evaluation-participant responses or rowwise fitting to source responses. Use the six E025 `kd_only` Tuckute representation caches, average the six seed representations separately at layers 6 and 7, concatenate the two seed means, and preserve the frozen 1,000-sentence order. Inside each outer fold, residualize every text coordinate against the locked nuisance block using outer-training rows, standardize from outer-training rows, fit PCA rank 5 on outer-training rows, and apply the transform to held-out rows. Whiten the five outer-training text scores with a leading-eigenvalue-relative floor of `1e-8`, then recolor them with the symmetric positive-semidefinite square root of the centered covariance of the outer-training `consensus_weighted` target. Stop if either rank is below 5. This matches dimension, centered train covariance, and fold-local scale. It does not claim matched headroom, content capacity, or held-out learnability.
5. **`text_to_consensus_crossfit`:** the confirmatory text-conditional control. Begin from the same seed-averaged layer-6-plus-layer-7 features. For each outer-training block held out in turn, fit nuisance residualization, float64 standardization, and PCA rank 50 only on the other three blocks, then fit a no-intercept multivariate ridge with fixed alpha `100` from those text scores to the five `consensus_weighted` coordinates. Predict the held-out training block and concatenate the four inner out-of-fold predictions. Refit the same pipeline on the full outer-training complement and predict the outer-test block. The evaluation-participant outcome baseline is `nuisance + text_to_consensus_crossfit`; the full model adds the aligned `consensus_weighted` target. This cross-fitting prevents an in-sample text-to-target fit from creating artificial specificity.
6. **`block_shifted`:** after fully constructing each biological target arm, circularly rotate it by `floor(L / 2)` rows separately inside every contiguous outer-train and outer-test segment of length \(L\). Never rotate across a fold boundary. Apply the identical target normalization, dimension, calibration, and ridge-selection path to the aligned and shifted arms. The manifest records every segment boundary, offset, and resulting row-map hash.

The target builders receive no evaluation-participant response at target-construction time. The evaluation-participant response may be used only as the outcome inside its outer training and held-out content folds.

The cache map is `outputs/E025/extraction.json`, SHA-256 `b49c2795c55961cae161084afa1d3409dd662b893f9a40fa6a4e9373bc2c84c5`, under E025 manifest SHA-256 `2729c0c97b2f845ccf8f58a13e01ecf87f44029564ca615269230437de46698d`. The six frozen nonbrain cache identities are:

| Seed | Cache SHA-256 |
|---:|---|
| 0 | `f18da48f50717f999398a194a945056f062b64ec86b38cde822891616474066b` |
| 1 | `83046f62d6e0e482a05f59d6b3b89bfe8905fbf8e226b27ed9b43d46d79c1181` |
| 2 | `33b6ee55b7ecf11588ec5986cfc31f9aeb621c55daef4a4d943a5f5f44977ea5` |
| 3 | `164f7db4d1faf9f5f637165e0da77cdb74aa662e77ee1b68c7a1253099cf8b4e` |
| 4 | `c5106533509dc3e7842e8f0a58f22472831bc228910de5650f0a5cbb55628be6` |
| 5 | `dc8736e0030b6c2470436130f89d8928d0099054ea6bd3d72676f86cb227c417` |

Every cache must contain float32 `tuckute_layer_6` and `tuckute_layer_7` arrays of shape `1000 x 768`, metadata pooling `attention-mask mean`, layers `[6, 7]`, and ordered-text SHA-256 `6766e068a2b4f4ad84fad525cdb1f41f60524f1c206139741e9fc22ef1cb5702`. The extraction alias must map the cache only to `kd_only` at its named seed. Cast each array to float64, average in seed order `0,1,2,3,4,5` separately by layer, then concatenate layer 6 before layer 7.

All PCA uses centered float64 `numpy.linalg.svd(..., full_matrices=False)`. Resolve each component sign by making its largest-absolute loading positive. Covariance uses denominator `n_train - 1`. Whitening and recoloring use `numpy.linalg.eigh` with eigenpairs ordered descending. Stop on an eigenvalue below `-1e-10`; clamp smaller negative roundoff to zero. The whitening floor is `1e-8` times the leading eigenvalue. The symmetric square root is \(V\operatorname{diag}(\sqrt{\lambda})V^\top\).

The geometry-control gate requires exact dimension 5, finite rank 5, centered-covariance relative Frobenius error
\(\lVert C_{\mathrm{text}}-C_{\mathrm{cw}}\rVert_F/\max(\lVert C_{\mathrm{cw}}\rVert_F,10^{-12})\)
at most `1e-6`, maximum eigenvalue error divided by the leading biological eigenvalue at most `1e-6`, and outer-training mean absolute error at most `1e-7`. Failure makes the standalone text comparison unavailable rather than activating a replacement text model.

### C1 fixed numerical constants

- Preserve the E025 condition-B row order and split the 1,000 rows into five contiguous 200-row outer blocks.
- Center and scale every predictor with outer-training population moments (`ddof=0`) and floor standard deviations at `1e-8`. Fit the fixed GPT-2-medium static-embedding nuisance PCA at rank 50 by the SVD convention above on each outer-training complement. Apply the identical training-only transform to its held-out block.
- For source-response residualization, fit the centered nuisance design separately to every source-participant-by-ROI response with float64 `numpy.linalg.lstsq(..., rcond=None)` and no intercept. Apply each outer-training coefficient vector to its held-out source response. Center and scale the resulting target coordinates from outer-training rows with `ddof=0` and floor `1e-8`.
- Use ridge alphas `[1, 10, 100, 1000, 10000]` for every evaluation-participant nuisance-only and nuisance-plus-target model. Standardize predictors and each evaluation ROI from outer-training rows, fit float64 `sklearn.linear_model.Ridge(solver="svd", fit_intercept=False)`, and choose one alpha shared across the five ROIs by mean inner-block validation MSE. The four non-test outer blocks serve in turn as inner validation blocks. Ties within `1e-12` choose the larger alpha.
- Apply the same evaluation-outcome model-selection path to `uniform_residual`, `consensus_weighted`, `text_surrogate_geometry_matched`, `text_to_consensus_crossfit`, and `block_shifted`. No arm receives a separate outcome-model alpha search or response transform.
- For `block_shifted`, rotate each 200-row outer block by exactly 100 rows and record the five row-map hashes.

### C1 estimands

For evaluation participant \(u\), target arm \(a\), and ROI \(r\), concatenate all outer-fold held-out predictions in original row order. Let \(\mathrm{SSE}^{\mathrm{nuis}}_{u,r}\) and \(\mathrm{SSE}^{a}_{u,r}\) be the squared errors of the nuisance-only and nuisance-plus-target predictions, and let \(\mathrm{SST}_{u,r}\) use the corresponding out-of-fold observed responses around their out-of-fold grand mean. Define

\[
U_{u,a}
=
\frac{1}{5}\sum_{r=1}^{5}
\frac{
\mathrm{SSE}^{\mathrm{nuis}}_{u,r}
-
\mathrm{SSE}^{a}_{u,r}
}{
\mathrm{SST}_{u,r}
}.
\]

Every ROI receives equal weight. \(U_{u,a}\) is computed once from concatenated out-of-fold predictions, never by averaging fold \(R^2\) values. All primary arms use identical outer-fold transforms, target dimension, ridge grid, nested selection, and evaluation-outcome model.

The primary target-validity estimand is

\[
A_{\mathrm{cw}}
=
\frac{1}{5}\sum_u U_{u,\mathrm{consensus\_weighted}}.
\]

The primary consensus increment is

\[
D_{\mathrm{cw-uniform}}
=
\frac{1}{5}\sum_u
\left(
U_{u,\mathrm{consensus\_weighted}}
-
U_{u,\mathrm{uniform\_residual}}
\right).
\]

The primary content-specificity contrast is

\[
S_{\mathrm{cw}}
=
\frac{1}{5}\sum_u
\left(
U_{u,\mathrm{consensus\_weighted}}
-
U_{u,\mathrm{cw\_shifted}}
\right).
\]

The primary text-conditional specificity estimand is

\[
B_{\mathrm{cw\mid text}}
=
\frac{1}{5}\sum_u
\frac{1}{5}\sum_{r=1}^{5}
\frac{
\mathrm{SSE}^{\mathrm{nuis+text}}_{u,r}
-
\mathrm{SSE}^{\mathrm{nuis+text+cw}}_{u,r}
}{
\mathrm{SST}_{u,r}
}.
\]

Also report the standalone descriptive contrast
\[
T_{\mathrm{cw-text}}
=
\frac{1}{5}\sum_u
\left(
U_{u,\mathrm{consensus\_weighted}}
-
U_{u,\mathrm{text\_surrogate\_geometry\_matched}}
\right).
\]

`source_mean_raw` and \(T_{\mathrm{cw-text}}\) are descriptive. A shared-linear or nonlinear latent is deferred from E031 v1. No winner-selected target replaces `consensus_weighted` after outcomes are opened.

### C1 uncertainty

- Report all five evaluation-participant values.
- The scope is the five named evaluation participants conditional on the four named source participants. No population-participant claim is permitted.
- Report participant mean with two-sided t-CI95, participant median, one-sided exact sign test where defined, and leave-one-participant-out estimates. Sign tests and leave-one-participant-out values are stability diagnostics, not significance gates.
- The confirmatory family is \(A_{\mathrm{cw}}\), \(D_{\mathrm{cw-uniform}}\), \(S_{\mathrm{cw}}\), and \(B_{\mathrm{cw\mid text}}\). At full precision, the fixed-cohort gate requires mean \(A_{\mathrm{cw}}\) and \(D_{\mathrm{cw-uniform}}\) to be at least `+0.002`, mean \(S_{\mathrm{cw}}\) and \(B_{\mathrm{cw\mid text}}\) to be strictly positive, and at least four of five participant values for every contrast to be strictly positive. Equality at `+0.002` passes the mean practical threshold; an individual value of exactly zero never counts toward the four-positive rule.
- Also report one-sided participant-\(t\) lower bounds with Bonferroni familywise alpha `0.05`; each bound therefore uses one-sided alpha `0.0125`. These model-based bounds calibrate stability in the fixed cohort and do not create a participant-population claim.
- Report fold values descriptively. Do not flatten participant-by-fold cells.
- The four source participants, inner folds, ROIs, target dimensions, and optimizer initializations are not biological replication units.
- A prospective power and minimum-detectable-effect calculation for the weakest conjunct at the participant unit must use the recorded E030 participant-level variance without opening any E031 candidate outcome. If the design cannot distinguish its threshold, C1 remains a fixed-cohort engineering gate and cannot support a participant-population claim.

### C1 historical-variance calibration

The outcome-blind calibration command was:

```bash
uv run python scripts/e031_power_calibration.py \
  --output outputs/E031/power_calibration.json
```

It consumed the mechanically verified E030 analysis SHA-256 `43a4f3b01641072345149e651cdd0b1ae0c903bb74366db2006f31b89d8dd818` and only the recorded imageability-primary values for participants `797, 837, 841, 856, 880`. Under family alpha `0.05`, four one-sided contrasts, target power `0.80`, and the `+0.002` null:

- the E030 absolute-validity variance proxy had sample SD `0.009350`, lower-bound half-width `0.014615`, and required a true mean of `0.021167` for 80% power; and
- the E030 aligned-minus-twin variance proxy had sample SD `0.004930`, lower-bound half-width `0.007706`, and required a true mean of `0.012106` for 80% power.

The calibration script SHA-256 is `4e9114a5c2d827aac7cc965a56b301e41e8bad0a8d38735502f687cca71d8f57`. The artifact is `outputs/E031/power_calibration.json`, SHA-256 `1a6f199b5d462f8554748f3fc847efb2afe3b8234d8557708cc030065cb9955a`. An independent recomputation reproduced the participant inputs, hashes, critical value, half-widths, and noncentral-\(t\) solutions to floating-point precision; fresh stdout was byte-identical to the artifact.

These are historical variance proxies, not E031 outcomes or estimates of E031 arm means. They show that the five-person design cannot be expected to resolve an effect near `+0.002` with simultaneous participant-\(t\) inference. C1 can still make a predeclared deterministic continuation decision for these five participants, but no population-level `PASS` label is available. For the zero-null specificity contrasts, the relevant 80% detectable mean is the reported excess itself, not the excess plus `+0.002`.

## C2 design: fixed-content repeat-information response

### Frozen repeat split

- Builder repeats: indices `0, 2, 4, 6, 8`.
- Evaluation repeats: indices `1, 3, 5, 7, 9`.
- The reverse assignment is one named sensitivity.
- The evaluation-repeat mean is sealed until every builder target and nuisance prediction is complete.
- Builder targets use repeat counts \(k \in \{1,2,3,4,5\}\).
- For each \(k\), enumerate every size-\(k\) subset of the five builder repeats. Subset estimates are overlapping descriptive measurements, not independent replications.
- The primary voxel base is the full 95,556-column cortical response space in the released UTS03 HDF array. The little-endian int64 index vector `arange(95556)` has SHA-256 `cff6598c131bdf725894c953341e389d1a3f5a3fb2acfc68b42adb0612bb487d`. Before evaluation-repeat access, intersect this base only with voxels that are finite and have variance above `1e-12` across builder repeats and retained builder time rows. Seal that builder-side mask and its hash. Any nonfinite evaluation value inside the sealed mask triggers a stop; it never causes retrospective voxel exclusion.
- No response-reliability mask or voxel-selected sensitivity is run in E031 v1.
- Before evaluation-repeat access, estimate a builder cross-repeat reference \(R_{\mathrm{builder}}\). Enumerate the 10 unordered `2-versus-3` partitions of the five builder repeats and both directions for exactly 20 directed comparisons. For each direction, use the same outer time folds, nuisances, calibration, fixed shift twin, and sealed primary voxel mask as C2. Subtract shifted from aligned inside voxel, take the median across the sealed voxel mask, then take the equal mean across the 20 full-precision directed values. If unrounded \(R_{\mathrm{builder}} < 0.01\) unique-\(R^2\), classify `INSTRUMENT FLOOR` and do not open evaluation repeats; equality continues. Otherwise seal the conditional C2 response floor as \(\delta_{\mathrm{C2}} = 0.10 R_{\mathrm{builder}}\).
- The builder seal must contain \(R_{\mathrm{builder}}\), \(\delta_{\mathrm{C2}}\), all 10 partition identities and 20 directions, folds, shift maps, primary-mask hash, aggregation constants, and data, configuration, and executable hashes. `c2-score` must refuse evaluation-repeat access on any builder-seal hash mismatch.

### C2 preprocessing and target construction

- Apply only the recorded preprocessing already present in the verified LeBel response arrays.
- Standardize each voxel from the builder-side outer training time blocks only.
- Construct the response target as the arithmetic mean of the selected builder repeats. No learned denoiser is fit in C2.
- Fit the E006 low-level and `eng1000` nuisance path inside each contiguous outer time fold: FIR delays `1-4` for both blocks, with the delayed `eng1000` block reduced by the frozen E006 rank-100 train-fold PCA and the delayed five-column low-level block kept unreduced.
- Add an outcome-independent acoustic block from the released story audio: eight log-mel energy bands spanning `80-7600 Hz`, plus their first temporal differences. The stereo 44,100 Hz int16 WAV is converted to float64 by division by `32768` and averaged across channels. Use a periodic Hann window of 1,103 samples, hop 441, FFT size 2,048, `center=False`, power spectrum, and 10 equally spaced edges under the HTK map \(2595\log_{10}(1+f/700)\) to form eight unit-area triangular filters. Take \(\log(\max(\mathrm{energy},10^{-10}))\), prepend zeros for first differences, place frames at window-center times, Lanczos-resample to the story TR grid with `window=3`, trim rows `[10:-5]`, and apply FIR delays `1-4 TR`. Stop unless the result has exactly 291 rows.
- Purge the FIR support around every outer-fold boundary so lagged regressors cannot share response support across train and held-out time blocks.
- Add the same-voxel builder target as the biological predictor of the disjoint evaluation-repeat mean.
- Standardize builder targets and the evaluation-repeat mean separately using their own outer-training moments only. Fit the builder-to-evaluation ridge calibration on outer training time blocks, choose regularization by inner contiguous training folds, and score held-out time blocks.
- Build temporal twins separately within every retained contiguous outer-train and outer-test segment. Circularly rotate the fully constructed builder target by `floor(L / 2)` rows inside a segment of length \(L\), using the same offset for every \(k\). Never rotate across a fold or purged boundary. Stop if any offset is at most seven TRs. Seal every offset and row-map hash before evaluation-repeat access.

### C2 fixed numerical constants

- Response HDF: `data/lebel_ds003020/preprocessed_data/UTS03/wheretheressmoke.hf5`, 2,447,000,216 bytes, SHA-256 `e172a8bc0a325146e94acd083bdc47b09e758330116c2705db16cf8f14c24c8d`.
- TextGrid: `data/lebel_ds003020/derivatives/TextGrids/wheretheressmoke.TextGrid`, 998,492 bytes, SHA-256 `abf315ed25d8811dd2b76256b6cb8c4dc2bcde079a7c1d0b9957fe5242828613`.
- Audio: `data/stimuli_wav/wheretheressmoke.wav`, 106,181,968 bytes, SHA-256 `eb18af15cf390064f410f5d5f3e2b9c6c5068c9ec9af302e4ebee743a72bddc5`; two channels, int16, 44,100 Hz, 26,545,481 frames.
- `eng1000`: `data/lebel_ds003020/derivatives/english1000sm.hf5`, 82,673,264 bytes, SHA-256 `6eea5f79821fb77dc600abdfe4058284961e4e53521136212415163ed6df848d`.
- Recorded nuisance adapter: `scripts/lebel_adapter.py`, SHA-256 `f6d15750c977a573dfb38495a84ada34d0f7d0d2b3bc547474d8f9b201784061`.
- The manifest must reproduce response shape `10 x 291 x 95,556` for UTS03 `wheretheressmoke`.
- Create five outer time blocks with `numpy.array_split(arange(291), 5)`, yielding one block of 59 rows followed by four blocks of 58 rows.
- Purge seven TRs on each side of every train/test boundary: three TRs for Lanczos `window=3` interpolation support plus four TRs for FIR delays `1-4`. Assert mechanically that no raw feature or delayed feature support crosses a retained boundary.
- Use ridge alphas `[1, 10, 100, 1000, 10000]`. Standardize every predictor and each voxel outcome on the relevant outer-training rows with `ddof=0`; a training standard deviation at most `1e-12` excludes that builder-side voxel before the mask is sealed. Fit float64 `sklearn.linear_model.Ridge(solver="svd", fit_intercept=False)` and choose one alpha shared across sealed voxels by the mean inner-block validation MSE. The four non-test outer blocks serve in turn as inner validation blocks. Ties within `1e-12` choose the larger alpha.
- For each voxel, concatenate outer-fold held-out predictions in original time order and compute unique \(R^2 = (\mathrm{SSE}_{\mathrm{nuis}}-\mathrm{SSE}_{\mathrm{full}})/\mathrm{SST}\), where \(\mathrm{SST}\) is around that voxel's concatenated observed evaluation-response grand mean. Stop if evaluation \(\mathrm{SST}\le 10^{-12}\) inside the sealed mask. Preserve negative values. Never average fold \(R^2\) values.
- Average builder subsets inside voxel first, subtract the matched shift inside voxel second, and take the median over the all-finite cortical scope last.

C2 intentionally changes only repeat count. Participant, story, stimulus content, voxel coordinates, nuisance features, folds, and evaluation target remain fixed.

### C2 estimands

For voxel \(v\), repeat count \(k\), and builder subset \(B\), let \(Q_{v,k,B}\) be held-out unique \(R^2\) of the aligned builder target beyond the nuisance model when predicting the disjoint evaluation-repeat mean. First average \(Q_{v,k,B}\) over every size-\(k\) subset \(B\) within voxel. Then compute the primary curve as the median over all finite cortical voxels of the aligned-minus-mean-shifted contrast.

Report:

1. the primary median aligned-minus-mean-shifted curve over all finite cortical voxels;
2. the arithmetic voxel mean and unadjusted aligned \(Q_{v,k,B}\) summaries as sensitivities;
3. the fraction of voxels with positive aligned-minus-shifted contrast;
4. the \(k=5\) minus \(k=1\) primary contrast and all five curve points;

Strict observed monotonicity is not a gate because overlapping subset averages make adjacent points dependent and sampling variation can reverse them. Let \(\Delta Q_k\) be the primary aligned-minus-shifted curve. The primary response condition is \(T = \Delta Q_5 - \Delta Q_1 \ge \delta_{\mathrm{C2}}\), together with a positive unweighted least-squares slope with intercept of \(\Delta Q_k\) against \(1-1/k\), the expected averaging scale under independent noise. A slope of exactly zero fails. The `0.01` builder floor and `10%` reference fraction are prospective allocation preferences: a later LeBel gradient assay is not worth running unless repeat averaging recovers at least one tenth of a builder-demonstrable signal that itself reaches one percent unique predictivity. Neither constant is estimated from evaluation repeats, and the Tuckute `+0.002` threshold is not transplanted. Erfan must explicitly accept these two allocation preferences before `READY-TO-RUN: YES`.

### C2 uncertainty and scope

- The story is the stimulus-population unit, and there is only one story. No across-story confidence interval or population claim is permitted.
- Report variability across contiguous time blocks and voxels descriptively, with spatial dependence stated.
- Repeat-subset combinations and voxels are not independent; no t-test or power calculation over combinations or voxel count.
- The reverse repeat split is a sensitivity, not a second confirmatory result.
- C2 can identify a fixed-content measurement mechanism for UTS03. It cannot establish that a denoised target improves participant transfer or LM training.
- The identifying assumptions are a stable latent response across repeats, conditional independence of builder and evaluation measurement errors, no repeat-order adaptation that tracks the fixed split, no preprocessing across repeat or fold boundaries, and adequate removal of aligned acquisition, acoustic, and lexical artifacts. Violating any assumption routes C2 to `UNRESOLVED`.

## Terminal classifications

1. **`CONSENSUS-TRANSFER PASS`:** C1 consensus-weighted target clears the absolute and incremental practical thresholds, beats its shifted twin, and adds positive information conditional on the frozen contextual-text surrogate.
2. **`NO CONSENSUS INCREMENT`:** the consensus target has absolute fixed-cohort predictivity, but \(D_{\mathrm{cw-uniform}}\) misses `+0.002` or its four-positive rule. This issues no specificity or intervention license.
3. **`SHARED-SEMANTICS FAILURE`:** \(A_{\mathrm{cw}}\) and \(D_{\mathrm{cw-uniform}}\) pass, but the shifted contrast or text-conditional contrast fails.
4. **`FIXED-COHORT TARGET FAILURE`:** \(A_{\mathrm{cw}}\) misses `+0.002` or its four-positive rule in the five named evaluation participants.
5. **`FIXED-CONTENT REPEAT-INFORMATION RESPONSE`:** C2's \(k=5\) minus \(k=1\) primary contrast crosses its conditional response floor and its fixed \(1-1/k\) slope is positive.
6. **`REPEAT-INFORMATION INADEQUATE`:** raw repeat agreement rises, but content-specific unique predictivity does not clear the C2 response gate.
7. **`BUILDER INSTRUMENT FLOOR`:** \(R_{\mathrm{builder}} < 0.01\); evaluation repeats remain sealed and no C2 mechanism label is issued.
8. **`UNRESOLVED`:** validity or provenance failures prevent a scoped classification.

Only classification 1 can justify a Tuckute target-gradient gate. Classification 5 can separately justify repeat-aware LeBel target work. Their conjunction is convergent evidence only, not a pooled estimate or an identified common noise mechanism. E031 never licenses student training directly.

## Confound and control battery

- Target-construction-held-out biological view: evaluation participants for C1; disjoint repeat mean for C2.
- Contiguous stimulus or time splits; no random item split.
- Fold-only centering, scaling, PCA, nuisance regression, functional alignment, rank choice, covariance estimation, and regularization.
- Locked participant and repeat membership.
- Unweighted mean baseline.
- Per-kind content-destroyed twin.
- Frozen geometry-matched contextual-text benchmark plus cross-fitted text-to-consensus conditional control.
- Dimension, centered covariance spectrum, and fold-local scale audit for the standalone geometry benchmark. Headroom, content capacity, and held-out learnability are not claimed to be matched.
- Participant-first or story-scoped uncertainty; no seed, fold, ROI, voxel, or repeat-subset pseudo-replication.
- No outcome-driven nonlinear model, layer, loss, target family, nuisance set, repeat split, or voxel mask.
- No student checkpoint, LM quality outcome, E028 endpoint, or external author result is opened.

## Compute and stop rule

E031 is expected to be CPU and memory bound. It may reuse verified local response and covariate arrays but creates a new metadata-bound result.

Stop immediately on:

- response, text, participant, repeat, ROI, voxel, or covariate identity mismatch;
- incomplete participant ROI coverage;
- train/test transform leakage;
- non-finite target or outcome values;
- target-arm rank or covariance mismatch beyond frozen tolerance;
- source or evaluation participant contamination;
- builder/evaluation repeat overlap;
- failure to reproduce the locked nuisance-only baseline path;
- prospective power below the continuation threshold; or
- any manifest or executable hash mismatch.

No extra participant, denoiser, nonlinear model, rank, nuisance, shift, repeat split, or target family is added after endpoint access.

## Planned executable surface

- `configs/e031_biological_target_information_recovery.json`: frozen data identities, participant/repeat splits, folds, target definitions, thresholds, tolerances, and output paths.
- `scripts/e031_biological_target_recovery.py`: synthetic self-test, metadata-only manifest, C1 runner, C2 runner, and fail-closed analyzer.
- `outputs/E031/`: gitignored heavy outputs.
- This record: design, precheck, exact commands, artifact hashes, results, and adjudication.

The executable must separate:

1. `--stage selftest`, which uses synthetic data only;
2. `--stage manifest`, which reads metadata and hashes but computes no endpoint;
3. `--stage c1`, which cannot access C2 evaluation repeats;
4. `--stage c2-build`, which cannot access evaluation repeats;
5. `--stage c2-score`, which requires a sealed builder artifact;
6. `--stage analyze`, which requires exact reviewed manifest and result hashes.

## Precheck

### Anti-confound designer

**Verdict: HOLD.** The 2026-07-28 review found that cross-participant agreement is consensus, not measurement reliability; the weighted arm was not fairly matched to its comparator; C1 power and simultaneous gates were undefined; the text control and derangements were not executable; `shared_linear` named two estimators; the C2 curve, mask, shift, and monotonicity gate were underdefined; and the cross-substrate conjunction could not identify a binding noise mechanism.

This revision:

- renames and exactly defines `consensus_weighted`;
- makes `uniform_residual` its byte-identical primary comparator;
- adds the participant-level matched-text contrast and simultaneous C1 gate family;
- defers the shared latent from E031 v1;
- defines the C2 subset estimand, all-finite primary voxel scope, segment-local shift rule, acoustic control, and \(k=5\) minus \(k=1\) response; and
- narrows the continuation claim to two scoped gates.

The text-control construction and tolerances are now frozen above, the C1 historical-variance calibration is independently audited, and the builder-only C2 threshold rule is frozen without opening evaluation repeats. A fresh anti-confound review returned `PASS` for synthetic-only implementation and metadata-manifest stages after the cross-fitted text-conditional gate, builder seal, primary-mask correction, and numerical constants were added. This does not authorize endpoint computation.

### Oracle reviewer

**Verdict: PASS for the outcome-blind preflight.** The independent re-audit verified that:

- the consensus estimator performs foldwise `atanh`, equal averaging, and `tanh` before nonnegative normalization and halfway shrinkage to uniform;
- the C1 manifest binds the Tuckute response CSV, nuisance cache, E025 manifest, loader, participant/ROI identities, covariates, array shapes, and hashes;
- the synthetic C2 builder seal requires all frozen fields, 10 partition identities, 20 direction identities, folds, shift maps, aggregation constants, and data, configuration, and executable hashes; and
- `c1`, `c2-build`, `c2-score`, and `analyze` each fail closed with exit code `2`, `BLOCKED_BY_DESIGN_HOLD`, and `endpoint_values_accessed=false`.

The reviewed outcome-blind artifacts are:

| Artifact | SHA-256 |
|---|---|
| `configs/e031_biological_target_information_recovery.json` | `ca598159920820fc5956bcaa145dd8866d39173c5ddb2f1a66ad46dcfa3217f2` |
| `scripts/e031_biological_target_recovery.py` | `f780d2c2f8b31ef74f4b6b6c64aa6091163c6a10cd918ffc65eaecbf15393b5f` |
| `outputs/E031/preflight_manifest.json` | `2b05fa6f87f541484c5ed559a020be2763c818c6f505db7b28ccf70aa59bafce` |
| Canonical manifest payload | `c3da5fcf07d63f4c44cf8693298d10254b28ba60ce7cea407d3930595a36c8b4` |

The exact design-stage preflight commands were:

```bash
uv run python -m py_compile scripts/e031_biological_target_recovery.py
uv run python scripts/e031_biological_target_recovery.py --stage selftest
uv run python scripts/e031_biological_target_recovery.py --stage manifest
```

Compilation passed, all nine synthetic tests passed, and the metadata-only manifest passed with `endpoint_values_accessed=false`. This oracle verdict licensed no endpoint computation.

On 2026-07-29, immediately after the exact handoff `/work E031; accept R_builder < 0.01 and delta_C2 = 0.10 R_builder`, Erfan instructed the agent to proceed with the suggested plan. This is recorded as acceptance of the two frozen allocation constants and explicit authorization of `/work E031`.

The implemented stages then underwent a fresh outcome-blind precheck. The first anti-confound pass returned `HOLD` on four provenance defects: stale C1 admission to C2, under-bound nuisance cache identity, insufficient builder-seal arithmetic/array validation, and stale result admission to analysis. All four were repaired. The fresh anti-confound re-review returned `PASS` with no endpoint access. An independent oracle then reviewed the outcome-blind candidate, independently ran compilation, the 13-test synthetic battery, the metadata manifest, and all four locked endpoint invocations, and returned `PASS` with `endpoint_values_accessed=false`. The oracle authorized changing only the configuration's status and endpoint-authorization fields, regenerating the metadata manifest, and then running C1.

After activation, the first C1 invocation failed before loading biological values because the standalone executable could not resolve the local `scripts` package. The repair added the repository root to `sys.path` and made the manifest report the activated authorization boolean instead of a hard-coded false value. A narrow anti-confound re-review and a narrow independent oracle re-review both returned `PASS` on the exact final candidate: config SHA-256 `b44b59c13d96a1d8349d6d02fb7814136108b06166f4630203185fc4f7a88b90`, executable SHA-256 `c0adcf221919115b9241ff5603b8e5cb2c1886b7b05998a7e4b0555caca3818f`, and preflight-manifest SHA-256 `96c0d49b246759a23a011d5c3e7dd8297c8c760e025d75e7d7c261f013a6474b`. Compilation, all 13 synthetic tests, the metadata manifest, and a target-free loader smoke test passed. No biological response value was accessed by the failed invocation.

`READY-TO-RUN: TERMINAL`

## Results

### Retained artifacts

The load-bearing gitignored artifacts are:

| Artifact | SHA-256 |
|---|---|
| `outputs/E031/preflight_manifest.json` | `96c0d49b246759a23a011d5c3e7dd8297c8c760e025d75e7d7c261f013a6474b` |
| `outputs/E031/c1_result.json` | `6401bcc09c12a985b34ad991957bbe4f08daef79ad1a276669abefeca04fc70e` |
| `outputs/E031/c1_arrays.npz` | `b2381acaff4fb9dc7fc123752834fd15b1756e2add645aab4fab93b4c3fe152c` |
| `outputs/E031/c2_nuisance.npz` | `dc6140cb8b2c9d3cb88a8b22e6d45d5370cfd8b87a119d94b12d7a3e4488babb` |
| `outputs/E031/c2_builder_result.json` | `86fd18a09dd239f0e3b312dabd38e9808e607444ecfb39f80cf355c8b7833eac` |
| `outputs/E031/c2_builder_arrays.npz` | `1b32981ccae214f417a73569efdb7bf0eae11c3ac16700f5df4113c6e48be0b4` |
| `outputs/E031/c2_builder_seal.json` | `53478a41bc2080025adedaf79be49cd6f701c9b9fa24dc2d4a13dd304c9459af` |
| `outputs/E031/analysis.json` | `d3d005a820c207915221b3761f02fa801857cac2409e44666d6eddb1b87f5cf6` |

### C1: source-consensus transfer

Independent recomputation from the sealed arrays matched every stored participant value, summary, leave-one-participant-out estimate, and gate with maximum numerical discrepancy `0.0`.

| Confirmatory contrast | Mean unique \(R^2\) | t-CI95 | Positive participants | Gate |
|---|---:|---:|---:|---|
| \(A_{\mathrm{cw}}\) | `+0.004379456` | `[-0.002901670,+0.011660581]` | `4/5` | pass |
| \(D_{\mathrm{cw-uniform}}\) | `+0.000936178` | `[+0.000054798,+0.001817559]` | `5/5` | **fail: mean below `+0.002`** |
| \(S_{\mathrm{cw}}\) | `+0.004862842` | `[-0.002953532,+0.012679216]` | `4/5` | pass |
| \(B_{\mathrm{cw\mid text}}\) | `+0.004577917` | `[-0.002497510,+0.011653345]` | `4/5` | pass |

The exact terminal classification is **`NO CONSENSUS INCREMENT`**. The consensus-weighted target has absolute fixed-cohort predictivity under the primary nuisance model, beats its block-shifted twin, and adds information conditional on the frozen contextual-text control. Consensus weighting also improves over uniform residual averaging in all five named evaluation participants, but the mean increment is less than half the frozen `+0.002` practical threshold. This is a failure of the continuation magnitude gate, not evidence of zero increment.

The predeclared sensitivities do not rescue the gate. Expanded imageability raises \(D_{\mathrm{cw-uniform}}\) to `+0.001589820`, still below threshold, while its text-conditional contrast is positive in only `3/5` participants. Under the full-covariate stress, \(A_{\mathrm{cw}}=+0.000985228\) and the text-conditional contrast is positive in only `3/5`. The primary result therefore permits no broad biological-specificity or nuisance-invariance claim.

C1 supports only this fixed-cohort statement: a residualized source-participant aggregate contains modest content-aligned information about the five named held-out participants, but the frozen consensus-weighting procedure does not improve enough over uniform averaging to license a target-gradient gate. It does not identify measurement-noise removal, because source agreement also contains shared stimulus structure and participant-common biology. It supports no participant-population claim.

### C2: fixed-content repeat information

The C2 builder used only repeats `[0,2,4,6,8]`. Its 20 directed two-versus-three repeat comparisons gave

\[
R_{\mathrm{builder}}=0.00011644860666361512,
\qquad
\delta_{\mathrm{C2}}=0.10R_{\mathrm{builder}}
=0.000011644860666361512.
\]

Independent recomputation matched both values exactly. All 20 aligned-minus-shifted direction medians were positive, but they ranged only from `+0.000077687` to `+0.000142091`. The frozen builder floor was `0.01`, so the exact terminal classification is **`BUILDER INSTRUMENT FLOOR`**. The independent evaluation repeats `[1,3,5,7,9]` remained sealed, no `c2-score` artifact exists, and no repeat-count response or repeat-information mechanism label is issued.

This is a failure of the predeclared even-repeat, whole-cortex-median linear instrument. It is not evidence that repeat averaging, localized auditory/language responses, nonlinear calibration, or fMRI denoising generally fail. A post-result reviewer noted that the builder mask spans all `95,556` fixed voxels and every one of the `300` nuisance/aligned/shifted fold fits chose the maximum ridge alpha `10000`. Together with the positive but tiny direction medians, this makes spatial dilution and cortex-wide over-shrinkage the strongest alternative explanation. That observation is exploratory and cannot rescue E031.

### Audit and licenses

The post-result statistical audit returned `PASS`. It independently recomputed the four C1 confirmatory contrasts, all stored C1 summaries and diagnostics, the 20 C2 builder direction values, \(R_{\mathrm{builder}}\), \(\delta_{\mathrm{C2}}\), mask identity, artifact hashes, and provenance links with maximum discrepancy `0.0`. Counter-argument and first-principles reviews accepted the mechanical classifications and held any stronger conclusion that denoising failed or that biological supervision cannot work.

The terminal licenses remain:

- Tuckute target-gradient gate: **false**
- repeat-aware LeBel target work under E031: **false**
- student training: **false**

Erfan's confirmation of the two scoped classifications remains required before they are synchronized into the extended manuscript. A separate prospectively frozen spatial-scope diagnostic may test the instrument-mismatch alternative while the C2 evaluation repeats remain sealed.

## Related

- [`H002`](../hypotheses/H002_repeat-stable-biological-supervision.md) - governing hypothesis and staged mechanism
- [`E004`](E004_brain-loss-lever-test.md) - existing loss family and readout-absorption failure
- [`E006`](E006_lebel-voxelwise-feasibility.md) - verified repeated-story substrate and nuisance path
- [`E014`](E014_averaging-encoding-confound.md) - estimand change under participant averaging
- [`E020`](E020_empirical-EYgivenS-ceiling.md) - empirical shared-target reliability floor
- [`E025`](E025_participant-e016-biological-transfer.md) - participant-level biological-transfer result
- [`E026`](E026_tribe-textfeat-target-comparability.md) - target-comparability requirements
- [`E030`](E030_exact-substrate-transport-diagnostic.md) - first observed exact-substrate failure
- [`status.md`](../status.md) - canonical operations
