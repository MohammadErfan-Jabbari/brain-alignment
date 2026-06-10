# 06 — Theory grounding: the Information-Theory and Probabilistic-ML course as a source of truth

**Created:** 2026-06-10 (Session 5 — analysis). **Status:** living index. **Full width, no hard wrap.**

## What this is, and why it exists

This repo has three kinds of external source feeding the thesis: the **papers** (canonical notes in `literature/canonical/`, the frontier map in `01-research-landscape.md`), the **datasets** (`04-data-benchmarks.md`, `05-dataset-registry.md`), and — added here — Erfan's **master's coursework** in Information Theory for ML and Probabilistic ML (UC3M, 2025–26). The coursework is the *theoretical grounding* layer: it is where the math the thesis keeps invoking informally (the information budget, the weak-prior bound, the unique-variance metric, the compression trade-off) has its exact, proved, textbook-faithful form. This file is the map from that coursework to the thesis, so a future session can cite the right result instead of re-deriving it from scratch or guessing the constant.

The material lives under `data/course-material/` (gitignored — see "How it is stored" below). It is **already preprocessed** to a high standard, so the job of any future session is to *use* it, not to re-extract it.

## How it is stored, and the one decision that matters (no re-OCR)

The raw material is 125 files, ≈ 292 MB, in two folders plus a reference book:

- `data/course-material/info-theory-course/` — 26 lecture slide decks (PDF) + Erfan's own notes: **24 `*_study.md`** (polished teaching notes, flowing prose + faithful LaTeX + worked examples + failure-mode sections) and **9 `*_OCR.md`** (clean, audit-corrected formula reconstructions of the slides).
- `data/course-material/prob-ml-course/` — 8 numbered topic blocks; lecture-note PDFs **and** the research-paper readings, with **`*_study.md` / `*_overview.md` / `*_Study_Guide.md` / `BLOCK*_EXAM_PREP.md`** notes for most blocks.
- `data/course-material/Preview_of_the_book.pdf` — *Network Information Theory*, El Gamal & Kim (reference text).

**The preprocessing decision (Session 5):** do **not** run a PDF/OCR skill on the lecture decks. The slide PDFs are sparse and image-heavy (≈ 700–1100 characters of embedded text over three pages); the existing `*_study.md` / `*_OCR.md` notes are *higher quality* than anything a fresh OCR pass would produce, because they were written by a dedicated `course-lecture-study` workflow with grounding-first prose and a human-audited formula pass. So the markdown notes **are** the usable text; the PDFs are kept only as the source-of-record. The only material with no notes is a handful of paper PDFs (see "Gaps"), and those belong in the repo's existing `paper-digest` pipeline if and when they become load-bearing — not a generic OCR.

**Git tracking (D014):** the notes are left under gitignored `data/` (not version-controlled with the thesis); canonical copies live in Erfan's `~/uni/` workspace, and this committed index is the durable, portable record. If portability of the notes themselves ever matters, un-ignore `*.md` under `data/course-material/` — the text is < 1 MB.

## How to use this file

- When a thesis claim needs a **formal bound, definition, or theorem**, look it up in the map below and cite the course note by filename. Do not re-derive a result the course already proves; do not invent a constant the course already fixes.
- The map separates **load-bearing** connections (the math the thesis argument actually rests on) from **adjacent** ones (thematically related, not currently used). Spend rigor on the load-bearing rows.
- This is an *analysis-session* resource: it reads and organizes existing material. It never produces an experimental number. Numbers come from `experiments/`.

---

## The load-bearing map (the math the thesis rests on)

These five connections are the ones R03's argument actually depends on. Each row gives the course result, its exact statement, the note it lives in, and the precise thesis claim it grounds.

### 1. The mutual-information generalization bound — the formal twin of R03's "weak prior" bound

The course proves (lecture 26, via Donsker-Varadhan + sub-Gaussian concentration) that for a learning algorithm modelled as a channel $P_{W\mid Z^n}$ from the training set $Z^n$ to the learned parameters $W$, with $\sigma$-sub-Gaussian loss, the *average* generalization gap obeys

$$
\overline{\operatorname{gen}} \;=\; L - \widehat{L} \;\le\; \sqrt{\frac{2\sigma^2\, I(W;Z^n)}{n}},
$$

and the bounded-loss variant $d(\widehat{L}\,\|\,L) \le I(W;Z^n)/n$ (file: `info-theory-course/26_generalization_error_bounds_OCR.md`). **This is the exact in-expectation form of the bound R03 §2 Step 6 invokes through its PAC-Bayes (McAllester) face.** Both descend from the *same* Donsker-Varadhan variational representation of KL that the course derives in lecture 5 and reuses in lecture 26 — PAC-Bayes is the high-probability form, the MI bound is the in-expectation form. The thesis consequence is direct: the brain term enters training as a weak prior, so its entire contribution to *generalization* is mediated by how much it changes $I(W;Z^n)$. If the brain prior adds only $\Delta I$ bits to the algorithm's input-output mutual information, the generalization benefit is bounded by $O(\sqrt{\Delta I / n})$ — which is *why* the benefit is real but small, and *why* it decays as task data $n$ grows. R03's order-of-magnitude "info budget" (Steps 2–4) is the estimate of that $\Delta I$.

### 2. The data-processing inequality — the ceiling on alignment, and the answer to the compression counter-paper

The course states and proves (lecture 6) that for a Markov chain $X \to Y \to Z$,

$$
I(X;Y) \;\ge\; I(X;Z),
$$

and — crucially — its own "deployment reading" is *exactly* the thesis's compression argument (file: `info-theory-course/6_10022026_DPI_SourceCodingI_study.md`): "If you train a representation $Z$ from features $Y$ that were themselves derived from raw data $X$, then $I(Z;\text{label}) \le I(Y;\text{label})$." Map $X \to$ stimulus, $Y \to$ teacher LM features, $Z \to$ compressed student representation, label $\to$ brain activation $B$: then $I(Z_{\text{student}}; B) \le I(Y_{\text{teacher}}; B)$. **Compression can only lose brain alignment, never create it.** This is the formal grounding for two R03 claims at once: (a) §2 Step 4's "$I(\theta^\star;Y) \le I(\theta^\star;S)$ — most of the brain signal is already in the text," and (b) §2's third brake — the compression-preserves-alignment counter-evidence (arXiv 2602.07547). The counter-paper's empirical finding that alignment survives compression means the DPI bound is *nearly tight* in practice (compression is near-alignment-lossless), which is precisely why the thesis must compete on the **trade-off curve** (how favorably alignment trades against rate), not on a preserve-vs-destroy binary.

### 3. Conditional mutual information — the formal definition of "unique R² beyond confounds"

The course defines (lecture 4) conditional mutual information

$$
I(X;Y \mid Z) \;=\; H(Y\mid Z) - H(Y\mid X,Z),
$$

as the dependence between $X$ and $Y$ that *remains after the context $Z$ is already known* (file: `info-theory-course/4_03022026_RelativeEntropy_MI_Jensen_study.md`). **The thesis's "unique variance after nuisance subtraction" is this object:** with $X \to$ LM features, $Y \to$ brain activation, $Z \to$ nuisance regressors (length, position, static embeddings), the quantity the encoding model is after is $I(\text{LM};\,B \mid \text{nuisance})$. The contiguous-split, nuisance-baseline anti-confound protocol (learnings L003; R01 §2/§4) is the empirical, ridge-regression operationalization of conditioning on $Z$. This is why "unique R²" is not an arbitrary convention but the right information-theoretic target.

### 4. The rate-distortion function — the formal object behind the F1 "trade-off curve"

The course gives (lecture 1) the rate-distortion function

$$
R(D) \;=\; \min_{P_{\hat S\mid S}:\,\mathbb{E}[(S-\hat S)^2]\le D}\; I(S;\hat S),
$$

the minimum rate achievable at a given distortion budget (file: `info-theory-course/1_InfTh_Intro_study.md`, Chunk 2). **F1 (alignment-guided distillation at matched budget) is literally a rate-distortion claim:** a compressed student sits at an operating point where *rate* is the student's budget (params / FLOPs) and *distortion* is alignment loss relative to the teacher. The thesis's contribution is to show brain-guided distillation moves the operating point favorably — lower alignment-distortion at the same rate. Lecture 1's Chunk 3 explicitly notes these ideas reappear "in representation learning, in reconstruction objectives, and in generalization analysis," which is the bridge from classical source coding to the neural setting the thesis works in.

### 5. The Donsker-Varadhan variational representation — proof engine, and a path to *measuring* the brain budget

The course derives (lecture 5, reused in lecture 26)

$$
\mathbb{E}_{P}[f] \;\le\; \log \mathbb{E}_{Q}\!\left[e^{f}\right] + D(P\,\|\,Q),
$$

the variational lower bound on KL that powers both generalization bounds above (file: `info-theory-course/5_04022026_Inequalities_study.md`, `26_generalization_error_bounds_OCR.md`). Beyond being the proof engine, **DV is the basis of neural mutual-information estimation (MINE):** if the thesis ever needs to *estimate* $I(\text{LM representations};\text{brain})$ in high dimensions rather than bound it, this is the tool. It connects the bound to a potential measurement.

---

## The probabilistic-ML connections (encoding model + low-data framing)

The Prob-ML course grounds the *modelling* side rather than the *bounds* side. The genuinely load-bearing rows:

- **Ridge regression is a Bayesian Gaussian noisy-measurement MAP estimate** (Block 1, `prob-ml-course/1_Data Models and Conjugate Distributions/1_1_data_models_study.md`). The encoding model — ridge from LM features to fMRI — is the NIX/NIW conjugate-Gaussian model: observe $y_i = W x_i + \varepsilon_i$, $\varepsilon_i \sim \mathcal{N}(0,\sigma^2)$, put a Gaussian prior on $W$, and the MAP estimate *is* ridge. The posterior-mean shrinkage formula tells you exactly when the regularizer dominates (small $n$, high noise) — i.e. exactly the noise-ceiling-limited regime the brain data lives in.
- **The ELBO decomposition** $\log p_\theta(x) = \mathcal{L}(q,\theta) + D(q_{Z\mid X}\,\|\,p_{Z\mid X,\theta})$ (Block 3 + info-theory L20, `prob-ml-course/3_Latent Variable Models & Approximate Inference/BLOCK3_EXAM_PREP.md`). If $\mathcal{L}_{\text{brain}}$ is ever framed as a prior on a latent representation, the KL regularizer term is exactly where it enters; the gap $D(q\,\|\,p_{\text{true}})$ is another face of R03's "how far can a prior move the posterior."
- **EM / incomplete-data likelihood ↔ confound subtraction.** The EM decomposition is the principled version of "estimate the variance explained by nuisance, then maximize alignment on the residual" — it shows the two-stage confound subtraction is not ad hoc.
- **TabPFN as amortized Bayesian inference** (Block 6, `prob-ml-course/6_Foundation Models for Tabular Data (TabPFN)/TabPFN_study.md`) maps to **F2 (low-data regularizer):** a prior trained offline on broad structure, applied cheaply to a small dataset — structurally the same move as using the human brain as a pre-trained prior accessed cheaply via a linear map. Load-bearing as an analogy for the F2 framing, not as imported machinery.

**Adjacent but not load-bearing** (recorded so a future session doesn't chase them): autoregressive models / MADE (Block 2), survival analysis & point processes (Block 5), implicit neural representations / SIREN / NeRF (Block 7), DDPMs / score matching (Block 8), and the multimodal-VAE papers (Block 4). DDPMs connect to the ELBO (a DDPM is a hierarchical VAE with a fixed encoder), so the *bound* is shared, but no diffusion-specific mechanism is used by the thesis as currently framed.

---

## Condensed syllabus inventory

**Information Theory for ML** (26 lectures): foundations & rate-distortion preview (L1) → notation/entropy (L2–3) → KL, mutual information, conditional MI, Jensen (L4–5) → data-processing inequality + source coding (L6–9, Kraft/Shannon/Huffman/McMillan) → arithmetic coding (L10–12) → universal compression / Lempel-Ziv / minimax redundancy (L13–15) → Fisher information & Cramér-Rao (L16–17, *notes missing*) → ML bridge: cross-entropy = code length, MLE = KL minimization (L18–19) → latent-variable models & ELBO (L20) → EM, GMM, variational inference (L21–22) → VAEs + reparameterization (L23–24) → generalization: setup and the MI bound (L25–26).

**Probabilistic ML** (8 blocks): (1) Bayesian inference, conjugacy, exponential family, Fisher info, model selection; (2) deep autoregressive models (MADE, OA-ARDM, deep AR for time series); (3) latent-variable models & approximate inference (EM, VI, VAE, importance sampling, Metropolis-Hastings, HMM, Kalman); (4) advanced VAEs (IWAE, GMVAE, VQ-VAE, NVAE, VampPrior, multimodal); (5) survival analysis & temporal point processes (Cox, Hawkes, neural variants); (6) TabPFN & tabular foundation models; (7) implicit neural representations (SIREN, NeRF, GASP, VaMoH); (8) DDPMs & diffusion.

## Gaps — filled 2026-06-10 (the course-central ones), rest deferred

The deferred gap-fill ran on 2026-06-10 (6 Sonnet subagents). **Seven new notes were written, co-located with their PDFs under `data/course-material/`** (gitignored, like the other 44). These are **agent-generated digests** (frontmatter `generated_by: agent`), not products of Erfan's `course-lecture-study` workflow, and each carries a `## Source audit` flagging slide-vs-standard provenance — treat them as solid but secondary to Erfan's own `*_study.md`. All remain **adjacent, not load-bearing** for the current thesis framing; the digests just complete the archive and each ends with an honest `## Thesis hook`.

- **Info-theory L16–L17 — Fisher information & Cramér-Rao** — now noted: `16_18032026_FisherInformation_CramerRao_study.md` (score function, $I(\theta)=\mathbb{E}[(\partial_\theta\log p_\theta)^2]$, CRB $\mathrm{Var}(\hat\theta)\ge 1/(nI(\theta))$) and `17_CramerRaoII_study.md` (Fisher matrix, matrix CRB $\mathrm{Cov}(\hat\theta)\succeq (nI(\theta))^{-1}$, biased-estimator + asymptotic-MLE efficiency). Reconstructed from sparse slides + standard results, cross-referenced to the Block-1 note. *Hook:* a tool for bounding the variance of the encoding-map ($W$) estimate under the noise ceiling — usable, not yet used.
- **Prob-ML Block 4 — the five course-central VAE papers** — now noted: `3_IWAE_study.md`, `4_GMVAE_study.md`, `7_VQ-VAE_study.md`, `8_NVAE_study.md`, `9_VampPrior_study.md`. *Hooks (all adjacent):* IWAE = the variance-reduction analogue of multi-run/CV alignment estimation; VQ-VAE = a rate operating point (shared rate-distortion lens); VampPrior = a clean illustration of "optimal prior = where the data concentrates," echoing R03's prior-over-the-manifold framing.

**Still un-noted (deliberately skipped — zero/low thesis relevance, never in the deferred task):** the two multimodal-VAE papers (`5_…MoE…`, `6_…multimodal…`) and the Gamma-Poisson note (`2_A_note_on_gamma_poisson.pdf`) in Block 4; the Block-1 Occam evidence note (`1_2_occam.pdf`) and Block-2 ARDM paper (content already covered inside the block study notes). Run `paper-digest` on these only if a use-case appears.

## Pointers into the rest of the brain

- `reports/R03_brain-as-training-signal.md` §2 — the first-principles bound this file formally grounds (MI bound, DPI, weak-prior selection).
- `01-research-landscape.md` — the anti-confound protocol (= conditional MI) and the compression trade-off (= rate-distortion / DPI) the course backs.
- `learnings.md` L003 — why every brain-alignment number must be unique variance after nuisance subtraction (the conditional-MI requirement).
