#!/usr/bin/env python3
"""E014 — the averaging confound on the ENCODING BRAIN-SCORE (the measurement, not just our
distillation pipeline). The main-track lift: show that the field's standard practice of
scoring an LM against a CROSS-SUBJECT-AVERAGED fMRI target (Tuckute 2024's published target;
group-average RSA) INFLATES the apparent brain-score relative to per-individual scoring.

Pure encoding (ridge variance-partition, no LM training): extract LM features ONCE for the
1000 Tuckute sentences, then compute unique R^2 (LM beyond nuisance) against:
  * each individual subject's ROI target  (per-subject brain-score)
  * the k-averaged target for k=1..10      (the averaging dose-response, on the MEASUREMENT)
  * the standard 5-UID-averaged target     (Tuckute's published-style target)
and show the averaged-target score > mean per-subject score, tracking the noise-ceiling
prediction NC_k = NC/(NC+(1-NC)/k). This is the measurement analogue of E005-vs-E008 and is
about the published benchmark metric, not our optimization — a strictly broader claim.

Run: export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
  CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_averaging_encoding.py --model Qwen/Qwen2.5-0.5B
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P
from data_adapters import load_tuckute, TUCKUTE_SUBROIS

ALL_UIDS = (797, 837, 841, 848, 853, 856, 865, 875, 876, 880)
VERDICT_LAYER = {12: 7, 24: 12, 28: 14}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--k-values", nargs="+", type=int, default=[1, 2, 3, 5, 9])
    ap.add_argument("--n-subsets", type=int, default=5, help="random size-k subsets per k (decouple count from identity)")
    ap.add_argument("--out", default="outputs/E014_averaging_encoding.json")
    args = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
    device = P.pick_device()
    nlayers = AutoConfig.from_pretrained(args.model).num_hidden_layers
    layer = VERDICT_LAYER.get(nlayers, max(1, nlayers // 2))

    # usable UIDs (853 incomplete ROI) — load per-uid targets; texts identical across uids
    usable = [u for u in ALL_UIDS if u != 853]
    per_uid = {}
    texts = None
    for u in usable:
        t_u, Y_u, _ = load_tuckute(args.data_dir, uids=(u,))
        if texts is None:
            texts = t_u
        per_uid[u] = Y_u
    nc = _matched_nc(args.data_dir)
    n = len(texts)
    print(f"{args.model} L{layer}; {n} sentences; {len(usable)} subjects; matched NC={nc:.3f}")

    # extract LM features + nuisance ONCE
    tok = AutoTokenizer.from_pretrained(args.model)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model).to(device).eval()
    ecfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
    X = P.extract_hidden_states(model, tok, texts, ecfg, device, layer=layer)
    Z = P.scalar_nuisance(texts, tok)
    S = P.static_embedding_features(model, tok, texts, device)
    del model
    import torch
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    def uR2(Y):
        return float(P.variance_partition(X, Z, S, Y, k_folds=5, n_pca=50)["unique_r2"])

    t0 = time.time()
    # per-subject brain-scores
    per_subj = {u: uR2(per_uid[u]) for u in usable}
    mean_persubj = float(np.mean(list(per_subj.values())))
    print(f"per-subject unique R^2: mean={mean_persubj:+.4f}  range [{min(per_subj.values()):+.4f},{max(per_subj.values()):+.4f}]")

    # averaging dose-response on the MEASUREMENT: random size-k subsets
    rng = np.random.default_rng(20260612)
    import math
    dose = {}
    for k in args.k_values:
        n_poss = math.comb(len(usable), k)
        want = min(args.n_subsets, n_poss)
        seen, scores = set(), []
        while len(scores) < want:
            s = tuple(sorted(rng.choice(usable, size=k, replace=False).tolist()))
            if s in seen:
                continue
            seen.add(s)
            Yk = np.mean([per_uid[u] for u in s], axis=0)
            scores.append(uR2(Yk))
        nc_k = nc / (nc + (1 - nc) / k)
        dose[k] = {"mean": float(np.mean(scores)), "scores": scores, "nc_k_pred": nc_k,
                   "inflation_vs_k1": float(np.mean(scores) / (dose[1]["mean"] if 1 in dose else np.mean(scores)))}
        print(f"  k={k}: avg-target unique R^2 = {np.mean(scores):+.4f}  (NC_k pred {nc_k:.3f}; {len(scores)} subsets)")

    # the standard Tuckute 5-UID-averaged target (the published-style score)
    std_avg = uR2(load_tuckute(args.data_dir)[1])
    print(f"\nStandard 5-UID-averaged (Tuckute published-style) unique R^2 = {std_avg:+.4f}")
    print(f"vs mean per-subject = {mean_persubj:+.4f}  -> INFLATION factor {std_avg/mean_persubj:.2f}x")

    results = {"model": args.model, "layer": layer, "nc": nc, "n_sentences": n, "subjects": usable,
               "per_subject_uR2": per_subj, "mean_per_subject_uR2": mean_persubj,
               "dose_response": dose, "standard_5uid_avg_uR2": std_avg,
               "inflation_factor": std_avg / mean_persubj if mean_persubj else None,
               "elapsed_s": time.time() - t0}
    Path(args.out).write_text(json.dumps(results, indent=2))
    print(f"\n=== E014: averaging inflates the ENCODING brain-score ===")
    print(f"  per-subject mean {mean_persubj:+.4f} → k-averaged grows with k → 5-UID-avg {std_avg:+.4f} ({std_avg/mean_persubj:.1f}x)")
    print(f"  wrote {args.out} ({results['elapsed_s']:.0f}s)")


def _matched_nc(data_dir):
    import pandas as pd
    ncf = sorted(Path(data_dir).rglob("NC-allroi-data.csv"))[0]
    ncd = pd.read_csv(ncf)
    return float(np.mean([float(ncd.loc[ncd["roi"] == r, "nc"].iloc[0]) for r in TUCKUTE_SUBROIS]))


if __name__ == "__main__":
    main()
