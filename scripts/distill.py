#!/usr/bin/env python3
"""Distillation with an optional brain-alignment loss term.

Teacher (gpt2-medium) -> student (gpt2). Both share the GPT-2 byte-level BPE
vocab, so logit-space KD aligns token-for-token with no remapping. The student
is the standard `gpt2` checkpoint, fine-tuned under the distillation objective.

Two arms, identical budget, differ only in `lambda_brain`:
  * baseline arm : L = lambda_kd * KL(student || teacher)            (brain-blind)
  * brain arm    : L = lambda_kd * KL(...) + lambda_brain * L_brain

L_brain is the toy operationalisation of "preserve brain-predictive structure":
a trainable linear head maps the student's middle-layer pooled hidden state to
the fMRI responses of the *training* stimuli, and its MSE is added to the loss.
This pressures the student's representation to keep the component that predicts
the brain. The head is discarded at evaluation; encoding R^2 is re-measured with
a fresh ridge on a CONTIGUOUS eval block the brain loss never saw (no leakage).

This is deliberately the simplest defensible L_brain. Whether a frozen-encoding-
map loss or a CKA proxy is better was a later design decision — this
pilot exists to prove the *pipeline*, not to lock the loss.
"""
from __future__ import annotations

import numpy as np

from pilot_lib import DistillConfig, DistillResult, middle_layer_index


def _masked_mean(hs, attention_mask):
    mask = attention_mask.unsqueeze(-1).float()
    return (hs * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1.0)


def distill(
    teacher,
    student,
    tokenizer,
    train_texts: list[str],
    cfg: DistillConfig,
    device: str,
    fmri_train: np.ndarray | None = None,
    seed: int = 0,
    arm: str = "baseline",
) -> DistillResult:
    """Run the distillation loop for one arm and return a DistillResult.

    `fmri_train` (n_train_items, n_voxels) is required when cfg.lambda_brain > 0;
    its row order must match `train_texts`.
    """
    import torch
    from torch import nn

    teacher.eval()
    student.train()
    for p in teacher.parameters():
        p.requires_grad_(False)

    s_layer = cfg.student_layer if cfg.student_layer >= 0 else middle_layer_index(student)
    params = list(student.parameters())

    brain_head = None
    fmri_t = None
    if cfg.lambda_brain > 0:
        if fmri_train is None:
            raise ValueError("brain arm requires fmri_train")
        n_vox = fmri_train.shape[1]
        d_student = student.config.hidden_size
        brain_head = nn.Linear(d_student, n_vox).to(device)
        params = params + list(brain_head.parameters())
        fmri_t = torch.tensor(fmri_train, dtype=torch.float32, device=device)

    opt = torch.optim.AdamW(params, lr=cfg.lr)
    T = cfg.kd_temperature
    n = len(train_texts)
    idx = np.arange(n)

    last = {"loss": 0.0, "kd": 0.0, "brain": 0.0}
    steps = 0
    for epoch in range(cfg.epochs):
        # Shuffle the ITEM ORDER for SGD only; this does not touch the contiguous
        # train/eval data split (the eval block is held out entirely upstream).
        rng = np.random.default_rng(seed * 1000 + epoch)
        order = rng.permutation(idx)
        for start in range(0, n, cfg.batch_size):
            bidx = order[start : start + cfg.batch_size]
            batch = [train_texts[i] for i in bidx]
            enc = tokenizer(
                batch, return_tensors="pt", padding=True,
                truncation=True, max_length=cfg.max_length,
            ).to(device)

            with torch.no_grad():
                t_out = teacher(**enc)
            s_out = student(**enc, output_hidden_states=(brain_head is not None))

            # --- KD: temperature-scaled KL on next-token logits, masked --------
            t_logp = torch.log_softmax(t_out.logits / T, dim=-1)
            s_logp = torch.log_softmax(s_out.logits / T, dim=-1)
            kl = torch.exp(t_logp) * (t_logp - s_logp)           # (B, Tk, V)
            tok_mask = enc["attention_mask"].unsqueeze(-1).float()
            kd = (kl.sum(-1, keepdim=True) * tok_mask).sum() / tok_mask.sum()
            kd = kd * (T * T)
            loss = cfg.lambda_kd * kd

            # --- Brain-alignment loss -----------------------------------------
            brain_val = torch.tensor(0.0, device=device)
            if brain_head is not None:
                pooled = _masked_mean(s_out.hidden_states[s_layer], enc["attention_mask"])
                pred = brain_head(pooled)                        # (B, n_vox)
                target = fmri_t[bidx]
                brain_val = nn.functional.mse_loss(pred, target)
                loss = loss + cfg.lambda_brain * brain_val

            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
            steps += 1
            last = {"loss": float(loss.item()), "kd": float(kd.item()),
                    "brain": float(brain_val.item())}

    student.eval()
    return DistillResult(
        arm=arm, seed=seed, final_loss=last["loss"], final_kd=last["kd"],
        final_brain=last["brain"], steps=steps,
    )
