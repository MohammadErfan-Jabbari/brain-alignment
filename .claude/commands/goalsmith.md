---
description: Build the working-session GOAL TEXT for one item from /orient. Read-only — it prints a goal you copy-paste into the /goal command to launch. Working sessions only (not analysis).
allowed-tools: Read, Glob, Grep, Bash(git log:*), mcp__gbrain__query
---

You are in the `brain-alignment` thesis repo. Erfan has run `/orient` and is handing you ONE item to work on this **working** session — passed as the argument (e.g. "E023a", "denizenslab n=6 full-FT", "measure O6 brain-as-regularizer", "P1 ZuCo learning curve", "test the Y⊥θ\*|S ceiling"). Your single job: **build the GOAL TEXT for that item and print it.** Do **not** start the work, run anything, or edit any file — the goal text is the deliverable; Erfan copies it into the `/goal` command to launch the session.

**Guard.** If the item is analysis-lane work (a finding-report R08–R14, the manuscript, figures), stop and say so — that is Erfan's analysis lane (D011), not a working-session goal this command builds.

Do this:

1. **Locate the item — read the source of truth, never re-derive.** In order: `docs/ladder.md` (rung status + the "Next session" block), `docs/expansion-program.md` §8 (the S24 tiered trajectory + the **5-control battery**), `docs/idea-tree.md` (the node — id `T*/E*/O*`, layer, parent, status, prior, and the **assumption it rests on**), the item's own `docs/experiments/E*.md` if it has one, `docs/03-methodology.md` (the epistemic spine), and `docs/06-theory-grounding.md` if it is a theory/proof node. Optionally `mcp__gbrain__query` for what prior sessions already did on this item. If the item isn't given, read the "Next session" block + expansion-program §8 Tier 1 and propose the highest-leverage open one, then ask which.

2. **Build and print the goal text**, instantiated for this item, with these sections:
   - **The item & where it sits** — node id, tier, one-line claim, the parent rung that must hold, current status + prior.
   - **Estimand & predeclared kill criterion** — name the estimand, the estimator, the identifying assumption (estimand-first lens); lock the kill criterion BEFORE running (D003). *Theory/proof node:* the proposition to prove or bound, and what counts as "closed."
   - **Design (lock before running)** — strongest baseline at matched budget/perplexity (never a strawman); the applicable controls from the **5-control battery** — phase-randomized shape-twin · zeroed/shuffled-PI · did-the-representation-move gate (L042) · matched-perplexity + per-subject crossed fold/subject clustering · matched-information non-brain privileged teacher; ≥3 seeds for stochastic; contiguous splits + nuisance baselines (anti-confound, L003); stop rule; **oracle-gate the design before any compute.**
   - **Run** — up to 4 experiments in parallel on the 4× L40S; always `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; long runs as background processes. Subagent model-routing: opus = think/design/judge · sonnet = doc-nav/engineering · haiku = mechanical/extraction · **fable banned**. Use the repo's defined agents; propose new/updated agents when a need recurs.
   - **Judge** — run the thinking panel (`counter-argument` + `socratic-thinker` + `premortem-analyst` + `first-principles-grounder`) + the Codex code-critic on the result; verify each objection against the data; address survivors; re-run the panel until no hole survives.
   - **Record + compound** — update `experiments/E*.md` + `learnings.md` + `decisions/` + `idea-tree.md` (spawn/prune nodes); flag the ladder change. **Numbers come only from runs; rungs flip ONLY on Erfan's confirmation.**

3. **Bake in the standing discipline** (every goal carries it, distilled from the expansion-program kickoff): 100%-not-99% — act like a senior researcher and go all the way until the question is closed; **question the assumptions under "done" nodes** (try different methods / objectives / regimes for the same concept — a closed verdict is a place to attack, not a wall); multiple competing hypotheses with predeclared kill criteria; root cause not symptom; specific numbers with uncertainty and the named test ("Δ = +0.06 ± 0.01, n=3, contiguous split"), raw evidence kept separate from interpretation; **gbrain-first** review of prior work before starting; record back to the docs after each node so the next session resumes from the docs alone.

Print the assembled goal text ready to paste into `/goal`. Close with the kill criterion and the oracle-gate reminder. **Do not begin the work.**
