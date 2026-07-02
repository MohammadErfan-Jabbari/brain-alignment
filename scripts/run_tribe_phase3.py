#!/usr/bin/env python3
"""E016 Phase 3 runner: KD-only vs KD+TRIBE vs KD+TRIBE-permuted.

This is infrastructure, not a verdict engine. It trains matched-budget arms on
a KD corpus slice backed by a TRIBE target cache, records held-out perplexity,
and optionally records held-out TRIBE-target encoding if a heldout target cache
is supplied. The analyzer decides whether the run is science-ready.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import brain_loss as BL  # noqa: E402
import pilot_lib as P  # noqa: E402
from distill import distill  # noqa: E402
from pilot_lib import DistillConfig  # noqa: E402
from run_kd_alignment import eval_perplexity  # noqa: E402

CORPUS_HELDOUT = ROOT / "data/kd_corpus/wikitext103_sentences_heldout.txt"


def read_lines(path: Path, limit: int | None = None) -> list[str]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines if limit is None else lines[:limit]


def load_cache(path: Path) -> dict:
    raw = np.load(path, allow_pickle=True)
    meta = json.loads(str(raw["metadata"].item())) if "metadata" in raw else {}
    return {
        "path": path,
        "targets": raw["targets"].astype(np.float32),
        "texts": [str(x) for x in raw["texts"].tolist()],
        "item_indices": raw["item_indices"].astype(np.int64),
        "vertex_index": raw["vertex_index"].astype(np.int64),
        "metadata": meta,
    }


def standardize_train(Y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = Y.mean(axis=0, keepdims=True)
    std = Y.std(axis=0, keepdims=True) + 1e-6
    return ((Y - mean) / std).astype(np.float32), mean.astype(np.float32), std.astype(np.float32)


def apply_standardize(Y: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return ((Y - mean) / std).astype(np.float32)


def load_lm(name: str, device: str):
    from transformers import AutoModelForCausalLM

    return AutoModelForCausalLM.from_pretrained(name).to(device)


def load_tokenizer(name: str):
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok


def target_encoding_r2(model, tok, train_texts, Y_train, heldout_texts, Y_heldout, device, max_length, layer):
    """Fresh ridge readout from pooled hidden states to TRIBE targets."""
    from sklearn.linear_model import RidgeCV
    from sklearn.preprocessing import StandardScaler

    ext = P.ExtractConfig(pool="mean", max_length=max_length, batch_size=32)
    Xtr = P.extract_hidden_states(model, tok, train_texts, ext, device, layer=layer)
    Xte = P.extract_hidden_states(model, tok, heldout_texts, ext, device, layer=layer)
    xs = StandardScaler().fit(Xtr)
    y_mean = Y_train.mean(axis=0, keepdims=True)
    ridge = RidgeCV(alphas=[1.0, 10.0, 100.0, 1000.0, 10000.0])
    ridge.fit(xs.transform(Xtr), Y_train - y_mean)
    pred = ridge.predict(xs.transform(Xte)) + y_mean
    ss_res = ((Y_heldout - pred) ** 2).sum(axis=0)
    ss_tot = ((Y_heldout - Y_heldout.mean(axis=0, keepdims=True)) ** 2).sum(axis=0)
    r2 = 1.0 - ss_res / np.clip(ss_tot, 1e-8, None)
    return float(np.mean(r2))


def lambda_grid(spec: str) -> list[float]:
    vals = [float(x) for x in spec.split(",") if x.strip()]
    if not vals:
        raise ValueError("--lambda-brain-grid must contain at least one float")
    return vals


def validate_target_label(label: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", label):
        raise ValueError("--target-label must contain only letters, digits, and underscores")
    return label


def jsonable_args(args: argparse.Namespace) -> dict:
    out = {}
    for key, value in vars(args).items():
        out[key] = str(value) if isinstance(value, Path) else value
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-cache", type=Path, required=True)
    ap.add_argument("--target-label", default="tribe", help="arm prefix for target/permuted arms")
    ap.add_argument("--heldout-target-cache", type=Path, default=None)
    ap.add_argument("--heldout-corpus", type=Path, default=CORPUS_HELDOUT)
    ap.add_argument("--out", type=Path, default=ROOT / "outputs/E016_tribe/phase3/phase3_smoke.json")
    ap.add_argument("--teacher", default="gpt2-medium")
    ap.add_argument("--student", default="gpt2")
    ap.add_argument("--seeds", default="0")
    ap.add_argument("--lambda-brain-grid", default="1.0")
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--max-length", type=int, default=64)
    ap.add_argument("--limit-train", type=int, default=None)
    ap.add_argument("--limit-heldout", type=int, default=128)
    ap.add_argument("--perm-blocks", type=int, default=10)
    ap.add_argument("--skip-target-r2", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    device = P.pick_device()
    target_label = validate_target_label(args.target_label)
    train_cache = load_cache(args.target_cache)
    train_texts = train_cache["texts"]
    Y = train_cache["targets"]
    if args.limit_train is not None:
        train_texts = train_texts[: args.limit_train]
        Y = Y[: args.limit_train]
    Yz, y_mean, y_std = standardize_train(Y)

    heldout_texts = read_lines(args.heldout_corpus, args.limit_heldout)
    Yh = None
    if args.heldout_target_cache is not None:
        heldout_cache = load_cache(args.heldout_target_cache)
        heldout_texts = heldout_cache["texts"][: len(heldout_texts)]
        Yh = apply_standardize(heldout_cache["targets"][: len(heldout_texts)], y_mean, y_std)

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    lams = lambda_grid(args.lambda_brain_grid)
    tok = load_tokenizer(args.student)
    teacher = load_lm(args.teacher, device).eval()

    dcfg_base = DistillConfig(
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
        max_length=args.max_length,
        kd_temperature=2.0,
        lambda_kd=1.0,
        lambda_hidden=0.0,
        lambda_brain=0.0,
    )

    rows = []
    for seed in seeds:
        arm_specs: list[tuple[str, float, np.ndarray | None]] = [("kd_only", 0.0, None)]
        for lam in lams:
            arm_specs.append((f"{target_label}_mse", lam, Yz))
            Yperm = BL.block_permute(Yz, n_blocks=min(args.perm_blocks, max(1, len(Yz))), seed=seed)
            arm_specs.append((f"{target_label}_perm", lam, Yperm))
        for arm, lam, target in arm_specs:
            print(f"== seed={seed} arm={arm} lambda={lam} ==", flush=True)
            P.set_seed(seed)
            student = load_lm(args.student, device)
            cfg = DistillConfig(**{**asdict(dcfg_base), "lambda_brain": lam})
            result = distill(
                teacher,
                student,
                tok,
                train_texts,
                cfg,
                device,
                fmri_train=target,
                seed=seed,
                arm=arm,
            )
            ppl = eval_perplexity(student, tok, heldout_texts, device, max_length=args.max_length)
            layer = P.middle_layer_index(student)
            target_r2 = None
            if Yh is not None and not args.skip_target_r2:
                target_r2 = target_encoding_r2(
                    student, tok, train_texts, Yz, heldout_texts, Yh, device, args.max_length, layer
                )
            rows.append(
                {
                    **asdict(result),
                    "lambda_brain": lam,
                    "perplexity": ppl,
                    "target_r2": target_r2,
                    "target_dim": int(Yz.shape[1]),
                    "n_train": len(train_texts),
                    "n_heldout_ppl": len(heldout_texts),
                }
            )
            print(
                f"  ppl={ppl:.3f}"
                + ("" if target_r2 is None else f" target_r2={target_r2:+.4f}"),
                flush=True,
            )
            del student
            try:
                import torch

                torch.cuda.empty_cache()
            except Exception:
                pass

    payload = {
        "experiment": "E016 Phase 3 synthetic-target KD",
        "science_status": "runner output; analyzer gate required before interpretation",
        "teacher": args.teacher,
        "student": args.student,
        "device": device,
        "target_cache": str(args.target_cache),
        "target_label": target_label,
        "heldout_target_cache": str(args.heldout_target_cache) if args.heldout_target_cache else None,
        "target_cache_meta": train_cache["metadata"],
        "config": jsonable_args(args),
        "target_standardization": {
            "mean_shape": list(y_mean.shape),
            "std_shape": list(y_std.shape),
            "std_min": float(y_std.min()),
            "std_max": float(y_std.max()),
        },
        "rows": rows,
        "elapsed_s": round(time.time() - t0, 3),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"saved {args.out}", flush=True)


if __name__ == "__main__":
    main()
