---
name: review
description: >-
  Enter the review stance: stress-test a result, claim, design, or manuscript with the
  adversarial panel plus Codex when a script is in question. Read-only judgment.
tools: Read, Glob, Grep, Bash, Task, Skill
---
# Review mode

**Target:** the subject passed with this skill. If none was passed, ask for it before acting.

Stress-test a result, claim, or design on demand. The engine is the thinking panel plus Codex; this
stance spawns them and reconciles. Distinct from `/interpret`, which runs the panel as one step of
adjudicating a verdict; `/review` is the panel invoked standalone on any target.

## The procedure

- **The panel** (D017): `counter-argument` (attack the conclusion), `socratic-thinker` (expose hidden
  assumptions), `premortem-analyst` (assume it failed, trace back), `first-principles-grounder`
  (re-derive from mechanism and the math/papers). Plus `oracle-reviewer` in DESIGN mode before compute
  or RESULT mode after.
- **Codex** (the code-level critic the panel does not reach): `/codex:adversarial-review`, or a
  read-only persona panel via `codex:codex-rescue`. Use when the claim rests on a script.
- Each agent emits a machine-readable `PANEL-VERDICT` block. Verify each objection against the data,
  address the ones that hold, re-run until `PANEL-CLEAN:YES`.

## The standard

Review attacks the layer it names (the conclusion, or the code). It produces no science number and
flips no rung. A surviving objection is a finding to address, not a vote that overrules Erfan.

## Boundary

Critiques. It does not produce evidence (`/work`), land the verdict (`/interpret`), or write the report
(`/write`).
