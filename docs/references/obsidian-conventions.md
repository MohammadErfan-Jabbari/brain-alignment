---
title: "Obsidian & Markdown Conventions (the container layer)"
tags: [reference, methodology]
aliases: [obsidian-conventions, markdown-conventions, vault-conventions]
---

# Obsidian & Markdown Conventions — the container layer

**This is the canonical spec for how every `.md` file in this repo is *structured*.** It is the
*container*; the *prose body* of reports and manuscripts is owned by `/write` (the `sci-write-v2`
pipeline). The rule of thumb:

> **Structure from these conventions; words from `/write`.** Frontmatter, links, tags, callouts and
> hub layout follow this file. The scientific argument, the claim↔evidence binding, the `[E0nn]`
> cites and every number follow `/write` and its hooks. The two never overlap.

`.tex` files are LaTeX, not Markdown — these conventions do **not** apply to them (only `/write` does).

## Why these and not the Obsidian defaults

The repo is simultaneously a **GitHub repo** (remote `origin`) and an **Obsidian vault**. Everything
here must render correctly in *both*. That forces one deliberate override of the `obsidian-markdown`
skill:

- **Internal links are standard Markdown `[text](path.md)`, NOT `[[wikilinks]]`.** The skill
  recommends wikilinks for in-vault links; we reject that because `[[ ]]`, `![[ ]]` embeds and
  `^block-refs` render as literal junk on GitHub. **Standard Markdown links create Obsidian graph
  edges exactly like wikilinks do** — so we lose nothing in the graph and keep GitHub clean. (Proof:
  `data/reference-repos/awesome-llm-apps` is 100% standard Markdown and lights up perfectly in the
  graph.)

We adopt the rest of the skill's syntax knowledge (frontmatter/properties, tags, callouts, math,
mermaid). For Obsidian syntax questions, route to the `obsidian-*` skills:

| Need | Skill |
|---|---|
| Markdown syntax / formatting | `obsidian-markdown` |
| Database / table views over notes | `obsidian-bases` |
| Visual canvas boards | `json-canvas` |
| Driving the Obsidian app from the shell | `obsidian-cli` |
| Web page → clean Markdown | `defuddle` |

## 1. Frontmatter (every `.md` file)

Every doc opens with YAML frontmatter:

```yaml
---
title: <human-readable title>
tags: [<rung?>, <type>]
aliases: [<code handle>, <nickname>]
---
```

- **`title`** — the human title (Obsidian shows it; node label stays the filename).
- **`tags`** — from the controlled vocabulary below. Powers the tag pane, filtered search, and graph
  colour groups.
- **`aliases`** — **the code-system handle goes here** (`R07`, `E017`, `D048`, `Q2`) plus any
  nickname. This makes the `Qn/Ennn/Dnnn/Lnnn` codes searchable and link-resolvable in Obsidian
  without linkifying every inline mention.

## 2. Controlled tag vocabulary

Keep it small and exact (one handle per concept — no synonyms).

- **Rung** (when the doc is about one): `Q0` `Q1` `Q2` `Q3` `Q4` `Q5`
- **Type** (always one): `report` `experiment` `decision` `learning` `reference` `manuscript`
  `dataset` `literature` `timeline` `methodology` `hypothesis` `charter`

Example — a report on Q1: `tags: [Q1, report]`. An experiment record: `tags: [experiment, Q3]`.

## 3. Links — the standard-Markdown rule

- A cross-reference to another file is a **real relative link**, never bare backticked text.
  - ❌ `` see `ladder.md` ``
  - ✅ ``see [`ladder.md`](../ladder.md)`` (backticks inside the link keep the monospace look and
    render as a clickable link in both GitHub and Obsidian)
- Paths are **relative to the current file**. A link from `docs/reports/R07.md` to the ladder is
  `[`ladder.md`](../ladder.md)`.
- **Do not linkify the dense inline code tokens** (every `Q2`, `E017`, `D048` in prose). That is
  noise and churn. The graph connects through **hubs + the "Related" footer** (§5), and the codes
  resolve through **aliases** (§1). Linkify only: (a) hub→child links, (b) the "Related" footer, (c)
  the first/defining mention of another doc in prose where a reader would click.
- **`[E0nn]` evidence cites stay verbatim.** They are a `/write` content convention bound to the
  honesty hook — never rewrite them into links.

## 4. Callouts — the 5 cross-compatible types only

GitHub and Obsidian share exactly five alert types. Use only these (case-insensitive):

```markdown
> [!NOTE]
> ...
> [!TIP]
> ...
> [!IMPORTANT]
> ...
> [!WARNING]
> ...
> [!CAUTION]
> ...
```

**Banned** (Obsidian-only — degrade to plain blockquotes on GitHub): every other callout type
(`[!info]`, `[!question]`, `[!example]`, …) and the foldable `-`/`+` suffix.

## 5. Hub notes and the "Related" footer

The connected graph comes from this pattern (the same one that centres `awesome-llm-apps`):

- **`map.md`** is the master hub — the graph centre. It links to the main docs.
- **Every `README.md`** is its folder's hub: it links down to the notable files in that folder.
- **Every substantive note ends with a `## Related` footer** linking *up* to its hub and *across* to
  its key siblings:

  ```markdown
  ## Related
  - [`ladder.md`](../ladder.md) — status board
  - [`R06`](R06_alignment-signal-is-real-beyond-confounds.md) — the prior finding
  ```

Hub-down + Related-up is what makes the graph connect, with zero risky edits to prose.

## 6. Banned everywhere (GitHub-incompatible)

- `[[wikilinks]]` and `[[note|alias]]`
- `![[embeds]]` (use standard `![alt](path.png)` for images)
- `^block-references`
- `%%Obsidian comments%%` (invisible on GitHub — use normal prose or HTML comments if truly needed)
- `==highlight==` (renders literally on GitHub)
- Obsidian-only callout types and foldable callouts (§4)

Allowed and cross-compatible: standard Markdown, GFM tables, task lists, footnotes, fenced code,
`$LaTeX$` math, ` ```mermaid ` diagrams, the 5 alerts, YAML frontmatter.

## 7. The `.obsidian/` folder and `.claude` visibility

- `.obsidian/` is **tracked in git** (shared view config: `app.json`, `appearance.json`,
  `core-plugins.json`, `graph.json`, `themes/`). Only `workspace.json` is gitignored (per-machine
  cursor/pane churn).
- Obsidian hard-hides any folder starting with `.`, so `.claude` is invisible by default. Three
  non-dot **symlinks at the repo root** expose the writable apparatus for review:
  `claude-agents → .claude/agents`, `claude-commands → .claude/commands`,
  `claude-skills → .claude/skills`. (Regenerate with the one-liner in the repo root if a checkout
  drops them.) `.claude/state` and `.claude/worktrees` are deliberately *not* exposed (machine state
  / git worktrees — noise).

## 8. Reports & manuscript — container only, body is `/write`'s

For `docs/reports/*.md` and `docs/manuscript/`: apply the **container** (frontmatter, hub backlinks,
a Related footer) but **do not touch the prose body, the `[E0nn]` cites, or any number** outside a
real `/write` session — those files are guarded by the `honesty_writecheck` + `ai_tell_lint` hooks
and the signed `sci-write-v2` acceptance suite.

## Related
- [`README.md`](../README.md) — the docs map
- [`map.md`](../map.md) — the master hub / code system
- [`03-methodology.md`](../03-methodology.md) — how we work (deliverable layers)
