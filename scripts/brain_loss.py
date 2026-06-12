#!/usr/bin/env python3
"""Differentiable brain-alignment loss family — the D010 candidates.

`L_brain` pressures a model's pooled middle-layer hidden state `h` (B, d) to be
more predictive of fMRI BOLD `Y` (B, n_roi). Five candidate forms, chosen from
the brain-tuning literature and the conditional-MI grounding (docs/06 §3):

  * "mse"     : ||W h - Y||^2 with a co-trained linear readout W (+ ridge penalty).
                The theory-preferred form — the differentiable twin of the eval
                metric (unique encoding R^2 = conditional MI under a Gaussian map).
                moussa-2025 L2; best-at-scale in their ablation.
  * "cos"     : 1 - cosine(W h, Y), co-trained W. bilgin-2026 text-LM form.
  * "pearson" : - mean_roi r(W h, Y)^2 over the batch, co-trained W.
                merlin-2026 (neg squared Pearson); moussa small-data winner.
  * "frozen"  : ||W0 h - Y||^2 with W0 = ridge fit on the UNTUNED model's block-A
                features then FROZEN. D010 option (b); no text-LM precedent.
  * "cka"     : 1 - linearCKA(h, Y), NO readout (geometric). D010 option (c);
                kornblith-2019. Expected weak: CKA is rotation/scale invariant,
                so the model can satisfy it by rotating (a flagged risk).

The readout (for mse/cos/pearson/frozen) is owned by the caller; these functions
take the already-projected prediction `pred = W h` (except cka, which takes `h`).
Everything is batch-wise and differentiable. torch is imported lazily so the
module imports without a GPU present (mirrors pilot_lib).
"""
from __future__ import annotations

import numpy as np

BRAIN_LOSS_KINDS = ("mse", "cos", "pearson", "frozen", "cka", "contrastive")
# kinds that use a linear readout W: pred = W h  (frozen uses a frozen W)
READOUT_KINDS = ("mse", "cos", "pearson", "frozen", "contrastive")


def mse_loss(pred, target):
    """Mean squared error between readout prediction and BOLD. (moussa L2.)"""
    import torch.nn.functional as F
    return F.mse_loss(pred, target)


def cos_loss(pred, target):
    """1 - mean per-item cosine similarity. (bilgin-2026.)

    Per row (item), cosine between the predicted and observed ROI vectors; we
    maximise it, i.e. minimise (1 - cos). With only 5 ROIs this is a coarse but
    cheap directional objective.
    """
    import torch.nn.functional as F
    cos = F.cosine_similarity(pred, target, dim=-1)        # (B,)
    return 1.0 - cos.mean()


def neg_pearson_sq_loss(pred, target, eps: float = 1e-8):
    """- mean over ROIs of squared Pearson r across the batch. (merlin-2026.)

    For each ROI column, Pearson correlation of the predicted vs observed value
    over the items in the batch; minimise the negative squared correlation
    (maximise variance-explained-style alignment). Needs batch_size >> 1 to be a
    stable estimate — the caller uses batch_size=16+.
    """
    import torch
    # center each column over the batch
    p = pred - pred.mean(dim=0, keepdim=True)
    t = target - target.mean(dim=0, keepdim=True)
    num = (p * t).sum(dim=0)
    den = torch.sqrt((p * p).sum(dim=0) * (t * t).sum(dim=0) + eps)
    r = num / (den + eps)                                  # (n_roi,)
    return -(r ** 2).mean()


def linear_cka_loss(h, target, eps: float = 1e-8):
    """1 - linear CKA between pooled hidden states h (B,d) and BOLD (B,n_roi).

    Linear CKA = ||X_c^T Y_c||_F^2 / (||X_c^T X_c||_F * ||Y_c^T Y_c||_F), with
    both matrices column/feature-centered over the batch (kornblith-2019). No
    readout — compares representational geometry directly. Rotation/isotropic-
    scale invariant (the documented weakness as a training signal).
    """
    import torch
    X = h - h.mean(dim=0, keepdim=True)
    Y = target - target.mean(dim=0, keepdim=True)
    # HSIC-style cross term via Gram matrices: ||X^T Y||_F^2 = <X X^T, Y Y^T>
    xty = X.t() @ Y                                        # (d, n_roi)
    hsic_xy = (xty * xty).sum()
    xtx = X.t() @ X
    yty = Y.t() @ Y
    hsic_xx = (xtx * xtx).sum()
    hsic_yy = (yty * yty).sum()
    cka = hsic_xy / (torch.sqrt(hsic_xx * hsic_yy) + eps)
    return 1.0 - cka


def infonce_loss(pred, target, temp: float = 0.07):
    """Symmetric InfoNCE / NT-Xent (CLIP-style) contrastive loss — Negi-2025's objective
    family. Co-trained readout pred = W h (B, n_roi) is pulled toward its OWN-item BOLD
    target and away from the other items' BOLD in the batch (positives on the diagonal).
    Cosine-similarity logits / temperature; averaged over the two directions.

    Caveat (honest): on the 5-ROI Tuckute target the contrastive space is low-dimensional,
    so this is a weaker test of the objective axis than a voxelwise contrastive (E013); it
    nonetheless asks whether a ranking/contrastive objective (vs MSE regression) changes the
    per-individual result on data we have."""
    import torch
    import torch.nn.functional as F
    p = F.normalize(pred, dim=-1)
    t = F.normalize(target, dim=-1)
    logits = p @ t.t() / temp                       # (B, B)
    labels = torch.arange(p.size(0), device=p.device)
    return 0.5 * (F.cross_entropy(logits, labels) + F.cross_entropy(logits.t(), labels))


def brain_loss(kind: str, pred_or_h, target):
    """Dispatch to the requested brain-loss form.

    For READOUT_KINDS, `pred_or_h` is the readout output W h (B, n_roi).
    For "cka", `pred_or_h` is the pooled hidden state h (B, d).
    """
    if kind in ("mse", "frozen"):
        return mse_loss(pred_or_h, target)
    if kind == "cos":
        return cos_loss(pred_or_h, target)
    if kind == "pearson":
        return neg_pearson_sq_loss(pred_or_h, target)
    if kind == "cka":
        return linear_cka_loss(pred_or_h, target)
    if kind == "contrastive":
        return infonce_loss(pred_or_h, target)
    raise ValueError(f"unknown brain-loss kind: {kind!r} (want one of {BRAIN_LOSS_KINDS})")


def fit_ridge_readout(h: np.ndarray, Y: np.ndarray, alpha: float = 100.0):
    """Closed-form ridge W mapping standardized features h -> BOLD Y, for the
    FROZEN arm. Returns (W, b, x_mean, x_std, y_mean) so the caller can apply
    pred = ((h - x_mean)/x_std) @ W + y_mean on the fly.

    W = (Xs^T Xs + alpha I)^-1 Xs^T (Y - y_mean), standardized X, centered Y —
    matching pilot_lib._ridge_r2's standardize-X / center-Y convention so the
    frozen readout is the same object the eval metric would fit.
    """
    x_mean = h.mean(axis=0, keepdims=True)
    x_std = h.std(axis=0, keepdims=True) + 1e-8
    Xs = (h - x_mean) / x_std
    y_mean = Y.mean(axis=0, keepdims=True)
    Yc = Y - y_mean
    d = Xs.shape[1]
    A = Xs.T @ Xs + alpha * np.eye(d)
    W = np.linalg.solve(A, Xs.T @ Yc)                      # (d, n_roi)
    return W.astype(np.float32), x_mean.astype(np.float32), x_std.astype(np.float32), y_mean.astype(np.float32)


def block_permute(Y: np.ndarray, n_blocks: int = 10, seed: int = 0) -> np.ndarray:
    """Block-permuted-fMRI null: shuffle the stimulus<->response correspondence
    while preserving the marginal BOLD distribution and contiguous-block
    structure (moussa random-brain-tuned control template).

    Split the n items into `n_blocks` contiguous blocks and permute the BLOCK
    ORDER (not items within a block), so each item keeps a real BOLD vector from
    a different stimulus and local autocorrelation structure is preserved. A
    real brain lever must beat this null.
    """
    n = Y.shape[0]
    rng = np.random.default_rng(seed)
    bounds = np.linspace(0, n, n_blocks + 1).astype(int)
    blocks = [np.arange(bounds[i], bounds[i + 1]) for i in range(n_blocks)]
    order = rng.permutation(n_blocks)
    # Reassign each block's rows the BOLD of the permuted-partner block, truncating
    # to the min length so shapes line up regardless of uneven block sizes.
    perm_idx = np.arange(n)
    for dst, src in zip(range(n_blocks), order):
        d_idx, s_idx = blocks[dst], blocks[src]
        m = min(len(d_idx), len(s_idx))
        perm_idx[d_idx[:m]] = s_idx[:m]
    return Y[perm_idx]
