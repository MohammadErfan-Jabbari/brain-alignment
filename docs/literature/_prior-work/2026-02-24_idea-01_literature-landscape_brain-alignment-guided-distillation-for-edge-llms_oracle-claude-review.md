Empty oracle review. That's a gap itself. Here's the full decomposition.

---

## 1) Atomic Decomposition Validity

The dossier correctly decomposes into four load-bearing atoms:

**Atom 1: Brain-alignment signal is real and language-relevant.** Not "models score well on brain benchmarks" but "the scored signal reflects linguistic processing, not nuisance." [inference] The dossier correctly identifies this via Feghhi 2024 and Oota 2024 counter-evidence, but no experiment in the dossier's own pipeline has tested this atom independently. It's inherited from other people's work on other models.

**Atom 2: This signal survives compression when explicitly protected.** The Oota 2026 anchor says alignment *sometimes* survives compression, but under what regimes and whether the survival is because of or despite the compression objective is unresolved. [inference] The dossier treats this as "probable" based on observational correlation, not interventional evidence.

**Atom 3: Protecting it during distillation costs less utility than it buys in robustness.** This is the entire thesis. Zero evidence exists for this atom. The dossier acknowledges this honestly ("pending Stage 4/5 execution"), but the problem is that atoms 1 and 2 are also untested by *this project*, so you're stacking three unverified assumptions before you even run an experiment. [fact]

**Atom 4: The measurement protocol can distinguish real gain from confound.** This is the anti-confound gate. The dossier's strongest move. Feghhi's split-leakage critique and the nuisance-baseline requirements are well-integrated. But: no concrete split design, no named dataset, no named brain benchmark are locked. The protocol is described in prose, not operationalized. [fact]

**Verdict on decomposition:** The four-atom structure is sound. The problem is that atoms 1-2 are borrowed evidence from preprints with narrow participant pools, atom 3 is completely speculative, and atom 4 is aspirational. The decomposition is valid; the load each atom carries is not yet justified.

---

## 2) Hidden Assumptions and SPOFs

**SPOF 1: Brain-benchmark availability and quality.** The entire thesis hangs on accessing a language-relevant neural benchmark with enough signal for encoding models at edge scale. No specific benchmark is named anywhere. If the available benchmarks (e.g., Pereira, Blank, Fedorenko datasets) are too small, too noisy, or too English-centric, the measurement bet collapses. [fact: no benchmark is selected]

**SPOF 2: Teacher model access at the right scale.** The Oota overlay scopes to "mid-scale regime (around 3B-equivalent teacher/student)." But running distillation experiments with 3B+ teachers requires non-trivial compute. There's no compute budget mentioned anywhere in the dossier. If you can't run the teacher at 3B, you can't test the hypothesis as stated. [fact: no compute plan]

**SPOF 3: The alignment-utility Pareto assumption.** The dossier assumes a Pareto frontier exists where alignment and utility trade off smoothly. It's entirely possible that the relationship is not Pareto-smooth but step-function: alignment collapses below a threshold and is trivially preserved above it. If that's the case, the thesis reduces to "don't compress too much," which is not a contribution. [guess, but a dangerous one]

**Hidden assumption: $\mathcal{L}_{\text{brain}}$ is differentiable and tractable.** The formal objective includes a brain-predictive loss term. Actually computing gradients through an encoding model that maps to fMRI voxels is non-trivial. The dossier never discusses how this loss is computed, what architecture the encoding model uses, or whether end-to-end training is feasible. This is hand-waved behind notation. [fact: no implementation path specified]

**Hidden assumption: "Language-relevant" can be separated from "nuisance" in practice.** The dossier demands this separation but never proposes a specific ablation procedure. Feghhi's critique says you need residualized targets. But residualization requires choosing which features to partial out, and that choice is itself a design decision that can be gamed or poorly calibrated. [inference]

---

## 3) Strongest Counterargument

The killer objection is not about confounds (the dossier has internalized that risk). The killer is this:

**If alignment-preserving distillation works, the gain is almost certainly small, and the cost of measuring it dwarfs the contribution.**

Here's why. The Oota 2026 result suggests alignment *already partly survives* standard compression in mid-scale regimes. If that's true, then the marginal gain from an explicit alignment term in the KD loss is going to be modest, maybe a few percentage points of encoding-model R-squared. Now ask: is that modest gain worth building a whole thesis around? Because to *prove* it's real and not confounded, you need:

- Multiple seeds (3+)
- Multiple compression ratios
- Nuisance ablation controls
- Split-integrity checks
- Matched-budget baselines
- At least one secondary benchmark

That's an enormous experimental matrix for what might be +0.03 encoding R-squared on one benchmark. A reviewer will ask: "Even if this gain is real, why should I care? The uncompressed model is better anyway, and real deployment uses quantization, not KD." The dossier has no answer to the practical deployment objection because it never names a real deployment scenario. [inference, strongly grounded]

---

## 4) Missing Evidence Before Stage 3

1. **Named brain benchmark with power analysis.** Which dataset? How many participants? What's the noise floor? Can you detect a +0.05 effect with the available N? Without this, the measurement bet is a wish. [fact: absent]

2. **Concrete $\mathcal{L}_{\text{brain}}$ implementation sketch.** Is this a frozen encoding model trained on fMRI data, then used as a fixed loss? Is it a differentiable proxy? A CKA-style comparison? The mathematical objective is written down; the computational pipeline is not. [fact: absent]

3. **Compute budget and timeline.** Distillation experiments at 3B scale are not cheap. One seed, one compression ratio, one evaluation pass could take days. The dossier proposes a matrix that would require dozens of runs. Who pays for this and on what hardware? [fact: absent]

4. **At least one pilot result.** Even a toy-scale experiment (distill GPT-2 medium to small, measure encoding-model fit before and after adding alignment loss) would massively de-risk the thesis. Right now it's pure theory. [fact: absent]

5. **Deployment scenario grounding.** The "edge" in the title is doing a lot of work. Edge of what? Mobile? IoT? Clinical device? The constraints (FLOPs, latency, params) are in the formal setup but uninstantiated. [fact: absent]

6. **The Feghhi overlay is wired to idea-03, not idea-01.** The overlay tags say `#idea-03`. This is the most important counter-evidence paper for idea-01's anti-confound protocol, and the overlay isn't even written for this direction. The dossier references it, but the structured transformation hasn't been done for the idea-01 thread. [fact]

---

## 5) Exact Stage-3 Contract Edits

The current H001 hypothesis file needs these changes before it can credibly be called Stage-3 ready:

**H001 Measurement Bet section:**
- Add: specific named benchmark (e.g., "Pereira 2018 neural language benchmark, N=X participants, Y voxels, fMRI modality")
- Add: minimum detectable effect size given benchmark noise, or commit to running a power analysis as Stage-3 gate
- Change threshold from ">= 0.90 ratio and +0.05" to include confidence interval or variance-aware language ("across >= 3 seeds, median improvement >= +0.05, 95% CI excluding zero")

**H001 Kill Criteria section:**
- Add: "Kill if no suitable brain benchmark with sufficient signal-to-noise can be identified within [X weeks]"
- Add: "Kill if $\mathcal{L}_{\text{brain}}$ cannot be implemented as a differentiable or proxy loss within the training loop"
- Add: "Kill if compute budget cannot support >= 3 seeds x >= 2 compression ratios x >= 2 baselines within the thesis timeline"

**H001 Testing Strategy section:**
- Replace "TBD" server/code location with at least: target hardware class, approximate GPU-hours per run, and whether the team has access

**Frontier Map, Stage 3 Guardrails:**
- Add explicit entry: "Create idea-01-specific overlay for Feghhi 2024 with anti-confound protocol mapped to alignment-guided distillation, not PRH adjudication"
- Add: "Deployment scenario must be named and edge constraints instantiated before first experiment run"

**New required artifact:**
- Create a `$\mathcal{L}_{\text{brain}}$ implementation memo` (even 1 page) that commits to a specific encoding model architecture, training data, and gradient path

---

## 6) Final Verdict: HOLD

Not pass. Not kill. Hold.

**Why not pass:** The dossier has done genuinely excellent Stage-2 work. The iterative narrative, the adversarial self-correction, the anti-confound awareness, the matched-budget requirements are all a step above generic literature reviews. But it has zero operational specificity. No named benchmark, no compute plan, no implementation sketch, no pilot, no deployment scenario. It's a well-argued brief for a thesis that *could* exist, not a contract for one that *will* exist. Passing this to Stage 3 in current form means you'd immediately stall on "okay but how do we actually compute this loss." [inference]

**Why not kill:** The intellectual structure is sound. The three falsifiable assumptions are correctly identified. The counter-evidence is integrated rather than hidden. If any of the 21 directions can survive Stage 3, this one has a reasonable shot, provided the five evidence gaps above are closed. The novelty claim (no canonical alignment-first distillation protocol with explicit falsification) is plausible if narrow. [inference]

**What converts HOLD to PASS:** Close items 1-3 and 6 from the missing evidence list. A toy-scale pilot (item 4) would be the single highest-value action. Even if results are noisy, it forces you to build the actual $\mathcal{L}_{\text{brain}}$ pipeline, which is where this thesis will live or die. [inference]

**What converts HOLD to KILL:** If the pilot shows alignment signal is inseparable from nuisance at any scale, or if no brain benchmark with adequate power is available, or if compute access can't support the experimental matrix, kill immediately rather than spending months on a thesis that can't produce publishable evidence. [inference]
