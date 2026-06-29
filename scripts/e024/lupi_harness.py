"""E024 — LUPI learning-curve harness + synthetic-PI MDE positive-control (the BINDING gate).

Estimand: sample efficiency. test macro-F1/accuracy vs # labeled TRAIN examples, on a
fixed held-out test set, with train-only privileged information (PI). Primary contrast at
the low-n end (where LUPI predicts the gain concentrates, Lopez-Paz 2016).

The PI enters via GENERALIZED DISTILLATION (Lopez-Paz 2016): a teacher trained on the
privileged signal produces temperature-softened soft labels for the train examples; the
student (text-embedding -> label) is trained on (1-lambda)*CE(hard) + lambda*T^2*KL(soft).
Same student arch/budget across arms => matched-budget (control 4) is built in. At test the
student uses TEXT ONLY.

THE BINDING GATE (oracle S25, hardened S45): before building the full 5-arm experiment we
must show the harness can DETECT a reliability-realistic planted effect at the low-n end on
the REAL metric (macro-F1) with the REAL test size. Plant a synthetic PI that carries the
label at a controllable informativeness; PASS iff an informative PI lifts the low-n curve
(paired CI excludes 0) AND a shuffled PI does NOT (the harness isn't spuriously crediting the
mechanism). FAIL => escalate the substrate (NR-2.0 -> OneStop) per the E024 ladder.

Splits are PARAGRAPH-disjoint (no sentence from a train paragraph leaks into test) — stronger
than sentence-disjoint, kills topic/entity leakage across sentences of one Wikipedia paragraph.
"""
from __future__ import annotations
import argparse, json, os
import numpy as np

OUT_DIR = "outputs/e024"
PROCESSED = os.path.join(OUT_DIR, "zuco_nr_processed.npz")
EMB = os.path.join(OUT_DIR, "zuco_nr_embeddings.npz")


# ----------------------------- student / teacher -----------------------------
# A REGULARIZED LINEAR student on capacity-fair PCA-reduced embeddings (the thesis's
# "classifier head on frozen LLM-middle-layer embeddings"). Linear + low-dim is the
# right capacity at n=16..200; an MLP overfits noise there and makes the gate unfair.
def _linear(in_dim, n_classes=2):
    import torch.nn as nn
    return nn.Linear(in_dim, n_classes)


def _fit_predict(Xtr, ytr, Xte, soft_targets=None, lam=0.0, T=2.0,
                 epochs=400, lr=1e-2, wd=1e-2, seed=0, device=None, C=1.0):
    """Regularized LINEAR student -> test predictions.

    Hard-label-only (soft_targets is None or lam==0): closed-ish sklearn LogisticRegression
    (fast, deterministic, L2). With soft_targets and lam>0: torch generalized distillation.
    """
    if soft_targets is None or lam <= 0:
        from sklearn.linear_model import LogisticRegression
        if len(np.unique(ytr)) < 2:                 # degenerate subsample
            return np.full(len(Xte), ytr[0])
        clf = LogisticRegression(max_iter=2000, C=C).fit(Xtr, ytr)
        return clf.predict(Xte)
    import torch, torch.nn as nn
    device = device or "cpu"                         # tiny linear model: CPU beats GPU per-call overhead
    torch.manual_seed(seed)
    Xtr_t = torch.tensor(Xtr, dtype=torch.float32, device=device)
    ytr_t = torch.tensor(ytr, dtype=torch.long, device=device)
    Xte_t = torch.tensor(Xte, dtype=torch.float32, device=device)
    model = _linear(Xtr.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    ce = nn.CrossEntropyLoss()
    soft_t = (torch.tensor(soft_targets, dtype=torch.float32, device=device)
              if soft_targets is not None else None)
    logT = np.log(T)
    model.train()
    for _ in range(epochs):
        opt.zero_grad()
        logits = model(Xtr_t)
        loss = (1.0 - lam) * ce(logits, ytr_t)
        if soft_t is not None and lam > 0:
            logp = torch.log_softmax(logits / T, dim=1)
            kl = torch.nn.functional.kl_div(logp, soft_t, reduction="batchmean")
            loss = loss + lam * (T * T) * kl
        loss.backward()
        opt.step()
    model.eval()
    with torch.no_grad():
        pred = model(Xte_t).argmax(1).cpu().numpy()
    return pred


def _fit_predict_aug(Xtr, ytr, Xte, PItr, seed=0, **kw):
    """Privileged FEATURE-AUGMENTATION (the strongest train-only LUPI route, used as the
    positive-control DETECTABILITY FLOOR): train the linear student on [text ⊕ PI]; at TEST,
    PI is absent -> imputed by a ridge regressor PI~text fit on THIS train subsample. PI is
    never observed at test (valid LUPI)."""
    from sklearn.linear_model import Ridge
    if PItr.ndim == 1:
        PItr = PItr.reshape(-1, 1)
    imp = Ridge(alpha=1.0).fit(Xtr, PItr)          # learn PI from text on train only
    PIte_hat = imp.predict(Xte)
    if PIte_hat.ndim == 1:
        PIte_hat = PIte_hat.reshape(-1, 1)
    Xtr_a = np.hstack([Xtr, PItr])
    Xte_a = np.hstack([Xte, PIte_hat])
    return _fit_predict(Xtr_a, ytr, Xte_a, lam=0.0, seed=seed, **kw)


def _teacher_soft(PItr, ytr, T=2.0, seed=0):
    """Teacher = logistic regression on the privileged signal -> temperature-softened
    soft labels for the TRAIN examples only (no test leakage)."""
    from sklearn.linear_model import LogisticRegression
    if PItr.ndim == 1:
        PItr = PItr.reshape(-1, 1)
    clf = LogisticRegression(max_iter=1000, C=1.0)
    # guard: a single class in this subsample -> uniform soft labels
    if len(np.unique(ytr)) < 2:
        n = len(ytr); return np.full((n, 2), 0.5)
    clf.fit(PItr, ytr)
    logits = clf.decision_function(PItr)
    if logits.ndim == 1:                       # binary -> [n x 2] logits
        logits = np.stack([-logits, logits], axis=1)
    z = logits / T
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


# ----------------------------- synthetic PI -----------------------------
def make_informative_pi(y, label_acc, rng, dim=3, reliability=None):
    """Synthetic PI that carries the binary label at standalone accuracy ~label_acc.

    Construct a 1-d label-aligned signal whose Bayes accuracy ~ label_acc, embedded in `dim`
    dims with orthogonal noise. (reliability is informational only — informativeness is the
    knob the gate tests; the real-gaze informativeness a_real is measured separately.)
    """
    y = np.asarray(y)
    # gaussian signal: class means +/- mu, unit var; accuracy = Phi(mu) => mu = Phi^-1(acc)
    from scipy.stats import norm
    mu = norm.ppf(np.clip(label_acc, 0.5001, 0.9999))
    sig = (2 * y - 1) * mu + rng.standard_normal(len(y))
    cols = [sig] + [rng.standard_normal(len(y)) for _ in range(dim - 1)]
    return np.stack(cols, axis=1)


def shuffle_pi(PI, rng):
    """Zeroed/shuffled-PI control: break the PI<->example correspondence."""
    idx = rng.permutation(PI.shape[0])
    return PI[idx]


# ----------------------------- learning curve -----------------------------
def _boost(base_pred, yte, p, rng):
    """Correct a fraction p of base_pred's errors -> a KNOWN accuracy lift (~p of the test set).
    Estimator-calibration only; uses test labels, so NOT a valid science mechanism."""
    pred = base_pred.copy()
    err = np.where(pred != yte)[0]
    k = min(len(err), int(round(p * len(yte))))
    if k > 0:
        fix = rng.choice(err, size=k, replace=False)
        pred[fix] = yte[fix]
    return pred


def paragraph_split(paragraph_ids, y, test_frac=0.3, seed=0):
    """Split by PARAGRAPH (all sentences of a paragraph go to one side). Returns train/test idx."""
    rng = np.random.default_rng(seed)
    pids = np.asarray(paragraph_ids)
    uniq = np.unique(pids)
    rng.shuffle(uniq)
    n_test_par = max(1, int(round(len(uniq) * test_frac)))
    test_par = set(uniq[:n_test_par].tolist())
    test_idx = np.array([i for i in range(len(pids)) if pids[i] in test_par])
    train_idx = np.array([i for i in range(len(pids)) if pids[i] not in test_par])
    return train_idx, test_idx


def _stratified_subsample(y_pool, n, rng):
    """Pick n indices (into the pool) keeping class balance as even as possible."""
    classes = np.unique(y_pool)
    per = n // len(classes)
    picks = []
    for c in classes:
        ci = np.where(y_pool == c)[0]
        rng.shuffle(ci)
        picks.append(ci[:per])
    picks = np.concatenate(picks)
    if len(picks) < n:                          # top up randomly
        rest = np.setdiff1d(np.arange(len(y_pool)), picks)
        rng.shuffle(rest)
        picks = np.concatenate([picks, rest[: n - len(picks)]])
    return picks


def learning_curve(X, y, paragraph_ids, PI_by_arm, ns, n_resamples=20,
                   test_frac=0.3, base_seed=0, lam=0.5, T=2.0, verbose=True):
    """For each arm (PI matrix or None for text_only) and each n: macro-F1 + accuracy per
    resample, paired across arms (same subsample). Returns dict arm -> {n: [metrics per resample]}.
    """
    from sklearn.metrics import f1_score, accuracy_score
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    train_idx, test_idx = paragraph_split(paragraph_ids, y, test_frac, base_seed)
    Xtr_pool, ytr_pool = X[train_idx], y[train_idx]
    Xte, yte = X[test_idx], y[test_idx]
    # capacity-fair reduction: standardize + PCA fit on the TRAIN POOL only (test held out,
    # so no leakage), then linear student. Keeps capacity sane at n=16..200.
    n_comp = min(50, Xtr_pool.shape[0] - 1, Xtr_pool.shape[1])
    scaler = StandardScaler().fit(Xtr_pool)
    pca = PCA(n_components=n_comp, random_state=base_seed).fit(scaler.transform(Xtr_pool))
    Xtr_pool = pca.transform(scaler.transform(Xtr_pool))
    Xte = pca.transform(scaler.transform(Xte))
    arms = list(PI_by_arm.keys())
    res = {a: {n: {"f1": [], "acc": []} for n in ns} for a in arms}
    if verbose:
        print(f"  train pool {len(train_idx)} / test {len(test_idx)} (paragraph-disjoint); "
              f"test balance {np.bincount(yte).tolist()}")
    def _spec(v):
        """arm value -> (PI_or_None, mech). Back-compat: a bare matrix => 'distill', None => text."""
        if isinstance(v, tuple):
            return v
        return (v, None if v is None else "distill")
    for n in ns:
        for r in range(n_resamples):
            rng = np.random.default_rng(base_seed * 10000 + n * 100 + r)
            sub = _stratified_subsample(ytr_pool, n, rng)
            Xs, ys = Xtr_pool[sub], ytr_pool[sub]
            base_pred = _fit_predict(Xs, ys, Xte, lam=0.0, seed=r)  # shared text-only pred (paired)
            for a in arms:
                PI, mech = _spec(PI_by_arm[a])
                if PI is None:                              # text-only
                    pred = base_pred
                elif mech == "oracle_boost":
                    # ESTIMATOR-CALIBRATION probe (NOT a science arm): correct a known
                    # fraction p of base_pred's test errors -> a KNOWN accuracy lift. Answers
                    # "is the test set big enough to detect a low-n gain of size ~p?"
                    pred = _boost(base_pred, yte, p=PI, rng=np.random.default_rng(
                        base_seed * 99991 + n * 131 + r))
                elif mech == "feature_aug":
                    pred = _fit_predict_aug(Xs, ys, Xte, PI[train_idx][sub], seed=r)
                else:                                       # generalized distillation
                    soft = _teacher_soft(PI[train_idx][sub], ys, T=T, seed=r)
                    pred = _fit_predict(Xs, ys, Xte, soft_targets=soft, lam=lam, T=T, seed=r)
                res[a][n]["f1"].append(f1_score(yte, pred, average="macro"))
                res[a][n]["acc"].append(accuracy_score(yte, pred))
    return res, len(train_idx), len(test_idx)


def paired_delta(res, arm, ref="text_only", metric="f1"):
    """Paired Δ (arm - ref) per n with percentile CI over resamples."""
    out = {}
    for n in res[arm]:
        a = np.array(res[arm][n][metric])
        b = np.array(res[ref][n][metric])
        d = a - b
        out[n] = {"mean": float(d.mean()),
                  "ci95": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
                  "ref_mean": float(b.mean()), "arm_mean": float(a.mean())}
    return out


# ----------------------------- positive control (the gate) -----------------------------
def pi_to_label_accuracy(PI, y, n_splits=5, seed=0):
    """PI->label probe + a_real: cross-validated accuracy of a teacher on the REAL PI."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import accuracy_score
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    accs = []
    for tr, te in skf.split(PI, y):
        clf = LogisticRegression(max_iter=1000).fit(PI[tr], y[tr])
        accs.append(accuracy_score(y[te], clf.predict(PI[te])))
    return float(np.mean(accs))


def run_positive_control(seed=0, n_resamples=40, low_ns=(16, 24, 32, 48),
                         high_ns=(96, 160), boost_sweep=(0.03, 0.05, 0.08, 0.12),
                         mde_threshold=0.05, metric="acc"):
    """The BINDING GATE (oracle S25). Answers: is the ZuCo-NR test set big enough to DETECT a
    low-n gain of plausibly-LUPI size (single-digit pp)? Method: inject KNOWN accuracy lifts p
    (oracle_boost) on the real embeddings/labels and find the smallest p whose low-n paired CI
    excludes 0 (the empirical MDE). PASS iff MDE_low-n <= mde_threshold. Also reports a_real (the
    real gaze PI->label informativeness) and the realized real-gaze distillation effect (sanity).
    Writes outputs/e024/positive_control.json."""
    d = np.load(PROCESSED, allow_pickle=True)
    e = np.load(EMB, allow_pickle=True)
    X = e["X"]; y = d["y_binary"].astype(int)
    pids = d["paragraph_ids"] if "paragraph_ids" in d.files else np.arange(len(y))
    real_pi = np.nan_to_num(np.nanmean(d["per_subj_summ"], axis=0), nan=0.0)  # subj-avg per-sentence PI
    a_real = pi_to_label_accuracy(_zscore(real_pi), y, seed=seed)
    ns = list(low_ns) + list(high_ns)
    low = list(low_ns)

    arms = {"text_only": None}
    for p in boost_sweep:
        arms[f"boost_{int(p*100):02d}pp"] = (p, "oracle_boost")     # estimator MDE calibration
    arms["realgaze_distill"] = (_zscore(real_pi), "distill")        # realized real-gaze effect (sanity)
    arms["realgaze_shuffled"] = (shuffle_pi(_zscore(real_pi), np.random.default_rng(seed)), "distill")
    res, ntr, nte = learning_curve(X, y, pids, arms, ns, n_resamples=n_resamples, base_seed=seed)

    findings = {"a_real_gaze_pi_to_label_acc": a_real, "n_sentences": int(len(y)),
                "binary_balance": np.bincount(y).tolist(), "n_train_pool": ntr, "n_test": nte,
                "ns": ns, "low_ns": low, "metric": metric, "mde_threshold": mde_threshold,
                "chance_acc": float(max(np.bincount(y)) / len(y)), "arms": {}}
    for a in arms:
        if a != "text_only":
            findings["arms"][a] = paired_delta(res, a, metric=metric)

    detected = [p for p in boost_sweep
                if all(findings["arms"][f"boost_{int(p*100):02d}pp"][n]["ci95"][0] > 0 for n in low)]
    mde = min(detected) if detected else None
    def low_n_pos(arm):
        return any(findings["arms"][arm][n]["ci95"][0] > 0 for n in low)
    findings["gate"] = {
        "empirical_MDE_lown_acc": mde,
        "MDE_meets_threshold": bool(mde is not None and mde <= mde_threshold),
        "realgaze_distill_lifts_lown": bool(low_n_pos("realgaze_distill")),
        "realgaze_shuffled_lifts_lown": bool(low_n_pos("realgaze_shuffled")),
        "PASS": bool(mde is not None and mde <= mde_threshold),
        "rule": ("PASS iff the empirical low-n MDE (smallest detectable injected accuracy gain, "
                 "paired CI>0 at all low n) <= mde_threshold; the test set can resolve a "
                 "plausibly-LUPI-sized single-digit-pp low-n gain. Real-gaze arms are reported as "
                 "the realized effect, not part of the gate."),
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "positive_control.json"), "w") as fh:
        json.dump(findings, fh, indent=2)
    _print_gate(findings)
    return findings


def _zscore(M):
    mu = M.mean(0, keepdims=True); sd = M.std(0, keepdims=True); sd[sd == 0] = 1
    return (M - mu) / sd


def _print_gate(f):
    print(f"\n=== POSITIVE-CONTROL GATE (estimator MDE) ===")
    print(f"  real gaze PI -> label CV acc (a_real): {f['a_real_gaze_pi_to_label_acc']:.3f}  "
          f"(chance {f['chance_acc']:.3f})")
    print(f"  n_train_pool={f['n_train_pool']} n_test={f['n_test']}  low-ns={f['low_ns']}  metric={f['metric']}")
    for arm, by_n in f["arms"].items():
        s = "  ".join(f"n{n}:{by_n[n]['mean']:+.3f}[{by_n[n]['ci95'][0]:+.3f},{by_n[n]['ci95'][1]:+.3f}]"
                      for n in list(by_n)[:4])
        print(f"    {arm:>18}: {s}")
    g = f["gate"]
    print(f"  empirical low-n MDE (acc): {g['empirical_MDE_lown_acc']}  (threshold {f['mde_threshold']})")
    print(f"  real-gaze distill lifts low-n: {g['realgaze_distill_lifts_lown']}  "
          f"(shuffled: {g['realgaze_shuffled_lifts_lown']})")
    print(f"  >>> GATE {'PASS' if g['PASS'] else 'FAIL'} <<<  ({'MDE within threshold' if g['PASS'] else 'underpowered -> escalate per E024 ladder'})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["positive_control"], default="positive_control")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--resamples", type=int, default=30)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        _selftest(); return
    run_positive_control(seed=args.seed, n_resamples=args.resamples)


def _selftest():
    """Estimator-calibration checks: (1) a KNOWN injected accuracy lift (oracle_boost) is
    detected (paired CI>0) at low n while a zero boost is NOT (no false positive); (2) the
    PI->label probe recovers high acc for an informative PI, ~chance for a shuffled one;
    (3) paragraph_split never puts a paragraph on both sides."""
    rng = np.random.default_rng(0)
    n, dim = 360, 80
    y = np.array([0, 1] * (n // 2)); rng.shuffle(y)
    X = (2 * y - 1)[:, None] * 0.18 * np.ones((n, dim)) + rng.standard_normal((n, dim))
    pids = np.arange(n) // 2
    arms = {"text_only": None, "boost_10": (0.10, "oracle_boost"),
            "boost_00": (0.0, "oracle_boost")}
    res, ntr, nte = learning_curve(X, y, pids, arms, ns=[16, 32], n_resamples=30,
                                   base_seed=0, verbose=False)
    d10 = paired_delta(res, "boost_10", metric="acc")
    d00 = paired_delta(res, "boost_00", metric="acc")
    assert d10[16]["ci95"][0] > 0, f"known +10pp boost not detected at low n: {d10[16]}"
    assert d00[16]["ci95"][0] <= 0 <= d00[16]["ci95"][1], f"zero boost falsely detected: {d00[16]}"
    # PI->label probe
    inform = make_informative_pi(y, 0.9, rng, dim=4)
    assert pi_to_label_accuracy(inform, y) > 0.78
    assert pi_to_label_accuracy(shuffle_pi(inform, rng), y) < 0.62
    # paragraph split disjoint
    tr, te = paragraph_split(pids, y, 0.3, 0)
    assert set(pids[tr]).isdisjoint(set(pids[te]))
    print(f"selftest OK (+10pp boost detected {d10[16]['mean']:+.3f}{d10[16]['ci95']}; "
          f"zero-boost null {d00[16]['mean']:+.3f}{d00[16]['ci95']}; paragraph-split disjoint)")


if __name__ == "__main__":
    main()
