---
title: "Scripts Agent Guidance"
tags: [reference, onboarding]
aliases: [scripts-agents]
---

# Scripts Agent Guidance

This folder holds experiment runners, data adapters, analysis scripts, literature-sweep utilities, and figure builders. Treat scripts as part of the research evidence pipeline, not standalone product code.

## Rules

- Do not create new `README.md` files under `scripts/`; folder-local agent instructions belong in `AGENTS.md`.
- Run Python with `uv run`.
- Use `HF_HOME=/home/centcom/data/hf-cache` when loading cached Hugging Face models.
- Before changing or running an experiment script, read the matching `docs/experiments/E*.md` and current status in `docs/ladder.md`.
- Put heavy outputs in gitignored `outputs/` or `data/`, not in tracked source directories.
- Preserve anti-artifact controls: contiguous splits, nuisance baselines, matched budget/perplexity where the design requires them, capacity-fair feature comparisons, and explicit seed handling.
- A synthetic run validates plumbing only. Do not present synthetic numbers as science.

## Common Paths

| Path | Use |
|---|---|
| `pilot_lib.py` | Shared experiment primitives: seeding, hidden states, baselines, contiguous CV, ridge encoding, variance partition. |
| `data_adapters.py` / `lebel_adapter.py` | Dataset loading and normalization. |
| `run_*.py` | Experiment runners. |
| `analyze_*.py` / `reanalyze_*.py` | Post-run analysis and robustness checks. |
| `build_text_feature_target_cache.py` | E016 matched-information control target builder: frozen LM text features projected into the Phase-3 target-cache schema; pair with `run_tribe_phase3.py --target-label textfeat`. |
| `build_context_feature_target_cache.py` | E016 possible post-positive long-context control builder: frozen LM text features conditioned on recovered WikiText context, projected into the Phase-3 target-cache schema. Full caches should wait until E016 and textfeat justify them. |
| `run_tribe_phase3.py` | E016 matched-budget runner for KD-only / target-MSE / target-permuted arms. Use optional `--save-model-dir` on future post-positive/control runs when trained students may be needed for real-brain or probe follow-up; saved artifacts are gitignored and are not verdicts. |
| `e016_eval_saved_student_alignment.py` | Post-hoc E016 helper that loads saved `model_artifact_dir` students and scores them on the real Tuckute alignment endpoint with the E003 contiguous-CV nuisance-subtracted protocol. Use only after artifacts exist; outputs are diagnostics for `/interpret`, not verdicts. |
| `e016_watch_tuckute_eval.py` | Postprocess watcher for artifact-saving E016 runs; waits for a selected run JSON, confirms the selected Phase-3 runner has exited via `e016_phase3_status.py`, then invokes `e016_eval_saved_student_alignment.py`. It is orchestration only, not a result engine. |
| `e016_analyze_tuckute_alignment.py` | Post-hoc E016 helper that reads one or more saved-student Tuckute alignment JSONs, aligns complete TRIBE/textfeat seed grids, and writes seed-level real-brain contrasts/PCA robustness. It is a diagnostic handoff for `/interpret`, not a verdict engine. |
| `e016_audit_tuckute_alignment.py` | Local audit helper that recomputes a saved-student Tuckute analysis from raw alignment rows and checks row/protocol/arithmetic/PCA consistency before `/interpret`. It is not an independent evaluator and not a verdict engine. |
| `e016_make_textfeat_control_script.py` | Writes the post-E016 full text-feature control launcher under `outputs/`; use after a positive TRIBE Phase-3 result makes the matched-information control necessary. |
| `e016_phase3_status.py` | Read-only monitor for the long E016 Phase-3 pipeline; reports artifact presence, stage-aware cache progress/ETA, training-arm markers, completed-arm diagnostics, rough saved-artifact cadence ETA, analyzer gate fields, runner processes, node-level GPU activity, and a `health` block for quiet-but-live training. Use `uv run python scripts/e016_phase3_status.py --pretty` for the original full run; for reruns, pass explicit `--log`, `--run-json`, `--analysis-json`, and `--run-script` paths so the helper does not report the completed default artifact. ETA fields are operational only and are not science results. |
| `e016_monitor_phase3_status.py` | Periodic wrapper around `e016_phase3_status.py`; writes a latest JSON plus compact Markdown status page, including rough training ETA when available, for a selected Phase-3 run. Use it for detached 5-minute monitoring only. It is read-only with respect to science artifacts and does not launch training, analyze results, or adjudicate a claim. |
| `e016_tuckute_gate_status.py` | Read-only gate-status helper for the E016 combined Tuckute interpretation gate; reports which required rerun/Tuckute/analysis/audit files are present, whether the gate is ready for `/interpret`, whether the S99 interpretation doc/recompute are present, compact rerun progress/ETA from `e016_phase3_status.py`, postprocess watcher process health for the selected paths, and the next safe handoff action. It does not run scoring, analysis, audit, or verdict logic. |
| `e016_monitor_tuckute_gate_status.py` | Periodic wrapper around `e016_tuckute_gate_status.py`; writes the combined gate status to latest JSON/Markdown every interval and can stop once `ready_for_interpret=true`. It is monitoring only and does not launch training, scoring, analysis, audit, or verdict logic. |
| `analyze_tribe_phase3.py` | E016 Phase-3 gate/analyzer; writes conservative readiness fields, target-cache metadata, and `paper_branch_hint`. The hint routes to the paper plan only after `science_ready=true`; it is not a verdict or rung flip. |
| `e016_make_readiness_packet.py` | Read-only post-analyzer packet builder for E016; extracts gate status, branch hint, target-cache scope, paired effects, reviewer-burden flags, and next actions for `/interpret`. For positive branches it carries the post-textfeat top-venue burden from the 2026-07-03 privileged-signal adjacency audit. It is not a verdict engine. |
| `e016_finalize_phase3.py` | Guarded E016 finalizer; no-ops while the full run JSON is missing, then runs or refreshes the analyzer and readiness-packet helper once artifacts exist. It uses repo-root script paths, so it is safe from subdirectories. It is not a verdict engine. |
| `e016_watch_finalize_phase3.py` | Thin E016 watcher/finalizer wrapper; checks once by default, or polls with `--watch`, and runs `e016_finalize_phase3.py` only after the full run JSON exists. It is not a verdict engine. |
| `e016_branch_decision.py` | Post-finalizer E016 router; reads run/analyzer/readiness artifact state and prints the next safe command or stance. It also warns that a future TRIBE>textfeat comparison is not brain-specific clearance without post-positive review. It never launches training and is not a verdict engine. |
| `e016_compare_target_controls.py` | Post-positive E016 comparator for ready TRIBE and text-feature analyzer JSONs; compares within-target paired gains over KD/permuted controls and emits target-scope metadata, a branch hint, and top-venue reviewer-burden metadata, never a verdict. |
| `e016_recover_kd_context_metadata.py` | CPU-only E016 helper that replays the original WikiText KD-corpus extraction, verifies exact sentence equality, and writes gitignored context/provenance metadata for possible long-context controls. It is not a target builder or result engine. |
| `figures/` | Figure generation scripts. |
| `litsweep/` | Literature search and PDF utilities. See `litsweep/AGENTS.md`. |

## Toy Pilot Legacy Context

The original toy pilot asked whether adding a brain-alignment loss during GPT-2-medium to GPT-2 distillation improves the student's encoding-model fit to fMRI under the anti-artifact protocol, versus identical brain-blind distillation.

Core files:

| File | Role |
|---|---|
| `pilot_lib.py` | Scientific spine: seeding, hidden-state extraction, scalar/static nuisance baselines, contiguous-block CV, ridge encoding, capacity-fair variance partition. |
| `distill.py` | GPT-2-medium to GPT-2 distillation loop: logit-KD plus optional trainable brain-alignment head. |
| `data_adapters.py` | Common `(texts, fmri, meta)` interface with synthetic, Pereira sentence, and Pereira neural-response paths. |
| `run_toy_pilot.py` | Loads data, runs arms and seeds at matched budget, evaluates, writes `outputs/toy-pilot/<run>/{summary.json,results.csv}`. |
| `../configs/toy_pilot.json` | Hyperparameters and smoke overrides. |

The only alignment number allowed from this pilot shape is `unique_R2`: contextual representation variance after length, position, and static lexical controls, with capacity-fair PCA. Raw R2 can be reported as diagnostic only.

Run shape:

```bash
export HF_HOME=/home/centcom/data/hf-cache
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json --smoke
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json
```
