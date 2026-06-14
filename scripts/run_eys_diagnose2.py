#!/usr/bin/env python3
"""E020 diagnostic-2 — is the nuisance-partial (diagnostic B) VALID or VACUOUS? (thesis venv)
Counter-argument + premortem demanded these before any Fork-B read:

  (D) SYMMETRIC PARTIAL (the decisive one). Diagnostic B residualized eps on eng1000 and A_resid
      collapsed +0.090->-0.008. But eng1000 spans the LM's OWN semantic subspace, so the collapse
      could be over-subtraction, not "leaked stimulus removed." Test: does A_SHARED (LM->E[Y|S]) ALSO
      collapse under the SAME eng1000 partial?  A_shared survives & A_resid dies => B DISCRIMINATES
      (residual was stimulus). BOTH die => B is VACUOUS (eng1000 eats all LM-reachable variance) =>
      E020 cannot tell, concede bounded-not-closed.
  (E) GRADED nuisance. Partial eps on LOW-LEVEL only (rate+envelope, NO eng1000). If A_resid survives
      the low-level partial but dies only when eng1000 is added, the collapse lives entirely in the
      semantic subspace (where leaked-stimulus and a real semantic residual are indistinguishable).
  (F) PERMUTED-eng1000. Partial eps on a TIME-PERMUTED eng1000 (same dim/spectrum, wrong alignment).
      If A_resid collapses just as hard vs scrambled eng1000, the collapse is a degrees-of-freedom /
      overfit artifact of partialling a 171-dim FIR design out of 306 TRs, not stimulus removal.
  (G) GAPPED partial. Re-run the eng1000 partial WITH fold-gaps (compose B+C; B was gap=0, leaky).
  (H) rho vs A_total (commensurable denominator) + the A_total<A_shared anomaly.

All on trained + untrained, higher-language, story_11, n=6.
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
from run_tribe_ceiling import lm_grid, MODEL, UNTRAINED_SEEDS  # noqa: E402
from run_eys_ceiling import load_real_reps, loo_mean, HL  # noqa: E402
from run_eys_diagnose import ridge_pred_gap  # noqa: E402

OUT = ROOT / "outputs/E020_eys"
NDELAYS = F.NDELAYS


def enc(X, target, hl, gap=0):
    return float(np.nanmean(F._percol_corr(ridge_pred_gap(X, target, gap), target)[hl]))


def partial_on(Xnuis, target, gap=0):
    """residualize target on the nuisance design (held-out ridge), return residual."""
    return (target - ridge_pred_gap(Xnuis, target, gap)).astype(np.float32)


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
    Ygroup = np.mean([Ymean[s] for s in subs], 0).astype(np.float32)
    ncgroup = np.mean([ncs[s] for s in subs], 0)
    grp_roi = {g: (np.mean([F._anyroi(roisets[s], names) for s in subs], 0) >= 0.5)
               for g, names in F.ROI_GROUPS.items()}
    hl = grp_roi[HL] & (ncgroup > F.NC_MIN)
    eps = {s: (Ymean[s] - loo_mean(Ymean, subs, s)).astype(np.float32) for s in subs}

    Xstrong = F.lowlevel_design(strong=True)      # rate+artic+envelope+eng1000-PCA
    Xweak = F.lowlevel_design(strong=False)       # rate+envelope only (no eng1000/artic)
    # permuted-eng1000 strong design: time-roll the eng1000 PCA block only. Rebuild a permuted strong design.
    rng = np.random.RandomState(0)
    perm = rng.permutation(F.N_TR)
    Xstrong_perm = Xstrong.copy()
    # the FIR strong design = [low-level(71)|eng1000-PCA(100)] each *NDELAYS; permute whole rows (simplest valid scramble of temporal alignment)
    Xstrong_perm = Xstrong[perm]

    print("== trained ==")
    mt = AutoModelForCausalLM.from_pretrained(MODEL).to(device).eval()
    LM_t = lm_grid(mt, tok, layer, device); del mt; torch.cuda.empty_cache()
    LM_u = []
    for sd in UNTRAINED_SEEDS:
        torch.manual_seed(sd); cfg = AutoConfig.from_pretrained(MODEL); torch.manual_seed(sd)
        mu = AutoModelForCausalLM.from_config(cfg).to(device).eval()
        LM_u.append(lm_grid(mu, tok, layer, device)); del mu; torch.cuda.empty_cache()

    def umean(fn):
        return float(np.mean([fn(lu) for lu in LM_u]))

    out = {"layer": layer}

    # ---- (D) symmetric partial: A_shared and A_resid under the SAME strong eng1000 partial ----
    a_shared_raw = enc(LM_t, Ygroup, hl)
    a_shared_par = enc(LM_t, partial_on(Xstrong, Ygroup), hl)
    a_resid_raw = float(np.mean([enc(LM_t, eps[s], hl) for s in subs]))
    a_resid_par = float(np.mean([enc(LM_t, partial_on(Xstrong, eps[s]), hl) for s in subs]))
    out["symmetric_partial"] = {
        "A_shared_raw": round(a_shared_raw, 4), "A_shared_partialled": round(a_shared_par, 4),
        "A_resid_raw": round(a_resid_raw, 4), "A_resid_partialled": round(a_resid_par, 4),
        "shared_survival_frac": round(a_shared_par / a_shared_raw, 3) if a_shared_raw > 1e-6 else None,
        "resid_survival_frac": round(a_resid_par / a_resid_raw, 3) if a_resid_raw > 1e-6 else None}
    print("\n=== (D) SYMMETRIC partial (decisive) ===")
    print(f"  A_shared {a_shared_raw:+.3f} -> {a_shared_par:+.3f} (survives {out['symmetric_partial']['shared_survival_frac']})")
    print(f"  A_resid  {a_resid_raw:+.3f} -> {a_resid_par:+.3f} (survives {out['symmetric_partial']['resid_survival_frac']})")
    discr = (a_shared_par > 0.5 * a_shared_raw) and (a_resid_par < 0.25 * a_resid_raw)
    print(f"  => {'B DISCRIMINATES (shared survives, resid dies) -> residual was stimulus' if discr else 'B VACUOUS-ish (eng1000 eats shared too) -> bounded-not-closed'}")

    # ---- (E) graded: A_resid under low-level-only partial ----
    a_resid_weak = float(np.mean([enc(LM_t, partial_on(Xweak, eps[s]), hl) for s in subs]))
    out["graded"] = {"A_resid_lowlevel_partialled": round(a_resid_weak, 4)}
    print(f"\n=== (E) graded: A_resid after LOW-LEVEL-only partial = {a_resid_weak:+.3f} (raw {a_resid_raw:+.3f}) ===")

    # ---- (F) permuted-eng1000 partial ----
    a_resid_perm = float(np.mean([enc(LM_t, partial_on(Xstrong_perm, eps[s]), hl) for s in subs]))
    out["permuted_nuisance"] = {"A_resid_permuted_partialled": round(a_resid_perm, 4)}
    print(f"=== (F) permuted-nuisance partial: A_resid = {a_resid_perm:+.3f} "
          f"({'collapse is DOF/overfit artifact (scramble kills it too)' if a_resid_perm < 0.25*a_resid_raw else 'real alignment (scramble does NOT kill it)'}) ===")

    # ---- (G) gapped strong partial (compose B+C) ----
    a_resid_par_gap = float(np.mean([enc(LM_t, partial_on(Xstrong, eps[s], gap=NDELAYS), hl, gap=NDELAYS) for s in subs]))
    a_resid_par_gap_u = umean(lambda lu: float(np.mean([enc(lu, partial_on(Xstrong, eps[s], gap=NDELAYS), hl, gap=NDELAYS) for s in subs])))
    out["gapped_partial"] = {"A_resid_trained": round(a_resid_par_gap, 4), "A_resid_untrained": round(a_resid_par_gap_u, 4),
                             "gap": round(a_resid_par_gap - a_resid_par_gap_u, 4)}
    print(f"=== (G) gapped+partialled: trained {a_resid_par_gap:+.3f} untrained {a_resid_par_gap_u:+.3f} gap {out['gapped_partial']['gap']:+.3f} ===")

    # ---- (H) rho vs A_total ----
    a_total = float(np.mean([enc(LM_t, Ymean[s], hl) for s in subs]))
    out["rho_commensurable"] = {"A_total": round(a_total, 4), "A_shared": round(a_shared_raw, 4),
                                "A_resid": round(a_resid_raw, 4),
                                "rho_vs_shared": round(a_resid_raw / a_shared_raw, 3),
                                "rho_vs_total": round(a_resid_raw / a_total, 3) if a_total > 1e-6 else None}
    print(f"=== (H) A_total {a_total:+.3f} A_shared {a_shared_raw:+.3f} | rho/shared {out['rho_commensurable']['rho_vs_shared']} rho/total {out['rho_commensurable']['rho_vs_total']} ===")

    (OUT / "eys_diagnose2.json").write_text(json.dumps(out, indent=2))
    print("\nWROTE", OUT / "eys_diagnose2.json")


if __name__ == "__main__":
    run()
