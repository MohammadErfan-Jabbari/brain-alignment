# Worked example — the walking skeleton on the abstract

`abstract-lattice.json` + `abstract.tex` are the F3/F6/F8a output for the manuscript abstract (one bound claim
C1 → E006; the deferred-results summary is a prose `\gap`; the budget-argument/weak-prior sentences are framing,
not bound claims — see the Phase-1 honest-limits note in `../SKILL.md`).

## Phase-1 acceptance evidence (C8)

| Case | Command | Result |
|---|---|---|
| Happy path | `run_checks --lattice abstract-lattice.json --prose abstract.tex` (after `gate_state approve`) | **PASS** (6/6 DET) |
| Voice clean | `sw-voice-auditor` on `abstract.tex` | **REGISTER-CLEAN: YES** |
| Voice catches the class | `sw-voice-auditor` on a Claudio-dirtied copy | **flags** agency-to-abstraction (3 findings) |
| No prose before gate | `gate_state check` before approval | **BLOCKED** (SC-PROC-1) |
| Stage=3-with-prose bypass | `run_checks --prose …` on a stage-3 lattice, unapproved | **BLOCKED** (gate binds to prose existence, not the self-reported stage) |
| Logic-revision re-gate | a gated field changed after approval → `gate_state check` | **BLOCKED** (hash stale → re-enter the gate; SC-PROC-5) |

Every claim is `\evd`-bound (C1→E006); the DET floor is clean; the Claudio storytelling class is caught and the
clean abstract is not flagged. Phase-1 bar met.

## Deferred to Phase-2 acceptance widening
A multi-section document (the abstract is one section), the full orchestrated re-gate loop end-to-end, and the
Argument concern (F4/F5) on the framing sentences. The mechanisms are unit-tested (each script's `--selftest`);
these widen the *end-to-end* coverage once Phase 2 lands.
