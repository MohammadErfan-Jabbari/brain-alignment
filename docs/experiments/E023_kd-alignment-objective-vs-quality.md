---
title: "E023 — Does perplexity-only KD shed brain alignment *beyond quality*? An identified program across…"
tags: [experiment]
aliases: [E023]
---

# E023 — Does perplexity-only KD shed brain alignment *beyond quality*? An identified program across scale

**Type:** program design + identification framework (analysis-lane authored; **nothing run yet**). **Status:** ⬜ DESIGNED — not gated, not run. **Created:** 2026-06-18 (S24, analysis). **Owner:** Erfan (analysis-lane design). **Gate:** requires `oracle-reviewer` PASS + a thesis-vs-paper scope decision before any compute.

> **What this doc is.** R07 (Q1) established that plain perplexity-only KD does *not* preserve a teacher's alignment, but left the load-bearing question unresolved: is the loss *specific to the distillation objective*, or merely the side effect of a worse language model? R07 could not separate them because its evidence (5 points, gpt2-small↔gpt2-medium, a 3× span far below the ~3B alignment-saturation knee) is confounded — alignment co-varies with log-perplexity at $r=-0.88$ [E003], and the objective-specific dissociations were only $p\approx0.09$. This doc **formalizes the estimand that separates the two**, proves why a wider scale sweep alone does *not* identify it, gives the identification strategy that does, and derives the complete set of experiments that strategy licenses — each with a predeclared kill criterion. The theory sections (§1–§3) are written to lift into a manuscript Methods/Framework section; cite [E003], [E015], [`06-theory-grounding.md`](../06-theory-grounding.md) rows 2/3/4/6.

---

## 1. The estimand: objective-specific shedding, defined against a counterfactual

Write $A(\cdot)$ for brain alignment measured as the conditional-MI / unique-R² object R06 fixes ([`06-theory-grounding.md`](../06-theory-grounding.md) §3: $I(Z;B\mid\text{nuisance})$, NC-normalised unique R² under contiguous splits). Write $p(\cdot)$ for held-out perplexity, the exponential of the model's cross-entropy, which by `06` §6 is monotone in the output-KL to the data, $\ln p = H(\widehat P_X) + D(\widehat P_X\|q)$.

The naive headroom R07 measured is the raw gap to the teacher, $\Delta = A_T - A_S$. The problem is that $\Delta$ mixes two causes. Decompose it against the quality the student lost:

$$
A_T - A_S \;=\; \underbrace{\big[f(p_S) - f(p_T)\big]}_{\text{quality cost: what any model of quality } p_S \text{ would lose}} \;+\; \underbrace{\big[A_S - f(p_S)\big]}_{\delta_{\text{obj}}:\ \text{objective-specific shedding}},
$$

where $f(p)$ is the **alignment a normally-trained (non-distilled) model of perplexity $p$ attains** — the counterfactual. The quantity the thesis actually wants is the second term:

$$
\boxed{\;\delta_{\text{obj}}(S) \;=\; A_S - f(p_S)\;}
$$

the vertical distance of a KD student $S$ *below the baseline manifold* $f$. $\delta_{\text{obj}}<0$ means KD destroyed alignment that a same-quality model keeps — an objective-specific effect, the thing R07 could not claim. $\delta_{\text{obj}}\approx 0$ means the whole drop is just lost quality, and "protect alignment during KD" is a non-problem (the F1 cell collapses, R07 §"The question"). This is the estimand. R07's $\Delta$ is $\delta_{\text{obj}}$ plus the quality cost; it cannot isolate the box.

**Identifying assumption.** $f$ is the correct counterfactual: a non-KD model at perplexity $p_S$ is the right "what alignment should a model this good have" reference. This holds iff $f$ is estimated on models that differ from the KD students *only* in the training objective (not in family/architecture/data confounds that themselves move alignment at fixed $p$ — the E015 architecture-residual, +0.006–0.009 above quality for modern families [E015]). So the manifold and the KD students must live in the **same family/architecture lineage**, or the architecture-residual must be partialled out. This is the one assumption the whole program rests on; §3 and the kill criteria defend it.

## 2. Why a scale sweep alone does NOT identify $\delta_{\text{obj}}$ (the formal version of the prior argument)

The tempting design — "train KD students from 50M to 8B and look at alignment" — fails, and the failure is exact. Each KD student lands at its own perplexity $p_S$, so a sweep traces out pairs $(p_S, A_S)$. But E015 already established the law $A \approx f(p)$ across 22 models / 6 families ($r\approx-0.78$ across range) [E015]. A KD sweep that only varies size therefore re-measures $f$ with KD points instead of off-the-shelf points, and reads off $A_S$, not $A_S - f(p_S)$. The confound is not diluted by more sizes; the estimator of the wrong quantity just gets tighter. Formally, $\operatorname{Var}$ of the size axis adds power to estimate $f$, and **zero** power to estimate the residual $\delta_{\text{obj}}$ unless a *same-quality non-KD counterfactual* is present at each operating point. Size is a covariate of $f$, not an instrument for $\delta_{\text{obj}}$.

So the wide range is justified only in a specific role (a covariate that lets §3's identification gradient be measured), never as the identification itself. This is why the honest program is "build $f$ densely + put KD students against it," not "sweep KD across scale."

## 3. The identification strategy, and why saturation is the friend

Two ingredients identify $\delta_{\text{obj}}$.

**(i) A baseline manifold $f$, estimated on non-KD models.** Fit $A = f(p)$ on normally-trained models within a fixed family lineage (so the architecture-residual is held constant), with the nuisance/anti-confound protocol of R06. E015 is most of this already (its off-the-shelf $(p, A)$ points *are* $f$); the program extends it to the lineage and density needed.

**(ii) Matched-perplexity KD students placed against $f$.** Train KD students and read their vertical residual $A_S - f(p_S)$. The paired, powered form is R07's permuted-twin / matched-ppl machinery generalised: at a given operating point compare the KD student to the non-KD model of the same $p$.

**The saturation argument, formalised.** How well $\delta_{\text{obj}}$ is identified depends on the *slope* of the manifold at the operating point. By error propagation, a perplexity-measurement error $\varepsilon_p$ contaminates the residual estimate by $f'(p)\,\varepsilon_p$:

$$
\widehat{\delta}_{\text{obj}} \;=\; A_S - f(\widehat p_S) \;\approx\; \delta_{\text{obj}} \;-\; f'(p_S)\,\varepsilon_p .
$$

- In the **rising regime** ($p$ large, models small, below ~3B): $f'(p)$ is steep (alignment and quality co-move hard — E015's across-range $r\approx-0.78$, R01/Oota-2026 rising arm). A small quality difference maps to a large predicted-alignment difference, so $\delta_{\text{obj}}$ is swamped by quality. **This is exactly the regime R07's cold arm sat in** (ppl 477, far up the steep arm) — which is *why* R07 couldn't separate objective from quality. It is the worst place to look.
- In the **saturated regime** ($\gtrsim 3$B): $f'(p)\approx 0$ — alignment and perplexity *decouple* (E015 within-saturated-family correlations are noise; Qwen even inverts, 7B aligns lowest [E015]; AlKhamissi-2025 "outgrows the network"). The manifold is flat, so $f'(p_S)\varepsilon_p\to 0$ and **any** alignment drop in a KD student reads almost directly as $\delta_{\text{obj}}$: quality cannot explain it, because quality barely moves alignment there.

**Consequence (the design principle):** $\delta_{\text{obj}}$ is *most identifiable where the manifold is flattest* — at and above saturation. This inverts the naive "go wide and small" instinct: the decisive operating point is **teacher and student both near/above the ~3B knee**, not a sweep down to 50M. The small/steep end contributes only manifold anchors, never a clean residual.

**Grounding (manifold = empirical rate–distortion frontier).** $f$ is the empirical alignment-vs-quality frontier; $\delta_{\text{obj}}$ is the gap between KD's operating point and that frontier (`06` §4, rate–distortion). Row 6 says output-KL (perplexity, the KD objective) under-constrains the representation, so a below-frontier $\delta_{\text{obj}}$ is *possible*; rows 2 (DPI break) say it is *not bounded away*; this program *measures* whether it is *actual*. The three are the possibility / non-bound / measurement faces of one claim.

## 4. The experiment program (each row: estimand · design · kill criterion · feasibility)

Coverage is over the **question space**, not the size axis. Tiered by compute. Every arm uses the R06 apparatus (unique R², contiguous splits, capacity-fair nuisance) and predeclares its kill criterion (D003).

| ID | Question / estimand | Design | Kill criterion | Feasibility |
|---|---|---|---|---|
| **E023a** | **Build the baseline manifold $f$ densely, in one lineage.** Estimand: $f(p)$ and its slope $f'(p)$ across the rising→saturated range. | Extend E015 within the **Pythia** ladder (70M–2.8B, same data+arch, only scale — the clean instrument) + **Qwen2.5** (0.5–7B), all off-the-shelf, cached. Fit $f$, locate the knee, estimate $f'(p)$ by regime. | n/a (descriptive infrastructure); flag if no flat regime exists (then the whole saturation strategy is void). | **Cheap** — forward passes only, no training. Mostly done in E015; needs the slope-by-regime read + knee localisation. |
| **E023b** | **The core contrast: $\delta_{\text{obj}}$ for pure-logit KD, in the saturated regime.** | Distill within one lineage with teacher+student both near/above knee (e.g. Pythia-2.8B→1.4B, or Qwen-7B→3B), pure temperature-KL ($\lambda_{\text{brain}}=\lambda_{\text{hidden}}=0$). Read $A_S - f(p_S)$, paired vs the same-$p$ non-KD model; warm-init confound handled per R07. | $\delta_{\text{obj}}$ CI includes 0 at adequate power → **objective sheds nothing beyond quality** (the F1 cell is empty; report as a clean null). | **Medium–High** — see §5; warm-init at this scale is feasible, cold-init is not (the fork). |
| **E023c** | **Scale-dependence of $\delta_{\text{obj}}$.** Estimand: $\partial \delta_{\text{obj}}/\partial\text{scale}$ — is shedding a small-model phenomenon that vanishes at saturation, or persistent? | Repeat E023b at ≥3 operating points spanning rising→saturated. The *one* place the wide range is licensed (covariate of identification, §2/§3). | $\delta_{\text{obj}}$ flat and ≈0 across regimes → no objective effect anywhere; or monotone-vanishing → it's a quality artifact of the steep arm (vindicates R07's caveat). | **High** — several trained students; gate hardest here. |
| **E023d** | **Where in the network does KD shed?** Estimand: layerwise $\delta_{\text{obj}}(\ell)$. | Layerwise unique-R² readout on the *already-trained* E023b/c students (no new training). Tests the R01 prediction that mid-layers (alignment peak) are where a destructive transform bites. | Shedding uniform across depth → not a representational-structure effect (argues quality, not objective). | **Cheap** — readout only on existing checkpoints. A figure. |
| **E023e** | **Does a representation-level KD term *protect* alignment?** Estimand: $\delta_{\text{obj}}^{\text{logit+hidden}} - \delta_{\text{obj}}^{\text{logit}}$ at matched ppl. | Add a teacher-hidden-state matching term (the distilgpt2 cosine knob R07 flagged) on top of pure-logit KD; compare residuals at matched $p$. Directly tests the F1 mechanism with a *teacher*-side, controllable knob (distinct from the brain-loss). | hidden-term residual ≈ logit-only residual → representation distillation does not protect alignment (the mechanism is inert). | **Medium** — same students, extra loss term. |
| **E023f** | **Is KD different from plain finetuning at matched ppl?** Estimand: $A_{\text{KD}} - A_{\text{LMft}}$ at matched $p$, across scale. | Generalise R07's `lmft_warm` vs `kd_warm` (was $p\approx0.085$, n=tiny) to the lineage + saturated regime. Isolates "the KD objective" from "any training run." | gap CI includes 0 → KD is not special vs ordinary finetuning at matched quality (the objective qua objective does nothing). | **Medium** — paired with E023b/c arms. |

**Deliberately EXCLUDED (and why) — the discipline ledger:**
- **Cold-init KD at ≥1B.** Cold-init was R07's rigor (no inheritance confound), but from random init it is *pretraining-scale* compute; a cold 3B/8B cannot converge on 4×L40S in thesis time (E003's cold-124B hit ppl 477 *under-trained* on 2 epochs). So at scale we are forced to warm-init, and we declare that limit openly rather than hide an under-trained arm. → see §5 fork.
- **Distilling DOWN to <50M.** Pure steep-arm; $f'$ huge; $\delta_{\text{obj}}$ unidentifiable (§3). Useful only as manifold anchors (E023a already has them off-the-shelf). No new training there.
- **8B teachers.** Marginal identification gain over 3–7B (both saturated), large cost. Add only if 3–7B shows a live $\delta_{\text{obj}}$ worth a scale-up.
- **Cross-family KD** (e.g. Qwen→Pythia). Breaks the identifying assumption (§1): architecture-residual contaminates $f$. Same-lineage only, unless the residual is explicitly partialled.

## 5. The cold-vs-warm fork (the real feasibility wall, stated openly)

R07's clean read needed **cold-init** (random student) so any alignment was *transmitted through the KD channel*, not inherited from the student's own pretraining. At ≥1B that is infeasible (above). The honest resolutions, in preference order:

1. **Warm-init + the right counterfactual.** Use a pretrained student, but read $\delta_{\text{obj}}$ as the residual *below the manifold at matched ppl*, with the **non-KD finetune (E023f) as the paired control**. The inheritance confound is then differenced out: both KD and LMft students start from the same pretrained init, so $A_{\text{KD}} - A_{\text{LMft}}$ at matched $p$ isolates the objective without needing cold-init. **This is the feasible spine.** (It is exactly why E023f is not optional.)
2. **Cold-init only at small scale (≤350M)** as a steep-arm sanity tie to R07, never as the verdict (it lives where $\delta_{\text{obj}}$ is unidentifiable).
3. Acquire pretraining compute for one cold mid-scale student — out of scope unless a sponsor/cluster appears.

## 6. Scope, gate, and what would flip a rung

- **Which deliverable?** Q1 is a *supporting* rung; the matched-ppl contribution is already banked (E008 + E015). If this is for the **thesis verdict**, opportunity cost is high and it will not move the headline. If it is a **figure-bearing section of the negative-results / methodology paper** — "KD sheds alignment; here is the objective-specific component, isolated where quality decouples; and it is/ isn't protected by representation-level terms" — it can earn its compute. **Decide before E023b.**
- **Gate.** No compute until `oracle-reviewer` PASSes the E023b design (matched-ppl identification, the warm-init differencing, power/MDE) and the thinking panel (D017) clears it. **No rung flips without Erfan.**
- **What would change R07/Q1.** A powered $\delta_{\text{obj}}<0$ in the saturated regime (E023b/c) that survives E023f (KD ≠ LMft at matched ppl) would upgrade Q1 from "sheds, but objective-specificity unproven" to "objective-specifically sheds" — the claim R07 explicitly does *not* license today. A clean $\delta_{\text{obj}}\approx0$ closes the F1 cell honestly.

---

**One-line summary.** The thing to measure is not "alignment across KD'd sizes" (that re-traces E015) but **the vertical drop of a KD student below the same-family alignment-vs-perplexity manifold, measured where the manifold is flat (≥3B), with a same-init non-KD finetune as the paired control** — and the cold-init ideal is infeasible at scale, so the feasible identification is the KD-minus-finetune difference at matched perplexity.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
