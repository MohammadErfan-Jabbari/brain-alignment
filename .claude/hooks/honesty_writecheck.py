#!/usr/bin/env python3
"""PostToolUse honesty flag (D011), stance-independent and NON-BLOCKING.

Fires after an Edit / Write / MultiEdit to the evidence doc set:
    docs/reports/  docs/experiments/  docs/manuscript/  docs/ladder.md  docs/learnings.md
Runs the existing D011 number-checker (scientific-writing/scripts/check_evd_resolution.py) on the
written file. If a result-like number has no evidence cite, it surfaces the findings to the model as
feedback. The write already succeeded, so this never blocks; it flags. The /wrap number-provenance
audit is the backstop.

Why a hook and not stance prose: the fabrication guard must fire no matter which stance is active, so
a number cannot land unsourced just because the work was mislabeled. (Plan: "honesty armed at
write-time, not in the stance.") docs/learning/ is deliberately NOT guarded (its records cite a report
by field, not an inline [E0nn], so they would false-positive).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

GUARDED_PREFIXES = ("docs/reports/", "docs/experiments/", "docs/manuscript/")
GUARDED_FILES = ("docs/ladder.md", "docs/learnings.md")
CHECKABLE_SUFFIXES = (".md", ".markdown", ".tex")


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # never break the tool flow

    tool_input = data.get("tool_input") or {}
    fp = tool_input.get("file_path") or tool_input.get("filePath")
    if not fp:
        return 0

    proj = os.environ.get("CLAUDE_PROJECT_DIR", "")
    path = Path(fp)
    try:
        rel = path.resolve().relative_to(Path(proj).resolve()) if proj else path
    except Exception:
        rel = path
    rel_s = str(rel).replace(os.sep, "/")

    guarded = rel_s.startswith(GUARDED_PREFIXES) or rel_s in GUARDED_FILES
    if not guarded or path.suffix.lower() not in CHECKABLE_SUFFIXES or not path.exists():
        return 0

    checker = Path(proj) / ".claude/skills/scientific-writing/scripts/check_evd_resolution.py"
    if not checker.exists():
        return 0

    cmd = [sys.executable, str(checker), str(path)]
    if proj:
        cmd += ["--repo-root", proj]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except Exception:
        return 0
    if proc.returncode == 0:
        return 0

    findings = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    sys.stderr.write(
        "D011 honesty flag (NON-BLOCKING; the write already succeeded). A result-like number with no "
        "evidence cite was found in a guarded doc:\n\n" + findings + "\n\n"
        "Resolve it before /wrap: add an [E0nn]/\\evd cite, or mark it \\gap{...}. Never invent or "
        "estimate the number. This guard is stance-independent (D044)."
    )
    return 2  # PostToolUse: stderr is surfaced to the model as feedback; the tool already ran


if __name__ == "__main__":
    sys.exit(main())
