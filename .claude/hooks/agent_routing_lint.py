#!/usr/bin/env python3
"""PreToolUse linter for agent spawns — nudge model-routing (D013/D026).

Non-blocking by design: always exits 0 and only writes a warning to stderr, so it
can never break a spawn (incl. the workflow's own). Enforces what CLAUDE.md states
in prose: fable is banned; judgment-heavy agents belong on opus; lit-scout /
dataset-scout are task-dependent (sonnet to gather, opus to analyze) and are exempt.
"""
import json
import sys

OPUS_AGENTS = {
    "counter-argument", "socratic-thinker", "premortem-analyst",
    "first-principles-grounder", "oracle-reviewer",
    "stat-aggregation-auditor", "anti-confound-designer", "paper-digest",
}
# Exempt (task-dependent / lower tier): lit-scout, dataset-scout (sonnet to gather),
# dataset-verifier + session-logger (sonnet), paper-repo-extractor (haiku).


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input", {}) or {}
    sub = (ti.get("subagent_type") or "")
    base = sub.split(":")[-1]
    model = (ti.get("model") or "").lower()
    warns = []
    if "fable" in model:
        warns.append(
            f"fable is BANNED (D013/D026) — never route '{base or 'agent'}' to fable; "
            "use opus/sonnet/haiku."
        )
    if base in OPUS_AGENTS and model and "opus" not in model:
        warns.append(
            f"'{base}' is judgment-heavy and should run on opus; got model='{model}'. "
            "(lit-scout / dataset-scout are task-dependent and exempt.)"
        )
    if warns:
        sys.stderr.write("[agent-routing-lint] " + " ".join(warns) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
