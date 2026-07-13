---
title: "Brain-Informed Language Model Training Enables Scalable and Generalizable Alignment with Human…"
tags: [literature]
aliases: [bilgin-2026_brain-informed-lm-training]
---

# Brain-Informed Language Model Training Enables Scalable and Generalizable Alignment with Human Brain Activity

**Authors:** Isil Poyraz Bilgin; Marie St-Laurent; Pierre Bellec; Leila Wehbe
**Year:** 2026
**Venue:** ICLR 2026 (under double-blind review at time of PDF)
**DOI/arXiv:** OpenReview ID 07S1CPoQYP (no arXiv preprint as of 2026-06-10)
**Canonical ID:** bilgin-2026_brain-informed-lm-training

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 20-page PDF read page-by-page including all appendices (A.1–A.11) and supplementary figures (S1–S3). Prior note was abstract-only with multiple [inferred] flags; all have now been resolved from the full text.

Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Prior work treats brain alignment as a post-hoc measurement; this paper asks whether fMRI from naturalistic movie watching can be used as an active training signal for general-purpose text LMs, improving both encoding and downstream utility.
2. Core insight: Inserting LoRA adapters into the upper layers of a pretrained LM and training with a dual-loss objective (cosine-similarity brain loss + token CE LM loss, adaptively weighted) consistently beats both a frozen text-only baseline and a brain-from-scratch model on voxelwise encoding, with gains scaling with both data volume (1–40 h) and model size (GPT-2 124M vs. LLaMA-2 7B); LLaMA-2 shows consistent VL-Commonsense gains while GPT-2 does not.
3. If-wrong breakage: The paper includes no shuffled-brain or random-brain control; all encoding improvements are attributed to the brain signal specifically, but without a permuted-target ablation this attribution is not verified. Training and validation TRs are randomly shuffled within-subject, which does not follow Feghhi-style contiguous splits and may overstate generalization.
4. Main result location: Section 4.1 (Figures 2–3, scaling with data and model size), Section 4.2 (Figure 4, dual-loss vs. brain-only), Section 4.4 (cross-subject generalization), Section 4.5 (Figure 6, cross-stimulus generalization to Movie10), Section 4.6 (Table 1, VL-Commonsense CoDa), Discussion (Section 5).

---

## Source Grounding

**Dataset.** CNeuroMod Friends fMRI corpus: 50 hours of fMRI from 6 English-speaking participants (3 women) watching the Friends TV show, acquired on a 3T Siemens PrismaFit scanner, TR = 1.49 s. Season 3 of Friends is the held-out test set; remaining seasons are used for training and validation with an incremental scheme at 1, 5, 10, 20, 30, and 40 hours. Movie10 (approximately 10 hours of fMRI from audiovisual movies: The Wolf of Wall Street, The Bourne Supremacy, Hidden Figures, and Life) provides the cross-stimulus out-of-distribution evaluation. fMRI preprocessed with fMRIPrep; confound regressors include framewise displacement, DVARS, global signals, and physiological components (aCompCor, tCompCor).

**Text/stimulus alignment.** Movie transcripts extracted from DVDs and word-aligned to the audio track using AssemblyAI automatic speech-to-text. Each word is tokenized with the LM tokenizer; sub-tokens inherit the word's timestamp. For each TR, the 32 most recent tokens are selected and weighted by a canonical single-gamma HRF:

$$\text{HRF}(t) = \begin{cases} t^{8.6}\, e^{-t/0.547}, & t \leq 15 \\ 0, & t > 15 \end{cases}$$

This yields a temporal integration window of approximately 12–15 seconds, covering 5–6 seconds of preceding speech. HRF weights are applied to the final-layer LM hidden states, producing a weighted linear combination fed to the voxelwise encoding head.

**Models.** GPT-2 (124M parameters) and LLaMA-2 (7B parameters). Both are pretrained text LMs, not trained from scratch. LoRA adapters (rank 8 for GPT-2, rank 16 for LLaMA-2) are inserted into the self-attention projections and feedforward blocks of the last 6 layers of GPT-2 and the last 8 layers of LLaMA-2. All other LM weights are frozen. A fully connected voxelwise linear encoding layer (ridge-regularized) maps final-layer HRF-weighted representations to predicted BOLD time series. This encoding layer is trained jointly with the LoRA adapters; the CNN feature extractor analogy does not apply here — there is no frozen front end.

**Training setup.** Three regimes are compared: (i) brain-fine-tuned (pretrained LM + LoRA + encoding head, dual-loss), (ii) brain-from-scratch (randomly initialized transformer + linear encoding head, brain loss only, serves as a lower-bound control), (iii) text-only baseline (frozen LM backbone, only encoding head trained, non-fine-tuned). Two loss objectives are compared within regime (i): brain-only loss versus the dual-loss. The dual-loss objective (Appendix A.5, Equation 1) is:

$$\mathcal{L} = w_{\text{brain}} \cdot \underbrace{\mathcal{L}_{\text{brain}}}_{\text{cosine similarity}} + w_{\text{lm}} \cdot \underbrace{\mathcal{L}_{\text{LM}}}_{\text{token CE / perplexity}} + \lambda \|W_{\text{ridge}}\|_2^2$$

with $w_{\text{brain}} + w_{\text{lm}} = 1$ and an adaptive weighting schedule that increases $w_{\text{brain}}$ whenever validation perplexity plateaus (with patience and minimum-steps guards). This preserves linguistic structure early and prioritizes brain alignment once LM loss saturates. The brain loss is **cosine similarity** between predicted and observed voxelwise BOLD responses — not L2. AdamW optimizer; separate learning rates for LoRA layers ($10^{-5}$–$10^{-4}$) and the ridge encoding head (smaller, fixed); early stopping on validation loss. Per-subject fine-tuning: each of the 6 subjects is trained separately.

**Split strategy.** Movie segments are randomly shuffled for both training and validation datasets. The test set is Season 3 of Friends (unseen episodes held out entirely). This is TR-level random shuffling within the training/validation partition, not the Feghhi-style contiguous-split protocol; temporal autocorrelation across train/val boundaries is not controlled.

**Cross-subject generalization.** LM and LoRA parameters are frozen after training on a source subject; a new voxelwise RidgeCV layer is re-fit for each target subject from their own data. The LM representations are thus shared and fixed; only the linear readout adapts to new voxel geometry. This is not zero-shot transfer — it requires new fMRI from the target subject to fit the readout.

**Downstream evaluation.** VL-Commonsense (CoDa; Zhang et al. 2022): a text-based probe of visual-linguistic commonsense evaluating noun-attribute relations (Color, Co-occurrence, Material, Shape, Size). Scored via conditional next-token log-probability with PMI de-biasing and tokenization controls (per-candidate token capping). Top-1 accuracy per relation; micro-averaged overall. Results in Table 1 (main text, p.9).

---

## Core Claims

- `C1`: Brain-fine-tuned models consistently outperform the text-only baseline on voxelwise encoding (Pearson r), with gains that increase monotonically from 1 to approximately 20–30 hours of training data, after which GPT-2 plateaus and LLaMA-2 shows modest continued improvement to 40 hours (Figure 4).
- `C2`: Larger model capacity amplifies the brain-fine-tuning benefit: LLaMA-2 (7B) achieves higher encoding accuracy than GPT-2 (124M) across the cortex, with the strongest differential gains in higher-order association cortices (Figure 3).
- `C3`: Dual-loss training (brain + LM) outperforms brain-only-loss training from 5 hours onward, with the strongest advantage at approximately 20 hours; beyond 30 hours the advantage slightly reverses for LLaMA-2, suggesting possible overfitting (Figure 4).
- `C4`: Brain-fine-tuned representations generalize across subjects at the voxel level: representations trained on one participant predict another participant's voxel responses reliably, with consistent mean correlations across all subject pairs and data volumes from 1 to 40 hours (Appendix Figure S10).
- `C5`: Brain-fine-tuned GPT-2 and LLaMA-2 generalize to all five unseen Movie10 movies, producing widespread cortical activation predictions despite no training on these stimuli (Figure 6).
- `C6`: Brain-fine-tuning improves LLaMA-2's VL-Commonsense (CoDa) performance from 0.560 to 0.584 overall, with the largest gains on Co-occurrence (+0.092) and Color (+0.039); GPT-2 does not benefit (0.381 base vs. 0.375 fine-tuned; Table 1).
- `C7`: The dual-loss schedule avoids representational collapse relative to brain-only optimization, which is prone to collapse at higher data volumes.

---

## Evidence Pointers

- `C1` evidence: Figure 2 (voxelwise Pearson r maps at 1, 5, 10, 20, 30, 40 h for one subject); Figure 4 (mean voxelwise correlation curves across training durations for GPT-2 and LLaMA-2 on sub-03); Appendix Figure S7 (all subjects). Table 2 (Appendix): at 10h GPT-2 achieves mean correlation 0.0330, val loss 0.9738; at 5h 0.0217 / 0.9752; at 1h 0.0086 / 0.9933.
- `C2` evidence: Figure 3 (voxelwise comparison maps LLaMA-2 vs. GPT-2 for sub-03; scatter plot with most points above diagonal).
- `C3` evidence: Figure 4; text p.6 "from 5h onward, dual-loss consistently surpasses brain-only-loss, with the strongest advantage at 20h."
- `C4` evidence: Appendix Figure S10; text p.8 "consistent mean correlations across subjects and training durations (1–40 hours) for both GPT-2 and LLaMA backbones."
- `C5` evidence: Figure 6 (cross-stimulus cortical maps for 5 movies); text p.8 "brain-fine-tuned models consistently predicted neural responses across all five unseen movies and in all subjects."
- `C6` evidence: Table 1 (p.9): LLaMA-2 base 0.560 vs. fine-tuned 0.584; GPT-2 base 0.381 vs. fine-tuned 0.375. Text p.9 "the largest absolute gain is in co-occurrence, followed by color and shape."
- `C7` evidence: Text pp.6–7; Appendix Figure S8 (optimization trajectories).

---

## Assumptions and Limits

No shuffled-brain or random-brain-tuned control is run anywhere in the paper. The encoding gains over the text-only baseline are attributed entirely to the brain signal, but without a permuted-target ablation this attribution rests on the face plausibility of the dual-loss architecture rather than an ablation. This is the most important gap for evaluating validity under learning L003.

Training and validation TRs are randomly shuffled within the Friends episodes used for training. The test set (Season 3) is held out entirely, providing some temporal separation, but the TR-level shuffling within train/val may inflate validation estimates relative to a strictly contiguous split, since temporally adjacent TRs share hemodynamic and contextual autocorrelation.

The "scales with model size" claim rests on exactly two model sizes (GPT-2 124M and LLaMA-2 7B), which differ by approximately 56 times in parameter count and also differ in architecture (GPT-2 decoder vs. LLaMA-2 decoder with grouped-query attention and RoPE). This is not a controlled scaling curve within one family.

GPT-2 does not improve on CoDa overall (0.375 vs. 0.381 baseline); the VL-Commonsense result is therefore model-specific to LLaMA-2. The interpretation that brain supervision injects visually grounded knowledge only holds for the larger model.

The Friends stimulus is dialogue-heavy audiovisual content. The LM receives only the text transcript, but the brain response integrates audio, visual, and social processing. The alignment target therefore contains non-linguistic variance that the text LM cannot in principle model, raising the noise ceiling question.

Cross-subject generalization requires re-fitting a new voxelwise RidgeCV layer per target subject from new fMRI data; it is not zero-shot transfer of the full encoding model.

No compression, distillation, or matched-budget experiment is run. The paper adds LoRA adapters (rank 8 or 16) and a linear encoding head, increasing effective trainable parameters. It never produces a smaller or computationally cheaper model.

The adaptive loss weighting schedule (Appendix A.5) introduces hyperparameters (brain_weight_start, brain_weight_final, perp_patience, sched_steps, sched_min_epochs) that are tuned on validation; the sensitivity of results to this schedule is not fully ablated.

Only 6 subjects are used; the brain-from-scratch model is treated as a lower-bound control rather than a practical baseline.

---

## Interpretation Notes

**Scooping verdict on the bare text-LM inversion: YES, definitively scooped.** The paper establishes end-to-end that fMRI can guide text LM training (GPT-2, LLaMA-2), that it improves brain encoding measurably over a frozen text-only baseline, that it generalizes cross-subject and cross-stimulus, and that it transfers to downstream VL-Commonsense for LLaMA-2. The bare claim "use fMRI as a training signal for a text LM" is no longer an open question — it has been run, and the answer is yes.

**Does our distillation gap (F1) survive? YES, cleanly.** Bilgin et al. augment pretrained LMs with LoRA and an encoding head; they never compress. The question "does brain-alignment guidance improve the alignment/utility trade-off for a smaller model at a matched student parameter budget compared to perplexity-only KD?" is entirely absent. The paper's own Discussion (p.10) explicitly identifies "broader architectural sweeps" and "capacity interaction with neural supervision" as future work but does not touch distillation or compression. F1 is untouched.

**Does the low-data regularizer gap (F2) survive? PARTIALLY, but weakened.** The paper runs a genuine data-scaling experiment from 1 to 40 hours and shows continued gains up to 20–30 hours. Table 2 (Appendix) shows GPT-2 mean voxelwise correlation rising from 0.0086 (1h) to 0.0330 (10h). However, this is not framed as a systematic low-data regularization test: there is no matching text-data-scarce condition for the LM component, no matched-budget comparison against a text-only LM trained on equally scarce text, and the weak-prior bound mechanism (that brain regularization helps most when text data is scarce, as predicted by the PAC-Bayes argument in R03) is not tested. The data-scaling curve provides existence proof that less brain data is worse, but not the contrastive prediction F2 requires.

**R03 claim check:**
> "fMRI-augmented training of GPT-2 (124M) and LLaMA-2 (7B) on Friends fMRI beats text-only baselines, scales with model size, generalizes across subjects/stimuli, and helps VL-Commonsense. This is the inversion, for text LMs, already published."

Verdict: **MOSTLY CORRECT, two details need updating.** (1) The model size pair is confirmed (GPT-2 124M, LLaMA-2 7B). (2) "Beats text-only baselines" on encoding: correct for both models. (3) "Scales with model size": confirmed directionally (LLaMA-2 > GPT-2) but this is two data points with architectural differences, not a scaling curve. (4) "Generalizes across subjects/stimuli": correct. (5) "Helps VL-Commonsense": correct for LLaMA-2 (+0.024 overall); **GPT-2 actually regresses slightly (−0.006)**. R03 should say "helps VL-Commonsense for LLaMA-2; GPT-2 does not benefit." (6) "The inversion for text LMs, already published": correct and confirmed.

**Critical correction from abstract-only note:** The brain loss form was [inferred] as L2 voxelwise in the prior note. The full text (Appendix A.5, Equation 1 label) confirms it is **cosine similarity**, not L2. This matters for replication and for our own implementation: cosine similarity loss normalizes out scale differences between predicted and observed BOLD, which has different gradient behavior than L2.

**Critical addition from full text:** The abstract-only note did not flag the shuffled-split problem. The full text (Section 3.1) states training and validation TRs are randomly shuffled. This means the paper does not follow the Feghhi anti-confound protocol (L003). The encoding gains are real but their magnitude may be inflated relative to a contiguous-split estimate.

**Relation to A1/A2/A3.**
- A1 (brain alignment is an actionable training signal): directly confirmed by C1–C5, conditional on the missing shuffled-brain control.
- A2 (alignment is anti-confounded / real): not verified in this paper. No shuffled-brain, no random-fMRI control, and TR-level random shuffling across train/val does not guard against temporal autocorrelation confounds. This is the main evidential gap.
- A3 (alignment correlates with downstream utility): partially confirmed by C6 for LLaMA-2 only; GPT-2 fails to show this. The relationship is model-size-dependent and the mechanism (multisensory inductive bias from audiovisual stimuli) is hypothesis only.

---

## Open Questions

The single most tractable question this paper leaves open for our thesis: does brain-alignment-guided training improve the alignment/utility trade-off for a **compressed** model at a matched parameter and compute budget compared to perplexity-only knowledge distillation? Bilgin et al. exclusively fine-tune upward (LoRA adds parameters, encoding head adds parameters). The question of whether the same cosine-similarity brain loss, applied during KD from a large teacher to a small student, produces a student with better alignment and downstream performance than a perplexity-matched student is entirely untested in the 2026 literature.

Secondary question: does the cosine-similarity brain loss, rather than L2, drive the dual-loss benefit? The choice of cosine similarity over L2 is stated but not ablated, and it changes the gradient geometry substantially.

---

## Read Date

2026-06-10


## Related
- [`status.md`](../../status.md) — the canonical status board
