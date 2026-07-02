---
title: "R08: The brain-alignment objective has not shown a reliable held-out alignment gain"
tags: [Q2, report]
aliases: [R08]
---

# R08: The brain-alignment objective has not shown a reliable held-out alignment gain

**Answers Q2. Verdict: ❌ no demonstrated reliable alignment gain.** E004 built the differentiable brain-alignment loss and tested whether optimizing it could raise held-out alignment. The strongest result was a small Qwen co-trained-MSE advantage over its own permuted-brain twin: $\Delta_{\text{spec}}=+0.0032$. The first read treated 3 seeds × 5 folds as 15 independent cells and gave a CI excluding zero. The corrected S25 read uses the honest inference unit, the five held-out folds, and the interval includes zero: $+0.0032$ with 95% CI $[-0.0023,+0.0086]$ [E004]. Fold 4 carries most of the summed signal, the unpaired permuted-null test already failed, and the LeBel follow-up substrate could not resolve an effect of this size. The result is therefore not a reliable training effect. It is also not evidence that the true effect is exactly zero: the valid unit has only five folds, and that is too little power to exclude a small effect around $+0.003$ [E004].

R08 sits after two settled steps. R06 established that the alignment signal is real and measurable. R07 showed that ordinary distillation leaves alignment headroom below the teacher, but that headroom is entangled with language-model quality. The next question is whether the brain objective can *move* the alignment score. On the recorded evidence, reliable movement has not been demonstrated. Sources: E004 for the objective test, E006 for the powered-substrate/MDE decision, L011/L012/L015 for the quality and inference-unit lessons.

## The question

The objective question is stricter than the measurement question. R06 asked whether a trained model's representation predicts brain activity beyond a nuisance floor. Q2 asks whether changing the model with a brain-alignment loss changes the held-out alignment score in the intended direction.

Write $A(\theta)$ for the held-out unique $R^2$ of a model with parameters $\theta$ under the same encoding evaluation used in R06. A brain-tuned model starts at the base model $\theta_0$ and is optimized on training stimuli with

$$
\mathcal{L}(\theta) = \mathcal{L}_{\text{LM}}(\theta) + \lambda_{\text{brain}}\mathcal{L}_{\text{brain}}(\theta).
$$

The basic movement is

$$
\Delta_{\text{base}} = A(\theta_{\text{brain}}) - A(\theta_0).
$$

That is not enough for a brain-specific claim. Fine-tuning on the same sentences can change alignment for ordinary reasons: domain adaptation, language-model degradation, or a smoother perturbation of the representation. The decisive comparison is therefore each brain-tuned arm against its own matched shuffled-target twin,

$$
\Delta_{\text{spec}} = A(\theta_{\text{real brain}}) - A(\theta_{\text{permuted brain}}).
$$

The permuted twin keeps the same training recipe, loss scale, text, architecture, folds, and seeds, but breaks the stimulus-to-brain correspondence. If $\Delta_{\text{spec}}>0$ at the independent inference unit, the real brain target changed held-out alignment more than the same objective with meaningless brain labels. That is the narrow effect E004 tries to demonstrate.

A usable training signal needs three things at once: the movement must be positive, specific to the real brain target rather than the shuffled target, and reliable at the unit that is actually independent. E004 gave a small positive point estimate on the best arm. It did not clear the reliability condition.

## The design

E004 uses the Tuckute 2024 sentence benchmark: 1000 isolated sentences, five left-hemisphere language ROIs, and the same unique-$R^2$ apparatus used by R06's ROI screen. It is a small, fast substrate, useful for discovering whether a loss form can move the score at all, but not a powered final test of a small gain [E004].

The loss family tested the design options that were live at the time:

| Arm | Brain objective | Readout | Role |
|---|---|---|---|
| `mse` | squared error from a learned linear readout to fMRI | co-trained | primary, theory-preferred |
| `cos` | cosine distance to fMRI | co-trained | text-brain tuning precedent |
| `pearson` | negative squared correlation | co-trained | correlation-form precedent |
| `frozen` | squared error through a ridge readout fit before tuning | frozen | tests whether features move under a fixed brain map |
| `cka` | linear CKA between hidden states and fMRI | none | geometry probe |

The primary candidate was Qwen2.5-0.5B with the co-trained-MSE loss. That choice was not arbitrary. The evaluation score is unique $R^2$, and under a linear-Gaussian readout the corresponding training surrogate is squared prediction error through a linear brain readout, the differentiable form closest to the evaluation metric [E004] [D016]. The co-trained readout also won the empirical horse race: among the tested forms, only Qwen `mse` showed a positive real-minus-permuted contrast [E004].

Two design choices matter for interpreting the result. First, the split is five rotating contiguous outer folds. Each item is held out exactly once, so the score is evaluated only on stimuli the model did not optimize against, and the obvious item-order shift in the benchmark is averaged over folds rather than hidden inside one train/test split [E004]. Second, tuning uses LoRA rather than full fine-tuning. Full fine-tuning at useful $\lambda$ destroyed perplexity; LoRA preserved the language model enough that a change in alignment could still be read as a representation effect rather than as a broken model [E004] [L012].

The design is still only a screen. It has five ROIs and five folds. Before running, E004's own power analysis estimated that Qwen had about 31% power for a $+0.003$ absolute movement and about 79% power for $+0.006$ [E004]. So a null on the absolute movement would never prove the effect absent. The only plausible positive was the more sensitive paired real-vs-permuted contrast.

## The evidence

The verdict table starts with the strongest substrate, Qwen2.5-0.5B. All values are held-out unique $R^2$ changes on the rotating folds, with bootstrap CIs from the original 15 seed-fold cells unless noted [E004].

| Qwen arm | $\Delta_{\text{base}}$ [CI] | Real minus own permuted twin | Arm minus `lm_only` | Held-out ppl | Read |
|---|---:|---:|---:|---:|---|
| `mse` | +0.0025 [−0.0011,+0.0067] | +0.0032 [+0.0006,+0.0058] | +0.0056 [+0.0031,+0.0089] | 205 | small apparent specific effect [E004] |
| `frozen` | −0.0018 [−0.0055,+0.0013] | −0.0009 [−0.0058,+0.0023] | +0.0012 [−0.0005,+0.0028] | 184 | no specificity [E004] |
| `lm_only` | −0.0031 [−0.0063,+0.0005] | n/a | n/a | 256 | ordinary same-text tuning [E004] |

Three facts follow.

First, no arm reliably raised alignment above the untuned base. The best absolute movement, Qwen `mse`, is $+0.0025$ and its interval includes zero. Fine-tuning on 800 Tuckute sentences, even with LoRA, tends to perturb the model and double perplexity relative to the base; the question becomes whether the real brain target degrades alignment less, or preserves a brain-specific part better, than the matched null [E004].

Second, the co-trained-MSE loss was the only promising form. Qwen `mse` beat its own permuted twin by $+0.0032$ under the original paired cell bootstrap. The frozen-readout arm behaved like a generic regularizer and did not beat its own permuted twin. The geometric and cosine arms on GPT-2 were worse. So D010's practical loss-form decision survives: if the project uses a brain-alignment loss at all, co-trained MSE is the sensible form to carry forward [E004] [D016].

Third, the specific effect is tiny and quality-entangled. The `mse` arm also has much better held-out perplexity than `lm_only` (205 vs 256), so arm-minus-`lm_only` cannot by itself prove brain specificity. The real check is real brain target versus permuted brain target. That check gives the $+0.0032$ point estimate, but it has to be read at the right unit [E004] [L011].

## The inference-unit correction

The original E004 report treated the 3 seeds × 5 folds as 15 independent draws. That produced the optimistic line:

| Unit used for the interval | Mean | CI | Excludes zero? |
|---|---:|---:|---|
| Flat 15-cell bootstrap | +0.00316 | [+0.00062,+0.00584] | yes [E004] |
| Honest fold unit, seeds averaged within fold | +0.00316 | [−0.00227,+0.00858] | no [E004] |

The mean is unchanged. The uncertainty changes because the unit changes.

The five folds are not fifteen biological or stimulus-independent replications. They are one rotating partition of the same 1000-sentence, train-participant-averaged target. Seeds reuse the same data. Treating all seed-fold cells as independent understates the error, the same pseudo-replication problem L015 caught in E005. Once seeds are averaged inside each fold and the fold is treated as the inference unit, the interval includes zero [E004] [L015].

The per-fold paired contrasts make the instability visible:

| Fold | Qwen `mse` minus `mse_perm` | Source |
|---:|---:|---|
| 0 | −0.0007 | [E004] |
| 1 | +0.0003 | [E004] |
| 2 | +0.0045 | [E004] |
| 3 | +0.0016 | [E004] |
| 4 | +0.0101 | [E004] |

Fold 4 carries 64% of the summed signal. Dropping fold 4 leaves a mean of $+0.0014$ [E004]. That pattern is not a reliable training effect. It is a small positive trend whose apparent certainty came from counting correlated cells as independent evidence.

The original report already contained one warning sign: `summary.mse.beats_permuted_null = False`. The paired contrast was the more sensitive statistic and the right one to inspect, but the unpaired permuted-null exceedance failing means E004 never had the broad specificity pattern one would want from a strong effect [E004].

## Why E007 was not built

The predeclared path after a suggestive Tuckute result was a powered voxelwise re-test on LeBel. E006 first asked whether the LeBel substrate carried the alignment signal at all. It did: the trained-minus-untrained gap was $+0.0207$ for GPT-2 and $+0.0277$ for Qwen across 11,442 reliable voxels [E006]. So the substrate was alive for measurement.

The objective-induced-gain question failed the power check. E006 estimated the minimum detectable effect for the planned E007 mean-over-voxels statistic at about $+0.013$ for GPT-2 and $+0.015$ for Qwen, roughly four to five times larger than E004's $+0.003$ specific contrast [E006]. A heavier TR-level tuning run would therefore have been structurally unable to resolve the effect scale that motivated it.

There is one honest nuance. E006's MDE is for the crude mean-over-voxels statistic, while E004's signal appeared in a paired real-minus-permuted contrast that removes common fold-level noise. A paired E007 statistic could have been better powered. That remains an unrun possibility, not evidence. The recorded decision was to stop the bespoke re-test and move to the matched-perplexity distillation experiments, where the same kind of permuted-twin comparison is tested inside the actual use case [E006] [D016].

## The verdict

Q2 asks whether optimizing $\mathcal{L}_{\text{brain}}$ reliably raises held-out alignment. The current answer is **no demonstrated reliable gain**.

E004 did build a real optimization objective, and it identified the only plausible loss form: co-trained MSE on the strongest aligner. But the evidence for movement rests on a small $+0.0032$ real-minus-permuted point estimate, fold 4 carries most of that estimate, and the valid fold-level interval includes zero [E004]. The Tuckute screen therefore does not demonstrate that optimizing the brain loss moves held-out alignment.

The negative is deliberately scoped. It does not say the population effect is zero, that co-trained MSE is useless in all regimes, or that a paired voxelwise version could never work. It says the recorded evidence does not establish a reliable training effect. That is enough for the report sequence: after R06's positive, measurement and optimization separate. The signal is real. The objective built from it has not yet shown reliable control over held-out alignment.

## Caveats

- **Small effects are unresolved, not disproven.** Five folds cannot exclude a true effect around $+0.003$. The honest wording is "undemonstrated" rather than "zero" [E004].
- **The Tuckute screen is coarse.** Five ROIs make E004 useful for loss-form discovery, not for a decisive small-effect null. The powered LeBel measurement was strong for A2, but its planned objective-induced-gain statistic could not resolve the E004-scale effect [E006].
- **Perplexity remains entangled.** E003 established that alignment tracks language-model quality; E004's best arm also differs in perplexity from `lm_only`. Only matched-perplexity designs can attribute a gain to the brain objective cleanly [L011].
- **The loss form is still informative.** Co-trained MSE remains the best supported form of $\mathcal{L}_{\text{brain}}$ in this repo. The report rejects the demonstrated-gain claim, not the engineering fact that this was the only form with a positive specific contrast [E004] [D016].
- **R08 stops before the per-individual question.** E005/E008 and the later robustness experiments belong to R09-R14. R08 supplies the bridge: a real measured signal does not automatically become a controllable training signal.

## Related

- [`ladder.md`](../ladder.md) - canonical status board
- [`map.md`](../map.md) - code system and journey map
- [`R06_alignment-signal-is-real-beyond-confounds.md`](R06_alignment-signal-is-real-beyond-confounds.md) - the signal is real
- [`R07_plain-kd-does-not-preserve-alignment.md`](R07_plain-kd-does-not-preserve-alignment.md) - plain KD leaves headroom but quality is entangled
- [`../experiments/E004_brain-loss-lever-test.md`](../experiments/E004_brain-loss-lever-test.md) - source experiment
- [`../experiments/E006_lebel-voxelwise-feasibility.md`](../experiments/E006_lebel-voxelwise-feasibility.md) - powered substrate and E007 MDE
