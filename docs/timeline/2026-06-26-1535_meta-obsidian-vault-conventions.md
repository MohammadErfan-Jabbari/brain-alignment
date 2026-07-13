---
title: "S44 — /meta: Obsidian-native vault conventions + repo-wide apply"
tags: [timeline]
aliases: [S44]
---

# S44 — /meta: make the repo an Obsidian-native vault (conventions + apply)

**Date:** 2026-06-26 · **Stance:** `/meta` (sole). **NO experiment, NO science number, NO rung change — Q0–Q5 stand exactly as S43.**

This session started as "/orient → evaluate the `/write` skill" but Erfan redirected to a complete Obsidian overhaul of the repo. The `/write` R07 evaluation is deferred to the next session (the original goal).

## What this session did

Made the repo a first-class **Obsidian vault that still renders clean on GitHub**, in six atomic commits (all pushed to `origin`):

- **`c047ead`** — adopt the container-layer conventions: wrote [`obsidian-conventions.md`](../references/obsidian-conventions.md); added the `CLAUDE.md` routing block (structure from conventions, prose from `/write`); tracked `.obsidian/` (app.json forces standard relative links in-app; graph.json colour-groups by tag/path); created `claude-agents`/`claude-commands`/`claude-skills` root symlinks so Obsidian (which hides dotfolders) shows `.claude`.
- **`fda5a1b`** — frontmatter (title/tags/aliases) + a `## Related` footer on 183 docs (deterministic script), so the graph connects with `ladder.md` + `map.md` as hubs.
- **`2789c9c`** — linkified code/filename references repo-wide (8-folder sonnet/medium swarm + a reports/manuscript script): 330 links, clickable cites `[E003]`→`[E003](path)`.
- **`195525a`** — ratified the complete conventions spec (overhauled + extended), grounded in tool research + a repo anti-pattern audit (3 research/audit agents). Key rules: link every in-repo reference, citations link to canonical note on first mention, one-line-per-paragraph, escape `\|` in tables, one H1 + no emoji in headings, `-`-only bullets, no trailing whitespace; em-dashes banned in NEW prose only (Erfan: option A, existing ~4.9k left); exemption for `_prior-work/`.
- **`470836a`** — applied the conventions: 268 path-links + 123 citation-links (deterministic scripts) + a 10-agent sonnet/medium verify swarm that checked 342 links and fixed 24 errors (paren-swallowed citation spans, 7 dead folder-links in the former docs index, 2 broken tables in [`E004`](../experiments/E004_brain-loss-lever-test.md)/[`E021`](../experiments/E021_surprisal-residualized-cognitive-signal.md), 5 manuscript over-links). Verified: 0 broken links, content-safe (numbers/claims/`[E0nn]` cites untouched).
- **`57e460f`** — `alwaysOpenInNewTab: true` in `.obsidian/app.json` (links open in a new tab, vault-wide).

**Research findings (recorded in the spec):** `obsidian-linter` is app-only (no CLI; its `yaml-title-alias` rule injects a private frontmatter key on save → git churn, disable it); the agent/CI enforcement layer is `markdownlint-cli2` + `lychee` + an internal link-checker; Prettier is banned (re-wraps prose).

## Deferred / not done

- **Hard-wrap reflow** — no safe global rule (auto-reflow can't tell a hard-wrap from intentionally-separate lines; it wanted to touch 100+ structured docs). Needs a targeted per-file pass, mostly on `paper-digest` output.
- Cosmetic: mixed bullets, emoji-in-headings; folder-index notes for `experiments/`/`timeline/` (their README entries are plain text for now).

## Next session

`/write` on **R07** (Q1 finding-report) — redo it with the `sci-write-v2` pipeline to evaluate the new `/write` skill on real prose. This was the session's original goal.

## Related
- `ladder.md` — the canonical status board (Q0–Q5 unchanged)
- `upspeed.md` — current state
- [`obsidian-conventions.md`](../references/obsidian-conventions.md) — the ruleset this session built
