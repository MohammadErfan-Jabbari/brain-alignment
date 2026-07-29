---
title: "Uncovering Cortical MEG Responses to Listened Audiobook Stories"
tags: [literature]
aliases:
  - "Koskinen and Seppä 2014"
  - "Task-optimized MEG"
---

# Uncovering Cortical MEG Responses to Listened Audiobook Stories

**M. Koskinen and M. Seppä, 2014, NeuroImage 100, 263-270** · **DOI:** [10.1016/j.neuroimage.2014.06.018](https://doi.org/10.1016/j.neuroimage.2014.06.018) · **PubMed:** [PMID 24945666](https://pubmed.ncbi.nlm.nih.gov/24945666/)

## TL;DR

Koskinen and Seppä learn an individual-specific MEG spatial filter from repeated one-minute audiobook responses, test it on separate repeated trials, and then apply it to nonrepeated story listening. Their similarity-constrained multiset CCA (SimCCA) requires the same projection matrix across trial datasets, so it is genuinely compatible with unseen-repeat application. The paper reports signal-to-noise improvements up to 20-fold and little comparable benefit from PCA or ICA alone. That result comes from a much richer repeat-calibration regime and a multi-stage preprocessing pipeline, so it motivates E032 but does not predict its outcome.

## Key ideas

### Exact estimator and constraint

For repeated trial matrices \(X_i\), the method forms projected responses

\[
Y_i = X_i W
\]

and chooses \(W\) so the projected time courses agree maximally across repeated trials. The defining similarity constraint is that the same matrix \(W\) is used for every trial dataset. For one component \(w\), this is the shared-filter multiset-CCA objective later written in CorrCA form:

\[
\max_w
\frac{
w^\top
\left(\sum_i\sum_{j \ne i} X_i^\top X_j\right)
w
}{
w^\top
\left(\sum_i X_i^\top X_i\right)
w
}.
\]

An overall constant changes the score's scale but not the maximizing filter. The first canonical variate is the direction with the largest repeat agreement under this constraint. The shared \(W\) is the important operational fact: after training, the same sensor-space transform can be applied to a new repeated or nonrepeated recording from that individual.

The paper calls this estimator similarity-constrained CCA or SimCCA. It belongs to the same shared-projection generalized-eigenvalue family that Parra et al. later formalize as CorrCA. It should not be described as assigning a separate filter to each repeat.

### Held-out design

The primary method assessment separates fitting from testing:

- 33 one-minute repeated trials are used for model training;
- 15 separate one-minute repeated trials are used for primary performance testing; and
- the learned filter is then applied to responses to nonrecurring audiobook stories.

This distinction matters. Improvement on the 33 fitting trials alone would not show that the filter captured a stable response rather than trial-specific noise. The 15-trial test set probes transfer to unseen repetitions, while application to nonrecurring stories probes whether the calibrated sensor transform can be used when repeat averaging is unavailable.

### Processing pipeline and comparison methods

The paper places SimCCA inside a broader SSS-PCA-wavelet-SimCCA-ICA processing sequence. Its analyses cover the 204 planar gradiometer channels and compare the task-optimized result with PCA and ICA representations.

The reported improvement therefore belongs to the evaluated pipeline and data regime. It cannot be attributed cleanly to one algebraic step or treated as a universal multiplier for an independently preprocessed dataset.

### Regularization and component constraints

The verified paper material establishes a shared \(W\), the use of the leading canonical variate, and a separate 33-trial/15-trial fit-test design. It does not expose a prospective E032-compatible shrinkage grid, a four-exposure nested selection rule, or a moving-block uncertainty procedure.

This absence is operationally important. E032 cannot import an unstated regularizer or infer a component count from the reported maximum signal-to-noise improvement. With only four builder exposures, E032 precommits to one component and explicit shrinkage selection. Those are thesis design choices for variance control, not claims that Koskinen and Seppä used the same rule.

## Evidence

The paper supports the following claims:

- response repeatability can be used as an unsupervised target for learning an individual-specific MEG spatial filter;
- SimCCA constrains the projection matrix to be shared across repeated trial datasets;
- the filter is trained on repeated trials, assessed on separate repeated trials, and then applied to nonrecurring story responses;
- the evaluated method produced signal-to-noise improvements of up to 20-fold in that study; and
- PCA and ICA alone did not produce a notable comparable signal-to-noise improvement.

These are external findings. They do not show that:

- Kymata's preprocessing leaves the same recoverable signal;
- four builder exposures are enough to estimate a stable filter;
- the recovered signal is linguistic rather than acoustic, technical, or otherwise repeat-locked;
- repeat-optimized filtering improves encoding into any language model;
- a denoised target improves distillation; or
- one language-model layer or loss location is preferable.

## Limitations

- The 33-training-trial and 15-test-trial calibration regime is far richer than E032's four builder and four evaluation exposures.
- The up-to-20-fold figure is a maximum from one study, not a prospective effect size for Kymata.
- The multi-stage pipeline limits attribution of the gain to SimCCA alone.
- The learned filter is individual- and acquisition-specific. Transfer depends on stable sensor geometry and source mixing.
- Repeated calibration segments and nonrecurring audiobook segments can differ in attention, adaptation, movement, and response stationarity.
- Repeatability does not distinguish linguistic content from repeat-locked acoustics or nuisance.
- The paper does not implement E032's sealed builder/evaluation contract, fixed shrinkage grid, matched PCA1 baseline, shifted controls, or moving-block inference.
- The method remains linear and time-alignment dependent.

## Relevance to this thesis

This paper is direct precedent for the theory behind [H002](../../hypotheses/H002_repeat-stable-biological-supervision.md): repeated naturalistic MEG can supervise a spatial filter without language labels, and that filter can be applied where repeated averaging is unavailable.

For [E032](../../experiments/E032_kymata-cross-run-repeat-recovery.md), the most useful lesson is the estimator's transfer structure. SimCCA does use one shared \(W\). CorrCA remains the cleaner primary implementation for E032 because its covariance ratio, shrinkage path, component ordering, and held-out testing rules can be stated and audited directly under the much smaller Kymata repeat budget.

The practical translation is:

- learn only from builder exposures;
- fit one shared sensor filter;
- choose regularization without touching evaluation exposures;
- apply the fixed transform to unseen cross-run repeats; and
- compare against equal-dimensional nonbiological baselines and shifted controls.

If E032 passes, Koskinen and Seppä make a later application to nonrepeated language-model stimuli more plausible. The thesis would still need a separate content-specific experiment before the filtered signal could be called biological supervision, and a further intervention before it could be placed in a loss at any model layer.

## Verified

Publication metadata and the study's main claims were checked against the PubMed record and DOI metadata. The 33-training-trial/15-test-trial split, the common-\(W\) SimCCA constraint, the leading-variate analysis, and the processing sequence were checked against indexed passages from the author manuscript. Exact regularization details not visible in those verified passages are deliberately left unspecified rather than inferred.

## Related

- [H002: repeat-stable biological supervision](../../hypotheses/H002_repeat-stable-biological-supervision.md)
- [E032: Kymata cross-run repeat recovery](../../experiments/E032_kymata-cross-run-repeat-recovery.md)
- [Research landscape](../../01-research-landscape.md)
- [Parra et al. 2019: correlated components analysis](parra-2019_correlated-components-analysis.md)
- [Literature note contract](../AGENTS.md)
