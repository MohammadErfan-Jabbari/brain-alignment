---
title: "Inducing Brain-Relevant Bias in Natural Language Processing Models"
tags: [literature]
aliases: [schwartz-2019_inducing-brain-relevant-bias]
---

# Inducing Brain-Relevant Bias in Natural Language Processing Models

**Authors:** Dan Schwartz; Mariya Toneva; Leila Wehbe
**Year:** 2019
**Venue:** NeurIPS 2019
**DOI/arXiv:** arXiv:1911.03268
**Canonical ID:** schwartz-2019_inducing-brain-relevant-bias

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-11 — full 18-page paper (9 main + 9 appendix) downloaded from arXiv, converted with pdftotext, and read in full including all appendix figures (A1–A8) and Table 1. No parse issues.

Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Standard pretrained LMs are not explicitly trained to encode brain-relevant language information; fine-tuning BERT on fMRI and MEG recordings from people reading text might bias it toward representations that better capture how the brain processes language.
2. Core insight: MSE-fine-tuned BERT predicts held-out fMRI better than frozen BERT (the vanilla baseline), the learned relationship transfers across participants, and GLUE scores are not hurt — but the paper never tests against a shuffled-brain control, uses no matched-perplexity baseline, and the GLUE gains are framed as "does not harm" rather than a genuine improvement claim.
3. If-wrong breakage: The core result (fine-tuned > vanilla on brain prediction) is not accompanied by a permuted-target or random-label control, so the benefit could arise from any auxiliary fine-tuning signal, not specifically from the brain's representational content.
4. Main result location: Section 4 (Results), Figure 2 (accuracy curves), Figure 3 (voxelwise maps), Table 1 (GLUE), Section 5 (Discussion).

---

## Source Grounding

**Brain data.** Two datasets, both from participants reading Chapter 9 of *Harry Potter and the Sorcerer's Stone* word-by-word at 0.5 s per word (5,176 words total).

- **fMRI (Wehbe et al. 2014b):** 9 participants, 3×3×3 mm voxels, data published online. After masking for grey matter, 50,000–60,000 voxels per subject are retained. Data are slice-time and motion corrected (SPM8), detrended, and per-voxel standardized within each of the 4 scanner runs.
- **MEG (Wehbe et al. 2014a):** 9 participants recorded with Elekta Neuromag (306 sensors, 1 kHz sampling, downsampled to 25 ms non-overlapping bins → 20 time points per word). One participant excluded for artifacts, leaving 8 usable. SSS + tSSS noise reduction applied. Only content words (adjective, adverb, aux verb, noun, pronoun, proper noun, verb) are used for MEG training and evaluation.

**Model.** BERT-base (Devlin et al. 2018; 12 layers, pretrained on BooksCorpus + Wikipedia). All 12 transformer layers are fine-tuned end-to-end.

- **MEG head:** a linear layer maps per-token output embeddings (concatenated with word length and context-independent log-probability of the word) to 6,120 values (306 sensors × 20 time points) per content word.
- **fMRI head:** a linear layer maps the [CLS] token embedding to the voxelwise BOLD pattern for the 20-word window preceding each fMRI image.
- **Loss function:** mean squared error (MSE) for both modalities.
- **Optimizer:** linear warmup to lr = 5×10⁻⁵ (first 10% of epochs), linear decay back to 0. Epochs vary by comparison (10–50) but are matched within each pair. Random seeds matched across compared runs.

**Training regimes compared.** Four variants (Section 3.4):

1. *Vanilla model* — pretrained BERT frozen; only the linear output head is trained per fMRI participant (10–30 epochs).
2. *Fine-tuned model* — per-participant: linear head trained 10 epochs, then full BERT fine-tuned 20 epochs.
3. *Participant-transfer model* — fine-tuned on the single most-predictable fMRI participant (same 10+18 schedule), then frozen; for each other participant only a new linear head is trained for 10 epochs.
4. *MEG-transfer model* — jointly fine-tuned on all 8 MEG participants (10+20 epochs), then per-participant fMRI fine-tuned (10+20 epochs).
5. *Fully joint model* — simultaneously trains on all MEG and all fMRI participants (10+50 epochs).

**Evaluation metric.** The "20 vs. 20" classification accuracy (Mitchell et al. 2008): for each held-out fMRI run, 1,000 times sample 20 examples as target and 20 as distractor, check if the model's prediction is closer (Euclidean) to the target than to the distractor; accuracy averaged over voxels. Four-fold cross-validation (one run held out at a time). Proportion of variance explained is also computed as a secondary check (Appendix A4; qualitatively consistent).

**Downstream NLP evaluation.** GLUE benchmark development sets — only two of the five model variants are run: the MEG-transfer model and the fully joint model. Compared to the vanilla pretrained BERT from the Hugging Face repo (not to the author-trained vanilla baseline).

---

## Core Claims

- `C1`: Fine-tuned BERT predicts held-out fMRI more accurately than frozen vanilla BERT on the 20 vs. 20 classification task, with gains concentrated in canonical language network regions (Figure 2a, Figure 3 row 1).
- `C2`: The participant-transfer model (fine-tuned on one participant, linear-only for all others) outperforms vanilla BERT for all other participants, showing the learned language-brain relationship generalizes across individuals (Figure 2c, Figure 3 row 2).
- `C3`: For some but not all participants, MEG-transfer fine-tuning improves fMRI prediction in language regions compared to fMRI-only fine-tuning; results are mixed participant-to-participant (Figure 2b, Figure 3 row 3; "mixed results" is the authors' own characterization).
- `C4`: The fully joint model (all MEG + all fMRI participants) outperforms vanilla BERT, though it does not match individually fine-tuned models (Figure 2d).
- `C5`: Fine-tuning on brain data does not harm GLUE performance; for 11 of 13 GLUE subtasks, at least one brain-fine-tuned model is marginally better than pretrained BERT. The STS-B task is the exception (slightly worse).

---

## Evidence

**Brain prediction (20 vs. 20 accuracy).** No single absolute accuracy number is reported in the main text; results are presented as difference-in-accuracy curves in Figure 2, with per-participant colored lines and a black mean. The curves for fine-tuned vs. vanilla (Figure 2a) show consistent positive differences across voxels for most participants; the curves for MEG-transfer vs. fine-tuned (Figure 2b) are near zero on average with participant-level variability. No single headline correlation or R² is given in the main text (variance-explained version in Appendix A4 confirms the direction but is noted to show overfitting for noisier voxels).

**GLUE scores (Table 1).** The three columns are Vanilla (pretrained BERT), MEG-transfer, and Joint:

| Task | Vanilla | MEG | Joint |
|---|---|---|---|
| CoLA | 57.29 | 57.63 | 57.97 |
| SST-2 | 93.00 | 93.23 | 91.62 |
| MRPC Acc. | 83.82 | 83.97 | 84.04 |
| MRPC F1 | 88.85 | 88.93 | 88.91 |
| STS-B Pears. | 89.70 | 89.32 | 88.60 |
| STS-B Spear. | 89.37 | 88.87 | 88.23 |
| QQP Acc. | 90.72 | 91.06 | 90.87 |
| QQP F1 | 87.41 | 87.91 | 87.69 |
| MNLI-m | 83.95 | 84.26 | 84.08 |
| MNLI-mm | 84.39 | 84.65 | 85.15 |
| QNLI | 89.04 | 91.73 | 91.49 |
| RTE | 61.01 | 65.42 | 62.02 |
| WNLI | 53.52 | 53.80 | 51.97 |

The differences are small: the largest gain is RTE (+4.41 for MEG vs. Vanilla); the largest loss is SST-2 (−1.38 for Joint vs. Vanilla). The authors state: "The fine-tuning may or may not be helping the model to perform these NLP tasks, but it clearly does not harm performance in these tasks."

**Key quote on the strength of claim (Section 4, NLP section):** "Apart from the semantic textual similarity (STS-B) task, all of the other tasks are very slightly improved on the development sets after the model has been fine-tuned on brain activity data." And from the Discussion: "Models which have been fine-tuned to predict brain activity are no worse at NLP tasks than the vanilla BERT model."

**Attention analysis.** Fine-tuning reduces [CLS]-to-[SEP] attention in layers 8 and 9, interpreted tentatively as the model attending less to the "no-op" token and more to content.

---

## Limitations

**No shuffled-brain or permuted-target control.** The key confound is never tested: would fine-tuning on temporally shuffled (or spatially randomized) fMRI produce equally good brain predictions and equally neutral GLUE results? Without this control, the benefit of fine-tuning cannot be attributed to brain representational content specifically — any auxiliary training signal with similar statistical structure could produce the same pattern. This is the single largest validity gap.

**No matched-perplexity baseline.** The paper does not control for the fact that fine-tuning on brain data changes the LM's language model loss (perplexity). A model fine-tuned on brain data for 20+10 epochs moves away from its LM pretraining objective. The GLUE comparison is therefore not at matched perplexity — it confounds the brain signal with the auxiliary fine-tuning regime.

**Only two of five models evaluated on GLUE.** The MEG-transfer and fully joint models are the only variants run on GLUE. The per-participant fine-tuned model — the primary brain-prediction winner — is never evaluated on downstream NLP tasks. The selection is acknowledged in the text ("These models were chosen because we thought they had the best chance of giving us interesting GLUE results") which introduces cherry-picking risk.

**Cross-validation is run-based, not contiguous-split.** The four fMRI runs divide the Harry Potter chapter into four sequential segments. Cross-validation holds one run out, which does give some temporal separation. However, within each training partition, examples from adjacent runs share story context and hemodynamic autocorrelation. This does not follow the stricter contiguous-split protocol of Feghhi et al. (2024) and may inflate estimates.

**Single stimulus, single language, single modality of reading.** All data come from one chapter of one English novel, read one word at a time. Generalization to other corpora, languages, or naturalistic reading is entirely untested.

**No absolute brain-prediction numbers reported.** All brain results are presented as accuracy differences (Figure 2) rather than absolute 20 vs. 20 accuracies, making it impossible to assess effect size against noise ceilings or to compare with later work's absolute correlations.

**Small sample sizes for feature analysis.** The feature distribution analysis (Section 7.3 / Appendix) is explicitly flagged as preliminary: 146 changed examples vs. 1,022 unchanged. The "move" label finding is treated as a hypothesis, not a claim.

---

## Relevance to this thesis

**Anchor (A1/A3).** This is the founding paper for the idea that brain fine-tuning of a text LM leaves GLUE performance intact or marginally improved — directly the historical baseline E009 must acknowledge. It instantiates A1 (brain alignment can be used as a training signal for a text LM, not just measured) in the simplest possible form: MSE loss from a linear head onto frozen fMRI/MEG targets. It also makes the first empirical gesture toward A3 (alignment may help downstream NLP) via the GLUE table, though the framing is explicitly "does not harm," not "improves."

**Counter-evidence framing (E009 design).** The Bilgin 2026 note already flags that GPT-2 *regresses* on VL-Commonsense after brain fine-tuning — sharper than the 2019 pattern of "very slightly improved or flat." This 2019 paper is the most optimistic version of the A3 story: GLUE improvements are small but positive for 11/13 tasks for MEG-transfer. Our E009 design supersedes it in rigor by adding (i) matched-perplexity control, (ii) permuted-brain twin, and (iii) robustness/OOD as the primary outcome rather than in-distribution GLUE accuracy (pirlot-2022 established that shuffled labels can replicate accuracy gains; only robustness gains require real neural structure).

**Cite as:** founding idea, weak control, superseded in rigor. Should appear in related work as the paper that opened the paradigm (brain fine-tuning does not harm NLP tasks) while explicitly noting the missing permuted-brain and matched-perplexity controls that our design addresses. The exact wording from the paper — "The fine-tuning may or may not be helping the model to perform these NLP tasks, but it clearly does not harm performance" — is the honest prior that E009 is designed to adjudicate in one direction or the other.

**Does not touch:** compression, distillation, matched student budget, anti-confound protocol (Feghhi), contiguous splits. All of these remain our contribution space.

---

## Verified

Full PDF read: yes. Downloaded via `curl` from arXiv (1911.03268v1, 18 pages), extracted with `pdftotext`, read in full including all appendix figures (A1–A8) and Table 1. No image-only pages; text extraction was clean throughout. Parse issues: none.

Read date: 2026-06-11


## Related
- [`ladder.md`](../../ladder.md) — the canonical status board
- [`map.md`](../../map.md) — code system (Q/E/A/D/L) & journey map
