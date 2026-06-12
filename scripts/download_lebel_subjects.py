"""Download a story subset for additional LeBel deep subjects (UTS01, UTS02) from the
public OpenNeuro ds003020 S3 bucket (unsigned) — enables the multi-subject per-individual
voxelwise test (E012). Mirrors the stories UTS03 already has locally.

Run: uv run python scripts/download_lebel_subjects.py --subjects UTS01 UTS02 --n-stories 20
"""
import argparse
from pathlib import Path

import boto3
from botocore import UNSIGNED
from botocore.config import Config

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "data/lebel_ds003020/preprocessed_data"
BUCKET = "openneuro.org"
PREFIX = "ds003020/derivatives/preprocessed_data"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", nargs="+", default=["UTS01", "UTS02"])
    ap.add_argument("--n-stories", type=int, default=20)
    args = ap.parse_args()

    stories = sorted(p.name for p in (LOCAL / "UTS03").glob("*.hf5"))[:args.n_stories]
    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    print(f"mirroring {len(stories)} stories for {args.subjects}")
    for subj in args.subjects:
        outdir = LOCAL / subj
        outdir.mkdir(parents=True, exist_ok=True)
        for st in stories:
            dst = outdir / st
            if dst.exists() and dst.stat().st_size > 1_000_000:
                print(f"  [{subj}/{st}] exists, skip"); continue
            key = f"{PREFIX}/{subj}/{st}"
            try:
                s3.download_file(BUCKET, key, str(dst))
                print(f"  [{subj}/{st}] OK ({dst.stat().st_size/1e6:.0f} MB)", flush=True)
            except Exception as e:
                print(f"  [{subj}/{st}] FAIL: {type(e).__name__} {e}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
