# /write redesign — build plan (the bridge from design to code)

Design is BUILD-READY (`write-redesign-design.html` v1.1, hardened across 4 opus reviews). This is the plan to
implement it: the migration map (the "tags"), the walking-skeleton slice, and the build order. **Principle:**
build the new orchestration + new components *from scratch* in a clean location; **lift** the 9 working scripts
(the DET floor — tested, the reviews' strongest part) rather than rewrite them; **retire the old `/write` flow only
once the new pipeline passes the 119-scenario suite.**

## Session provenance — the build's source-of-truth logs

Two sessions carry the full reasoning behind this build. When a decision or a design choice is unclear, the answer
is in these logs (mine them with a subagent; never re-derive). Project slug: `-home-centcom-data-brain-alignment`.

| Session | Role | Log file |
|---|---|---|
| `3ce96589-47c5-4d6b-ab6b-d2e7b7a85134` | **The redesign** — designed the whole pipeline to BUILD-READY (the *why*: 4 concerns, gated loop, 119 scenarios, CC mapping, D047/D048) | `~/.claude/projects/-home-centcom-data-brain-alignment/3ce96589-47c5-4d6b-ab6b-d2e7b7a85134.jsonl` |
| `1709254b-72c6-40a0-bacd-0d88e900691f` | **First build** — implemented Phase 1 (C1–C8) + P2-A under the per-chunk build→opus-oracle→fresh-`claude -p`-verify→commit loop (the *how*) | `~/.claude/projects/-home-centcom-data-brain-alignment/1709254b-72c6-40a0-bacd-0d88e900691f.jsonl` |

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

## Build method — the per-chunk verification loop (proven across C1–C8 + P2-A; learnings L059–L061)

Each atomic chunk passes **three nets** before its commit, in this order:
1. **Embedded `--selftest`** (the regression net) — every script carries its chunk's scenarios; run green.
2. **Opus oracle review** (the discovery net) — `oracle-reviewer`, run on *every* chunk regardless of selftest
   greenness (every chunk so far had a silent-pass/bypass the selftest missed). Fix every must-fix; **fold the
   oracle's new boundary scenarios into the selftest;** re-run green.
3. **Fresh `claude -p` clean-room verify** — a real subprocess that loads the just-added on-disk artifact, builds
   its OWN fixtures (not `--selftest`), runs the scenarios against EXPECT. **Oracle-first, then this** (L061).

Then an **atomic commit** with a build-log entry below. Mechanics that bit us once each (don't re-hit):
- Set the **Bash tool `timeout` ≥ 540000 ms** for any `claude -p` verify (the 120 s default silently kills it).
- **Export `CLAUDE_WRAP_SNAPSHOT_SKIP=1`** on every verifier child or it clobbers the parent `/wrap` snapshot.
- A fresh `claude -p` **loads** mid-session artifacts; an in-process Agent subagent does **not** — verify with a subprocess.
- **Never HARD-block a dual-use lexical pattern** (L060) — flag it SOFT and let the RUB judge adjudicate.
- **A DET floor binds to ground truth, and fails toward *more* checking on ambiguity** (L059).

## Authority note — the 2d remaps win over the scenario-suite coverage table

`write-redesign-design.html` step **2d** re-mapped which functionality *enforces* several scenarios; the coverage
table in `write-redesign-scenarios.md` still lists the **pre-2d** owner. The 2d mapping is authoritative:
- **SC-STR-06 (width) + SC-STR-07 (CARS-niche)** — table files them under **F6**; enforced by the **F11 structure
  judge, stage-3 site** (F6 is hook-only, can't grade a rubric).
- **SC-HON-06 (frame-blend in prose)** — table files it under **F2**; enforced by the **F5 scope judge, stage-5
  site** (F2 only *sets and gates* the frame; it is not a prose auditor). SC-HON-06 is also RUB, not DET (only a
  lexical "deployment" trigger is the DET sliver).

## Status (live)
**Phase 1 (C1–C8) ✅ + Phase 2 P2-A ✅** (green; recorded S35→S36, see the two session logs above). **P2-B in
progress** (F1 reader-model · F2 message&frame · F11 structure judge). Then P2-C, P2-D, P3 (cutover, irreversible —
explicit go required). Per-chunk decisions recorded in the build log below.

## Build log (append-only; durable decisions mined/made during the build)
*Phase 1 + P2-A decisions live in the two session logs (provenance table above) + `docs/learnings.md` L059–L061.
This log starts at P2-B.*

**P2-B-i — stage-1 front-end (F1 reader-model + F2 message&frame).** Built `agents/sw-reader-model.md` (sonnet),
the `frame`/`contribution_type`/`reader_model`-shape schema checks in `lattice_integrity.py`, the SKILL stage-1
section, LATTICE.md schema, both fixture lattices. Three nets green (selftest · opus oracle FIX-THEN-PASS ·
fresh `claude -p` ALL-PASS, SC-RM-1/2 correct). Durable decisions:
- **F1 writes the lattice `reader_model` field, not a separate `reader-model.md` file.** The lattice is the single
  spine artifact (F15); the design's "→ reader-model.md ARTIFACT" is realized as that field. Shape extended from
  `{venue, old, new}` to `{venue, old, new, prior_beliefs, doubts}` (the design's three fields + the seed venue).
- **New top-level lattice fields `frame` (enum `basic-science|technology`) + `contribution_type` (free text).**
  Required & well-formed at stage ≥ 3 (the gate package), optional before — mirroring how `message`/`reader_model`
  are handled (NOT added to the always-required `TOP_KEYS`).
- **F2's "message is one sentence" is NOT a DET check (L060).** A sentence-counter false-positives on
  "Sec."/"U.S."/ellipses; "one sentence" is a stylistic norm, not a ground-truth invariant. The floor only
  asserts the message *exists*; the human gates one-sentence-ness at F16. (Same call as SC-HON-06 → RUB.)
- **Oracle D2 (real append-safe breach, fixed):** the `diff` guard walked only `claims`, so the new content-bearing
  top-level fields could be silently emptied by a stage write (esp. a stage *regression* below 3, which skips the
  validate block). `diff` now guards `message`/`frame`/`contribution_type`/`reader_model` at top level **and**
  `reader_model`'s sub-fields at sub-key granularity.
- Empty *lists* inside `reader_model` (a reader with no NEW terms / no doubts) are legitimately allowed by
  `validate`; only emptying a field that *had* content is an append-safe flag.
