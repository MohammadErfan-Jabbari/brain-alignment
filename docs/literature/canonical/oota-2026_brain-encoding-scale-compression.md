# Linguistic properties and model scale in brain encoding: from small to compressed language models

**Authors:** Subba Reddy Oota; Vijay Rowtula; Satya Sai Srinath Namburi; Khushbu Pahwa; Anant Khandelwal; Manish Gupta; Tanmoy Chakraborty; Bapi S. Raju
**Year:** 2026
**Venue:** arXiv preprint (q-bio.NC), submitted 7 Feb 2026
**DOI/arXiv:** arXiv:2602.07547
**Canonical ID:** oota-2026_brain-encoding-scale-compression

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 20-page PDF plus appendices A–O read directly from disk (pages 1–20). All core results, tables, and figures confirmed from the PDF. Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: How much model capacity is actually required for brain alignment, and does post-training compression (quantization, pruning) destroy or preserve the brain-relevant representational geometry that emerges with scale?
2. Core insight: Brain alignment saturates at ~3B parameters across three model families; ~1–1.5B remains consistently under the threshold; most quantization methods (AWQ, SmoothQuant) and moderate pruning (≤25%) preserve brain alignment near the uncompressed baseline, with GPTQ as the consistent exception; a dissociation is observed between linguistic benchmark performance and brain predictivity under compression.
3. If-wrong breakage: If the encoding pipeline uses shuffled rather than temporally contiguous train/test splits, autocorrelation inflates all scores and the saturation/compression claims collapse; the paper does not specify split type explicitly, which is a validity risk flagged below.

---

## Source Grounding

**Dataset.** Publicly available Subset-Moth-Radio-Hour fMRI dataset (Deniz et al. 2019). Nine participants listened to 11 naturalistic stories (10–15 min each) from The Moth Radio Hour. 3,737 training TRs, 291 test TRs (one held-out story). Stimuli aligned to transcripts via force alignment; word representations downsampled to TR rate (2.0045 s) with a 3-lobed Lanczos filter. HRF modeled with a finite-impulse-response filter per voxel, 4 temporal delays (≈8 s). 180 ROIs per hemisphere (Glasser Atlas multi-modal parcellation). Language ROIs include AG, ATL, PTL, IFG, IFGOrb, MFG, PCC, dmPFC. A supplementary reading fMRI condition (same participants, same dataset, different task) is used for generalization checks.

**Models.** Three families: Qwen2.5 (1.5B, 3B, 7B, 14B), LLaMA-3.2 (1B, 3B, 7B, 14B), DeepSeek-R1 (1B, 3B, 7B, 14B). All are base (non-instruction-tuned) checkpoints. Representations extracted from all transformer layers; best-performing layer per model used for reporting.

**Compression methods tested.**
- Post-training quantization: AWQ (activation-aware weight quantization, INT4/INT8), GPTQ (gradient-guided weight quantization, INT4/INT8), SmoothQuant (joint weight-activation quantization).
- Unstructured magnitude pruning: 10%, 25%, 50% sparsity (L1-norm smallest weights removed from all linear layers, no retraining).
- Knowledge distillation is NOT tested. The paper explicitly lists KD as a gap in its limitations section ("A broader comparison with other compression strategies, such as structured pruning or knowledge distillation, would further clarify how different efficiency interventions affect neural representations").

**Alignment metric.** Bootstrap ridge regression (Tikhonov regularization, λ ∈ [10, 1000], chosen by cross-validation on a 10% random subset of the training split). Normalized brain alignment = Pearson r(predicted voxel activity, observed voxel activity) divided by estimated cross-subject prediction accuracy ceiling (noise ceiling). Restricted to voxels with ceiling ≥ 0.05. Statistical significance via block permutation test (blocks of 10 contiguous TRs, 5000 permutations) and Wilcoxon signed-rank test across subjects.

**Split methodology.** The paper uses 10 stories for training and 1 held-out story for testing (temporal contiguity preserved within each story). The block permutation test explicitly uses contiguous TR blocks, indicating awareness of autocorrelation. However, the 10% hyperparameter-tuning subset is drawn randomly from the training split rather than being held out contiguously — a minor but non-zero risk.

**Linguistic probing.** FlashHolmes benchmark (Waldis et al. 2024): 66 linguistic tasks across morphology (19), syntax (75 subtasks collapsed), semantics (67), discourse (28), and reasoning (19). Linear classifier probing applied to hidden states from all tested models and compressed variants.

---

## Core Claims

- `C1`: Brain alignment saturates at ~3B parameters. 3B SLMs match 7B–14B LLMs in normalized brain predictivity across whole brain and all major language ROIs. Paired t-test (Qwen2.5, n=9 subjects): 3B vs 14B: Δ = 0.000, t(8) = −0.03, p = 1.0 (no difference). 3B vs 1.5B: Δ = 0.07, t(8) = 4.89, p = 0.004 (clear, significant). 1.5B is reliably below the saturation regime.
- `C2`: Post-training compression mostly preserves brain alignment for 3B+ models. Qwen2.5-3B normalized alignment (IFG, Table 5): FP16 baseline 0.924 ± 0.033; AWQ 0.933 ± 0.035; GPTQ 0.910 ± 0.037; SmoothQuant 0.930 ± 0.035. AWQ and SmoothQuant do not differ significantly from FP16 (p > 0.05 after correction); GPTQ is significantly worse (Δ = −0.020 vs 7B baseline, t(8) = 6.20, p < 0.001; Table 4). For 1B–1.5B models, all quantization methods yield significant alignment drops (p < 0.01).
- `C3`: Unstructured pruning preserves brain alignment at moderate sparsity. Qwen2.5-3B at 10% sparsity: 0.910 ± 0.032; 25%: 0.908 ± 0.033; 50%: 0.907 ± 0.043 — all within error of FP16 baseline. Degradation becomes marked only at 50% for smaller (1B–1.5B) models.
- `C4`: Linguistic competence and brain alignment dissociate under compression. GPTQ degrades discourse, reasoning, and morphology probing scores AND reduces brain alignment. AWQ/SmoothQuant degrade discourse/syntax FlashHolmes scores but do not reduce brain alignment. 1B–1.5B models maintain FlashHolmes task performance yet show marked brain alignment deficits, showing the dissociation runs in both directions.

---

## Evidence Pointers

- `C1` evidence: Fig. 2 (p. 6) whole-brain and IFG normalized alignment bar charts across all three model families; Table 2 (p. 7) pairwise paired t-test statistics for Qwen2.5; Tables 9–10 in Appendix I for LLaMA-3.2 and DeepSeek-R1 showing same qualitative pattern; reading fMRI replication in Appendix L.
- `C2` evidence: Fig. 3 (p. 8) Qwen2.5 IFG quantization comparison; Table 4 (p. 7) pairwise quantization significance tests for Qwen2.5-7B and 3B; Table 5 (p. 9) full quantization+pruning numbers for Qwen2.5-3B; Fig. 4 (p. 9) voxelwise percentage-change maps.
- `C3` evidence: Table 5 (p. 9) pruning rows; Appendix N (pruning effect for 1.5B models).
- `C4` evidence: Fig. 5 (p. 10) scatter of FlashHolmes task score vs normalized brain alignment across compression methods and scale; Tables 7–8 (Appendix H) linguistic probing breakdown by category.
- Decoding evidence: Table 3 (p. 7) brain-to-text reconstruction metrics for LLaMA-3.2 models: LLaMA-3.2-3B achieves BLEU-1 = 0.120, WER = 4.22, METEOR = 0.110, BERT-F1 = 0.825; LLaMA-3.2-8B: BLEU-1 = 0.070, WER = 5.78, METEOR = 0.055, BERT-F1 = 0.811; LLaMA-3.2-1B: BLEU-1 = 0.110, WER = 4.49, METEOR = 0.099, BERT-F1 = 0.824.

---

## Assumptions and Limits

No knowledge distillation is tested. All compression is post-hoc (no retraining, no fine-tuning after compression). The paper does not test alignment-guided compression at any level — alignment is always the dependent variable, never the training objective. The paper never constructs a matched-compute or matched-budget comparison between distilled SLMs and quantized SLMs; it compares families and sizes as they exist off the shelf.

The 10% hyperparameter-tuning subset is drawn randomly from the training stories rather than held out contiguously, introducing a mild autocorrelation risk for the regularization selection step, though the main train/test split respects temporal continuity at the story level.

Only text-based fMRI (listening and reading) from nine English-speaking participants is used; results may not generalize to other languages, populations, or non-narrative stimuli. The paper caps model size at 14B; whether the saturation claim holds against 70B+ models is explicitly listed as future work. All compression methods are standard post-training variants; structured pruning and KD are absent.

Linguistic probing uses linear classifiers, capturing accessible but not necessarily causally relevant features. The FlashHolmes benchmark measures model behavior, not internal representations directly, which can mask representational changes that do not affect task accuracy.

---

## Interpretation Notes

This paper is the primary counter-evidence candidate for framing F1 (alignment-guided distillation at matched budget). The relevant question is precise: does it show that alignment is preserved by KD (knowledge distillation), or only by quantization/pruning?

The answer is clear: the paper tests only post-hoc quantization (AWQ, GPTQ, SmoothQuant) and unstructured pruning. Knowledge distillation is explicitly absent, and the authors call it out themselves as a limitation. This is the decisive gap for the thesis.

The threat to F1 runs as follows: if brain alignment is robust to compression by default (as this paper shows for most quantization methods), then "protecting alignment during compression" is solving a problem that doesn't exist — at least for the quantization-and-pruning regime. The strongest version of this threat is: 3B SLMs already sit on the saturation plateau; compressing a 3B model with AWQ barely moves alignment; so the alignment you would be "protecting" was never in danger.

However, F1 is not refuted. The paper leaves the following room open:

1. KD is not tested. A student trained by logit/attention imitation from a 7B+ teacher might not land at the same representational geometry as the 7B compressed via quantization. The saturation plateau is a scale fact, not a distillation fact.
2. The paper never asks whether using alignment as a distillation objective improves utility (NLP task performance, downstream accuracy) at a matched parameter count. It measures alignment as a readout, never as a signal. The trade-off curve between alignment and utility during distillation — which is the specific object F1 proposes to optimize — is simply not addressed.
3. The GPTQ exception shows alignment is not universally preserved: a commonly used quantization method meaningfully degrades semantic region alignment. Under distillation, where the loss surface is shaped by imitation objectives that may not preserve representational geometry, similar or larger degradation is plausible.
4. The dissociation result (C4) cuts both ways for F1: it shows that linguistic competence and brain alignment can come apart, which means optimizing task performance during distillation does not guarantee alignment preservation — precisely the motivation for monitoring alignment explicitly.

Verdict on R03's claim: OVERSTATED. R03 says "post-hoc compression already preserves alignment by default, so 'protect alignment during compression' may be solving a non-problem." This is overstated because (a) the paper covers only quantization and magnitude pruning, not KD, and the authors say so explicitly; (b) GPTQ shows non-trivial degradation, proving the "by default" qualifier is method-dependent; (c) for small models (1B–1.5B), nearly all compression methods hurt alignment. The claim is accurate for the specific regime of AWQ/SmoothQuant applied to ≥3B models, but that regime is not the same as distillation at matched budget. R03 should qualify: "post-hoc quantization (AWQ, SmoothQuant) of ≥3B models largely preserves alignment by default; this does not extend to KD, to smaller scales, or to GPTQ."

---

## Open Questions

The decisive open question for the thesis: does a student trained by standard KD (logit imitation + attention transfer) from a 7–14B teacher land at a different point on the alignment–utility plane than a 3B model quantized with AWQ to comparable inference cost? If KD-trained students inherit the teacher's representational geometry, the thesis framing is partially pre-empted. If they do not — which is likely given that distillation reshapes hidden states via imitation losses not designed to preserve brain-relevant structure — the trade-off curve is real and alignment-guided distillation is meaningful.

---

## Read Date

2026-06-10
