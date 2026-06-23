#!/usr/bin/env python3
"""Stop hook — the sci-write-v2 stage-5 convergence gate (P2-D-3, D047 pattern).

On turn-end, if a sci-write-v2 draft is actively mid-audit, this refuses to let the agent stop until every
stage-5 RUB reader is `ready_to_ship` for the CURRENT draft (verdicts.py status). It is the automatic terminator
for the "revise-until-clean" loop — the teeth behind P2-D-2's verdict bookkeeping.

PIPELINE-SCOPED, fail-closed-only-when-armed: it does NOTHING unless `.claude/state/sw-gate/active.json` exists
(the orchestrator writes it at stage 4 via `verdicts.py activate`, clears it at ship via `verdicts.py ship`). So
it never blocks an unrelated session. active.json also pins the ONE canonical draft path — the hook trusts that,
not any per-call arg (closes the F8a-vs-F8b wrong-draft seam).

Trust model (same as stop_register_gate.py / gate_state.py): the verdict store is TRUSTED, not verified. This
hook enforces D047 staleness-freshness (a one-byte draft edit voids every verdict via the hash) and forces
convergence; it does NOT prove a verdict came from a real subagent vs a hand-typed boolean (provenance). That
upgrade — parse the session transcript for fresh reader spawns — is deliberately out of scope (it couples to an
undocumented transcript format for a non-threat in a single-user pipeline).

Loop guard (mandatory): block at most MAX_BLOCKS times for the same draft hash, then escalate to Erfan (stderr)
instead of trapping the agent. An edit changes the hash and resets the count. Escape hatch: an Erfan-logged
accepted-residual sign-off for the current bytes (`verdicts.py accept-residual`).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROJ = os.environ.get("CLAUDE_PROJECT_DIR", "")
sys.path.insert(0, str(Path(PROJ) / ".claude/skills/sci-write-v2/scripts"))

try:
    import verdicts as V
except Exception:
    sys.exit(0)  # never break the turn flow if the lib is missing

MAX_BLOCKS = 3


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0  # re-entrancy guard
    root = Path(PROJ).resolve() if PROJ else Path(".").resolve()

    draft = V.active_draft(root)
    if draft is None:
        return 0  # no sci-write-v2 draft armed — nothing to enforce
    # Enforce ONLY for the session that armed it, and fail toward release (never block an unrelated session — a
    # wrongly-blocked session is a repo-wide outage). Two distinct non-enforce cases:
    armed, cur = V.active_session(root), data.get("session_id")
    if armed and cur and armed != cur:
        V.deactivate(root)   # CONFIRMED different/abandoned session owns it -> disarm + release
        return 0
    if not V.session_matches(armed, cur):
        return 0             # can't confirm THIS session owns it this turn (transient missing id) -> release,
                             # but do NOT disarm — one dropped event id must not permanently kill a legit run
    # armed and cur both present and equal -> this session owns the gate -> enforce below
    if not draft.is_file():
        sys.stderr.write(f"sw-converge: armed draft {draft} is missing; run `verdicts.py ship` if the run ended.\n")
        return 0
    if V.is_residual(root, draft):
        return 0  # Erfan signed off the current bytes

    conv, lines = V.status(root, draft)
    if conv:
        return 0  # every reader ready for this draft — allow stop

    h = V.prose_hash(draft)
    n = V.bump_block(root, h)
    detail = "\n".join(lines)
    if n > MAX_BLOCKS:
        sys.stderr.write(
            f"sw-converge: draft {h} still not converged after {n - 1} blocks. ESCALATE to Erfan: drive the "
            f"stage-5 readers to ready, or sign off `verdicts.py accept-residual --prose {draft}`.\n{detail}\n"
        )
        return 0  # stop trapping the agent; hand it to Erfan

    reason = (
        "SW-CONVERGE GATE (P2-D-3) — stage-5 not converged; you cannot finish until every reader is "
        f"ready_to_ship for the current draft (or Erfan signs a residual):\n{detail}\n"
        "Revise the flagged points, re-run the stage-5 reader(s) on the (re)drafted prose, re-record each verdict "
        "(`verdicts.py record …`), then this releases. A prose edit invalidates every prior verdict (the hash "
        "changes), so re-audit after any change. When converged + approved, run `verdicts.py ship`."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
