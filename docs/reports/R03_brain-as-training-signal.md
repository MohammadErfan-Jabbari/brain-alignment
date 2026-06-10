# R03 — Brain as a Training Signal: a first-principles interrogation of the inversion idea, and where the real open space is

**Created:** 2026-06-10 (Session 4 — working/analysis). **Status:** living direction doc. **Full width, no hard wrap.**

**What this is.** Erfan's overnight brain dump proposed *inverting* the usual brain-alignment direction: instead of only *measuring* that LLM middle layers map linearly to fMRI, *use* the fMRI (plus that mapping) as a *training signal* to shape or train the LM. He asked to reason this from first principles — learning theory, the mechanics of training deep nets and LLMs, probabilistic generative models — and to build the idea layer by layer, evolving or deleting parts. This report does that, confronts the idea with the 2025–26 literature (which partly scoops it), and lays out a falsifiable experimental ladder. It is a recommendation and a map, not a decision; the kill criteria are real.

---

## 1. The idea, stated precisely

The literature establishes: for a human and an LLM processing the same language stimulus, there exists a linear map $W$ such that $\text{fMRI} \approx W \cdot h_\ell(\text{stimulus})$, where $h_\ell$ is a middle-layer LLM representation. This map is reliable and is the standard "brain score" / encoding-model instrument. 

The inversion: treat the brain as a *target* the model should be pulled toward during training, i.e. add a term $\mathcal{L}_{\text{brain}}$ that rewards the model for having representations that predict (or are predicted by) recorded brain activity, and ask whether a model trained with it is *better* in some practical sense than one trained without.

This is a clean, real idea. It is also — and we have to say this plainly because the job is to help Erfan decide well, not to flatter the idea — **largely already done as of 2025–26.** The honest contribution is a narrower, sharper slice, and the first-principles work below is what locates that slice.

---

## 2. First principles: can brain data train a language model at all?

**What an LM is.** A language model is a probabilistic generative model of text: it learns $p_\theta(x)$ by maximum likelihood on next-token prediction over trillions of tokens. Its gradient signal is enormous, dense, and self-supervised — every token is a label.

**What the brain signal is.** fMRI is a slow (TR ≈ 2 s), noisy, indirect (BOLD hemodynamics) measurement of neural activity, with a *noise ceiling* that caps explainable variance at roughly $r \approx 0.3$–$0.56$ even for a perfect model. A typical language-fMRI dataset has $10^3$–$10^4$ stimulus points per subject, not $10^{12}$. The mutual information between the recorded brain signal and the stimulus that is *not already present in the text itself* is therefore tiny.

**The bound this implies — derived slowly, from the learning theory underneath.** The claim of this section compresses to one sentence: *brain data cannot be a primary training target that competes with next-token prediction; its only coherent role is as a weak prior.* That sentence is easy to assert and easy to wave away, so the rest of this block builds it properly — as a Bayesian-inference argument, an information budget, and a generalization bound — because every downstream framing decision (§4) inherits from it. Take it one step at a time.

*Step 1 — Training is inference, and a loss term is a prior.* Write training as choosing parameters $\theta$. Adding a brain term to the usual language-model loss gives the objective

$$
\hat{\theta} \;=\; \arg\min_{\theta}\; \underbrace{\Big[-\textstyle\sum_{t=1}^{N}\log p_\theta(x_t \mid x_{<t})\Big]}_{-\log p(\mathcal{D}_{\text{text}}\mid\theta)\;=\;\text{text loss}} \;+\; \lambda\,\underbrace{\mathcal{L}_{\text{brain}}(\theta)}_{-\log p(\theta)\;=\;\text{a prior}} .
$$

Up to additive constants this is *exactly* a maximum-a-posteriori (MAP) estimate, $\hat\theta_{\text{MAP}} = \arg\max_\theta \big[\log p(\mathcal{D}_{\text{text}}\mid\theta) + \log p(\theta)\big]$: the text enters as the **likelihood** (the evidence about the task), and any added regularizer — $\mathcal{L}_{\text{brain}}$ included — enters as the **log-prior**. So the real question is not the vague "can the brain train the model?" but the quantitative one: *given a likelihood this strong, how far can this prior move the posterior?*

*Step 2 — Count the evidence on each side (the information budget).* The likelihood's pull on $\theta$ scales with how many independent constraints it imposes. Next-token prediction supplies, per token, roughly its conditional entropy $H(x_t\mid x_{<t})$ — a few bits for natural language — across $N\approx 10^{12}$ tokens, so on the order of $10^{12}$–$10^{13}$ bits of supervision. The brain side has only $n\approx10^{3}$–$10^{4}$ stimuli; each records $v$ voxels, but the voxels are heavily correlated and noisy, so the *usable* information is far below the naive $n\times v$ and is capped by the noise ceiling — which the next step turns into an actual number.

*Step 3 — The noise ceiling is a channel capacity.* For each effectively-independent voxel, the best achievable correlation between any model's prediction and the recorded response is bounded by the noise ceiling $r_{\max}\approx 0.3$–$0.56$. Model the stimulus-driven response as signal-plus-Gaussian-noise; then the information one voxel carries about its stimulus-driven component, per stimulus, is at most the Gaussian channel capacity

$$
I \;\le\; \tfrac{1}{2}\log_2\!\big(1+\mathrm{SNR}\big), \qquad \mathrm{SNR} \;=\; \frac{r_{\max}^2}{1-r_{\max}^2}.
$$

At $r_{\max}=0.5$ this gives $\mathrm{SNR}\approx0.33$ and $I\lesssim 0.21$ bits; at the Tuckute LangNetw ceiling $r_{\max}\approx0.35$, $I\lesssim 0.09$ bits. Multiply by the *effective* (post-redundancy) voxel count — tens, not thousands; Tuckute is literally 5 ROIs — and by $n$ stimuli, and the total usable brain information lands around $10^{4}$–$10^{6}$ bits. That is **six to nine orders of magnitude** below the text budget. (This is an order-of-magnitude heuristic, not a theorem — but no honest tightening closes a gap that wide.)

*Step 4 — Most of even that is already in the text (data-processing inequality).* The brain signal is itself a noisy function of the same stimulus. With $S$ the stimulus and $R$ the brain's internal representation, we have the Markov chain $S \to R(S) \to Y$, and the language model is *already* trained on text drawn from $S$. So the brain can only add its **unique** information about the optimal parameters beyond the text, $I\big(\theta^\star; Y \mid \mathcal{D}_{\text{text}}\big)$, and the data-processing inequality forbids $Y$ from carrying more about $\theta^\star$ than the stimulus it was derived from:

$$
I\big(\theta^\star; Y\big) \;\le\; I\big(\theta^\star; S\big).
$$

Because much of the brain-predictive structure (length, position, word identity, even syntax) is recoverable from text alone — precisely the point R01 §2/§4 makes when it insists on *unique* variance after nuisance subtraction — this conditional term is smaller still. The honest brain budget is not even the $10^{4}$–$10^{6}$ bits of Step 3, but the thin slice of it not already implied by the text the model has seen.

*Step 5 — A prior that weak cannot teach; it can only select.* With a likelihood worth $\sim10^{12}$ bits and a unique prior worth, generously, $\sim10^{5}$ bits, the posterior over $\theta$ is overwhelmingly shaped by the text — the brain term cannot install new task knowledge against that imbalance. What it *can* do is break ties. An overparameterized language model does not have one text-optimum; it has a high-dimensional **low-loss manifold** of near-equivalent solutions,

$$
\Theta_\epsilon \;=\; \big\{\,\theta : \mathcal{L}_{\text{text}}(\theta) \le \mathcal{L}^\star_{\text{text}} + \epsilon\,\big\},
$$

all of which fit the text comparably well yet *generalize differently*. The brain term acts as a **selection rule over **$\Theta_\epsilon$**, **$\;\hat\theta \approx \arg\min_{\theta\in\Theta_\epsilon}\mathcal{L}_{\text{brain}}(\theta)$**: it chooses** *which* text-consistent solution we end up in. That is the exact technical meaning of "**inductive bias / regularizer / selection signal**" — not a teacher of new facts, but a chooser among the solutions the text already permits. This is also why "train the LM *on* the brain" collapses, under the budget above, into "*bias* an LM that is mostly trained on text."

*Step 6 — Why this predicts exactly where it can help (a generalization bound).* That a weak prior matters *most* when data is scarce is not a slogan; it falls out of any sample-complexity bound. The PAC-Bayes (McAllester) bound, for a prior $P$ and a learned posterior $Q$ over parameters, reads

$$
\mathbb{E}_{\theta\sim Q}\big[\mathrm{risk}(\theta)\big] \;\le\; \mathbb{E}_{\theta\sim Q}\big[\widehat{\mathrm{risk}}(\theta)\big] \;+\; \sqrt{\frac{\mathrm{KL}(Q\,\Vert\,P) + \ln(n/\delta)}{2\,n}} .
$$

A prior $P$ that already concentrates its mass on brain-aligned (here: more abstract, more human-like) hypotheses *lowers* $\mathrm{KL}(Q\Vert P)$ for the good $Q$, and so tightens the bound — but the whole correction term scales as $1/\sqrt{n}$ and **vanishes as the effective task data **$n$** grows**. This is the bias–variance tradeoff in another costume: a prior trades a little bias for a variance reduction that only pays off while variance still dominates. Hence the conclusion, now *derived* rather than asserted — a weak-but-well-aimed brain prior can help **most** in low-information regimes (small models, scarce data, aggressive compression) and is **washed out** where the text signal already dominates (large models, abundant data). This single consequence is the most important in the report: it determines everything downstream in §4 — it is *why* the surviving slice of the idea lives in distillation and low-data regularization, and *why* it cannot live in "make a frontier model better by pouring in fMRI."

*Step 7 — The same bounds, in the course's exact form (formal backing, not hand-waving).* Steps 1–6 were built from first principles; it is worth recording that each rests on a theorem the Information-Theory-for-ML course (Erfan's MSc coursework) states and proves, so the thesis can *cite* the result rather than re-derive it or guess a constant. The full concept→thesis map is `docs/06-theory-grounding.md`; the three load-bearing anchors are these.

First, the generalization claim. Step 6 used the PAC-Bayes (McAllester) bound; the course derives its in-expectation twin (lecture 26, file `data/course-material/info-theory-course/26_generalization_error_bounds_OCR.md`) — for a learning algorithm modelled as a channel $P_{W\mid Z^n}$ from the training set to the learned parameters $W$, with $\sigma$-sub-Gaussian loss,

$$
\overline{\operatorname{gen}} \;=\; L - \widehat{L} \;\le\; \sqrt{\frac{2\sigma^2\,I(W;Z^n)}{n}}.
$$

Both faces — the high-probability PAC-Bayes form used above and this in-expectation form — descend from the *same* Donsker-Varadhan variational representation of KL (course lecture 5). That collapses Step 6's conclusion to a single quantity to watch: the brain prior changes generalization only through the algorithm's input-output mutual information $I(W;Z^n)$, and the benefit it can buy is $O(\sqrt{\Delta I / n})$, where $\Delta I$ is the extra mutual information the brain term injects. The entire "information budget" of Steps 2–4 is precisely the estimate of that $\Delta I$ — which is *why* a budget six-to-nine orders below the text's forces the prior to be weak, and *why* the $1/\sqrt{n}$ scaling washes it out as task data grows.

Second, the "most of it is already in the text" claim of Step 4 is the data-processing inequality verbatim (course lecture 6, file `data/course-material/info-theory-course/6_10022026_DPI_SourceCodingI_study.md`): for the Markov chain $S \to R(S) \to Y$, $I(\theta^\star;Y) \le I(\theta^\star;S)$. Read forward through the distillation pipeline — stimulus $\to$ teacher LM features $\to$ compressed student representation — the very same theorem gives $I(Z_{\text{student}};B) \le I(Y_{\text{teacher}};B)$: **compression can only lose brain alignment, never create it.** That is the formal statement of §2's third brake (the arXiv 2602.07547 counter-evidence). If compression *empirically preserves* alignment, the DPI bound is near-tight in practice, which is exactly why F1 must compete on the rate-distortion **trade-off curve** — $R(D)=\min_{P_{\hat S\mid S}:\,\mathbb{E}[(S-\hat S)^2]\le D} I(S;\hat S)$, course lecture 1 — and not on a preserve-vs-destroy binary.

Third, the "unique variance after nuisance subtraction" that every brain-alignment number in this thesis is required to report (L003) is conditional mutual information (course lecture 4, file `data/course-material/info-theory-course/4_03022026_RelativeEntropy_MI_Jensen_study.md`): $I(\text{LM};\,B \mid \text{nuisance})$. The contiguous-split, nuisance-baseline protocol is its ridge-regression operationalization. So the anti-confound discipline is not caution bolted on after the fact — it is the only quantity the generalization bound above is actually about, since nuisance-explained alignment carries no $\Delta I$ the text did not already supply.

**Why a bias toward the brain might help (the mechanism, Feynman-style).** Two non-exclusive stories, both with 2026 evidence:

1. *Abstraction.* Brain alignment in middle layers tracks *meaning abstraction*, not next-word statistics (Cheng et al. 2026: a layer's local intrinsic dimension predicts its brain-predictivity; brain-tuning *causally raises* intrinsic dimension and semantic content together). Independently, lower-intrinsic-dimension representations generalize better and align better, across artificial and biological nets (arXiv 2601.22722). So the brain is a *pointer* to a more abstract, more generalizable region of representation space. Aligning to it = regularizing toward abstraction.
2. *Human invariances / robustness.* The brain's representation encodes the invariances a human uses to understand language robustly. A model biased toward that geometry might be more robust to distribution shift and more sample-efficient. This is the vision precedent: a neural-data (monkey IT) regularizer via Deep CCA improved CNN accuracy *and* adversarial robustness (Federer et al. 2022).

**Where the mechanism breaks (the brakes, mandatory).** (a) If the brain-predictive structure is mostly *nuisance* — sentence length, position, low-level lexical identity — then aligning to it teaches nothing useful; this is the Feghhi 2024 / Oota 2024 brake and is exactly why every number in this thesis must be a *unique* variance after nuisance subtraction under contiguous splits (L003). (b) If the abstraction geometry is already reached by scale alone — brain alignment *saturates* around 3B parameters (Oota 2026) — then the bias is redundant above that scale. (c) If post-hoc compression already preserves alignment by default (arXiv 2602.07547, the key 2026 counter-evidence), then "protect alignment during compression" may be solving a non-problem unless framed as a *trade-off curve*, not a *preserve-vs-destroy* binary. These three brakes jointly pin the value of the idea to a specific corner: **small / under-trained / compressed models, in low-data regimes** — precisely where a weak-but-well-structured prior matters most.

---

## 3. The literature already does most of the bare inversion (be honest about it)

A focused 2023–26 survey of NeurIPS/ICML/ICLR/ACL + neuro venues (full shortlist in the session timeline) returns:

- **Brain-tuning, speech** — Moussa, Klakow, Toneva, *ICLR 2025* (`moussa-2025_brain-tuning-speech-lms`): an L2 voxelwise fMRI loss fine-tunes ~90M speech LMs, +30% late-language alignment, consistent downstream gains, using &lt;0.7% of training data. Follow-up *NeurIPS 2025* (arXiv 2510.21520): multi-participant LoRA brain-tuning, up to +50% alignment, 5× fMRI-data efficiency.
- **Brain-tuning, text** — Bilgin, Wehbe et al., *ICLR 2026* (OpenReview 07S1CPoQYP): fMRI-augmented training of **GPT-2 (124M) and LLaMA-2 (7B)** on Friends fMRI beats text-only baselines, scales with model size, generalizes across subjects/stimuli, and helps VL-Commonsense. This is the inversion, *for text LMs*, already published.
- **Causal necessity** — Merlin &amp; Toneva, *ICLR 2026* (arXiv 2603.23091): models trained to be *brain-misaligned at matched perplexity* do substantially worse across 200+ downstream tasks. Brain alignment is load-bearing, causally, not just correlated.
- **Auditory CNNs** — Freteault et al., *Imaging Neuroscience 2025*: fMRI fine-tuning of a 2.5M-param audio CNN improves 12/19 HEAR tasks, *especially under low data*. Direct support for the sample-efficiency mechanism.

**Verdict.** "Use fMRI as a training signal to improve an LM" is *established*, including for text. The bare inversion is **not novel**. What is *not* done: using brain alignment as the objective **inside knowledge distillation / compression at a matched student budget**, and separating "did we keep the alignment signal" from "did keeping it buy something practical (A3)." Every brain-tuning paper to date *fine-tunes and grows* a model (adds a brain module / extra loss); none *compresses* one. That gap is real but narrow, and it sits next to the live complication that compression alone often preserves alignment.

---

## 4. The idea, evolved: three candidate framings

Given §2's bound (brain = weak regularizer, valuable only in low-information regimes) and §3's scooping map, the surviving framings are:

- **F1 — Alignment-guided distillation at matched budget (the repo's current charter).** Use $\mathcal{L}_{\text{brain}}$ as a *what-to-preserve* signal during KD to a small student; the claim is a *better alignment/utility trade-off curve* than perplexity-only KD at the same compression ratio — not "alignment survives only if protected." This directly answers the 2602.07547 complication by competing on the curve, not the binary. Open, MSc-scoped, defensible.
- **F2 — Brain as a low-data / sample-efficiency regularizer.** First principles say a weak prior helps most when the data signal is weak. Test whether brain-regularized training beats a matched baseline *most* in the low-data regime (mirrors Freteault in vision). This is arguably the *cleanest* place a tiny-information signal can demonstrably matter, and it is under-explored for text LMs.
- **F3 — A differentiable brain *proxy* that needs no live fMRI (the ambitious one).** The deepest practical objection to all of this is that fMRI is scarce and you cannot have it in the loop at every training step. But if brain alignment ≈ abstraction geometry (Cheng 2026; LID), then an *abstraction surrogate* (an intrinsic-dimension / CKA-to-a-frozen-brain-encoder objective) — validated once against real fMRI — could carry most of the benefit without the data bottleneck. This decouples the *method* from the *data*, which is what would make it deployable and genuinely new.

**Recommendation (Erfan decides).** For an MSc finishing ~Aug 2026, **F1 + F2 as a hybrid** is the right scope: a defensible, falsifiable contribution that the literature has left open, runnable on the data now staged. **F3 is the stretch / future-work / PhD seed** — flag it, prototype the surrogate if F1/F2 clear, but don't bet the thesis on it.

---

## 5. Build it layer by layer: the experimental ladder (each layer gates the next)

The honest way to "build the idea layer by layer" is a ladder where each rung has a predeclared kill criterion and you only climb if the rung below holds. This also sequences the work from cheapest/most-foundational to most-ambitious.

- **Layer 0 — Does the signal exist beyond confounds, on real data? (tests A2; the charter's gating question.)** The synthetic pilot (E001) could *not* answer this by construction (L004). **E002** (this session) runs the real encoding-feasibility probe on Tuckute 2024: does an LM's contextual middle-layer representation predict LH-language-network BOLD *beyond* nuisance (length, position, static embeddings), under contiguous splits, vs an untrained-network control? **Kill:** if trained unique $R^2 \approx 0$ or $\approx$ untrained, the premise fails and the thesis reframes to measurement rigor. *(Result: see `experiments/E002_*.md`.)*
- **Layer 1 — Is the signal a *lever* we can move?** Brain-tune a small model (GPT-2 / Qwen-0.5B) on Tuckute/LeBel and verify the unique $R^2$ *moves* in the expected direction. Establishes that $\mathcal{L}_{\text{brain}}$ is trainable and controllable before we ask it to do anything useful. **Kill:** if alignment cannot be increased by direct optimization, no downstream framing is viable.
- **Layer 2 — Does preserved/induced alignment buy something? (tests A3 — the untested assumption.)** Compare a brain-regularized small model vs a matched baseline on OOD generalization and/or low-data sample-efficiency (this is F2). **Kill:** if gains stay confined to the alignment metric and never reach a downstream task, A3 fails and the practical claim dies.
- **Layer 3 — The distillation use-case (F1).** Alignment-guided KD vs perplexity-only KD vs structure-aware KD (MiniLM/MGSKD), matched compression ratio and budget, ≥3 seeds, reported as a trade-off curve with confound-corrected alignment. This is the headline thesis experiment; the E001 harness already implements the distillation + anti-confound machinery.
- **Layer 4 — The fMRI-free method (F3).** Replace the live-fMRI loss with an abstraction/LID/CKA surrogate validated against real fMRI at Layer 0–1; show it recovers most of the Layer-3 benefit without the data bottleneck. Stretch goal.

The point of the ladder: each rung is a small, honest experiment that *could* kill the thesis cheaply, and the order is forced by §2 (you cannot meaningfully test the distillation trade-off before you know the signal is real and movable).

---

## 6. Data staged this session (decision D013)

Two real, literature-used datasets are now on disk, chosen to cover both ends of the design space:

- **Tuckute 2024** (`data/tuckute2024/`, OSF ru38b, ~8 MB core): 1000 isolated baseline sentences × 5 LH language ROIs, 5-train-participant average, published noise ceiling (LangNetw nc ≈ 0.35; AlKhamissi's higher $r\approx0.56$ is a different normalization). Coarse (ROI-level) but real, high-ceiling, tiny, and — being isolated sentences — it *sidesteps* the temporal-autocorrelation leakage that plagues naturalistic data. **This is the Layer-0 / Layer-1 testbed and the fast real-data verdict.**
- **LeBel ds003020, subject UTS03** (`data/lebel_ds003020/preprocessed_data/UTS03/`, ~20 GB, 84 story HDF5s): the committed D008 powered within-subject naturalistic benchmark with a CC_norm noise ceiling. **This is the Layer-3 thesis-result benchmark**, and needs a time-series/FIR adapter (the documented next working step — *not* a config swap, contrary to earlier optimism).

The literature's own substrate is Narratives/Pereira/Fedorenko/Harry-Potter/Tuckute; our LeBel choice is *ours* (deliberate powered deep-sampling), worth remembering when comparing to published numbers.

---

## 7. What this changes about the thesis framing

1. Stop pitching "use fMRI to train an LM" — it is scooped (text included). Pitch the unscooped slice: **alignment-guided *distillation* at matched budget (F1), and/or brain as a *low-data* regularizer (F2)**, with the honest trade-off-curve framing that survives the "compression already preserves alignment" complication.
2. The first-principles bound (§2) is itself a *contribution* worth writing: a clear argument for *why* brain data can only be a weak regularizer, and therefore *where* (small/compressed/low-data) it can matter — which predicts the regimes the experiments should target. Step 7 now anchors it to the exact theorems of the Information-Theory course (MI generalization bound, DPI, conditional MI, rate-distortion), so the methods/related-work sections can cite established results rather than assert them — see `docs/06-theory-grounding.md`.
3. The ladder (§5) is the de-risking plan: cheap kills first. Layer 0 (E002) is done tonight; it tells us whether to climb at all.

