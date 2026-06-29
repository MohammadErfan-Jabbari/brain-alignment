"""E024 — ZuCo 1.0 task2-NR per-word GAZE loader + sentence/label join + split-half reliability.

Substrate per the S45 converged decision (docs/experiments/E024_*.md):
ZuCo NR relation detection, GAZE-FIRST. Privileged signal = per-word eye-tracking
(FFD, GD, GPT, TRT, nFixations). We deliberately load ONLY the gaze scalars, not the
raw EEG/ET fixation timeseries (the multi-hundred-MB part), so extraction is fast.

What this produces:
  - the (sentence -> relation label) join from task_materials/relations_labels_task2.csv
  - per (subject, sentence) per-word gaze matrix  [n_words x 5]
  - per (subject, sentence) gaze summary vector   (the per-sentence PI candidate)
  - GAZE SPLIT-HALF RELIABILITY across subjects (the oracle's reliability-first gate:
    it sets the control-5 non-brain-teacher noise target and tells us whether the PI
    is reliable enough for LUPI at all). Spearman-Brown corrected, averaged over random
    subject splits.

Reference for the .mat structure (NOT imported — it uses removed-in-h5py-3 `.value`):
  data/zuco-benchmark/src/data_loading_helpers.py  (h5py 'sentenceData' layout).

ponytail: gaze scalars only; raw EEG/ET intentionally skipped (not needed for the gaze PI,
and loading it is the slow/heavy path). Add an EEG-channel loader only if the EEG-secondary
arm is actually built.
"""
from __future__ import annotations
import argparse, csv, glob, json, os, re, sys
import numpy as np
import scipy.io as sio  # ZuCo 1.0 .mat are MATLAB v5, NOT v7.3/HDF5 (verified magic bytes)

GAZE_FIELDS = ["FFD", "GD", "GPT", "TRT", "nFixations"]  # per-word eye-tracking scalars
NR_DIR = "data/zuco1/osfstorage/task2 - NR/Matlab files"
LABELS_CSV = "data/zuco1/osfstorage/task_materials/relations_labels_task2.csv"
OUT_DIR = "outputs/e024"


def norm_text(s: str) -> str:
    """Whitespace-normalized lowercased text (display / dedupe key)."""
    return re.sub(r"\s+", " ", s).strip().lower()


def loose_key(s: str) -> str:
    """Alnum-only lowercased key: robust to the .mat(ASCII hyphen) vs CSV(en-dash) and
    punctuation differences. Long sentences make this near-collision-free."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def binary_label(relation: str) -> int:
    """Best-powered primary task: 1 if the sentence asserts ANY factual relation, 0 if NO-RELATION.
    (Composite multilabels like 'AWARD;EDUCATION' are all =1.)"""
    return 0 if relation.strip().upper() == "NO-RELATION" else 1


def decode_str(h5obj) -> str:
    """MATLAB char array (uint16) -> python str (matches reference load_matlab_string)."""
    arr = np.array(h5obj).flatten()
    return "".join(chr(int(c)) for c in arr)


def load_labels(path: str):
    """relations_labels_task2.csv -> list of {sentence, paragraph_id, sentence_id, relation, control}."""
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append({
                "sentence": r["sentence"].strip(),
                "paragraph_id": r["paragraph_id"],
                "sentence_id": r["sentence_id"],
                "relation": r["relation_types"].strip(),
                "control": r.get("control", "").strip(),
            })
    return rows


def _scalar_v5(v) -> float:
    """A per-word gaze field (scipy v5) -> float; nan if empty (word not fixated)."""
    if v is None:
        return np.nan
    arr = np.atleast_1d(np.asarray(v, dtype=object)).flatten()
    if arr.size == 0:
        return np.nan
    try:
        return float(arr[0])
    except (TypeError, ValueError):
        return np.nan


def _content_str(c) -> str:
    """sentence/word .content -> str ('' if empty array)."""
    if isinstance(c, str):
        return c
    if c is None:
        return ""
    arr = np.atleast_1d(np.asarray(c)).flatten()
    return str(arr[0]) if arr.size and isinstance(arr[0], str) else ""


def extract_subject(filepath: str):
    """One subject .mat (MATLAB v5) -> {norm_content: per-word gaze matrix [n_words x 5]} + content list."""
    out = {}
    contents = []
    m = sio.loadmat(filepath, struct_as_record=False, squeeze_me=True)
    sd = np.atleast_1d(m["sentenceData"])
    for s in sd:
        content = _content_str(getattr(s, "content", None))
        if not content:
            continue
        contents.append(content)
        words = getattr(s, "word", None)
        if words is None:
            continue
        # A sentence with no word-level data squeezes to a float nan / empty array; keep only
        # real word mat_structs (Codex review: np.atleast_1d(nan) was injecting a fake all-zero
        # word -> deflating reliability for ZJS/ZPH). Skip -> leave that subj-sentence MISSING.
        words = [w for w in np.atleast_1d(words) if hasattr(w, "FFD") or hasattr(w, "content")]
        if len(words) == 0:
            continue
        mat = np.full((len(words), len(GAZE_FIELDS)), np.nan, dtype=np.float64)
        for j, w in enumerate(words):
            for k, fld in enumerate(GAZE_FIELDS):
                mat[j, k] = _scalar_v5(getattr(w, fld, None))
        out[loose_key(content)] = mat   # join key: robust to hyphen/punct differences
    return out, contents


def sentence_summary(word_mat: np.ndarray) -> np.ndarray:
    """Per-word gaze [n_words x 5] -> per-sentence PI summary vector.

    Fixated words only (a non-fixated word has nan). Features: mean of FFD/GD/GPT/TRT over
    fixated words, total TRT, mean & total nFix, fixated-word count, fixation-rate.
    Returns a fixed-length 9-vector; all-nan (no fixations) -> zeros.
    """
    ffd, gd, gpt, trt, nfix = [word_mat[:, k] for k in range(5)]
    fix_mask = ~np.isnan(ffd)
    n_words = word_mat.shape[0]
    if fix_mask.sum() == 0 or n_words == 0:
        return np.zeros(9, dtype=np.float64)

    def m(x):
        xx = x[~np.isnan(x)]
        return float(xx.mean()) if xx.size else 0.0

    def s(x):
        xx = x[~np.isnan(x)]
        return float(xx.sum()) if xx.size else 0.0

    return np.array([
        m(ffd), m(gd), m(gpt), m(trt),
        s(trt),
        m(nfix), s(nfix),
        float(fix_mask.sum()),
        float(fix_mask.sum()) / n_words,
    ], dtype=np.float64)


def spearman_brown(r: float) -> float:
    """Half-split correlation r -> full-length reliability."""
    if np.isnan(r):
        return np.nan
    denom = 1.0 + r
    return (2.0 * r) / denom if denom != 0 else np.nan


def split_half_reliability(per_subj_summ: np.ndarray, n_iter: int = 200, seed: int = 0):
    """per_subj_summ: [n_subjects x n_sentences x n_features].

    For each random half-split of subjects: average each half over subjects -> two
    [n_sentences x n_features] matrices; correlate across sentences per feature; mean
    over iterations; Spearman-Brown correct. Also reports a combined (z-scored, summed)
    reliability. Sentences with a nan in either half are dropped pairwise.
    """
    rng = np.random.default_rng(seed)
    n_subj, n_sent, n_feat = per_subj_summ.shape
    feat_rs = np.full((n_iter, n_feat), np.nan)
    comb_rs = np.full(n_iter, np.nan)
    idx = np.arange(n_subj)
    for it in range(n_iter):
        rng.shuffle(idx)
        h1, h2 = idx[: n_subj // 2], idx[n_subj // 2:]
        a = np.nanmean(per_subj_summ[h1], axis=0)  # [n_sent x n_feat]
        b = np.nanmean(per_subj_summ[h2], axis=0)
        for k in range(n_feat):
            ak, bk = a[:, k], b[:, k]
            ok = ~np.isnan(ak) & ~np.isnan(bk)
            if ok.sum() > 2 and np.std(ak[ok]) > 0 and np.std(bk[ok]) > 0:
                feat_rs[it, k] = np.corrcoef(ak[ok], bk[ok])[0, 1]
        # combined: z-score each feature across sentences then sum -> one score/sentence
        az = _zsum(a)
        bz = _zsum(b)
        ok = ~np.isnan(az) & ~np.isnan(bz)
        if ok.sum() > 2 and np.std(az[ok]) > 0 and np.std(bz[ok]) > 0:
            comb_rs[it] = np.corrcoef(az[ok], bz[ok])[0, 1]
    feat_half = np.nanmean(feat_rs, axis=0)
    comb_half = float(np.nanmean(comb_rs))
    return {
        "per_feature_halfsplit_r": dict(zip(GAZE_FIELDS_SUMMARY, [float(x) for x in feat_half])),
        "per_feature_reliability_SB": dict(zip(GAZE_FIELDS_SUMMARY, [float(spearman_brown(x)) for x in feat_half])),
        "combined_halfsplit_r": comb_half,
        "combined_reliability_SB": float(spearman_brown(comb_half)),
        "n_iter": n_iter,
    }


GAZE_FIELDS_SUMMARY = ["mFFD", "mGD", "mGPT", "mTRT", "sTRT", "mNFIX", "sNFIX", "nFixWords", "fixRate"]


def _zsum(mat):
    """[n_sent x n_feat] -> [n_sent] z-scored-then-summed, nan-safe."""
    out = np.full(mat.shape[0], np.nan)
    cols = []
    for k in range(mat.shape[1]):
        c = mat[:, k]
        mu, sd = np.nanmean(c), np.nanstd(c)
        cols.append((c - mu) / sd if sd > 0 else np.zeros_like(c))
    Z = np.vstack(cols).T
    for i in range(mat.shape[0]):
        row = Z[i]
        if not np.all(np.isnan(row)):
            out[i] = np.nansum(row)
    return out


def resolve_labels(mat_keys, labels, fuzzy_cutoff=0.93):
    """Map each .mat loose-key -> label row. Tier 1: alnum-only exact. Tier 2: guarded
    fuzzy (difflib ratio >= cutoff AND a unique best match). Returns {loose_key: label}."""
    import difflib
    exact = {loose_key(r["sentence"]): r for r in labels}
    lab_keys = list(exact.keys())
    resolved, n_exact, n_fuzzy = {}, 0, 0
    for mk in mat_keys:
        if mk in exact:
            resolved[mk] = exact[mk]; n_exact += 1
            continue
        cand = difflib.get_close_matches(mk, lab_keys, n=2, cutoff=fuzzy_cutoff)
        if len(cand) == 1 or (len(cand) >= 2 and
                              difflib.SequenceMatcher(None, mk, cand[0]).ratio()
                              - difflib.SequenceMatcher(None, mk, cand[1]).ratio() > 0.03):
            resolved[mk] = exact[cand[0]]; n_fuzzy += 1
    return resolved, n_exact, n_fuzzy


def build(subjects, labels, verbose=True):
    """Returns kept loose-keys (with labels) + per_subj_summ [n_subj x n_sent x n_feat] + diagnostics."""
    subj_data = {}
    for subj, path in subjects:
        gaze, contents = extract_subject(path)
        subj_data[subj] = gaze
        if verbose:
            print(f"  {subj}: {len(contents)} sentences in .mat, {len(gaze)} with word-gaze")
    n_subj = len(subjects)
    # union of all mat keys, resolve to labels (exact + guarded fuzzy)
    all_keys = set().union(*[set(d.keys()) for d in subj_data.values()])
    resolved, n_exact, n_fuzzy = resolve_labels(all_keys, labels)
    if verbose:
        print(f"  label join: {n_exact} exact + {n_fuzzy} fuzzy = {len(resolved)}/{len(labels)} resolved")
    # keep resolved sentences present in >= half the subjects
    keep = [k for k in resolved if sum(1 for s, _ in subjects if k in subj_data[s]) >= max(2, n_subj // 2)]
    keep.sort(key=lambda k: (str(resolved[k]["paragraph_id"]).zfill(4), str(resolved[k]["sentence_id"]).zfill(4)))
    n_sent, n_feat = len(keep), len(GAZE_FIELDS_SUMMARY)
    per_subj = np.full((n_subj, n_sent, n_feat), np.nan)
    for si, (subj, _) in enumerate(subjects):
        for ti, k in enumerate(keep):
            mat = subj_data[subj].get(k)
            if mat is not None:
                per_subj[si, ti] = sentence_summary(mat)
    kept_labels = [resolved[k] for k in keep]
    y_bin = np.array([binary_label(r["relation"]) for r in kept_labels], dtype=int)
    rel_dist = {}
    for r in kept_labels:
        rel_dist[r["relation"]] = rel_dist.get(r["relation"], 0) + 1
    diag = {
        "n_subjects": n_subj, "n_sentences_kept": n_sent,
        "label_join": {"exact": n_exact, "fuzzy": n_fuzzy, "total_resolved": len(resolved)},
        "binary_balance": {"relation(1)": int(y_bin.sum()), "no_relation(0)": int((y_bin == 0).sum())},
        "relation_distribution": rel_dist,
    }
    return keep, kept_labels, per_subj, y_bin, diag


def discover_subjects():
    paths = sorted(glob.glob(os.path.join(NR_DIR, "results*_NR.mat")))
    subs = []
    for p in paths:
        m = re.search(r"results(\w+?)_NR\.mat", os.path.basename(p))
        if m:
            subs.append((m.group(1), p))
    return subs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["one", "all"], default="one",
                    help="one = single-subject smoke test; all = full build + reliability")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        _selftest()
        return

    labels = load_labels(LABELS_CSV)
    print(f"labels: {len(labels)} sentences; relations present: "
          f"{sorted(set(r['relation'] for r in labels))}")
    subjects = discover_subjects()
    print(f"NR subjects on disk: {[s for s, _ in subjects]}")

    if args.mode == "one":
        subj, path = subjects[0]
        print(f"\n[smoke] extracting {subj} from {path} ...")
        gaze, contents = extract_subject(path)
        resolved, n_exact, n_fuzzy = resolve_labels(set(gaze.keys()), labels)
        print(f"  sentences in .mat: {len(contents)}; with word-gaze: {len(gaze)}; "
              f"label join: {n_exact} exact + {n_fuzzy} fuzzy = {len(resolved)}")
        if resolved:
            k = next(iter(resolved))
            mat = gaze[k]
            print(f"  example: {resolved[k]['sentence'][:80]!r}")
            print(f"    relation={resolved[k]['relation']}  binary={binary_label(resolved[k]['relation'])}  "
                  f"n_words={mat.shape[0]}  fixated={int((~np.isnan(mat[:,0])).sum())}")
            print(f"    summary ({GAZE_FIELDS_SUMMARY}): {np.round(sentence_summary(mat), 3).tolist()}")
        return

    # full build
    os.makedirs(OUT_DIR, exist_ok=True)
    keep, kept_labels, per_subj, y_bin, diag = build(subjects, labels)
    print(f"\nKept {diag['n_sentences_kept']} labelled sentences across {diag['n_subjects']} subjects")
    print(f"Binary balance: {diag['binary_balance']}")
    print(f"Relation distribution: {diag['relation_distribution']}")
    rel = split_half_reliability(per_subj)
    print("\n=== GAZE SPLIT-HALF RELIABILITY (Spearman-Brown corrected) ===")
    print("  combined PI vector:  half-r=%.3f  reliability=%.3f"
          % (rel["combined_halfsplit_r"], rel["combined_reliability_SB"]))
    for f_, r_ in rel["per_feature_reliability_SB"].items():
        print(f"    {f_:>10}: {r_:.3f}")
    np.savez_compressed(
        os.path.join(OUT_DIR, "zuco_nr_processed.npz"),
        per_subj_summ=per_subj,
        y_binary=y_bin,
        paragraph_ids=np.array([str(r["paragraph_id"]) for r in kept_labels], dtype=object),
        sentence_ids=np.array([str(r["sentence_id"]) for r in kept_labels], dtype=object),
        sentences=np.array(keep, dtype=object),
        relations=np.array([r["relation"] for r in kept_labels], dtype=object),
        subjects=np.array([s for s, _ in subjects], dtype=object),
        feature_names=np.array(GAZE_FIELDS_SUMMARY, dtype=object),
        sentence_texts=np.array([r["sentence"] for r in kept_labels], dtype=object),
    )
    with open(os.path.join(OUT_DIR, "zuco_nr_reliability.json"), "w") as fh:
        json.dump({"reliability": rel, "diagnostics": diag,
                   "feature_names": GAZE_FIELDS_SUMMARY}, fh, indent=2)
    print(f"\nsaved -> {OUT_DIR}/zuco_nr_processed.npz, {OUT_DIR}/zuco_nr_reliability.json")


def _selftest():
    """No-h5py logic checks: decode, summary shape/values, reliability monotonicity."""
    # decode_str
    assert decode_str(np.array([72, 105])) == "Hi"
    # sentence_summary: 3 words, 2 fixated
    wm = np.array([[100., 120., 130., 150., 1.],
                   [np.nan]*5,
                   [80., 90., 95., 110., 2.]])
    summ = sentence_summary(wm)
    assert summ.shape == (9,)
    assert abs(summ[0] - 90.0) < 1e-9        # mean FFD over fixated = (100+80)/2
    assert abs(summ[4] - 260.0) < 1e-9       # total TRT = 150+110
    assert abs(summ[7] - 2.0) < 1e-9         # 2 fixated words
    assert abs(summ[8] - 2.0/3.0) < 1e-9     # fix rate
    # all-nan sentence -> zeros
    assert np.allclose(sentence_summary(np.full((2, 5), np.nan)), 0.0)
    # reliability: identical halves -> r=1 -> SB=1; pure noise -> ~0
    rng = np.random.default_rng(1)
    signal = rng.normal(size=(8, 50, 9))
    rel_sig = split_half_reliability(signal * 0 + signal[0:1], n_iter=20)  # all subjects identical
    assert rel_sig["combined_reliability_SB"] > 0.95, rel_sig["combined_reliability_SB"]
    noise = rng.normal(size=(8, 50, 9))
    rel_noise = split_half_reliability(noise, n_iter=50)
    assert abs(rel_noise["combined_reliability_SB"]) < 0.5, rel_noise["combined_reliability_SB"]
    # spearman_brown monotone
    assert spearman_brown(0.5) > 0.5 and spearman_brown(1.0) == 1.0
    print("selftest OK")


if __name__ == "__main__":
    main()
