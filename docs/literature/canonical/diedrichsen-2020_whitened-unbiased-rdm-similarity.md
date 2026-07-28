---
title: "Comparing representational geometries using whitened unbiased-distance-matrix similarity"
tags: [literature]
aliases: [diedrichsen-2020_whitened-unbiased-rdm-similarity]
---

# Comparing representational geometries using whitened unbiased-distance-matrix similarity

**Jörn Diedrichsen, Eva Berlot, Marieke Mur, Heiko H. Schütt, Mahdiyar Shahbazi, and Nikolaus Kriegeskorte / 2020 / arXiv preprint** · **Link:** [arXiv:2007.02789](https://arxiv.org/abs/2007.02789)

## TL;DR

Representational dissimilarities estimated from noisy neural patterns have two distinct problems: ordinary squared distances are positively biased by measurement noise, and the many pairwise distances in an RDM have correlated estimation errors. Diedrichsen et al. combine crossvalidated distances with whitening by the expected RDM-error covariance, yielding whitened unbiased RDM cosine similarity, or WUC.

For [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md), WUC provides a concrete repeat-aware alternative to fitting raw neural coordinates. For [`E031`](../../experiments/E031_biological-target-information-recovery.md), it is a candidate comparison or target geometry only where independent repeat or run partitions exist; it is not a denoiser, shared-participant model, or biological-specificity test by itself.

## Key ideas

### Crossvalidation removes distance bias

Let \(\hat B_m\) be independently estimated activity patterns for all conditions in partition \(m\). A squared Euclidean or Mahalanobis distance computed within one noisy partition includes noise power and is therefore positive even when two true condition patterns are identical.

The crossvalidated Mahalanobis distance, commonly called crossnobis, forms the condition difference in one partition and takes its inner product with the difference estimated in another independent partition. Independent noise terms have zero expected cross-product, so the estimator is unbiased and can be negative in finite data. A negative estimate is not an invalid distance; it is sampling variation around a true distance that may be zero.

Crossvalidation trades bias for variance. It requires genuinely independent partitions and a noise-precision estimate learned without leaking the evaluated condition contrast.

### RDM errors must be whitened

Distances sharing a condition also share pattern-estimation error, so RDM entries are not independent. Treating every RDM cell as equally precise and independent yields suboptimal model comparison.

The paper derives the mean and covariance of biased and crossvalidated squared Euclidean and Mahalanobis distances. For a practical whitening matrix, it uses the covariance structure expected under zero true distances:

\[
\operatorname{Var}(\tilde{\mathbf d})
=
c(\Xi \circ \Xi)
=
cV,
\]

where \(\Xi\) captures condition-estimate covariance and \(c\) is an irrelevant common scale for the similarity calculation. The WUC criterion is

\[
\tilde r_W
=
\frac{\tilde{\mathbf d}^{\top}V^{-1}\mathbf m}
{\sqrt{
(\tilde{\mathbf d}^{\top}V^{-1}\tilde{\mathbf d})
(\mathbf m^{\top}V^{-1}\mathbf m)
}},
\]

for crossvalidated data distances \(\tilde{\mathbf d}\) and a model RDM vector \(\mathbf m\). A whitened Pearson form additionally removes each RDM's mean when the model claim is invariant to an additive distance offset.

The choice between cosine and correlation is scientific. Cosine evaluates the predicted distance scale from a meaningful zero, while correlation discards the mean distance and evaluates only deviations around it.

## Evidence

The paper uses analytical derivations and simulations across several experimental designs to compare biased and unbiased distance estimators, whitened and unwhitened RDM comparisons, and pattern-component-model likelihood as a theoretical reference under Gaussian assumptions.

- Ignoring RDM-error covariance had previously produced 3% to 12% fewer correct model-selection decisions than the full likelihood-ratio reference in the simulation regimes discussed by the paper.
- WUC substantially increased model-selection power and performed close to the pattern-component-model likelihood reference for normally distributed data.
- The zero-distance covariance approximation remained useful under violations of the idealized noise assumptions tested by the authors.
- Biased whitened RDM cosine is shown to connect to the RV coefficient and linear centered-kernel alignment; WUC adds crossvalidated unbiased distances.

These results concern model comparison under simulated and example neural-data conditions. They do not establish that WUC-trained representations improve a downstream model.

## Limitations

1. **Independent partitions are load-bearing.** Reusing the same repeat, run, or temporally dependent residuals on both sides restores bias.
2. **WUC estimates geometry, not a latent response.** It discards absolute neural coordinates and cannot by itself predict an untouched participant's response.
3. **The whitening model is approximate.** The practical \(V\) uses the covariance structure under zero distances. This avoids difficult signal-covariance estimation but is not the exact error covariance for every dataset.
4. **Noise precision must be estimated.** Poorly regularized voxel covariance or leakage in precision estimation can erase the intended advantage of Mahalanobis normalization.
5. **Negative distances require compatible downstream code.** Clipping them at zero would reintroduce bias.
6. **No biological-specificity control.** A stimulus or text representation can reproduce neural geometry; WUC does not identify which information is uniquely biological.
7. **No participant or condition population inference.** The paper's similarity estimator does not replace the two-factor inferential treatment developed by [Schütt et al. 2021](schutt-2021_statistical-inference-representational-geometries.md).

## Relevance to this thesis

### Relevance to H002

WUC sharpens H002's fourth target family, repeat-crossvalidated representational geometry. It estimates the repeat-stable differences among stimuli without requiring a model to reproduce raw voxel axes, and it downweights RDM directions whose estimation errors are correlated or large.

The geometry can still be nonbiological. H002 therefore needs the same nuisance subtraction, text-matched target, deranged twin, and untouched biological-view prediction required for coordinate targets. Higher WUC against a participant-average RDM is not sufficient evidence of participant-preserving biological information.

### Relevance to E031

The LeBel C2 substrate has disjoint builder and evaluation repeats, but E031 currently freezes arithmetic response means so that repeat count is the only manipulated factor. WUC is therefore a design anchor or separately preregistered follow-on, not an unannounced replacement for C2.

For a later geometry arm, all noise precision, condition covariance, distance estimation, whitening, and dimensionality choices must be fit inside builder repeats and outer training time blocks. The scored target must predict an untouched biological view and beat both an unweighted biological geometry and a capacity- and structure-matched content-destroyed geometry.

The Tuckute C1 data do not provide repeated measurements of each participant-condition response in the same way. A crossnobis arm there requires an independently justified partition structure; participant identity cannot be treated as interchangeable repeat noise because that changes H002's estimand.

## Verified

Canonical metadata, bias derivation, crossvalidated-distance rationale, RDM-error covariance, WUC equation, cosine-versus-correlation distinction, simulation comparisons, and stated robustness were checked in the primary arXiv paper body. The exact peer-reviewed venue and DOI are `\gap` here because the requested canonical source was arXiv:2007.02789. All reported values remain external-paper evidence.

## Related

- [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md) - repeat-stable, participant-preserving biological supervision
- [`E031`](../../experiments/E031_biological-target-information-recovery.md) - prospective target-information recovery gate
- [Schütt et al. 2021](schutt-2021_statistical-inference-representational-geometries.md) - subject-by-condition model-comparative inference
- [Prince et al. 2022](prince-2022_glmsingle.md) - repeat-supervised single-trial fMRI estimation
- [`literature/AGENTS.md`](../AGENTS.md) - canonical literature-note contract
