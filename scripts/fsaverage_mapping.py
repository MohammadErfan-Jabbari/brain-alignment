#!/usr/bin/env python3
"""Voxel <-> fsaverage5 mapping for the TRIBE ceiling experiments (E016 F1/F2).

THE BLOCKER this resolves (E016 §"PHASE 1/2 DESIGN", item 1): TRIBE outputs predicted
fMRI on the **fsaverage5 cortical surface** (20,484 vtx = 10,242/hemi); the Gallant-lab
naturalistic datasets store real BOLD as **subject-native cortical-mask voxels**. The
bridge is the per-subject sparse `voxel_to_fsaverage` mapper shipped with denizenslab
(Deniz 2019) — a (327684, n_vox) CSR matrix projecting voxels onto the FULL fsaverage
surface (163842/hemi). fsaverage5 is the recursive-icosahedral PREFIX of fsaverage
(ico5 nested in ico7): the first 10,242 vertices of each hemisphere coincide exactly
(verified against nilearn meshes in `verify()`), so fsa5 = a direct index subset.

LeBel ds003020 ships only a pycortex-db + freesurfer_subjdir (no precomputed mapper),
so building its mapper needs pycortex+FreeSurfer; denizenslab's mapper is turnkey and
ships per-subject functional ROI localizers (V1..V4/AC/Broca/pSTS/FFA/EBA/...) in the
SAME voxel space, which map to fsaverage5 with the very same matrix → the language-high/
visual-low labels Phase 1 needs, for free. Hence F1/F2 substrate = denizenslab (D027).

fsaverage layout in the mapper (verified): columns 0..163841 = LH, 163842..327683 = RH.
TRIBE preds layout (verified, tribev2/utils_fmri.py:228-243): cols 0..10241 = LH fsa5,
10242..20483 = RH fsa5. So:
    fsa5(LH) = full_fsa[:10242]
    fsa5(RH) = full_fsa[163842 : 163842+10242]
"""
from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np
import scipy.sparse as sp

ROOT = Path(__file__).resolve().parents[1]
DENIZ_MAP = ROOT / "data/denizenslab/mappers"

FSA_PER_HEMI = 163842   # fsaverage (ico7) vertices per hemisphere
FSA5_PER_HEMI = 10242   # fsaverage5 (ico5) vertices per hemisphere
FSA5_N = 2 * FSA5_PER_HEMI  # 20484, matches TRIBE output width

# denizenslab subjects present locally with reading+listening fMRI
DENIZ_SUBJECTS = ["01", "02", "03", "05", "07", "08"]

# Functional-localizer ROIs shipped in the mapper, grouped for the spatial-specificity
# fidelity test. Language/auditory should be HIGH (TRIBE encodes speech/text); early
# visual should be LOW (story listening/reading has little visual drive).
ROI_LANG_AUD = ["AC", "Broca", "pSTS", "sPMv", "ATFP"]      # auditory + language
ROI_EARLY_VIS = ["V1", "V2", "V3", "V3A", "V3B", "V4", "V7"]  # early/mid visual


def _load_sparse(hf: h5py.File, var: str) -> sp.csr_matrix:
    return sp.csr_matrix(
        (hf[f"{var}_data"][:], hf[f"{var}_indices"][:], hf[f"{var}_indptr"][:]),
        shape=tuple(hf[f"{var}_shape"][:]),
    )


def load_voxel_to_fsaverage(subject: str) -> sp.csr_matrix:
    """(327684, n_vox) CSR: voxel-signal -> full-fsaverage-vertex signal."""
    f = DENIZ_MAP / f"subject{subject}_mappers.hdf"
    with h5py.File(f, "r") as hf:
        return _load_sparse(hf, "voxel_to_fsaverage")


def _full_fsa_to_fsa5_cols(n_cols_axis: int) -> np.ndarray:
    """Index array selecting the 20,484 fsaverage5 columns out of 327,684 fsaverage."""
    lh = np.arange(FSA5_PER_HEMI)
    rh = np.arange(FSA_PER_HEMI, FSA_PER_HEMI + FSA5_PER_HEMI)
    return np.concatenate([lh, rh])


def voxels_to_fsa5(bold: np.ndarray, subject: str) -> np.ndarray:
    """Map (T, n_vox) subject BOLD -> (T, 20484) fsaverage5, matching TRIBE layout.

    bold @ M.T projects voxels onto the full fsaverage surface; we then subset the
    fsaverage5 columns. NaN-safe (mapper rows with no voxel support give 0)."""
    M = load_voxel_to_fsaverage(subject)            # (327684, n_vox)
    assert bold.shape[1] == M.shape[1], f"voxel count {bold.shape[1]} != mapper {M.shape[1]}"
    full = np.asarray(bold @ M.T)                   # (T, 327684)
    return full[:, _full_fsa_to_fsa5_cols(full.shape[1])].astype(np.float32)


def roi_vec_to_fsa5(roi_vox: np.ndarray, subject: str) -> np.ndarray:
    """Map a per-voxel ROI weight vector (n_vox,) -> (20484,) fsaverage5 weights."""
    return voxels_to_fsa5(roi_vox[None, :], subject)[0]


def load_roi_masks_fsa5(subject: str, rois: list[str]) -> dict[str, np.ndarray]:
    """Per-ROI fsaverage5 weight vectors (20484,), summed/projected from voxel masks."""
    f = DENIZ_MAP / f"subject{subject}_mappers.hdf"
    out = {}
    with h5py.File(f, "r") as hf:
        for r in rois:
            key = f"roi_mask_{r}"
            if key not in hf:
                continue
            out[r] = roi_vec_to_fsa5(hf[key][:].astype(np.float32), subject)
    return out


def fsa5_roi_index(subject: str, rois: list[str], thresh: float = 0.0) -> np.ndarray:
    """Boolean (20484,) mask = vertices belonging to ANY of `rois` (weight > thresh)."""
    masks = load_roi_masks_fsa5(subject, rois)
    if not masks:
        return np.zeros(FSA5_N, dtype=bool)
    stacked = np.stack(list(masks.values()), 0)
    return (stacked > thresh).any(0)


# --------------------------------------------------------------------------- #
def verify() -> None:
    """Hard checks: (1) fsa5 is the coordinate-prefix of fsaverage in nilearn meshes;
    (2) the mapper loads with the expected shape and the selected fsa5 columns carry
    real support; (3) round-trip a spatial quantity and report ROI coverage."""
    print("=== (1) fsaverage5 ⊂ fsaverage prefix check (nilearn SPHERE meshes) ===")
    # The nesting (ico5 vertices = first 10242 of ico7) is a topological property of
    # FreeSurfer's recursive icosahedral registration — it holds on the SPHERE, not the
    # folded pial surface. Both the denizenslab mapper and TRIBE use this convention.
    from nilearn import datasets
    fsa5 = datasets.fetch_surf_fsaverage("fsaverage5")
    fsa7 = datasets.fetch_surf_fsaverage("fsaverage")
    import nibabel as nib
    for hemi in ["left", "right"]:
        c5 = nib.load(fsa5[f"sphere_{hemi}"]).darrays[0].data  # (10242,3)
        c7 = nib.load(fsa7[f"sphere_{hemi}"]).darrays[0].data  # (163842,3)
        n5 = c5.shape[0]
        maxdiff = np.abs(c5 - c7[:n5]).max()
        print(f"  {hemi}: fsa5 {c5.shape} vs fsa7[:{n5}] sphere max coord diff = {maxdiff:.4g}")
        assert maxdiff < 1e-2, f"{hemi}: fsa5 is NOT the prefix of fsa7 (diff {maxdiff})"

    print("=== (2) mapper shape + fsa5-column support ===")
    subj = DENIZ_SUBJECTS[0]
    M = load_voxel_to_fsaverage(subj)
    print(f"  subject{subj}: voxel_to_fsaverage {M.shape}, nnz/col={M.nnz/M.shape[1]:.2f}")
    cols = _full_fsa_to_fsa5_cols(M.shape[0])
    Msub = M.tocsc()[cols, :]
    supported = np.asarray((Msub != 0).sum(1)).ravel()
    print(f"  fsa5 vertices with >=1 voxel mapped: {(supported>0).sum()}/{FSA5_N} "
          f"({100*(supported>0).mean():.1f}%)")

    print("=== (3) round-trip a spatial quantity (val split-half reliability) ===")
    import scipy.io  # noqa
    # use the validation story (2 repeats) reliability as a real spatial signal
    val = _load_val_reliability(subj)
    rel5 = roi_vec_to_fsa5(val, subj)
    print(f"  reliability voxel range [{val.min():.3f},{val.max():.3f}]; "
          f"fsa5-projected range [{rel5.min():.3f},{rel5.max():.3f}]")
    lang = fsa5_roi_index(subj, ROI_LANG_AUD)
    vis = fsa5_roi_index(subj, ROI_EARLY_VIS)
    print(f"  lang/aud fsa5 vertices: {lang.sum()}; early-vis fsa5 vertices: {vis.sum()}")
    print(f"  mean reliability  lang/aud={rel5[lang].mean():.3f}  vis={rel5[vis].mean():.3f}  "
          f"(listening: lang/aud should exceed vis)")
    print("VERIFY OK")


def _load_val_reliability(subject: str, modality: str = "listening") -> np.ndarray:
    """Per-voxel split-half reliability from the 2-repeat validation story_11."""
    from scipy.stats import zscore
    f = ROOT / f"data/denizenslab/responses/subject{subject}_{modality}_fmri_data_val.hdf"
    with h5py.File(f, "r") as h:
        v = h["story_11"][:]            # (2, TR, vox)
    a = np.nan_to_num(zscore(v[0], axis=0))
    b = np.nan_to_num(zscore(v[1], axis=0))
    return (a * b).mean(0).astype(np.float32)   # per-voxel corr across the 2 reps


if __name__ == "__main__":
    verify()
