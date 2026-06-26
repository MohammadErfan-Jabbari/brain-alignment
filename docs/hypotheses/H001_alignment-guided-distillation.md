---
title: "Hypothesis H001 — Alignment-guided distillation retains neural predictivity under compression"
tags: [hypothesis]
aliases: [H001]
---

# Hypothesis H001 — Alignment-guided distillation retains neural predictivity under compression

**ID:** H001
**Created:** 2026-02-27 (Nexus) · ported 2026-06-08
**Status:** proposed (inherited; not yet tested by us)
**Charter:** `../00-charter.md` · **Landscape:** `../01-research-landscape.md`
**Experiment:** `../experiments/toy-pilot-gpt2.md` (to be created)

---

## Claim (falsifiable)

Under **matched compression ratio and training budget**, an alignment-guided distillation objective
retains **higher neural predictivity** than perplexity-only distillation while keeping acceptable
language utility.

## Measurement bet

- **Metric:** neural-predictivity retention ratio (student/teacher) on a named language-fMRI benchmark.
- **Threshold:** retains ≥ 0.90 ratio **and** improves ≥ +0.05 over perplexity-only KD at the same
  compression ratio.
- **Baseline:** perplexity-only KD with matched student size, data budget, and optimization budget.
- **Condition:** results survive the anti-confound protocol (contiguous splits, nuisance subtraction)
  and ≥ 3 seeds.

## Kill criteria

- Improvement over perplexity-only KD < +0.05 in retained neural predictivity across declared seeds.
- The measurement bet can't be operationalized with reproducible baseline parity after one design
  revision cycle.
- If killed: regress to reframe the thesis around measurement/evaluation rigor rather than
  objective-guided compression.

## How H001 depends on the three thesis assumptions

- **A1** (signal survives compression when protected) — H001 is the direct test.
- **A2** (alignment is not nuisance) — enforced by the anti-confound condition above.
- **A3** (preserved alignment buys something practical) — **not** covered by H001; needs a sibling
  hypothesis (robustness / OOD / sample-efficiency). See "Competing/sibling hypotheses".

## Competing / sibling hypotheses to add (Claim phase)

- **H002 (null/step-function):** the alignment↔utility relationship is a step function — alignment is
  trivially preserved above a compression threshold and collapses below it; the objective adds nothing.
- **H003 (practical payoff, tests A3):** a student that preserves alignment generalizes better OOD or
  is more sample-efficient than a matched perplexity-only student.

## Open design questions (must resolve before Design lock)

- The named benchmark + power analysis (the SPOF).
- The concrete form of $\mathcal{L}_{\text{brain}}$ (frozen encoding model / CKA proxy / differentiable).
- The compression mechanism (KD vs pruning vs quant) and the calibration-data policy.

## Evidence

- **From literature:** see `../01-research-landscape.md`. Anchors: Oota 2026 (dissociation), Merlin
  2024 (non-trivial target), Gao 2024 (base teacher). Brakes: Feghhi 2024, Oota 2024.
- **From experiments:** none yet. The toy pilot is the first.

## Log

| Date | Update |
|---|---|
| 2026-02-27 | Created from Nexus Wave-5 Stage-3 simulation. |
| 2026-06-08 | Ported into this repo; reframed A1/A2/A3 dependence; sibling hypotheses noted. |


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
