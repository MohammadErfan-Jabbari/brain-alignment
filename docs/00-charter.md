---
title: "Project Charter — Brain-Alignment-Guided Methods for LLMs"
tags: [charter]
---

# Project Charter — Brain-Alignment-Guided Methods for LLMs

**Owner:** MohammadErfan Jabbari
**Program:** MSc, Machine Learning for Health at Universidad Carlos III de Madrid (UC3M). Erfan is a pre-PhD student finishing this master; the thesis remains the primary deliverable. The original deadline-driven NeurIPS track was dropped, and a separate post-thesis conference extension reopened on 2026-07-14.
**Repo:** `/home/centcom/data/brain-alignment` (single-node, centcom)
**Status:** **Thesis share-ready; conference extension active.** The original thesis experiment program is closed, while the extension follows the three kill-gated packages in [D057](decisions/decisions.md). See [`status.md`](status.md) for the live verdict and next actions. This charter records the original framing plus the extension boundary; status remains the operational authority.
**Deadline:** ~end of August 2026 (tentative — exact date TBD, confirm).
**Created:** 2026-06-08 · **Scope locked:** 2026-06-08 (see [`decisions/decisions.md`](decisions/decisions.md) D006).

---

## Conference-extension addendum

The extension preserves the share-ready thesis as its baseline and investigates three alternative paper identities: Package A, a methodological/falsification protocol; Package B, a conditional theoretical boundary; and Package C, a positive brain-guided mechanism. Their accepted definitions, activation gates, kill criteria, and execution order are recorded in [D057](decisions/decisions.md). The package idea originated in the [initial ChatGPT Pro audit](external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md) and was corrected and expanded in the [second audit](external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md); both are idea provenance only, not evidence authorities.

The corrected naming is canonical: A is methodological/falsification, B is theory, and C is the positive mechanism. The initial audit used a conflicting letter order. Future sessions may plan each package separately, but scientific compute remains conditional on the package-specific gates in D057.

## The core idea (Erfan's framing)

Middle layers of LLMs have a **linear mapping to brain activation** recorded while a human does the
same task. That mapping is real and measurable. **The thesis question is whether that mapping can be
put to work** — used as a signal for downstream objectives rather than only measured.

**Distillation is the first, easy-to-measure use case, not the whole thesis.** It is the concrete
place to test whether the mapping carries usable information: can we distill a smaller model that
keeps the brain-relevant structure (and thereby its performance/robustness) better than a
brain-blind baseline at the same budget?

## The concrete first use case (from the prior dossier)

> "Use brain alignment as a first-class objective for model compression. Instead of distilling for
> perplexity only, train/prune a smaller student model to preserve features that predict
> neural/behavioral responses while discarding the high-precision statistical tail that mainly
> improves next-token prediction." — origin idea, 2026-02-23

Candidate pipeline:
1. Select/train teacher checkpoints.
2. Measure representation alignment with encoding-model metrics (a language-fMRI benchmark).
3. Alignment-aware distillation/pruning → compact student.
4. Evaluate the trade-off: brain alignment, language utility, robustness, edge efficiency.

Objective sketch (one candidate, not locked):

$$\min_{\theta}\; \mathcal{L}_{\text{task}} + \lambda_{\text{KD}}\mathcal{L}_{\text{KD}} + \lambda_{\text{struct}}\mathcal{L}_{\text{struct}} + \lambda_{\text{brain}}\mathcal{L}_{\text{brain}}$$

subject to FLOPs / latency / parameter budgets.

## Why it might matter

- Converts a cognitive-science observation (alignment, and its saturation behaviour) into an
  actionable ML method.
- Bridges Erfan's ML-for-health background (brain benchmarks) with efficient/edge models.
- Clean gap: the literature *measures* brain alignment but rarely *uses it as the objective*.

## The first question (gates everything)

Before any method, distillation design, or "edge" story, the thesis must answer one fundamental
question: **does the LLM-middle-layer ↔ brain-activation mapping actually carry usable information —
information that helps a downstream task — once confounds are stripped out?** If the apparent signal
is mostly nuisance (length, position, low-level features, split leakage), or is trivially preserved/
destroyed regardless of objective, then the premise fails and the thesis reframes. We establish this
*first*, with the smallest honest experiment, and only then build the method. Everything below serves
this question; the deployment ("edge") framing is explicitly deferred until it is answered.

## The three falsifiable assumptions the thesis rests on

(From the prior oracle review — these are inherited from observational literature, **not yet tested
by us**. Testing A1–A3 is the contribution space.)

- **A1** — Language-relevant neural signal survives compression *when protected* by a structural/
  alignment objective. *Fails if* matched-budget utility-only KD reaches equal neural predictivity.
- **A2** — Measured alignment is not primarily nuisance. *Fails if* anti-confound controls (Feghhi)
  collapse the apparent gain.
- **A3** — Preserved alignment improves something *practical* (OOD transfer, robustness, sample
  efficiency). *Fails if* gains stay confined to the alignment metric. **No prior paper has tested A3.**

## Success / kill criteria (thesis-level, provisional)

- **Win:** alignment-guided distillation retains ≥ 0.90 neural-predictivity ratio (student/teacher)
  AND beats perplexity-only KD by ≥ +0.05 at matched compression + budget, on a named benchmark,
  surviving anti-confound controls and ≥ 3 seeds.
- **Kill:** if a toy-scale pilot shows the alignment signal is inseparable from nuisance at every
  scale, OR no language-fMRI benchmark with adequate statistical power is accessible, OR the
  compute matrix is infeasible. Kill early rather than spend months on unpublishable evidence.

## The single highest-value next action (oracle's verdict, still true)

Run a **toy-scale pilot**: GPT-2 medium → small, measure encoding-model fit before/after adding an
alignment loss. It forces us to build the real $\mathcal{L}_{\text{brain}}$ pipeline and de-risks
the whole thesis. *"This is where this thesis will live or die."*

## Relationship to sibling directions

- **Brain-JEPA** (`/home/centcom/data/brain-jepa`) — sibling, not a dependency. Shares the
  encoding-model-as-instrument idea and the ABIDE/neural-data tooling. Closest code cousin.
- **Platonic Representation Hypothesis** — sibling idea-03; could give theoretical grounding for why
  brain alignment generalizes across model families.

## What this charter does not pin down

- The named language-fMRI benchmark (Pereira / Narratives / LeBel-style) and its power analysis.
- The concrete form of $\mathcal{L}_{\text{brain}}$ (frozen encoding model as fixed loss? CKA-style?
  differentiable proxy?).
- The "edge" deployment scenario — **explicitly deferred.** We do not design for deployment until the
  fundamental question above (does the signal help, beyond confounds?) is answered.


## Related
- [`status.md`](./status.md) — the canonical status board
- [D057 conference package decision](decisions/decisions.md): package definitions, gates, and provenance
