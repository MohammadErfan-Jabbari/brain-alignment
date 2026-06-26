---
title: "R05 — The Thesis, From First Principles: a step-by-step, concept-by-concept narrative of the whole…"
tags: [report]
aliases: [R05]
---

# R05 — The Thesis, From First Principles: a step-by-step, concept-by-concept narrative of the whole experimental arc

**Created:** 2026-06-12 (Session 9 — analysis). **Status: RETIRED 2026-06-16.** Frozen, no longer maintained, and not part of the active report set. Superseded by the current-truth finding-reports ([`R06`](R06_alignment-signal-is-real-beyond-confounds.md) onward; index in `reports/README.md`) and the journey tree in [`map.md`](../map.md). Kept verbatim for history: it is the only doc that walked the arc chronologically (through Q2), and the wrong turns it records are part of the lesson. Nothing here is canonical; when it disagrees with [`ladder.md`](../ladder.md) or a finding-report, they win.

**Retired (read the status line above).** The text below is preserved unchanged from this report's last living revision, which narrated the arc through Q2 (the lever verdict and the E007 reroute). The rest of the arc, including the reversal this narrative never reached (E005's apparent headline, its collapse to a per-individual null (E008), the robustness escapes, the cross-family quality law (E015), the bounded stimulus-predictability ceiling (E020), the external reproduction (E019), and the Fork-B scope correction (L041)), now lives in the finding-reports `R06` onward and is mapped in `map.md`. Canonical status is always `ladder.md`.

**Review status:** this report was stress-tested by the thinking panel (counter-argument, first-principles-grounder, socratic-thinker, premortem-analyst) on 2026-06-12; their accuracy/grounding/pedagogy/framing findings have been folded in (corrected noise-ceiling, ρ′ labelling, A3 novelty scope, DPI chain, per-rung verdicts in §3, theory hedges).

---

## §0. What this report is, and what it is not

This is the **pedagogical, first-principles, course-grounded narrative** of the thesis: the story told slowly, from scratch, in plain language, with the math derived at enough length to actually follow and tied back to Erfan's MSc coursework and the papers we read. Its job is *understanding*. It is deliberately distinct from the other docs so it does not become a redundant copy of any of them.

- It is **not the manuscript** (`docs/manuscript/00_paper-draft-v0.md`). The manuscript is the terse artifact for submission — compressed, hedged, written for reviewers. R05 is the expanded "teach it to me" version: where the manuscript states a result in one sentence, R05 spends a paragraph on *why* the experiment was shaped that way and what the number means.
- It is **not R03** ([`R03_brain-as-training-signal.md`](R03_brain-as-training-signal.md)). R03 was the early *direction* doc (Session 4–5): it argued the idea was largely scooped, located the surviving slice (F1), and laid out the ladder — but it stops at E003 and predates everything dramatic. R05 *continues* where R03 stops, and re-tells R03's own setup more accessibly.
- It is **not the experiment docs or [`learnings.md`](../learnings.md)**. Those are the primary records (one file per experiment; one lesson per L-number). R05 is the connective tissue that turns them into a single readable story.
- It assumes the vocabulary primer (`docs/07-concepts-primer.md`) for the reusable primitives (voxel, ROI, encoding model, unique $R^2$, noise ceiling, the trained−untrained gap, the permuted twin). It re-summarizes them where needed but does not re-derive them.

A note on discipline: per the reports rule, **every empirical number in here is one a working session actually produced and recorded** (cited to its experiment doc / learning), and every literature number is cited to its canonical note. Nothing is invented or estimated.

---

## §1. The bet, in one breath

Here is the whole thesis in two sentences, before any machinery. The literature has firmly established that for a human and a language model processing the *same* text, there exists a simple (linear) map from a middle layer of the model to the recorded brain activity — this is the standard "brain score" instrument, and it is reliable. **The bet of this thesis is that this map is not just something to *measure* but something to *use*: that the brain, via that map, can serve as a training signal that shapes a model toward being more brain-like, and that doing so buys something we care about.**

The concrete, easy-to-measure first use case is **knowledge distillation** (compressing a big "teacher" model into a small "student"). The question becomes: if we distil a student not only to match the teacher's next-word predictions but *also* to preserve the brain-relevant structure, do we get a better small model than a brain-blind baseline at the same compute budget? Distillation is the *test bed*, not the whole thesis — it is simply the cleanest place to ask "does the signal carry usable information?"

```
            measure it  ──────────────►  USE it  (the bet)
   LLM mid-layer  ──linear map W──►  brain activation
   "brain score" (established)        "training signal" (the contribution space)
```

---

## §2. First principles — how much can the brain actually teach a language model?

Before running anything, the honest move is to ask what is even *possible*. This section derives, slowly, a single conclusion that governs everything downstream: **brain data cannot be a primary training target that competes with next-token prediction; its only coherent role is as a weak prior — and a weak prior helps most exactly where the main signal is weak (small models, scarce data, aggressive compression).** This is R03 §2 retold for understanding; the formal versions live in `docs/06-theory-grounding.md`, which maps each step to the exact lecture in Erfan's Information-Theory-for-ML course.

**Step 1 — Training is inference, and an added loss term is a *prior*.** When we train with the usual language loss plus a brain term, the objective is to minimise $[\text{text loss}] + \lambda \cdot L_{\text{brain}}$. Reading this through the Bayesian lens, choosing the most probable parameters given the data means maximising the log-posterior, which *splits additively*: $\log p(\theta \mid \text{data}) = \log p(\text{data} \mid \theta) + \log p(\theta) - \text{const}$. Line that up against our objective (minimising a loss = maximising its negative): the text loss plays the **likelihood** $\log p(D_{\text{text}} \mid \theta)$ — the evidence the task gives about the parameters — and *any* added regulariser, the brain term included, plays the **log-prior** $\log p(\theta)$. So adding the brain loss is, up to constants, a maximum-a-posteriori (MAP) estimate. (One honest caveat: the brain term is strictly a *second likelihood* $p(D_{\text{brain}} \mid \theta)$ — it depends on data — and "log-prior" is the regularisation convention for it; Steps 2–5 then read it the other way, as evidence to be counted against the text's evidence. Both readings give the same verdict — the brain term is weak — so nothing downstream turns on the label.) The real question is therefore not the vague "can the brain train the model?" but the quantitative "given a likelihood this strong, how far can this prior move the answer?"

**Step 2 — Count the evidence on each side (the information budget).** The pull of the likelihood scales with how many independent constraints it imposes. Next-token prediction supplies a few bits of supervision per token across roughly $10^{12}$ tokens → on the order of $10^{12}$–$10^{13}$ bits. The brain side has only $10^3$–$10^4$ stimuli per subject, each a handful of *effectively independent* voxels (they are heavily correlated and noisy), so its usable information is far smaller — we make this precise next.

**Step 3 — The noise ceiling is a channel capacity.** This is where the noise ceiling from the primer becomes a *bound*, not just a normaliser. Think of one voxel as a **noisy communication channel**: the message sent is the *stimulus-driven* part of its response (the signal), and what corrupts the message is the measurement/physiological noise. fMRI is noisy, so even a perfect model can only correlate up to the noise ceiling $r_{\max}$ with the true response — $r_{\max} \approx 0.3$–$0.56$ across language datasets. If we model the voxel as signal-plus-Gaussian-noise, the correlation $r_{\max}$ pins down the signal-to-noise ratio exactly: writing the recorded response as signal + independent noise, $r_{\max} = \sigma_{\text{signal}} / \sqrt{\sigma_{\text{signal}}^2 + \sigma_{\text{noise}}^2}$, which rearranges to $\mathrm{SNR} \equiv \sigma_{\text{signal}}^2 / \sigma_{\text{noise}}^2 = r_{\max}^2 / (1 - r_{\max}^2)$. The information one voxel can carry about its stimulus per presentation is then at most the Gaussian channel capacity

$$ I \;\le\; \tfrac{1}{2}\log_2\!\big(1 + \mathrm{SNR}\big), \qquad \mathrm{SNR} = \frac{r_{\max}^2}{1 - r_{\max}^2}. $$

Even at a *generous* $r_{\max} \approx 0.5$ this is only $I \approx 0.21$ bits per voxel per stimulus (at $r_{\max} \approx 0.35$, $\approx 0.09$ bits) — the number is illustrative, not a property of any one dataset. Multiply by the *effective* (post-redundancy) voxel count — tens, not thousands; Tuckute is literally 5 ROIs — and by the number of stimuli, and the total usable brain information lands around $10^4$–$10^6$ bits. That is **six to nine orders of magnitude** below the text budget. (This is an order-of-magnitude argument, not a theorem, and the bracket endpoints are not independently tight — but no honest tightening closes a gap that wide.)

**Step 4 — Most of even *that* is already in the text (the data-processing inequality).** The brain signal is itself a noisy function of the same stimulus the model already trains on. Put the optimal parameters at the head of a Markov chain — $\theta^\star \to S \to R(S) \to Y$ (the recorded brain data $Y$ informs $\theta^\star$ *only through* the shared stimulus $S$, i.e. $Y \perp \theta^\star \mid S$; this conditional-independence assumption is what licenses the next line — get it wrong and the DPI does not apply). The data-processing inequality (DPI) then says $Y$ cannot carry more information about the optimal parameters than the stimulus it came from:

$$ I(\theta^\star; Y) \;\le\; I(\theta^\star; S). $$

```
   θ*  ──►  S  ──►  R(S)  ──►  Y       (Markov chain; Y ⊥ θ* | S)
  params  stimulus  brain    fMRI
   │                rep.     data
   └── the LM is ALREADY trained on text drawn from S
       so the brain's UNIQUE contribution is only
       what's left after subtracting what text already gives
```

Because much of what predicts the brain (length, position, word identity, even a lot of syntax) is recoverable from text alone, the brain's *unique* contribution — $I(\theta^\star; Y \mid \text{text})$ — is thinner still. **This is the formal reason every alignment number in the thesis must be a *unique* $R^2$ after nuisance subtraction** (primer; learning L003): nuisance-explained alignment carries no information the text did not already supply. The DPI is course lecture 6 (`data/course-material/info-theory-course/6_10022026_DPI_SourceCodingI_study.md`); and unique $R^2$ (a squared semi-partial correlation) **operationalises** the conditional mutual information $I(\mathrm{LM}; B \mid \text{nuisance})$ — under joint Gaussianity it is a monotone transform of it, $\mathrm{CMI} = -\tfrac{1}{2}\log_2(1 - \rho^2_{\text{partial}})$, not literally equal to it — course lecture 4 (`4_03022026_RelativeEntropy_MI_Jensen_study.md`).

**Step 5 — A prior that weak cannot *teach*; it can only *select*.** With a likelihood worth $\sim 10^{12}$ bits and a unique prior worth, generously, $\sim 10^5$ bits, the parameters are overwhelmingly shaped by the text. The brain term cannot install new knowledge against that imbalance. What it *can* do is **break ties**: an overparameterised model has not one text-optimum but a whole high-dimensional manifold of near-equivalent solutions that fit the text equally well yet generalise differently. The brain term picks *which* of those text-consistent solutions we land in. That is the precise technical meaning of "inductive bias / regulariser / selection signal" — not a teacher of facts, but a chooser among the solutions the text already permits.

**Step 6 — Why this predicts *exactly where* it can help (a generalisation bound).** That a weak prior matters most when data is scarce is not a slogan; it falls out of any sample-complexity bound. In the course's information-theoretic form (lecture 26, `26_generalization_error_bounds_OCR.md`; same Donsker–Varadhan root as PAC-Bayes, lecture 5), the expected generalisation gap is bounded by

$$ \overline{\mathrm{gen}} \;=\; L - \widehat{L} \;\le\; \sqrt{\frac{2\sigma^2\, I(W; Z^n)}{n}}, $$

where $W$ is the learned weights, $Z^n$ is the training set of $n$ samples, $I(W; Z^n)$ is the mutual information between them (how much the trained model "memorised" its training set), and $n$ is the amount of task data. A well-aimed brain prior can only change generalisation through this $I(W; Z^n)$ term, and the benefit it buys scales as $O(\sqrt{\Delta I / n})$ — so it **shrinks as $1/\sqrt{n}$ and washes out as task data grows.** (Honest caveat: identifying the brain "information budget" of Steps 2–3 with $\Delta I$ here is a *ceiling heuristic*, not a derived equality — the budget bounds $I(\text{brain}; \text{stimulus})$, a different MI object from $I(W; Z^n)$; the point is only that a prior cannot inject more than it carries.) This is the bias–variance trade-off in another costume: a prior trades a little bias for a variance reduction that only pays off while variance dominates.

**The single most important consequence.** A weak-but-well-aimed brain prior can help **most** in low-information regimes — small models, scarce data, aggressive compression — and is **washed out** where the text signal already dominates (large models, abundant data). This is *why* the surviving slice of the idea lives in **distillation / low-data regularisation** and not in "make a frontier model better by pouring in fMRI." Every framing decision downstream inherits from this one sentence.

**The mechanism, in words (why a brain bias might help at all).** Two non-exclusive stories, both with 2026 evidence: (1) *abstraction* — brain-aligned middle layers track meaning abstraction rather than next-word statistics, so aligning to the brain regularises toward a more abstract, more generalisable region of representation space (Cheng 2026; though the intrinsic-dimension *direction* is contested — Cheng finds higher local ID → more aligned in language, Yu 2026 finds lower → more aligned in vision, so an ID surrogate has no agreed sign yet); (2) *human invariances / robustness* — the brain encodes the invariances a human uses to understand language robustly, so a model biased toward that geometry might be more robust and sample-efficient (the vision precedent, Pirlot 2022 — though a shuffled-label control there reproduced the accuracy gain, leaving only the *robustness* gain attributable to real neural structure). **Where the mechanism breaks (the brakes):** if the brain-predictive structure is mostly nuisance (Feghhi/Hadidi), aligning to it teaches nothing; if abstraction is reached by scale alone (alignment saturates ~3B, Oota), the bias is redundant above that scale; if compression already preserves alignment by default, "protect it" solves a non-problem unless framed as a *trade-off curve*. These brakes pin the value to the same corner: small / compressed / low-data.

---

## §3. The three assumptions, and the kill-gated ladder

R03 turned the bet into **three falsifiable assumptions**, inherited from an oracle review. Testing them *is* the contribution — no prior paper had cleanly tested all three with the confound-clean controls below. (They are numbered A1–A3 but introduced here in *dependency* order — A2 first, because it gates the other two.)

- **A2 — the signal is real, not nuisance.** Measured alignment survives the full anti-confound (it is not mostly length/rate/position/static-word artifact). *Fails if* the controls collapse the gain.
- **A1 — the signal survives compression when protected.** A student distilled *with* a brain/structural objective keeps neural predictivity that a perplexity-only student at the same budget loses. *Fails if* matched-budget utility-only KD reaches equal predictivity.
- **A3 — preserved alignment buys something practical.** OOD transfer, robustness, sample efficiency — not just a higher alignment number. *Fails if* gains stay confined to the metric. The honest novelty here is narrow: practical payoff *had* been claimed (e.g. Negi 2025), but never against a **matched-perplexity + permuted-twin** baseline — so **no prior paper had tested A3 with that confound-clean control** (L017/L023), which is the slice that is actually ours.

The decisive structural point: these are **dependent, not parallel.** A1 and A3 are meaningless if A2 fails — protecting or testing the usefulness of a signal that is mostly noise is protecting/testing noise. So the work is sequenced as a **kill-gated ladder**: each rung has a predeclared kill criterion, and you only climb if the rung below holds. This also orders the work cheapest/most-foundational first.

**Spoiler / status (do not read the table as an all-passing climb — two rungs came back negative).** The canonical verdicts live in `docs/ladder.md`; the final column carries them so this table cannot be screenshotted into the wrong story.

| Rung | Question | Maps to | **Final verdict (per ladder.md)** |
|---|---|---|---|
| **Q0 · A2** | Is the alignment signal real beyond confounds? | the gating question | ✅ **PASS (powered)** |
| **Q1** | Does plain perplexity-only KD preserve or destroy alignment? | the cheap F1 gate | 🟡 PARTIAL (headroom; not preserve-for-free) |
| **Q2** | Is $L_{\text{brain}}$ a *lever* — does optimising it raise held-out alignment? | movability | 🟡 PARTIAL (fragile, sub-threshold) |
| **Q3 · F1** | Alignment-guided KD vs perplexity-only KD at matched perplexity → per-person gain? | the headline | ❌ **NULL per-subject** (well-powered) |
| **Q4 · A3** | Does induced alignment buy something practical (OOD)? | the payoff | ❌ **bounded NULL** |
| **Q5 · F3** | An fMRI-free proxy that recovers most of the benefit? | the stretch | ⬜ deferred (moot) |

This report walks rungs **Q0, Q1, and Q2** — i.e. up to "the signal is real, and the lever is fragile." The two ❌ rungs (Q3/Q4 — where the headline collapsed) are the coverage frontier and are narrated in §9 onward (not yet written); the spoiler is here so no reader mistakes the early rungs for a finished, winning thesis.

---

## §4. The instrument — how we measure alignment without fooling ourselves

(Primer summary; full plain definitions in `docs/07-concepts-primer.md`.) We fit a **ridge (regularised linear) encoding model** that predicts brain activation from an LLM middle layer, scored by **held-out $R^2$**. We keep the map **linear on purpose** — a flexible nonlinear map could manufacture alignment from almost any representation, so linearity is a guardrail and tests whether the brain-relevant information is *linearly accessible*. A raw $R^2$ lies in four distinct ways, each with its own fix:

| The lie | Fix |
|---|---|
| Nuisance/low-level features inflate $R^2$ | **Unique $R^2$** = $R^2$(nuisance + LM) − $R^2$(nuisance alone) — only what the LM adds beyond length/rate/position/static-embedding counts (this is conditional MI, §2 Step 4) |
| Shuffled splits leak autocorrelated neighbours | **Contiguous splits** — whole blocks (Tuckute) / whole stories held out (LeBel) |
| A random net might score too (just architecture) | **Untrained control** + the verdict statistic is the **trained − untrained gap** |
| Brain data is noisy; raw $R^2$ has no scale | **Noise ceiling** (CC_norm), report alignment as a *fraction* of it; select reliable voxels on *held-out* repeats (no double-dipping) |
| (When *optimising* alignment) a gain might be generic | **Permuted twin** — a real brain-specific effect must beat its own target-permuted control, not just zero |

---

## §5. Q0 — is the signal real? (A2)

**E001 — the synthetic pilot that could not answer the question (lesson L004).** The first pilot used *synthetic* fMRI. By construction, synthetic data cannot tell you whether *real* brain structure is present beyond nuisance — it can only test plumbing. The lesson recorded (L004): a feasibility test has to be on real neural data or it answers nothing. This is why E002 exists.

**E002 — Tuckute, ROI level: the first real-data test (A2 PASS).** Tuckute 2024 (Fedorenko lab) recorded the brain's language network while people read **1000 isolated English sentences**, delivered as **5 left-hemisphere language-ROI averages** over 5 participants (ROI = a named region; the voxels inside it averaged — coarse but robust). Feeding the same sentences to GPT-2/Qwen and fitting the encoding model: trained models peak at their **middle** layers, and the random-init control is **negative at every layer and seed**. The trained−untrained gap is **+0.030 to +0.050**; the strongest model (Qwen) captures a single-digit-to-~10% fraction of the noise ceiling — the exact figure depends on which ceiling estimate you use: E002's headline divided by the *anatomical*-mask ceiling 0.353 (→ ~10%), but the ceiling matched to the actual *functional* language ROIs is higher (~0.49–0.56), giving the more honest **~7%** (the 0.353 mislabel and the correction are recorded in L012). **Verdict: A2 PASS on real data** — but ROI-level is only 5-dimensional, coarse and statistically thin, which is *why* the powered voxel-level confirmation was run next. (`experiments/E002_*.md`.)

**E006 — LeBel UTS03, voxelwise: the powered confirmation (A2 STRONG PASS).** LeBel ds003020 is the deep-sampling benchmark: subject **UTS03** listened to ~82 spoken stories over 20+ hours, recorded at the **voxel** level (~95k voxels). We keep only the **11,442 noise-ceiling-reliable voxels** (reliability > 0.5, measured on a *held-out* repeated story so selection doesn't cheat), use **whole-stories-held-out** cross-validation (the contiguous rule for continuous speech — adjacent 2-second TRs are autocorrelated, so you cannot hold out random TRs), and subtract the full nuisance stack (word rate, phoneme rate, word duration, word length, log word-frequency, and the 985-dim static eng1000 word embedding). Result:

| Model · layer | trained − untrained gap [95% CI] | % reliable voxels with gap > 0 |
|---|---|---|
| gpt2 · L7 | **+0.0207 [+0.0205, +0.0209]** | 95% |
| Qwen2.5-0.5B · L12 | **+0.0277 [+0.0274, +0.0280]** | 99% |

The confidence intervals are *extremely* tight (11k voxels × folds = a mountain of data), and nearly every reliable voxel shows the effect (not an average dragged up by a few). One honest sizing note: the *gap* is the verdict statistic (L007), but it is large partly because the untrained control is meaningfully *negative* (−0.017), not ~0 — the trained model's *absolute* unique $R^2$ is modest (+0.0038 gpt2 / +0.0103 Qwen). So the effect is real and near-universal, but don't over-size the raw trained signal; the gap is what cleanly isolates "what training added." **Verdict: A2 STRONG PASS, powered.** It clears the **Hadidi/Feghhi 2026** bar — the skeptics' paper that argues most published alignment is nuisance and that untrained nets can score — because the effect survives the full nuisance *and* the untrained model explains nothing. **This is the bedrock the whole thesis still stands on: everything downstream collapses, but "the signal is real" never does.** (`experiments/E006_*.md`.)

---

## §6. The Q1 gate — does perplexity-only distillation keep alignment? (E003, lesson L011)

Before building any brain loss, a cheap kill-test: where does ordinary perplexity/logit distillation land a student on the alignment axis, relative to its teacher? If KD preserves alignment *for free*, then F1 ("protect alignment during compression") is solving a non-problem. First, the labels: a **warm-KD** student is initialised from the teacher's weights and then distilled; a **cold-KD** student is distilled from scratch (random init); distilgpt2 is the off-the-shelf distilled GPT-2. **E003 found a clean monotone gradient** in *floor-anchored retention* $\rho' = (A_{\text{student}} - A_{\text{floor}})/(A_{\text{teacher}} - A_{\text{floor}})$ — conventional GPT-2 $\approx$ teacher > warm-KD ($\rho'=0.84$) > distilgpt2 (0.60) > from-scratch cold-KD (0.37); cold-KD sits $\Delta=0.018$ ($p<0.001$) below the teacher. (Read $\rho'$ carefully: it is retention *relative to an untrained floor*, not a fraction of the teacher's alignment — cold-KD's $\rho'=0.37$ looks middling but its raw unique $R^2$ is +0.0005 against the teacher's +0.0188, i.e. it kept ~nothing; $\rho'$ is inflated only because the floor is negative.) So alignment is **not** preserved by default — there is headroom for a brain objective to matter. **But the deeper lesson (L011) is the one that reshapes everything after it:** alignment **co-varies with general LM quality**. Quality is measured by **perplexity** — roughly, how "surprised" the model is by held-out text (the exponential of its average next-token loss); *lower perplexity = better language model*. Across these students, alignment tracks perplexity at $\rho = -0.88$ on log-perplexity (better model → more aligned), and the *KD-specific* shedding-beyond-what-perplexity-costs is only $p \approx 0.1$ at this ROI-coarse benchmark. **Consequence:** any future "alignment went up" result is confounded unless the baseline is matched on **perplexity**, not just compute budget — otherwise you cannot tell a brain-objective win from "I just made a better language model." This single requirement — *matched perplexity* — becomes the load-bearing control of the entire headline experiment. (`experiments/E003_*.md`.)

---

## §7. Q2 — can we *move* it? The lever, and why E007 was cancelled (the coverage frontier)

**E004 — building $L_{\text{brain}}$ and testing it as a lever.** A "lever" means: if we *optimise* the brain loss (brain-tune a small model), does *held-out* unique $R^2$ actually *rise*? E004 built the loss family (MSE / cosine / Pearson / frozen-encoder / CKA variants, plus a block-permuted twin) and brain-tuned via **LoRA** (Low-Rank Adaptation — a cheap fine-tuning method that freezes the model and learns small low-rank weight-update matrices, chosen here because full fine-tuning at any useful $\lambda$ wrecked perplexity, L012(5)). The finding was a **fragile, brain-specific lever on the strongest aligner**: Qwen co-trained-MSE minus its own permuted twin = **+0.0032 [+0.0006, +0.0058]** — positive and specific (it beats the permuted control), but small, and one fold (fold 4) carries about half of it. On the coarse 5-ROI screen no arm raised alignment above base by a resolvable margin (the screen's MDE is too large), the `frozen` variant behaved as a *non-specific* regulariser, and — consistent with L011 — the lever co-varies with perplexity. **Verdict: PARTIAL.** A brain-specific lever exists but is fragile and perplexity-entangled (lessons L011/L012). Its predeclared rule routes the question to a powered substrate. (`experiments/E004_*.md`.)

**E006's second job — could a powered substrate even *resolve* that lever? (the MDE analysis).** This is the hinge, and it needs the concept of statistical power, so here it is as a standalone explainer:

> **Box — statistical power and MDE (used everywhere from here on).** Running an experiment to detect an effect has two failure modes: a **false alarm** (claim an effect that isn't there — controlled by the p<0.05 threshold) and a **miss** (a real effect comes back "not significant"). **Power** = the probability you *catch* a real effect of a given size if it is truly there; power 0.80 = caught 80% of the time. Power rises with (1) bigger true effect, (2) less noise, (3) more data. The crucial consequence: **an underpowered "no significant effect" is ambiguous** — it could mean "no effect" or "real effect, couldn't see it." So a null only *means* something if you had the power to have seen the effect. **MDE (minimum detectable effect)** flips this around: fixing the power you want and your data's noise, the MDE is the *smallest true effect you could reliably catch.* It is the **resolution of your instrument.** A bathroom scale marked in 1 kg steps cannot detect a 200 g change — and a flat needle does not prove your weight is unchanged, only that any change was below the scale's resolution. To claim "no change," you need a scale fine enough to have seen the change you care about.

E006 computed, from the fold-to-fold variance of unique $R^2$ on those 11k reliable voxels, the **MDE for the planned E007 lever test: $\approx$ +0.013–0.015** at 80% power. But the effect we'd want to catch — the E004 lever — is only **~+0.003**, four to five times *smaller* than the instrument's resolution. So the substrate powerful enough to *prove the signal is real* is still **too coarse to confirm the signal is movable** at the scale the lever lives. Running E007 would be weighing a 200 g change on a 1 kg scale: a null answer would be uninformative.

**The decision: cancel E007, reroute to E005.** One honest nuance kept the lever from being declared dead: the +0.013 MDE is for the *crude unpaired* statistic, whereas E004's +0.003 surfaced only in the *paired* arm-vs-permuted-twin contrast (which removes common-mode noise and could be better powered). So the verdict was not "the lever is zero" but "**building the heavy E007 training loop is a gamble against a fragile +0.003 on a substrate that can't cleanly resolve it.**" There is also a logical thread worth making explicit: if the lever is this fragile and sub-threshold, then the *same* loss used inside distillation should be expected to buy $\approx 0$ per person — so E005 was run not because we expected a Fork-A win, but because it is the cleanest way to *measure* the per-individual gain, win or null. The honest move was to **not build E007** and instead run **E005** — alignment-guided vs perplexity-only distillation at *matched perplexity* — which is decision-useful either way: a big brain-term win would be the optimistic thesis (Fork A), a small/null result is the honest measurement/trade-off contribution (Fork B). (`experiments/E006_*.md`, decision recorded there.)

**The seam this opens.** Q0 said the signal is *real*, overwhelmingly. The first powered look at "is it *movable*?" said: the movable effect, if any, is *tiny* and hard to pin down. That is the distinction that organises the entire rest of the thesis:

```
   REAL  ≠  MOVABLE   ≠  USEFUL
   (A2)      (Q2)         (A3)
   E002,     E004         E009
   E006      fragile,     bounded
   STRONG    sub-thresh.  NULL
   PASS      → reroute    → (and Q3/F1 = per-person NULL)
   ✅         🟡 → ❌       ❌
```
(The diagram is drawn *at this coverage frontier*; the two right-hand questions do not stay open — both later resolve **negative** per `ladder.md`. They are shown fragile/to-come only because §9+ has not yet narrated their collapse.)

A strong PASS on "real" tells you *nothing* about "movable" or "useful." Keeping these three apart is the spine of everything that follows. And the ending is already known: **the matched-perplexity headline (E005) looked like a +0.0081 brain-specific win, but it does not survive — it collapses to a per-individual null (E008), and the ladder already records Q3/F1 as ❌.** The next sections explain *how* that collapse happened and why the null is, in the end, the contribution.

---

## §8. Coverage frontier — what comes next (placeholders for the following sessions)

The narrative above is complete through the lever verdict. The following are recorded in the ladder and experiment docs and will be written into R05, in this style, as we walk them in subsequent sessions:

- [ ] **§9 — Q3 / F1, the would-be headline (E005).** The matched-perplexity alignment-guided vs perplexity-only KD experiment; the apparent **+0.0081** brain-specific gain; what target it was measured against.
- [ ] **§10 — The panel catch and the collapse (E008).** Pseudo-replication exposed before compute (L015); the well-powered per-individual experiment ($n=9$, MDE $\approx +0.0006$, power 1.0 at $\delta=+0.003$) returning a **null** (+0.00010, CI crossing 0); why a *powered* null is a real result, not a shrug.
- [ ] **§11 — The reframe (Fork B) and the averaging confound.** Why cross-subject target-averaging manufactures apparent brain-specificity; why the null is the positive contribution.
- [ ] **§12 — Closing every escape (robustness), now method-general.** E011 (capacity), E013b (objective), E013 (substrate / mechanism failure), E014 (the encoding-side averaging that is *not* a confound), and **E017** (the powered full-FT escape, $n=9$, $p=0.27$) — the null survives every axis: capacity / objective / substrate / *parameterisation* (LoRA + full fine-tuning), a method-general lever failure (L036).
- [ ] **§13 — The supporting law: why "brain-specific" gains track quality.** E009 (A3, bounded null, null-by-construction) and **E015** (the cross-family alignment $\propto$ −bits-per-byte law, **$r \approx -0.78$** — corrected from the v2 $-0.92$, which was inflated by per-token-perplexity + best-layer + a 3-family span; operative capable-band $\approx -0.48$ with CI crossing 0; L034) — and why this is the *mechanism* that makes matched-perplexity the load-bearing control.
- [ ] **§14 — The stimulus-predictability ceiling, scoped honestly (the conceptual core).** **E020** (the empirical $E[Y\mid S]$ ceiling, **bounded-not-closed** — instrument-limited at $n=6$, demoted to convergent corroboration; D030/L039/L040) and the **S14 scope correction (L041, keystone):** the evidence supports the *operational* claim ("no brain-specific gain is **inducible** beyond perplexity via the readouts tried"), not the information-theoretic "the residual is task-independent noise"; **$Y \perp \theta^\star \mid S$ is an assumption**, not a result; and the one **unmeasured** door — a DPI selection/regularisation side-channel (a brain prior that helps OOD without moving the alignment metric, lecture-26 $I(W;Z^n)$) — is *argued*-shut by E009's ~0 fulcrum, not *measured*-shut.
- [ ] **§15 — The external reproduction (corroboration, not clincher).** **E019** (a faithful Negi head — differentiable Lanczos+FIR+NT-Xent full-FT on LeBel — with no positive encoding gain at any lr; L042) and why it is *corroboration* of the lever-failure spine, not a clean "Negi doesn't reproduce" (the raw-mean-$r$ ruler is quality-blind; decoder $\neq$ Negi's BERT); the literature positioning (Jia L-PACT, Raugel, Hadidi→Nature-Comms).
- [ ] **§16 — Where we stand.** Manuscript reframe to the refocused headline (control-protocol + per-individual null + $E[Y\mid S]$ ceiling); the one untested door (full fine-tuning on multi-subject naturalistic voxelwise) now superseded/moot (E017's powered null; D033); why Q5/F3 is deferred.

---

## Sources

**Experiments (recorded numbers):** `experiments/E001_*` (L004), `E002_*` (Tuckute A2 PASS), `E003_*` (KD gradient, L011), `E004_*` (lever PARTIAL, L011/L012), `E006_*` (powered A2 PASS + E007 MDE). **Lessons:** `docs/learnings.md` L003 (anti-confound), L004, L007, L011, L012. **Theory grounding:** `docs/06-theory-grounding.md` and the course notes under `data/course-material/info-theory-course/` — lecture 1 (rate–distortion), 4 (relative entropy / MI / conditional MI), 5 (Donsker–Varadhan), 6 (DPI / source coding), 26 (generalisation-error bounds). **Literature (canonical notes, `docs/literature/canonical/`):** hadidi-2024/feghhi-2024 (anti-confound bar), moussa-2025/2025b (brain-tuning speech), bilgin-2026 (text-LM inversion), merlin-2026 (causal necessity), oota-2026 (compression × alignment), cheng-2026 / yu-2026 (intrinsic dimension, contested sign), pirlot-2022 (neural-data regulariser, vision). **Status board:** `docs/ladder.md` (always canonical when this report lags). **Vocabulary:** `docs/07-concepts-primer.md`.

---

**Last updated:** 2026-06-12 (Session 9; panel-reviewed + revised). Narrative frontier: end of Q2 (lever verdict / E007 reroute). Next: §9 (E005).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
