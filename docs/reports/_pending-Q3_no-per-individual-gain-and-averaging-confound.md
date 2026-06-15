# R06 — No per-individual brain-specific alignment gain is inducible beyond perplexity; cross-subject averaging manufactures the apparent gain

**Answers Q3 (F1, the headline). Verdict: ❌ NULL per-individual, well-powered, and stable across capacity, objective, substrate, and parameterisation. The positive contribution is methodological: a measurement-validity finding (cross-subject target-averaging manufactures apparent brain-specificity) plus the control protocol that detects it (matched-perplexity, a per-kind permuted-brain twin, and per-subject inference).** This report states current truth only. The discovery order (E005 looked like a win, then collapsed) lives in `map.md`, `timeline/`, and `decisions/`, not here. Sources: `experiments/E005`, `E008`, `E011`, `E013`, `E013b`, `E017`, `E006`; lessons L011 / L015 / L016 / L041.

This is a finding-report under the report convention (D036): one claim, Q-tagged, current-truth-only, fixed skeleton. It is the synthesis of Q3. The history of how the field (and we) got here lives in `map.md` (the journey tree), `timeline/`, and `decisions/`.

## The question

Does alignment-guided knowledge distillation, measured against the control a *brain-specific* claim actually requires (matched perplexity plus a permuted-brain twin), produce a per-individual gain in held-out brain alignment beyond what a perplexity-matched baseline already gives, when each participant is treated as an independent replication unit rather than as one cross-subject average?

## The design (what makes the number trustworthy)

The verdict statistic is the paired difference `kd_brain − kd_brain_permuted` at matched perplexity (the permuted-brain twin is the matched-ppl brain-specificity null; the base model and perplexity cancel by construction), aggregated per participant as the median over 3 seeds × 5 folds, on Tuckute's 5 LH-language ROIs [E008]. Inference is crossed over two axes, subjects (n=9) and stimulus-folds (n=5), because all participants see the same 1000 sentences on the same fold partition, so a single lucky stimulus fold can masquerade as agreement across nominally independent brains. The conservative fold-clustered CI plus leave-one-fold-out is the headline, never the subject t-CI alone [E008]. Controls: rotating contiguous folds (no tune/eval leakage), frozen input embeddings (LoRA), a train-4 vs held-out-5 subject split to expose data reuse, and an SNR rank-correlation control. Kill criteria were predeclared before running [E008].

## The evidence

- The per-individual effect is a centered null: mean `e_u` = **+0.00010**, subject t-CI95 **[−0.00037, +0.00058]**, sign **5/9** positive (p=0.50) [E008].
- It fails the conservative test too: fold-clustered mean +0.00026, t-CI95 **[−0.0004, +0.0009]**, bootstrap p(≤0)=0.111, and leave-one-fold-out fails on every drop [E008].
- The null is well-powered, not a noise-floor shrug: subject-axis MDE(80%) ≈ **+0.0006 to +0.0013**, power 1.0 at δ=+0.003; a true per-subject effect of E005's size would have shown about 9/9 strongly positive at t≈19, instead of 5/9 centered at zero [E008].
- The collapse: E005's apparent **+0.0081** falls to **+0.00010** per-subject, roughly **80× smaller** [E005, E008]. E005's headline was 15 cells (3 seeds × 5 folds) over one 5-UID-averaged target, which is pseudo-replication, not n=15 (L015); one outlier fold (fold4/seed0) carried 52% of it; honest fold-level re-analysis gives median +0.0034 with a CI including 0 [E005].
- The averaged effect is a property of the average, not of brains: the four subjects E005 literally averaged are individually null or negative (train-4 mean **−0.00010**) [E008].
- The null holds across every escape axis: capacity (E011, heavy LoRA r64/6ep) stays null at +0.0004 [E011]; objective (E013b, contrastive/InfoNCE) −0.0002 at matched ppl [E013b]; substrate (E013, voxelwise λ-sweep), where the lever never beats base or its permuted twin, a single-subject mechanism failure [E013]; parameterisation (E017, full fine-tuning, n=9) real−perm +0.0003, p=0.27 [E017].

## The verdict

Alignment-guided KD shows no detectable per-individual brain-specific alignment gain beyond perplexity (n=9, mean +0.00010, 95% CI [−0.0004, +0.0006], well-powered, MDE≈+0.0006), and the null holds across capacity, objective, substrate, and parameterisation [E008, E011, E013, E013b, E017]. The apparent gain exists only against a cross-subject-averaged target, where it is a higher-SNR measurement of the shared stimulus-evoked response: inflated about 1.7× by the averaging-driven noise-ceiling rise (NC≈0.49) and about 2.4× by one outlier fold, not per-person brain alignment [E008]. The positive result is therefore methodological. Cross-subject target-averaging manufactures apparent brain-specificity (the +0.0081 to +0.00010 collapse; L016), and the controls that expose it (matched perplexity, a per-kind permuted-brain twin, and per-subject inference with crossed subject/fold clustering) are exactly the controls the brain-tuning literature omits. This stands on the bedrock that the signal itself is real and powered: the trained−untrained unique-R² gap is +0.021 (gpt2) / +0.028 (Qwen) on about 11.4k reliable voxels [E006].

## The caveats (carried in the claim, not a footnote)

- The claim is operational: "not *inducible* beyond perplexity via the readouts tested (linear-ridge / MSE / contrastive, LoRA and full-FT)." The stronger information-theoretic reading ("the residual is task-independent noise") rests on Y⊥θ\*|S as an assumption, not a result (L041).
- "Brain-specific" is relative to the nuisance set actually subtracted; surprisal and imageability are not conditioned in (L011 / L012), so a residual low-level nuisance cannot be fully excluded. This weakens only the averaged-target positive, never the per-individual null.
- The one grounded path to a per-individual positive is higher per-subject SNR (within-subject repeats), not more averaging [E008].
