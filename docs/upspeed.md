---
title: "Upspeed - last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed - read first, write last

**Last updated:** 2026-07-02 (S49 - `/meta` agent orientation, README migration, minimal `.agents` layer. No experiment, no science number, no rung change.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md).** With no task, run `/orient`.

## Current state

S49 was a repo-hygiene `/meta` session. It made the repository easier for agents to navigate without changing the
scientific state.

The tracked repo now has root `README.md` as the only README. Folder-local guidance lives in `AGENTS.md` files.
Root `AGENTS.md` points to `CLAUDE.md`, and subfolder `AGENTS.md` files carry local maps, conventions, commands,
and traps for future agents.

No experiment ran, no result was interpreted, and no ladder rung changed. Q0-Q5 stand exactly as before.

## What was done

- Added root `AGENTS.md -> CLAUDE.md`.
- Added `docs/repo-orientation.md` with a compact repo map, evidence trail, first-read order, and coding conventions.
- Mirrored Claude's saved project memories into `memories/*.md`, indexed by `memories/AGENTS.md`.
- Migrated every tracked non-root README into the nearest useful `AGENTS.md`, then removed those non-root README files.
- Updated README links and folder links across docs/configs/timeline records to point at `AGENTS.md` or the new
  orientation note.
- Added a continuous-maintenance rule to `CLAUDE.md`, `/wrap`, and `session-logger`: when folder structure or workflow
  changes, refresh the nearest folder `AGENTS.md`.
- Added a deliberately minimal `.agents` layer:
  `.agents/AGENTS.md`, `.agents/skills -> ../.claude/skills`, and `.agents/agents -> ../.claude/agents`.
  Commands, workflows, hooks, and settings are not mapped yet.

## What to do next

- Official thesis next step remains `/write` Section 4.3 / Q2 and Figure 6, unless Erfan redirects.
- If continuing agent setup, keep it stepwise: test the minimal `.agents` skills/agents surface before mapping commands,
  workflows, hooks, or settings.
- When editing any folder, keep the nearest `AGENTS.md` fresh in the same change.

## Blockers / open loops

- Generic link checking still reports pre-existing placeholder/example links unrelated to the README migration
  (`references/codex-usage.md`, `rel/path.md`, `path.png`, and similar examples).
- Ignored third-party/downloaded README files may still exist under gitignored data/artifact directories; the tracked
  repo policy is root README only.
- The wrap start hook's `start_sha` predates several committed sessions, so `start_sha..HEAD` is broader than S49.
  Treat `git status --short` as the practical S49 working-tree inventory.

## Key facts

- `.agents/` is a compatibility layer, not a second apparatus.
- `.claude/skills` and `.claude/agents` remain canonical; `.agents/skills` and `.agents/agents` are symlinks.
- The root README rule is now explicit: do not create non-root `README.md` files.
