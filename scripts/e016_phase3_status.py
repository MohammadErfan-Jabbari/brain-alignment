#!/usr/bin/env python3
"""Read-only status helper for the E016 full Phase-3 pipeline."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
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
TRAINING_ARMS_EXPECTED = 9


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


def parse_etime_seconds(spec: str) -> int | None:
    """Parse ps etime strings of the form [[DD-]HH:]MM:SS."""
    day_part = 0
    rest = spec.strip()
    if "-" in rest:
        day_text, rest = rest.split("-", 1)
        try:
            day_part = int(day_text)
        except ValueError:
            return None
    parts = rest.split(":")
    try:
        vals = [int(part) for part in parts]
    except ValueError:
        return None
    if len(vals) == 2:
        hours = 0
        minutes, seconds = vals
    elif len(vals) == 3:
        hours, minutes, seconds = vals
    else:
        return None
    return day_part * 86400 + hours * 3600 + minutes * 60 + seconds


def section_batches(text: str, start_marker: str, end_markers: list[str]) -> list[tuple[int, int]]:
    start_idx = text.find(start_marker)
    if start_idx < 0:
        return []
    end_candidates = [idx for marker in end_markers if (idx := text.find(marker, start_idx + 1)) >= 0]
    end_idx = min(end_candidates, default=len(text))
    section = text[start_idx:end_idx]
    return [(int(a), int(b)) for a, b in re.findall(r"=== batch (\d+):(\d+) ===", section)]


def progress_rec(batches: list[tuple[int, int]], expected_items: int) -> dict | None:
    if not batches:
        return None
    start, end = batches[-1]
    return {
        "latest_batch": {"start": start, "end": end},
        "items_done_lower_bound": min(end, expected_items),
        "items_expected": expected_items,
        "fraction": round(min(end, expected_items) / expected_items, 6),
    }


def parse_float_or_none(spec: str) -> float | None:
    if spec in {"None", "NA", "nan"}:
        return None
    return float(spec)


def parse_training_progress(text: str) -> dict | None:
    arms: list[dict] = []
    current: dict | None = None
    marker_re = re.compile(r"== seed=(\d+) arm=([a-z_]+) lambda=([^\s=]+) ==")
    metric_re = re.compile(r"^\s*ppl=([^\s]+)(?:\s+target_r2=([^\s]+))?\s*$")
    for line in text.splitlines():
        marker = marker_re.search(line)
        if marker:
            current = {
                "seed": int(marker.group(1)),
                "arm": marker.group(2),
                "lambda": float(marker.group(3)),
                "status": "started",
            }
            arms.append(current)
            continue
        metric = metric_re.match(line)
        if metric and current is not None and current.get("status") != "completed":
            current["status"] = "completed"
            current["ppl"] = parse_float_or_none(metric.group(1))
            if metric.group(2) is not None:
                current["target_r2"] = parse_float_or_none(metric.group(2))
            current["science_status"] = "partial arm diagnostic only; not a Phase-3 result"
    if not arms:
        return None
    completed = [arm for arm in arms if arm.get("status") == "completed"]
    latest = arms[-1]
    latest_completed = completed[-1] if completed else None
    active_arm = latest if latest.get("status") != "completed" else None
    return {
        "latest_arm": {key: latest[key] for key in ("seed", "arm", "lambda")},
        "latest_completed_arm": (
            {
                key: latest_completed[key]
                for key in ("seed", "arm", "lambda", "ppl", "target_r2", "science_status")
                if key in latest_completed
            }
            if latest_completed
            else None
        ),
        "active_arm": ({key: active_arm[key] for key in ("seed", "arm", "lambda")} if active_arm else None),
        "arm_markers_seen": len(arms),
        "completed_arm_count": len(completed),
        "arms_expected": TRAINING_ARMS_EXPECTED,
        "completed_arms": completed,
    }


def add_training_eta(log: dict, processes: list[dict], *, now: datetime) -> None:
    """Add a rough training-arm ETA from saved artifact timestamps.

    The runner only prints between arms, so this is intentionally coarse. It is
    operational monitoring metadata, not science evidence.
    """
    progress = log.get("training_progress")
    if not progress:
        return
    completed_count = int(progress.get("completed_arm_count") or 0)
    arms_expected = int(progress.get("arms_expected") or TRAINING_ARMS_EXPECTED)
    if completed_count <= 0 or arms_expected <= completed_count:
        return

    artifact_paths: list[Path] = []
    for line in log.get("tail") or []:
        if "saved_model=" not in str(line):
            continue
        _, raw_path = str(line).split("saved_model=", 1)
        path = Path(raw_path.strip())
        if not path.is_absolute():
            path = ROOT / path
        sidecar = path / "e016_model_artifact.json"
        if sidecar.exists():
            artifact_paths.append(sidecar)

    # The log tail can miss early artifacts, so fall back to all saved_model
    # lines in the full log when needed.
    log_path = Path(str(log.get("path", "")))
    if len(artifact_paths) < 2 and log_path.exists():
        text = log_path.read_text(encoding="utf-8", errors="replace")
        for raw_path in re.findall(r"saved_model=([^\s]+)", text):
            path = Path(raw_path.strip())
            if not path.is_absolute():
                path = ROOT / path
            sidecar = path / "e016_model_artifact.json"
            if sidecar.exists():
                artifact_paths.append(sidecar)

    artifact_paths = sorted(set(artifact_paths), key=lambda path: path.stat().st_mtime)
    if len(artifact_paths) < 2:
        return

    runner_elapsed = [
        parse_etime_seconds(str(proc.get("elapsed", "")))
        for proc in processes
        if "run_tribe_phase3.py" in str(proc.get("cmd", ""))
    ]
    runner_elapsed = [value for value in runner_elapsed if value is not None]
    if not runner_elapsed:
        return

    runner_start = now - timedelta(seconds=max(runner_elapsed))
    completed_times = [datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc) for path in artifact_paths]
    observed_seconds: list[int] = []
    previous = runner_start
    for completed_at in completed_times:
        delta = int((completed_at - previous).total_seconds())
        if delta > 0:
            observed_seconds.append(delta)
            previous = completed_at
    if not observed_seconds:
        return

    mean_arm_s = sum(observed_seconds) / len(observed_seconds)
    active_arm = progress.get("active_arm")
    active_elapsed_s = int((now - completed_times[-1]).total_seconds()) if active_arm else 0
    remaining_completed_equiv = max(0, arms_expected - len(completed_times))
    if active_arm:
        active_remaining_s = max(0, int(round(mean_arm_s - active_elapsed_s)))
        future_arms_after_active = max(0, arms_expected - len(completed_times) - 1)
        eta_s = active_remaining_s + int(round(future_arms_after_active * mean_arm_s))
    else:
        eta_s = int(round(remaining_completed_equiv * mean_arm_s))

    progress["rough_training_eta"] = {
        "method": "saved-artifact cadence from completed arms",
        "science_status": "operational estimate only; not a Phase-3 result",
        "completed_artifact_count": len(completed_times),
        "observed_arm_seconds": observed_seconds,
        "mean_completed_arm_s": round(mean_arm_s, 1),
        "active_arm_elapsed_s": active_elapsed_s if active_arm else None,
        "eta_s": eta_s,
        "eta_utc": (now + timedelta(seconds=eta_s)).isoformat(),
        "confidence": "rough",
        "note": "Assumes remaining arms take about the same wall-clock time as completed saved-artifact arms.",
    }


def add_active_eta(log: dict, processes: list[dict], train_cache: Path, heldout_cache: Path, run_script: Path) -> None:
    stage = log.get("active_cache_stage")
    if stage not in {"train", "heldout"}:
        return
    progress = log.get(f"{stage}_cache_progress")
    if not progress:
        return
    fraction = float(progress.get("fraction") or 0.0)
    if fraction <= 0.0 or fraction >= 1.0:
        return
    active_cache = train_cache if stage == "train" else heldout_cache
    elapsed_options = [
        parse_etime_seconds(str(proc.get("elapsed", "")))
        for proc in processes
        if str(active_cache) in str(proc.get("cmd", ""))
    ]
    if not elapsed_options and stage == "train":
        elapsed_options = [
            parse_etime_seconds(str(proc.get("elapsed", "")))
            for proc in processes
            if str(run_script) in str(proc.get("cmd", ""))
        ]
    elapsed = max([value for value in elapsed_options if value is not None], default=None)
    if elapsed is None or elapsed <= 0:
        return
    items_done = int(progress["items_done_lower_bound"])
    expected = int(progress["items_expected"])
    remaining = max(0, expected - items_done)
    items_per_hour = items_done / (elapsed / 3600.0)
    estimated_total = elapsed / fraction
    eta = max(0, int(round(estimated_total - elapsed)))
    progress["active_elapsed_s"] = int(elapsed)
    progress["items_per_hour_lower_bound"] = round(items_per_hour, 2)
    progress["eta_s_lower_bound"] = eta
    progress["eta_utc_lower_bound"] = (datetime.now(timezone.utc) + timedelta(seconds=eta)).isoformat()
    progress["remaining_items_lower_bound"] = remaining


def discover_processes(
    run_script: Path = RUN_SCRIPT,
    train_cache: Path = TRAIN_CACHE,
    heldout_cache: Path = HELDOUT_CACHE,
    run_json: Path = RUN_JSON,
) -> list[dict]:
    proc = subprocess.run(["ps", "-eo", "pid=,etime=,stat=,cmd="], check=False, text=True, capture_output=True)
    rows = []
    for line in proc.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) != 4:
            continue
        pid, elapsed, stat, cmd = parts
        is_parent = str(run_script) in cmd
        is_builder = "tribe_predict_kd_corpus.py" in cmd and (str(train_cache) in cmd or str(heldout_cache) in cmd)
        is_runner = "run_tribe_phase3.py" in cmd and str(run_json) in cmd
        if is_parent or is_builder or is_runner:
            rows.append({"pid": int(pid), "elapsed": elapsed, "stat": stat, "cmd": cmd})
    return rows


def log_rec(path: Path, expected_train: int) -> dict:
    rec = file_rec(path)
    if not path.exists():
        return rec
    text = path.read_text(encoding="utf-8", errors="replace")
    markers = [
        "Building full train TRIBE cache",
        "Building full heldout TRIBE cache",
        "Validating full caches",
        "Running full GPT-2 Phase-3 arms",
        "Running analyzer",
        "E016 full Phase-3 pipeline complete",
    ]
    rec["markers_seen"] = [m for m in markers if m in text]
    train_progress = progress_rec(
        section_batches(
            text,
            "Building full train TRIBE cache",
            ["Building full heldout TRIBE cache", "Validating full caches"],
        ),
        expected_train,
    )
    heldout_progress = progress_rec(
        section_batches(
            text,
            "Building full heldout TRIBE cache",
            ["Validating full caches", "Running full GPT-2 Phase-3 arms"],
        ),
        HELDOUT_EXPECTED,
    )
    if train_progress:
        rec["train_cache_progress"] = train_progress
    if heldout_progress:
        rec["heldout_cache_progress"] = heldout_progress
    if "Building full heldout TRIBE cache" in rec["markers_seen"] and "Validating full caches" not in rec["markers_seen"]:
        rec["active_cache_stage"] = "heldout"
    elif "Building full train TRIBE cache" in rec["markers_seen"] and "Building full heldout TRIBE cache" not in rec["markers_seen"]:
        rec["active_cache_stage"] = "train"
    if rec.get("active_cache_stage"):
        active = rec.get(f"{rec['active_cache_stage']}_cache_progress")
        if active:
            rec["latest_batch"] = active["latest_batch"]
    training_progress = parse_training_progress(text)
    if training_progress:
        rec["training_progress"] = training_progress
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


def gpu_rec() -> dict:
    cmd = [
        "nvidia-smi",
        "--query-gpu=index,name,memory.used,memory.total,utilization.gpu,utilization.memory",
        "--format=csv,noheader,nounits",
    ]
    proc = subprocess.run(cmd, check=False, text=True, capture_output=True)
    if proc.returncode != 0:
        return {"available": False, "error": proc.stderr.strip() or proc.stdout.strip()}
    gpus = []
    for line in proc.stdout.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 6:
            continue
        try:
            idx, name, mem_used, mem_total, util_gpu, util_mem = parts
            gpus.append(
                {
                    "index": int(idx),
                    "name": name,
                    "memory_used_mib": int(mem_used),
                    "memory_total_mib": int(mem_total),
                    "utilization_gpu_pct": int(util_gpu),
                    "utilization_memory_pct": int(util_mem),
                }
            )
        except ValueError:
            continue
    active = [gpu for gpu in gpus if gpu["utilization_gpu_pct"] > 0 or gpu["memory_used_mib"] > 1024]
    return {
        "available": True,
        "note": "GPU process PIDs may be host-namespace PIDs; this block is node-level activity, not E016 attribution.",
        "active_gpu_count": len(active),
        "max_utilization_gpu_pct": max((gpu["utilization_gpu_pct"] for gpu in gpus), default=None),
        "gpus": gpus,
    }


def health_rec(
    *,
    now: datetime,
    log: dict,
    processes: list[dict],
    run: dict,
    analysis: dict,
) -> dict:
    runner_processes = [proc for proc in processes if "run_tribe_phase3.py" in str(proc.get("cmd", ""))]
    runner_elapsed = [
        parse_etime_seconds(str(proc.get("elapsed", "")))
        for proc in runner_processes
    ]
    runner_elapsed = [value for value in runner_elapsed if value is not None]
    log_mtime = log.get("mtime_utc")
    log_quiet_s = None
    if log_mtime:
        try:
            log_quiet_s = int((now - datetime.fromisoformat(log_mtime)).total_seconds())
        except ValueError:
            log_quiet_s = None
    if analysis.get("exists"):
        status = "analysis_artifact_present"
    elif run.get("exists"):
        status = "run_json_present_no_analysis"
    elif runner_processes:
        status = "runner_alive_log_quiet" if log_quiet_s is not None and log_quiet_s > 600 else "runner_alive_log_recent"
    elif "Running full GPT-2 Phase-3 arms" in (log.get("markers_seen") or []):
        status = "training_marker_no_runner"
    elif processes:
        status = "processes_alive"
    else:
        status = "no_processes"
    return {
        "status": status,
        "process_count": len(processes),
        "runner_process_count": len(runner_processes),
        "runner_elapsed_s_max": max(runner_elapsed, default=None),
        "log_quiet_s": log_quiet_s,
    }


def infer_phase(train: dict, heldout: dict, run: dict, analysis: dict, log: dict, processes: list[dict]) -> str:
    if analysis.get("exists"):
        gate = analysis.get("gate") or {}
        return "analysis_ready" if gate.get("science_ready") else "analysis_blocked_or_incomplete"
    if run.get("exists"):
        return "run_json_ready_no_analysis"
    if any("run_tribe_phase3.py" in str(proc.get("cmd", "")) for proc in processes):
        return "training_running_or_interrupted"
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
    ap.add_argument("--run-json", type=Path, default=RUN_JSON)
    ap.add_argument("--analysis-json", type=Path, default=ANALYSIS_JSON)
    ap.add_argument("--run-script", type=Path, default=RUN_SCRIPT)
    ap.add_argument("--train-cache", type=Path, default=TRAIN_CACHE)
    ap.add_argument("--heldout-cache", type=Path, default=HELDOUT_CACHE)
    ap.add_argument("--parent-pid", type=int)
    ap.add_argument("--builder-pid", type=int)
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()

    train_cache = args.train_cache if args.train_cache.is_absolute() else ROOT / args.train_cache
    heldout_cache = args.heldout_cache if args.heldout_cache.is_absolute() else ROOT / args.heldout_cache
    run_json = args.run_json if args.run_json.is_absolute() else ROOT / args.run_json
    analysis_json = args.analysis_json if args.analysis_json.is_absolute() else ROOT / args.analysis_json
    run_script = args.run_script if args.run_script.is_absolute() else ROOT / args.run_script
    log_path = args.log if args.log.is_absolute() else ROOT / args.log

    train = file_rec(train_cache)
    heldout = file_rec(heldout_cache)
    run = file_rec(run_json)
    analysis = analysis_rec(analysis_json)
    log = log_rec(log_path, TRAIN_EXPECTED)
    explicit_pids = [pid for pid in [args.parent_pid, args.builder_pid] if pid is not None]
    processes = ps_rec(explicit_pids) if explicit_pids else discover_processes(run_script, train_cache, heldout_cache, run_json)
    add_active_eta(log, processes, train_cache, heldout_cache, run_script)
    now = datetime.now(timezone.utc)
    add_training_eta(log, processes, now=now)
    gpu = gpu_rec()
    payload = {
        "checked_at_utc": now.isoformat(),
        "phase": infer_phase(train, heldout, run, analysis, log, processes),
        "health": health_rec(now=now, log=log, processes=processes, run=run, analysis=analysis),
        "gpu": gpu,
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
