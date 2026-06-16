#!/usr/bin/env python3
"""SessionStart hook: snapshot the git HEAD and transcript path at session start.

This is the enabling piece for the swarm-wrap (`/wrap`). It records, per worktree,
the commit the session started from and the authoritative transcript path, so `/wrap`
can compute an exact session changeset (`git diff <start_sha>..HEAD` + uncommitted) and
locate the right `.jsonl` without guessing by mtime (which breaks under parallel sessions).

It only RECORDS state. It never blocks, edits, or nags — it is not a gate.

Input (stdin, JSON from Claude Code): {session_id, transcript_path, cwd, source, ...}.
Output: writes <cwd>/.claude/state/wrap/start.json. Exits 0 always (a hook failure must
never break session start). State is gitignored and per-worktree, so parallel work in
separate worktrees stays isolated; two sessions in ONE worktree is unsupported (the second
overwrites) — by design, parallel work uses separate worktrees.
"""
import json
import os
import subprocess
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    cwd = payload.get("cwd") or os.getcwd()
    session_id = payload.get("session_id", "")
    transcript_path = payload.get("transcript_path", "")
    source = payload.get("source", "")

    try:
        start_sha = subprocess.check_output(
            ["git", "-C", cwd, "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        start_sha = ""

    try:
        start_ts = subprocess.check_output(["date", "+%Y-%m-%dT%H:%M:%S%z"], text=True).strip()
    except Exception:
        start_ts = ""

    state_dir = os.path.join(cwd, ".claude", "state", "wrap")
    try:
        os.makedirs(state_dir, exist_ok=True)
        with open(os.path.join(state_dir, "start.json"), "w") as f:
            json.dump(
                {
                    "start_sha": start_sha,
                    "transcript_path": transcript_path,
                    "session_id": session_id,
                    "source": source,
                    "start_ts": start_ts,
                },
                f,
                indent=2,
            )
    except Exception:
        pass  # never break session start

    sys.exit(0)


if __name__ == "__main__":
    main()
