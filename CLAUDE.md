# brain-alignment — MSc thesis research repo

This repository is the execution and writing home for Erfan’s thesis on whether the linear mapping between LLM middle layers and human brain activation is a usable signal, with brain-alignment-guided distillation as the main test case. It is a single-paper research workspace, not a software product.

## Read first

1. [`docs/status.md`](docs/status.md): operational state, blockers, and at most five next actions.
2. Follow only the E-record and extended-manuscript links needed for the active action.
3. Use [`docs/03-methodology.md`](docs/03-methodology.md) for the authority and evidence contract.

## Four authorities

| Question | Authority |
|---|---|
| What was run and what did it produce? | `docs/experiments/ENNN_*.md` plus retained load-bearing artifacts |
| What does the thesis currently conclude? | `docs/manuscript/extended/` |
| Where are we and what happens next? | `docs/status.md` |
| Why did the project change? | decisions, learnings, selected consequential timelines, and Git |

No report layer, alternate status board, claim database, artifact registry, dashboard, or routine timeline is authoritative. Public manuscript cuts are immutable. An interrupted upstream correction sets `manuscript-sync-pending` until the extended manuscript is synchronized.

## Interaction stances

State the active stance and switch when work changes. The `stances` skill owns details.

| Stance | Job |
|---|---|
| `/work` | lock, run, and record evidence; explicit-only |
| `/interpret` | recompute and adjudicate recorded evidence |
| `/write` | draft settled claims directly into the extended manuscript |
| `/teach` | transfer understanding from sources |
| `/scout` | bring external literature/data into canonical records |
| `/plan` | choose direction without touching numbers |
| `/review` | stress-test result, claim, design, or manuscript |
| `/meta` | simplify or maintain apparatus |

## Evidence rules

- A scientific number is born in `/work` and recorded in an owning E record.
- Predeclare kill criteria, design, baselines, controls, seeds, stop rules, estimand, estimator, inference unit, and identifying assumptions.
- Use contiguous splits, nuisance controls, and confound subtraction for brain-alignment claims.
- Use at least three seeds for stochastic experiments; report specific estimates with uncertainty and the named test.
- Keep raw artifacts separate from interpretation. Record the reason for each non-obvious design choice when it is made.
- `/interpret` independently recomputes the load-bearing contrast, then uses adversarial review. Erfan confirms changed scientific verdicts.
- A missing value is a `\gap`, never a guess. A contradiction discovered outside `/interpret` is routed there rather than silently resolved.

The evidence transaction is:

`artifact → E record → extended manuscript if settled and paper-relevant → status if operations changed`

Only load-bearing gitignored artifacts cited by the manuscript receive stable paths and SHA-256 values, in their owning E records.

## Writing

Write directly from E records into `docs/manuscript/extended/`:

1. Read the owning E records and current section.
2. Apply [question-led writing](.claude/skills/question-led-writing/SKILL.md): map the document question to section and paragraph-level reader questions, with subsections only when useful.
3. State the intended answer, claim, scope, caveats, and evidence.
4. Draft with `\evd{Ennn}` markers and keyed values from `numbers.tex`.
5. Run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/extended`.
6. Run one fresh independent question-chain, prose, and scientific-scope review, revise, and obtain Erfan’s approval for load-bearing framing.

Use `--share-ready` only when every gap is resolved and the manuscript is intended to ship. Do not create intermediate reports, claim lattices, convergence state, or checkpoint logs.

## Start and close

- `/orient` reads `status.md`, checks Git, and follows only the links needed for the first next action.
- `/wrap` updates only authorities that changed. A no-op session makes no documentation changes.
- Write a timeline only for a result, adjudication, correction, durable decision/learning, manuscript/public milestone, or lasting failure.
- Update the nearest `AGENTS.md` when a folder’s structure, commands, workflow, or traps change.

## Agent fleet

Use agents at load-bearing scientific boundaries, not as a routine fan-out ritual.

| Phase | Agents |
|---|---|
| Before compute | `anti-confound-designer` then `oracle-reviewer` via `/precheck` |
| After aggregated results | `stat-aggregation-auditor` |
| Result/claim stress test | `counter-argument`, `socratic-thinker`, `premortem-analyst`, `first-principles-grounder`, plus `oracle-reviewer` when warranted |
| Literature/data | `lit-scout`, `paper-digest`, `dataset-scout`, `dataset-verifier` |

Use opus for analysis/design/judgment, sonnet for navigation/gathering, and haiku only for genuinely mechanical extraction. Fable is banned. Each agent declares `model:` and `effort:` in frontmatter.

Codex is an independent code critic or rescue implementation, not a scientific adjudicator. It never produces a thesis number or settles a verdict.

## Repository conventions

- `docs/` is both GitHub Markdown and an Obsidian vault. Follow [`docs/references/obsidian-conventions.md`](docs/references/obsidian-conventions.md): YAML frontmatter, standard relative Markdown links, no wikilinks, compatible callouts, hub links, and `## Related` footers.
- `.tex` files follow LaTeX conventions. Keep manuscript source search-friendly, with one sentence or paragraph per source line.
- Root `README.md` is the only README. Folder contracts live in `AGENTS.md`.
- `.agents/` is only a compatibility symlink surface to `.claude/skills` and `.claude/agents`; keep it valid when those change.
- Use the three external knowledge owners rather than re-deriving: canonical paper notes, dataset registry, and [`docs/06-theory-grounding.md`](docs/06-theory-grounding.md). Do not re-OCR preprocessed course notes.

## Running code

- Always use `uv run`; add packages with `uv add`.
- Set `HF_HOME=/home/centcom/data/hf-cache` to reuse models.
- Python 3.11, torch cu128, 4× L40S, single node; no Slurm, Docker, or tmux.
- Heavy artifacts belong under gitignored `data/` and `outputs/`, never the overlay root.

## Git

- Commit every meaningful step atomically with a conventional message.
- Stage explicit paths only; never `git add -A` or `git add .`.
- Do not amend. Do not use destructive operations without explicit approval.
- Preserve unrelated user changes in a dirty worktree.
- At close, push completed commits to `origin` unless Erfan says not to or the push is blocked.

## Reasoning

Use [`docs/references/reasoning-frame.md`](docs/references/reasoning-frame.md): delete false constraints (Elon), explain the mechanism and failure boundary plainly (Feynman), prefer the smallest durable change that compounds (Naval), and name the estimand/estimator/identifying assumption before interpreting a measurement.

## External tools

- Firecrawl and other web tools are retrieval providers subordinate to the docs authorities. Use the `firecrawl-research-index` skill for literature retrieval. They do not produce thesis numbers.
- Prefer context-mode’s indexed/search tools when available for large transcript or repository analysis; do not dump raw large files into model context.
- Secrets stay in configured environment files and are never committed.
