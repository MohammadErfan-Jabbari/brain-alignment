---
title: "Claude Apparatus Agent Guidance"
tags: [reference, onboarding]
aliases: [claude-agents-guidance]
---

# Claude Apparatus Agent Guidance

This folder contains the Claude Code apparatus for the repo: commands, subagents, hooks, and skills. Edit it as workflow infrastructure, not as research evidence.

## Rules

- Do not create `README.md` files here; folder-local guidance belongs in `AGENTS.md`.
- Do not edit `.claude/state/` for shared knowledge. It is ignored per-worktree session state.
- Keep root `CLAUDE.md` as the shared operating contract; root `AGENTS.md` symlinks to it for non-Claude agents.
- When changing commands, agents, hooks, or skills, update the relevant docs or memories if the behavior matters outside Claude Code.
- Do not loosen evidence or writing gates without recording the reason in `docs/decisions/decisions.md`.

## Subfolders

| Path | Use |
|---|---|
| `agents/` | Specialized Claude subagent prompts. |
| `commands/` | Slash-command workflows and stance entry points. |
| `hooks/` | Automation and write/check gates. |
| `skills/` | Repo-local skills and writing/research pipelines. |
| `state/` | Ignored local state; do not treat as shared truth. |
