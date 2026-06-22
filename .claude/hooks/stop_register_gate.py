#!/usr/bin/env python3
"""Stop hook — the register convergence gate (D047).

The terminator that the v0.2 session lacked. On turn-end, if a manuscript/report
deliverable was edited THIS session and the FINAL bytes do not carry a fresh,
independent clean register verdict, this blocks the agent from stopping and tells
it to converge. This is decoupled from /wrap by design: /wrap finalizes a session;
THIS enforces write quality, keyed to what changed, stance-independent.

Why a Stop hook: it is the only Claude Code primitive that can refuse to let the
agent end its turn (verified contract: print {"decision":"block","reason":...} →
the model receives the reason and must continue). The PostToolUse prose hook is the
cheap per-edit tripwire; this is the hard terminator.

Loop guard (mandatory — Claude Code has no automatic one): block at most MAX_BLOCKS
times for the SAME content hash, then escalate to Erfan instead of trapping the
agent. An edit changes the hash and resets the count, so real progress is never
penalised.

A clean verdict is produced ONLY by record_register_verdict.py after a fresh quorum
of prose-register-auditor agents returns zero findings; this hook never trusts a
self-claim, only the hash-keyed artifact. Escape hatch: an Erfan-logged
accepted-residual sentinel for the current bytes.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROJ = os.environ.get("CLAUDE_PROJECT_DIR", "")
sys.path.insert(0, str(Path(PROJ) / ".claude/skills/scientific-writing/scripts"))

try:
    import register_state as rs
except Exception:
    sys.exit(0)  # never break the turn flow if the lib is missing

MAX_BLOCKS = 3
EDIT_TOOLS = ("Edit", "Write", "MultiEdit")


def touched_groups(transcript_path: str, root: Path) -> set[str]:
    """Which gated deliverable groups were edited this session (from the transcript)."""
    groups: set[str] = set()
    try:
        lines = Path(transcript_path).read_text(errors="replace").splitlines()
    except Exception:
        return groups
    for line in lines:
        if not any(t in line for t in EDIT_TOOLS):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        msg = obj.get("message", {}) if isinstance(obj, dict) else {}
        for c in (msg.get("content") or []):
            if not isinstance(c, dict) or c.get("type") != "tool_use" or c.get("name") not in EDIT_TOOLS:
                continue
            inp = c.get("input") or {}
            fp = inp.get("file_path") or inp.get("filePath") or ""
            if not fp:
                continue
            rel = fp
            try:
                rel = str(Path(fp).resolve().relative_to(root))
            except Exception:
                pass
            g = rs.group_for(rel.replace(os.sep, "/"))
            if g:
                groups.add(g)
    return groups


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0
    root = rs.repo_root(PROJ)
    tp = data.get("transcript_path", "")
    if not tp:
        return 0
    groups = touched_groups(tp, root)
    if not groups:
        return 0  # no gated deliverable edited this session — nothing to enforce

    blocking: list[str] = []
    escalations: list[str] = []
    for g in sorted(groups):
        if rs.has_signoff(g, root) or rs.is_clean(g, root):
            continue
        n = rs.bump_block(g, root)
        if n > MAX_BLOCKS:
            escalations.append(
                f"[{g}] still has no clean register verdict after {n - 1} blocks. "
                f"ESCALATE to Erfan: either drive it to zero findings, or get an explicit "
                f"accepted-residual sign-off (record_register_verdict.py --accept-residual)."
            )
            continue
        blocking.append(
            f"[{g}] was edited this session but the FINAL bytes have no fresh clean register "
            f"verdict. Before finishing: spawn a quorum (>=2) of FRESH prose-register-auditor "
            f"agents on the final draft, drive to ZERO findings (not zero load-bearing — zero), "
            f"then run scripts/record_register_verdict.py to stamp the verdict for these exact "
            f"bytes. You cannot stop until it is clean or Erfan signs off a residual."
        )

    if blocking:
        reason = "REGISTER GATE (D047) — convergence required:\n- " + "\n- ".join(blocking)
        if escalations:
            reason += "\n- " + "\n- ".join(escalations)
        print(json.dumps({"decision": "block", "reason": reason}))
        return 0
    if escalations:
        sys.stderr.write("REGISTER GATE escalation (loop guard tripped):\n- " + "\n- ".join(escalations) + "\n")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
