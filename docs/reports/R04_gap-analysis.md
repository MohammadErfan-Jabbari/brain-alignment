# R04 — Gap analysis: does "use the brain to train an LM" survive contact with the 2025–26 papers, and what is the single unscooped question left?

**Created:** 2026-06-10 (Session 5 — analysis). **Status:** living gap-analysis doc. **Full width, no hard wrap.**

**What this is.** R03 argued from first principles that brain data can only be a *weak prior*, mapped the idea into three framings (F1 distillation / F2 low-data regularizer / F3 fMRI-free proxy), and asserted — from a web-snippet survey — that the bare inversion is "largely already done." This report does the thing that survey could not: it reads the twelve relevant papers *in full* (ten arXiv PDFs on disk, two fetched — Bilgin via a local 14 MB PDF, Freteault via the PMC submitted version) and checks, claim by claim, whether R03's framing survives the actual evidence. The deliverable is a verdict on each framing, the single sharpest unscooped question, and a flagged list of places R03 itself needs correcting. This is an analysis session: every number below traces to a canonical note written this session from the real paper, never to an abstract or a guess.

The twelve notes are in `docs/literature/canonical/`. The short ids used throughout: `moussa-2025` (ICLR'25 speech), `moussa-2025b` (NeurIPS'25 multi-participant), `moussa-2025c` (Interspeech'25 processing-stages), `bilgin-2026` (ICLR'26 text LMs), `merlin-2026` (ICLR'26 causal), `oota-2026` (= arXiv 2602.07547, the compression counter-evidence), `cheng-2026` / `yu-2026` (intrinsic-dimension theory), `groger-2026` (Aristotelian/Platonic), `pirlot-2022` (vision DCCA precedent), `pepino-2026` and `freteault-2025` (audio).

---

## 1. The one structural picture that organizes everything

Before any verdict, lay the work out on the two axes that actually matter. Every paper in this literature does two independent things: it does *something* to the model's parameter budget, and it treats brain alignment in *one of two ways*. Make those the axes of a 2×2 and the entire field — and the gap — becomes visible at a glance.

- **Axis 1 — what happens to the parameter budget.** Either the intervention **grows** the model (fine-tune it, add LoRA adapters, bolt on a brain-encoding head — parameter count goes up or stays equal), or it **shrinks** the model (quantize, prune, or *distill* into a smaller student).
- **Axis 2 — the role of brain alignment.** Either alignment is **measured** (a dependent variable you observe after the fact, via an encoding model / brain score), or it is **optimized** (it sits inside the training objective, and a gradient flows through it into the weights).

|  | **alignment MEASURED** | **alignment OPTIMIZED** |
|---|---|---|
| **model GROWN** | the classical brain-score literature: Gao 2024, Oota 2023, Pepino 2026 (cross-model corr.), Cheng/Yu (correlational LID) | **brain-tuning** — Moussa (speech), **Bilgin (text)**, Merlin (text, causal). **SCOOPED.** |
| **model SHRUNK** | **Oota 2026 / 2602.07547** — alignment under quantization + pruning (the "counter-evidence"). KD *not even measured here*. | **F1: alignment-guided distillation at matched student budget. EMPTY CELL.** |

This single table is the whole argument. The bottom-right cell — *shrink the model while putting brain alignment in the objective* — is empty in the 2025–26 literature. That is the thesis. The reason R03 worried that the counter-evidence (`oota-2026`) might kill the idea is that it confused two different cells: `oota-2026` lives in *shrink × measure*, and F1 lives in *shrink × optimize*. They are not the same question, and the rest of this report makes that precise.

---

## 2. Verification at a glance — R03's claims vs what the papers actually say

Each row is a claim R03 makes about a paper, the verdict after a full read, and the real numbers. "OVERSTATED" means the direction is right but the strength or scope is inflated; "WRONG" means a factual error to fix.

| R03 claim (paraphrased) | Paper | Verdict | What the paper actually shows |
|---|---|---|---|
| L2 voxelwise loss, +30% late-language alignment, consistent downstream gains, <0.7% data | `moussa-2025` | **OVERSTATED** | +30% is **Wav2Vec2 / HuBERT only**; Whisper shows no significant late-language gain. Downstream up on **5/6** tasks (emotion recognition is the exception). L2, ~90M, <0.7% data: correct. |
| Multi-participant LoRA brain-tuning, up to +50% alignment, 5× data-efficiency | `moussa-2025b` | **CORRECT** | LoRA rank-8, per-participant L2 over ~30k voxels, **3 training participants** (not 88 — that was a hallucination in the old note, now fixed). +50% NC-normalized alignment, ~5× fMRI-data efficiency on held-out participants. Speech only. |
| Misalignment at matched perplexity hurts 200+ downstream tasks; alignment is causally load-bearing | `merlin-2026` | **MOSTLY CORRECT (+ understated)** | Gradient-reversal de-alignment hurts broadly across a 200+ dataset suite, but not uniformly (GPT-2/Harry-Potter p=0.055, n.s.). **R03 understates the positive arm:** brain-tuning *up* significantly *helps* downstream — stronger A3-in-principle support than R03 claims. **Text models** (BERT, GPT-2, Llama-3.2-1B). All at constant parameter count. |
| Text-LM brain-tuning exists: GPT-2 124M + LLaMA-2 7B on Friends fMRI beats text-only, scales with size, generalizes, helps VL-Commonsense | `bilgin-2026` | **MOSTLY CORRECT (2 corrections)** | Loss is **cosine similarity, not L2**. VL-Commonsense gain is **LLaMA-2-only** (0.560→0.584); **GPT-2 regresses** (0.381→0.375). "Scales with size" = two points, not a curve. Splits are **random TR shuffles, not contiguous**, and there is **no shuffled-brain control** — so the alignment gains are directionally credible but *not* anti-confound-verified. |
| Post-hoc compression preserves alignment "by default" (the key counter-evidence) | `oota-2026` | **OVERSTATED** | True only for **AWQ / SmoothQuant on ≥3B** models (e.g. Qwen2.5-3B IFG ~0.92–0.93, n.s. drop). **GPTQ degrades** it (Δ≈−0.020, p<0.001); **1–1.5B models and 50% pruning degrade** it. And critically: **KD / distillation is never tested** — they flag it as a limitation. |
| LID predicts brain-predictivity; brain-tuning causally raises intrinsic dimension + semantics | `cheng-2026` | **OVERSTATED (causal part)** | Correlational core is solid (higher **local** LID → higher predictivity, ρ≈0.76 fMRI). The causal claim rests on **one model, one layer, two subjects**. An RFF control shows high LID *alone* (without learned linguistic structure) is not sufficient. |
| Lower-intrinsic-dimension representations generalize better and align better | `yu-2026` | **CORRECT, but creates a contradiction** | Lower **local** LID → better AI–AI alignment (r≈−0.84), AI–brain alignment (r≈−0.84), ImageNet generalization (r≈−0.92). **Vision only.** See §5: this points the *opposite way* to `cheng-2026`, and both use *local* ID. |
| Neural-data DCCA regularizer (monkey IT) improved CNN accuracy + adversarial robustness (Federer 2022) | `pirlot-2022` | **WRONG on attribution + OVERSTATED** | It is **Pirlot et al. 2022, not Federer**; **monkey V1, not IT**. Accuracy +4.9pp and FGSM robustness improved — but a **shuffled-label control reproduces the accuracy gain within 0.4%**; only the *robustness* gain needs real neural structure. |
| fMRI fine-tuning of a 2.5M audio CNN improves 12/19 HEAR tasks, especially under low data | `freteault-2025` | **CORRECT on 12/19, OVERSTATED on "especially low data"** | 12/19 (Wilcoxon p<0.05) is verbatim. The low-data advantage is a **directional pattern with no interaction test and no matched non-brain control** — suggestive, not isolated. |

Two adjacent papers carry no R03 claim to check: `moussa-2025c` (brain-tuning flips the late-language alignment profile from bell-shaped to monotonically rising — structural support for A1) and `pepino-2026` (across 36 audio models, downstream quality correlates with auditory-cortex alignment at r≈0.90, replicated on two datasets — the strongest *correlational* A3 evidence, but cross-model correlation is not a within-model intervention). `groger-2026` is handled in §5.

---

## 3. Is the bare inversion scooped? Yes — text included — and the full Bilgin read settles it

R03 said this; the full reads confirm it without hedging. The cell *grow × optimize* is occupied for every modality the thesis could plausibly target:

- **Speech:** `moussa-2025` / `moussa-2025b` fine-tune ~90M speech encoders with an L2 voxelwise loss and report alignment and downstream gains.
- **Text:** `bilgin-2026` LoRA-fine-tunes **GPT-2 124M and LLaMA-2 7B** with a cosine-similarity brain loss on CNeuroMod Friends fMRI, with cross-subject and cross-stimulus evaluation and a downstream task (CoDa). This is the inversion, for text LMs, published.
- **Causally:** `merlin-2026` uses a gradient-reversal layer to drive text models (BERT, GPT-2, Llama-3.2-1B) *away* from alignment at matched perplexity and shows broad downstream damage — and the positive arm shows driving *toward* alignment helps.

So "use fMRI to train/shape an LM" as a bare claim is dead as a thesis. R03 was right to retire it, and the only correction needed there is to stop describing the Bilgin loss as L2 (it is cosine) and to qualify the VL-Commonsense result as LLaMA-only. The contribution has to be the empty cell, not the inversion.

---

## 4. Does F1 (alignment-guided distillation at matched budget) survive? Yes — it is the strongest surviving slice

F1 survives cleanly, and the structural map (§1) is why. Three independent facts converge on the same empty cell.

*First, every brain-tuning paper grows the model; none shrinks it.* `bilgin-2026` adds LoRA adapters plus an encoding head and only ever fine-tunes upward — the full read confirms the discussion lists "broader architectural sweeps" as future work and never mentions distillation. `moussa-*` add a trainable head to a frozen extractor. `merlin-2026` operates at constant parameter count. No paper in *grow × optimize* moves into *shrink × optimize*.

*Second, the one paper that does shrink (`oota-2026`) never optimizes alignment, and never even tests KD.* It measures how AWQ/GPTQ/SmoothQuant quantization and magnitude pruning affect an *observed* brain score. That is *shrink × measure*. It tells us nothing about what happens when alignment is a training target during compression, and — decisively — it does not test knowledge distillation at all. Distillation is a fundamentally different operation from quantization: quantization perturbs weights post-hoc around a fixed function, while KD re-fits a smaller function from scratch against the teacher's outputs, which is far more likely to discard mid-layer structure (and mid-layer structure is exactly where alignment lives — `oota-2023`). So R03's fear that `oota-2026` makes F1 a non-problem is **misplaced**: `oota-2026` answers a neighboring question in a different cell, and its own "preserved by default" headline is already qualified (GPTQ breaks it, sub-2B breaks it, pruning breaks it).

*Third, `merlin-2026` supplies the payoff F1 needs.* It establishes — causally, at constant size — that brain alignment is load-bearing for 200+ downstream capabilities. If standard KD silently destroys that alignment, `merlin-2026` predicts a measurable downstream cost, and an alignment-guided KD objective has a concrete capability to recover. F1 is therefore not just "an empty cell"; it is an empty cell with a *predicted mechanism* and a *predicted payoff*. That is the difference between a gap and an opportunity.

There is a formal backbone under all of this, and it is already mapped in `docs/06-theory-grounding.md` §3 (so I cite it rather than re-derive). The data-processing inequality, applied to compression, gives $I(Z_{\text{student}}; B) \le I(Y_{\text{teacher}}; B)$: a compressed student can only *lose* brain alignment relative to its teacher, never create it. `oota-2026`'s empirical finding that quantization barely dents alignment means that for quantization the bound is *nearly tight* — compression is near-alignment-lossless there. The whole bet of F1 is that knowledge distillation, being a far lossier transform than quantization, sits *well below* tightness by default — i.e. that ordinary KD throws away alignment the DPI permits it to keep — and that an alignment-guided objective pulls the student back toward the bound. This is why the question is quantitative (how far below tight is KD?), not binary.

The honest framing constraint R03 imposed still holds and is now sharpened: do not claim "alignment survives only if protected" (that is the binary `oota-2026` already complicates). Claim a **better alignment/utility trade-off curve at matched compression ratio** than perplexity-only KD — competing on the curve, not the binary. That curve is not a metaphor: it is the rate–distortion function (`docs/06-theory-grounding.md` §4), with the student's budget as *rate* and alignment loss as *distortion*, and F1's contribution is to move the operating point favorably.

---

## 5. F2 and F3 survive, but weaker than R03 implied — and one R03 mechanism claim is internally inconsistent

**F2 (brain as a low-data / sample-efficiency regularizer) — survives, but the precedents are softer than R03 leans on.** The first-principles case (a weak prior helps most when the data signal is weak; R03 §2 Step 6) is sound. But the empirical precedents R03 cites to support the *mechanism* each have a hole the full read exposed:

- `pirlot-2022` is the load-bearing vision precedent, and its **shuffled-label control reproduces the accuracy gain within 0.4%** — meaning the *accuracy / sample-efficiency* benefit there does **not** require real neural structure; only adversarial robustness does. That is close to the opposite of what F2 wants to borrow from it.
- `freteault-2025` shows a real 12/19 improvement but with **no interaction test and no matched non-brain fine-tuning control**, so its "especially under low data" cannot be cleanly attributed to the brain signal.
- `bilgin-2026` has a 1–40h data-scaling ablation but does **not** frame or test the contrastive prediction F2 actually rests on — that the brain prior helps *most* when *text* data is scarce.

So F2 is genuinely open *and* genuinely under-tested for text — which is both the opportunity (run the matched control everyone skipped) and the risk (the effect may evaporate under that control, exactly as it did for accuracy in `pirlot-2022`). The practical implication: F1 should carry more of the thesis weight than an even F1+F2 split; F2 is a strong secondary experiment, not a co-headline.

**F3 (fMRI-free differentiable proxy) — most novel, theoretically shakiest, and it exposes a real inconsistency in R03 §2.** R03's mechanism story leans on two intrinsic-dimension papers as if they agree. They do not:

- `cheng-2026` (language/speech, GRIDE estimator): **higher local intrinsic dimension → more brain-aligned.**
- `yu-2026` (vision, Levina–Bickel MLE): **lower local intrinsic dimension → more brain-aligned and more generalizable.**

Both are *local* intrinsic dimension, so the "local vs global" reconciliation does not save it. The sign of the LID↔alignment relationship is opposite across the two, plausibly because they differ in modality, estimator, and analysis frame (`cheng-2026` looks across layers within a model and intervenes; `yu-2026` correlates across pretrained models). R03 §2 (the "Abstraction" mechanism, line 71) cites both in adjacent sentences as jointly supporting "abstraction = lower dimension = better generalization" — but they point in opposite directions, so that synthesis is not earned. For F3 this is decisive: **you cannot build an intrinsic-dimension surrogate objective without first knowing whether to push LID up or down**, and the literature currently disagrees on the sign for the language case. On top of that, `groger-2026` shows the obvious alternative surrogate — a **CKA**-style global similarity to a frozen brain encoder — is **confounded by width and depth** and largely vanishes after null-calibration, with only *local neighborhood overlap* (mutual-kNN) surviving. So if F3 is pursued, the surrogate should be a null-calibrated neighborhood-overlap objective, not CKA and not a naive LID push, and its direction must be validated against real fMRI first. R03's verdict (F3 = stretch / PhD seed) stands, but the *reason* is sharper than "fMRI is scarce": the proxy's very direction is unsettled.

---

## 6. The single sharpest unscooped question

Collapsing §1–§5: the empty cell is *shrink × optimize*, `merlin-2026` says alignment is causally worth recovering, and `oota-2026` measured compression-robustness for everything **except** distillation. The sharpest question lives exactly at that intersection, and it factors into a cheap half and a thesis half:

> **(a, cheap, decisive, nobody has run it)** Does standard knowledge distillation — perplexity/logit KD into a smaller student — *preserve* or *destroy* the teacher's brain alignment? `oota-2026` answered this for quantization and pruning; it is unmeasured for KD, which is a far more destructive transform.
>
> **(b, the thesis)** If KD destroys it, does an **alignment-guided KD objective recover downstream capability at matched student budget** that perplexity-only KD loses — i.e. a better alignment/utility trade-off curve — where `merlin-2026` tells us the recoverable capability is real?

Why this is the right single question: it is the only one that is simultaneously (i) in the empty cell, (ii) anchored to a *causal* result rather than a correlation, (iii) cheap to begin — half (a) is a measurement on models we can already run, no training — and (iv) self-killing. If half (a) comes back "KD preserves alignment by default," then F1 collapses the same way `oota-2026` complicates the quantization story, and we learn that early and cheaply. If it comes back "KD destroys alignment," the thesis has a confirmed job and a predicted payoff. Either outcome is publishable and neither wastes compute.

This refines, rather than replaces, the repo charter. The charter's "alignment-guided distillation" was the right cell all along; what the papers add is the sharper edge — *frame it as recovering Merlin-style causal capability that KD silently sheds*, and *open with the KD-preservation measurement as the kill-test*, because that is the experiment that decides whether there is a thesis at all.

---

## 7. Corrections R03 needs (flagged, not yet applied)

The task was to flag where R03's claims need correcting against the papers. Here is the list; none are fatal to R03's thesis, but all are factual fixes. I can apply them on your go-ahead.

1. **Line 1 is corrupted** — an unrelated signal-processing transcript fragment ("you know that you are averaging the random transmitted symbols…") is prepended to the title. This is in the uncommitted working tree only; `git HEAD` has the clean title. Safe to restore.
2. **§3 / line 82 (Moussa ICLR'25):** "+30% … consistent downstream gains" should read **+30% for Wav2Vec2/HuBERT only (Whisper n.s.)**, downstream up on **5/6** tasks.
3. **§3 / line 83 (Bilgin):** the loss is **cosine similarity, not L2**; the VL-Commonsense gain is **LLaMA-2-only (GPT-2 regresses)**; "scales with model size" is **two points, not a curve**; and the splits are **random-shuffle, not contiguous, with no shuffled-brain control** — so cite it as scooping the inversion but *not* as an anti-confound-clean result.
4. **§3 / line 84 (Merlin):** broadly correct, but (a) not uniform (GPT-2/HP p=0.055) and (b) **understated** — add that brain-tuning *up* significantly helps downstream, which strengthens A3.
5. **§2 brake (c) / line 74 (Oota 2602.07547):** soften "preserves alignment by default" to **AWQ/SmoothQuant on ≥3B only; GPTQ, sub-2B, and pruning degrade it**, and add that **KD is untested** there (which is *why* F1 survives). Also note for bookkeeping: **2602.07547 *is* the `oota-2026` note** — same paper, two names — so do not double-count it as a separate work.
6. **§2 mechanism / line 71–72:** two fixes. (a) The vision precedent is **Pirlot et al. 2022, monkey V1**, not "Federer … monkey IT," and the **accuracy gain there survives a shuffled-label control** (only robustness needs real neural data) — so it is a weaker F2 precedent than stated. (b) `cheng-2026` (higher LID → aligned) and `yu-2026` (lower LID → aligned) **point in opposite directions and both use local ID**; they cannot be cited as jointly supporting one "lower-dimension-is-better" story. This is the internal inconsistency from §5.

---

## 8. What this changes about the ladder

R03's ladder is sound; the papers add one rung and re-weight two.

- **Insert a new Layer 2a (cheapest, decisive): measure whether perplexity-only KD preserves or destroys alignment**, the `oota-2026`-style measurement transposed to distillation. This is question 6(a), needs no training, and gates the entire distillation thesis. Run it before Layer 3.
- **Re-weight F2 below F1.** The low-data mechanism precedents (`pirlot-2022`, `freteault-2025`) do not cleanly survive their own controls, so F2 is a strong secondary experiment, not a co-headline. Build it with the matched non-brain-signal control that those papers skipped.
- **Hold F3 as a stretch, and if pursued, use a null-calibrated neighborhood-overlap surrogate** (per `groger-2026`), not CKA or a naive LID objective, and validate the surrogate's *direction* against real fMRI first (the `cheng-2026`/`yu-2026` sign problem).

The headline is unchanged and now better defended: the thesis lives in the empty *shrink × optimize* cell, framed as recovering the causally load-bearing alignment that knowledge distillation silently sheds.
