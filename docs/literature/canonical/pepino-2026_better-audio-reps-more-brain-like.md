---
title: "Better audio representations are more brain-like: linking model-brain alignment with performance in…"
tags: [literature]
aliases: [pepino-2026_better-audio-reps-more-brain-like]
---

# Better audio representations are more brain-like: linking model-brain alignment with performance in downstream auditory tasks

**Authors:** Leonardo Pepino; Pablo Riera; Juan Kamienkowski; Luciana Ferrer
**Year:** 2026 (arXiv submission date: 4 Mar 2026; arXiv v2)
**Venue:** arXiv preprint (cs.LG)
**DOI/arXiv:** arXiv:2511.16849
**Canonical ID:** pepino-2026_better-audio-reps-more-brain-like

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 20-page PDF read page-by-page including all methods, results, discussion, and figure captions.
Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: It is unknown whether audio models that perform better on downstream tasks also have more brain-like internal representations; this paper provides the first systematic cross-model correlation study in the auditory domain.
2. Core insight: Across 36 audio models, a model's overall downstream task performance (HEAREval z-score over 6 tasks) Pearson-correlates with its brain alignment score ($r = 0.90$ for NH2015, $r = 0.89$ for B2021 via voxel regression $R^2$; $r > 0.80$ via RSA) — strong, positive, and replicated on two independent fMRI datasets with different subjects. The study is purely observational/correlational: no model is trained to be more brain-like.
3. If-wrong breakage: The correlation is across a heterogeneous model population; if the model set were restricted to same-architecture variants of equal scale, the correlation could collapse. The observation that speech-only tasks (SC, ER) show little or no correlation with alignment when low-performing models are excluded (Table 1, RSA > −1 rows: $r = −0.016$ and $r = 0.038$ for SC and ER) already shows the relationship is task-contingent, not universal.
4. Main result location: Section 2.3 (Figure 6, Table 1, pp.12–13); Section 2.2 (Figure 5, pp.10–11 for the pretraining dynamics finding).

---

## Source Grounding

**Models.** 36 audio models spanning convolutional networks (CochDNN CNN9, CochResNet50 in 8 variants), recurrent models (DeepSpeech2, Sepformer, MetricGAN, DCASE2020), supervised classifiers (VGGish, AST), and recent self-supervised transformers: EnCodecMAE (10 variants, 43M–261M parameters), BEATs (4 checkpoints, 12-layer ViT, Audioset), and Dasheng (4 checkpoints including B/XL/XXL at 86M–1.2B parameters). Older models (trained pre-2022, typically supervised or domain-specific) are compared against the newer self-supervised ones. For each model the authors extract activations from every transformer/convolutional layer and select the layer that best predicts brain activity per analysis.

**fMRI datasets.** Two independent datasets: NH2015 (8 participants, non-musicians, age 19–25, 165 two-second everyday auditory stimuli, 3 scanning sessions each, ~962 voxels per participant selected by t-test $p < 0.001$ and consistency threshold $r > 0.3$, auditory cortex coverage in the superior temporal plane) and B2021 (20 participants, 10 with musical training, age 23–26, same 165 stimuli, 6 presentations, ~1340 voxels per participant). Both datasets capture BOLD responses to the same set of 165 short everyday sounds covering speech, music, and environmental sounds.

**Brain alignment metrics.** Two orthogonal methods used throughout: (1) voxel-wise ridge regression — for each voxel and subject an L2-regularized regressor is trained (nested 5-fold CV on 5 equal-size splits balanced by stimulus type) to predict the $N=165$ BOLD responses from model layer activations; the Pearson $R^2$ is computed per voxel, then median across voxels per subject, then mean across subjects, yielding a single scalar $R^2_m$ per model; (2) representational similarity analysis (RSA) — RDMs built from model activations and fMRI activity matrices are compared via Spearman correlation $\rho_{m,l,s}$, then averaged across subjects and maximised across layers, yielding $\rho_m$. Both metrics are applied to both datasets, giving 4 independent alignment scores per model.

**Downstream evaluation.** HEAREval benchmark protocol: 6 tasks spanning music (music note classification NS, music genre classification GC), speech (speech commands SC, speech emotion recognition ER), and environmental sounds (acoustic event detection FSD, environmental sound classification ESC). A multi-layer perceptron downstream model is trained using combined representations from all layers (unlike standard HEAREval which uses only the last layer, to match how brain alignment is computed). Performance per task is z-scored and averaged to a single overall score.

**Component analysis.** As a third alignment method, the paper factorises the average fMRI activity matrix into 6 components (accounting for ~80% of variance), identified as selective to LF tones, HF tones, Broadband, Pitch, Speech, and Music. Component-wise $R^2$ is correlated with per-task downstream performance, yielding Table 1.

---

## Core Claims

- `C1`: Overall downstream HEAREval performance and voxel-regression brain alignment $R^2$ are strongly positively correlated across 36 models: Pearson $r = 0.90$ (NH2015) and $r = 0.89$ (B2021), $p < 10^{-13}$. The same holds via RSA: $r = 0.82$ (NH2015) and $r = 0.84$ (B2021). Even when three outlier low-performing models (DCASE2020, MetricGAN, DeepSpeech) are excluded, the correlation remains $r = 0.71$ and $r = 0.70$ (voxel regression, both datasets).
- `C2`: Recent self-supervised models (EnCodecMAE, BEATs, Dasheng) outperform older supervised or domain-specific models on both brain alignment and downstream tasks; models pretrained on diverse audio (speech + music + environmental) outperform those trained on a single domain.
- `C3`: Pretraining of EnCodecMAE monotonically increases RSA brain similarity across 100k steps without any explicit brain objective; later transformer layers gain faster than early ones; the primary and posterior auditory ROIs differentiate from step ~20k onward, with posterior cortex correlating more with deeper layers.
- `C4`: The downstream–alignment correlation is task-contingent: it is strongest for acoustic event detection (FSD: $r = 0.866$–$0.895$) and music genre classification (GC: $r = 0.819$–$0.840$); it is weakest and sometimes non-significant for speech commands (SC) and emotion recognition (ER) when low-performing models are excluded.
- `C5`: Finetuning on a specific task (BEATs FT, Dasheng FT) does not significantly improve brain alignment relative to the non-finetuned checkpoint for these models, suggesting that the self-supervised pretext task itself drives alignment, not task-specific adaptation.

---

## Evidence Pointers

- `C1` evidence: Section 2.3, Figure 6 (p.13), Table 1 (p.14); correlation values stated explicitly in text p.12.
- `C2` evidence: Section 2.1, Figure 2 (pp.7–8); newer models (EnCodecMAE It2, BEATs It3) top both the regression and RSA rankings.
- `C3` evidence: Section 2.2, Figure 5A–C (p.11); RSA $\rho$ curves across 100k pretraining steps for each layer of EnCodecMAE on both datasets.
- `C4` evidence: Table 1 (p.14), "All" vs "$>−1$" rows for SC and ER; text p.12–13.
- `C5` evidence: Section 2.1, p.7; no significant difference between BEATs (FT) vs BEATs (It 3) or Dasheng (FT) vs Dasheng (B) in Figure 2.

---

## Assumptions and Limits

**Observational design.** The study is cross-model correlational. The correlation across 36 models does not imply that pushing a single model's alignment up will improve its downstream performance. The unit of analysis is the model population, not a training trajectory (except for the pretraining dynamics result in C3, which is correlational within a single model's history, not interventional).

**Heterogeneous model pool.** The 36 models differ simultaneously in architecture, training objective, pretraining data volume, data diversity, and scale. The correlation may be driven by the covariation of all these factors with capability, not by alignment per se.

**Stimulus set coverage.** 165 two-second everyday sounds are used as fMRI stimuli. The paper acknowledges this sample may favour models pretrained on diverse audio and may disadvantage speech-only models for reasons unrelated to their alignment capacity. The discussion notes that ECMAE (LL), trained only on clean speech, may appear underaligned because the stimuli include non-speech sounds it was never trained on.

**fMRI data scope.** Both datasets cover auditory cortex (superior temporal plane, temporal gyrus, temporal sulcus) only — no language network, prefrontal, or parietal ROIs. The generalization to the brain regions most relevant for text LMs (inferior frontal, angular gyrus, lateral temporal) is not established.

**Task selection.** 6 HEAREval tasks are not fully representative of auditory cognition. Authors note the correlation should increase with more tasks. The downstream model uses a fixed MLP architecture, and it has been shown (Ref 39) that downstream model choice affects representation rankings.

**No interventional test.** No model is trained with a brain alignment objective, so whether the correlation is exploitable as a training signal is not tested. The pretraining dynamics result (C3) is the only within-model observation; it is consistent with emergence but does not establish direction.

**Speech-related task weakness.** The weakest correlations are for the most linguistically demanding tasks (SC, ER) once bad models are excluded — exactly the regime our thesis cares about. This is a genuine caveat for the text domain.

**Temporal resolution.** fMRI BOLD signal has low temporal resolution (~2 seconds per TR). The paper acknowledges EEG/MEG would better capture fine-grained temporal encoding. The 165-stimulus sample size constrains statistical power in the component-wise analysis.

---

## Interpretation Notes

**Relation to A1/A2/A3.**

A3 (brain alignment and downstream utility co-vary) is the central claim of this paper. The evidence is correlational and strong within its scope: $r \approx 0.90$ across 36 models is not a weak association. The replication across two independent fMRI datasets with different participants strengthens confidence that the correlation is not a dataset artifact. This is the cleanest cross-model correlational support for A3 in the audio domain, and it echoes analogous findings for language models (the paper cites Schrimpf et al. and Goldstein et al.).

However, the thesis requires more than correlational support for A3. Our thesis asks whether optimizing a single student model for brain alignment — at a matched compression budget — produces better downstream utility than standard KD. A cross-model correlation cannot answer that question. The distinction is important and the paper does not obscure it: the authors explicitly call it a future direction (p.16, "one promising direction is to use fMRI-based RDMs to regularize model training"). The pretraining dynamics finding (C3) is the closest thing to a within-model directional signal, but it is still observational — brain similarity increases as a byproduct of the pretraining objective, not because it was optimized.

A1 (brain alignment is a usable training signal) is not tested here. A2 (confounds are controlled) is partially addressed — the two datasets have different subjects, different GLM preprocessing, and the consistent results across both reduce the risk of a single-dataset confound. However, the paper does not apply the Feghhi protocol (contiguous splits, autocorrelation controls); the 165-stimulus set is fully presented in randomised blocks repeated multiple times, which may mitigate some temporal autocorrelation concerns but is not the same as the contiguous-split discipline required by our guardrails.

**Practical implication for design.** The paper suggests that brain alignment could serve as a fast proxy for downstream performance during pretraining (p.14). For our thesis this is interesting in two directions: (a) it provides independent support that the alignment signal carries downstream-relevant information — strengthening the prior for F1 (that an alignment-guided student could outperform perplexity-only KD); and (b) the task-contingency result (C4) is a warning — the correlation is weakest for linguistically specific tasks, and our thesis targets text LMs evaluated on language benchmarks, not environmental sound classification.

**Relation to F1/F2.** F1 (alignment-guided distillation beats perplexity-only KD) has correlational backing from this paper but no interventional test. F2 (brain signal as a low-data regularizer) is not directly addressed; the paper is about the model population, not data efficiency. The pretraining dynamics result hints that brain-like structure emerges from diverse data, which is an indirect argument that targeted alignment training might accelerate this emergence — but this is speculative.

**Key caveat for the thesis.** A population-level correlation ($r \approx 0.90$ across 36 heterogeneous models) is consistent with A3 but does not license the inference that optimizing alignment within a single model family will improve that model's utility. The design space conflates capability, scale, data diversity, and alignment; pulling one lever (alignment) while holding the others fixed is the experiment that has not been done. Our thesis must run that experiment and must predeclare a minimum margin to claim a contribution.

---

## Open Questions

The paper's own discussion raises the most critical open question for our thesis: can the population-level correlation be cashed in as an interventional result — i.e., does training a model to be more brain-like (via fMRI-based RDM regularization or direct voxelwise loss) improve its downstream performance on language benchmarks, not just audio tasks? The audio domain is a cleaner setting because brain-alignment and downstream tasks share a stimulus space (sounds); in the text domain the stimulus mismatch (naturalistic fMRI stories vs NLP benchmarks) makes the translation non-trivial. That gap is exactly what our thesis occupies.

---

## Read Date

2026-06-10


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
