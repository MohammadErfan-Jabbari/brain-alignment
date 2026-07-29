---
title: "Correlated Components Analysis: Extracting Reliable Dimensions in Multivariate Data"
tags: [literature]
aliases:
  - "Parra et al. 2019"
  - "CorrCA"
---

# Correlated Components Analysis: Extracting Reliable Dimensions in Multivariate Data

**Lucas C. Parra, Stefan Haufe, and Jacek P. Dmochowski, 2019, Neurons, Behavior, Data Analysis, and Theory 2(1), article 001c.7125** · **DOI:** [10.51628/001c.7125](https://doi.org/10.51628/001c.7125) · **Preprint:** [arXiv:1801.08881](https://arxiv.org/abs/1801.08881)

## TL;DR

Correlated components analysis (CorrCA) learns one linear spatial projection shared across repeated measurements and orders components by repeat reliability. Its shared filter, explicit generalized-eigenvalue estimator, and independent-test regularization make it a strong candidate for determining whether Kymata contains a repeat-stable biological subspace before any language-model alignment or loss experiment. The paper shows that CorrCA can recover reliable dimensions better than PCA of the repeat average at low signal-to-noise ratio and can generalize better than more flexible multiset CCA. Those are external paper results, not evidence that the thesis data contain usable biological supervision.

## Key ideas

### Exact estimator

Let \(X_i \in \mathbb{R}^{T \times D}\) be the centered data from repeat or subject \(i \in \{1,\ldots,N\}\), with matched samples across datasets. Define

\[
R_W = \sum_{i=1}^{N} X_i^\top X_i
\]

and

\[
R_B = \sum_{i=1}^{N}\sum_{j \ne i} X_i^\top X_j.
\]

For a shared spatial filter \(w \in \mathbb{R}^{D}\), CorrCA maximizes

\[
\rho(w)
=
\frac{1}{N-1}
\frac{w^\top R_B w}{w^\top R_W w}.
\]

The stationary solutions are the generalized eigenvectors

\[
R_B W = R_W W \Lambda.
\]

Under these definitions, the component-wise inter-dataset correlations are the generalized eigenvalues divided by \(N-1\): \(\rho_k=\Lambda_{kk}/(N-1)\). The eigenvectors are ordered identically under either scaling and are mutually uncorrelated with respect to \(R_W\). Unlike ordinary unconstrained multiset CCA, CorrCA uses the same \(w\) for every repeat, so the learned filter can be applied directly to a new repeat with the same feature coordinates.

### What the objective means

The numerator rewards covariance that recurs across repeats. The denominator normalizes by total within-repeat variance. Under the paper's shared-signal model, this ratio is equivalent to a repeat-reliability signal-to-noise criterion: variance of the repeat mean relative to average variance around that mean.

This objective does not identify a biological source merely because it is reliable. Stimulus acoustics, preprocessing artifacts, environmental interference, head-position structure, or any nuisance that repeats with the stimulus can also score highly. Repeat reliability is therefore a necessary information-recovery test, not a biological-specificity test.

### Regularization

The generalized eigenproblem becomes unstable when \(R_W\) is poorly conditioned. The paper describes two remedies.

Truncated singular-value decomposition keeps only \(K\) eigen-directions of \(R_W\):

\[
\widetilde R_W^{-1}
=
\widetilde U_W \widetilde\Lambda_W^{-1}\widetilde U_W^\top.
\]

Shrinkage instead uses

\[
\widetilde R_W
=
(1-\gamma)R_W
+
\gamma \bar{\lambda}I,
\qquad
\bar{\lambda}
=
\frac{\operatorname{tr}(R_W)}{D}.
\]

Shrinkage retains the full sensor dimension. Truncation gives components that remain strictly uncorrelated under the retained \(R_W\) representation, whereas shrinkage only approximately preserves that property under the original covariance. In both cases, \(K\) or \(\gamma\) is a fitted hyperparameter and must be selected without looking at the final evaluation repeats.

The paper recommends selecting regularization on training data and scoring reliability on independent test data. High training reliability is not enough: its simulations and EEG comparison show that flexible or weakly regularized estimators can inflate training scores when signal-to-noise ratio is low.

### Components and statistical testing

CorrCA returns up to \(D\) ordered components, but the existence of an eigenvector does not imply that it generalizes. The paper treats held-out reliability as the meaningful score. For independent observations an analytic \(F\) test is possible, but ordinary time samples violate that assumption when the signal is autocorrelated.

For time series, the paper recommends surrogate nulls such as circular temporal shifts or phase scrambling. Testing the maximum component score in each surrogate realization can control selection across components. This is directly relevant to avoiding a post hoc choice of the best-looking Kymata component.

### Why the shared filter matters

CorrCA estimates \(D\) parameters per component. Multiset CCA estimates a separate projection for each of \(N\) datasets, or roughly \(ND\) parameters per component. The extra freedom can increase training correlation while worsening transfer to unseen data.

In the paper's 18-subject, 64-channel, 197-second EEG example, regularized multiset CCA used a 12-dimensional truncated representation and 216 parameters per component. It achieved higher training inter-subject correlation but lower independent-test correlation than CorrCA for four of the first five components. Three CorrCA components and one multiset-CCA component were significant on the independent test data. These counts describe that paper's dataset and split; they are not expected outcomes for Kymata.

## Evidence

The paper supports the following claims:

- CorrCA is the generalized-eigenvalue estimator above and uses a single projection shared across repeats or subjects.
- In simulations, CorrCA recovers shared sources better than PCA of the repeat or subject average at medium and low signal-to-noise ratio.
- Training reliability becomes optimistic at low signal-to-noise ratio, so regularization and held-out scoring are load-bearing.
- More flexible multiset CCA can overfit relative to CorrCA despite stronger training correlation.
- CorrCA depends on approximately stable spatial mixing and time alignment across repeats.

None of these results establish that:

- Kymata MEG or EEG has a recoverable repeat-stable component;
- a recovered component contains linguistic rather than acoustic or technical structure;
- denoising will improve brain-to-language-model alignment;
- a brain-derived target is useful in a distillation loss; or
- any particular language-model layer should receive that loss.

Those are thesis questions that require evidence from the repository's experiment records.

## Limitations

- CorrCA is linear. Nonlinear repeat-stable structure is outside its estimator.
- It assumes matched samples across repeats. Relative latency shifts reduce recovered reliability.
- It assumes sufficiently stable spatial mixing. Movement, sensor changes, or subject-specific mixing can violate this assumption.
- Any repeat-locked nuisance can be recovered alongside neural signal.
- The leading component need not be the most linguistically informative component.
- Component selection, shrinkage, and all preprocessing choices can overfit if chosen on evaluation repeats.
- Significance procedures must respect temporal autocorrelation and component selection.
- The paper's multi-subject EEG demonstrations have more independent datasets than E032's single-participant, few-repeat design.

## Relevance to this thesis

For [E032](../../experiments/E032_kymata-cross-run-repeat-recovery.md), CorrCA is best understood as an information-recovery assay. It asks whether one projection learned from builder exposures recovers a repeat-stable signal in sealed evaluation exposures.

E032 makes the paper's estimator more conservative for the available data:

- it fits only one CorrCA component;
- it selects \(\gamma\) from a fixed shrinkage grid inside builder exposures using contiguous time blocks;
- it resolves ties toward stronger shrinkage;
- it fits the final filter on all builder exposures only after \(\gamma\) is fixed;
- it evaluates cross-run repeat pairs that were not used to choose \(\gamma\);
- it compares against a matched PCA1 baseline and shifted controls; and
- it treats MEG gradiometers as primary and EEG as secondary.

The one-component restriction is not a claim that neural information is one-dimensional. It is a variance-control decision for four builder exposures and prevents component selection from becoming an additional hidden search.

A positive E032 result would support the narrower claim in [H002](../../hypotheses/H002_repeat-stable-biological-supervision.md) that a repeat-stable subspace is recoverable. It would license a later content-specific assay. It would not yet license adding CorrCA output to a loss, choosing a language-model layer, or claiming biological specificity.

## Verified

Checked against the final journal record and article, including the estimator, regularization section, simulation conclusions, significance guidance, and EEG comparison. Publication metadata were cross-checked against the journal page. The arXiv record is the 2018 preprint; this note uses the 2019 final publication year.

## Related

- [H002: repeat-stable biological supervision](../../hypotheses/H002_repeat-stable-biological-supervision.md)
- [E032: Kymata cross-run repeat recovery](../../experiments/E032_kymata-cross-run-repeat-recovery.md)
- [Research landscape](../../01-research-landscape.md)
- [Koskinen and Seppä 2014: task-optimized MEG](koskinen-2014_task-optimized-meg.md)
- [Literature note contract](../AGENTS.md)
