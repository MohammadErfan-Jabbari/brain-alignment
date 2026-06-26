---
title: "R06: The LM↔brain alignment signal is real, beyond confounds"
tags: [Q0, report]
aliases: [R06]
---

# R06: The LM↔brain alignment signal is real, beyond confounds. A trained language model's middle layer predicts held-out brain activity well above an untrained control after the full nuisance subtraction

**Answers Q0 (A2). Verdict: ✅ PASS, and powered at voxel scale.** A trained language model's middle-layer representation carries unique variance about real human language-network activity that survives a low-level nuisance regression under contiguous splits, and that a same-architecture *untrained* network does not carry. The effect is small in absolute R² but unambiguous: at voxel scale the trained−untrained gap is **+0.021 (gpt2) / +0.028 (Qwen)** with tight bootstrap CIs and 95–99% of reliable voxels positive [E006](../experiments/E006_lebel-voxelwise-feasibility.md). This report states current truth only; the order in which we learned it (an ROI screen first, then the powered voxelwise confirmation) lives in [`map.md`](../map.md), `timeline/`, and `decisions/`, not here. Sources: `experiments/E002`, `E006`; lessons L003, L007, L011/L012.

This is a finding-report under the report convention (D036): one claim, Q-tagged, current-truth-only. It is also the **foundation the rest of the report set stands on**: every later report (the lever, the per-individual null, the quality law, the ceiling) is a qualification of *this* positive, and every one of them reuses the measurement apparatus defined here. The history of how the arc actually unfolded (the wrong turns, the order they happened) lives in [`map.md`](../map.md) (the journey tree) and `timeline/`, not in any report.

## The question

Does a trained language model's contextual middle-layer representation predict human language-network brain activity *beyond* what is already explained by low-level confounds (utterance length, speech rate, static word identity, position), under an anti-confound protocol that does not let temporal or split leakage inflate the score, and is that unique signal materially larger than what a same-architecture *untrained* network produces from the same nuisance-controlled fit?

The question matters because the entire thesis premise rests on it. If a trained LM aligns to the brain only through length, rate, and word identity, then "brain alignment" is a confound and there is nothing to optimize, preserve, or distill. A2 is the gate: it must pass on real neural data, or the program reframes to measurement rigor (the charter kill condition).

## The design (and the apparatus the whole program reuses)

The measurement is an **encoding model**: ridge regression from a model's per-stimulus features to measured brain activity, scored out-of-sample. The quantity we claim is never raw predictive R² but **unique R²**, the variance the language-model features add *on top of* the nuisance set, defined as the difference of two cross-validated fits,

$$
\text{unique }R^2 \;=\; R^2\big([Z_{\text{nuis}},\,\text{LM}]\big) \;-\; R^2\big([Z_{\text{nuis}}]\big),
$$

where $Z_{\text{nuis}}$ is the nuisance set [E002](../experiments/E002_tuckute-encoding-feasibility.md). A positive unique R² says the contextual representation explains brain activity that length, rate, and static word identity cannot.

This section gives the apparatus conceptually; the full measurement pipeline drawn stage by stage as a diagram lives with the evidence, in the experiment files — `experiments/E002` for the ROI screen and `experiments/E006` for the powered voxelwise run.

**What this quantity is, formally.** Unique R² is the linear-Gaussian estimator of a *conditional mutual information*; the conditional MI object is defined in [`06-theory-grounding.md`](../06-theory-grounding.md) §3 (Information Theory for ML, lecture 4). For a triple $(X,Y,Z)$, the conditional mutual information is

$$
I(X;Y\mid Z) = H(Y\mid Z) - H(Y\mid X,Z),
$$

the dependence between $X$ and $Y$ that survives once the context $Z$ is known. It is the right object here because plain mutual information $I(X;Y)$ conflates two cases: a genuine dependence between $X$ and $Y$, and a spurious one in which the two are merely co-driven by a common source $Z$. In the second case $X \perp Y \mid Z$, so $I(X;Y\mid Z)=0$ even while $I(X;Y)>0$; conditioning on $Z$ is what tells them apart.

The chain rule splits the question into a baseline and an increment. For a cheap baseline $X$, an expensive learned representation $Y$, and a target $Z$,

$$
I\big((X,Y);Z\big) = I(X;Z) + I(Y;Z\mid X),
$$

so the value of the representation is the incremental term $I(Y;Z\mid X)$: what it explains about the target beyond the baseline. Identifying $X$ with the nuisance, $Y$ with the LM middle layer, and $Z$ with brain activity, A2 is the claim

$$
I\big(\text{LM};\,B \mid Z_{\text{nuis}}\big) > 0,
$$

which unique R² estimates with ridge. For jointly Gaussian variables, conditional MI is a monotone function of the squared partial correlation $\rho^2_{XY\cdot Z}$ (standard result; see [`06-theory-grounding.md`](../06-theory-grounding.md) §3 for the object, Cover & Thomas 2006 §8 for the Gaussian closed form),

$$
I(X;Y\mid Z) = -\tfrac{1}{2}\ln\!\big(1-\rho^2_{XY\cdot Z}\big).
$$

The report's unique R² is the *semipartial* R² — the raw increment $R^2([Z,\text{LM}]) - R^2([Z])$ — which differs from the partial $\rho^2$ by the factor $1/(1-R^2([Z]))$. Both are zero together, so $\text{unique }R^2 > 0 \iff \rho^2_{XY\cdot Z} > 0 \iff I(\text{LM};B\mid Z_{\text{nuis}}) > 0$; the biconditional the argument needs holds regardless. Because ridge is linear, this captures the *linearly decodable* conditional dependence — a lower bound on the true $I$ at the population level, which is the appropriate target for a thesis about the linear map.

**Which **$Z$**, and why it scopes the whole report set.** A2 conditions on $Z_{\text{nuis}}$, a *weak* proxy for the stimulus: low-level features only. So A2 establishes that the signal is real beyond low-level confound, not beyond the stimulus as a common cause. The strong conditioning, $Z = \mathbb{E}[Y\mid S]$ (the full stimulus-predictable response), is the ceiling question (E020); there the conditional term collapses to $\approx 0$, which is the per-individual null. Same chain rule, stronger $Z$.

The verdict statistic is the **trained−untrained gap**, not a trained model's absolute unique R² [E006, L007]. In papers with a weaker nuisance set, an untrained network can score slightly positive on naturalistic data via a shared-cause structure: the stimulus $S$ drives both the BOLD signal $B$ and the untrained features $U$ (via random projection of the token sequence), so a residual dependence

$$
\operatorname{Cov}(U,\,B \mid Z_{\text{nuis}}) \neq 0
$$

persists when $Z_{\text{nuis}}$ only partially conditions on $S$ — not because $U \to B$ causally, but because both share the same temporal cause. Our strong nuisance (eng1000 + full phone tier) absorbs most of this floor: in E006 the untrained unique R² is −0.017, not positive. Even so, the gap is the right statistic because it directly isolates what *language training* adds over random initialisation under identical nuisance and splits — controlling for architecture, tokenisation, and any residual temporal structure the nuisance does not capture [E006, L007]. Both arms pass through the byte-identical nuisance subtraction, so $R^2([Z_{\text{nuis}}])$ cancels in the difference,

$$
\text{gap} = R^2\!\bigl([Z_{\text{nuis}},\,\text{LM}_{\text{trained}}]\bigr) \;-\; R^2\!\bigl([Z_{\text{nuis}},\,\text{LM}_{\text{untrained}}]\bigr),
$$

leaving a direct comparison of what each representation adds to the same nuisance floor. The gap is the quantity reported throughout [E002, E006].

Three controls make that gap trustworthy, and they are the repo standard from here on.

**Contiguous splits.** Train and test are divided in blocks, never by shuffling: block cross-validation on the ROI screen, and whole-story-held-out cross-validation on the voxelwise run. Adjacent timepoints in fMRI are strongly correlated, so a shuffled split would put near-duplicate samples on both sides and leak the test answer into training, inflating the score. Holding out whole stories removes that leak (the L003 fix for shuffle-inflated alignment) [E002, E006].

**A capacity-fair nuisance floor.** Two *wide* feature blocks compete in the fit, the contextual LM block and a high-dimensional static block, and either can absorb more variance simply by carrying more dimensions, regardless of content. So before the fit those two blocks are reduced by PCA to the same rank, fit on the training fold only; the few-dimensional low-level scalars have no such advantage and stay raw. This is the L004 fix: when the LM wins, it wins on content, not on dimension count. The floor itself, the set of confounds subtracted in both arms, is small on the ROI screen: length, position, and the mean static word embedding. It expands on the voxelwise run to word-rate, phoneme-rate (from the TextGrid phone tier), word-duration, word-length, log word-frequency, and the 985-dimensional eng1000 static embedding, each FIR-delayed by 1 to 4 TRs to match the hemodynamic lag [E002, E006].

**A held-out noise ceiling.** On the voxelwise run we keep only reliable voxels, and we choose them on data the encoding fit never sees: a separate story repeated ten times, held out of the cross-validation pool entirely, and scored by split-half reliability. Selecting voxels on the same data used to score them would be circular and would bias the estimate upward (double-dipping); selecting on the held-out repeats avoids it [E006](../experiments/E006_lebel-voxelwise-feasibility.md).

Surprisal is deliberately left *out* of the nuisance set: it is itself an LM-derived quantity, so subtracting it would over-subtract the very construct under test (log word-frequency, a static lexical scalar, is distinct and is subtracted) [E006](../experiments/E006_lebel-voxelwise-feasibility.md). A *permuted-brain twin* (the shuffled-target null that tests brain-*specificity*) is not part of A2; it enters later, where the question is whether the signal can be *moved* (Q2) rather than whether it is *real* (here).

## The evidence

The ROI screen passes on every model tested [E002](../experiments/E002_tuckute-encoding-feasibility.md). On Tuckute 2024's five left-hemisphere language ROIs (1000 isolated sentences, 5 contiguous folds):

| Model | Best layer | Trained unique R² (mean ± SD) | Untrained unique R² | Trained−untrained gap | NC-normalised |
|---|---|---|---|---|---|
| GPT-2 (12L) | L7 | +0.020 ± 0.008 | −0.011 | +0.030 | 0.056 |
| GPT-2-medium (24L) | L14 | +0.019 ± 0.005 | −0.014 | +0.033 | 0.053 |
| Qwen2.5-0.5B (24L) | L12 | +0.036 ± 0.010 | −0.014 | +0.050 | 0.102 |

GPT-2 and GPT-2-medium are comparable; Qwen is substantially stronger, at ~10% of the noise ceiling (NC ≈ 0.353). The untrained control is negative at every layer and every seed across all three models. The signal is positive across all mid-layer positions (a broad plateau, not a sharp peak), and absent from random features [E002](../experiments/E002_tuckute-encoding-feasibility.md).

The powered voxelwise run confirms it where the ROI screen could only hint [E006](../experiments/E006_lebel-voxelwise-feasibility.md). On LeBel UTS03 (20 naturalistic stories, 5 story-level folds, 11,442 voxels at split-half reliability > 0.5 on a held-out repeated story):

| Model | Layer | Trained−untrained gap [95% CI] | % reliable voxels gap > 0 | Untrained unique R² |
|---|---|---|---|---|
| GPT-2 | L7 | +0.021 [+0.0205, +0.0209] | 95% | −0.017 |
| Qwen2.5-0.5B | L12 | +0.028 [+0.0274, +0.0280] | 99% | −0.017 |

The gap is carried by language training, not by architecture or the rate and temporal structure the nuisance floor absorbs [E006](../experiments/E006_lebel-voxelwise-feasibility.md).

Three controls keep the positive honest. The ROI screen uses isolated sentences, removing the temporal-autocorrelation inflation that contaminates naturalistic time-series — a lower-bound-friendly setting that makes its positive *harder*, not easier, to obtain [E002](../experiments/E002_tuckute-encoding-feasibility.md). The voxelwise run reintroduces naturalistic stimuli but adds two further controls: whole-story-held-out CV prevents temporal leakage (test TRs are never adjacent to training TRs, so the model cannot exploit hemodynamic autocorrelation); and voxel selection on a held-out repeated story prevents selection bias (reliable voxels are identified on data the encoding fit never sees, so the score cannot be inflated by voxels that happen to correlate with the model by chance). Feghhi and Hadidi (2026) showed that speech rate, phoneme rate, word duration, word length, and static lexical features (eng1000's 985-d context-free semantic vectors) are the dominant low-level predictors of auditory cortex responses — the features most likely to produce a false positive if left uncontrolled. We subtract exactly this set. The trained model's contextual gap survives that subtraction, so the signal cannot be attributed to surface acoustics or static word identity [E006](../experiments/E006_lebel-voxelwise-feasibility.md).

## The verdict

The LM↔brain alignment signal is real, beyond confounds, on real neural data: a trained model's middle layer adds unique, out-of-sample variance about language-network activity that a same-architecture untrained network does not, after a capacity-fair low-level nuisance regression under contiguous splits, with the trained−untrained gap at **+0.021–0.028** and tight CIs excluding zero on 95–99% of reliable voxels [E002, E006]. Qwen, the most recent model and the strongest aligner of the three, aligns substantially more strongly than either GPT-2 variant — consistent with a quality ordering, though the two GPT-2 variants are nearly tied despite a 3× parameter difference [E002](../experiments/E002_tuckute-encoding-feasibility.md). A2 holds, and at voxel scale it holds with power.

This is the one load-bearing *positive* of the thesis, and everything downstream is a qualification of it. It licenses asking whether the signal can be *moved* by training (Q2, the lever) and whether moving it *buys* anything (Q3/Q4); it does not pre-judge those, which are answered (negatively, and at matched perplexity) in their own reports. The discipline to keep straight, stated once here because the whole arc turns on it: **real ≠ movable ≠ useful.** A2 establishes only the first.

## The caveats (carried in the claim, not a footnote)

- "Beyond confounds" means beyond the nuisance set *actually subtracted*. Surprisal and imageability are not conditioned in (L011/L012); surprisal is held out on purpose to avoid over-subtracting the construct, so a residual contextual low-level nuisance cannot be fully excluded by the nuisance floor alone. What *does* bound it is the untrained same-architecture control: it sees the identical nuisance and scores negative, so architecture plus rate plus residual temporal structure cannot manufacture the gap. The claim is a statement about the gap, and the gap is clean.
- The signal is small in absolute R², a few percent, ≈5–10% of the noise ceiling at ROI scale [E002](../experiments/E002_tuckute-encoding-feasibility.md). That is the expected scale at this resolution, not a weakness; the honest reading is the trained−untrained gap and the NC-normalised fraction, never raw R². At voxel scale the gap is both small and overwhelmingly consistent in sign (95–99% of voxels), which is the stronger evidence.
- The ROI screen (E002) is coarse (five dimensions, train-participant-averaged) and is a screen, not the verdict. The powered claim is the voxelwise run (E006). Where the two could disagree, E006 wins. E006's 11,442 voxels are selected by split-half reliability on naturalistic story listening, not by a language localizer; this trades anatomical specificity for statistical power. In practice, voxels reliably driven by story listening are predominantly language-responsive, consistent with the ROI screen [E002, E006].
- A2 says the signal is real and measurable. It says nothing about whether optimizing a brain-alignment loss raises held-out alignment (the lever is fragile, in its own report) or whether induced alignment transfers to a per-individual or practical gain (it does not, at matched perplexity — its own report). Reading A2's positive as evidence for those is the exact over-claim the rest of the report set exists to prevent.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
