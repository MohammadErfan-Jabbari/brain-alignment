#!/usr/bin/env python3
"""PreToolUse linter for agent spawns: model routing (D026, D068, D069).

Warn-only. It writes to stderr and always exits 0, so it can never break a spawn.
That is deliberate: after D069 there is no banned model left to deny, and every
remaining rule here is a *preference* about tier, where a wrong deny costs more
than a wrong warning. The two real denials in this repo live elsewhere: fable was
never the hazard, a model-less spawn is (global require-subagent-model.sh), and so
is an unsandboxed codex exec (bash_gate.py).

Decides from `tool_input` alone (subagent_type, model). Reads no repo path.
"""
import json
import sys

# Hard adversarial judgment: the /review panel plus the pre-compute design gate.
# D069 restores fable here, which is the rule D026 superseded only because the
# model had vanished. opus remains acceptable; anything below is a warning.
FRONTIER_AGENTS = {
    "counter-argument", "socratic-thinker", "premortem-analyst",
    "first-principles-grounder", "oracle-reviewer",
}
# Analysis, assembly, and recomputation: correctness matters more than adversarial
# depth, so these stay on opus rather than moving up.
OPUS_AGENTS = {
    "stat-aggregation-auditor", "anti-confound-designer", "paper-digest",
}
# Exempt (task-dependent / lower tier): lit-scout, dataset-scout (sonnet to gather,
# opus to analyze), dataset-verifier (sonnet). Use haiku only for truly mechanical
# extraction.

FRONTIER = ("opus", "fable")


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input", {}) or {}
    base = (ti.get("subagent_type") or "").split(":")[-1]
    model = (ti.get("model") or "").lower()
    warns = []
    if base in FRONTIER_AGENTS and model and not any(m in model for m in FRONTIER):
        warns.append(
            f"'{base}' is hard adversarial judgment and belongs on fable or opus; "
            f"got model='{model}'."
        )
    if base in OPUS_AGENTS and model and "opus" not in model:
        warns.append(
            f"'{base}' is analysis or recomputation and belongs on opus; got model='{model}'. "
            "(lit-scout / dataset-scout / dataset-verifier are task-dependent and exempt.)"
        )
    if warns:
        sys.stderr.write("[agent-routing-lint] " + " ".join(warns) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
