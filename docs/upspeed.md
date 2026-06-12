# Upspeed — read first, write last

**Last updated:** 2026-06-12 (Session 11 — PLANNING/handoff: two parallel lanes + dual meta-goal set;
implementation reopened as an ordered roadmap; TRIBE-v2 read + scoped as the capstone. Autonomous run pending
the goal command.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (the rung board + roadmap, D015). This file is the
> last-session prose; if it disagrees with the ladder, the ladder wins. With no task, run `/orient`.

## Current state

**The dual meta-goal (D022):** finish the MSc thesis **AND** extract **≥1 top-venue AI paper** (ICML/ICLR/
NeurIPS/AAAI-class). Work runs in **two parallel lanes (D020)** sharing the `docs/` evidence brain:
- **🔬 IMPLEMENTATION lane (autonomous) — an ORDERED ROADMAP; start at the top, TRIBE is the capstone (LAST):**
  **I1** expand E015 (cross-family alignment∝−ppl law) → **I2** matched-ppl control on an *external* published
  result (the "main-track lift", premortem #1) → **I3** full-FT multi-subject voxelwise (E013 door, denizenslab
  n=6) → **I4 CAPSTONE** E016 TRIBE synthetic brain targets. Full detail in `tasks.md`; per-item docs in
  `experiments/`. After every step: thinking panel (D017) + Codex critic (D019) until no hole survives → record.
- **📖 ANALYSIS lane (Erfan) — FROZEN** at resume point: R05 §9 (Layer 3 = E005 → §14), then figures + manuscript.

**Science verdicts UNCHANGED — no rung moved.** L0/A2 ✅ PASS; L3/F1 ❌ per-individual null (robust); L2b/A3 ❌
bounded null. The roadmap pursues the remaining *untested doors* + the TRIBE capstone; it does not contradict
the closed-rung verdicts.

## What to do next (autonomous loop)

**Start at I1** (the first incomplete roadmap item) — do NOT jump to TRIBE. Work each item Design→Run→Judge,
ground every claim in the papers (`docs/literature/`, `data/papers`, `data/paper-repos`) and course material
(`06-theory-grounding.md`, `data/course-material`), run the counter-critique loop after each verdict, commit
atomically, and update the experiment doc + `learnings.md` + `decisions.md` + `ladder.md`/`tasks.md` as you go.
Close each working session with `/wrap`. The idea is not holy text — refocus it toward the real literature gap
as evidence accumulates. **Stop only** when you truly need an Erfan decision (a Fork-A surprise; the I2 headline/
spine call) or hit a real wall. Numbers come from runs; **no rung flips without Erfan.**

## Blockers / open loops

- **I3 data acquisition:** denizenslab BOLD HDFs are on GIN **git-annex**; `git-annex`/`datalad` not installed
  → use GIN HTTP `/raw/` or `apt-get install git-annex`. (I4/TRIBE *sidesteps* this — it generates its own fMRI.)
- **I4/TRIBE P0 gate PASS:** isolated venv `data/paper-repos/tribev2/.venv-tribe`, `import` OK; weights non-gated;
  Llama-3.2-3B access resolves (confirm on first real download). Background install log: `outputs/E016_tribe/`.
- **Carry-forward:** reapply the `codex.mjs` sandbox patch after any codex plugin update.
- **Untouched:** S8/S9 doc-audit follow-ups in `tasks.md` (stale Status headers; E005 body retracted-lead).

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs 4× L40S free.
- **TRIBE env is ISOLATED** (`.venv-tribe`): it pins torch<2.7 + numpy==2.2.6; the thesis env is torch
  2.11.0+cu128 / numpy 2.4.6 — never install TRIBE into the thesis venv (it would downgrade torch and break the
  experiment scripts). Hand off via disk: TRIBE writes synthetic-BOLD `.npy`; our pipeline reads them.
- **Subagent routing (D017/D019/Erfan's rule):** fable = hard adversarial/counter-arguing + oracle-reviewer;
  sonnet = lit-scout/paper-digest/socratic/session-logger; haiku = mechanical fan-out. Codex = code-level critic
  (`/codex:adversarial-review` or a persona panel) + rescue/second-implementation. Spin up subagents liberally.
- **Codex:** full guide `docs/references/codex-usage.md`; sandbox DISABLED (container); reasoning xhigh.
- **Corrected number to carry:** Tuckute functional NC ceiling 0.491/0.559 (not 0.353); E002 "~10%"→ honest ~7%.
- **Tooling gotcha:** offline `load_dataset("wikitext",...)` FAILS → use `"Salesforce/wikitext"`. `outputs/` gitignored.
- **Git:** `main`, push only when asked.
