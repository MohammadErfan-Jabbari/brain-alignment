#!/usr/bin/env python3
"""PostToolUse prose-quality flag (D046), stance-independent and NON-BLOCKING.

Sibling to honesty_writecheck.py. That hook guards NUMBERS (D011); this one guards
PROSE. Fires after an Edit / Write / MultiEdit to a prose deliverable:
    docs/reports/  docs/manuscript/
Runs the anti-AI-tell linter (scientific-writing/scripts/ai_tell_lint.py) on the
written file and surfaces its output — both the hard Class-C tells and the soft
Class-A register / Class-B passive warnings — to the model as feedback.

Why a hook and not skill prose: the v0.1 extended manuscript was written in one
unlogged burst that bypassed the whole scientific-writing full loop (no /write
session, no review pass), so the gate never fired and storytelling prose reached a
supervisor (L054, D046). A hook fires no matter the stance or whether the ritual
ran — it is the one check the bypass cannot skip. The write already succeeded, so
this never blocks; it flags. The non-skippable review pass (prose-register-auditor)
and the /wrap audit are the deeper backstops; this is the always-on tripwire.

The deterministic linter cannot catch the full Class-A register class (no banned
token) — a clean run here is NOT a clearance. Anything supervisor-facing still owes
the review pass. This hook only guarantees the cheap layer is never silently skipped.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

GUARDED_PREFIXES = ("docs/reports/", "docs/manuscript/")
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

    guarded = rel_s.startswith(GUARDED_PREFIXES)
    if not guarded or path.suffix.lower() not in CHECKABLE_SUFFIXES or not path.exists():
        return 0

    linter = Path(proj) / ".claude/skills/scientific-writing/scripts/ai_tell_lint.py"
    if not linter.exists():
        return 0

    try:
        proc = subprocess.run(
            [sys.executable, str(linter), str(path)],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return 0

    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    has_hard = proc.returncode != 0
    has_soft = "soft warning(s)" in out
    if not has_hard and not has_soft:
        return 0  # genuinely clean

    findings = (out + ("\n" + err if err else "")).strip()
    sys.stderr.write(
        "Prose flag (NON-BLOCKING; the write already succeeded). The anti-AI-tell linter found "
        "issues in a guarded prose doc:\n\n" + findings + "\n\n"
        "Hard Class-C tells: fix silently. Soft register/passive warnings: heuristic leads — the "
        "deterministic linter CANNOT catch the full register class, so a clean run is not a clearance. "
        "Anything supervisor-facing still owes the non-skippable review pass (prose-register-auditor). "
        "This guard is stance-independent (D046)."
    )
    return 2  # PostToolUse: stderr is surfaced to the model as feedback; the tool already ran


if __name__ == "__main__":
    sys.exit(main())
