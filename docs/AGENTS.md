# Docs Agent Guidance

## Load order

1. [`status.md`](status.md) for current state and the next action.
2. Follow only the E-record and manuscript links required for that action.
3. Use [`03-methodology.md`](03-methodology.md) for evidence and authority rules.

## Authorities

| Need | Owner |
|---|---|
| Evidence, provenance, experiment verdict | `experiments/ENNN_*.md` plus retained artifacts |
| Current scientific interpretation | `manuscript/rewrite/` |
| Operational state and next actions | `status.md` |
| Historical rationale | `decisions/`, `learnings.md`, selected timelines, Git |

Do not create a report, roadmap, dashboard, readiness matrix, audit memo, routine timeline, claim database, or global artifact registry.

## Rules

- Numbers originate in E records and must carry the correct inference unit and uncertainty.
- Route scientific contradictions to `/interpret`; do not resolve them during cleanup or prose editing.
- Write settled paper-relevant interpretation directly into the canonical rewrite manuscript.
- Set `status.md` to `manuscript-sync-pending` whenever an upstream correction has not yet reached the manuscript.
- Update only authorities whose state changed. No-op sessions create no documentation churn.
- Timeline logs are exceptional: result, adjudication, correction, durable decision/learning, manuscript or submission milestone, or lasting failure only.
- Markdown must render in GitHub and Obsidian: relative Markdown links, no wikilinks, controlled frontmatter, supported callouts only.
- Keep report/manuscript prose one paragraph per source line. LaTeX files follow LaTeX conventions, not Obsidian conventions.
- Update the nearest `AGENTS.md` whenever folder structure or recurring commands change.

## Main map

| Path | Purpose |
|---|---|
| `00-charter.md` | Problem and scope |
| `01-research-landscape.md` | Literature frontier |
| `02-environment.md` | Compute, data, and run instructions |
| `03-methodology.md` | Research and authority contract |
| `04-data-benchmarks.md`, `05-dataset-registry.md` | Dataset facts |
| `06-theory-grounding.md` | Formal grounding |
| `status.md` | Current operations |
| `experiments/` | Evidence records |
| `hypotheses/` | Falsifiable claims and gates |
| `literature/canonical/` | Canonical paper notes |
| `external-reviews/` | Verbatim, non-authoritative external-review provenance |
| `manuscript/rewrite/` | Canonical live scientific account |
| `manuscript/submission/` | Supervisor-review derivative of `rewrite/`; never an authority |
| `learning/` | `/teach` lessons and the mastery ledger |
| `references/` | Conventions and shared reference material |
| `decisions/`, `learnings.md` | Durable history |
| `timeline/` | Selected consequential session records |

Use `uv run` for Python. Heavy artifacts belong in gitignored `data/` or `outputs/`.
