# brain-alignment — MSc thesis research repo

This repository is the execution and writing home for Erfan’s thesis on whether the linear mapping between LLM middle layers and human brain activation is a usable signal, with brain-alignment-guided distillation as the main test case. It is a single-paper research workspace, not a software product.

## Read first

1. [`docs/status.md`](docs/status.md): operational state, blockers, and at most five next actions.
2. Follow only the E-record and canonical-rewrite-manuscript links needed for the active action.
3. Use [`docs/03-methodology.md`](docs/03-methodology.md) for the authority and evidence contract.

## Four authorities

| Question | Authority |
| --- | --- |
| What was run and what did it produce? | `docs/experiments/ENNN_*.md` plus retained load-bearing artifacts |
| What does the thesis currently conclude? | `docs/manuscript/rewrite/` |
| Where are we and what happens next? | `docs/status.md` |
| Why did the project change? | decisions, learnings, selected consequential timelines, and Git |

No report layer, alternate status board, claim database, artifact registry, dashboard, or routine timeline is authoritative. `docs/manuscript/submission/` is a supervisor-review derivative, never an authority. An interrupted upstream correction sets `manuscript-sync-pending` until the canonical rewrite manuscript is synchronized.

> [!important] Sync suspension in force (from 2026-09-01, until Erfan lifts it)
> Erfan directed that `docs/manuscript/submission/` is the only manuscript tree being worked on, and that `docs/manuscript/rewrite/` is left untouched. For the duration:
> - **Do not edit `rewrite/`, and do not mirror any change into it.** Not for a scientific change, not for a prose fix, not for typography.
> - **Do not treat divergence between the trees as a defect.** `submission/` is the working tree; `rewrite/` is frozen at commit `5688de9`, where a clean twin audit over 41 file pairs found the two identical except for format-only lines. That commit is the exact divergence point.
> - **Do not dispatch `manuscript-twin-auditor`**, and do not act on a twin finding as though it required a fix. Its authority-direction rule assumes both trees are live.
> - **Check Git history before undoing anything.** A sentence missing from `submission/` may have been cut deliberately; `submission/AGENTS.md` permits condensation. Run `git log -S "<the sentence>"` before restoring it. This rule exists because restoring five sentences the owner had removed in `7345b63` is how the suspension was discovered to be needed.
> - `manuscript-sync-pending` is set in `docs/status.md` on purpose and is not a blocker to clear. It records that the sync-back is owed, not that it is due now.
> - `rewrite/numbers.tex`, `rewrite/acronyms.tex`, and `rewrite/references.bib` stay single-source and are still read across the tree boundary. Reading them is not editing `rewrite/`.
>
> Lifting this restores canonical-first: every submission-only change after `5688de9` flows back into `rewrite/`, and only then is `rewrite/` an authority again.
>
> **When it is lifted, retire it everywhere in the same commit.** This block is the only place that states the terms; six other sites point at it and each must lose its pointer, or a retired rule stays documented as live, which is exactly the failure [L077](docs/learnings.md) records. The sites are `docs/manuscript/AGENTS.md` (the `submission/` layout row, protocol step 14, and the synchronization sentence after the `--share-ready` rule), `docs/manuscript/submission/AGENTS.md` (the authority bullet and the `sections/` bullet), `docs/manuscript/rewrite/AGENTS.md` (the frozen callout under the title), and the `Manuscript:` line in `docs/status.md`. Verify with `grep -rn "sync.suspension\|Suspended until further notice" --include=AGENTS.md .` returning nothing.

## Skills are the entry points

Every workflow is a skill in `.claude/skills/`, one directory each. Two ways in, both first-class:

- **Auto-activation on matching intent** is the normal path and needs no invocation. This is what actually happened across 11,416 owner prompts in the rewrite era: the stance was inferred, never typed ([L078](docs/learnings.md)).
- **Explicit `/name`** forces one. `work` and `wrap` are explicit-only by construction (`disable-model-invocation: true`), so `/work` never auto-fires and `/wrap` never auto-commits.

| Skill | Job |
| --- | --- |
| `work` | lock, run, and record evidence; explicit-only |
| `interpret` | recompute and adjudicate recorded evidence |
| `write` | route manuscript prose work to the method and the gates |
| `question-led-writing` | the writing method: question tree, inference path, audits |
| `thinking-panel` | the four review methods: claims, bottlenecks, allocation, coordination |
| `teach` | transfer understanding from sources |
| `scout` | bring external literature or data into canonical records |
| `firecrawl-research-index` | the retrieval lane `scout` uses for papers |
| `plan` | choose direction without touching numbers |
| `review` | stress-test a result, claim, design, or manuscript |
| `meta` | simplify or maintain apparatus |
| `orient` / `wrap` | open and close a session |
| `precheck` | gate a design before compute |
| `manuscript-check` | run the deterministic manuscript gate |
| `session-mining` | answer a question from the session transcripts without reading them in |

State the active stance in one line and say when it switches. Reach for a skill rather than reconstructing its procedure inline; if a procedure is worth writing down twice, it belongs in the skill instead.

The four reasoning methods this repo reviews with are user-level skills at `~/.claude/skills/`: `test-claims`, `remove-bottlenecks`, `allocate-for-compounding`, and `coordinate-strategy`. `thinking-panel` is the repo handle for them and says which one a situation calls for; reach for the smallest applicable set, and never confuse them with the four adversarial subagents of `/review`.

## Evidence rules

- A scientific number is born in `/work` and recorded in an owning E record.
- Predeclare kill criteria, design, baselines, controls, seeds, stop rules, estimand, estimator, inference unit, and identifying assumptions.
- Use contiguous splits, nuisance controls, and confound subtraction for brain-alignment claims.
- Use at least three seeds for stochastic experiments; report specific estimates with uncertainty and the named test.
- Keep raw artifacts separate from interpretation. Record the reason for each non-obvious design choice when it is made.
- `/interpret` independently recomputes the load-bearing contrast, then uses adversarial review. Erfan confirms changed scientific verdicts.
- A missing value is a `\gap`, never a guess. A contradiction discovered outside `/interpret` is routed there rather than silently resolved.
- A predicted or defense-prep answer is advocacy, not evidence. Preparing persuasive answers for a viva or a reviewer is legitimate work, but such an answer is labeled as a prediction, is never copied into the manuscript or an E record, and never becomes the source of a number.

The evidence transaction is:

`artifact → E record → canonical rewrite manuscript if settled and paper-relevant → status if operations changed`

Only load-bearing gitignored artifacts cited by the manuscript receive stable paths and SHA-256 values, in their owning E records.

## Writing

The writing paradigm is **question-led**: a maintained question tree decides what the reader must understand, and a guided inference path makes each answer earned. Three owners, no fourth copy:

| Layer | Owner |
| --- | --- |
| Method | [`question-led-writing`](.claude/skills/question-led-writing/SKILL.md) skill |
| Repository gates, review set, approval routing | [`docs/manuscript/AGENTS.md`](docs/manuscript/AGENTS.md) |
| The maintained question tree itself | [`docs/manuscript/rewrite/question-tree.md`](docs/manuscript/rewrite/question-tree.md) |

Do not restate the method or the protocol anywhere else, including here. Enter through the `write` skill or by editing a manuscript file, which auto-loads the protocol.

Contract-level non-negotiables that outrank any procedure: prose reports only evidence recorded upstream, carrying `\evd{Ennn}` markers and keyed values from `numbers.tex`; a missing value is a `\gap`, never a reconstruction; `--share-ready` only when no gap remains and the manuscript is intended to ship; a contradiction found while writing routes to `/interpret` and sets `manuscript-sync-pending`. Do not create intermediate reports, claim lattices, convergence state, or checkpoint logs.

## Start and close

- `/orient` reads `status.md`, checks Git, and follows only the links needed for the first next action.
- `/wrap` updates only authorities that changed. A no-op session makes no documentation changes.
- Write a timeline only for a result, adjudication, correction, durable decision/learning, manuscript or submission milestone, or lasting failure.
- Update the nearest `AGENTS.md` when a folder’s structure, commands, workflow, or traps change.

## Working with Erfan

- **Produce nothing that was not asked for.** Outside `/teach`, do not create a new artifact, file, report, or scratch document beyond the ones that already exist. This is the general case of the anti-report rule above.
- **His standing preferences are files, not folklore.** [`memories/`](memories/AGENTS.md) mirrors fourteen recorded preferences covering how he wants questions asked, progress reported, sections drafted and cut, layout judged, agents briefed, and findings verified. Read the one that matches the work instead of rediscovering it. Across the transcripts the corrections he has actually had to repeat are about page layout and wasted vertical space, prose taste and em dashes, and terminology that drifts back after a decision; each has an owning memory.
- **Answer terse and scannable.** Lead with the answer, keep it short, and iterate. Do not lecture, do not restate the question, and do not pad a short answer to look thorough.
- **Match the autonomy to the work.** Three rungs, and guessing wrong is a recurring friction:
  - *Structural change to the repo or the apparatus:* confirm the list of changes before implementing.
  - *Manuscript drafting in flow:* propose the complete unit and apply it on an explicit approval.
  - *Long research or compute:* full autonomy. Do not stop until the steps are done or a finding worth publishing appears.
- **Interrupting Erfan:** if it is sensitive, say it immediately. Otherwise let him finish, then say where the mistake is.

## Agent fleet

Use agents at load-bearing scientific boundaries, not as a routine fan-out ritual. Where the table names an agent, spawn it rather than doing the job inline: a reviewer that shares the working context under-detects, three residuals against roughly thirteen from a fresh pass (L055). Independence is the reason to spawn, so a review agent gets no `Write` or `Edit`.

| Phase | Agents |
| --- | --- |
| Before compute | `anti-confound-designer` then `oracle-reviewer` via `/precheck` |
| After aggregated results | `stat-aggregation-auditor` |
| Result/claim stress test | `counter-argument`, `socratic-thinker`, `premortem-analyst`, `first-principles-grounder`, plus `oracle-reviewer` when warranted |
| Literature/data | `lit-scout`, `paper-digest`, `dataset-scout`, `dataset-verifier` |
| Manuscript verification | `evidence-number-auditor`, `citation-support-auditor`, `manuscript-twin-auditor` |
| Search and gathering | the built-in `Explore`, or `general-purpose` when the task needs to run commands as well as read |

The built-in agents are the workhorses and the table used to omit them: across the submission era they were 124 of 171 spawns, against 47 for every named agent combined. That is the right split, because most delegation here is finding things, not judging them. Use `Explore` whenever the answer means sweeping many files and you want the conclusion rather than the file dumps, and `general-purpose` when the sweep also has to execute something. Neither carries this repo's scientific judgment, so neither substitutes for a named agent at a boundary the table covers: a design gate, an aggregation audit, a claim stress test, or a manuscript verification pass. The dispatch contract in [`.claude/AGENTS.md`](.claude/AGENTS.md) applies to a built-in agent exactly as it does to a named one, including the coverage floor you compute yourself.

The three verification agents are the layer that checks whether what is written matches what is recorded, which the deterministic gate structurally cannot: it confirms an E record exists and a key is declared, and never opens the record. They are read-only by construction and carry no `Write` or `Edit`. Their rule corpus is [`docs/references/manuscript-verification-rules.md`](docs/references/manuscript-verification-rules.md), which may only gain checks; an auditor proposes a rule and never edits one.

Route by tier: fable for hard adversarial judgment (the `/review` panel and `oracle-reviewer`), opus for analysis, design, and recomputation, sonnet for navigation and gathering including the verification auditors, haiku only for genuinely mechanical extraction. Effort follows the job rather than the tier, and the spread is deliberate: `xhigh` for the five adversarial agents, whose whole value is detection depth; `high` for analysis, recomputation, and the citation judgment that decides whether a paper supports a claim; `medium` for resolve-and-compare verification and for gathering; `low` for `dataset-verifier`, which is a mechanical readiness check. Do not flatten these back to one value.

Each agent declares `model:` and `effort:` in frontmatter, and a spawn inherits neither from the parent. They are not equally live: `effort:` is settable only in the file, while `model:` is a default that the `model` passed at spawn time replaces, and a global hook rejects a spawn that passes none. So the spawn always picks the model, `agent_routing_lint.py` only warns when that pick leaves the tier, and the frontmatter value is the one to match.

Codex is an independent code critic or rescue implementation, not a scientific adjudicator. It never produces a thesis number or settles a verdict.

## Repository conventions

- `docs/` is both GitHub Markdown and an Obsidian vault. Follow [`docs/references/obsidian-conventions.md`](docs/references/obsidian-conventions.md): YAML frontmatter, standard relative Markdown links, no wikilinks, compatible callouts, hub links, and `## Related` footers.
- `.tex` files follow LaTeX conventions. Keep manuscript source search-friendly, with one sentence or paragraph per source line.
- Root `README.md` is the only README. Folder contracts live in `AGENTS.md`.
- Each folder contract is a real `AGENTS.md` with a sibling `CLAUDE.md` symlinked to it, so Claude Code auto-loads the same bytes every other harness reads. Edit `AGENTS.md`; Claude Code refuses to write through the link and will name the target.
- `.agents/` is only a compatibility symlink surface to `.claude/skills` and `.claude/agents`; keep it valid when those change.
- Use the three external knowledge owners rather than re-deriving: canonical paper notes, dataset registry, and [`docs/06-theory-grounding.md`](docs/06-theory-grounding.md). Do not re-OCR preprocessed course notes.

## Running code

- Always use `uv run`; add packages with `uv add`.
- Set `HF_HOME=/home/centcom/data/hf-cache` to reuse models.
- Python 3.11, torch cu128, 4× L40S, single node; no Slurm, Docker, or tmux.
- Heavy artifacts belong under gitignored `data/` and `outputs/`, never the overlay root.
- The shell is zsh with `noclobber`: `> file` fails with "file exists". Use `>|` or `rm -f` first.
- LaTeX builds use TeX Live 2023 through `latexmk` only. Tectonic is retired: its bundle is frozen at TeX Live 2021 and its biblatex disagrees with the system one, so mixing engines corrupts the build. See [L056](docs/learnings.md).
- Apparatus checks: `uv run python tests/test_bash_gate.py` (the Bash gate's 34 cases), `uv run python scripts/prose_lint.py --selftest`, and `uv run python scripts/manuscript_check.py`. Run the relevant one after changing a hook, the prose floor, or manuscript source.

## Git

- Commit every meaningful step atomically with a conventional message.
- Stage explicit paths only; never `git add -A` or `git add .`.
- Do not amend. Do not use destructive operations without explicit approval.
- Preserve unrelated user changes in a dirty worktree.
- At close, push completed commits to `origin` unless Erfan says not to or the push is blocked.

## Session history (Codex)

Most of this repo's work was carried out in Codex sessions. When docs/ and Git do not explain what was done or how a decision was reached, consult those transcripts before asking Erfan or guessing:

- `~/.codex/sessions/**/rollout-*.jsonl` and `~/.codex/archived_sessions/`. Select with `grep -l brain-alignment`; several hundred transcripts exist.
- `~/.codex/history.jsonl` holds the prompt log.

Transcripts are process evidence, not authority. They explain how a decision was made; the four authorities still record what stands. Query with `ctx_execute` or grep and print only extracted answers; raw transcripts are far too large to read into context.

## Reasoning

Use [`docs/references/reasoning-frame.md`](docs/references/reasoning-frame.md): delete false constraints (Elon), explain the mechanism and failure boundary plainly (Feynman), prefer the smallest durable change that compounds (Naval), and name the estimand/estimator/identifying assumption before interpreting a measurement.

## External tools

- Firecrawl and other web tools are retrieval providers subordinate to the docs authorities. Use the `firecrawl-research-index` skill for literature retrieval. They do not produce thesis numbers.
- Prefer context-mode’s indexed/search tools when available for large transcript or repository analysis; do not dump raw large files into model context.
- Secrets stay in configured environment files and are never committed.
