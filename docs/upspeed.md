---
title: "Upspeed — last-session state (read first)"
tags: [reference]
aliases: [upspeed]
---

# Upspeed — read first, write last

**Last updated:** 2026-06-26 (S44 — **/meta: made the repo an Obsidian-native vault.** Wrote + ratified
the markdown conventions spec ([`obsidian-conventions.md`](references/obsidian-conventions.md)), added
frontmatter + `## Related` footers to 183 docs, linkified references repo-wide (330 + 268 path-links +
123 citation-links, clickable cites), tracked `.obsidian/`, exposed `.claude` via symlinks, set
links-open-in-new-tab. 6 commits, all pushed. **NO experiment, NO science number, NO rung change —
Q0–Q5 stand.** Prior: S43 — /meta: D048 `/write` cutover (sci-write-v2 is the default engine).)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged since S25). With no
> task, run `/orient`. **Next session: `/write` R07 to evaluate sci-write-v2 on real prose.**

## What this session did (/meta — Obsidian vault overhaul)
- **Conventions spec + apply.** [`obsidian-conventions.md`](references/obsidian-conventions.md) is the
  binding ruleset for all markdown: link every in-repo reference (bare backtick paths banned),
  citations link to their canonical note on first mention, clickable cites, one-line-per-paragraph,
  `-`-only bullets, escape `\|` in tables, one H1 + no emoji in headings, no trailing whitespace; 5
  cross-compatible callouts only; banned wikilinks/embeds/highlights. Em-dashes banned in NEW prose
  only (Erfan option A; existing ~4.9k left). Exemptions: `_prior-work/`, `graphify-out/`.
- **Graph connects** via frontmatter (title/tags/aliases) + `## Related` footers on 183 docs, with
  [`ladder.md`](ladder.md) + [`map.md`](map.md) as hubs; graph.json colours by tag/path.
- **`.claude` is visible** in Obsidian via `claude-agents`/`claude-commands`/`claude-skills` symlinks.
- Verified: 0 broken links; all link edits wrap-only (numbers/claims/`[E0nn]` cites untouched).

## What's next (resume here)
- **`/write` R07** (Q1 — "plain KD does not preserve alignment") — redo the report through the
  `sci-write-v2` pipeline to **evaluate the new `/write` skill on real prose**. This is the session's
  original goal, deferred by the Obsidian work.
- **Live science thread (UNCHANGED since S25):** `/work` Q4 sample-efficiency E024, OR `/write` R08
  (Q2), OR `/interpret` the parked E006 voxelwise-CI item. Erfan's call.
- **Deferred Obsidian cleanup (optional):** targeted hard-wrap reflow of `paper-digest` output;
  folder-index notes for `experiments/`/`timeline/`; cosmetic bullet/emoji-heading tidy.

## Blockers / open loops
- **`docs/manuscript/00_paper-draft-v0.md` was link-edited** this session (container links only — no
  prose/number/register change; no `/write` ran). No clean register verdict exists for its current
  bytes; that is for a future `/write` session, not owed here.
- **One untracked stray** left untouched: [`docs/learning/lessons/2026-06-24-boruta-feature-selector.md`](learning/lessons/2026-06-24-boruta-feature-selector.md)
  (foreign to repo conventions, per Erfan). Working tree otherwise clean; all pushed.

## Key facts for next session
- **The vault conventions are law:** [`obsidian-conventions.md`](references/obsidian-conventions.md).
  When writing any `.md`, follow it (link references, frontmatter, no bare backtick paths). `/write`
  still owns report/manuscript prose bodies.
- **Pushing:** the `origin` remote is HTTPS with no stored creds; `gh` is authed (token, `repo` scope),
  so run `gh auth setup-git` once then `git push origin main` works.
- **obsidian-linter is app-only** (no CLI); if enabled in-app, disable its `yaml-title-alias` rule (it
  dirties frontmatter on save). CLI lint layer = `markdownlint-cli2` + `lychee` (not installed).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`.
- **Wrap gotcha (hit this session):** on a compacted/resumed session `start.json` holds a mid-session
  SHA (`source: "compact"`) — use the first-commit-parent fallback for the true changeset.
