# Upspeed — read first, write last

**Last updated:** 2026-06-25 (S42 — **/meta: G1 RUB-grading harness BUILT (a–d); G2/G3 cleared; dual opus review →
READY-FOR-P3.** Cleared the entire pre-P3 readiness checklist for the `/write` rebuild (D048). Built the one hard
blocker — the RUB-grading harness `rub_harness.py` (94 RUB scenarios, 4 grading mechanisms) — in 4 atomic chunks
under the three-net loop (selftest → opus oracle → fresh `claude -p`/black-box → commit), then decided the
framing-escape (G2/D051), demonstrated the convergence loop closes on real prose (G3), and confirmed readiness with
two opus reviewers (`oracle-reviewer` READY + `premortem-analyst` READY after its findings were fixed). 8 atomic
commits. **NO experiment, NO science number, NO rung change — Q0–Q5 stand.** Prior: S41 — /meta verified the X1–X4
build holds (read-only); S40 — built X1–X4 (D050).)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **`/write` build state lives in
> [`write-redesign-build-plan.md`](references/write-redesign-build-plan.md)** (Phase 2 ✅ · X1–X4 ✅ · **G1 ✅ ·
> G2 ✅ · G3 ✅ — pre-P3 checklist CLEARED**). G1 design: [`write-redesign-g1-plan.md`](references/write-redesign-g1-plan.md).
> With no task, run `/orient`.

## What this session did (/meta — clear the pre-P3 checklist)
- **Mined the working pattern** from the 5 prior build/design session logs (parallel sonnet subagents), then
  replicated it: plan → opus-harden → atomic chunks under the three-net loop → commit + build-log.
- **G1 (the blocker) — the RUB-grading harness, COMPLETE.** `scripts/rub_harness.py` + `rub_scenarios.json`.
  - **G1-a** store + `validate-suite` DET (live-parses `scenarios.md`, diffs the store); fixed the canonical
    RUB count **~51 → 94** in `tasks.md`/`scenarios.md`.
  - **G1-b** the scorer: 4 mechanism-readers (verdict-line 80 · handoff-state 10 · panel-synthesis 2 ·
    lattice-classification 2) + the threshold (DET green ∧ every RUB fresh-and-PASS, anchors never waivable) +
    the INPUT-freshness binding (stale result → FAIL).
  - **G1-c** the `sign-off` CLI (refuses a failing suite, binds to the suite hash, STALE on change) + the
    run-protocol doc `references/rub-harness-protocol.md`.
  - **G1-d** the live dry-run: real graders on one fixture per mechanism, all PASS, both run anchors cleared.
- **G2 — D051:** framing-sentence escape ACCEPTED as a documented cutover limit (+ an F16 gate forcing-function);
  do not build a high-FP prose→lattice check.
- **G3:** the revise loop closes on real prose (draft → audit flags real defects → one revise → all judges clean).
- **Readiness hardening (from the premortem):** panel-synthesis normalizer + MALFORMED→FAIL; `--raw` provenance;
  protocol field-name fix; P3-plan guardrails (dress rehearsal + split the irreversible step).

## What's next (resume here)
- **P3 cutover — IRREVERSIBLE, Erfan drives; confirm before each step.** The pre-P3 checklist is cleared and both
  opus reviewers confirm READY-FOR-P3. **First task P3-0:** a committed, fresh-context **~10-scenario dress
  rehearsal** of the harness (≥2 per mechanism, incl. a `flag`-expecting panel row + an anchor; `--raw` on every
  verdict-line/panel row; commit the `state/rub-results/*.json`). This converts S42's n=4 self-reported G1-d into a
  reproducible artifact and surfaces the real manual-entry burden before the one-shot 94-run.
- **Then P3-1:** run the full 135-suite (DET green + RUB harness-pass). **Expect a multi-round first pass** — 60%
  of graders were live-unexercised at G1-d; each FAIL is a pipeline fix or a fixture fix, never a waiver.
- **Then P3-2:** retire the old `scientific-writing` flow (tombstone it ~1 week first), triage which of the 13 DET
  checks are safe as always-on per-edit hooks, repoint `CLAUDE.md` + `03-methodology.md`, record D048-complete.

## Blockers / open loops
- **E006 voxelwise CI — still a parked `/interpret` item, NOT adjudicated** (carried since S39). Orthogonal to P3
  (the handoff mechanism is built+verified, so re-adjudicating E006 does not block the cutover). Verify in
  `/interpret`/`/work`.
- **The 94-spawn P3 run is the TRUSTED-not-verified risk surface** (premortem mode 1): the harness can't tell a
  real judge run from a hand-typed PASS. Mitigated (not eliminated) by `--raw` provenance + the PROVENANCE-GAP
  surfacing + the committed dress rehearsal; the human running the gate is the backstop.
- **Live science thread (UNCHANGED since S25):** Q4 sample-efficiency E024; analysis lane next = R08 (Q2). Q2 ❌,
  Q3 ❌ stand.

## Key facts for next session
- **`sci-write-v2` is still NOT the default** (cutover is P3). DET sanity in one shot:
  `cd .claude/skills/sci-write-v2/scripts && uv run python {run_checks,verdicts,rub_harness}.py --selftest` — all PASS.
- **RUB harness CLI:** `rub_harness.py {validate-suite | gen-store | record --id <ID> --result '<json>' --raw "<verdict line>" | score [--det-green] | sign-off [--by Erfan | --status]}`. The run protocol is `references/rub-harness-protocol.md`.
- **Build method (unchanged, reuse for P3):** per chunk — `--selftest` → opus `oracle-reviewer` on EVERY chunk →
  fresh `claude -p` clean-room (or black-box for pure-Python+data) → atomic commit + build-log. Mechanics:
  `CLAUDE_WRAP_SNAPSHOT_SKIP=1` on every `claude -p` child; Bash `timeout` ≥ 540000 ms; `cd` to repo root inside
  subprocess commands; scoped staging only.
- **The premortem is the right final gate for a self-built+self-reviewed apparatus** (L066): per-chunk oracles
  check the chunk; the premortem caught the false-PASS code defect + the self-graded-"COMPLETE" escalation they miss.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
- **Stray file:** `docs/learning/lessons/2026-06-24-boruta-feature-selector.md` is foreign to this repo's
  conventions (our lessons live in `docs/learnings.md`); left untouched per Erfan.
