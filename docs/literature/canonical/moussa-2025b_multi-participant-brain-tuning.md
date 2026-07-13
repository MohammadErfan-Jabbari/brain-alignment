---
title: "Brain-tuning Improves Generalizability and Efficiency of Brain Alignment in Speech Models"
tags: [literature]
aliases: [moussa-2025b_multi-participant-brain-tuning]
---

# Brain-tuning Improves Generalizability and Efficiency of Brain Alignment in Speech Models

**Authors:** Omer Moussa; Mariya Toneva
**Year:** 2025
**Venue:** NeurIPS 2025
**DOI/arXiv:** arXiv:2510.21520
**Canonical ID:** moussa-2025b_multi-participant-brain-tuning

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-06-10 — Full 19-page PDF (main paper pp. 1–13 + appendices pp. 14–19) read page-by-page via the Read tool.
Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Single-participant brain-tuning (Moussa et al., ICLR 2025) is data-inefficient and non-generalizable — aligning to a new participant requires large amounts of that participant's own fMRI data. This paper introduces Multi-brain-tuning, which jointly fine-tunes speech models on fMRI data pooled across multiple participants via a shared projection head, dramatically reducing per-participant data requirements and enabling zero-shot transfer to unseen participants and datasets.
2. Core insight: Pooling fMRI data across participants via a single shared FreeSurfer-aligned projection head, updated by per-participant L2 loss computed sequentially and independently, produces representations that generalize across individuals. The critical design choice is NOT averaging losses or responses across participants, but computing and backpropagating each (stimulus, participant-i) pair's loss independently — this retains individual variation that participant-averaged methods discard.
3. If-wrong breakage: If the alignment gains are driven primarily by the increased training-data volume rather than the multi-participant signal structure, stimulus-tuned or LM-tuned baselines at matched data volume should close the gap — but they do not, ruling this out (Fig. 9, Supp. B.3).
4. Main result locations: Sec. 4.1 / Fig. 2 (efficiency); Sec. 4.2 / Fig. 3 (generalization to held-out participants and to Narratives); Sec. 4.3 / Fig. 4 (downstream performance); Sec. 4.4 / Fig. 5 (LoRA rank and loss ablations); Supp. A.3 (loss function math).

---

## Source Grounding

Two pretrained speech model families are brain-tuned: Wav2Vec2.0 and HuBERT (both ~90M parameters, 12 transformer layers, 768-dim, pretrained on 960h of unlabeled audio). The feature extractor is frozen; only the transformer layers (via LoRA rank-8 updates) plus a single shared average-pool + linear projection head are trainable — 0.625% of total model parameters. fMRI data comes from the Moth Radio Hour dataset (LeBel et al., 2024): 8 participants, up to ~16.1h audio per participant (3 participants with 84 stories; 5 participants with 27 stories ≈ 6.4h), TR = 2.0s, 30K voxels per participant across bilateral auditory and late language ROIs after FreeSurfer parcellation. Audio is divided into 2s snippets, each paired with the fMRI TR that incorporates the preceding 8s (4 TRs) to account for hemodynamic delay. Cross-dataset generalization is tested on a held-out 16-participant subset of the Narratives fMRI dataset (Nastase et al., 2021; 56-minute fictional short story, TR = 1.5s). Brain alignment is evaluated via voxelwise ridge-regression encoding models (Pearson r, noise-ceiling normalized) on upper-middle transformer layers; downstream tasks are linear probes on TIMIT phoneme prediction (39 classes) and phonetic sentence type (SA/SX/SI) with F1-score on held-out sets.

---

## Core Claims

- `C1`: Multi-brain-tuning reaches the pretrained model's maximum brain alignment with approximately one-fifth of the per-participant encoding data needed by the pretrained model, and the same one-fifth threshold for held-out participants not seen during brain-tuning.
- `C2`: With full encoding data, Multi-brain-tuning yields up to 50% improvement in normalized brain alignment over the pretrained model's maximum (Fig. 2 caption; Sec. 4.1), and consistently outperforms Single-brain-tuned models at all data fractions.
- `C3`: The Multi-brain-tuned model transfers meaningfully to an entirely new dataset (Narratives): its alignment is close to that of a Narratives-Multi-brain-tuned oracle trained on the same 16 Narratives participants (Fig. 3C), confirming cross-dataset generalization without additional tuning data.
- `C4`: Downstream phoneme prediction and phonetic sentence type F1 improve monotonically with more brain-tuning data; Multi-brain-tuned models eventually match LLM-tuned performance and never fall below pretrained baseline, ruling out catastrophic forgetting.

---

## Evidence Pointers

- `C1` evidence: Fig. 2 (both Wav2Vec2.0 and HuBERT panels), right-hand "Held-out Participants" plots. Both model families show Multi-brain-tuned matching pretrained max at ~1/5 of encoding data; Single-brain-tuned requires ~2/5 for held-out participants. The 5-fold efficiency figure is the encoding data fraction, not the brain-tuning training data size.
- `C2` evidence: Fig. 2 caption explicitly states "improving brain alignment up to 50% from the max. pretrained brain alignment." The y-axis is percent change in alignment from pretrained max, so +50% means 50 percentage points above the pretrained model's noise-ceiling-normalized performance at full data.
- `C3` evidence: Fig. 3C bar chart; Moth-Multi-brain-tuned bar (tuned on Moth data only, evaluated on Narratives participants) is substantially above pretrained and close to Narratives-Multi-brain-tuned (upper-bound oracle).
- `C4` evidence: Fig. 4 (Wav2Vec2.0) and Fig. 11 (HuBERT). F1 improvement curves never cross zero; Multi-brain-tuned converges faster to LLM-tuned level than Single-brain-tuned.

---

## Method Details (Loss Form and Architecture)

The loss for Multi-brain-tuning is the L2 reconstruction loss over a batch B of audio-fMRI pairs for participant i:

$$\mathcal{L}_{l2} = \frac{1}{|B|} \sum_{b=0}^{|B|-1} (R^i_b - \hat{R}^i_b)^2$$

where $R^i_b$ is the ground-truth fMRI response vector (30K voxels, spatially aligned via FreeSurfer to a common cortical surface) and $\hat{R}^i_b = \text{FC}(\text{Pool}(\text{LoRA-transformer}(\text{audio}_b)))$ is the model prediction. The loss is computed and backpropagated independently for each (stimulus, participant-i) pair — not averaged across participants before the gradient step. The projection head is a single FC layer shared across all participants, on top of average-pooled transformer output tokens. LoRA rank = 8 corresponds to 0.625% of the total model parameters; rank > 8 does not improve performance and full-model fine-tuning scales more slowly (Supp. Fig. 8). Training: batch size 128, learning rate $1 \times 10^{-4}$ with 10% warmup + linear decay, 30 epochs, stopped at validation loss saturation; ~6h on 2× NVIDIA A40 48GB GPUs.

Multi-participant combination strategy: each stimulus is used as an anchor; the model is presented with all available fMRI responses for that stimulus sequentially, computing and backpropagating the loss for each participant-stimulus pair independently. This design does NOT require all participants to share the full stimulus set, making it robust to partial overlap.

Three loss functions were ablated (Supp. A.3): L2 (Eq. 1), Correlation loss (1 - Pearson r over voxels), and Cosine + L2 ($\lambda = 0.5$). L2 scales best with data size; Correlation loss is best at very small data sizes ($\leq$ 6 hours) but saturates. L2 was selected for the main experiments.

---

## Assumptions and Limits

All experiments are on speech models only (Wav2Vec2.0 and HuBERT, ~90M parameters). Text-only LMs are never tested. The method is not applied to language models operating on text tokens; the audio-to-TR alignment (2s snippets, 4-TR HRF delay) is specific to the speech modality. Only English-language naturalistic fMRI datasets are used; multilingual generalization is explicitly listed as future work. The "88 participants" figure does not appear in this paper — training uses 3 participants from the Moth dataset (those with the most data, ~16.1h each); the 5 held-out participants for evaluation bring the Moth total to 8, plus 16 Narratives participants for generalization testing. Downstream evaluation covers only phoneme prediction and phonetic sentence type prediction (not the fuller six-task suite from the ICLR 2025 predecessor). No matched-budget compression or distillation experiment is run; the paper makes no claims about models beyond ~90M parameters. The paper does not test whether the shared projection head produces meaningful participant-level decoding or whether the alignment gain transfers to non-English or non-speech stimuli.

---

## Interpretation Notes

**Relation to thesis framings and assumptions:**

F1 (alignment-guided distillation at matched student budget): This paper is the strongest direct existence proof for A1 — it shows that an L2 fMRI loss injected into LoRA-adapted transformer layers is a stable and effective training signal, not a fragile special case. The loss form, the LoRA rank, and the layer strategy (freeze feature extractor, tune transformer) are directly portable to a text-LM distillation setup. However, this paper performs fine-tuning, not distillation; it never asks whether a smaller student starting from random or compressed weights can acquire brain alignment. The distillation loop is the open gap.

F2 (brain as low-data / sample-efficiency regularizer): Directly confirmed and sharpened. The 5-fold data efficiency result (Sec. 4.1 / Fig. 2) is the quantitative backbone of this framing: a Multi-brain-tuned model needs only ~1/5 of the per-participant encoding data to match pretrained model peak alignment. The efficiency benefit also holds for held-out participants (zero-shot transfer), which is stronger than the ICLR 2025 predecessor where per-participant tuning was required. This is the key number for F2 guardrails in our design: brain data volume is not a bottleneck once multi-participant pooling is used.

F3 (fMRI-free differentiable abstraction proxy): This paper deepens the need for F3. The multi-participant generalization result shows that cross-individual alignment is learnable, which means a differentiable proxy (if it captures the cross-individual shared signal) might substitute for real fMRI at inference time. But this paper offers no proxy — all alignment measurements and tuning targets are real fMRI. F3 remains entirely unaddressed.

A1 (alignment is actionable): Strongly confirmed. L2 voxelwise loss on LoRA-adapted speech transformers consistently improves both alignment and downstream performance. The LLM-tuned baseline (Llama2-7B representations as targets) is always worse than brain-tuned at matched data, confirming the signal is specifically neural, not just any rich semantic target.

A2 (alignment is not a nuisance confounder): Confirmed indirectly. Downstream phoneme and sentence-type F1 improve monotonically with brain-tuning data; there is no catastrophic-forgetting regime even at full data. This is a speech-model result only; whether text-LM utility is similarly preserved under brain-tuning is untested.

A3 (preserving alignment buys utility under compression): Not addressed. No compression, distillation, or matched-budget comparison is run. This is the central open question for our thesis.

The paper also settles a design choice directly relevant to our implementation: per-participant independent loss computation beats loss averaging, response averaging, and per-participant separate heads (Supp. A.3 / Fig. 7). This should be adopted if we extend to multi-participant brain data in our own distillation experiments.

---

## Open Questions

Does the 5-fold encoding-data efficiency result transfer to text LMs? The mechanism relies on pooling across participants sharing speech stimuli — for text LMs the stimulus space is word sequences, and the cross-participant shared signal structure may be similar (fMRI during reading), but this has never been tested in this framework. A direct test — Multi-brain-tuning a text LM on the Narratives reading fMRI data — would bridge the gap from this paper to our thesis setting and is the most actionable next experiment the authors do not run.

---

## R03 Claim Verification

R03 states: "multi-participant LoRA brain-tuning, up to +50% alignment, 5× fMRI-data efficiency."

VERDICT: **CORRECT** for the numbers, but with an important precision note on what is measured.

- "+50% alignment": The paper states (Fig. 2 caption, Sec. 4.1) "improving brain alignment up to 50% from the max. pretrained brain alignment." The metric is percent change in noise-ceiling-normalized Pearson r over upper-middle transformer layers, evaluated on held-in and held-out participants. This is 50 percentage points above the pretrained model's already-normalized score, not 50% of an absolute scale. The claim is stated correctly but "50%" could be misread as a relative improvement; it is an absolute improvement in the normalized alignment scale.
- "5× fMRI-data efficiency": Also stated correctly. Fig. 2 shows that Multi-brain-tuned models reach pretrained-model maximum alignment with ~1/5 of the encoding data (for both training and held-out participants, both model families). "5× efficiency" = "needs 1/5 as much data" is arithmetically correct.
- "multi-participant LoRA": LoRA rank = 8 = 0.625% trainable parameters. Correct.
- The one thing R03 omits: the 5× efficiency is measured against the pretrained model's own peak alignment as a threshold — not against the brain-tuned model's peak. The brain-tuned model at full data is substantially higher (+50%), so the efficiency claim is conservative. R03 does not overstate.

---

## Read Date

2026-06-10


## Related
- [`status.md`](../../status.md) — the canonical status board
