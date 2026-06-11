# What Are Large Language Models Mapping to in the Brain? A Case Against Over-Reliance on Brain Scores

**Authors:** Ebrahim Feghhi*; Nima Hadidi*; Bryan Song; Idan A. Blank; Jonathan C. Kao
(* equal contribution; list order is random; in the Nature Communications 2026 published version the
author order is Hadidi first)
**Year:** 2024 (arXiv) / 2026 (Nature Communications)
**Venue:** Nature Communications 2026; arXiv preprint 2406.01538 (v2, 20 Jun 2024)
**DOI/arXiv:** arXiv:2406.01538 · NC DOI: 10.1038/s41467-026-72253-7
**Canonical ID:** hadidi-2024_case-against-brainscore-reliance

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-06-11 — full 20-page arXiv v2 PDF read page-by-page (10 main pages + 10
appendix pages A.1–A.17). All figures (1–10), all tables (1–4), and all appendix sections read.
The arXiv v2 is confirmed to be the same work as the Nature Communications 2026 paper; the author
list is identical (equal-contribution order differs between the two versions; the NC version lists
Hadidi first). No parse failures.

Comprehension self-check passed: Y

**Note on existing note:** An earlier stub (`feghhi-2024_case-against-over-reliance-brain-scores`)
exists in this directory from a pre-full-read session (2026-03-02). That note was abstract-level and
lacked all quantitative specifics. The present note supersedes it as the complete, numbers-exact
record of the same paper. The old slug should be treated as deprecated; `01-research-landscape.md`
references should migrate to this slug.

---

## Comprehension Summary [REQUIRED]

1. Problem solved: Prior brain-score literature used shuffled train-test splits and did not control
for simple non-linguistic features; this paper asks how much of GPT-2XL's reported neural
predictivity survives when those methodological holes are closed.

2. Core insight: Nearly all of trained GPT-2XL's neural predictivity on the Pereira fMRI dataset is
accounted for by sentence position (SP), sentence length (SL), and static word embeddings (WORD);
contextual features (sense disambiguation, syntax) add only a small additional margin. Untrained
GPT-2XL adds zero unique variance over SP+SL. On Fedorenko ECoG a word-position ramp explains
most of the signal. On Blank fMRI (Natural Stories), GPT-2XL predicts at chance levels.
Shuffled splits are the root methodological failure: on Pereira they flip the across-layer profile
sign (r = −0.929 with contiguous) and inflate OASM overlap to 81.5 ± 5.5%.

3. If-wrong breakage: The decomposition uses banded ridge regression with a specific feature-space
hierarchy; omitted feature spaces or nonlinear interactions could shift attribution percentages.
The authors acknowledge this as the primary limitation.

---

## Source Grounding

**Datasets.** Three re-analyses, all using the same versions as Schrimpf et al. 2021 (Nat. Acad.
Sci.):

- **Pereira fMRI**: participants visually read short passages. EXP1: 96 passages × 4 sentences,
  n = 9 participants, fMRI matrix 384 × 92450 (sentences × voxels). EXP2: 72 passages × 3–4
  sentences, n = 6, matrix 243 × 60100. Single fMRI scan (TR) per sentence. Analyses focus on
  voxels in the language network (Fedorenko 2011 localizer). Stimuli from Pereira et al. 2018
  (Nat. Commun.).

- **Fedorenko ECoG**: n = 5 participants, 52 sentences of 8 words each (416 words), 47–97
  language-responsive electrodes per participant, matrix 416 × 97.

- **Blank fMRI**: n = 5 participants listening to 8 stories from the Natural Stories Corpus. fMRI
  TR = 2 s, 1317 TRs total. 60 fROIs across all 5 participants; matrix 1317 × 60.

**Models.** Primary: GPT-2XL (~1.5B parameters, 48 layers, causal LM, absolute positional
embeddings). Secondary: RoBERTa-Large (~335M, 24 layers, masked LM). Both use learned absolute
positional embeddings. For untrained models, 10 random seeds, averaged best-layer R².

**Feature spaces (Table 1).** All feature spaces are used with banded ridge regression:

| Name | Description | Dim | Dataset |
|---|---|---|---|
| SP | Sentence position (one-hot) | 4D | Pereira |
| SL | Sentence length (number of words) | 1D | Pereira |
| WORD | Static word embeddings (LMMS/WordNet, pronoun-dereferenced, sum-pooled per sentence) | 1024D | Pereira |
| SENSE | Sense-specific word embeddings (LMMS, context-disambiguated) | 1024D | Pereira |
| SYNT | Syntactic representations (GPT-2XL averaged across 100 meaning-controlled sentences, SpaCy POS+dep) | 1600D | Pereira |
| WP | Word position (ramping positional signal + nearby-word similarity kernel, Gaussian-filtered) | 9D | Fedorenko |

**Regression.** Banded ridge regression (Dupré la Tour et al. 2022, Neuroimage 264:119728) with
L2 penalty per feature space; hyperparameters chosen by random search (1000 iterations, early
stop if R² improvement < 10⁻⁴). Out-of-sample R² ($R^2_{oos}$): defined as $1 - MSE_M / MSE_I$
relative to an intercept-only model (Hawinkel et al.). Negative $R^2_{oos}$ clipped to 0 when
averaging across voxels. **Contiguous** nested cross-validation used throughout; shuffled splits
re-run only for comparison.

**Confound metrics.** Two derived quantities:

$$\Omega_{LLM}(M) = \left(1 - \frac{R^2_{M+LLM*} - R^2_{M*}}{R^2_{LLM}}\right) \times 100\%$$

(fraction of LLM neural variance also explained by model M; clip at 100%)

$$\Phi_{LLM} = \left(\frac{R^2_{OASM+LLM*}}{R^2_{OASM}} - 1\right) \times 100\%$$

(unique LLM variance relative to OASM; negative means OASM explains more than LLM alone)

**OASM (Orthogonal Autocorrelated Sequences Model).** An n×n identity matrix Gaussian-filtered
along the diagonal within passage/sentence/story blocks, one per passage. Encodes temporal
autocorrelation without any linguistic content. OASM parameters: σ = 2.2 (Pereira), 1.8
(Fedorenko), 1.5 (Blank).

---

## Key Ideas

### Failure 1 — Shuffled train-test splits (Sections 3.1, 4.1, 5.1)

Shuffled splits allow a regressor to memorize within-passage temporal autocorrelation. On Pereira:

- The across-layer R² profile for GPT-2XL is **strongly anti-correlated** between shuffled and
  contiguous splits: r = −0.929 (EXP1), r = −0.764 (EXP2). Early/late layers look best under
  shuffled; intermediate layers (the linguistically correct answer) look best only under contiguous.
- OASM outperforms GPT-2XL on both EXP1 and EXP2 under shuffled splits (Fig. 1b).
- Fraction of GPT-2XL variance explained by OASM under shuffled: **Ω(OASM) = 81.5 ± 5.5%** (EXP1),
  **62.7 ± 4.7%** (EXP2). Unique LLM increment over OASM under shuffled: **Φ = 15.3 ± 5.5%**
  (EXP1), **37.7 ± 9.0%** (EXP2).
- On Blank (fMRI, TR=2s, highest autocorrelation): OASM achieves **103.6× higher R²** than GPT-2XL
  under shuffled splits.
- On Fedorenko: shuffled vs. contiguous are correlated (r = 0.622), but OASM still explains
  **56.8 ± 4.9%** of GPT-2XL variance; Φ = 57.8 ± 12.8% (roughly half of OASM).

**Prescribed fix:** Use contiguous splits (passages/sentences/stories never split across train/test).
All main results use contiguous splits.

### Failure 2 — Untrained GPT-2XL explained entirely by sentence length and position (Section 3.2)

Under contiguous splits, untrained GPT-2XL (10 seeds, best layer) is fully accounted for by SP+SL:

- $\Omega_{GPT2XLU}(SP+SL) = 98.4\% \pm 1.5\%$ (EXP1), **100.0% ± 0.0%** (EXP2).
- Before FDR correction: only **1.26%** (EXP1) and **0.95%** (EXP2) of voxels are significantly
  better predicted by adding GPT-2XLU to SP+SL.
- After within-participant FDR correction: **zero voxels** in either experiment are significantly
  better predicted by adding untrained GPT-2XL to SP+SL.

Mechanism: GELU nonlinearity in GPT-2's first MLP layer converts normally distributed inputs to
positive-mean outputs. When sum-pooled across tokens, this produces a length-sensitive positive
component. Absolute positional embeddings cause same-position sentences across different passages to
have similar representations.

**Implication:** The "untrained LLMs predict neural activity" finding from Schrimpf et al. 2021 and
replications is entirely explained by sentence length and sentence position — not transformer
architecture biases.

### Failure 3 — Trained GPT-2XL largely explained by SP+SL+WORD (Section 3.3)

Under contiguous splits, trained GPT-2XL on Pereira (Table 2):

| Model | EXP1 R² | EXP2 R² | Average R² |
|---|---|---|---|
| GPT-2XL alone | 0.0315 | 0.0371 | 0.0343 |
| SP+SL | 0.0134 | 0.0314 | 0.0224 |
| SP+SL+WORD | 0.0248 | 0.0395 | 0.0322 |
| SP+SL+WORD+SENSE | 0.0260 | 0.0398 | 0.0329 |
| SP+SL+WORD+SENSE+SYNT | 0.0268 | 0.0425 | 0.0347 |
| SP+SL+WORD+SENSE+SYNT+GPT-2XL | 0.0319 | 0.0449 | 0.0384 |

Key percentages (Table 3, voxel-corrected, mean ± SEM across participants):

- SP+SL accounts for **39.1 ± 7.8% (EXP1), 60.7 ± 10.2% (EXP2)** of GPT-2XL neural variance.
- Adding WORD: **81.2 ± 5.2% (EXP1), 90.1 ± 4.1%** cumulative.
- Adding SENSE: **86.2 ± 3.8% (EXP1), 92.5 ± 2.8%**.
- Adding SYNT: **89.9 ± 3.8% (EXP1), 97.8 ± 1.5%** — so the full nuisance set (SP+SL+WORD+SENSE+SYNT)
  explains essentially all of trained GPT-2XL on EXP2 and ~90% on EXP1.

SP+SL+WORD* (the simpler, no-SENSE-no-SYNT model) performs **72.3 ± 9.2%** as well as GPT-2XL in
EXP1 and **outperforms** GPT-2XL in EXP2.

**With GloVe replacing LMMS static embeddings** (Appendix A.11): results are consistent,
Ω(SP+SL+GloVe)(GPT-2XL) = 82.3 ± 6.9% (EXP1), 87.0 ± 5.2% (EXP2). Without pronoun
dereferencing: 85.4 ± 4.7% (EXP1), 90.1 ± 3.7% (EXP2). Confound is not an artifact of
transformer-based static embeddings.

**Residual contextual signal.** After accounting for SP+SL+WORD, SENSE and SYNT together add a
small but non-trivial increment: in EXP1 the joint model performs 83.6 ± 9.9% as well as GPT-2XL,
and in EXP2 78.5 ± 8.9% — the residual is real but small. GPT-2XL adds **at most 10.1% unique R²**
(EXP1: 100 − 89.9 = 10.1%) beyond the full nuisance set.

**RoBERTa-Large replication (Table 4, Appendix A.8):** Same pattern. SP+SL+WORD explains
81.4 ± 4.9% (EXP1), 86.9 ± 5.0% (EXP2). ROB performs 98.3% (EXP1) and 98.8% (EXP2) as well as
GPT-2XL in the language network.

### Failure 4 — Word-position ramp on Fedorenko (Section 4.2)

On ECoG, trained GPT-2XL is largely driven by word position within a sentence:

- WP* performs **90.8 ± 8.0%** as well as trained GPT-2XL.
- $\Omega_{GPT2XL}(WP) = 81.6 \pm 4.5\%$: word position explains 81.6% of GPT-2XL variance.
- 3 electrodes are significantly better predicted by adding GPT-2XLU to WP before FDR correction;
  none after FDR correction within participants.

### Finding 5 — Blank: GPT-2XL at chance (Section 5.1)

On the Blank Natural Stories fMRI dataset with contiguous splits:

- GPT-2XL predicts **1 fROI** significantly better than an intercept-only model before FDR
  correction; **0 fROIs** after FDR correction.
- OASM achieves 103.6× higher R² than GPT-2XL under shuffled splits — confirming Blank is the
  highest-autocorrelation-confound dataset of the three.

---

## Evidence

**Primary model:** GPT-2XL (~1.5B parameters), trained and untrained (10 seeds).
**Secondary model:** RoBERTa-Large (~335M).
**Datasets:** Pereira fMRI (EXP1: 384 × 92450; EXP2: 243 × 60100), Fedorenko ECoG (416 × 97),
Blank fMRI (1317 × 60 fROIs).
**Metric:** Out-of-sample R² ($R^2_{oos}$) with banded ridge regression, voxelwise.
**Split strategy:** Contiguous (passages/sentences/stories held out by semantic category or fold);
shuffled runs reproduced for direct comparison.

Headline numbers (all contiguous, language network, mean ± SEM):

- SP+SL+WORD accounts for ~82–90% of trained GPT-2XL neural variance (EXP1/EXP2).
- Untrained GPT-2XL: 98.4–100% accounted for by SP+SL; zero voxels significant after FDR.
- Shuffled-vs-contiguous layer correlation: r = −0.929 (EXP1), −0.764 (EXP2).
- GPT-2XL on Blank: 0 fROIs significant after FDR; OASM is 103.6× larger R².

---

## Limitations

1. **Scaling of nuisance search.** The banded ridge decomposition becomes exponentially more
   expensive as the number of feature spaces grows. The authors acknowledge potential bias when many
   feature spaces compete.

2. **Low sample sizes.** Neural data are noisy; small n means validation performance is a poor
   predictor of test performance. The banded procedure partially compensates but cannot eliminate
   this.

3. **Absence of large naturalistic fMRI.** The paper notes (Section 6) that on larger-per-participant
   datasets (e.g., LeBel 2023) the gap between simple and complex features might be substantially
   larger. Their three datasets are all sentence-presentation paradigms with low trial counts.

4. **Static embeddings are not purely non-contextual.** LMMS and GloVe embeddings are used as
   "static" baselines, but LMMS is generated from a transformer. The GloVe robustness check
   (Appendix A.11) partially addresses this; the non-pronoun-dereferenced GloVe check (85.4% / 90.1%)
   confirms the finding does not depend on the pronoun-resolution operation.

5. **No residual significance test for the trained-LLM unique increment.** The paper shows the
   residual is small (~10% EXP1) but does not provide a formal voxelwise significance test for
   whether this increment is above chance (as distinct from zero). The logic is that SP+SL+WORD is
   nearly as good, not that the LLM increment is zero.

6. **Two LLMs only (GPT-2XL, RoBERTa-Large).** Both have absolute positional embeddings; the
   sentence-position confound is partly architectural. Newer models (Llama, Qwen, with RoPE) may
   behave differently.

---

## Relevance to this thesis

**Which assumption this paper touches:** A2 (brain alignment is real and not a confound artifact).

**Role in our framework:** This is the *mandatory anti-confound protocol* paper. It defines exactly
what a credible brain-alignment result must pass, and it is the strongest single challenge to any
uncritical use of brain-score numbers — including our own.

**The five-point protocol this paper implicitly prescribes (our bar for the LeBel voxelwise run):**
1. Use **contiguous** train-test splits (passage/story-level, not TR-level random shuffle).
2. Run an OASM baseline — if OASM matches or beats the LLM, the split is contaminated.
3. Subtract SP+SL (sentence position + sentence length) as a minimum nuisance set.
4. Subtract static word embeddings (GloVe or LMMS) as the second-tier nuisance; report
   unique R² *after* this subtraction.
5. Run an **untrained** control at the same architecture; if its unique R² (after SP+SL subtraction)
   is non-zero, the method is not isolated.

**Connection to our existing evidence:**

- L003 recorded the lesson "bake the anti-confound in from day one" — this paper is the full source.
  The five-point protocol above is the operationalisation of L003.
- L007 (E002 on Tuckute real data) shows our anti-confound harness already implements points 1, 3,
  4, and 5 from the above list. The trained−untrained gap we measured (+0.030 to +0.050 unique R²,
  positive for trained, negative for untrained) is structurally consistent with this paper: untrained
  is wiped out by SP+SL; trained retains a small but real residual.
- L011 (E003, perplexity confound in KD) is a second-order instance of the same epistemology: just
  as SP+SL+WORD is the dominant explainer of raw brain scores, log-perplexity is the dominant
  explainer of raw alignment across KD conditions (r = −0.88). Both findings say: always partial out
  the obvious low-level predictor before claiming a model-specific effect.
- L012 (E004, alignment loss lever) confirms the Qwen co-trained MSE arm is brain-specific
  (+0.0032 paired vs. permuted fMRI). That is a positive result that survives the spirit of this
  paper's protocol (permuted-fMRI control is exactly point 5 above applied to the training signal).
- `feghhi-2024_case-against-over-reliance-brain-scores` (the prior abstract-only stub) referred to
  the same paper; see the note above — this file supersedes it.
- `oota-2024_speech-lms-lack-brain-semantics` adds a modality version of the same brake: raw
  alignment in speech models' late-language regions is almost entirely low-level. Together these two
  papers bound the measurement problem from two directions.
- `merlin-2026_when-lms-lose-their-mind` is the *positive* complement: alignment is load-bearing
  causally, but only after the confounds this paper identifies are controlled.
- `bilgin-2026_brain-informed-lm-training` uses TR-level random shuffling within train/val — which
  this paper says inflates estimates. Bilgin's test-set hold-out (entire Season 3) provides partial
  protection, but their validation estimates are likely upward-biased.

**Does this paper push toward (A) pursuing distillation-guided alignment, or (B) pivoting to
rate-distortion / measurement rigor?**

Neither exclusively — but it sharpens the **conditions** for (A) to be credible. The paper does
not say alignment is zero; it says the measurement protocol must close the methodological holes
before any alignment claim is trustworthy. Our E002 (L007) evidence already passed the contiguous +
untrained-control bar on Tuckute; E004 (L012) passed the permuted-BOLD bar. The Hadidi/Feghhi paper
means we must replicate on LeBel voxelwise (the predeclared powered benchmark) using all five
protocol points above before claiming the LeBel result supports A2. If LeBel passes, (A) is viable;
if LeBel fails (the residual collapses after SP+SL+GloVe subtraction on a large naturalistic
dataset), the authors' own Section 6 caveat about large datasets becomes the decisive counter-evidence
and (B) is the correct pivot.

**What changes in our design or guardrails:** The LeBel anti-confound run must explicitly include:
(a) a GloVe or equivalent static embedding nuisance block, (b) a sentence/story-position nuisance
block, (c) an OASM baseline as a split-sanity check, and (d) an untrained same-architecture control.
The existing harness has (b) and (d); (a) and (c) need to be added before treating LeBel results as
definitive.

---

## Verified

Full 20-page arXiv v2 PDF (arXiv:2406.01538) read page-by-page (pages 1–20 in two read calls).
All tables (1–4) and figures (1–10) inspected. Key numbers confirmed directly from the PDF.
The Nature Communications 2026 version (DOI 10.1038/s41467-026-72253-7) is behind a paywall and
was not separately fetched; the arXiv preprint is confirmed to be the same work.
Code is publicly available at `beyond-brainscore` on GitHub.
Read date: 2026-06-11
