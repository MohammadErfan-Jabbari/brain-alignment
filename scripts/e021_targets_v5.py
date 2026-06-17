#!/usr/bin/env python
"""E021 aux-target construction — v5 (the two decisive panel-requested controls).

Both opus panels (counter-argument + first-principles) independently killed the v4
"positive" with the SAME structural gap: the learnability axis (linear aux-MSE) is
too weak a control, and RT is the only target that is JOINTLY heavy-tailed (kurtosis
~13-15) AND temporally autocorrelated (lag-1 AC ~0.62-0.69). The v4 controls match
one or the other, never both: permuted matches RT's marginal but kills AC; random_struct
matches AC but is Gaussian; logfreq/wlen/surp_other_lm are neither. So "RT below the
learnability trend" is confounded with "RT has a shape no control reproduces."

v5 adds the two neutralizing controls that close that gap. Run them as extra arms at
n>=10 alongside the v4 arms; if RT STILL beats both, the positive survives; if RT lands
ON them, the v4 below-trend gap was signal-shape / nonlinear-nuisance, i.e. clean NULL.

  CONTROL A — shape_matched (counter-argument + first-principles' request, STRONGEST form).
    A NON-cognitive target that matches RT-residual's FULL temporal autocorrelation (entire
    power spectrum, not just lag-1) AND its heavy-tailed marginal, per story, but carries no
    word-identity content. Built by PHASE-RANDOMIZING the residual per story (FFT, randomize
    phases, inverse FFT) — this preserves the exact power spectrum, hence the full
    autocorrelation function (all lags, RT's real spillover memory), while scrambling which
    word gets which value; then quantile-map (rank-warp) onto the residual's empirical marginal
    so kurtosis matches too. Result: same full autocorrelation + same marginal as RT-residual,
    zero behavioral content. This is strictly stronger than random_struct (lag-1 AR only).
    Drawn with the experiment seed. The first-principles panel: "RT beating THAT is the
    cognition positive; RT tying it is the regularizer-shape artifact."

  CONTROL C — surp_smoothed (counter-argument's "smoothed-surprisal" request). Take the
    DIFFERENT-LM (Qwen2.5-0.5B) per-word surprisal — a REAL linguistic-difficulty signal,
    non-cognitive — and low-pass it with a causal per-story EWMA until its lag-1 autocorrelation
    matches RT's (~0.62), then z-score. This fills the empty cell both panels named: a target
    that is real-difficulty AND temporally smooth AND non-cognitive. If RT beats surp_smoothed,
    the edge is not mere smoothness; if RT ties it, the edge IS smoothness of a real-difficulty
    signal, not cognition.

  CONTROL B — rt_hat_nuisance (first-principles' request). The NONLINEAR out-of-fold
    reconstruction of RT from ONLY the nuisances already in the control set: a gradient-
    boosted regressor predicting meanRT from [surp_gpt2, surp_other_lm, wlen, logfreq,
    sentpos + their prev-word lags], leave-one-story-out, z-scored. This is RT's nonlinear-
    nuisance-explainable component — pure non-cognition by construction. If RT does not
    beat rt_hat_nuisance, RT's advantage is reconstructible from frequency/length/surprisal
    (the L024(2) confound) and is NOT cognition.

Reuses the v3/v4 residual + surrogate construction verbatim so the shared arms are
byte-identical. All targets z-scored on the training words (matched aux-MSE scale).

Returned columns: item, zone, word,
  raw, residual, permuted, random_struct, logfreq, wlen, surp_other_lm,
  shape_matched, rt_hat_nuisance
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

from e021_targets_v3 import (
    build_byword_table, residualize_rt_oof, block_permute, matched_random, _zscore,
)
from e021_targets_v4 import OTHER_LM_COL


def _phase_randomize(x, items, rng):
    """Per-story phase-randomized surrogate: FFT, randomize phases (keep magnitudes =>
    exact power spectrum => full autocorrelation at ALL lags), inverse FFT, take real part.
    Destroys word-identity content while preserving the entire autocorrelation function.
    Strictly stronger than the lag-1 AR(1) random_struct."""
    out = np.empty_like(x, float)
    for it in np.unique(items):
        idx = np.where(items == it)[0]
        seg = x[idx]
        n = len(seg)
        if n < 4:
            out[idx] = rng.permutation(seg)
            continue
        F = np.fft.rfft(seg)
        mag = np.abs(F)
        phases = np.exp(1j * rng.uniform(0, 2 * np.pi, len(F)))
        phases[0] = 1.0                       # keep DC real
        if n % 2 == 0:
            phases[-1] = 1.0                  # keep Nyquist real
        sur = np.fft.irfft(mag * phases, n=n)
        out[idx] = sur
    return out


def _ewma_to_ac(x, items, target_ac, tol=0.02, max_iter=40):
    """Causal per-story EWMA-smooth x until its pooled lag-1 autocorrelation >= target_ac.
    Binary-search the EWMA alpha (alpha=1 -> no smoothing/low AC; alpha->0 -> high AC)."""
    def smooth(alpha):
        out = np.empty_like(x, float)
        for it in np.unique(items):
            idx = np.where(items == it)[0]
            seg = x[idx]; s = np.empty_like(seg); s[0] = seg[0]
            for t in range(1, len(seg)):
                s[t] = alpha * seg[t] + (1 - alpha) * s[t - 1]
            out[idx] = s
        return out

    def ac1(v):
        vals = []
        for it in np.unique(items):
            s = v[items == it]
            if len(s) > 2:
                vals.append(np.corrcoef(s[:-1], s[1:])[0, 1])
        return float(np.nanmean(vals))

    lo, hi = 0.02, 1.0   # alpha
    best = smooth(0.3)
    for _ in range(max_iter):
        a = 0.5 * (lo + hi)
        v = smooth(a)
        cur = ac1(v)
        if abs(cur - target_ac) < tol:
            return v
        if cur > target_ac:   # too smooth -> raise alpha (less smoothing)
            lo = a
        else:
            hi = a
        best = v
    return best


def _quantile_map(source, target, items):
    """Rank-warp `source` onto the empirical marginal of `target`, per story. Output has
    target's exact marginal (sorted target values placed at source's rank order), source's
    rank structure (hence its autocorrelation). Per-story to match the residual construction."""
    out = np.empty_like(source, float)
    for it in np.unique(items):
        idx = np.where(items == it)[0]
        s = source[idx]; t = np.sort(target[idx])
        ranks = np.argsort(np.argsort(s))   # 0..n-1 rank of each source value
        out[idx] = t[ranks]
    return out


def _nuisance_oof_gbm(tab, train_items):
    """Out-of-fold (leave-one-story-out) NONLINEAR reconstruction of meanRT from the
    nuisances only. Returns a per-row prediction aligned to the residualize_rt_oof rows."""
    nuis = ["wlen", "logfreq", "sentpos", "surp_gpt2", OTHER_LM_COL,
            "prev_wlen", "prev_logfreq", "prev_surp_gpt2"]
    need = ["meanRT"] + nuis
    w = tab[tab["item"].isin(train_items)].dropna(subset=need).copy().reset_index(drop=True)
    items = w["item"].values
    X = w[nuis].values.astype(float)
    y = w["meanRT"].values.astype(float)
    pred = np.full(len(w), np.nan)
    for held in np.unique(items):
        tr = items != held; te = items == held
        m = HistGradientBoostingRegressor(max_depth=3, max_iter=300,
                                          learning_rate=0.05, random_state=0)
        m.fit(X[tr], y[tr])
        pred[te] = m.predict(X[te])
    return w[["item", "zone"]].assign(rt_hat=pred)


def make_targets(byword_csv: str, train_items, seed: int = 0, alpha: float = 1.0):
    tab = build_byword_table(byword_csv)
    w = residualize_rt_oof(tab, train_items, alpha=alpha)
    extra_cols = ["logfreq", "wlen", OTHER_LM_COL]
    w = w.merge(tab[["item", "zone"] + extra_cols], on=["item", "zone"], how="left")
    # nonlinear nuisance reconstruction of RT (out-of-fold), joined by (item, zone)
    rt_hat = _nuisance_oof_gbm(tab, train_items)
    w = w.merge(rt_hat, on=["item", "zone"], how="left")

    rng = np.random.default_rng(seed)
    items = w["item"].values
    raw_z = _zscore(w["meanRT"].values)
    res_z = _zscore(w["residual"].values)
    perm = block_permute(res_z, items, rng)
    rand = _zscore(matched_random(res_z, items, rng))
    other_z = _zscore(w[OTHER_LM_COL].values)
    # residual's per-story lag-1 AC (target for the smoothness-matched controls)
    res_ac = float(np.nanmean([np.corrcoef(res_z[items == it][:-1], res_z[items == it][1:])[0, 1]
                               for it in np.unique(items) if (items == it).sum() > 2]))
    # CONTROL A: phase-randomized residual (FULL autocorrelation) -> quantile-map to residual marginal
    phase = _phase_randomize(res_z, items, rng)
    shape_matched = _zscore(_quantile_map(phase, res_z, items))
    # CONTROL B: nonlinear nuisance reconstruction of RT (z-scored)
    rt_hat_z = _zscore(w["rt_hat"].values)
    # CONTROL C: Qwen surprisal EWMA-smoothed to RT's lag-1 AC (real-difficulty + smooth, non-cog)
    surp_smoothed = _zscore(_ewma_to_ac(other_z, items, res_ac))

    out = pd.DataFrame({
        "item": w["item"].values, "zone": w["zone"].values, "word": w["word"].values,
        "raw": raw_z, "residual": res_z,
        "permuted": _zscore(perm), "random_struct": rand,
        "logfreq": _zscore(w["logfreq"].values), "wlen": _zscore(w["wlen"].values),
        "surp_other_lm": other_z,
        "shape_matched": shape_matched, "rt_hat_nuisance": rt_hat_z,
        "surp_smoothed": surp_smoothed,
    })
    return out
