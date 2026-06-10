#!/usr/bin/env python3
"""E003 — does perplexity-only KD preserve or destroy brain alignment? (R04 Layer 2a)

The cheap, decisive kill-test from R04 §6(a). NOT alignment-guided KD (that is
E004); here lambda_brain is 0 everywhere. We distil gpt2-medium (teacher) into a
gpt2-architecture student with PURE logit/perplexity KD and measure how much of
the teacher's brain alignment the student carries, under the E002 anti-confound
protocol (contiguous CV, nuisance subtraction, capacity-fair PCA, NC-normalised).

The design (locked in docs/experiments/E003_kd-alignment-preservation.md) was
reshaped by two Opus reviews. The load-bearing fixes are baked in here:
  * THE VERDICT ARM IS COLD-INIT KD (random-init student trained only via KD) —
    the only arm where any alignment the student ends with was transmitted
    through the KD channel, not inherited from pretraining. Warm-init KD is a
    fine-tuning-drift control; plain LM-finetune is a corpus-drift control.
  * >=3 seeds on every trained arm (single-run leaves a 50% drop at p~0.10).
  * Floor-anchored retention rho' = (A_student - A_floor)/(A_teacher - A_floor),
    bootstrap CIs, decide on Delta — never a raw point ratio.
  * Perplexity reported per student (under-training confound guard).
  * Fixed static-embedding nuisance (frozen teacher) across ALL arms, so the
    variance partition isolates the contextual block fairly arm-to-arm.
  * Verdict at a FIXED layer for the 12L gpt2-arch arms (L7, E002's gpt2 peak) —
    no winner's-curse layer selection for the comparison that decides anything.
  * distilgpt2 scored vs its real teacher gpt2 (context, not verdict).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P  # noqa: E402
from data_adapters import load_tuckute  # noqa: E402
from distill import distill  # noqa: E402
from pilot_lib import DistillConfig  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "data/kd_corpus"
CORPUS_TRAIN = CORPUS_DIR / "wikitext103_sentences_train.txt"
CORPUS_HELDOUT = CORPUS_DIR / "wikitext103_sentences_heldout.txt"


# --------------------------------------------------------------------------- #
# KD corpus: broad English sentences, disjoint from Tuckute
# --------------------------------------------------------------------------- #
def prepare_corpus(n_train: int, n_heldout: int, tuckute_dir: str) -> None:
    """Download wikitext-103-raw-v1, split into sentences, dedup vs Tuckute,
    write a fixed train slice + a held-out slice for perplexity. Idempotent."""
    import re

    if CORPUS_TRAIN.exists() and CORPUS_HELDOUT.exists():
        print(f"corpus already prepared: {CORPUS_TRAIN}")
        return
    from datasets import load_dataset

    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    print("loading wikitext-103-raw-v1 (train) ...", flush=True)
    # The legacy `wikitext` repo id fails to parse in datasets>=5 (needs a
    # namespace); Salesforce/wikitext is the maintained parquet mirror.
    ds = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="train")

    # Tuckute sentences to exclude (no stimulus-distribution leakage).
    tuck_texts, _, _ = load_tuckute(tuckute_dir)
    banned = {t.strip().lower() for t in tuck_texts}

    splitter = re.compile(r"(?<=[.!?])\s+")
    seen: set[str] = set()
    sents: list[str] = []
    target = n_train + n_heldout
    for row in ds:
        line = row["text"].strip()
        if not line or line.startswith("="):  # skip wikitext headers
            continue
        for s in splitter.split(line):
            s = s.strip()
            w = s.split()
            if not (4 <= len(w) <= 45):
                continue
            key = s.lower()
            if key in banned or key in seen:
                continue
            seen.add(key)
            sents.append(s)
        if len(sents) >= target:
            break

    train = sents[:n_train]
    heldout = sents[n_train:n_train + n_heldout]
    CORPUS_TRAIN.write_text("\n".join(train))
    CORPUS_HELDOUT.write_text("\n".join(heldout))
    print(f"wrote {len(train)} train + {len(heldout)} heldout sentences to {CORPUS_DIR}")


def load_corpus() -> tuple[list[str], list[str]]:
    if not CORPUS_TRAIN.exists():
        raise FileNotFoundError(
            f"{CORPUS_TRAIN} missing — run `--prepare-corpus` first (needs network).")
    train = [ln for ln in CORPUS_TRAIN.read_text().splitlines() if ln.strip()]
    heldout = [ln for ln in CORPUS_HELDOUT.read_text().splitlines() if ln.strip()]
    return train, heldout


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #
def load_pretrained(name: str, device: str):
    from transformers import AutoModelForCausalLM
    return AutoModelForCausalLM.from_pretrained(name).to(device).eval()


def make_random_gpt2(device: str, seed: int):
    """Random-init gpt2 (the cold student / untrained floor). Feghhi control path."""
    from transformers import AutoConfig, AutoModelForCausalLM
    cfg = AutoConfig.from_pretrained("gpt2")
    P.set_seed(seed)
    return AutoModelForCausalLM.from_config(cfg).to(device).eval()


def verdict_layer(model) -> int:
    """The fixed report layer: 12L->7 (E002 gpt2 peak), 24L->14, 6L->3."""
    n = model.config.num_hidden_layers
    return {12: 7, 24: 14, 6: 3}.get(n, max(1, int(round(0.58 * n))))


def layers_to_probe(model) -> list[int]:
    n = model.config.num_hidden_layers
    base = sorted({max(1, int(round(f * n))) for f in (0.25, 0.5, 0.6, 0.75)})
    vl = verdict_layer(model)
    return sorted(set(base) | {vl})


# --------------------------------------------------------------------------- #
# Training
# --------------------------------------------------------------------------- #
def lm_finetune(student, tokenizer, texts, cfg: DistillConfig, device: str, seed: int):
    """Plain causal-LM fine-tune (no teacher) — the corpus-drift control arm."""
    import torch

    student.train()
    opt = torch.optim.AdamW(student.parameters(), lr=cfg.lr)
    n = len(texts)
    last = 0.0
    for epoch in range(cfg.epochs):
        rng = np.random.default_rng(seed * 1000 + epoch)
        order = rng.permutation(np.arange(n))
        for start in range(0, n, cfg.batch_size):
            bidx = order[start:start + cfg.batch_size]
            batch = [texts[i] for i in bidx]
            enc = tokenizer(batch, return_tensors="pt", padding=True,
                            truncation=True, max_length=cfg.max_length).to(device)
            labels = enc["input_ids"].clone()
            labels[enc["attention_mask"] == 0] = -100
            out = student(**enc, labels=labels)
            opt.zero_grad()
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(student.parameters(), 1.0)
            opt.step()
            last = float(out.loss.item())
    student.eval()
    return {"final_lm_loss": last}


def eval_perplexity(model, tokenizer, texts, device, max_length=64, batch_size=32) -> float:
    """Held-out token-level perplexity (convergence guard, review Objection 5)."""
    import torch

    model.eval()
    total_nll, total_tok = 0.0, 0
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            enc = tokenizer(batch, return_tensors="pt", padding=True,
                            truncation=True, max_length=max_length).to(device)
            logits = model(**enc).logits
            # shift for next-token prediction
            sl = logits[:, :-1, :]
            st = enc["input_ids"][:, 1:]
            mask = enc["attention_mask"][:, 1:].bool()
            logp = torch.log_softmax(sl, dim=-1)
            tok_logp = logp.gather(-1, st.unsqueeze(-1)).squeeze(-1)
            total_nll += float((-tok_logp[mask]).sum().item())
            total_tok += int(mask.sum().item())
    return float(np.exp(total_nll / max(total_tok, 1)))


# --------------------------------------------------------------------------- #
# Scoring (the anti-confound encoding partition, reused from pilot_lib)
# --------------------------------------------------------------------------- #
def score_model(model, tok, texts, Y, Z, S_fixed, device, n_pca_sweep=50,
                n_pca_robust=(25, 50, 100)):
    """Per-layer unique R^2 (capacity-fair partition vs fixed static nuisance).
    Returns (per_layer_records, verdict_record_with_pca_robustness)."""
    ext = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
    vl = verdict_layer(model)
    recs = []
    verdict = None
    for layer in layers_to_probe(model):
        X = P.extract_hidden_states(model, tok, texts, ext, device, layer=layer)
        part = P.variance_partition(X, Z, S_fixed, Y, k_folds=5, n_pca=n_pca_sweep)
        rec = {"layer": layer, "unique_r2": part["unique_r2"],
               "unique_r2_std": part["unique_r2_std"],
               "unique_r2_per_fold": part["unique_r2_per_fold"],
               "r2_nuisance": part["r2_nuisance"], "r2_full": part["r2_full"]}
        if layer == vl:
            rec["pca_robustness"] = {}
            for npca in n_pca_robust:
                p = P.variance_partition(X, Z, S_fixed, Y, k_folds=5, n_pca=npca)
                rec["pca_robustness"][str(npca)] = {
                    "unique_r2": p["unique_r2"], "unique_r2_std": p["unique_r2_std"]}
            verdict = rec
        recs.append(rec)
    return recs, vl, verdict


# --------------------------------------------------------------------------- #
# Stats: floor-anchored retention + bootstrap CIs
# --------------------------------------------------------------------------- #
def _folds_for(records: list[dict]) -> np.ndarray:
    """Pool per-fold unique-R^2 across (seed, ) records at the verdict layer."""
    vals = []
    for r in records:
        vals.extend(r["verdict"]["unique_r2_per_fold"])
    return np.array(vals, dtype=np.float64)


def bootstrap_ci(samples: np.ndarray, n_boot=10000, seed=0) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    if len(samples) == 0:
        return (float("nan"),) * 3
    boots = rng.choice(samples, size=(n_boot, len(samples)), replace=True).mean(axis=1)
    return float(samples.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def retention_stats(student_folds, teacher_folds, floor_folds, n_boot=10000, seed=0):
    """rho' = (A_s - A_0)/(A_T - A_0) with bootstrap CI; Delta = A_T - A_s with p."""
    rng = np.random.default_rng(seed)
    a_s, a_t, a_0 = student_folds.mean(), teacher_folds.mean(), floor_folds.mean()
    denom = a_t - a_0
    rho = (a_s - a_0) / denom if abs(denom) > 1e-9 else float("nan")
    delta = a_t - a_s
    bs_rho, bs_delta = [], []
    for _ in range(n_boot):
        s = rng.choice(student_folds, len(student_folds), replace=True).mean()
        t = rng.choice(teacher_folds, len(teacher_folds), replace=True).mean()
        f = rng.choice(floor_folds, len(floor_folds), replace=True).mean()
        d = t - f
        bs_rho.append((s - f) / d if abs(d) > 1e-9 else np.nan)
        bs_delta.append(t - s)
    bs_rho = np.array(bs_rho); bs_delta = np.array(bs_delta)
    return {
        "A_student": float(a_s), "A_teacher": float(a_t), "A_floor": float(a_0),
        "rho_prime": float(rho),
        "rho_prime_ci": [float(np.nanpercentile(bs_rho, 2.5)), float(np.nanpercentile(bs_rho, 97.5))],
        "delta": float(delta),
        "delta_ci": [float(np.percentile(bs_delta, 2.5)), float(np.percentile(bs_delta, 97.5))],
        "p_delta_le_0": float((bs_delta <= 0).mean()),  # P(no drop) under bootstrap
    }


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-corpus", action="store_true")
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--n-train", type=int, default=96000)
    ap.add_argument("--n-heldout", type=int, default=2000)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=5e-5, help="fine-tune LR (warm arms)")
    ap.add_argument("--cold-lr", type=float, default=3e-4, help="from-scratch LR (kd_cold)")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--arms", nargs="+", default=["kd_cold", "kd_warm", "lmft_warm"])
    ap.add_argument("--limit-train", type=int, default=None,
                    help="Cap KD train sentences (smoke test only).")
    ap.add_argument("--out", default="outputs/E003_kd_alignment.json")
    args = ap.parse_args()

    if args.prepare_corpus:
        prepare_corpus(args.n_train, args.n_heldout, args.data_dir)
        return

    import torch
    from transformers import AutoTokenizer

    device = P.pick_device()
    tok = AutoTokenizer.from_pretrained("gpt2")
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    texts, Y, meta = load_tuckute(args.data_dir)
    nc = meta["noise_ceiling_langnetw"]
    print(f"Tuckute: {meta['n_items']} sentences x {meta['n_voxels']} ROI; nc={nc}; device={device}")
    corpus_train, corpus_heldout = load_corpus()
    if args.limit_train:
        corpus_train = corpus_train[:args.limit_train]
    print(f"KD corpus: {len(corpus_train)} train + {len(corpus_heldout)} heldout sentences")

    # Fixed nuisance design (identical across ALL arms) — isolates the contextual block.
    Z = P.scalar_nuisance(texts, tok)
    teacher = load_pretrained("gpt2-medium", device)
    S_fixed = P.static_embedding_features(teacher, tok, texts, device)

    dcfg = DistillConfig(epochs=args.epochs, lr=args.lr, batch_size=args.batch_size,
                         max_length=64, kd_temperature=2.0, lambda_kd=1.0,
                         lambda_hidden=0.0, lambda_brain=0.0)

    results = {"meta": meta, "config": vars(args), "nc": nc,
               "dcfg": asdict(dcfg), "models": {}}

    def record(tag, model, seed=None, ppl=None):
        recs, vl, verdict = score_model(model, tok, texts, Y, Z, S_fixed, device)
        entry = {"tag": tag, "seed": seed, "verdict_layer": vl, "perplexity": ppl,
                 "verdict": verdict, "sweep": recs,
                 "nc_normalised_unique_r2": verdict["unique_r2"] / nc if nc else None}
        results["models"].setdefault(tag, []).append(entry)
        vn = verdict["unique_r2"]
        print(f"  [{tag}{'' if seed is None else f' s{seed}'}] L{vl} unique_r2={vn:+.4f} "
              f"(NC {vn/nc:+.3f}){'' if ppl is None else f'  ppl={ppl:.1f}'}", flush=True)
        return entry

    t0 = time.time()
    # --- Reference points (free) ------------------------------------------
    print("== references ==")
    record("teacher", teacher)                          # gpt2-medium (DPI ceiling)
    g2 = load_pretrained("gpt2", device); record("gpt2", g2); del g2; torch.cuda.empty_cache()
    dg = load_pretrained("distilgpt2", device); record("distilgpt2", dg); del dg; torch.cuda.empty_cache()

    # --- Floor: untrained gpt2 over seeds ---------------------------------
    print("== floor (untrained gpt2) ==")
    for s in args.seeds:
        m = make_random_gpt2(device, s); record("untrained", m, seed=s); del m; torch.cuda.empty_cache()

    # --- Trained arms over seeds ------------------------------------------
    for s in args.seeds:
        for arm in args.arms:
            print(f"== train {arm} seed={s} ==")
            P.set_seed(s)
            if arm == "kd_cold":
                student = make_random_gpt2(device, s)
            else:
                student = load_pretrained("gpt2", device)
            student.train()
            # Arm-appropriate LR: cold must learn from scratch (a fine-tune LR
            # would leave it ~random — a trivial confound), warm fine-tunes.
            # Matched across arms: data, step count, architecture.
            arm_lr = args.cold_lr if arm == "kd_cold" else args.lr
            arm_cfg = DistillConfig(**{**asdict(dcfg), "lr": arm_lr})
            if arm == "lmft_warm":
                lm_finetune(student, tok, corpus_train, arm_cfg, device, seed=s)
            else:  # kd_cold, kd_warm — pure logit KD (lambda_brain=0)
                distill(teacher, student, tok, corpus_train, arm_cfg, device,
                        fmri_train=None, seed=s, arm=arm)
            student.eval()
            ppl = eval_perplexity(student, tok, corpus_heldout, device)
            record(arm, student, seed=s, ppl=ppl)
            del student; torch.cuda.empty_cache()

    # --- Aggregate + retention stats --------------------------------------
    teacher_folds = _folds_for(results["models"]["teacher"])
    floor_folds = _folds_for(results["models"]["untrained"])
    gpt2_folds = _folds_for(results["models"]["gpt2"])
    summary = {"teacher_unique_r2": float(teacher_folds.mean()),
               "floor_unique_r2": float(floor_folds.mean()),
               "gpt2_unique_r2": float(gpt2_folds.mean()),
               "nc": nc, "arms": {}}
    for tag in ["kd_cold", "kd_warm", "lmft_warm", "distilgpt2", "gpt2"]:
        if tag not in results["models"]:
            continue
        sf = _folds_for(results["models"][tag])
        ref = teacher_folds if tag != "distilgpt2" else gpt2_folds  # distilgpt2 vs its real teacher
        st = retention_stats(sf, ref, floor_folds)
        st["ref_teacher"] = "gpt2" if tag == "distilgpt2" else "gpt2-medium"
        st["nc_normalised"] = float(sf.mean() / nc) if nc else None
        mean, lo, hi = bootstrap_ci(sf)
        st["unique_r2_ci"] = [lo, hi]
        if tag in results["models"] and results["models"][tag][0]["perplexity"] is not None:
            st["mean_perplexity"] = float(np.mean([e["perplexity"] for e in results["models"][tag]
                                                   if e["perplexity"] is not None]))
        summary["arms"][tag] = st
    results["summary"] = summary

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(results, indent=2))
    print(f"\n=== SUMMARY (elapsed {time.time()-t0:.0f}s) ===")
    print(f"teacher A_T={summary['teacher_unique_r2']:+.4f}  floor A_0={summary['floor_unique_r2']:+.4f}  "
          f"gpt2={summary['gpt2_unique_r2']:+.4f}  (NC={nc})")
    for tag, st in summary["arms"].items():
        ppl_str = f"  ppl={st['mean_perplexity']:.1f}" if "mean_perplexity" in st else ""
        rci = st["rho_prime_ci"]
        print(f"  {tag:10s} A_s={st['A_student']:+.4f} (NC {st['nc_normalised']:+.3f})  "
              f"rho'={st['rho_prime']:+.2f} CI[{rci[0]:+.2f},{rci[1]:+.2f}]  "
              f"Delta={st['delta']:+.4f} p(no-drop)={st['p_delta_le_0']:.3f}{ppl_str}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
