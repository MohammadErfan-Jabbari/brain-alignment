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
- When changing commands, agents, hooks, or skills, update the relevant docs or memories if the behavior matters outside Claude Code.
- Do not loosen evidence or writing gates without recording the reason in `docs/decisions/decisions.md`.

## Subfolders

| Path | Use |
| --- | --- |
| `agents/` | Specialized Claude subagent prompts. |
| `commands/` | Slash-command workflows and stance entry points. |
| `hooks/` | Automation and write/check gates. |
| `skills/` | Repo-local skills and writing/research pipelines. |
