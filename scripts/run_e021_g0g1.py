#!/usr/bin/env python
"""E021 gating G0 + G1 — surprisal-orthogonal RT variance on Natural Stories (SPR).

G0: unique R^2 of base-LM surprisal (+spillover) in by-word reading time, over
    nuisances (word length, log-freq, sentence position, spillover length/freq),
    by-item CV ridge. And the residual fraction of total RT variance.
G1: split-half reliability of the surprisal-residualized by-word residual
    (the decision number), against the by-word RT noise ceiling.

No model training. Surprisal from GPT-2-small (primary) and Qwen2.5-0.5B (report).
Outputs JSON + a per-word table CSV.

Usage:
  HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_g0g1.py
"""
import json
import math
import re
from collections import defaultdict

import numpy as np
import pandas as pd
import torch
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from transformers import AutoModelForCausalLM, AutoTokenizer

NS = "/home/centcom/data/brain-alignment/data/paper-repos/naturalstories"
RTS = f"{NS}/naturalstories_RTS"
OUT_DIR = "/home/centcom/data/brain-alignment/outputs/e021_g0g1"
SEED = 0
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

np.random.seed(SEED)
torch.manual_seed(SEED)


# ---------------------------------------------------------------------------
# 1. Build canonical per-word table (item, zone, word) in story order.
# ---------------------------------------------------------------------------
def load_words():
    tok = pd.read_csv(f"{RTS}/all_stories.tok", sep="\t")
    tok = tok.sort_values(["item", "zone"]).reset_index(drop=True)
    return tok  # columns: word, zone, item


# ---------------------------------------------------------------------------
# 2. Per-subject RTs -> per-word mean + per-subject matrix (for split-half).
# ---------------------------------------------------------------------------
def load_rts():
    cols = ["WorkerId", "item", "zone", "RT"]
    df = pd.read_csv(f"{RTS}/processed_RTs.tsv", sep="\t", usecols=cols)
    return df


# ---------------------------------------------------------------------------
# 3. GPT-2 / Qwen per-word surprisal aligned to the running story text.
#    For each story, concatenate the words (the .tok wordforms), tokenize the
#    full text, and assign each subword's NLL to the word whose character span
#    contains it. Surprisal of a word = sum of subword NLLs (nats).
# ---------------------------------------------------------------------------
def word_surprisals(words_df, model_name):
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.float32
    ).to(DEVICE)
    model.eval()

    has_bos = tok.bos_token_id is not None
    out = {}  # (item, zone) -> surprisal nats

    for item, g in words_df.groupby("item"):
        g = g.sort_values("zone")
        wordforms = [str(w) for w in g["word"].tolist()]
        zones = g["zone"].tolist()

        # Build running text with a single leading space before each word
        # (GPT-2/Qwen BPE encode leading-space-prefixed words). Record the
        # char span of each word's *content* (the space belongs to the word).
        text = ""
        spans = []  # (start, end) char offsets in `text` for each word
        for w in wordforms:
            start = len(text)
            text += " " + w  # leading space
            end = len(text)
            spans.append((start, end))

        enc = tok(text, return_offsets_mapping=True, add_special_tokens=False)
        all_ids = enc["input_ids"]
        offsets = enc["offset_mapping"]  # per-token (cstart, cend)

        # Score with a sliding window respecting the model context limit, so a
        # story longer than the context still gets full-context surprisal for
        # every token (each token scored with as much left context as fits).
        max_ctx = min(getattr(model.config, "n_positions", 1024) or 1024, 1024)
        stride = max_ctx // 2
        nll = [float("nan")] * len(all_ids)
        bos_id = tok.bos_token_id if has_bos else None
        start = 0
        while start < len(all_ids):
            end = min(start + max_ctx - (1 if has_bos else 0), len(all_ids))
            chunk = all_ids[start:end]
            if has_bos:
                ids = torch.tensor([[bos_id] + chunk], device=DEVICE)
                n_pre = 1
            else:
                ids = torch.tensor([chunk], device=DEVICE)
                n_pre = 0
            with torch.no_grad():
                logits = model(ids).logits
            logp = torch.log_softmax(logits.float(), dim=-1)
            # Only commit scores for tokens not already scored (avoid double
            # counting in the overlap); first chunk's first token has no
            # context if no BOS -> stays nan.
            for j in range(len(chunk)):
                gidx = start + j
                if not math.isnan(nll[gidx]):
                    continue
                pos_in_ids = j + n_pre
                if pos_in_ids == 0:
                    continue
                tgt = chunk[j]
                nll[gidx] = -logp[0, pos_in_ids - 1, tgt].item()
            if end == len(all_ids):
                break
            start += stride

        # Assign each subword token to the word whose span covers its cstart.
        # offsets are into `text`; word w covers chars (start, end) including
        # the leading space. A token's center belongs to word i if its
        # cstart in [spans[i].start, spans[i].end).
        word_nll = [0.0] * len(spans)
        word_has = [False] * len(spans)
        # build a sorted list of span starts for bisect-free linear scan
        for k, (cs, ce) in enumerate(offsets):
            if cs == ce:  # special / empty token
                continue
            if math.isnan(nll[k]):
                continue
            # find word whose span contains cs
            for i, (ws, we) in enumerate(spans):
                if ws <= cs < we:
                    word_nll[i] += nll[k]
                    word_has[i] = True
                    break

        for i, z in enumerate(zones):
            out[(item, z)] = word_nll[i] if word_has[i] else float("nan")

    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return out


# ---------------------------------------------------------------------------
# 4. Unigram log-frequency from the corpus freqs file (Google ngram counts).
#    freqs-1.tsv col format: code, item, word, count, NA
# ---------------------------------------------------------------------------
def load_logfreq(words_df):
    # Use freqs-1.tsv: rows like "1.1.word\t1\tIf\t123141271\tNA"
    rows = []
    with open(f"{NS}/freqs/freqs-1.tsv") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            code, item, word, count = parts[0], parts[1], parts[2], parts[3]
            if not code.endswith(".word"):
                continue
            # code = item.zone.word
            seg = code.split(".")
            try:
                it = int(seg[0]); zn = int(seg[1])
                c = float(count)
            except ValueError:
                continue
            rows.append((it, zn, c))
    fdf = pd.DataFrame(rows, columns=["item", "zone", "count"])
    fdf = fdf.drop_duplicates(["item", "zone"])
    return fdf


# ---------------------------------------------------------------------------
# Sentence-position feature: reset position counter at sentence-final punct.
# ---------------------------------------------------------------------------
def sentence_positions(words_df):
    recs = []
    for item, g in words_df.groupby("item"):
        g = g.sort_values("zone")
        p = 1
        for _, row in g.iterrows():
            recs.append((item, row["zone"], p))
            w = str(row["word"])
            if re.search(r"[.!?]", w):
                p = 1
            else:
                p += 1
    return pd.DataFrame(recs, columns=["item", "zone", "sentpos"])


# ---------------------------------------------------------------------------
# Cross-validated ridge: by-item folds. Returns per-fold R^2.
# ---------------------------------------------------------------------------
def cv_ridge_r2(X, y, items, alpha=1.0):
    uniq = sorted(set(items))
    r2s = []
    for held in uniq:
        tr = items != held
        te = items == held
        if te.sum() < 5 or tr.sum() < 50:
            continue
        sc = StandardScaler().fit(X[tr])
        Xtr, Xte = sc.transform(X[tr]), sc.transform(X[te])
        ymu = y[tr].mean()
        m = Ridge(alpha=alpha).fit(Xtr, y[tr] - ymu)
        pred = m.predict(Xte) + ymu
        ss_res = np.sum((y[te] - pred) ** 2)
        ss_tot = np.sum((y[te] - y[tr].mean()) ** 2)
        r2s.append(1 - ss_res / ss_tot)
    return np.array(r2s), uniq


def cv_ridge_resid(X, y, items, alpha=1.0):
    """Return held-out predictions for every row (out-of-fold), for residuals."""
    uniq = sorted(set(items))
    pred_all = np.full(len(y), np.nan)
    for held in uniq:
        tr = items != held
        te = items == held
        sc = StandardScaler().fit(X[tr])
        Xtr, Xte = sc.transform(X[tr]), sc.transform(X[te])
        ymu = y[tr].mean()
        m = Ridge(alpha=alpha).fit(Xtr, y[tr] - ymu)
        pred_all[te] = m.predict(Xte) + ymu
    return pred_all


def spearman_brown(r):
    if r <= -1:
        return float("nan")
    return 2 * r / (1 + r)


def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)

    words = load_words()
    rts = load_rts()
    logfreq = load_logfreq(words)
    sentpos = sentence_positions(words)

    # Per-word mean RT across subjects (only words that have RTs).
    byword = rts.groupby(["item", "zone"]).agg(
        meanRT=("RT", "mean"), nsubj=("WorkerId", "nunique")
    ).reset_index()

    # Merge into the canonical word table.
    tab = words.merge(byword, on=["item", "zone"], how="inner")
    tab = tab.merge(logfreq, on=["item", "zone"], how="left")
    tab = tab.merge(sentpos, on=["item", "zone"], how="left")
    tab = tab.sort_values(["item", "zone"]).reset_index(drop=True)

    # Word length (chars, stripped).
    tab["wlen"] = tab["word"].astype(str).str.replace(r"[^\w]", "", regex=True).str.len()
    tab["logfreq"] = np.log(tab["count"].fillna(tab["count"].median()) + 1)

    # Spillover nuisances (previous word within same item).
    tab["prev_wlen"] = tab.groupby("item")["wlen"].shift(1)
    tab["prev_logfreq"] = tab.groupby("item")["logfreq"].shift(1)

    results = {"corpus": "natural_stories_SPR", "n_words_with_rt": int(len(tab)),
               "n_subjects": int(rts["WorkerId"].nunique()), "n_stories": int(tab["item"].nunique()),
               "seed": SEED, "models": {}}

    for model_name, key in [("gpt2", "gpt2"), ("Qwen/Qwen2.5-0.5B", "qwen2.5-0.5b")]:
        print(f"\n==== {model_name} ====", flush=True)
        surp = word_surprisals(words, model_name)
        tab[f"surp_{key}"] = [surp.get((it, zn), float("nan"))
                              for it, zn in zip(tab["item"], tab["zone"])]
        tab[f"prev_surp_{key}"] = tab.groupby("item")[f"surp_{key}"].shift(1)

        # Working frame: drop rows missing any needed feature.
        need = ["meanRT", "wlen", "logfreq", "sentpos", "prev_wlen", "prev_logfreq",
                f"surp_{key}", f"prev_surp_{key}"]
        w = tab.dropna(subset=need).copy()
        items = w["item"].values
        y = w["meanRT"].values.astype(float)

        nuis_cols = ["wlen", "logfreq", "sentpos", "prev_wlen", "prev_logfreq"]
        full_cols = nuis_cols + [f"surp_{key}", f"prev_surp_{key}"]
        Xn = w[nuis_cols].values.astype(float)
        Xf = w[full_cols].values.astype(float)

        r2_n, _ = cv_ridge_r2(Xn, y, items)
        r2_f, _ = cv_ridge_r2(Xf, y, items)
        unique = r2_f - r2_n  # paired per fold
        # CI over folds (t-based 95%)
        def ci(a):
            a = np.asarray(a)
            m = a.mean(); s = a.std(ddof=1); n = len(a)
            half = 1.96 * s / math.sqrt(n)
            return m, half
        r2n_m, r2n_h = ci(r2_n)
        r2f_m, r2f_h = ci(r2_f)
        uq_m, uq_h = ci(unique)

        # Residual = meanRT - full-model out-of-fold prediction.
        pred = cv_ridge_resid(Xf, y, items)
        resid = y - pred
        resid_var_frac = np.var(resid) / np.var(y)

        # --- G1: split-half reliability of the residual ---------------------
        # Split SUBJECTS into two halves; recompute by-word mean RT per half;
        # residualize EACH half against the SAME full-model design (refit the
        # nuisance+surprisal ridge on that half's by-word RT, out-of-fold), then
        # correlate the two halves' by-word residuals across words.
        rng = np.random.default_rng(SEED)
        workers = rts["WorkerId"].unique()
        n_rep = 25
        resid_rels, rt_rels = [], []
        for rep in range(n_rep):
            perm = rng.permutation(workers)
            hA = set(perm[: len(perm) // 2]); hB = set(perm[len(perm) // 2:])
            rA = rts[rts["WorkerId"].isin(hA)].groupby(["item", "zone"])["RT"].mean()
            rB = rts[rts["WorkerId"].isin(hB)].groupby(["item", "zone"])["RT"].mean()
            wa = w.copy()
            wa["rtA"] = [rA.get((it, zn), np.nan) for it, zn in zip(wa["item"], wa["zone"])]
            wa["rtB"] = [rB.get((it, zn), np.nan) for it, zn in zip(wa["item"], wa["zone"])]
            wa = wa.dropna(subset=["rtA", "rtB"])
            it2 = wa["item"].values
            Xf2 = wa[full_cols].values.astype(float)
            yA = wa["rtA"].values.astype(float)
            yB = wa["rtB"].values.astype(float)
            # raw by-word RT reliability (noise ceiling)
            rt_rels.append(spearmanr(yA, yB).correlation)
            # residualized reliability
            raA = yA - cv_ridge_resid(Xf2, yA, it2)
            rbB = yB - cv_ridge_resid(Xf2, yB, it2)
            resid_rels.append(spearmanr(raA, rbB).correlation)

        rt_rel_raw = float(np.nanmean(rt_rels))
        resid_rel_raw = float(np.nanmean(resid_rels))
        rt_rel_sb = spearman_brown(rt_rel_raw)
        resid_rel_sb = spearman_brown(resid_rel_raw)

        res = {
            "n_words_modeled": int(len(w)),
            "R2_nuisances": [round(r2n_m, 4), round(r2n_h, 4)],
            "R2_full": [round(r2f_m, 4), round(r2f_h, 4)],
            "unique_R2_surprisal": [round(uq_m, 4), round(uq_h, 4)],
            "n_folds": int(len(unique)),
            "residual_var_fraction": round(float(resid_var_frac), 4),
            "rt_splithalf_raw": round(rt_rel_raw, 4),
            "rt_splithalf_SB": round(rt_rel_sb, 4),
            "residual_splithalf_raw": round(resid_rel_raw, 4),
            "residual_splithalf_SB": round(resid_rel_sb, 4),
            "splithalf_reps": n_rep,
        }
        results["models"][key] = res
        print(json.dumps(res, indent=2), flush=True)

    # Save per-word table and results.
    keep = ["item", "zone", "word", "meanRT", "nsubj", "wlen", "logfreq",
            "sentpos", "surp_gpt2", "surp_qwen2.5-0.5b"]
    keep = [c for c in keep if c in tab.columns]
    tab[keep].to_csv(f"{OUT_DIR}/byword_table.csv", index=False)
    with open(f"{OUT_DIR}/g0g1_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {OUT_DIR}/g0g1_results.json and byword_table.csv", flush=True)


if __name__ == "__main__":
    main()
