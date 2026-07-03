---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-03 (S62 - `/goal` continuation: guarded E016 finalizer; `/work`. Full E016 target caches remain built and validated; training has 3/9 arm markers and 2 completed-arm diagnostics; no science result, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

The active E016 full Phase-3 run is in GPT-2 training. Last status check in S62: `phase=training_running_or_interrupted`; `health.status=runner_alive_log_recent`; train cache exists with sidecar `n_items=95999`, `target_dim=20484`; heldout cache exists with sidecar `n_items=1999`, `target_dim=20484`; launcher validation printed finite targets and `missing=0` for both caches. Latest parsed training marker is `seed=0`, `arm=tribe_perm`, `lambda=0.1`, with `3/9` arm markers seen and `completed_arm_count=2`. Two arms have completed diagnostic output (`kd_only` and `tribe_mse`), both explicitly labeled by the status helper as partial-arm diagnostics only, not a Phase-3 result. The runner process is alive (`uv run python scripts/run_tribe_phase3.py` plus `.venv/bin/python3` child). There is still no Phase-3 run JSON and no analyzer JSON, so no `/interpret` result exists yet.

The top-tier contribution path is now explicit and source-facing: the paper cell is **brain-alignment-guided compression/distillation under fixed student budget**, not generic brain-tuning. The refreshed open-question audit is [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md). The result-contingent paper plan is recorded in [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), the claim-by-claim readiness ledger is [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), and the pre-result post-run manifest is [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md). The matched-information text-feature control launcher is prepared but must not be run unless the active TRIBE Phase-3 result is positive enough to need a brain-specificity check; [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) is prepared for the later ready-TRIBE-vs-ready-textfeat comparison.

[`e016_finalize_phase3.py`](../scripts/e016_finalize_phase3.py) is now prepared as the guarded post-run handoff command. It no-ops with `run_json_missing` while the full artifact is absent; once the run JSON exists, it runs or refreshes the conservative analyzer and readiness packet. [`e016_make_readiness_packet.py`](../scripts/e016_make_readiness_packet.py) remains the lower-level packet builder. Neither helper is a verdict engine.

No experiment result was produced, no science number was adjudicated, and no ladder rung changed.

## What was done

- Added and hardened [`scripts/e016_phase3_status.py`](../scripts/e016_phase3_status.py) so it reports cache-stage progress, ETA fields, heldout-vs-train denominators, training-arm markers, the active `run_tribe_phase3.py` runner processes, and a `health` block for quiet-but-live training.
- Recorded E016 Steps 21-25 in [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md): ETA monitor, stage-aware cache progress, full cache validation/training start, runner-process discovery, and quiet-training health status.
- Added [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md), mapping each possible paper claim to current evidence, missing proof, and venue burden.
- Added `paper_branch_hint` to [`scripts/analyze_tribe_phase3.py`](../scripts/analyze_tribe_phase3.py). It stays `not_ready` unless `gate.science_ready=true`; once ready, it routes to the predeclared paper branches (`controlled_null_candidate`, `tribe_positive_needs_textfeat`, or matched-information control comparison).
- Added [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), freezing the branch-specific claim-intent manifests, overturn criteria, gate checks, and branch actions before the full-run numbers are visible.
- Added [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py), a read-only comparator for ready TRIBE and text-feature analyzer JSONs. It compares within-target paired gains over KD/permuted controls and emits a post-positive branch hint, not a verdict.
- Confirmed the full train and heldout target caches exist and validated, then left the full Phase-3 launcher running with `3/9` arm markers and `2` completed-arm diagnostics.
- Added completed-arm parsing to [`scripts/e016_phase3_status.py`](../scripts/e016_phase3_status.py), so it separates started arm markers from completed arm diagnostics and labels partial metrics as not Phase-3 results.
- Added [`e016_make_readiness_packet.py`](../scripts/e016_make_readiness_packet.py), a read-only post-analyzer packet builder for the eventual `/interpret` handoff.
- Added [`top-venue-open-question-audit-2026-07-03.md`](top-venue-open-question-audit-2026-07-03.md), a live source-facing audit that keeps fixed-student-budget KD/compression as the open top-venue cell while marking generic brain-guided LLM/training novelty as crowded.
- Added [`e016_finalize_phase3.py`](../scripts/e016_finalize_phase3.py), a guarded finalizer that safely no-ops while the full run JSON is missing, then runs or refreshes the analyzer and readiness packet once the artifact exists.
- Latest non-wrap work commit: `821163f feat: add guarded E016 finalizer`.

## What to do next

1. Stay in `/work` and monitor the active full E016 run with `uv run python scripts/e016_phase3_status.py --pretty`.
2. If the runner exits without writing `phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, debug the runner/log before interpreting anything.
3. When the run JSON exists, run `uv run python scripts/e016_finalize_phase3.py`, then switch to `/interpret` only if the analyzer gate is science-ready. Inspect gate completeness, paired seed deltas, sign-flip p-values, and PPL matching before recording any result.
4. If E016 is positive at matched PPL, run the prepared text-feature control launcher only after confirming the active TRIBE run is complete and resources are free; when both analyzer JSONs are science-ready, use [`e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) before any brain-specific claim.
5. If E016 is null at matched PPL, use [`e016-interpretation-protocol-2026-07-03.md`](e016-interpretation-protocol-2026-07-03.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), and [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) to frame the controlled-negative paper branch.

## Blockers / open loops

- The full E016 training run is still incomplete and currently on the third parsed arm marker (`seed=0`, `tribe_perm`). The completed arm diagnostics are not science results. Full-arm training may be long; do not treat quiet log mtime as failure unless the runner process exits or GPU/process state changes.
- Firecrawl Research MCP tools were not exposed in the S51 scout turn, so the literature frontier record used web search and primary pages/PDFs.
- The prepared text-feature launcher is queued-only. Running it while the active TRIBE job is building would compete for GPU and disk bandwidth.

## Key facts

- Active run script: `outputs/E016_tribe/phase3/run_full_phase3_20260702.sh`.
- Prepared textfeat control launcher: `outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh`.
- Expected full TRIBE artifacts: `outputs/E016_tribe/kd_targets/text/train_start0_n95999_full.npz`, `outputs/E016_tribe/kd_targets/text/heldout_start0_n1999_full.npz`, `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json`, and `outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json`.
- Guarded finalizer command: `uv run python scripts/e016_finalize_phase3.py`.
- Latest non-wrap work commit for this continuation: `821163f feat: add guarded E016 finalizer`.
