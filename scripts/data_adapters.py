#!/usr/bin/env python3
"""Data adapters: one interface, swappable backends.

Every backend returns the same triple so the pilot is source-agnostic:

    texts : list[str]                 # stimulus sentences/segments, in order
    fmri  : np.ndarray (n_items, V)   # response matrix, rows aligned to texts
    meta  : dict                      # provenance + any noise-ceiling info

Backends:
  * `make_synthetic_fmri` — a stand-in with KNOWN structure (a low-rank function
    of real LM features + nuisance + noise). It exists to validate the harness
    end-to-end and to prove the anti-confound partition behaves correctly. A
    positive brain-loss effect on synthetic data proves PLUMBING, not science.
  * `load_pereira` — Pereira et al. 2018 sentence-level responses (OSF crwz7).
    Small, CC-BY, no login. This is the real lightweight pilot benchmark.

Order is meaningful everywhere: contiguous splits depend on it. Do not shuffle
`texts`/`fmri` rows except inside the SGD loop (which never re-slices the data).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np


# --------------------------------------------------------------------------- #
# Synthetic stand-in
# --------------------------------------------------------------------------- #
def make_synthetic_fmri(
    base_feats: np.ndarray,
    lengths: np.ndarray,
    n_voxels: int = 200,
    signal: float = 1.0,
    nuisance_strength: float = 0.7,
    noise: float = 1.0,
    rank: int = 16,
    seed: int = 0,
) -> tuple[np.ndarray, dict]:
    """Build synthetic fMRI Y with a controllable, KNOWN decomposition.

        Y = signal * (low-rank semantic map of base_feats)
          + nuisance_strength * (length + position confound)
          + noise * N(0, 1)

    `base_feats` should be real LM hidden states for the same items, so the
    encoding model has genuine (if synthetic) structure to recover. Because both
    a semantic component AND a length/position confound are injected, the
    variance-partition test is meaningful: unique_r2 must come out BELOW raw r2.
    """
    rng = np.random.default_rng(seed)
    n = base_feats.shape[0]

    # Low-rank "semantic" signal: project features down then up through a random map.
    feats = (base_feats - base_feats.mean(0)) / (base_feats.std(0) + 1e-6)
    Wd = rng.standard_normal((feats.shape[1], rank)) / np.sqrt(feats.shape[1])
    Wu = rng.standard_normal((rank, n_voxels)) / np.sqrt(rank)
    semantic = feats @ Wd @ Wu
    semantic /= semantic.std() + 1e-6

    # Nuisance: length + position, mapped to voxels.
    position = np.arange(n, dtype=np.float64)
    nz = np.stack([(lengths - lengths.mean()) / (lengths.std() + 1e-6),
                   (position - position.mean()) / (position.std() + 1e-6)], axis=1)
    Wn = rng.standard_normal((2, n_voxels))
    nuis = nz @ Wn
    nuis /= nuis.std() + 1e-6

    eps = rng.standard_normal((n, n_voxels))
    Y = signal * semantic + nuisance_strength * nuis + noise * eps
    meta = {
        "backend": "synthetic",
        "n_items": n,
        "n_voxels": n_voxels,
        "components": {"signal": signal, "nuisance": nuisance_strength, "noise": noise, "rank": rank},
        "note": "Known-structure stand-in; validates pipeline + anti-confound, not science.",
    }
    return Y.astype(np.float32), meta


def load_sentences_txt(path: str | Path, limit: int | None = None) -> list[str]:
    """Load one-sentence-per-line stimuli (e.g. Pereira stimuli_384sentences.txt).

    Used by the hybrid path: REAL stimulus sentences paired with SYNTHETIC fMRI,
    so the harness exercises real linguistic input and is one swap away from the
    real neural responses (which align row-for-row to these same sentences)."""
    lines = [ln.strip() for ln in Path(path).read_text(errors="ignore").splitlines() if ln.strip()]
    return lines[:limit] if limit else lines


def synthetic_sentences(n: int = 240, seed: int = 0) -> list[str]:
    """Toy sentences with varied length (so the length confound is real)."""
    rng = np.random.default_rng(seed)
    subjects = ["the cat", "a scientist", "the river", "my neighbour", "the old map",
                "an engine", "the quiet child", "the distant star", "a broken clock", "the market"]
    verbs = ["found", "described", "carried", "ignored", "repaired", "measured", "remembered", "lost"]
    objs = ["a strange signal", "the warm afternoon", "several heavy boxes",
            "an unexpected result", "the narrow bridge", "two faded photographs",
            "the final answer", "a long forgotten song"]
    tails = ["", " near the harbour", " before the storm arrived",
             " while everyone else was sleeping", " in the crowded station at noon"]
    out = []
    for _ in range(n):
        s = f"{rng.choice(subjects)} {rng.choice(verbs)} {rng.choice(objs)}{rng.choice(tails)}."
        out.append(s)
    return out


# --------------------------------------------------------------------------- #
# Pereira 2018 (OSF crwz7) — sentence-level responses
# --------------------------------------------------------------------------- #
def load_pereira(
    data_dir: str | Path,
    experiment: str = "384sentences",
    subject: str | None = None,
) -> tuple[list[str], np.ndarray, dict]:
    """Load Pereira 2018 sentence-level fMRI: one averaged response vector / sentence.

    The OSF release ships per-subject MATLAB files. The widely used packaging
    (e.g. brain-score's Pereira2018) exposes, per experiment:
      * `examples`  : (n_sentences, n_voxels) response matrix
      * a sentence/key list giving the stimulus text per row
    Voxels are typically restricted to language-responsive voxels per subject.

    This loader is defensive: it searches `data_dir` for the subject's .mat file
    for the chosen experiment, reads the response matrix and the sentence text,
    and returns them aligned. Exact field names are resolved at load time and
    logged, because the OSF layout varies by mirror. Raises a clear error (rather
    than fabricating data) if the expected fields are absent — the pilot then
    falls back to the synthetic backend.
    """
    from scipy.io import loadmat

    data_dir = Path(data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"Pereira data dir not found: {data_dir}")

    # Find candidate .mat files for this experiment.
    cands = sorted(data_dir.rglob("*.mat"))
    cands = [c for c in cands if experiment.replace("sentences", "") in c.name or experiment in c.name] or cands
    if subject:
        cands = [c for c in cands if subject in str(c)] or cands
    if not cands:
        raise FileNotFoundError(f"No .mat files for experiment={experiment} under {data_dir}")

    path = cands[0]
    mat = loadmat(path, squeeze_me=True, struct_as_record=False)
    keys = [k for k in mat.keys() if not k.startswith("__")]

    # Response matrix: prefer 'examples', else the largest 2-D float array.
    Y = None
    if "examples" in mat:
        Y = np.asarray(mat["examples"], dtype=np.float32)
    else:
        best = None
        for k in keys:
            v = mat[k]
            if isinstance(v, np.ndarray) and v.ndim == 2 and np.issubdtype(v.dtype, np.number):
                if best is None or v.size > mat[best].size:
                    best = k
        if best is not None:
            Y = np.asarray(mat[best], dtype=np.float32)
    if Y is None:
        raise ValueError(f"No response matrix found in {path}; keys={keys}")

    # Sentence text: look for a sentences/keys field; else accept a sibling .txt.
    sents = None
    for k in keys:
        if "sent" in k.lower() or "key" in k.lower() or "stim" in k.lower():
            val = mat[k]
            try:
                cand = [str(s) for s in np.atleast_1d(val).ravel()]
                if len(cand) == Y.shape[0]:
                    sents = cand
                    break
            except Exception:
                continue
    if sents is None:
        txts = sorted(data_dir.rglob("*sentences*.txt")) + sorted(data_dir.rglob("*stimuli*.txt"))
        for t in txts:
            lines = [ln.strip() for ln in t.read_text(errors="ignore").splitlines() if ln.strip()]
            if len(lines) == Y.shape[0]:
                sents = lines
                break
    if sents is None:
        raise ValueError(
            f"Found responses {Y.shape} in {path} but no aligned sentence text; keys={keys}"
        )

    meta = {"backend": "pereira", "experiment": experiment, "subject": subject,
            "file": str(path), "n_items": Y.shape[0], "n_voxels": Y.shape[1], "fields": keys}
    return sents, Y, meta


# --------------------------------------------------------------------------- #
# Tuckute et al. 2024 (OSF ru38b) — sentence-level LH language-ROI responses
# --------------------------------------------------------------------------- #
# Train participants used by the paper to fit the encoding model (the 5 "train"
# UIDs; the other 5 are held-out evaluation participants). Source: the noise
# ceiling file (NC-allroi-data.csv, UIDs column) and the paper's methods.
TUCKUTE_TRAIN_UIDS = (848, 853, 865, 875, 876)

# The six LH language ROIs shipped in the public CSV. `lang_LH_netw` is the
# network mean over the five sub-ROIs; keeping it as a 7th column would double
# count, so the default voxel set is the five sub-ROIs (and `netw` is offered as
# a 1-D target for a quick scalar check).
TUCKUTE_SUBROIS = ("lang_LH_AntTemp", "lang_LH_IFG", "lang_LH_IFGorb",
                   "lang_LH_MFG", "lang_LH_PostTemp")


def load_tuckute(
    data_dir: str | Path,
    condition: str = "B",
    uids: tuple[int, ...] | None = None,
    rois: tuple[str, ...] | None = None,
    target: str = "subrois",
) -> tuple[list[str], np.ndarray, dict]:
    """Load Tuckute 2024 sentence-level fMRI: LH language-ROI BOLD per sentence.

    The public release (`data.tar` from OSF ru38b) is a long-format CSV:
    one row per (sentence x ROI x participant). `response_target` is the
    session-wise-z-scored, voxel-averaged BOLD in each ROI. We pivot it to a
    dense (n_sentences, n_roi) matrix, averaging across the chosen participants
    (default: the 5 train UIDs, matching the paper's encoding-model fit).

    This is ROI-level (coarse, 5-6 dims), not voxelwise — a documented limitation
    — but it is REAL neural data with a published noise ceiling (the synthetic
    pilot's gap, L004). Isolated sentences also sidestep the temporal-autocorr
    leakage that plagues naturalistic data (a Feghhi-relevant plus).

    `target`: "subrois" -> (n,5) matrix of the five sub-ROIs;
              "netw"    -> (n,1) the network-mean column.
    Rows are ordered by `item_id` (deterministic, contiguous-split friendly).
    """
    import pandas as pd

    data_dir = Path(data_dir)
    cands = sorted(data_dir.rglob("brain-lang-data_participant_*.csv"))
    if not cands:
        raise FileNotFoundError(
            f"Tuckute participant CSV not found under {data_dir} "
            f"(expected brain-lang-data_participant_*.csv)")
    df = pd.read_csv(cands[0])

    uids = uids or TUCKUTE_TRAIN_UIDS
    df = df[(df["cond"] == condition) & (df["target_UID"].isin(uids))]
    if df.empty:
        raise ValueError(f"No rows for cond={condition}, uids={uids} in {cands[0]}")

    if target == "netw":
        rois = ("lang_LH_netw",)
    else:
        rois = rois or TUCKUTE_SUBROIS

    # Pivot: mean response_target over participants -> (item_id x roi).
    sub = df[df["roi"].isin(rois)]
    pivot = (sub.groupby(["item_id", "roi"])["response_target"].mean()
                .unstack("roi").reindex(columns=list(rois)))
    pivot = pivot.sort_index()                      # order by item_id
    if pivot.isna().any().any():
        raise ValueError("NaNs after pivot — a sentence/ROI is missing for the chosen UIDs")

    # Sentence text per item_id (identical across participants/ROIs).
    text_map = (df.drop_duplicates("item_id").set_index("item_id")["sentence"])
    sents = [str(text_map.loc[i]) for i in pivot.index]
    Y = pivot.to_numpy(dtype=np.float32)

    # Noise ceiling for the language network, if the NC file is present.
    nc = None
    nc_files = sorted(data_dir.rglob("NC-allroi-data.csv"))
    if nc_files:
        ncdf = pd.read_csv(nc_files[0])
        row = ncdf[ncdf["roi"] == "anatglasser_LHRH_LangNetw"]
        if not row.empty:
            nc = float(row["nc"].iloc[0])

    meta = {"backend": "tuckute", "condition": condition, "uids": list(uids),
            "rois": list(rois), "file": str(cands[0]), "n_items": Y.shape[0],
            "n_voxels": Y.shape[1], "noise_ceiling_langnetw": nc}
    return sents, Y, meta
