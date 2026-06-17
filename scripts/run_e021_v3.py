#!/usr/bin/env python
"""E021 v3 — CLEAN frozen-probe AULC rerun (Codex fixes 1-6 + log-freq control arm).

Same locked design as run_e021_v2.py (frozen-trunk linear-probe AULC, lower=better),
with the Codex-confirmed fixes applied and the decisive log-frequency control arm
added. Writes NEW filenames (arms_v3_*, g2v3_*); does NOT overwrite v2.

FIXES APPLIED (file:line refer to the v2 sources these replace):
  1. Stage-A pad-label bug (run_e021_arms.py:182-183). v2 reused run_e021_arms.stage_a,
     which called model(..., labels=ids) with `ids` straight — padded positions
     (attention_mask==0) contributed to the LM CE loss. v3 defines its own
     stage_a_fixed that builds labels = ids.clone(); labels[attn==0] = -100 before
     the model call, so pads never count. (Expected to shrink the ~500 baseline->
     structured AULC gap that was partly a pad artifact.)
  2. Per-seed surrogates (run_e021_v2.py:339, :291). v2 called make_targets(seed=0)
     ONCE for all experiment seeds, so permuted/random_struct were identical across
     seeds. v3 regenerates the targets with the EXPERIMENT seed each run.
  3. Out-of-fold residualization (e021_targets.py residualize_rt). v2's residual was
     fit+predicted on the same rows (in-sample). v3 uses
     e021_targets_v3.residualize_rt_oof (leave-one-story-out).
  4. Identical probe init across arms (run_e021_v2.py:145-150). v2's fresh_probe
     copied EACH ARM's own post-Stage-A wte, giving an arm-specific readout-init
     advantage. v3 initializes the probe identically for every arm/seed from the
     BASE (pre-Stage-A) GPT-2 wte (a single fixed tensor), so the metric reflects
     frozen-hidden quality only.
  5. Seed the trunk training (run_e021_arms.stage_a). v3's stage_a_fixed calls
     torch.manual_seed(seed) before training so dropout is controlled per the
     paired-seed design (the np rng already controlled batch order; this controls
     the torch-side stochasticity too).
  6. (vi) log-frequency arm — z-scored per-word log unigram frequency, word-aligned
     identically to the other targets. A REAL, perfectly aligned, NON-cognitive
     surface feature already regressed out of the residual. Decisive control.

Usage:
  HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_v3.py --mode g2v2
  HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_v3.py --mode arms
"""
from __future__ import annotations

import argparse
import json
import math
import os

import numpy as np
import torch
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer

import e021_targets_v3 as T
# REUSE data prep + constants exactly; do NOT reuse the buggy stage_a / fresh_probe.
from run_e021_arms import (
    BASE, DEVICE, OUT, MAX_LEN, LAMBDA_AUX, CAPS, BYWORD, TRAIN_ITEMS,
    STAGE_A_LR, STAGE_A_BATCH, STAGE_A_STEPS,
    load_ns_stories, build_aux_batches, load_wiki_tokens,
)

# ---- Frozen-probe Stage-B budget (matched across all arms) -----------------
PROBE_LR = 1e-3
PROBE_EPOCHS = 8
PROBE_BATCH = 4
PROBE_BLOCK = 256
N_SLICES = 3


# ===========================================================================
# Stage A — FIXED (pad labels masked; trunk seeded)
# ===========================================================================
def stage_a_fixed(model, tokenizer, aux_examples, lambda_aux, seed):
    """Stage-A aux co-training with the pad-label fix (1) and torch seed (5).
    Otherwise identical to run_e021_arms.stage_a: light linear aux head read at
    word-final tokens, MSE vs per-word target, gradient into the trunk, matched
    steps/lr/batch/data across arms, deterministic per-seed head init."""
    torch.manual_seed(seed)                                  # FIX 5: control dropout etc.
    model.train()
    d = model.config.hidden_size
    aux_head = nn.Linear(d, 1).to(DEVICE)
    g = torch.Generator(device="cpu").manual_seed(seed)      # identical head init across arms
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
            labels = ids.clone()                             # FIX 1: pads do not count
            labels[attn == 0] = -100
            out = model(input_ids=ids, attention_mask=attn,
                        output_hidden_states=True, labels=labels)
            lm_loss = out.loss
            hs = out.hidden_states[-1]                       # (B, L, d)
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


def stage_a_aux_arm(target_map, lambda_aux, tokenizer, stories, seed):
    model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32).to(DEVICE)
    aux_examples = build_aux_batches(tokenizer, stories, target_map)
    a_logs = stage_a_fixed(model, tokenizer, aux_examples, lambda_aux, seed)
    state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    n_aux = len(aux_examples)
    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return state, a_logs, n_aux


def stage_a_headstart(tokenizer, wiki_train, seed):
    """G2 v2 PLANTED prior — head-start trunk: Stage-A pure-LM on a held-out wiki
    slice (disjoint from every probe cap and the eval block). FIX 1 (pad labels)
    and FIX 5 (torch seed) applied; matched STAGE_A_STEPS/lr/batch to the aux arms."""
    torch.manual_seed(seed)                                  # FIX 5
    model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32).to(DEVICE)
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=STAGE_A_LR)
    hs_slice = wiki_train[len(wiki_train) - 400000: len(wiki_train) - 100000]
    chunks = [hs_slice[i:i + MAX_LEN] for i in range(0, len(hs_slice), MAX_LEN)]
    chunks = [c for c in chunks if len(c) >= 8]
    rng = np.random.default_rng(seed)
    step = 0
    logs = []
    while step < STAGE_A_STEPS:
        order = rng.permutation(len(chunks))
        for j in range(0, len(order), STAGE_A_BATCH):
            if step >= STAGE_A_STEPS:
                break
            bidx = order[j:j + STAGE_A_BATCH]
            batch = [chunks[i] for i in bidx]
            maxlen = max(len(c) for c in batch)
            ids = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            attn = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            for i, c in enumerate(batch):
                ids[i, :len(c)] = torch.tensor(c, device=DEVICE)
                attn[i, :len(c)] = 1
            labels = ids.clone()                             # FIX 1 (already present in v2 headstart, kept)
            labels[attn == 0] = -100
            out = model(input_ids=ids, attention_mask=attn, labels=labels)
            opt.zero_grad()
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            if step % 50 == 0:
                logs.append({"step": step, "lm": float(out.loss.item())})
            step += 1
    model.eval()
    state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return state, logs


# ===========================================================================
# Frozen-representation linear probe — FIX 4: identical init across arms
# ===========================================================================
def _hidden_states(model, ids, attn):
    out = model(input_ids=ids, attention_mask=attn, output_hidden_states=True)
    return out.hidden_states[-1]


def train_frozen_probe(model, probe, cap_ids, seed):
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    probe.train()
    opt = torch.optim.AdamW(probe.parameters(), lr=PROBE_LR)
    chunks = [cap_ids[i:i + PROBE_BLOCK] for i in range(0, len(cap_ids), PROBE_BLOCK)]
    chunks = [c for c in chunks if len(c) >= 8]
    rng = np.random.default_rng(seed)
    ce = nn.CrossEntropyLoss(ignore_index=-100)
    for ep in range(PROBE_EPOCHS):
        order = rng.permutation(len(chunks))
        for j in range(0, len(order), PROBE_BATCH):
            bidx = order[j:j + PROBE_BATCH]
            batch = [chunks[i] for i in bidx]
            maxlen = max(len(c) for c in batch)
            ids = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            attn = torch.zeros(len(batch), maxlen, dtype=torch.long, device=DEVICE)
            for i, c in enumerate(batch):
                ids[i, :len(c)] = torch.tensor(c, device=DEVICE)
                attn[i, :len(c)] = 1
            with torch.no_grad():
                hs = _hidden_states(model, ids, attn)
            logits = probe(hs)
            labels = ids.clone()
            labels[attn == 0] = -100
            sl = logits[:, :-1, :].reshape(-1, logits.size(-1))
            tl = labels[:, 1:].reshape(-1)
            loss = ce(sl, tl)
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(probe.parameters(), 1.0)
            opt.step()
    probe.eval()


def eval_probe_ppl(model, probe, eval_ids, block=512):
    model.eval()
    probe.eval()
    ce = nn.CrossEntropyLoss(ignore_index=-100, reduction="sum")
    nll, ntok = 0.0, 0
    with torch.no_grad():
        for s in range(0, len(eval_ids) - 1, block):
            chunk = eval_ids[s:s + block + 1]
            if len(chunk) < 2:
                continue
            ids = torch.tensor([chunk], device=DEVICE)
            attn = torch.ones_like(ids)
            hs = _hidden_states(model, ids, attn)
            logits = probe(hs)
            sl = logits[0, :-1, :]
            tl = ids[0, 1:]
            nll += float(ce(sl, tl).item())
            ntok += tl.numel()
    return math.exp(nll / ntok)


def fresh_probe(base_wte, d, vocab):
    """FIX 4: identical probe init for EVERY arm/seed — a single fixed tensor,
    the BASE (pre-Stage-A) GPT-2 wte. NOT each arm's own post-Stage-A wte (which
    leaked an arm-specific readout-init advantage into the v2 metric)."""
    probe = nn.Linear(d, vocab, bias=False).to(DEVICE)
    with torch.no_grad():
        probe.weight.copy_(base_wte)
    return probe


def frozen_probe_aulc(state_dict, base_wte, wiki_train, wiki_eval, seed, d, vocab):
    ppls = {}
    rng = np.random.default_rng(2000 + seed)
    region = len(wiki_train) - max(CAPS) - 1
    for cap in CAPS:
        per_slice = []
        for si in range(N_SLICES):
            off = int(rng.integers(0, region))
            model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32).to(DEVICE)
            model.load_state_dict(state_dict)
            probe = fresh_probe(base_wte, d, vocab)          # FIX 4: identical init
            train_frozen_probe(model, probe, wiki_train[off:off + cap], seed * 100 + si)
            per_slice.append(eval_probe_ppl(model, probe, wiki_eval))
            del model, probe
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
        ppls[cap] = float(np.mean(per_slice))
    aulc = float(np.mean([ppls[c] for c in CAPS]))
    return aulc, ppls


# ===========================================================================
# Stats
# ===========================================================================
def paired_ci(a, b):
    d = np.array(a) - np.array(b)
    m = d.mean()
    if len(d) < 2:
        return float(m), float("nan"), float("nan")
    s = d.std(ddof=1)
    half = 1.96 * s / math.sqrt(len(d))
    return float(m), float(m - half), float(m + half)


# ===========================================================================
# Main
# ===========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["g2v2", "arms"], required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(BASE)
    tokenizer.pad_token = tokenizer.eos_token
    stories = load_ns_stories()
    wiki_train, wiki_eval = load_wiki_tokens(tokenizer)
    print(f"wiki_train={len(wiki_train)} tok  wiki_eval={len(wiki_eval)} tok", flush=True)

    m0 = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32)
    d, vocab = m0.config.hidden_size, m0.config.vocab_size
    # FIX 4: capture the base (pre-Stage-A) wte ONCE as the shared probe init.
    base_wte = m0.state_dict()["transformer.wte.weight"].detach().clone().to(DEVICE)
    del m0

    config = {
        "base_lm": BASE, "aux_corpus": "natural_stories (10 stories)",
        "heldout_domain": "wikitext-103 (Wikipedia prose)",
        "metric": "frozen-trunk linear-probe AULC (mean held-out-domain probe ppl over caps, lower=better)",
        "version": "v3 (Codex fixes 1-5 + log-freq arm)",
        "stage_a_steps": STAGE_A_STEPS, "stage_a_lr": STAGE_A_LR,
        "stage_a_batch": STAGE_A_BATCH, "lambda_aux": LAMBDA_AUX,
        "caps": CAPS, "probe_lr": PROBE_LR, "probe_epochs": PROBE_EPOCHS,
        "probe_block": PROBE_BLOCK, "n_slices": N_SLICES, "seeds": args.seeds,
        "fixes": ["pad_labels_-100", "per_seed_surrogates", "oof_residual",
                  "identical_probe_init_base_wte", "torch_manual_seed_trunk", "logfreq_arm"],
    }

    if args.mode == "g2v2":
        targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=0)
        ctrl_map = {(r.item, r.zone): 0.0 for r in targ.itertuples()}
        rows = []
        for seed in args.seeds:
            hs_state, hs_logs = stage_a_headstart(tokenizer, wiki_train, seed)
            hs_aulc, hs_ppls = frozen_probe_aulc(hs_state, base_wte, wiki_train, wiki_eval, seed, d, vocab)
            del hs_state
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
            ct_state, ct_logs, _ = stage_a_aux_arm(ctrl_map, 0.0, tokenizer, stories, seed)
            ct_aulc, ct_ppls = frozen_probe_aulc(ct_state, base_wte, wiki_train, wiki_eval, seed, d, vocab)
            del ct_state
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
            rows.append({"seed": seed, "headstart_aulc": hs_aulc, "control_aulc": ct_aulc,
                         "headstart_ppls": hs_ppls, "control_ppls": ct_ppls,
                         "headstart_stage_a": hs_logs, "control_stage_a": ct_logs})
            print(f"[seed {seed}] headstart AULC={hs_aulc:.3f}  control AULC={ct_aulc:.3f}  "
                  f"diff(hs-ctrl)={hs_aulc - ct_aulc:+.3f}", flush=True)

        hs_a = [r["headstart_aulc"] for r in rows]
        ct_a = [r["control_aulc"] for r in rows]
        m, lo, hi = paired_ci(hs_a, ct_a)
        diff = np.array(hs_a) - np.array(ct_a)
        sd = diff.std(ddof=1) if len(diff) > 1 else float("nan")
        mde = 1.96 * sd / math.sqrt(len(diff)) if len(diff) > 1 else float("nan")
        detected = bool(hi < 0)
        result = {
            "mode": "g2v2", "config": config,
            "headstart_aulc_per_seed": hs_a, "control_aulc_per_seed": ct_a,
            "planted_effect_headstart_minus_control": {"mean": m, "ci": [lo, hi]},
            "paired_sd": float(sd), "MDE_predeclared": float(mde),
            "G2v2_detected": detected,
            "verdict": ("PASS — frozen-probe AULC detects the planted representational prior"
                        if detected else
                        "FAIL — planted prior not detected (or wrong sign) -> STOP, bounded/inconclusive"),
            "rows": rows,
        }
        with open(f"{OUT}/g2v3_frozen_probe.json", "w") as f:
            json.dump(result, f, indent=2)
        print(json.dumps({k: result[k] for k in
              ["planted_effect_headstart_minus_control", "MDE_predeclared", "G2v2_detected", "verdict"]}, indent=2))
        print(f"\nG2 v3 {'PASS' if detected else 'FAIL'} — wrote {OUT}/g2v3_frozen_probe.json")
        return

    # mode == arms — 6 arms (FIX 6 adds logfreq). Targets regenerated PER SEED (FIX 2).
    arms = ["baseline", "raw", "residual", "permuted", "random_struct", "logfreq"]
    rows = []
    for seed in args.seeds:
        targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=seed)   # FIX 2: per-seed surrogates
        if seed == args.seeds[0]:
            targ.to_csv(f"{OUT}/aux_targets_v3.csv", index=False)
        arm_target = {
            "baseline": (None, 0.0),
            "raw": ({(r.item, r.zone): r.raw for r in targ.itertuples()}, LAMBDA_AUX),
            "residual": ({(r.item, r.zone): r.residual for r in targ.itertuples()}, LAMBDA_AUX),
            "permuted": ({(r.item, r.zone): r.permuted for r in targ.itertuples()}, LAMBDA_AUX),
            "random_struct": ({(r.item, r.zone): r.random_struct for r in targ.itertuples()}, LAMBDA_AUX),
            "logfreq": ({(r.item, r.zone): r.logfreq for r in targ.itertuples()}, LAMBDA_AUX),
        }
        for arm in arms:
            tmap, lam = arm_target[arm]
            if tmap is None:
                tmap = {(r.item, r.zone): 0.0 for r in targ.itertuples()}
            state, a_logs, n_aux = stage_a_aux_arm(tmap, lam, tokenizer, stories, seed)
            aulc, ppls = frozen_probe_aulc(state, base_wte, wiki_train, wiki_eval, seed, d, vocab)
            del state
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
            rows.append({"arm": arm, "seed": seed, "aulc": aulc, "ppls": ppls,
                         "n_aux_examples": n_aux, "stage_a_logs": a_logs})
            print(f"[seed {seed}] {arm:14s} AULC={aulc:.3f}  ppls={ppls}", flush=True)

    def arm_aulc(name):
        return [r["aulc"] for r in rows if r["arm"] == name]

    means = {a: float(np.mean(arm_aulc(a))) for a in arms}
    sems = {a: float(np.std(arm_aulc(a), ddof=1) / math.sqrt(len(arm_aulc(a))))
            if len(arm_aulc(a)) > 1 else float("nan") for a in arms}
    c_iii_iv = paired_ci(arm_aulc("residual"), arm_aulc("permuted"))
    c_iii_v = paired_ci(arm_aulc("residual"), arm_aulc("random_struct"))
    c_ii_iii = paired_ci(arm_aulc("raw"), arm_aulc("residual"))           # raw - residual (DPI check)
    c_ii_iv = paired_ci(arm_aulc("raw"), arm_aulc("permuted"))
    c_lf_iv = paired_ci(arm_aulc("logfreq"), arm_aulc("permuted"))        # DECISIVE: logfreq - permuted
    c_lf_v = paired_ci(arm_aulc("logfreq"), arm_aulc("random_struct"))    # DECISIVE: logfreq - random
    pos = (c_iii_iv[2] < 0) and (c_iii_v[2] < 0)
    # cognition-specificity reopens ONLY if logfreq sits at the floor while residual beats it.
    logfreq_beats_controls = (c_lf_iv[2] < 0) and (c_lf_v[2] < 0)
    verdict = ("generic word-aligned regularization (cognition NOT the ingredient) — "
               "logfreq, a non-cognitive aligned feature, ALSO beats the surrogates"
               if logfreq_beats_controls else
               "logfreq sits at the surrogate floor — cognition-specificity NOT excluded by this control")
    result = {
        "mode": "arms", "config": config,
        "arm_aulc_per_seed": {a: arm_aulc(a) for a in arms},
        "arm_aulc_mean": means, "arm_aulc_sem": sems,
        "contrast_iii_minus_iv_residual_minus_permuted": {"mean": c_iii_iv[0], "ci": c_iii_iv[1:]},
        "contrast_iii_minus_v_residual_minus_random": {"mean": c_iii_v[0], "ci": c_iii_v[1:]},
        "contrast_ii_minus_iii_raw_minus_residual": {"mean": c_ii_iii[0], "ci": c_ii_iii[1:]},
        "contrast_ii_minus_iv_raw_minus_permuted": {"mean": c_ii_iv[0], "ci": c_ii_iv[1:]},
        "contrast_logfreq_minus_permuted_DECISIVE": {"mean": c_lf_iv[0], "ci": c_lf_iv[1:]},
        "contrast_logfreq_minus_random_DECISIVE": {"mean": c_lf_v[0], "ci": c_lf_v[1:]},
        "triple_dissociation_residual_positive": bool(pos),
        "logfreq_also_beats_controls": bool(logfreq_beats_controls),
        "verdict": verdict,
        "rows": rows,
    }
    with open(f"{OUT}/arms_v3_results.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n=== ARM frozen-probe AULC v3 (mean +/- sem, lower=better) ===")
    for a in arms:
        print(f"  {a:14s} {means[a]:.3f} +/- {sems[a]:.3f}")
    print(f"  (iii)-(iv) residual-permuted = {c_iii_iv[0]:+.3f}  CI[{c_iii_iv[1]:+.3f},{c_iii_iv[2]:+.3f}]")
    print(f"  (iii)-(v)  residual-random   = {c_iii_v[0]:+.3f}  CI[{c_iii_v[1]:+.3f},{c_iii_v[2]:+.3f}]")
    print(f"  (ii)-(iii) raw-residual      = {c_ii_iii[0]:+.3f}  CI[{c_ii_iii[1]:+.3f},{c_ii_iii[2]:+.3f}]")
    print(f"  logfreq-permuted (DECISIVE)  = {c_lf_iv[0]:+.3f}  CI[{c_lf_iv[1]:+.3f},{c_lf_iv[2]:+.3f}]")
    print(f"  logfreq-random   (DECISIVE)  = {c_lf_v[0]:+.3f}  CI[{c_lf_v[1]:+.3f},{c_lf_v[2]:+.3f}]")
    print(f"  VERDICT: {verdict}")
    print(f"Wrote {OUT}/arms_v3_results.json")


if __name__ == "__main__":
    main()
