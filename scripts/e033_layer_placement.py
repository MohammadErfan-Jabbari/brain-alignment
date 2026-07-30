#!/usr/bin/env python3
"""E033 recorded-response loss-placement robustness runner.

Commands
--------
selftest
    Deterministic plumbing tests with no model or neural endpoint.
gradient-gate
    Builder-only initial-gradient calibration, block-reach diagnostics, and
    dynamic co-trained-head nonabsorption gate. Never scores held-out outcomes.
manifest
    Hash-bind the locked design, code, calibration, ordered targets, folds, and
    matched permutation arrays before scientific outcome scoring.
kd-reference
    Train the 15 shared KD-only fold/seed models and score every participant at
    both fixed evaluation layers.
run-shard
    Train participant-specific mid/final real and matched-permuted target arms.

The owning design is docs/experiments/E033_layer-placement-robustness.md.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brain_loss as BL  # noqa: E402
import pilot_lib as P  # noqa: E402
import run_brain_lever as R  # noqa: E402
from data_adapters import load_tuckute  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
E_RECORD = ROOT / "docs/experiments/E033_layer-placement-robustness.md"
ANALYZER = ROOT / "scripts/e033_analyze_layer_placement.py"
MODEL_NAME = "Qwen/Qwen2.5-0.5B"
TEACHER_NAME = "Qwen/Qwen2.5-1.5B"
ALL_UIDS = (797, 837, 841, 848, 856, 865, 875, 876, 880)
BUILDER_UIDS = (848, 865, 875, 876)
HELDOUT_UIDS = (797, 837, 841, 856, 880)
SEEDS = (0, 1, 2)
N_FOLDS = 5
N_PERM = 5
MID_LAYER = 12
FINAL_LAYER = 24
LAMBDA_MID = 10.0
SESOI = 0.001
PPL_MARGIN = 1.05
TRAINING = {
    "epochs": 3,
    "lr": 2e-4,
    "batch_size": 16,
    "max_length": 64,
    "lora_r": 16,
    "lambda_lm": 1.0,
    "kd_temp": 2.0,
    "grad_clip": 1.0,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def canonical_json_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def write_json(path: str | Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def manifest_digest(value: dict) -> str:
    payload = dict(value)
    payload.pop("manifest_sha256", None)
    return sha256_bytes(canonical_json_bytes(payload))


def artifact_digest(value: dict) -> str:
    payload = dict(value)
    payload.pop("artifact_sha256", None)
    return sha256_bytes(canonical_json_bytes(payload))


def block_permutation(Y: np.ndarray, fold: int, seed: int, draw: int) -> np.ndarray:
    """Exact E008 matched target permutation, independent of attachment placement."""
    return BL.block_permute(
        Y,
        n_blocks=10,
        seed=R.stable_seed("brain_lever_perm", "mse", fold, seed, draw),
    )


def permutation_row_map(n: int, fold: int, seed: int, draw: int) -> np.ndarray:
    rows = np.arange(n, dtype=np.int64).reshape(-1, 1)
    return block_permutation(rows, fold, seed, draw).reshape(-1)


def fold_indices(n: int = 1000) -> dict[int, tuple[np.ndarray, np.ndarray]]:
    return {f: (tr, te) for f, tr, te in R.outer_folds(n, N_FOLDS)}


def resolve_layers(model) -> dict[str, int]:
    n = int(model.config.num_hidden_layers)
    if n != FINAL_LAYER:
        raise RuntimeError(f"E033 requires exactly 24 decoder blocks, got {n}")
    return {"mid": MID_LAYER, "final": n}


def block_number(name: str) -> int | None:
    match = re.search(r"(?:^|\.)layers\.(\d+)(?:\.|$)", name)
    return int(match.group(1)) if match else None


def trainable_lora_named(model) -> list[tuple[str, object]]:
    rows = [(n, p) for n, p in model.named_parameters() if p.requires_grad and "lora_" in n]
    if not rows:
        raise RuntimeError("no trainable LoRA parameters found")
    return rows


def grad_vector(grads: Iterable, params: Iterable) -> np.ndarray:
    import torch

    chunks = []
    for grad, param in zip(grads, params):
        if grad is None:
            chunks.append(torch.zeros_like(param).reshape(-1))
        else:
            chunks.append(grad.detach().reshape(-1))
    if not chunks:
        return np.zeros(0, dtype=np.float64)
    return torch.cat(chunks).float().cpu().numpy()


def vector_norm(vector: np.ndarray) -> float:
    return float(np.linalg.norm(vector.astype(np.float64, copy=False)))


def vector_distance(a: np.ndarray, b: np.ndarray) -> float:
    return vector_norm(
        a.astype(np.float64, copy=False) - b.astype(np.float64, copy=False)
    )


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = vector_norm(a) * vector_norm(b)
    if denom <= 0:
        return float("nan")
    return float(np.dot(a.astype(np.float64), b.astype(np.float64)) / denom)


def heldout_probe_texts() -> list[str]:
    return [
        line
        for line in R.CORPUS_HELDOUT.read_text().splitlines()
        if line.strip()
    ][:1000]


def model_identities(student_config=None, student_tok=None, teacher_config=None) -> dict:
    from transformers import AutoConfig, AutoTokenizer

    if student_config is None:
        student_config = AutoConfig.from_pretrained(MODEL_NAME, local_files_only=True)
    if teacher_config is None:
        teacher_config = AutoConfig.from_pretrained(TEACHER_NAME, local_files_only=True)
    if student_tok is None:
        student_tok = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)

    def config_identity(name, config):
        commit = getattr(config, "_commit_hash", None)
        if not commit:
            raise RuntimeError(f"missing immutable Hugging Face revision for {name}")
        config_json = json.loads(config.to_json_string(use_diff=False))
        return {
            "name": name,
            "commit_hash": str(commit),
            "config_sha256": sha256_bytes(canonical_json_bytes(config_json)),
        }

    tokenizer_json = student_tok.backend_tokenizer.to_str().encode()
    return {
        "student": config_identity(MODEL_NAME, student_config),
        "teacher": config_identity(TEACHER_NAME, teacher_config),
        "tokenizer": {
            "name": MODEL_NAME,
            "backend_sha256": sha256_bytes(tokenizer_json),
            "vocab_size": len(student_tok.get_vocab()),
        },
    }


def bound_input_identity(data_dir: str) -> dict:
    texts_ref = None
    targets = {}
    target_hashes = {}
    for uid in ALL_UIDS:
        texts, Y, _meta = load_tuckute(data_dir, uids=(uid,))
        if texts_ref is None:
            texts_ref = texts
        if texts != texts_ref:
            raise RuntimeError(f"stimulus order differs for uid {uid}")
        targets[uid] = Y
        target_hashes[str(uid)] = sha256_bytes(np.ascontiguousarray(Y).tobytes())

    folds = fold_indices(len(texts_ref))
    fold_hashes = {
        str(fold): {
            "train": sha256_bytes(np.ascontiguousarray(train_idx).tobytes()),
            "eval": sha256_bytes(np.ascontiguousarray(eval_idx).tobytes()),
        }
        for fold, (train_idx, eval_idx) in folds.items()
    }
    permutation_cells = []
    for uid in ALL_UIDS:
        for fold, (train_idx, _eval_idx) in folds.items():
            Y_train = targets[uid][train_idx]
            for seed in SEEDS:
                for draw in range(N_PERM):
                    row_map = permutation_row_map(len(train_idx), fold, seed, draw)
                    perm = block_permutation(Y_train, fold, seed, draw)
                    if not np.array_equal(perm, Y_train[row_map]):
                        raise RuntimeError("permutation row-map identity failed")
                    permutation_cells.append(
                        {
                            "uid": uid,
                            "fold": fold,
                            "seed": seed,
                            "draw": draw,
                            "row_map_sha256": sha256_bytes(
                                np.ascontiguousarray(row_map).tobytes()
                            ),
                            "target_sha256": sha256_bytes(
                                np.ascontiguousarray(perm).tobytes()
                            ),
                        }
                    )
    probe = heldout_probe_texts()
    return {
        "texts_sha256": sha256_bytes(canonical_json_bytes(texts_ref)),
        "target_sha256": target_hashes,
        "fold_sha256": fold_hashes,
        "permutation_cell_count": len(permutation_cells),
        "permutation_aggregate_sha256": sha256_bytes(
            canonical_json_bytes(permutation_cells)
        ),
        "permutation_cells": permutation_cells,
        "ppl_probe_count": len(probe),
        "ppl_probe_sha256": sha256_bytes(canonical_json_bytes(probe)),
    }


def verify_bound_inputs(
    manifest: dict,
    data_dir: str,
    student_config=None,
    student_tok=None,
    teacher_config=None,
) -> None:
    current_inputs = bound_input_identity(data_dir)
    if manifest.get("inputs") != current_inputs:
        raise RuntimeError("runtime data/fold/permutation/PPL inputs differ from manifest")
    current_models = model_identities(student_config, student_tok, teacher_config)
    if manifest.get("model_identities") != current_models:
        raise RuntimeError("runtime model/tokenizer identities differ from manifest")


def block_grad_norms(named_params, grads) -> dict[str, float]:
    accum: dict[int, float] = {}
    for (name, _param), grad in zip(named_params, grads):
        block = block_number(name)
        if block is None:
            continue
        value = 0.0 if grad is None else float(grad.detach().double().pow(2).sum().item())
        accum[block] = accum.get(block, 0.0) + value
    return {str(block): math.sqrt(value) for block, value in sorted(accum.items())}


def kd_loss(model, teacher, enc):
    import torch

    labels = enc["input_ids"].clone()
    labels[enc["attention_mask"] == 0] = -100
    out = model(**enc, labels=labels, output_hidden_states=True)
    with torch.no_grad():
        teacher_logits = teacher(**enc).logits
    temperature = TRAINING["kd_temp"]
    teacher_logp = torch.log_softmax(teacher_logits / temperature, dim=-1)
    student_logp = torch.log_softmax(out.logits / temperature, dim=-1)
    kl = (torch.exp(teacher_logp) * (teacher_logp - student_logp)).sum(-1, keepdim=True)
    mask = enc["attention_mask"].unsqueeze(-1).float()
    retention = (kl * mask).sum() / mask.sum() * (temperature * temperature)
    return out, retention


def co_trained_head(hidden_size: int, n_roi: int, device: str, seed: int):
    import torch
    from torch import nn

    state = torch.random.get_rng_state()
    cuda_state = torch.cuda.get_rng_state(device) if str(device).startswith("cuda") else None
    torch.manual_seed(R.stable_seed("E033_head", seed))
    if str(device).startswith("cuda"):
        torch.cuda.manual_seed_all(R.stable_seed("E033_head", seed))
    head = nn.Linear(hidden_size, n_roi).to(device)
    nn.init.normal_(head.weight, std=0.02)
    nn.init.zeros_(head.bias)
    torch.random.set_rng_state(state)
    if cuda_state is not None:
        torch.cuda.set_rng_state(cuda_state, device)
    return head


def batch_for_fold(texts, Y, fold: int, seed: int, limit: int | None = None):
    train_idx, _ = fold_indices(len(texts))[fold]
    if limit is not None:
        train_idx = train_idx[:limit]
    order = np.random.default_rng(seed * 1000).permutation(np.arange(len(train_idx)))
    local = order[: TRAINING["batch_size"]]
    global_idx = train_idx[local]
    return global_idx, [texts[i] for i in global_idx], Y[global_idx]


def make_lora_model(seed: int, device: str):
    P.set_seed(seed)
    model, tok = R.load_model(MODEL_NAME, device)
    model = R.wrap_lora(model, MODEL_NAME, r=TRAINING["lora_r"])
    model.train()
    return model, tok


def final_hidden_identity(model, tok, texts: list[str], device: str) -> float:
    import torch

    model.eval()
    enc = tok(texts[:2], return_tensors="pt", padding=True, truncation=True, max_length=64).to(device)
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
        reconstructed = model.get_output_embeddings()(out.hidden_states[-1])
    return float((reconstructed - out.logits).abs().max().item())


def frozen_projection(features: np.ndarray, target: np.ndarray):
    return BL.fit_ridge_readout(features, target, alpha=100.0)


def frozen_prediction(hidden, projection, device: str):
    import torch

    W, xm, xs, ym = projection
    tensors = [torch.tensor(v, dtype=hidden.dtype, device=device) for v in (W, xm, xs, ym)]
    Wt, xmt, xst, ymt = tensors
    return ((hidden - xmt) / xst) @ Wt + ymt


def initial_gradient_gate(args) -> dict:
    """Outcome-blind E033A initial calibration and block-reach diagnostics."""
    import torch

    device = P.pick_device()
    texts_by_uid = {}
    targets = {}
    for uid in BUILDER_UIDS:
        texts, Y, _meta = load_tuckute(args.data_dir, uids=(uid,))
        texts_by_uid[uid] = texts
        targets[uid] = Y
    texts = texts_by_uid[BUILDER_UIDS[0]]
    if any(texts_by_uid[u] != texts for u in BUILDER_UIDS):
        raise RuntimeError("builder participant stimulus orders differ")

    base, tok = R.load_model(MODEL_NAME, device)
    teacher, _ = R.load_model(TEACHER_NAME, device)
    teacher.eval()
    for param in teacher.parameters():
        param.requires_grad_(False)
    layers = resolve_layers(base)
    identity_error = final_hidden_identity(base, tok, texts, device)
    if identity_error > 1e-4:
        raise RuntimeError(f"final hidden/logit identity failed: {identity_error}")

    extract_cfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
    base_features = {
        label: P.extract_hidden_states(base, tok, texts, extract_cfg, device, layer=layer)
        for label, layer in layers.items()
    }

    folds = fold_indices(len(texts))
    initial_rows = []
    reach_rows = []
    g_aux = {"mid": [], "final": []}
    g_kd = []

    for seed in SEEDS:
        model, _ = make_lora_model(seed, device)
        named_params = trainable_lora_named(model)
        params = [p for _n, p in named_params]
        heads = {
            label: co_trained_head(model.config.hidden_size, 5, device, seed)
            for label in ("mid", "final")
        }
        heads["final"].load_state_dict(copy.deepcopy(heads["mid"].state_dict()))

        for fold, (train_idx, _eval_idx) in folds.items():
            order = np.random.default_rng(seed * 1000).permutation(np.arange(len(train_idx)))
            global_idx = train_idx[order[: TRAINING["batch_size"]]]
            batch = [texts[i] for i in global_idx]
            enc = tok(batch, return_tensors="pt", padding=True, truncation=True, max_length=64).to(device)
            out, retention = kd_loss(model, teacher, enc)
            kd_grads = torch.autograd.grad(retention, params, retain_graph=True, allow_unused=True)
            kd_vec = grad_vector(kd_grads, params)
            kd_norm = vector_norm(kd_vec)
            g_kd.append(kd_norm)

            for uid in BUILDER_UIDS:
                Y_train = targets[uid][train_idx]
                target_variants = [("real", None, Y_train)]
                for draw in range(N_PERM):
                    target_variants.append(
                        (f"perm{draw}", draw, block_permutation(Y_train, fold, seed, draw))
                    )
                batch_local = order[: TRAINING["batch_size"]]
                for target_label, draw, target_array in target_variants:
                    target_tensor = torch.tensor(
                        target_array[batch_local], dtype=torch.float32, device=device
                    )
                    for placement, layer in layers.items():
                        hidden = R.masked_mean(out.hidden_states[layer], enc["attention_mask"])
                        pred = heads[placement](hidden)
                        aux = BL.brain_loss("mse", pred, target_tensor)
                        aux_grads = torch.autograd.grad(
                            aux, params, retain_graph=True, allow_unused=True
                        )
                        aux_vec = grad_vector(aux_grads, params)
                        aux_norm = vector_norm(aux_vec)
                        g_aux[placement].append(aux_norm)
                        initial_rows.append(
                            {
                                "uid": uid,
                                "fold": fold,
                                "seed": seed,
                                "target": target_label,
                                "perm_draw": draw,
                                "placement": placement,
                                "aux_trunk_norm_unit": aux_norm,
                                "kd_trunk_norm": kd_norm,
                                "aux_kd_cosine": cosine(aux_vec, kd_vec),
                            }
                        )

            if seed == 0 and fold == 0:
                uid = BUILDER_UIDS[0]
                batch_local = order[: TRAINING["batch_size"]]
                Y_train = targets[uid][train_idx]
                diagnostic_targets = [("real", None, Y_train)] + [
                    (
                        f"perm{draw}",
                        draw,
                        block_permutation(Y_train, fold, seed, draw),
                    )
                    for draw in range(N_PERM)
                ]
                frozen_vectors = {"mid": {}, "final": {}}
                for target_label, draw, target_array in diagnostic_targets:
                    target_tensor = torch.tensor(
                        target_array[batch_local], dtype=torch.float32, device=device
                    )
                    for placement, layer in layers.items():
                        projection = frozen_projection(
                            base_features[placement][train_idx], target_array
                        )
                        hidden = R.masked_mean(out.hidden_states[layer], enc["attention_mask"])
                        pred = frozen_prediction(hidden, projection, device)
                        aux = BL.brain_loss("frozen", pred, target_tensor)
                        grads = torch.autograd.grad(
                            aux, params, retain_graph=True, allow_unused=True
                        )
                        vec = grad_vector(grads, params)
                        frozen_vectors[placement][target_label] = vec
                        reach_rows.append(
                            {
                                "uid": uid,
                                "fold": fold,
                                "seed": seed,
                                "target": target_label,
                                "placement": placement,
                                "trunk_norm": vector_norm(vec),
                                "block_norms": block_grad_norms(named_params, grads),
                                "aux_kd_cosine": cosine(vec, kd_vec),
                            }
                        )
                for placement in ("mid", "final"):
                    real_vec = frozen_vectors[placement]["real"]
                    perm_labels = [f"perm{draw}" for draw in range(N_PERM)]
                    for label in perm_labels:
                        reach_rows.append(
                            {
                                "uid": uid,
                                "fold": fold,
                                "seed": seed,
                                "placement": placement,
                                "diagnostic": "aligned_vs_permuted_gradient_distance",
                                "left": "real",
                                "right": label,
                                "distance": vector_distance(
                                    real_vec, frozen_vectors[placement][label]
                                ),
                            }
                        )
                    for left_index, left in enumerate(perm_labels):
                        for right in perm_labels[left_index + 1 :]:
                            reach_rows.append(
                                {
                                    "uid": uid,
                                    "fold": fold,
                                    "seed": seed,
                                    "placement": placement,
                                    "diagnostic": "permutation_vs_permutation_gradient_distance",
                                    "left": left,
                                    "right": right,
                                    "distance": vector_distance(
                                        frozen_vectors[placement][left],
                                        frozen_vectors[placement][right],
                                    ),
                                }
                            )
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    median_mid = float(np.median(g_aux["mid"]))
    median_final = float(np.median(g_aux["final"]))
    median_kd = float(np.median(g_kd))
    lambda_final = LAMBDA_MID * median_mid / median_final if median_final > 0 else float("nan")
    ratio_mid = LAMBDA_MID * median_mid / median_kd if median_kd > 0 else float("nan")
    ratio_final = lambda_final * median_final / median_kd if median_kd > 0 else float("nan")

    reach_checks = []
    for row in reach_rows:
        if "block_norms" not in row:
            continue
        norms = {int(k): float(v) for k, v in row["block_norms"].items()}
        if row["placement"] == "mid":
            upstream = all(math.isfinite(norms.get(b, 0.0)) and norms.get(b, 0.0) > 1e-12 for b in range(12))
            downstream = all(norms.get(b, 0.0) <= 1e-12 for b in range(12, 24))
            passed = upstream and downstream
        else:
            passed = all(
                math.isfinite(norms.get(b, 0.0)) and norms.get(b, 0.0) > 1e-12
                for b in range(24)
            )
        reach_checks.append(
            {
                "placement": row["placement"],
                "target": row["target"],
                "passed": bool(passed),
            }
        )

    ratio_match = (
        math.isfinite(ratio_mid)
        and math.isfinite(ratio_final)
        and max(ratio_mid, ratio_final) / min(ratio_mid, ratio_final) <= 1.10
    )
    initial_pass = bool(
        identity_error <= 1e-4
        and all(check["passed"] for check in reach_checks)
        and math.isfinite(lambda_final)
        and 0.1 <= lambda_final <= 100.0
        and ratio_mid >= 0.01
        and ratio_final >= 0.01
        and ratio_match
    )
    return {
        "stage": "initial",
        "science_outcomes_opened": False,
        "model": MODEL_NAME,
        "teacher": TEACHER_NAME,
        "layers": layers,
        "builder_uids": list(BUILDER_UIDS),
        "identity_max_abs": identity_error,
        "lambda_mid": LAMBDA_MID,
        "lambda_final": lambda_final,
        "median_aux_unit": {"mid": median_mid, "final": median_final},
        "median_kd_trunk_norm": median_kd,
        "weighted_aux_kd_ratio": {"mid": ratio_mid, "final": ratio_final},
        "ratio_match_within_10pct": ratio_match,
        "reach_checks": reach_checks,
        "reach_rows": reach_rows,
        "initial_rows": initial_rows,
        "passed": initial_pass,
    }


def dynamic_training_metrics(
    texts,
    Y,
    placement: str,
    layer: int,
    lam: float,
    fold: int,
    seed: int,
    target_label: str,
    device: str,
    teacher,
    tok,
):
    import torch

    train_idx, _eval_idx = fold_indices(len(texts))[fold]
    Y_train = Y[train_idx]
    if target_label == "perm0":
        Y_train = block_permutation(Y_train, fold, seed, 0)
    model, _ = make_lora_model(seed, device)
    named_params = trainable_lora_named(model)
    params = [p for _n, p in named_params]
    head = co_trained_head(model.config.hidden_size, Y.shape[1], device, seed)
    opt = torch.optim.AdamW(params + list(head.parameters()), lr=TRAINING["lr"])
    initial = [p.detach().clone() for p in params]
    target_tensor = torch.tensor(Y_train, dtype=torch.float32, device=device)
    checkpoints = {1, 75, 150}
    records = []
    step = 0
    for epoch in range(TRAINING["epochs"]):
        order = np.random.default_rng(seed * 1000 + epoch).permutation(np.arange(len(train_idx)))
        for start in range(0, len(train_idx), TRAINING["batch_size"]):
            local_idx = order[start : start + TRAINING["batch_size"]]
            global_idx = train_idx[local_idx]
            batch = [texts[i] for i in global_idx]
            enc = tok(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=TRAINING["max_length"],
            ).to(device)
            out, retention = kd_loss(model, teacher, enc)
            hidden = R.masked_mean(out.hidden_states[layer], enc["attention_mask"])
            pred = head(hidden)
            aux = BL.brain_loss("mse", pred, target_tensor[local_idx])
            total = retention + lam * aux
            step += 1
            pre_record = None
            if step in checkpoints:
                kd_grads = torch.autograd.grad(
                    retention, params, retain_graph=True, allow_unused=True
                )
                aux_grads = torch.autograd.grad(
                    aux, params, retain_graph=True, allow_unused=True
                )
                kd_vec = grad_vector(kd_grads, params)
                aux_vec = grad_vector(aux_grads, params) * lam
                head_grads = torch.autograd.grad(
                    aux, list(head.parameters()), retain_graph=True, allow_unused=True
                )
                head_vec = grad_vector(head_grads, list(head.parameters()))
                pre_record = {
                    "step": step,
                    "weighted_aux_trunk_norm": vector_norm(aux_vec),
                    "kd_trunk_norm": vector_norm(kd_vec),
                    "weighted_aux_kd_ratio": (
                        vector_norm(aux_vec) / vector_norm(kd_vec)
                        if vector_norm(kd_vec) > 0
                        else float("nan")
                    ),
                    "weighted_aux_kd_cosine": cosine(aux_vec, kd_vec),
                    "head_grad_norm": vector_norm(head_vec),
                }
            opt.zero_grad()
            total.backward()
            torch.nn.utils.clip_grad_norm_(params + list(head.parameters()), TRAINING["grad_clip"])
            opt.step()
            if pre_record is not None:
                update_sq = 0.0
                for param, start_param in zip(params, initial):
                    update_sq += float((param.detach() - start_param).double().pow(2).sum().item())
                pre_record["lora_update_norm"] = math.sqrt(update_sq)
                records.append(pre_record)
    if step != 150:
        raise RuntimeError(f"dynamic gate expected 150 steps, got {step}")
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return records


def run_gradient_gate(args) -> None:
    import torch

    t0 = time.time()
    initial = initial_gradient_gate(args)
    if not initial["passed"]:
        result = {
            "stage": "E033A",
            "passed": False,
            "stop_reason": "initial gradient/reach/calibration gate failed",
            "initial": initial,
            "dynamic": None,
            "elapsed_seconds": time.time() - t0,
        }
        write_json(args.out, result)
        raise SystemExit("E033A STOP: initial gate failed")

    device = P.pick_device()
    teacher, _ = R.load_model(TEACHER_NAME, device)
    _student, tok = R.load_model(MODEL_NAME, device)
    del _student
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    teacher.eval()
    for param in teacher.parameters():
        param.requires_grad_(False)
    layers = initial["layers"]
    lambdas = {"mid": initial["lambda_mid"], "final": initial["lambda_final"]}
    dynamic_rows = []
    for uid in BUILDER_UIDS:
        texts, Y, _meta = load_tuckute(args.data_dir, uids=(uid,))
        for seed in SEEDS:
            for placement in ("mid", "final"):
                for target_label in ("real", "perm0"):
                    records = dynamic_training_metrics(
                        texts,
                        Y,
                        placement,
                        layers[placement],
                        lambdas[placement],
                        fold=0,
                        seed=seed,
                        target_label=target_label,
                        device=device,
                        teacher=teacher,
                        tok=tok,
                    )
                    for record in records:
                        dynamic_rows.append(
                            {
                                "uid": uid,
                                "seed": seed,
                                "fold": 0,
                                "placement": placement,
                                "target": target_label,
                                **record,
                            }
                        )

    dynamic_checks = []
    for placement in ("mid", "final"):
        for step in (1, 75, 150):
            rows = [
                row
                for row in dynamic_rows
                if row["placement"] == placement and row["step"] == step
            ]
            real = [
                row
                for row in rows
                if row["target"] == "real"
            ]
            ratios = [float(row["weighted_aux_kd_ratio"]) for row in real]
            finite_nonzero = all(
                all(
                    math.isfinite(float(row[key])) and float(row[key]) > 0
                    for key in (
                        "weighted_aux_trunk_norm",
                        "kd_trunk_norm",
                        "weighted_aux_kd_ratio",
                        "head_grad_norm",
                        "lora_update_norm",
                    )
                )
                for row in rows
            )
            cosine_finite_nonzero = all(
                math.isfinite(float(row["weighted_aux_kd_cosine"]))
                and abs(float(row["weighted_aux_kd_cosine"])) > 0
                for row in rows
            )
            median_ratio = float(np.median(ratios))
            dynamic_checks.append(
                {
                    "placement": placement,
                    "step": step,
                    "median_real_weighted_aux_kd_ratio": median_ratio,
                    "finite_nonzero": finite_nonzero,
                    "cosine_finite_nonzero": cosine_finite_nonzero,
                    "passed": bool(
                        finite_nonzero
                        and cosine_finite_nonzero
                        and median_ratio >= 0.01
                    ),
                }
            )

    passed = bool(all(check["passed"] for check in dynamic_checks))
    result = {
        "stage": "E033A",
        "science_outcomes_opened": False,
        "passed": passed,
        "initial": initial,
        "dynamic": {"rows": dynamic_rows, "checks": dynamic_checks},
        "frozen_lambdas": lambdas,
        "elapsed_seconds": time.time() - t0,
        "runner_sha256": sha256_file(__file__),
        "e_record_sha256": sha256_file(E_RECORD),
    }
    result["artifact_sha256"] = sha256_bytes(canonical_json_bytes(result))
    write_json(args.out, result)
    if not passed:
        raise SystemExit("E033A STOP: dynamic nonabsorption gate failed")
    print(
        f"E033A PASS lambda_mid={lambdas['mid']:.8g} "
        f"lambda_final={lambdas['final']:.8g} wrote {args.out}"
    )


def locked_config(calibration: dict) -> dict:
    return {
        "experiment": "E033",
        "model": MODEL_NAME,
        "teacher": TEACHER_NAME,
        "all_uids": list(ALL_UIDS),
        "builder_uids": list(BUILDER_UIDS),
        "heldout_uids": list(HELDOUT_UIDS),
        "seeds": list(SEEDS),
        "n_folds": N_FOLDS,
        "n_perm": N_PERM,
        "layers": {"mid": MID_LAYER, "final": FINAL_LAYER},
        "eval_layers": [MID_LAYER, FINAL_LAYER],
        "lambdas": {
            "mid": float(calibration["frozen_lambdas"]["mid"]),
            "final": float(calibration["frozen_lambdas"]["final"]),
        },
        "training": TRAINING,
        "sesoi": SESOI,
        "ppl_margin": PPL_MARGIN,
    }


def verify_calibration(calibration: dict) -> None:
    if (
        calibration.get("stage") != "E033A"
        or calibration.get("science_outcomes_opened") is not False
        or not calibration.get("passed")
        or not calibration.get("initial", {}).get("passed")
        or calibration.get("dynamic") is None
    ):
        raise RuntimeError("calibration is not a complete outcome-blind E033A PASS")
    if artifact_digest(calibration) != calibration.get("artifact_sha256"):
        raise RuntimeError("calibration artifact self-hash mismatch")
    if calibration.get("runner_sha256") != sha256_file(__file__):
        raise RuntimeError("calibration was produced by a different runner")
    if calibration.get("e_record_sha256") != sha256_file(E_RECORD):
        raise RuntimeError("calibration was produced from a different E033 design")


def run_manifest(args) -> None:
    calibration = json.loads(Path(args.calibration).read_text())
    verify_calibration(calibration)
    config = locked_config(calibration)
    inputs = bound_input_identity(args.data_dir)
    identities = model_identities()
    files = {
        "runner": sha256_file(__file__),
        "analyzer": sha256_file(ANALYZER),
        "e_record": sha256_file(E_RECORD),
        "calibration": sha256_file(args.calibration),
    }
    manifest = {
        "experiment": "E033",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "config": config,
        "files": files,
        "calibration_artifact_sha256": calibration["artifact_sha256"],
        "inputs": inputs,
        "model_identities": identities,
    }
    manifest["manifest_sha256"] = manifest_digest(manifest)
    write_json(args.out, manifest)
    print(f"manifest {manifest['manifest_sha256']} wrote {args.out}")


def load_and_verify_manifest(path: str | Path, calibration_path: str | Path) -> dict:
    manifest = json.loads(Path(path).read_text())
    if manifest_digest(manifest) != manifest.get("manifest_sha256"):
        raise RuntimeError("manifest self-hash mismatch")
    expected_files = {
        "runner": sha256_file(__file__),
        "analyzer": sha256_file(ANALYZER),
        "e_record": sha256_file(E_RECORD),
        "calibration": sha256_file(calibration_path),
    }
    if manifest.get("files") != expected_files:
        raise RuntimeError(
            f"manifest executable/design hashes changed: {manifest.get('files')} != {expected_files}"
        )
    calibration = json.loads(Path(calibration_path).read_text())
    verify_calibration(calibration)
    if manifest.get("calibration_artifact_sha256") != calibration.get("artifact_sha256"):
        raise RuntimeError("calibration artifact identity mismatch")
    if manifest.get("config") != locked_config(calibration):
        raise RuntimeError("manifest config mismatch")
    return manifest


def score_from_features(X, Z, S, Y) -> tuple[float, list[float]]:
    result = P.variance_partition(X, Z, S, Y, k_folds=5, n_pca=50)
    return float(result["unique_r2"]), [float(x) for x in result["unique_r2_per_fold"]]


def common_data(data_dir: str, uids: Iterable[int]):
    targets = {}
    texts_ref = None
    metas = {}
    for uid in uids:
        texts, Y, meta = load_tuckute(data_dir, uids=(int(uid),))
        if texts_ref is None:
            texts_ref = texts
        if texts != texts_ref:
            raise RuntimeError(f"stimulus order differs for uid {uid}")
        targets[int(uid)] = Y
        metas[int(uid)] = meta
    return texts_ref, targets, metas


def base_nuisance(base, tok, texts, device):
    Z = P.scalar_nuisance(texts, tok)
    S = P.static_embedding_features(base, tok, texts, device)
    return Z, S


def run_kd_reference(args) -> None:
    import torch

    manifest = load_and_verify_manifest(args.manifest, args.calibration)
    device = P.pick_device()
    texts, targets, _metas = common_data(args.data_dir, ALL_UIDS)
    base, tok = R.load_model(MODEL_NAME, device)
    teacher, _ = R.load_model(TEACHER_NAME, device)
    teacher.eval()
    for param in teacher.parameters():
        param.requires_grad_(False)
    verify_bound_inputs(
        manifest,
        args.data_dir,
        student_config=base.config,
        student_tok=tok,
        teacher_config=teacher.config,
    )
    resolve_layers(base)
    Z, S = base_nuisance(base, tok, texts, device)
    heldout = heldout_probe_texts()
    rows = []
    t0 = time.time()
    folds = fold_indices(len(texts))
    for fold, (train_idx, eval_idx) in folds.items():
        eval_texts = [texts[i] for i in eval_idx]
        for seed in SEEDS:
            P.set_seed(seed)
            model, _ = R.load_model(MODEL_NAME, device)
            dummy = np.zeros((len(train_idx), 5), dtype=np.float32)
            trained = R.brain_tune(
                model,
                tok,
                [texts[i] for i in train_idx],
                dummy,
                None,
                0.0,
                1.0,
                MID_LAYER,
                device,
                TRAINING["epochs"],
                TRAINING["lr"],
                TRAINING["batch_size"],
                seed,
                use_lora=True,
                model_name=MODEL_NAME,
                lora_r=TRAINING["lora_r"],
                teacher=teacher,
                kd_temp=TRAINING["kd_temp"],
            )
            ppl = R.eval_perplexity(trained, tok, heldout, device)
            for eval_layer in (MID_LAYER, FINAL_LAYER):
                cfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
                X_base = P.extract_hidden_states(
                    base, tok, eval_texts, cfg, device, layer=eval_layer
                )
                X_kd = P.extract_hidden_states(
                    trained, tok, eval_texts, cfg, device, layer=eval_layer
                )
                for uid in ALL_UIDS:
                    Y_eval = targets[uid][eval_idx]
                    base_score, base_internal = score_from_features(
                        X_base, Z[eval_idx], S[eval_idx], Y_eval
                    )
                    score, internal = score_from_features(
                        X_kd, Z[eval_idx], S[eval_idx], Y_eval
                    )
                    rows.append(
                        {
                            "uid": uid,
                            "fold": fold,
                            "seed": seed,
                            "arm": "kd_only",
                            "eval_layer": eval_layer,
                            "unique_r2": score,
                            "base_unique_r2": base_score,
                            "delta_vs_base": score - base_score,
                            "unique_r2_internal_folds": internal,
                            "base_internal_folds": base_internal,
                            "perplexity": ppl,
                        }
                    )
            del trained
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    output = {
        "experiment": "E033",
        "stage": "kd-reference",
        "science": True,
        "manifest_sha256": manifest["manifest_sha256"],
        "calibration_artifact_sha256": manifest["calibration_artifact_sha256"],
        "config": manifest["config"],
        "rows": rows,
        "elapsed_seconds": time.time() - t0,
    }
    write_json(args.out, output)
    print(f"KD reference rows={len(rows)} wrote {args.out}")


def selected_runtime(args, manifest: dict | None):
    if args.smoke:
        seeds = tuple(args.seeds or (0,))
        folds = tuple(args.fold_indices or (0,))
        n_perm = int(args.n_perm if args.n_perm is not None else 1)
    else:
        seeds = SEEDS
        folds = tuple(range(N_FOLDS))
        n_perm = N_PERM
        if args.seeds or args.fold_indices or args.n_perm is not None or args.limit_tune:
            raise RuntimeError("scientific run forbids runtime grid overrides")
        if manifest is None:
            raise RuntimeError("scientific run requires manifest")
    return seeds, folds, n_perm


def run_target_shard(args) -> None:
    import torch

    calibration = json.loads(Path(args.calibration).read_text())
    verify_calibration(calibration)
    manifest = None if args.smoke else load_and_verify_manifest(args.manifest, args.calibration)
    config = locked_config(calibration)
    lambdas = config["lambdas"]
    seeds, fold_subset, n_perm = selected_runtime(args, manifest)
    uids = tuple(int(u) for u in args.uids)
    if not uids or any(uid not in ALL_UIDS for uid in uids):
        raise RuntimeError(f"invalid UID shard {uids}")
    device = P.pick_device()
    texts, targets, _metas = common_data(args.data_dir, uids)
    base, tok = R.load_model(MODEL_NAME, device)
    teacher, _ = R.load_model(TEACHER_NAME, device)
    teacher.eval()
    for param in teacher.parameters():
        param.requires_grad_(False)
    if manifest is not None:
        verify_bound_inputs(
            manifest,
            args.data_dir,
            student_config=base.config,
            student_tok=tok,
            teacher_config=teacher.config,
        )
    resolve_layers(base)
    Z, S = base_nuisance(base, tok, texts, device)
    heldout = heldout_probe_texts()
    extract_cfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
    rows = []
    folds = fold_indices(len(texts))
    t0 = time.time()

    for fold in fold_subset:
        train_idx, eval_idx = folds[fold]
        if args.limit_tune is not None:
            train_idx = train_idx[: args.limit_tune]
        train_texts = [texts[i] for i in train_idx]
        eval_texts = [texts[i] for i in eval_idx]
        base_features = {
            eval_layer: P.extract_hidden_states(
                base, tok, eval_texts, extract_cfg, device, layer=eval_layer
            )
            for eval_layer in (MID_LAYER, FINAL_LAYER)
        }
        for uid in uids:
            Y = targets[uid]
            base_scores = {}
            for eval_layer in (MID_LAYER, FINAL_LAYER):
                base_scores[eval_layer] = score_from_features(
                    base_features[eval_layer], Z[eval_idx], S[eval_idx], Y[eval_idx]
                )
            for seed in seeds:
                target_variants = [("real", None, Y[train_idx])]
                for draw in range(n_perm):
                    target_variants.append(
                        (
                            f"perm{draw}",
                            draw,
                            block_permutation(Y[train_idx], fold, seed, draw),
                        )
                    )
                for placement, train_layer in (("mid", MID_LAYER), ("final", FINAL_LAYER)):
                    for target_label, draw, Y_train in target_variants:
                        P.set_seed(seed)
                        model, _ = R.load_model(MODEL_NAME, device)
                        trained = R.brain_tune(
                            model,
                            tok,
                            train_texts,
                            Y_train,
                            "mse",
                            float(lambdas[placement]),
                            1.0,
                            train_layer,
                            device,
                            TRAINING["epochs"],
                            TRAINING["lr"],
                            TRAINING["batch_size"],
                            seed,
                            use_lora=True,
                            model_name=MODEL_NAME,
                            lora_r=TRAINING["lora_r"],
                            teacher=teacher,
                            kd_temp=TRAINING["kd_temp"],
                        )
                        ppl = R.eval_perplexity(trained, tok, heldout, device)
                        for eval_layer in (MID_LAYER, FINAL_LAYER):
                            X = P.extract_hidden_states(
                                trained,
                                tok,
                                eval_texts,
                                extract_cfg,
                                device,
                                layer=eval_layer,
                            )
                            score, internal = score_from_features(
                                X, Z[eval_idx], S[eval_idx], Y[eval_idx]
                            )
                            base_score, base_internal = base_scores[eval_layer]
                            rows.append(
                                {
                                    "uid": uid,
                                    "fold": fold,
                                    "seed": seed,
                                    "placement": placement,
                                    "train_layer": train_layer,
                                    "target": target_label,
                                    "perm_draw": draw,
                                    "eval_layer": eval_layer,
                                    "unique_r2": score,
                                    "base_unique_r2": base_score,
                                    "delta_vs_base": score - base_score,
                                    "unique_r2_internal_folds": internal,
                                    "base_internal_folds": base_internal,
                                    "perplexity": ppl,
                                    "lambda_brain": float(lambdas[placement]),
                                }
                            )
                        del trained
                        if torch.cuda.is_available():
                            torch.cuda.empty_cache()
    output = {
        "experiment": "E033",
        "stage": "placement-smoke" if args.smoke else "placement-shard",
        "science": not args.smoke,
        "manifest_sha256": None if manifest is None else manifest["manifest_sha256"],
        "calibration_artifact_sha256": calibration["artifact_sha256"],
        "config": config,
        "runtime": {
            "uids": list(uids),
            "seeds": list(seeds),
            "folds": list(fold_subset),
            "n_perm": n_perm,
            "limit_tune": args.limit_tune,
            "smoke": bool(args.smoke),
        },
        "rows": rows,
        "elapsed_seconds": time.time() - t0,
    }
    write_json(args.out, output)
    print(f"{output['stage']} rows={len(rows)} wrote {args.out}")


def run_selftest() -> None:
    import torch

    assert block_number("base_model.model.model.layers.23.self_attn.q_proj.lora_A.default.weight") == 23
    assert block_number("lm_head.weight") is None
    Y = np.arange(200, dtype=float).reshape(100, 2)
    a = block_permutation(Y, 0, 0, 0)
    b = block_permutation(Y, 0, 0, 0)
    c = block_permutation(Y, 0, 0, 1)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)
    value = {"b": 2, "a": 1}
    digest = manifest_digest(value)
    value["manifest_sha256"] = digest
    assert manifest_digest(value) == digest

    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = torch.nn.ModuleList([torch.nn.Linear(4, 4, bias=False) for _ in range(4)])

        def forward(self, x):
            states = [x]
            for layer in self.layers:
                x = torch.tanh(layer(x))
                states.append(x)
            return states

    toy = Toy()
    x = torch.ones(2, 4)
    states = toy(x)
    mid_grads = torch.autograd.grad(states[2].sum(), list(toy.parameters()), allow_unused=True)
    states = toy(x)
    final_grads = torch.autograd.grad(states[-1].sum(), list(toy.parameters()), allow_unused=True)
    assert mid_grads[0] is not None and mid_grads[1] is not None
    assert mid_grads[2] is None and mid_grads[3] is None
    assert all(grad is not None for grad in final_grads)
    print("E033 selftest PASS")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("selftest")

    gate = sub.add_parser("gradient-gate")
    gate.add_argument("--data-dir", default="data/tuckute2024")
    gate.add_argument("--out", default="outputs/E033/gradient_gate.json")

    manifest = sub.add_parser("manifest")
    manifest.add_argument("--data-dir", default="data/tuckute2024")
    manifest.add_argument("--calibration", default="outputs/E033/gradient_gate.json")
    manifest.add_argument("--out", default="outputs/E033/manifest.json")

    kd = sub.add_parser("kd-reference")
    kd.add_argument("--data-dir", default="data/tuckute2024")
    kd.add_argument("--calibration", default="outputs/E033/gradient_gate.json")
    kd.add_argument("--manifest", default="outputs/E033/manifest.json")
    kd.add_argument("--out", default="outputs/E033/kd_reference.json")

    shard = sub.add_parser("run-shard")
    shard.add_argument("--uids", nargs="+", type=int, required=True)
    shard.add_argument("--data-dir", default="data/tuckute2024")
    shard.add_argument("--calibration", default="outputs/E033/gradient_gate.json")
    shard.add_argument("--manifest", default="outputs/E033/manifest.json")
    shard.add_argument("--out", required=True)
    shard.add_argument("--smoke", action="store_true")
    shard.add_argument("--seeds", nargs="*", type=int)
    shard.add_argument("--fold-indices", nargs="*", type=int)
    shard.add_argument("--n-perm", type=int)
    shard.add_argument("--limit-tune", type=int)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "selftest":
        run_selftest()
    elif args.command == "gradient-gate":
        run_gradient_gate(args)
    elif args.command == "manifest":
        run_manifest(args)
    elif args.command == "kd-reference":
        run_kd_reference(args)
    elif args.command == "run-shard":
        run_target_shard(args)
    else:
        raise AssertionError(args.command)


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
