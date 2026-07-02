---
title: "S49 - agent orientation and README migration"
tags: [timeline, session]
---

# S49 - agent orientation and README migration

## Purpose

Make the repository easier for future agents to enter cold, while respecting Erfan's rule that only the
root may have a `README.md` and folder-local guidance belongs in `AGENTS.md`.

## Stances

Dominant stance: `/meta`.

Also used: light `/review` hygiene while checking links, symlinks, and stale folder guidance.

## What happened

- Added root `AGENTS.md` as a symlink to `CLAUDE.md`, so Codex-style agents and Claude read the same root
  operating contract.
- Added `docs/repo-orientation.md` as a compact map of the repo structure, evidence trail, read order, and
  coding conventions.
- Mirrored Claude's saved project memories into `memories/*.md`, with `memories/AGENTS.md` as the autoload
  index.
- Read every tracked non-root `README.md`, migrated its useful content into the nearest `AGENTS.md`, and
  deleted the non-root README files.
- Updated links that pointed at deleted README files so they now point to `AGENTS.md` or the new orientation
  note.
- Added a standing root rule: whenever a folder's structure, workflow, commands, conventions, or recurring
  traps change, update the nearest folder `AGENTS.md` in the same change.
- Added the minimal `.agents` compatibility layer requested by Erfan:
  `.agents/AGENTS.md`, `.agents/skills -> ../.claude/skills`, and `.agents/agents -> ../.claude/agents`.
  Commands, workflows, hooks, and settings were intentionally not mapped.

## Decisions Made

- The root `README.md` is the only README in the tracked repo.
- `.claude/` remains the canonical apparatus for existing skills and subagent role definitions.
- `.agents/` is intentionally minimal for now. It exposes skills and agents by symlink only; further Codex-native
  command/workflow/hook mappings will happen step by step only if Erfan asks for them.

## Current Truth

No experiment ran, no science number was produced, and no ladder rung changed. Q0-Q5 stand exactly as before.
The official science next step remains `/write` Section 4.3 / Q2 and Figure 6 unless Erfan redirects.

## Next Session

- If continuing repo hygiene, inspect the minimal `.agents` layer in use before adding any more mappings.
- If returning to thesis work, default to `/write` Section 4.3 / Q2 and Figure 6.

## Friction & Improvements

- A generic link check surfaced old placeholder links unrelated to the README migration
  (`references/codex-usage.md`, `rel/path.md`, `path.png`, and similar examples). Left as pre-existing noise.
- The wrap start hook's `start_sha` predates several committed sessions, so `start_sha..HEAD` is broader than
  this S49 change. The close record separates today's uncommitted S49 meta work from older committed history.

## Related

- [`../repo-orientation.md`](../repo-orientation.md)
- [`../../CLAUDE.md`](../../CLAUDE.md)
- [`../../.agents/AGENTS.md`](../../.agents/AGENTS.md)
- [`../../memories/AGENTS.md`](../../memories/AGENTS.md)
