---
title: "Brain-tuning improves generalizability and efficiency of brain alignment in speech models"
tags: [literature]
aliases: [moussa-2025b_multi-participant-brain-tuning]
---

# Brain-tuning improves generalizability and efficiency of brain alignment in speech models

**Omer Moussa and Mariya Toneva / 2025 / arXiv preprint** · **Link:** [arXiv:2510.21520](https://arxiv.org/abs/2510.21520) · **Code:** [multi-brain-tuning](https://github.com/bridge-ai-neuro/multi-brain-tuning)

## TL;DR

Moussa and Toneva fine-tune pretrained speech models to predict fMRI responses from multiple participants while retaining each participant's response as a separate target. A single projection head is shared across participants, but each available stimulus-participant pair produces its own loss and parameter update; this performed better than averaging responses, averaging participant losses before an update, fitting separate participant heads, or the paper's shared-response-model alternative.

For [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md), this is the closest direct precedent for participant-preserving biological supervision. For [`E031`](../../experiments/E031_biological-target-information-recovery.md), it motivates the shared-head follow-on only after target recovery and gradient specificity pass; it does not replace E031 because it opens intervention and downstream outcomes without first isolating the information carried by the target.

## Key ideas

### Preserve participant targets while sharing the model update

The method uses Wav2Vec 2.0 and HuBERT speech encoders. The convolutional feature extractor is frozen, rank-8 LoRA adapters are trained in the transformer, and an average-pooling plus linear projection head maps model representations to a common FreeSurfer-aligned fMRI output space. The head is shared rather than participant-specific.

For a stimulus \(S\) with responses \(R^i\) from participants \(i\), the model predicts each response separately. The main objective is participant-specific squared error:

\[
\mathcal{L}_{L2}^{i}
=
\frac{1}{|B|}
\sum_{b \in B}
\left(R_b^i-\hat R_b^i\right)^2.
\]

Available participant responses for a stimulus are presented consecutively, and the model is updated for each stimulus-participant pair. Participants need not share the complete stimulus set. The model therefore pools evidence through shared parameters without replacing individual responses by a participant mean.

The exact effect of participant presentation order and unequal participant data volume on the learned update is `\gap`; the inspected paper reports the procedure and comparison methods but does not identify an order-invariant estimand.

### Loss form depends on data volume

The paper compares \(L_2\), spatial correlation loss, and cosine plus \(L_2\). Correlation loss performs best at small brain-tuning data sizes of at most six hours but saturates, whereas \(L_2\) improves more as training data increase and is used for the main experiments.

Rank-8 LoRA updates correspond to 0.625% of model parameters. Larger ranks and full-model tuning do not improve the reported scaling result. This is evidence for a bounded adaptation mechanism in these speech models, not a universal LoRA rank or loss rule.

## Evidence

### Data and evaluation

Multi-brain-tuning uses the naturalistic-speech Moth Radio Hour fMRI dataset. Three participants with the longest recordings supply brain-tuning data, five other Moth participants test transfer, and 16 participants from the Narratives dataset provide an external-dataset evaluation. Brain alignment is measured with voxelwise ridge encoding models and Pearson correlation normalized by a voxelwise noise ceiling, summarized over language regions and upper-middle model layers.

The paper reports:

- a five-fold decrease in the amount of new-participant fMRI encoding data needed to reach the pretrained model's maximum alignment;
- up to a 50% increase in normalized brain alignment over the pretrained reference;
- transfer to held-out participants and to the Narratives dataset; and
- improvement rather than degradation on the paper's downstream phoneme and sentence-type probes.

These are external-paper results. The five-fold figure refers to encoding-data efficiency relative to the pretrained model's peak, not to five-fold less brain-tuning data, and the 50% figure is reported on the paper's normalized alignment scale.

### Comparisons

- **Single-brain-tuned:** same procedure using one participant.
- **Loss average:** compute participant losses and average them before one update.
- **Response average:** average participant fMRI responses before computing the loss.
- **Separate heads:** use one projection head per participant.
- **SRM-tuned:** align responses through the paper's shared-response-model alternative before tuning.
- **LLM-tuned:** replace fMRI targets with Llama-2-7B representations.
- **Stimulus-tuned:** continue the speech model's self-supervised objective on the stimulus audio.

The participant-specific sequential update with one shared head performs best among the multi-participant combination strategies inspected. The stimulus- and LLM-tuned baselines reduce the explanation that any additional audio or semantic training is sufficient, but they are not matched to the fMRI target on covariance, baseline predictability, gradient magnitude, or optimization difficulty.

## Limitations

1. **No target-information gate.** The work does not first show that the fMRI target contains unique held-out biological information beyond matched stimulus and nuisance models.
2. **No content-destroyed biological twin.** The controls do not include an E031-style target with matched scale, covariance, autocorrelation, rank, and headroom but destroyed stimulus-response pairing.
3. **Intervention and evaluation share the model family.** The paper fine-tunes speech encoders and then evaluates their fMRI encoding performance; this is not a target-only recoverability test.
4. **Speech scope.** Only approximately 90-million-parameter Wav2Vec 2.0 and HuBERT models on English naturalistic speech are tested. Text LMs, distillation, compression, and matched-budget students are absent.
5. **Shared anatomical output coordinates.** FreeSurfer alignment and one shared head may retain less participant-specific functional geometry than separate subject maps. Better performance than the tested SRM variant does not rule out other functional-alignment models.
6. **Noise-ceiling normalization is an evaluation operation.** It does not make the training loss uncertainty-aware at the voxel or sample level.
7. **Participant count remains modest.** The participant-level uncertainty supporting population generalization is limited by the available Moth and Narratives samples.

## Relevance to this thesis

### Relevance to H002

The paper supports H002's distinction between participant pooling and participant averaging. Shared model parameters can accumulate evidence across people while every participant remains an observed view with its own loss. This matches H002's measurement model more closely than a participant-mean target.

It does not establish biological specificity. A shared head, additional data, and participant-specific gradients can improve regularization even when the target's uniquely biological content is weak. H002 therefore still requires untouched biological views, nuisance subtraction, matched text targets, and content-destroyed twins before interpreting the participant-preserving update as biological supervision.

### Relevance to E031

E031's `shared_linear` arm tests whether participant-specific maps recover information about untouched participants before any speech or language model is tuned. Moussa and Toneva supply the most direct later intervention design if that gate passes: one shared projection, separate participant targets, and no response averaging.

The paper also argues against making \(L_2\) a fixed default. If a later gradient record is licensed, correlation and \(L_2\) should be compared inside training folds at the available data scale, with aligned-target and matched-twin trunk gradients matched and inspected before student outcomes are opened. E031 itself does not select this loss.

## Verified

Canonical metadata, architecture, participant-preserving update, loss equations, data-volume ablation, LoRA ablation, comparison strategies, alignment evaluation, and reported outcomes were checked in the primary arXiv paper body. Details not established in the inspected primary text are marked as `\gap`. All reported values remain external-paper evidence and do not become thesis numbers.

## Related

- [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md) - repeat-stable, participant-preserving biological supervision
- [`E031`](../../experiments/E031_biological-target-information-recovery.md) - prospective target-information recovery gate
- [Moussa et al. 2025](moussa-2025_brain-tuning-speech-lms.md) - single-participant speech-model brain-tuning predecessor
- [Diedrichsen et al. 2020](diedrichsen-2020_whitened-unbiased-rdm-similarity.md) - repeat-crossvalidated representational target
- [`literature/AGENTS.md`](../AGENTS.md) - canonical literature-note contract
