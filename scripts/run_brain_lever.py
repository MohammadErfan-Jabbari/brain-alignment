#!/usr/bin/env python3
"""E004 — is L_brain a usable LEVER? (R03 Layer 1) + the D010 loss-form resolution.

Brain-tune a small LM with a differentiable brain-alignment loss on a held-IN
block of Tuckute stimuli; measure whether HELD-OUT unique encoding R^2 (on a
block it never optimized against) RISES vs the untuned model, under the E002
anti-confound protocol, and whether the rise survives the controls that separate
"the brain objective worked" from "any fine-tune would have done it".

Design locked in docs/experiments/E004_brain-loss-lever-test.md (two oracle
reviews; HOLD->PASS). Load-bearing choices baked in here:
  * ROTATING K=5 contiguous outer folds: tune on 4, eval unique-R^2 only on the
    held-out fold (its own internal 5-fold CV) -> every item is eval once, so the
    tune<->eval covariate shift (imageability/surprisal, verified real) averages
    out and the eval is always on never-tuned stimuli.
  * `mse` is the SINGLE predeclared confirmatory arm (theory-preferred = the
    Gaussian lower bound on conditional MI = the eval metric). cos/pearson/frozen/
    cka are EXPLORATORY (never decide the verdict; cka is negative-control-ish).
  * Controls (matched steps/lr/data/seeds/frozen-embeddings): `lm_only` (plain LM
    finetune on the same block, no brain target) and `permuted` (block-permuted
    BOLD -> a null distribution; real arm must exceed its 95th pct).
  * Input embeddings (wte/embed_tokens) FROZEN during tuning -> a lever cannot
    come from relabeling lexical vectors (the static-nuisance pathway).
  * Static nuisance S is from the UNTUNED base model, byte-identical across arms.
  * NC-normalised by the mean of the 5 functional target sub-ROI NCs (~0.491),
    NOT the anatomical 0.353 E002/E003 mislabeled with. Verdict is on raw Delta.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P  # noqa: E402
import brain_loss as BL  # noqa: E402
from data_adapters import load_tuckute, TUCKUTE_SUBROIS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CORPUS_HELDOUT = ROOT / "data/kd_corpus/wikitext103_sentences_heldout.txt"

# Per-arm lambda_brain, set by LOSS-SCALE reasoning (blind to unique-R^2), so the
# brain term is non-negligible vs CE for each form. mse runs a curve (see --lambda-grid).
ARM_LAMBDA = {"mse": 10.0, "cos": 5.0, "pearson": 50.0, "cka": 5.0, "frozen": 10.0, "contrastive": 1.0}  # verdict mse λ=10; contrastive is CE-scale → λ=1
VERDICT_LAYER = {12: 7, 24: 12, 28: 14}  # gpt2->7 (E002 peak); Qwen2.5-0.5B(24L)->12; fallback below


def verdict_layer(model) -> int:
    n = model.config.num_hidden_layers
    return VERDICT_LAYER.get(n, max(1, int(round(0.5 * n))))


def matched_nc(data_dir: str) -> float:
    """Mean noise ceiling over the 5 functional target sub-ROIs (lang_LH_*),
    the ceiling matched to the actual targets (NOT anatglasser 0.353)."""
    import pandas as pd
    ncf = sorted(Path(data_dir).rglob("NC-allroi-data.csv"))[0]
    nc = pd.read_csv(ncf)
    vals = [float(nc.loc[nc["roi"] == r, "nc"].iloc[0]) for r in TUCKUTE_SUBROIS]
    return float(np.mean(vals))


def stable_seed(*parts) -> int:
    h = hashlib.blake2s("|".join(map(str, parts)).encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(h, "little") % (2**32 - 1)


def load_covariates(data_dir: str, n_items: int) -> np.ndarray:
    """Per-item [imageability, gpt2xl-surprisal, pcfg-surprisal], item_id order —
    for the imageability-subtracted robustness sensitivity only."""
    import pandas as pd
    csv = sorted(Path(data_dir).rglob("brain-lang-data_participant_*.csv"))[0]
    df = pd.read_csv(csv)
    items = sorted(df[df["cond"] == "B"]["item_id"].unique())
    im = df.drop_duplicates("item_id").set_index("item_id")
    cols = ["rating_imageability_mean", "log-prob-gpt2-xl_mean", "log-prob-pcfg_mean"]
    C = np.stack([im.loc[items, c].to_numpy(dtype=float) for c in cols], axis=1)
    assert C.shape[0] == n_items, (C.shape, n_items)
    return C


def load_model(name: str, device: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(name).to(device)
    return model, tok


def freeze_input_embeddings(model):
    """Freeze wte/embed_tokens (review #5). On tied models the lm_head is tied to
    it and is frozen too — acceptable: only the contextual computation may move.
    (Redundant under LoRA, which freezes the whole base; kept for the --no-lora path.)"""
    model.get_input_embeddings().weight.requires_grad_(False)


def lora_targets(model_name: str):
    """Model-appropriate LoRA target modules. gpt2 uses Conv1D (c_attn/c_proj/c_fc);
    Qwen uses standard linear attention+MLP projections."""
    if "gpt2" in model_name or "distilgpt2" in model_name:
        return ["c_attn", "c_proj", "c_fc"]
    return ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def wrap_lora(model, model_name, r=16, alpha=32, dropout=0.05):
    """Wrap with LoRA adapters (base LM frozen by construction -> no catastrophic
    forgetting; perplexity stays near base). The literature regime (bilgin/merlin/
    moussa). Embeddings are frozen automatically (not a target module)."""
    from peft import LoraConfig, get_peft_model, TaskType
    cfg = LoraConfig(task_type=TaskType.CAUSAL_LM, r=r, lora_alpha=alpha,
                     lora_dropout=dropout, target_modules=lora_targets(model_name), bias="none")
    return get_peft_model(model, cfg)


def outer_folds(n: int, k: int):
    bounds = np.linspace(0, n, k + 1).astype(int)
    allidx = np.arange(n)
    for i in range(k):
        eval_idx = allidx[bounds[i]:bounds[i + 1]]
        tune_idx = np.concatenate([allidx[:bounds[i]], allidx[bounds[i + 1]:]])
        yield i, tune_idx, eval_idx


def masked_mean(hs, attn):
    import torch
    m = attn.unsqueeze(-1).float()
    return (hs * m).sum(1) / m.sum(1).clamp(min=1.0)


def brain_tune(model, tok, texts, Y, kind, lam_brain, lam_lm, layer, device,
               epochs, lr, batch_size, seed, frozen_W=None, use_lora=True,
               model_name="gpt2", lora_r=16, teacher=None, kd_temp=2.0):
    """Fine-tune `model` with lam_brain*L_brain + lam_lm*RETENTION on (texts, Y).
    RETENTION = KD KL(student‖teacher) if `teacher` given (E005 distillation setting),
    else token CE (E004 lever setting). kind=None -> retention-only (lm_only / kd_ppl).
    frozen_W -> (W,xm,xs,ym) for the frozen arm. use_lora -> LoRA (base frozen), merged before return."""
    import torch
    from torch import nn

    n_roi = Y.shape[1]
    d = model.config.hidden_size
    if use_lora:
        model = wrap_lora(model, model_name, r=lora_r)   # base + embeddings frozen
    else:
        freeze_input_embeddings(model)
    model.train()
    params = [p for p in model.parameters() if p.requires_grad]

    readout = None
    fW = None
    if kind in ("mse", "cos", "pearson", "contrastive"):
        readout = nn.Linear(d, n_roi).to(device)
        nn.init.normal_(readout.weight, std=0.02); nn.init.zeros_(readout.bias)
        params = params + list(readout.parameters())
    elif kind == "frozen":
        W, xm, xs, ym = frozen_W
        fW = {k_: torch.tensor(v, device=device) for k_, v in
              dict(W=W, xm=xm, xs=xs, ym=ym).items()}

    opt = torch.optim.AdamW(params, lr=lr)
    Yt = torch.tensor(Y, dtype=torch.float32, device=device)
    n = len(texts)
    idx = np.arange(n)
    for epoch in range(epochs):
        rng = np.random.default_rng(seed * 1000 + epoch)
        order = rng.permutation(idx)
        for start in range(0, n, batch_size):
            bidx = order[start:start + batch_size]
            batch = [texts[i] for i in bidx]
            enc = tok(batch, return_tensors="pt", padding=True, truncation=True,
                      max_length=64).to(device)
            labels = enc["input_ids"].clone()
            labels[enc["attention_mask"] == 0] = -100
            out = model(**enc, labels=labels, output_hidden_states=True)
            if teacher is not None:
                # KD: temperature-scaled KL(student‖teacher) on next-token logits, masked
                with torch.no_grad():
                    t_logits = teacher(**enc).logits
                T = kd_temp
                t_logp = torch.log_softmax(t_logits / T, dim=-1)
                s_logp = torch.log_softmax(out.logits / T, dim=-1)
                kl = (torch.exp(t_logp) * (t_logp - s_logp)).sum(-1, keepdim=True)
                tok_mask = enc["attention_mask"].unsqueeze(-1).float()
                retention = (kl * tok_mask).sum() / tok_mask.sum() * (T * T)
            else:
                retention = out.loss                          # token CE
            loss = lam_lm * retention
            if kind is not None:
                h = masked_mean(out.hidden_states[layer], enc["attention_mask"])  # (B,d)
                tgt = Yt[bidx]
                if kind in ("mse", "cos", "pearson", "contrastive"):
                    pred = readout(h)
                    bl = BL.brain_loss(kind, pred, tgt)
                elif kind == "frozen":
                    pred = ((h - fW["xm"]) / fW["xs"]) @ fW["W"] + fW["ym"]
                    bl = BL.brain_loss("frozen", pred, tgt)
                elif kind == "cka":
                    bl = BL.brain_loss("cka", h, tgt)
                loss = loss + lam_brain * bl
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
    model.eval()
    if use_lora:
        model = model.merge_and_unload()   # fold adapters into a plain model for scoring
    return model


def score_unique_r2(model, tok, texts_eval, Y_eval, Z_eval, S_eval, layer, device):
    ecfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
    X = P.extract_hidden_states(model, tok, texts_eval, ecfg, device, layer=layer)
    part = P.variance_partition(X, Z_eval, S_eval, Y_eval, k_folds=5, n_pca=50)
    return part["unique_r2"], part["unique_r2_per_fold"]


def eval_perplexity(model, tok, texts, device, max_length=64, batch_size=32):
    import torch
    model.eval()
    nll, ntok = 0.0, 0
    with torch.no_grad():
        for s in range(0, len(texts), batch_size):
            enc = tok(texts[s:s + batch_size], return_tensors="pt", padding=True,
                      truncation=True, max_length=max_length).to(device)
            logits = model(**enc).logits[:, :-1, :]
            tgt = enc["input_ids"][:, 1:]
            mask = enc["attention_mask"][:, 1:].bool()
            lp = torch.log_softmax(logits, -1).gather(-1, tgt.unsqueeze(-1)).squeeze(-1)
            nll += float((-lp[mask]).sum()); ntok += int(mask.sum())
    return float(np.exp(nll / max(ntok, 1)))


def bootstrap_ci(samples, n_boot=10000, seed=0):
    rng = np.random.default_rng(seed)
    s = np.asarray(samples, float)
    if len(s) == 0:
        return float("nan"), float("nan"), float("nan")
    bs = rng.choice(s, size=(n_boot, len(s)), replace=True).mean(1)
    return float(s.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def run_target(texts, Y, base, tok, layer, nc, cov, heldout, conditions,
               Z_all, S_all, args, kd_teacher, device, uid=None):
    """Run all folds × seeds × conditions for ONE brain target (one UID, or the
    legacy multi-UID average when uid=None). Returns (raw_rows, folds_info,
    base_by_fold). Reuses the module helpers; rows are tagged with `uid`."""
    import torch
    n = len(texts)
    raw_rows, folds_info, base_by_fold = [], {}, {}

    def aB(idx):
        return {"texts": [texts[i] for i in idx], "Y": Y[idx],
                "Z": Z_all[idx], "S": S_all[idx]}

    for fi, tune_idx, eval_idx in outer_folds(n, args.folds):
        ev = aB(eval_idx)
        if args.limit_tune:
            tune_idx = tune_idx[:args.limit_tune]
        tn = aB(tune_idx)
        bal = {c: [float(cov[tune_idx, j].mean()), float(cov[eval_idx, j].mean())]
               for j, c in enumerate(["imageability", "gpt2xl_surprisal", "pcfg_surprisal"])}
        a0, a0_folds = score_unique_r2(base, tok, ev["texts"], ev["Y"], ev["Z"], ev["S"], layer, device)
        base_by_fold[fi] = a0
        folds_info[fi] = {"n_tune": len(tune_idx), "n_eval": len(eval_idx),
                          "base_unique_r2": a0, "ab_balance": bal}
        tag_uid = "" if uid is None else f"uid{uid} "
        print(f"\n== {tag_uid}fold {fi}: tune={len(tune_idx)} eval={len(eval_idx)}  base unique_r2={a0:+.4f} "
              f"(NC {a0/nc:+.3f}) ==", flush=True)
        for seed in args.seeds:
            for tag, kind, lam, perm, null_key in conditions:
                P.set_seed(seed)
                m, _ = load_model(args.model, device)
                Ytune = tn["Y"]
                if perm is not False:
                    Ytune = BL.block_permute(tn["Y"], n_blocks=10,
                                             seed=stable_seed("brain_lever_perm", null_key, fi, seed, perm))
                frozen_W = None
                if kind == "frozen":
                    ecfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
                    Xb = P.extract_hidden_states(base, tok, tn["texts"], ecfg, device, layer=layer)
                    frozen_W = BL.fit_ridge_readout(Xb, Ytune, alpha=100.0)
                m = brain_tune(m, tok, tn["texts"], Ytune, kind, lam, args.lambda_lm,
                               layer, device, args.epochs, args.lr, args.batch_size, seed,
                               frozen_W=frozen_W, use_lora=args.use_lora,
                               model_name=args.model, lora_r=args.lora_r, teacher=kd_teacher)
                a_s, a_folds = score_unique_r2(m, tok, ev["texts"], ev["Y"], ev["Z"], ev["S"], layer, device)
                ppl = eval_perplexity(m, tok, heldout, device) if heldout else None
                raw_rows.append({"uid": uid, "fold": fi, "seed": seed, "arm": tag, "kind": kind,
                                 "is_perm": bool(perm is not False), "lambda_brain": lam,
                                 "perm_draw": None if perm is False else int(perm),
                                 "null_key": null_key,
                                 "unique_r2": a_s, "delta": a_s - a0,
                                 "nc_norm": a_s / nc, "perplexity": ppl})
                print(f"  [{tag_uid}{tag:12s} s{seed}] unique_r2={a_s:+.4f} (NC {a_s/nc:+.3f})  "
                      f"Δ={a_s - a0:+.4f}{'' if ppl is None else f'  ppl={ppl:.1f}'}", flush=True)
                del m
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
    return raw_rows, folds_info, base_by_fold


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt2")
    ap.add_argument("--arms", nargs="+",
                    default=["mse", "frozen", "lm_only", "cos", "pearson", "cka"])
    ap.add_argument("--permute-kinds", nargs="*", default=["mse", "frozen"],
                    help="kinds that get a matched permuted-fMRI null twin (brain-specificity test)")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=None, help="default 2e-4 (LoRA) / 5e-5 (full-FT)")
    ap.add_argument("--no-lora", dest="use_lora", action="store_false", help="full fine-tune instead of LoRA")
    ap.set_defaults(use_lora=True)
    ap.add_argument("--lora-r", type=int, default=16)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--lambda-lm", type=float, default=1.0)
    ap.add_argument("--lambda-grid", nargs="*", type=float, default=None,
                    help="mse-only lambda_brain curve; default single ARM_LAMBDA[mse]")
    ap.add_argument("--n-perm", type=int, default=1, help="permutation draws per (fold,seed)")
    ap.add_argument("--uids", nargs="*", type=int, default=None,
                    help="E008: run the contrast PER participant (each UID a separate target); "
                         "raw rows tagged with uid. Default None = the legacy multi-UID-average target.")
    ap.add_argument("--limit-tune", type=int, default=None, help="cap tune sentences (smoke)")
    ap.add_argument("--kd-teacher", default=None,
                    help="E005: distill from this teacher (KD KL retention instead of CE). e.g. gpt2-medium")
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.lr is None:
        args.lr = 2e-4 if args.use_lora else 5e-5

    import torch
    device = P.pick_device()
    kd_teacher = None
    if args.kd_teacher:
        kd_teacher = load_model(args.kd_teacher, device)[0].eval()
        for p in kd_teacher.parameters():
            p.requires_grad_(False)
        print(f"KD teacher: {args.kd_teacher} (retention = KL(student‖teacher))")
    nc = matched_nc(args.data_dir)
    heldout = [l for l in CORPUS_HELDOUT.read_text().splitlines() if l.strip()][:1000] \
        if CORPUS_HELDOUT.exists() else []

    # Build the list of brain targets: one per UID (E008), or the legacy multi-UID average.
    targets = []  # (uid, texts, Y)
    if args.uids:
        for uid in args.uids:
            t_u, Y_u, meta = load_tuckute(args.data_dir, uids=(uid,))
            targets.append((uid, t_u, Y_u))
        texts = targets[0][1]
        for uid, t_u, _ in targets:
            assert t_u == texts, f"texts differ for uid {uid} — per-UID item sets must match"
    else:
        texts, Y, meta = load_tuckute(args.data_dir)
        targets = [(None, texts, Y)]
    n = len(texts)
    cov = load_covariates(args.data_dir, n)
    print(f"{args.model}: Tuckute {n} items x {targets[0][2].shape[1]} ROI; matched NC={nc:.3f}; "
          f"device={device}; ppl-heldout={len(heldout)} sents; targets={len(targets)} "
          f"({'uids ' + ','.join(map(str, args.uids)) if args.uids else 'train-avg'})")

    base, tok = load_model(args.model, device)
    layer = verdict_layer(base)
    base_ppl = eval_perplexity(base, tok, heldout, device) if heldout else None
    print(f"verdict layer L{layer} (of {base.config.num_hidden_layers}); arms={args.arms}; "
          f"seeds={args.seeds}; folds={args.folds}; n_perm={args.n_perm}")

    # Fixed nuisance pieces (S from UNTUNED base, byte-identical across arms AND targets).
    Z_all = P.scalar_nuisance(texts, tok)
    S_all = P.static_embedding_features(base, tok, texts, device)

    mse_lams = args.lambda_grid if args.lambda_grid else [ARM_LAMBDA["mse"]]
    # Precompute conditions: real arms + a matched permuted-fMRI twin per permute-kind.
    # `null_key` binds real arms to their correct null. With --lambda-grid, each MSE
    # lambda needs a lambda-matched permuted twin rather than one pooled mse_perm.
    conditions = []  # (tag, kind, lambda_brain, perm, null_key)  perm: False=real, int=draw index
    for arm in args.arms:
        if arm == "lm_only":
            conditions.append(("lm_only", None, 0.0, False, "lm_only"))
        elif arm == "mse":
            for lam in mse_lams:
                key = "mse" if len(mse_lams) == 1 else f"mse_l{lam:g}"
                conditions.append((key, "mse", lam, False, key))
        else:
            conditions.append((arm, arm, ARM_LAMBDA[arm], False, arm))
    for pk in args.permute_kinds:
        if pk == "mse" and args.lambda_grid:
            perm_specs = [("mse" if len(mse_lams) == 1 else f"mse_l{lam:g}", lam) for lam in mse_lams]
        else:
            perm_specs = [(pk, ARM_LAMBDA[pk])]
        for null_key, lam in perm_specs:
            for d in range(args.n_perm):
                tag = f"{null_key}_perm" if args.n_perm == 1 else f"{null_key}_perm{d}"
                conditions.append((tag, pk, lam, d, null_key))
    print("conditions:", [c[0] for c in conditions])
    results = {"model": args.model, "layer": layer, "nc_matched": nc,
               "anat_nc_legacy": meta["noise_ceiling_langnetw"], "config": vars(args),
               "base_perplexity": base_ppl, "uids": args.uids, "folds": {}, "raw": []}

    t0 = time.time()
    base_by_fold = {}
    for uid, t_texts, Y in targets:
        rr, fi_info, bbf = run_target(t_texts, Y, base, tok, layer, nc, cov, heldout,
                                      conditions, Z_all, S_all, args, kd_teacher, device, uid=uid)
        results["raw"].extend(rr)
        key = "" if uid is None else f"uid{uid}:"
        for fk, fv in fi_info.items():
            results["folds"][f"{key}{fk}"] = fv
        base_by_fold.update({f"{key}{fk}": v for fk, v in bbf.items()})

    # ---------------- aggregate (pooled descriptive; E008 crossed inference is in analyze_e008.py) ----------------
    raw = results["raw"]
    arms_seen = sorted({r["arm"] for r in raw})
    summary = {}
    # nulls keyed by null_key: each real readout arm is tested vs ITS OWN permuted twin.
    perm_by_kind = {}
    perm_by_cell = {}
    for r in raw:
        if r["is_perm"]:
            perm_by_kind.setdefault(r.get("null_key", r["kind"]), []).append(r["delta"])
            cell = (r.get("null_key", r["kind"]), r.get("uid"), r["fold"], r["seed"])
            perm_by_cell.setdefault(cell, []).append(r["delta"])
    lmonly_by_fs = {(r.get("uid"), r["fold"], r["seed"]): r["delta"] for r in raw if r["arm"] == "lm_only"}
    for arm in arms_seen:
        rs = [r for r in raw if r["arm"] == arm]
        is_perm_arm = rs[0]["is_perm"]; kind = rs[0]["kind"]
        deltas = [r["delta"] for r in rs]
        m, lo, hi = bootstrap_ci(deltas)
        ent = {"n": len(rs), "kind": kind, "is_perm": is_perm_arm, "delta_mean": m, "delta_ci": [lo, hi],
               "unique_r2_mean": float(np.mean([r["unique_r2"] for r in rs])),
               "nc_norm_mean": float(np.mean([r["nc_norm"] for r in rs]))}
        ppls = [r["perplexity"] for r in rs if r["perplexity"] is not None]
        if ppls:
            ent["perplexity_mean"] = float(np.mean(ppls))
        if not is_perm_arm and arm != "lm_only":
            # paired vs lm_only (same fold,seed): the domain-adaptation control
            paired = [r["delta"] - lmonly_by_fs[(r.get("uid"), r["fold"], r["seed"])]
                      for r in rs if (r.get("uid"), r["fold"], r["seed"]) in lmonly_by_fs]
            if paired:
                pm, plo, phi = bootstrap_ci(paired)
                ent["vs_lm_only_mean"] = pm; ent["vs_lm_only_ci"] = [plo, phi]
            # Paired permuted-null contrast vs this arm's lambda/fold/seed-matched twin.
            null_key = rs[0].get("null_key", kind)
            if null_key in perm_by_kind:
                paired_perm = []
                for r in rs:
                    cell = (null_key, r.get("uid"), r["fold"], r["seed"])
                    if cell in perm_by_cell:
                        paired_perm.append(r["delta"] - float(np.mean(perm_by_cell[cell])))
                if paired_perm:
                    ppm, pplo, pphi = bootstrap_ci(paired_perm)
                    ent["vs_matched_perm_mean"] = ppm
                    ent["vs_matched_perm_ci"] = [pplo, pphi]
                    ent["vs_matched_perm_ci_excludes_0"] = bool(pplo > 0 or pphi < 0)
                nd = perm_by_kind[null_key]
                ent["permuted_null_p95_unpaired"] = float(np.percentile(nd, 95))
                ent["beats_permuted_null_unpaired"] = bool(m > np.percentile(nd, 95))
        summary[arm] = ent
    results["summary"] = summary
    results["permuted_null_by_kind"] = {
        k: {"n": len(v), "p95": float(np.percentile(v, 95)), "mean": float(np.mean(v))}
        for k, v in perm_by_kind.items()}

    out = args.out or f"outputs/E004_brain_lever_{args.model.replace('/', '_')}.json"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(results, indent=2))
    print(f"\n=== SUMMARY {args.model} (elapsed {time.time()-t0:.0f}s, NC={nc:.3f}) ===")
    print(f"base mean unique_r2 = {np.mean(list(base_by_fold.values())):+.4f}")
    for arm in arms_seen:
        e = summary[arm]
        extra = ""
        if "vs_lm_only_mean" in e:
            extra += f"  vs_lm_only={e['vs_lm_only_mean']:+.4f} CI[{e['vs_lm_only_ci'][0]:+.4f},{e['vs_lm_only_ci'][1]:+.4f}]"
        if "vs_matched_perm_mean" in e:
            extra += (f"  vs_perm_pair={e['vs_matched_perm_mean']:+.4f} "
                      f"CI[{e['vs_matched_perm_ci'][0]:+.4f},{e['vs_matched_perm_ci'][1]:+.4f}]")
        if "beats_permuted_null_unpaired" in e:
            extra += f"  >perm95_unpaired={e['beats_permuted_null_unpaired']}"
        if "perplexity_mean" in e:
            extra += f"  ppl={e['perplexity_mean']:.1f}"
        print(f"  {arm:12s} Δ={e['delta_mean']:+.4f} CI[{e['delta_ci'][0]:+.4f},{e['delta_ci'][1]:+.4f}] "
              f"(NC-norm uR²={e['nc_norm_mean']:+.3f}){extra}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
