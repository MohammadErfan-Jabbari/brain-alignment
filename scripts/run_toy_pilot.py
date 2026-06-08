#!/usr/bin/env python3
"""Toy brain-alignment distillation pilot — orchestrator.

The make-or-break feasibility test (charter, oracle review): does adding a
brain-alignment loss during GPT-2-medium -> GPT-2 distillation improve the
student's encoding-model fit to fMRI, measured under the anti-confound protocol,
versus an identical brain-blind distillation?

Per seed it runs two arms at MATCHED budget (same data, epochs, lr, KD weight),
differing only by `lambda_brain`. It reports, on a CONTIGUOUS held-out eval block
the brain loss never saw:
  * raw encoding R^2 (the inflatable number), and
  * unique R^2 = R^2([nuisance, LM features]) - R^2(nuisance)   <-- the honest one
where nuisance = length + position + static (non-contextual) embeddings.

Backends (see data_adapters):
  --backend synthetic   known-structure stand-in (always available; smoke test)
  --backend pereira     Pereira 2018 sentence responses (--data-dir REQUIRED)

Run:
  export HF_HOME=/home/centcom/data/hf-cache
  uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json
  uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json \
      --backend pereira --data-dir data/pereira/exp2
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np

from data_adapters import (
    load_pereira,
    load_sentences_txt,
    make_synthetic_fmri,
    synthetic_sentences,
)
from distill import distill
from pilot_lib import (
    DistillConfig,
    ExtractConfig,
    encoding_score,
    extract_hidden_states,
    middle_layer_index,
    pick_device,
    scalar_nuisance,
    set_seed,
    static_embedding_features,
    variance_partition,
)

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=str, default=str(ROOT / "configs/toy_pilot.json"))
    p.add_argument("--backend", type=str, default=None, choices=["synthetic", "pereira"])
    p.add_argument("--data-dir", type=str, default=None)
    p.add_argument("--seeds", type=int, nargs="+", default=None)
    p.add_argument("--lambda-brain", type=float, default=None,
                   help="Override the brain-loss weight for the brain arm.")
    p.add_argument("--out", type=str, default=None)
    p.add_argument("--smoke", action="store_true",
                   help="Tiny/fast settings (CPU-friendly) for a pipeline smoke test.")
    return p.parse_args()


def load_config(args: argparse.Namespace) -> dict:
    cfg = json.loads(Path(args.config).read_text())
    if args.backend:
        cfg["backend"] = args.backend
    if args.data_dir:
        cfg["data_dir"] = args.data_dir
    if args.seeds:
        cfg["seeds"] = args.seeds
    if args.lambda_brain is not None:
        cfg["lambda_brain"] = args.lambda_brain
    if args.out:
        cfg["out"] = args.out
    if args.smoke:
        cfg.update(cfg.get("smoke_overrides", {}))
    return cfg


def get_data(cfg: dict, base_feats_fn) -> tuple[list[str], np.ndarray, dict]:
    """Return (texts, fmri, meta). Synthetic Y is built from real LM features."""
    backend = cfg.get("backend", "synthetic")
    if backend == "pereira":
        return load_pereira(cfg["data_dir"], cfg.get("experiment", "384sentences"),
                            cfg.get("subject"))
    # synthetic: use real stimulus sentences if provided (hybrid: real text,
    # synthetic responses), else generated toy sentences. Real fMRI responses
    # aligned to these same sentences plug in tomorrow via the pereira backend.
    sents_file = cfg.get("sentences_file")
    if sents_file:
        texts = load_sentences_txt(sents_file, limit=cfg.get("n_items"))
    else:
        texts = synthetic_sentences(cfg.get("n_items", 240), seed=0)
    feats = base_feats_fn(texts)
    lengths = np.array([len(t.split()) for t in texts], dtype=np.float64)
    Y, meta = make_synthetic_fmri(
        feats, lengths,
        n_voxels=cfg.get("n_voxels", 200),
        signal=cfg.get("syn_signal", 1.0),
        nuisance_strength=cfg.get("syn_nuisance", 0.7),
        noise=cfg.get("syn_noise", 1.0),
        seed=0,
    )
    return texts, Y, meta


def zscore_train(Y: np.ndarray, train_idx: np.ndarray) -> np.ndarray:
    mu = Y[train_idx].mean(0, keepdims=True)
    sd = Y[train_idx].std(0, keepdims=True) + 1e-6
    return (Y - mu) / sd


def evaluate_features(X_eval, Z_scalar, S_eval, Y_eval, k_folds, n_pca) -> dict:
    raw = encoding_score(X_eval, Y_eval, k_folds=k_folds, n_pca=n_pca)
    part = variance_partition(X_eval, Z_scalar, S_eval, Y_eval, k_folds=k_folds, n_pca=n_pca)
    return {"raw_r2": raw["mean_r2"], **part}


def main() -> None:
    args = parse_args()
    cfg = load_config(args)
    device = pick_device()
    backend = cfg.get("backend", "synthetic")
    seeds = cfg.get("seeds", [0, 1, 2])
    k_folds = cfg.get("k_folds", 5)
    n_pca = cfg.get("n_pca", 50)
    eval_frac = cfg.get("eval_frac", 0.3)

    out_dir = Path(cfg.get("out", ROOT / "outputs/toy-pilot")) / f"{backend}_{int(time.time())}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[pilot] backend={backend} device={device} seeds={seeds} out={out_dir}")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    teacher_name = cfg.get("teacher", "gpt2-medium")
    student_name = cfg.get("student", "gpt2")
    tok = AutoTokenizer.from_pretrained(teacher_name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    teacher = AutoModelForCausalLM.from_pretrained(teacher_name).to(device)
    teacher.eval()

    ext = ExtractConfig(pool=cfg.get("pool", "mean"), max_length=cfg.get("max_length", 64),
                        batch_size=cfg.get("extract_bs", 16))

    def teacher_feats(texts):
        return extract_hidden_states(teacher, tok, texts, ext, device,
                                     layer=middle_layer_index(teacher))

    # --- Data ---------------------------------------------------------------
    texts, Y, data_meta = get_data(cfg, teacher_feats)
    n = len(texts)
    # Contiguous train/eval split — the eval block is held out from the brain loss.
    split = int(round(n * (1 - eval_frac)))
    train_idx = np.arange(split)
    eval_idx = np.arange(split, n)
    Yz = zscore_train(Y, train_idx)
    train_texts = [texts[i] for i in train_idx]
    eval_texts = [texts[i] for i in eval_idx]
    fmri_train = Yz[train_idx]
    Y_eval = Yz[eval_idx]
    print(f"[pilot] n={n} train={len(train_idx)} eval={len(eval_idx)} "
          f"voxels={Y.shape[1]} backend_meta={data_meta.get('backend')}")

    # --- Fixed nuisance design on the eval block (identical across arms) -----
    # Static (non-contextual) embeddings come from the FROZEN teacher so the
    # nuisance baseline is byte-identical for every arm — a fair comparison.
    Z_scalar = scalar_nuisance(eval_texts, tok)
    S_eval = static_embedding_features(teacher, tok, eval_texts, device)

    # --- Reference: teacher + untrained student on eval ----------------------
    refs = {}
    Xt = teacher_feats(eval_texts)
    refs["teacher"] = evaluate_features(Xt, Z_scalar, S_eval, Y_eval, k_folds, n_pca)
    s0 = AutoModelForCausalLM.from_pretrained(student_name).to(device)
    Xs0 = extract_hidden_states(s0, tok, eval_texts, ext, device, layer=middle_layer_index(s0))
    refs["student_untrained"] = evaluate_features(Xs0, Z_scalar, S_eval, Y_eval, k_folds, n_pca)
    del s0
    if device == "cuda":
        torch.cuda.empty_cache()
    print(f"[pilot] ref teacher unique_r2={refs['teacher']['unique_r2']:.4f} "
          f"raw={refs['teacher']['raw_r2']:.4f} | untrained student "
          f"unique_r2={refs['student_untrained']['unique_r2']:.4f}")

    dcfg = DistillConfig(
        epochs=cfg.get("epochs", 3), lr=cfg.get("lr", 5e-5),
        batch_size=cfg.get("batch_size", 8), max_length=cfg.get("max_length", 64),
        kd_temperature=cfg.get("kd_temperature", 2.0),
        lambda_kd=cfg.get("lambda_kd", 1.0), lambda_hidden=0.0,
        lambda_brain=cfg.get("lambda_brain", 1.0),
    )

    rows = []
    for seed in seeds:
        for arm, lam in (("baseline", 0.0), ("brain", dcfg.lambda_brain)):
            set_seed(seed)
            student = AutoModelForCausalLM.from_pretrained(student_name).to(device)
            arm_cfg = DistillConfig(**{**asdict(dcfg), "lambda_brain": lam})
            dres = distill(teacher, student, tok, train_texts, arm_cfg, device,
                           fmri_train=fmri_train if lam > 0 else None, seed=seed, arm=arm)
            Xe = extract_hidden_states(student, tok, eval_texts, ext, device,
                                       layer=middle_layer_index(student))
            metrics = evaluate_features(Xe, Z_scalar, S_eval, Y_eval, k_folds, n_pca)
            row = {"seed": seed, "arm": arm, "lambda_brain": lam,
                   "final_loss": dres.final_loss, "final_kd": dres.final_kd,
                   "final_brain": dres.final_brain, **metrics}
            rows.append(row)
            print(f"[pilot] seed={seed} arm={arm:8s} "
                  f"raw_r2={metrics['raw_r2']:.4f} unique_r2={metrics['unique_r2']:.4f} "
                  f"(nuis={metrics['r2_nuisance']:.4f} full={metrics['r2_full']:.4f})")
            del student
            if device == "cuda":
                torch.cuda.empty_cache()

    # --- Aggregate: paired Δ(unique_r2) across seeds ------------------------
    def by_arm(arm, key):
        return np.array([r[key] for r in rows if r["arm"] == arm])

    base_u = by_arm("baseline", "unique_r2")
    brain_u = by_arm("brain", "unique_r2")
    delta = brain_u - base_u            # paired by seed order
    summary = {
        "backend": backend,
        "data_meta": data_meta,
        "config": cfg,
        "device": device,
        "n_items": n, "n_train": len(train_idx), "n_eval": len(eval_idx),
        "n_voxels": int(Y.shape[1]),
        "seeds": seeds,
        "refs": refs,
        "baseline_unique_r2_mean": float(base_u.mean()),
        "baseline_unique_r2_std": float(base_u.std(ddof=1)) if len(base_u) > 1 else 0.0,
        "brain_unique_r2_mean": float(brain_u.mean()),
        "brain_unique_r2_std": float(brain_u.std(ddof=1)) if len(brain_u) > 1 else 0.0,
        "delta_unique_r2_mean": float(delta.mean()),
        "delta_unique_r2_std": float(delta.std(ddof=1)) if len(delta) > 1 else 0.0,
        "delta_per_seed": delta.tolist(),
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    with (out_dir / "results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("\n[pilot] ===== SUMMARY =====")
    print(f"  baseline unique_r2 = {summary['baseline_unique_r2_mean']:.4f} "
          f"± {summary['baseline_unique_r2_std']:.4f}")
    print(f"  brain    unique_r2 = {summary['brain_unique_r2_mean']:.4f} "
          f"± {summary['brain_unique_r2_std']:.4f}")
    print(f"  Δ(unique_r2)       = {summary['delta_unique_r2_mean']:+.4f} "
          f"± {summary['delta_unique_r2_std']:.4f}  (n={len(seeds)} seeds, paired)")
    print(f"  teacher reference unique_r2 = {refs['teacher']['unique_r2']:.4f}")
    print(f"  wrote {out_dir}/summary.json and results.csv")


if __name__ == "__main__":
    main()
