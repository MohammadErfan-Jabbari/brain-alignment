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

1. `docs/upspeed.md` — where we are, what's next, blockers. **Always read before doing anything.**
2. `docs/tasks.md` — the path behind and ahead.
3. Then the relevant deep doc: `docs/00-charter.md` (idea/scope), `docs/01-research-landscape.md`
   (literature + the gap), `docs/02-environment.md` (compute/data/how-to-run),
   `docs/03-methodology.md` (how we work and why).

`docs/` is the persistent research brain — see `docs/README.md` for the full map. If something
matters past this session, it goes in `docs/`, not just in chat.

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
| `lit-scout` | Search across sources for papers on a topic; return a ranked, deduped shortlist. |
| `paper-digest` | Read a paper (PDF/arXiv/URL) → a canonical note in `docs/literature/canonical/`. |
| `oracle-reviewer` | Adversarially stress-test a hypothesis or design before committing compute. Reproduces the prior HOLD-review value. |
| `session-logger` | At session end: write `docs/timeline/…`, REPLACE `docs/upspeed.md`, update `tasks.md`/`learnings.md`. |

Add more agents/skills only when a need recurs (adaptive semistructure). We deliberately did **not**
port the Nexus v2 stage-machine — see `docs/decisions/decisions.md` D001.

## Session close ritual

End **every** session — working or analysis — by running `session-logger` (or doing it by hand):
immutable timeline log, refreshed `upspeed.md`, moved tasks, and any hard-won lesson appended to
`docs/learnings.md`. The logger asks which mode the session was and frames the close accordingly (a
working session logs *what ran / what's next to run*; an analysis session logs *what's understood /
written / figured*). See "Two kinds of session" above and `docs/03-methodology.md`.

## Maintenance

These instructions, the docs, and the agents are living. When a workflow keeps getting reconstructed,
or a mistake repeats, update the relevant file. Per Erfan's global rule, propose changes to his
private/global instructions before editing them — but this repo's own files are ours to keep current.
