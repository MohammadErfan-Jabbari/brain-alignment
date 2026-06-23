# 2026-06-23 — /write pipeline BUILD: Phase-1 walking skeleton (C1–C8) + P2-A (Argument concern)

**Stance:** `/meta` (build the apparatus). **NO experiment, NO science number, NO rung change — Q0–Q5 stand
exactly as S35.** This session implemented the BUILD-READY `/write` redesign (D048) from the S35 design.

## What this session did

Built and verified the redesigned `/write` pipeline as a new, self-contained skill at
`.claude/skills/sci-write-v2/` (the live `scientific-writing` skill is **untouched** — cutover is Phase 3).
Implemented Erfan's exact method: **phase by phase, in small atomic chunks; at the end of each chunk a fresh
`claude -p` session loads the new artifact and runs its scenarios, an opus reviewer adversarially critiques it
and designs new scenarios, all must clear before moving on.** Two sources of truth per chunk: the
`docs/references/write-redesign-*` docs **and** the S35 session log (`3ce96589-…jsonl`), mined per-chunk by a
subagent.

**Phase 1 — walking skeleton (C1–C8), all green end-to-end on the abstract:**
- **C1** claim-lattice schema (F15) + `lattice_integrity` DET floor.
- **C2** claim-binding (F3) + `evidence-register.json` (seeded from the ladder).
- **C3** F6 skeleton stage-3 procedure + hardened coverage floor.
- **C4** F8a drafter (`sw-drafter`, emits `\evd{claim-id}{strength}`) + `draft_check` prose floor.
- **C5** F12 voice audit — lifted `ai_tell_lint` (DET) + `sw-voice-auditor` (RUB); **the Claudio regression
  anchor SC-VOICE-01–04 is caught.**
- **C6** claim-fidelity F9a (DET tag≤strength) + F9b (`sw-claim-fidelity-judge`, RUB assertion≤tag).
- **C7** F16 gate (`gate_state`, no-prose-before-approval, D047 content-hash pattern).
- **C8** orchestrator `SKILL.md` + `run_checks.py` DET dispatcher; **Phase-1 acceptance met** (DET floor 6/6,
  voice clean on the real abstract, voice catches a Claudio-dirtied copy, gate blocks pre-approval).

**Phase 2 — P2-A (the Argument concern):** F4 warrant-validity + F5 scope, each a DET hook
(`warrant_schema`, `scope_lint`) + an opus-xhigh RUB judge (`sw-argument-judge`, `sw-scope-judge`), one judge
at two sites (stage-2 lattice + stage-5 prose). Closes the highest-value Phase-1 gap (an assertive sentence
whose inference doesn't hold or whose scope exceeds its evidence).

## Method discipline (held every chunk)
log-mine (subagent) → build → **opus oracle review** (every chunk returned FIX-THEN-PASS with real findings —
all fixed) → **fresh `claude -p` clean-room verification** → atomic commit. ~9 chunks, 9 commits. A recurring
lesson surfaced and was applied repeatedly: **never HARD-block a dual-use lexical pattern** (tricolon in C5,
`full ... curve`/`any model` in P2-A → demoted/dropped to the RUB judge). The gate's deepest fix: the
ordering floor binds to **prose existence**, not the agent-self-reported `meta.stage` (an agent could
otherwise write prose at stage 3 and bypass the gate).

## State of the build
- ~9 DET scripts + 4 RUB agents + the orchestrator, all with embedded `--selftest`s; `run_checks --selftest`
  is the integration smoke (all green). Verification artifacts in `.claude/skills/sci-write-v2/examples/`.
- `git check-ignore` confirms `.claude/state/sw-gate/` (gate approval state) is gitignored.

## What's next (remaining /write build)
- **P2-B** — F11 structure judge (2 sites) + F1 reader-model + F2 message&frame.
- **P2-C** — F18 acknowledgment + F13 premortem-panel wiring + F7 figures + F17 exemplar pin + F8b
  voice-realize + F19 consistency.
- **P2-D** — CC-power upgrades: parallel stage-5 fan-out + structured `ready_to_ship` verdicts + the D047
  Stop-hook convergence + the AskUserQuestion gate.
- **P3 (gated, IRREVERSIBLE — needs Erfan)** — run the FULL 119-scenario suite end-to-end; only when green,
  retire the old `scientific-writing` flow, wire the DET checks as always-on hooks, point `CLAUDE.md` +
  `docs/03-methodology.md` at the new pipeline, record D048-complete.

## Ladder
Unchanged. This is a `/meta` apparatus build; no rung flips, Q0–Q5 stand. The live science next-step
(Q4 sample-efficiency E024) is unchanged.
