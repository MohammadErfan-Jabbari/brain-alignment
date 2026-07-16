---
title: "Fine-tuning Language Encoding Models on Slow fMRI Improves Prediction for Fast ECoG"
tags: [literature]
aliases: [vaidya-2026_slow-fmri-fast-ecog-transfer]
---

# Fine-tuning language encoding models on slow fMRI improves prediction for fast ECoG

**Authors:** Aditya R. Vaidya; Richard J. Antonello; Alexander G. Huth
**Year:** 2026
**Venue:** Preprint, arXiv v1 submitted 2026-05-19
**DOI/arXiv:** 10.48550/arXiv.2605.19224
**Canonical ID:** vaidya-2026_slow-fmri-fast-ecog-transfer

**Primary sources:** [arXiv abstract](https://arxiv.org/abs/2605.19224), [HTML paper](https://arxiv.org/html/2605.19224), [PDF](https://arxiv.org/pdf/2605.19224)

## Read method

- [ ] Full PDF read page by page
- [x] Full HTML scanned with targeted reading of methods, results, figures, appendices, artifact statements, and compute statement
- [x] Extracted text cross-checked

Primary-source audit completed 2026-07-16. Comprehension self-check passed: Y.

## Comprehension summary

1. **Problem:** fMRI provides slow but spatially dense supervision, while ECoG provides fast local measurements. The paper asks whether fine-tuning a speech representation on deeply sampled fMRI transfers to ECoG recorded from entirely different people hearing different material.
2. **Core result:** WavLM Base+ models fine-tuned separately on three fMRI participants improve linear prediction of Podcast ECoG high-gamma responses relative to pretrained WavLM, and the reported ECoG benefit increases with the amount of fMRI training data.
3. **Critical boundary:** This is the strongest identified participant-, stimulus-, and modality-crossing biological transfer result for brain-tuning, but it compares primarily against pretrained WavLM. It does not isolate neural content from generic auxiliary-training, target-geometry, selection, or regularization effects.
4. **Role here:** It closes the broad claim that no brain-tuned representation has transferred across participants, stimulus, and recording modality. It is also the best prospective external adjudication target for Package A because both neural datasets are public and its missing controls align directly with the package's identification gates.

## Source grounding

**fMRI supervision.** The source is the deeply sampled natural-language fMRI dataset of LeBel et al. Each of three participants contributes approximately 17.8 to 19.7 hours and 94 to 103 training stories. A separate WavLM Base+ model is adapted for each participant using rank-4 LoRA, a rank-100 spatial readout, and a spatial-correlation objective. Training runs for 30 epochs, with the best epoch selected using two validation stories and a held-out story reserved for testing.

**ECoG transfer endpoint.** The endpoint is the public Podcast ECoG dataset: nine clinical participants, one different 30-minute podcast, 1,268 electrodes after quality control, and high-gamma activity in the 70 to 200 Hz band sampled at 20 Hz. The fMRI-tuned representation is frozen before fitting ECoG encoding readouts. Evaluation uses four-fold cross-validation and 81 candidate lags spanning -2 to +2 seconds, with a best lag selected for each electrode.

**Independence structure.** The fMRI participants and ECoG patients are disjoint, the narrated material differs, and the measurement modality changes from fMRI to ECoG. The endpoint is therefore a genuine representation-transfer test across people, content, and neural modality. It is not zero-shot neural prediction because a new ECoG encoding readout is fitted to each endpoint participant.

**Data and artifacts.** Both sources are public: [LeBel natural-language fMRI, OpenNeuro ds003020](https://openneuro.org/datasets/ds003020) and [Podcast ECoG, OpenNeuro ds005574](https://openneuro.org/datasets/ds005574). The paper does not link paper-specific training code, an environment, LoRA checkpoints, data-scaling checkpoints, preprocessing manifests, or an electrode-by-participant results table.

**Compute.** The paper reports approximately 30 GPU-hours per fMRI model and approximately 10 GPU-hours per ECoG evaluation on an NVIDIA A6000. A full seed and control matrix is therefore substantially more expensive than the original comparison.

## Core claims and exact scope

- `C1`: Fine-tuning WavLM Base+ on each of three deeply sampled fMRI participants improves prediction of ECoG responses from nine different patients relative to pretrained WavLM.
- `C2`: The transfer crosses participant, stimulus, and measurement modality. This is stronger biological generalization than same-participant or same-story held-out-sample evaluation.
- `C3`: The reported ECoG gain grows with the number of fMRI training stories, supporting a supervision-dose relationship within the implemented procedure.
- `C4`: The result establishes transfer of a learned representation, not target-specific causal value of neural content. A new linear ECoG readout still uses neural observations from each endpoint participant.

## Controls and identification gaps

The primary comparison is fMRI-tuned versus pretrained WavLM. The paper does not report a temporally permuted or participant-permuted fMRI target, a stimulus-derived auxiliary target, a language-model target, or a synthetic target matched to the fMRI target in covariance spectrum, effective rank or intrinsic dimension, scale, held-out head learnability, gradient magnitude, and update norm. It also does not report independent LoRA training seeds. The three participant-specific fMRI models measure biological-source variation, not optimizer-seed variation.

Inference is reported over electrodes using paired tests and electrode-level uncertainty, while electrodes are nested within nine ECoG participants. Population generalization therefore requires a participant-level reanalysis that first aggregates electrodes within participant, followed by paired participant contrasts, participant bootstrap or permutation intervals, and leave-one-participant-out sensitivity. The paper also searches 81 lags per electrode; the source does not make sufficiently clear for an independent audit whether lag choice and every readout hyperparameter are nested wholly within training folds.

The use of one speech architecture and one selected representation configuration limits architectural generality. No independent language-behavior, speech-utility, or compression endpoint is reported. The result is an arXiv v1 preprint and has not yet received proceedings-level peer review.

## Exact relevance to Package A

This paper removes “first transfer across participants, stimuli, and neural modalities” from the available novelty space. Package A's remaining contribution is intervention identification: whether the participant-level ECoG contrast survives correct hierarchical inference and exceeds the strongest nonbrain auxiliary intervention matched on target geometry, learnability, optimization pressure, compute, adaptation capacity, and generic model quality.

The decisive prospective sequence is: reproduce the published electrode-level result without changing the original protocol; reanalyze with participant as the biological inference unit; nest lag and readout selection inside contiguous buffered folds; repeat at least three LoRA seeds per fMRI participant; then compare fMRI tuning against permuted-fMRI, stimulus or language-model supervision, and a geometry-and-learnability-matched nonbrain target at fixed budget. The primary estimand is the participant-level ECoG difference between brain-guided and strongest matched auxiliary training, averaged across independent training seeds.

Either boundary is informative. If the original result reproduces but fails participant-level or matched-target adjudication, it is a high-value demonstration of why intervention-specific gates are necessary. If it survives, it becomes unusually strong positive evidence that slow fMRI contains target-specific information transferable to fast ECoG in unseen people and content.

## Artifact request before reproduction

Request the exact code commit and environment, the three principal LoRA checkpoints, any data-scaling checkpoints, fold and lag-selection code, preprocessing manifests, and the electrode-by-participant result table. Pre-register the reanalysis before inspecting those disaggregated outcomes. If the artifacts are unavailable, the public data permit reconstruction, but the result should be labeled a reimplementation rather than an exact reproduction.

## Read date

2026-07-16

## Related

- [`01-research-landscape.md`](../../01-research-landscape.md) - authoritative literature frontier map
- [`E025`](../../experiments/E025_participant-e016-biological-transfer.md) - participant-level biological-transfer analysis
- [`E026`](../../experiments/E026_tribe-textfeat-target-comparability.md) - target comparability audit
- [Cheng et al., 2026](cheng-2026_abstraction-induces-brain-alignment.md) - intrinsic dimension, semantic content, and brain-tuning geometry
