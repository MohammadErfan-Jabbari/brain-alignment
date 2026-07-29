---
title: "Independent-component-based encoding models of brain activity during story comprehension"
tags: [literature]
aliases: [hari-2026_independent-component-encoding-models, hari-2026]
---

# Independent-component-based encoding models of brain activity during story comprehension

**Kamya Hari, Taha Binhuraib, Jin Li, Cory Shain, and Anna A. Ivanova / 2026 / arXiv preprint** · **Link:** [arXiv:2604.24942](https://arxiv.org/abs/2604.24942) · **Code:** [IC-Encoding-Models](https://github.com/kamyahari/IC-Encoding-Models)

## TL;DR

Hari et al. replace voxelwise targets with subject-specific independent-component time series for encoding naturalistic story-listening fMRI. They fit 100 spatial components per participant on three stories that are separate from the 22 encoding-model training stories and the repeated held-out test story, then keep the spatial maps fixed when projecting the remaining data into component space.

The result makes ICA a serious candidate target builder for [`E031`](../../experiments/E031_biological-target-information-recovery.md): highly predicted components often correspond to auditory or language networks, while ICA-AROMA noise-labelled components have low encoding predictivity. It does not establish that IC targets are superior to matched voxel or ROI targets for this thesis's estimand, and its test-ranked top-component figures cannot be reused as a target-selection rule.

## Key ideas

### Separate component estimation from encoding evaluation

The paper uses the [LeBel natural-language fMRI dataset](https://doi.org/10.1038/s41597-023-02437-z), with eight participants listening to 26 complete naturalistic stories. For each participant, three stories define the subject-specific ICA basis, 22 different stories train the encoding models, and one repeated story is held out and averaged for the main test.

The ICA estimation stories are preprocessed with fMRIPrep, gray-matter masking, confound regression, temporal filtering, spatial smoothing, detrending, and standardization. The encoding train and test stories use the corresponding fMRIPrep, masking, confound-regression, detrending, and standardization path without the ICA-set temporal filtering and spatial smoothing.

The model order is fixed at 100 components per participant. Once the spatial component maps are estimated from the three ICA stories, they are held fixed. Time series for the 22 training stories and the held-out story are obtained by projecting their voxelwise data through the pseudoinverse of that fixed spatial basis, rather than by refitting ICA on those stories.

### Predict component time series from stimulus features

The encoding targets are the projected component time series. The paper uses word rate, lexical surprisal, and contextualized Pythia-410M representations as stimulus features, aligns them to fMRI with a finite-impulse-response model, and fits ridge-regression encoding models with cross-validation.

Prediction is evaluated by Pearson correlation between predicted and observed component time series. ICA-AROMA labels components using motion- and artifact-related spatial and temporal features, but the labelled components are retained for analysis rather than automatically removed from the target space.

### Interpret components as candidate functional networks

To associate components with auditory, language, and visual networks, the paper compares thresholded component maps with reference atlases and assigns the best spatial match. Highly predicted components often map to auditory or language networks, whereas visual components are weak for the auditory story-listening task.

The paper also matches components across participants using temporal and spatial similarity. This provides evidence that some strongly predicted subject-specific components have corresponding temporal dynamics and spatial organization across people, without requiring one fixed group atlas as the target basis.

## Evidence

- The component basis, encoding-training data, and main test data are separated by story: three stories for ICA estimation, 22 for encoding-model fitting, and one repeated held-out story for evaluation.
- The held-out stories are projected into fixed spatial maps learned only from the ICA-estimation stories.
- Each participant has 100 estimated components.
- Encoding predictivity is non-uniform across components. The paper's highlighted top-component figures rank components by Pearson correlation on the held-out repeated test story, and the highlighted components often correspond to auditory or language networks.
- Temporal-shuffle permutation tests with multiple-comparison correction show that stimulus features predict many component time series above the paper's null procedure.
- ICA-AROMA components labelled as noise or motion artifacts have low encoding predictivity and do not dominate the highly predicted components.
- The appendix compares IC encoding models with voxelwise models and anatomical ROI-average models. IC models are easier to compare at a network level and can adapt to subject-specific spatial organization, but the comparison changes the prediction unit and target aggregation at the same time.

## Limitations

1. **The highlighted target ranking uses the held-out test story.** The paper's top-IC figures select components by their held-out test predictivity. That is valid for descriptive result presentation, but selecting a biological-loss target from the same ranking would leak the evaluation outcome into target construction. Any thesis use must choose the component count, retained components, atlas correspondence, and target weighting strictly inside builder folds, with evaluation stories or repetitions sealed.
2. **No matched target-space superiority result.** The voxel, anatomical ROI-average, and IC comparisons use different coordinate systems, aggregation levels, dimensionalities, and noise properties. The paper therefore does not clearly establish that an IC target is better than geometry-, learnability-, and optimization-matched voxel or ROI targets for the estimand in [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md).
3. **Stimulus predictivity is not biological specificity.** Low predictivity for ICA-AROMA noise labels argues against a simple motion-artifact explanation, but a component can be highly predictable because it tracks text, word timing, acoustics, or another stable nuisance shared with the stimulus. Brain-specific value still requires text-only, acoustic, nuisance, temporal-shift, and geometry-matched controls.
4. **The repeated test target has higher signal-to-noise than ordinary stories.** This is useful for evaluation, but it can raise reported predictivity relative to unrepeated deployment stories and must not be conflated with an improvement caused by ICA.
5. **ICA model order remains a design choice.** The paper fixes 100 components per participant and reports qualitative robustness in preliminary alternative-order analyses, but does not provide a decisive model-order selection rule for a downstream biological loss.
6. **Correlation does not test amplitude fidelity.** The evaluation metric rewards temporal-shape agreement and is invariant to linear rescaling, so a highly correlated component target can still have poorly recovered response amplitude.
7. **No downstream intervention test.** The work evaluates encoding models. It does not show that training or distilling a language model against IC targets improves language quality, compression, biological transfer, or any other sealed endpoint.

## Relevance to this thesis

This paper is a measurement and target-construction contribution, not evidence that brain-guided distillation works. It strengthens the case for a subject-specific latent target that can pool correlated voxel signal without averaging participants or imposing one anatomical coordinate system.

For [`E031`](../../experiments/E031_biological-target-information-recovery.md), the admissible arm is a fully nested ICA builder: learn each participant's spatial basis on builder stories only, project builder and sealed data through the fixed basis, select or weight components using builder-fold evidence only, and evaluate on untouched stories or repetitions. The most important comparator is not raw voxel correlation alone, but the strongest voxel, ROI, and nonbrain target matched for dimensionality, covariance spectrum, effective rank, held-out head learnability, gradient scale, and optimization pressure.

For [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md), ICA offers a plausible way to preserve distributed participant-specific signals while reducing voxel redundancy. The hypothesis remains conditional: an IC target is useful only if it improves sealed repeat or participant transfer beyond nuisance, text, acoustic, shifted, and geometry-matched controls.

The paper should therefore change the target-builder shortlist, not the thesis verdict. It adds subject-specific ICA alongside [GLMsingle](prince-2022_glmsingle.md), repeat-crossvalidated representational targets, and participant-preserving losses as candidates to be adjudicated under one common estimand.

## Verified

Read from the full arXiv v2 HTML, including Methods, Results, Discussion, and appendix sections on cross-validation and voxelwise and ROI baselines. The public repository README was also inspected to confirm the linked preprocessing, ICA-AROMA, fixed-basis projection, component-labelling, and encoding-model workflow. The note does not treat any external-paper value as a thesis result.

## Related

- [`01-research-landscape.md`](../../01-research-landscape.md) - authoritative literature frontier map
- [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md) - repeat-stable, participant-preserving biological supervision
- [`E031`](../../experiments/E031_biological-target-information-recovery.md) - target-information recovery gate
- [Prince et al., 2022](prince-2022_glmsingle.md) - repeat-supervised single-trial fMRI estimation
- [`literature/AGENTS.md`](../AGENTS.md) - canonical literature-note contract
