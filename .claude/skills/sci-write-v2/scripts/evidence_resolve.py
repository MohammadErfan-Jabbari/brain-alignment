#!/usr/bin/env python3
"""Evidence-key resolution — lifted from scientific-writing/scripts/check_evd_resolution.py.

Shared by the new /write DET checks (F3 claim_binding, later F9a). An experiment key Ennn
resolves to a file under docs/experiments/<KEY>*.md; a learning key Lnn resolves to an L<NN>
entry in docs/learnings.md. Kept as its own tiny module so the binding/fidelity checks share
one resolver instead of each re-implementing it.
"""
from __future__ import annotations

import re
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for p in [start.resolve(), *start.resolve().parents]:
        if (p / "docs" / "experiments").is_dir():
            return p
    raise SystemExit(f"could not find repo root (a parent with docs/experiments/) from {start}")


def resolve_key(key: str, root: Path) -> bool:
    """True iff the evidence key resolves to a real record under docs/.

    Robust to a sub-lettered key (E013b) and a zero-pad mismatch (E13 <-> E013): try the literal
    glob first, then fall back to the zero-padded numeric stem (E013b -> E013*), so an arm documented
    inside its parent experiment's file resolves. Empty/garbage keys resolve to False, not a crash.
    """
    key = (key or "").strip()
    if not key:
        return False
    kind, rest = key[0].upper(), key[1:]
    stem = re.match(r"(\d+)", rest)
    if kind == "E":
        pats = [f"docs/experiments/E{rest}*.md"]
        if stem:
            pats.append(f"docs/experiments/E{int(stem.group(1)):03d}*.md")
        return any(any(root.glob(p)) for p in pats)
    if kind == "L":
        learnings = root / "docs" / "learnings.md"
        if not learnings.exists() or not stem:
            return False
        num = stem.group(1)
        return re.search(rf"\bL{int(num):03d}\b|\bL{num}\b",
                         learnings.read_text(encoding="utf-8", errors="replace")) is not None
    return False
