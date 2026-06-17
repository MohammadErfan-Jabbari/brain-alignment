"""
setup_moussa_data.py
====================
One-shot setup for the Moussa & Toneva 2025 (multi-brain-tuning) experiment.

Steps:
  1. Download all 84 story wav files from OpenNeuro S3 → data/stimuli_wav/
  2. Resample to 16 kHz mono → save as data/processed_stim_data_dp/{story}/wav.npy
  3. Build grids_huge.jbl from ds003020/derivative/TextGrids/
  4. Build trfiles_huge.jbl by simulating TRFiles from the fMRI TR counts
  5. Prove one story loads end-to-end through FMRIStory

Run with:  uv run python scripts/setup_moussa_data.py
"""

import os, sys, urllib.request, json, time
import numpy as np
import joblib
import librosa
import h5py

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = "/home/centcom/data/brain-alignment"
TEXTGRID_DIR  = f"{REPO_ROOT}/data/lebel_ds003020/derivatives/TextGrids"
FMRI_DIR      = f"{REPO_ROOT}/data/lebel_ds003020/preprocessed_data"
RAW_WAV_DIR   = f"{REPO_ROOT}/data/stimuli_wav"           # raw downloads
STIM_DIR      = f"{REPO_ROOT}/data/processed_stim_data_dp"  # wav.npy files
STORY_DATA_DIR = f"{REPO_ROOT}/data/story_data"            # grids/trfiles jbl

os.makedirs(RAW_WAV_DIR, exist_ok=True)
os.makedirs(STORY_DATA_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Ridge-utils imports from the multi-brain-tuning repo
# ---------------------------------------------------------------------------
RIDGE_UTILS = f"{REPO_ROOT}/data/paper-repos/multi-brain-tuning/src"
sys.path.insert(0, RIDGE_UTILS)
from ridge_utils.textgrid import TextGrid
from ridge_utils.stimulus_utils import TRFile

# ---------------------------------------------------------------------------
# Story list — all 84 stories present in TextGrids dir
# ---------------------------------------------------------------------------
STORIES = sorted([
    f.replace(".TextGrid", "")
    for f in os.listdir(TEXTGRID_DIR)
    if f.endswith(".TextGrid")
])
print(f"Stories found: {len(STORIES)}")

S3_BASE = "https://s3.amazonaws.com/openneuro.org/ds003020/stimuli"
TARGET_SR = 16000
TRIM_START = 10  # TRs trimmed at start in dataset.py
TRIM_END   = 5   # TRs trimmed at end
TR         = 2.0045  # expected TR in seconds

# ---------------------------------------------------------------------------
# Step 1 + 2: Download wavs + build wav.npy
# ---------------------------------------------------------------------------
failed_audio = []
succeeded_audio = []

for story in STORIES:
    npy_path = f"{STIM_DIR}/{story}/wav.npy"
    if os.path.exists(npy_path):
        succeeded_audio.append(story)
        continue

    raw_path = f"{RAW_WAV_DIR}/{story}.wav"
    url = f"{S3_BASE}/{story}.wav"

    # Download if needed
    if not os.path.exists(raw_path):
        try:
            print(f"  Downloading {story} ...", flush=True)
            urllib.request.urlretrieve(url, raw_path)
        except Exception as e:
            print(f"  FAILED download {story}: {e}", flush=True)
            failed_audio.append(story)
            continue

    # Resample to 16 kHz mono and save as npy
    try:
        audio, sr = librosa.load(raw_path, sr=TARGET_SR, mono=True)
        os.makedirs(f"{STIM_DIR}/{story}", exist_ok=True)
        np.save(npy_path, audio)
        succeeded_audio.append(story)
        print(f"  Saved {story} wav.npy shape={audio.shape}", flush=True)
    except Exception as e:
        print(f"  FAILED resample {story}: {e}", flush=True)
        failed_audio.append(story)

print(f"\nAudio done: {len(succeeded_audio)} ok, {len(failed_audio)} failed")
if failed_audio:
    print("  Failed:", failed_audio)

# ---------------------------------------------------------------------------
# Step 3: Build grids_huge.jbl from local TextGrid files
# ---------------------------------------------------------------------------
GRIDS_PATH = f"{STORY_DATA_DIR}/grids_huge.jbl"
if os.path.exists(GRIDS_PATH):
    print("grids_huge.jbl already exists, loading to verify...")
    grids = joblib.load(GRIDS_PATH)
else:
    print("Building grids_huge.jbl ...", flush=True)
    grids = {}
    for story in STORIES:
        tg_path = f"{TEXTGRID_DIR}/{story}.TextGrid"
        if os.path.exists(tg_path):
            grids[story] = TextGrid(open(tg_path).read())
        else:
            print(f"  WARNING: no TextGrid for {story}")
    joblib.dump(grids, GRIDS_PATH)
    print(f"  Saved grids_huge.jbl ({len(grids)} stories)")

# ---------------------------------------------------------------------------
# Step 4: Build trfiles_huge.jbl by simulating from fMRI TR counts
# ---------------------------------------------------------------------------
# Strategy: for each story, get the number of TRs from the fMRI data (UTS03
# has all 84 stories). Simulate a TRFile: start=10s (trim_start), TR=2.0045.
# The fMRI data is already trimmed (trim_start=10, trim_end=5 are applied in
# dataset.py AFTER loading), so the raw hf5 has trim_start+trim_end extra TRs.
# Actually dataset.py loads the full story and trims via delayed_wav[trim_start:-trim_end].
# The TRFile times are fed into DataSequence.from_grid via wordseqs[story].tr_times.
# We need tr_times to have length == fMRI shape[0] (untrimmed).
TRFILES_PATH = f"{STORY_DATA_DIR}/trfiles_huge.jbl"
if os.path.exists(TRFILES_PATH):
    print("trfiles_huge.jbl already exists, loading to verify...")
    trfiles = joblib.load(TRFILES_PATH)
else:
    print("Building trfiles_huge.jbl ...", flush=True)
    trfiles = {}
    fmri_sub = "UTS03"  # has all 84 stories
    fmri_subdir = f"{FMRI_DIR}/{fmri_sub}"
    for story in STORIES:
        hf5_path = f"{fmri_subdir}/{story}.hf5"
        if not os.path.exists(hf5_path):
            print(f"  WARNING: no fMRI for {story} in {fmri_sub}, skipping TRFile")
            continue
        with h5py.File(hf5_path) as f:
            ntrs = f['data'].shape[0]

        # Simulate: sound starts at 10s (= trim_start * TR), ntrs TRs total
        trf = TRFile(None, expectedtr=TR)
        trf.soundstarttime = TRIM_START * TR  # ~20s
        trf.simulate(ntrs)  # ntrs evenly spaced TRs at expectedtr
        # soundstoptime: rough estimate (not critical for tr_times usage)
        trf.soundstoptime = trf.soundstarttime + ntrs * TR
        trfiles[story] = [trf]

    joblib.dump(trfiles, TRFILES_PATH)
    print(f"  Saved trfiles_huge.jbl ({len(trfiles)} stories)")

print(f"\ngrids: {len(grids)} stories")
print(f"trfiles: {len(trfiles)} stories")
stories_with_all = set(grids) & set(trfiles) & set(succeeded_audio)
print(f"Stories fully assembled (audio + grid + fMRI): {len(stories_with_all)}")

# ---------------------------------------------------------------------------
# Step 5: End-to-end load test via FMRIStory
# ---------------------------------------------------------------------------
# We need to patch dataset.py's module-level paths before import.
# dataset.py does a module-level joblib.load at import time — override that.
import unittest.mock as mock

STORY_TEST = "adollshouse"
SUBJECT_TEST = 3  # UTS03 has all 84 stories

print(f"\n=== End-to-end test: {STORY_TEST}, subject {SUBJECT_TEST} ===")

# dataset.py imports grids/trfiles at module level from hardcoded paths.
# Patch joblib.load to return our objects, then import the module.
import importlib

_orig_load = joblib.load
def _patched_load(path, *a, **kw):
    if "grids_huge" in str(path):
        return grids
    if "trfiles_huge" in str(path):
        return trfiles
    return _orig_load(path, *a, **kw)

with mock.patch("joblib.load", side_effect=_patched_load):
    import dataset as ds_module
    importlib.reload(ds_module)  # reload so module-level code reruns with patch

print(f"dataset.py wordseqs keys (first 5): {list(ds_module.wordseqs.keys())[:5]}")

# Instantiate the dataset with patched paths
dataset = ds_module.FMRIStory(
    story_name=STORY_TEST,
    subject=SUBJECT_TEST,
    read_stim_dir=STIM_DIR,
    read_fmri_dir=f"{FMRI_DIR}",
    chunksz_sec=1,
    contextsz_sec=0,
    sampling_rate=TARGET_SR,
)

# Call fetch_data which loads fMRI and aligns
dataset.fetch_data()

print(f"\nRESULT:")
print(f"  audio tensor shape (delayed_wav):  {dataset.delayed_wav.shape}")
print(f"  fMRI tensor shape:                 {dataset.fmri_tensor.shape}")
assert dataset.delayed_wav.shape[0] == dataset.fmri_tensor.shape[0], \
    f"MISMATCH: wav {dataset.delayed_wav.shape[0]} != fmri {dataset.fmri_tensor.shape[0]}"
print(f"  Time dims MATCH: {dataset.delayed_wav.shape[0]} TRs")
print(f"  Dataset length (__len__): {len(dataset)}")
print(f"\n>>> END-TO-END TEST PASSED <<<")
