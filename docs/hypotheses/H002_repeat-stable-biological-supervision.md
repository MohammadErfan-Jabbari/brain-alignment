---
title: "Hypothesis H002 - repeat-stable, participant-preserving biological supervision"
tags: [hypothesis]
---

# Hypothesis H002 - repeat-stable, participant-preserving biological supervision

**ID:** H002
**Created:** 2026-07-28
**Status:** proposed
**Charter:** [`../00-charter.md`](../00-charter.md) · **Experiment:** [`E031`](../experiments/E031_biological-target-information-recovery.md)

---

## Governing question

Can the biological auxiliary signal become useful if the target preserves repeat-stable, participant-general information instead of asking the model to fit raw or participant-averaged neural coordinates?

**Provisional answer:** possibly, but denoising is useful only if it increases information about an untouched biological view, retains content that is not reproduced by text and nuisance controls, and sends a content-specific gradient into the model. A smoother or more predictable training target is not sufficient.

## Claim (falsifiable)

A repeat-aware target will carry more disjoint-repeat information than a lower-repeat target if measurement noise is active within a fixed substrate. Separately, a cross-fitted source-consensus target may carry more target-construction-held-out participant information than an otherwise identical uniform residual target. Cross-participant consensus is not measurement reliability, and the two claims must not be pooled into one mechanism.

The claim receives prospective support only if the candidate target:

1. improves held-out-participant or held-out-repeat biological predictivity beyond the locked nuisance model;
2. beats its byte-identical uniform residual baseline by the inherited `+0.002` unique-\(R^2\) smallest effect of interest in the Tuckute consensus test;
3. clears a separate prospective conditional threshold and the expected \(1-1/k\) slope in the LeBel repeat test;
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
3. **Shared latent or functional alignment:** estimate \(Z_s\) with participant-specific maps and explicit view-specific noise.
4. **Repeat-crossvalidated representational geometry:** when independent repeats exist, estimate crossnobis or whitened unbiased distances rather than fitting raw coordinates.

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

## What each modality can contribute

- **Repeated fMRI:** the best first substrate for identifying a reliability curve because independent repeats permit fixed-content target and evaluation averages. [`E006`](../experiments/E006_lebel-voxelwise-feasibility.md) records ten repeats of the LeBel UTS03 story `wheretheressmoke`.
- **Multi-participant fMRI:** the best first substrate for testing whether shared latent alignment retains information that participant averaging loses. Tuckute provides common sentences and individual participant responses.
- **ECoG:** the strongest later temporal-precision test when enough aligned language data and independent participants are available. [`E028`](../experiments/E028_vaidya-crossmodal-intervention-falsification.md) remains the controlled external route but is blocked on author artifacts.
- **MEG:** a non-invasive high-temporal-resolution candidate for representational and layer-time alignment. It is a separate measurement test, not automatic denoising.
- **EEG:** scalable and temporally precise, but high artifact burden and cross-subject shift mean that alignment, reliability, and content controls must pass before intervention training. [`E024`](../experiments/E024_zuco-lupi-sample-efficiency.md) tested ZuCo gaze rather than establishing an EEG route.
- **fNIRS:** hemodynamic and portable, but it does not currently offer a clearer language-matched, participant-general test than the registered fMRI and electrophysiology substrates.

Multimodal fusion is licensed only when modalities share stimuli at a defensible time scale. Diagnosis-level co-availability or unrelated subjects does not identify a shared stimulus response.

The outcome-blind substrate order is:

1. use the already-local LeBel fixed-content repeats and Tuckute participant views to identify whether repeat stability or participant preservation recovers independent biological information;
2. if the fixed-content mechanism passes, replicate it on [MEG-MASC](https://www.nature.com/articles/s41597-023-02752-5), where 22 participants have two sessions with the same four stories;
3. if a participant-preserving latent passes, test fMRI-MEG fusion on [SMN4Lang](https://www.nature.com/articles/s41597-022-01708-5), where the same 12 people heard the same 60 stories in both modalities;
4. use [Podcast ECoG](https://www.nature.com/articles/s41597-025-05462-2) as a disjoint high-temporal-resolution endpoint rather than as the first training substrate; and
5. defer a new EEG intervention until a dataset provides adequate participant transfer, artifact controls, and either fixed-content repeats or a clean independent endpoint.

This order tests a mechanism before paying the acquisition, preprocessing, and multiple-comparison cost of a new modality. It does not imply that fMRI is intrinsically superior to electrophysiology.

## Measurement bet

- **Primary metric:** participant-first held-out unique \(R^2\) beyond the locked stimulus and nuisance model.
- **Specificity metric:** aligned target minus capacity- and structure-matched content-destroyed twin.
- **Independent-view metric:** prediction of a target-construction-held-out participant or disjoint repeat average.
- **Threshold:** inherited `+0.002` unique-\(R^2\) smallest effect of interest for Tuckute participant-level biological measurability. The LeBel voxelwise single-story diagnostic requires a separate substrate-appropriate threshold in the [`E031`](../experiments/E031_biological-target-information-recovery.md) prospective power gate.
- **Baseline:** uniform residual biological mean, raw response where available, nuisance-only model, and matched nonbiological target.
- **Inference units:** participant for Tuckute; repeat and contiguous time block for the single-subject LeBel mechanism diagnostic, without population generalization.
- **Condition/domain:** Tuckute condition B and LeBel UTS03 `wheretheressmoke` first. No new dataset is needed for the first gate.

## Kill criteria

- Kill the current-data shared-target route if its reference information remains below the preregistered instrument floor, it fails to beat the uniform residual mean, or its apparent gain is reproduced by the content-destroyed or matched text-only target.
- Reject "measurement noise is the binding bottleneck" if increasing fixed-content repeat count substantially improves target reconstruction but does not improve independent content-specific biological predictivity by the preregistered practical amount.
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

### From literature

- [Lage-Castellanos et al. 2019](../literature/canonical/lage-castellanos-2019_fmri-noise-ceiling.md): reliability bounds observed fMRI model performance, while group averaging requires separate treatment.
- [Moussa and Toneva 2025](../literature/canonical/moussa-2025b_multi-participant-brain-tuning.md): multi-participant training preserves participant-specific losses through a shared projection instead of averaging responses.
- [Guo et al. 2024](../literature/canonical/guo-2024_eeg-cotrain-adversarial-robustness.md): real EEG, shuffled EEG, and random EEG can all improve an auxiliary-training outcome, so biological-content controls are load-bearing.
- [Zhang et al. 2026](../literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md): full spatiotemporal ECoG targets are a plausible temporal-precision exception, but participant and split questions remain.
- [Prince et al. 2022](../literature/canonical/prince-2022_glmsingle.md): cross-validated HRF, nuisance, and ridge modeling can improve single-trial fMRI estimates.
- [Li et al. 2019](../literature/canonical/li-2019_learning-brains-regularize-machines.md): a learned neural system-identification model can serve as a denoiser before constructing a neural representational target; the raw neural similarity target did not reproduce the same result.
- [Diedrichsen et al. 2020](../literature/canonical/diedrichsen-2020_whitened-unbiased-rdm-similarity.md): crossvalidated distances remove positive noise bias, while whitening accounts for correlated distance errors; this motivates a later repeat-crossvalidated geometry target when independent partitions exist.
- [Schütt et al. 2021](../literature/canonical/schutt-2021_statistical-inference-representational-geometries.md): subject and condition generalization require separate factors, and flexible representational models must be fit inside crossvalidation.

## Alternative explanations

- **Shared semantics, not biology:** a denoiser may amplify stimulus structure already present in text or KD. Distinguish it with nuisance subtraction and matched text-only targets.
- **Estimand substitution:** a shared latent may discard participant-specific biology. Distinguish it with target-construction-held-out participant prediction and participant-specific losses.
- **Geometry or headroom:** a latent target may simply be easier to fit. Match dimension, covariance spectrum, baseline predictability, loss scale, and trunk-gradient magnitude.
- **Optimization coupling:** the target may be valid while the readout or layer blocks a useful gradient. Test gradients before training.
- **Nonlinear measurability:** E030's linear assay may miss usable structure. Permit a bounded nonlinear branch only after reliability and nested controls pass.
- **Temporal mismatch:** fMRI may omit the timing required by the model. Use a later MEG/ECoG test only after the same target-validity harness is available.

## Staged decision

1. [`E031`](../experiments/E031_biological-target-information-recovery.md) separately tests Tuckute source-consensus transfer and the LeBel fixed-content repeat-information response without student training.
2. A Tuckute target-gradient record is licensed by the C1 gate; repeat-aware LeBel work is licensed separately by C2. Their conjunction is not a common-mechanism claim.
3. A small layer-placement training factorial is licensed only if one layer carries a stable aligned-versus-twin trunk-gradient advantage.
4. Participant-specific shared-head intervention training is licensed only after the target and gradient gates pass.
5. An external modality validates the mechanism only after the same controls and inference units are available.

## Log

| Date | Update |
|---|---|
| 2026-07-28 | Created from the repository failure localization, four independent grounding passes, and a verified literature-family scout. |
| 2026-07-28 | Anti-confound review separated Tuckute source consensus from LeBel repeat reliability. The recorded E030 variance calibration also restricted Tuckute C1 to a fixed-cohort engineering gate because five-person simultaneous inference cannot resolve an effect near the `+0.002` threshold. |

## Related

- [`status.md`](../status.md) - canonical operations and next actions
- [`01-research-landscape.md`](../01-research-landscape.md) - external frontier map
- [`06-theory-grounding.md`](../06-theory-grounding.md) - information-theoretic and probabilistic-ML grounding
- [`E031`](../experiments/E031_biological-target-information-recovery.md) - first target-information experiment
