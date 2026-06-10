# Revisiting the Platonic Representation Hypothesis: An Aristotelian View

**Authors:** Fabian Gröger; Shuo Wen; Maria Brbić
**Year:** 2026
**Venue:** arXiv preprint (submitted February 2026)
**DOI/arXiv:** arXiv:2602.14486
**Canonical ID:** groger-2026_aristotelian-platonic-representation

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-10 — full 20-page PDF read page-by-page including all appendices (A–F).
Comprehension self-check passed: Y

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Raw representational similarity metrics (CKA, CCA, RSA) are systematically inflated by two confounders — model width (embedding dimension relative to sample size) and model depth (max-over-layers selection inflation) — making previously reported global convergence trends in the Platonic Representation Hypothesis (Huh et al. 2024) largely artifactual.
2. Core insight: After permutation-based null-calibration that controls for both confounders, global spectral convergence (CKA) disappears with scale, but local neighborhood convergence (mutual k-NN overlap, cycle-kNN, CKNNA) remains robust and statistically significant across vision-language and video-language pairs.
3. If-wrong breakage: If local neighborhood overlap is itself a weaker signal than global spectral structure for capturing task-relevant representational content, the Aristotelian refinement would be a methodological fix without a substantive positive claim; the authors do not provide a direct test of whether local alignment predicts downstream task performance.
4. Main result location: Section 6.3 and Figures 6–7 (pp. 7–8) for the re-evaluated Platonic Representation Hypothesis; Sections 4–5 (pp. 3–6) for the theoretical confounders and calibration framework.

---

## Source Grounding

The empirical re-analysis of the Platonic Representation Hypothesis uses the WIT dataset (Wikipedia-based Image Text; Srinivasan et al. 2021) with n = 1024 image-text pairs. Three language model families are evaluated — Bloomz, OpenLLaMA, LLaMA — spanning base/large/huge scale variants. Five vision model families are evaluated — ImageNet-21K, MAE, DINOv2, CLIP, CLIP-finetuned — yielding 204 vision-language model pairs with d/n ratios in [0.75, 8]. For global similarity, linear and RBF kernel CKA are reported with max aggregation over layer pairs; for local similarity, mutual k-NN (mKNN, k = 10), cycle-kNN, and CKNNA are used. Benjamini-Hochberg FDR correction is applied across model pairs. The video-language extension (Section 6.3, Figure 7) uses the protocol of Zhu et al. (2026) with VideoMAE base/large/huge against the same language model families. Theoretical validation uses controlled synthetic experiments with n ∈ {128, 256, 512, 1024, 2048, 4096} and d ∈ {128, 256, 512, 1024, 2048}, sampling from Gaussian, Student-t (ν = 3), Laplace, and Gaussian mixture distributions (Section 6.1, Figures 3–5, Appendix F.1). The null-calibration framework uses K = 200 permutations at α = 0.05; computation requires K × L_A × L_B similarity evaluations, parallelizable across permutations (Appendix E).

---

## Core Claims

- `C1`: Raw CKA scores exhibit a systematic positive null baseline that scales as O(d/n) (Proposition 4.1), causing wider models to appear more aligned than narrower ones under pure independence (width confounder). Empirically confirmed: calibrated CKA scores collapse to zero across (n, d) configurations while raw scores drift upward (Figure 3).
- `C2`: Selection-based summaries (maximum alignment over L_A × L_B layer pairs) inflate reported similarity by O(σ√log M) where M = L_A × L_B (Proposition 4.2, Equations 5–7), making deeper models appear more convergent than shallower ones under the null (depth confounder). Calibrated aggregation removes this (Figure 5).
- `C3`: After calibration, the previously reported trend of increasing global spectral similarity (CKA) with model scale largely disappears; calibrated CKA scores show no systematic increase with language model capacity across the 204 vision-language pairs (Figure 6a).
- `C4`: After calibration, local neighborhood similarity (mKNN, cycle-kNN, CKNNA) retains statistically significant cross-modal alignment that increases with model scale; the trend holds for both image-language and video-language pairs (Figures 6b, 7).
- `C5` (Aristotelian Representation Hypothesis): Neural networks trained with different objectives on different data and modalities converge to shared *local neighborhood relationships* ("who is near whom") rather than to a globally isometric geometry ("how far apart are points").

---

## Evidence Pointers

- `C1` evidence: Proposition 4.1 (p. 3–4) proves O(d/n) null baseline for spectral metrics via Random Matrix Theory; Figure 3 (p. 6) shows empirical confirmation across Gaussian and heavy-tailed distributions; Appendix F.1 (Figure 8) extends to Laplace and Gaussian mixtures.
- `C2` evidence: Proposition 4.2 (p. 4) proves k/n null baseline for mKNN; Equations 5–7 (p. 4) derive the O(σ√log M) depth inflation; Figure 5 (p. 7) shows aggregation-aware calibration removes layer-count inflation.
- `C3` evidence: Figure 6a (p. 8), calibrated CKA-RBF vs. language model capacity — calibrated scores flat or noisy, no trend; uncalibrated scores show the upward slope originally reported by Huh et al. (2024).
- `C4` evidence: Figure 6b (p. 8), calibrated mKNN vs. language model capacity — clear increasing trend remains after calibration; Figure 7 (p. 8) replicates for VideoMAE video encoders.
- `C5` evidence: Section 6.3 interpretation (p. 7–8); further note that models converge in *which points are neighbors*, but not in pairwise distances — CKA-RBF with small bandwidth (sensitive to local distances) shows no calibrated alignment (Appendix F.9, cited p. 8).

---

## Assumptions and Limits

The calibration framework requires exchangeability of sample pairs under the null (Assumption 3.1); this is violated for grouped or sequentially structured data (e.g., fMRI time series with autocorrelation), where restricted permutations (block permutation) are needed (Appendix A). The re-analysis of the Platonic Representation Hypothesis is conducted entirely on image-text and video-text pairs; the Aristotelian claim has not been tested on brain-model alignment datasets. The paper does not test whether local neighborhood convergence is more *useful* for downstream tasks than global alignment — only that it is more methodologically robust after calibration. The theoretical proofs assume i.i.d. rows; in practice neural activations are correlated across layers, making the depth inflation bound (Proposition 4.2 / Appendix D.5) a conservative upper bound rather than an exact characterization. The paper is a preprint (February 2026) and has not yet been peer-reviewed.

---

## Interpretation Notes

This paper directly and forcefully complicates F3, the thesis framing that posits a universal geometry shared by capable LLMs and the brain that an fMRI-free surrogate (e.g., CKA to a frozen brain encoder, or an intrinsic-dimension objective) could target.

The key consequence for F3 is the local-vs-global distinction. If cross-modal convergence is only in local neighborhood structure — not in global spectral geometry — then a CKA-based surrogate trained to align an LLM's global spectral structure to a frozen brain encoder is targeting something that does not robustly generalize across model scales or architectures. CKA is precisely the kind of global spectral metric that the paper shows is confounded and, after calibration, largely non-convergent. An intrinsic-dimensionality objective (which also acts on the global spread of the representation manifold) faces the same concern. Conversely, a surrogate built on local neighborhood overlap (mKNN or topological overlap of the manifold) would be targeting the signal that does survive calibration.

This is a complication, not a refutation. A1 (brain alignment is actionable as a training signal) is untouched — the paper never tests brain data and makes no claim about whether brain-LLM alignment is real or artifactual. A2 (the alignment signal is not purely nuisance) is also untouched, since A2 depends on anti-confound controls (contiguous splits, random-brain baselines) already required by our methodology (L003), not on the metric-calibration problem this paper addresses. What the paper attacks is the specific form of the surrogate implied by the original Platonic view: a universal, globally isometric endpoint that any sufficiently capable model converges to regardless of training details.

The practical upshot: if we use CKA to a frozen brain encoder as our F3 surrogate, we should (a) use a neighborhood-based variant (mKNN, cycle-kNN, or CKNNA) rather than linear/kernel CKA, and (b) apply null-calibration at K ≥ 200 permutations when reporting alignment numbers to prevent width and depth confounders from contaminating our ablations. The calibration algorithm is published and trivial to implement (Algorithm 1, Appendix E). This is a direct design guardrail for the pilot experiment.

Relation to huh-2024_platonic-representation-hypothesis: that note records the original Platonic claim (global convergence driven by PMI-structured kernels). The present paper is a critical refinement that retains the convergence phenomenon but restricts it to local topology. The two notes should be read together; the Aristotelian view supersedes the Platonic view's specific mechanistic claim about global spectral structure.

---

## Open Questions

If local neighborhood convergence is the robust signal, does it carry sufficient gradient information to serve as a training objective in distillation? A topological loss (e.g., mKNN overlap or persistent homology) is generally non-differentiable or requires a relaxation; the original Platonic view's CKA is differentiable and widely used in distillation. The thesis needs to decide whether to use a differentiable relaxation of neighborhood overlap (e.g., soft nearest-neighbor loss) or to accept that CKA is "good enough" as a practical surrogate despite its theoretical confoundedness — and if the latter, to calibrate reported alignment numbers with permutation null so that confounder inflation does not masquerade as a distillation signal.

---

## Read Date

2026-06-10
