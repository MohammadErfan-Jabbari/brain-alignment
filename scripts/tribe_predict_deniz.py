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


def _build_events_correct(audio_path: str):
    """Faithful replacement for TribeModel.get_events_dataframe(audio_path=...) that fixes
    TRIBE's long-audio bug WITHOUT triggering w2v-bert OOM.

    TRIBE's get_audio_and_text_events does [ChunkEvents(60s) → ExtractWordsFromAudio → …].
    The bug: ExtractWordsFromAudio cross-joins the FULL whisperx transcript onto EVERY 60s
    chunk and adds `start+offset` (chunk position double-counted) → ~N× word duplication and
    a ~2.8x time stretch (591s of speech → 1671s of events for the 602s denizenslab story).
    Making it a single huge chunk fixes timing but OOMs w2v-bert (O(T²) self-attention over
    ~591s). So we REORDER: run ExtractWordsFromAudio on the UN-chunked audio first (one event,
    offset 0 → correct absolute word timestamps 0–591s, no duplication), THEN ChunkEvents(60s)
    to split only the Audio rows for the w2v-bert extractor (memory-safe). whisperx is reused
    from its cached .tsv. The text-context transforms then run on the correct words."""
    import pandas as pd
    from tribev2.demo_utils import (
        ExtractAudioFromVideo, ChunkEvents, ExtractWordsFromAudio, AddText,
        AddSentenceToWords, AddContextToWords, RemoveMissing, standardize_events,
    )
    ev = pd.DataFrame([{"type": "Audio", "filepath": audio_path, "start": 0,
                        "timeline": "default", "subject": "default"}])
    ev = standardize_events(ev)
    ev = ExtractAudioFromVideo()(ev)
    ev = ExtractWordsFromAudio()(ev)            # words on UN-chunked audio → correct 0–591s
    ev = ChunkEvents(event_type_to_chunk="Audio", max_duration=60, min_duration=30)(ev)  # chunk Audio for w2v-bert
    ev = AddText()(ev)
    ev = AddSentenceToWords(max_unmatched_ratio=0.05)(ev)
    ev = AddContextToWords(sentence_only=False, max_context_len=1024, split_field="")(ev)
    ev = RemoveMissing()(ev)
    return standardize_events(ev)


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
        # TRIBE's audio loader mis-times 44.1 kHz stereo (computes timestamps as if 16 kHz
        # → ~2.76x stretch). Pre-resample to 16 kHz mono PCM (what whisperx/w2v-bert expect).
        wav16 = Path(CACHE) / f"story_{st}_16k.wav"
        if not wav16.exists():
            import subprocess
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav),
                            "-ar", "16000", "-ac", "1", str(wav16)], check=True)
        print(f"=== story_{st}: events (audio path, 16kHz, single-chunk) ===", flush=True)
        events = _build_events_correct(str(wav16))
        try:
            print(f"  [events] start span [{events['start'].astype(float).min():.1f},"
                  f"{events['start'].astype(float).max():.1f}]s (expect ~602)", flush=True)
        except Exception:  # noqa
            pass
        print(f"  events {events.shape}; predict...", flush=True)
        # Save word-level events (wav clock) for the low-level-encoder floor (same clock
        # as preds → a single lag aligns both to real BOLD). Best-effort column subset.
        try:
            cols = [c for c in ["text", "word", "start", "duration", "type", "onset", "offset"]
                    if c in events.columns]
            events[cols].to_csv(outdir / f"story_{st}_events.csv", index=False)
        except Exception as ex:  # noqa
            print(f"  (events save skipped: {ex})", flush=True)
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
