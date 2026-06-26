---
title: "S27 — The stances operating model (working/analysis retired)"
tags: [timeline]
---

# S27 — The stances operating model (working/analysis retired)

**Date:** 2026-06-19 · **Stances:** `/meta` (dominant: methodology + tooling) · `/plan` (the design +
atomic walk) · `/review` (two adversarial panels). **NO experiment ran, NO science number produced, NO
Q-rung changed (Q0–Q5 stand exactly as S25/S26).** **Commits:** `6760f46` → `b0a5da3` (6 atomic).
**Cost:** ~$430 (authorized heavy design + build).

## Purpose

Erfan opened a "rethink how you teach me / how we run sessions" thread. It became a full redesign of the
repo's operating model: replace the D011 working/analysis session binary with invokable interaction
stances, and build a LearnLM/Gemini-style `/teach` stance plus the report→teach pipeline.

## What happened

1. **Design (atomic walk with Erfan, 14 decisions).** Converged on: eight stances (`/work`,
   `/interpret`, `/write`, `/teach`, `/scout`, `/meta`, `/plan`, `/review`) replacing working/analysis;
   one fat skill whose `SKILL.md` spine routes to deep per-mode files; explicit + auto-trigger invocation
   (agent states the stance; `/work` explicit-only); the honesty guard armed at write-time, not
   in-stance; `/teach` = LearnLM five principles + the Gemini guided-learning loop + four sub-modes
   (guided/walkthrough/feynman/drill) + a learning-record ledger (Matt Pocock's filesystem-as-memory,
   evidence-gated, anchored to report+number); `/interpret` = claim-manifest + panel + stat-auditor +
   SCR; reports keep verdict-first storage with a plain-language lead and `/teach` renders simple-first;
   SCR (predict-before-reveal) in teach+interpret; a light claim-manifest in interpret. Build sequence:
   core-first, then expand.
2. **Gather.** Read the `academic-research-skills` repo (modes-in-fat-skills, Material Passport,
   anti-leakage, SCR), the LearnLM / Gemini Guided-Learning / Bloom-two-sigma pedagogy, Matt Pocock's
   skills repo (the teach skill's filesystem-as-memory ledger + clean skill-authoring format), and
   Erfan's two Gemini transcripts (extracted the guided-learning loop).
3. **Two adversarial panels** (four opus lenses + Codex) on the design. They converged hard: arm honesty
   at write-time not in-stance; keep verdict-first reports and render at teach-time; adopt Matt's ledger;
   keep stances decoupled, not a Nexus pipeline. Erfan overruled the "a skill is just a prompt"
   objection (a skill is a durable, optimizable artifact). Plan written, approved, exited plan mode.
4. **Built (Pass 1 + Pass 2, 6 commits).** The `stances` skill (`SKILL.md` spine + 8 mode files +
   `formats/learning-record.md`), 8 command doors, the write-time honesty hook
   (`.claude/hooks/honesty_writecheck.py`, tested), the report plain-language-lead amendment to
   `scientific-writing`, `docs/operating-map.md`, the canonical docs rewritten to stances (`CLAUDE.md`,
   `03-methodology.md`, **D044**, `orient`/`wrap`/`session-logger`), and the LearnLM + Bloom canonical
   notes. The learning ledger seeded at `docs/learning/`.

## Decisions

- **D044** — operating model = invokable interaction stances; working/analysis (D011) retired; honesty
  armed at write-time. (Recorded in `decisions/decisions.md`.)

## Current truth

The science is **UNCHANGED**: Q0 ✅, Q1 ✅partial, Q2 ❌, Q3 ❌, Q4 ❌bounded, Q5 ⬜ — exactly as S25
left them. This session changed only the apparatus (how we work), not the evidence. The live science
thread is still **Q4 sample-efficiency/LUPI** (re-substrate to higher-N gaze), unchanged from S25.

## Next session

- **Test `/teach` live** on a real report (Erfan, planned) — the only real proof of the guided loop.
- The honesty hook is live (fired this session); scoped to reports + manuscript after the ladder false-positived (L052).
- Science next-step unchanged: **Q4** (E024 re-substrate → synthetic-PI MDE control → build), per
  `expansion-program.md` §8.

## Friction & improvements

- Initially presented decisions as bundled mega-paths; Erfan corrected → present **atomic decision-forks
  one at a time**, argue each (L052).
- Was over-indexed on the Nexus over-specification fear; the real lesson is about **coupling**, not a
  vocabulary of independent invokable tools (L052).
- **Tooling gotcha:** `.claude/state/wrap/start.json` held a mid-session re-fire SHA (`07e344e`, one of
  this session's own commits) rather than the true session start — the SessionStart hook re-fired after
  the long session. `/wrap` should sanity-check `start_sha` against the session's commits; used the
  `dfe5223` fallback here.
- **Hook-scope fire (caught by the trial):** the first `/wrap` edit to `docs/ladder.md` flagged 41
  pre-existing bare numbers — the ladder references results by bare code, not `[E0nn]`. Narrowed the
  hook from 5 paths to `docs/reports/` + `docs/manuscript/` (the prose deliverables); ladder/learnings/
  experiments need a different check (L052).
- **Pre-existing finding the new hook surfaces:** `R06:96` has a bare `+0.0280` with no cite — needs an
  `[E0nn]` or a `\gap` (analysis-lane, Erfan's call). Not fixed here.
- **Follow-up:** sweep the remaining "working/analysis" mentions in `CLAUDE.md`'s fleet section,
  `goalsmith` ("working sessions only"), and agent descriptions; D044 documents the mapping so they stay
  interpretable, but a cleanup pass removes the drift.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
