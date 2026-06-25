# Upspeed — read first, write last

**Last updated:** 2026-06-25 (S40 — **/meta: cross-stance handoff X1–X4 BUILT (D050); `/write` suite 119 → 135.**
Implemented the S39 BUILD-READY design as four atomic chunks under the three-net loop (selftest → opus oracle →
fresh `claude -p` → commit): X1 `evidence_status: suspect` (4 sites), X2 `verdicts.py` handoff store + the sticky
`handoffs-open` blocker, X3 SKILL stage-5.5 triage, X4 folded the 16 `SC-XSTANCE-*` into the suite + a P3 test-plan.
Every oracle a real PASS/FIX-THEN-PASS with findings folded; the fresh net caught a routing ambiguity the oracle
missed (X3). 4 commits. **NO experiment, NO science number, NO rung change — Q0–Q5 stand.** Prior: S39 — /write
dry-run + cross-stance design.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **`/write` build state lives in
> [`write-redesign-build-plan.md`](references/write-redesign-build-plan.md)** (X1–X4 ✅ COMPLETE); the 135-scenario
> suite + P3 test-plan is [`write-redesign-scenarios.md`](references/write-redesign-scenarios.md). With no task, run
> `/orient`.

## What this session did (/meta — build X1–X4)
- **X1** (`e1702a5`) `evidence_status: suspect` at 4 sites. A `/write` reader can flag a recorded result as doubtful
  (no later verdict overruled it, the aggregation is contested — the E006 voxel-bootstrap CI); citing it as live
  fires `[stale-evidence]`. Set by `/interpret`→`/work`+Erfan, never by `/write`.
- **X2** (`fd07799`) `verdicts.py`: the `handoffs.json` store + `handoff open/resolve/status/check` + the **sticky
  `handoffs-open` blocker** in `status()` (M1 keystone — read independently of the prose hash, so a reword can never
  clear a substrate defect; only the upstream stance recording its output can) + `ship`/`accept-residual` refusal.
- **X3** (`077a57b`) SKILL **Stage 5.5 · Handoff triage**: the 3 outcomes (PASS / WRITING-REVISE / NEEDS-STANCE),
  the M3 backstop force-rule (a panel `SURVIVES-IF-NARROWED` needing an out-of-`docs/` number is forced to
  needs-stance — catches E006), the 7-row taxonomy, the two-gate rebind contract.
- **X4** (`d12c725`) folded the 16 `SC-XSTANCE-*` into the suite (119 → 135) + a P3 test-plan mapping each to its
  live DET selftest label or its RUB P3-harness pass criterion.

## What's next (resume here)
- **P3 cutover — IRREVERSIBLE, Erfan drives.** X1–X4 are done, so the cutover no longer freezes a known gap.
  **First task: stand up the RUB-grading harness** for the ~51 RUB scenarios (incl. the 10 RUB `SC-XSTANCE-*`) + a
  sign-off mechanic — none exists (the standing P3 open loop, now also carrying the cross-stance scenarios). Then:
  run the full 135-suite → if green, retire the old `scientific-writing` flow, repoint `CLAUDE.md` +
  `docs/03-methodology.md`, wire DET as always-on hooks, record D048-complete. **Confirm with Erfan first.**
- **Optional next-step I offered:** scope the RUB-grading harness design (Erfan's call whether to do that before P3).
- **Live science thread (UNCHANGED since S25):** Q4 sample-efficiency E024; analysis lane next = R08 (Q2). Q2 ❌,
  Q3 ❌ stand.

## Blockers / open loops
- **E006 voxelwise CI — still a parked `/interpret` item, NOT adjudicated** (carried from S39). The F13 dry-run panel
  showed the headline CI is a voxel bootstrap (pseudo-replicated; inferential n = 1 brain, not the voxel count); the
  fold-level recompute (still excludes zero) is a **lead to verify, not a fact**. It backs a ✅-rung result (Q0/A2),
  so it matters. D050's whole point is that `/write` now routes exactly this kind of defect upstream instead of
  papering over it. Verify in `/interpret`/`/work`. (tracked in `tasks.md`)
- **P3 RUB-grading harness still undefined** (now the larger of the two P3 blockers — ~51 RUB scenarios, no harness,
  no sign-off mechanic).
- **Framing-sentence escape still open** — D050 does NOT close it (only the human gate catches a load-bearing
  sentence never entered as a claim). Recorded in SKILL "Honest limits."
- Build not cut over; the old `scientific-writing` skill remains the default until P3.

## Key facts for next session
- **The new pipeline is `sci-write-v2` (still NOT the default).** Cross-stance handoff X1–X4 complete. DET sanity in
  one shot: `cd .claude/skills/sci-write-v2/scripts && uv run python {lattice_integrity,claim_binding,verdicts,run_checks}.py --selftest` — all PASS.
- **Handoff CLI:** `verdicts.py handoff open <id> --finding … --threatens-claim <C> --target-stance <work|interpret|review|scout|plan> --why … --what-to-produce … --recommended-command …`; `handoff resolve <id> --ref <recorded-output>`; `handoff status`; `handoff check --lattice <L>` (run after a re-skeleton — dangling-orphan guard). `ship`/`accept-residual` refuse past an open handoff.
- **Build method (unchanged, reuse for P3 work):** three nets per chunk — `--selftest` → opus `oracle-reviewer` on
  EVERY chunk → fresh `claude -p` clean-room → atomic commit + build-log. Fresh verifier:
  `CLAUDE_WRAP_SNAPSHOT_SKIP=1 timeout 540 claude -p "<task>" --model sonnet --permission-mode bypassPermissions --add-dir <scratch>`; Bash `timeout` ≥ 540000 ms. The third net is not redundant — it caught an ambiguity the oracle missed this session.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
- **Stray file:** `docs/learning/lessons/2026-06-24-boruta-feature-selector.md` is foreign to this repo's
  conventions (our lessons live in `docs/learnings.md`); left untouched per Erfan.
