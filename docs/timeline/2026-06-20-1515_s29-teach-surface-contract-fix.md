# S29 — /teach surface-contract fix (the v2 build had inverted Erfan's instruction)

**Date:** 2026-06-20 · **Stance:** `/meta` (dominant; investigation + apparatus fix). **NO experiment ran,
NO science number produced, NO Q-rung changed (Q0–Q5 stand exactly as S25/S27/S28).** **Commits:** `d9ec687`
(D045 fix) · `<gitignore>` (disposable HTML renders).

## Purpose

Erfan started a live test of the finalized `/teach` on report R07 and hit a wall: the agent dumped the whole
DPI derivation as raw `$$…$$` into the terminal, which cannot render LaTeX — the exact failure the mode was
built to prevent. He asked for a complete review of how `/teach` got built and where it went wrong.

## What happened

1. **Reviewed the build history.** `/teach` was touched in three blocks on 2026-06-19: S27 (born, in the
   stances operating model), the **teach v2** evening block (rewrote it: "teach anything", rendered
   whiteboard, two-layer memory — *no timeline log of its own*), and S28 (grounded the pedagogy `\gap`s).
2. **Found the bug by reading the actual transcripts.** Erfan's explicit instruction (teach v2 session
   `210f5c0e`, msg 227): *each round, write the explanation into the markdown file (LaTeX renders there),
   then ask the question in the terminal.* The agent **agreed** at the time (msg 237) — then encoded it
   wrong: `modes/teach.md` line 47 became *"the live Q&A is in the terminal; update the lesson at the end of
   a round"*, which inverts the timing and recasts the terminal as the teaching surface. The R07 test agent
   (session `c4b6fb0d`) followed the written text faithfully → math in the terminal. **Design bug, not an
   execution bug.**
3. **Surfaced the tension the v2 counter-critique had raised** (msg 1198): a two-surface file+terminal split
   risks split-attention cost; the panel leaned toward single-surface inline rendering. The final build
   never resolved it and defaulted to the worst option.
4. **Fixed it (D045).** Rewrote the surface contract in `modes/teach.md` + `formats/lesson-format.md` to the
   **part-boundary loop**: write the part's explanation+math+diagrams into the rendered lesson file *first* →
   ask in the terminal (math allowed when it echoes the rendered file) → run the whole back-and-forth in the
   terminal, plain language → at the part boundary, record the answer/diagnosis + author the next part, in one
   pass. Math never appears unrendered in the terminal. Template unit is now "part", not "round". Grounded in
   Erfan's own prior `data/course-lecture-study` skill (teach a chunk into the rendered note → interact →
   stabilize → advance) and the pedagogy (LearnLM "manage cognitive load"; split-attention avoided because
   the surfaces are sequential, not simultaneous).
5. **Cleaned up + diagnosed a second observation.** Removed the old R07 test stub. When Erfan flagged the new
   test's three entry-point paths as poorly selected, traced it to source: D045 touched only line 44; the
   entry-point instruction (lines 72–74) is byte-identical across both runs → the path variation is **model
   generation variance, not the change.** Noted the real lever (the "Open" step instruction is thin — only
   "different depths"), left for a future change.

## Decisions

- **D045** — `/teach` surface contract: explanation→file, dialogue→terminal, written at part boundaries.
  (Recorded in `decisions/decisions.md`.)

## Current truth

Science **UNCHANGED**: Q0 ✅ · Q1 ✅partial · Q2 ❌ · Q3 ❌ · Q4 ❌bounded · Q5 ⬜ — exactly as S25/S27/S28.
Apparatus-only session. The live science next-step is still **Q4 sample-efficiency / E024 re-substrate**.

## Next session

- Science next-step unchanged: **Q4** (E024 re-substrate → synthetic-PI MDE control → build), per
  `expansion-program.md` §8. Stance `/work` (after `/precheck`), or `/teach` to test the fixed tutor live.
- **Optional `/meta` follow-up:** strengthen the `/teach` "Open" step so entry-point selection is specified
  (partition the report's content / MECE), not left to model luck — the cause of the weak path set Erfan saw.

## Friction & improvements

- **The v2 build silently dropped an explicit instruction when encoding it into prose** (L053). The agent
  understood the instruction live, then compressed it out when writing the skill file. Lesson: verify skill
  text against the literal user instruction, not against the gist.
- **teach v2 had no timeline log** — the biggest rewrite of the mode happened in an unlogged evening block,
  which is why the regression went unnoticed until the live test.
- Gitignored `docs/learning/lessons/*.html` (disposable renders) so they stop showing as untracked.
