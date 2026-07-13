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
| `run_tribe_phase3.py` | E016 matched-budget runner for KD-only / target-MSE / target-permuted arms. Use optional `--save-model-dir` on future post-positive/control runs when trained students may be needed for real-brain or probe follow-up; saved artifacts are gitignored and are not verdicts. |
| `e016_eval_saved_student_alignment.py` | Post-hoc E016 helper that loads saved `model_artifact_dir` students and scores them on the real Tuckute alignment endpoint with the E003 contiguous-CV nuisance-subtracted protocol. Use only after artifacts exist; outputs are diagnostics for `/interpret`, not verdicts. |
| `e016_analyze_tuckute_alignment.py` | Post-hoc E016 helper that reads one or more saved-student Tuckute alignment JSONs, aligns complete TRIBE/textfeat seed grids, and writes seed-level real-brain contrasts/PCA robustness. It is a diagnostic handoff for `/interpret`, not a verdict engine. |
| `e016_audit_tuckute_alignment.py` | Local audit helper that recomputes a saved-student Tuckute analysis from raw alignment rows and checks row/protocol/arithmetic/PCA consistency before `/interpret`. It is not an independent evaluator and not a verdict engine. |
| `e016_make_textfeat_control_script.py` | Writes the post-E016 full text-feature control launcher under `outputs/`; use after a positive TRIBE Phase-3 result makes the matched-information control necessary. |
| `analyze_tribe_phase3.py` | E016 Phase-3 gate/analyzer; writes conservative readiness fields, target-cache metadata, and `paper_branch_hint`. The hint routes to the paper plan only after `science_ready=true`; it is not a verdict or rung flip. |
| `e016_compare_target_controls.py` | Post-positive E016 comparator for ready TRIBE and text-feature analyzer JSONs; compares within-target paired gains over KD/permuted controls and emits target-scope metadata, a branch hint, and top-venue reviewer-burden metadata, never a verdict. |
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
