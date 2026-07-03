#!/usr/bin/env python3
"""Guarded E016 Phase-3 finalizer.

This helper is intentionally procedural: if the full run JSON is absent, it
prints a monitor packet and exits cleanly. If the run JSON is present, it runs
the conservative analyzer and then builds the readiness packet for /interpret.
It is not a verdict engine.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from e016_phase3_status import ANALYSIS_JSON, ROOT, RUN_JSON
from e016_make_readiness_packet import out_path_for

ANALYZER = ROOT / "scripts/analyze_tribe_phase3.py"
READINESS_BUILDER = ROOT / "scripts/e016_make_readiness_packet.py"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return data


def analysis_path_for(run_json: Path) -> Path:
    if run_json == RUN_JSON:
        return ANALYSIS_JSON
    return run_json.with_suffix(".analysis.json")


def absolutize(path: Path | None) -> Path | None:
    if path is None:
        return None
    return path if path.is_absolute() else (Path.cwd() / path).resolve()


def run_step(cmd: list[str]) -> None:
    print("$ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT)


def stale(output: Path, inputs: list[Path]) -> bool:
    if not output.exists():
        return True
    out_mtime = output.stat().st_mtime
    return any(path.exists() and path.stat().st_mtime > out_mtime for path in inputs)


def summary_packet(
    *,
    run_json: Path,
    analysis_json: Path,
    readiness_json: Path,
    status: str,
    next_action: str,
) -> dict[str, Any]:
    packet: dict[str, Any] = {
        "science_status": "finalizer status only; not a verdict or rung flip",
        "status": status,
        "run_json": str(run_json),
        "run_json_exists": run_json.exists(),
        "analysis_json": str(analysis_json),
        "analysis_json_exists": analysis_json.exists(),
        "readiness_json": str(readiness_json),
        "readiness_json_exists": readiness_json.exists(),
        "next_action": next_action,
    }
    if analysis_json.exists():
        analysis = load_json(analysis_json)
        packet["gate"] = analysis.get("gate")
        packet["paper_branch_hint"] = analysis.get("paper_branch_hint")
    if readiness_json.exists():
        readiness = load_json(readiness_json)
        packet["readiness_next_actions"] = readiness.get("next_actions")
        packet["reviewer_burden_flags"] = readiness.get("reviewer_burden_flags")
    return packet


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-json", type=Path, default=RUN_JSON)
    ap.add_argument("--analysis-json", type=Path, default=None)
    ap.add_argument("--readiness-json", type=Path, default=None)
    ap.add_argument("--comparison-json", type=Path, default=None)
    ap.add_argument("--force", action="store_true", help="Regenerate analyzer/readiness artifacts even if present.")
    ap.add_argument("--out", type=Path, default=None, help="Optional status packet path.")
    args = ap.parse_args()

    run_json = absolutize(args.run_json)
    assert run_json is not None
    analysis_json = absolutize(args.analysis_json) or analysis_path_for(run_json)
    readiness_json = absolutize(args.readiness_json) or out_path_for(analysis_json)
    comparison_json = absolutize(args.comparison_json)
    out_path = absolutize(args.out)

    if not run_json.exists():
        packet = summary_packet(
            run_json=run_json,
            analysis_json=analysis_json,
            readiness_json=readiness_json,
            status="run_json_missing",
            next_action="Stay in /work and monitor with scripts/e016_phase3_status.py.",
        )
        text = json.dumps(packet, indent=2)
        print(text)
        if out_path:
            out_path.write_text(text + "\n", encoding="utf-8")
        return

    if args.force or stale(analysis_json, [run_json]):
        run_step(
            [
                sys.executable,
                str(ANALYZER),
                str(run_json),
                "--out",
                str(analysis_json),
            ]
        )

    readiness_cmd = [
        sys.executable,
        str(READINESS_BUILDER),
        str(analysis_json),
        "--out",
        str(readiness_json),
    ]
    if comparison_json is not None:
        readiness_cmd.extend(["--comparison-json", str(comparison_json)])
    readiness_inputs = [analysis_json]
    if comparison_json is not None:
        readiness_inputs.append(comparison_json)
    if args.force or stale(readiness_json, readiness_inputs):
        run_step(readiness_cmd)

    packet = summary_packet(
        run_json=run_json,
        analysis_json=analysis_json,
        readiness_json=readiness_json,
        status="finalized_for_interpretation_handoff",
        next_action="Read the readiness packet, then switch to /interpret if gate.science_ready is true.",
    )
    text = json.dumps(packet, indent=2)
    print(text)
    if out_path:
        out_path.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
