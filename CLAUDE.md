# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

# brain-alignment — MSc thesis research repo

This repo is the execution home for Erfan's master's thesis (ML for Health, UC3M) on **using the
linear mapping between LLM middle layers and brain activation as a usable signal** — with
**brain-alignment-guided distillation** as the first concrete use case. It is a single-paper research
workspace, not a software product.

## Interaction stances — invoke one, switch freely

Work in this repo runs by **interaction stance**, not by session type. The old working/analysis split is
retired (D044, supersedes D011). At any moment you are in one stance; **state the stance you are in** and
switch as the work turns. Eight stances, each setting a tone, an autonomy level, and the procedures it
arms, over one shared honesty spine. Mechanics: the `stances` skill (`.claude/skills/stances/`).
Day-to-day picture: `docs/operating-map.md`.

| Stance | Does | Touches a number? |
|---|---|---|
| `/work` | produce evidence (Design → Run → Judge); high-autonomy `/goal` runs; **explicit-only** | yes, produces |
| `/interpret` | turn a recorded result into an adjudicated verdict (claim-manifest + panel) | yes, adjudicates |
| `/write` | turn a finding into report/manuscript prose (the `scientific-writing` skill) | reports them |
| `/teach` | transfer understanding of any subject (concept, report, file, experiment, paper, question) into Erfan's head (guided-learning, rendered) | reads them |
| `/scout` | bring external papers/data in (`lit-scout`/`dataset-scout`/`paper-digest` → canonical notes) | external |
| `/plan` | set direction: roadmap, kill-gate triage, what to run next | no |
| `/review` | stress-test a result/claim/design (the thinking panel + Codex on demand) | no |
| `/meta` | build or maintain the apparatus (tooling, methodology, records) | no |

`/work` and `/interpret` are truth-producing and carry the strict standard (kill criteria, contiguous
splits, ≥3 seeds; strict adjudication). `/write`, `/teach`, `/scout` report or consume numbers under
cite-or-flag. `/plan`, `/meta` touch none. Auto-activation states the stance so you can redirect; only
`/work` is explicit-only.

The non-negotiable that binds all of them: **a number is born in a `/work` session and recorded in
`docs/`; no stance may state a result a working session did not record; a needed-but-missing number is a
`\gap` to flag, never invented or estimated.** This is armed by a **write-time hook** (D044), not by
memory: writes to `docs/reports/` and `docs/manuscript/` (the prose deliverables that use the
inline-cite convention) are checked regardless of stance, and the `/wrap` provenance audit is the
backstop. Raw evidence stays separate from interpretation.

**The three written deliverable layers (D035).** Written prose lands in one of three layers, not one
document: **reports** (`docs/reports/*.md`, Markdown) are the *continuous* single-topic synthesis layer
you write as work happens; the **extended manuscript** (`docs/manuscript/extended/`, LaTeX) is the
internal master (always-current paper body + append-only checkpoint log); the **public manuscript**
(`docs/manuscript/public/vN/`, LaTeX) is a frozen submission cut compressed from the extended. Knowledge
flows down only. **Route all report and manuscript writing through the `scientific-writing` skill, and
never auto-update the extended or public manuscript — they are rebuilt only at a checkpoint Erfan
explicitly calls.** Full spec: `docs/03-methodology.md` ("Deliverable layers"); skill:
`.claude/skills/scientific-writing/`.

## Read this first, every session

0. `docs/ladder.md` — **the canonical status board: which rungs are done, with what verdict, and the
   single next step (impl or analysis). This is the source of truth for project state — when any doc
   disagrees with it, it wins and the others get fixed.** With no specific task, run `/orient` (it reads
   the board and briefs you). **The code system and the whole journey-as-a-tree live in `docs/map.md`** —
   read it if the rung codes or the path lose you: **Q**n = ladder rung / research question (Q0–Q5, in climb
   order), **E**nnn = experiment (the evidence), **A**1–A3 = the three assumptions, **D**nnn = decision,
   **L**nnn = learning. Rungs were renamed **L→Q** in execution order on 2026-06-15 (D036); learnings stay
   **L**, and pre-2026-06-15 timeline logs keep the old L labels (`map.md` has the L↔Q table).
1. `docs/upspeed.md` — last-session prose: what ran, blockers, key facts.
2. `docs/tasks.md` — the granular backlog behind and ahead.
3. Then the relevant deep doc: `docs/00-charter.md` (idea/scope), `docs/01-research-landscape.md`
   (literature + the gap), `docs/02-environment.md` (compute/data/how-to-run),
   `docs/03-methodology.md` (how we work and why).

`docs/` is the persistent research brain — see `docs/README.md` for the full map. If something
matters past this session, it goes in `docs/`, not just in chat.

**Three external sources feed the thesis — use them, don't re-derive from them:** (1) the **papers**
(`docs/literature/canonical/`, frontier map in `01-research-landscape.md`); (2) the **datasets**
(`04-data-benchmarks.md`, `05-dataset-registry.md`); (3) Erfan's **master's coursework** in Information
Theory for ML and Probabilistic ML, mapped to the thesis in **`docs/06-theory-grounding.md`**. The
coursework is the math grounding: when a claim needs a formal bound/definition/theorem (the MI
generalization bound, the data-processing inequality, conditional MI = "unique R²", rate-distortion =
the F1 trade-off curve), cite the course note via `06-theory-grounding.md` instead of re-deriving it.
Raw notes live under gitignored `data/course-material/` (already preprocessed — **do not re-OCR the
lecture PDFs**; the `*_study.md`/`*_OCR.md` notes beat any fresh OCR pass).

**Reports (`docs/reports/`) are written full width — one line per paragraph, no hard wrapping.**

## How we run code

- **Always `uv run`.** This is a minimal uv project (Python 3.11, `.venv/`, `[tool.uv] package=false`
  — no `src/` scaffolding). Add libraries with `uv add <pkg>` as the work demands.
- Set `export HF_HOME=/home/centcom/data/hf-cache` to reuse cached models (Qwen2.5 0.5–7B, GPT-2
  family, pythia-1b).
- torch is pinned to the cu128 wheel index (already in `pyproject.toml`). 4× L40S available; single
  node, no Slurm/Docker/tmux — long runs are background processes.
- Heavy artifacts go under `data/` and `outputs/` (gitignored), never on the overlay root.

## How we do research (the spine, kept light)

Follow the epistemic path in `docs/03-methodology.md`: Notice → Commit → Map → **Claim** → **Design**
→ **Run** → **Judge** → Argue → Compound. The non-negotiables:

- Multiple competing hypotheses, not one cherished one. **Kill criteria predeclared.**
- **Lock the design before running** (baselines at matched budget, controls, seeds, stop rule).
- Keep raw evidence separate from interpretation.
- **Specific numbers with uncertainty and the named test.** "Δ = +0.06 ± 0.01, n=3, contiguous
  split" — never "it worked better." ≥ 3 seeds for stochastic experiments.
- Anti-confound is mandatory for any brain-alignment number (Feghhi/Oota): contiguous splits,
  nuisance baselines, gains shown after confound subtraction. See `docs/learnings.md` L003.
- Root cause, not symptom. Strongest baseline, never a strawman.

Use the repo's **reasoning toolkit** (`docs/references/reasoning-frame.md`) when designing or deciding:
the **Elon/Feynman/Naval** frame (real goal + delete false constraints; plain mechanism + where it breaks;
smallest durable change that compounds), and the **estimand-first** lens for any question resting on a
measurement (name the estimand, the estimator, and the identifying assumption that ties them; ask whether a
dependence is real or common-cause). **The toolkit is living: when a new way of approaching a problem proves
itself on real work, record it there as a named lens (name + alternative names, when to reach for it, a
worked instance from our own work, and where its detailed form lives) — adding one only when it recurs or
clearly generalizes, and pruning what stops earning its keep.**

## Working with Erfan

- Direct, no ceremony. **Challenge when there are grounds** — don't agree by default; if he's wrong,
  say so and why. Prompts may have typos; infer intent.
- Simple/single-step → just do it. Complex/vague/risky → plan first, then go. If we discussed the
  plan this session, proceed freely.
- **Stop-hook / autonomous re-fires are not fresh intent (L031).** When an automated hook re-injects a
  standing "keep going" prompt, treat it as *continuation only until a newer explicit user instruction
  supersedes it.* Erfan's most recent explicit message wins over the auto-re-fire — on an explicit
  "wrap up / stop", wrap even if the hook keeps firing. The autonomous mandate is real but bounded by
  the last direct human instruction.

## Presentation — make answers easy to read

Format for the eye, functionally, scaled to the turn (a one-line answer needs none of this):

- **Whitespace and short paragraphs** over walls of text; break a long uniform run with a short line.
- **Tone:** plain and direct (the global voice); no decoration, no filler enthusiasm.
- **Tables** when three or more things are compared across the same dimensions, instead of a list the
  reader has to assemble mentally.

This is presentation, not voice (the voice rules are global). Formatting earns its place by aiding the
read, never as ornament.

## Git — commit continuously and atomically

The repo is a git repo on `main`. **Commit every meaningful step as its own scoped, atomic commit**
with a proper conventional-commit message (`docs:`, `feat(agents):`, `chore:`, …) so the git history
is a granular, inspectable record of file changes. Don't batch unrelated changes into one commit;
don't let work pile up uncommitted. (Decision D007.)

This is **in addition to, not a replacement for, the docs record.** Always keep recording decisions
in `docs/decisions/decisions.md` and writing a `docs/timeline/` log each session — docs carry the
*why*, git carries the *what/when*.

Rules (unchanged): scoped staging only — never `git add -A`/`.`; stage explicit paths; no `--amend`
(prefer a new commit); no destructive ops without explicit approval; **push only when asked.**

## Subagents (`.claude/agents/`)

| Agent | Use when |
|---|---|
| `lit-scout` | Search across sources for papers on a topic; return a ranked, deduped shortlist. (sonnet to gather / opus to analyze a specific paper) |
| `paper-digest` | Read a paper (PDF/arXiv/URL) → a canonical note in `docs/literature/canonical/`. (opus) |
| `oracle-reviewer` | Adversarially stress-test a hypothesis or design **before** committing compute (PASS/HOLD/KILL). Reproduces the prior HOLD-review value. (opus) |
| `session-logger` | At session end: write `docs/timeline/…`, REPLACE `docs/upspeed.md`, update `tasks.md`/`learnings.md`. (sonnet) |
| `wrap-auditor` | One read-only audit scope at session close, fanned out in parallel by `/wrap` on a heavy session; returns structured findings for the orchestrator to verify and apply. Never writes, never flips a rung. (sonnet; `ladder-integrity` scope → opus only when an experiment ran). D038. Now also invocable standalone mid-session with a single scope. |
| `stat-aggregation-auditor` | AFTER a multi-seed/arm run, re-compute the load-bearing contrast (within-seed vs pooled, bootstrap-unit, P-construction) — the run-then-judge stats check `counter-argument` only names. (opus) |
| `anti-confound-designer` | BEFORE oracle: assemble the locked control battery (nuisance / splits / matched-ppl / the 5-control battery) from `docs/references/confound-catalog.md`. (opus) |
| `dataset-verifier` | Mechanical data-readiness — response matrix present? shape? voxel mapper? timestamps? annex pulled? — to prevent mid-run walls. (sonnet) |
| `dataset-scout` | Find/characterize a new dataset (access / format / pipeline / prior-use); the dataset mirror of `lit-scout`. (sonnet to gather / opus to analyze) |
| `paper-repo-extractor` | One paper's repo → mechanical data/code/checkpoint/license extraction; built for fan-out. (haiku) |
| `prose-register-auditor` | Read a draft (report/manuscript) for the scientific-register tells the linter can't catch — anthropomorphized abstractions, self-narrated moves, internal-metaphor leakage, dramatized framing, reflex passive density. Spawned by the `scientific-writing` review pass for anything supervisor-facing; the dedicated voice reader (vs the panel, which attacks the claim). Read-only; never edits. (sonnet; D046/L054) |

The **`/precheck`** command (anti-confound-designer → oracle-reviewer → READY-TO-RUN) is the pre-compute gate; the full fleet rationale + the §4 thinker-prompt alignment live in `docs/references/agent-fleet-redesign.md`.

**The thinking panel** (D017) — four reasoning-methodology agents run *after a step produces a result/
verdict*, to find holes before the verdict lands in the ladder/docs/manuscript. Distinct from
`oracle-reviewer` (a *pre-compute* design gate); these are *post-step* analysts. The loop: run the
panel → verify each objection against the data → address the ones that hold → re-run the panel until no
hole survives.

| Agent | Lens | Use when |
|---|---|---|
| `counter-argument` | Red-team the conclusion — build the strongest case it's an artifact/over-claim. (opus) | A run produced a verdict; before believing it. |
| `socratic-thinker` | Expose hidden assumptions and undefined terms by asking, not asserting. (opus) | A direction feels settled too quickly; before locking a framing. |
| `premortem-analyst` | Assume it already failed (didn't replicate / rejected / defense collapsed); trace backward. (opus) | Before building heavily on a result or spending the next compute. |
| `first-principles-grounder` | Re-derive from mechanism + the math/papers (`06-theory-grounding.md`, canonical notes, course material). (opus) | A claim needs a mechanism, leans on a theorem, or might contradict a source. |

Model routing (Erfan's rule, set 2026-06-13; **fable is banned/removed — never select it**):
**opus** for anything that needs THINKING, ANALYSIS, or DESIGN — the thinking panel (`counter-argument`,
`socratic-thinker`, `premortem-analyst`, `first-principles-grounder`), `oracle-reviewer`, `stat-aggregation-auditor`, `anti-confound-designer`, and `paper-digest`
(comprehending + synthesizing a paper is analysis), and any experiment-design subagent. **`lit-scout` and
`dataset-scout` are TASK-dependent (Erfan, S24): sonnet for gathering / breadth, opus only when judging
relevance or analyzing a specific paper.** **sonnet** for navigating OUR docs — reviewing the up-to-date status of the docs,
finding a fact and all its traces, and record-writing (`session-logger`). **haiku** for simpler mechanical
fan-out (extraction, file-mapping, formatting). When in doubt whether a task "needs thinking" → opus.
Each agent declares its default in `model:` frontmatter; override per call when the task warrants.

## The fleet — what's available, and when it fires by default (self-activation)

Full rationale: `docs/references/agent-fleet-redesign.md`. **Fire these by default at the matching phase — don't wait to be asked; commoditizing the workflow so Erfan never re-explains it is the whole point.**

**Commands** (`.claude/commands/`): **`/orient`** (session start — where we are + next step; now also flags uncommitted work + a missed `/wrap`) · **`/precheck`** (pre-compute gate — `anti-confound-designer` assembles the control battery → `oracle-reviewer` gates it → `READY-TO-RUN`) · **`/goalsmith <item>`** (build the ≤4000-char single-line `/goal` condition for a working item, pointing at its PRD) · **`/wrap`** (session close — ritual + parallel `wrap-auditor` swarm). **Skills:** **`scientific-writing`** (all report/manuscript prose; the D011 number rule) and **`/graphify`** (code/corpus navigation); global gbrain/estack skills route via their resolvers.

**Agents** (`.claude/agents/`, 14) — grouped by *when* in the loop they run:
- **Pre-compute (BEFORE a run):** `anti-confound-designer` (assemble the battery) → `oracle-reviewer` (gate it, DESIGN mode).
- **Post-result (AFTER a run, before the verdict lands):** `stat-aggregation-auditor` (re-compute the contrast) + the thinking panel `counter-argument` · `socratic-thinker` · `premortem-analyst` · `first-principles-grounder` (+ `oracle-reviewer` RESULT mode). Each emits a machine-readable `PANEL-VERDICT:` block; reconcile to `PANEL-CLEAN:YES`.
- **Data / literature:** `dataset-verifier` (is the data usable) · `dataset-scout` (find/characterize new data) · `lit-scout` (find papers) · `paper-digest` (canonical note) · `paper-repo-extractor` (mechanical repo extraction, fan-out).
- **Records:** `session-logger` · `wrap-auditor` (now also invocable standalone mid-session, one scope).

**Self-activation map (the standing default):**
- **Session start** → `/orient`.
- **Claim→Design** → `anti-confound-designer` → **`/precheck`**; no compute before PASS.
- **Goal for the session** → `/goalsmith <item>` → paste into `/goal`.
- **First use of a dataset** → `dataset-verifier`; **scouting new data/papers** → `dataset-scout` / `lit-scout` (sonnet to gather), `paper-repo-extractor` (haiku) for repo artifacts, `paper-digest` (opus) for a note.
- **After a multi-seed/arm run, before recording a verdict** → `stat-aggregation-auditor` **then** the panel + Codex; reconcile the `PANEL-VERDICT` blocks to `PANEL-CLEAN:YES` before it lands.
- **The moment a verdict flips or a number lands** → `wrap-auditor` on the single relevant scope (mid-session), not only at close.
- **Session close** → `/wrap`.

**Auto-firing guardrails (hooks — no model decision needed):** `agent_routing_lint` (PreToolUse on agent spawns: nudges fable-banned + judgment-heavy→opus; `lit-scout`/`dataset-scout` exempt as task-dependent) and the SessionStart snapshot that arms `/wrap`. True OS-level auto-invocation exists only for these hooks; everything else above is the standing default the agent follows by itself.

Add more agents/skills only when a need recurs (adaptive semistructure). We deliberately did **not**
port the Nexus v2 stage-machine — see `docs/decisions/decisions.md` D001.

## Session close ritual

End **every** session — whatever stances ran — by running **`/wrap`** (the close command: it runs the
`session-logger` ritual *plus* a continuity audit — friction, broken tooling, doc consistency,
new-artifact check; mirror of the `/orient` start command). The `session-logger` agent or doing it by
hand are equivalent fallbacks. The ritual: immutable timeline log, refreshed `upspeed.md`, moved tasks,
any hard-won lesson appended to `docs/learnings.md`, and — **the keystone of the state-tracking process
(D015)** — an updated `docs/ladder.md`: flip the rung status, record the verdict, and rewrite the
"Next session" block.
**The ladder update must be confirmed with Erfan before it lands** (a rung flips to ✅ only on a
verdict he has agreed); never update the board on a unilateral read. The logger records which
**stances** ran and frames the close by the dominant one (a `/work` session logs *what ran / what's next
to run*; an `/interpret` / `/write` / `/teach` session logs *what's now understood / written /
figured*), and sets the ladder "Next session" tag to the next stance. See "Interaction stances" above
and `docs/03-methodology.md`.

## Maintenance

These instructions, the docs, and the agents are living. When a workflow keeps getting reconstructed,
or a mistake repeats, update the relevant file. Per Erfan's global rule, propose changes to his
private/global instructions before editing them — but this repo's own files are ours to keep current.

## Codex (second-model critic + rescue — subordinate to the docs brain)

We drive **Codex** (OpenAI CLI, `gpt-5.5`) from Claude via the `codex` plugin as an *independent second
model*. Full procedure + personas + command surface in **`docs/references/codex-usage.md`**. Two jobs only:

1. **A critic that ADDS to the thinking panel.** The panel (`counter-argument`, … sonnet) attacks
   the *conclusion*; Codex attacks the *code* — the layer the panel doesn't reach. Use
   `/codex:adversarial-review` for a single pass, or spin up a **Codex persona panel** — 1–4 background,
   read-only `task` runs via `codex:codex-rescue`, each with a distinct reviewer personality
   (statistical referee · reviewer-2 skeptic · first-principles re-deriver · reproducibility/leakage
   auditor) — and collect with `/codex:result`. Code-level analogs of our panel lenses.
2. **Rescue / second implementation** of a buggy or gnarly analysis script (`codex:codex-rescue`, the
   one place `--write` is appropriate). A fresh impl that agrees with ours is evidence; one that
   disagrees is a bug lead.

**Model/effort policy (asymmetric: medium worker, xhigh critic).** Global default
`model_reasoning_effort = "xhigh"` (`~/.codex/config.toml`) → **reviews run xhigh by inheritance** (the
review commands expose no per-call `--effort`). **Delegated `task` work passes `--effort medium`
explicitly** to override down — fast worker, slow critic; bump only for a genuinely hard build.

**The hard line.** Codex **never** produces a science number or flips a rung — numbers come only from
the `docs/` brain, verdicts only from Erfan. Codex reviews code correctness and proposes
implementations; it does not adjudicate a hypothesis. **Stop-review-gate stays OFF** (it fights the
docs-first `/wrap` ritual). **Sandbox note:** bwrap can't run in this container, so Codex's OS sandbox
is **disabled** (`danger-full-access`; the Docker container is the boundary, git catches stray edits) —
mechanics + the plugin-patch-reapply caveat in `docs/references/codex-usage.md`.

## graphify (code/corpus navigator — subordinate to the docs brain)

graphify builds a queryable knowledge graph of this repo at `graphify-out/` (god nodes,
communities, cross-file edges). It is a **navigation aid, not a source of truth.** The order of
authority is unchanged: `docs/ladder.md` and the `docs/` brain win (read them first, per "Read this
first"); gbrain is the knowledge layer; graphify just helps you find code and trace relationships
fast. **Never let graphify override the docs-first session ritual, and never report a number from the
graph — numbers come only from the `docs/` brain.**

Use it when it helps:
- Tracing code you didn't write (esp. the cloned external repos under `data/paper-repos/`):
  `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify explain "<concept>"` —
  faster than grepping an unfamiliar repo. Scope is set by `.graphifyignore` (overrides `.gitignore`).
- After changing our own code, `graphify update .` keeps it current (AST-only, free).

Mechanics: code is parsed locally by tree-sitter (free); docs/PDFs/images go to the host model
(token cost) — so the full graph is built in Antigravity/Gemini, then queried from here. No PreToolUse
hooks are installed (deliberately — they nag against the docs ritual).

## Firecrawl (web-data provider — subordinate to the docs brain)

Firecrawl turns live web pages into clean, LLM-ready markdown and runs a research index over papers
and code. It is wired in as a **project-scoped MCP server** (`.mcp.json` at repo root, remote transport
`https://mcp.firecrawl.dev/${FIRECRAWL_API_KEY}/v2/mcp`; key from `~/.config/secrets/env`, never
hardcoded). **Cloud API only** — the self-hosted stack needs Docker, which this container can't run.
First use in a session prompts for MCP approval; that's expected. Same authority order as graphify/Codex:
**`docs/ladder.md` and the `docs/` brain win; gbrain is the knowledge layer; Firecrawl just fetches
external web content.** It never produces a science number and never flips a rung.

The tool surface (`firecrawl_*`), grouped:
- **Fetch / crawl:** `scrape` (one URL → markdown), `map` (discover a site's URLs), `crawl` +
  `check_crawl_status` (whole-site → markdown), `batch` (many URLs), `extract` (schema'd structured
  extraction across pages via LLM), `parse` (a local/non-public doc → clean data).
- **Search:** `search` (web/news/images with full-page extraction — richer than `WebSearch`).
- **Research index (thesis-relevant — complements `lit-scout`):** `research_search_papers` (find arXiv
  papers by topic/method/benchmark), `research_inspect_paper`, `research_related_papers` (citation-graph
  expansion), `research_read_paper` (the in-body passages that answer one question), `research_search_github`
  (issue/PR history + READMEs for implementation notes).
- **Agentic:** `agent` + `agent_status` (FIRE-1 autonomous navigation), `interact` (drive a live browser
  session after a scrape), `monitor_*` (recurring scrape/crawl with content diffs).

**When to reach for it (and when not).** This repo already has a deep web stack — `WebFetch`/`WebSearch`,
exa MCP, the `perplexity-research` / `deep-research` skills, `lit-scout`/`dataset-scout`, and academic
APIs (S2, OpenAlex, CrossRef, Unpaywall, IEEE). **Don't default to Firecrawl for cheap one-off fetches —
credits are billed (`creditsUsed` per call).** Reach for it when those fail or fall short: a JS-heavy or
anti-bot page `WebFetch` chokes on, a **whole-site crawl/map** (docs sites, a dataset's pages, a paper's
repo), **schema'd extraction** across many pages, or the **research index** as a second lane alongside
`lit-scout`. Cheap path first, Firecrawl when it earns the credit.

**Installed here:** the `firecrawl-research-index` skill (repo-local, `.claude/skills/firecrawl-research-index/`)
— the paper-retrieval workflow (semantic search → citation-graph expansion via citers/references → in-body
verify with `read_paper`) that complements `lit-scout`; it drives the `firecrawl_research_*` MCP tools.
**One command away (not installed):** the Python SDK for scripted/batch scraping inside an experiment
(`uv add firecrawl-py`). Full capability index: `https://docs.firecrawl.dev/llms.txt`.
