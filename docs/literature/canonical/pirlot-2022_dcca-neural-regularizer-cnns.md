---
title: "Improving the Accuracy and Robustness of CNNs Using a Deep CCA Neural Data Regularizer"
tags: [literature]
aliases: [pirlot-2022_dcca-neural-regularizer-cnns]
---

# Improving the Accuracy and Robustness of CNNs Using a Deep CCA Neural Data Regularizer

**Authors:** Cassidy Pirlot; Richard C. Gerum; Cory Efird; Joel Zylberberg; Alona Fyshe
**Year:** 2022
**Venue:** arXiv preprint (cs.CV)
**DOI/arXiv:** arXiv:2209.02582
**Canonical ID:** pirlot-2022_dcca-neural-regularizer-cnns

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 12-page PDF read page-by-page including all figures and limitations section. No appendix pages were included in this preprint version.
Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Prior neural-data (ND) regularizers for CNNs used RSM matching or neural readout losses with serious limitations (fixed neuron subset, linear similarity only, no noise weighting); this paper replaces them with a Deep CCA (DCCA) branch that can handle nonlinear CNN-to-brain relationships and differentially weight noisy neurons, showing larger gains in accuracy and robustness on CIFAR-100.
2. Core insight: A joint loss $\mathcal{L} = \lambda \mathcal{L}_{\text{DCCA}} + (1-\lambda)\mathcal{L}_{\text{CE}}$ correlates CORnetZ's V1 activations with monkey V1 spike counts via learned nonlinear projections; the clean-accuracy gain (47.4% → 52.3%) is comparable to a shuffled-label control (within 0.4%), but adversarial robustness to moderate FGSM attacks is meaningfully higher only for the real, un-shuffled neural data.
3. If-wrong breakage: If the accuracy gain is fully explained by the shuffled-data control, the paper's claim that brain-specific structure drives accuracy improvement fails — and the authors themselves report exactly this for accuracy (the shuffle matches), while noting only adversarial robustness differentiates real from shuffled data.
4. Main result location: Section 4.1 (Figure 2, accuracy), Section 4.2 (Figure 2b, super-class), Section 4.3 (Figures 3–4, adversarial robustness), Section 5 (limitations).

---

## Source Grounding

Architecture: CORnetZ (Kubilius et al. 2018), the simplest brain-inspired CNN — four areas (V1, V2, V4, IT), each a single convolution + ReLU + max-pool, plus a 100-way linear classification head. The CNN-View for the DCCA branch is taken from CORnetZ's V1 layer (matching the brain-view source area). DCCA sub-models: each branch is 3 dense layers of width 1024 + 0.0001 dropout + a final dense layer of width 10; $C = 10$ canonical pairs. Training: learning rate 0.01, batch size 128, 0.5 dropout, 100 epochs, 5 randomly-seeded repetitions per $\lambda$; DCCA hyperparameters tuned separately (batch 50, ReLU, L2 weight decay 1e-5, Normal init std 0.01). Because the monkey stimuli (956 images) are far smaller than CIFAR-100 (60,000 images), for each CIFAR epoch the neural data is cycled 20 times.

Task dataset: CIFAR-100 (Krizhevsky 2009) — 100 classes, 60,000 images, 20 super-classes of 5 sub-classes each. Metrics: exact-class accuracy (correct class) and super-class accuracy (correct super-class) on the validation set.

Neural dataset: Coen-Cagli et al. (2015), publicly available from CRCNS. Utah arrays in primary visual cortex (V1) of 3 anaesthetized macaques; ~100 neurons per session, 10 sessions, 956 stimuli (270 natural images + static gratings), each image presented for 100 ms × 20 repeats. Preprocessed: spike counts averaged across repeats; top-80 PCs per session concatenated across sessions → final shape 956 × (80 × 10 = 800) pseudo-population.

Baselines: (1) Unregularized CORnetZ ($\lambda = 0$, 47.4% exact-class accuracy, 59% super-class accuracy); (2) RSM-based ND regularizer of Federer et al. 2020 (best r = 0.1, max exact-class ~49.5%, max super-class ~62% — read from Figure 2b); (3) Shuffled-label control: image-to-neural-response labels randomly permuted, preserving firing-rate distributions but destroying image-specific tuning.

Adversarial test: FGSM (Goodfellow et al. 2014) at attack strengths 0.00–1.75 (Figure 3) and extended range (Supplementary S2). No other attack types tested.

---

## Core Claims

- `C1`: DCCA-regularized CORnetZ at $\lambda = 0.5$ reaches 52.3% exact-class accuracy and 64.5% super-class accuracy on CIFAR-100 at 100 epochs, versus 47.4% / 59% for baseline and ~49.5% / ~62% for the best prior RSM regularizer.
- `C2`: The accuracy gain from DCCA is nearly fully reproduced by the shuffled-label control (shuffled best: ~52.1% at $\lambda = 0.75$, within 0.4% of real-data best); the accuracy benefit does not appear to require the brain's image-specific tuning, only its distributional statistics.
- `C3`: For adversarial robustness to moderate-strength FGSM attacks, real un-shuffled neural data produces a network meaningfully more robust than baseline, while the shuffled-data network is only marginally more robust than baseline (Figure 4b). Real neural structure (not merely statistics) drives the robustness gain.
- `C4`: ResNet-50 also benefits from the DCCA regularizer at small $\lambda$ (= 0.1), but larger $\lambda$ can be detrimental to already high-capacity models (Supplementary S1).

---

## Evidence Pointers

- `C1` evidence: Figure 2a (validation accuracy curves by $\lambda$), Figure 2b (exact-class and super-class accuracy at 100 epochs vs. $\lambda$); text p.8 "optimal $\lambda$ to be 0.5 at 100 epochs, with accuracy 52.3%" and "baseline ($\lambda = 0$, 47.4%)."
- `C2` evidence: Figure 4a (shuffled vs. un-shuffled accuracy comparison); text p.9 "accuracies are within 0.4% of each other"; text p.8 "shuffled dataset...produced an ND regularizer that was almost as effective in terms of accuracy."
- `C3` evidence: Figure 4b (robustness curves for baseline, real-data $\lambda=0.5$, shuffled $\lambda=0.75$); text p.10 "using the non-shuffled data in the ND regularizer produces a network that is more robust to adversarial attack."
- `C4` evidence: Supplementary Section S1 (referenced in text p.9); text p.9 "smaller $\lambda (= 0.1)$ values achieved higher accuracy...regularizer can be less beneficial or even detrimental."

---

## Assumptions and Limits

The neural data is from anaesthetized monkeys (not alert, motivated animals), which the authors flag as a limitation (Section 5); the ND regularizer may be more effective with awake, task-engaged subjects. Only ~100 neurons per session are recorded per Utah array, capturing a small retinotopic patch of V1 — not representative of full V1 activity. Only one CNN family is tested at scale (CORnetZ); ResNet-50 is explored in supplementary but not reported with the same rigor. The dataset is CIFAR-100 (32×32 images) only — no ImageNet-scale experiments. The paper does not run language models, text data, or any LM-adjacent architecture. No explicit test of whether the gain persists in a low-data (sample-scarce) task regime. Adversarial testing is limited to FGSM; no PGD, AutoAttack, or other adaptive attacks. The accuracy benefit of DCCA over a shuffled-labels control is not shown to be statistically significant — the 0.4% gap is within the reported noise.

---

## Interpretation Notes

This paper is the primary vision-domain proof-of-concept for framing F2 (brain as low-data regularizer) and for the R03 claim that brain-alignment training helps in practice. Several things about the result require careful framing for thesis use.

**What the paper actually shows, precisely.** The accuracy gain (+4.9 pp exact-class, +5.5 pp super-class over unregularized baseline) is real but is nearly entirely reproduced by the shuffled-data control. That means, on accuracy, the DCCA is acting as a generic regularizer — the brain's specific image tuning is not required. This is a partial failure of the "brain structure is the key ingredient" story. Only for adversarial robustness does real neural structure differentiate from shuffled structure (C3). That is one genuinely controlled result: real neural data drives adversarial robustness beyond what statistical structure alone provides.

**Relation to A1/A2/A3.** A1 (brain alignment is an actionable training signal): supported — the DCCA loss is differentiable and backpropagates through V1. A2 (alignment signal is not pure nuisance): partially supported but weakened — on accuracy, distributional statistics (shuffled data) mostly suffice; only robustness requires actual image-specific tuning. A3 (alignment gains translate to downstream utility): supported for accuracy and super-class accuracy, and for robustness; the gain is real but the attribution is muddied by the shuffled baseline.

**How strong is this as a precedent for F2?** Moderate-to-weak for the specific claim "real neural structure is the active ingredient." Strong for the general claim "neural-data regularizer improves CNN generalization metrics." The architecture and domain are entirely different from text LMs (vision CNNs vs. transformer LMs; image stimuli vs. language stimuli; monkey V1 vs. human language network). The CIFAR-100 / CORnetZ setting is also small-scale and brain-inspired in architecture, which may make the regularizer unusually effective here. The paper does not test the low-data regime explicitly, which is the strongest predicted benefit from R03's first-principles argument (§2 Step 6). The 270-image neural stimulus set is small but is fully cycled 20× per CIFAR epoch, so it is not a low-data test.

**Specific open question for us.** Does the accuracy gain from a neural-data regularizer also mostly collapse to a shuffled-data control in the text LM setting? If yes, the interesting question shifts from "does brain alignment help" to "which aspect of brain structure (if any) buys uniquely useful inductive bias beyond generic regularization."

---

## Open Questions

For text LMs, does real fMRI structure outperform distributional-statistics-only controls (shuffled fMRI), or does the same partial failure of attribution reproduce? This is the direct analogue of Figure 4a/4b for the language domain, and no existing paper has run it.

---

## Read Date

2026-06-10


## Related
- [`status.md`](../../status.md) — the canonical status board
