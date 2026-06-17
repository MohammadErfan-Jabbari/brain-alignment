#!/usr/bin/env python
"""E021 aux-target construction — the per-word training targets for the 5 arms.

Reuses the G0/G1 machinery (scripts/run_e021_g0g1.py): per-word surprisal from
GPT-2-small, nuisances (length, log-freq, sentence position, spillover), and a
train-fold-fit ridge that residualizes mean RT on [surprisal + nuisances]. The
RESIDUAL is the cognition-specific, surprisal-orthogonal target (arm iii).

This module produces, for every Natural Stories word (item, zone) used in
training, the five per-word targets:

  - raw          : z-scored mean RT                       (arm ii)
  - residual     : surprisal-residualized RT, z-scored    (arm iii, THE TEST)
  - permuted     : block-permuted residual (within story) (arm iv)
  - random_struct: fresh Gaussian matched to residual's    (arm v)
                   scale + lag-1 autocorrelation
  - (baseline arm i uses no target; lambda_aux = 0)

Leakage control: the residualization ridge is fit ONLY on the training stories
passed in (`train_items`). Words from stories not in `train_items` are dropped
(the aux head only ever trains on training-story words, so the held-out wikitext
domain — the AULC eval — never touches RT or the ridge). All targets are z-scored
on the training words so the aux MSE scale is identical across arms.

Also exposes `make_synthetic_downstream_target` for the G2 power positive control:
a per-word target constructed to be DOWNSTREAM-predictive (it teaches the model a
representational bias that demonstrably lowers held-out-domain perplexity), used
to confirm the pipeline can detect a strong planted effect at the available N.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler


def build_byword_table(byword_csv: str) -> pd.DataFrame:
    """Load the G0/G1 per-word table (already has surprisal + nuisances)."""
    tab = pd.read_csv(byword_csv)
    # spillover nuisances (previous word within same story)
    tab = tab.sort_values(["item", "zone"]).reset_index(drop=True)
    tab["prev_wlen"] = tab.groupby("item")["wlen"].shift(1)
    tab["prev_logfreq"] = tab.groupby("item")["logfreq"].shift(1)
    tab["prev_surp_gpt2"] = tab.groupby("item")["surp_gpt2"].shift(1)
    return tab


def residualize_rt(tab: pd.DataFrame, train_items, alpha: float = 1.0):
    """Fit RT ~ [surprisal + nuisances] ridge on TRAIN STORIES only; return the
    residual for every train-story word. Returns a frame indexed by (item, zone)
    with columns: meanRT, surp, residual (raw RT minus fitted prediction)."""
    nuis = ["wlen", "logfreq", "sentpos", "prev_wlen", "prev_logfreq"]
    full = nuis + ["surp_gpt2", "prev_surp_gpt2"]
    need = ["meanRT"] + full
    w = tab[tab["item"].isin(train_items)].dropna(subset=need).copy()
    X = w[full].values.astype(float)
    y = w["meanRT"].values.astype(float)
    sc = StandardScaler().fit(X)
    ymu = y.mean()
    m = Ridge(alpha=alpha).fit(sc.transform(X), y - ymu)
    pred = m.predict(sc.transform(X)) + ymu
    w = w.copy()
    w["residual"] = y - pred
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
        # lag-1 autocorr of this story's residual
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
    Columns: item, zone, word, raw, residual, permuted, random_struct (all z-scored)."""
    tab = build_byword_table(byword_csv)
    w = residualize_rt(tab, train_items, alpha=alpha)
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
    })
    return out


def make_wikiteacher_target(byword_csv, train_items, word_wiki_surprisal):
    """G2 v2 positive control — a per-word target whose learning provably helps
    held-out-domain (wiki) perplexity: the WIKI-FINE-TUNED teacher's per-word
    surprisal on the Natural Stories text. Teaching the student to predict the
    wiki-teacher's next-token difficulty biases its representation toward wiki
    statistics during Stage A -> it begins Stage B closer to the wiki manifold ->
    lower AULC. word_wiki_surprisal: {(item, zone): float}. Returns z-scored frame."""
    tab = build_byword_table(byword_csv)
    w = tab[tab["item"].isin(train_items)].copy()
    w["wikisurp"] = [word_wiki_surprisal.get((it, zn), np.nan)
                     for it, zn in zip(w["item"], w["zone"])]
    w = w.dropna(subset=["wikisurp"])
    return pd.DataFrame({
        "item": w["item"].values, "zone": w["zone"].values, "word": w["word"].values,
        "wikiteacher": _zscore(w["wikisurp"].values),
    })


def make_synthetic_downstream_target(byword_csv, train_items, hidden_probe,
                                     words_to_tokens, seed=0):
    """G2 power positive control: a per-word target the model CAN learn and whose
    learning provably lowers held-out-domain perplexity.

    Construction: project each word's frozen base-LM hidden state onto a fixed
    direction `hidden_probe` (a held-out-domain-relevant direction supplied by the
    caller, e.g. the top principal component of held-out-domain word hiddens). The
    aux head then learns to predict this projection, which pressures the
    representation toward the held-out-domain manifold -> faster adaptation. This
    is a STRONG, by-construction downstream-useful target (the positive control).
    Returns a frame: item, zone, word, synthetic (z-scored).
    """
    tab = build_byword_table(byword_csv)
    w = tab[tab["item"].isin(train_items)].dropna(subset=["meanRT", "surp_gpt2"]).copy()
    vals = []
    for it, zn in zip(w["item"], w["zone"]):
        h = words_to_tokens.get((it, zn))
        vals.append(float(h @ hidden_probe) if h is not None else np.nan)
    w["synthetic"] = vals
    w = w.dropna(subset=["synthetic"])
    return pd.DataFrame({
        "item": w["item"].values, "zone": w["zone"].values, "word": w["word"].values,
        "synthetic": _zscore(w["synthetic"].values),
    })
