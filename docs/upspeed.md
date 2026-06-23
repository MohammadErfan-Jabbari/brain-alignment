# Upspeed — read first, write last

**Last updated:** 2026-06-23 (S36 — **/meta: BUILT the `/write` redesign — Phase-1 walking skeleton (C1–C8) + Phase-2 Argument concern (P2-A), all verified.** Implemented the S35 BUILD-READY design (D048) as a new self-contained skill `.claude/skills/sci-write-v2/` (the live `scientific-writing` skill is untouched; cutover is Phase 3). Method: phase-by-phase atomic chunks, each = log-mine (S35 log + reference docs) → build → **opus oracle review (every chunk FIX-THEN-PASS, all fixed)** → **fresh `claude -p` clean-room verification** → atomic commit (9 commits). The walking skeleton runs green end-to-end on the abstract; the Claudio regression anchor is caught. **NO experiment, NO science number, NO rung change — Q0–Q5 stand exactly as S35.** Prior: S35 — designed the `/write` pipeline to BUILD-READY.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **How to operate = [`operating-map.md`](operating-map.md)** (8 stances). With no task, run `/orient`.

## What this session did (/meta — the BUILD)
Built the redesigned `/write` pipeline at **`.claude/skills/sci-write-v2/`** (new, self-contained; the live
`scientific-writing` skill is untouched). 9 atomic chunks, 9 commits, each opus-oracle-reviewed +
fresh-`claude -p`-session verified:
- **Phase 1 (C1–C8), green e2e on the abstract:** lattice + `lattice_integrity` (C1); claim-binding F3 +
  `evidence-register.json` (C2); F6 skeleton (C3); F8a drafter `sw-drafter` + `draft_check` (C4); F12 voice
  `ai_tell_lint` + `sw-voice-auditor` — **catches the Claudio anchor** (C5); F9a/F9b claim-fidelity +
  `sw-claim-fidelity-judge` (C6); F16 gate `gate_state` (C7); orchestrator `SKILL.md` + `run_checks.py`
  dispatcher (C8). **Phase-1 acceptance met.**
- **Phase 2 P2-A (Argument concern):** F4 `warrant_schema` + `sw-argument-judge`, F5 `scope_lint` +
  `sw-scope-judge` (opus xhigh, 2 sites each).
- **Apparatus:** every script has a `--selftest`; `run_checks --selftest` is the integration smoke (green).
  The per-chunk verifier loop Erfan designed (fresh session loads the new artifact + opus reviewer adds
  scenarios) is proven to work — a fresh `claude -p` does load skills/commands/scripts added mid-session.

## What's next (resume the build here)
- **P2-B** — F11 structure judge (2 sites) + F1 reader-model + F2 message&frame.
- **P2-C** — F18 ack + F13 premortem-panel + F7 figures + F17 exemplar pin + F8b voice-realize + F19 consistency.
- **P2-D** — CC-power upgrades: parallel stage-5 fan-out + structured `ready_to_ship` verdicts + D047 Stop-hook
  convergence + AskUserQuestion gate.
- **P3 (IRREVERSIBLE — confirm with Erfan):** full 119-scenario suite e2e → retire old flow → wire DET hooks →
  point `CLAUDE.md`/`03-methodology.md` at the new pipeline → record D048-complete.
- **Live science thread (UNCHANGED since S25):** Q4 sample-efficiency E024. Q2 ❌, Q3 ❌ stand.

## Blockers / open loops
- The build is **not cut over** — the old `scientific-writing` flow is still the default until the new pipeline
  passes the full 119-suite (Phase 3). Both coexist; `sci-write-v2` is invokable for testing.
- Per-chunk discipline must continue for P2-B onward: log-mine → build → opus oracle → fresh-session → commit.

## Key facts
- **New skill:** `.claude/skills/sci-write-v2/` (SKILL.md = orchestrator; `scripts/` = DET floor;
  `schema/LATTICE.md` = the spine; `examples/` = the abstract worked-example + acceptance evidence). New
  agents: `sw-drafter`, `sw-voice-auditor`, `sw-claim-fidelity-judge`, `sw-argument-judge`, `sw-scope-judge`.
- **One DET call:** `python3 .claude/skills/sci-write-v2/scripts/run_checks.py --lattice L [--prose P] [--prev PREV]`.
- **The gate binds to prose-existence**, not the self-reported stage (the key C8 fix). `.claude/state/sw-gate/` is gitignored.
- **Fresh-session verifier mechanics (use for P2-B onward):** `timeout 540 claude -p "<task>" --model <m> --permission-mode bypassPermissions --add-dir <scratch>`; **raise the Bash tool's `timeout` to ≥540000ms** or the default 120s kills the run (this bit once). A fresh `claude -p` DOES load skills/commands/scripts added this session; an in-process Agent subagent does NOT (L061). Run the opus oracle review FIRST, fix, THEN the fresh-session verify.
- **Design master doc:** `docs/references/write-redesign-design.html`; the 119-scenario suite is
  `docs/references/write-redesign-scenarios.md`. Build map: `write-redesign-build-plan.md`.
- **Effort tiers (Erfan-approved):** all subagents HIGH; F4/F5/F11 XHIGH.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
