---
title: "When Language Models Lose Their Mind: The Consequences of Brain Misalignment"
tags: [literature]
aliases: [merlin-2026_when-lms-lose-their-mind]
---

# When Language Models Lose Their Mind: The Consequences of Brain Misalignment

**Authors:** Gabriele Merlin; Mariya Toneva
**Year:** 2026
**Venue:** ICLR 2026
**DOI/arXiv:** arXiv:2603.23091
**Canonical ID:** merlin-2026_when-lms-lose-their-mind

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 33-page PDF read in four passes (pages 1–10 main paper; 11–20 references + Appendices A–D; 21–33 Appendices E–I with all per-model, per-dataset figures). Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: The causal role of LLM↔brain alignment for downstream linguistic competence was unknown. Brain-aligned models might just correlate with good models, without alignment being necessary. This paper tests the necessity claim directly by constructing an adversarial model that is brain-misaligned but perplexity-matched to a control.
2. Core insight: A gradient reversal layer added to a pretrained LM during LoRA fine-tuning can actively suppress brain-predictive information from model representations while keeping language modeling loss statistically indistinguishable from a control trained the same way with permuted fMRI images (the Brain Preserving model). Comparing Brain Misaligned vs Brain Preserving across 200+ classifier-probed linguistic tasks isolates the causal effect of alignment. The Brain Misaligned model loses substantially and consistently across semantics and syntax tasks.
3. If-wrong breakage: If the gradient reversal procedure inadvertently destroys representations beyond brain-relevant content (i.e., it is not a clean ablation of alignment, but also damages unrelated structure), the downstream harm could be over-attributed to alignment loss. The Brain Preserving control with permuted fMRI is designed to rule this out, but any residual asymmetry in what the adversarial loss actually removes (beyond brain-predictive dimensions) is the key threat to causal interpretation.

---

## Source Grounding

Three pretrained model families are used: bert-base-cased (BERT), gpt-small (GPT-2), and meta-llama/Llama-3.2-1B. All are fine-tuned with LoRA for 5 epochs, batch size 16, AdamW, on sequences of 5 TRs from two fMRI datasets. Dataset 1: Wehbe et al. 2014 Harry Potter Chapter 9, 8 participants, word-by-word reading, 1211 fMRI images per participant (TR = 2 s). Dataset 2: Deniz et al. 2019 Moth Radio Hour reading modality, 6 participants, 4028 fMRI images per participant. Voxels with estimated noise ceiling > 0.05 in language ROIs (Fedorenko et al. 2010; Fedorenko & Thompson-Schill 2014; Binder et al. 2009) are used as training targets. Brain alignment is measured as Pearson correlation between a linear ridge-regression head's predictions and held-out voxel values, evaluated via 4-fold cross-validation on held-out runs.

The combined loss during Brain Misaligned training is $\mathcal{L} = \omega_{lm} \cdot \mathcal{L}_{lm} + \omega_{ba} \cdot \mathcal{L}_{ba}$, where $\mathcal{L}_{lm}$ is standard cross-entropy (masked for BERT, causal for GPT-2/Llama), $\mathcal{L}_{ba}$ is the mean negative squared Pearson correlation between predicted voxels and ground-truth fMRI (minimising this maximises misalignment via gradient reversal), $\omega_{lm} = 0.1$ (fixed, calibrated against pre-training loss magnitude), and $\omega_{ba} = 10$. A gradient reversal layer sits between the model body and the brain mapping head; gradients from $\mathcal{L}_{ba}$ are negated before entering the model. The Brain Preserving model uses the identical setup but with permuted fMRI images, so the adversarial pressure points at noise rather than genuine brain signal. The Brain Tuned model removes the gradient reversal and directly minimises $\mathcal{L}_{ba}$, i.e., actively improves alignment while also optimising $\mathcal{L}_{lm}$.

Linguistic competence is evaluated using the Holmes benchmark (Waldis et al. 2024, flash-holmes variant), a classifier-probing suite of more than 200 datasets spanning 5 linguistic subfields: syntax, semantics, discourse, reasoning, morphology, and 60+ specific phenomena (argument structure, binding, filler gap, island effects, negative polarity item licensing, quantifiers, rhetorical structure theory, etc.; see Appendix A Table 3 for the full list). Each task uses 6 probe seeds. Performance comparison is via a binary "win matrix": a model "wins" a dataset only when it statistically significantly outperforms the other (two-sample t-test across seeds). Win rates are then aggregated across tasks and participants, and overall significance is assessed with the Wilcoxon signed-rank test.

---

## Core Claims

- `C1`: Brain Misaligned models, trained to be brain-unresponsive at matched language modeling performance, substantially underperform Brain Preserving controls across the full 200+ task Holmes benchmark (Brain Preserving win rate significantly higher, Wilcoxon p < 0.05 in most model-dataset combinations; p < 0.001 for BERT-Harry Potter, the best-controlled setting).
- `C2`: The competence drop is especially pronounced in semantics and syntax subfields; for BERT-Harry Potter, all five linguistic subfields show significant differences after Holm-Bonferroni correction (p < 0.05).
- `C3`: The complementary direction also holds: the Brain Tuned model (alignment increased via direct $\mathcal{L}_{ba}$ minimisation) significantly outperforms the Brain Preserving control in every experimental setting (Wilcoxon p < 0.05), with the largest gains in semantics and syntax (p < 0.05, Holm-Bonferroni corrected). Specific phenomena reaching significance include filler gap and negative polarity item licensing.
- `C4`: GPT-2 is the weakest condition: Harry Potter comparison reaches p = 0.055 (trend, not significant); Moth Radio Hour reaches p < 0.01. The authors attribute this to weaker gradient reversal effect for GPT-2, not noise.

---

## Evidence Pointers

- `C1` evidence: Figure 3A (all models, averaged) — Brain Preserving average win rate ~0.22 vs Brain Misaligned ~0.11. Figure 12A (BERT-Harry Potter) — Brain Preserving ~0.57 vs Brain Misaligned ~0.02 (p < 0.001). Figure 21A (BERT-Moth) — Brain Preserving ~0.30 vs Brain Misaligned ~0.23 (p < 0.01). Figure 30A (GPT2-Harry Potter) — Brain Preserving ~0.09 vs Brain Misaligned ~0.08 (p = 0.055, not significant at conventional threshold).
- `C2` evidence: Figure 12B — BERT-Harry Potter subfield win rates: all five subfields (discourse, morphology, reasoning, semantics, syntax) show Brain Preserving higher, all reaching p < 0.05 (Holm-Bonferroni). Figure 3B (all models averaged) — syntax and semantics show the largest gap; discourse, morphology, reasoning gaps are smaller and not significant after correction.
- `C3` evidence: Figure 5A (all models, Brain Tuned vs Brain Preserving) — Brain Tuned average win rate ~0.38 vs Brain Preserving ~0.08 (p < 0.05). Figure 14A (BERT-Harry Potter) — Brain Tuned ~0.68 vs Brain Preserving ~0.04 (p < 0.001). Figure 23A (BERT-Moth) — Brain Tuned ~0.60 vs Brain Preserving ~0.15 (p < 0.001). Brain Tuned vs original Pretrained model (Figures 16, 25) shows more modest advantages; the Pretrained model retains stronger discourse performance in some conditions.
- `C4` evidence: Figures 30–35 for GPT-2; p = 0.055 for Harry Potter (no significant difference after conventional threshold). Brain alignment effect on GPT-2 was also weaker in brain alignment difference maps (Figure 27 vs Figure 9).

---

## Assumptions and Limits

The adversarial fine-tuning removes brain-predictive information, but it is not proven to remove *only* brain-predictive information. The gradient reversal targets all variance that is linearly predictable from the brain mapping head; if that head captures structure shared with non-brain-relevant linguistic representations, those are also damaged. The Brain Preserving permuted-fMRI control is the main safeguard, but it cannot fully deconfound what the model learns from the fMRI spatial structure regardless of content. The two fMRI datasets (Harry Potter, Moth Radio Hour) are both English naturalistic reading; the causal claim does not extend to other languages, tasks, or stimulus types. Only three model families are tested, all pretrained; models trained from scratch with or without alignment are not studied. The Brain Tuned model vs Pretrained comparison (Figures 16, 25) shows the Pretrained model is still competitive in several conditions, meaning alignment-UP gains are more modest when starting from a strong pretrained base. No test of whether the causal relationship is monotone (is more alignment always better, or is there a saturation point?). No size ablation within families; only bert-base (~110M), gpt-small (~117M), and Llama-3.2-1B are used. Speech and multimodal settings are not tested. No compression or distillation setting; all models are fine-tuned at full parameter count (LoRA only modifies a small fraction).

---

## Interpretation Notes

This paper is the strongest causal evidence in the field that brain alignment is load-bearing, not merely correlated with competence. It establishes the bidirectionality: destroying alignment hurts (C1/C2), and increasing it helps (C3), both with statistical significance in the best-controlled settings (BERT on Harry Potter, all Llama conditions). The win-rate framing is conservative: it counts only statistically significant per-task wins, so the aggregate effect size is likely larger than the win-rate gap suggests.

For the thesis's framing, this maps as follows. F1 (brain alignment measures something real and useful): this paper upgrades F1 from correlational to causal — alignment predicts utility because it is necessary for utility, at least for semantic and syntactic tasks. F2 (alignment is a training signal we can use): the Brain Tuned result directly instantiates F2 for full-parameter fine-tuning (LoRA). F3 (preserving alignment under compression should buy something): this paper provides the strongest available motivation for F3, but it does *not* test compression. The causal chain it establishes is: alignment → linguistic competence. It does not establish: preserving alignment under distillation → preserving competence under distillation. That extension requires our own experiment.

Relation to assumptions. A1 (brain alignment is an actionable training signal): confirmed by C3 for fine-tuning. A2 (preserving alignment under compression retains downstream utility): not tested — this paper is motivation, not evidence. A3 (the alignment–utility relationship is causal, not merely correlational): directly supported by C1/C2 and C3 — this paper is the primary anchor for A3. The effect is not uniform: GPT-2 results are weaker and the discourse/morphology/reasoning subfields are less consistently significant than semantics/syntax.

One design implication: the Brain Preserving vs Brain Misaligned design is also a template for our ablation. When we train a brain-alignment-guided student and compare it to a perplexity-only student, the Merlin-2026 adversarial design tells us we need a third arm — a "perplexity-only but otherwise equally fine-tuned" control — not just the two students. Otherwise we cannot separate alignment loss from the effects of the training procedure itself.

---

## Open Questions

Does the causal necessity of alignment transfer to the compression/distillation regime? Merlin-2026 shows alignment is necessary under fine-tuning at constant parameter count; it is entirely silent on whether a compressed student that preserves alignment via an auxiliary loss retains more competence than a compressed student that doesn't. That gap is the exact contribution space of this thesis. A secondary question the paper raises but does not resolve: is the causal relationship monotone, or does it saturate? The Brain Tuned vs Pretrained comparison suggests the gains of *increasing* alignment diminish when starting from a strong pretrained base — a saturation effect that would constrain how much our distillation objective can realistically improve over a perplexity-only student.

---

## Verified

Full PDF read page-by-page (all 33 pages, main paper + all appendices D–I with per-model and per-dataset figures). Real title confirmed: "When Language Models Lose Their Mind: The Consequences of Brain Misalignment." No parse issues. Quantitative win rates and significance levels read directly from Figures 3, 5, 12, 14, 21, 23, 30; subfield breakdowns from Figures 12B, 21B, 30B; phenomenon-level results from Figures 4, 6, 13, 15, 22, 24.

---

## Read Date

2026-06-10


## Related
- [`status.md`](../../status.md) — the canonical status board
