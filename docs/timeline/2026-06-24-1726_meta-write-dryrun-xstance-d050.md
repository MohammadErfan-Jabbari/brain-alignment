# 2026-06-24 17:26 — /meta: /write dry-run + cross-stance handoff designed to BUILD-READY (D050)

**Stances:** `/meta` throughout (dominant). Crossed into `/review` (the opus reviewer panel) and a thin
`/scout`-style log-mine. **No `/work`, no science number produced or consumed, no rung moved — Q0–Q5 stand.**
Two commits: `c94ab74` (canvas Step 3), `cadfea3` (D050).

## What happened

1. **`/meta` review of the `/write` rebuild** — read the four redesign/build session logs + all `docs/references/write-redesign-*`. Confirmed Phase 2 complete, P3 next; surfaced the open holes (RUB-grading harness undefined, framing-sentence escape, provenance non-goal, never-run-on-real-prose).

2. **Updated the design canvas** (`write-redesign-design.html`, `c94ab74`): the canvas stopped at BUILD-READY and never reflected the actual build. Added **Step 3 · the build** (phase-status board, the three-net method, a "where the build refined the design" delta table) + the open-P3 holes. v1.1 → v2.0.

3. **Ran a `/write` dry-run** of `sci-write-v2` on the simple case **R06 / §4.1** ("the alignment signal is real, beyond confounds"), generate-mode, output in gitignored `outputs/dryrun-A/` (NOT a committed deliverable). The full pipeline ran end-to-end: lattice → reader-model (F1) + acknowledgments (F18) + stage-2 judges (F4/F5) → skeleton + structure judge (F11) → **F16 gate (Erfan approved)** → drafter (F8a) → voice-realize (F8b) → DET floor (9 checks green incl. number-conservation) → the **7-reader parallel audit**.
   - **The pipeline works, and the audit is sharp.** F4/F5 passed; F9b caught a fidelity over-read ("prevent…from manufacturing" over-reads its `supported` tag); F11 caught an old→new gloss-ordering miss; F12 caught the **exact Claudio voice class** ("the effect *survives*", "breadth *speaks to*"); the **F13 panel found a real science problem**: the E006 voxelwise CI is a **within-subject voxel bootstrap** (pseudo-replicated — the L015 error caught on E005, uncorrected on E006). The counter-argument agent recomputed a fold-level CI from stored JSON and reports it still excludes zero (so the verdict survives, but the *stated statistic* is wrong-unit).
   - **The boundary worked as the hard line predicts:** the draft *cannot converge in `/write`* — the blocking finding is a number that must be fixed upstream, and the convergence loop would otherwise have "fixed" it by rewording with the panel's unrecorded recompute. Disarmed the dry-run Stop-hook cleanly; gate state left clean.

4. **Designed the cross-stance handoff to BUILD-READY (D050)** — the structural gap the dry-run proved: when an auditor finds a defect the prose cannot fix (it lives in the evidence/argument substrate), `/write` had no path to route it. Followed the original redesign methodology (ideal framing → trigger taxonomy → 2a functionality F20 → 2b scenarios → 2c CC-projection → 2d coverage → build chunks), with a **clean-context opus critic at every phase boundary** (L058) — four reviews, each NEEDS-WORK→fixed, ending BUILD-READY. The single-store collapse (review #3 ponytail finding) simplified the build to four chunks. Integrated into `write-redesign-xstance.md` (new, full spec), the build-plan (X1–X4), the scenario coverage table (F20, 119→135 at X4), the canvas (Step 4, v2.1), and recorded **D050**. `cadfea3`.

## The design in one line
A third audit outcome `NEEDS-STANCE(S)`: detect → classify → emit a handoff → **block convergence stickily** (`handoffs.json` keyed off the prose hash, so a reword can't close it) → recommend the stance; never auto-spawn, never adopt an unrecorded number. DET backstop forces it on out-of-`docs/` panel narrowings; `evidence_status: suspect` makes the lesson sticky. Detect-and-recommend, not auto-initiate (Erfan's call).

## Parked / open
- **E006 voxel-bootstrap CI = a `/interpret` item** (a ✅-rung result reports a pseudo-replicated CI). The panel's fold-level recompute is a **lead to verify, not a fact**. Do NOT run before the handoff is built. Tracked in `tasks.md`.
- **Hard-case dry-run (R07/§4.2) was never run** — we pivoted to the design once the simple case surfaced the gap. Optional now; the dry-run's purpose was achieved.

## Continuity notes
- `start.json` was stale (its `start_sha` was this session's own last commit `cadfea3` — the SessionStart hook re-fired on a resume after the commits). Used the git-log fallback (`310021f..HEAD`).
- Untracked `docs/learning/lessons/2026-06-24-boruta-feature-selector.md` was present at session start (not from this session) — left as-is.
