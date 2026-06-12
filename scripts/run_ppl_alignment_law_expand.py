#!/usr/bin/env python3
"""I1 — E015 EXPANSION: the alignment∝−(LM quality) law across ≥6 model families.

Extends scripts/run_ppl_alignment_law.py (v2, 8 models / 3 families) to ~21 models / 6 families
(adds OPT + Llama-3.2 + Mistral + full pythia/OPT scaling ladders). Single consistent code path for ALL
models (old + new): the original 8 must reproduce v2's alignment numbers (internal-consistency check).

GATED DESIGN (oracle-reviewer HOLD→PASS, fable, 2026-06-12; see E015 doc "I1 DESIGN — REVISED"):
- **x-axis = bits-per-byte** (tokenizer-independent), NOT per-token perplexity. Per-token NLL is not
  comparable across the 32k–151k vocab span and vocab correlates with family → would contaminate x.
  per-token ppl kept only for continuity. [F1, fatal]
- BOS standardized (prepend one leading token uniformly + score all content tokens), probe max_length
  raised to 160 (no truncation of ≤60-word sentences), right padding, per-model diagnostics. [F2]
- alignment extraction uses add_special_tokens=False uniformly (no-op for the original 8). [F2]
- **primary y = MIDDLE layer (0.5)**; best-layer kept as robustness only (post-hoc max = forking). [F3]
- individual-subject targets (UIDs 848/853/797) at mid-layer to guard the L016 averaging confound. [Q2]

Efficiency: ONE forward pass per model, pooling every depth-grid layer at once. Sharded by --models/--out.

Run (one shard, GPU g):
  export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
  CUDA_VISIBLE_DEVICES=g uv run python scripts/run_ppl_alignment_law_expand.py \
      --models facebook/opt-125m facebook/opt-350m --out outputs/E015_expand/shard_g.json
"""
from __future__ import annotations
import argparse, json, math, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P
from data_adapters import load_tuckute
from run_ppl_alignment_law import load_wikitext_sentences  # reuse v2's FAIR probe (L030)

DEPTH_GRID = (0.4, 0.5, 0.6, 0.7, 0.8)
SUBJECT_UIDS = (848, 837, 797)  # individual-subject control for the Q2 averaging guard (L016); all 3
#                                 have complete 1000-item coverage (853 drops 12 items → excluded)

SCALE_T = {  # approx pretraining-data scale [T tokens] — illustrative axis only (as v2)
    "distilgpt2": 0.04, "gpt2": 0.04, "gpt2-medium": 0.04, "gpt2-large": 0.04,
    "pythia-70m": 0.3, "pythia-160m": 0.3, "pythia-410m": 0.3, "pythia-1b": 0.3,
    "pythia-1.4b": 0.3, "pythia-2.8b": 0.3,
    "Qwen2.5-0.5B": 18.0, "Qwen2.5-1.5B": 18.0, "Qwen2.5-3B": 18.0, "Qwen2.5-7B": 18.0,
    "opt-125m": 0.18, "opt-350m": 0.18, "opt-1.3b": 0.18, "opt-2.7b": 0.18, "opt-6.7b": 0.18,
    "Llama-3.2-1B": 9.0, "Llama-3.2-3B": 9.0, "Mistral-7B-v0.1": 8.0,
}


def family_of(name: str) -> str:
    n = name.split("/")[-1].lower()
    if "distilgpt2" in n or n.startswith("gpt2"):
        return "gpt2"
    for fam in ("pythia", "qwen", "llama", "mistral"):
        if fam in n:
            return fam
    if n.startswith("opt"):
        return "opt"
    return n


def bits_per_byte(model, tok, texts, device, max_length=160, batch_size=16):
    """Tokenizer-INDEPENDENT LM quality: total NLL in bits / total UTF-8 bytes of the probe text [F1].
    A single leading token (bos else eos) is prepended uniformly so every content token is scored,
    making BOS handling consistent across families [F2]. Truncation at 160 never fires for <=60-word
    sentences, so probe bytes = full sentence bytes. Also returns per-token ppl (continuity only)."""
    import torch
    model.eval()
    lead_id = tok.bos_token_id if tok.bos_token_id is not None else tok.eos_token_id
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else lead_id
    total_nll_nats, total_tok, total_bytes = 0.0, 0, 0
    n_trunc, max_content_len = 0, 0  # Codex MUST-FIX guard: detect if any sentence hit the cap
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            enc = tok(batch, add_special_tokens=False, truncation=True, max_length=max_length - 1)
            content = enc["input_ids"]                       # already truncated to max_length-1
            n_trunc += sum(1 for ids in content if len(ids) >= max_length - 1)
            max_content_len = max(max_content_len, max(len(ids) for ids in content))
            seqs = [[lead_id] + ids for ids in content]
            mx = max(len(s) for s in seqs)
            input_ids = torch.full((len(seqs), mx), pad_id, dtype=torch.long)
            attn = torch.zeros((len(seqs), mx), dtype=torch.long)
            for i, s in enumerate(seqs):
                input_ids[i, :len(s)] = torch.tensor(s)
                attn[i, :len(s)] = 1
            input_ids, attn = input_ids.to(device), attn.to(device)
            out = model(input_ids=input_ids, attention_mask=attn)
            logits = out.logits[:, :-1, :]
            tgt = input_ids[:, 1:]
            m = attn[:, 1:].float()
            logp = torch.log_softmax(logits.float(), dim=-1)
            nll = -logp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1)  # (B,T-1)
            total_nll_nats += float((nll * m).sum())
            total_tok += int(m.sum())
            # Codex MUST-FIX: bytes must correspond to the SCORED tokens, not the raw sentence
            # (decode the actually-modeled content ids), so truncation can never inflate the denominator.
            total_bytes += sum(len(tok.decode(ids).encode("utf-8")) for ids in content)
    return {"bpb": (total_nll_nats / math.log(2)) / max(total_bytes, 1),
            "ppl_token": math.exp(total_nll_nats / max(total_tok, 1)),
            "n_tokens": total_tok, "n_bytes": total_bytes, "n_truncated": n_trunc,
            "max_content_len": max_content_len,
            "vocab": int(getattr(model.config, "vocab_size", len(tok))), "lead_id": int(lead_id)}


def extract_multilayer(model, tok, texts, device, layers, max_length=64, batch_size=32):
    """ONE forward pass; mean-pool over real tokens for every requested hidden-state layer.
    add_special_tokens=False uniformly [F2] (no-op for the original 8 → v2 reproduction preserved)."""
    import torch
    tok.padding_side = "right"
    model.eval()
    feats = {L: [] for L in layers}
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            enc = tok(batch, return_tensors="pt", padding=True, truncation=True,
                      max_length=max_length, add_special_tokens=False).to(device)
            out = model(**enc, output_hidden_states=True)
            mask = enc["attention_mask"].unsqueeze(-1).float()
            denom = mask.sum(dim=1).clamp(min=1.0)
            for L in layers:
                pooled = (out.hidden_states[L] * mask).sum(dim=1) / denom
                feats[L].append(pooled.float().cpu().numpy())
            del out
    return {L: np.concatenate(v, axis=0) for L, v in feats.items()}


def uniq(X, Z, S, Y):
    return float(P.variance_partition(X, Z, S, Y, k_folds=5, n_pca=50)["unique_r2"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-ppl", type=int, default=800)
    args = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    device = P.pick_device()

    texts, Y_avg, meta = load_tuckute(args.data_dir)           # standard participant-averaged target
    subj_targets = {}                                           # individual-subject control (Q2/L016)
    for uid in SUBJECT_UIDS:
        s_t, Y_s, _ = load_tuckute(args.data_dir, uids=(uid,))
        assert s_t == texts, f"subject {uid} text order differs from averaged target"
        subj_targets[uid] = Y_s
    ppl_probe = load_wikitext_sentences(args.n_ppl)             # FAIR natural-text probe (L030)
    print(f"{len(texts)} Tuckute sentences (alignment) + {len(ppl_probe)} WikiText (probe); "
          f"subjects {list(subj_targets)}\n")
    print(f"{'model':>22s} {'fam':>8s} {'params':>8s} {'vocab':>7s} {'bos':>4s} {'bpb':>6s} "
          f"{'pplT':>8s} {'L*':>4s} {'uR2mid':>9s} {'uR2*':>9s}")

    rows = []
    for name in args.models:
        t0 = time.time()
        try:
            tok = AutoTokenizer.from_pretrained(name)
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32).to(device).eval()
        except Exception as e:
            print(f"{name:>22s}  SKIP (load failed: {type(e).__name__}: {str(e)[:70]})")
            rows.append({"model": name, "error": f"{type(e).__name__}: {str(e)[:200]}"})
            continue

        nlayers = model.config.num_hidden_layers
        nparams = int(sum(p.numel() for p in model.parameters()))
        mid = P.middle_layer_index(model)
        grid = sorted({max(1, min(nlayers, round(f * nlayers))) for f in DEPTH_GRID})
        layers = sorted(set(grid) | {mid})
        adds_bos = len(tok("hello world").input_ids) - len(tok("hello world", add_special_tokens=False).input_ids)

        q = bits_per_byte(model, tok, ppl_probe, device)
        Xs = extract_multilayer(model, tok, texts, device, layers)
        Z = P.scalar_nuisance(texts, tok)
        S = P.static_embedding_features(model, tok, texts, device)
        per_layer = {int(L): uniq(Xs[L], Z, S, Y_avg) for L in layers}
        best_layer = max(grid, key=lambda L: per_layer[L])          # robustness only
        u_subj = {int(uid): uniq(Xs[mid], Z, S, Ys) for uid, Ys in subj_targets.items()}  # mid-layer

        short = name.split("/")[-1]
        rows.append({
            "model": name, "family": family_of(name), "nlayers": nlayers, "params": nparams,
            "mid_layer": int(mid), "best_layer": int(best_layer),
            "unique_r2_mid": per_layer[mid],          # PRIMARY y
            "unique_r2_best": per_layer[best_layer],  # robustness
            "u_subj_mid": u_subj,                     # Q2 individual-subject control
            "bpb": q["bpb"], "ppl_token": q["ppl_token"], "log_bpb": math.log(q["bpb"]),
            "vocab": q["vocab"], "adds_bos": adds_bos, "n_ppl_tokens": q["n_tokens"], "n_ppl_bytes": q["n_bytes"],
            "n_truncated": q["n_truncated"], "max_content_len": q["max_content_len"],
            "per_layer": per_layer, "scale_T": SCALE_T.get(short)})
        print(f"{name:>22s} {family_of(name):>8s} {nparams/1e6:>7.0f}M {q['vocab']:>7d} {adds_bos:>4d} "
              f"{q['bpb']:>6.3f} {q['ppl_token']:>8.1f} {best_layer:>4d} {per_layer[mid]:>+9.4f} "
              f"{per_layer[best_layer]:>+9.4f}  ({time.time()-t0:.0f}s)")
        del model, Xs
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps({"models": rows, "tuckute_meta": meta,
                                          "subject_uids": list(SUBJECT_UIDS)}, indent=2))
    ok = len([r for r in rows if "error" not in r])
    print(f"\n  wrote {args.out}  ({ok}/{len(rows)} ok)")


if __name__ == "__main__":
    main()
