---
title: "Experiment - E031: biological-target information recovery"
tags: [experiment, active]
aliases: [E031]
---

# Experiment - E031: biological-target information recovery

**Created:** 2026-07-28 · **Status:** DESIGN HOLD - no E031 endpoint compute; anti-confound reviewed, remaining freezes and oracle review required · **Mode:** working
**Hypothesis:** [`H002`](../hypotheses/H002_repeat-stable-biological-supervision.md)
**Direction:** Test whether existing fMRI measurements contain recoverable, repeat-stable and participant-preserving target information before changing the LM loss or opening a new modality.

## Objective and claim boundary

Test two upstream claims required by the proposed denoising direction:

> A cross-fitted source-consensus target retains more information about target-construction-held-out participants than an otherwise identical uniform source target, and fixed-content repeat averaging increases independent biological information within the repeated LeBel story.

Cross-participant consensus is not measurement reliability. It mixes measurement noise with stable participant-specific biology. C1 therefore tests consensus transfer, while C2 tests a fixed-content repeat-information response. Each can justify only its same-substrate follow-on. Their conjunction cannot establish that measurement noise caused C1 behavior or any prior intervention failure.

E031 does not train or score a student, select a loss layer, establish biological specificity unless its matched controls pass, compare downstream utility, or change the thesis verdict.

`READY-TO-RUN: NO`

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
3. a matched text-derived target before any brain-specific interpretation.

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
- The primary C2 voxel scope must be selected from builder repeats only, without access to evaluation repeats. All finite cortical voxels and the prior E006 mask are named sensitivities. The E006 mask cannot be primary because it was estimated from these same ten repeats.
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
3. **`consensus_weighted`:** use byte-identical transforms and output normalization to `uniform_residual`, changing only the source-participant weights. For each outer fold, participant, and ROI, the four existing outer-training blocks become four inner validation folds. In each inner fold, fit transforms on the other three blocks and compute Pearson agreement between that participant's residual and the uniform mean of the other three participants. Clip correlations to `[-0.999999, 0.999999]`, Fisher-transform them, average the four values with equal fold weights, transform back, and set negative values to zero. If the four non-negative participant scores sum above `1e-6`, normalize them and shrink halfway to uniform, `w = 0.5 * w_normalized + 0.5 * 0.25`; otherwise use four weights of `0.25`. Apply the frozen participant-by-ROI weights to the outer-train and held-out source residuals. This is a source-consensus estimator, not a measurement-reliability estimator.
4. **`text_matched`:** a five-dimensional contextual text target constructed without evaluation-participant responses. Its exact source encoder, train-only projection, covariance and local-order matching, nuisance-only predictability, fixed-reference learnability, tolerances, and failure rule remain a blocking precheck freeze. A target-only version of the [`E026`](E026_tribe-textfeat-target-comparability.md) measured-axis battery must pass before C1 can support a biology-specific label.
5. **`block_shifted`:** after fully constructing each biological target arm, circularly rotate it by `floor(L / 2)` rows separately inside every contiguous outer-train and outer-test segment of length \(L\). Never rotate across a fold boundary. Apply the identical target normalization, dimension, calibration, and ridge-selection path to the aligned and shifted arms. The manifest records every segment boundary, offset, and resulting row-map hash.

The target builders receive no evaluation-participant response at target-construction time. The evaluation-participant response may be used only as the outcome inside its outer training and held-out content folds.

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

The matched-text contrast is

\[
T_{\mathrm{cw-text}}
=
\frac{1}{5}\sum_u
\left(
U_{u,\mathrm{consensus\_weighted}}
-
U_{u,\mathrm{text\_matched}}
\right).
\]

`source_mean_raw` is descriptive. A shared-linear or nonlinear latent is deferred from E031 v1. No winner-selected target replaces `consensus_weighted` after outcomes are opened.

### C1 uncertainty

- Report all five evaluation-participant values.
- The scope is the five named evaluation participants conditional on the four named source participants. No population-participant claim is permitted.
- Report participant mean with two-sided t-CI95, participant median, one-sided exact sign test where defined, and leave-one-participant-out estimates. Sign tests and leave-one-participant-out values are stability diagnostics, not significance gates.
- The confirmatory family is \(A_{\mathrm{cw}}\), \(D_{\mathrm{cw-uniform}}\), \(S_{\mathrm{cw}}\), and \(T_{\mathrm{cw-text}}\). The fixed-cohort gate requires the mean of every contrast to clear its threshold and at least four of five participant contrasts to have the expected sign.
- Also report one-sided participant-\(t\) lower bounds with Bonferroni familywise alpha `0.05`; each bound therefore uses one-sided alpha `0.0125`. These model-based bounds calibrate stability in the fixed cohort and do not create a participant-population claim.
- \(A_{\mathrm{cw}}\) and \(D_{\mathrm{cw-uniform}}\) must each clear `+0.002` unique-\(R^2\). \(S_{\mathrm{cw}}\) and \(T_{\mathrm{cw-text}}\) must each clear zero.
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
- The primary voxel scope is every finite cortical voxel shared by all ten repeats. No response-derived voxel selection enters the primary curve.
- A fold-local builder-only reliability mask fixed across \(k\) and the prior E006 reliability mask are named sensitivities. Neither may replace the all-finite primary scope.

### C2 preprocessing and target construction

- Apply only the recorded preprocessing already present in the verified LeBel response arrays.
- Standardize each voxel from the builder-side outer training time blocks only.
- Construct the response target as the arithmetic mean of the selected builder repeats. No learned denoiser is fit in C2.
- Fit the E006 low-level and `eng1000` nuisance path inside each contiguous outer time fold.
- Add an outcome-independent acoustic block from the released story audio: eight log-mel energy bands spanning `80-7600 Hz`, computed with a `25 ms` Hann window and `10 ms` hop, plus their first temporal differences. Resample to the TR grid and apply the same FIR delays `1-4 TR` as the recorded E006 path. The exact audio identity, sample rate, resampling, edge trimming, and feature hashes must be frozen in the manifest.
- Purge the FIR support around every outer-fold boundary so lagged regressors cannot share response support across train and held-out time blocks.
- Add the same-voxel builder target as the biological predictor of the disjoint evaluation-repeat mean.
- Standardize builder targets and the evaluation-repeat mean separately using their own outer-training moments only. Fit the builder-to-evaluation ridge calibration on outer training time blocks, choose regularization by inner contiguous training folds, and score held-out time blocks. The ridge grid, variance weighting, fold aggregation, and exact four-TR boundary purge remain blocking manifest freezes.
- Build temporal twins separately within every contiguous outer-train and outer-test segment. In each outer fold, estimate a builder-only autocorrelation horizon on training segments as the first lag after which the median absolute residual autocorrelation stays below `0.1` for five lags. Let the minimum shift be one plus the larger of that horizon and the four-TR FIR support. Use both positive and negative shifts and average their scores. If the minimum shift is not smaller than half of every affected segment, stop. Exact shifts and hashes must be sealed before evaluation-repeat access.

C2 intentionally changes only repeat count. Participant, story, stimulus content, voxel coordinates, nuisance features, folds, and evaluation target remain fixed.

### C2 estimands

For voxel \(v\), repeat count \(k\), and builder subset \(B\), let \(Q_{v,k,B}\) be held-out unique \(R^2\) of the aligned builder target beyond the nuisance model when predicting the disjoint evaluation-repeat mean. First average \(Q_{v,k,B}\) over every size-\(k\) subset \(B\) within voxel. Then compute the primary curve as the median over all finite cortical voxels of the aligned-minus-mean-shifted contrast.

Report:

1. the primary median aligned-minus-mean-shifted curve over all finite cortical voxels;
2. the variance-weighted mean and unadjusted aligned \(Q_{v,k,B}\) summaries as sensitivities;
3. the fraction of voxels with positive aligned-minus-shifted contrast;
4. the \(k=5\) minus \(k=1\) primary contrast and all five curve points;
5. the same summaries in the frozen E006 reliability-mask sensitivity.

Strict observed monotonicity is not a gate because overlapping subset averages make adjacent points dependent and sampling variation can reverse them. Let \(\Delta Q_k\) be the primary aligned-minus-shifted curve. The primary response condition is \(T = \Delta Q_5 - \Delta Q_1\) clearing a predeclared conditional practical threshold, together with a positive fixed least-squares slope of \(\Delta Q_k\) against \(1-1/k\), the expected averaging scale under independent noise. The numeric threshold must be justified from the minimum improvement needed for the later LeBel gradient assay and frozen before `READY-TO-RUN: YES`; it is not estimated from evaluation repeats. The Tuckute `+0.002` threshold is not transplanted to this voxelwise single-story diagnostic.

### C2 uncertainty and scope

- The story is the stimulus-population unit, and there is only one story. No across-story confidence interval or population claim is permitted.
- Report variability across contiguous time blocks and voxels descriptively, with spatial dependence stated.
- Repeat-subset combinations and voxels are not independent; no t-test or power calculation over combinations or voxel count.
- The reverse repeat split is a sensitivity, not a second confirmatory result.
- C2 can identify a fixed-content measurement mechanism for UTS03. It cannot establish that a denoised target improves participant transfer or LM training.
- The identifying assumptions are a stable latent response across repeats, conditional independence of builder and evaluation measurement errors, no repeat-order adaptation that tracks the fixed split, no preprocessing across repeat or fold boundaries, and adequate removal of aligned acquisition, acoustic, and lexical artifacts. Violating any assumption routes C2 to `UNRESOLVED`.

## Terminal classifications

1. **`CONSENSUS-TRANSFER PASS`:** C1 consensus-weighted target clears the absolute and incremental practical thresholds, beats its shifted twin, and is not reproduced by the matched text target.
2. **`UNIFORM-RESIDUAL SUFFICIENT`:** the uniform residual mean passes target validity and specificity, but consensus weighting does not improve it.
3. **`SHARED-SEMANTICS FAILURE`:** a candidate appears predictive, but the text-matched or shifted control reproduces the gain.
4. **`PARTICIPANT-TRANSFER FAILURE`:** source-view fit is adequate, but the candidate does not predict target-construction-held-out evaluation participants.
5. **`FIXED-CONTENT REPEAT-INFORMATION RESPONSE`:** C2's \(k=5\) minus \(k=1\) primary contrast crosses its conditional practical threshold and its fixed \(1-1/k\) slope is positive.
6. **`REPEAT-INFORMATION INADEQUATE`:** raw repeat agreement rises, but content-specific unique predictivity does not clear the C2 response gate.
7. **`INSTRUMENT FLOOR`:** C1 reference variance, C2 conditional threshold, or prospective power cannot distinguish the continuation threshold; no mechanism label is issued.
8. **`UNRESOLVED`:** validity or provenance failures prevent a scoped classification.

Classification 1 or 2 can justify a Tuckute target-gradient gate. Classification 5 can separately justify repeat-aware LeBel target work. Their conjunction is convergent evidence only, not a pooled estimate or an identified common noise mechanism. E031 never licenses student training directly.

## Confound and control battery

- Target-construction-held-out biological view: evaluation participants for C1; disjoint repeat mean for C2.
- Contiguous stimulus or time splits; no random item split.
- Fold-only centering, scaling, PCA, nuisance regression, functional alignment, rank choice, covariance estimation, and regularization.
- Locked participant and repeat membership.
- Unweighted mean baseline.
- Per-kind content-destroyed twin.
- Matched text-derived target for biology-specific interpretation.
- Dimension, covariance spectrum, scale, headroom, and baseline-predictability audit.
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

The remaining blockers are the exact executable text-control construction and tolerances, C1 power from the frozen E030 variance source, the C2 conditional practical threshold, remaining manifest constants named above, and an outcome-blind implementation review.

### Oracle reviewer

Pending. The oracle may review only after every remaining blocker is numeric or hash-bound and the synthetic-only implementation passes.

`READY-TO-RUN: NO`

## Results

Not run.

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
