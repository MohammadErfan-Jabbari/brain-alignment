# Upspeed — read first, write last

**Last updated:** 2026-06-23 (S37 — **/meta: BUILT `/write` Phase-2 P2-B + P2-C — all verified, green.** Continued the D048 rebuild (new skill `.claude/skills/sci-write-v2/`; live `scientific-writing` untouched). Built five atomic chunks (F1 reader-model, F2 message&frame, F11 structure judge, F7 figures, F13 premortem panel, F18 acknowledgment, F17 exemplar pin, F8b voice-realize, F19 consistency), each via the three-net loop — `--selftest` → **opus oracle (every chunk FIX-THEN-PASS, all fixed)** → **fresh `claude -p` verify** → atomic commit + build-log entry. 7 commits. **NO experiment, NO science number, NO rung change — Q0–Q5 stand.** Prior: S36 — built C1–C8 + P2-A.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **`/write` build state lives in [`docs/references/write-redesign-build-plan.md`](references/write-redesign-build-plan.md)** — its **Status** line + the append-only **build log** are the source of truth for the rebuild. With no task, run `/orient`.

## What this session did (/meta — the build)
Phase-2 of the `/write` pipeline is now built end-to-end except the CC-power upgrades:
- **P2-B-i (F1+F2):** `sw-reader-model` agent → lattice `reader_model`; new fields `frame`/`contribution_type`; stage-≥3 schema floor.
- **P2-B-ii (F11):** `sw-structure-judge` (sonnet, xhigh), one judge / two sites (skeleton width+CARS · prose point-sentence/old→new/CCC).
- **P2-C-1 (F7+F13+F18):** `sw-acknowledgment` (opus, two-pass); F7 figure planning (DET already existed); F13 = the shared D017 panel wired at stage 5.
- **P2-C-2a (F17+F8b):** `references/F17-exemplars.md` + `register` field/DET; `sw-voice-realize` (sonnet) edits-in-place, preserving tags/markers/numbers.
- **P2-C-2b (F19):** `consistency_check.py` (abstract↔body result-numbers + CI-in-abstract).

The opus oracle earned its keep at every chunk — see the build-plan **build log** for each chunk's FIX-THEN-PASS findings (the load-bearing ones: F11 stage-5 reader_model sourcing; F8b number-conservation; the F19 L060 over-block; the F13→F18 claim-id adapter).

## What's next (resume the build here)
- **P2-D — the CC-power upgrades** (the last Phase-2 work; orchestration/hook plumbing, different in kind from the F-functionalities):
  - **parallel stage-5 fan-out** — spawn the stage-5 RUB readers (F4/F5/F9b/F11/F12/F13/F19-caption) in one message, not serially.
  - **structured `ready_to_ship` Stop-hook convergence** — a real `settings.json` Stop hook (the D047 pattern, pipeline-scoped) that re-blocks until every reader's `*-VERDICT: {ready_to_ship:true}`. The judges already emit those lines.
  - **AskUserQuestion / ExitPlanMode gate** for F16 (a real approval primitive, not ad-hoc text).
- **P3 — cutover (IRREVERSIBLE; confirm with Erfan):** full 119-scenario suite green → retire the old `scientific-writing` flow → wire the DET checks as always-on hooks → point `CLAUDE.md` + `docs/03-methodology.md` at the new pipeline → record D048-complete.
- **Live science thread (UNCHANGED since S25):** Q4 sample-efficiency E024; the analysis lane (Erfan) next = R08 (Q2). Q2 ❌, Q3 ❌ stand.

## Blockers / open loops
- The build is **not cut over** — the old `scientific-writing` flow is the default until the full 119-suite passes (P3). Both coexist; `sci-write-v2` is invokable for testing.
- **`start.json` clobber recurs (L062):** a fresh `claude -p` verifier child overwrites the parent's wrap snapshot despite `CLAUDE_WRAP_SNAPSHOT_SKIP=1` (this session: `start.json.session_id` was a child's, `start_sha` mid-session). `/wrap` must verify `session_id` matches the live session and fall back to the first-commit diff. Fix owed (in `tasks.md`).

## Key facts for P2-D onward
- **The build method (unchanged, mandatory):** per atomic chunk → embedded `--selftest` (regression net) → **opus `oracle-reviewer`** (discovery net — run on EVERY chunk; each so far had a silent-pass/over-block the selftest missed) → fix + fold the oracle's new scenarios → **fresh `claude -p` clean-room verify** → atomic commit + a build-log entry in `write-redesign-build-plan.md`.
- **Fresh-session verifier command:** `CLAUDE_WRAP_SNAPSHOT_SKIP=1 timeout 540 claude -p "<task>" --model sonnet --permission-mode bypassPermissions --add-dir <scratch>` — and **set the Bash tool `timeout` to ≥ 540000 ms** (the default 120 s silently kills it). A fresh `claude -p` DOES load mid-session-added skills/agents/scripts; an in-process Agent subagent does NOT (verify with a subprocess). (L061.)
- **The two DET failure modes that recurred at every chunk:** **L059** — a DET floor binds to ground truth and fails toward MORE checking on ambiguity; **L060** — never HARD-block a dual-use lexical/numeric surface (flag SOFT / give it to the RUB judge). The number-conservation DET (`draft_check --prev-prose`) is the prose analog of the lattice append-safe `diff`.
- **One DET call:** `python3 .claude/skills/sci-write-v2/scripts/run_checks.py --lattice L [--prose P] [--prev PREV-lattice] [--prev-prose PREV-prose] [--repo-root DIR]`. `--selftest` runs all 9 components' selftests (the integration smoke; green).
- **The gate binds to prose-existence** (not `meta.stage`); `.claude/state/sw-gate/` is gitignored. The gate-package hash now includes `frame`/`contribution_type`/`register` (a stage-1 change re-enters the gate).
- **New agents this session:** `sw-reader-model`, `sw-structure-judge`, `sw-acknowledgment`, `sw-voice-realize`. **F13 reuses** the existing `premortem-analyst` + `counter-argument` (do NOT rebuild them; the orchestrator adapts their output to claim-ids).
- **Source-of-truth logs** (mine with a subagent when a design choice is unclear): redesign `3ce96589-47c5-4d6b-ab6b-d2e7b7a85134`, first build `1709254b-72c6-40a0-bacd-0d88e900691f` (recorded in the build plan).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
