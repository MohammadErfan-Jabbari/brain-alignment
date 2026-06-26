---
title: "Scaling laws for language encoding models in fMRI"
tags: [literature]
aliases: [antonello-2023_scaling-laws-fmri-encoding]
---

# Scaling laws for language encoding models in fMRI

**Authors:** Richard Antonello; Aditya Vaidya; Alexander G. Huth
**Year:** 2023
**Venue:** NeurIPS 2023
**DOI/arXiv:** arXiv:2305.11863
**PMC:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11258918/
**Canonical ID:** antonello-2023_scaling-laws-fmri-encoding

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [ ] Full PDF read (page-by-page comprehension)
- [x] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-13 — full-text PMC HTML version read in detail; PDF exceeded fetch size limit. All tables, figures, footnotes, methods, and discussion confirmed from the PMC full text. Comprehension self-check passed: Y

> **Parse note:** The raw PDF at arxiv.org/pdf/2305.11863 exceeded the 10 MB fetch limit. Content sourced from the PMC full-text HTML (PMC11258918), which is the publisher-deposited version of the NeurIPS 2023 paper and matches the final published record. Results cross-checked across three targeted PMC fetches. No guessing from abstract.

---

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper establishes whether the well-known empirical scaling laws for language model downstream performance (loss vs. parameters) also hold for brain-encoding performance, and whether audio LMs show the same pattern; it is the first systematic scaling-law study for neural encoding across model families up to 30B parameters.
2. Core insight: Brain-encoding performance (voxelwise Pearson r on held-out fMRI) scales approximately logarithmically with parameter count from 125M to 30B, with r = 0.91 for the OPT family; LLaMA models are stated to be "marginally better" (~5 % by correlation, in a footnote), attributed informally to their larger training corpus (1.4T vs. 180B tokens), with no perplexity or quality control performed.
3. If-wrong breakage: If the log-linear trend reflects nuisance confounds (temporal autocorrelation, ill-conditioned ridge at large widths, context-length artifacts) rather than genuine model-quality gains, the scaling claim collapses; the authors acknowledge the regression becomes ill-conditioned beyond ~30B parameters, and the confound infrastructure from Feghhi/Hadidi 2024 is entirely absent here.
4. Main result location: Figure 1a–b (OPT/text scaling), Figure 1d (Whisper scaling), Figure 2 (training-data scaling), and the footnote on LLaMA vs. OPT; Discussion section on noise ceiling and limitations.

---

## Source Grounding

**Dataset.** Custom fMRI dataset from the Huth lab (referenced as LeBel et al. and Tang et al., not a named benchmark used elsewhere). Three subjects listened to approximately 95 naturalistic English-language podcast stories (~20 hours total) from The Moth Radio Hour, Modern Love, and The Anthropocene Reviewed, yielding ~33,000 BOLD datapoints per voxel. Scanner: 3T Siemens Skyra at UT Austin, TR = 2.0 s, TE = 30.8 ms, 2.6 mm isotropic voxels. For testing, subjects listened to two stories repeated 5 times each and one story repeated 10 times.

**Preprocessing and split.** Motion correction, coregistration, and low-frequency drift removal (2nd-order Savitzky-Golay, 120 s window). Train/test split is at the story level: approximately 95 stories for training, 2–3 held-out stories for testing. This is contiguous at the story level (whole stories reserved for test), not shuffled within stories. The first 20 s of each training story and the first/last 20 s of test stories are trimmed; a further 80 s of leading test data is excluded to eliminate long-context artifacts, which can inflate performance by up to 20 % in early auditory cortex.

**Encoding model.** Ridge regression maps LM hidden states (contextual embeddings with dynamic context windows: max 512 tokens, reset at 256) to BOLD time series at 2, 4, 6, 8 s delays. For evaluation, the best-performing layer per model is selected and reported. For stacked regression combining text and audio models, cross-validation uses an 80/20 split (not described as contiguous).

**Models tested (text).** OPT family: 125M, 1.3B, 13B, 30B, 66B, 175B. LLaMA family: 33B, 66B (only two sizes tested for LLaMA). GPT-2 family tested in training-data scaling ablation (OPT-125M with varying training data volume). The paper does not test GPT-4, instruction-tuned variants, or models trained with RLHF.

**Models tested (audio).** HuBERT, WavLM, and Whisper families.

---

## Core Claims

- `C1`: Brain-encoding performance scales logarithmically with parameter count (OPT family, 125M–30B), with a Pearson r = 0.91 between log(parameter count) and mean voxelwise encoding correlation across three subjects. Each order-of-magnitude increase in parameters yields approximately 4.4 % improvement in average cortical correlation. Performance plateaus for models exceeding ~30B parameters.

- `C2`: LLaMA models achieve approximately 5 % higher encoding correlation than OPT models at matched parameter count (~33B–66B). This comparison appears only in a footnote, not as a main result. The paper attributes it informally to LLaMA's larger pretraining corpus (1.4T vs. 180B tokens) but performs no perplexity or quality control, and does not test whether the gap is statistically significant.

- `C3`: Training data volume also scales logarithmically with encoding performance. For OPT-125M trained on increasing numbers of naturalistic stories (the Huth lab dataset), each order-of-magnitude increase in training stories yields a 122 % improvement in encoding performance (r = 0.989 between log(stories) and encoding score).

- `C4`: Audio encoding models (Whisper family) show stronger scaling than text models: r = 0.991 between log(Whisper model size) and encoding performance, with a 32.2 % gain per order of magnitude, and no evidence of plateau at the sizes tested.

- `C5`: OPT and LLaMA show different layer-optimal profiles. OPT reaches peak encoding at layers roughly 3/4 through the network (e.g., layer 33 of OPT-30B). LLaMA reaches peak performance in relatively early layers with a slow decay thereafter.

- `C6`: The best text encoding models approach the noise ceiling in precuneus and higher auditory cortex; angular gyrus and parts of prefrontal cortex remain substantially below ceiling.

- `C7`: Stacked regression combining text and audio models shows complementary gains localized to auditory cortex and mouth motor cortex, with modest synergy elsewhere.

---

## Evidence Pointers

- `C1` evidence: Figure 1a (OPT encoding performance vs. parameter count, log scale, 3 subjects); main text: "For each order of magnitude increase in the number of parameters in the language, the encoding performance of the average subject increases by roughly 4.4%" and "logarithmic relationship (r = 0.91)."

- `C2` evidence: Footnote 1 only: "it should be noted that the best model from the LLaMA family is about 5% more performant as measured by correlation." Main text: "The LLaMA models are marginally better at encoding than the OPT models." No figure, no statistical test, no perplexity comparison reported.

- `C3` evidence: Figure 2 (OPT-125M, layer 9, training data scaling); stated r = 0.989, 122 % per order of magnitude.

- `C4` evidence: Figure 1d (Whisper encoding performance vs. model size); stated r = 0.991, 32.2 % per order of magnitude.

- `C5` evidence: Main results section on LLaMA vs. OPT layer profile: "OPT models have maximum performance with layers that are roughly 3/4 into the model. In contrast, the LLaMA models... have a different pattern, with peak performance in relatively early layers followed by slow decay."

- `C6` evidence: Figure 3 (noise ceiling comparison map); text: "precuneus and higher auditory cortex are close to optimal"; "angular gyrus... still have the potential for substantial modeling improvement."

- `C7` evidence: Stacked regression section; text: "highly localized to auditory cortex and mouth motor cortex."

---

## Assumptions and Limits

**Regression ill-conditioning at large scale.** The ridge regression becomes ill-conditioned when model hidden-state dimensionality exceeds the number of training datapoints (~33,000). This is explicitly acknowledged as the reason performance plateaus beyond ~30B, and means the claimed plateau is partly a measurement artifact of the encoding procedure, not necessarily a property of the models themselves.

**No confound controls (Feghhi/Hadidi-style).** The paper does not test for temporal autocorrelation inflation, does not use contiguous within-story splits for the ridge hyperparameter search, and does not subtract nuisance baselines (sentence length, word position, static embeddings). The story-level train/test split is contiguous, which is the minimum acceptable bar, but no decomposition into confound-explainable vs. contextual-only components is attempted.

**No perplexity or quality normalization.** The LLaMA vs. OPT comparison is never controlled for next-word prediction quality, bits-per-byte, or any language modeling metric. The attribution to training data volume is informal speculation. This is the decisive gap for any claim that architecture or training-data choice adds brain-alignment beyond what model quality (perplexity) already predicts.

**Small N.** Only 3 subjects. No statistical tests for inter-subject variability are reported for the scaling result. Generalizability is assumed.

**Long-context inflation.** The authors note that failing to exclude leading test data inflates performance by up to 20 % in early auditory cortex due to long-context artifacts in the LM representations. This is controlled in their final numbers, but the correction magnitude is large enough to matter for cross-study comparisons.

**LLaMA coverage.** LLaMA is tested at only 33B and 66B — two points, both at the large end of the OPT range. The claimed scaling law for LLaMA is not established from a full parameter sweep; it is an interpolation point on the OPT-fitted curve.

**Single domain.** All stimuli are English podcast narratives. Encoding performance for other stimulus types (reading, dialogue, instructions) is untested.

---

## Interpretation Notes

This paper is the primary empirical anchor for the claim that brain-encoding performance tracks model scale — the foundational scaling-law result that motivates asking whether distillation degrades brain alignment. Its limitations, however, are substantial and load-bearing for the thesis:

1. The r = 0.91 is a correlation across model sizes for the OPT family, measuring whether the log-linear trend holds — it is not an encoding score for a single model. Do not confuse it with the r = 0.991 for Whisper/audio, which is a different modality with a steeper, unplateau'd trend.

2. The LLaMA > OPT comparison (~5 % by correlation, footnote only, 33B–66B range, no statistical test, no perplexity control) is the direct empirical precursor to the thesis Q2 question. The paper does not answer Q2; it is the observation that Q2 seeks to explain. Antonello et al. speculate that data volume (1.4T vs. 180B training tokens) explains the gap but provide no evidence for this — no perplexity comparison, no controlled ablation. This leaves it entirely open whether the residual is from (a) better language modeling quality (lower perplexity), (b) richer training data semantics independent of perplexity, or (c) architectural differences.

3. The dataset is the Huth lab custom dataset, distinct from the Moth Radio Hour subset used by Oota 2026. Both draw from overlapping podcast sources but differ in preprocessing and subject pools. Cross-study comparisons of absolute r values are unreliable.

4. The encoding methodology (ridge, 4-delay FIR HRF, best-layer selection per model) is widely adopted as the field standard but was not yet subjected to the Feghhi/Hadidi confound audit when this paper was published. Subsequent analysis (Feghhi/Hadidi 2024) demonstrated that shuffled splits inflate brain scores substantially on other datasets; Antonello uses story-level contiguous splits (mitigating the worst case) but does not verify this with a formal autocorrelation test.

---

## Relevance to this thesis

**Grounding for E015.** The paper provides the cleanest published evidence for a log-linear brain-alignment vs. parameter count law (r = 0.91, OPT family, 125M–30B). This is the baseline scaling law that E015 re-tests across model families and within a distillation context. E015 should explicitly cite Figure 1a as the prior that motivates checking whether the law holds under distillation and whether family membership (OPT vs. LLaMA) adds a systematic offset.

**Q2 (architecture/data residual) — what Antonello does and does NOT establish.** The paper documents that LLaMA outperforms OPT by ~5 % correlation at matched size (~33B), which is the Q2 observation. It does NOT establish whether this is due to (a) lower perplexity from larger training data, (b) training-data quality/diversity independent of perplexity, or (c) architectural differences. No perplexity metric is reported anywhere; no model is placed on a common next-word-prediction scale; bits-per-byte normalization is entirely absent. The informal explanation ("larger training set... may explain") is uncontrolled speculation. The thesis Q2 is precisely the controlled version of this question: after regressing out perplexity (or bits-per-character), is there a residual family effect? Antonello is the anchor paper for Q2, but its evidence is observational, not causal.

**The r = 0.991 confusion.** The thesis roadmap cites "r = 0.991 within OPT" — this is incorrect per the paper. r = 0.991 is for Whisper (audio) models, not OPT language models (which get r = 0.91). This should be corrected wherever the thesis cites that number; the correct OPT value is r = 0.91.

**Confound exposure.** The study predates Feghhi/Hadidi 2024 and does not apply their confound battery. The story-level split provides some protection, but the ridge hyperparameter tuning split is not described as contiguous, and no autocorrelation baseline is subtracted. Any E015 design that replicates Antonello's pipeline must apply Feghhi-style controls before interpreting the family-residual (Q2) as signal.

**Relation to Oota 2026 (scale-compression).** Oota 2026 finds that brain alignment saturates at ~3B parameters across newer model families (Qwen2.5, LLaMA-3.2, DeepSeek-R1), which partially contradicts Antonello's claim that performance continues to grow to 30B. The discrepancy is likely a combination of: (a) Antonello's regression ill-conditioning beyond 30B conceals the plateau, while Oota's normalized alignment metric corrects for it; (b) different datasets (Huth lab vs. Moth Radio Hour subset); (c) different model generations (GPT-2 era OPT vs. 2025 LLaMA-3.2). E015 should treat the "plateau around 3B" (Oota) as more reliable given better methodology, while using Antonello's 125M–3B segment as the sub-saturation scaling regime that distillation operates in.

**Relation to Gao 2024 (scaling not instruction).** Gao 2024 finds that scaling improves alignment but instruction tuning does not. Antonello is consistent with the scaling half of this finding and is silent on instruction tuning. Together they suggest that raw scale (parameters × training data) is the dominant driver of brain alignment improvement, not post-training alignment.

---

## Open Questions

Does the LLaMA vs. OPT ~5 % gap persist after bits-per-character normalization (i.e., putting models on a common next-word-prediction scale)? This is Q2, and Antonello provides no answer.

Does the OPT scaling law hold for families trained post-2023 (LLaMA-3.2, Qwen2.5, Mistral), or does the Oota-2026 saturation at ~3B supersede it?

Is the layer-optimal shift (OPT peaks at 3/4 depth; LLaMA peaks early) a consequence of model size, architecture, or training data? Could the layer shift be exploited to reduce the feature-extraction cost for brain encoding?

---

## Read Date

2026-06-13


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
