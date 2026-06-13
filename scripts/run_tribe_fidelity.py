#!/usr/bin/env python3
"""E016 Phase 1 — FIDELITY: is TRIBE a faithful in-pipeline fMRI stand-in? (thesis venv)

Oracle-locked gate (E016 "Step 3"): the bare lang>visual contrast is vacuous, so the gate
is a THREE-WAY comparison that can FAIL — TRIBE must beat a LOW-LEVEL ridge encoder floor
[numwords, numphonemes, numletters, pauses, audio-envelope] (FIR, contiguous-block CV) in
HIGHER-ORDER language ROIs (Broca/pSTS/ATFP/sPMv, not just envelope-trackable AC), with a
within-cortex gradient (higher-order language HIGH vs somatomotor M1/S1 LOW).

Two levels (single-subject per-vertex is noise-dominated by the 2-rep ceiling; TRIBE
predicts the GROUP-averaged E[Y|S], so we estimand-match):
  • PRIMARY descriptive: GROUP-averaged real fsa5 BOLD (6 subj × 2 reps) → per-vertex r
    maps for TRIBE vs the floor (high SNR, matched estimand).
  • INFERENCE: per-subject ROI-MEAN timecourse correlations, paired across n=6 — TRIBE_corr
    vs floor_corr in higher-order language (the gate), and the lang-vs-motor gradient.

Substrate: denizenslab, story_11 ("wheretheressmoke"; only 2-rep val story → a ceiling),
listening, n=6. TRIBE pred is per-stimulus → ONE prediction shared across subjects
(`outputs/E016_tribe/deniz/full/story_11_pred.npz`). Low-level features = the lab's
PRE-ALIGNED `features_val_NEW.hdf` (306 TR, BOLD clock; story starts at TR 5 = lead
silence) + audio envelope aligned via numwords xcorr. TRIBE (wav-clock, 1 Hz) → resampled
to 2.0045 s, lag-aligned to BOLD on AC (expected ~+5 TR, window-checked).

KILL if TRIBE ≈ the low-level floor in higher-order language. No rung flips — tool gate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import h5py
import numpy as np
from scipy.interpolate import interp1d
from scipy.io import wavfile
from scipy.stats import zscore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fsaverage_mapping import DENIZ_SUBJECTS, voxels_to_fsa5, load_roi_masks_fsa5  # noqa: E402

TR_REAL = 2.0045
NDELAYS = 4
NFOLDS = 5
N_TR = 306                  # lab feature grid (real BOLD 311 → drop 5 trailing-silence TR)
TRIBE_NPZ = ROOT / "outputs/E016_tribe/deniz/full/story_11_pred.npz"
LAB_FEATS = ROOT / "data/denizenslab/features/features_val_NEW.hdf"
WAV = ROOT / "data/denizenslab/stimuli/story_11.wav"
OUT = ROOT / "outputs/E016_tribe/fidelity"

ROI_GROUPS = {
    "higher_lang": ["Broca", "pSTS", "ATFP", "sPMv"],
    "auditory":    ["AC"],
    "early_vis":   ["V1", "V2", "V3", "V3A", "V3B", "V4", "V7"],
    "somatomotor": ["M1F", "M1H", "M1M", "S1F", "S1H", "S1M", "SMFA", "SMHA"],
}
LOWLEVEL_KEYS = ["numwords", "numphonemes", "numletters", "pauses"]
NC_MIN = 0.10
LAG_WINDOW = range(0, 13)


# --------------------------- features & alignment --------------------------- #
def _fir(x, ndelays=NDELAYS):
    T, d = x.shape
    out = np.zeros((T, d * ndelays), np.float32)
    for i, lag in enumerate(range(1, ndelays + 1)):
        out[lag:, i * d:(i + 1) * d] = x[:-lag]
    return out


def _envelope(n_tr):
    sr, wav = wavfile.read(WAV)
    mono = (wav.mean(1) if wav.ndim > 1 else wav).astype(np.float64)
    win = int(round(TR_REAL * sr))
    nwin = len(mono) // win
    rms = np.sqrt(np.array([np.mean(mono[i*win:(i+1)*win]**2) for i in range(nwin)]) + 1e-9).astype(np.float32)
    with h5py.File(LAB_FEATS, "r") as h:
        nw = np.asarray(h["story_11/numwords"][:], np.float32).ravel()
    bestL, bestc = 0, -2.0
    for L in range(12):
        g = np.zeros(n_tr, np.float32); seg = rms[:max(0, n_tr - L)]; g[L:L+len(seg)] = seg
        m = min(len(g), len(nw)); c = np.corrcoef(g[:m], nw[:m])[0, 1]
        if c > bestc: bestc, bestL = c, L
    g = np.zeros(n_tr, np.float32); seg = rms[:max(0, n_tr - bestL)]; g[bestL:bestL+len(seg)] = seg
    return g.reshape(-1, 1), bestL, float(bestc)


def lowlevel_design(n_tr=N_TR):
    with h5py.File(LAB_FEATS, "r") as h:
        feats = [np.asarray(h[f"story_11/{k}"][:], np.float32).reshape(-1, 1) for k in LOWLEVEL_KEYS]
    X = np.concatenate(feats, 1)[:n_tr]
    env, L, c = _envelope(n_tr)
    print(f"  [envelope] lead L={L} TR (corr numwords={c:.3f})")
    X = np.concatenate([X, env], 1)
    return _fir(np.nan_to_num(zscore(X, 0)))


def load_real(subj):
    f = ROOT / f"data/denizenslab/responses/subject{subj}_listening_fmri_data_val.hdf"
    with h5py.File(f, "r") as h:
        v = h["story_11"][:]                                  # (2,311,nvox)
    r0, r1 = voxels_to_fsa5(v[0], subj), voxels_to_fsa5(v[1], subj)
    z0, z1 = np.nan_to_num(zscore(r0, 0)), np.nan_to_num(zscore(r1, 0))
    nc = (z0 * z1).mean(0); nc = (2 * nc / (1 + np.clip(nc, -0.999, 0.999))).astype(np.float32)
    Y = ((r0 + r1) / 2)[:N_TR].astype(np.float32)
    return Y, nc


def load_tribe_aligned(Y_group, ac_sel):
    d = np.load(TRIBE_NPZ)
    preds, tr = d["preds"].astype(np.float32), float(d["tr"])
    t_src = np.arange(preds.shape[0]) * tr
    t_dst = np.arange(int(np.ceil(t_src[-1] / TR_REAL)) + 1) * TR_REAL
    res = interp1d(t_src, preds, axis=0, bounds_error=False, fill_value=0.0)(t_dst).astype(np.float32)
    prof, bestL, bestc = {}, 0, -2.0
    for L in LAG_WINDOW:
        g = np.zeros((N_TR, res.shape[1]), np.float32); seg = res[:max(0, N_TR - L)]; g[L:L+len(seg)] = seg
        c = _meancorr(g[:, ac_sel], Y_group[:, ac_sel]); prof[int(L)] = round(float(c), 4)
        if c > bestc: bestc, bestL = c, L
    g = np.zeros((N_TR, res.shape[1]), np.float32); seg = res[:max(0, N_TR - bestL)]; g[bestL:bestL+len(seg)] = seg
    sharp = bestc - float(np.median(list(prof.values())))
    print(f"  [TRIBE lag] L={bestL} TR (AC corr={bestc:.3f}, sharpness={sharp:.3f})")
    return g, int(bestL), float(bestc), float(sharp), prof


# --------------------------- stats helpers --------------------------- #
def _meancorr(A, B):
    return float(np.nanmean(np.nanmean(zscore(A, 0) * zscore(B, 0), 0)))


def _percol_corr(P, Y):
    return (np.nan_to_num(zscore(P, 0)) * np.nan_to_num(zscore(Y, 0))).mean(0)


def ridge_cv_pred(X, Y, alphas=(1.0, 1e1, 1e2, 1e3, 1e4)):
    """Contiguous 5-fold ridge; return held-out predictions (T,·), alpha by mean test corr.
    Centers X and Y on the TRAINING fold (intercept handled, not regularized) — without
    this, the BOLD mean leaks into the fit since features are z-scored over the full series
    (not per fold), which spuriously favors huge alpha. Y may be 1-D or 2-D."""
    Y2 = Y if Y.ndim == 2 else Y[:, None]
    T = X.shape[0]; folds = np.array_split(np.arange(T), NFOLDS)
    best = (-2.0, None, None)
    for a in alphas:
        pred = np.zeros_like(Y2)
        for te in folds:
            trn = np.setdiff1d(np.arange(T), te)
            mx, my = X[trn].mean(0), Y2[trn].mean(0)
            Xtr, Ytr = X[trn] - mx, Y2[trn] - my
            B = np.linalg.solve(Xtr.T @ Xtr + a * np.eye(X.shape[1]), Xtr.T @ Ytr)
            pred[te] = (X[te] - mx) @ B + my
        m = float(np.nanmean(_percol_corr(pred, Y2)))
        if m > best[0]: best = (m, a, pred)
    return best[2], best[1]


def _anyroi(rois, names, thr=0.0):
    present = [rois[n] for n in names if n in rois]
    return (np.stack(present) > thr).any(0) if present else np.zeros(20484, bool)


def _ci(x):
    x = np.asarray(x, float); m = x.mean(); s = x.std(ddof=1) / np.sqrt(len(x))
    return round(m, 4), [round(m - 1.96*s, 4), round(m + 1.96*s, 4)]


# --------------------------------- run --------------------------------- #
def run():
    OUT.mkdir(parents=True, exist_ok=True)
    if not TRIBE_NPZ.exists():
        print(f"WAIT: TRIBE preds not ready at {TRIBE_NPZ}"); return

    # load all subjects' real BOLD + per-subject functional ROIs
    reals, ncs, roisets = {}, {}, {}
    for s in DENIZ_SUBJECTS:
        reals[s], ncs[s] = load_real(s)
        roisets[s] = load_roi_masks_fsa5(s, sum(ROI_GROUPS.values(), []))
    Ygroup = np.mean([reals[s] for s in DENIZ_SUBJECTS], 0).astype(np.float32)
    ncgroup = np.mean([ncs[s] for s in DENIZ_SUBJECTS], 0)
    # group ROI = majority vote of per-subject functional localizers
    grp_roi = {g: (np.mean([(_anyroi(roisets[s], names)) for s in DENIZ_SUBJECTS], 0) >= 0.5)
               for g, names in ROI_GROUPS.items()}
    ac_sel = grp_roi["auditory"] & (ncgroup > NC_MIN)

    Xlow = lowlevel_design()
    Ttribe, lag, ac_c, sharp, prof = load_tribe_aligned(Ygroup, ac_sel)
    if not (LAG_WINDOW.start <= lag < LAG_WINDOW.stop) or sharp < 0.02:
        print(f"  WARNING: lag {lag}/sharpness {sharp:.3f} suspect — alignment may be unreliable.")

    # ---- PRIMARY: group-avg per-vertex r maps ----
    floor_pred_g, alpha = ridge_cv_pred(Xlow, Ygroup)
    r_floor_g = _percol_corr(floor_pred_g, Ygroup)
    r_tribe_g = _percol_corr(Ttribe, Ygroup)
    group_summary = {"alpha": alpha, "lag_tr": lag, "ac_corr": ac_c, "lag_sharpness": sharp,
                     "lag_profile": prof}
    for g, mask in grp_roi.items():
        sel = mask & (ncgroup > NC_MIN)
        group_summary[g] = {"n": int(sel.sum()),
                            "tribe_r": round(float(np.nanmean(r_tribe_g[sel])), 4),
                            "floor_r": round(float(np.nanmean(r_floor_g[sel])), 4),
                            "tribe_minus_floor": round(float(np.nanmean(r_tribe_g[sel] - r_floor_g[sel])), 4)}

    # ---- INFERENCE: per-subject ROI-mean timecourse correlations, paired n=6 ----
    per_subj = []
    for s in DENIZ_SUBJECTS:
        Y, nc, rois = reals[s], ncs[s], roisets[s]
        rec = {"subject": s}
        for g, names in ROI_GROUPS.items():
            sel = _anyroi(rois, names) & (nc > NC_MIN)
            if sel.sum() < 10:
                rec[g] = {"tribe_corr": float("nan"), "floor_corr": float("nan"), "n": int(sel.sum())}
                continue
            y = Y[:, sel].mean(1)                                  # real ROI-mean timecourse
            t = Ttribe[:, sel].mean(1)                             # TRIBE ROI-mean
            fp, _ = ridge_cv_pred(Xlow, y[:, None])                # floor → ROI-mean (CV)
            rec[g] = {"n": int(sel.sum()),
                      "tribe_corr": round(float(np.corrcoef(zscore(t), zscore(y))[0, 1]), 4),
                      "floor_corr": round(float(_percol_corr(fp, y[:, None])[0]), 4)}
        rec["delta_higher_lang"] = round(rec["higher_lang"]["tribe_corr"] - rec["higher_lang"]["floor_corr"], 4)
        rec["grad_lang_minus_motor"] = round(rec["higher_lang"]["tribe_corr"] - rec["somatomotor"]["tribe_corr"], 4)
        rec["spec_lang_minus_vis"] = round(rec["higher_lang"]["tribe_corr"] - rec["early_vis"]["tribe_corr"], 4)
        per_subj.append(rec)
        print(f"  subj{s}: higher_lang TRIBE={rec['higher_lang']['tribe_corr']:.3f} "
              f"floor={rec['higher_lang']['floor_corr']:.3f} Δ={rec['delta_higher_lang']:+.3f} "
              f"grad={rec['grad_lang_minus_motor']:+.3f}")

    agg = {
        "delta_higher_lang": dict(zip(["mean", "ci95"], _ci([r["delta_higher_lang"] for r in per_subj]))),
        "grad_lang_minus_motor": dict(zip(["mean", "ci95"], _ci([r["grad_lang_minus_motor"] for r in per_subj]))),
        "spec_lang_minus_vis": dict(zip(["mean", "ci95"], _ci([r["spec_lang_minus_vis"] for r in per_subj]))),
        "tribe_higher_lang": dict(zip(["mean", "ci95"], _ci([r["higher_lang"]["tribe_corr"] for r in per_subj]))),
        "floor_higher_lang": dict(zip(["mean", "ci95"], _ci([r["higher_lang"]["floor_corr"] for r in per_subj]))),
        "delta_positive": int(sum(r["delta_higher_lang"] > 0 for r in per_subj)),
        "grad_positive": int(sum(r["grad_lang_minus_motor"] > 0 for r in per_subj)),
        "n": len(per_subj),
    }
    res = {"group": group_summary, "per_subject": per_subj, "aggregate": agg}
    (OUT / "fidelity_results.json").write_text(json.dumps(res, indent=2))
    print("\n=== GROUP per-vertex (high-SNR) ===")
    for g in ROI_GROUPS:
        print(f"  {g:12s} TRIBE={group_summary[g]['tribe_r']:+.3f} floor={group_summary[g]['floor_r']:+.3f} "
              f"Δ={group_summary[g]['tribe_minus_floor']:+.3f} (n={group_summary[g]['n']})")
    print("\n=== INFERENCE (per-subject ROI-mean, n=6) ===")
    print(json.dumps(agg, indent=2))
    _verdict(agg)


def _verdict(agg):
    pf = agg["delta_higher_lang"]["ci95"][0] > 0
    pg = agg["grad_lang_minus_motor"]["ci95"][0] > 0
    print("\n=== PHASE-1 VERDICT (pre-panel) ===")
    print(f"  TRIBE > low-level floor in higher-order language: Δ={agg['delta_higher_lang']['mean']} "
          f"CI{agg['delta_higher_lang']['ci95']} ({agg['delta_positive']}/{agg['n']}) -> {'PASS' if pf else 'HOLD'}")
    print(f"  higher-lang > somatomotor gradient: {agg['grad_lang_minus_motor']['mean']} "
          f"CI{agg['grad_lang_minus_motor']['ci95']} ({agg['grad_positive']}/{agg['n']}) -> {'PASS' if pg else 'HOLD'}")
    print("  => faithful, proceed to Phase 2 (panel-gate first)" if pf and pg
          else "  => HOLD/KILL: not clearly beating the low-level floor; do not build Phase 3")


if __name__ == "__main__":
    run()
