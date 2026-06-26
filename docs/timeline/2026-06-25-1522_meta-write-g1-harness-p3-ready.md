---
title: "2026-06-25 15:22 — /meta: G1 RUB-grading harness built; G2/G3 cleared; dual opus review →…"
tags: [timeline]
---

# 2026-06-25 15:22 — /meta: G1 RUB-grading harness built; G2/G3 cleared; dual opus review → READY-FOR-P3

**Stance:** `/meta` throughout (build/maintain the apparatus). No other stance entered. **NO experiment, NO
science number, NO rung change — Q0–Q5 stand exactly as S40/S41.** This session cleared the **pre-P3 readiness
checklist** for the `/write` rebuild (D048): built the one hard blocker (G1, the RUB-grading harness), decided the
framing-escape (G2/D051), demonstrated the convergence loop (G3), and confirmed readiness with two opus reviewers.

## What was done (the request: build G1, then G2/G3, stop when ready for P3 + opus confirms)

First, mined the last 5 build/design session logs (the redesign + the 4 build sessions) with parallel sonnet
subagents to extract the working pattern faithfully — plan-then-chunk, the **three-net loop** (embedded
`--selftest` → opus `oracle-reviewer` on every chunk → fresh `claude -p` clean-room → atomic commit + build-log
entry), continuous adversarial review. Then replicated it.

**Phase A — the G1 plan, hardened to BUILD-READY (2 oracle rounds).** Drafted [`write-redesign-g1-plan.md`](../references/write-redesign-g1-plan.md); opus
oracle round 1 = **HOLD** (5 must-fixes) → revised → round 2 = **PASS**. The HOLD paid off: it caught that the
canonical docs **undercounted the RUB suite (~51 → 94 real rows)** and that "spawn the judge, read flag/no-flag"
only covers ⅔ of the suite — the F13 panel, reader-model, and XSTANCE-triage scenarios each grade differently.
Fix: a per-scenario **`grading_mechanism`** field (four mechanisms). `eb479f8`.

**Phase B — built G1 in 4 atomic chunks, each through the three-net loop:**
- **G1-a** (`6c79062`) — `rub_harness.py` parser + store (`rub_scenarios.json`, 94 RUB rows) + `validate-suite`
  DET (parses `scenarios.md` LIVE, diffs the store so they never drift). Corrected the `~51→94` count in
  [`tasks.md`](../tasks.md) + `scenarios.md`. Oracle FIX-THEN-PASS: MF-1 `SC-STR-03` misroute (→ F11 verdict-line, not lattice);
  MF-2 `expect_class` for lattice; MF-3 `expect_reason` in the drift tuple; NH-1 parse-integrity (6-field guard).
- **G1-b** (`1a1e474`) — the scorer: four mechanism-readers + the threshold (every DET green ∧ every RUB
  recorded-fresh-and-PASS, anchors never waivable) + `record`. Oracle FIX-THEN-PASS: MF-1 restored
  `_coerce_bool` (a string `"false"` was silently reading as not-flagged — the cardinal silent-pass); MF-2 lattice
  `None==None` guard; MF-3 the **INPUT-freshness binding** (each result stamped with the scenario INPUT hash; a
  later edit makes it STALE→FAIL — the `verdicts.py` content-hash twin).
- **G1-c** (`8a1e38e`) — the `sign-off` CLI (lifts `accept-residual`: refuses a failing suite, binds to the suite
  hash, goes STALE on change) + the run-protocol doc `rub-harness-protocol.md`. Oracle FIX-THEN-PASS: MF-1 the
  **inverted-guard silent-pass** — `SC-XSTANCE-08/16` phrase noflag as "NOT a handoff" (no literal "MUST NOT"), so
  `expect` derived to `flag` and the guards graded inverted (correct behavior FAILed, the regression PASSed); fixed
  with `_derive_expect`.
- **G1-d** (`265a7a3`) — the **required live dry-run**: spawned the real graders on one fixture per mechanism.
  `sw-voice-auditor` on SC-VOICE-01 flagged agency-to-abstraction (anchor reason-match satisfied); `sw-reader-model`
  classified SC-RM-2 NEW; `counter-argument` on SC-ARG-10 returned SURVIVES+mapped→noflag; the stage-5.5 triage on
  SC-XSTANCE-01 opened `needs-stance(/interpret)`, didn't narrow, named E006 (M3 backstop fired). All four graded
  PASS; both run anchors cleared. The spawning layer the Python selftest can't reach is proven.

**G2 — D051 (`9c40c79`).** The framing-sentence escape is DECIDED: **accept as a documented cutover limit**, don't
build a prose→lattice check. Rationale: the residual is narrow (F5 scope + F12 voice read ALL prose, so
over-scoped and badly-voiced framing — incl. the Claudio anchors — are already caught); closing it is a high-FP
RUB judge (the L060 over-flagging trap); the F16 human gate is the backstop.

**G3 (`d24ea00`, optional confidence).** Ran the live stage-5 prose judges on a real Methods slice: the first
draft was correctly NOT clean (voice flagged a reflex passive; structure flagged old→new inversion + a CCC break)
→ applied the findings (one revise round) → re-audit → all three `ready_to_ship`. **The revise loop closes and
good prose ships; the audit discriminates** (it didn't rubber-stamp).

**Final dual opus readiness review.** `oracle-reviewer` = **READY-FOR-P3** (verified the selftest/count/formats/
fail-closed behavior). `premortem-analyst` (the pessimist) found real pre-cutover defects → all fixed in the
**readiness-hardening** commit (`710309c`): the panel-synthesis exact-match brittleness (`cs == "SURVIVES"`
false-passed "Survives"/"SURVIVES (caveat)" → now normalized + MALFORMED→FAIL); a `--raw` verbatim-verdict
provenance field (narrows batch-faking in the 94-spawn run); the protocol field-name fix (`old`/`new`); and the
P3-plan guardrails (P3-0 committed dress rehearsal; P3-2 split the irreversible step). On re-check the premortem
returned **READY** with no hard blocker. D051 amended with an F16 framing-sentence forcing-function.

## Verdict
**Pre-P3 checklist CLEARED** (G1 built+oracle-hardened+live-proven · G2 decided · G3 demonstrated); **both opus
reviewers confirm READY-FOR-P3.** No science touched. The actual P3 cutover is IRREVERSIBLE and **Erfan-driven** —
not done here, per the stop condition.

## Next focus
**P3 cutover (Erfan drives, IRREVERSIBLE; confirm before each step).** First **P3-0**: a committed fresh-context
~10-scenario dress rehearsal (≥2/mechanism, a flag-expecting panel row + an anchor, `--raw`, artifacts committed)
before the 94-run. Then P3-1 (full 135-suite, expect a multi-round first pass) → P3-2 (split the irreversible
commit: tombstone the old flow ~1 week, triage the 13 DET checks for hook-safety) → repoint `CLAUDE.md` +
[`03-methodology.md`](../03-methodology.md), record D048-complete. The E006 voxelwise-CI `/interpret` item stays parked (orthogonal).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
