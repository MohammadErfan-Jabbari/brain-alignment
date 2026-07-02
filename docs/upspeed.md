---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-02 (S48 - `/work` priority closure: E023 gate, E005 λ-sweep, E016 Phase-3 no-go. **New bounded science numbers, NO rung change - Q0-Q5 stand exactly as S25.**)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

S48 completed the three requested `/work` priorities end-to-end under gates:

1. **E023a-prime gate ran.** `scripts/e023_slope_gate.py` reads `outputs/E015_expand/E015_expand_merged.json` and writes `outputs/E023/e023a_slope_gate.json`. Result: Pythia has one lower-quality pilot flat pair (`pythia-1b -> pythia-410m`), Qwen has no flat pair, and `ready_for_decisive_e023b_training=false`. Decision: do not run decisive E023b/E023f saturated KD-vs-LMFT training.
2. **E005/Qwen averaged-target λ-sweep ran.** Patched `run_brain_lever.py` so `--lambda-grid` creates λ-matched permuted twins with `null_key`/`perm_draw` and paired real-minus-perm summaries. Ran Qwen2.5-0.5B with Qwen2.5-1.5B teacher, λ ∈ {1,3,10,30}, 3 seeds × 5 folds. Outputs: `outputs/E005_lambda_sweep_avg_Qwen.json`, log, and `outputs/E005_lambda_sweep_avg_Qwen_analysis.json`.
3. **E016 Phase-3 preflight closed as NO-GO.** The valid current action is a PRD/build gate, not multi-day training: no dense TRIBE KD-corpus target cache exists, no matched-ppl three-arm Phase-3 runner exists, and the Phase-2 ceiling artifact remains walled/inconclusive.

No ladder rung changes. The λ-sweep is averaged-target context only, not per-individual evidence.

## What was done

- Added `scripts/e023_slope_gate.py` and recorded the E023 S48 gate update in `docs/experiments/E023_kd-alignment-objective-vs-quality.md`.
- Fixed `scripts/run_brain_lever.py` λ-grid controls: λ-specific permuted twins, stable non-colliding permutation seed, `perm_draw`, paired `vs_matched_perm`, and explicitly unpaired legacy p95 labels.
- Added `scripts/analyze_lambda_sweep.py` with stale-output guards for old multi-λ outputs lacking `null_key`/`perm_draw`.
- Ran smoke tests and the full Qwen λ-sweep; recorded the fold-level table in `docs/experiments/E005_alignment-guided-kd-tradeoff.md`.
- Marked the opportunistic λ-sweep complete in `docs/tasks.md`.
- Recorded the E016 Phase-3 no-go / PRD-before-compute gate in `docs/experiments/E016_tribe-synthetic-brain-targets.md`.

## What to do next

- Official next step still defaults to `/write` Section 4.3 (Q2 / E004) and Figure 6, using the honest fold-level inference unit.
- If returning to `/work`, the valid next E023 action is a dedicated lower-quality Pythia pilot runner/power gate, not decisive saturated E023b/E023f training.
- If returning to E016 Phase 3, first build the dense TRIBE target cache + matched-ppl three-arm runner + smoke/reviewer gate.

## Blockers / open loops

- E023 decisive training is gate-blocked: no same-lineage high-quality/saturated flat pair is supported by the E015-expanded data.
- E016 Phase 3 is build-blocked: no dense KD-corpus TRIBE targets and no valid runner yet.
- The λ-sweep does not change Q3/F1: it is averaged-target only; near-rate λ=1/3/10 do not survive fold-level CIs; λ=30 is fold-level-positive but degrades PPL materially.

## Key facts

- E005 λ-sweep fold-level headline: λ=3 is the best near-rate mean (`ppl=51.9`, Δ=+0.0046, fold-CI [-0.0021,+0.0112]) but fold-4/control dominated; λ=30 is the only fold-level-positive arm (`ppl=67.4`, Δ=+0.0043, vs perm +0.0060) and is a rate-costly trade.
- `outputs/E005_lambda_sweep_avg_Qwen_analysis.json` is the honest inference artifact; the flat 15-cell bootstrap in the runner summary is descriptive.
- `outputs/E023/e023a_slope_gate.json` is the E023 gate artifact.
- Git close rule D054 remains active: scoped commit first, push to `origin` at wrap by default.
