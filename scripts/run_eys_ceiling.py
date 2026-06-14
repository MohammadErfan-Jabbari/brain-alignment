#!/usr/bin/env python3
"""E020 — the empirical-E[Y|S] ceiling (TRIBE-free), STAGE 1 = story_11. (thesis venv)

Question (spine): does the trained LM align to brain signal BEYOND the stimulus-predictable
part E[Y|S]? Decompose Y_s = E[Y|S] + eps_s. Measure three alignments ON ONE SCALE
(raw per-vertex Pearson r, NC reported separately — D029/L039 v2.1 fix):
  A_total  = LM -> Y_s          (raw per-subject BOLD; the thing alignment is usually measured against)
  A_shared = LM -> E[Y|S]       (the stimulus-predictable part = cross-subject mean)
  A_resid  = LM -> eps_s        (the per-subject residual = Y_s - E[Y|S]_{-s}, leave-one-subject-out)
Primary statistic rho = A_resid / A_shared (same normalization on both). rho small AND
A_total ~ A_shared  =>  the LM's alignment is carried almost entirely by E[Y|S]  =>  Fork-B ceiling.

HONEST SCOPE (L039, pre-lock panel): the LM R(S) is SHARED across subjects, and eps_s subtracts
everything shared, so A_resid ~ 0 is the EXPECTED, theory-consistent result (DPI; conditional-mean
projection). E020 CONFIRMS + BOUNDS + GUARDS; it is the mechanistic ceiling explaining E008's
per-individual null (no per-subject-residual signal for a shared rep to grab), not a standalone proof.
The universal Fork-B rests on CONVERGENCE with E008/E011/E017.

Controls (oracle HOLD fixes, D029):
  G1  repeat-split: story_11 has 2 reps. Use rep-1 to build E[Y|S]^(1)/eps^(1); VALIDATE A_resid
      against rep-2 (eps^(2)) -> a real residual alignment survives the leave-repeat-out check; also
      gives eps's own noise ceiling (split-half across reps).
  G2  reference-reliability jackknife: split the 5 LOO subjects 2-vs-3, correlate the sub-means ->
      reliability of E[Y|S]_{-s}. A noisy reference can BOTH zero-out (false Fork-B) AND inflate
      (false Fork-A via leaked stimulus) A_resid -> report it both ways.
  C1  strong eng1000 nuisance floor: A_resid must beat what rate+artic+eng1000-PCA explains of eps_s
      (trained-untrained alone under-controls the lexical-semantic stimulus path -- L035).
  untrained floor (3 seeds): the verdict is (trained A_resid - untrained A_resid).

NOTE: single story => the MDE here is a within-story/seed-spread PROXY and Fork-A CANNOT fire on it
(asymmetric bar, L038/oracle G3). Stage 2 adds >=2 more stories for the across-story replication unit.
This stage answers: how big is A_resid, is the ceiling tight, does the repeat-2 check hold.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import h5py
import numpy as np
from scipy.stats import zscore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "data/paper-repos/deep-fMRI-dataset/encoding"))
import run_tribe_fidelity as F  # noqa: E402  (load helpers, ridge, ROI groups, NC machinery)
from run_tribe_ceiling import lm_grid, lm_encode, MODEL, UNTRAINED_SEEDS  # noqa: E402
from fsaverage_mapping import voxels_to_fsa5  # noqa: E402

OUT = ROOT / "outputs/E020_eys"
HL = "higher_lang"


def load_real_reps(subj):
    """Per-REPEAT real BOLD in fsa5 (G1 — do NOT average the 2 reps as F.load_real does).
    Returns r0,r1 each (N_TR,20484) on the raw mapper scale, + per-subject split-half NC."""
    f = ROOT / f"data/denizenslab/responses/subject{subj}_listening_fmri_data_val.hdf"
    with h5py.File(f, "r") as h:
        v = h["story_11"][:]                                       # (2,311,nvox)
    r0 = voxels_to_fsa5(v[0], subj)[: F.N_TR].astype(np.float32)
    r1 = voxels_to_fsa5(v[1], subj)[: F.N_TR].astype(np.float32)
    z0, z1 = np.nan_to_num(zscore(r0, 0)), np.nan_to_num(zscore(r1, 0))
    nc = (z0 * z1).mean(0)
    nc = (2 * nc / (1 + np.clip(nc, -0.999, 0.999))).astype(np.float32)
    return r0, r1, nc


def loo_mean(per_subj, subjects, exclude):
    """E[Y|S]_{-s}: mean over all subjects except `exclude`."""
    return np.mean([per_subj[s] for s in subjects if s != exclude], 0).astype(np.float32)


def split_half_nc(a, b):
    """Spearman-Brown corrected split-half reliability between two estimates a,b (per-vertex)."""
    za, zb = np.nan_to_num(zscore(a, 0)), np.nan_to_num(zscore(b, 0))
    r = (za * zb).mean(0)
    return (2 * r / (1 + np.clip(r, -0.999, 0.999))).astype(np.float32)


def mean_in(mask, vec):
    return float(np.nanmean(vec[mask]))


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    subs = F.DENIZ_SUBJECTS
    nlayers = AutoConfig.from_pretrained(MODEL).num_hidden_layers
    layer = {12: 7, 24: 12, 28: 14}.get(nlayers, max(1, nlayers // 2))
    tok = AutoTokenizer.from_pretrained(MODEL); tok.pad_token = tok.pad_token or tok.eos_token
    print(f"{MODEL}: L{layer}/{nlayers}  subjects={subs}")

    # ---- load per-repeat real BOLD + functional ROIs ----
    r0, r1, ncs, roisets = {}, {}, {}, {}
    for s in subs:
        r0[s], r1[s], ncs[s] = load_real_reps(s)
        roisets[s] = F.load_roi_masks_fsa5(s, sum(F.ROI_GROUPS.values(), []))
    Ymean = {s: ((r0[s] + r1[s]) / 2).astype(np.float32) for s in subs}        # 2-rep avg per subject
    Ygroup = np.mean([Ymean[s] for s in subs], 0).astype(np.float32)           # full 6-subj mean = E[Y|S] estimate
    ncgroup = np.mean([ncs[s] for s in subs], 0)
    grp_roi = {g: (np.mean([F._anyroi(roisets[s], names) for s in subs], 0) >= 0.5)
               for g, names in F.ROI_GROUPS.items()}
    hl = grp_roi[HL] & (ncgroup > F.NC_MIN)
    print(f"  higher-lang vertices (NC-gated): {int(hl.sum())}")

    # ---- residuals (G1: rep-split). eps^(1) from rep-1, eps^(2) from rep-2 (validation). ----
    # primary residual uses the 2-rep-avg LOO mean (cleanest E[Y|S] estimate); rep-split used for NC + check.
    eps_avg = {s: (Ymean[s] - loo_mean(Ymean, subs, s)).astype(np.float32) for s in subs}
    eps_r0  = {s: (r0[s] - loo_mean(r0, subs, s)).astype(np.float32) for s in subs}
    eps_r1  = {s: (r1[s] - loo_mean(r1, subs, s)).astype(np.float32) for s in subs}
    # eps noise ceiling: split-half (rep-1 vs rep-2 residuals), per subject, mean over HL
    eps_nc = {s: split_half_nc(eps_r0[s], eps_r1[s]) for s in subs}
    eps_nc_hl = float(np.mean([mean_in(hl, eps_nc[s]) for s in subs]))
    print(f"  eps split-half NC (HL, mean over subj): {eps_nc_hl:+.3f}")

    # ---- G2: reference-reliability jackknife of E[Y|S]_{-s} (2-vs-3 split of the 5 LOO subjects) ----
    ref_rel = []
    for s in subs:
        others = [x for x in subs if x != s]
        a = np.mean([Ymean[x] for x in others[:2]], 0)
        b = np.mean([Ymean[x] for x in others[2:]], 0)
        ref_rel.append(mean_in(hl, split_half_nc(a, b)))
    ref_rel_hl = float(np.mean(ref_rel))
    print(f"  E[Y|S]_-s reference reliability (HL jackknife): {ref_rel_hl:+.3f}")

    # ---- nuisance floor design (C1) ----
    Xnuis = F.lowlevel_design(strong=True)

    def encode_mean(LMfir_or_X, target):
        """raw per-vertex corr of (LM block | nuisance) predicting target -> mean over HL (one scale)."""
        return mean_in(hl, lm_encode(LMfir_or_X, target))

    def alignments(LMfir, tag):
        A_shared = encode_mean(LMfir, Ygroup)                                   # LM -> E[Y|S]
        A_total  = float(np.mean([encode_mean(LMfir, Ymean[s]) for s in subs])) # LM -> Y_s (raw, per subj)
        A_resid  = float(np.mean([encode_mean(LMfir, eps_avg[s]) for s in subs]))# LM -> eps_s
        A_resid_r1 = float(np.mean([encode_mean(LMfir, eps_r1[s]) for s in subs]))# validate on rep-2 residual
        rec = {"tag": tag, "A_shared": round(A_shared, 4), "A_total": round(A_total, 4),
               "A_resid": round(A_resid, 4), "A_resid_rep2": round(A_resid_r1, 4),
               "rho_resid_over_shared": round(A_resid / A_shared, 4) if A_shared > 1e-6 else None}
        print(f"  [{tag}] A_shared={A_shared:+.3f} A_total={A_total:+.3f} A_resid={A_resid:+.3f} "
              f"(rep2 {A_resid_r1:+.3f}) rho={rec['rho_resid_over_shared']}")
        return rec

    # ---- trained ----
    print("== trained ==", flush=True)
    mt = AutoModelForCausalLM.from_pretrained(MODEL).to(device).eval()
    LMfir_t = lm_grid(mt, tok, layer, device); del mt; torch.cuda.empty_cache()
    trained = alignments(LMfir_t, "trained")

    # nuisance floor on eps (C1): what the strong nuisance set explains of eps_s
    nuis_resid = float(np.mean([encode_mean(Xnuis, eps_avg[s]) for s in subs]))
    print(f"  [nuisance->eps] A_resid_nuisance={nuis_resid:+.3f}  (C1 floor A_resid must beat)")

    # ---- untrained floor (3 seeds) ----
    untr = []
    for sd in UNTRAINED_SEEDS:
        print(f"== untrained seed {sd} ==", flush=True)
        torch.manual_seed(sd); cfg = AutoConfig.from_pretrained(MODEL); torch.manual_seed(sd)
        mu = AutoModelForCausalLM.from_config(cfg).to(device).eval()
        LMfir_u = lm_grid(mu, tok, layer, device); del mu; torch.cuda.empty_cache()
        untr.append(alignments(LMfir_u, f"untrained_s{sd}"))

    u_resid = np.array([u["A_resid"] for u in untr])
    gap_resid = trained["A_resid"] - u_resid.mean()                             # brain-specific-beyond-arch
    sd_pool = float(np.std(u_resid, ddof=1)) if len(untr) > 1 else float("nan")
    mde_proxy = 2.49 * sd_pool / np.sqrt(max(len(untr), 1))                     # SINGLE-STORY PROXY ONLY

    verdict = {
        "model": MODEL, "layer": layer, "n_subjects": len(subs), "story": "story_11",
        "eps_nc_hl": round(eps_nc_hl, 4), "ref_reliability_hl": round(ref_rel_hl, 4),
        "trained": trained, "untrained": untr,
        "nuisance_resid": round(nuis_resid, 4),
        "gap_resid_trained_minus_untrained": round(float(gap_resid), 4),
        "untrained_resid_mean": round(float(u_resid.mean()), 4),
        "mde_proxy_singlestory": round(float(mde_proxy), 4),
        "rho_trained": trained["rho_resid_over_shared"],
        "notes": "single-story: MDE is a seed-spread PROXY; Fork-A cannot fire here (needs across-story, stage 2).",
    }
    (OUT / "eys_story11_results.json").write_text(json.dumps(verdict, indent=2))

    print("\n=== E020 STAGE-1 (story_11) VERDICT (pre-panel) ===")
    print(f"  A_shared (LM->E[Y|S])   = {trained['A_shared']:+.3f}")
    print(f"  A_total  (LM->Y_s)      = {trained['A_total']:+.3f}   [decomp check: A_total ~ A_shared?]")
    print(f"  A_resid  (LM->eps_s)    = {trained['A_resid']:+.3f}   rep-2 {trained['A_resid_rep2']:+.3f}")
    print(f"  rho = A_resid/A_shared  = {trained['rho_resid_over_shared']}")
    print(f"  trained-untrained resid = {gap_resid:+.3f}  (untrained {u_resid.mean():+.3f}, MDE-proxy {mde_proxy:+.3f})")
    print(f"  nuisance->eps floor     = {nuis_resid:+.3f}  | eps NC {eps_nc_hl:+.3f} | ref-rel {ref_rel_hl:+.3f}")
    forkA_proxy = (gap_resid > mde_proxy) and (trained["A_resid"] > nuis_resid) and (trained["A_resid_rep2"] > 0)
    print(f"  => {'A_resid POSITIVE on story_11 — escalate to across-story stage 2 BEFORE any Fork-A' if forkA_proxy else 'A_resid within proxy-MDE of 0 / collapses on a control -> ceiling holds (Fork-B), bound rho'}")


if __name__ == "__main__":
    run()
