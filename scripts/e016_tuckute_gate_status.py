#!/usr/bin/env python3
"""Report readiness for the E016 combined Tuckute interpretation gate.

This is a read-only handoff helper. It does not run training, score models,
analyze rows, audit arithmetic, adjudicate a claim, or flip a rung.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_RUN_JSON = Path("outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json")
DEFAULT_RERUN_TUCKUTE = Path(
    "outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.tuckute_alignment.json"
)
DEFAULT_EXISTING_TRIBE_TUCKUTE = Path(
    "outputs/E016_tribe/phase3/phase3_extra_tribe_gpt2_n95999_s3-5_lam0.1.tuckute_alignment.json"
)
DEFAULT_TEXTFEAT_TUCKUTE = Path(
    "outputs/E016_tribe/phase3/phase3_combined_textfeat_gpt2_n95999_s0-5_lam0.1.tuckute_alignment.json"
)
DEFAULT_ANALYSIS_JSON = Path(
    "outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment_analysis.json"
)
DEFAULT_AUDIT_JSON = Path(
    "outputs/E016_tribe/phase3/phase3_combined_tribe_vs_textfeat_s0-5_tuckute_alignment.audit.json"
)


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def file_status(path: Path) -> dict[str, Any]:
    resolved = resolve(path)
    exists = resolved.exists()
    stat = resolved.stat() if exists else None
    return {
        "path": str(path),
        "resolved_path": str(resolved),
        "exists": exists,
        "nonempty": bool(exists and stat and stat.st_size > 0),
        "size_bytes": int(stat.st_size) if stat else None,
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat() if stat else None,
    }


def load_json_if_present(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    status = file_status(path)
    if not status["nonempty"]:
        return None, None
    try:
        data = json.loads(resolve(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"{path}: {exc}"
    if not isinstance(data, dict):
        return None, f"{path}: JSON root is {type(data).__name__}, expected object"
    return data, None


def discover_runner_processes(run_json: Path) -> list[dict[str, Any]]:
    needle = str(resolve(run_json))
    proc = subprocess.run(
        ["ps", "-eo", "pid,ppid,stat,etime,args"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    out = []
    for line in proc.stdout.splitlines()[1:]:
        if "run_tribe_phase3.py" not in line or needle not in line:
            continue
        parts = line.split(maxsplit=4)
        if len(parts) < 5:
            continue
        out.append({
            "pid": int(parts[0]),
            "ppid": int(parts[1]),
            "stat": parts[2],
            "elapsed": parts[3],
            "cmd": parts[4],
        })
    return out


def classify(
    required: dict[str, dict[str, Any]],
    audit: dict[str, Any] | None,
    audit_error: str | None,
    runners: list[dict[str, Any]],
) -> str:
    if not required["run_json"]["nonempty"]:
        return "waiting_for_rerun_run_json" if runners else "waiting_for_rerun_or_runner_stopped_without_json"
    if not required["rerun_tuckute"]["nonempty"]:
        return "waiting_for_rerun_tuckute_scoring"
    if not required["analysis_json"]["nonempty"]:
        return "waiting_for_combined_tuckute_analysis"
    if not required["audit_json"]["nonempty"]:
        return "waiting_for_combined_tuckute_audit"
    if audit_error or not isinstance(audit, dict):
        return "audit_present_but_unreadable"
    if audit.get("all_checks_pass") is True:
        return "audit_ready_for_interpret"
    return "audit_present_but_failed_or_incomplete"


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    paths = {
        "run_json": args.run_json,
        "rerun_tuckute": args.rerun_tuckute,
        "existing_tribe_tuckute": args.existing_tribe_tuckute,
        "textfeat_tuckute": args.textfeat_tuckute,
        "analysis_json": args.analysis_json,
        "audit_json": args.audit_json,
    }
    required = {key: file_status(path) for key, path in paths.items()}
    audit, audit_error = load_json_if_present(args.audit_json)
    analysis, analysis_error = load_json_if_present(args.analysis_json)
    runners = discover_runner_processes(args.run_json)
    phase = classify(required, audit, audit_error, runners)
    missing = [key for key, status in required.items() if not status["nonempty"]]
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "phase": phase,
        "science_status": "gate status only; not a result, verdict, or rung update",
        "ready_for_interpret": phase == "audit_ready_for_interpret",
        "missing_or_empty": missing,
        "required_files": required,
        "runner_process_count": len(runners),
        "runner_processes": runners,
        "analysis_summary": {
            "ready_for_interpret": analysis.get("ready_for_interpret") if isinstance(analysis, dict) else None,
            "complete_seeds": analysis.get("complete_seeds") if isinstance(analysis, dict) else None,
            "missing_expected_seeds": analysis.get("missing_expected_seeds") if isinstance(analysis, dict) else None,
            "read_error": analysis_error,
        },
        "audit_summary": {
            "all_checks_pass": audit.get("all_checks_pass") if isinstance(audit, dict) else None,
            "route": audit.get("route") if isinstance(audit, dict) else None,
            "complete_seeds": audit.get("complete_seeds") if isinstance(audit, dict) else None,
            "missing_expected_seeds": audit.get("missing_expected_seeds") if isinstance(audit, dict) else None,
            "read_error": audit_error,
        },
        "next_action_hint": next_action_hint(phase),
    }


def next_action_hint(phase: str) -> str:
    return {
        "waiting_for_rerun_run_json": "keep monitoring the selected rerun; do not run Tuckute scoring yet",
        "waiting_for_rerun_or_runner_stopped_without_json": "inspect rerun log and runner exit state before taking action",
        "waiting_for_rerun_tuckute_scoring": "wait for e016_watch_tuckute_eval.py or run saved-student scoring manually if the watcher failed",
        "waiting_for_combined_tuckute_analysis": "run e016_analyze_tuckute_alignment.py over TRIBE seeds 0-5 and textfeat seeds 0-5",
        "waiting_for_combined_tuckute_audit": "run e016_audit_tuckute_alignment.py before interpretation",
        "audit_ready_for_interpret": "switch to /interpret; do not flip a rung without Erfan confirmation",
        "audit_present_but_failed_or_incomplete": "debug row/protocol/arithmetic checks before any claim",
        "audit_present_but_unreadable": "inspect the audit JSON parse/schema before any claim",
    }.get(phase, "inspect gate state")


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# E016 Combined Tuckute Gate Status",
        "",
        f"- checked_at_utc: `{payload['checked_at_utc']}`",
        f"- phase: `{payload['phase']}`",
        f"- ready_for_interpret: `{payload['ready_for_interpret']}`",
        f"- runner_process_count: `{payload['runner_process_count']}`",
        f"- missing_or_empty: `{payload['missing_or_empty']}`",
        f"- audit_route: `{payload['audit_summary']['route']}`",
        f"- audit_all_checks_pass: `{payload['audit_summary']['all_checks_pass']}`",
        f"- next_action: {payload['next_action_hint']}",
        "",
        "## Required Files",
        "",
    ]
    for key, status in payload["required_files"].items():
        state = "present" if status["nonempty"] else "missing"
        lines.append(f"- {state}: `{key}` -> `{status['path']}`")
    lines.append("")
    lines.append("Status only. This helper does not produce or adjudicate a science result.")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-json", type=Path, default=DEFAULT_RUN_JSON)
    ap.add_argument("--rerun-tuckute", type=Path, default=DEFAULT_RERUN_TUCKUTE)
    ap.add_argument("--existing-tribe-tuckute", type=Path, default=DEFAULT_EXISTING_TRIBE_TUCKUTE)
    ap.add_argument("--textfeat-tuckute", type=Path, default=DEFAULT_TEXTFEAT_TUCKUTE)
    ap.add_argument("--analysis-json", type=Path, default=DEFAULT_ANALYSIS_JSON)
    ap.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON)
    ap.add_argument("--pretty", action="store_true")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--fail-if-not-ready", action="store_true")
    args = ap.parse_args()

    payload = build_payload(args)
    if args.markdown:
        print(render_markdown(payload), end="")
    else:
        print(json.dumps(payload, indent=2 if args.pretty else None, sort_keys=args.pretty))
    if args.fail_if_not_ready and not payload["ready_for_interpret"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
