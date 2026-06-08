#!/usr/bin/env python3
"""Shared library for the toy brain-alignment distillation pilot.

This module holds the *scientific spine* of the pilot, kept separate from
orchestration so the pieces can be unit-smoke-tested and reused once real
language-fMRI data is plugged in. Everything here is data-source agnostic: it
operates on (stimulus_texts, fmri_matrix) regardless of whether the fMRI is a
real benchmark slice or the synthetic stand-in.

The non-negotiable anti-confound protocol (Feghhi 2024, learnings L003) lives in
`encoding_score` and `variance_partition`:
  * CONTIGUOUS block cross-validation, never shuffled splits (shuffling leaks via
    temporal autocorrelation and inflates R^2).
  * Nuisance baselines (length, position, static/non-contextual embeddings).
  * The honest number is the UNIQUE variance of the contextual LM features after
    the nuisance variance is partialled out, not the raw R^2.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

import numpy as np

# torch / sklearn are imported lazily inside functions so this module can be
# inspected and partially tested even before the heavy deps finish installing.


# --------------------------------------------------------------------------- #
# Reproducibility
# --------------------------------------------------------------------------- #
def set_seed(seed: int) -> None:
    """Seed every RNG we touch. Determinism matters: the pilot reports >=3 seeds."""
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def pick_device() -> str:
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


# --------------------------------------------------------------------------- #
# Hidden-state extraction
# --------------------------------------------------------------------------- #
@dataclass
class ExtractConfig:
    layer: int = -1          # which hidden_states index; resolved per-model if negative
    pool: str = "mean"       # "mean" (masked mean over tokens) or "last"
    max_length: int = 64
    batch_size: int = 16


def extract_hidden_states(
    model,
    tokenizer,
    texts: list[str],
    cfg: ExtractConfig,
    device: str,
    layer: int | None = None,
) -> np.ndarray:
    """Run `texts` through `model`, return (n_items, d_model) pooled hidden states.

    `layer` indexes into `output_hidden_states` (0 = embeddings, 1..N = blocks).
    A middle layer is the brain-alignment sweet spot (Oota 2023: alignment is
    largely mid-layer syntactic structure). We pool over real (non-pad) tokens.
    """
    import torch

    use_layer = layer if layer is not None else cfg.layer
    model.eval()
    feats: list[np.ndarray] = []
    with torch.no_grad():
        for start in range(0, len(texts), cfg.batch_size):
            batch = texts[start : start + cfg.batch_size]
            enc = tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=cfg.max_length,
            ).to(device)
            out = model(**enc, output_hidden_states=True)
            hs = out.hidden_states[use_layer]            # (B, T, d)
            mask = enc["attention_mask"].unsqueeze(-1).float()  # (B, T, 1)
            if cfg.pool == "last":
                # last real token per sequence
                lengths = enc["attention_mask"].sum(dim=1) - 1
                pooled = hs[torch.arange(hs.size(0)), lengths]
            else:
                pooled = (hs * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1.0)
            feats.append(pooled.float().cpu().numpy())
    return np.concatenate(feats, axis=0)


def middle_layer_index(model) -> int:
    """Index into hidden_states for the geometric middle block (1-based blocks)."""
    n = model.config.num_hidden_layers
    return max(1, n // 2)


# --------------------------------------------------------------------------- #
# Nuisance features (the anti-confound baselines)
# --------------------------------------------------------------------------- #
def scalar_nuisance(texts: list[str], tokenizer) -> np.ndarray:
    """Low-dimensional scalar confounds: token length + item position.

    Length is Feghhi's headline confound (untrained models 'explain' fMRI via
    length alone); position is a temporal-autocorrelation proxy. These are kept
    RAW (2 columns) — the high-dim static-embedding confound is handled
    separately and PCA-reduced symmetrically with the contextual features so the
    variance partition is capacity-fair (see variance_partition).
    """
    n = len(texts)
    lengths = np.array(
        [len(tokenizer(t, truncation=True, max_length=512)["input_ids"]) for t in texts],
        dtype=np.float64,
    ).reshape(-1, 1)
    position = np.arange(n, dtype=np.float64).reshape(-1, 1)
    return np.concatenate([lengths, position], axis=1)


def static_embedding_features(model, tokenizer, texts: list[str], device: str) -> np.ndarray:
    """Non-contextual baseline: mean of the model's *input* embeddings per item.

    This is the 'bag of word vectors with no context' control. If contextual
    hidden states cannot beat this, the alignment is not about language
    processing — it is about lexical identity.
    """
    import torch

    emb = model.get_input_embeddings()
    feats: list[np.ndarray] = []
    with torch.no_grad():
        for t in texts:
            ids = tokenizer(t, return_tensors="pt", truncation=True, max_length=512)["input_ids"].to(device)
            vecs = emb(ids).squeeze(0)            # (T, d)
            feats.append(vecs.mean(dim=0).float().cpu().numpy())
    return np.stack(feats, axis=0)


# --------------------------------------------------------------------------- #
# Encoding model + contiguous block CV
# --------------------------------------------------------------------------- #
def contiguous_folds(n: int, k: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """Yield (train_idx, test_idx) for K CONTIGUOUS blocks. No shuffling.

    Test block i is a contiguous slice; train is everything else. Contiguity is
    the whole point — it stops temporal-autocorrelation leakage between train
    and test (Feghhi 2024).
    """
    bounds = np.linspace(0, n, k + 1).astype(int)
    folds = []
    all_idx = np.arange(n)
    for i in range(k):
        test = all_idx[bounds[i] : bounds[i + 1]]
        train = np.concatenate([all_idx[: bounds[i]], all_idx[bounds[i + 1] :]])
        if len(test) and len(train):
            folds.append((train, test))
    return folds


def _maybe_pca(X_tr, X_te, n_pca):
    """PCA-reduce features, fit on TRAIN only (no leakage). Encoding models live in
    the d >> n regime (few stimuli, wide hidden states); reducing to the top
    components is standard practice and keeps ridge R^2 well-behaved."""
    if not n_pca or X_tr.shape[1] <= n_pca:
        return X_tr, X_te
    from sklearn.decomposition import PCA

    pca = PCA(n_components=min(n_pca, X_tr.shape[0] - 1, X_tr.shape[1]))
    pca.fit(X_tr)
    return pca.transform(X_tr), pca.transform(X_te)


def _ridge_r2(X_tr, Y_tr, X_te, Y_te, alphas, n_pca=None) -> np.ndarray:
    """Fit standardized RidgeCV (GCV alpha selection on train) -> per-voxel R^2 on test."""
    from sklearn.linear_model import RidgeCV
    from sklearn.preprocessing import StandardScaler

    X_tr, X_te = _maybe_pca(X_tr, X_te, n_pca)
    xs = StandardScaler().fit(X_tr)
    X_tr_s, X_te_s = xs.transform(X_tr), xs.transform(X_te)
    # Center Y on train mean so R^2 is well-defined on the contiguous test block.
    y_mean = Y_tr.mean(axis=0, keepdims=True)
    model = RidgeCV(alphas=alphas)
    model.fit(X_tr_s, Y_tr - y_mean)
    pred = model.predict(X_te_s) + y_mean
    # Per-voxel R^2 against the test mean.
    ss_res = ((Y_te - pred) ** 2).sum(axis=0)
    ss_tot = ((Y_te - Y_te.mean(axis=0, keepdims=True)) ** 2).sum(axis=0)
    return 1.0 - ss_res / np.clip(ss_tot, 1e-8, None)


def encoding_score(
    X: np.ndarray,
    Y: np.ndarray,
    k_folds: int = 5,
    alphas=(1.0, 10.0, 100.0, 1000.0, 10000.0),
    n_pca: int | None = 50,
) -> dict:
    """Contiguous-block CV encoding R^2 of features X predicting fMRI Y.

    Returns mean R^2 across voxels and folds, plus the per-fold means so the
    caller can compute uncertainty. RAW score — see variance_partition for the
    confound-corrected number.
    """
    folds = contiguous_folds(len(X), k_folds)
    per_fold_voxel = []
    for tr, te in folds:
        r2 = _ridge_r2(X[tr], Y[tr], X[te], Y[te], list(alphas), n_pca=n_pca)
        per_fold_voxel.append(r2)
    per_fold_mean = np.array([v.mean() for v in per_fold_voxel])
    return {
        "mean_r2": float(per_fold_mean.mean()),
        "per_fold_mean_r2": per_fold_mean.tolist(),
        "mean_voxel_r2": np.mean(per_fold_voxel, axis=0).tolist(),
    }


def variance_partition(
    X: np.ndarray,
    Z_scalar: np.ndarray,
    S: np.ndarray,
    Y: np.ndarray,
    k_folds: int = 5,
    alphas=(1.0, 10.0, 100.0, 1000.0, 10000.0),
    n_pca: int | None = 50,
) -> dict:
    """The honest brain-alignment number: UNIQUE variance of contextual X over nuisance.

    Nuisance has two blocks: raw scalars `Z_scalar` (length, position) and the
    static / non-contextual embedding `S` (mean input embedding per item). The
    static block AND the contextual block X are PCA-reduced to the SAME number of
    components per fold (train-fit), so the partition is CAPACITY-FAIR — the
    contextual features are not handed an unfair dimensionality advantage over
    the static-embedding confound, nor vice versa.

      R2_nuis  = [Z_scalar, PCA(S)]          -> Y
      R2_full  = [Z_scalar, PCA(S), PCA(X)]  -> Y
      unique_X = R2_full - R2_nuis           (gain from CONTEXT, post-confound)

    A positive `unique_r2` that survives this subtraction is the only result the
    thesis is allowed to claim as brain alignment (Feghhi 2024; learnings L003).
    """
    folds = contiguous_folds(len(X), k_folds)
    nuis, full = [], []
    for tr, te in folds:
        Xtr_r, Xte_r = _maybe_pca(X[tr], X[te], n_pca)
        Str_r, Ste_r = _maybe_pca(S[tr], S[te], n_pca)
        nuis_tr = np.concatenate([Z_scalar[tr], Str_r], axis=1)
        nuis_te = np.concatenate([Z_scalar[te], Ste_r], axis=1)
        full_tr = np.concatenate([nuis_tr, Xtr_r], axis=1)
        full_te = np.concatenate([nuis_te, Xte_r], axis=1)
        nuis.append(_ridge_r2(nuis_tr, Y[tr], nuis_te, Y[te], list(alphas)).mean())
        full.append(_ridge_r2(full_tr, Y[tr], full_te, Y[te], list(alphas)).mean())
    nuis = np.array(nuis)
    full = np.array(full)
    unique = full - nuis
    return {
        "r2_nuisance": float(nuis.mean()),
        "r2_full": float(full.mean()),
        "unique_r2": float(unique.mean()),
        "unique_r2_per_fold": unique.tolist(),
        "unique_r2_std": float(unique.std(ddof=1)) if len(unique) > 1 else 0.0,
    }


# --------------------------------------------------------------------------- #
# Distillation
# --------------------------------------------------------------------------- #
@dataclass
class DistillConfig:
    epochs: int = 3
    lr: float = 5e-5
    batch_size: int = 8
    max_length: int = 64
    kd_temperature: float = 2.0
    lambda_kd: float = 1.0          # KL on logits
    lambda_hidden: float = 0.0      # optional hidden-state MSE (projected)
    lambda_brain: float = 0.0       # brain-alignment loss weight (0 = baseline arm)
    student_layer: int = -1         # which student hidden layer feeds the brain head
    teacher_layer: int = -1


@dataclass
class DistillResult:
    arm: str
    seed: int
    final_loss: float
    final_kd: float
    final_brain: float
    steps: int
    extra: dict = field(default_factory=dict)
