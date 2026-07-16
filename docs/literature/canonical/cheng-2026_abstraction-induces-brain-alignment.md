---
title: "Abstraction Induces the Brain Alignment of Language and Speech Models"
tags: [literature]
aliases: [cheng-2026_abstraction-induces-brain-alignment]
---

# Abstraction Induces the Brain Alignment of Language and Speech Models

**Authors:** Emily Cheng; Aditya R. Vaidya; Richard Antonello
**Year:** 2026
**Venue:** Preprint (arXiv, submitted February 2026)
**DOI/arXiv:** 10.48550/arXiv.2602.04081
**Canonical ID:** cheng-2026_abstraction-induces-brain-alignment
**Primary sources:** [arXiv abstract](https://arxiv.org/abs/2602.04081), [HTML paper](https://arxiv.org/html/2602.04081), [PDF](https://arxiv.org/pdf/2602.04081), [OpenReview forum](https://openreview.net/forum?id=n5Ds4qbtjM)

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 20-page PDF read page-by-page including all appendices (A–I).
Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: It is unexplained why intermediate, not output, layers of LLMs and speech models best predict brain responses; this paper identifies the local intrinsic dimension ($I_d$) of layer representations as the single strongest predictor of layerwise brain-encoding performance, stronger than next-token surprisal.
2. Core insight: Layers with a high $I_d$ (a local-neighborhood nonlinear manifold dimension estimated by GRIDE) coincide with the layers that (a) best predict fMRI/ECoG responses, (b) are most decodable for higher-order semantic rather than surface linguistic features, and (c) emerge as the best-predicting layers over the course of LLM pre-training — and directly brain-tuning a layer causally raises both its $I_d$ and its semantic content.
3. If-wrong breakage: The causal inference rests on a single speech model (WavLM-base-plus), a single finetuning target (layer 9 on fMRI from two subjects), and a single modality (speech); if $I_d$ gains in this fine-tuning experiment were confounded by head-count or architecture artifacts of WavLM rather than the fMRI signal itself, the causal claim collapses to correlation. The Random Fourier Feature control (Appendix, §4.4) also shows that high $I_d$ is necessary but not sufficient for brain predictivity.
4. Main result location: §4.1–4.3 (pp. 4–7), Table 1 (p. 4), Figures 2–5 (pp. 5–7), Appendices C–I.

---

## Source Grounding

**Neural data.** fMRI: LeBel et al. (2023) dataset, 2 subjects (UTS02, UTS03), ~20 h listening to English podcast stories per subject, ~90,000 cortical voxels per subject (8 mm of mid-cortical surface), ridge regression encoding models trained on 95 stories and tested on 3 stories (one test story repeated 10 times, two repeated 5 times; responses averaged). ECoG: Zada et al. (2025) open Podcast dataset, 9 subjects, 30 min, high-gamma 70–200 Hz band, 1,268 electrodes after QC. Encoding performance is Pearson $R$ on the validation set, with lag selection from 128 evenly-spaced −2 to +2 s lags.

**Language models.** Six mid-sized causal LMs: OPT-125m, OPT-1.3b, OPT-13b (12/24/40 layers); Pythia-160m, Pythia-410m, Pythia-6.9b (12/24/32 layers). All trained on large-scale text (The Pile). Representations extracted as the last-token residual stream for each layer; stimuli are N = 10,000 random 20-word contexts from The Pile.

**Speech models.** WavLM-base-plus (12 layers), WavLM-large (24 layers), Whisper-large encoder (36 layers). $I_d$ computed on N = 10,000 random audio chunks ≤20 s from LibriSpeech, averaged over 5 bootstraps.

**$I_d$ estimator.** GRIDE (Generalized Ratios Intrinsic Dimension Estimator; Denti et al. 2022). GRIDE operates on ratios $\mu_{i,2k,k} := r_{i,2k}/r_{i,k}$ (ratio of distance to the $2k$-th vs. $k$-th nearest neighbor). These ratios follow a generalized Pareto distribution with parameter $I_d$; $I_d$ is recovered by maximum likelihood. GRIDE is a methodological successor to TwoNN (Facco et al. 2017) that relaxes TwoNN's assumption of local uniformity up to the second nearest neighbor, allowing unbiased estimates up to the $2k$-th neighbor. A scale analysis over $k \in [2^0, 2^{12}]$ is run per model; the stable plateau value is chosen (e.g., $k = 2^4$ for Pythia-6.9b). Linear dimensionality (PCA-99 and Participation Ratio) was also computed as a check (Appendix C.2–C.3); it yielded high correlations to encoding performance but the absolute values were very low ($d \approx 1$–2) and failed to track semantic probing tasks, so the analysis focusses on nonlinear $I_d$.

**Surprisal.** Computed via TunedLens (Belrose et al. 2023) affine maps from each intermediate layer to the vocabulary; a speech-model equivalent was constructed with learned affine maps to LibriSpeech next-token predictions.

**Linguistic probing.** SentEval (Conneau et al. 2018) for LLMs (surface: Word Content, Sentence Length; higher-order/semantic: Bigram Shift, Odd Man Out, Coordination Inversion); acoustic/semantic probing for speech models (Vattikonda et al. 2025), using GloVe-300d as the semantic regression target.

**Brain-tuning intervention.** WavLM-base-plus layer 9 was directly fine-tuned on voxelwise fMRI responses (Vattikonda et al. 2025 protocol, extended context from 2 s to 4 s audio) for subjects UTS02 and UTS03 separately. The model is described in Appendix F; no other architectural changes. After fine-tuning, encoding performance, semantic probe $R^2$, and $I_d$ at all 12 layers are compared to the original checkpoint.

**Data, code, and compute.** The neural sources are public: [LeBel natural-language fMRI, OpenNeuro ds003020 v2.0.0](https://openneuro.org/datasets/ds003020/versions/2.0.0) and [Podcast ECoG, OpenNeuro ds005574](https://openneuro.org/datasets/ds005574). Appendix A says the paper-specific GitHub link will be added after deanonymization, but no paper-specific code or brain-tuned checkpoint is linked in the verified version. The paper reports approximately 1,000 CPU node-hours for ridge models, 300 GPU node-hours for feature extraction, and roughly 40 days of total parallelized runtime including preliminary and failed runs.

## Intervention controls

The random Fourier feature experiment is a useful geometry control for the frozen encoding analysis because it shows that high $I_d$ alone is insufficient for strong neural prediction. It is not a control for the brain-tuning intervention. The intervention compares the fMRI-tuned WavLM checkpoint only with its original pretrained checkpoint; it does not include shuffled fMRI, stimulus-derived supervision, a language-model target, or an auxiliary target matched on spectrum, effective rank, $I_d$, scale, head learnability, gradient magnitude, and update norm. No independent fine-tuning seeds are reported. UTS02 and UTS03 are separate biological targets, not optimizer-seed replications.

---

## Core Claims

- `C1`: Layerwise $I_d$ is strongly positively correlated with layerwise brain-encoding performance across all LLM and speech model families, both fMRI and ECoG. Global Spearman $\rho = 0.76$ (fMRI) and $\rho = 0.43$ (ECoG), both significant at $p < 0.01$ (permutation test). Within individual well-predicted voxels, $\rho(I_d, \text{EP}) = 0.73$ for fMRI (OPT-1.3b, UTS03) and $\rho = 0.63$ for ECoG. See Table 1 and Figure 2B.
- `C2`: Layerwise surprisal does NOT account for the best-predicting layer or for layerwise variation in encoding performance. Global $\rho(\text{surprisal}, \text{EP}) = -0.51$ (fMRI), $-0.21$ (ECoG); within individual models the sign is inconsistent (negative for OPT/Whisper, positive for WavLM). The $I_d$–EP correlation is significantly higher than the surprisal–EP correlation across all conditions (Table 1, both rows).
- `C3`: $I_d$ and encoding performance co-emerge over pre-training. In Pythia-6.9b trained over checkpoints from 1K to 143K steps, the $I_d$ peak at layer 13 (fMRI) / layer 12 (ECoG) stabilises as $I_d$ grows globally, and the peak layer for $I_d$ and the peak layer for encoding performance coincide at all checkpoints (Figures 2C–E, Appendix H.4). The global Spearman $\rho$ between fMRI encoding performance and $I_d$ is $\rho = 0.96$ across training steps (p < 1e-3).
- `C4` (causal): Directly fine-tuning WavLM-base-plus layer 9 on fMRI voxelwise responses causally increases both $I_d$ (right panel, Figure 5) and semantic probe $R^2$ (middle panel) at the finetuned layer and adjacent layers, without a corresponding increase from the unfinetuned checkpoint. This confirms that the $I_d$–brain-alignment link is not merely a byproduct of layer depth or architecture.
- `C5`: High $I_d$ is necessary but not sufficient for brain predictivity. Random Fourier Feature (RFF) spaces with increasing extrinsic dimension (128 to 2048) show $\rho = 1$ between RFF-$I_d$ and encoding performance, but encoding performance plateaus at $R \approx 0.04$ — far below LLM/speech model performance at the same $I_d$ (Figure 6). Thus rich meaning abstraction in a model trained on language is required; $I_d$ is a correlate, not the cause.

---

## Evidence Pointers

- `C1` evidence: Table 1 (p. 4), bottom rows "$I_d \uparrow$"; Figure 2A (p. 5) layerwise $I_d$ and EP profiles; Figure 2B global scatter; Figure 4 (p. 6) voxel/electrode distribution; Tables I.2–I.3 (pp. 19–20) full per-model, per-subject breakdown.
- `C2` evidence: Table 1 (p. 4), top rows "Surprisal $\downarrow$"; Figure 1 (p. 4) and Figure E.1 (p. 17) surprisal vs. EP trajectories.
- `C3` evidence: Figures 2C, 2D, 2E (p. 5); Appendix H.4 (p. 19).
- `C4` evidence: Figure 5 (p. 7); Appendix H.5 (p. 19) for second subject UTS02.
- `C5` evidence: Figure 6 (p. 8) RFF control scatter; §4.4 discussion (p. 8).

---

## Assumptions and Limits

Only two fMRI subjects (UTS02, UTS03 from LeBel et al. 2023) and 9 ECoG subjects are used; the correlation results have not been replicated across the wider population of brain-tuning subjects. All LLMs are causal mid-scale models (OPT and Pythia families, 125m–13b); instruction-tuned, RLHF-aligned, or encoder-only models are absent. The intervention (§4.3 / C4) is performed on a single speech model (WavLM-base-plus), a single layer (9), and two subjects; no text-LLM brain-tuning intervention is performed. Without a shuffled-neural or learning-matched auxiliary intervention, the experiment shows that this fMRI-tuning procedure moves $I_d$ and semantic content, but it does not establish that neural content rather than generic auxiliary optimization caused those changes. Model-training seeds and a participant-level intervention inference hierarchy are not reported. The paper does not show that maximizing $I_d$ as a training objective would yield alignment gains; it shows that the correlation holds and that an fMRI-tuning intervention moves $I_d$ in the expected direction. There is no distillation experiment or matched-budget comparison. Brain regions are analyzed globally (full cortical surface), not decomposed into language ROI vs. non-language ROI as done in Moussa et al. (2025); the auditory cortex is noted as an exception where speech models have high EP driven by low-level features but $I_d$ does not track it (§6, p. 6). Linear dimensionality (PCA-99, PR) also correlates with encoding performance (Table C.2: PCA-$d$ correlation 0.91–0.96 for OPT models) but the authors treat it as a supporting check rather than a primary measure, partly because absolute PR values are $\approx 1$–2.

---

## Interpretation Notes

**LID definition and sign.** $I_d$ is defined as the local nonlinear intrinsic dimension of the layer's representation manifold, estimated by GRIDE (a k-NN ratio method). HIGHER $I_d$ predicts HIGHER brain-encoding performance. The relationship is positive and monotone through the ascending (abstraction) half of the network, and encoding performance falls as $I_d$ falls in the later (prediction) layers.

**Relation to arXiv 2601.22722.** The sign question requires care. If 2601.22722 claims that LOWER intrinsic dimension aligns/generalizes better, the two papers are using a different notion of "dimension" or operating in a different context. Cheng et al. use LOCAL nonlinear $I_d$ (GRIDE, neighborhood scale), which captures how many independent directions the manifold spans locally — a high $I_d$ means the manifold is high-dimensional and fills representational space richly. Papers working with GLOBAL linear dimension (e.g., participation ratio, rank, or isotropic spread) sometimes find that more isotropic (lower rank collapse) or lower-rank representations generalize better, which would be directionally opposite. The two claims are not necessarily contradictory: local nonlinear $I_d$ can be high while global linear rank is low, or vice versa. The user should confirm what quantity 2601.22722 actually measures before concluding a contradiction; this note flags it as a potential false conflict from a dimension-of-dimension mismatch rather than a genuine empirical contradiction.

**Relevance to A1/A2/A3 and F3.**

- A1 (brain alignment is an actionable training signal): C4 confirms this causally for speech models. The paper is the strongest single piece of evidence that pushing alignment up also pushes $I_d$ and semantics up together — a mechanistic story for why A1 works, not just that it works.
- A2 (alignment is not pure nuisance): C2 rules out surprisal/next-token prediction as the driver; C5 rules out $I_d$ alone (requires learned linguistic structure). Together they argue the alignment signal carries something specific that static or random features do not.
- A3 (alignment gains translate to utility): Not directly tested here; the paper is agnostic about downstream task performance.
- F3 (fMRI-free differentiable abstraction proxy): This paper is the strongest theoretical motivation for F3. If $I_d$ is the proximate correlate of brain alignment, and $I_d$ can be computed from model activations alone (no fMRI needed), then a loss that maximizes $I_d$ at the student's best-performing layer is a candidate fMRI-free surrogate. However, C5 is a hard warning: RFF spaces with high $I_d$ do not brain-predict well; the $I_d$ must arise from learned linguistic structure, not imposed geometrically. A distillation loss that simply maximizes $I_d$ without preserving the semantic content that underlies it may fail. The correct F3 design implied by this paper is: maximize $I_d$ while aligning the student's representation to a linguistically rich teacher's layer — not maximize $I_d$ as a standalone geometric objective. This is a design guardrail.

**Exact Package A relevance.** The paper closes the broad novelty claim that representation geometry has not been connected to brain alignment or moved by a brain-tuning intervention. It does not close the intervention-specific gap because its fine-tuning comparison lacks neural-content controls, training seeds, participant-held-out intervention transfer, and a practical endpoint. For [E026](../../experiments/E026_tribe-textfeat-target-comparability.md), matching target dimension or linear rank alone is inadequate: the audit should compare covariance spectrum, effective rank, nonlinear $I_d$, scale, held-out head learnability, gradient norm, update norm, and resulting generic model quality. C5 also prevents the converse overclaim: matching or increasing $I_d$ alone cannot establish a brain-specific mechanism.

**Verdict on R03 claim:** "a layer's local intrinsic dimension predicts its brain-predictivity; brain-tuning causally raises intrinsic dimension and semantic content together."

CORRECT for the first half; OVERSTATED for the causal half. The correlation is robustly established across 6 LLMs + 3 speech models, 2 imaging modalities, and over training dynamics (C1, C3). The causal claim (C4) is supported by direct evidence (brain-tuned WavLM layer 9 raises $I_d$ and semantic probe) but rests on one model, one layer, and two subjects — the paper itself describes it as a partial causal test and the authors note a no-fMRI control is absent for the $I_d$-raising direction. "Causally raises" is acceptable shorthand if understood as: "brain-tuning, which is the only known intervention that directly targets brain responses, raises $I_d$ as a byproduct." The claim is not falsified; its scope is narrower than stated.

---

## Open Questions

If $I_d$ is the right surrogate, there is a precise distillation design question: does a student trained with an $I_d$-maximization regularizer (applied at the layer whose $I_d$ profile best matches the teacher's peak) achieve higher brain-alignment than a perplexity-only student at matched budget — and does this happen without any fMRI signal at training time? This is the exact F3 test that neither this paper nor any prior work has run.

---

## Read Date

2026-06-10


## Related
- [`status.md`](../../status.md) — the canonical status board
- [`01-research-landscape.md`](../../01-research-landscape.md) - authoritative literature frontier map
- [Vaidya et al., 2026](vaidya-2026_slow-fmri-fast-ecog-transfer.md) - independent fMRI-to-ECoG biological transfer
