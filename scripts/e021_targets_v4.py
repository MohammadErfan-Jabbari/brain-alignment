#!/usr/bin/env python
"""E021 aux-target construction — v4 (learnability-matched adjudication).

Builds on e021_targets_v3.py. Keeps every v3 fix:
  FIX 3 — OUT-OF-FOLD residualization (leave-one-story-out ridge).
  FIX 2 — surrogates (permuted, random_struct) drawn with the EXPERIMENT seed.
  FIX 6 — log-frequency control arm.
All targets z-scored on the training words (matched aux-MSE scale).

NEW in v4 — a learnability RANGE of non-cognitive word-aligned controls so the
learnability-trend regression (probe-AULC ~ aux-MSE) has spread to fit:
  - logfreq        : z-scored per-word log unigram frequency (v3 control; very learnable).
  - wlen           : z-scored per-word character length (real, aligned, non-cognitive).
  - surp_other_lm  : z-scored per-word surprisal from a DIFFERENT LM than base GPT-2
                     (Qwen2.5-0.5B; already in the byword table as `surp_qwen2.5-0.5b`).
                     A real, aligned, non-cognitive linguistic-difficulty target whose
                     learnability sits between the trivial surface features and the
                     stochastic surrogates.
The test arms (raw RT, residualized RT) and the two surrogates (permuted,
random_struct) are unchanged from v3. baseline is lambda=0.

Returned columns: item, zone, word,
  raw, residual, permuted, random_struct, logfreq, wlen, surp_other_lm
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# reuse the v3 builders verbatim (build_byword_table, residualize_rt_oof,
# block_permute, matched_random, _zscore) so the residual/surrogate construction
# is byte-identical to the clean v3 harness.
from e021_targets_v3 import (
    build_byword_table,
    residualize_rt_oof,
    block_permute,
    matched_random,
    _zscore,
)

OTHER_LM_COL = "surp_qwen2.5-0.5b"   # different-LM surprisal already in the byword table


def make_targets(byword_csv: str, train_items, seed: int = 0, alpha: float = 1.0):
    """v4 targets. Same residual/surrogate construction as v3, plus the wlen and
    different-LM-surprisal non-cognitive controls for the learnability-trend fit."""
    tab = build_byword_table(byword_csv)
    w = residualize_rt_oof(tab, train_items, alpha=alpha)
    # join the extra per-word features (already in the byword table), word-aligned
    # by (item, zone) — identical alignment to every other target.
    extra_cols = ["logfreq", "wlen", OTHER_LM_COL]
    lf = tab[["item", "zone"] + extra_cols]
    w = w.merge(lf, on=["item", "zone"], how="left")
    rng = np.random.default_rng(seed)
    items = w["item"].values
    raw_z = _zscore(w["meanRT"].values)
    res_z = _zscore(w["residual"].values)
    perm = block_permute(res_z, items, rng)
    rand = _zscore(matched_random(res_z, items, rng))
    out = pd.DataFrame({
        "item": w["item"].values,
        "zone": w["zone"].values,
        "word": w["word"].values,
        "raw": raw_z,
        "residual": res_z,
        "permuted": _zscore(perm),
        "random_struct": rand,
        "logfreq": _zscore(w["logfreq"].values),
        "wlen": _zscore(w["wlen"].values),
        "surp_other_lm": _zscore(w[OTHER_LM_COL].values),
    })
    return out
