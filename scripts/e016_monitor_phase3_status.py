#!/usr/bin/env python3
"""Periodic renderer for E016 Phase-3 status snapshots.

This is a monitor wrapper only: it does not launch training, analyze results, or
adjudicate a claim. It repeatedly calls the read-only E016 status helper and
writes a latest JSON plus a compact Markdown status page.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def run_status(args: argparse.Namespace) -> dict[str, Any]:
    cmd = [
        "uv",
        "run",
        "python",
        "scripts/e016_phase3_status.py",
        "--log",
        str(args.phase3_log),
        "--run-json",
        str(args.run_json),
        "--analysis-json",
        str(args.analysis_json),
        "--run-script",
        str(args.run_script),
    ]
    if args.train_cache is not None:
        cmd.extend(["--train-cache", str(args.train_cache)])
    if args.heldout_cache is not None:
        cmd.extend(["--heldout-cache", str(args.heldout_cache)])
    proc = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(proc.stdout)


def artifact_row(path: Path) -> str:
    resolved = resolve(path)
    if not resolved.exists():
        return f"- missing: `{path}`"
    size = resolved.stat().st_size
    mtime = datetime.fromtimestamp(resolved.stat().st_mtime, tz=timezone.utc).isoformat()
    return f"- present: `{path}` ({size} bytes, mtime `{mtime}`)"


def render_markdown(payload: dict[str, Any], required_artifacts: list[Path]) -> str:
    health = payload.get("health") or {}
    log = payload.get("log") or {}
    progress = log.get("training_progress") or {}
    active = progress.get("active_arm")
    latest = progress.get("latest_completed_arm")
    gpu = payload.get("gpu") or {}
    processes = payload.get("processes") or []

    lines = [
        "# E016 Rerun Status",
        "",
        f"- checked_at_utc: `{payload.get('checked_at_utc')}`",
        f"- phase: `{payload.get('phase')}`",
        f"- health: `{health.get('status')}`",
        f"- runner_elapsed_s_max: `{health.get('runner_elapsed_s_max')}`",
        f"- log_quiet_s: `{health.get('log_quiet_s')}`",
        f"- process_count: `{health.get('process_count')}`",
        f"- runner_process_count: `{health.get('runner_process_count')}`",
        f"- completed_arms: `{progress.get('completed_arm_count')}/{progress.get('arms_expected')}`",
        f"- active_arm: `{active}`",
        f"- latest_completed_arm: `{latest}`",
        f"- max_gpu_utilization_pct: `{gpu.get('max_utilization_gpu_pct')}`",
        "",
        "## Processes",
        "",
    ]
    if processes:
        for proc in processes:
            lines.append(
                f"- pid `{proc.get('pid')}`, elapsed `{proc.get('elapsed')}`, "
                f"stat `{proc.get('stat')}`"
            )
    else:
        lines.append("- none discovered for selected run")

    lines.extend(["", "## Required Artifacts", ""])
    if required_artifacts:
        lines.extend(artifact_row(path) for path in required_artifacts)
    else:
        lines.append("- none listed")

    tail = log.get("tail") or []
    lines.extend(["", "## Log Tail", "", "```text"])
    lines.extend(str(line) for line in tail[-12:])
    lines.extend(
        [
            "```",
            "",
            "Status only. Partial-arm diagnostics are not E016 verdicts and do not clear a paper claim.",
            "",
        ]
    )
    return "\n".join(lines)


def write_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    payload = run_status(args)
    latest_json = resolve(args.latest_json)
    latest_md = resolve(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(render_markdown(payload, args.required_artifact), encoding="utf-8")
    return payload


def should_stop(payload: dict[str, Any], *, stop_when_analysis_ready: bool) -> bool:
    if not stop_when_analysis_ready:
        return False
    return payload.get("phase") in {"analysis_ready", "analysis_blocked_or_incomplete"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase3-log", type=Path, required=True)
    ap.add_argument("--run-json", type=Path, required=True)
    ap.add_argument("--analysis-json", type=Path, required=True)
    ap.add_argument("--run-script", type=Path, required=True)
    ap.add_argument("--train-cache", type=Path)
    ap.add_argument("--heldout-cache", type=Path)
    ap.add_argument("--latest-json", type=Path, required=True)
    ap.add_argument("--latest-md", type=Path, required=True)
    ap.add_argument("--required-artifact", type=Path, action="append", default=[])
    ap.add_argument("--interval-s", type=int, default=300)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--stop-when-analysis-ready", action="store_true")
    args = ap.parse_args()

    while True:
        payload = write_snapshot(args)
        if args.once or should_stop(payload, stop_when_analysis_ready=args.stop_when_analysis_ready):
            break
        time.sleep(args.interval_s)


if __name__ == "__main__":
    main()
