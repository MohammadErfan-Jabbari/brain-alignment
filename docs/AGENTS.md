---
title: "Docs Agent Guidance"
tags: [agent-contract, docs]
aliases: [docs-contract]
---

# Docs Agent Guidance

The operating contract, the four authorities, the evidence transaction, and the session rules live in the root [`AGENTS.md`](../AGENTS.md) and are not restated here. This file owns only what is specific to `docs/`: where things live, and the rules that exist because this folder is simultaneously a GitHub repository and an Obsidian vault.

## Main map

| Path | Purpose |
|---|---|
| `status.md` | Operational state, blockers, and next actions. Read first |
| `00-charter.md` | Problem and scope |
| `01-research-landscape.md` | Literature frontier |
| `02-environment.md` | Compute, data, and run instructions |
| `03-methodology.md` | Evidence and authority contract |
| `04-data-benchmarks.md`, `05-dataset-registry.md` | Dataset facts |
| `06-theory-grounding.md` | Formal grounding |
| `experiments/` | Evidence records ([contract](experiments/AGENTS.md)) |
| `hypotheses/` | Falsifiable claims and their gates |
| `literature/canonical/` | Canonical paper notes ([contract](literature/AGENTS.md)) |
| `external-reviews/` | Verbatim, non-authoritative external-review provenance ([contract](external-reviews/AGENTS.md)) |
| `manuscript/` | Every manuscript tree and the writing gates ([contract](manuscript/AGENTS.md)) |
| `manuscript/rewrite/` | Canonical live scientific account, plus the maintained [question tree](manuscript/rewrite/question-tree.md) |
| `manuscript/submission/` | Supervisor-review derivative of `rewrite/`; never an authority |
| `learning/` | `/teach` lessons and the mastery ledger ([contract](learning/AGENTS.md)) |
| `references/` | Conventions, the confound catalog, the reasoning frame, and process records |
| `decisions/decisions.md`, `learnings.md` | Durable history: `Dnnn` decisions, `Lnnn` learnings |
| `timeline/` | Selected consequential session records ([contract](timeline/AGENTS.md)) |

## Rules specific to this folder

- Do not create a report, roadmap, dashboard, readiness matrix, audit memo, claim database, or global artifact registry here. Root states that none of them would be authoritative; this folder is where they would otherwise appear, so the rule here is that they are not created at all.
- Markdown must render in both GitHub and Obsidian: YAML frontmatter, relative Markdown links, no wikilinks, supported callouts only. The full contract is [`references/obsidian-conventions.md`](references/obsidian-conventions.md).
- Keep Markdown prose one paragraph per source line, the same rule root states for `.tex`. It is what makes `grep` a usable index across more than 150 documents.
- A new `Dnnn` or `Lnnn` is appended, never renumbered, and a superseded entry keeps its number with a currency note rather than being edited into agreement.
- A retired mechanism is removed from every file that asserts it is live, in the same commit that retires it. Three hooks stayed documented as active while dead, retired, or unenforced because this was done later and then not at all ([L077](learnings.md)).
- Update the nearest `AGENTS.md` when a subfolder's structure, commands, or traps change, and add its `CLAUDE.md` symlink in the same change.

## Related

- [Root operating contract](../AGENTS.md)
- [Evidence and authority contract](03-methodology.md)
- [Operational status](status.md)
