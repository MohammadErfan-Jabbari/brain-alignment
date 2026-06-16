# Upspeed — read first, write last

**Last updated:** 2026-06-16 (Session 16 — analysis. **Restructured the write-up layer: renamed the ladder rungs
L→Q, added `map.md`, adopted the finding-report convention (D036), retired R05, and wrote the first finding-report
R06 (Q0/A2).** No science rung changed; the ladder is unchanged from S14. The analysis lane is now ACTIVE — the next
step is the next finding-report, R07.)

> **Canonical state lives in [`ladder.md`](ladder.md).** This is last-session prose. With no task, run `/orient`.

## What got built this session (not science — the write-up layer)

1. **Rungs renamed L→Q in execution order + `map.md` (D036).** The old `L` rung labels collided with learning IDs
   and ran out of climb order; rungs are now `Q0→Q5` in climb order (`L0→Q0`, `L2a→Q1`, `L1→Q2`, `L3→Q3`, `L2b→Q4`,
   `L4→Q5`). Stable artifacts (`E`/`D`/`L`/`A`) keep flat, immutable, chronological IDs (issue-number rule); the
   ladder is a separate hierarchical view. `docs/map.md` is the new one-screen orientation aid (legend + the whole
   journey as a tree); it is **not** the status board — `ladder.md` still wins. Timeline logs stay immutable (old `L`;
   `map.md` carries the L↔Q table).
2. **The finding-report convention (D036).** A report is now **one durable claim per file**, flat append-only `R<NN>`
   IDs (never renumbered), **current-truth-only** (no chronological spoilers — the history lives in `map.md`,
   `timeline/`, `decisions/`), Q-tagged, each mapping **1:1 to a manuscript Results section**. The reading order and
   the Q→report map live in `reports/README.md`, not in the filename. **R05 is retired** (frozen for history,
   superseded by the finding-reports + `map.md`).
3. **R06 written — the first finding-report (Q0/A2).** "The LM↔brain alignment signal is real, beyond confounds."
   Formalized as conditional-MI with a math-grounded report convention (formalize the core quantity + foundational
   concepts in real LaTeX, cite the course note rather than re-derive). Two voice rules added to the
   `scientific-writing` skill: a math-voice rule and a "presenting a measured quantity" rule.
4. **The estimand-first lens** added to the reasoning toolkit (`docs/references/reasoning-frame.md`), plus a rule to
   grow the toolkit as new lenses prove themselves on real work.

## What's next — the analysis lane is ACTIVE (write the finding-report set)

> **📍 The plan with deep reading order, concepts, and self-checks per report: [`docs/analysis-roadmap.md`](analysis-roadmap.md).**
> The reports are written in **reading order** (`reports/README.md` index), each through the `scientific-writing` skill
> (it lints the prose and checks every number against the recorded evidence, D011).
- **R06** (Q0/A2 — signal real) ✅ written.
- **R07** (Q1 — plain KD does not preserve alignment, from E003) ⬜ **NEXT**.
- Then **R08** (Q2 — lever real but weak), **R09** (Q3 — no per-individual gain; the averaging confound; the parked
  `_pending-Q3_*.md` draft reclaims this number), **R10** (Q3 — null is method-general), **R11** (Q3 — the quality
  law), **R12** (Q3 — the ceiling, scoped; keystone), **R13** (Q3 — external reproduction), **R14** (Q4/A3 — no
  practical payoff).
- At a checkpoint Erfan explicitly calls, the finding-reports consolidate into the **extended manuscript** (never
  auto-updated, D035); the first extended checkpoint seeds from v0.9 (`manuscript/00_paper-draft-v0.md`).
- Forward-program rungs remain parked (F3 superseded, F4 analysis-lane); no new compute is needed for the paper.

## Blockers / open loops

- **Boards reconciled + brain mirror done (this close, 2026-06-16):** ladder/upspeed/tasks/analysis-roadmap now agree
  (R05 retired, next = R07); the D036 gbrain page (`brain-alignment-naming-convention`) was updated with the
  finding-report convention + R06 (the D035 page was already current). A reconstructed S16 timeline log + this
  session's log are in `docs/timeline/`.
- **⚠️ Concurrent in-flight work, uncommitted (NOT this session's):** `reports/R06`, `experiments/E002`,
  `experiments/E006` are modified and `docs/explainer_pipeline.html` is new in the working tree — active R06 work
  (math rendering, the trained−untrained-gap reasoning, pipeline diagrams) by Erfan or another agent. Left untouched;
  its author should commit it.
- The parked Q3 draft's title line reads "# R06 —"; it becomes R09 when promoted at read-position 4 (fix the title then).
- `projects/brain-alignment` gbrain hub is still a bare stub (enrich when convenient).
- No background jobs running.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. 4× L40S.
- **Codes (D036):** `Q`n = ladder rung (Q0→Q5, climb order); `E`/`D`/`L`/`A` = flat immutable artifact IDs. Legend +
  journey tree in `docs/map.md`; canonical status in `docs/ladder.md`.
- **Writing:** route all report/manuscript prose through the `scientific-writing` skill (D035/D036). Reports =
  `docs/reports/R<NN>_*.md` (md, continuous, one claim per file); manuscripts = `docs/manuscript/{extended,public}/`
  (LaTeX, checkpoint-derived only on Erfan's call). Codes are internal: reports use them freely, the public manuscript
  carries zero codes.
- **Subagent routing (D026):** opus = think/analysis/design; sonnet = doc-nav; haiku = mechanical. fable BANNED.
- **Git:** `main`, push only when asked. Untracked-and-harmless: `untitled.md` (scratch copy of an old `/goal` prompt).
