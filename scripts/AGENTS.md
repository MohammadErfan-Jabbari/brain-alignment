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
- Before changing or running an experiment script, read the matching `docs/experiments/E*.md` and current status in `docs/status.md`.
- Put heavy outputs in gitignored `outputs/` or `data/`, not in tracked source directories.
- E028 is a narrow exception: its synthetic-development runner and analyzer intentionally reject repository `outputs/` and `data/`. Write their ephemeral, non-load-bearing artifacts to a fresh safe temporary directory outside the repository.
- Preserve anti-artifact controls: contiguous splits, nuisance baselines, matched budget/perplexity where the design requires them, capacity-fair feature comparisons, and explicit seed handling.
- A synthetic run validates plumbing only. Do not present synthetic numbers as science.

## Common Paths

| Path | Use |
|---|---|
| `pilot_lib.py` | Shared experiment primitives: seeding, hidden states, baselines, contiguous CV, ridge encoding, variance partition. |
| `data_adapters.py` / `lebel_adapter.py` | Dataset loading and normalization. |
| `run_*.py` | Experiment runners. |
| `analyze_*.py` / `reanalyze_*.py` | Post-run analysis and robustness checks. |
| `e028_vaidya_crossmodal_falsification.py` | Outcome-blind E028 synthetic Stage-1 runner. Its only commands are `manifest`, `synthetic-replay`, `selftest`, `benchmark`, and `bundle`; every output remains explicitly not endpoint-ready. |
| `e028_analyze_vaidya_stage1.py` | Fail-closed analyzer for the E028 synthetic Stage-1 schema and exact patient-level sign-flip gate. It never licenses Stage 2 or accepts a neural endpoint. |
| `build_text_feature_target_cache.py` | E016 matched-information control target builder: frozen LM text features projected into the Phase-3 target-cache schema; pair with `run_tribe_phase3.py --target-label textfeat`. |
| `run_tribe_phase3.py` | E016 matched-budget runner for KD-only / target-MSE / target-permuted arms. Use optional `--save-model-dir` on future post-positive/control runs when trained students may be needed for real-brain or probe follow-up; saved artifacts are gitignored and are not verdicts. |
| `e016_eval_saved_student_alignment.py` | Post-hoc E016 helper that loads saved `model_artifact_dir` students and scores them on the real Tuckute alignment endpoint with the E003 contiguous-CV nuisance-subtracted protocol. Use only after artifacts exist; outputs are diagnostics for `/interpret`, not verdicts. |
| `e016_analyze_tuckute_alignment.py` | Post-hoc E016 helper that reads one or more saved-student Tuckute alignment JSONs, aligns complete TRIBE/textfeat seed grids, and writes seed-level real-brain contrasts/PCA robustness. It is a diagnostic handoff for `/interpret`, not a verdict engine. |
| `e016_audit_tuckute_alignment.py` | Local audit helper that recomputes a saved-student Tuckute analysis from raw alignment rows and checks row/protocol/arithmetic/PCA consistency before `/interpret`. It is not an independent evaluator and not a verdict engine. |
| `e016_make_textfeat_control_script.py` | Writes the post-E016 full text-feature control launcher under `outputs/`; use after a positive TRIBE Phase-3 result makes the matched-information control necessary. |
| `analyze_tribe_phase3.py` | E016 Phase-3 gate/analyzer; writes conservative readiness fields, target-cache metadata, and `paper_branch_hint`. The hint routes to the paper plan only after `science_ready=true`; it is not a verdict or rung flip. |
| `e016_compare_target_controls.py` | Post-positive E016 comparator for ready TRIBE and text-feature analyzer JSONs; compares within-target paired gains over KD/permuted controls and emits target-scope metadata, a branch hint, and top-venue reviewer-burden metadata, never a verdict. |
| `manuscript_check.py` | Deterministic manuscript gate: evidence-marker resolution, keyed-number resolution across the `\input` graph, bare result-like numbers, `\gap` survival under `--share-ready`, and the LaTeX build. Builds with latexmk only, and judges undefined references from the final `.log` rather than latexmk's multi-pass stdout; both matter, see `docs/manuscript/AGENTS.md`. Moved here from `.claude/` by D068. |
| `prose_lint.py` | Deterministic prose floor for banned tokens. A token list is complete by construction; register and semantics are not lintable and belong to review (L052). |
| `figures/` | Figure generation scripts. |
| `litsweep/` | Literature search and PDF utilities. See `litsweep/AGENTS.md`. |

## Toy-pilot code (E001)

The scientific question, the estimand rule, the anti-confound protocol, and the run commands belong to [`E001`](../docs/experiments/E001_toy-pilot-gpt2.md), which owns them. This section is navigation only.

| File | Role |
|---|---|
| `pilot_lib.py` | Scientific spine: seeding, hidden-state extraction, scalar and static nuisance baselines, contiguous-block CV, ridge encoding, capacity-fair variance partition. |
| `distill.py` | GPT-2-medium to GPT-2 distillation loop: logit KD plus an optional trainable brain-alignment head. |
| `data_adapters.py` | Common `(texts, fmri, meta)` interface with synthetic, Pereira sentence, and Pereira neural-response paths. |
| `run_toy_pilot.py` | Entry point; writes `outputs/toy-pilot/<run>/{summary.json,results.csv}`. |
| `../configs/toy_pilot.json` | Hyperparameters and smoke overrides. |
