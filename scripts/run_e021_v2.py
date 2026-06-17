#!/usr/bin/env python
"""E021 v2 — frozen-representation linear-probe AULC (REVISED metric, S22 lock).

The fine-tune-then-perplexity AULC metric (run_e021_arms.py) is RETIRED — it was
unpowered and biased (G2 v1 FAILED, wrong sign every seed; see outputs/e021/
G2_VERDICT.md). This script implements the LOCKED replacement from
docs/experiments/E021_surprisal-residualized-cognitive-signal.md:

  STAGE A — aux co-training (UNCHANGED, reused from run_e021_arms.py's stage_a).
    GPT-2-small fine-tuned on the 10 Natural Stories texts with
        L = L_LM (next-token CE)  +  lambda_aux * L_aux
    L_aux = MSE of a light linear aux head (hidden->1) at each WORD-FINAL subword
    token vs the per-word target. Gradient flows into the trunk — that is the
    mechanism we want to measure. Every arm shares head/optimizer/steps/data;
    only the TARGET differs.

  STAGE B — FROZEN-REPRESENTATION linear-probe AULC (THE FIX).
    FREEZE the Stage-A trunk (transformer body + embeddings + ln_f). Then train
    ONLY a fresh linear probe = an UNTIED nn.Linear(d, vocab) initialised from the
    frozen wte, on held-out-DOMAIN Wikitext-103 prose, across the predeclared caps
    {100, 300, 1k, 3k} tokens. PRIMARY metric = AULC = mean held-out-domain
    frozen-probe perplexity over the 4 caps (lower=better), paired per seed. This
    measures the installed representational change WITHOUT the fine-tune-overwrite
    or trunk-perturbation-of-generation confound that killed v1.
      (GPT-2's hidden_states[-1] is post-ln_f and logits = hs @ lm_head.weight.T,
       so a frozen-trunk probe is exactly: train a fresh Linear(d,vocab) on hs.)

  G2 v2 — power positive-control on the NEW metric (RUN FIRST, hard gate).
    Plant a KNOWN representational prior: a "head-start" arm whose Stage-A co-trains
    the trunk toward held-out-domain (Wikitext) structure ITSELF (Stage-A LM loss on
    Wikitext text), so the frozen trunk is genuinely more useful for the Wikitext
    probe than a no-prior control trunk (Stage-A on Natural Stories, lambda=0).
    Confirm the frozen-probe AULC detects it (headstart < control, correct sign)
    at a predeclared MDE computed from this run's own seed variance (L017(3)).
    If G2 v2 FAILS -> STOP, do NOT run the science arms; report bounded/inconclusive.

  ARMS (only if G2 v2 passes) — 5 arms x >=3 seeds, frozen-probe AULC, matched budget:
    i baseline (lam=0), ii raw-RT, iii surprisal-residual [TEST], iv permuted-twin,
    v random-structured. DECISION = TRIPLE DISSOCIATION: cognition-specific positive
    requires AULC(iii) < AULC(iv) AND AULC(iii) < AULC(v), both paired CIs over seeds
    excluding 0. (iii)~=(iv) or (iii)~=(v) = negative.

Usage:
  HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_v2.py --mode g2v2
  HF_HOME=/home/centcom/data/hf-cache uv run python scripts/run_e021_v2.py --mode arms
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

import e021_targets as T
# REUSE the existing harness exactly for data prep + Stage-A co-training.
from run_e021_arms import (
    BASE, DEVICE, OUT, MAX_LEN, LAMBDA_AUX, CAPS, BYWORD, TRAIN_ITEMS,
    STAGE_A_LR, STAGE_A_BATCH, STAGE_A_STEPS,
    load_ns_stories, build_aux_batches, load_wiki_tokens, stage_a,
)

# ---- Frozen-probe Stage-B budget (matched across all arms) -----------------
PROBE_LR = 1e-3            # probe is a single linear layer -> higher lr than full-FT
PROBE_EPOCHS = 8           # passes over the capped wiki slice (matched per cap)
PROBE_BATCH = 4
PROBE_BLOCK = 256          # token window for probe training/eval
N_SLICES = 3              # disjoint cap-slices averaged per cap (variance reduction)


# ===========================================================================
# Frozen-representation linear probe
# ===========================================================================
def _hidden_states(model, ids, attn):
    """Final post-ln_f hidden states for a batch (the frozen representation)."""
    out = model(input_ids=ids, attention_mask=attn, output_hidden_states=True)
    return out.hidden_states[-1]            # (B, L, d)


def train_frozen_probe(model, probe, cap_ids, seed):
    """Freeze the trunk; train ONLY `probe` (Linear d->vocab) on a flat token slice
    for next-token prediction. Matched budget per cap. Trunk params get no grad."""
    model.eval()                            # trunk frozen (no dropout, no update)
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
                hs = _hidden_states(model, ids, attn)      # frozen rep
            logits = probe(hs)                              # (B, L, vocab) — only grad path
            labels = ids.clone()
            labels[attn == 0] = -100
            # shift for next-token
            sl = logits[:, :-1, :].reshape(-1, logits.size(-1))
            tl = labels[:, 1:].reshape(-1)
            loss = ce(sl, tl)
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(probe.parameters(), 1.0)
            opt.step()
    probe.eval()


def eval_probe_ppl(model, probe, eval_ids, block=512):
    """Held-out-domain perplexity of the frozen-trunk + trained-probe readout."""
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


def fresh_probe(state_dict, d, vocab):
    """A fresh UNTIED linear probe initialised from the frozen wte (so it starts at
    the model's own tied-head readout, then adapts to the held-out domain)."""
    probe = nn.Linear(d, vocab, bias=False).to(DEVICE)
    with torch.no_grad():
        probe.weight.copy_(state_dict["transformer.wte.weight"])
    return probe


def frozen_probe_aulc(state_dict, wiki_train, wiki_eval, seed, d, vocab):
    """For each cap, reload the frozen Stage-A trunk, train a FRESH probe on N_SLICES
    disjoint wiki slices, average held-out probe ppl. AULC = mean over caps."""
    ppls = {}
    rng = np.random.default_rng(2000 + seed)
    region = len(wiki_train) - max(CAPS) - 1
    for cap in CAPS:
        per_slice = []
        for si in range(N_SLICES):
            off = int(rng.integers(0, region))
            model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32).to(DEVICE)
            model.load_state_dict(state_dict)
            probe = fresh_probe(state_dict, d, vocab)
            train_frozen_probe(model, probe, wiki_train[off:off + cap], seed * 100 + si)
            per_slice.append(eval_probe_ppl(model, probe, wiki_eval))
            del model, probe
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
        ppls[cap] = float(np.mean(per_slice))
    aulc = float(np.mean([ppls[c] for c in CAPS]))
    return aulc, ppls


# ===========================================================================
# Stage-A variants
# ===========================================================================
def stage_a_aux_arm(target_map, lambda_aux, tokenizer, stories, seed):
    """Standard Stage-A aux co-training (the science arms + the G2 control)."""
    model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32).to(DEVICE)
    aux_examples = build_aux_batches(tokenizer, stories, target_map)
    a_logs = stage_a(model, tokenizer, aux_examples, lambda_aux, seed)
    state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    n_aux = len(aux_examples)
    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return state, a_logs, n_aux


def stage_a_headstart(tokenizer, wiki_train, seed):
    """G2 v2 PLANTED representational prior — a 'head-start' trunk. Stage-A co-trains
    the trunk on held-out-DOMAIN (Wikitext) text itself (pure LM loss, no aux head),
    matched to the same STAGE_A_STEPS/lr/batch as the aux arms. This installs a
    GENUINE wiki-relevant representational prior in the frozen trunk -> the frozen
    probe should adapt to wiki FASTER than the no-prior control. The head-start uses
    a wiki slice DISJOINT from every probe cap and from the eval block (far end)."""
    model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32).to(DEVICE)
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=STAGE_A_LR)
    # slice far from the cap region (caps draw offsets across the whole train file;
    # take a fixed contiguous block at the far end, held out from the probe caps).
    hs_slice = wiki_train[len(wiki_train) - 400000: len(wiki_train) - 100000]
    chunks = [hs_slice[i:i + MAX_LEN] for i in range(0, len(hs_slice), MAX_LEN)]
    chunks = [c for c in chunks if len(c) >= 8]
    rng = np.random.default_rng(seed)
    step = 0
    logs = []
    ce = nn.CrossEntropyLoss(ignore_index=-100)
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
            labels = ids.clone()
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
# Stats
# ===========================================================================
def paired_ci(a, b):
    """Paired diff (a - b) mean and 95% t-CI over seeds. a,b aligned by seed."""
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
    del m0

    config = {
        "base_lm": BASE, "aux_corpus": "natural_stories (10 stories)",
        "heldout_domain": "wikitext-103 (Wikipedia prose)",
        "metric": "frozen-trunk linear-probe AULC (mean held-out-domain probe ppl over caps, lower=better)",
        "stage_a_steps": STAGE_A_STEPS, "stage_a_lr": STAGE_A_LR,
        "stage_a_batch": STAGE_A_BATCH, "lambda_aux": LAMBDA_AUX,
        "caps": CAPS, "probe_lr": PROBE_LR, "probe_epochs": PROBE_EPOCHS,
        "probe_block": PROBE_BLOCK, "n_slices": N_SLICES, "seeds": args.seeds,
    }

    if args.mode == "g2v2":
        # PLANTED representational prior: head-start trunk (Stage-A on wiki text)
        # vs no-prior control (Stage-A aux arm on Natural Stories, lambda=0).
        # Expect headstart AULC < control AULC (headstart adapts to wiki faster).
        targ = T.make_targets(BYWORD, TRAIN_ITEMS, seed=0)
        ctrl_map = {(r.item, r.zone): 0.0 for r in targ.itertuples()}  # lambda=0 neutral trunk
        rows = []
        for seed in args.seeds:
            hs_state, hs_logs = stage_a_headstart(tokenizer, wiki_train, seed)
            hs_aulc, hs_ppls = frozen_probe_aulc(hs_state, wiki_train, wiki_eval, seed, d, vocab)
            del hs_state
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
            ct_state, ct_logs, _ = stage_a_aux_arm(ctrl_map, 0.0, tokenizer, stories, seed)
            ct_aulc, ct_ppls = frozen_probe_aulc(ct_state, wiki_train, wiki_eval, seed, d, vocab)
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
        m, lo, hi = paired_ci(hs_a, ct_a)              # planted effect = headstart - control
        diff = np.array(hs_a) - np.array(ct_a)
        sd = diff.std(ddof=1) if len(diff) > 1 else float("nan")
        # predeclared MDE from THIS run's own seed variance (smallest paired mean
        # whose 95% CI would exclude 0 at this n): MDE = 1.96 * sd / sqrt(n).
        mde = 1.96 * sd / math.sqrt(len(diff)) if len(diff) > 1 else float("nan")
        detected = bool(hi < 0)                        # headstart strictly better (lower AULC)
        result = {
            "mode": "g2v2", "config": config,
            "headstart_aulc_per_seed": hs_a, "control_aulc_per_seed": ct_a,
            "planted_effect_headstart_minus_control": {"mean": m, "ci": [lo, hi]},
            "paired_sd": float(sd), "MDE_predeclared": float(mde),
            "G2v2_detected": detected,
            "verdict": ("PASS — frozen-probe AULC detects the planted representational prior"
                        if detected else
                        "FAIL — planted prior not detected (or wrong sign); metric/regime cannot decide -> STOP, bounded/inconclusive"),
            "rows": rows,
        }
        with open(f"{OUT}/g2v2_frozen_probe.json", "w") as f:
            json.dump(result, f, indent=2)
        print(json.dumps({k: result[k] for k in
              ["planted_effect_headstart_minus_control", "MDE_predeclared", "G2v2_detected", "verdict"]}, indent=2))
        print(f"\nG2 v2 {'PASS' if detected else 'FAIL'} — wrote {OUT}/g2v2_frozen_probe.json")
        return

    # mode == arms (run ONLY after G2 v2 passes)
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
            if tmap is None:
                tmap = {(r.item, r.zone): 0.0 for r in targ.itertuples()}
            state, a_logs, n_aux = stage_a_aux_arm(tmap, lam, tokenizer, stories, seed)
            aulc, ppls = frozen_probe_aulc(state, wiki_train, wiki_eval, seed, d, vocab)
            del state
            if DEVICE == "cuda":
                torch.cuda.empty_cache()
            rows.append({"arm": arm, "seed": seed, "aulc": aulc, "ppls": ppls,
                         "n_aux_examples": n_aux, "stage_a_logs": a_logs})
            print(f"[seed {seed}] {arm:14s} AULC={aulc:.3f}  ppls={ppls}", flush=True)

    def arm_aulc(name):
        return [r["aulc"] for r in rows if r["arm"] == name]  # ordered by seed

    arms = ["baseline", "raw", "residual", "permuted", "random_struct"]
    means = {a: float(np.mean(arm_aulc(a))) for a in arms}
    sems = {a: float(np.std(arm_aulc(a), ddof=1) / math.sqrt(len(arm_aulc(a))))
            if len(arm_aulc(a)) > 1 else float("nan") for a in arms}
    c_iii_iv = paired_ci(arm_aulc("residual"), arm_aulc("permuted"))
    c_iii_v = paired_ci(arm_aulc("residual"), arm_aulc("random_struct"))
    c_ii_iv = paired_ci(arm_aulc("raw"), arm_aulc("permuted"))
    # cognition-specific positive: residual STRICTLY LOWER than both controls (CI upper < 0)
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
    with open(f"{OUT}/arms_v2_results.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n=== ARM frozen-probe AULC (mean +/- sem, lower=better) ===")
    for a in arms:
        print(f"  {a:14s} {means[a]:.3f} +/- {sems[a]:.3f}")
    print(f"  (iii)-(iv) residual-permuted = {c_iii_iv[0]:+.3f}  CI[{c_iii_iv[1]:+.3f},{c_iii_iv[2]:+.3f}]")
    print(f"  (iii)-(v)  residual-random   = {c_iii_v[0]:+.3f}  CI[{c_iii_v[1]:+.3f},{c_iii_v[2]:+.3f}]")
    print(f"  VERDICT: {verdict}")
    print(f"Wrote {OUT}/arms_v2_results.json")


if __name__ == "__main__":
    main()
