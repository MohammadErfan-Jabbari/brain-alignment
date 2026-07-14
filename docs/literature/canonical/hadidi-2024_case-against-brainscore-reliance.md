---
title: "Spurious alignment between large language models and brains can emerge from non-robust methods and overlooked confounds"
tags: [literature]
aliases: [hadidi-2024_case-against-brainscore-reliance, hadidi-2026_spurious-alignment-confounds]
---

# Spurious alignment between large language models and brains can emerge from non-robust methods and overlooked confounds

**Authors:** Nima Hadidi*; Ebrahim Feghhi*; Bryan H. Song; Idan A. Blank; Jonathan C. Kao (* equal contribution)
**Year:** 2026
**Venue:** Nature Communications 17:5769
**DOI/arXiv:** 10.1038/s41467-026-72253-7; earlier preprint arXiv:2406.01538
**Canonical ID:** hadidi-2024_case-against-brainscore-reliance

## Read method

- [x] Full publisher PDF read (page-by-page comprehension)
- [x] Figures, methods, and statistical captions cross-checked
- [x] Earlier-note claims compared against the final version

The 17-page Nature Communications Version of Record was read in full on 2026-07-14. The retained source is `data/papers/hadidi-2026_spurious-alignment-confounds.pdf`, SHA-256 `7f75ccdd57b865c415030573ad79d107638d2617c4487b1666a4b12edbe9ebf7`.

> [!IMPORTANT]
> The published paper is materially revised relative to arXiv:2406.01538v2. The prior canonical digest incorrectly treated the versions as quantitatively interchangeable. The final changes the confound model, model suite, participant/data summaries, untrained seed count, analysis details, and several headline values. This note reports the published final; old preprint-specific numbers must not be cited as Nature Communications results.

Comprehension self-check passed: Y.

## Comprehension summary

1. **Problem:** Influential brain-score work reported that next-word-predictive language models, particularly causal transformers, best predict human language responses and that even untrained transformers are surprisingly brain-like. This paper asks whether those comparative conclusions survive robust splits, appropriate activation pooling and regularization, and simple confound controls.
2. **Core result:** On three reused neural datasets, shuffled splits, activation-extraction choices, and position or word-rate confounds materially change model and layer rankings. Under contiguous splits, the famous cross-model next-word-prediction relationship is not robust, and simple position/word-rate baselines share most of the variance attributed to trained LLMs and essentially all variance attributed to untrained GPT-2XL.
3. **Scope:** The paper does not show that all LLM-brain alignment is spurious. It audits three small datasets used by Schrimpf et al., explicitly notes that many studies avoid these problems, and acknowledges that position signals can be entangled with genuine linguistic structure.
4. **Role here:** It justifies strict split, pooling, regularization, and nuisance controls. It does not impose OASM or an untrained model as a universal requirement for every training experiment, and it does not answer whether a controlled neural training signal transfers.

## Data and inference scope

- **Pereira2018 fMRI:** two experiments with 384 and 243 sentence-level samples, reported over 10 unique participants in the combined analyses. The final language-network matrices contain 12,155 and 8,031 voxels, with 13,553 unique language voxels across experiments.
- **Fedorenko2016 ECoG:** five participants read 52 fixed eight-word sentences, yielding 416 word samples and 97 language-responsive electrodes in total.
- **Blank2014 fMRI:** five participants listened to eight Natural Stories, yielding 1,317 TRs and 60 language-network fROI summaries, 12 per participant.

Participant is the unit for model-level Wilcoxon comparisons, with $n=10$, $5$, and $5$. Within-participant added-value analyses compare samplewise squared errors at each voxel, electrode, or fROI and apply FDR correction. Because samplewise errors remain temporally dependent, the authors repeat the main GPT-2XL added-value analysis using passage, sentence, or 10-TR blocks.

## Models and encoding design

GPT-2XL is the primary model. The final paper replicates its confound result with RoBERTa-Large, Llama-3.2-3B-Instruct, and RWKV-4-3B-Pile, and uses a broader set of 45 models for model-class and next-word-prediction analyses. Untrained GPT-2XL is evaluated with five random initializations, not the ten reported in the earlier note.

Three ways to aggregate tokens within one neural sample are explicitly compared: last-token, mean, and sum pooling. OLS is used only to reproduce the earlier pipeline; main single-space fits use ridge regression and combined feature spaces use banded ridge. The ridge grid is $\{0\}\cup 2^{-5\ldots19}$ inside nested cross-validation.

Contiguous nested folds respect passage, sentence, or story blocks. Pereira uses category-balanced passage folds, Fedorenko holds out four sentences per fold, and Blank holds out one story. Shuffled comparisons preserve fold sizes but randomize block labels.

Best layer and PWR/OASM hyperparameters are selected on test performance to reproduce the inherited Schrimpf pipeline. The authors flag this as a limitation and report that validation-based selection gives similar qualitative conclusions.

## Confound models

**OASM.** The Orthogonal Autocorrelated Sequences Model starts from a block-diagonal identity over passage, sentence, or story samples and applies Gaussian smoothing within blocks, with 48 candidate widths from 0.1 to 4.8. OASM is exactly zero under contiguous block holdout because its blocks have no support in the test block. Under shuffled splits it can exploit within-block autocorrelation. The authors explicitly caution that OASM may capture position-correlated linguistic similarity as well as nonlinguistic temporal autocorrelation, so “linguistic-content free” is too strong.

**PWR.** The positional-signal and word-rate baseline is dataset specific. Pereira uses smoothed sentence-position indicators plus sentence word count; Fedorenko uses a position ramp and smoothed eight-position indicators; Blank uses story-start ramps plus words per TR. GloVe is added for Pereira. It does not improve the Fedorenko or Blank baseline and is omitted there.

**SYNTAX diagnostic.** A GPT-2XL-derived syntax representation is used only for a Pereira variance-sharing diagnostic. The published paper does not retain the earlier note's hierarchy of LMMS WORD, SENSE, and SYNT feature spaces.

## Core findings

### Shuffled splits can manufacture comparative conclusions

Under shuffled splits, OASM performs on par with or better than GPT-2XL, and no GPT-2XL pooling variant significantly exceeds it. Under contiguous splits OASM is structurally zero and GPT-2XL is significantly positive in all three datasets. The correct conclusion is that shuffled splits are non-robust, not that they uniformly increase every score.

Under shuffled splits, OASM overlaps with more than 80 percent of GPT-2XL-explained variance on Pereira, more than 50 percent on Fedorenko, and nearly 100 percent on Blank. Adding GPT-2XL beyond OASM is significant for roughly 20 percent of Pereira voxels, 30 percent of electrodes, and no Blank fROIs (Figures 1 and 2, pp. 2-5).

The across-layer pattern changes sharply between shuffled and contiguous splits. For GPT-2XL's 48 layers, the published shuffled-versus-contiguous correlations are $-.60$, $-.86$, and $-.85$ for Pereira last/mean/sum pooling; $.61$, $.57$, and $.52$ for Fedorenko; and $.46$, $-.65$, and $-.44$ for Blank. The older $-.929$ and $-.764$ values are preprint-specific and are not final-paper headlines.

### Activation extraction biases architecture rankings

With contiguous splits and each model's best pooling method, causal transformers do not consistently outperform bidirectional transformers or causal RNNs. On Pereira, last-token extraction produces significant causal-versus-bidirectional differences in 51.1 percent of comparisons, while mean, sum, or best-pooling choices produce fewer than 10 percent (Figure 3).

Cross-dataset model-ranking correlations largely disappear under contiguous splits once static embeddings are removed. This means a pooling decision can make an architecture family appear especially brain-like even when the broader comparison is unstable.

### Next-word prediction is not a robust cross-model explanation here

Under contiguous splits, correlations between next-word prediction and neural predictivity appear only when static embeddings are retained in the model set. Among contextual models, the relationship disappears for every dataset and pooling choice. Within architecture classes, only one causal-model comparison remains, Pereira with last-token pooling, and no bidirectional comparison survives (Figure 4).

This is scoped to these datasets and the inherited perplexity measurements. The paper notes that larger naturalistic datasets often find a positive relationship and does not claim a field-wide refutation.

### Simple baselines share most trained-LLM variance

PWR plus GloVe accounts for more than 85 percent of GPT-2XL out-of-sample $R^2$ on Pereira. PWR accounts for more than 80 percent on Fedorenko and nearly 100 percent on Blank. GPT-2XL adds significant variance beyond these baselines for only about 3.4 percent of Pereira voxels, 4.7 percent of electrodes, and no Blank fROIs (Figure 5).

The baseline-versus-GPT-2XL difference is significant only for Pereira last-token and sum pooling, with $p=.0020$ and $.0097$. The same broad sharing pattern is reported for RoBERTa, Llama, and RWKV in the supplementary analysis.

PWR also accounts for roughly 55 percent of GloVe variance on Pereira, while GloVe adds significant variance over PWR for 7.6 percent of voxels. PWR accounts for more than 80 percent of the SYNTAX representation's variance, and SYNTAX adds significant prediction in only a vanishing fraction of voxels. The authors infer that Pereira is poorly suited to disentangling these correlated properties, not that linguistic information is absent.

### Untrained predictivity is fully accounted for by simple controls

PWR accounts for more than 98 percent of untrained GPT-2XL variance in all three datasets. Adding untrained GPT-2XL produces no significant voxel, electrode, or fROI after correction (Figure 6). This directly undermines claims that neural predictivity of the untrained architecture alone demonstrates brain-like computation.

## What the paper recommends

The authors recommend contiguous block splits for autocorrelated language data, appropriate regularization, systematic comparison of token-pooling methods when a neural sample contains multiple tokens, simple position and word-rate controls, and rechecking model-property correlations first obtained under shuffled splits.

OASM, GloVe, and untrained controls are claim-dependent diagnostics, not a universal five-item checklist stated by the authors. This repository's stricter control battery is a derived design standard motivated by this paper and other evidence.

## Limitations

The final paper is restricted to three relatively small and sometimes atypical datasets inherited from Schrimpf et al. Large feature spaces may be disadvantaged by limited samples. Its percentage-overlap statistic is unstable when the denominator LLM $R^2$ is near zero, particularly on Blank. Layer and confound hyperparameters are selected on the test set to mirror the inherited pipeline. Analyses are restricted to language-localizer voxels, electrodes, or fROIs and depend on inherited preprocessing.

Most importantly, position and word rate can covary with genuine linguistic structure. The paper shows that the measured variance is not uniquely attributable to contextual LLM computations; it does not identify the causal cognitive content of the baseline itself.

## Relevance to this project

[E008](../../experiments/E008_per-participant-f1-solidification.md) already uses contiguous folds, fixed pooling and layers, fixed scalar plus static nuisances, permuted-brain matched-quality controls, and participant/fold inference. Hadidi et al. reinforce that design. They do not imply that E008 is missing a mandatory OASM analysis, because OASM is structurally zero under proper contiguous block holdout. E008's stated omission of surprisal and imageability remains the correct scope limitation.

[E016](../../experiments/E016_tribe-synthetic-brain-targets.md) uses contiguous real-brain scoring folds, train-fit PCA and scalers, fixed position/length/static nuisances, and controlled training targets. Hadidi et al. support interpreting its endpoint as unique only relative to those specified nuisances. They do not answer whether synthetic supervision transfers.

The paper cannot support “brain alignment is zero.” Its defensible lesson is that several famous comparative explanations are fragile and that simple baselines share most measured variance on these three datasets.

## Read date

2026-07-14

## Related

- [`01-research-landscape.md`](../../01-research-landscape.md) - literature frontier map
- [`E008`](../../experiments/E008_per-participant-f1-solidification.md) - participant and fold inference under controlled splits
- [`E016`](../../experiments/E016_tribe-synthetic-brain-targets.md) - proxy learnability and real-brain transfer
