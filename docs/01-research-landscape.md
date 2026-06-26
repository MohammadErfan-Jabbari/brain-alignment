---
title: "Research Landscape — Brain-Alignment-Guided Distillation"
tags: [literature, reference]
---

# Research Landscape — Brain-Alignment-Guided Distillation

**Last updated:** 2026-06-08 (seeded from the prior Nexus dossier + oracle review)
**Stage:** Map (frontier mapping). Literature is strong; this is a digest, not a fresh survey.

> Full provenance: `literature/_prior-work/` holds the 26 KB literature dossier and the 10 KB oracle
> review verbatim. Canonical per-paper notes are in `literature/canonical/`. This file is the map.

## The gap (one sentence)

The literature *measures* LLM↔brain alignment, and — as of 2025–26 — *also uses fMRI as a training
signal* (brain-tuning: Moussa/Toneva for speech, Bilgin/Wehbe for text LMs). What no one has done is
use brain alignment as the objective **in distillation/compression at a matched student budget**, then
test whether *preserving* it (vs a perplexity-only student) buys anything practical. That untested loop
is the contribution space — and it must survive one live complication: brain alignment is already fairly
robust to *post-hoc* compression (arXiv 2602.07547), so the thesis must show distillation differs, or
that it improves the alignment/utility *trade-off curve* at matched compression. See R03.

## Prior art, organized

### A. What the alignment signal is, and what drives it (anchors)

| Paper | Note | What it gives us |
|---|---|---|
| Gao et al. 2024 | `gao-2024_scaling-not-instruction-brain-alignment` | Alignment rises with scale; instruction-tuning adds little at matched params → use a **base** teacher for naturalistic alignment. |
| Oota et al. 2026 (= arXiv 2602.07547) | `oota-2026_brain-encoding-scale-compression` | Benchmark perf and brain alignment **partially dissociate** under compression; alignment robust to AWQ/SmoothQuant **only on ≥3B** (GPTQ, sub-2B, and 50% pruning degrade it). **KD/distillation is never tested** — only post-hoc quantization+pruning → this is *shrink×measure*, not *shrink×optimize*, so it does **not** close the F1 gap. The compression "counter-evidence" and this row are the **same paper**. |
| Oota et al. 2023 | `oota-2023_joint-linguistic-processing-brain-lms` | Alignment is built largely of **syntactic structure** that varies with layer depth → compression that destroys mid-layer syntax should be detectable. |
| Aw & Toneva 2023 | `aw-2023_narrative-summarization-improves-brain-alignment` | Training objective shapes brain-relevant structure **beyond** next-word prediction → alignment is learnable, not just emergent from scale. |
| Schwartz, Toneva, Wehbe 2019 | `schwartz-2019_inducing-brain-relevant-bias` | **Founding A3 paper.** MSE fine-tune of BERT on Harry Potter fMRI+MEG leaves GLUE intact or marginally up (claim is literally "does not harm"); no shuffled-brain, no matched-ppl, GLUE on only 2 of 5 variants. The honest prior E009 adjudicates. |
| Negi, Oota et al. 2025 (NeurIPS) | `negi-2025_brain-informed-finetuning-multilingual` | **Closest A3 prior art.** Bilingual brain-tuning (full FT) of BERT/mBERT/XLM-R/XGLM/LLaMA-3.2-1B → GLUE/CLUE +0.5–1.6pp avg, zero-shot to 5 unseen languages. **Baseline = vanilla pretrained only; no perplexity-matched control, no shuffled-brain downstream null, no compression** → the gap E009 closes. |
| Moussa et al. 2025 (ICLR/NeurIPS) | `moussa-2025_brain-tuning-speech-lms` | **Closest prior to our loop.** L2-voxelwise fMRI loss fine-tunes ~90M speech LMs; +30% late-language alignment, consistent downstream gains, <0.7% of training data. Speech only; no compression/distillation at matched budget; text LMs untested → our contribution space. |
| Bilgin, Wehbe et al. 2026 (ICLR) | `bilgin-2026_brain-informed-lm-training` | **Text-LM brain-tuning exists (bare inversion scooped for text).** **Cosine-similarity** brain loss (not L2) LoRA-fine-tunes GPT-2 (124M) and LLaMA-2 (7B) on Friends fMRI; generalises across subjects/stimuli. Full-read caveats: VL-Commonsense gain is **LLaMA-only (GPT-2 regresses)**; "scales with size" = 2 points; splits are **random-shuffle, no shuffled-brain control** (not anti-confound-clean). Models **grow**, never compress → **F1 distillation gap still open.** |
| Merlin & Toneva 2024 | `merlin-2024_beyond-next-word-brain-alignment` | A residual alignment component survives controls for word-level + next-word prediction → there is a **non-trivial target** standard KD won't capture. |
| Proietti et al. 2025 | `proietti-2025_brain-llm-alignment-input-attribution` | **Input attribution: brain-alignment and next-word-prediction draw on largely DISTINCT word subsets** (IoU≈0.16 at top-10%, 5 architectures, 2 fMRI datasets); BA favors semantic/discourse, NWP favors syntax + edge-of-context. The mechanistic basis for our "beyond-perplexity" claim (E005/L014). **Lean moderately, not proof:** frozen models (passive, not causal), no Hadidi anti-confound, preprint. |
| Alkhamissi 2025 | `alkhamissi-2025_llms-outgrow-human-language-network` | Larger LMs can outgrow the human language network — bears on the saturation/scale story. |
| Yin 2025 | `yin-2025_associative-memory-improves-lm-brain-alignment` | Associative-memory mechanisms improve alignment — a possible lever. |
| Zhu 2025 | `zhu-2025_probabilistic-neural-behavioral-representation-alignment` | Probabilistic neural/behavioral alignment — candidate measurement framing. |

### B. Counter-evidence (the brakes — these are mandatory, not optional)

| Paper | Note | The brake it applies |
|---|---|---|
| Feghhi et al. 2024 | `feghhi-2024_case-against-over-reliance-brain-scores` | **Mandatory protocol override.** Shuffled splits inflate scores via temporal autocorrelation; untrained GPT-2 "explains" data via length/position. → contiguous splits, nuisance baselines, gains shown *after* confound subtraction. **NOW published: Hadidi/Feghhi Nature Comms 2026 (10.1038/s41467-026-72253-7)** — cite the published version. |
| Jia 2026 (arXiv, q-bio.NC) | `jia-2026_lpact-prediction-scores-not-enough` | **Strongest 2026 A2 challenge — and our scope-fence.** L-PACT four-gate audit (predictive/relational/mechanism-stripping/reliability-bounded); 146/146 real LM rows control_explained on Brain-Treebank/Podcast-ECoG/MEG-MASC; synthetic positive control passes all gates. **BUT frozen-encoding only, intracranial/MEG (no fMRI), NO perplexity-matched control, NO averaging confound, NO powered per-individual null** → pre-empts the *generic* "scores aren't enough" claim (cite, don't re-claim) but leaves all 3 of our brain-TUNING differentiators intact. Borrow: `random_matched_autocorr` control + source-audit closure test. |
| Oota et al. 2024 | `oota-2024_speech-lms-lack-brain-semantics` | **Anti-confound brake.** Aggregate alignment can mask different mechanisms (speech models' alignment was low-level phonology). → never report raw scores; decompose feature space. |
| Guo et al. 2024 | `guo-2024_eeg-cotrain-adversarial-robustness` | **A3 floor-setter.** EEG co-training (ResNet50, 720 models) → ~4pp mean (max 8pp) adversarial-robustness gain, but shuffled controls ALSO gain (brain-specific increment unquantified). → predeclare a **2–4pp MDE** for E009 (language likely lower) + the permuted-brain arm as the load-bearing control. Clean accuracy never tested. |
| Lage-Castellanos et al. 2019 | `lage-castellanos-2019_fmri-noise-ceiling` | **Novelty-scoping anchor.** Formal voxelwise fMRI noise ceiling ρ_NC=σ̂_β/σ̂_β̂; averaging *repetitions* suppresses noise variance → raises the achievable ceiling (within-subject; explicitly NOT group-level). Grounds our §4.2 ceiling-inflation math — so our novelty is NOT "averaging inflates ceilings" (known) but its **consequence for brain-*tuning* validity** (cross-subject is our extension). |
| Nili et al. 2014 (RSA) | — | RSA group noise ceilings compare each subject's RDM to the group-average RDM (higher ceiling). The "averaging raises apparent ceiling" principle is long-standing in neuro methods → cite to scope novelty. |
| Moussa & Toneva 2025 (NeurIPS) | `moussa-2025` (speech) | **Closest anti-averaging prior.** Per-participant independent gradient steps beat averaged-loss/averaged-response targets (+50% alignment, 5× data-eff) → corroborates that averaging matters, but frames it as a data-efficiency design choice, NOT as a confound invalidating averaged-target gains (our framing). |

### C. Distillation / compression baselines (the method must compose with these)

| Paper | Note | Role |
|---|---|---|
| Wang 2020 (MiniLM) | `wang-2020_minilm-self-attention-distillation` | Relation-space KD; reference architecture; alignment loss must work with decoupled teacher/student dims. |
| Liu 2022 (MGSKD) | `liu-2022_multi-granularity-structural-kd` | Hierarchical layer routing; brain alignment slots into the sample/discourse tier. |
| Fu 2021 (LRC-BERT) | `fu-2021_lrc-bert-contrastive-kd` | Angular/contrastive transfer; brain alignment is geometric, may compose naturally. |
| Zhang 2025 (AlignDistil) | `zhang-2025_aligndistil-token-level-policy-distillation` | Alignment-as-token-level-distillation; suggests alignment losses can decompose without per-step recordings. |
| Zhou 2022 (MetaDistil) | `zhou-2022_bert-learns-to-teach-metadistil` | Learned-teacher distillation; possible meta-objective. |
| Jia 2024 | `jia-2024_adversarial-moment-matching-llm-distillation` | Token-prob copying is a weak proxy; behavioral/value imitation is stronger — supports a behavioral target. |

### D. Systems-side constraints

| Paper | Note | Constraint it raises |
|---|---|---|
| Ji 2025 | `ji-2025_calibration-data-pruning-llms` | Calibration **data distribution** matters more than the pruning algorithm → calibration corpus is a first-order design variable. |
| Tang 2025 (RazorAttention) | `tang-2025_razorattention-kv-cache-compression` | Functional head asymmetry → do brain-alignment heads overlap retrieval heads? Possible selective-compression lever. |

### E. Measurement & theory tools

- `kornblith-2019_cka-similarity-representations` — CKA, a candidate differentiable-ish alignment proxy.
- `huh-2024_platonic-representation-hypothesis` — why cross-model representations may converge to a
  shared (brain-predictive) geometry; theoretical backing for generalization.
- **Course theory grounding** ([`06-theory-grounding.md`](06-theory-grounding.md)) — Erfan's MSc Information-Theory coursework supplies the *formal, proved* tools the argument leans on, so methods/related-work can cite rather than assert: the **MI generalization bound** $\overline{\mathrm{gen}}\le\sqrt{2\sigma^2 I(W;Z^n)/n}$ (the exact form of R03's weak-prior bound); the **data-processing inequality** $I(Z_{\text{student}};B)\le I(Y_{\text{teacher}};B)$ (compression can only *lose* alignment — the formal backing for engaging the 2602.07547 trade-off, not the binary); **conditional mutual information** $I(\text{LM};B\mid\text{nuisance})$ (exactly the "unique R²" the §B anti-confound protocol measures); and the **rate-distortion function** $R(D)=\min_{P_{\hat S\mid S}:\,\mathbb{E}[d]\le D}I(S;\hat S)$ (the F1 alignment-vs-rate trade-off curve).

## Baseline matrix the thesis must run (from the frontier map)

1. Perplexity-only KD (matched student size, data, optimization budget).
2. Structure-aware KD (MiniLM- or MGSKD-class).
3. Alignment-guided objective at the same compression ratio.
4. Hybrid (alignment + utility) under matched resources.

## Stage-3 guardrails (predeclared, non-negotiable)

- Matched compression ratio and training budget across all baselines.
- All-seed reporting (≥ 3 seeds) for neural predictivity and utility.
- Predeclare the minimum margin over perplexity-only KD before claiming a contribution.
- Anti-confound evaluation: contiguous (not shuffled) splits; nuisance-feature controls (length,
  position, static embeddings); report gains after confound subtraction.
- Predeclare the calibration-data policy for pruning/quantization baselines.

**Must-not-claim:** no causal cognitive equivalence from an encoding-model gain; no universal
robustness from one benchmark family.

## Known risks / kill scenarios

- Alignment may be purely emergent from parameter count with no transferable geometric signature →
  distillation kills it → thesis dead.
- The effect may be small (+0.03–0.05 R²) and the measurement matrix enormous → is it worth proving?
- "Edge" is unspecified → reviewers ask "why care?" Need a named deployment scenario.
- **SPOF:** a language-fMRI benchmark with adequate power and an open license must be accessible.
  None is staged on disk yet (see [`02-environment.md`](02-environment.md)). This is the first thing to de-risk.
- The alignment↔utility trade-off might be a step function (collapses below a threshold, trivial
  above) → reduces the thesis to "don't over-compress."

## New-search needs (not covered by the frozen dossier)

- Language-fMRI datasets: Pereira 2018, Nastase *Narratives*, LeBel 2023, Fedorenko lab releases —
  which are open, sized, and English/multilingual? **Power analysis required.**
- Recent (2026) brain-alignment-for-compression work to confirm the gap is still open.


## Related
- [`ladder.md`](./ladder.md) — the canonical status board
- [`map.md`](./map.md) — code system (Q/E/A/D/L) & journey map
