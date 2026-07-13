---
title: "06 — Theory grounding: the Information-Theory and Probabilistic-ML course as a source of truth"
tags: [methodology]
---

# 06 — Theory grounding: the Information-Theory and Probabilistic-ML course as a source of truth

**Created:** 2026-06-10 (Session 5 — analysis). **Status:** living index. **Full width, no hard wrap.**

## What this is, and why it exists

This repo has three kinds of external source feeding the thesis: the **papers** (canonical notes in `literature/canonical/`, the frontier map in [`01-research-landscape.md`](01-research-landscape.md)), the **datasets** ([`04-data-benchmarks.md`](04-data-benchmarks.md), [`05-dataset-registry.md`](05-dataset-registry.md)), and — added here — Erfan's **master's coursework** in Information Theory for ML and Probabilistic ML (UC3M, 2025–26). The coursework is the *theoretical grounding* layer: it is where the math the thesis keeps invoking informally (the information budget, the weak-prior bound, the unique-variance metric, the compression trade-off) has its exact, proved, textbook-faithful form. This file is the map from that coursework to the thesis, so a future session can cite the right result instead of re-deriving it from scratch or guessing the constant.

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

These six connections are the ones the thesis argument actually depends on — the first five ground R03's first-principles case; the sixth grounds R07's distillation result (Q1). Each row gives the course result, its exact statement, the note it lives in, and the precise thesis claim it grounds.

### 1. The mutual-information generalization bound — a diagnostic constraint, not a benefit guarantee

The course proves (lecture 26, via Donsker-Varadhan + sub-Gaussian concentration) that for a learning algorithm modelled as a channel $P_{W\mid Z^n}$ from the training set $Z^n$ to the learned parameters $W$, with $\sigma$-sub-Gaussian loss, the *average* generalization gap obeys

$$
\overline{\operatorname{gen}} \;=\; L - \widehat{L} \;\le\; \sqrt{\frac{2\sigma^2\, I(W;Z^n)}{n}},
$$

and the bounded-loss variant $d(\widehat{L}\,\|\,L) \le I(W;Z^n)/n$ (file: `info-theory-course/26_generalization_error_bounds_OCR.md`). This is an in-expectation upper bound on the magnitude of the generalization gap. Its right-hand side increases with $I(W;Z^n)$, so it does **not** say that adding an auxiliary brain signal improves generalization, and it does not supply a benefit of order $\sqrt{\Delta I/n}$. A brain-guided regularizer could tighten this bound only if it reduces the learned parameters' dependence on the sampled text while retaining empirical fit; whether it does so is an empirical question. The earlier order-of-magnitude information-budget argument is therefore retired and must not be used in the thesis.

### 2. The data-processing inequality — valid only after the Markov chain is stated

The course states and proves (lecture 6) that for a Markov chain $X \to Y \to Z$,

$$
I(X;Y) \;\ge\; I(X;Z),
$$

For this thesis the useful reading is conditional. If a student representation $C$ is literally constructed only by post-processing a teacher representation $T$, so that brain response $B \to T \to C$ is a justified Markov chain, then $I(B;C) \le I(B;T)$. Ordinary knowledge distillation does not automatically satisfy that chain: teacher and student both receive stimulus or corpus information, which provides a side path. Likewise, a chain such as $\theta^\star \to S \to B$ is an explicit conditional-independence model, not a theorem that "most brain information is already in text." DPI therefore motivates preservation tests after the relevant chain is defended; it does not prove that compression must reduce an empirical encoding score or that an observed preservation result is near a universal ceiling.

### 3. Conditional mutual information and unique $R^2$ — related under explicit assumptions

The course defines (lecture 4) conditional mutual information

$$
I(X;Y \mid Z) \;=\; H(Y\mid Z) - H(Y\mid X,Z),
$$

as the dependence between $X$ and $Y$ that remains after $Z$ is known (file: `info-theory-course/4_03022026_RelativeEntropy_MI_Jensen_study.md`). Under a population linear-Gaussian model with correctly specified, unregularized conditional means,

$$
I(X;Y\mid Z)=-\tfrac12\log\!\left(1-R^2_{\mathrm{partial}}\right),
\qquad
\Delta R^2_{\mathrm{semi}}=(1-R^2_{\mathrm{reduced}})R^2_{\mathrm{partial}}.
$$

The thesis instead estimates a finite-sample, cross-validated **semipartial** $\Delta R^2$ using regularized ridge models. It is therefore an operational measure of incremental linear predictive value beyond specified nuisance features, not an estimator or lower bound for conditional mutual information. Contiguous splits and fold-only preprocessing protect that predictive estimand against particular leakage and nuisance pathways; they do not turn it into CMI without the assumptions above.

### 4. The rate-distortion function — an organizing analogy for the empirical trade-off

The course gives (lecture 1) the rate-distortion function

$$
R(D) \;=\; \min_{P_{\hat S\mid S}:\,\mathbb{E}[(S-\hat S)^2]\le D}\; I(S;\hat S),
$$

the minimum mutual-information rate achievable at a specified expected distortion (file: `info-theory-course/1_InfTh_Intro_study.md`, Chunk 2). The thesis does not identify this Shannon object: parameter count or FLOPs are not $I(S;\hat S)$, and brain-alignment loss is not shown to be the distortion measure of a source-coding problem. "Rate--distortion" is therefore used only as a **rate--distortion-style engineering analogy** for an empirical Pareto frontier among model budget, language-model quality, and alignment. No theorem about $R(D)$ licenses a favorable movement of that frontier.

### 5. The Donsker-Varadhan variational representation — proof engine, and a path to *measuring* the brain budget

The course derives (lecture 5, reused in lecture 26)

$$
\mathbb{E}_{P}[f] \;\le\; \log \mathbb{E}_{Q}\!\left[e^{f}\right] + D(P\,\|\,Q),
$$

the variational lower bound on KL that powers both generalization bounds above (file: `info-theory-course/5_04022026_Inequalities_study.md`, `26_generalization_error_bounds_OCR.md`). Beyond being the proof engine, **DV is the basis of neural mutual-information estimation (MINE):** if the thesis ever needs to *estimate* $I(\text{LM representations};\text{brain})$ in high dimensions rather than bound it, this is the tool. It connects the bound to a potential measurement.

### 6. Cross-entropy = KL minimization — why "perplexity-only" and "distillation" are the same KL objective, and why neither pins down alignment

The course proves the ML bridge in two steps. Lecture 18 establishes that cross-entropy is *exactly* code length — $H(P_{\text{data}}, P_{\text{model}}) = \mathbb{E}_{x\sim P_{\text{data}}}[\text{code length under model}]$, an identity, not an analogy (file: `info-theory-course/18_motivation_ML_part_study.md`). Lecture 19 closes it: maximum-likelihood training *is* KL minimization between the empirical and model distributions (file: `info-theory-course/19_fully_observed_models_study.md`),

$$
\arg\max_\theta \tfrac{1}{n}\sum_i \log P_{X\mid\theta}(x_i) \;=\; \arg\min_\theta D\big(\widehat{P}_X \,\big\|\, P_{X\mid\theta}\big),
$$

because $\tfrac1n\sum_i -\log P_{X\mid\theta}(x_i) = H(\widehat{P}_X, P_{X\mid\theta}) = H(\widehat{P}_X) + D(\widehat{P}_X\,\|\,P_{X\mid\theta})$ and the empirical entropy $H(\widehat{P}_X)$ is fixed. Perplexity is the exponential of that per-token cross-entropy in nats, $\text{ppl} = \exp\!\big(H(\widehat{P}_X, P_{X\mid\theta})\big)$ (the standard definition, not from L18/L19, which measure code length in bits), so **lower perplexity is exactly smaller $D(\widehat{P}_X\,\|\,P_{X\mid\theta})$**: the language-model objective is, precisely, "make the model's next-token distribution close in KL to the data's."

**(a) Perplexity-only training and knowledge distillation are the same KL objective against different references.** Both are KL projections of the student's next-token distribution onto a reference; they differ in what the reference is. Plain LM training projects onto the empirical data, $\min_\theta D(\widehat{P}_X\,\|\,q_\theta)$; KD projects onto the teacher's temperature-softened distribution, $\mathcal{L}_{\text{KD}} = D\big(p_T^{\tau} \,\big\|\, q_S^{\tau}\big)$ (up to the standard $\tau^2$ scaling, an irrelevant constant here). The references carry different information — a one-hot empirical target versus the teacher's full soft distribution over non-realized tokens, the "dark knowledge" — but that difference is orthogonal to the control in the next paragraph: matching *held-out perplexity* across arms (on a shared corpus, so the data-entropy term $H(\widehat{P}_X)$ cancels) matches $D(\widehat{P}_X\,\|\,q)$, the quality of the next-token model, whichever reference produced it. This is why matched perplexity is the interpretable way to hold output quality fixed and vary only the objective (L011; R07/Q1), where matched-compute is not.

**(b) The objective constrains the output distribution; alignment is a property of the representation; the map between them is many-to-one.** KD and perplexity optimize KL on the **output** distribution, the next-token distribution, whereas alignment is the conditional MI $I(Z_S; B \mid \text{nuisance})$ of row 3, a property of the **internal** representation $Z_S$. The two connect only through the architecture's readout $Z_S \to \text{logits}$, which is many-to-one: many internal geometries realize the same output distribution. So matching the output does not *guarantee* matching the representation, and preservation of alignment is not forced a priori,

$$
D\big(p_T \,\big\|\, q_S\big) \to 0 \;\;\not\Rightarrow\;\; Z_S \approx Y_{\text{teacher}} \;\;\not\Rightarrow\;\; I(Z_S;B\mid\text{nuisance}) = I(Y_{\text{teacher}};B\mid\text{nuisance}).
$$

That many-to-one readout is shared with the teacher and with any LM, so it is a *necessary condition* for the student's geometry to diverge, not the cause; the cause is row 2's broken Markov chain — the from-scratch student's corpus side-channel lets its geometry be rebuilt away from the teacher's. Row 6 adds the objective-side statement about that same freed degree of freedom: the loss does not penalize the divergence. So row 2 says the teacher's alignment stops *upper-bounding* the student's; row 6 says the objective does not *pull* the student back to it. Neither forces an answer, which is why "does KD preserve alignment?" is empirical. The evidence does not license the *strong* reading that output match is uninformative about alignment: R07 finds alignment co-varies tightly with held-out perplexity across arms ($r=-0.88$), so output quality predicts most of the alignment *variation*, and any objective-specific effect must live in the *residual* after perplexity — which is exactly the quantity the matched-perplexity experiments isolate, and find only marginal ($p\approx0.09$; R07/Q1).

File anchors: `18_motivation_ML_part_study.md`, `19_fully_observed_models_study.md` (CE = code length = KL identities; perplexity is the standard $\exp$ of the per-token CE); the KL object itself is lecture 4 (`4_03022026_RelativeEntropy_MI_Jensen_study.md`, also row 3); the representation-side metric is row 3's conditional MI; the ceiling it complements is row 2's DPI. Thesis targets: R07 §"The design" and §"The evidence" ($r=-0.88$), learnings L011 (the matched-perplexity control), `experiments/E003`.

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

- [`manuscript/extended/sections/03_methods.tex`](manuscript/extended/sections/03_methods.tex) — the manuscript derivations this file formally grounds (MI bound, DPI, weak-prior selection).
- [`01-research-landscape.md`](01-research-landscape.md) — the anti-confound protocol (= conditional MI) and the compression trade-off (= rate-distortion / DPI) the course backs.
- [`learnings.md`](learnings.md) L003 — why every brain-alignment number must be unique variance after nuisance subtraction (the conditional-MI requirement).

## Learning-science grounding (for the `/teach` stance — apparatus, not thesis math)

The `/teach` pedagogy is grounded in three canonical notes, kept here so teach cites them rather than
asserting from memory. None carries A1/A2/A3 weight or a brain-alignment number — this is how-we-teach,
not thesis science.

- [`literature/canonical/dunlosky-2013_effective-learning-techniques.md`](literature/canonical/dunlosky-2013_effective-learning-techniques.md) — practice testing + distributed
  practice (high utility); interleaving / self-explanation / elaborative interrogation (moderate). The
  evidence-strength ratings the teach loop rests on.
- [`literature/canonical/bjork-2011_desirable-difficulties.md`](literature/canonical/bjork-2011_desirable-difficulties.md) — storage vs retrieval strength, the
  performance/learning dissociation (in-session fluency is an anti-signal), and the expertise caveat
  behind teach's per-topic gating.
- [`literature/canonical/open-learner-models-and-errorful-learning.md`](literature/canonical/open-learner-models-and-errorful-learning.md) — synthesis over four digested notes
  (Wong & Lim 2022 derring; [Butterfield & Metcalfe 2001](literature/canonical/butterfield-metcalfe-2001_hypercorrection-effect.md) hypercorrection; [Moser 2011](literature/canonical/moser-2011_growth-mindset-error-processing.md) mindset/error ERP;
  Robles Mucho et al. 2025 OLM review): why teach's mistake handling is diagnostic, not a scorecard.


## Related
- [`status.md`](./status.md) — the canonical status board
