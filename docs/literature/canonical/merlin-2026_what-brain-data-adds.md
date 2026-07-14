---
title: "What Brain Data Adds to Language Model Training"
tags: [literature]
aliases: [merlin-2026_what-brain-data-adds]
---

# What Brain Data Adds to Language Model Training

**Authors:** Gabriele Merlin; Omer Moussa; Mariya Toneva
**Year:** 2026
**Venue:** CoNLL 2026, pp. 178-212
**DOI/Anthology:** 10.18653/v1/2026.conll-main.12; ACL Anthology 2026.conll-main.12
**Canonical ID:** merlin-2026_what-brain-data-adds
**Code:** https://github.com/bridge-ai-neuro/lm-brain-tuning

## Read method

- [x] Full PDF read (page-by-page comprehension)
- [x] Appendix figures and captions inspected
- [x] Extracted text cross-checked

The full 35-page CoNLL proceedings PDF was read on 2026-07-14. The retained source is `data/papers/merlin-2026_what-brain-data-adds.pdf`, SHA-256 `f78aa727af4b861f13e2009a64f1b15782d78840d7b8bf95498a2be0c5af5611`.

Comprehension self-check passed: Y.

## Comprehension summary

1. **Problem:** Previous brain-tuning work did not cleanly compare fMRI supervision with additional exposure to the same stimulus text. This paper compares brain-prediction, stimulus language-modeling, and joint objectives on BERT and GPT-2, then measures fMRI encoding and linearly accessible linguistic information.
2. **Core result:** Under the paper's thresholded Holmes win-rate metric, Brain-Tuned models outperform Stimulus-Tuned models in all four architecture-dataset plots, while Jointly-Tuned models have the highest aggregate win rate and beat pretrained models in three of four combinations.
3. **Critical boundary:** Brain and Stimulus arms are matched on input text, LoRA rank, learning rate, and broad duration, but not on target dimensionality, covariance, loss geometry, predictability, information, checkpoint criterion, or optimization difficulty. The result shows an advantage for the implemented fMRI-prediction objective over the implemented LM objective, not proof that brain recordings contain unique statistical information unavailable in text.
4. **Role here:** This is important positive prior art for brain-targeted text-LM training. It narrows novelty but does not close the controlled, fixed-budget, participant-transfer, or compression question addressed by [E008](../../experiments/E008_per-participant-f1-solidification.md) and [E016](../../experiments/E016_tribe-synthetic-brain-targets.md).

## Source grounding

**Models.** The paper LoRA-tunes `bert-base-cased` and `gpt2-small`. There is no smaller student, compression ratio, or deployment-budget comparison.

**Datasets.** Harry Potter contains eight participants reading one chapter, 1,211 brain images per participant, and four runs. The Moth Radio Hour reading condition contains six participants and 4,028 fMRI images. Brain models are trained separately for each participant.

**Training arms.** Brain-Tuned models optimize a participant-specific fMRI prediction objective. Stimulus-Tuned models optimize ordinary language modeling on the same text. Jointly-Tuned models combine the two losses. Brain and Stimulus use LoRA rank 4 and learning rate $5\times10^{-5}$; Joint uses rank 8 and learning rate $5\times10^{-4}$ with $\omega_{lm}=0.1$ and $\omega_{ba}=10$.

**Splits.** Training examples span five TRs. Four consecutive segments enable participant-specific cross-validation. Brain alignment is evaluated with ridge mappings on held-out segments, so transfer is to held-out stimuli within the same participant, not to unseen participants.

**Downstream diagnostic.** FlashHolmes contains more than 200 frozen-representation probing datasets across syntax, semantics, morphology, discourse, and reasoning. Each probe is run with six seeds for classifier initialization and data order. Those are probe seeds, not independent brain-tuned model-training seeds.

## Reported results

### Holmes win rates

The main Figure 3 visually gives approximate aggregate win rates of $.27$ to $.28$ for Jointly-Tuned, $.18$ for Brain-Tuned, $.10$ for Stimulus-Tuned, and $.22$ to $.23$ for pretrained. Exact values are not tabulated. The caption reports Jointly-Tuned above Brain and Stimulus, and Brain above Stimulus, with Wilcoxon significance; Joint's strongest subfield advantages are syntax, morphology, and discourse.

The four model-dataset plots are heterogeneous:

| Dataset and model | Joint | Brain | Stimulus | Pretrained | Direct reading |
|---|---:|---:|---:|---:|---|
| Harry Potter, BERT | ~.30 | ~.30 | ~.12 | ~.40 | Joint does not beat pretrained |
| Harry Potter, GPT-2 | ~.145 | ~.075 | ~.05 | ~.09 | Joint beats pretrained; Brain beats Stimulus |
| Moth, BERT | ~.43 | ~.23 | ~.18 | ~.34 | Joint beats pretrained; Brain beats Stimulus |
| Moth, GPT-2 | ~.28 | ~.10 | ~.055 | ~.09 | Joint beats pretrained; Brain beats Stimulus |

These values are visual approximations from Figures 10, 15, 20, and 25 because the PDF supplies no exact numeric table. The aggregate subfield plot also appears to place Joint slightly below pretrained on reasoning, so “better in every subfield” is too strong.

### Brain-alignment changes

The appendix reports percentage changes relative to pretrained:

| Dataset and model | Brain | Stimulus | Joint | Source |
|---|---:|---:|---:|---|
| Harry Potter, BERT | +12.4% | -5.7% | -45.3% | Figure 9 |
| Harry Potter, GPT-2 | +4.8% | +5.1% | -7.2% | Figure 14 |
| Moth, BERT | +2.7% | -16.0% | +5.7% | Figure 19 |
| Moth, GPT-2 | +1.2% | -1.5% | +6.8% | Figure 24 |

Brain exceeds Stimulus on Holmes even for Harry Potter GPT-2, where its reported encoding change is slightly smaller. Encoding improvement and Holmes improvement are therefore not monotonically coupled in these four conditions.

## Statistical audit

For each Holmes dataset, six probe seeds feed two-sample t-tests. A model receives a binary win only when it significantly beats another at $p<.05$. Win rates then aggregate across tasks, folds, participants, models, and datasets. This procedure discards effect magnitude and makes win probability depend on probe variance.

The observational unit for the reported Wilcoxon tests is not specified. Figure 3 says its standard error spans four model-dataset combinations, but an ordinary exact two-sided Wilcoxon test on four pairs cannot yield $p<.05$, so a lower-level unit must have been used without being named. Initial per-task pairwise tests do not have a clearly described multiplicity correction.

No independent model-training seeds are reported. Stimulus and pretrained controls carry no participant-specific supervision, so treating repeated participant pairings as independent would risk pseudoreplication unless those control models were independently trained and the dependence handled. The paper does not explain this sufficiently.

Figure 4's caption refers to significance asterisks that are not visible in the supplied figure, and the comparator for “significant improvement” is ambiguous.

## Matchedness and controls

Brain and Stimulus arms are matched on the stimulus input, LoRA rank, learning rate, and broad training duration. They are not matched on target dimension, covariance, smoothness, entropy, loss geometry, gradient scale, predictability, sample complexity, checkpoint criterion, or information content.

Accordingly, Brain above Stimulus establishes that the fMRI-prediction objective yields more Holmes wins than the selected language-modeling objective under this protocol. It does not distinguish neural information from dense-target regularization, target geometry, nuisance structure, or an optimization shortcut.

Joint above pretrained is less isolated because Joint also changes objective count, LoRA rank, learning rate, compute, and additional exposure. There is no text-plus-matched-nonbrain auxiliary arm.

The paper also lacks a shuffled or permuted brain target, a target-geometry-matched non-brain target, a matched-perplexity or quality twin, and participant-held-out transfer.

## What the paper establishes and does not establish

**Established within the reported protocol:** Brain-Tuned models win more Holmes probe comparisons than Stimulus-Tuned models; Joint has the best aggregate Holmes win rate; positive patterns appear across two architectures and two fMRI datasets; brain and text objectives can be complementary under LoRA fine-tuning.

**Not established:** unique statistical information in fMRI beyond text; survival under target-geometry, permutation, quality, or compute matching; transfer to a new participant; generation, OOD, or deployment utility; compression value; a clean causal relationship between increased encoding alignment and increased linguistic competence.

## Relevance to this project

The broad novelty claim “brain-target training can outperform one stimulus-only LM objective on broad frozen probes” is now prior art. The stronger statement “brain data adds unique information unavailable from text” remains unresolved because information and optimization are not matched.

The paper does not close [E008](../../experiments/E008_per-participant-f1-solidification.md), which tests a fixed-budget brain-specific lever with matched quality and participant/fold inference. It strongly motivates [E016](../../experiments/E016_tribe-synthetic-brain-targets.md)'s separation of proxy learnability from real-brain transfer and the need for target-comparability diagnostics.

In the five-gate view, measurement is partial, manipulation passes, incremental brain specificity is suggestive but not isolated, biological transfer is within-participant only, downstream utility is frozen-probe utility, and compression is absent.

## Open questions

1. Does Brain above Stimulus survive a non-brain auxiliary target matched on dimension, rank, covariance, predictability, and gradient scale?
2. Does the result survive a permuted-brain target and matched perplexity or generation quality?
3. What is the correct inference unit for the thresholded win-rate comparison?
4. Do effects survive independent model-training seeds?
5. Does any benefit transfer to new participants, new stories, generation, OOD tasks, or smaller students?
6. Why are encoding and Holmes changes nonmonotonic across the four architecture-dataset conditions?

## Read date

2026-07-14

## Related

- [`01-research-landscape.md`](../../01-research-landscape.md) - literature frontier map
- [`E008`](../../experiments/E008_per-participant-f1-solidification.md) - controlled individual-participant lever test
- [`E016`](../../experiments/E016_tribe-synthetic-brain-targets.md) - synthetic-target and real-brain transfer gate
