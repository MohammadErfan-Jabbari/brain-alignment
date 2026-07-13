---
title: "Fine-Grained Analysis of Brain-LLM Alignment through Input Attribution"
tags: [literature]
aliases: [proietti-2025_brain-llm-alignment-input-attribution]
---

# Fine-Grained Analysis of Brain-LLM Alignment through Input Attribution

**Authors:** Michela Proietti; Roberto Capobianco; Mariya Toneva
**Year:** 2025
**Venue:** arXiv preprint (submitted 14 Oct 2025; no published venue as of 2026-06-11)
**DOI/arXiv:** arXiv:2510.12355
**Canonical ID:** proietti-2025_brain-llm-alignment-input-attribution

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-11 — full PDF downloaded from arXiv and extracted with pdftotext; main paper (9 pages) + all appendices A–J (A.1–A.4 Methods; B Layer selection; C Masking sanity check; D MRH generalizability; E IG validation; F Full positional results; G Best-aligned model; H Qwen2 controls; I Short-context control; J Compute details) read in full. All figures (1–5 in main; D.1–D.3, E.1–E.2, F.1–F.5, G, H, I in appendices) inspected. No parse issues; pdftotext conversion was clean throughout.

Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Existing methods for studying brain-LLM alignment either perturb model representations or scramble input order globally — both are coarse. This paper asks which specific individual input words drive brain alignment (BA) vs. next-word prediction (NWP), enabling a fine-grained comparison of the two tasks.

2. Core insight: An end-to-end gradient-based attribution pipeline (Gradient × Input, validated with Integrated Gradients) threads through the LLM → ridge encoding model → MSE-vs-fMRI loss, producing word-level importance scores for BA. Contrasting these scores with NWP (cross-entropy loss) attributions across five architectures and two fMRI datasets shows that BA and NWP rely on "largely distinct word subsets" at strict thresholds (IoU ≈ 0.16 at top-10%), with systematic differences in feature type (BA: semantic + discourse; NWP: syntactic) and positional bias (NWP: sharp recency + primacy; BA: broader, focused recency only).

3. If-wrong breakage: If gradient-based attributions are unreliable for the BA pipeline (local nonlinearities, vanishing gradients through the ridge regressor), the claimed divergence could be an attribution-method artifact rather than a property of the tasks. The IG cross-check on two models partially mitigates this, but a perturbation-based replication across the full model set was not run.

---

## Source Grounding

**Brain datasets.**

- **Harry Potter (HP):** Wehbe et al. 2014. 8 subjects reading Chapter 9 of Harry Potter and the Sorcerer's Stone word-by-word (0.5 s per word). 5,176 words. fMRI TR = 2 s. Four runs of similar length. 4-fold cross-validation (runs). Primary dataset; also carries word-level linguistic annotations (semantic: 100-dim co-occurrence vectors; syntactic: 45-dim POS+dependency vectors; discourse: 27-dim feature vector encoding verbs, speech, motion, emotion, character identity).

- **Moth Radio Hour (MRH):** Deniz et al. 2019. 9 subjects reading 10 autobiographical stories (10–15 min each). One repeated story serves as validation. Word presentation rate equals the spoken word's duration. TR = 2.0045 s. Two 3-hour scanning sessions on different days. 11-fold cross-validation (one story per fold). Used only for generalizability replication; no linguistic annotations.

**Models (Table 1).** Five pretrained LLMs at 1–2B parameters, all frozen during attribution (no fine-tuning for BA). Hidden size = 2048 across all five.

| Name | Params | Layers | Architecture | Context |
|---|---|---|---|---|
| Falcon3-1B | ~1B | 18 | Transformer (RoPE, GQA) | 4K |
| Gemma-2B | ~2B | 18 | Transformer (RoPE, MQA) | 8K |
| Llama3.2-1B | ~1B | 16 | Transformer (RoPE, GQA) | 128K |
| Mamba-1.4B | ~1.4B | 48 | Pure SSM | 2K |
| Zamba2-1.2B | ~1.2B | 38 | Hybrid SSM+Attention | 4K |

**Encoding model.** For each layer of each model, a ridge-regularized linear regressor maps LLM TR-level activations (input shape: K × 4H, concatenating 4 previous TR embeddings to account for hemodynamic delay, context L = 640 words) to fMRI voxel activity. Hyperparameter selected via nested cross-validation following Jain & Huth 2018 and Schrimpf et al. 2021. Cross-validation folds: 4-fold (HP runs), 11-fold (MRH stories). Brain alignment metric: Pearson correlation between predicted and actual voxel activity.

**Attribution method.** Gradient × Input (GXI; Shrikumar et al. 2016) as primary method; Integrated Gradients (IG; Sundararajan et al. 2017, m=20 interpolation steps, zero-embedding baseline) as validation on two models (Llama3.2-1B, Gemma-2B). GXI score: $\mathrm{GXI}(x_i) = \frac{\partial F(x)}{\partial x_i} \cdot x_i$. Token-level scores summed to word-level. For BA: gradient taken with respect to MSE loss between predicted and actual voxel activity. For NWP: gradient taken with respect to mean cross-entropy loss over sub-word tokens of the next word (teacher forcing).

**Evaluation metrics.** IoU (Jaccard similarity) between the sets of "important words" for BA and NWP, where the set is defined as the smallest word subset whose cumulative attribution reaches threshold t%. Reported for t = 1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98%. Center of Mass (CoM) captures mean position of attributed words in context (0 = most recent word, 640+ = furthest). AUC of the unique-word-count vs. t curve (attribution spread). Statistical tests: two-sided paired t-test with Benjamini-Hochberg FDR correction on AUC differences.

---

## Key Ideas

### The precise claim about distinct word subsets

Section 4, Results, paragraph "Low overlap between top-attributed words for BA and NWP" (p.6), verbatim:

> "BA and NWP rely on largely distinct subsets of input words."

More precisely: "At low thresholds (t ≤ 10%), the overlap is minimal (IoU ≈ 0.1–0.2), suggesting that the two tasks rely on distinct subsets of important words. As t increases, IoU gradually rises, eventually exceeding 0.8 at t = 98%."

And from the abstract: "BA and NWP rely on largely distinct word subsets: NWP exhibits recency and primacy biases with a focus on syntax, while BA prioritizes semantic and discourse-level information with a more targeted recency effect."

This is a claim about **input attribution** — specifically, which input context words receive the highest gradient-times-input score when optimizing either (a) MSE between predicted and actual fMRI voxels or (b) next-word cross-entropy loss, given the same frozen LLM representations. It is NOT a claim about which features live in the LLM's weight space, nor about which tokens are structurally necessary for the mapping. The granularity is **word-level** (token-level GXI scores summed per word). The comparison is made at the level of the 640-word input context window, not across the full document.

### Attribution spread differences across layers

Section 4, paragraph "BA and NWP have opposing trends of attribution spread" (p.7):

- **Early layers**: NWP requires significantly more unique words than BA to reach threshold t (NWP AUC > BA AUC; p < 0.001, BH-corrected). Interpretation: NWP at early layers relies on many local word-level cues; BA is more concentrated.
- **Middle and late layers**: BA AUC exceeds NWP AUC (p < 0.001, BH-corrected). Interpretation: BA draws on increasingly distributed semantic/discourse representations that emerge deeper in the model.
- AUC trend: BA AUC increases steadily from early to late layers; NWP AUC decreases. These patterns replicate on MRH (Appendix D.2).

### Linguistic feature analysis (HP dataset only)

Section 4, paragraph "NWP relies heavily on syntax, while BA also draws on semantics and discourse" (pp.7–8) with Figure 4 at t = 10%, 60%, 80%:

At t = 10%: NWP shows a "clear bias toward syntactic features"; BA shows a "more balanced distribution" emphasizing semantic and discourse-level content alongside syntax.

At t = 60%: BA marks ~33% of semantic feature words as important; NWP marks ~20% (~7% uniquely, ~13% jointly). BA uniquely covers more semantic and discourse-level content than NWP. Syntactic features are important for both tasks (Oota et al. 2023b).

The discourse and semantic advantage of BA vs. NWP holds across all three thresholds. Results validated with IG (Appendix E.1) — not an attribution-method artifact.

### Positional biases

Section 4, paragraph "Fine-grained attribution reveals positional biases" (pp.8–9) with Figure 5:

- **NWP**: Consistent sharp bimodal distribution — pronounced peak at end of context (recency) and secondary peak at beginning (primacy). Holds across all five architectures (including SSM Mamba-1.4B).
- **BA**: Broader, more focused recency peak; minimal primacy bias. BA CoM is slightly closer to the most recent word than NWP CoM in most models, but the spread is wider. Results hold for MRH (Appendix D.3), except Llama3.2-1B's oscillatory pattern (stimulus-dependent, not architectural — disappears at shorter context lengths and on MRH; see Appendix I).

### Sanity checks

Appendix C: Masking the top 1% of attributed words "virtually abolishes predictive power" for both tasks: NWP cross-entropy loss more than doubles; BA Pearson correlation drops ~100% across language-selective ROIs. This confirms attribution scores capture meaningful signal, not noise.

Appendix E.2: IG replicates GXI patterns for Llama3.2-1B and Gemma-2B positional distributions — the oscillatory Llama pattern is not a GXI artifact.

---

## Evidence

**Models:** Five pretrained 1–2B-parameter LLMs (Falcon3-1B, Gemma-2B, Llama3.2-1B, Mamba-1.4B, Zamba2-1.2B). All frozen; no alignment fine-tuning.

**Datasets:** Harry Potter fMRI (8 subjects, 5,176 words, TR=2s, 4-fold CV); Moth Radio Hour fMRI (9 subjects, 10 stories, TR=2.0045s, 11-fold CV).

**Headline numbers (HP, averaged across models, layers, subjects, contexts):**

- IoU at t=10%: ≈ 0.16 (random baseline ≈ 0; stated as "essentially zero" at t < 10%)
- IoU at t=60%–80%: 1.5–2× above chance
- IoU at t=98%: > 0.80
- AUC shift across layers: statistically significant (p < 0.001, BH-corrected) for both early-layer NWP > BA and mid/late-layer BA > NWP
- Top-1% masking: NWP cross-entropy doubles; BA Pearson correlation drops ~100%

All patterns replicate on MRH (Appendix D).

---

## Limitations

1. **Attribution method reliability.** GXI computes local first-order gradient information; for deep nonlinear models with the ridge regressor bottleneck, the gradient path may be noisy or saturated. IG was only run on two of five models, and only for positional and linguistic comparisons — not for the full IoU analysis. No perturbation-based (occlusion/LIME) cross-check was performed on the full model set.

2. **Frozen models only.** Attributions reflect the inductive biases of pretrained models; they do not reflect what a brain-alignment-fine-tuned model (e.g., Brain Tuned from [Merlin 2026](merlin-2026_when-lms-lose-their-mind.md)) would rely on. The finding is about the passive structure of the mapping, not about an optimized objective.

3. **No anti-confound controls per Hadidi/Feghhi 2026.** The study uses contiguous folds (4-fold by runs for HP; 11-fold by story for MRH), which satisfies the basic temporal-leakage requirement. However, there is no explicit subtraction of sentence-position, sentence-length, or static word-embedding nuisance variables from the brain alignment measure used as the attribution target. The claim that BA reflects semantic/discourse content is observational; the alternative — that the BA attribution patterns trace word-level features that happen to be semantic by coincidence (e.g., content words are longer and at less predictable positions) — is not ruled out by a formal nuisance decomposition.

4. **Small model scale.** All five models are 1–2B parameters. The generalization of the BA-vs-NWP attribution divergence to larger models (7B+, instruction-tuned models) is noted as future work in the Discussion.

5. **Discourse annotations are coarse.** The HP discourse annotation (27-dim vector for verbs, speech, motion, emotion, character name) is a rough proxy for discourse-level processing. The finding that BA draws more on discourse-level words than NWP does is sensitive to this annotation quality.

6. **No significance test on IoU values directly.** The paper reports the random baseline (≈0 at t<10%) and shows observed IoU = 0.16–0.2 as "above chance," but no formal statistical test of the IoU difference from baseline is provided (only AUC spread comparisons have formal tests). The IoU claim rests on visual comparison with the random baseline curve.

7. **Preprint only.** The paper was posted October 2025 and has not (as of June 2026) been published in a peer-reviewed venue.

---

## Relevance to this thesis

**Which assumption this touches:** A1 (brain alignment carries information beyond perplexity/NWP that is actionable) and — more indirectly — A2 (measured alignment is not purely a nuisance artifact).

**Role in our framework:** This is the mechanistic support paper for our "beyond perplexity" framing. The claim we had been using without a grounded citation — that brain alignment and next-word prediction rely on distinct input subsets — is the paper's central finding, and the attribution evidence for it is real and methodologically sound at the level of showing divergent gradient signals. The paper supports the claim that *what the brain alignment loss responds to is not the same input features as cross-entropy loss*, which is exactly the mechanistic story for why adding $\mathcal{L}_\text{brain}$ in KD recovers alignment that perplexity-only KD does not.

**Verdict on whether it says what we attributed to it:** YES, but with important qualification. The citation is directionally correct: the paper provides the most direct mechanistic evidence that brain alignment and next-word prediction draw on different input-level information. However, the evidence is gradient-based attribution on frozen models — it is a characterization of the difference in information use, not a causal test or a guarantee that the difference is exploitable under compression. The paper does not show that optimizing for BA during distillation will recover distinctly BA-relevant information; it shows that a frozen model's BA mapping draws on different input words than its NWP head. That is a necessary but not sufficient mechanistic account for our E005 result.

**Connection to E005 / L014 / L015:**

The Proietti et al. finding offers a plausible mechanism for the E005 F1 result (alignment-guided KD recovers +0.0081 brain-specific alignment at matched perplexity). If BA and NWP gradients point at different input subsets, a student trained only on KL/cross-entropy divergence will optimize the NWP-relevant information but not the BA-relevant information, leaving an exploitable gap — exactly what the co-trained MSE brain loss fills. This is the "beyond perplexity" mechanism. However, L015 (honest re-analysis of E005) shows the in-domain effect is borderline (fold-level t-CI includes 0, one outlier fold carries 52%), so we should cite Proietti et al. as the motivating mechanism for the BA-NWP divergence hypothesis, not as confirmation that the exploitation of that divergence is robust.

**Anti-confound bar (Hadidi/Feghhi 2026 standard):** Proietti et al. do NOT meet the full Hadidi/Feghhi anti-confound bar. They use contiguous splits (pass), but they do not subtract SP+SL+static-word-embeddings from the alignment measure before running attributions. This means the "BA-important words are semantic/discourse" finding is observational and could partly reflect that semantic/discourse words are content words that also happen to be less predictable and longer. For our purposes, this is not a critical flaw — the attribution method measures the gradient-level difference, not a variance-partitioning — but it means we should not quote this paper as evidence that the BA alignment measure itself is clean of nuisance (that case requires Hadidi/Feghhi + our own E006 controls). What we can say is: given the alignment measure as-is, the information BA relies on from the input is attributively distinct from what NWP relies on.

**What this changes in our design or guardrails:**

- The citation is now grounded. We can use Proietti et al. (arXiv:2510.12355) as the specific reference for "brain alignment and next-word prediction draw on distinct input word subsets (Proietti et al. 2025)" in the mechanism paragraph of the thesis.
- Do NOT upgrade this citation to "brain alignment is causally independent of NWP" — that would require [Merlin 2024](merlin-2024_beyond-next-word-brain-alignment.md) (residual alignment after controlling NWP) and Merlin 2026 (causal gradient reversal).
- The finding that the divergence is larger at middle and late layers (BA AUC > NWP AUC in mid/late) matches the theoretical motivation for using middle-layer representations in our encoding model — and is worth citing in the layer-selection rationale.
- No change to the experimental design is required; the paper is supporting motivation, not a procedure we need to replicate.

**Lean-on verdict:** Moderate. The paper delivers exactly the mechanistic claim we cited it for — BA and NWP draw on different input-level information — and the finding is robust across five architectures and two datasets with IG cross-validation. The limitation is that it is gradient-based attribution on frozen models (not a causal test), the anti-confound bar is lower than Hadidi/Feghhi, and the paper is a preprint. Cite as mechanistic motivation, not as proof.

---

## Verified

Full PDF extracted with pdftotext from arXiv:2510.12355v1 PDF (5.9 MB, downloaded 2026-06-11). Main paper pages 1–9 read in full. Appendices A (Methods: A.1 dataset details, A.2 model descriptions, A.3 attribution formulas, A.4 brain activity prediction pipeline), B (layer selection), C (masking sanity check), D (MRH replication: D.1 IoU, D.2 spread, D.3 positional), E (IG validation: E.1 linguistic features, E.2 positional patterns), F (full positional results: F.1 t=10% CoM, F.2–F.5 per-model distributions), G (best-aligned model), H (Qwen2-1.5B control), I (short-context Llama oscillation control), J (compute details) all read. No parse failures; text extraction was clean. Key numbers (IoU ≈ 0.16 at t=10%, IoU > 0.80 at t=98%, AUC significance p < 0.001 BH-corrected) confirmed directly from text. Code at https://github.com/michelaproietti/Brain-LLM-Alignment-Attribution.

Read date: 2026-06-11


## Related
- [`status.md`](../../status.md) — the canonical status board
