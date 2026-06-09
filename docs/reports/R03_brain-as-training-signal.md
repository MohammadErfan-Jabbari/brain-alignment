# R03 — Brain as a Training Signal: a first-principles interrogation of the inversion idea, and where the real open space is

**Created:** 2026-06-10 (Session 4 — working/analysis). **Status:** living direction doc. **Full width, no hard wrap.**

**What this is.** Erfan's overnight brain dump proposed *inverting* the usual brain-alignment direction: instead of only *measuring* that LLM middle layers map linearly to fMRI, *use* the fMRI (plus that mapping) as a *training signal* to shape or train the LM. He asked to reason this from first principles — learning theory, the mechanics of training deep nets and LLMs, probabilistic generative models — and to build the idea layer by layer, evolving or deleting parts. This report does that, confronts the idea with the 2025–26 literature (which partly scoops it), and lays out a falsifiable experimental ladder. It is a recommendation and a map, not a decision; the kill criteria are real.

---

## 1. The idea, stated precisely

The literature establishes: for a human and an LLM processing the same language stimulus, there exists a linear map $W$ such that $\text{fMRI} \approx W \cdot h_\ell(\text{stimulus})$, where $h_\ell$ is a middle-layer LLM representation. This map is reliable and is the standard "brain score" / encoding-model instrument. The inversion: treat the brain as a *target* the model should be pulled toward during training, i.e. add a term $\mathcal{L}_{\text{brain}}$ that rewards the model for having representations that predict (or are predicted by) recorded brain activity, and ask whether a model trained with it is *better* in some practical sense than one trained without.

This is a clean, real idea. It is also — and we have to say this plainly because the job is to help Erfan decide well, not to flatter the idea — **largely already done as of 2025–26.** The honest contribution is a narrower, sharper slice, and the first-principles work below is what locates that slice.

---

## 2. First principles: can brain data train a language model at all?

**What an LM is.** A language model is a probabilistic generative model of text: it learns $p_\theta(x)$ by maximum likelihood on next-token prediction over trillions of tokens. Its gradient signal is enormous, dense, and self-supervised — every token is a label.

**What the brain signal is.** fMRI is a slow (TR ≈ 2 s), noisy, indirect (BOLD hemodynamics) measurement of neural activity, with a *noise ceiling* that caps explainable variance at roughly $r \approx 0.3$–$0.56$ even for a perfect model. A typical language-fMRI dataset has $10^3$–$10^4$ stimulus points per subject, not $10^{12}$. The mutual information between the recorded brain signal and the stimulus that is *not already present in the text itself* is therefore tiny.

**The bound this implies.** Brain data cannot be a *primary* training target that competes with next-token prediction — there is nowhere near enough information in it, and what there is, is noisy and redundant with the text. Any framing of the form "train the LM *on* the brain" collapses, under an information budget, into "*bias* an LM that is mostly trained on text." So the only coherent role for $\mathcal{L}_{\text{brain}}$ is as an **inductive bias / regularizer / selection signal**: it does not teach the model new facts about the task, it nudges *which* of the many text-consistent solutions the model settles into. This reframe is the single most important first-principles consequence, and it determines everything downstream — including *where* the idea can possibly add value (low-information regimes: small models, scarce data, compression) and where it cannot (large models with abundant data, where the text signal already dominates).

**Why a bias toward the brain might help (the mechanism, Feynman-style).** Two non-exclusive stories, both with 2026 evidence:
1. *Abstraction.* Brain alignment in middle layers tracks *meaning abstraction*, not next-word statistics (Cheng et al. 2026: a layer's local intrinsic dimension predicts its brain-predictivity; brain-tuning *causally raises* intrinsic dimension and semantic content together). Independently, lower-intrinsic-dimension representations generalize better and align better, across artificial and biological nets (arXiv 2601.22722). So the brain is a *pointer* to a more abstract, more generalizable region of representation space. Aligning to it = regularizing toward abstraction.
2. *Human invariances / robustness.* The brain's representation encodes the invariances a human uses to understand language robustly. A model biased toward that geometry might be more robust to distribution shift and more sample-efficient. This is the vision precedent: a neural-data (monkey IT) regularizer via Deep CCA improved CNN accuracy *and* adversarial robustness (Federer et al. 2022).

**Where the mechanism breaks (the brakes, mandatory).** (a) If the brain-predictive structure is mostly *nuisance* — sentence length, position, low-level lexical identity — then aligning to it teaches nothing useful; this is the Feghhi 2024 / Oota 2024 brake and is exactly why every number in this thesis must be a *unique* variance after nuisance subtraction under contiguous splits (L003). (b) If the abstraction geometry is already reached by scale alone — brain alignment *saturates* around 3B parameters (Oota 2026) — then the bias is redundant above that scale. (c) If post-hoc compression already preserves alignment by default (arXiv 2602.07547, the key 2026 counter-evidence), then "protect alignment during compression" may be solving a non-problem unless framed as a *trade-off curve*, not a *preserve-vs-destroy* binary. These three brakes jointly pin the value of the idea to a specific corner: **small / under-trained / compressed models, in low-data regimes** — precisely where a weak-but-well-structured prior matters most.

---

## 3. The literature already does most of the bare inversion (be honest about it)

A focused 2023–26 survey of NeurIPS/ICML/ICLR/ACL + neuro venues (full shortlist in the session timeline) returns:

- **Brain-tuning, speech** — Moussa, Klakow, Toneva, *ICLR 2025* (`moussa-2025_brain-tuning-speech-lms`): an L2 voxelwise fMRI loss fine-tunes ~90M speech LMs, +30% late-language alignment, consistent downstream gains, using <0.7% of training data. Follow-up *NeurIPS 2025* (arXiv 2510.21520): multi-participant LoRA brain-tuning, up to +50% alignment, 5× fMRI-data efficiency.
- **Brain-tuning, text** — Bilgin, Wehbe et al., *ICLR 2026* (OpenReview 07S1CPoQYP): fMRI-augmented training of **GPT-2 (124M) and LLaMA-2 (7B)** on Friends fMRI beats text-only baselines, scales with model size, generalizes across subjects/stimuli, and helps VL-Commonsense. This is the inversion, *for text LMs*, already published.
- **Causal necessity** — Merlin & Toneva, *ICLR 2026* (arXiv 2603.23091): models trained to be *brain-misaligned at matched perplexity* do substantially worse across 200+ downstream tasks. Brain alignment is load-bearing, causally, not just correlated.
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
2. The first-principles bound (§2) is itself a *contribution* worth writing: a clear argument for *why* brain data can only be a weak regularizer, and therefore *where* (small/compressed/low-data) it can matter — which predicts the regimes the experiments should target.
3. The ladder (§5) is the de-risking plan: cheap kills first. Layer 0 (E002) is done tonight; it tells us whether to climb at all.
