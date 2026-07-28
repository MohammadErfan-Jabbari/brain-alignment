---
title: "Statistical inference on representational geometries"
tags: [literature]
aliases: [schutt-2021_statistical-inference-representational-geometries]
---

# Statistical inference on representational geometries

**Heiko H. Schütt, Alexander D. Kipnis, Jörn Diedrichsen, and Nikolaus Kriegeskorte / 2021 / arXiv preprint** · **Link:** [arXiv:2112.09200](https://arxiv.org/abs/2112.09200)

## TL;DR

Schütt et al. distinguish generalization to new measurements, new subjects, new conditions, and both new subjects and conditions. Their two-factor bootstrap estimates uncertainty across subjects and conditions, while nested two-factor crossvalidation prevents flexible representational models from fitting noise in either factor.

For [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md), the paper supplies the inferential contract for learned target builders and learned layer mixtures. For [`E031`](../../experiments/E031_biological-target-information-recovery.md), it supports participant-first and contiguous-stimulus evaluation but also clarifies that the single-story LeBel mechanism arm cannot justify generalization to a story population.

## Key ideas

### The intended population determines the resampling design

A subject-only test treats the sampled stimuli or conditions as fixed. That is appropriate only when the claim concerns exactly those conditions or when they exhaust the relevant population. Most computational-neuroscience claims instead aim to generalize to both new people and new stimuli.

The two-factor bootstrap resamples subjects and conditions. Because resampling both factors creates interacting variance components and a naive bootstrap overcounts some variability, the paper derives a corrected estimate of model-performance variance and covariance. These covariance estimates support pairwise model tests, comparison with the noise ceiling, and comparison with chance.

### Flexible models need two-factor crossvalidation

A fixed model predicts an RDM without fitting its representation to the evaluated neural data. A flexible model learns feature weights, measurement-model parameters, layer mixtures, or other parameters from neural RDMs. Its apparent performance is optimistic if the same subjects or conditions are used for fitting and testing.

Two-factor crossvalidation fits the flexible model using fitting subjects and fitting conditions, then scores its predicted dissimilarities for held-out subjects and held-out conditions. The crossvalidation is nested inside the two-factor bootstrap. Two complementary crossvalidation cycles allow the method to estimate and remove excess variance introduced by crossvalidation.

Large nonlinear models may be too expensive to refit thousands of times. The paper permits fitting them on a separate neural dataset, but the resulting inference is conditional on that fitting data rather than fully general over a refitted model.

### Noise ceilings and alternatives are part of the test

The lower noise-ceiling bound asks how well the average representation from other subjects predicts each held-out subject. A model below this bound leaves explainable shared geometry unaccounted for. A model near the ceiling is not proved to implement the brain's mechanism; it may only be indistinguishable at the available resolution.

Testing a single model against zero is a weak criterion because many representations share broad stimulus geometry. The paper calls for direct model comparisons and comparison with the noise ceiling rather than treating positive RDM correlation as strong support.

## Evidence

The authors validate false-positive control and generalization behavior using simulations with known generating models, including deep-network-derived representational structure. They also resample calcium-imaging and fMRI datasets to test the procedures on realistic dependence and noise.

The validated methods support:

- inference conditional on the same subjects and conditions but new measurements;
- generalization to new subjects;
- generalization to new conditions; and
- simultaneous generalization to new subjects and new conditions.

The procedures apply to any dissimilarity estimator and RDM comparator supplied by the analyst. The paper also introduces a Poisson-KL dissimilarity for spike-count data and a faster rank-based RDM comparator, but those additions are not required by H002 or E031.

## Limitations

1. **Sample size remains decisive.** A method that targets subject and condition populations still needs enough independent subjects and conditions to estimate their variability.
2. **Bootstrap units must match the claim.** Voxels, ROIs, folds, repeats, and optimizer seeds are not substitutes for subjects or stimulus-population units.
3. **Flexible fitting is computationally expensive.** Bootstrap-wrapped two-factor crossvalidation may require thousands of model fits.
4. **Condition exchangeability can fail.** Contiguous narratives and temporally dependent conditions cannot be naively resampled as independent items.
5. **Noise ceilings are dataset-specific.** They bound performance under the sampled participants, conditions, preprocessing, and measurement reliability; they are not universal brain-model ceilings.
6. **Valid inference does not establish biological specificity.** A matched text model can win under the same inferential framework.
7. **Geometry is a summary.** Different coordinate-level mechanisms can induce similar RDMs.
8. **Exact finite-sample requirements are design-specific.** The minimum subject and condition counts for E031 are `\gap` until its prospective power and dependence calibration are completed.

## Relevance to this thesis

### Relevance to H002

H002 proposes reliability weights, participant-specific maps, and possibly a learned multi-layer mixture. Each is a flexible model because biological data choose parameters. Schütt et al. imply that those choices must be made using training participants and training conditions, then judged on untouched participants and conditions if the claim is participant- and stimulus-general.

The paper also guards against the single-model-significance fallacy. A reliability-aware target that predicts biology above zero is not enough. It must beat the unweighted biological baseline, the matched text target, the content-destroyed twin, and relevant noise-ceiling or instrument-floor references under the intended inference units.

### Relevance to E031

E031 C1 correctly keeps five evaluation participants as the biological inference units and uses contiguous stimulus folds. A flexible `reliability_weighted` or `shared_linear` builder must fit reliability, nuisance, rank, alignment, covariance, and regularization choices without evaluation-participant responses and without held-out stimulus content.

C2 has one participant and one story. It can generalize only to new measurements or time blocks within that fixed participant-story acquisition. Resampling voxels, repeat subsets, or contiguous blocks cannot create a story-population or participant-population claim. This matches E031's existing scope restriction.

Schütt et al. do not require E031 to adopt their full bootstrap algorithm. They require the report to name the generalization target and keep the corresponding units intact. With only five C1 evaluation participants, E031's prospective power gate and full participant-level reporting remain more important than an elaborate asymptotic procedure.

## Verified

Canonical metadata, two-factor bootstrap and crossvalidation logic, fixed-versus-flexible model distinction, noise-ceiling comparisons, supported generalization scopes, simulation and empirical validation, and computational limits were checked in the primary arXiv paper body. Details not determined for the E031 design are marked as `\gap`. All findings remain external-paper evidence.

## Related

- [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md) - repeat-stable, participant-preserving biological supervision
- [`E031`](../../experiments/E031_biological-target-information-recovery.md) - prospective target-information recovery gate
- [Diedrichsen et al. 2020](diedrichsen-2020_whitened-unbiased-rdm-similarity.md) - whitened unbiased RDM comparison
- [Lage-Castellanos et al. 2019](lage-castellanos-2019_fmri-noise-ceiling.md) - fMRI reliability and noise-ceiling framework
- [`literature/AGENTS.md`](../AGENTS.md) - canonical literature-note contract
