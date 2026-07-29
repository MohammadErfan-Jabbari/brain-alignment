---
title: "Hypothesis H002 - repeat-stable, participant-preserving biological supervision"
tags: [hypothesis]
---

# Hypothesis H002 - repeat-stable, participant-preserving biological supervision

**ID:** H002
**Created:** 2026-07-28
**Status:** partially tested
**Charter:** [`../00-charter.md`](../00-charter.md) · **Experiments:** [`E031`](../experiments/E031_biological-target-information-recovery.md), [`E032`](../experiments/E032_kymata-cross-run-repeat-recovery.md)

---

## Governing question

Can the biological auxiliary signal become useful if the target preserves repeat-stable, participant-general information instead of asking the model to fit raw or participant-averaged neural coordinates?

**Provisional answer:** the broad hypothesis remains open, but two simple current-data routes did not earn continuation. E031 found modest held-out-participant information in a residualized source aggregate, while consensus weighting improved over uniform averaging by only `+0.000936`, below the frozen `+0.002` gate. Its whole-cortex repeat instrument had \(R_{\mathrm{builder}}=0.000116\), below the `0.01` floor, so the independent repeats stayed sealed. These results reject those implementations, not denoising in general. E032 now asks the narrower next question: can a repeat-optimized common spatial filter recover a stable cross-run MEG or EEG direction before any target or loss is constructed?

## Claim (falsifiable)

A repeat-aware target will carry more disjoint-repeat information than a lower-repeat target if measurement noise is active within a fixed substrate. Separately, a cross-fitted source-consensus target may carry more target-construction-held-out participant information than an otherwise identical uniform residual target. Cross-participant consensus is not measurement reliability, and the two claims must not be pooled into one mechanism.

The claim receives prospective support only if the candidate target:

1. improves held-out-participant or held-out-repeat biological predictivity beyond the locked nuisance model;
2. beats its byte-identical uniform residual baseline by the inherited `+0.002` unique-\(R^2\) smallest effect of interest in the Tuckute consensus test;
3. clears its substrate-specific prospective reliability and method-increment thresholds on independent runs or repeats;
4. beats a capacity-, covariance-, and autocorrelation-matched content-destroyed twin;
5. respects the named participant and contiguous-stimulus inference limits; and
6. later produces a biological-content-specific trunk gradient before any student-outcome comparison is opened.

The claim is not supported by lower target MSE, higher in-sample reconstruction, higher participant-average alignment, or easier target uptake alone.

## Why "the signal is noisy" is incomplete

The existing evidence separates several links that a useful biological loss must satisfy:

\[
\text{useful biological supervision}
=
\text{target reliability}
\times
\text{brain-specific information}
\times
\text{usable gradient}
\times
\text{participant transfer}.
\]

Noise can weaken the first factor. It does not establish the other three.

- [`E025`](../experiments/E025_participant-e016-biological-transfer.md) showed that the synthetic target was learned and the student moved, yet the participant-general biological contrast was near zero.
- [`E026`](../experiments/E026_tribe-textfeat-target-comparability.md) showed that the saved nonbrain comparator was not matched on target difficulty, geometry, nuisance predictability, or induced movement.
- [`E030`](../experiments/E030_exact-substrate-transport-diagnostic.md) localized the first observed failure to unique linear measurability of the target in recorded fMRI, before student-to-brain overlap. It left nonlinear information, information outside PCA-50, nuisance-redundant information, and other endpoints open.
- [`E014`](../experiments/E014_averaging-encoding-confound.md) showed why participant averaging is not neutral denoising: it improves the reliability of a shared target while changing the estimand away from individual response.

The stronger theory must therefore distinguish noise removal from estimand change, semantic leakage, target simplification, and generic regularization.

## Measurement model

For stimulus \(s\), participant \(u\), and modality \(m\), write the recorded response as

\[
Y_{u,m,s}
=
A_{u,m} Z_s
+ C_{u,m} N_s
+ \varepsilon_{u,m,s}.
\]

- \(Z_s\) is the repeat-stable biological component that is shared enough to transfer.
- \(A_{u,m}\) maps that component into participant- and modality-specific measurement coordinates.
- \(N_s\) contains measured stimulus and acquisition nuisance, including information already recoverable from text.
- \(C_{u,m}\) is the participant- and modality-specific nuisance map.
- \(\varepsilon_{u,m,s}\) contains measurement noise and unresolved idiosyncratic variation.

The target-building problem is not to make \(Y\) smooth. It is to estimate a cross-fitted posterior for \(Z_s\) without using the evaluation participant, evaluation repeat, or evaluation stimulus fold.

This model treats participant variation as a view with its own map rather than noise to average away. It also permits EEG, MEG, ECoG, and fMRI to contribute complementary views only when their stimuli and timing are alignable.

## The proposed target

The first target family is deliberately linear and auditable:

1. **Uniform residual biological mean:** the strongest simple cross-participant baseline, with fold-only nuisance residualization and target normalization.
2. **Consensus-weighted shrinkage:** estimate source-to-other-source agreement inside the outer training fold and shrink source-participant dimensions toward uniform weights. This targets shared transfer, not measurement reliability.
3. **Shared latent or functional alignment:** estimate \(Z_s\) with participant-specific maps and explicit view-specific noise. Subject-specific independent components are one auditable candidate, but component estimation and selection must remain inside builder folds.
4. **Repeat-optimized common spatial filtering:** for time-resolved repeated measurements, fit one shrinkage-regularized CorrCA direction on builder exposures, then apply the fixed filter to cross-run evaluation exposures. Reliability is the objective; PCA and content-destroyed temporal shifts remain required controls.
5. **Repeat-crossvalidated representational geometry:** when independent repeats exist, estimate crossnobis or whitened unbiased distances rather than fitting raw coordinates.

A nonlinear denoiser is not the first move. It becomes eligible only if repeat reliability is adequate, the linear target fails, and nested participant-by-stimulus evaluation can distinguish additional signal from nuisance learning.

## How the target should enter the loss

If a target posterior has mean \(\mu_s\) and covariance \(\Sigma_s\), a noise-aware auxiliary loss is

\[
\mathcal{L}_{\mathrm{bio},\ell}
=
\frac{1}{2}
\left(P_\ell h_\ell(s)-\mu_s\right)^\top
\left(\Sigma_s+\tau I\right)^{-1}
\left(P_\ell h_\ell(s)-\mu_s\right)
+ \frac{1}{2}\log\left|\Sigma_s+\tau I\right|.
\]

Here \(h_\ell(s)\) is the model representation at layer \(\ell\), \(P_\ell\) is a biological projection, and \(\tau\) is a locked numerical floor. The precision term reduces the influence of uncertain target directions. The log-determinant term prevents uncertainty from becoming a cost-free escape.

This loss is only a candidate. The projection can absorb the objective, as the co-trained readout did in [`E004`](../experiments/E004_brain-loss-lever-test.md). Before training, the gradient reaching the model trunk must therefore be measured against the correctly paired target and its matched twin. A frozen or separately prefit projection remains a required control.

## Where the loss should enter

The repository has not run a prospective layer-placement experiment.

- [`E004`](../experiments/E004_brain-loss-lever-test.md) used one predeclared middle "verdict layer."
- [`E016`](../experiments/E016_tribe-synthetic-brain-targets.md) trained the synthetic objective at layer 6.
- [`E025`](../experiments/E025_participant-e016-biological-transfer.md) evaluated layers 6 and 7 and found no displacement rescue. That is not evidence about every possible attachment layer.

The next layer decision must be nested and small:

1. compare one upper-middle layer, one late hidden layer, and one learned multi-layer mixture;
2. select or fit weights using training participants and training stimulus folds only;
3. judge the fixed choice on untouched participants and folds;
4. compare aligned-target and matched-twin trunk gradients before student training.

The LM output logits are not a neural measurement space. A "head" test means a projection from the final hidden state, while the language head remains governed by CE or KD. A broad all-layer sweep would create a winner's-curse search and is forbidden.

A later placement gate must also separate layer suitability from raw gradient scale. On builder data, each candidate receives a separately prefit, then frozen biological projection. Its auxiliary-loss weight is normalized once against the median trunk-gradient norm of the CE or KD objective and then frozen. Report projection-only gradient, trunk-gradient norm, aligned-versus-twin trunk-gradient difference, and cosine with the language-objective gradient. Applying losses independently at several layers is a different intervention because it adds correlated gradients and more total auxiliary energy. It is eligible only after a single-layer or builder-fit convex-mixture choice passes, and only under matched total trunk-gradient norm.

## What each modality can contribute

- **Repeated fMRI:** independent repeats permit fixed-content target and evaluation averages. [`E031`](../experiments/E031_biological-target-information-recovery.md) tested the available whole-cortex-median linear LeBel instrument, which stopped at its builder floor. That does not rule out localized, nonlinear, or differently regularized fMRI denoising, but it licenses no post-result variant.
- **Multi-participant fMRI:** the best first substrate for testing whether shared latent alignment retains information that participant averaging loses. Tuckute provides common sentences and individual participant responses.
- **ECoG:** the strongest later temporal-precision test when enough aligned language data and independent participants are available. [`E028`](../experiments/E028_vaidya-crossmodal-intervention-falsification.md) remains the controlled external route but is blocked on author artifacts.
- **MEG:** the current external measurement test because Kymata combines repeated naturalistic stimulation with simultaneous high-temporal-resolution measurement. E032 tests cross-run CorrCA against PCA and shifted controls. A stable component is not automatically linguistic or useful for model training.
- **EEG:** scalable and temporally precise, but high artifact burden and cross-subject shift mean that alignment, reliability, and content controls must pass before intervention training. [`E024`](../experiments/E024_zuco-lupi-sample-efficiency.md) tested ZuCo gaze rather than establishing an EEG route.
- **fNIRS:** hemodynamic and portable, but it does not currently offer a clearer language-matched, participant-general test than the registered fMRI and electrophysiology substrates.

Multimodal fusion is licensed only when modalities share stimuli at a defensible time scale. Diagnosis-level co-availability or unrelated subjects does not identify a shared stimulus response.

The outcome-blind substrate order is:

1. treat E031 as terminal for its frozen Tuckute consensus-weighting and whole-cortex LeBel instruments; neither earned a gradient or repeat-aware follow-on;
2. run [`E032`](../experiments/E032_kymata-cross-run-repeat-recovery.md) on Kymata E2 only after raw-header, trigger, complete-window, channel, and calibration integrity pass. Learn one common CorrCA filter on runs 1 and 3, evaluate it only across runs 2 and 4, keep MEG primary and EEG secondary, and compare with PCA-1 and shifted controls;
3. if E032 passes, freeze the estimator and seek participant and language breadth on [MEG-MASC](https://www.nature.com/articles/s41597-023-02752-5); the current public paired subset remains smaller than the paper's full cohort and must be reverified before use;
4. transfer a frozen estimator to fMRI only with a valid repeat split: use CNeuroMod-THINGS as non-language calibration, then test [Caption Scene Dataset](https://www.nature.com/articles/s41597-026-07248-6) after rebuilding repeat-isolated responses because its released GLMsingle fitting groups mix both presentations;
5. if a participant-preserving latent passes, test fMRI-MEG fusion on [SMN4Lang](https://www.nature.com/articles/s41597-022-01708-5), where the same participants heard the same stories in both modalities;
6. use [Brain Treebank](https://braintreebank.dev/) or [Podcast ECoG](https://www.nature.com/articles/s41597-025-05462-2) as disjoint high-temporal-resolution endpoints rather than first training substrates; and
7. defer an intervention on non-repeated EEG corpora until a dataset provides adequate participant transfer, artifact controls, and either fixed-content repeats or a clean independent endpoint.

This order tests a mechanism before paying the acquisition, preprocessing, and multiple-comparison cost of a new modality. Repeats identify denoising; cross-modal agreement supplies a prior but does not by itself separate signal from noise. The order does not imply that fMRI is intrinsically superior to electrophysiology.

## Measurement bet

- **Completed current-data tests:** E031's participant-first unique-\(R^2\) consensus increment missed its frozen threshold, and its fixed-content repeat test stopped at the builder instrument floor.
- **E032 primary metric:** average Fisher-\(z\) correlation of the fixed CorrCA component over the four run-2-versus-run-4 exposure pairs after the locked nuisance model.
- **E032 method metric:** CorrCA minus same-capacity PCA-1.
- **E032 specificity metrics:** CorrCA minus the maximum shifted-filter twin and maximum shifted-template twin.
- **E032 thresholds:** aligned \(r \ge 0.10\), every method and specificity increment at least `0.05` Fisher-\(z\), every evaluation exposure positive on average, and conservative paired moving-block-bootstrap lower endpoints above zero.
- **Inference unit:** one fixed participant-story pair. Runs, exposures, and time blocks are repeated measurements, not population units.
- **Condition/domain:** Kymata English participant E2, builder runs 1 and 3, evaluation runs 2 and 4. The acquisition-integrity gate precedes every neural score.

## Kill criteria

- The current E031 shared-target and whole-cortex repeat routes are closed under their frozen estimators. Do not tune their masks, ridge grids, or thresholds after observing the results.
- Kill E032's repeat-optimizer route if raw timing or calibration integrity fails, builder cross-run stability is inadequate, CorrCA fails to beat PCA-1 by `0.05` Fisher-\(z\), or shifted controls reproduce the apparent gain.
- Reject the claim that E032 found a usable biological target if it recovers only repeat stability. Content specificity, participant transfer, a nonabsorbed trunk gradient, and downstream utility remain separate gates.
- Do not proceed to student training if correctly paired and matched-twin targets produce indistinguishable trunk gradients or if the projection head absorbs the loss.
- Stop after the uniform residual and consensus-weighted target families unless adequate independent-view information plus linear failure prospectively activates one shared-latent or nonlinear family.
- Treat a participant-average-only result, a training-participant-only result, or a language-quality regression as a kill, not a weak positive.
- EEG, MEG, ECoG, or multimodal work does not open merely because fMRI fails. A candidate dataset must first pass the same response, reliability, alignment, control, and independent-endpoint checks.

## Evidence

### From repository experiments

- [`E004`](../experiments/E004_brain-loss-lever-test.md): a co-trained readout can absorb neural MSE; the corrected valid-unit result showed no demonstrated lever.
- [`E014`](../experiments/E014_averaging-encoding-confound.md): participant averaging raises apparent reliability while changing the estimand.
- [`E020`](../experiments/E020_empirical-EYgivenS-ceiling.md): the leave-one-subject-out shared reference hit its reliability floor, making an instrument gate mandatory.
- [`E025`](../experiments/E025_participant-e016-biological-transfer.md): target uptake and representation movement did not yield participant-general transfer.
- [`E026`](../experiments/E026_tribe-textfeat-target-comparability.md): target geometry, headroom, nuisance predictability, and induced movement must be matched.
- [`E030`](../experiments/E030_exact-substrate-transport-diagnostic.md): unique recorded-fMRI measurability failed before student-to-brain overlap under the frozen linear PCA-50 assay.
- [`E031`](../experiments/E031_biological-target-information-recovery.md): residualized source aggregation retained modest held-out-participant information, but consensus weighting missed its practical increment and the whole-cortex repeat assay stopped at its builder instrument floor.
- [`E032`](../experiments/E032_kymata-cross-run-repeat-recovery.md): prospective cross-run CorrCA information-recovery assay; no participant neural endpoint has been opened.

### From literature

- [Lage-Castellanos et al. 2019](../literature/canonical/lage-castellanos-2019_fmri-noise-ceiling.md): reliability bounds observed fMRI model performance, while group averaging requires separate treatment.
- [Moussa and Toneva 2025](../literature/canonical/moussa-2025b_multi-participant-brain-tuning.md): multi-participant training preserves participant-specific losses through a shared projection instead of averaging responses.
- [Guo et al. 2024](../literature/canonical/guo-2024_eeg-cotrain-adversarial-robustness.md): real EEG, shuffled EEG, and random EEG can all improve an auxiliary-training outcome, so biological-content controls are load-bearing.
- [Zhang et al. 2026](../literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md): full spatiotemporal ECoG targets are a plausible temporal-precision exception, but participant and split questions remain.
- [Prince et al. 2022](../literature/canonical/prince-2022_glmsingle.md): cross-validated HRF, nuisance, and ridge modeling can improve single-trial fMRI estimates.
- [Li et al. 2019](../literature/canonical/li-2019_learning-brains-regularize-machines.md): a learned neural system-identification model can serve as a denoiser before constructing a neural representational target; the raw neural similarity target did not reproduce the same result.
- [Hari et al. 2026](../literature/canonical/hari-2026_independent-component-encoding-models.md): subject-specific ICA provides a plausible lower-dimensional story-encoding target, but stimulus-predictive components are not automatically brain-specific and any component ranking must be nested inside target-builder folds.
- [Diedrichsen et al. 2020](../literature/canonical/diedrichsen-2020_whitened-unbiased-rdm-similarity.md): crossvalidated distances remove positive noise bias, while whitening accounts for correlated distance errors; this motivates a later repeat-crossvalidated geometry target when independent partitions exist.
- [Schütt et al. 2021](../literature/canonical/schutt-2021_statistical-inference-representational-geometries.md): subject and condition generalization require separate factors, and flexible representational models must be fit inside crossvalidation.
- [Koskinen and Seppä 2014](../literature/canonical/koskinen-2014_task-optimized-meg.md): a shared SimCCA filter learned from repeated MEG trials transferred to held-out repetitions and nonrepeated stories in a much richer calibration regime.
- [Parra et al. 2019](../literature/canonical/parra-2019_correlated-components-analysis.md): CorrCA supplies an auditable common-filter reliability objective, shrinkage path, and held-out-repeat evaluation logic.

## Alternative explanations

- **Shared semantics, not biology:** a denoiser may amplify stimulus structure already present in text or KD. Distinguish it with nuisance subtraction and matched text-only targets.
- **Estimand substitution:** a shared latent may discard participant-specific biology. Distinguish it with target-construction-held-out participant prediction and participant-specific losses.
- **Geometry or headroom:** a latent target may simply be easier to fit. Match dimension, covariance spectrum, baseline predictability, loss scale, and trunk-gradient magnitude.
- **Optimization coupling:** the target may be valid while the readout or layer blocks a useful gradient. Test gradients before training.
- **Nonlinear measurability:** E030's linear assay may miss usable structure. Permit a bounded nonlinear branch only after reliability and nested controls pass.
- **Temporal mismatch:** fMRI may omit the timing required by the model. Use a later MEG/ECoG test only after the same target-validity harness is available.

## Staged decision

1. [`E031`](../experiments/E031_biological-target-information-recovery.md) is complete. Neither Tuckute consensus weighting nor the whole-cortex LeBel repeat instrument licensed its follow-on.
2. [`E032`](../experiments/E032_kymata-cross-run-repeat-recovery.md) now tests only whether a common CorrCA filter recovers fixed-E2, fixed-story stability across recording blocks beyond PCA and shifted controls.
3. An E032 pass licenses a separate content-specific assay, not a target, loss, layer choice, or student.
4. A small layer-placement training factorial is licensed only after a frozen target produces a stable aligned-versus-twin trunk-gradient advantage.
5. Participant-specific intervention training is licensed only after the target and gradient gates pass.

## Log

| Date | Update |
|---|---|
| 2026-07-28 | Created from the repository failure localization, four independent grounding passes, and a verified literature-family scout. |
| 2026-07-28 | Anti-confound review separated Tuckute source consensus from LeBel repeat reliability. The recorded E030 variance calibration also restricted Tuckute C1 to a fixed-cohort engineering gate because five-person simultaneous inference cannot resolve an effect near the `+0.002` threshold. |
| 2026-07-29 | Recent-dataset scout separated repeat-identifying substrates from cross-modal priors and independent endpoints. Kymata Soto and MEG-MASC are the first external repeat tests; CSD is the repeat-rich fMRI transfer; SMN4Lang and intracranial corpora remain conditional follow-ups. |
| 2026-07-29 | Metadata/code gates passed Kymata, restricted MEG-MASC to its current ten-person paired public subset, and rejected CSD's released GLMsingle betas as an independent repeat endpoint because all fitted run groups mix the two presentations. |
| 2026-07-29 | E031 returned `NO CONSENSUS INCREMENT` and `BUILDER INSTRUMENT FLOOR`; the independent evaluation repeats stayed sealed and neither target-gradient nor repeat-aware LeBel work was licensed. |
| 2026-07-29 | E032 froze a cross-run, one-component CorrCA assay on Kymata E2 with MEG primary, EEG secondary, PCA-1 and shifted controls, builder-only decisions, and an acquisition-integrity stop before neural scoring. |

## Related

- [`status.md`](../status.md) - canonical operations and next actions
- [`01-research-landscape.md`](../01-research-landscape.md) - external frontier map
- [`06-theory-grounding.md`](../06-theory-grounding.md) - information-theoretic and probabilistic-ML grounding
- [`E031`](../experiments/E031_biological-target-information-recovery.md) - first target-information experiment
- [`E032`](../experiments/E032_kymata-cross-run-repeat-recovery.md) - prospective cross-run repeat-recovery experiment
