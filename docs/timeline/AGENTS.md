---
title: "Timeline Agent Guidance"
tags: [agent-contract, timeline]
aliases: [timeline-contract]
---

# Timeline Agent Guidance

This folder holds selected consequential session records. It is **not** an authority and **not** a log. Git already records what changed; the four authorities already record what stands. A timeline entry exists only to explain *why* a consequential turn happened, in a form Git's diff cannot carry.

## When an entry is written, and when it is not

Write one only for a result, an adjudication, a correction, a durable decision or learning, a manuscript or submission milestone, or a lasting failure.

Do not write one for a routine session, a cleanup, a no-op, a session that only read, or a session whose whole story is already in the commit messages. A session that changed nothing changes nothing here either. When a session produced a durable decision or learning, the entry points at the `Dnnn` or `Lnnn`; it does not restate its content, and it never becomes a second copy that can drift.

## Naming

`YYYY-MM-DD_slug.md`, one entry per consequential turn.

The convention drifted: the earliest 20-odd entries carry a `-HHMM` or `-Snn` infix (`2026-06-09-0013_scope-lock.md`, `2026-06-14-S14_...`) from when several entries landed in one day. Existing filenames are left alone, because links and Git history point at them. New entries use the date-only form.

## Shape

YAML frontmatter (`title`, `tags: [timeline]`, `aliases`), then the sections the recent entries use: the active stance, what changed, and what it means for the next action. Keep it short. An entry that grows past a screen is usually restating an authority it should be linking instead.

## Traps

- An entry is written after the fact and stays fixed. A later correction gets its own entry or a note in the owning authority; entries are not edited to agree with what was learned afterwards.
- A number that appears here is a quotation from its owning E record, not a source. If the two disagree, the E record wins and the discrepancy routes to `/interpret`.
- This folder passed the point of being comfortably readable some time ago. Prefer not writing an entry over writing a thin one, and treat every additional entry as needing to justify the ones a reader must skim past to reach it.

## Related

- [Docs guidance](../AGENTS.md)
- [Operational status](../status.md)
- [Decisions](../decisions/decisions.md)
- [Learnings](../learnings.md)
