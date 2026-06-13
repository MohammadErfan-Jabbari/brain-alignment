#!/usr/bin/env python3
"""Generate TRIBE-v2 synthetic fMRI for denizenslab stories (E016 F1/F2).

RUNS IN THE ISOLATED .venv-tribe (torch 2.6, custom Meta deps) — NEVER the thesis venv.
Hand-off to the thesis pipeline is by disk (.npz). For each story we feed the REAL
story audio (denizenslab .wav) so TRIBE uses w2v-bert audio + Llama-from-ASR text (the
faithful multimodal prediction; no gTTS synthesis). `from_pretrained` hardcodes
`config["average_subjects"]=True` (demo_utils.py:218) → TRIBE predicts the group-averaged
E[Y|S] (no subject axis; P0 output (T,20484)). This is the exact §2 quantity. We assert
the 20484 width below so a config change can't silently swap the estimand (oracle F3).

remove_empty_segments=False → preds are CONTIGUOUS at TRIBE's TR from t=0 (story audio
start), so the time axis is clean (preds[i] ↔ t = i*TR_tribe). Temporal alignment to the
real fMRI TR grid (incl. the leading-silence offset) is done downstream in the thesis
venv with an explicit lag-search — see scripts/run_tribe_fidelity.py.

Usage (from data/paper-repos/tribev2, with .venv-tribe):
    .venv-tribe/bin/python /abs/path/scripts/tribe_predict_deniz.py --stories 11 01 02 \
        [--features audio,video]   # omit for full (text+audio); set for the no-text ablation
"""
import argparse
import sys
from pathlib import Path

import numpy as np

THESIS = Path("/home/centcom/data/brain-alignment")
STIM = THESIS / "data/denizenslab/stimuli"
OUT = THESIS / "outputs/E016_tribe/deniz"
CACHE = "/home/centcom/data/tribe_cache"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stories", nargs="+", required=True, help="story numbers, e.g. 11 01 02")
    ap.add_argument("--features", default=None,
                    help="comma list to restrict extractors, e.g. 'audio,video' for the "
                         "no-text ablation; default None = full (text+audio for an audio input)")
    ap.add_argument("--tag", default=None, help="output subfolder tag (default: full / notext)")
    args = ap.parse_args()

    sys.path.insert(0, ".")
    from tribev2.demo_utils import TribeModel

    cfg = {"data.text_feature.model_name": "unsloth/Llama-3.2-3B"}
    if args.features is not None:
        feats = [f.strip() for f in args.features.split(",")]
        cfg["data.features_to_use"] = feats
        print(f"[ablation] features_to_use = {feats}", flush=True)
    tag = args.tag or ("notext" if args.features else "full")
    outdir = OUT / tag
    outdir.mkdir(parents=True, exist_ok=True)

    print("=== loading facebook/tribev2 ===", flush=True)
    model = TribeModel.from_pretrained(
        "facebook/tribev2", cache_folder=CACHE, config_update=cfg,
    )
    model.remove_empty_segments = False  # contiguous time axis from t=0
    TR = float(model.data.TR)
    print(f"TRIBE TR = {TR:.4f}s; features_to_use = "
          f"{getattr(model.data, 'features_to_use', 'default')}", flush=True)

    for st in args.stories:
        wav = STIM / f"story_{st}.wav"
        if not wav.is_file():
            print(f"  [story_{st}] MISSING {wav}", flush=True); continue
        dst = outdir / f"story_{st}_pred.npz"
        if dst.exists():
            print(f"  [story_{st}] exists, skip", flush=True); continue
        print(f"=== story_{st}: events (audio path) ===", flush=True)
        events = model.get_events_dataframe(audio_path=str(wav))
        print(f"  events {events.shape}; predict...", flush=True)
        preds, segs = model.predict(events)   # (n_seg, 20484) contiguous
        assert preds.ndim == 2 and preds.shape[1] == 20484, (
            f"expected E[Y|S] group prediction (T,20484); got {preds.shape} — "
            "average_subjects may have been overridden (oracle F3)")
        t_grid = np.arange(preds.shape[0]) * TR
        np.savez_compressed(
            dst, preds=preds.astype(np.float32), tr=TR, t_grid=t_grid.astype(np.float32),
            features=str(cfg.get("data.features_to_use", "full")),
        )
        print(f"  [story_{st}] SAVED {dst.name} preds {preds.shape} "
              f"BOLD mean {float(preds.mean()):.4f} std {float(preds.std()):.4f}", flush=True)
    print("=== DONE ===", flush=True)


if __name__ == "__main__":
    main()
