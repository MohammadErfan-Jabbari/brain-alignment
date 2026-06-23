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
**Phase 1 (C1–C8) ✅ + Phase 2 P2-A ✅ + P2-B ✅ + P2-C ✅** (green; P1+P2-A recorded S35→S36, P2-B + P2-C this
session — see the two session logs above + the build log below). **P2-D next** — the CC-power upgrades: parallel
stage-5 fan-out · structured `ready_to_ship` Stop-hook convergence · AskUserQuestion gate. Then P3 (cutover,
irreversible — explicit go required). Per-chunk decisions recorded in the build log below.

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

**P2-B-ii — F11 structure judge (2 sites).** Built `agents/sw-structure-judge.md` (sonnet, xhigh), one judge at
two sites; wired into SKILL stage-3 + stage-5. No new DET script (the structure coverage floor — orphan-claim,
empty-section — already lives in `lattice_integrity`; width/CARS/point-sentence are all RUB). Three nets green
(selftest floor intact · opus oracle FIX-THEN-PASS · fresh `claude -p` **8/8**, incl. all precision near-misses
NOT flagged). Durable decisions:
- **Stage-3 site:** width = Schimel opening=resolution, **counted by claim-ID** (a contribution = a distinct
  claim-ID in the opening; "resolved" = that claim-ID discussed *with its result* in the discussion, not merely
  re-named) + CARS niche (Move-2 present). **Stage-5 site:** point-sentence, old→new *relative to the
  reader-model*, CCC.
- **Oracle D1 (the load-bearing fix):** the stage-5 judge needs `reader_model` to judge old→new, but the contract
  said "the lattice is NOT your input" — telling a literal judge to ignore the one field it needs (SC-STR-12 would
  silently pass). Fixed: it reads `reader_model` from the lattice; **if absent/empty it flags old→new as
  *unjudgeable*, never silent-pass** (mirrors F4's grounding-unverifiable rule). SKILL stage-5 spawn now names the
  `reader_model` input explicitly.
- **Oracle D3 (arc vs register):** added the operational test — *judge the order of ideas, never the diction*; a
  sound problem→resolution arc is CLEAN even if the wording is dramatized (dramatization is F12's flag). Stops F11
  double-flagging an arc that co-occurs with a register tell.
- **Stale-doc fix:** re-tagged the scenario suite — SC-STR-06/07 `F6 → F11`, SC-HON-06 `F2 → F5` (table + inline) —
  so a P3 suite-runner routes them to the judge that enforces them, not the hook.
- Wired F4/F5 (P2-A) into the SKILL stage-5 reader list too — the orchestrator narrative had lagged P2-A.

**P2-C-1 — case-completeness layer (F7 figures + F13 premortem panel + F18 acknowledgment).** Built
`agents/sw-acknowledgment.md` (F18, opus); wired F7 (stage-3 figure planning — the `central-claim-figure` DET
already exists), F13 (stage-5 — reuses the D017 `premortem-analyst` + `counter-argument`), F18 (stage-2 plan +
stage-5 re-check) into SKILL. No new DET/schema (`acknowledgments`/`figures` are existing lattice fields). Three
nets green (floor selftest · opus oracle FIX-THEN-PASS · fresh `claude -p` **9/9**). Durable decisions:
- **"Defended claim" pinned to a predicate:** *bound* (`bound_experiment != null`) AND `strength ∈
  {observed,supported,strong}` (an `unsupported`/`\gap` claim gets a gap, not a limitation). Was undefined →
  F18 would over-pad (every claim) or miss (defended non-central). **F18 covers defended NON-central claims too**
  — coverage is not limited to `is_central`.
- **The SC-ARG-12 line (load-bearing):** a future-work pointer is an acknowledgment only **as a tail on** a named
  present limitation, never **as a substitute** for naming it ("unproven but TRIBE fixes it" → flag; "limited
  because <mechanism>; future work may improve it" → clean).
- **F18 is a two-pass agent (made explicit in the agent, oracle D2):** stage-2 plans limitations from
  claims+scope (no premortem objections exist yet); stage-5 re-checks against the F13 objections.
- **Oracle D3 (the real enforcement gap):** the shared panel agents (`premortem-analyst`/`counter-argument`)
  emit a fixed `PANEL-VERDICT` format with **no `claim_id` slot**, so "each objection names its claim" can't be a
  prose ask layered on them. The **orchestrator** maps each returned objection to the `claim_id` it threatens and
  **flags an unmapped objection (SC-ARG-5) rather than passing it to F18** — added as a SKILL stage-5 adapter
  step; the shared agents are left untouched.
- F7 reuses the existing `central-claim-figure` DET (dormant at stage 3, mandatory at stage ≥ 4); no new script.

**P2-C-2a — voice-delivery pair (F17 exemplar pin + F8b voice-realize).** Built `references/F17-exemplars.md`
(per-section anchors lifted from the scenarios `SC-EX-*` set — no re-mine), the lattice `register` field + a
stage-≥4 `no-exemplar-pin` DET (SC-VOICE-10), and `agents/sw-voice-realize.md` (F8b, sonnet, an edits-in-place
generator). Three nets green (selftest · opus oracle FIX-THEN-PASS · fresh `claude -p` ALL-PASS). Durable decisions:
- **F8b is voice-only and its invariants are now MECHANICALLY floored** (oracle D1, the load-bearing fix): it
  must change no number / drop no `\evd` tag / drop no `%%SECTION` marker. Tags+markers were already caught by the
  post-F8b `draft_check`/`lattice_integrity` re-run; **numbers were honor-system only** — a silently-altered result
  number passed every check. Added a **number-conservation DET**: `draft_check --prev-prose` asserts the
  numeric-literal multiset is identical before/after (wired through `run_checks --prev-prose`). This is the prose
  analog of the lattice append-safe diff.
- **`register` is a stage-1 voice output** (`{venue, exemplars}`), required a *non-empty list* at stage ≥ 4 — the
  voice pass cannot run without a pinned exemplar set. Tightened from a shallow `_empty` check (oracle D2: `[""]`
  and a string-not-list slipped through at the gate) to `isinstance(list) and _has_content`.
- **Oracle S1 (a gap P2-B-i opened):** the gate-package hash (`gate_state._projection`) omitted `frame`,
  `contribution_type`, and `register`, so a post-approval change to any wouldn't re-fire the gate. Added all three
  to the projection — now consistent with `message`/`reader_model` (a stage-1 case/plan change re-enters the gate).
- F17 anchors carry the "from a good paper ≠ passes our rules" caution + the danger-zone (abstract/discussion)
  weighting; the full graded corpus stays the `SC-EX-*`/`SC-VIO-*` set in scenarios.md.

**P2-C-2b — F19 consistency.** Built `scripts/consistency_check.py` (DET): abstract↔body result-number match +
no full CI in the abstract (SC-XS-1/2), wired into `run_checks --prose`. caption ≤ figure (SC-XS-3) is **deferred**
— it is RUB and the lattice carries no caption text (figures are `{figure_id, claim_id}`). Three nets green
(selftest · opus oracle FIX-THEN-PASS · fresh `claude -p` 6/6). Durable decisions:
- **Oracle D1 (FATAL as first built — the L060 failure):** a verbatim *all-numbers* abstract↔body match
  over-blocks on the first abstract that names a model (`Qwen2.5-0.5B` → `2.5`/`0.5`) or cites a year (`2024`) —
  the first real use would disable the check. The estimand is "did the abstract invent a *result*," so the fix
  (the oracle's option b) restricts the comparison to **RESULT numbers**: a decimal, not part of an identifier
  (lookbehind/lookahead exclude `Qwen2.5`/`0.5B`/version `2.5.3`), not a bare integer (year/count), with a
  leading `+` normalized. A sentence-final number (`+0.028.`) still matches (the version-guard allows a trailing
  period). **Residual (documented):** a rounded abstract decimal differing from the body still flags; a bare
  bracket interval with no "CI" label is a known recall miss (the labeled `95% CI` form is caught).
- **Oracle D2:** `NUM_RE` captured a trailing comma (`2024,` ≠ `2024`) — also a **latent bug in the committed
  `draft_check.check_numbers`** (a number moved to a clause boundary would false-flag drift). Fixed the thousands
  group in both (`(?:,\d{3})*`).
- **Oracle C2:** the abstract section is matched **exactly** (`== "abstract"`), not by substring, so
  `abstract-of-results` is not mistaken for the abstract.
- **C3 (noted, not done):** `consistency_check` and `draft_check` duplicate the LaTeX/number primitives
  (`strip_tex_comments`, `SEC_RE`, `EVD_RE`); behaviorally consistent now, a shared module would prevent future
  drift — a bounded future cleanup.

**P2-C complete** (C-1 + C-2a + C-2b). Phase 2 remaining: **P2-D** (parallel stage-5 fan-out, structured
`ready_to_ship` Stop-hook convergence, AskUserQuestion gate). Then P3 cutover (irreversible — explicit go).
