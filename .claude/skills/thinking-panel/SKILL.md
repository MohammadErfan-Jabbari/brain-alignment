---
name: thinking-panel
description: >-
  The four reasoning methods used as this repo's review set: test-claims, remove-bottlenecks,
  allocate-for-compounding, coordinate-strategy. Use when a claim, plan, allocation, or
  manuscript section needs structured review, when asked for "the four reviews", "the panel of
  four", "the four thinking skills", or "the smallest applicable set", and at every load-bearing
  manuscript boundary named by the question-led writing protocol.
tools: Read, Grep, Glob, Skill
---

# Thinking panel

Four reasoning methods, invoked by name. They are **user-level skills** at `~/.claude/skills/`, not repo agents and not personalities: apply them as functional methods and name the selected one only when it helps the reader.

| Skill | Answers | Reach for it when |
| --- | --- | --- |
| `test-claims` | Is this claim supported, contradicted, or still uncertain? | A conclusion is asserted, a verdict is proposed, or prose states more than its evidence carries |
| `remove-bottlenecks` | What is the one binding constraint on a clear goal? | Work is blocked, slow, costly, or stuck in rework; a reader cannot get through an argument |
| `allocate-for-compounding` | Where should limited time, attention, and length go? | Choosing what to pursue or stop, or deciding how much space a section earns |
| `coordinate-strategy` | How does this land with someone who can refuse or react? | Terminology, ownership, handoffs, supervisor-facing framing, whole-manuscript fit |

## Two panels, different things

This is the repo's most common naming collision, so state which one you mean:

- **This panel** is four *skills* and reviews reasoning, prose, allocation, and framing. It produces findings about the argument.
- **The `/review` panel** is four *subagents* (`counter-argument`, `socratic-thinker`, `premortem-analyst`, `first-principles-grounder`, plus `oracle-reviewer`) and adversarially attacks a scientific claim or design. It runs on fable per [D069](../../../docs/decisions/decisions.md) and produces `PANEL-VERDICT` blocks.

Use this panel for writing and direction. Use `/review` for a result, a verdict, or a design.

## How to run it

Use the **smallest applicable set**. One skill is the normal case; combine only when genuinely distinct failure modes are in play. Running all four is reserved for a load-bearing boundary, which the [question-led writing protocol](../../../docs/manuscript/AGENTS.md) defines as a subsection or section close, or a material change in framing, scope, ownership, or attention allocation.

Reconcile multiple outputs into one proposed revision before acting. Address each accepted finding, or say concretely why it conflicts with recorded evidence or a higher-level question.

Independence is the point of running them at all. A reviewer that shares the drafting context under-detects: the recorded failure is three residuals found in-session against roughly thirteen found by a fresh pass (L055).

## Boundary

These methods review reasoning and prose. None of them produces a scientific number, adjudicates an experiment, or flips a rung. A finding that would change a verdict, a claim's scope, or governing terminology routes to `/interpret` or to Erfan, per the approval rule in the writing protocol.

## Related

- [Question-led writing method](../question-led-writing/SKILL.md)
- [Manuscript writing protocol and gates](../../../docs/manuscript/AGENTS.md)
- [Review stance](../review/SKILL.md)
