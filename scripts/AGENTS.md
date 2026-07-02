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
| `e016_phase3_status.py` | Read-only monitor for the long E016 Phase-3 pipeline; use `uv run python scripts/e016_phase3_status.py --pretty` before hand-parsing the log. |
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
