#!/usr/bin/env python3
"""Read-only status helper for the E016 full Phase-3 pipeline."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE3 = ROOT / "outputs/E016_tribe/phase3"
TARGETS = ROOT / "outputs/E016_tribe/kd_targets/text"

DEFAULT_LOG = PHASE3 / "phase3_full_gpt2_n95999_s0-1-2_lam0.1.log"
RUN_SCRIPT = PHASE3 / "run_full_phase3_20260702.sh"
TRAIN_CACHE = TARGETS / "train_start0_n95999_full.npz"
HELDOUT_CACHE = TARGETS / "heldout_start0_n1999_full.npz"
RUN_JSON = PHASE3 / "phase3_full_gpt2_n95999_s0-1-2_lam0.1.json"
ANALYSIS_JSON = PHASE3 / "phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json"

TRAIN_EXPECTED = 95_999
HELDOUT_EXPECTED = 1_999


def iso_mtime(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def file_rec(path: Path) -> dict:
    rec = {"path": str(path), "exists": path.exists(), "mtime_utc": iso_mtime(path)}
    if path.exists():
        rec["size_bytes"] = path.stat().st_size
        sidecar = path.with_suffix(".json")
        if sidecar.exists():
            try:
                meta = json.loads(sidecar.read_text(encoding="utf-8"))
                rec["meta"] = {
                    "n_items": meta.get("n_items"),
                    "target_dim": meta.get("target_dim"),
                    "elapsed_s": meta.get("elapsed_s"),
                    "science_status": meta.get("science_status"),
                }
            except json.JSONDecodeError:
                rec["meta_error"] = f"invalid json sidecar: {sidecar}"
    return rec


def ps_rec(pids: list[int]) -> list[dict]:
    if not pids:
        return []
    cmd = ["ps", "-p", ",".join(str(pid) for pid in pids), "-o", "pid=,etime=,stat=,cmd="]
    proc = subprocess.run(cmd, check=False, text=True, capture_output=True)
    rows = []
    for line in proc.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) == 4:
            rows.append({"pid": int(parts[0]), "elapsed": parts[1], "stat": parts[2], "cmd": parts[3]})
    return rows


def discover_processes() -> list[dict]:
    proc = subprocess.run(["ps", "-eo", "pid=,etime=,stat=,cmd="], check=False, text=True, capture_output=True)
    rows = []
    for line in proc.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) != 4:
            continue
        pid, elapsed, stat, cmd = parts
        is_parent = str(RUN_SCRIPT) in cmd
        is_builder = "tribe_predict_kd_corpus.py" in cmd and str(TRAIN_CACHE) in cmd
        if is_parent or is_builder:
            rows.append({"pid": int(pid), "elapsed": elapsed, "stat": stat, "cmd": cmd})
    return rows


def log_rec(path: Path, expected_train: int) -> dict:
    rec = file_rec(path)
    if not path.exists():
        return rec
    text = path.read_text(encoding="utf-8", errors="replace")
    batches = [(int(a), int(b)) for a, b in re.findall(r"=== batch (\d+):(\d+) ===", text)]
    if batches:
        start, end = batches[-1]
        rec["latest_batch"] = {"start": start, "end": end}
        rec["train_cache_progress"] = {
            "items_done_lower_bound": min(end, expected_train),
            "items_expected": expected_train,
            "fraction": round(min(end, expected_train) / expected_train, 6),
        }
    markers = [
        "Building full train TRIBE cache",
        "Building full heldout TRIBE cache",
        "Validating full caches",
        "Running full GPT-2 Phase-3 arms",
        "Running analyzer",
        "E016 full Phase-3 pipeline complete",
    ]
    rec["markers_seen"] = [m for m in markers if m in text]
    rec["tail"] = text.splitlines()[-12:]
    return rec


def analysis_rec(path: Path) -> dict:
    rec = file_rec(path)
    if not path.exists():
        return rec
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        rec["analysis_error"] = "invalid json"
        return rec
    rec["gate"] = data.get("gate")
    rec["grid"] = data.get("grid")
    rec["paired"] = data.get("paired")
    return rec


def infer_phase(train: dict, heldout: dict, run: dict, analysis: dict, log: dict, processes: list[dict]) -> str:
    if analysis.get("exists"):
        gate = analysis.get("gate") or {}
        return "analysis_ready" if gate.get("science_ready") else "analysis_blocked_or_incomplete"
    if run.get("exists"):
        return "run_json_ready_no_analysis"
    markers = log.get("markers_seen") or []
    if "Running full GPT-2 Phase-3 arms" in markers:
        return "training_running_or_interrupted"
    if heldout.get("exists"):
        return "heldout_cache_ready_waiting_validation_or_training"
    if train.get("exists"):
        return "heldout_cache_building_or_pending"
    if processes:
        return "train_cache_building"
    return "not_running_or_pre_cache"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG)
    ap.add_argument("--parent-pid", type=int)
    ap.add_argument("--builder-pid", type=int)
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()

    train = file_rec(TRAIN_CACHE)
    heldout = file_rec(HELDOUT_CACHE)
    run = file_rec(RUN_JSON)
    analysis = analysis_rec(ANALYSIS_JSON)
    log = log_rec(args.log, TRAIN_EXPECTED)
    explicit_pids = [pid for pid in [args.parent_pid, args.builder_pid] if pid is not None]
    processes = ps_rec(explicit_pids) if explicit_pids else discover_processes()
    payload = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "phase": infer_phase(train, heldout, run, analysis, log, processes),
        "processes": processes,
        "train_cache": train,
        "heldout_cache": heldout,
        "run_json": run,
        "analysis_json": analysis,
        "log": log,
        "expected": {"train_items": TRAIN_EXPECTED, "heldout_items": HELDOUT_EXPECTED},
    }
    print(json.dumps(payload, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
