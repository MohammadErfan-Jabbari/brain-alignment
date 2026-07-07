#!/usr/bin/env python3
"""Periodic renderer for the E016 combined Tuckute gate status.

This is a monitor wrapper only. It repeatedly calls the read-only gate helper
and writes a latest JSON plus compact Markdown status page. It does not launch
training, score Tuckute, run the combined analyzer/audit, adjudicate a claim, or
flip a rung.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import e016_tuckute_gate_status as gate


ROOT = Path(__file__).resolve().parents[1]


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def build_gate_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        run_json=args.run_json,
        phase3_log=args.phase3_log,
        phase3_analysis_json=args.phase3_analysis_json,
        run_script=args.run_script,
        rerun_tuckute=args.rerun_tuckute,
        existing_tribe_tuckute=args.existing_tribe_tuckute,
        textfeat_tuckute=args.textfeat_tuckute,
        analysis_json=args.analysis_json,
        audit_json=args.audit_json,
    )


def write_snapshot(args: argparse.Namespace) -> dict:
    payload = gate.build_payload(build_gate_args(args))
    latest_json = resolve(args.latest_json)
    latest_md = resolve(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)
    latest_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    latest_md.write_text(gate.render_markdown(payload), encoding="utf-8")
    return payload


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-json", type=Path, default=gate.DEFAULT_RUN_JSON)
    ap.add_argument("--phase3-log", type=Path, default=gate.DEFAULT_PHASE3_LOG)
    ap.add_argument("--phase3-analysis-json", type=Path, default=gate.DEFAULT_PHASE3_ANALYSIS_JSON)
    ap.add_argument("--run-script", type=Path, default=gate.DEFAULT_RUN_SCRIPT)
    ap.add_argument("--rerun-tuckute", type=Path, default=gate.DEFAULT_RERUN_TUCKUTE)
    ap.add_argument("--existing-tribe-tuckute", type=Path, default=gate.DEFAULT_EXISTING_TRIBE_TUCKUTE)
    ap.add_argument("--textfeat-tuckute", type=Path, default=gate.DEFAULT_TEXTFEAT_TUCKUTE)
    ap.add_argument("--analysis-json", type=Path, default=gate.DEFAULT_ANALYSIS_JSON)
    ap.add_argument("--audit-json", type=Path, default=gate.DEFAULT_AUDIT_JSON)
    ap.add_argument("--latest-json", type=Path, required=True)
    ap.add_argument("--latest-md", type=Path, required=True)
    ap.add_argument("--interval-s", type=int, default=300)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--stop-when-ready", action="store_true")
    args = ap.parse_args()

    while True:
        payload = write_snapshot(args)
        if args.once or (args.stop_when_ready and payload.get("ready_for_interpret")):
            break
        time.sleep(args.interval_s)


if __name__ == "__main__":
    main()
