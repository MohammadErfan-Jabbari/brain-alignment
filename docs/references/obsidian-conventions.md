---
title: "Obsidian & Markdown Conventions (the container layer)"
tags: [reference, methodology]
aliases: [obsidian-conventions, markdown-conventions, vault-conventions]
---

# Obsidian & Markdown Conventions — the container layer

**The canonical spec for how every `.md` file in this repo is *structured*.** The repo is at once a
**GitHub repo** (remote `origin`) and an **Obsidian vault**; every file must render correctly in
*both*. This file governs the *container* (naming, frontmatter, links, formatting, layout). The
*prose body* of reports and manuscripts is owned by `/write` (the `sci-write-v2` pipeline).

> **Structure from these conventions; words from `/write`.** The two never overlap. `.tex` files are
> LaTeX, not Markdown — these conventions do not apply to them (only `/write` does).

When writing or editing any `.md` file, follow the numbered rules below. The do/don't checklist at the
end is the fast reference. Obsidian syntax questions route to the `obsidian-*` skills (`obsidian-markdown`,
`obsidian-bases`, `json-canvas`, `obsidian-cli`, `defuddle`) — but **this spec overrides the skill's
wikilink default** (§4).

---

## 1. File naming

- Lowercase, hyphen-separated slugs: `04-data-benchmarks.md`, `oota-2024_speech-lms-lack-brain-semantics.md`.
- Code-system files carry their flat ID as the prefix: `E008_*.md`, `R07_*.md`, `H001_*.md`, and the decision/learning logs (`decisions/decisions.md`, `learnings.md`) hold `D`/`L` entries as in-file sections.
- **Zero-pad to the prefix's established width** (`E`/`H` = 3 digits, `R` = 2 digits). Do not renumber existing files; just match the width when adding one. *(Known inconsistency: `R` is 2-digit while `E`/`H` are 3 — kept as-is to avoid breaking refs; flagged, not fixed.)*
- Filenames are the Obsidian graph node label, so they must be self-describing.

## 2. Frontmatter (every tracked `.md`, except the exemptions in §11)

```yaml
---
title: "<human-readable title>"
tags: [<type>, <rung?>]
aliases: [<code handle>, <nickname>]
---
```

- **Key order is fixed:** `title`, `tags`, `aliases`. Nothing else unless a rule adds it.
- **`title`** — concise human title (≤ ~100 chars). Not the whole H1 sentence.
- **`tags`** — from the controlled vocabulary only:
  - **type** (exactly one, required): `report` `experiment` `decision` `learning` `reference` `manuscript` `dataset` `literature` `timeline` `methodology` `hypothesis` `charter`
  - **rung** (optional, when the doc is *about* one rung): `Q0`–`Q5`. Kept in `tags` intentionally so the graph can colour by rung.
- **`aliases`** — the code handle (`R07`, `E008`, `oota-2024`) plus any nickname, so the code system and paper keys resolve in search.
- No synonym tags, no one-off tags outside the vocab.

## 3. Prose formatting

- **One physical line per paragraph** (and per bullet, per table row). Let the editor soft-wrap. **Never hard-wrap a paragraph across multiple short lines** — hard wraps make diffs noisy and re-flow as broken double-spaced text. *(This is the single most violated rule by the `paper-digest` agent output — fix on touch.)*
- **No em-dashes** (`—` or the spaced ` — `) in new prose, per the global voice rule: use commas, parentheses, or separate sentences. The report/manuscript hook already enforces this. *(Existing docs predate the rule and carry ~4.9k uses; a repo-wide cleanup is a separate decision, not automatic.)*
- One blank line between blocks; a single trailing newline at EOF; **no trailing whitespace** (a trailing double-space is a stray markdown hard-break).

## 4. Links — link every reference; never a bare path

**The core rule: if you mention another file, doc, experiment, decision, or paper that has a page in this repo, make it a link.** A path or title in plain backticks is dead text — it is *not* clickable in either tool and defeats the vault.

- ❌ `` see `04-data-benchmarks.md` `` &nbsp;&nbsp; ❌ `` `decisions/decisions.md` `` &nbsp;&nbsp; ❌ "Anchors: Oota 2026"
- ✅ ``see [`04-data-benchmarks.md`](../04-data-benchmarks.md)`` &nbsp;&nbsp; ✅ `[Oota et al., 2026](../literature/canonical/oota-2026_brain-encoding-scale-compression.md)`

Rules:
1. **Internal links are standard Markdown `[text](relative/path.md)`, never `[[wikilinks]]`.** Standard links create Obsidian graph edges exactly like wikilinks *and* stay clickable on GitHub; wikilinks render as literal junk on GitHub. (Proof: `data/reference-repos/awesome-llm-apps` is 100% standard Markdown and the graph is fully connected.)
2. **Paths are relative to the current file** (`../experiments/E008_*.md` from a report). Verify the target exists.
3. **Evidence cites are clickable:** `[E003]` → `[E003](../experiments/E003_*.md)`. The `[E003]` form is preserved (the honesty checker matches it regardless of the trailing `(path)`), so the cite still validates *and* navigates.
4. **Literature citations link to the canonical note on first mention** in a doc: `[Negi et al., 2025](../literature/canonical/negi-2025_*.md)`. A "Surname YYYY" mention left bare when the canonical note exists is a defect.
5. **First meaningful mention per doc** gets the link (plus links in tables, lists, and the `## Related` footer). Don't linkify every one of dozens of inline repeats — that is a wall of links. Backticks remain correct for true non-navigable literals (a shell command, a config key, a filename with no page).
6. **Never link a bare `folder/`** as a navigation target — it's a dead click in Obsidian. Link to the folder's index note (`[reports](../reports/README.md)`) or leave it as plain text if no index exists.
7. External URLs are normal Markdown links; never bare URLs.

## 5. Callouts — the 5 cross-compatible types only

`> [!NOTE]` `> [!TIP]` `> [!IMPORTANT]` `> [!WARNING]` `> [!CAUTION]` (case-insensitive) render in both tools. **Banned:** every other type (`[!info]`, `[!question]`, …) and the foldable `-`/`+` suffix (Obsidian-only; degrade to plain blockquotes on GitHub).

## 6. Tables

- Every row's cell count must equal the header's. **Escape literal pipes inside a cell as `\|`** (an unescaped `|` — common in a command or a `→|` config string — silently breaks the table on GitHub).
- Blank line before and after the table.
- Status glyphs (✅/❌/🟡) inside table *cells* are fine and load-bearing.

## 7. Headings

- **Exactly one H1** per file, matching the title intent; the rest nest without skipping levels.
- **No emoji or decorative glyphs in headings** — they leak into the auto-generated anchor slug and make in-doc links fragile. Carry status as a trailing plain token if needed (`## Addendum (caution)`).
- Sentence case for scientific titles; no trailing `.`/`!` on a heading.

## 8. Lists & whitespace

- **One bullet marker repo-wide: `-`.** No `+` or `*` for unordered lists.
- Ordered lists and task lists are standard GFM.
- No raw HTML for content that must render in both tools (`<details>` does not collapse in Obsidian; a literal `<placeholder>` can be eaten as an unknown tag). Use plain Markdown; for a template placeholder use a backtick literal.

## 9. Banned everywhere (GitHub-incompatible)

`[[wikilinks]]` · `![[embeds]]` (use `![alt](path.png)`) · `^block-refs` · `%%comments%%` · `==highlight==` · Obsidian-only callouts (§5) · raw HTML for load-bearing content (§8).

Allowed and cross-compatible: standard Markdown, GFM tables/task-lists/footnotes, fenced code, `$LaTeX$` math, ` ```mermaid ` diagrams, the 5 alerts, YAML frontmatter.

## 10. Hub notes and the `## Related` footer

The connected graph comes from this pattern (what centres `awesome-llm-apps`):

- `map.md` is the master hub; every `README.md` is its folder's hub (links down to its notable files).
- Every substantive note ends with a `## Related` footer linking *up* to its hub and *across* to key siblings:

  ```markdown
  ## Related
  - [`ladder.md`](../ladder.md) — status board
  - [`R06`](R06_alignment-signal-is-real-beyond-confounds.md) — the prior finding
  ```

## 11. Exemptions

These trees are **not** held to the rules above (archival or machine-generated):

- `docs/literature/_prior-work/` — frozen provenance (the wikilinks / missing frontmatter there are inherent; never edited).

## 12. Tooling

`obsidian-linter` (platers) is **app-only — no CLI/headless mode** — so it is not an agent/CI gate; it is a *live formatter inside the Obsidian GUI* you may enable. If you do, set the safe rules (yaml-key-sort, consecutive-blank-lines, heading-blank-lines, blank-lines-around code-fences/tables, `-` list style, line-break-at-EOF) and **disable `yaml-title-alias`** (it injects a private `linter-yaml-title-alias` key into every file's frontmatter on save → git churn) and `capitalize-headings`.

The **agent/CI-runnable stack** (the actual enforcement layer):

| Tool | Type | Job |
|---|---|---|
| `markdownlint-cli2` | CLI, `--fix` | formatting gate (headings, blank lines, list style, trailing whitespace) |
| internal link-checker (`scratchpad`/repo script) | Python | every relative `[](*.md)` link resolves (0 broken) |
| `lychee` | CLI (CI, not pre-commit) | external-URL health |

Do **not** use Prettier — it re-wraps paragraphs, breaking §3.

## 13. The `.obsidian/` folder and `.claude` visibility

- `.obsidian/` is tracked (shared view config: `app.json` forces standard relative links in-app; `graph.json` colour-groups by tag/path; `appearance.json`, `core-plugins.json`, `themes/`). Only `workspace.json` is gitignored.
- Obsidian hides dotfolders, so `.claude` is exposed via root symlinks `claude-agents → .claude/agents`, `claude-commands → .claude/commands`, `claude-skills → .claude/skills`. `.claude/state` and `.claude/worktrees` are deliberately not exposed.

## 14. Reports & manuscript — container only, body is `/write`'s

For `docs/reports/*.md` and `docs/manuscript/`: the container rules apply (frontmatter, links, hub backlinks, Related footer), but **the prose body, the `[E0nn]` cites' text, and every number are `/write`'s** — change them only in a real `/write` session (they are guarded by the `honesty_writecheck` + `ai_tell_lint` hooks and the signed `sci-write-v2` suite). Making a cite *clickable* (adding the `(path)`) is a container edit and is allowed; rewording or re-citing is not.

---

## Do / Don't quick checklist

| Do | Don't |
|---|---|
| `[text](rel/path.md)` for every in-repo reference | bare `` `path.md` `` in backticks |
| link a paper's first mention to its canonical note | leave "Surname YYYY" unlinked |
| `[E003](../experiments/E003_*.md)` (clickable cite) | leave `[E003]` as dead text |
| one physical line per paragraph | hard-wrap a paragraph |
| `-` for every bullet | mix `-` / `+` / `*` |
| escape `\|` inside table cells; equal cell counts | unescaped `|` in a cell |
| plain heading text, one H1 | emoji in headings; multiple H1 |
| commas / parens / sentences | em-dashes in new prose |
| link to a folder's `README.md` | link a bare `folder/` |
| standard Markdown links | `[[wikilinks]]`, `![[embeds]]`, `==highlight==`, `%%comments%%` |

## Related
- [`README.md`](../README.md) — the docs map
- [`map.md`](../map.md) — the master hub / code system
- [`03-methodology.md`](../03-methodology.md) — how we work (deliverable layers)
