#!/usr/bin/env python3
"""Wait for the E016 full Phase-3 run JSON, then run the guarded finalizer.

By default this checks once and exits. Pass --watch to poll until the run JSON
appears or --max-wait-s expires. This wrapper never interprets a result; it only
hands the completed artifact to e016_finalize_phase3.py.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from e016_phase3_status import ROOT, RUN_JSON

FINALIZER = ROOT / "scripts/e016_finalize_phase3.py"


def absolutize(path: Path | None) -> Path | None:
    if path is None:
        return None
    return path if path.is_absolute() else (Path.cwd() / path).resolve()


def waiting_packet(run_json: Path, *, watch: bool, interval_s: int, max_wait_s: int | None) -> dict[str, Any]:
    return {
        "science_status": "watch status only; not a verdict or rung flip",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "waiting_for_run_json",
        "run_json": str(run_json),
        "run_json_exists": run_json.exists(),
        "watch": watch,
        "interval_s": interval_s if watch else None,
        "max_wait_s": max_wait_s if watch else None,
        "next_action": (
            "Keep watching until the run JSON appears, then run the guarded finalizer."
            if watch
            else "Stay in /work and monitor with scripts/e016_phase3_status.py."
        ),
    }


def run_finalizer(args: argparse.Namespace, run_json: Path) -> None:
    cmd = [sys.executable, str(FINALIZER), "--run-json", str(run_json)]
    for flag, value in (
        ("--analysis-json", args.analysis_json),
        ("--readiness-json", args.readiness_json),
        ("--comparison-json", args.comparison_json),
        ("--out", args.out),
    ):
        if value is not None:
            cmd.extend([flag, str(value)])
    if args.force:
        cmd.append("--force")
    print("$ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-json", type=Path, default=RUN_JSON)
    ap.add_argument("--analysis-json", type=Path, default=None)
    ap.add_argument("--readiness-json", type=Path, default=None)
    ap.add_argument("--comparison-json", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None, help="Optional finalizer status packet path.")
    ap.add_argument("--force", action="store_true", help="Pass --force through to e016_finalize_phase3.py.")
    ap.add_argument("--watch", action="store_true", help="Poll until the run JSON exists or --max-wait-s expires.")
    ap.add_argument("--interval-s", type=int, default=300, help="Polling interval when --watch is set.")
    ap.add_argument("--max-wait-s", type=int, default=None, help="Maximum watch duration; omit for no limit.")
    args = ap.parse_args()

    run_json = absolutize(args.run_json)
    assert run_json is not None
    args.analysis_json = absolutize(args.analysis_json)
    args.readiness_json = absolutize(args.readiness_json)
    args.comparison_json = absolutize(args.comparison_json)
    args.out = absolutize(args.out)

    if args.interval_s <= 0:
        raise SystemExit("--interval-s must be positive")
    if args.max_wait_s is not None and args.max_wait_s < 0:
        raise SystemExit("--max-wait-s must be non-negative")

    start = time.monotonic()
    while True:
        if run_json.exists():
            run_finalizer(args, run_json)
            return

        packet = waiting_packet(run_json, watch=args.watch, interval_s=args.interval_s, max_wait_s=args.max_wait_s)
        print(json.dumps(packet, indent=2), flush=True)

        if not args.watch:
            return
        sleep_s: float = float(args.interval_s)
        if args.max_wait_s is not None:
            remaining_s = args.max_wait_s - (time.monotonic() - start)
            if remaining_s <= 0:
                return
            sleep_s = min(sleep_s, remaining_s)
        time.sleep(sleep_s)


if __name__ == "__main__":
    main()
