#!/usr/bin/env python3
"""Shared state for the register convergence gate (D047).

The gate's job: a manuscript/report deliverable cannot be "finished" (the agent
cannot end its turn) until a FRESH, independent prose-register audit of the FINAL
bytes comes back clean. The verdict is keyed to a content hash of the deliverable
so a stale YES dies the moment a byte changes.

This module is the single source of truth for: which files make up a deliverable
group, the content hash of that group, the persisted verdict, the accepted-residual
sign-off sentinel, and the per-hash block count (the loop guard). It is imported by
both the Stop hook (.claude/hooks/stop_register_gate.py) and the recorder
(record_register_verdict.py).
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
from pathlib import Path

STATE_DIRNAME = ".claude/state/register"


def repo_root(explicit: str | None = None) -> Path:
    return Path(explicit or os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()


def group_for(rel_path: str) -> str | None:
    """Map a changed deliverable path to its gate group key, or None if ungated.

    - any prose .tex under docs/manuscript/  -> the single 'manuscript-extended' group
    - a docs/reports/*.md report             -> a per-file group 'report:<path>'
    """
    rel = rel_path.replace(os.sep, "/")
    if rel.startswith("docs/manuscript/") and rel.endswith(".tex"):
        return "manuscript-extended"
    if rel.startswith("docs/reports/") and rel.endswith(".md"):
        return f"report:{rel}"
    return None


def group_files(group_key: str, root: Path) -> list[Path]:
    """The concrete files whose bytes define a group's content hash."""
    if group_key == "manuscript-extended":
        files = sorted(glob.glob(str(root / "docs/manuscript/extended/sections/*.tex")))
        main = root / "docs/manuscript/extended/main-extended.tex"
        if main.exists():
            files.append(str(main))
        return [Path(f) for f in files]
    if group_key.startswith("report:"):
        p = root / group_key[len("report:"):]
        return [p] if p.exists() else []
    return []


def content_hash(group_key: str, root: Path) -> str:
    h = hashlib.sha256()
    for f in group_files(group_key, root):
        h.update(Path(f).name.encode())
        h.update(b"\0")
        try:
            h.update(Path(f).read_bytes())
        except Exception:
            pass
        h.update(b"\0")
    return h.hexdigest()[:16]


def state_dir(root: Path) -> Path:
    d = root / STATE_DIRNAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def _verdict_path(root: Path) -> Path:
    return state_dir(root) / "verdict.json"


def load_verdicts(root: Path) -> dict:
    p = _verdict_path(root)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def save_verdicts(root: Path, d: dict) -> None:
    _verdict_path(root).write_text(json.dumps(d, indent=2))


def is_clean(group_key: str, root: Path) -> bool:
    """True iff a YES verdict exists keyed to the CURRENT content hash."""
    v = load_verdicts(root).get(group_key)
    if not v:
        return False
    return v.get("verdict") == "YES" and v.get("hash") == content_hash(group_key, root)


def _safe(group_key: str) -> str:
    return group_key.replace("/", "_").replace(":", "_")


def sentinel_path(group_key: str, root: Path, h: str) -> Path:
    return state_dir(root) / f"accepted-residual_{_safe(group_key)}_{h}.flag"


def has_signoff(group_key: str, root: Path) -> bool:
    """True iff Erfan logged an accepted-residual sign-off for the CURRENT bytes."""
    return sentinel_path(group_key, root, content_hash(group_key, root)).exists()


def _blocks_path(root: Path) -> Path:
    return state_dir(root) / "blocks.json"


def _load_blocks(root: Path) -> dict:
    p = _blocks_path(root)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def block_count(group_key: str, root: Path) -> int:
    h = content_hash(group_key, root)
    return _load_blocks(root).get(f"{group_key}@{h}", 0)


def bump_block(group_key: str, root: Path) -> int:
    d = _load_blocks(root)
    h = content_hash(group_key, root)
    key = f"{group_key}@{h}"
    d[key] = d.get(key, 0) + 1
    _blocks_path(root).write_text(json.dumps(d))
    return d[key]
