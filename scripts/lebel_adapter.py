#!/usr/bin/env python3
"""LeBel ds003020 (UTS03) voxelwise encoding adapter — the POWERED benchmark.

Tuckute (E002/E003/E004) is a 5-ROI screen (NC~0.49). LeBel UTS03 gives ~95k
voxels of within-subject deep-sampling (27+ stories, NC by CC_norm), the powered
substrate for confirming the ~0.005 gaps and re-running the lever / headline at
voxel resolution (R03 Layer 3).

We REUSE the official pipeline (`data/paper-repos/deep-fMRI-dataset/encoding`,
the LeBel repo) for the fiddly, battle-tested parts — TextGrid parsing, word
sequences, Lanczos downsampling to TR times, FIR delays — and add the ONE custom
piece the repo lacks: per-word *contextual LM* features (their eng1000 is a
static lookup). Conventions matched to the source (verified 2026-06-11):
  * TR = 2.0045 s; simulated TR files via respdict.json (start_time=10, pad=5).
  * downsample: lanczosinterp2D(word_feats, data_times, tr_times, window=3).
  * trim + FIR: feat[10:-5] (5+trim, -trim with trim=5), zscore, make_delayed(1..4).
  * BOLD: .hf5 'data' = (TRs, voxels); trimmed [trim:-trim], zscore.
  * Story-level splits (whole stories held out) for the anti-confound — the
    contiguous-block analogue for naturalistic data (no within-story TR leakage).

LM word features (custom): each story is run through the LM in overlapping token
chunks; each word's feature is the verdict-layer hidden state at the word's final
sub-token, taken from a chunk where it has >= `min_context` tokens of left
context. This is the efficient standard (one forward per chunk, not per word).

GPU-validate `lm_word_features` before trusting any number — the CPU smoke at the
bottom of run_lebel_encoding.py checks the stimulus/BOLD/FIR/split path only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LEBEL_REF = ROOT / "data/paper-repos/deep-fMRI-dataset/encoding"
LEBEL_DIR = ROOT / "data/lebel_ds003020"
TG_DIR = LEBEL_DIR / "derivatives/TextGrids"
RESP_DIR = LEBEL_DIR / "preprocessed_data"           # /<subject>/<story>.hf5
RESPDICT = LEBEL_DIR / "derivatives/respdict.json"

sys.path.insert(0, str(LEBEL_REF))


def _ref():
    """Lazy import of the LeBel reference utils (kept off module import path)."""
    from ridge_utils.textgrid import TextGrid
    from ridge_utils.stimulus_utils import load_simulated_trfiles
    from ridge_utils.dsutils import make_word_ds
    from ridge_utils.interpdata import lanczosinterp2D
    from ridge_utils.utils import make_delayed
    return TextGrid, load_simulated_trfiles, make_word_ds, lanczosinterp2D, make_delayed


def list_stories(subject: str = "UTS03") -> list[str]:
    """Stories with BOTH a response file (subject) and a TextGrid."""
    resp = {p.stem for p in (RESP_DIR / subject).glob("*.hf5")}
    grids = {p.stem for p in TG_DIR.glob("*.TextGrid")}
    return sorted(resp & grids)


def get_wordseqs(stories: list[str]):
    """TextGrid + simulated TR files -> DataSequence per story (words, data_times, tr_times)."""
    TextGrid, load_simulated_trfiles, make_word_ds, _, _ = _ref()
    respdict = json.load(open(RESPDICT))
    grids = {st: TextGrid(open(TG_DIR / f"{st}.TextGrid").read()) for st in stories}
    trfiles = load_simulated_trfiles(respdict)
    return make_word_ds(grids, trfiles)             # dict story -> DataSequence


def load_response(story: str, subject: str = "UTS03") -> np.ndarray:
    import h5py
    with h5py.File(RESP_DIR / subject / f"{story}.hf5", "r") as h:
        return h["data"][:].astype(np.float32)       # (TRs, voxels)


def lm_word_features(model, tok, words: list[str], layer: int, device: str,
                     chunk_tokens: int = 256, stride: int = 128, min_context: int = 64,
                     pool: str = "last") -> np.ndarray:
    """Per-word contextual features at `layer`: (n_words, d_model).

    The story text = " ".join(words). We tokenize with offset mapping, map each
    word to its sub-token span, and run the LM in overlapping `chunk_tokens`
    windows (stride `stride`). A word's feature is read from the LATEST chunk in
    which it has >= `min_context` left-context tokens, pooled over its sub-tokens
    ('last' = final sub-token, the standard contextual-word-embedding choice).
    """
    import torch
    model.eval()
    # Build running text + per-word character spans (prefix a space so GPT-2 BPE
    # treats every word as word-initial, matching how it sees running text).
    text = ""
    word_char_spans = []
    for i, w in enumerate(words):
        if i > 0:
            text += " "
        start = len(text)
        text += w
        word_char_spans.append((start, len(text)))

    enc = tok(text, return_offsets_mapping=True, add_special_tokens=False)
    input_ids = enc["input_ids"]
    offsets = enc["offset_mapping"]                  # (n_tok, 2) char spans
    n_tok = len(input_ids)

    # Map each word -> list of token indices whose char span overlaps the word.
    tok_starts = np.array([o[0] for o in offsets])
    tok_ends = np.array([o[1] for o in offsets])
    word_tok_idx = []
    for (ws, we) in word_char_spans:
        idx = np.nonzero((tok_starts < we) & (tok_ends > ws))[0]
        word_tok_idx.append(idx)

    d = model.config.hidden_size
    feats = np.full((len(words), d), np.nan, dtype=np.float32)
    # token -> (feature vector, left-context length) from the best chunk seen
    tok_feat = [None] * n_tok
    tok_ctx = np.full(n_tok, -1, dtype=np.int64)
    with torch.no_grad():
        for s in range(0, n_tok, stride):
            e = min(s + chunk_tokens, n_tok)
            ids = torch.tensor([input_ids[s:e]], device=device)
            hs = model(ids, output_hidden_states=True).hidden_states[layer][0]  # (chunk, d)
            for j in range(e - s):
                gtok = s + j                          # global token index
                ctx = j                                # left-context length in this chunk
                if ctx > tok_ctx[gtok]:
                    tok_ctx[gtok] = ctx
                    tok_feat[gtok] = hs[j].float().cpu().numpy()
            if e == n_tok:
                break
    # Pool per word over its tokens (prefer tokens with enough context).
    for wi, idx in enumerate(word_tok_idx):
        if len(idx) == 0:
            continue
        if pool == "last":
            chosen = idx[-1]
            feats[wi] = tok_feat[chosen] if tok_feat[chosen] is not None else np.zeros(d, np.float32)
        else:  # mean over the word's sub-tokens
            vs = [tok_feat[t] for t in idx if tok_feat[t] is not None]
            feats[wi] = np.mean(vs, axis=0) if vs else np.zeros(d, np.float32)
    # any unfilled (shouldn't happen) -> zero
    feats[np.isnan(feats).any(1)] = 0.0
    return feats


def downsample_to_tr(word_feats: np.ndarray, ws) -> np.ndarray:
    """Lanczos-interpolate word-level features to TR times (window=3, the source default)."""
    _, _, _, lanczosinterp2D, _ = _ref()
    return lanczosinterp2D(word_feats, ws.data_times, ws.tr_times, window=3)


def build_xy(stories, model, tok, layer, subject="UTS03", trim=5, ndelays=4,
             device="cuda", **lm_kwargs):
    """Per story: LM word feats -> TR downsample -> trim[10:-5] -> zscore -> FIR(1..ndelays);
    BOLD trim[trim:-trim] -> zscore. Concatenate across stories.
    Returns X (TRs, d*ndelays), Y (TRs, voxels), story_lengths (for grouped CV)."""
    from scipy.stats import zscore
    _, _, _, _, make_delayed = _ref()
    wordseqs = get_wordseqs(stories)
    Xs, Ys, lens = [], [], []
    for st in stories:
        ws = wordseqs[st]
        wf = lm_word_features(model, tok, list(ws.data), layer, device, **lm_kwargs)
        ds = downsample_to_tr(wf, ws)                          # (n_tr, d)
        ds = zscore(ds[5 + trim:-trim], axis=0)                # feat[10:-5], matches source
        resp = load_response(st, subject)
        resp = zscore(resp[trim:-trim], axis=0)                # BOLD[trim:-trim]
        m = min(len(ds), len(resp))                            # guard off-by-one
        Xs.append(ds[:m]); Ys.append(resp[:m]); lens.append(m)
    X = make_delayed(np.nan_to_num(np.vstack(Xs)), range(1, ndelays + 1))
    Y = np.nan_to_num(np.vstack(Ys))
    return X.astype(np.float32), Y.astype(np.float32), lens
