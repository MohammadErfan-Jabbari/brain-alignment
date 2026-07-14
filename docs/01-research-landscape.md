---
title: "Research Landscape — Brain-Alignment-Guided Distillation"
tags: [literature, reference]
---

# Research Landscape — Brain-Alignment-Guided Distillation

**Last updated:** 2026-07-14 (five-paper primary-PDF audit)
**Stage:** Map (frontier mapping). Literature is strong; this is a digest, not a fresh survey.

> Full provenance: `literature/_prior-work/` holds the 26 KB literature dossier and the 10 KB oracle
> review verbatim. Canonical per-paper notes are in `literature/canonical/`. This file is the map.

## The gap (one sentence)

The literature measures LLM–brain alignment and now also uses brain data to tune speech and text models. Feature distillation, privileged-information distillation, and on-policy hidden-state supervision are also active, so neither “brain data can guide a model” nor “training-time privileged information can help a smaller LM” remains an available broad novelty claim. The narrow unresolved question is whether a biological or synthetic-neural privileged target transfers useful information to a fixed smaller student beyond strong text-derived controls and then survives evaluation on real brain alignment. E016 directly tests that sequence and finds proxy optimization without real-brain transfer, shifting the contribution from a new positive algorithm to the measurement and transfer controls needed to prevent a proxy success from becoming a biological overclaim.

## Prior art, organized

### A. What the alignment signal is, and what drives it (anchors)

| Paper | Note | What it gives us |
|---|---|---|
| [Gao et al. 2024](literature/canonical/gao-2024_scaling-not-instruction-brain-alignment.md) | `gao-2024_scaling-not-instruction-brain-alignment` | Alignment rises with scale; instruction-tuning adds little at matched params → use a **base** teacher for naturalistic alignment. |
| [Oota et al. 2026](literature/canonical/oota-2026_brain-encoding-scale-compression.md) (= arXiv:2602.07547v1) | `oota-2026_brain-encoding-scale-compression` | On one fixed held-out Moth story (n=9), selected 3B checkpoints have raw ceiling-normalized encoding scores comparable to selected larger checkpoints, and several post-hoc AWQ/SmoothQuant conditions remain near FP16; GPTQ is often lower and Qwen-1.5B fails sharply at 50% pruning. These are descriptive, no-equivalence results with ambiguous layer selection, separate test standardization, no nuisance subtraction, and no formal task-alignment dissociation test. Controlled KD is not tested, so this is *shrink×measure*, not *shrink×optimize*. |
| [Oota et al. 2023](literature/canonical/oota-2023_joint-linguistic-processing-brain-lms.md) | `oota-2023_joint-linguistic-processing-brain-lms` | Alignment is built largely of **syntactic structure** that varies with layer depth → compression that destroys mid-layer syntax should be detectable. |
| [Aw & Toneva 2023](literature/canonical/aw-2023_narrative-summarization-improves-brain-alignment.md) | `aw-2023_narrative-summarization-improves-brain-alignment` | Training objective shapes brain-relevant structure **beyond** next-word prediction → alignment is learnable, not just emergent from scale. |
| Schwartz, Toneva, Wehbe 2019 | `schwartz-2019_inducing-brain-relevant-bias` | **Founding A3 paper.** MSE fine-tune of BERT on Harry Potter fMRI+MEG leaves GLUE intact or marginally up (claim is literally "does not harm"); no shuffled-brain, no matched-ppl, GLUE on only 2 of 5 variants. The honest prior E009 adjudicates. |
| [Negi, Oota et al. 2025](literature/canonical/negi-2025_brain-informed-finetuning-multilingual.md) (NeurIPS) | `negi-2025_brain-informed-finetuning-multilingual` | Bilingual fMRI full fine-tuning reports descriptive GLUE/CLUE and zero-shot multilingual gains. The three-fine-tuned-versus-one-vanilla voxel argmax has an approximately 75% exchangeable-null floor, and the highlighted regional cross-participant gains coexist with an aggregate difference of -0.00055 ± 0.00029. No training seeds, participant-population test, downstream shuffled-brain control, matched-quality baseline, or compression. |
| Moussa et al. 2025 (ICLR/NeurIPS) | `moussa-2025_brain-tuning-speech-lms` | **Closest prior to our loop.** L2-voxelwise fMRI loss fine-tunes ~90M speech LMs; +30% late-language alignment, consistent downstream gains, <0.7% of training data. Speech only; no compression/distillation at matched budget; text LMs untested → our contribution space. |
| [Zhang et al. 2026](literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md) (ACL) | `zhang-2026_temporal-precision-ecog-tuning` | Word-level high-gamma ECoG-tuning of speech encoders beats the paper's pretrained, permuted, temporal-mean, temporal-shuffle, BigSLM, and LLM controls. Full-target improvement ratios exceed Temporal-Mean by 6.8-16.8 percentage points. This is same-participant, same-podcast transfer with an underdescribed outer split, no training seeds, no declared inference unit, and no participant holdout; the pool-all-participants appendix is not cross-participant generalization. |
| Bilgin, Wehbe et al. 2026 (ICLR) | `bilgin-2026_brain-informed-lm-training` | **Text-LM brain-tuning exists (bare inversion scooped for text).** **Cosine-similarity** brain loss (not L2) LoRA-fine-tunes GPT-2 (124M) and LLaMA-2 (7B) on Friends fMRI; generalises across subjects/stimuli. Full-read caveats: VL-Commonsense gain is **LLaMA-only (GPT-2 regresses)**; "scales with size" = 2 points; splits are **random-shuffle, no shuffled-brain control** (not anti-confound-clean). Models **grow**, never compress → **F1 distillation gap still open.** |
| [Merlin et al. 2026](literature/canonical/merlin-2026_what-brain-data-adds.md) (CoNLL) | `merlin-2026_what-brain-data-adds` | Brain-Tuned BERT/GPT-2 models beat input-text and single-arm-hyperparameter-matched Stimulus-Tuned models on thresholded Holmes probe win rates; Jointly-Tuned has the best aggregate result and beats pretrained in three of four model-dataset combinations. Targets, losses, information, and optimization are not matched; model-training seeds and the Wilcoxon inference unit are not reported; no permutation, participant holdout, generation-quality, compression, or KD test. This is strong positive evidence for the implemented objective comparison, not closure of unique brain-information value. |
| [Xiao et al. 2026](literature/canonical/xiao-2026_brain-guided-llm-reasoning.md) | `xiao-2026_brain-guided-llm-reasoning` | **Brain-guided LLM behavior improvement now exists beyond language alignment.** NARI/NARF use task-fMRI-derived representation directions to intervene on or fine-tune LLMs for reasoning, with random-signal and label-only controls. This further closes broad "neural signals can improve LLMs" novelty. It still has no compression, no KD-only student, no matched-perplexity frontier, and no matched-information privileged-teacher control; it sharpens, rather than closes, the F1 student-budget gap. |
| [Merlin & Toneva 2024](literature/canonical/merlin-2024_beyond-next-word-brain-alignment.md) | `merlin-2024_beyond-next-word-brain-alignment` | A residual alignment component survives controls for word-level + next-word prediction → there is a **non-trivial target** standard KD won't capture. |
| [Proietti et al. 2025](literature/canonical/proietti-2025_brain-llm-alignment-input-attribution.md) | `proietti-2025_brain-llm-alignment-input-attribution` | **Input attribution: brain-alignment and next-word-prediction draw on largely DISTINCT word subsets** (IoU≈0.16 at top-10%, 5 architectures, 2 fMRI datasets); BA favors semantic/discourse, NWP favors syntax + edge-of-context. The mechanistic basis for our "beyond-perplexity" claim (E005/L014). **Lean moderately, not proof:** frozen models (passive, not causal), no Hadidi anti-confound, preprint. |
| [Alkhamissi 2025](literature/canonical/alkhamissi-2025_llms-outgrow-human-language-network.md) | `alkhamissi-2025_llms-outgrow-human-language-network` | Larger LMs can outgrow the human language network — bears on the saturation/scale story. |
| [Yin 2025](literature/canonical/yin-2025_associative-memory-improves-lm-brain-alignment.md) | `yin-2025_associative-memory-improves-lm-brain-alignment` | Associative-memory mechanisms improve alignment — a possible lever. |
| [Zhu 2025](literature/canonical/zhu-2025_probabilistic-neural-behavioral-representation-alignment.md) | `zhu-2025_probabilistic-neural-behavioral-representation-alignment` | Probabilistic neural/behavioral alignment — candidate measurement framing. |

### B. Counter-evidence (the brakes — these are mandatory, not optional)

| Paper | Note | The brake it applies |
|---|---|---|
| [Hadidi et al. 2026](literature/canonical/hadidi-2024_case-against-brainscore-reliance.md) (Nature Communications) | `hadidi-2024_case-against-brainscore-reliance` | On Pereira, Fedorenko, and Blank, shuffled splits make a block-autocorrelation baseline competitive with GPT-2XL and can reverse layer/model comparisons; under contiguous splits, pooling choice still changes rankings, while position/word-rate plus GloVe share more than 80% of GPT-2XL-explained variance. This is a scoped robustness warning, not a field-wide null: use block-held-out evaluation, appropriate pooling and regularization, and claim-relevant nuisance controls before interpreting brain scores. |
| [Jia 2026](literature/canonical/jia-2026_lpact-prediction-scores-not-enough.md) (arXiv, q-bio.NC) | `jia-2026_lpact-prediction-scores-not-enough` | **Strongest 2026 A2 challenge — and our scope-fence.** L-PACT four-gate audit (predictive/relational/mechanism-stripping/reliability-bounded); 146/146 real LM rows control_explained on Brain-Treebank/Podcast-ECoG/MEG-MASC; synthetic positive control passes all gates. **BUT frozen-encoding only, intracranial/MEG (no fMRI), NO perplexity-matched control, NO averaging confound, NO powered per-individual null** → pre-empts the *generic* "scores aren't enough" claim (cite, don't re-claim) but leaves all 3 of our brain-TUNING differentiators intact. Borrow: `random_matched_autocorr` control + source-audit closure test. |
| [Oota et al. 2024](literature/canonical/oota-2024_speech-lms-lack-brain-semantics.md) | `oota-2024_speech-lms-lack-brain-semantics` | **Anti-confound brake.** Aggregate alignment can mask different mechanisms (speech models' alignment was low-level phonology). → never report raw scores; decompose feature space. |
| [Guo et al. 2024](literature/canonical/guo-2024_eeg-cotrain-adversarial-robustness.md) | `guo-2024_eeg-cotrain-adversarial-robustness` | **A3 floor-setter.** EEG co-training (ResNet50, 720 models) → ~4pp mean (max 8pp) adversarial-robustness gain, but shuffled controls ALSO gain (brain-specific increment unquantified). → predeclare a **2–4pp MDE** for E009 (language likely lower) + the permuted-brain arm as the load-bearing control. Clean accuracy never tested. |
| Lage-Castellanos et al. 2019 | `lage-castellanos-2019_fmri-noise-ceiling` | **Novelty-scoping anchor.** Formal voxelwise fMRI noise ceiling ρ_NC=σ̂_β/σ̂_β̂; averaging *repetitions* suppresses noise variance → raises the achievable ceiling (within-subject; explicitly NOT group-level). Grounds our §4.2 ceiling-inflation math — so our novelty is NOT "averaging inflates ceilings" (known) but its **consequence for brain-*tuning* validity** (cross-subject is our extension). |
| Nili et al. 2014 (RSA) | — | RSA group noise ceilings compare each subject's RDM to the group-average RDM (higher ceiling). The "averaging raises apparent ceiling" principle is long-standing in neuro methods → cite to scope novelty. |
| Moussa & Toneva 2025 (NeurIPS) | `moussa-2025` (speech) | **Closest anti-averaging prior.** Per-participant independent gradient steps beat averaged-loss/averaged-response targets (+50% alignment, 5× data-eff) → corroborates that averaging matters, but frames it as a data-efficiency design choice, NOT as a confound invalidating averaged-target gains (our framing). |

### C. Distillation / compression baselines (the method must compose with these)

| Paper | Note | Role |
|---|---|---|
| [Wang 2020](literature/canonical/wang-2020_minilm-self-attention-distillation.md) (MiniLM) | `wang-2020_minilm-self-attention-distillation` | Relation-space KD; reference architecture; alignment loss must work with decoupled teacher/student dims. |
| [Liu 2022](literature/canonical/liu-2022_multi-granularity-structural-kd.md) (MGSKD) | `liu-2022_multi-granularity-structural-kd` | Hierarchical layer routing; brain alignment slots into the sample/discourse tier. |
| [Fu 2021](literature/canonical/fu-2021_lrc-bert-contrastive-kd.md) (LRC-BERT) | `fu-2021_lrc-bert-contrastive-kd` | Angular/contrastive transfer; brain alignment is geometric, may compose naturally. |
| [Zhang 2025](literature/canonical/zhang-2025_aligndistil-token-level-policy-distillation.md) (AlignDistil) | `zhang-2025_aligndistil-token-level-policy-distillation` | Alignment-as-token-level-distillation; suggests alignment losses can decompose without per-step recordings. |
| [Zhou 2022](literature/canonical/zhou-2022_bert-learns-to-teach-metadistil.md) (MetaDistil) | `zhou-2022_bert-learns-to-teach-metadistil` | Learned-teacher distillation; possible meta-objective. |
| [Jia 2024](literature/canonical/jia-2024_adversarial-moment-matching-llm-distillation.md) | `jia-2024_adversarial-moment-matching-llm-distillation` | Token-prob copying is a weak proxy; behavioral/value imitation is stronger — supports a behavioral target. |
| [Saadi & Wang 2026](literature/canonical/saadi-2026_task-tangent-feature-distillation-llms.md) | `saadi-2026_task-tangent-feature-distillation-llms` | Flex-KD makes modern feature-level LLM distillation a live baseline family: task-relevant functional subspaces, not raw feature matching. Pressure on E016: a TRIBE gain can be read as generic useful dense-target geometry unless it beats `textfeat`. |
| [Penaloza et al. 2026](literature/canonical/penaloza-2026_privileged-information-distillation-lms.md) | `penaloza-2026_privileged-information-distillation-lms` | Generic privileged-information distillation for LMs is active in agentic tool-use settings. Closes "first PI distillation for LMs"; does not use brain/neural targets or fixed-budget language KD. |
| [Wu et al. 2026](literature/canonical/wu-2026_pride-privileged-information-distillation-dialogue.md) (PRIDE) | `wu-2026_pride-privileged-information-distillation-dialogue` | Closest PI-enhanced KD pressure: training-only expert/future-context PI improves smaller empathetic-dialogue students. Closes "training-only PI can improve smaller LMs"; leaves the biological/synthetic-neural target and matched-information-control question open. |
| [OPRD](https://arxiv.org/abs/2606.06021), [PHF](https://arxiv.org/abs/2606.29340), and 2026 on-policy/context self-distillation | Current frontier family | Representation-level and privileged hidden-process distillation are active algorithmic claims. They use model-internal or solution-conditioned teachers rather than neural measurements, but they prevent E016 from claiming novelty for dense hidden targets alone. The relevant distinction is the neural target plus a real-brain transfer gate. |
| [Rethinking On-Policy Self-Distillation](https://arxiv.org/abs/2607.05184) and [DemoPSD](https://arxiv.org/abs/2607.02502) | Current frontier family | Privileged context can create shortcuts or fail to transfer to the unconditioned student. This makes transfer failure a first-class outcome rather than an afterthought and supports reporting E016 as a controlled proxy-to-endpoint failure. |

### D. Systems-side constraints

| Paper | Note | Constraint it raises |
|---|---|---|
| [Ji 2025](literature/canonical/ji-2025_calibration-data-pruning-llms.md) | `ji-2025_calibration-data-pruning-llms` | Calibration **data distribution** matters more than the pruning algorithm → calibration corpus is a first-order design variable. |
| [Tang 2025](literature/canonical/tang-2025_razorattention-kv-cache-compression.md) (RazorAttention) | `tang-2025_razorattention-kv-cache-compression` | Functional head asymmetry → do brain-alignment heads overlap retrieval heads? Possible selective-compression lever. |

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
- PI-enhanced KD and feature-KD follow-ups now staged as scout-grade notes; full PDF reads only if E016 positive branch survives or reviewers press that adjacency.


## Related
- [`status.md`](./status.md) — the canonical status board
