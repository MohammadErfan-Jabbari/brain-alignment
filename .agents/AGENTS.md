---
title: ".agents Compatibility Layer"
tags: [agent-contract, tooling]
aliases: [agents-layer, codex-agent-layer]
---

# .agents Compatibility Layer

This folder is intentionally minimal. It exists so Codex-style and other `.agents`-aware harnesses can find the repo's local agent apparatus without copying or translating the whole Claude setup.

## Canonical Sources

| Path | Status | Use |
|---|---|---|
| [`../AGENTS.md`](../AGENTS.md) | Canonical root contract | Load first for repo behavior, evidence rules, and read order. |
| [`skills`](skills) | Symlink to `../.claude/skills` | Shared repo skills; edit the `.claude` target, not a copy. |
| [`agents`](agents) | Symlink to `../.claude/agents` | Shared subagent role definitions; treat as source material for delegation or role emulation. |

## Maintenance Rules

- Keep this layer small until Erfan asks for a specific Codex-native mapping.
- Do not add command, workflow, hook, or settings mappings here yet.
- If `../.claude/skills` or `../.claude/agents` moves, update the symlinks in the same change.
- Do not create non-root `README.md` files; folder-local guidance belongs in `AGENTS.md`.
