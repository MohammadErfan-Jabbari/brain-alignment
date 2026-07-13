---
title: "Brain-Informed Fine-Tuning for Improved Multilingual Understanding in Language Models"
tags: [literature]
aliases: [negi-2025_brain-informed-finetuning-multilingual]
---

# Brain-Informed Fine-Tuning for Improved Multilingual Understanding in Language Models

**Authors:** Anuja Negi*; Subba Reddy Oota* (* equal contribution); Anwar O Nunez-Elizalde; Manish Gupta; Fatma Deniz
**Year:** 2025
**Venue:** NeurIPS 2025 (poster)
**DOI/arXiv:** bioRxiv 10.1101/2025.07.07.662360 · OpenReview JPogehP8By
**Canonical ID:** negi-2025_brain-informed-finetuning-multilingual

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-11 — full 30-page NeurIPS 2025 submission PDF (main text pp. 1–10 + NeurIPS
checklist pp. 13–20 + appendices A–H pp. 21–30) read page-by-page. All figures (1–6) and all tables
(1–11) inspected directly. No parse failures.

Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Prior brain-tuning studies used monolingual (English-only) fMRI data; this paper
   asks whether fine-tuning language models with bilingual brain data (English + Chinese) can elicit
   multilingual and cross-linguistic downstream NLP improvements that monolingual brain-tuning cannot
   produce.

2. Core insight: Bilingual individuals share semantic representations across languages in higher-level
   cortical regions; fine-tuning LMs against bilingual fMRI responses injects this shared structure
   into the model, producing modest but consistent gains on downstream NLP benchmarks not only in the
   fine-tuned language but also in the participant's other language and in entirely unseen languages
   (zero-shot). A TR-shuffled fMRI control and an mBERT-representations-as-target control both fail
   to reproduce the effect on higher-level semantic voxels, confirming brain specificity of the
   encoding gains (though the downstream task comparison is not repeated against TR-shuffled targets).

3. If-wrong breakage: The downstream gains are small (typically +0.5–1.5 pp on individual GLUE/CLUE
   tasks) and are reported as averages across six participants; statistical significance tests on
   individual task gains are absent. The vanilla (pretrained) baseline is the only downstream
   comparison — there is no perplexity-matched or compute-matched fine-tuning control. If a generic
   fine-tuning step on any text target produces equivalent gains, the brain-specificity claim for the
   downstream effects cannot be supported by the current evidence.

4. Main result location: Section 4.2 (pp. 7–8) and Table 1 (p. 8) for downstream NLP; Section 4.1
   (pp. 6–7) and Fig. 2 (p. 6) for brain encoding; Appendix F.1 / Fig. 4 (p. 24–25) for TR-shuffled
   and mBERT controls on encoding performance; Appendix G (pp. 26–30) / Tables 8–11 for
   whole-brain / language-selective / monolingual variants.

---

## Source Grounding

**fMRI dataset (bilingual, primary).** Six healthy bilingual participants (native Mandarin Chinese,
English as L2; 3 male, 3 female) from Chen et al. (2024b). BOLD recorded on a 3T Siemens TIM Trio
scanner, 32-channel volume coil, gradient-echo EPI (TR = 2.0045 s, TE = 35 ms, flip angle = 74°,
voxel = 2.24 × 2.24 × 4.1 mm, 30 interleaved axial slices). Participants read 11 narrative stories
from The Moth Radio Hour (Huth et al. 2016) word-by-word, presented in separate scanning sessions
for English and Chinese. Total coverage: 2756 TRs across 11 stories. Split: 7 stories for
brain-informed fine-tuning (1117 TRs used for VEM validation), 3 stories for VEM training, 1 held-out
story for VEM test (291 TRs). The same story set is used for both languages.

**fMRI dataset (monolingual, control).** Three English-monolingual participants: two from LeBel et
al. (2023) [UTS07, male age 25; UTS08, male age 24] and one from Deniz et al. (2019). Participants
listened to the same Moth Radio Hour stories. Used in Section 4.3 / Table 2 to compare bilingual
vs. monolingual brain-informed fine-tuning targets.

**Cortical region variants.** Fine-tuning is performed separately with three ROI masks: (a)
whole-brain, (b) language-selective regions (Fedorenko et al. 2010 localizer, fsaverage surface
registration), (c) semantically-selective regions (two-stage regression: first regress out low-level
sensory features — word count, letter count, phonemes, diphones, triphones, visual motion energy,
pixel-based orthographic similarity — then select voxels with significant semantic feature
prediction by one-sided permutation test, FDR-corrected, p < 0.05). Main paper Tables 1 and 2 use
semantically-selective regions; Appendix Tables 8–10 report all three variants.

**Language models tested.**

Monolingual:
- BERT-en (English BERT, Devlin et al. 2019): 12 Transformer layers, hidden dim 768.
- BERT-zh (Chinese BERT, Devlin et al. 2019): same architecture, pretrained on Chinese.

Multilingual:
- mBERT (multilingual BERT, Devlin et al. 2019): 12 layers, hidden dim 768.
- XLM-R (Conneau et al. 2020): 12 layers, hidden dim 768 (base version).
- XGLM (Lin et al. 2022): 24 layers, hidden dim 1024 (base version; cross-lingual pretrained).
- LLaMA-3.2 (Touvron et al. 2023): 16 layers, hidden dim 2048; **1B parameter version**. Results
  for XLM-R, XGLM, and LLaMA-3.2 are in Supplementary sections 2 and 3 (not included in the
  main paper Tables 1–2; referenced but not reproduced in the appendices visible in this PDF).

**Brain-informed fine-tuning pipeline.** Pretrained LM receives word-by-word transcript of the
narrative story (sequence length 20 tokens). Representation of the last token from the last hidden
layer is extracted, passed through dropout (p = 0.2), then through differentiable 3-lobe Lanczos
interpolation to downsample to the fMRI TR rate (2.0045 s). A finite impulse response (FIR) filter
with four delays (2, 4, 6, 8 s = 1, 2, 3, 4 TRs) is applied to model hemodynamic lag; the
concatenated delayed representations are passed through a linear projection layer to predict
voxelwise BOLD responses. Training objective: NT-Xent (Normalized Temperature-Scaled Cross-Entropy,
Sohn 2016) between predicted and actual BOLD — the contrastive loss aligns predicted BOLD patterns
to recorded patterns across the batch. MSE, ridge, spatial, and hybrid losses are also tested;
NT-Xent performs best. Optimizer: AdamW (LR = 1e-4, weight decay = 1e-3), 30 epochs, batch 32,
ReduceLROnPlateau scheduler, early stopping (patience = 5 epochs). All transformer layers plus the
projection layer are updated (full fine-tuning, not LoRA). Fine-tuning is done separately per
participant. Hardware: NVIDIA TITAN RTX (24 GB) and RTX A6000 (40 GB).

**Voxelwise encoding model (VEM) evaluation.** Representations extracted from layer 7 (selected by
validation performance) of each model variant, z-scored per voxel per story, downsampled with
Lanczos, delayed with 4-delay FIR, ridge-regressed onto BOLD (MSE loss, L2 regularization λ ∈
[10^-10, 10^-10], 1000 λ values, batch 1000). 5-fold cross-validation for λ selection on the 3
training stories; test performance on the 1 held-out story. Metric: Pearson r between predicted and
recorded BOLD per voxel, per participant, per model variant. Visual cortex voxels are excluded from
the semantically-selective ROI analysis (two-stage regression removes low-level features including
visual motion energy).

**Downstream NLP benchmarks.**
- English: GLUE (9 tasks): CoLA (MCC), SST-2, MRPC, STS-B, QQP, MNLI, QNLI, RTE, WNLI (all
  standard GLUE metrics).
- Chinese: CLUE (7 tasks): AFQMC, CMNLI, CSL, IFLYTEK, TNEWS, ChiD, C³.
- Cross-language (unseen): XGLUE (PAWS-X, XNLI, NER) and XTREME (PAWS-X, XNLI, NER) evaluated
  on German, French, Spanish, Japanese, Korean — 5 languages, not seen during fine-tuning and not
  known to the participants.
- Fine-tuning for downstream evaluation: batch 64, LR 2e-5, weight decay 0.01, batch per device
  128, 3 epochs.

**Baselines.**
- Vanilla pretrained LM (the only downstream comparison baseline).
- TR-shuffled fMRI as fine-tuning target (Appendix C.3): brain responses permuted in blocks of 10
  contiguous TRs, breaking stimulus-response correspondence while preserving temporal autocorrelation
  structure. Used only for VEM encoding comparison, not for downstream NLP tasks.
- mBERT representations as fine-tuning target (Appendix C.3): replaces fMRI with mBERT layer
  representations as the supervisory signal; tests whether using a multilingual model's
  representations (instead of brain data) achieves the same effect. Used only for VEM encoding
  comparison, not for downstream NLP tasks.
- Monolingual brain data as fine-tuning target (Section 4.3 / Table 2): fine-tuning with
  English-only brain data from monolingual participants instead of bilingual brain data. This is the
  only downstream comparison that is not "vanilla pretrained."

---

## Core Claims

- `C1`: Brain-informed fine-tuning with bilingual brain data improves voxelwise encoding performance
  across both languages and both monolingual (BERT-en, BERT-zh) and multilingual (mBERT) models. The
  best-performing fine-tuned variant explains more variance in a majority of voxels (76–84% of
  well-predicted voxels, r > 0.1) relative to the vanilla baseline. The improvement is consistent
  across all 6 participants (Fig. 5, Appendix F.2). Maximum encoding gain reported: Δr ≈ 0.15
  (main text, p. 7). Cross-participant transfer: fine-tuning on Participant 1's data and evaluating
  on Participants 2–6 yields small consistent encoding improvements (Δr ≈ 0.03–0.05) in high-level
  semantic areas (Appendix F.3).

- `C2` (brain specificity of encoding): TR-shuffled fMRI fine-tuning (blocks of 10 contiguous TRs)
  and mBERT-representations fine-tuning both fail to produce systematic improvements in higher-level
  semantic areas; VEM encoding advantage for BERT-en relative to those baselines is
  Δr_vanilla−TRshuffle = 0.133, Δr_vanilla−mBERT = 0.136 (Appendix F.1). This confirms the
  encoding gains are driven by meaningful stimulus-response alignment, not temporal autocorrelation
  artifacts.

- `C3` (downstream NLP — same language): Brain-informed fine-tuned BERT-en (English brain data)
  outperforms vanilla BERT-en on 7/9 GLUE tasks, average gain +0.80 pp, max gain +3.57 (WNLI).
  mBERT-ft-en improves on 7/9 tasks, average +0.89 pp, max +3.12 (WNLI). For Chinese: BERT-zh
  improves 5/7 CLUE tasks, average +0.65 pp, max +1.23 (CSL). mBERT-ft-zh improves 6/7, average
  +0.53 pp, max +1.02 (C³). (Table 1a, semantically-selective ROI fine-tuning.)

- `C4` (downstream NLP — cross-language transfer between known languages): BERT-ft-zh (fine-tuned
  with Chinese brain data) outperforms vanilla BERT-zh on GLUE (English tasks) on 8/9 tasks, average
  +1.01 pp, max +2.82 (WNLI). mBERT-ft-zh improves all 9 GLUE tasks, average +1.61 pp, max +2.96
  (MRPC Acc). BERT-ft-en evaluated on CLUE (Chinese) improves 4/7 tasks, average +0.44 pp, max
  +0.63 (TNEWS F1). mBERT-ft-en improves 6/7 CLUE tasks, average +0.68 pp, max +1.38 (AFQMC).
  (Table 1b, semantically-selective ROI fine-tuning.)

- `C5` (zero-shot transfer to unseen languages): mBERT-ft-en evaluated on XGLUE improves 3/3 tasks
  in German, French, Spanish (avg +0.85, +2.06, +0.14 pp) and 1/3 in Japanese, Korean (+0.14, +0.33
  pp). On XTREME, improves 2/3 in German, French, Spanish, Japanese and 1/3 Korean (avg +0.24,
  +0.81, +0.36, +0.99, +0.04 pp). (Table 1c, semantically-selective ROI.)

- `C6` (bilingual > monolingual brain data for cross-linguistic gains): On GLUE (within-language),
  monolingual brain data fine-tuning improves across several tasks, but bilingual brain-informed
  fine-tuning outperforms monolingual on 7/9 GLUE tasks — specifically on all inference-related
  tasks (MNLI, QNLI, WNLI). On CLUE (cross-language), bilingual brain-informed fine-tuning leads to
  higher performance on 5/7 tasks than monolingual. (Table 2, Section 4.3.)

---

## Evidence Pointers

- C1: Fig. 2 (p. 6), text p. 7 "76–84% of well-predicted voxels"; Fig. 5 Appendix (p. 26) all 6
  participants; "maximum Δr ≈ 0.15" text p. 7.
- C2: Appendix F.1 (p. 23–25), Fig. 4 (p. 25), Δr numbers quoted in text p. 25.
- C3: Table 1a (p. 8), text p. 7; Appendix Table 8a (p. 27) whole-brain/language-selective variants.
- C4: Table 1b (p. 8), text pp. 7–8; Appendix Tables 8b, 9b, 10b.
- C5: Table 1c (p. 8), text p. 8 with individual language averages quoted.
- C6: Table 2 (p. 10), Section 4.3; Appendix Table 11 (p. 30) with whole-brain variant.

---

## Assumptions and Limits

**Baseline is vanilla pretrained only — no perplexity-matched, compute-matched, or generic-text
fine-tuning control.** This is the central methodological gap. The paper compares brain-tuned models
to their unmodified pretrained counterparts. Any generic fine-tuning on a similar corpus (e.g., fine-
tuning on the fMRI stimulus text itself) or a fine-tuning step matched in compute could potentially
produce equivalent downstream gains. The TR-shuffled and mBERT-representations controls address
brain specificity of the *encoding* metric only, not of the downstream NLP gains. The authors do not
run either control as a downstream task comparison. This is the most important limitation for our
thesis: the claim that brain data specifically buys downstream NLP utility cannot be separated from
"fine-tuning on naturalistic text buys downstream NLP utility" with the current experimental design.

**No shuffled-brain control on downstream tasks.** A TR-shuffled fine-tuning condition evaluated on
GLUE/CLUE would be the direct brain-specificity null for the downstream gains — it is absent.

**No compression or distillation.** The models are fine-tuned (full fine-tuning, all layers), not
compressed. No student-teacher setup, no budget-matched distillation, no pruning or quantization.
The paper does not address whether brain-tuned representations survive compression.

**Small-N and no significance tests on individual downstream task gains.** N = 6 bilingual
participants; error bars in Table 1 are SD across participants. No formal hypothesis test (t-test,
permutation) is reported for individual GLUE/CLUE task improvements. The NeurIPS checklist item 7
cites "multiple experiments across 6 participants" as the statistical justification, which is an
unusual framing — the 6 replicates are participants in the VEM experiment, not independent
fine-tuned models. Downstream fine-tuning is done once per participant, so the SD in Table 1
captures participant-level variation, not seed-level stability.

**No sample-size calculation.** Explicitly acknowledged (Section B.2, p. 22): "No sample size
calculations were performed, as each participant serves as a full replication of the results."

**Only two fine-tuning languages (English and Chinese).** Cross-linguistic generalization is claimed
from the fMRI of two typologically close-ish high-resource languages; whether bilingual brain data
from, e.g., English + Korean would generalise differently is untested.

**Anti-confound rigor relative to Hadidi/Feghhi:** The paper does not use contiguous train-test
splits in the Hadidi/Feghhi sense for the fMRI regression used in fine-tuning target construction.
The VEM evaluation uses a held-out story (1 of 11), which is story-level holdout — similar in spirit
to contiguous splits. Semantically-selective voxel selection explicitly removes low-level sensory
features (word count, letter count, phonemes, diphones, triphones, visual motion energy,
orthographic similarity) via two-stage regression, which is a partial nuisance-removal step. However:
(a) sentence position and sentence length are not explicitly listed as controlled features; (b) no
OASM or autocorrelation-model baseline is reported; (c) the TR-shuffled control uses blocks of 10
contiguous TRs — coarser than the within-passage shuffle that Hadidi/Feghhi show inflates scores.
The Hadidi/Feghhi five-point protocol (contiguous splits, OASM, SP+SL, static word embeddings,
untrained control) is not fully implemented.

**Gains are modest.** Average downstream gains are typically +0.5–1.6 pp across tasks; individual
task maxima reach +3.57 pp (WNLI, notoriously unstable). These are real but small.

**XLM-R, XGLM, LLaMA-3.2 results referenced but not fully tabulated.** Main paper and appendices
note "Results for other multilingual language models (XLM-R, XGLM, and LLaMA) are also reported in
the Supplementary sections 2 and 3" — these are in a separately downloadable zip file not included
in the main 30-page PDF; the quantitative values for those models are not directly readable from the
available document.

---

## Relevance to this thesis

**Which assumption this paper touches:** A3 — does preserved/induced brain alignment improve
something practical beyond the alignment metric?

**Role in our framework:** This is the most direct existing A3-positive evidence. Negi et al. is the
paper E009 is designed to surpass in rigor. It provides a usable prior for the effect size (typical
downstream gains +0.5–1.6 pp, max ~3.5 pp on individual tasks) and a clear statement of what is
missing.

**What it gives us (positive):**
- First published demonstration that brain-tuning a text LM (not just a speech LM) produces
  downstream NLP gains across multiple languages, going beyond the [Schwartz et al. (2019)](schwartz-2019_inducing-brain-relevant-bias.md) founding
  work and the Moussa et al. (2025) speech-model line.
- The multilingual and zero-shot transfer result is a new A3-relevant finding: the semantic
  structure encoded by bilingual fMRI generalises beyond the fine-tuning languages, which is
  consistent with the shared-semantics hypothesis.
- The monolingual vs. bilingual comparison (C6 / Table 2) is directly useful: it shows the
  cross-linguistic gains require specifically bilingual brain data, not generic fine-tuning on any
  brain data — a partial brain-specificity argument for the downstream effects.
- The TR-shuffled and mBERT-representations controls on encoding (not downstream) establish that
  brain-specificity controls are feasible in this design.

**What our thesis adds beyond it:**

1. **Matched-perplexity baseline (critical gap).** Negi et al. compare only to vanilla pretrained.
   E009 adds a `kd_ppl` arm fine-tuned to matched perplexity on the same data — directly testing
   whether brain data adds anything beyond the fine-tuning step per se.

2. **Brain-specificity null on downstream tasks (critical gap).** Negi et al. run the TR-shuffled
   control only for encoding. E009 includes a `kd_brain_permuted` arm (permuted fMRI targets) as a
   downstream-task null — the load-bearing control that Negi et al. do not run.

3. **Compression and distillation.** Negi et al. do not compress; E009 frames the brain-tuned signal
   as a distillation objective in a student-teacher setup at matched student budget — the F1 gap.

4. **Primary outcome = robustness/OOD, not accuracy** (per pirlot-2022 and Hoak et al. 2025 lessons
   in E009 design): accuracy gains may be reproducible by shuffled controls; robustness/OOD gains
   are where the brain-specificity signal should survive. Negi et al. report only accuracy.

5. **Statistical rigor:** E009 predeclares ≥ 3 seeds, bootstrap CIs, a minimum detectable effect,
   and the decision rule (A3 CONFIRMED vs. A3 NULL) before running. Negi et al. have no seed-level
   replication and no formal significance tests on downstream task gains.

**Design guardrail this paper informs:** The fMRI fine-tuning pipeline architecture (NT-Xent loss,
FIR hemodynamic modeling, Lanczos downsampling, layer 7 as the best-performing layer for
BERT/mBERT-class models, dropout p = 0.2) is directly reusable for our E009 brain-tuning step. The
training hyperparameters (LR 1e-4, AdamW, 30 epochs, batch 32) provide a starting point.

**How strongly we can lean on it as A3 prior:** Lean on it as *encouraging positive prior art that
motivates E009* — it establishes that brain-tuning a text LM can produce downstream gains and that
those gains generalise cross-linguistically. Do not lean on it as *evidence that the gains are
brain-specific* for downstream tasks — that claim is unsupported by the existing controls. Our
contribution is exactly the matched-ppl + permuted-brain downstream evaluation that would settle the
question.

**Does this paper change anything in [`docs/01-research-landscape.md`](../../01-research-landscape.md)?** Yes — it should be added to
Section A as a new row in the "What the alignment signal is, and what drives it" table, directly
adjacent to the Moussa et al. (2025) row. The existing E009 design doc (S8 lit-scout entry) already
cites Negi et al. accurately; the landscape should be updated to reflect that the full paper has now
been read and the limitation (no matched-ppl control, no shuffled-brain downstream null) is
confirmed. Suggested addition to the table in Section A:

> | Negi, Oota et al. 2025 (NeurIPS) | `negi-2025_brain-informed-finetuning-multilingual` | **Closest A3 prior art.** Bilingual brain-tuning (NT-Xent, full fine-tune) of BERT-en, BERT-zh, mBERT, XLM-R, XGLM, LLaMA-3.2 on 6 bilingual participants (EN+ZH, Moth Radio Hour); downstream GLUE/CLUE/XGLUE/XTREME gains +0.5–1.6 pp avg, zero-shot to 5 unseen languages. **Baseline = vanilla pretrained only** — no perplexity-matched, compute-matched, or shuffled-brain downstream control. **No compression/distillation.** This is the gap E009 closes. |

---

## Verified

Full 30-page NeurIPS 2025 submission PDF (bioRxiv 10.1101/2025.07.07.662360, downloaded from
OpenReview attachment JPogehP8By) read page-by-page in two calls (pp. 1–10, pp. 11–20, pp. 21–30).
All tables (1–11) and all figures (1–6 main + Appendix Fig. 3–6) inspected. Key numbers confirmed
directly from Tables 1, 2, 8–11 and from the text of Sections 3.3, 3.4, 4.1, 4.2, 4.3, and
Appendix F.1. The supplementary zip (sections 2–3, XLM-R / XGLM / LLaMA results) was not
separately accessible; those model results are flagged above as not read.
Read date: 2026-06-11


## Related
- [`status.md`](../../status.md) — the canonical status board
