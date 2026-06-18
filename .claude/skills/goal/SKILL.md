---
name: goal
description: >-
  Build the working-session GOAL TEXT for this brain-alignment thesis repo. Run AFTER /orient, at the
  start of a WORKING session; pass the item from the orient output you want to work on (e.g. "E023a",
  "denizenslab n=6 full-FT", "measure O6 brain-as-regularizer", "P1 ZuCo learning curve", "test the
  Y⊥θ*|S ceiling"). It reads the source-of-truth docs, locates that item in the ladder / expansion-program
  / idea-tree, and expands it into a full, repo-aware, kill-gated goal that bakes in the standing
  working-session discipline (100%-not-99%, predeclared kill criteria, the 5-control battery, parallel
  GPUs, subagent model-routing, panel-after-each-step, record-back). The OUTPUT is the goal text — it does
  not start running the work. Working sessions only (Design→Run→Judge); NOT for analysis sessions (those
  write reports/manuscript — Erfan's lane).
---

# /goal — build the working-session goal text

**Purpose.** Replace hand-writing a long goal prompt each working session. Input is one item from the
`/orient` output; output is a structured, ready-to-launch goal for that item, grounded in the docs brain
and the repo's standing research discipline. **The goal text is the deliverable — do NOT begin the work;
Erfan reviews and launches.**

**Usage.** `/goal <item>` where `<item>` (`$ARGUMENTS`) is an orient item / node / experiment id. If no
item is given, read `docs/ladder.md` ("Next session") + `docs/expansion-program.md` §8 (Tier 1) and
propose the highest-leverage open one, then ask which to build for.

**Guard.** This is for WORKING sessions (generate evidence). If the item is analysis-lane work (a report
`R08`–`R14`, the manuscript, figures), stop and say so — that is Erfan's analysis lane (D011), not a goal
this command builds.

## Step 1 — locate the item (read the source of truth; never re-derive)
Resolve `$ARGUMENTS` against, in order:
- `docs/ladder.md` — rung status + the "Next session" block.
- `docs/expansion-program.md` §8 — the S24 tiered trajectory (Tier 1/2/3) + the **5-control battery**.
- `docs/idea-tree.md` — the node: its id (T*/E*/O*), layer, parent, status, prior, and the **assumption it rests on**.
- the item's own `docs/experiments/E*.md` if it has one; `docs/03-methodology.md` (the epistemic spine); `docs/06-theory-grounding.md` if it is a theory/proof node.
- `mcp__gbrain__query` — what prior sessions already did on this item (brain-first, before re-deriving).

Pin down: which **Tier**, which **node**, the **estimand**, the **prior/expected verdict**, and the **assumption it rests on**.

## Step 2 — emit the goal text (the output), instantiated for the item
Assemble these sections, filled in for this specific item:

1. **The item & where it sits** — node id, tier, one-line claim, the parent rung that must hold, current status + prior.
2. **Estimand & predeclared kill criterion** — name the estimand, the estimator, the identifying assumption (estimand-first lens); lock the kill criterion BEFORE running (D003). *Theory/proof node:* the proposition to prove or bound, and what counts as "closed."
3. **Design (locked before running)** — strongest baseline at matched budget/perplexity (never a strawman); the controls from the **5-control battery** that apply — (i) phase-randomized shape-twin, (ii) zeroed/shuffled-PI, (iii) did-the-representation-move gate (L042), (iv) matched-perplexity + per-subject + crossed fold/subject clustering, (v) matched-information non-brain privileged teacher; seeds (≥3 for stochastic); contiguous splits + nuisance baselines (anti-confound, L003); stop rule. **Oracle-gate the design before any compute.**
4. **Run** — up to 4 experiments in parallel on the 4× L40S; always `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; long runs as background processes. Subagent model-routing: **opus** = think/design/judge; **sonnet** = doc-nav/engineering; **haiku** = mechanical/extraction; **fable banned**. Use the repo's defined agents; propose new/updated agents when a need recurs.
5. **Judge** — run the thinking panel (`counter-argument` + `socratic-thinker` + `premortem-analyst` + `first-principles-grounder`) + Codex code-critic on the result; verify each objection against the data; address survivors; re-run the panel until no hole survives.
6. **Record + compound** — write/update the `experiments/E*.md`, `learnings.md`, `decisions/`; ask whether the result spawns or prunes `idea-tree.md` nodes; flag the ladder change for Erfan. **Numbers come only from runs; rungs flip ONLY on Erfan's confirmation.**

## Standing discipline (baked in from the expansion-program kickoff — applies to every goal)
- **100%, not 99%.** Be thorough; act like a senior researcher; go all the way until the question is closed.
- **Question the assumptions under "done" nodes** — re-think them, try different methods/objectives/regimes for the same concept; a closed verdict is a place to attack, not a wall.
- Multiple competing hypotheses, not one cherished one; kill criteria predeclared; root cause not symptom.
- Specific numbers with uncertainty and the named test ("Δ = +0.06 ± 0.01, n=3, contiguous split"), never "it worked better"; raw evidence kept separate from interpretation.
- **gbrain-first**: review what prior sessions did before starting; cite the page slug used.
- Spin up subagents liberally; **record back to the docs after each node** so the next session resumes from the docs alone.
- The docs brain (`ladder.md` first) is the source of truth; `expansion-program.md` §8 holds the current trajectory; the analysis lane (reports/manuscript) is off-limits to working sessions (D011).

## Output
Print the assembled goal text, ready to act on. Close by noting the kill criterion and the oracle-gate
step. **Do not start the work** — hand the goal to Erfan to review and launch.
