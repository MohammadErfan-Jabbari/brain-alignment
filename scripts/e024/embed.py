"""E024 — sentence embeddings from the LLM MIDDLE layer (the thesis's differentiator).

Frozen Qwen2.5-0.5B, mean-pooled hidden state at a middle layer (default 12 of 24).
This is the text-side representation the LUPI student learns on; the privileged gaze
signal shapes training only. Reads the sentence list from the Chunk-2 processed npz so
the embedding rows align 1:1 with the labels/gaze.

Output: outputs/e024/zuco_nr_embeddings.npz  (X [n_sent x hidden], layer, model, order check)
"""
from __future__ import annotations
import argparse, os
import numpy as np

OUT_DIR = "outputs/e024"
PROCESSED = os.path.join(OUT_DIR, "zuco_nr_processed.npz")
MODEL = "Qwen/Qwen2.5-0.5B"
DEFAULT_LAYER = 12


def mean_pool(hidden, mask):
    """hidden [B x T x H], mask [B x T] -> [B x H] mean over real tokens."""
    import torch
    m = mask.unsqueeze(-1).to(hidden.dtype)          # B x T x 1
    summed = (hidden * m).sum(dim=1)
    counts = m.sum(dim=1).clamp(min=1.0)
    return summed / counts


def extract(sentences, layer=DEFAULT_LAYER, batch_size=16, model_name=MODEL):
    import torch
    from transformers import AutoTokenizer, AutoModel
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name, output_hidden_states=True,
                                      torch_dtype=torch.float32)
    model.eval()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(dev)
    embs = []
    with torch.no_grad():
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            enc = tok(batch, return_tensors="pt", padding=True, truncation=True, max_length=128)
            enc = {k: v.to(dev) for k, v in enc.items()}
            out = model(**enc)
            hs = out.hidden_states[layer]            # B x T x H  (hidden_states[0] = embeddings)
            pooled = mean_pool(hs, enc["attention_mask"])
            embs.append(pooled.cpu().numpy().astype(np.float32))
    return np.concatenate(embs, axis=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", type=int, default=DEFAULT_LAYER)
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        _selftest(); return

    d = np.load(PROCESSED, allow_pickle=True)
    sentences = [str(s) for s in d["sentence_texts"]]
    print(f"extracting layer-{args.layer} embeddings for {len(sentences)} sentences ({MODEL}) ...")
    X = extract(sentences, layer=args.layer, batch_size=args.batch_size)
    print(f"embeddings: {X.shape}")
    np.savez_compressed(os.path.join(OUT_DIR, "zuco_nr_embeddings.npz"),
                        X=X, layer=args.layer, model=MODEL,
                        n_sentences=len(sentences))
    print(f"saved -> {OUT_DIR}/zuco_nr_embeddings.npz")


def _selftest():
    import torch
    # mean_pool: 1 example, 3 tokens, 2 real -> mean of first two rows
    h = torch.tensor([[[1., 1.], [3., 3.], [9., 9.]]])
    m = torch.tensor([[1., 1., 0.]])
    out = mean_pool(h, m).numpy()
    assert np.allclose(out, [[2., 2.]]), out
    # all-masked clamps to avoid div0
    out2 = mean_pool(h, torch.zeros(1, 3)).numpy()
    assert np.all(np.isfinite(out2))
    print("selftest OK")


if __name__ == "__main__":
    main()
