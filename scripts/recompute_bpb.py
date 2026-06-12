#!/usr/bin/env python3
"""I1 — recompute ONLY the bits-per-byte x-axis for the E015-expansion shards, in place.

The alignment y-axis (unique_r2_*, u_subj_mid, per_layer) is correct and independent of the bpb fix
(the eos-prepend pathology was purely on the ppl probe), so we patch bpb/ppl_token/log_bpb/diagnostics
without re-running the expensive Tuckute extraction + ridge. Fast (~probe only).

Run:  export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
      CUDA_VISIBLE_DEVICES=0 uv run python scripts/recompute_bpb.py --shards "outputs/E015_expand/shard_*.json"
"""
from __future__ import annotations
import argparse, glob, json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_ppl_alignment_law import load_wikitext_sentences
from run_ppl_alignment_law_expand import bits_per_byte
import pilot_lib as P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", default="outputs/E015_expand/shard_*.json")
    ap.add_argument("--n-ppl", type=int, default=800)
    args = ap.parse_args()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    device = P.pick_device()
    probe = load_wikitext_sentences(args.n_ppl)

    for f in sorted(glob.glob(args.shards)):
        data = json.loads(Path(f).read_text())
        for r in data["models"]:
            if "error" in r:
                continue
            name = r["model"]
            tok = AutoTokenizer.from_pretrained(name)
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            mdl = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32).to(device).eval()
            q = bits_per_byte(mdl, tok, probe, device)
            old = r.get("bpb")
            r.update({"bpb": q["bpb"], "ppl_token": q["ppl_token"], "log_bpb": math.log(q["bpb"]),
                      "n_ppl_tokens": q["n_tokens"], "n_ppl_bytes": q["n_bytes"],
                      "n_truncated": q["n_truncated"], "max_content_len": q["max_content_len"]})
            print(f"{name:>24s}: bpb {old:.3f} -> {q['bpb']:.3f}  pplT {q['ppl_token']:.1f}  "
                  f"trunc={q['n_truncated']} maxlen={q['max_content_len']}")
            del mdl
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        Path(f).write_text(json.dumps(data, indent=2))
        print(f"  patched {f}")


if __name__ == "__main__":
    main()
