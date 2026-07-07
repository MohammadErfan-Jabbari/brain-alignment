#!/usr/bin/env python3
"""Wait for an E016 artifacted run, then score saved students on Tuckute.

This is postprocess glue only. It does not launch training, analyze contrasts,
or adjudicate a claim. It waits for the selected run JSON to exist, waits until
the selected `run_tribe_phase3.py` process is no longer discovered by the
read-only status helper, then invokes `e016_eval_saved_student_alignment.py`.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel_for_repo(path: Path) -> str:
    resolved = resolve(path)
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_status(args: argparse.Namespace) -> dict[str, Any]:
    cmd = [
        "uv",
        "run",
        "python",
        "scripts/e016_phase3_status.py",
        "--log",
        rel_for_repo(args.phase3_log),
        "--run-json",
        rel_for_repo(args.run_json),
        "--analysis-json",
        rel_for_repo(args.analysis_json),
        "--run-script",
        rel_for_repo(args.run_script),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(proc.stdout)


def runner_count(payload: dict[str, Any]) -> int:
    health = payload.get("health") or {}
    return int(health.get("runner_process_count") or 0)


def run_eval(args: argparse.Namespace) -> None:
    cmd = [
        "uv",
        "run",
        "python",
        "scripts/e016_eval_saved_student_alignment.py",
        "--run-json",
        rel_for_repo(args.run_json),
        "--out",
        rel_for_repo(args.out),
        "--reference-model",
        args.reference_model,
    ]
    if args.require_artifacts:
        cmd.append("--require-artifacts")
    env = os.environ.copy()
    env.setdefault("HF_HOME", "/home/centcom/data/hf-cache")
    if args.cuda_visible_devices:
        env["CUDA_VISIBLE_DEVICES"] = args.cuda_visible_devices
    print(f"[{stamp()}] running: {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=ROOT, env=env, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-json", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--phase3-log", type=Path, required=True)
    ap.add_argument("--analysis-json", type=Path, required=True)
    ap.add_argument("--run-script", type=Path, required=True)
    ap.add_argument("--reference-model", default="gpt2-medium")
    ap.add_argument("--cuda-visible-devices", default="1")
    ap.add_argument("--interval-s", type=int, default=300)
    ap.add_argument("--settle-s", type=int, default=60)
    ap.add_argument("--require-artifacts", action="store_true")
    args = ap.parse_args()

    run_json = resolve(args.run_json)
    out = resolve(args.out)

    print(f"[{stamp()}] waiting for run JSON {run_json}", flush=True)
    while not run_json.is_file() or run_json.stat().st_size == 0:
        if out.is_file() and out.stat().st_size > 0:
            print(f"[{stamp()}] output already exists before run JSON wait finished: {out}", flush=True)
            return
        time.sleep(args.interval_s)

    print(f"[{stamp()}] detected run JSON; waiting for selected runner to exit", flush=True)
    while True:
        payload = run_status(args)
        count = runner_count(payload)
        print(
            f"[{stamp()}] phase={payload.get('phase')} runner_process_count={count}",
            flush=True,
        )
        if count == 0:
            break
        time.sleep(args.interval_s)

    if args.settle_s > 0:
        print(f"[{stamp()}] runner cleared; settling for {args.settle_s}s", flush=True)
        time.sleep(args.settle_s)

    if out.is_file() and out.stat().st_size > 0:
        print(f"[{stamp()}] output already exists: {out}", flush=True)
        return

    run_eval(args)
    print(f"[{stamp()}] Tuckute evaluation complete: {out}", flush=True)


if __name__ == "__main__":
    main()
