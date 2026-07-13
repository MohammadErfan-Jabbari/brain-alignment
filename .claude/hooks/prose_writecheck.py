#!/usr/bin/env python3
"""Non-blocking deterministic prose flag for manuscript writes."""
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
    linter = project / ".claude/scripts/prose_lint.py"
    try:
        proc = subprocess.run([sys.executable, str(linter), str(path)], capture_output=True, text=True, timeout=30)
    except Exception:
        return 0
    output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    if proc.returncode == 0 and "soft warning(s)" not in output:
        return 0
    sys.stderr.write("Manuscript prose flag (non-blocking):\n\n" + output + "\n\nVerify each heuristic finding. A clean linter is not a clearance; shipping still requires one fresh independent review.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
