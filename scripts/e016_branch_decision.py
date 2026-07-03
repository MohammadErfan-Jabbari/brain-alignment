#!/usr/bin/env python3
"""Route the next E016 action from finalizer/readiness artifacts.

This is a post-run decision aid, not a verdict engine. It never launches
training and never interprets a science result; it only names the next safe
command or stance from artifact state.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from e016_make_readiness_packet import out_path_for
from e016_phase3_status import ANALYSIS_JSON, ROOT, RUN_JSON, discover_processes

DEFAULT_TEXTFEAT_LAUNCHER = ROOT / "outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh"

POST_COMPARE_BURDEN_NOTE = (
    "If the later comparator says TRIBE is stronger than textfeat, switch to /interpret and clear the "
    "post-positive burden from docs/top-venue-privileged-signal-adjacency-audit-2026-07-03.md. Textfeat is a "
    "sentence-local frozen-LM hidden-state target; beating it is not by itself long-context/on-policy or "
    "real-brain clearance."
)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return data


def absolutize(path: Path | None) -> Path | None:
    if path is None:
        return None
    return path if path.is_absolute() else (Path.cwd() / path).resolve()


def stale(output: Path, inputs: list[Path]) -> bool:
    if not output.exists():
        return True
    out_mtime = output.stat().st_mtime
    return any(path.exists() and path.stat().st_mtime > out_mtime for path in inputs)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def command_for(*parts: str | Path) -> str:
    return " ".join(str(part) for part in parts)


def active_runner_processes() -> list[dict[str, Any]]:
    return [
        proc
        for proc in discover_processes()
        if "run_tribe_phase3.py" in str(proc.get("cmd", "")) or "run_full_phase3_20260702.sh" in str(proc.get("cmd", ""))
    ]


def base_packet(run_json: Path, analysis_json: Path, readiness_json: Path, textfeat_launcher: Path) -> dict[str, Any]:
    return {
        "science_status": "branch routing only; not a verdict or rung flip",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_json": str(run_json),
        "run_json_exists": run_json.exists(),
        "analysis_json": str(analysis_json),
        "analysis_json_exists": analysis_json.exists(),
        "readiness_json": str(readiness_json),
        "readiness_json_exists": readiness_json.exists(),
        "textfeat_launcher": str(textfeat_launcher),
        "textfeat_launcher_exists": textfeat_launcher.exists(),
        "must_not_claim": [
            "Do not claim an E016 result from this router.",
            "Do not claim brain specificity from TRIBE alone.",
            "Do not treat TRIBE>textfeat as brain-specific clearance without post-positive review and adjacency-burden follow-up.",
            "Do not run textfeat while the active TRIBE job is still consuming resources.",
            "Do not flip a ladder rung from this router.",
        ],
    }


def missing_run_packet(packet: dict[str, Any]) -> dict[str, Any]:
    packet.update(
        {
            "status": "waiting_for_run_json",
            "route": "monitor",
            "reason": "The full E016 run JSON is absent.",
            "recommended_commands": [
                command_for("uv", "run", "python", "scripts/e016_phase3_status.py", "--pretty"),
                command_for(
                    "uv",
                    "run",
                    "python",
                    "scripts/e016_watch_finalize_phase3.py",
                    "--run-json",
                    packet["run_json"],
                    "--watch",
                    "--interval-s",
                    "300",
                ),
            ],
        }
    )
    return packet


def needs_finalizer_packet(packet: dict[str, Any], reason: str) -> dict[str, Any]:
    packet.update(
        {
            "status": "needs_finalizer",
            "route": "finalize",
            "reason": reason,
            "recommended_commands": [
                command_for(
                    "uv",
                    "run",
                    "python",
                    "scripts/e016_finalize_phase3.py",
                    "--run-json",
                    packet["run_json"],
                    "--analysis-json",
                    packet["analysis_json"],
                    "--readiness-json",
                    packet["readiness_json"],
                ),
            ],
        }
    )
    return packet


def readiness_branch(readiness: dict[str, Any]) -> str:
    hint = readiness.get("paper_branch_hint")
    if isinstance(hint, dict):
        branch = hint.get("branch")
        if isinstance(branch, str):
            return branch
    return "missing"


def readiness_science_ready(readiness: dict[str, Any]) -> bool:
    gate = readiness.get("gate")
    return bool(isinstance(gate, dict) and gate.get("science_ready"))


def route_ready_packet(packet: dict[str, Any], readiness: dict[str, Any], textfeat_launcher: Path) -> dict[str, Any]:
    branch = readiness_branch(readiness)
    packet["readiness_branch"] = branch
    packet["readiness_next_actions"] = readiness.get("next_actions")
    packet["reviewer_burden_flags"] = readiness.get("reviewer_burden_flags")
    packet["gate"] = readiness.get("gate")
    packet["failed_gate_fields"] = readiness.get("failed_gate_fields")

    if not readiness_science_ready(readiness):
        packet.update(
            {
                "status": "not_science_ready",
                "route": "debug_or_complete_gate",
                "reason": "The readiness packet says gate.science_ready is false.",
                "recommended_commands": [
                    command_for("uv", "run", "python", "scripts/e016_phase3_status.py", "--pretty"),
                    command_for(
                        "uv",
                        "run",
                        "python",
                        "scripts/e016_finalize_phase3.py",
                        "--run-json",
                        packet["run_json"],
                        "--analysis-json",
                        packet["analysis_json"],
                        "--readiness-json",
                        packet["readiness_json"],
                        "--force",
                    ),
                ],
            }
        )
        return packet

    if branch == "controlled_null_candidate":
        packet.update(
            {
                "status": "ready_for_interpret_controlled_null",
                "route": "interpret",
                "reason": "TRIBE did not clear the KD/permuted contrasts under the analyzer branch hint.",
                "recommended_commands": [],
                "recommended_stance": "/interpret",
            }
        )
        return packet

    if branch == "tribe_positive_needs_textfeat":
        runners = active_runner_processes()
        packet.update(
            {
                "status": "textfeat_control_required",
                "route": "run_textfeat_after_resource_check",
                "reason": "TRIBE-only positive cannot support brain specificity; matched-information control is required.",
                "active_runner_process_count": len(runners),
                "active_runner_processes": runners,
                "post_compare_burden_note": POST_COMPARE_BURDEN_NOTE,
                "recommended_commands": [
                    command_for("bash", rel(textfeat_launcher))
                    if textfeat_launcher.exists()
                    else command_for("uv", "run", "python", "scripts/e016_make_textfeat_control_script.py"),
                ],
            }
        )
        if runners:
            packet["resource_warning"] = (
                "Runner processes are still visible; confirm the full TRIBE job is complete and GPUs are free before launching textfeat."
            )
        return packet

    if branch == "matched_information_control_ready":
        packet.update(
            {
                "status": "ready_for_target_control_comparison",
                "route": "compare_controls",
                "reason": "This appears to be a non-TRIBE target readiness packet; compare it with ready TRIBE analysis.",
                "post_compare_burden_note": POST_COMPARE_BURDEN_NOTE,
                "recommended_commands": [
                    command_for(
                        "uv",
                        "run",
                        "python",
                        "scripts/e016_compare_target_controls.py",
                        "--tribe-analysis",
                        rel(ANALYSIS_JSON),
                        "--textfeat-analysis",
                        rel(Path(str(packet["analysis_json"]))),
                    )
                ],
            }
        )
        return packet

    packet.update(
        {
            "status": "mixed_or_manual_interpretation_required",
            "route": "interpret",
            "reason": "The branch hint is mixed, missing, or unfamiliar; inspect seed-level paired values.",
            "recommended_commands": [],
            "recommended_stance": "/interpret",
        }
    )
    return packet


def decide(run_json: Path, analysis_json: Path, readiness_json: Path, textfeat_launcher: Path) -> dict[str, Any]:
    packet = base_packet(run_json, analysis_json, readiness_json, textfeat_launcher)
    if not run_json.exists():
        return missing_run_packet(packet)
    if not analysis_json.exists():
        return needs_finalizer_packet(packet, "Run JSON exists but analyzer JSON is absent.")
    if stale(analysis_json, [run_json]):
        return needs_finalizer_packet(packet, "Analyzer JSON is older than the run JSON.")
    if not readiness_json.exists():
        return needs_finalizer_packet(packet, "Analyzer JSON exists but readiness JSON is absent.")
    if stale(readiness_json, [analysis_json]):
        return needs_finalizer_packet(packet, "Readiness JSON is older than the analyzer JSON.")
    readiness = load_json(readiness_json)
    return route_ready_packet(packet, readiness, textfeat_launcher)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-json", type=Path, default=RUN_JSON)
    ap.add_argument("--analysis-json", type=Path, default=ANALYSIS_JSON)
    ap.add_argument("--readiness-json", type=Path, default=None)
    ap.add_argument("--textfeat-launcher", type=Path, default=DEFAULT_TEXTFEAT_LAUNCHER)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    run_json = absolutize(args.run_json)
    analysis_json = absolutize(args.analysis_json)
    assert run_json is not None and analysis_json is not None
    readiness_json = absolutize(args.readiness_json) or out_path_for(analysis_json)
    textfeat_launcher = absolutize(args.textfeat_launcher)
    assert textfeat_launcher is not None
    packet = decide(run_json, analysis_json, readiness_json, textfeat_launcher)
    text = json.dumps(packet, indent=2)
    print(text)
    out = absolutize(args.out)
    if out is not None:
        out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
