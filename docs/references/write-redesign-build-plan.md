# /write redesign — build plan (the bridge from design to code)

Design is BUILD-READY (`write-redesign-design.html` v1.1, hardened across 4 opus reviews). This is the plan to
implement it: the migration map (the "tags"), the walking-skeleton slice, and the build order. **Principle:**
build the new orchestration + new components *from scratch* in a clean location; **lift** the 9 working scripts
(the DET floor — tested, the reviews' strongest part) rather than rewrite them; **retire the old `/write` flow only
once the new pipeline passes the 119-scenario suite.**

## Migration map — existing apparatus → new design (the tags)

| Existing item | New role | Action |
|---|---|---|
| `scripts/ai_tell_lint.py` | F12 voice DET (lexical tells) | **lift** + tag |
| `scripts/check_evd_resolution.py` · `check_gap_survival.py` · `check_claim_survival.py` | F3 claim-binding / F9a provenance | **lift**, wire to the lattice |
| `scripts/check_number_consistency.py` | F19 consistency (abstract≠body) | **lift** (already does it) |
| `scripts/register_state.py` · `record_register_verdict.py` | F14 Stop-hook + F16 ordering (D047 state machine) | **lift / adapt** |
| `scripts/run_checks.py` | verifier dispatcher → `lattice_integrity` hook | **rewrite / absorb** |
| `.claude/hooks/prose_writecheck.py` | F12 hook wrapper | **keep** |
| `.claude/hooks/honesty_writecheck.py` | F3 hook | **extend** (+ `evidence.status`) |
| `.claude/agents/prose-register-auditor.md` | F12 RUB | **keep** |
| thinking panel (`premortem-analyst`, `counter-argument`, …) | F13 reviewer-premortem | **reuse** |
| `references/provenance-d011.md` | Trust concern rulebook | **keep** |
| `references/writing-style.md` (20KB) | Voice concern rulebook (F8b/F12) | **keep** |
| `references/review-pass.md` | audit philosophy (F9b–F13) | **keep / adapt** |
| `references/latex-conventions.md` + `assets/` | output formatting | **keep** |
| `SKILL.md` body ("path-select → draft → full-loop → ship-gate") | the staged gated-loop spine orchestrator | **rewrite from scratch** |
| — (none today) | `claim-lattice.json` (F15) · reader-model (F1) · message&frame (F2) · argument-validity judge (F4) · scope judge (F5) · acknowledgment (F18) · skeleton+figures (F6/F7) · drafter-emits-\evd (F8a) · voice-realize (F8b) · structure judge (F11) · consistency subagent (F19) · exemplar set (F17) · `lattice_integrity` hook · convergence Stop-hook · gate (AskUserQuestion/ExitPlanMode) | **build new** |

## Build order

**Phase 1 — Walking skeleton (validate the architecture on ONE case).**
Build the minimum vertical slice through the whole spine, reusing the lifted scripts:
`claim-lattice.json` schema (F15) → claim-binding (F3, lift honesty + evd checks) → a minimal skeleton (F6) →
drafter emitting `\evd` (F8a) → two audits (F12 voice [lift] + F9a/F9b fidelity) → gate (F16).
**Run it on the abstract** (a case we know — it was hand-cleaned this arc). **Acceptance:** catches Claudio's
class (SC-VOICE-01–04), passes the near-misses (SC-VOICE-12/13), every claim is `\evd`-bound. If the skeleton
makes trustworthy prose on one case, expand; if not, we learn it cheap.

**Phase 2 — Full concern coverage.** Add the argument front-end + the rest of the audits:
F4/F5 (argument + scope judges, xhigh, 2 sites) · F11 (structure, 2 sites) · F18 (acknowledgment) · F13 (panel
wiring) · F19 (consistency) · F1 (reader-model) · F2 (message&frame) · F7 (figures) · F17 (exemplar set).
Wire the **CC-power upgrades**: parallel stage-5 audits · structured-output verdicts (`ready_to_ship: bool`) ·
the Stop-hook convergence · the gate via AskUserQuestion.

**Phase 3 — Cutover.** Run the full 119-scenario suite. When green: retire the old `SKILL.md` flow, update
`CLAUDE.md` + `docs/03-methodology.md` to point at the new pipeline, record the decision.

## Effort / model (set)
HIGH for all subagents; **XHIGH for F4 (argument), F5 (scope), F11 (structure)**. opus for argument/scope/draft,
sonnet for structure/voice. (Erfan-approved.)

## Status
Plan recorded. Not yet started. Resume: Phase 1 walking skeleton. Full design + scenarios + mapping in the
sibling `write-redesign-*` docs.
