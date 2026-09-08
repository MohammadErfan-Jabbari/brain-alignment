---
title: "Claude Apparatus Agent Guidance"
tags: [reference, onboarding]
aliases: [claude-agents-guidance]
---

# Claude Apparatus Agent Guidance

This folder contains the Claude Code apparatus for the repo: subagents, hooks, skills, and settings, and nothing else. Runnable apparatus lives in the repo-root [`scripts/`](../scripts/AGENTS.md). Edit this folder as workflow infrastructure, not as research evidence.

## Rules

- Do not create `README.md` files here; folder-local guidance belongs in `AGENTS.md`.
- Keep root `AGENTS.md` as the shared operating contract; root `CLAUDE.md` symlinks to it so Claude Code auto-loads it.
- When changing agents, hooks, or skills, update the relevant docs or memories if the behavior matters outside Claude Code.
- Do not loosen evidence or writing gates without recording the reason in `docs/decisions/decisions.md`.

## Subfolders

| Path | Use |
| --- | --- |
| `agents/` | Specialized Claude subagent prompts. |
| `hooks/` | Automation and write/check gates. |
| `skills/` | Every stance and workflow entry point, one skill per directory. `/work` and `/wrap` set `disable-model-invocation: true`. |

## Dispatch contract

These apply to every spawn, so they are stated once here instead of retyped into each task prompt.

- **These rules bind the built-in agents too.** `Explore` and `general-purpose` do most of the spawning here, and every rule below applies to them unchanged: pass a deliberate `model`, compute the coverage floor yourself, reject a degenerate reply. The one thing they do not inherit is standing: a built-in agent gathers and reports, and its output is never the judgment at a scientific boundary that `agents/` covers.
- **A review agent is read-only and returns a verdict, not edits.** Give it no `Write` or `Edit`. Its output is its only product. Independence is the entire reason to spawn it: a reviewer that shares the working context under-detects, three residuals against roughly thirteen from a fresh pass (L055).
- **First-round subagent output is never merged.** A proposal is read, argued against by a reviewer, and reconciled before anything is applied. The point of the round is to establish that the change is an improvement, not that it exists.
- **Pass `model` on every spawn, and match it to the agent's frontmatter.** A global hook denies an Agent call that sets no `model`, and the value you pass overrides the definition's `model:`, so the frontmatter is the tier to match rather than the tier that ships. `effort:` has no spawn-time parameter at all: it is read only from the agent's own file, so changing it means editing that file. The recorded failure behind the rule: an inherited high thinking level burned a judge's entire 32k output cap and returned nothing twice, after which the provider exclusion-listed the model family for 24 hours and stalled a manuscript section by about seven hours.
- **Gate degenerate output instead of merging it.** A response below a plausible length or outside the declared format is rejected and re-dispatched, not reconciled. Off-task and 114-character replies have flowed downstream here before.
- **Compute coverage yourself before reading the findings.** Grep the scope for the items the child was asked to check, require one `ID:` block per item, and reject a `CHECKED:` count below that floor, along with any `RESULT: PASS` carrying `CHECKED: 0`. Spot-check two `RECORD: file:line` values against the file, because a fabricated citation is worse than silence. Retry once with the reason appended, then surface it rather than accepting. In the acceptance test one arm hit its floor exactly and another grouped items and under-reported by six, so the floor is the parent's number and never the child's claim.
- **Independent verification never runs the tool's own self-test.** A `--selftest` proves the script agrees with itself. Adjudicating a deterministic gate means fresh fixtures in a fresh session.
- **Smallest diff wins; reject churn.** A reviewer that proposes a rewrite where a sentence would do is proposing risk, not quality.

## Related

- [Root operating contract](../AGENTS.md)
- [Runnable apparatus](../scripts/AGENTS.md)
