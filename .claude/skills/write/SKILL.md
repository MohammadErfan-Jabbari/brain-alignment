---
name: write
description: >-
  Draft settled, paper-relevant evidence into the canonical rewrite manuscript. Use for any
  docs/manuscript/ prose work. This is an entry point, not a method: the method is the
  question-led-writing skill and the gates are the manuscript writing protocol.
tools: Read, Write, Edit, Bash, Glob, Grep, Task, Skill
---

# Write

**Target:** the claim or manuscript scope passed with this skill. If none was passed, ask for it before acting.

This skill carries no writing loop of its own. It exists to route, because five separate copies of the loop had already drifted apart at the load-bearing gate ([D070](../../../docs/decisions/decisions.md)).

1. **Method:** invoke [`question-led-writing`](../question-led-writing/SKILL.md). It owns the question tree, the guided inference path, the Plan / Draft / Review / Revise branches, pass scopes, evidence states, and the audits. Do not substitute a summary of it.
2. **Gates:** follow the question-led writing protocol in [`docs/manuscript/AGENTS.md`](../../../docs/manuscript/AGENTS.md). It owns which tree to edit, `\evd{Ennn}` and keyed-value provenance, the review set, `manuscript_check.py`, and approval routing. That file auto-loads when you edit a manuscript file.
3. **Tree:** the maintained question tree lives in [`docs/manuscript/rewrite/question-tree.md`](../../../docs/manuscript/rewrite/question-tree.md) and is the single source for the questions. Update it in the same change whenever the argument's structure moves.

## Boundary

Reports settled evidence. Does not create a scientific number, adjudicate an experiment, apply scientific changes against the `submission/` derivative, or mark the manuscript share-ready before the deterministic checks and fresh independent review pass.

If prose work uncovers a contradictory or statistically suspect source, stop that claim, set `manuscript-sync-pending` in [`docs/status.md`](../../../docs/status.md), and route it to `/interpret`. Writing never adjudicates.
