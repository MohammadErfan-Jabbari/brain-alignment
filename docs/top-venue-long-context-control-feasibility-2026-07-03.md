---
title: "Top-venue long-context control feasibility, 2026-07-03"
tags: [reference]
aliases: [top-venue-long-context-control-feasibility-2026-07-03, long-context-control-feasibility]
---

# Top-venue long-context control feasibility, 2026-07-03

**Status.** This is a `/work` infrastructure/feasibility memo, not a report, not a manuscript section, and not a science verdict. It checks whether the long-context non-brain control raised by the on-policy/context-distillation audit can be built from the current E016 KD corpus without launching new GPU training.

## Bottom line

The current E016 target caches are sentence-local, but the original WikiText context is **recoverable exactly** by replaying the original E003 corpus extraction. This refines the previous planning statement:

- **Still true:** the existing TRIBE/textfeat target caches alone do not clear long-context or on-policy distillation.
- **Refined:** a long-context non-brain target control is buildable as a new target-cache family because the raw WikiText row/header provenance can be recovered and joined to the active target caches by split-local item index.
- **Still unresolved:** an on-policy control remains a new runner protocol because it requires student rollouts and teacher supervision on those rollouts, not just recovered source context.

Do not launch the long-context control now. It is only justified if E016 is positive at matched PPL and then survives the prepared sentence-local `textfeat` control.

## What was inspected

- [`../scripts/run_kd_alignment.py`](../scripts/run_kd_alignment.py) defines the original E003 WikiText sentence extraction: load `Salesforce/wikitext`, skip raw rows beginning with `=`, split rows into sentences, keep 4-45 word sentences, deduplicate, and exclude Tuckute stimuli.
- [`../scripts/tribe_predict_kd_corpus.py`](../scripts/tribe_predict_kd_corpus.py) and [`../scripts/build_text_feature_target_cache.py`](../scripts/build_text_feature_target_cache.py) build target caches from the plain sentence files and preserve only `texts`, `item_indices`, and target arrays.
- [`../scripts/run_tribe_phase3.py`](../scripts/run_tribe_phase3.py) consumes target caches by `texts` and does not need context metadata for the active TRIBE/textfeat arms.
- The plain corpus files contain the full cached slices: `data/kd_corpus/wikitext103_sentences_train.txt` has 96,000 Python `splitlines()` entries; `data/kd_corpus/wikitext103_sentences_heldout.txt` has 2,000. The active E016 launcher uses the prefixes 95,999 and 1,999.

## Recovery helper

Added [`../scripts/e016_recover_kd_context_metadata.py`](../scripts/e016_recover_kd_context_metadata.py). It:

- replays the original WikiText extraction against `Salesforce/wikitext`,
- updates a heading stack from WikiText headers while preserving the original rule that all leading-`=` rows are skipped,
- verifies exact equality against the cached train and heldout sentence files,
- writes gitignored JSONL metadata under `outputs/E016_tribe/kd_context_metadata/`,
- records `split_index` as the join key for the existing target-cache `item_indices`.

Verification command:

```bash
HF_HOME=/home/centcom/data/hf-cache uv run python scripts/e016_recover_kd_context_metadata.py --overwrite
```

Observed summary:

| Split | Cached rows verified | Doc-title rows | Same-doc previous | Same-row previous | Unique doc titles |
|---|---:|---:|---:|---:|---:|
| train | 96,000 | 96,000 | 95,163 | 73,716 | 837 |
| heldout | 2,000 | 2,000 | 1,988 | 1,487 | 13 |

The helper prints `corpus_replay="exact_match"` and writes:

- `outputs/E016_tribe/kd_context_metadata/wikitext103_train_context_meta.jsonl`
- `outputs/E016_tribe/kd_context_metadata/wikitext103_heldout_context_meta.jsonl`
- `outputs/E016_tribe/kd_context_metadata/wikitext103_context_meta_summary.json`

## Design implication

If the positive branch reaches this burden, the next non-brain target family should be **context-feature** rather than a vague "stronger comparator":

1. For each sentence, recover preceding same-document context from the JSONL metadata.
2. Build a frozen-teacher hidden-state target with the teacher conditioned on preceding context plus the target sentence.
3. Keep the same Phase-3 training budget, target dimension, heldout target-R2 machinery, and block-permuted twin.
4. Name the arm precisely, for example `contextfeat_mse` / `contextfeat_perm`.
5. Treat the result as a context-conditioned non-brain control, not as on-policy distillation.

Open design choice before implementation: whether the target vector should pool only over the target sentence tokens after context-conditioning, or pool over the whole context+sentence sequence. The former is cleaner for the estimand if token offsets are reliable.

## Related

- [`top-venue-on-policy-context-distillation-audit-2026-07-03.md`](top-venue-on-policy-context-distillation-audit-2026-07-03.md)
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md)
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md)
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md)
