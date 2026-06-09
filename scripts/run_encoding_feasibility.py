#!/usr/bin/env python3
"""E002 — real-data encoding feasibility on Tuckute 2024 (the A2 question).

The foundational question the charter says gates everything, and the one the
synthetic pilot (E001) *could not* answer by construction (L004):

    On REAL neural data, does an LM's contextual middle-layer representation
    predict language-network BOLD *beyond* nuisance (length, position, static
    embeddings), under the contiguous-split anti-confound protocol — and how
    large is that unique signal relative to the noise ceiling?

We test this on Tuckute et al. 2024 (1000 isolated baseline sentences x 5 LH
language ROIs, train-participant average, published noise ceiling). Cheap,
high-ceiling, real. We sweep layers for a few models and include the critical
Feghhi control: a RANDOMLY-INITIALISED model of the same architecture. If an
untrained net "explains" the BOLD as well as a trained one after nuisance
subtraction, the signal is not about language processing (A2 fails).

Outputs raw R^2, unique R^2 (contextual over nuisance, capacity-fair), and the
noise-ceiling-normalised unique R^2, per (model, layer). Untrained controls are
run over >=3 random seeds. Nothing here distills anything — this is the encoding
feasibility probe that must pass before the distillation Delta (E001) is worth
running on real data.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P  # noqa: E402
from data_adapters import load_tuckute  # noqa: E402


def _load_model(name: str, device: str, untrained: bool, seed: int):
    """Load a HF causal LM + tokenizer. untrained=True re-initialises weights
    from the config (the Feghhi random-network control)."""
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    if untrained:
        cfg = AutoConfig.from_pretrained(name)
        P.set_seed(seed)
        model = AutoModelForCausalLM.from_config(cfg)
    else:
        model = AutoModelForCausalLM.from_pretrained(name)
    return model.to(device).eval(), tok


def _layers_to_probe(model, requested) -> list[int]:
    n = model.config.num_hidden_layers
    if requested:
        return [l if l >= 0 else n + 1 + l for l in requested]
    # default: a spread around the middle (the brain-alignment sweet spot)
    mids = sorted({max(1, int(round(f * n))) for f in (0.25, 0.5, 0.6, 0.75)})
    return mids


def run_model(name, texts, Y, device, layers, untrained, seed, n_pca):
    model, tok = _load_model(name, device, untrained, seed)
    ecfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
    Z = P.scalar_nuisance(texts, tok)                                  # (n,2)
    S = P.static_embedding_features(model, tok, texts, device)         # (n,d)
    out = []
    for layer in _layers_to_probe(model, layers):
        X = P.extract_hidden_states(model, tok, texts, ecfg, device, layer=layer)
        raw = P.encoding_score(X, Y, k_folds=5, n_pca=n_pca)
        part = P.variance_partition(X, Z, S, Y, k_folds=5, n_pca=n_pca)
        rec = {"model": name, "untrained": untrained, "seed": seed, "layer": layer,
               "raw_r2": raw["mean_r2"],
               "unique_r2": part["unique_r2"], "unique_r2_std": part["unique_r2_std"],
               "r2_nuisance": part["r2_nuisance"], "r2_full": part["r2_full"]}
        out.append(rec)
        tag = "untrained" if untrained else "trained"
        print(f"  [{name} {tag} L{layer:>2}] raw={rec['raw_r2']:+.4f}  "
              f"nuis={rec['r2_nuisance']:+.4f}  full={rec['r2_full']:+.4f}  "
              f"unique={rec['unique_r2']:+.4f}±{rec['unique_r2_std']:.4f}", flush=True)
    del model
    import torch
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--models", nargs="+", default=["gpt2", "gpt2-medium"])
    ap.add_argument("--layers", nargs="*", type=int, default=None,
                    help="hidden_states indices; default = spread around middle")
    ap.add_argument("--target", default="subrois", choices=["subrois", "netw"])
    ap.add_argument("--untrained-seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--n-pca", type=int, default=50)
    ap.add_argument("--out", default="outputs/E002_tuckute_feasibility.json")
    args = ap.parse_args()

    device = P.pick_device()
    texts, Y, meta = load_tuckute(args.data_dir, target=args.target)
    print(f"Tuckute: {meta['n_items']} sentences x {meta['n_voxels']} ROI "
          f"({meta['rois']}); noise ceiling (LangNetw) nc={meta['noise_ceiling_langnetw']}")
    print(f"device={device}\n")

    results = []
    for name in args.models:
        print(f"== {name} (trained) ==")
        results += run_model(name, texts, Y, device, args.layers, False, 0, args.n_pca)
        print(f"== {name} (untrained control, seeds {args.untrained_seeds}) ==")
        for s in args.untrained_seeds:
            results += run_model(name, texts, Y, device, args.layers, True, s, args.n_pca)

    # Best trained layer per model + untrained mean at that layer (the A2 contrast).
    summary = {}
    for name in args.models:
        tr = [r for r in results if r["model"] == name and not r["untrained"]]
        best = max(tr, key=lambda r: r["unique_r2"])
        un_same = [r["unique_r2"] for r in results
                   if r["model"] == name and r["untrained"] and r["layer"] == best["layer"]]
        nc = meta["noise_ceiling_langnetw"]
        summary[name] = {
            "best_layer": best["layer"],
            "trained_unique_r2": best["unique_r2"],
            "trained_unique_r2_std": best["unique_r2_std"],
            "untrained_unique_r2_mean": float(np.mean(un_same)) if un_same else None,
            "untrained_unique_r2_std": float(np.std(un_same, ddof=1)) if len(un_same) > 1 else None,
            "trained_minus_untrained": (best["unique_r2"] - float(np.mean(un_same))) if un_same else None,
            "nc_normalised_unique_r2": (best["unique_r2"] / nc) if nc else None,
        }
        s = summary[name]
        print(f"\n[SUMMARY {name}] best L{s['best_layer']}: trained unique R^2 "
              f"= {s['trained_unique_r2']:+.4f}±{s['trained_unique_r2_std']:.4f}, "
              f"untrained = {s['untrained_unique_r2_mean']:+.4f}, "
              f"trained-untrained = {s['trained_minus_untrained']:+.4f}, "
              f"NC-normalised = {s['nc_normalised_unique_r2']:+.3f}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(
        {"meta": meta, "results": results, "summary": summary,
         "config": vars(args)}, indent=2))
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
