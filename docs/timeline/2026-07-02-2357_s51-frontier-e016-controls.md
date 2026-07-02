---
title: "S51 - frontier scout and E016 control support"
tags: [timeline, session]
---

# S51 - frontier scout and E016 control support

## Purpose

Run Erfan's autonomous `/goal`: evaluate the thesis contribution space against current arXiv/top-venue work, identify the strongest publishable cell, and advance the live experiment path without over-claiming.

## Stances

Dominant stance: `/work`.

Also used: `/scout` for the literature frontier and `/meta` for E016 analysis/control tooling.

## What happened

- Oriented on the repo state, current E016 status, and the existing top-venue expansion program.
- Confirmed the best contribution target is not generic brain-tuning, but brain-alignment-guided compression/distillation under matched student-budget controls.
- Digested CoNLL 2026 "What Brain Data Adds to Language Model Training" into a canonical scout note and updated the frontier memo: broad brain-vs-stimulus text tuning is now closed for BERT/GPT-2 LoRA fine-tuning, but compression/KD remains open.
- Digested ACL 2026 ECoG-tuning into a canonical scout note and recorded it as a high-upside modality pivot, not the immediate thesis-native path.
- Added a scout-grade canonical note for Xiao et al. 2026 on brain-guided LLM reasoning. This further closes the broad "brain-derived representation guidance improves LLM behavior" pitch, but still leaves fixed-budget student distillation open.
- Recorded an AAAI/ICML measurement-only scan in the frontier memo. Those hits sharpen measurement and attribution but do not train, compress, distill, or test fixed student budgets.
- Added [`e016_phase3_status.py`](../../scripts/e016_phase3_status.py) so the long full E016 run can be monitored without hand-parsing the log or loading large arrays.
- Hardened [`analyze_tribe_phase3.py`](../../scripts/analyze_tribe_phase3.py) against partial arm-grid false readiness, then added paired-delta values and deterministic two-sided sign-flip p-values for the target-vs-permuted and target-vs-KD contrasts.
- Added [`build_text_feature_target_cache.py`](../../scripts/build_text_feature_target_cache.py), a matched-information non-brain target-cache builder based on frozen LM text features.
- Parameterized [`run_tribe_phase3.py`](../../scripts/run_tribe_phase3.py) with `--target-label` so the same runner can emit `tribe_*` arms or `textfeat_*` arms while preserving the active default behavior.
- Smoke-tested the text-feature path with tiny caches and `sshleifer/tiny-gpt2`; the analyzer stayed `science_ready=false` as intended.
- Updated E016, the landscape, the frontier memo, script guidance, and the ladder's operational status. No verdict moved.

## Decisions made

- Treat Merlin et al. 2026 and Xiao et al. 2026 as closing broad novelty claims. The paper pitch must say "fixed-budget compression/distillation frontier", not "brain data helps LMs".
- If E016 is positive, require the matched-information non-brain target control before any brain-specific claim.
- If E016 is null, treat it as a publishable controlled negative candidate because dense synthetic neural targets remove the fMRI scarcity excuse.
- Do not launch another heavy run while the active full E016 run is still building its train cache.

## Current truth

No Phase-3 science result exists yet. The active E016 run is still in `train_cache_building`. Last checked in S51: lower-bound train-cache progress was `82624/95999 = 0.860676`; no train cache, heldout cache, run JSON, or analyzer JSON existed.

The worktree was clean after all commits. Remote `main` was pushed through `eb355dd feat: add E016 paired effect stats`.

## Checks run

- `uv run python -m py_compile scripts/build_text_feature_target_cache.py scripts/run_tribe_phase3.py scripts/analyze_tribe_phase3.py scripts/e016_phase3_status.py`
- `uv run python scripts/analyze_tribe_phase3.py outputs/E016_tribe/phase3/phase3_mini_real_gpt2_n256_s0.json --out /tmp/e016_default_paired_stats_check.json`
- `uv run python scripts/analyze_tribe_phase3.py outputs/E016_tribe/phase3/phase3_smoke_textfeat_tiny.json --out /tmp/e016_textfeat_paired_stats_check.json`
- `HF_HOME=/home/centcom/data/hf-cache uv run python scripts/build_text_feature_target_cache.py --split heldout --limit 4 --model distilgpt2 --target-dim 16 --batch-size 2 --device cpu --out outputs/E016_tribe/kd_targets/text_feature/smoke_heldout_textfeat_d16.npz`
- `HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_tribe_phase3.py --target-cache outputs/E016_tribe/kd_targets/text_feature/smoke_train_textfeat_d16.npz --heldout-target-cache outputs/E016_tribe/kd_targets/text_feature/smoke_heldout_textfeat_d16.npz --target-label textfeat --out outputs/E016_tribe/phase3/phase3_smoke_textfeat_tiny.json --teacher sshleifer/tiny-gpt2 --student sshleifer/tiny-gpt2 --seeds 0 --lambda-brain-grid 0.1 --epochs 1 --batch-size 2 --max-length 32 --limit-train 4 --limit-heldout 4 --perm-blocks 2`
- `uv run python scripts/e016_phase3_status.py --pretty`
- `git diff --check`

## Next session

- Continue `/work` on E016 by monitoring `uv run python scripts/e016_phase3_status.py --pretty`.
- Once the analyzer JSON exists, switch to `/interpret` and run the post-result stat/panel audit before recording any verdict.
- If the result is positive, run the matched-information `textfeat` control before claiming brain-specificity.
- If the result is null, prepare the controlled-negative paper framing around fixed-budget distillation.

## Friction & improvements

- Firecrawl Research MCP tools were not exposed in this Codex turn. The literature scout fell back to web search and primary pages/PDFs.
- `docs/literature/AGENTS.md` says canonical notes should go through `paper-digest`, but no repo-specific `paper-digest` agent role was available under the exposed multi-agent tool surface and user did not authorize subagent spawning. The Xiao note is marked scout-grade rather than full digest.
- The active full run uses the working-tree scripts after cache building. Analyzer and runner changes were kept backward compatible with the default `tribe` label.

## Related

- [`../upspeed.md`](../upspeed.md)
- [`../tasks.md`](../tasks.md)
- [`../top-venue-frontier-refresh-2026-07-02.md`](../top-venue-frontier-refresh-2026-07-02.md)
- [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md)
- [`../literature/canonical/merlin-2026_what-brain-data-adds.md`](../literature/canonical/merlin-2026_what-brain-data-adds.md)
- [`../literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md`](../literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md)
- [`../literature/canonical/xiao-2026_brain-guided-llm-reasoning.md`](../literature/canonical/xiao-2026_brain-guided-llm-reasoning.md)
