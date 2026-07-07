#!/usr/bin/env python3
"""Report readiness for the E016 combined Tuckute interpretation gate.

This is a read-only handoff helper. It does not run training, score models,
analyze rows, audit arithmetic, adjudicate a claim, or flip a rung.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_RUN_JSON = Path("outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.json")
DEFAULT_PHASE3_LOG = Path("outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.log")
DEFAULT_PHASE3_ANALYSIS_JSON = Path(
    "outputs/E016_tribe/phase3/phase3_rerun_tribe_gpt2_n95999_s0-2_lam0.1_save.analysis.json"
)
DEFAULT_RUN_SCRIPT = Path("outputs/E016_tribe/phase3/run_rerun_tribe_s0-2_save_20260707.sh")
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


def path_needles(path: Path) -> list[str]:
    resolved = resolve(path)
    needles = [str(path), str(resolved)]
    try:
        needles.append(str(resolved.relative_to(ROOT)))
    except ValueError:
        pass
    return sorted(set(needles), key=len, reverse=True)


def line_matches_groups(line: str, groups: list[list[str]]) -> bool:
    return all(any(needle in line for needle in group) for group in groups)


def parse_process_line(line: str) -> dict[str, Any] | None:
    parts = line.split(maxsplit=4)
    if len(parts) < 5:
        return None
    return {
        "pid": int(parts[0]),
        "ppid": int(parts[1]),
        "stat": parts[2],
        "elapsed": parts[3],
        "cmd": parts[4],
    }


def discover_processes_by_groups(groups: list[list[str]]) -> list[dict[str, Any]]:
    proc = subprocess.run(
        ["ps", "-eo", "pid,ppid,stat,etime,args"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    out = []
    for line in proc.stdout.splitlines()[1:]:
        if not line_matches_groups(line, groups):
            continue
        parsed = parse_process_line(line)
        if parsed is not None:
            out.append(parsed)
    return out


def watcher_specs(args: argparse.Namespace) -> dict[str, list[list[str]]]:
    return {
        "rerun_tuckute_scorer": [
            ["e016_watch_tuckute_eval.py"],
            path_needles(args.run_json),
            path_needles(args.rerun_tuckute),
        ],
        "combined_tuckute_analyzer": [
            ["e016_analyze_tuckute_alignment.py"],
            path_needles(args.rerun_tuckute),
            path_needles(args.analysis_json),
        ],
        "combined_tuckute_auditor": [
            ["e016_audit_tuckute_alignment.py"],
            path_needles(args.analysis_json),
            path_needles(args.audit_json),
        ],
        "rich_status_monitor": [
            ["e016_monitor_phase3_status.py"],
            path_needles(args.run_json),
            path_needles(args.audit_json),
        ],
        "simple_rerun_monitor": [
            ["monitor_rerun_realbrain"],
        ],
    }


def discover_watchers(args: argparse.Namespace) -> dict[str, dict[str, Any]]:
    watchers: dict[str, dict[str, Any]] = {}
    for name, groups in watcher_specs(args).items():
        processes = discover_processes_by_groups(groups)
        watchers[name] = {
            "process_count": len(processes),
            "processes": processes,
        }
    return watchers


def summarize_rerun_status(status: dict[str, Any]) -> dict[str, Any]:
    health = status.get("health") if isinstance(status.get("health"), dict) else {}
    log = status.get("log") if isinstance(status.get("log"), dict) else {}
    progress = log.get("training_progress") if isinstance(log.get("training_progress"), dict) else {}
    eta = progress.get("rough_training_eta") if isinstance(progress.get("rough_training_eta"), dict) else {}
    gpu = status.get("gpu") if isinstance(status.get("gpu"), dict) else {}
    return {
        "available": True,
        "phase": status.get("phase"),
        "health_status": health.get("status"),
        "runner_process_count": health.get("runner_process_count"),
        "runner_elapsed_s_max": health.get("runner_elapsed_s_max"),
        "log_quiet_s": health.get("log_quiet_s"),
        "completed_arm_count": progress.get("completed_arm_count"),
        "arms_expected": progress.get("arms_expected"),
        "active_arm": progress.get("active_arm"),
        "latest_completed_arm": progress.get("latest_completed_arm"),
        "rough_training_eta_s": eta.get("eta_s"),
        "rough_training_eta_utc": eta.get("eta_utc"),
        "rough_training_eta_note": eta.get("note"),
        "max_gpu_utilization_pct": gpu.get("max_utilization_gpu_pct"),
        "science_status": "operational rerun status only; not a Phase-3 result",
    }


def collect_rerun_status(args: argparse.Namespace) -> dict[str, Any]:
    cmd = [
        sys.executable,
        "scripts/e016_phase3_status.py",
        "--pretty",
        "--log",
        str(resolve(args.phase3_log)),
        "--run-json",
        str(resolve(args.run_json)),
        "--analysis-json",
        str(resolve(args.phase3_analysis_json)),
        "--run-script",
        str(resolve(args.run_script)),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, check=False, text=True, capture_output=True)
    if proc.returncode != 0:
        return {
            "available": False,
            "returncode": proc.returncode,
            "stderr": proc.stderr.strip(),
            "stdout_tail": proc.stdout.splitlines()[-20:],
        }
    try:
        status = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {
            "available": False,
            "parse_error": str(exc),
            "stdout_tail": proc.stdout.splitlines()[-20:],
        }
    if not isinstance(status, dict):
        return {"available": False, "parse_error": f"expected object, got {type(status).__name__}"}
    return summarize_rerun_status(status)


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
    watchers = discover_watchers(args)
    rerun_status = collect_rerun_status(args)
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
        "rerun_status_summary": rerun_status,
        "postprocess_watchers": watchers,
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
        "## Rerun Progress",
        "",
    ]
    rerun = payload["rerun_status_summary"]
    if rerun.get("available"):
        lines.extend([
            f"- status_phase: `{rerun['phase']}`",
            f"- health: `{rerun['health_status']}`",
            f"- completed_arms: `{rerun['completed_arm_count']}/{rerun['arms_expected']}`",
            f"- active_arm: `{rerun['active_arm']}`",
            f"- latest_completed_arm: `{rerun['latest_completed_arm']}`",
            f"- rough_training_eta_utc: `{rerun['rough_training_eta_utc']}`",
            f"- rough_training_eta_s: `{rerun['rough_training_eta_s']}`",
            f"- max_gpu_utilization_pct: `{rerun['max_gpu_utilization_pct']}`",
            "- progress_status: operational estimate only; not a science result",
        ])
    else:
        lines.append(f"- unavailable: `{rerun}`")
    lines.extend([
        "",
        "## Watchers",
        "",
    ])
    for name, status in payload["postprocess_watchers"].items():
        lines.append(f"- {name}: `{status['process_count']}` process(es)")
    lines.extend([
        "",
        "## Required Files",
        "",
    ])
    for key, status in payload["required_files"].items():
        state = "present" if status["nonempty"] else "missing"
        lines.append(f"- {state}: `{key}` -> `{status['path']}`")
    lines.append("")
    lines.append("Status only. This helper does not produce or adjudicate a science result.")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-json", type=Path, default=DEFAULT_RUN_JSON)
    ap.add_argument("--phase3-log", type=Path, default=DEFAULT_PHASE3_LOG)
    ap.add_argument("--phase3-analysis-json", type=Path, default=DEFAULT_PHASE3_ANALYSIS_JSON)
    ap.add_argument("--run-script", type=Path, default=DEFAULT_RUN_SCRIPT)
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
