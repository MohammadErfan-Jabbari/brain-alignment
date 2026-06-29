"""E024 — does a RICHER gaze featurization predict the binary relation label above chance?

Pre-empts the key objection to the gate's a_real~chance finding: maybe the 9-d per-sentence
SUMMARY discarded signal. Re-extract per-word gaze, build a ~35-d per-sentence featurization
(mean/std/max/min/median/p90 of each of FFD/GD/GPT/TRT/nFix over fixated words + length/fixation
descriptors), subject-average, and CV-probe the binary label with several metrics. If even this
is ~chance, gaze ⊥ relation-label is robust (not a featurization artifact).
"""
from __future__ import annotations
import sys, json, os, glob, re, argparse
import numpy as np
sys.path.insert(0, "scripts/e024")
import zuco_nr_loader as Z

TASKS = {
    "NR":  ("data/zuco1/osfstorage/task2 - NR/Matlab files",  "results*_NR.mat",  r"results(\w+?)_NR\.mat",
            "data/zuco1/osfstorage/task_materials/relations_labels_task2.csv"),
    "TSR": ("data/zuco1/osfstorage/task3 - TSR/Matlab files", "results*_TSR.mat", r"results(\w+?)_TSR\.mat",
            "data/zuco1/osfstorage/task_materials/relations_labels_task3.csv"),
}


def load_labels_tsr(csv_path):
    """TSR relations_labels_task3.csv: ';'-delimited, rows = pid;sid;sentence;relation-type
    (header mislabels it as 3 cols). relation = last field; sentence = the middle (robust to
    an embedded ';')."""
    rows = []
    lines = open(csv_path, encoding="utf-8").read().splitlines()
    for ln in lines[1:]:
        parts = ln.split(";")
        if len(parts) < 4:
            continue
        rows.append({"sentence": ";".join(parts[2:-1]).strip(),
                     "paragraph_id": parts[0], "sentence_id": parts[1],
                     "relation": parts[-1].strip(), "control": ""})
    return rows


def discover_task_subjects(mat_dir, pat, rgx):
    subs = []
    for p in sorted(glob.glob(os.path.join(mat_dir, pat))):
        m = re.search(rgx, os.path.basename(p))
        if m:
            subs.append((m.group(1), p))
    return subs


def rich_summary(word_mat):
    """[n_words x 5] -> ~35-d rich per-sentence featurization (fixated words only)."""
    feats = []
    n_words = word_mat.shape[0]
    fix = ~np.isnan(word_mat[:, 0])
    for k in range(5):
        col = word_mat[fix, k]
        col = col[~np.isnan(col)]
        if col.size == 0:
            feats += [0.0] * 6
        else:
            feats += [col.mean(), col.std(), col.max(), col.min(),
                      np.median(col), np.percentile(col, 90)]
    feats += [float(n_words), float(fix.sum()), float(fix.sum()) / max(n_words, 1),
              float(np.nansum(word_mat[:, 4])), float(np.nansum(word_mat[:, 3]))]
    return np.array(feats, dtype=np.float64)


def probe(featmat, y):
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score
    from sklearn.preprocessing import StandardScaler
    out = {}
    for name, clf_fn in [("logreg", lambda: LogisticRegression(max_iter=2000, C=1.0)),
                         ("rf", lambda: RandomForestClassifier(n_estimators=300, random_state=0))]:
        skf = StratifiedKFold(5, shuffle=True, random_state=0)
        acc, bacc, f1, auc = [], [], [], []
        for tr, te in skf.split(featmat, y):
            sc = StandardScaler().fit(featmat[tr])
            Xtr, Xte = sc.transform(featmat[tr]), sc.transform(featmat[te])
            clf = clf_fn().fit(Xtr, y[tr])
            p = clf.predict(Xte)
            acc.append(accuracy_score(y[te], p))
            bacc.append(balanced_accuracy_score(y[te], p))
            f1.append(f1_score(y[te], p, average="macro"))
            try:
                auc.append(roc_auc_score(y[te], clf.predict_proba(Xte)[:, 1]))
            except Exception:
                auc.append(float("nan"))
        out[name] = {"acc": float(np.mean(acc)), "balanced_acc": float(np.mean(bacc)),
                     "macro_f1": float(np.mean(f1)), "auc": float(np.nanmean(auc))}
    return out


def primary_relation(rel):
    """Composite multilabel (e.g. 'AWARD;EDUCATION') -> first/primary type."""
    return rel.strip().upper().split(";")[0]


def perm_auc_test(featmat, y, n_perm=500, seed=0):
    """Permutation test on binary CV-AUC: p = P(null AUC >= observed)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_auc_score
    from sklearn.preprocessing import StandardScaler
    def cv_auc(yy, rng=None):
        skf = StratifiedKFold(5, shuffle=True, random_state=0)
        aucs = []
        for tr, te in skf.split(featmat, yy):
            sc = StandardScaler().fit(featmat[tr])
            clf = LogisticRegression(max_iter=2000).fit(sc.transform(featmat[tr]), yy[tr])
            aucs.append(roc_auc_score(yy[te], clf.predict_proba(sc.transform(featmat[te]))[:, 1]))
        return float(np.mean(aucs))
    obs = cv_auc(y)
    rng = np.random.default_rng(seed)
    null = np.array([cv_auc(rng.permutation(y)) for _ in range(n_perm)])
    p = float((np.sum(null >= obs) + 1) / (n_perm + 1))
    return {"observed_auc": obs, "null_mean": float(null.mean()),
            "null_p95": float(np.percentile(null, 95)), "perm_p": p}


def probe_multiclass(featmat, rels):
    """Multiclass relation-TYPE readout (primary type, classes with n>=10): balanced-acc + macro-F1
    vs chance (majority)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import balanced_accuracy_score, f1_score
    from sklearn.preprocessing import StandardScaler
    prim = np.array([primary_relation(r) for r in rels])
    keep_cls = [c for c in set(prim) if np.sum(prim == c) >= 10]
    mask = np.isin(prim, keep_cls)
    Xm, ym = featmat[mask], prim[mask]
    classes, ym_i = np.unique(ym, return_inverse=True)
    chance = float(max(np.bincount(ym_i)) / len(ym_i))
    def cv_bacc(yy):
        skf = StratifiedKFold(5, shuffle=True, random_state=0)
        b = []
        for tr, te in skf.split(Xm, yy):
            sc = StandardScaler().fit(Xm[tr])
            clf = LogisticRegression(max_iter=2000).fit(sc.transform(Xm[tr]), yy[tr])
            b.append(balanced_accuracy_score(yy[te], clf.predict(sc.transform(Xm[te]))))
        return float(np.mean(b))
    obs = cv_bacc(ym_i)
    rng = np.random.default_rng(0)
    null = np.array([cv_bacc(rng.permutation(ym_i)) for _ in range(300)])
    perm_p = float((np.sum(null >= obs) + 1) / (len(null) + 1))
    return {"classes": list(classes), "n": int(mask.sum()),
            "chance_majority": chance, "chance_balanced": 1.0 / len(classes),
            "balanced_acc": obs, "perm_null_mean": float(null.mean()),
            "perm_null_p95": float(np.percentile(null, 95)), "perm_p": perm_p}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=["NR", "TSR"], default="NR")
    args = ap.parse_args()
    mat_dir, pat, rgx, labels_csv = TASKS[args.task]
    global OUT
    OUT = f"outputs/e024/gaze_richness_probe_{args.task}.json"
    print(f"=== TASK {args.task} ===")
    labels = Z.load_labels(labels_csv) if args.task == "NR" else load_labels_tsr(labels_csv)
    subjects = discover_task_subjects(mat_dir, pat, rgx)
    # union of mat keys -> resolve labels (reuse loader join)
    subj_rich = {}
    for subj, path in subjects:
        gaze, _ = Z.extract_subject(path)
        subj_rich[subj] = {k: rich_summary(m) for k, m in gaze.items()}
        print(f"  {subj}: {len(gaze)} sentences")
    all_keys = set().union(*[set(d.keys()) for d in subj_rich.values()])
    resolved, ne, nf = Z.resolve_labels(all_keys, labels)
    keep = [k for k in resolved if sum(1 for s, _ in subjects if k in subj_rich[s]) >= max(2, len(subjects)//2)]
    keep.sort(key=lambda k: (str(resolved[k]["paragraph_id"]).zfill(4), str(resolved[k]["sentence_id"]).zfill(4)))
    ndim = len(rich_summary(np.array([[100., 100., 100., 100., 1.]])))
    feat = np.full((len(keep), ndim), np.nan)
    for ti, k in enumerate(keep):
        stack = [subj_rich[s][k] for s, _ in subjects if k in subj_rich[s]]
        feat[ti] = np.mean(stack, axis=0)
    y = np.array([Z.binary_label(resolved[k]["relation"]) for k in keep], dtype=int)
    feat = np.nan_to_num(feat, nan=0.0)
    print(f"\nrich featurization: {feat.shape}, binary balance {np.bincount(y).tolist()}, "
          f"chance(majority)={max(np.bincount(y))/len(y):.3f}")
    res, perm = None, None
    if len(np.unique(y)) >= 2:
        res = probe(feat, y)
        print("\n=== gaze (RICH ~35-d) -> BINARY relation label, 5-fold CV ===")
        for clf, m in res.items():
            print(f"  {clf:>7}: acc={m['acc']:.3f}  bal_acc={m['balanced_acc']:.3f}  "
                  f"macroF1={m['macro_f1']:.3f}  auc={m['auc']:.3f}")
        perm = perm_auc_test(feat, y)
        print(f"  permutation AUC test: observed={perm['observed_auc']:.3f}  null_mean={perm['null_mean']:.3f}  "
              f"null_p95={perm['null_p95']:.3f}  p={perm['perm_p']:.3f}")
    else:
        print(f"\n[binary probe skipped: only one class present (balance {np.bincount(y).tolist()}) "
              f"-> task-specific reading has no NO-RELATION sentences; multiclass is the readout]")
    mc = probe_multiclass(feat, [resolved[k]["relation"] for k in keep])
    print(f"\n=== gaze (RICH ~35-d) -> MULTICLASS relation TYPE ({len(mc['classes'])} classes, n={mc['n']}) ===")
    print(f"  balanced_acc={mc['balanced_acc']:.3f}  chance(balanced)={mc['chance_balanced']:.3f}  "
          f"null_mean={mc['perm_null_mean']:.3f}  null_p95={mc['perm_null_p95']:.3f}  perm_p={mc['perm_p']:.3f}")
    os.makedirs("outputs/e024", exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump({"n": len(y), "ndim": int(ndim), "balance": np.bincount(y).tolist(),
                   "chance": float(max(np.bincount(y))/len(y)), "binary_probe": res,
                   "binary_permutation_auc": perm, "multiclass_probe": mc}, fh, indent=2)
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
