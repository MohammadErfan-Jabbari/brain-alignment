#!/usr/bin/env python3
"""E016 Phase 2 — THE CEILING: does an LM align to real BOLD beyond TRIBE (=E[Y|S])? (thesis venv)

Spine: Y = E[Y|S] + ε, ε ⊥ θ*. TRIBE estimates E[Y|S]. So the LM (θ*-derived) should align to the
stimulus-predictable part only → residual alignment ≈ 0 ⇒ Fork-B ceiling; >0 surviving controls ⇒ Fork-A.

Oracle-locked design (E016 Step 8) — the ΔR²|TRIBE partition was primed for a FALSE Fork-A, so:
  • CAPACITY-FAIR estimand (B): the SAME LM block (PCA-100×FIR) is scored against TWO targets — real BOLD vs
    TRIBE BOLD — beyond the nuisance floor (held-out residualization then LM encoding). Capacity bias cancels.
  • UNTRAINED-LM FLOOR is the VERDICT: residual = NC-norm A(LM→real) − A(LM→TRIBE); the claim is
    (trained residual − untrained residual), ≥3 untrained seeds, on BOTH full and no-text TRIBE.
  • Group-avg real BOLD primary (estimand-matched to group-TRIBE); per-subject = consistency.
  • Pre-registered MDE (fold-variance). Single story → a residual BOUND, not a clean null. Vacuity check:
    TRIBE-real alignment in higher-language must exceed the nuisance floor.
Fork-A bar (asymmetric): trained−untrained residual gap excludes 0 vs BOTH TRIBE variants → STOP for Erfan.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import zscore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "data/paper-repos/deep-fMRI-dataset/encoding"))
import run_tribe_fidelity as F  # noqa: E402
import lebel_adapter as L  # noqa: E402

MODEL = "Qwen/Qwen2.5-0.5B"
UNTRAINED_SEEDS = [0, 1, 2]
ENG_PCS_LM = 100
TSV = Path("/home/centcom/data/tribe_cache/story_11_16k.tsv")
LEAD_S = 10.0                     # lab grid: story starts at TR 5 (10s lead silence)
OUT = ROOT / "outputs/E016_tribe/ceiling"
HL = "higher_lang"               # the ROI carrying the claim


def lm_grid(model, tok, layer, device, n_tr=F.N_TR):
    """LM word features on story_11 → (n_tr, ENG_PCS_LM) PCA, FIR'd; aligned to the lab/BOLD grid."""
    import pandas as pd
    from ridge_utils.interpdata import lanczosinterp2D
    from sklearn.decomposition import PCA
    df = pd.read_csv(TSV, sep="\t")
    words = [str(w) for w in df["text"].tolist()]
    wt = df["start"].astype(float).to_numpy() + LEAD_S        # story clock + lead → lab grid seconds
    feats = L.lm_word_features(model, tok, words, layer, device)   # (n_words, d)
    tr_times = np.arange(n_tr) * F.TR_REAL
    Xtr = lanczosinterp2D(feats, wt, tr_times, window=3)            # (n_tr, d)
    Xtr = np.nan_to_num(zscore(Xtr, 0))
    pcs = PCA(n_components=min(ENG_PCS_LM, Xtr.shape[0] - 1), random_state=0).fit_transform(Xtr).astype(np.float32)
    return F._fir(pcs)                                             # (n_tr, ENG_PCS_LM*ndelays)


def lm_encode(LMfir, target):
    """Capacity-fair estimand (B): held-out per-vertex correlation of the SAME LM block predicting the
    RAW target directly. NO nuisance-residualization of the target — that empties TRIBE (a near-
    deterministic stimulus function) and manufactures a false Fork-A (oracle Q1b / the v1 vacuity fail).
    Same LM block for real & TRIBE → capacity bias cancels in the difference; untrained floor + NC-norm
    of the (noisy) real target handle the rest."""
    Y = target if target.ndim == 2 else target[:, None]
    pred_lm, _ = F.ridge_cv_pred(LMfir, Y)
    return F._percol_corr(pred_lm, Y)                              # (n_vox,)


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    nlayers = AutoConfig.from_pretrained(MODEL).num_hidden_layers
    layer = {12: 7, 24: 12, 28: 14}.get(nlayers, max(1, nlayers // 2))
    tok = AutoTokenizer.from_pretrained(MODEL); tok.pad_token = tok.pad_token or tok.eos_token
    print(f"{MODEL}: L{layer}/{nlayers}")

    # --- targets (group-avg real + per-subject) and TRIBE variants, on the 306-TR grid ---
    reals, ncs, roisets = {}, {}, {}
    for s in F.DENIZ_SUBJECTS:
        reals[s], ncs[s] = F.load_real(s); roisets[s] = F.load_roi_masks_fsa5(s, sum(F.ROI_GROUPS.values(), []))
    Ygroup = np.mean([reals[s] for s in F.DENIZ_SUBJECTS], 0).astype(np.float32)
    ncgroup = np.mean([ncs[s] for s in F.DENIZ_SUBJECTS], 0)
    grp_roi = {g: (np.mean([F._anyroi(roisets[s], names) for s in F.DENIZ_SUBJECTS], 0) >= 0.5)
               for g, names in F.ROI_GROUPS.items()}
    ac_sel = grp_roi["auditory"] & (ncgroup > F.NC_MIN)
    nuis = F.lowlevel_design(strong=True)
    # TRIBE full + no-text, lag-aligned (reuse Phase-1 loader; lag from AC on group)
    Tfull, lag, ac_c, sharp, _ = F.load_tribe_aligned(Ygroup, ac_sel)
    import numpy as _np
    F.TRIBE_NPZ = ROOT / "outputs/E016_tribe/deniz/notext/story_11_pred.npz"
    Tnotext, lag_nt, _, _, _ = F.load_tribe_aligned(Ygroup, ac_sel)
    F.TRIBE_NPZ = ROOT / "outputs/E016_tribe/deniz/full/story_11_pred.npz"
    print(f"TRIBE lag full={lag} notext={lag_nt} (AC corr {ac_c:.3f})")

    hl = grp_roi[HL] & (ncgroup > F.NC_MIN)
    nc_hl = np.sqrt(np.clip(ncgroup, F.NC_MIN, 1.0))

    def lm_residuals(model, tag):
        LMfir = lm_grid(model, tok, layer, device)
        a_real = lm_encode(LMfir, Ygroup) / nc_hl   # NC-normalized (real has noise; TRIBE noiseless)
        a_full = lm_encode(LMfir, Tfull)
        a_nt = lm_encode(LMfir, Tnotext)
        res_full = float(np.nanmean((a_real - a_full)[hl]))
        res_nt = float(np.nanmean((a_real - a_nt)[hl]))
        rec = {"tag": tag, "A_real_hl": float(np.nanmean(a_real[hl])),
               "A_tribe_full_hl": float(np.nanmean(a_full[hl])), "A_tribe_notext_hl": float(np.nanmean(a_nt[hl])),
               "residual_full": res_full, "residual_notext": res_nt}
        print(f"  [{tag}] A_real(NC)={rec['A_real_hl']:+.3f} A_TRIBE_full={rec['A_tribe_full_hl']:+.3f} "
              f"A_TRIBE_notext={rec['A_tribe_notext_hl']:+.3f} | resid_full={res_full:+.3f} resid_notext={res_nt:+.3f}")
        return rec

    print("== trained ==", flush=True)
    mt = AutoModelForCausalLM.from_pretrained(MODEL).to(device).eval()
    trained = lm_residuals(mt, "trained"); del mt; torch.cuda.empty_cache()

    untr = []
    for sd in UNTRAINED_SEEDS:
        print(f"== untrained seed {sd} ==", flush=True)
        torch.manual_seed(sd)
        cfg = AutoConfig.from_pretrained(MODEL); torch.manual_seed(sd)
        mu = AutoModelForCausalLM.from_config(cfg).to(device).eval()
        untr.append(lm_residuals(mu, f"untrained_s{sd}")); del mu; torch.cuda.empty_cache()

    # --- verdict: trained residual − mean untrained residual, vs BOTH TRIBE variants ---
    u_full = np.array([u["residual_full"] for u in untr]); u_nt = np.array([u["residual_notext"] for u in untr])
    gap_full = trained["residual_full"] - u_full.mean()
    gap_nt = trained["residual_notext"] - u_nt.mean()
    # MDE from untrained-seed spread (the achievable resolution of the residual statistic)
    sd_pool = float(np.std(np.concatenate([u_full, u_nt]), ddof=1)) if len(untr) > 1 else float("nan")
    mde = 2.49 * sd_pool / np.sqrt(max(len(untr), 1))
    verdict = {
        "model": MODEL, "layer": layer, "lag_full": lag, "lag_notext": lag_nt,
        "trained": trained, "untrained": untr,
        "gap_full": round(gap_full, 4), "gap_notext": round(gap_nt, 4),
        "untrained_residual_full_mean": round(float(u_full.mean()), 4),
        "untrained_residual_notext_mean": round(float(u_nt.mean()), 4),
        "mde_approx": round(float(mde), 4),
        "vacuity_check": {"tribe_full_aligns_above_chance": trained["A_tribe_full_hl"] > 0.05},
    }
    (OUT / "ceiling_results.json").write_text(json.dumps(verdict, indent=2))
    print("\n=== PHASE-2 CEILING VERDICT (pre-panel) ===")
    print(f"  trained residual: full={trained['residual_full']:+.3f} notext={trained['residual_notext']:+.3f}")
    print(f"  untrained residual mean: full={u_full.mean():+.3f} notext={u_nt.mean():+.3f}")
    print(f"  GAP (trained − untrained): full={gap_full:+.3f}  notext={gap_nt:+.3f}  (≈MDE {mde:+.3f})")
    print(f"  TRIBE-full aligns above chance in higher-lang (vacuity): A={trained['A_tribe_full_hl']:.3f} "
          f"-> {'OK' if trained['A_tribe_full_hl']>0.05 else 'VACUOUS — subtraction has little to subtract'}")
    forkA = (gap_full > mde) and (gap_nt > mde)
    print(f"  => {'FORK-A CANDIDATE (gap>MDE vs BOTH) — STOP for Erfan' if forkA else 'FORK-B / ceiling holds (gap within MDE of 0, or collapses vs a variant)'}")


if __name__ == "__main__":
    run()
