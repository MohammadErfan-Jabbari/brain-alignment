#!/usr/bin/env python
"""E021 aux-target construction — v3 (clean rerun, Codex fixes 3 + 6).

Differences vs e021_targets.py (the committed original):

  FIX 3 — OUT-OF-FOLD residualization. The original residualize_rt fit one Ridge
    on all train-item rows and then predicted on the SAME rows (in-sample), so
    every word's "residual" was contaminated by a model that had seen it. v3 fits
    the surprisal+nuisance->RT ridge in a leave-one-story-out K-fold and predicts
    each story's words from a ridge trained on the OTHER stories only. The held-out
    residual is what actually isolates the surprisal-orthogonal component; an
    in-sample residual partly reflects overfit, not orthogonal cognition.

  FIX 6 — log-frequency arm (vi). A REAL, perfectly word-aligned, NON-cognitive
    surface feature (z-scored per-word log unigram frequency) — and one of the
    nuisances already regressed out of the residual. Decisive control: if logfreq
    also beats permuted/random like the RT arms, cognition is NOT the ingredient
    (any real word-aligned signal regularizes); if it sits at the permuted/random
    floor while RT arms beat it, cognition-specificity reopens.

  FIX 2 (caller-side) — the surrogate draw (permuted, random_struct) is seeded by
    the EXPERIMENT seed, so it varies across seeds. make_targets already takes a
    seed; v3's runner passes the experiment seed (the original runner hard-coded
    seed=0 for all experiment seeds). No code change needed here beyond honoring
    the passed seed, which it does.

The residual is still surprisal-orthogonal and the aux head still only ever trains
on training-story words, so the held-out Wikitext domain never touches RT or the
ridge. All targets are z-scored on the training words so the aux MSE scale is
identical across arms (the matched-budget parity).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler


def build_byword_table(byword_csv: str) -> pd.DataFrame:
    """Load the G0/G1 per-word table (already has surprisal + nuisances)."""
    tab = pd.read_csv(byword_csv)
    tab = tab.sort_values(["item", "zone"]).reset_index(drop=True)
    tab["prev_wlen"] = tab.groupby("item")["wlen"].shift(1)
    tab["prev_logfreq"] = tab.groupby("item")["logfreq"].shift(1)
    tab["prev_surp_gpt2"] = tab.groupby("item")["surp_gpt2"].shift(1)
    return tab


def residualize_rt_oof(tab: pd.DataFrame, train_items, alpha: float = 1.0):
    """FIX 3 — OUT-OF-FOLD residualization. Leave-one-story-out: for each train
    story, fit the RT ~ [surprisal + nuisances] ridge on the OTHER train stories
    and predict THIS story's words. Each word's residual comes from a ridge that
    never saw it. Returns a frame (item, zone, word, meanRT, surp_gpt2, residual)."""
    nuis = ["wlen", "logfreq", "sentpos", "prev_wlen", "prev_logfreq"]
    full = nuis + ["surp_gpt2", "prev_surp_gpt2"]
    need = ["meanRT"] + full
    w = tab[tab["item"].isin(train_items)].dropna(subset=need).copy().reset_index(drop=True)
    items = w["item"].values
    X = w[full].values.astype(float)
    y = w["meanRT"].values.astype(float)
    resid = np.full(len(w), np.nan)
    for held in np.unique(items):
        tr = items != held
        te = items == held
        sc = StandardScaler().fit(X[tr])
        ymu = y[tr].mean()
        m = Ridge(alpha=alpha).fit(sc.transform(X[tr]), y[tr] - ymu)
        pred_te = m.predict(sc.transform(X[te])) + ymu
        resid[te] = y[te] - pred_te
    w["residual"] = resid
    return w[["item", "zone", "word", "meanRT", "surp_gpt2", "residual"]].reset_index(drop=True)


def _zscore(a):
    a = np.asarray(a, float)
    return (a - a.mean()) / (a.std() + 1e-8)


def block_permute(values, items, rng):
    """Block-permute within each story (preserves marginal, breaks word alignment)."""
    out = np.array(values, float).copy()
    for it in np.unique(items):
        idx = np.where(items == it)[0]
        out[idx] = out[idx][rng.permutation(len(idx))]
    return out


def matched_random(residual, items, rng):
    """Fresh Gaussian per story matched to the residual's std and lag-1
    autocorrelation (AR(1) surrogate). NOT a permutation of the real signal."""
    res = np.asarray(residual, float)
    out = np.empty_like(res)
    for it in np.unique(items):
        idx = np.where(items == it)[0]
        seg = res[idx]
        sd = seg.std() + 1e-8
        if len(seg) > 2:
            phi = np.corrcoef(seg[:-1], seg[1:])[0, 1]
            phi = np.clip(np.nan_to_num(phi), -0.95, 0.95)
        else:
            phi = 0.0
        n = len(idx)
        innov = rng.standard_normal(n)
        x = np.empty(n)
        x[0] = innov[0]
        for t in range(1, n):
            x[t] = phi * x[t - 1] + np.sqrt(1 - phi**2) * innov[t]
        out[idx] = x / (x.std() + 1e-8) * sd
    return out


def make_targets(byword_csv: str, train_items, seed: int = 0, alpha: float = 1.0):
    """Return a frame with all per-word aux targets for the given train stories.
    Columns: item, zone, word, raw, residual, permuted, random_struct, logfreq
    (all z-scored). The surrogates (permuted, random_struct) are drawn with `seed`
    so they vary across experiment seeds (FIX 2). The residual is out-of-fold
    (FIX 3). logfreq is the decisive non-cognitive word-aligned control (FIX 6)."""
    tab = build_byword_table(byword_csv)
    w = residualize_rt_oof(tab, train_items, alpha=alpha)
    # join the per-word logfreq (already in the byword table) onto the residual rows,
    # word-aligned by (item, zone) — identical alignment to every other target.
    lf = tab[["item", "zone", "logfreq"]]
    w = w.merge(lf, on=["item", "zone"], how="left")
    rng = np.random.default_rng(seed)
    items = w["item"].values
    raw_z = _zscore(w["meanRT"].values)
    res_z = _zscore(w["residual"].values)
    perm = block_permute(res_z, items, rng)
    rand = _zscore(matched_random(res_z, items, rng))
    logfreq_z = _zscore(w["logfreq"].values)
    out = pd.DataFrame({
        "item": w["item"].values,
        "zone": w["zone"].values,
        "word": w["word"].values,
        "raw": raw_z,
        "residual": res_z,
        "permuted": _zscore(perm),
        "random_struct": rand,
        "logfreq": logfreq_z,
    })
    return out
