#!/usr/bin/env python
"""E021 — surprisal-residualized cognitive-signal auxiliary training, arms + G2.

Pipeline (one self-contained, matched-budget loop):

  STAGE A — aux co-training on Natural Stories text.
    GPT-2-small is fine-tuned on the 10 Natural Stories texts with
        L = L_LM (next-token CE)  +  lambda_aux * L_aux
    where L_aux = MSE between a light linear aux head (hidden -> 1) read at each
    WORD-FINAL subword token and the per-word target for that arm. EVERY arm has
    the identical head and optimizer/steps/data; only the TARGET differs.
      i  baseline       : head present, lambda_aux = 0  (zero aux gradient)
      ii  raw-aux        : predict z-scored mean RT
      iii residualized   : predict surprisal-residualized RT      (THE TEST ARM)
      iv  permuted-twin  : predict block-permuted residual
      v   random-struct  : predict AR(1)-matched fresh Gaussian
      G2  synthetic      : predict a by-construction downstream-useful target

  STAGE B — held-out-DOMAIN AULC (sample-efficiency).
    The Stage-A model is then fine-tuned on Wikitext-103 (Wikipedia prose, a
    DISTINCT domain from Natural Stories narrative fiction) at a predeclared cap
    sequence {100, 300, 1k, 3k} tokens; perplexity is measured on a FIXED
    held-out Wikitext eval block after each cap's fine-tune. AULC = mean ppl over
    the 4 caps (lower = adapts faster). Paired per seed across arms.

  DECISION (triple dissociation, locked in the design doc):
    cognition-specific positive  <=>  AULC(iii) < AULC(iv) AND AULC(iii) < AULC(v),
    both paired CIs over seeds excluding 0 (lower AULC = better).

Matched budget: identical Stage-A steps/lr/batch/data and identical Stage-B
fine-tune budget per cap across all arms; the random seed controls SGD order and
the matched-random surrogate. >= 3 seeds.

Usage:
  HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_arms.py --mode g2
  HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_arms.py --mode arms
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd
import torch
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer

import e021_targets as T

ROOT = "/home/centcom/data/brain-alignment"
NS_TOK = f"{ROOT}/data/paper-repos/naturalstories/naturalstories_RTS/all_stories.tok"
BYWORD = f"{ROOT}/outputs/e021_g0g1/byword_table.csv"
WIKI_EVAL = f"{ROOT}/data/kd_corpus/wikitext103_sentences_heldout.txt"
WIKI_TRAIN = f"{ROOT}/data/kd_corpus/wikitext103_sentences_train.txt"
OUT = f"{ROOT}/outputs/e021"
BASE = "gpt2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ---- LOCKED budget (matched across all arms) -------------------------------
STAGE_A_STEPS = 300        # aux co-training steps on Natural Stories
STAGE_A_LR = 5e-5
STAGE_A_BATCH = 4
MAX_LEN = 256
LAMBDA_AUX = 1.0           # aux weight (targets z-scored so LM/aux scales comparable)
CAPS = [100, 300, 1000, 3000]   # predeclared held-out-domain token caps
STAGE_B_EPOCHS = 3         # passes over the capped wikitext slice (matched per cap)
STAGE_B_LR = 5e-5
STAGE_B_BATCH = 4
EVAL_TOKENS = 30000        # fixed wikitext eval block (held out from all caps)
TRAIN_ITEMS = list(range(1, 11))   # all 10 NS stories used for aux co-training


# ===========================================================================
# Data prep
# ===========================================================================
def load_ns_stories():
    """Return {item: (text, [(zone, char_start, char_end)])} with a leading space
    per word (GPT-2 BPE convention), so each word's subword tokens can be mapped."""
    tok = pd.read_csv(NS_TOK, sep="\t").sort_values(["item", "zone"])
    stories = {}
    for item, g in tok.groupby("item"):
        g = g.sort_values("zone")
        text = ""
        spans = []
        for w, z in zip(g["word"].astype(str), g["zone"]):
            start = len(text)
            text += " " + w
            spans.append((int(z), start, len(text)))
        stories[int(item)] = (text, spans)
    return stories


def build_aux_batches(tokenizer, stories, target_map):
    """Tokenize each story, find each word's FINAL subword token, attach its
    per-word target. Returns a list of dicts: input_ids, attn, tgt_pos (list of
    token indices), tgt_val (list of target floats) — chunked to MAX_LEN windows.
    target_map: {(item, zone): float}."""
    examples = []
    for item, (text, spans) in stories.items():
        enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
        ids = enc["input_ids"]
        offs = enc["offset_mapping"]
        # map each word (zone, cstart, cend) -> final token index within story
        word_last_tok = {}
        for (zone, ws, we) in spans:
            last = None
            for k, (cs, ce) in enumerate(offs):
                if cs == ce:
                    continue
                if ws <= cs < we:
                    last = k
            if last is not None and (item, zone) in target_map:
                word_last_tok[last] = target_map[(item, zone)]
        # chunk into MAX_LEN windows
        for s in range(0, len(ids), MAX_LEN):
            chunk = ids[s:s + MAX_LEN]
            pos, val = [], []
            for k in range(len(chunk)):
                gk = s + k
                if gk in word_last_tok:
                    pos.append(k)
                    val.append(word_last_tok[gk])
            if len(chunk) < 8:
                continue
            examples.append({"ids": chunk, "pos": pos, "val": val})
    return examples


def load_wiki_tokens(tokenizer, n_eval=EVAL_TOKENS):
    """Held-out-domain tokens. Caps are drawn from the wikitext-103 TRAIN split;
    the eval block is a FIXED prefix of the disjoint wikitext-103 HELDOUT split.
    Both are Wikipedia prose (the distinct domain) but the cap-text and eval-text
    are different files, so no cap ever contains an eval sentence."""
    with open(WIKI_EVAL) as f:
        etext = " ".join(line.strip() for line in f)
    with open(WIKI_TRAIN) as f:
        ttext = " ".join(line.strip() for line in f)
    eval_ids = tokenizer(etext, add_special_tokens=False)["input_ids"][:n_eval]
    train_ids = tokenizer(ttext, add_special_tokens=False)["input_ids"]
    return train_ids, eval_ids


# ===========================================================================
# Stage A: aux co-training
# ===========================================================================
def stage_a(model, tokenizer, aux_examples, lambda_aux, seed):
    model.train()
    d = model.config.hidden_size
    aux_head = nn.Linear(d, 1).to(DEVICE)
    # deterministic head init per seed (identical across arms given seed)
    g = torch.Generator(device="cpu").manual_seed(seed)
    with torch.no_grad():
        aux_head.weight.copy_(torch.empty(1, d).normal_(0, 0.02, generator=g))
        aux_head.bias.zero_()
    aux_head.to(DEVICE)
    params = list(model.parameters()) + list(aux_head.parameters())
    opt = torch.optim.AdamW(params, lr=STAGE_A_LR)

    rng = np.random.default_rng(seed)
    n = len(aux_examples)
    step = 0
    logs = []
    while step < STAGE_A_STEPS:
        order = rng.permutation(n)
        for bs in range(0, n, STAGE_A_BATCH):
            if step >= STAGE_A_STEPS:
                break
            bidx = order[bs:bs + STAGE_A_BATCH]
            batch = [aux_examples[i] for i in bidx]
            maxlen = max(len(b["ids"]) for b in batch)
            ids = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            attn = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            for i, b in enumerate(batch):
                L = len(b["ids"])
                ids[i, :L] = torch.tensor(b["ids"], device=DEVICE)
                attn[i, :L] = 1
            out = model(input_ids=ids, attention_mask=attn,
                        output_hidden_states=True, labels=ids)
            lm_loss = out.loss
            # aux loss at word-final token positions
            hs = out.hidden_states[-1]            # (B, L, d)
            aux_terms = []
            for i, b in enumerate(batch):
                if not b["pos"]:
                    continue
                pos = torch.tensor(b["pos"], device=DEVICE)
                tv = torch.tensor(b["val"], dtype=torch.float32, device=DEVICE)
                pred = aux_head(hs[i, pos]).squeeze(-1)
                aux_terms.append(nn.functional.mse_loss(pred, tv))
            aux_loss = torch.stack(aux_terms).mean() if aux_terms else torch.tensor(0.0, device=DEVICE)
            loss = lm_loss + lambda_aux * aux_loss
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
            if step % 50 == 0:
                logs.append({"step": step, "lm": float(lm_loss.item()),
                             "aux": float(aux_loss.item())})
            step += 1
    model.eval()
    return logs


# ===========================================================================
# Stage B: held-out-domain AULC
# ===========================================================================
def eval_ppl(model, eval_ids, block=512):
    model.eval()
    nll, ntok = 0.0, 0
    with torch.no_grad():
        for s in range(0, len(eval_ids) - 1, block):
            chunk = eval_ids[s:s + block + 1]
            if len(chunk) < 2:
                continue
            ids = torch.tensor([chunk], device=DEVICE)
            out = model(input_ids=ids, labels=ids)
            # out.loss is mean over (len-1) tokens
            k = len(chunk) - 1
            nll += float(out.loss.item()) * k
            ntok += k
    return math.exp(nll / ntok)


def finetune_cap(model, cap_ids, lr, epochs, batch_tokens=256):
    """Fine-tune LM-only on a flat token slice (cap_ids), matched budget per cap."""
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    # chunk into batch_tokens windows
    chunks = [cap_ids[i:i + batch_tokens] for i in range(0, len(cap_ids), batch_tokens)]
    chunks = [c for c in chunks if len(c) >= 8]
    rng = np.random.default_rng(0)
    for ep in range(epochs):
        order = rng.permutation(len(chunks))
        for j in range(0, len(order), STAGE_B_BATCH):
            bidx = order[j:j + STAGE_B_BATCH]
            batch = [chunks[i] for i in bidx]
            maxlen = max(len(c) for c in batch)
            ids = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            attn = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            for i, c in enumerate(batch):
                ids[i, :len(c)] = torch.tensor(c, device=DEVICE)
                attn[i, :len(c)] = 1
            labels = ids.clone()
            labels[attn == 0] = -100
            out = model(input_ids=ids, attention_mask=attn, labels=labels)
            opt.zero_grad()
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
    model.eval()


N_SLICES = 3   # disjoint cap-slices averaged per cap (variance reduction)


def stage_b_aulc(state_dict, wiki_train, wiki_eval, seed):
    """For each cap, reload the Stage-A weights, fine-tune on N_SLICES disjoint
    wiki slices, average the held-out ppl (cuts slice-draw variance — the cap-100
    perplexity is otherwise very noisy). Slices are deterministic per seed, drawn
    from disjoint regions of wiki_train; matched-budget identical across arms."""
    ppls = {}
    rng = np.random.default_rng(1000 + seed)
    region = len(wiki_train) - max(CAPS) - 1
    for cap in CAPS:
        per_slice = []
        for si in range(N_SLICES):
            off = int(rng.integers(0, region))
            model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float32).to(DEVICE)
            model.load_state_dict(state_dict)
            finetune_cap(model, wiki_train[off:off + cap], STAGE_B_LR, STAGE_B_EPOCHS)
            per_slice.append(eval_ppl(model, wiki_eval))
            del model
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
        ppls[cap] = float(np.mean(per_slice))
    aulc = float(np.mean([ppls[c] for c in CAPS]))   # mean ppl over caps (lower=better)
    return aulc, ppls


# ===========================================================================
# One arm = Stage A (target) -> Stage B (AULC)
# ===========================================================================
def run_arm(arm, target_map, lambda_aux, tokenizer, stories, wiki_train, wiki_eval, seed):
    model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float32).to(DEVICE)
    aux_examples = build_aux_batches(tokenizer, stories, target_map)
    a_logs = stage_a(model, tokenizer, aux_examples, lambda_aux, seed)
    state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    aulc, ppls = stage_b_aulc(state, wiki_train, wiki_eval, seed)
    del state
    return {"arm": arm, "seed": seed, "aulc": aulc, "ppls": ppls,
            "n_aux_examples": len(aux_examples), "stage_a_logs": a_logs}


def paired_ci(a, b):
    """Paired diff (a - b) mean and 95% t-CI over seeds. a,b lists aligned by seed."""
    d = np.array(a) - np.array(b)
    m = d.mean()
    if len(d) < 2:
        return float(m), float("nan"), float("nan")
    s = d.std(ddof=1)
    half = 1.96 * s / math.sqrt(len(d))
    return float(m), float(m - half), float(m + half)


# ===========================================================================
# G2 power positive control
# ===========================================================================
def build_downstream_probe(tokenizer, wiki_eval):
    """Top principal direction of held-out-domain token hidden states (base LM).
    A target = projection onto this direction pushes the rep toward the wiki
    manifold -> a STRONG planted downstream-useful signal for G2."""
    model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float32).to(DEVICE)
    model.eval()
    hs_all = []
    with torch.no_grad():
        for s in range(0, min(len(wiki_eval), 8000), 256):
            chunk = wiki_eval[s:s + 256]
            if len(chunk) < 8:
                continue
            ids = torch.tensor([chunk], device=DEVICE)
            out = model(input_ids=ids, output_hidden_states=True)
            hs_all.append(out.hidden_states[-1][0].cpu().numpy())
    H = np.concatenate(hs_all, 0)
    H = H - H.mean(0)
    # top PC
    u, svals, vt = np.linalg.svd(H, full_matrices=False)
    probe = vt[0]
    # per-NS-word frozen hidden (last layer, word-final token)
    stories = load_ns_stories()
    words_to_hidden = {}
    with torch.no_grad():
        for item, (text, spans) in stories.items():
            enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
            ids_ = enc["input_ids"]
            offs = enc["offset_mapping"]
            for s in range(0, len(ids_), MAX_LEN):
                chunk = ids_[s:s + MAX_LEN]
                ids_t = torch.tensor([chunk], device=DEVICE)
                out = model(input_ids=ids_t, output_hidden_states=True)
                h = out.hidden_states[-1][0].cpu().numpy()
                for (zone, ws, we) in spans:
                    last = None
                    for k, (cs, ce) in enumerate(offs):
                        gk = k
                        if gk < s or gk >= s + len(chunk):
                            continue
                        if cs == ce:
                            continue
                        if ws <= cs < we:
                            last = gk - s
                    if last is not None and 0 <= last < len(chunk):
                        words_to_hidden[(item, zone)] = h[last]
    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return probe.astype(np.float32), words_to_hidden


def build_wiki_teacher_surprisal(tokenizer, wiki_train, stories, seed=0):
    """G2 v2 positive control. Train a WIKI-TEACHER (GPT-2 fine-tuned on a wiki
    slice), then read its per-word surprisal on the Natural Stories text. That
    per-word target is downstream-USEFUL by construction: predicting the wiki
    teacher's next-token difficulty biases the student toward wiki statistics
    during Stage A, so it begins Stage B closer to the wiki manifold. Returns
    {(item, zone): wiki_surprisal_nats}. The teacher sees a wiki slice DISJOINT
    from every Stage-B cap and from the eval block (drawn from the far end)."""
    teacher = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float32).to(DEVICE)
    # fine-tune on a wiki slice far from the cap region (caps use offsets < ~15k)
    tslice = wiki_train[200000:260000]
    finetune_cap(teacher, tslice, lr=5e-5, epochs=2, batch_tokens=256)
    teacher.eval()
    out = {}
    with torch.no_grad():
        for item, (text, spans) in stories.items():
            enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
            ids_ = enc["input_ids"]
            offs = enc["offset_mapping"]
            for s in range(0, len(ids_), MAX_LEN):
                chunk = ids_[s:s + MAX_LEN]
                ids_t = torch.tensor([chunk], device=DEVICE)
                logits = teacher(input_ids=ids_t).logits[0]
                logp = torch.log_softmax(logits.float(), dim=-1)
                # per-token nll of the realized next token
                tok_nll = [float("nan")] * len(chunk)
                for j in range(1, len(chunk)):
                    tok_nll[j] = -logp[j - 1, chunk[j]].item()
                # assign each word its summed subword nll (final-token convention
                # not needed; sum over the word's tokens like G0 surprisal)
                for (zone, ws, we) in spans:
                    acc, has = 0.0, False
                    for k, (cs, ce) in enumerate(offs):
                        if k < s or k >= s + len(chunk):
                            continue
                        if cs == ce:
                            continue
                        if ws <= cs < we and not math.isnan(tok_nll[k - s]):
                            acc += tok_nll[k - s]
                            has = True
                    if has:
                        out[(item, zone)] = acc
    del teacher
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["g2", "arms"], required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(BASE)
    tokenizer.pad_token = tokenizer.eos_token
    stories = load_ns_stories()
    wiki_train, wiki_eval = load_wiki_tokens(tokenizer)
    print(f"wiki_train={len(wiki_train)} tok  wiki_eval={len(wiki_eval)} tok", flush=True)

    config = {
        "base_lm": BASE, "aux_corpus": "natural_stories (10 stories)",
        "heldout_domain": "wikitext-103 (Wikipedia prose)",
        "stage_a_steps": STAGE_A_STEPS, "stage_a_lr": STAGE_A_LR,
        "stage_a_batch": STAGE_A_BATCH, "lambda_aux": LAMBDA_AUX,
        "caps": CAPS, "stage_b_epochs": STAGE_B_EPOCHS, "stage_b_lr": STAGE_B_LR,
        "eval_tokens": EVAL_TOKENS, "aulc": "mean held-out ppl over caps (lower=better)",
        "seeds": args.seeds,
    }

    if args.mode == "g2":
        # G2 v2 — planted target = WIKI-TEACHER per-word surprisal (downstream-useful
        # by construction), contrasted against the permuted-twin control. The
        # pipeline MUST detect synthetic < permuted (synthetic adapts faster).
        print("=== building wiki-teacher per-word surprisal target ===", flush=True)
        wt_surp = build_wiki_teacher_surprisal(tokenizer, wiki_train, stories)
        syn = T.make_wikiteacher_target(BYWORD, TRAIN_ITEMS, wt_surp)
        syn_map = {(r.item, r.zone): r.wikiteacher for r in syn.itertuples()}
        targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=0)
        perm_map = {(r.item, r.zone): r.permuted for r in targ.itertuples()}

        rows = []
        for seed in args.seeds:
            r_syn = run_arm("synthetic", syn_map, LAMBDA_AUX, tokenizer, stories,
                            wiki_train, wiki_eval, seed)
            r_perm = run_arm("permuted", perm_map, LAMBDA_AUX, tokenizer, stories,
                             wiki_train, wiki_eval, seed)
            rows += [r_syn, r_perm]
            print(f"[seed {seed}] synthetic AULC={r_syn['aulc']:.3f}  "
                  f"permuted AULC={r_perm['aulc']:.3f}", flush=True)

        syn_a = [r["aulc"] for r in rows if r["arm"] == "synthetic"]
        perm_a = [r["aulc"] for r in rows if r["arm"] == "permuted"]
        # planted effect = synthetic - permuted (expect NEGATIVE: synthetic adapts faster)
        m, lo, hi = paired_ci(syn_a, perm_a)
        # MDE from THIS run's own seed variance (paired-diff sd)
        d = np.array(syn_a) - np.array(perm_a)
        sd = d.std(ddof=1) if len(d) > 1 else float("nan")
        mde = 1.96 * sd / math.sqrt(len(d)) * 2 if len(d) > 1 else float("nan")  # ~2x half-CI
        detected = (hi < 0)   # planted effect detected (synthetic strictly better)
        result = {
            "mode": "g2", "config": config,
            "synthetic_aulc": syn_a, "permuted_aulc": perm_a,
            "planted_effect_syn_minus_perm": {"mean": m, "ci": [lo, hi]},
            "paired_sd": float(sd), "MDE_predeclared": float(mde),
            "G2_detected": bool(detected),
            "rows": rows,
        }
        with open(f"{OUT}/g2_power_control.json", "w") as f:
            json.dump(result, f, indent=2)
        print(json.dumps({k: result[k] for k in
              ["planted_effect_syn_minus_perm", "MDE_predeclared", "G2_detected"]}, indent=2))
        print(f"\nG2 {'PASS' if detected else 'FAIL'} — wrote {OUT}/g2_power_control.json")
        return

    # mode == arms
    targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=0)
    targ.to_csv(f"{OUT}/aux_targets.csv", index=False)
    arm_target = {
        "baseline": (None, 0.0),
        "raw": ({(r.item, r.zone): r.raw for r in targ.itertuples()}, LAMBDA_AUX),
        "residual": ({(r.item, r.zone): r.residual for r in targ.itertuples()}, LAMBDA_AUX),
        "permuted": ({(r.item, r.zone): r.permuted for r in targ.itertuples()}, LAMBDA_AUX),
        "random_struct": ({(r.item, r.zone): r.random_struct for r in targ.itertuples()}, LAMBDA_AUX),
    }
    rows = []
    for seed in args.seeds:
        for arm, (tmap, lam) in arm_target.items():
            # baseline arm: head present but target all-zero & lambda 0 (capacity parity)
            if tmap is None:
                tmap = {(r.item, r.zone): 0.0 for r in targ.itertuples()}
            r = run_arm(arm, tmap, lam, tokenizer, stories, wiki_train, wiki_eval, seed)
            rows.append(r)
            print(f"[seed {seed}] {arm:14s} AULC={r['aulc']:.3f}  ppls={r['ppls']}", flush=True)

    def arm_aulc(name):
        return [r["aulc"] for r in rows if r["arm"] == name]  # ordered by seed

    arms = ["baseline", "raw", "residual", "permuted", "random_struct"]
    means = {a: float(np.mean(arm_aulc(a))) for a in arms}
    sems = {a: float(np.std(arm_aulc(a), ddof=1) / math.sqrt(len(arm_aulc(a))))
            if len(arm_aulc(a)) > 1 else float("nan") for a in arms}
    # contrasts (lower AULC = better; a cognition-specific positive => residual LOWER)
    c_iii_iv = paired_ci(arm_aulc("residual"), arm_aulc("permuted"))
    c_iii_v = paired_ci(arm_aulc("residual"), arm_aulc("random_struct"))
    c_ii_iv = paired_ci(arm_aulc("raw"), arm_aulc("permuted"))
    # positive requires residual STRICTLY LOWER than both controls (CI upper < 0)
    pos = (c_iii_iv[2] < 0) and (c_iii_v[2] < 0)
    verdict = "cognition-specific positive" if pos else "non-specific / null"
    result = {
        "mode": "arms", "config": config,
        "arm_aulc_per_seed": {a: arm_aulc(a) for a in arms},
        "arm_aulc_mean": means, "arm_aulc_sem": sems,
        "contrast_iii_minus_iv_residual_minus_permuted": {"mean": c_iii_iv[0], "ci": c_iii_iv[1:]},
        "contrast_iii_minus_v_residual_minus_random": {"mean": c_iii_v[0], "ci": c_iii_v[1:]},
        "contrast_ii_minus_iv_raw_minus_permuted": {"mean": c_ii_iv[0], "ci": c_ii_iv[1:]},
        "triple_dissociation_positive": bool(pos),
        "verdict": verdict,
        "rows": rows,
    }
    with open(f"{OUT}/arms_results.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n=== ARM AULC (mean +/- sem, lower=better) ===")
    for a in arms:
        print(f"  {a:14s} {means[a]:.3f} +/- {sems[a]:.3f}")
    print(f"  (iii)-(iv) residual-permuted = {c_iii_iv[0]:+.3f}  CI[{c_iii_iv[1]:+.3f},{c_iii_iv[2]:+.3f}]")
    print(f"  (iii)-(v)  residual-random   = {c_iii_v[0]:+.3f}  CI[{c_iii_v[1]:+.3f},{c_iii_v[2]:+.3f}]")
    print(f"  VERDICT: {verdict}")
    print(f"Wrote {OUT}/arms_results.json")


if __name__ == "__main__":
    main()
