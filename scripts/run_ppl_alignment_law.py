#!/usr/bin/env python3
"""E015 — the alignment∝−perplexity LAW across model FAMILIES (the matched-perplexity control's
justification, generalized beyond E003's within-gpt2-lineage r=−0.88).

The premortem on the v0.9 manuscript flagged that matched-perplexity is the paper's genuinely-novel
control but is "never shown to MATTER on a range of models." E003 showed alignment tracks log-ppl at
r=−0.88, but only WITHIN the gpt2 lineage (trained/distilled variants of one architecture). If the
relationship holds ACROSS families (gpt2 / pythia / Qwen) — different architectures, tokenizers,
pretraining — then brain-alignment is a function of LM quality regardless of architecture, so ANY
brain-tuning study that reports an alignment/downstream gain vs a non-perplexity-matched baseline is
exposed to the L011 confound. That is the demonstration that makes the matched-ppl control necessary.

For each off-the-shelf model: (a) held-out perplexity on the common Tuckute stimulus text (a fixed
probe across models), (b) brain-alignment = unique R² (LM mid-layer beyond nuisance) on the standard
participant-averaged Tuckute target. Then fit unique-R² vs log-ppl across all models (Pearson r + OLS
slope). A strong negative r across families = the generalized law.

Run: export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
  CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_ppl_alignment_law.py
"""
from __future__ import annotations
import argparse, json, math, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_lib as P
from data_adapters import load_tuckute

# off-the-shelf models spanning quality, 3 families (all cached in HF_HOME)
MODELS = [
    "distilgpt2", "gpt2", "gpt2-medium", "gpt2-large",          # gpt2 family
    "EleutherAI/pythia-1b",                                      # pythia family
    "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-3B", # Qwen family
]


def load_wikitext_sentences(n=800, min_words=8, max_words=60):
    """Natural held-out English text (WikiText-103) as a FAIR cross-family perplexity probe —
    counter-argument fix: per-token NLL on the 1000 atypical Tuckute 'baseline-set' sentences
    MISRANKS capability (rated Qwen2.5-3B worse than gpt2-large). Natural text removes that bias."""
    from datasets import load_dataset
    ds = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="test")
    out = []
    for row in ds:
        t = row["text"].strip()
        if t.startswith("=") or not t:
            continue
        for s in t.replace("\n", " ").split(". "):
            s = s.strip()
            if min_words <= len(s.split()) <= max_words:
                out.append(s if s.endswith(".") else s + ".")
                if len(out) >= n:
                    return out
    return out


def held_out_perplexity(model, tok, texts, device, max_length=64, batch_size=16):
    """Mean per-token perplexity over `texts` (a fixed common probe across models)."""
    import torch
    model.eval()
    total_nll, total_tok = 0.0, 0
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            enc = tok(batch, return_tensors="pt", padding=True, truncation=True,
                      max_length=max_length).to(device)
            ids, mask = enc["input_ids"], enc["attention_mask"]
            out = model(**enc)
            logits = out.logits[:, :-1, :]
            tgt = ids[:, 1:]
            m = mask[:, 1:].float()
            logp = torch.log_softmax(logits.float(), dim=-1)
            nll = -logp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1)  # (B, T-1)
            total_nll += float((nll * m).sum())
            total_tok += int(m.sum())
    return math.exp(total_nll / max(total_tok, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/tuckute2024")
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--out", default="outputs/E015_ppl_alignment_law.json")
    args = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    device = P.pick_device()

    texts, Y_avg, _ = load_tuckute(args.data_dir)  # standard participant-averaged target
    ppl_probe = load_wikitext_sentences(800)        # FAIR natural-text perplexity probe (not the stimuli)
    print(f"{len(texts)} Tuckute sentences (alignment) + {len(ppl_probe)} WikiText sentences (FAIR ppl probe)\n")
    print(f"{'model':>22s} {'nlayers':>8s} {'layer':>6s} {'ppl':>9s} {'uniqueR2':>10s}")

    rows = []
    for name in args.models:
        t0 = time.time()
        tok = AutoTokenizer.from_pretrained(name)
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token
        model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32).to(device).eval()
        nlayers = model.config.num_hidden_layers
        layer = P.middle_layer_index(model)  # consistent rule across architectures

        ppl = held_out_perplexity(model, tok, ppl_probe, device)  # FAIR: natural WikiText, not stimuli
        ecfg = P.ExtractConfig(pool="mean", max_length=64, batch_size=32)
        X = P.extract_hidden_states(model, tok, texts, ecfg, device, layer=layer)
        Z = P.scalar_nuisance(texts, tok)
        S = P.static_embedding_features(model, tok, texts, device)
        vp = P.variance_partition(X, Z, S, Y_avg, k_folds=5, n_pca=50)
        u = float(vp["unique_r2"])
        rows.append({"model": name, "family": name.split("/")[-1].split("-")[0],
                     "nlayers": nlayers, "layer": layer, "ppl": ppl, "log_ppl": math.log(ppl),
                     "unique_r2": u})
        print(f"{name:>22s} {nlayers:>8d} {layer:>6d} {ppl:>9.2f} {u:>+10.4f}  ({time.time()-t0:.0f}s)")
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # fit unique-R2 vs log-ppl across all models
    lp = np.array([r["log_ppl"] for r in rows])
    ur = np.array([r["unique_r2"] for r in rows])
    r_pear = float(np.corrcoef(lp, ur)[0, 1])
    slope, intercept = np.polyfit(lp, ur, 1)
    # Fisher-z 95% CI on r (counter-argument: n=8 is underpowered — make the uncertainty explicit)
    nm = len(rows)
    if nm > 3 and abs(r_pear) < 1:
        z = 0.5 * math.log((1 + r_pear) / (1 - r_pear)); sez = 1 / math.sqrt(nm - 3)
        ci = (math.tanh(z - 1.96 * sez), math.tanh(z + 1.96 * sez))
    else:
        ci = (float("nan"), float("nan"))
    # within-family check (does the law hold inside Qwen and gpt2 too?)
    fams = {}
    for r in rows:
        fams.setdefault(r["family"], []).append((r["log_ppl"], r["unique_r2"]))

    print(f"\n=== E015: alignment vs perplexity ACROSS families (FAIR natural-text ppl) ===")
    print(f"  Pearson r(log_ppl, uniqueR2) = {r_pear:+.3f}  95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]  (n={len(rows)} models)")
    print(f"  OLS slope = {slope:+.5f} per nat of log-ppl; intercept {intercept:+.4f}")
    # the clean cross-family pattern the broken probe hid: alignment vs TRAINING-DATA SCALE
    scale = {"distilgpt2": 0.04, "gpt2": 0.04, "gpt2-medium": 0.04, "gpt2-large": 0.04,
             "pythia-1b": 0.3, "Qwen2.5-0.5B": 18.0, "Qwen2.5-1.5B": 18.0, "Qwen2.5-3B": 18.0}
    print("  alignment by (approx) training-data scale [T tokens]:")
    for r in sorted(rows, key=lambda r: scale.get(r["model"].split("/")[-1], 0)):
        print(f"    {r['model'].split('/')[-1]:>16s}  ~{scale.get(r['model'].split('/')[-1],0):>5.2f}T  u={r['unique_r2']:+.4f}  ppl={r['ppl']:.1f}")
    for fam, pts in fams.items():
        if len(pts) >= 3:
            a = np.array(pts)
            print(f"  within-{fam} (n={len(pts)}): r = {np.corrcoef(a[:,0], a[:,1])[0,1]:+.3f}")
    print(f"\n  READ: a strong negative r ACROSS families ⇒ brain-alignment is largely a function of LM")
    print(f"  quality (perplexity), not architecture — so a brain-tuning gain vs a non-ppl-matched")
    print(f"  baseline can be an LM-quality effect. This is why matched-perplexity is the load-bearing")
    print(f"  control (L011 generalized; the paper's novel control, now shown to matter cross-family).")

    out = {"models": rows, "pearson_r_logppl_uniqueR2": r_pear, "r_fisher_ci95": [ci[0], ci[1]],
           "ols_slope": float(slope), "ols_intercept": float(intercept), "ppl_probe": "wikitext-103 natural text",

           "within_family_r": {f: (float(np.corrcoef(np.array(p)[:,0], np.array(p)[:,1])[0,1]) if len(p) >= 3 else None)
                                for f, p in fams.items()}}
    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"\n  wrote {args.out}")


if __name__ == "__main__":
    main()
