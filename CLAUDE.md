# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

# brain-alignment — MSc thesis research repo

This repo is the execution home for Erfan's master's thesis (ML for Health, UC3M) on **using the
linear mapping between LLM middle layers and brain activation as a usable signal** — with
**brain-alignment-guided distillation** as the first concrete use case. It is a single-paper research
workspace, not a software product.

## Two kinds of session — know which you're in

Work in this repo runs in one of two modes. **Decide which at the start of every session** (the user
usually signals it; if not, infer from the ask and say which you assumed). They have different jobs,
different outputs, and a different close ritual. (Decision D011; mechanics in `docs/03-methodology.md`.)

| | **Working session** | **Analysis session** |
|---|---|---|
| Trigger | "do X / run X / implement X / get the verdict on X" | "explain X / why did we X / make a figure of X / write the X section / digest the results" |
| Epistemic phases | **Design → Run → Judge** (produce evidence) | **Argue → Compound** (consume + communicate evidence) |
| Primary output | code, runs, results in `docs/experiments/`, decisions, learnings | understanding (chat), figures, manuscript/report prose in `docs/manuscript/` |
| Touches the science? | **Yes** — generates new evidence | **No** — reads existing evidence; never invents a number |
| Close ritual | timeline log + REPLACE `upspeed.md` framed on *what ran / what's next to run* | timeline log + REPLACE `upspeed.md` framed on *what's now understood / written / figured* |

The non-negotiable that binds both: **an analysis session may only report numbers that a working
session actually produced and recorded.** If a figure or a paragraph needs a number that isn't in the
`docs/` brain, that is a gap to flag — not a number to invent or estimate. Raw evidence stays separate
from interpretation in both modes.

## Read this first, every session

0. `docs/ladder.md` — **the canonical status board: which rungs are done, with what verdict, and the
   single next step (impl or analysis). This is the source of truth for project state — when any doc
   disagrees with it, it wins and the others get fixed.** With no specific task, run `/orient` (it reads
   the board and briefs you).
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

Use the **Elon/Feynman/Naval** frame (`docs/references/reasoning-frame.md`) when designing or
deciding: real goal + delete false constraints; plain mechanism + where it breaks; smallest durable
change that compounds.

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
| `lit-scout` | Search across sources for papers on a topic; return a ranked, deduped shortlist. (sonnet) |
| `paper-digest` | Read a paper (PDF/arXiv/URL) → a canonical note in `docs/literature/canonical/`. (sonnet) |
| `oracle-reviewer` | Adversarially stress-test a hypothesis or design **before** committing compute (PASS/HOLD/KILL). Reproduces the prior HOLD-review value. (fable) |
| `session-logger` | At session end: write `docs/timeline/…`, REPLACE `docs/upspeed.md`, update `tasks.md`/`learnings.md`. (sonnet) |

**The thinking panel** (D017) — four reasoning-methodology agents run *after a step produces a result/
verdict*, to find holes before the verdict lands in the ladder/docs/manuscript. Distinct from
`oracle-reviewer` (a *pre-compute* design gate); these are *post-step* analysts. The loop: run the
panel → verify each objection against the data → address the ones that hold → re-run the panel until no
hole survives.

| Agent | Lens | Use when |
|---|---|---|
| `counter-argument` | Red-team the conclusion — build the strongest case it's an artifact/over-claim. (fable) | A run produced a verdict; before believing it. |
| `socratic-thinker` | Expose hidden assumptions and undefined terms by asking, not asserting. (sonnet) | A direction feels settled too quickly; before locking a framing. |
| `premortem-analyst` | Assume it already failed (didn't replicate / rejected / defense collapsed); trace backward. (fable) | Before building heavily on a result or spending the next compute. |
| `first-principles-grounder` | Re-derive from mechanism + the math/papers (`06-theory-grounding.md`, canonical notes, course material). (fable) | A claim needs a mechanism, leans on a theorem, or might contradict a source. |

Model routing (Erfan's rule): **fable** for the hard adversarial/counter-arguing work and `oracle-reviewer`;
**sonnet** for search/digest/Socratic/logging; **haiku** for mechanical fan-out (extraction, file-mapping).
Each agent declares its default in `model:` frontmatter; override per call when the task warrants.

Add more agents/skills only when a need recurs (adaptive semistructure). We deliberately did **not**
port the Nexus v2 stage-machine — see `docs/decisions/decisions.md` D001.

## Session close ritual

End **every** session — working or analysis — by running **`/wrap`** (the close command: it runs the
`session-logger` ritual *plus* a continuity audit — friction, broken tooling, doc consistency,
new-artifact check; mirror of the `/orient` start command). The `session-logger` agent or doing it by
hand are equivalent fallbacks. The ritual: immutable timeline log, refreshed `upspeed.md`, moved tasks,
any hard-won lesson appended to `docs/learnings.md`, and — **the keystone of the state-tracking process
(D015)** — an updated `docs/ladder.md`: flip the rung status, record the verdict, and rewrite the
"Next session" block.
**The ladder update must be confirmed with Erfan before it lands** (a rung flips to ✅ only on a
verdict he has agreed); never update the board on a unilateral read. The logger asks which mode the
session was and frames the close accordingly (a working session logs *what ran / what's next to run*;
an analysis session logs *what's understood / written / figured*). See "Two kinds of session" above
and `docs/03-methodology.md`.

## Maintenance

These instructions, the docs, and the agents are living. When a workflow keeps getting reconstructed,
or a mistake repeats, update the relevant file. Per Erfan's global rule, propose changes to his
private/global instructions before editing them — but this repo's own files are ours to keep current.

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
