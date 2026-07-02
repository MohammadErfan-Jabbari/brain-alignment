---
title: "S48 - work priorities: E023 gate, E005 lambda sweep, E016 Phase-3 no-go"
tags: [timeline, session]
---

# S48 - work priorities: E023 gate, E005 lambda sweep, E016 Phase-3 no-go

## Purpose

Run the three requested `/work` priorities end-to-end: E023 objective-vs-quality gate, the averaged-target
lambda/rate-distortion sweep, and the E016 TRIBE Phase-3 launch decision.

## Stance

Dominant stance: `/work`.

Also used: reviewer subagents for preflight, code/statistical wiring, and gate-faithfulness checks.

## What happened

- **Priority 1 / E023:** added and ran `scripts/e023_slope_gate.py` over
  `outputs/E015_expand/E015_expand_merged.json`. Pythia has one lower-quality pilot flat pair
  (`pythia-1b -> pythia-410m`), Qwen has no flat pair, and the gate artifact records
  `ready_for_decisive_e023b_training=false`. Recorded the no-go in `docs/experiments/E023_*`.
- **Priority 2 / λ-sweep:** fixed `scripts/run_brain_lever.py` so `--lambda-grid` creates lambda-matched
  permuted twins with `null_key`/`perm_draw`, non-colliding permutation seeds, and paired real-minus-perm
  summaries. Added `scripts/analyze_lambda_sweep.py` with stale-output guards.
- Ran smoke validation, then the full Qwen averaged-target sweep:
  `Qwen/Qwen2.5-0.5B` student, `Qwen/Qwen2.5-1.5B` teacher, λ ∈ {1,3,10,30}, 3 seeds × 5 folds, matched
  MSE permuted twins. Outputs: `outputs/E005_lambda_sweep_avg_Qwen.json`,
  `outputs/E005_lambda_sweep_avg_Qwen.log`, and `outputs/E005_lambda_sweep_avg_Qwen_analysis.json`.
- **Priority 3 / E016:** recorded Phase 3 as NO-GO for valid compute now. Phase 2 remains walled/inconclusive
  for the ceiling claim; independently, Phase 3 lacks the dense KD-corpus TRIBE target cache and the required
  matched-perplexity three-arm runner.

## Results

The λ-sweep is averaged-target context only and does not change Q3/F1. Honest fold-level summary:

- `mse_l1`: PPL 51.6, Δ +0.0032, fold-CI [-0.0009,+0.0073], vs matched perm +0.0030
  [-0.0025,+0.0085].
- `mse_l3`: PPL 51.9, Δ +0.0046, fold-CI [-0.0021,+0.0112], vs matched perm +0.0063
  [-0.0092,+0.0218]. Best near-rate mean, but fold-4/control dominated; leave-fold-4-out vs perm = +0.0010.
- `mse_l10`: PPL 55.4, Δ +0.0038, fold-CI [-0.0011,+0.0088], vs matched perm +0.0072
  [-0.0044,+0.0188].
- `mse_l30`: PPL 67.4, Δ +0.0043, fold-CI [+0.0020,+0.0065], vs matched perm +0.0060
  [+0.0002,+0.0119]. Only fold-level-positive arm, but materially degrades PPL.

## Decisions

- Do not run decisive E023b/E023f training from the current data. A lower-quality Pythia pilot would need its own
  runner/power/matched-BPB gate.
- Treat the λ-sweep as "how small / how costly" context, not per-individual evidence and not a rung move.
- Do not launch E016 Phase 3 until the target cache and matched-ppl three-arm runner exist and pass smoke/review.

## Current truth

New bounded work-session numbers were produced, but **no ladder rung changed**. Q0-Q5 stand exactly as S25.
The official next repo step remains `/write` Section 4.3 / Q2 and Figure 6 unless Erfan redirects to a new
`/work` build gate.

## Friction & improvements

The first lambda-grid patch fixed lambda matching but still summarized permuted controls unpaired. A reviewer
caught it before the full run completed; the run was stopped, the runner/analyzer were patched, smoke-tested, and
restarted cleanly. This is now protected by `null_key`, `perm_draw`, paired summaries, and stale-output validation.

## Related

- [`../experiments/E005_alignment-guided-kd-tradeoff.md`](../experiments/E005_alignment-guided-kd-tradeoff.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../experiments/E023_kd-alignment-objective-vs-quality.md`](../experiments/E023_kd-alignment-objective-vs-quality.md)
