# Upspeed — read first, write last

**Last updated:** 2026-06-23 (S38 — **/meta: /write rebuild — P2-D COMPLETE + P2-E authoring review.** Finished Phase 2 of the D048 rebuild (skill `.claude/skills/sci-write-v2/`; live `scientific-writing` untouched): the six P2-D CC-power chunks (convergence state machine, parallel stage-5 fan-out, the live convergence Stop-hook, the AskUserQuestion gate, SC-XS-3 caption, fluidity/deviation-log), each via the three-net loop. Then a full **authoring/quality review (P2-E)** against `writing-great-skills` + official CC sub-agent/hook docs → SKILL de-sediment 263→206, agent fixes, **effort frontmatter adopted fleet-wide**, settings brace form. 11 atomic commits. **NO experiment, NO science number, NO rung change — Q0–Q5 stand.** Prior: S37 — P2-B + P2-C.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **`/write` build state lives in [`docs/references/write-redesign-build-plan.md`](references/write-redesign-build-plan.md)** — its **Status** line + the append-only **build log** + the 4-session provenance table are the source of truth for the rebuild. With no task, run `/orient`.

## What this session did (/meta — the build + the review)
**Phase 2 of the `/write` pipeline is COMPLETE.** Two blocks:
- **P2-D (6 chunks, all green):** `verdicts.py` convergence machine (D-1) · parallel stage-5 fan-out + verdict recording (D-2) · the **live** `stop_sw_converge.py` Stop-hook, pipeline+session-scoped, loop-guarded (D-3 — oracle caught + I fixed a repo-wide-outage catastrophe) · F16 gate via `AskUserQuestion` (D-4) · SC-XS-3 caption≤figure folded into F5 + `caption`/`shows` fields (D-5) · fluidity/deviation-log SC-PROC-8/9/10/11 (D-6).
- **P2-E authoring review (before P3, so the components are clean before they become the default):** SKILL de-sediment + description rewrite (263→206; the build-chronology that duplicated the build-plan is gone) · 9 agents fixed (voice-realize lost `Write`; two descriptions reconciled; verdict-key unified) · **effort frontmatter adopted fleet-wide** (24 agents: xhigh for F4/F5/F11 — the real fix; high for the rest) · `${CLAUDE_PROJECT_DIR}` brace form. The hook reviewed fully compliant.

## What's next (resume here)
- **P3 cutover — IRREVERSIBLE, Erfan drives next session.** Run the full **119-scenario suite** (`docs/references/write-redesign-scenarios.md`). If green: retire the old `scientific-writing` flow, repoint `CLAUDE.md` + `docs/03-methodology.md` at sci-write-v2, wire the DET checks as always-on hooks, record D048-complete. **Confirm with Erfan before anything irreversible.** Note: P3 needs a RUB-grading harness/threshold + a sign-off mechanic for the ~41 RUB scenarios — not yet defined (flagged at S38).
- **Live science thread (UNCHANGED since S25):** Q4 sample-efficiency E024; analysis lane next = R08 (Q2). Q2 ❌, Q3 ❌ stand.

## Blockers / open loops
- The build is **not cut over** — old `scientific-writing` flow is the default until P3. Both coexist.
- **P3 RUB-grading harness undefined:** "pass the 119" has no scoring threshold/grader for the RUB half and no named sign-off mechanic beyond "Erfan signs." Resolve at P3 start.
- **Framing-sentence escape (Phase-2 residual, not closed):** an assertive sentence modeled as "framing" rather than a claim escapes the Trust floor; human gate is the only catch until a prose→lattice claim-coverage check exists.

## Key facts for P3
- **The convergence Stop-hook is LIVE but inert** — it no-ops unless a sci-write-v2 draft is armed (`verdicts.py activate --prose <F8b-draft>`); `ship` clears it; `accept-residual` is Erfan's escape. Real-repo state dir is clean (no `active.json`).
- **Build method (unchanged, use for any P3 fixups):** three nets per chunk — embedded `--selftest` → **opus `oracle-reviewer` (run on EVERY chunk — caught a real hole each time, incl. the P2-D-3 catastrophe)** → fresh `claude -p` clean-room verify → atomic commit + build-log entry.
- **Fresh-verifier command:** `CLAUDE_WRAP_SNAPSHOT_SKIP=1 timeout 540 claude -p "<task>" --model sonnet --permission-mode bypassPermissions --add-dir <scratch>` — and **set the Bash tool `timeout` ≥ 540000 ms** (the 120 s default silently kills it). (L062 did NOT bite this session — `start.json` was clean.)
- **One DET call:** `python3 .claude/skills/sci-write-v2/scripts/run_checks.py --selftest` (all components' selftests; green). `verdicts.py --selftest` covers the convergence machine + gate state.
- **All 24 agents now declare `model:` + `effort:`** (fleet default high; xhigh for F4/F5/F11). New convention, documented in `CLAUDE.md`.
- **Source-of-truth logs** (mine with a subagent when a design choice is unclear): the 4 in `write-redesign-build-plan.md`'s provenance table — redesign `3ce96589`, builds `1709254b` (P1+P2-A), `daa4f842` (P2-B/C), `1b3b0846` (P2-D + P2-E, this session).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
