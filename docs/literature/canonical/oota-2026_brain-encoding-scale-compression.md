---
title: "Linguistic properties and model scale in brain encoding: from small to compressed language models"
tags: [literature]
aliases: [oota-2026_brain-encoding-scale-compression]
---

# Linguistic properties and model scale in brain encoding: from small to compressed language models

**Authors:** Subba Reddy Oota; Vijay Rowtula; Satya Sai Srinath Namburi; Khushbu Pahwa; Anant Khandelwal; Manish Gupta; Tanmoy Chakraborty; Bapi S. Raju
**Year:** 2026
**Venue:** arXiv preprint, under review
**DOI/arXiv:** 10.48550/arXiv.2602.07547; arXiv:2602.07547v1
**Canonical ID:** oota-2026_brain-encoding-scale-compression

## Read method

- [x] Full PDF read (page-by-page comprehension)
- [x] Appendices A-O inspected
- [x] Tables and internal numerical consistency audited

The 40-page arXiv v1 PDF was read in full on 2026-07-14. It is retained at `data/papers/2602.07547.pdf`, SHA-256 `e32b85107a52e20e9ded010098d657d11f96dd4ee2bb85e014c8faec3e797779`.

Comprehension self-check passed: Y.

## Comprehension summary

1. **Problem:** How do model scale and post-training compression affect fMRI encoding scores and probe-accessible linguistic information?
2. **Direct result:** On nine participants and one fixed held-out Moth story, selected 3B checkpoints have ceiling-normalized encoding scores similar to selected larger checkpoints, while the smallest 1B to 1.5B checkpoints are usually lower. Several AWQ and SmoothQuant conditions remain near the corresponding FP16 score, GPTQ is often lower, and Qwen-1.5B drops sharply at 50 percent pruning.
3. **Required calibration:** These are selected-checkpoint, best-layer, no-equivalence results. Model training data and architecture are uncontrolled, layer selection is ambiguous, train and test sets are standardized separately, the endpoint lacks nuisance subtraction, and several tables conflict with prose. “Brain alignment saturates at 3B” is an interpretation, not a causal capacity threshold.
4. **Role here:** The paper shows that raw encoding scores need not collapse under every post-hoc compression method. It does not test brain-guided training, matched knowledge distillation, synthetic neural supervision, participant-specific transfer, or compression at matched language-model quality.

## Source grounding

**Dataset.** The main analysis uses the public Subset-Moth-Radio-Hour fMRI data from nine participants listening to 11 stories. Ten stories provide 3,737 training TRs and one fixed story provides 291 test TRs. Features are downsampled with a three-lobed Lanczos filter and concatenated across four FIR delays. A reading-condition replication uses the same nine participants and dataset family, not an independent population.

**Models.** The paper evaluates Qwen2.5, LLaMA, and DeepSeek families around 1B to 14B parameters. Exact checkpoint reporting is inconsistent: Table 1 omits 14B configurations later used in figures, LLaMA naming alternates among versions, and the smallest DeepSeek is called both 1B and 1.5B. Appendix N says the DeepSeek-R1-Distill family is distilled, although the main text characterizes the compared checkpoints as base models. These off-the-shelf family differences are not controlled scale interventions.

**Representations and encoding.** Each word is encoded with up to 20 preceding words. Hidden states from all layers are downsampled to fMRI TRs, delayed, and fit with bootstrap ridge regression. The ridge penalty from 10 to 1,000 is chosen using a randomly selected 10 percent of the training set. The paper says train and test features, and train and test fMRI, are z-scored separately, using held-out-distribution statistics.

**Endpoint.** Normalized alignment is voxelwise Pearson correlation divided by an estimated cross-subject prediction-accuracy ceiling, then averaged after restricting to voxels with ceiling at least .05. The ceiling estimator and its uncertainty are not fully specified, and normalized ratios can exceed one in ROI tables.

**Inference.** Chance is evaluated with 5,000 permutations of 10-TR blocks, followed by Wilcoxon tests on participant means. Model-size and quantization contrasts instead use paired t-tests across nine participants. A multiplicity procedure is not specified even where the prose says results survive correction.

**Layer selection.** The source is internally unclear. Figure captions sometimes describe averaging over layers, tables use each participant/model's maximum across layers, and Appendix K describes one model-specific layer chosen from mean language-ROI performance. No validation-only layer-selection protocol is clearly stated.

## Compression actually tested

- **AWQ, GPTQ, and SmoothQuant:** post-training quantization. The precise bit width, calibration data, and configuration are not consistently given across checkpoints. The method section mentions INT4 and INT8 generically; some appendix tables explicitly identify INT4.
- **Unstructured magnitude pruning:** 10, 25, and 50 percent sparsity without retraining. This is a preliminary Qwen2.5-3B and Qwen2.5-1.5B analysis, not a three-family pruning study.
- **Knowledge distillation:** no controlled KD experiment is run. DeepSeek-R1-Distill is an off-the-shelf model family, not a matched intervention, and the paper explicitly leaves structured pruning and knowledge distillation to future work.

No condition optimizes brain alignment during compression. The paper is shrink-then-measure, not shrink-with-neural-supervision.

## Core findings with calibrated scope

### Selected 3B checkpoints often match selected larger checkpoints

For Qwen best-layer participant means, the paper reports approximately $.850$ for 1.5B, $.923$ for 3B, roughly $.886$ to $.896$ for 7B depending on the table, and $.930$ for 14B. Table 2 reports no 3B-versus-14B difference, while both exceed 1.5B. LLaMA and DeepSeek appendix tables also place selected 3B checkpoints near selected 14B checkpoints and the smallest models lower.

This is a local empirical pattern, not an equivalence or noninferiority result. No equivalence margin is predeclared; absence of a significant difference with nine participants does not establish equality. The scale pattern is nonmonotonic, with 7B sometimes below 3B and 14B, and architecture, pretraining data, and checkpoint identity are not held fixed.

The Qwen text is internally contradictory: the main and appendix prose call 3B and 14B significantly better than 7B, while Table 2 reports the corresponding contrasts as nonsignificant. The source or code would need adjudication before citing that comparison.

### Quantization effects depend on family and size

For Qwen-3B, Table 5 reports normalized alignment of $.924\pm.033$ for FP16, $.933\pm.035$ for AWQ, $.910\pm.037$ for GPTQ, and $.930\pm.035$ for SmoothQuant. At Qwen-7B, AWQ and SmoothQuant exceed FP16 in the reported paired tests and GPTQ is lower. At Qwen-3B, none of the quantized variants differs significantly from FP16, although AWQ and SmoothQuant exceed GPTQ. At Qwen-1.5B, AWQ improves over FP16 while GPTQ and SmoothQuant do not differ reliably.

The LLaMA pattern is different. GPTQ is generally lower, but some large numerical AWQ or SmoothQuant differences from FP16 are nonsignificant with nine participants. The paper has no equivalence margin, so “preserved” should mean descriptively near baseline in the reported endpoint, not statistically proven equivalence.

Therefore, the earlier claim that quantization preserves alignment only above 3B or that every small-model quantization degrades alignment is false. The supported conclusion is method-, checkpoint-, family-, and size-specific.

### Pruning is preliminary and size dependent

For Qwen-3B, Table 5 reports $.910$, $.908$, and $.907$ at 10, 25, and 50 percent sparsity, compared with $.924$ for FP16. No pruning equivalence test is shown. For Qwen-1.5B, 10 and 25 percent remain near the original score, while 50 percent drops from approximately $.830$ to $.608$.

This supports a descriptive claim that aggressive pruning harms the smaller checkpoint while the measured Qwen-3B score is comparatively stable. It does not establish preservation across model families.

### Task-alignment dissociation is descriptive

FlashHolmes probes nearly 200 datasets grouped into morphology, syntax, semantics, discourse, and reasoning. Figure 5 and representative appendix tables show that probe changes and brain-score changes do not always move together. However, the paper reports no formal correlation, uncertainty, or statistical test for the claimed dissociation. The safe statement is that selected conditions exhibit different descriptive patterns across the two endpoint families.

### Decoding is exploratory and under-specified

The paper reports text-reconstruction metrics for 784 segments per model, including the best BERT-F1 for the 3B LLaMA condition. It does not give enough decoder architecture and training detail, participant-level inference, uncertainty, or shuffled/no-brain controls to support a strong semantic-decoding conclusion. The examples are qualitative and sometimes generic. Decoding should not carry the paper's role in this repository.

## Validity and reproducibility limits

- One fixed story is the final test set. The reading check reuses the same participants and dataset family.
- Train and test distributions are standardized separately.
- Best-layer selection is ambiguous and may use held-out performance.
- Raw normalized alignment is not residualized for word rate, acoustic features, position, static embeddings, surprisal, or an untrained-model baseline.
- Compression ratios, calibration data, bit widths, checkpoint IDs, seeds, and code are incompletely specified.
- No equivalence or noninferiority test supports “preservation” or “3B equals 14B.”
- Multiplicity handling is unclear, and some table values, p-values, and prose conclusions conflict.
- Ceiling-estimation uncertainty is not propagated into the normalized endpoint.
- Probe-alignment dissociation and decoding receive no load-bearing inference.

These limitations do not erase the descriptive patterns. They narrow the conclusion to this paper's raw encoding endpoint and reported checkpoints.

## Relevance to this project

The paper constrains any motivation claiming that compression generally destroys alignment. Several post-hoc AWQ and SmoothQuant checkpoints, and some pruning conditions, retain similar raw predictive scores. Compression effects should therefore be described as method and scale dependent.

It is not a direct competitor to [E008](../../experiments/E008_per-participant-f1-solidification.md). E008 studies a 1.5B-to-0.5B KD intervention below Oota et al.'s proposed local plateau and uses matched-quality, permuted-target, nuisance, participant, and fold controls. Oota et al. cannot predict whether E008's student should benefit from brain guidance.

It does not answer [E016](../../experiments/E016_tribe-synthetic-brain-targets.md). Oota et al. measure pretrained or post-hoc-compressed representations; E016 tests whether a synthetic target is learnable and whether that training transfers to a fixed real-brain diagnostic.

The narrow unresolved frontier remains controlled distillation or compression at fixed student budget and quality, with brain-derived supervision compared against permutation and a learnability-matched non-brain target, followed by transfer to genuine individual brain endpoints.

## Open questions

1. Do the 3B-versus-larger patterns survive validation-only layer selection, training-set-only standardization, and equivalence testing?
2. Do compression effects survive nuisance subtraction and an untrained-model control?
3. Which exact quantization configurations, calibration data, and checkpoint IDs generated each table?
4. Is the task-alignment dissociation significant after participant-level uncertainty and multiple testing are included?
5. Does controlled KD, rather than an off-the-shelf distilled checkpoint, preserve or alter unique brain-predictive information?
6. Can any compression result generalize to a new story and new participants?

## Read date

2026-07-14

## Related

- [`01-research-landscape.md`](../../01-research-landscape.md) - literature frontier map
- [`E008`](../../experiments/E008_per-participant-f1-solidification.md) - controlled brain-loss lever test
- [`E016`](../../experiments/E016_tribe-synthetic-brain-targets.md) - synthetic target and biological transfer gate
