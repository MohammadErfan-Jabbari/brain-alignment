---
title: "Local Intrinsic Dimension of Representations Predicts Alignment and Generalization in AI Models and…"
tags: [literature]
aliases: [yu-2026_intrinsic-dimension-alignment-generalization]
---

# Local Intrinsic Dimension of Representations Predicts Alignment and Generalization in AI Models and Human Brain

**Authors:** Junjie Yu; Wenxiao Ma; Chen Wei; Jianyu Zhang; Haotian Deng; Zihan Deng; Quanying Liu (equal contribution: Yu and Ma)
**Year:** 2026
**Venue:** arXiv preprint (submitted 30 Jan 2026)
**DOI/arXiv:** arXiv:2601.22722
**Canonical ID:** yu-2026_intrinsic-dimension-alignment-generalization

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 20-page PDF read page-by-page including all appendices (A–G).
Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: It is established that better-generalizing vision models align better with each other and with the brain, but no prior work identifies a concrete geometric property that explains this joint relationship.
2. Core insight: LOCAL intrinsic dimensionality (LID, measured at small neighborhood scale K) is negatively correlated with AI–AI alignment (r = −0.838, p < 0.001), AI–Brain alignment in EBA (r = −0.843, p < 0.001), and ImageNet-1K generalization performance (r = −0.916, p < 0.001) across a large set of ConvNeXt models; GLOBAL dimensionality estimates (large K) do not predict any of these.
3. If-wrong breakage: If the LID–alignment link were driven by the specific PCA preprocessing step (top-300 PCs, which already compresses global dimensionality uniformly), or by embedding dimensionality confounds, the paper's claims collapse; the authors address this with a fixed local-neighborhood control (Fig. 4D) and show the same effect persists, but the PCA step is not fully unpacked as a potential LID compressor.

4. Main result location: Section 4.2 (Fig. 3, p.5) for the core LID–alignment–generalization correlations; Section 4.3 (Fig. 4, pp.5–6) for local-vs-global scale analysis; Section 4.4 (Fig. 5, pp.6–7) for cross-architecture robustness; Section 4.5 (Fig. 6, p.8) for scaling mechanism.

---

## Source Grounding

Dataset: Natural Scenes Dataset (NSD; Allen et al. 2022) — high-resolution fMRI from 8 participants viewing thousands of natural-scene images; each image repeated multiple times to estimate noise ceilings. AI models: primary analysis on 20+ ConvNeXt variants (nano to xlarge, pretrained on ImageNet-1K/12K/22K and LAION-2B/A, with and without fine-tuning); cross-architecture validation on 20 ResNet models, 8 ResMLP models, and 3 ViT (MAE-pretrained) models. Embeddings are extracted per model, PCA-projected to the top 300 principal components on a training split (80%), then used in voxelwise ridge regression (5-fold cross-validation) to predict fMRI responses; the held-out coefficient of determination $R^2$ is the alignment score. AI–AI alignment is computed analogously: ridge regression predicts one model's embeddings from another's, using held-out $R^2$, averaged across both directions; a reference-based variant uses the highest-performing model (convnext_large_mlp.clip_laion2b_soup_ft_in12k_in1k_384) to avoid trivial circular correlation. Generalization is ImageNet-1K top-1 accuracy. Intrinsic dimensionality is estimated using the Maximum-Likelihood Estimator (MLE) of Levina & Bickel (2004): for anchor point $z$, $\hat{m}_K(z) = \left[\frac{1}{K-1}\sum_{j=1}^{K-1}\log\frac{T_K(z)}{T_j(z)}\right]^{-1}$ where $T_j(z)$ is the Euclidean distance to the $j$-th nearest neighbor; this is averaged over all points to give the scale-$K$ estimate $\hat{m}(K)$. The scale parameter $K$ ranges from small (local) to large (global). Appendix G confirms results are robust to alternative estimators (MOM, MADA).

---

## Core Claims

- `C1`: Lower local intrinsic dimensionality (LID, small-K MLE estimate) is significantly negatively correlated with stronger AI–AI alignment: Pearson r = −0.838, p < 0.001 (Fig. 3B, ConvNeXt, K=50).
- `C2`: Lower LID is significantly negatively correlated with stronger AI–Brain alignment in EBA: Pearson r = −0.843, p < 0.001 (Fig. 3D, ConvNeXt, K=1000 for brain alignment; best scale selected per metric from scale analysis).
- `C3`: Lower LID is significantly negatively correlated with higher ImageNet-1K generalization: Pearson r = −0.916, p < 0.001 (Fig. 3C, ConvNeXt).
- `C4`: Global dimensionality estimates (large K, approaching full-sample scale) do NOT predict alignment or generalization; the predictive power is specific to local neighborhood geometry (Fig. 4A–E).
- `C5`: Increasing model capacity (parameter count) and training dataset scale both reduce local intrinsic dimensionality while improving alignment and generalization (Fig. 6A–B; log-parameter vs. dimension r = −0.756, p < 0.001; performance vs. log-parameter r = 0.949, p < 0.001).
- `C6`: These relationships generalize across heterogeneous architectures (ViT, ConvNeXt, ResNet, ResMLP), though cross-architecture AI–AI alignment is attenuated by architecture-family clustering (Fig. 5G); AI–Brain alignment and generalization correlations with LID remain significant across architectures (Fig. 5D–F).
- `C7`: The LID–alignment correlations are consistent across all 8 NSD subjects (Appendix E, Figs. 8–10; all per-subject Pearson r < −0.596, p < 0.001) and across visual hierarchy regions from V1 through EBA/FBA (Appendix F), with the AI–Brain–generalization link being stronger in higher-level visual areas.

---

## Evidence Pointers

- `C1` evidence: Figure 3B (p.5); text p.5 "lower intrinsic dimensionality exhibit substantially stronger within-group alignment."
- `C2` evidence: Figure 3D (p.5); text p.5 "all relationships are statistically significant."
- `C3` evidence: Figure 3C (p.5); text p.5 "lower intrinsic dimensionality is negatively correlated with … generalization performance."
- `C4` evidence: Figure 4C (p.6), bar plots of Pearson correlation vs. scale K; text p.6 "dimensionality estimated at small (local) scales is most strongly predictive, whereas correlations weaken as the neighborhood size increases."
- `C5` evidence: Figure 6A (p.8) parameter-count panel (r = −0.756, log scale); Figure 6B dataset-size panel showing significant drops from 1K to 22K pretraining.
- `C6` evidence: Figure 5A–F (pp.6–7); text p.7 "overall relationships remain statistically significant."
- `C7` evidence: Appendix E Figures 8–10 (pp.18–19); Appendix F Figures 11–12 (p.20).

---

## Assumptions and Limits

All analyses are conducted on vision models (convolutional and transformer) evaluated against visual cortex fMRI; no language models, no auditory cortex, no text stimuli are tested — the paper explicitly flags this as a limitation and calls for future work in language and auditory modalities. The PCA preprocessing step that projects all embeddings to 300 PCs before LID estimation may partially collapse global dimensionality uniformly, potentially confounding the local-vs-global comparison; this is not explicitly addressed. The "generalization" metric is exclusively ImageNet-1K top-1 accuracy — no downstream transfer tasks. AI–Brain alignment is measured only in the visual cortex (NSD; primarily EBA and higher visual regions). Causal direction is inferred but untested: it is not shown whether directly reducing LID (e.g., via a distillation objective) causes improved brain alignment and generalization, or whether this is a passive byproduct of scale. Intrinsic dimensionality is estimated on the static embedding set (static model representations), not on mid-training dynamics. The mechanism linking local geometry compression to flat loss-landscape minima (Section 5) is speculative and relies on third-party theory (Hochreiter & Schmidhuber, 1997).

---

## Interpretation Notes

This paper is the primary theoretical foundation for framing assumption **A2** (brain alignment is a meaningful proxy for generalization quality) and for **F3** (fMRI-free differentiable proxy via intrinsic dimension). The central result makes the following structural argument: LID is a single scalar that simultaneously predicts AI–AI alignment, AI–Brain alignment, and generalization, without using any brain data. This means LID is a candidate fMRI-free surrogate for the alignment signal — exactly what F3 needs. However, three careful caveats apply for our thesis:

First, the direction is NEGATIVE: LOWER LID predicts BETTER alignment and BETTER generalization. This is compatible with the intuition that well-trained models compress their representations onto simpler, lower-dimensional manifolds in local neighborhoods. This directly supports the R03 claim.

Second, the notion of "intrinsic dimension" here is strictly LOCAL (small-K MLE, the Levina-Bickel estimator applied to k-nearest-neighbor distances). GLOBAL dimensionality — which maps more naturally to the participation ratio (PR) used in some neuroscience papers — does NOT predict alignment or generalization in this paper. This is the critical reconciliation point with Cheng et al. 2602.04081 (see below).

Third, all results are in vision models on visual cortex fMRI. For language models and language cortex (our domain), this paper provides theoretical grounding but zero direct evidence. The authors acknowledge this gap explicitly.

For **A1** (alignment is an actionable training signal): the paper is silent — it is purely observational/correlational with no training intervention.

For **A3** (alignment-trained models generalize better downstream): the paper provides strong cross-sectional correlational support — models with higher brain alignment do generalize better on ImageNet — but this is across models differing in architecture and data, not within a matched-budget intervention.

The scaling result (C5) is directly relevant to our thesis design: if distillation reduces the student's effective model capacity relative to the teacher, we should expect LID to change, and that change should be predictive of whether brain alignment is preserved. This gives us a cheap, fMRI-free diagnostic: monitor student LID during distillation; if LID rises relative to the teacher at matched scale K, alignment is likely degrading.

**Reconciliation with Cheng et al. (arXiv 2602.04081):** Cheng et al. reportedly find that brain-tuning RAISES local intrinsic dimension and that HIGHER LID predicts brain-predictivity. This appears to contradict Yu et al. directly, but the contradiction likely dissolves on three grounds. (1) Cheng et al. compare within a fine-tuning intervention (before vs. after brain-tuning on a SINGLE model), whereas Yu et al. compare ACROSS models differing in scale and training data — the direction of the LID change within a fine-tuning trajectory may be opposite to the cross-model correlation direction if brain-tuning increases local distributional richness. (2) If Cheng et al. use a different notion of "local" — e.g., participation ratio of the covariance matrix (a global spectral measure), or LID computed in a different representation space (layer-wise vs. final embedding) — the operationalizations may be genuinely non-comparable. (3) Domain: Cheng et al. work on speech/language LMs and auditory/language cortex; Yu et al. work on vision models and visual cortex. The sign of the LID–alignment relationship may differ by modality. **Before citing both in the thesis, we must confirm Cheng et al.'s exact LID operationalization and whether their effect holds cross-model or only within-model.** This is a live open question that could require a clarifying experiment.

---

## Open Questions

Does the LID–alignment negative correlation hold within a matched distillation trajectory — i.e., as a student model is trained to mimic a teacher, does student LID track teacher LID, and does a LID-compression auxiliary loss accelerate convergence of brain alignment? This is the precise gap between Yu et al.'s passive observation and our proposed use of LID as an active distillation objective (F3). Answering this would either validate or invalidate the F3 framing in our thesis.

---

## Read Date

2026-06-10


## Related
- [`status.md`](../../status.md) — the canonical status board
