# Upspeed — read first, write last

**Last updated:** 2026-06-24 (S39 — **/meta: /write dry-run + cross-stance handoff designed to BUILD-READY (D050).** Updated the design canvas with the build (Step 3, v2.0). Ran a `/write` dry-run of `sci-write-v2` on R06/§4.1 (generate-mode, gitignored `outputs/`): the full pipeline ran end-to-end and the 7-reader audit caught real writing defects **and** the F13 panel surfaced that the E006 voxelwise CI is a pseudo-replicated voxel-bootstrap statistic — a defect `/write` cannot fix. That gap → designed the **cross-stance handoff** (third audit outcome `NEEDS-STANCE`: route to the owning stance + block, never paper over) to BUILD-READY across 4 opus reviews; recorded D050; integrated into the canon (xstance spec, X1–X4 build chunks, Step 4 canvas, F20 scenarios). 2 commits. **NO experiment, NO science number, NO rung change — Q0–Q5 stand.** Prior: S38 — P2-D + P2-E.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **`/write` build state lives in [`write-redesign-build-plan.md`](references/write-redesign-build-plan.md)**; the **cross-stance handoff design (D050, BUILD-READY) lives in [`write-redesign-xstance.md`](references/write-redesign-xstance.md)**. With no task, run `/orient`.

## What this session did (/meta — review → dry-run → design)
- **Canvas Step 3** (`c94ab74`): folded the actual build (Phase 1+2) into `write-redesign-design.html` (it had stopped at BUILD-READY). v1.1→v2.0.
- **Dry-run of `sci-write-v2`** on R06/§4.1 (the simple case), generate-mode, `outputs/dryrun-A/` (gitignored, not a deliverable). Validated the pipeline end-to-end — and the F13 panel found the **E006 CI is a within-subject voxel bootstrap** (pseudo-replicated; the L015 error, uncorrected on E006). The draft *cannot converge in `/write`* because the blocker is upstream — exactly the hard line working. Disarmed cleanly; gate state clean.
- **Cross-stance handoff designed to BUILD-READY (D050, `cadfea3`):** the gap the dry-run proved. Followed the original redesign methodology + a clean-context opus critic at every phase (L058, 4 reviews → BUILD-READY). Single-store collapse simplified it to four build chunks X1–X4. Spec: `write-redesign-xstance.md`.

## What's next (resume here)
- **Build X1–X4 (cross-stance handoff, D050) FIRST, then P3 cutover.** X1–X4 must land **before** P3 so the cutover doesn't freeze the known gap. Three-net loop per chunk (selftest → opus oracle → fresh `claude -p` → commit). Spec: `write-redesign-xstance.md` §H; build entry: the "Cross-stance handoff" section of `write-redesign-build-plan.md`.
  - **X1** `evidence_status: suspect` at all four sites (`lattice_integrity.EVIDENCE_STATUS`, `claim_binding.STALE` + `check_register`, `LATTICE.md`, register).
  - **X2** `verdicts.py`: `handoffs.json` store + `handoff open/resolve/status/check --lattice` + the `handoffs-open` clause in `status()` + the `ship`/`accept-residual` refusal + no-op-when-missing selftest.
  - **X3** SKILL **stage-5.5 triage**: reader self-tag, the M3 backstop force-rule, the handoff emit + human surface, the two-gate rebind contract.
  - **X4** wire the anchor SC-XSTANCE-01 (= the dry-run) end-to-end + fold the 16 `SC-XSTANCE-*` into the suite (119→135).
- **Then P3 cutover — IRREVERSIBLE, Erfan drives.** Run the full **135-scenario suite**; if green: retire old `scientific-writing`, repoint `CLAUDE.md` + `docs/03-methodology.md`, wire DET as always-on hooks, record D048-complete. **First define** a RUB-grading harness/threshold + sign-off mechanic for the ~41 RUB scenarios (none exists). **Confirm with Erfan before anything irreversible.**
- **Live science thread (UNCHANGED since S25):** Q4 sample-efficiency E024; analysis lane next = R08 (Q2). Q2 ❌, Q3 ❌ stand.

## Blockers / open loops
- **E006 voxelwise CI — a parked `/interpret` item, NOT adjudicated.** The F13 panel showed the headline CI is a voxel bootstrap (pseudo-replicated; inferential n = 1 brain, not the voxel count). The panel's fold-level recompute (still excludes zero) is a **lead to verify, not a fact**. A ✅-rung result (Q0/A2) reports it, so it matters. Verify in `/interpret`/`/work`; do NOT run before X1–X4 is built. (tracked in `tasks.md`)
- **Hard-case dry-run (R07/§4.2) not run** — optional; the dry-run's purpose was met by the simple case. Erfan's call whether to run it next session.
- **P3 RUB-grading harness still undefined** (carried from S38); **framing-sentence escape** still open (D050 does NOT close it — human gate only).
- Build not cut over; old `scientific-writing` is the default until P3.

## Key facts for next session
- **Cross-stance design is BUILD-READY** — `write-redesign-xstance.md` (4 opus reviews). The keystone is the **sticky block**: a `handoffs-open` clause in `verdicts.py status()` keyed to a separate `.claude/state/sw-gate/handoffs.json`, NOT the prose hash — so a reword can't close a substrate defect, only the upstream stance's recorded output can. ONE store (no lattice field). `ship`/`accept-residual` refuse with an open handoff.
- **Dry-run mechanics (reuse for the hard case or any `/write` run):** lattice + drafts in a repo-internal gitignored dir (`outputs/…`) so `claim_binding` can find the repo root (it walks up for `docs/experiments/`; a scratchpad path outside the repo FAILS). The live Stop-hook arms on `verdicts.py activate`; clear `.claude/state/sw-gate/` to disarm a test.
- **Build method (unchanged):** three nets per chunk — `--selftest` → opus `oracle-reviewer` on EVERY chunk → fresh `claude -p` clean-room → atomic commit + build-log entry. Fresh-verifier: `CLAUDE_WRAP_SNAPSHOT_SKIP=1 timeout 540 claude -p "<task>" --model sonnet --permission-mode bypassPermissions --add-dir <scratch>`; set Bash `timeout` ≥ 540000 ms.
- **One DET call:** `python3 .claude/skills/sci-write-v2/scripts/run_checks.py --selftest`; `verdicts.py --selftest`.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
