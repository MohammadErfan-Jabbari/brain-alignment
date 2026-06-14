#!/usr/bin/env python3
"""E020 diagnostic — is the story_11 A_resd=+0.090 a REAL non-stimulus signal (Fork-A) or an ARTIFACT?
(thesis venv). Run after run_eys_ceiling.py flagged A_resid positive.

Three decisive diagnostics separate the candidate explanations:
  (A) REFERENCE-QUALITY SCALING. eps_s = Y_s - E[Y|S]_{-s}; at n=5 the LOO mean is a poor E[Y|S] estimate
      (ref-rel +0.33), so stimulus-evoked signal LEAKS into eps and a stimulus-locked LM aligns to it
      (the L016/L035 confound displaced into the residual; first-principles eta-leak). PREDICTION if
      eta-leak: A_resid DECREASES as the reference improves (more subjects in the mean). If real
      non-stimulus signal: A_resid is flat in k.
  (B) NUISANCE-PARTIAL. Residualize eps_s on the STRONG stimulus nuisance (rate+artic+eng1000-PCA), then
      LM -> (eps residual). PREDICTION if leaked-stimulus: A_resid collapses to ~0 after partialling the
      stimulus out. If real: it survives.
  (C) FOLD-GAP (C2). Contiguous-fold ridge w/o gaps lets HRF autocorrelation + FIR overlap leak train->test
      (untrained A_resid was +0.033 despite untrained A_shared~0 — an autocorrelation signature, NOT
      stimulus encoding). Re-run A_resid with NDELAYS-TR gaps dropped around each fold boundary. PREDICTION
      if autocorr-inflation: A_resid shrinks (esp. the untrained baseline) with gaps.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "data/paper-repos/deep-fMRI-dataset/encoding"))
import run_tribe_fidelity as F  # noqa: E402
from run_tribe_ceiling import lm_grid, MODEL, UNTRAINED_SEEDS  # noqa: E402
from run_eys_ceiling import load_real_reps, loo_mean, HL  # noqa: E402

OUT = ROOT / "outputs/E020_eys"
NDELAYS = F.NDELAYS


def ridge_pred_gap(X, Y, gap=0, alphas=(1.0, 1e1, 1e2, 1e3, 1e4)):
    """Contiguous-fold ridge with optional fold-boundary GAP (drop `gap` TRs adjacent to each test fold
    from the TRAIN set) to kill HRF-autocorrelation/FIR leakage. gap=0 == F.ridge_cv_pred."""
    Y2 = Y if Y.ndim == 2 else Y[:, None]
    T = X.shape[0]; folds = np.array_split(np.arange(T), F.NFOLDS)
    best = (-2.0, None)
    for a in alphas:
        pred = np.zeros_like(Y2)
        for te in folds:
            lo, hi = te[0], te[-1]
            trn = np.setdiff1d(np.arange(T), np.arange(max(0, lo - gap), min(T, hi + 1 + gap)))
            mx, my = X[trn].mean(0), Y2[trn].mean(0)
            Xtr, Ytr = X[trn] - mx, Y2[trn] - my
            B = np.linalg.solve(Xtr.T @ Xtr + a * np.eye(X.shape[1]), Xtr.T @ Ytr)
            pred[te] = (X[te] - mx) @ B + my
        m = float(np.nanmean(F._percol_corr(pred, Y2)))
        if m > best[0]: best = (m, pred)
    return best[1]


def encode_mean(X, target, hl, gap=0):
    return float(np.nanmean(F._percol_corr(ridge_pred_gap(X, target, gap), target)[hl]))


def run():
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    subs = F.DENIZ_SUBJECTS
    nlayers = AutoConfig.from_pretrained(MODEL).num_hidden_layers
    layer = {12: 7, 24: 12, 28: 14}.get(nlayers, max(1, nlayers // 2))
    tok = AutoTokenizer.from_pretrained(MODEL); tok.pad_token = tok.pad_token or tok.eos_token

    r0, r1, ncs, roisets = {}, {}, {}, {}
    for s in subs:
        r0[s], r1[s], ncs[s] = load_real_reps(s)
        roisets[s] = F.load_roi_masks_fsa5(s, sum(F.ROI_GROUPS.values(), []))
    Ymean = {s: ((r0[s] + r1[s]) / 2).astype(np.float32) for s in subs}
    ncgroup = np.mean([ncs[s] for s in subs], 0)
    grp_roi = {g: (np.mean([F._anyroi(roisets[s], names) for s in subs], 0) >= 0.5)
               for g, names in F.ROI_GROUPS.items()}
    hl = grp_roi[HL] & (ncgroup > F.NC_MIN)
    Xnuis = F.lowlevel_design(strong=True)

    def lm_feats(model):
        return lm_grid(model, tok, layer, device)

    print("== trained LM features ==");
    mt = AutoModelForCausalLM.from_pretrained(MODEL).to(device).eval()
    LM_t = lm_feats(mt); del mt; torch.cuda.empty_cache()
    LM_u = []
    for sd in UNTRAINED_SEEDS:
        torch.manual_seed(sd); cfg = AutoConfig.from_pretrained(MODEL); torch.manual_seed(sd)
        mu = AutoModelForCausalLM.from_config(cfg).to(device).eval()
        LM_u.append(lm_feats(mu)); del mu; torch.cuda.empty_cache()

    out = {"layer": layer}

    # ---------- (A) reference-quality scaling: A_resid vs k subjects in E[Y|S]_{-s} ----------
    # For each held-out subject s, build the reference from k of the OTHER 5; eps = Y_s - ref. Average over s.
    print("\n=== (A) reference-quality scaling (A_resid vs #subjects in E[Y|S]) ===")
    scaling = {}
    for k in [1, 2, 3, 5]:
        a_t, a_u = [], []
        refrel = []
        for s in subs:
            others = [x for x in subs if x != s]
            ref = np.mean([Ymean[x] for x in others[:k]], 0).astype(np.float32)
            eps = (Ymean[s] - ref).astype(np.float32)
            a_t.append(encode_mean(LM_t, eps, hl))
            a_u.append(np.mean([encode_mean(lu, eps, hl) for lu in LM_u]))
            if k >= 2:  # split-half reliability of the k-subject reference
                h = k // 2
                refrel.append(float(np.nanmean(_shr(np.mean([Ymean[x] for x in others[:h]],0),
                                                     np.mean([Ymean[x] for x in others[h:k]],0))[hl])))
        scaling[k] = {"A_resid_trained": round(float(np.mean(a_t)), 4),
                      "A_resid_untrained": round(float(np.mean(a_u)), 4),
                      "gap": round(float(np.mean(a_t) - np.mean(a_u)), 4),
                      "ref_reliability": round(float(np.mean(refrel)), 4) if refrel else None}
        print(f"  k={k}: A_resid trained={scaling[k]['A_resid_trained']:+.3f} "
              f"untrained={scaling[k]['A_resid_untrained']:+.3f} gap={scaling[k]['gap']:+.3f} "
              f"ref-rel={scaling[k]['ref_reliability']}")
    out["reference_scaling"] = scaling

    # ---------- (B) nuisance-partial: LM -> (eps residualized on stimulus nuisance) ----------
    print("\n=== (B) nuisance-partial (does A_resid survive removing stimulus structure from eps?) ===")
    a_t_raw, a_t_par, a_u_par = [], [], []
    for s in subs:
        eps = (Ymean[s] - loo_mean(Ymean, subs, s)).astype(np.float32)
        nuis_pred = ridge_pred_gap(Xnuis, eps)           # stimulus-nuisance explanation of eps
        eps_par = (eps - nuis_pred).astype(np.float32)   # eps with stimulus structure removed
        a_t_raw.append(encode_mean(LM_t, eps, hl))
        a_t_par.append(encode_mean(LM_t, eps_par, hl))
        a_u_par.append(np.mean([encode_mean(lu, eps_par, hl) for lu in LM_u]))
    out["nuisance_partial"] = {
        "A_resid_trained_raw": round(float(np.mean(a_t_raw)), 4),
        "A_resid_trained_partialled": round(float(np.mean(a_t_par)), 4),
        "A_resid_untrained_partialled": round(float(np.mean(a_u_par)), 4),
        "gap_partialled": round(float(np.mean(a_t_par) - np.mean(a_u_par)), 4)}
    print(f"  trained raw={out['nuisance_partial']['A_resid_trained_raw']:+.3f} "
          f"-> partialled={out['nuisance_partial']['A_resid_trained_partialled']:+.3f} | "
          f"untrained partialled={out['nuisance_partial']['A_resid_untrained_partialled']:+.3f} | "
          f"gap={out['nuisance_partial']['gap_partialled']:+.3f}")

    # ---------- (C) fold-gap: A_resid with HRF/FIR-leakage gaps ----------
    print("\n=== (C) fold-gap (kill HRF-autocorrelation/FIR train->test leakage) ===")
    foldgap = {}
    for gap in [0, NDELAYS, 2 * NDELAYS]:
        a_t, a_u = [], []
        for s in subs:
            eps = (Ymean[s] - loo_mean(Ymean, subs, s)).astype(np.float32)
            a_t.append(encode_mean(LM_t, eps, hl, gap=gap))
            a_u.append(np.mean([encode_mean(lu, eps, hl, gap=gap) for lu in LM_u]))
        foldgap[gap] = {"A_resid_trained": round(float(np.mean(a_t)), 4),
                        "A_resid_untrained": round(float(np.mean(a_u)), 4),
                        "gap": round(float(np.mean(a_t) - np.mean(a_u)), 4)}
        print(f"  gap={gap:2d}TR: trained={foldgap[gap]['A_resid_trained']:+.3f} "
              f"untrained={foldgap[gap]['A_resid_untrained']:+.3f} gap={foldgap[gap]['gap']:+.3f}")
    out["fold_gap"] = foldgap

    (OUT / "eys_diagnose.json").write_text(json.dumps(out, indent=2))
    print("\n=== DIAGNOSTIC READ ===")
    sc = out["reference_scaling"]
    print(f"  (A) A_resid trained: k=1 {sc[1]['A_resid_trained']:+.3f} -> k=5 {sc[5]['A_resid_trained']:+.3f} "
          f"({'SHRINKS w/ better ref => eta-leak/leaked-stimulus' if sc[5]['A_resid_trained'] < sc[1]['A_resid_trained'] else 'FLAT => not pure reference noise'})")
    print(f"  (B) trained A_resid after partialling stimulus: {out['nuisance_partial']['A_resid_trained_partialled']:+.3f} "
          f"(gap {out['nuisance_partial']['gap_partialled']:+.3f}) "
          f"({'COLLAPSES => leaked stimulus, NOT brain' if abs(out['nuisance_partial']['gap_partialled'])<0.01 else 'SURVIVES => investigate'})")
    print(f"  (C) trained-untrained gap: gap0 {foldgap[0]['gap']:+.3f} -> gap{2*NDELAYS} {foldgap[2*NDELAYS]['gap']:+.3f}")


def _shr(a, b):
    from scipy.stats import zscore
    za, zb = np.nan_to_num(zscore(a, 0)), np.nan_to_num(zscore(b, 0))
    r = (za * zb).mean(0)
    return (2 * r / (1 + np.clip(r, -0.999, 0.999))).astype(np.float32)


if __name__ == "__main__":
    run()
