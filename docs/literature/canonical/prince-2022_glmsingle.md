---
title: "Improving the accuracy of single-trial fMRI response estimates using GLMsingle"
tags: [literature]
aliases: [prince-2022_glmsingle]
---

# Improving the accuracy of single-trial fMRI response estimates using GLMsingle

**Jacob S. Prince, Ian Charest, Janik W. Kurzawski, John A. Pyles, Michael J. Tarr, and Kendrick N. Kay / 2022 / eLife 11:e77599** · **Link:** [DOI 10.7554/eLife.77599](https://doi.org/10.7554/eLife.77599) · **Full text:** [PMC9708069](https://pmc.ncbi.nlm.nih.gov/articles/PMC9708069/)

## TL;DR

GLMsingle is a single-trial fMRI estimation pipeline, not a generic neural-network denoiser. It combines voxel-specific hemodynamic-response-function selection, cross-validated nuisance regression, and voxel-specific fractional ridge regression; across three task-fMRI datasets, its complete beta estimates were more repeat-reliable and more useful for representational and decoding analyses than a canonical-HRF ordinary-least-squares baseline.

For [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md), the important mechanism is that repeats are used to choose how much nuisance removal and shrinkage to apply, rather than being averaged away before target construction. For [`E031`](../../experiments/E031_biological-target-information-recovery.md), GLMsingle is an upstream beta-estimation option only if raw time series, event designs, and condition repetitions are available; it is not a post-hoc operation that can be assumed to improve already-produced response arrays.

## Key ideas

### Four nested beta versions isolate the mechanism

1. **b1, AssumeHRF:** fit a conventional single-trial GLM with one canonical HRF and ordinary least squares.
2. **b2, FitHRF:** for each voxel, fit the design with each of 20 empirically derived HRFs and retain the HRF with the highest time-series variance explained. HRF choice is not cross-validated because the method treats the library members as equally admissible shapes rather than as a regularization path.
3. **b3, FitHRF + GLMdenoise:** identify a noise pool from in-brain voxels with negligible experiment-related ON-OFF variance, run PCA on those voxels separately by run, and add the leading noise-component time courses to the GLM one at a time. Choose the number of components that maximizes cross-validated beta predictivity over repeated conditions.
4. **b4, FitHRF + GLMdenoise + RR:** apply fractional ridge regression and select a shrinkage fraction separately for each voxel using the same repeat-based cross-validation framework. The default output then applies a post-hoc scale and offset to match the unregularized beta distribution, because ridge otherwise biases amplitudes toward zero.

Every variant also includes run-wise polynomial baseline regressors. An initial ON-OFF GLM supplies experiment-related variance estimates used to define the noise pool.

### Repeats provide the supervision for denoising

The nuisance-component count and ridge fraction are tuned by asking whether beta estimates from one occurrence of a condition predict beta estimates from other occurrences. This is the central relevance to H002: repeated measurements supply a criterion for preserving repeat-stable stimulus information while suppressing variance that does not generalize across repeats.

This criterion also defines the failure boundary. If within-condition variation is itself the scientific signal, for example trial-specific learning, behavior, or adaptation, then treating disagreement across repeats as noise may remove information of interest. The paper explicitly discusses this issue and recommends disabling or modifying components when the hypothesis depends on neighboring trials or genuine trial-to-trial variability.

### The three components attack different error sources

- Voxel-specific HRF selection reduces bias from imposing one response shape across regions and subjects.
- Noise-pool principal components absorb spatially shared physiological, motion, instrumental, or other nuisance variance without requiring a hand-enumerated nuisance model.
- Fractional ridge reduces variance caused by collinear single-trial regressors, especially in rapid event-related designs where adjacent BOLD responses overlap.

The final product remains a biased estimator. Ridge can make neighboring trial amplitudes more similar, and the optional autoscaling corrects marginal scale but cannot prove that trial-level structure is unbiased.

## Evidence

### Datasets and evaluation

- **Natural Scenes Dataset (NSD):** large-scale 7T visual fMRI with repeated natural images. The reported group summaries use four subjects. Repeated stimuli generally had three instances in the analyzed data.
- **BOLD5000:** natural-image fMRI collected under different acquisition and timing conditions. The reported group summaries use four subjects; repeated stimuli had three or four instances depending on subject. Because repetitions were sparse within a session, the authors processed rescaled groups of five sessions together.
- **StudyForrest music experiment:** 16 subjects, 25 six-second musical clips, eight repetitions per condition, one occurrence per run across eight runs. This provides a smaller, auditory, jittered-design replication.

The primary signal-quality measure was voxelwise test-retest Pearson correlation across split halves of repeated-condition response profiles. The paper also evaluated least-squares separate estimation, temporal autocorrelation, between-subject representational-dissimilarity-matrix agreement within and across NSD and BOLD5000, and image-identity decoding with leave-one-repetition-out linear SVMs.

### Outcomes

- b4 improved repeat reliability over b1 for every analyzed subject in NSD and BOLD5000, with the clearest and most nearly voxel-uniform gains in NSD. The intermediate b2 and b3 results showed that HRF fitting, nuisance regression, and ridge each added benefit.
- The StudyForrest analysis reproduced reliability gains across all 16 subjects, including for highly reliable voxels, despite its different modality, scale, and timing.
- b4 strengthened representational-dissimilarity agreement across subjects and even across NSD and BOLD5000, consistent with recovery of shared stimulus-related structure rather than only within-dataset idiosyncrasy.
- In the image-identity MVPA analysis, mean accuracy with b4 was approximately three times the b1 accuracy in NSD and approximately twice the b1 accuracy in BOLD5000. These are external-paper results, not thesis measurements.
- GLMsingle generally outperformed least-squares separate estimation in the paper's repeat-reliability comparison.

The paper does not report one universal numeric reliability gain. Effects vary by dataset, subject, voxel-reliability threshold, and component, so importing a single figure-read value as a general effect size would be misleading.

## Controls and comparisons

- The b1 to b4 nesting is an ablation sequence against a conventional canonical-HRF OLS baseline.
- Least-squares separate estimation is a method-family comparator for rapid event-related designs.
- NSD, BOLD5000, and StudyForrest vary in field strength, timing, task modality, number of conditions, and repetition structure.
- Repeat split-halves, cross-subject RDM agreement, cross-dataset RDM agreement, and image decoding probe different consequences of beta quality.

These controls support the claim that the complete estimation pipeline improves useful repeat-stable signal. They do not establish that every removed component is nonbiological, nor do they test whether a GLMsingle-derived target contributes unique biological information beyond a geometry-matched text or stimulus model.

## Limitations

1. **Repeated discrete conditions are required.** The cross-validated nuisance and ridge procedures cannot be used as designed when every condition occurs once. The method is not intended for resting-state data or continuous naturalistic paradigms such as uninterrupted stories and movies.
2. **Repeat stability is an estimand choice.** True trial-specific cognitive or behavioral variation can be penalized as noise. This is especially relevant if a biological loss aims to preserve state changes rather than stimulus-locked responses.
3. **Hyperparameter selection is noisy.** The paper leaves the minimum amount of data needed for accurate nuisance-count and ridge selection unresolved.
4. **The HRF library is constrained and NSD-derived.** Selecting among 20 shapes reduces variance relative to flexible HRF fitting, but the library may not cover every subject, region, task, or acquisition regime.
5. **Ridge introduces structured bias.** It can smooth amplitudes across neighboring trials. Autoscaling repairs overall scale and offset, not necessarily the local response geometry.
6. **Benefits are SNR- and design-dependent.** Improvements were smaller and more variable in lower-SNR BOLD5000 data, and ridge has less room to help when trials are widely separated.
7. **No biological-specificity control.** The work estimates fMRI responses; it does not compare the recovered target against matched stimulus-only, text-only, deranged, or nuisance-only targets.
8. **No sealed downstream intervention.** More reliable betas and stronger decoding do not show that using those betas as a training loss improves a separate model.

## Relevance to this thesis

### Relevance to H002

GLMsingle is a concrete precedent for the claim that the useful object is not necessarily the raw biological coordinate. It operationalizes a conservative target builder in which repeats select voxel-specific HRF, nuisance, and shrinkage choices, and its nested beta versions make the information-recovery mechanism testable.

It also sharpens H002's guardrail: "denoising" is not neutral. GLMsingle preserves what repeats predict and may attenuate non-repeat-stable biology. A thesis target therefore needs an explicit estimand, sealed repeats or participants for evaluation, and controls that separate repeat-stable biology from stable stimulus structure already recoverable without brain data.

### Relevance to E031

E031 currently tests recoverability from recorded, verified LeBel response arrays and explicitly seals evaluation repeats or participants from target construction. GLMsingle cannot be inserted into that arm as if it were a matrix-level filter. A GLMsingle arm would require a separately frozen path from raw BOLD time series and event designs to beta estimates, with all HRF, noise-pool, nuisance-count, ridge, and scaling choices fit strictly inside the builder folds.

If that substrate exists, the smallest informative comparison is not "GLMsingle versus raw" alone. It is b1 versus b2 versus b3 versus b4, each evaluated on an untouched biological view and against E031's deranged and matched nonbiological controls. If the substrate does not exist, this paper remains a design anchor rather than an executable E031 method.

## Verified

Read in full from the primary eLife article in PMC, including Results, Materials and methods, Discussion, limitations, implementation guidance, and author response. Method descriptions and outcome statements above were checked in the article body rather than inferred from the abstract. All numerical values are external-paper evidence only and do not become thesis numbers.

## Related

- [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md) - repeat-stable, participant-preserving biological supervision
- [`E031`](../../experiments/E031_biological-target-information-recovery.md) - prospective target-information recovery gate
- [Lage-Castellanos et al. 2019](lage-castellanos-2019_fmri-noise-ceiling.md) - fMRI reliability and noise-ceiling framework
- [`literature/AGENTS.md`](../AGENTS.md) - canonical literature-note contract
