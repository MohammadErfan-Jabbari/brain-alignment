#!/usr/bin/env python3
"""PreToolUse gate for agent spawns: model routing (D013/D026, hardened D068).

Two tiers, deliberately different:

- fable is DENIED. A ban that only warns is not a ban, and the warning form let
  every fable spawn through since the hook was written.
- the opus preference for judgment-heavy agents stays a stderr warning, because
  it is a preference and a wrong deny would break a legitimate spawn.

Decides from `tool_input` alone (subagent_type, model). Reads no repo path.
A missing model is left to the global require-subagent-model hook, which denies it.
"""
import json
import sys

OPUS_AGENTS = {
    "counter-argument", "socratic-thinker", "premortem-analyst",
    "first-principles-grounder", "oracle-reviewer",
    "stat-aggregation-auditor", "anti-confound-designer", "paper-digest",
}
# Exempt (task-dependent / lower tier): lit-scout, dataset-scout (sonnet to gather),
# dataset-verifier (sonnet); use haiku only for truly mechanical extraction.


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input", {}) or {}
    sub = (ti.get("subagent_type") or "")
    base = sub.split(":")[-1]
    model = (ti.get("model") or "").lower()
    if "fable" in model:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"fable is banned in this repo (D013/D026); '{base or 'agent'}' was routed "
                f"to model='{model}'. Use opus for analysis/design/judgment, sonnet for "
                "navigation/gathering/verification, haiku only for mechanical extraction."
            ),
        }}))
        return 0
    warns = []
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
