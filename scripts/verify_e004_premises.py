#!/usr/bin/env python3
"""Reproduce the design premises behind E004 (committed so they are auditable):
  (1) the A/B contiguous-split covariate shift (imageability/surprisal/BOLD mean),
  (2) the imageability<->BOLD correlation (the unsubtracted confound),
  (3) signal-retention under expanded nuisance (imageability+surprisal),
  (4) the matched functional NC (lang_LH_* sub-ROIs) vs the anatomical 0.353,
  (5) the lever-test power simulation (MDE per substrate).
Writes outputs/E004_premises.json and prints a summary. Idempotent; needs GPU+models for (3)/(5).
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P
from data_adapters import load_tuckute, TUCKUTE_SUBROIS

DATA = "data/tuckute2024"


def main():
    texts, Y, meta = load_tuckute(DATA)
    n = len(texts); Ymean = Y.mean(1)
    csv = sorted(Path(DATA).rglob("brain-lang-data_participant_*.csv"))[0]
    df = pd.read_csv(csv)
    items = sorted(df[df["cond"] == "B"]["item_id"].unique())
    im = df.drop_duplicates("item_id").set_index("item_id")
    cols = ["rating_imageability_mean", "log-prob-gpt2-xl_mean", "log-prob-pcfg_mean"]
    C = np.stack([im.loc[items, c].to_numpy(float) for c in cols], 1)
    out = {"n_items": n}

    # (1) naive A/B split shift
    a = slice(0, 700); b = slice(700, n)
    shift = {}
    for j, c in enumerate(cols + ["BOLD_mean"]):
        v = C[:, j] if j < len(cols) else Ymean
        t, p = stats.ttest_ind(v[a], v[b], equal_var=False)
        shift[c] = {"A": float(v[a].mean()), "B": float(v[b].mean()), "t": float(t), "p": float(p)}
    out["naive_split_shift"] = shift

    # (2) imageability <-> BOLD
    r, p = stats.pearsonr(C[:, 0], Ymean)
    out["imageability_vs_bold"] = {"r": float(r), "p": float(p)}

    # (4) NC values
    ncf = sorted(Path(DATA).rglob("NC-allroi-data.csv"))[0]
    ncdf = pd.read_csv(ncf)
    subnc = {r_: float(ncdf.loc[ncdf["roi"] == r_, "nc"].iloc[0]) for r_ in TUCKUTE_SUBROIS}
    out["nc"] = {"sub_rois": subnc, "mean_sub_roi": float(np.mean(list(subnc.values()))),
                 "lang_LH_netw": float(ncdf.loc[ncdf["roi"] == "lang_LH_netw", "nc"].iloc[0]),
                 "anatglasser_LHRH_LangNetw_legacy": float(ncdf.loc[ncdf["roi"] == "anatglasser_LHRH_LangNetw", "nc"].iloc[0])}

    # (3)+(5) need models
    try:
        import torch  # noqa
        from transformers import AutoModelForCausalLM, AutoTokenizer
        device = P.pick_device()

        def feats(name, layer):
            tok = AutoTokenizer.from_pretrained(name); tok.pad_token = tok.pad_token or tok.eos_token
            m = AutoModelForCausalLM.from_pretrained(name).to(device).eval()
            ec = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
            Z = P.scalar_nuisance(texts, tok); S = P.static_embedding_features(m, tok, texts, device)
            X = P.extract_hidden_states(m, tok, texts, ec, device, layer=layer)
            del m; torch.cuda.empty_cache()
            return X, Z, S

        nuis_ret, power = {}, {}
        rng = np.random.default_rng(0)
        for name, layer in [("gpt2", 7), ("Qwen/Qwen2.5-0.5B", 12)]:
            X, Z, S = feats(name, layer)
            base = P.variance_partition(X, Z, S, Y, k_folds=5, n_pca=50)
            exp = P.variance_partition(X, np.concatenate([Z, C], 1), S, Y, k_folds=5, n_pca=50)
            nuis_ret[name] = {"std_nuisance_unique_r2": base["unique_r2"], "std_std": base["unique_r2_std"],
                              "expanded_unique_r2": exp["unique_r2"], "expanded_std": exp["unique_r2_std"],
                              "retained_frac": exp["unique_r2"] / base["unique_r2"]}
            # power sim on rotating folds
            bnd = np.linspace(0, n, 6).astype(int)
            folds = [np.arange(bnd[i], bnd[i + 1]) for i in range(5)]
            bpf = np.array([P.variance_partition(X[f], Z[f], S[f], Y[f], k_folds=5, n_pca=50)["unique_r2"] for f in folds])
            sd = bpf.std(ddof=1)
            pw = {}
            for td in [0.003, 0.006, 0.010, 0.015]:
                hits = 0; B = 2000
                for _ in range(B):
                    sd_arr = td + rng.normal(0, sd, size=(3, 5))
                    alld = sd_arr.flatten()
                    lo = np.percentile(rng.choice(alld, size=(400, len(alld)), replace=True).mean(1), 2.5)
                    hits += (lo > 0)
                pw[f"{td:.3f}"] = hits / B
            power[name] = {"base_per_fold": float(bpf.mean()), "per_fold_sd": float(sd), "power": pw}
        out["nuisance_retention"] = nuis_ret
        out["power_sim"] = power
    except Exception as e:
        out["models_skipped"] = str(e)

    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/E004_premises.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print("\nwrote outputs/E004_premises.json")


if __name__ == "__main__":
    main()
