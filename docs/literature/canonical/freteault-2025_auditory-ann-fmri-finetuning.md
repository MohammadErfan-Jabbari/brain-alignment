---
title: "Alignment of Auditory Artificial Networks with Massive Individual fMRI Brain Data Leads to…"
tags: [literature]
aliases: [freteault-2025_auditory-ann-fmri-finetuning]
---

# Alignment of Auditory Artificial Networks with Massive Individual fMRI Brain Data Leads to Generalisable Improvements in Brain Encoding and Downstream Tasks

**Authors:** Maëlle Freteault; Maximilien Le Clei; Loic Tetrel; Lune Bellec; Nicolas Farrugia
**Year:** 2025
**Venue:** Imaging Neuroscience (MIT Press)
**DOI/arXiv:** 10.1162/imag_a_00525
**Canonical ID:** freteault-2025_auditory-ann-fmri-finetuning

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [ ] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [x] Extracted text only

PDF verified: 2026-06-10 — MIT Press PDF endpoint returns HTTP 403 for unauthenticated WebFetch. The PMC submitted-version (PMC12319826) was fetched in full and cross-checked against the DOI metadata and Google Scholar abstract. The PMC version is labelled "submittedVersion" and may differ slightly from the published version in wording but is expected to match in substance. All numbers below are from the PMC text; any item that could not be confirmed is flagged [PMC-unconfirmed].

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Do brain-alignment fine-tuning gains from fMRI generalize across stimulus distributions and benefit downstream auditory tasks, and does the benefit scale with fMRI data volume per subject?
2. Core insight: Fine-tuning SoundNet (~2.5M parameters) with an MSE loss against individual fMRI responses (up to 28 h training data per subject from the Courtois NeuroMod Friends corpus) improves brain encoding on held-out Season 4 data and significantly improves 12 of 19 HEAR benchmark tasks, with the largest and most consistent gains on tasks whose training sets are smallest (minutes-scale).
3. If-wrong breakage: The key structural test is whether gains are genuinely due to the brain-alignment objective or to incidental extended fine-tuning on the SoundNet backbone. The authors do not include a matched fine-tuning control (e.g., fine-tuning Conv1-Conv4 on a non-brain auxiliary target); if that control had been run and also improved 12/19 HEAR tasks, the "brain-alignment" interpretation would be substantially weakened.

---

## Source Grounding

**fMRI dataset.** Courtois NeuroMod project — six healthy participants (ages 31-47, three women, three men, right-handed, advanced English) watched all four seasons of the US sitcom Friends while scanned at 3T (Siemens Prisma Fit, TR = 1.49 s, TE = 37 ms, 2 mm isotropic, 60 slices). Training fMRI: Seasons 1-3, ~21 h training / ~7 h validation per subject, plus a group condition using the other five subjects (~105 h / ~34 h). Test fMRI: Season 4, 9.24 h per subject. Preprocessing: fMRIprep v20.2.5, MNI152NLin2009cAsym normalization. Two spatial targets: (1) whole-brain — 210 ROI-level averaged parcels from the MIST atlas; (2) STG — 556 individual voxels in the middle superior temporal gyrus mask.

**Backbone model.** SoundNet (Aytar et al. 2016): fully convolutional 1D audio CNN, seven layers, originally trained on 2 million Flickr videos for audio-visual correspondence. Architecture: Conv1 (16 ch, k=64, s=2) through Conv7 (1,024 ch, k=4, s=2); total backbone ~2.5M parameters. No recurrent or attention components; outputs 2,048-dim features at Conv7.

**Encoding layer.** A learnable 1D cross-correlation operator maps Conv7 features (2,048 channels) to predicted fMRI signal per parcel/voxel i: $\hat{y}_i = \sum_{k=0}^{N-1} h_{i,k} \star x_k$, where $h_{i,k}$ is a learned kernel (temporal window), $x_k$ is the Conv7 feature sequence for channel k, and $\star$ is valid cross-correlation. Optimal temporal window: 70 TRs (105 s), determined by hyperparameter search over 20-130 s.

**Fine-tuning levels tested.** Seven configurations: Conv7-only through Conv1 (i.e., "Conv7 model" = only last SoundNet layer + encoding layer trained; "Conv4 model" = Conv4 through Conv7 plus encoding layer trained). Conv4 selected as the best performance-efficiency trade-off.

**Downstream evaluation.** HEAR (Holistic Evaluation of Audio Representations) benchmark (Turian et al. 2022): 19 audio classification and regression tasks spanning environmental sounds, music, speech, and bioacoustics. Evaluation is rank-based: brain-aligned models are ranked against 29 other models previously submitted to HEAR and against the pretrained SoundNet baseline.

---

## Core Claims

- `C1`: MSE fine-tuning of SoundNet's Conv1-Conv4 layers on individual fMRI responses improves held-out Season 4 brain encoding. Most subjects gain 0.01-0.04 r² in the best-predicted ROI (15-30% relative), with one outlier subject (sub-05) showing +167% relative gain in MTG posterior. At the voxel level (STG, with spatial smoothing), the median r² gain across all voxels is 7-26% depending on subject; without spatial smoothing, 10-115%.
- `C2`: Brain-aligned models (both individual and group) significantly outperform the pretrained SoundNet baseline on 12 of 19 HEAR tasks (Wilcoxon test, p < 0.05) and underperform on 2 tasks (DCASE 2016 and VoxLingua107 top 10). Average rank improvement across all 19 tasks: approximately 2 ranks out of 29+ models.
- `C3`: The gains are largest for tasks with the smallest training sets. Gunshot Triangulation (~2 min training data) and Beijing Opera (~900 s) show the strongest effects; at 2 minutes of downstream training data, brain-aligned models surpass up to 18 of the 29 comparison models. Large-data tasks (e.g., NSynth at 50 h, FSD50k at >80 h) show smaller or absent gains.
- `C4`: Individual-level models (trained on one subject's fMRI) and group-level models (trained on five other subjects' fMRI) perform comparably on HEAR overall. For STG-only targets, group models significantly outperform individual models (p < 0.05), with average rank gains of 2.4 vs. 1.7 respectively. Whole-brain and STG models do not differ significantly from each other.

---

## Evidence Pointers

- `C1` evidence: PMC Section 3.3 (ROI-level Fig. 6; voxel-level Fig. 7); sub-05 167% outlier explicitly noted in text.
- `C2` evidence: PMC Section 3.4, "Brain-aligned models performed significantly better than SoundNet (p < 0.05) in 12 tasks out of 19, and performed worst in 2 tasks (DCASE 2016 and VoxLingua107 top 10)."
- `C3` evidence: PMC Section 3.4, "brain aligning a pretrained CNN network led to more generalisable representations, but also identify possibly large gains for downstream tasks with limited dataset available"; specific examples: Gunshot Triangulation, Beijing Opera; no formal statistical test separating the low-data regime from the full-data regime is reported.
- `C4` evidence: PMC Section 3.4, "we did not find any significant difference between individual and group models, both showing an average gain of two ranks"; STG-specific group advantage is reported with p < 0.05.

---

## Assumptions and Limits

Only SoundNet is tested. No other audio architectures (e.g., AST, wav2vec2.0, HuBERT) are evaluated, so the generality of the approach across model families is unknown and explicitly flagged as a limitation by the authors.

No matched fine-tuning control exists. The design confounds "extended fine-tuning" with "brain-signal fine-tuning." There is no condition in which Conv1-Conv4 are unfrozen and trained on a non-brain target (e.g., auxiliary classification, shuffled fMRI) at matched compute. This is the most important missing control for causal attribution.

The low-data finding is observational, not experimentally isolated. The 12/19 result groups all task sizes together; whether low-data tasks drive the headline number is qualitatively argued but not quantified via a formal interaction test (low-data tasks × alignment condition). The claim that the effect is "especially under low data" is a pattern in the data, not a tested hypothesis with a separation statistic.

No language or text models are evaluated. The HEAR benchmark is audio-only; no text-to-speech, language-model-derived, or cross-modal models are included. The results speak entirely to the audio processing domain.

No compression experiment. Fine-tuning SoundNet on fMRI increases representational quality; nothing here addresses parameter efficiency, student-teacher distillation, or whether the brain-alignment objective can substitute for scale.

Training and test stimuli are within-distribution: all from the Friends TV show, same acoustic and semantic register across seasons. The authors themselves note "strong similarities between each season, resulting in within-distribution training and testing" — a substantial caveat for the generalizability of brain encoding improvements.

---

## Interpretation Notes

This paper instantiates A1 (brain alignment is an actionable training signal) in the audio domain: the MSE voxelwise loss is a concrete, differentiable objective that moves the model's representations. It does not instantiate A2 (alignment tracks semantic quality as opposed to low-level features), since no feature-removal or nuisance ablation is reported.

The most load-bearing fact for the thesis framing F2 (brain as low-data regularizer) is C3: the qualitative pattern that gains concentrate in tasks with minimal downstream training data. This is genuine evidence for F2's prior expectation — a weak regularizer matters most where the data signal is weak. However, the evidence is imprecise in three ways: (a) the "low-data" effect is not formally isolated with an interaction statistic; (b) there is no matched fine-tuning control, so the brain signal specifically may not be what causes the effect; (c) all tasks improve together in the 12/19 count, including some that are not clearly low-data. The R03 characterization "especially under low data" is directionally correct but overstated as a clean, isolated finding.

The paper does not test F1 (distillation at matched budget) at all. It is a fine-tuning study that freely updates 40% of SoundNet's layers; the question of whether the same objective could guide a compression process is entirely open.

The domain gap from this work (audio CNN, 2.5M params, HEAR) to our target (text LM, GPT-2/Qwen scale, NLP tasks) is substantial. Three specific differences: (i) audio CNNs process continuous waveforms frame-by-frame; text LMs process discrete token sequences with attention over context — the fMRI-alignment loss structure differs fundamentally; (ii) SoundNet was never a strong baseline, making relative gains easier; (iii) the HEAR low-data tasks involve audio classification, not language generation or comprehension. The F2 analogue for text LMs needs its own verification, and this paper provides motivation but not transfer.

**Verdict on the R03 claim:** "fMRI fine-tuning of a 2.5M-param audio CNN improves 12/19 HEAR tasks, especially under low data. Direct support for the sample-efficiency mechanism."

- "2.5M-param audio CNN" — CORRECT. SoundNet total backbone ~2.5M parameters.
- "improves 12/19 HEAR tasks" — CORRECT. Directly stated in the paper with p < 0.05 (Wilcoxon).
- "especially under low data" — OVERSTATED. Directionally present in the results (Gunshot Triangulation, Beijing Opera are the strong examples), but the paper does not report a formal interaction or separation statistic distinguishing low-data tasks from high-data tasks. It is a qualitative observation, not an isolated experimental finding.
- "Direct support for the sample-efficiency mechanism" — PARTIALLY CORRECT / OVERSTATED. The pattern supports F2's intuition, but the missing matched fine-tuning control means the causal attribution to the brain signal specifically — rather than to the fine-tuning regime in general — is not established. The paper would be stronger support for F2 if an unfrozen-backbone + non-brain-target control were included and failed to replicate the low-data gains.

Overall R03 verdict: **OVERSTATED** (not WRONG). The numbers are real. The causal isolation and the "especially" qualifier are not supported as cleanly as R03 implies.

---

## Open Questions

The single most actionable open question for this thesis: does the low-data HEAR gain survive a matched control in which Conv1-Conv4 are fine-tuned on a non-brain auxiliary signal at identical compute? If yes, the brain signal itself is what matters; if no, extended fine-tuning is the mechanism and the brain alignment story collapses for F2. Designing that ablation — and running its text-LM analogue — is the exact empirical test that would promote F2 from a plausible-but-not-isolated pattern to an established mechanism.

---

## Read Date

2026-06-10


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
