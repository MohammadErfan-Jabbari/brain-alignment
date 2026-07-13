#!/usr/bin/env python3
"""Non-blocking provenance flag for writes to live or frozen manuscript sources."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

GUARDED_PREFIXES = ("docs/manuscript/extended/", "docs/manuscript/public/")


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = (data.get("tool_input") or {}).get("file_path") or (data.get("tool_input") or {}).get("filePath")
    if not fp:
        return 0
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    path = Path(fp).resolve()
    try:
        rel = path.relative_to(project).as_posix()
    except ValueError:
        return 0
    if not rel.startswith(GUARDED_PREFIXES) or path.suffix.lower() != ".tex" or not path.exists():
        return 0
    checker = project / ".claude/scripts/manuscript_check.py"
    try:
        proc = subprocess.run([sys.executable, str(checker), str(path), "--no-build"], capture_output=True, text=True, timeout=30)
    except Exception:
        return 0
    if proc.returncode == 0:
        return 0
    findings = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    sys.stderr.write("Manuscript provenance flag (non-blocking):\n\n" + findings + "\n\nResolve with an E marker, keyed result, or honest gap; never invent a value.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
