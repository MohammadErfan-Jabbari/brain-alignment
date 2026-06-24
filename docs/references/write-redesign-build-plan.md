# /write redesign — build plan (the bridge from design to code)

Design is BUILD-READY (`write-redesign-design.html` v1.1, hardened across 4 opus reviews). This is the plan to
implement it: the migration map (the "tags"), the walking-skeleton slice, and the build order. **Principle:**
build the new orchestration + new components *from scratch* in a clean location; **lift** the 9 working scripts
(the DET floor — tested, the reviews' strongest part) rather than rewrite them; **retire the old `/write` flow only
once the new pipeline passes the 119-scenario suite.**

## Session provenance — the build's source-of-truth logs

Four sessions carry the full reasoning behind this build. When a decision or a design choice is unclear, the answer
is in these logs (mine them with a subagent; never re-derive). Project slug: `-home-centcom-data-brain-alignment`.
These logs are the **related documents** of the redesign + rebuild — read them before continuing the build.

| Session | Role | Log file |
|---|---|---|
| `3ce96589-47c5-4d6b-ab6b-d2e7b7a85134` | **The redesign** — designed the whole pipeline to BUILD-READY (the *why*: 4 concerns, gated loop, 119 scenarios, CC mapping, D047/D048) | `~/.claude/projects/-home-centcom-data-brain-alignment/3ce96589-47c5-4d6b-ab6b-d2e7b7a85134.jsonl` (4.0M) |
| `1709254b-72c6-40a0-bacd-0d88e900691f` | **First build** (S35→S36) — implemented Phase 1 (C1–C8) + P2-A under the per-chunk build→opus-oracle→fresh-`claude -p`-verify→commit loop (the *how*) | `~/.claude/projects/-home-centcom-data-brain-alignment/1709254b-72c6-40a0-bacd-0d88e900691f.jsonl` (4.7M) |
| `daa4f842-64ac-43c3-b9e4-653f4acf7317` | **Second build** (S37) — implemented P2-B (F1/F2/F11) + P2-C (F7/F13/F18/F17/F8b/F19) under the same three-net loop; 7 atomic commits + the build log below | `~/.claude/projects/-home-centcom-data-brain-alignment/daa4f842-64ac-43c3-b9e4-653f4acf7317.jsonl` (3.4M) |
| `1b3b0846-9914-45ab-9ccf-b9d70bdecd10` | **Third build (S38)** — completed **P2-D** (D-1..D-6: convergence machine, parallel fan-out, the live Stop-hook, AskUserQuestion gate, SC-XS-3, fluidity/deviation-log) **+ P2-E** (authoring/quality review vs `writing-great-skills` + official CC docs: SKILL de-sediment, agent fixes, effort frontmatter fleet-wide). 11 commits. **Phase 2 complete; next = P3.** | `~/.claude/projects/-home-centcom-data-brain-alignment/1b3b0846-9914-45ab-9ccf-b9d70bdecd10.jsonl` |

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
**Phase 1 (C1–C8) ✅ + Phase 2 P2-A ✅ + P2-B ✅ + P2-C ✅ + P2-D ✅ (1..6) + P2-E ✅ (authoring review)** —
**PHASE 2 COMPLETE.** **NEXT = the cross-stance handoff build (X1–X4, D050, BUILD-READY — see the
section below + `write-redesign-xstance.md`) then P3 cutover (next session, Erfan drives — IRREVERSIBLE).**
(P1+P2-A S35→S36, P2-B + P2-C S37, P2-D + P2-E S38 — see the session logs above + the build log below.)
The CC-power upgrades, chunked: **P2-D-1 ✅** structured verdict schema + convergence state machine
(`verdicts.py`); **P2-D-2 ✅** parallel stage-5 fan-out + verdict-recording orchestration (SKILL stage 5);
**P2-D-3 ✅** the convergence Stop-hook (`stop_sw_converge.py`, wired live, pipeline+session-scoped, loop-guarded);
**P2-D-4 ✅** the F16 gate via `AskUserQuestion`; **P2-D-5 ✅** SC-XS-3 caption ≤ figure (folded into F5 +
`caption`/`shows`); **P2-D-6 ✅** fluidity/deviation-log enforcement (SC-PROC-8/9/10/11). **NEXT = P3 cutover**
(run the full 119-scenario suite → retire the old flow → repoint CLAUDE.md + 03-methodology → record
D048-complete) — **IRREVERSIBLE, explicit go from Erfan required.** Per-chunk decisions in the build log below.

## Cross-stance handoff (D050) — BUILD-READY addition, builds next session alongside P3

A dry-run (S39) proved a structural gap: when a stage-5 reader finds a defect the prose **cannot** fix
because it lives in the evidence/argument substrate (the E006 voxel-bootstrap CI the F13 panel caught),
the pipeline has no path to route it to the owning stance — it would either dump it on the human or
(worse) paper over it by rewording with an unrecorded number. The fix — a **cross-stance handoff**
orchestration function (detect → classify → emit handoff → block stickily → recommend the stance; never
auto-spawn, never adopt a number) — is designed to BUILD-READY in **`write-redesign-xstance.md`** (hardened
across 4 opus reviews). **Four build chunks, same three-net loop, dependency order X1→X4:**
- **X1** — `evidence_status: suspect` at all four sites (`lattice_integrity.EVIDENCE_STATUS`,
  `claim_binding.STALE` + `check_register`, `LATTICE.md`, register).
- **X2** — `verdicts.py`: the `handoffs.json` store + `handoff open/resolve/status/check --lattice` + the
  `handoffs-open` clause in `status()` + the `ship`/`accept-residual` refusal + no-op-when-missing selftest.
- **X3** — SKILL **stage-5.5 triage**: reader self-tag, the M3 backstop force-rule, the handoff emit +
  human surface, the two-gate rebind contract.
- **X4** — wire the anchor (SC-XSTANCE-01 = the dry-run) end-to-end; fold the 16 `SC-XSTANCE-*` into the
  suite (119 → 135).

This should land **before** P3 cutover so the cutover does not freeze a system with this known gap.

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

**P2-D-1 — structured verdict schema + the convergence state machine.** Built `scripts/verdicts.py` (the
stage-5 convergence aggregator) and unified all seven stage-5 readers on one machine line:
`<TAG>-VERDICT: {"ready_to_ship": <bool>, "findings": <int>}` (F12 voice was `REGISTER-CLEAN:`, F9b fidelity was
`FIDELITY-CLEAN:` — both converted; F4/F5/F11/F18 already emitted it). Three nets green (selftest 30 checks ·
opus oracle ACCEPT-WITH-CAVEAT, MF-2 fixed + B1–B8 folded · black-box CLI verify, independent fixtures). Durable
decisions:
- **`verdicts.py` is the DRAFT-side twin of `gate_state.py`** (the lattice-side F16 gate): same D047
  content-hash pattern, same `.claude/state/sw-gate/` store, same TRUSTED-not-verified model. Convergence is
  keyed to the **prose content hash** — verdicts live under `.../verdicts/<prose-hash>/<reader>.json`, so a
  one-byte draft edit makes every prior verdict stale (its hash no longer matches) → re-block. `record` files
  one reader's verdict; `status` is converged iff every required reader is present for the current hash AND all
  `ready_to_ship`. The Stop-hook (P2-D-3) calls `status`.
- **Required reader set = 7** (`argument F4 · scope F5 · fidelity F9b · structure F11 · voice F12 · premortem F13
  · acknowledgment F18`) — matches SKILL.md's stage-5 fan-out (which ends at F18). **F19 is NOT a reader** (its
  DET half runs in `run_checks`; its only RUB half, caption ≤ figure, is SC-XS-3, a KNOWN coverage hole owned by
  **P2-D-5**, not silently absorbed). (Oracle MF-3: my first docstring misremembered the spec as ending at F19 —
  corrected.)
- **`findings` = unresolved BLOCKING findings, so `ready_to_ship: true` requires `findings: 0`.** A
  `{ready_to_ship: true, findings: >0}` verdict is self-contradictory → treated **not ready** (oracle MF-2, the
  one place a *false* converged could pass). Fail-safe everywhere (L059): missing / unparseable / non-dict /
  contradiction all → not converged, never a silent pass.
- **`premortem` (F13) has no agent verdict line** — the shared D017 panel emits `PANEL-VERDICT:` with no
  `ready_to_ship` slot. The **orchestrator synthesizes** the premortem verdict (rule written into `verdicts.py`:
  ready := counter-argument SURVIVES ∧ every objection mapped to a claim — an unmapped objection is SC-ARG-5).
  **Verifying that synthesis came from a FRESH panel run (not a hand-typed boolean) is P2-D-3's hard
  requirement** — the freshness control D047 names; without it the store is fabricable in one turn (oracle's
  load-bearing residual, carried forward).
- **`--repo-root` moved onto the subcommands** (pass it after `record`/`status`); production falls back to
  `$CLAUDE_PROJECT_DIR`. A top-level-only flag was rejected by argparse after the subcommand — a footgun for the
  machine callers (hook/orchestrator). Tag-remapping in `lattice.tags[]` without a prose-byte change is out of
  scope here (owned by the stage-write round-trip diff `run_checks --prev`; oracle MF-4, documented).

**P2-D-2 — parallel stage-5 fan-out + verdict-recording orchestration.** Rewrote SKILL.md stage 5 (no new
script — drives `verdicts.py` from P2-D-1). Three nets green (run_checks + verdicts selftests · opus oracle
ACCEPT-WITH-CAVEAT, M1–M4 fixed · fresh `claude -p` **5/5 PASS** incl. the three load-bearing boundaries). Durable
decisions:
- **The fan-out:** the orchestrator spawns **seven subagents in ONE message** — F4 `sw-argument-judge`, F5
  `sw-scope-judge`, F9b `sw-claim-fidelity-judge`, F11 `sw-structure-judge`, F12 `sw-voice-auditor`, and the F13
  panel (`premortem-analyst` + `counter-argument`). **F18 `sw-acknowledgment` runs AFTER the batch** (it consumes
  F13's mapped objections, so it cannot be in the parallel message — else its ACK verdict is vacuous).
- **The premortem synthesis rule is now ternary-correct (oracle M1, the load-bearing fix)** and **duplicated
  verbatim in SKILL.md and `verdicts.py`'s docstring** (kept in lockstep; the fresh session confirmed MATCH).
  `counter-argument` emits `SURVIVES | SURVIVES-IF-NARROWED | DOES-NOT-SURVIVE`; **only bare `SURVIVES` is
  ready** — `SURVIVES-IF-NARROWED` is NOT ready (it was unstated before, computable two ways). `objections` =
  counter-argument's + **premortem-analyst's TOP-RISK folded in** (M3 — else a standalone risk is invisible to
  convergence). `findings = (# unmapped) + (1 if status != SURVIVES)` so it is **never 0 when not-ready** (M2).
- **The `acknowledgment` convergence verdict MUST be F18's stage-5 re-run** (consuming the mapped objections),
  never the vacuous stage-2 plan (oracle M4 — both write `acknowledgment.json` under the same hash; a future
  freshness stamp in P2-D-3 will enforce it mechanically).
- **One canonical draft path** (oracle Q3 residual): all record + status calls use the **F8b voice-realize
  output** (not the F8a pre-voice draft, which also exists on disk). The hash-keying surfaces a wrong-path record
  as `[missing]`, but the real fix — the **Stop-hook reading `meta.draft_path` from the lattice** so no
  orchestrator-supplied path is trusted — is **P2-D-3**.
- **Honest scoping (explicit in SKILL):** P2-D-2 is the verdict-recording **bookkeeping**; the *enforcement* (no
  stale/wrong-draft verdicts; convergence is mandatory) is **P2-D-3**. Provenance (no *fabricated* booleans) is a
  named accepted non-goal — the store is trusted, like `gate_state`/`stop_register_gate`.

**P2-D-3 — the convergence Stop-hook.** Built `.claude/hooks/stop_sw_converge.py` + the gate-state ops in
`verdicts.py` (`activate`/`ship`/`accept-residual`/`session_matches`/`clear_gate_state`) + wired the hook live in
`settings.json` (alongside `stop_register_gate.py`). Three nets green (verdicts selftest incl. 6 `session_matches`
+ 5 `clear_gate_state` cases · opus oracle: **first pass REJECT → fixed → re-review ACCEPT-WITH-CAVEAT, FATAL
cleared** · hook event-pipe black-box, all catastrophe + policy cases). Durable decisions:
- **Pipeline-scoped + session-scoped, fail-INERT:** the hook does nothing unless `.claude/state/sw-gate/active.json`
  exists (orchestrator writes it at stage 4 via `verdicts.py activate`, clears it at `ship`). So it never blocks
  an unrelated session. `active.json` also pins the **one canonical draft** (the F8b output) — the hook trusts
  that, not a per-call arg (closes the F8a-vs-F8b wrong-draft seam, oracle P2-D-2 Q3).
- **THE catastrophe the first oracle pass caught (REJECT → fixed):** the session guard must **fail toward
  release/disarm on ANY session-identity uncertainty** — a wrongly-blocked unrelated session is a repo-wide
  outage. `session_matches(armed, event)` is True only when both ids are present and equal; the hook disarms only
  on a **confirmed truthy mismatch** (abandoned session) and on a **transient missing event id releases WITHOUT
  disarming** (one dropped id must not permanently kill a legit run). Six unit-tested cases pin it.
- **Session-id value space VERIFIED** (the oracle's KILL risk): `CLAUDE_CODE_SESSION_ID` (stamped at `activate`)
  == the transcript filename == the Stop event's `session_id` — so the owner's happy path does not spuriously
  disarm. If a future CC build diverges them, the hook degrades to a **no-op** (fail-safe, never blocks a
  stranger) — documented in `verdicts.py`; re-verify on a CC bump.
- **Loop guard:** `MAX_BLOCKS=3` per draft hash via `bump_block`, then escalate to Erfan (stderr) + release —
  never trap. An edit changes the hash → fresh count. Escapes: Erfan-logged `accept-residual` (hash-keyed),
  `stop_hook_active` re-entrancy, import failure → `sys.exit(0)`.
- **Honest scope (matches the code, not over-claimed):** the hook enforces **staleness + convergence**, NOT
  provenance — a hand-typed verdict is indistinguishable from a real one (accepted non-goal, same trust model as
  the two sibling hooks). And per CC's `stop_hook_active` re-entrancy the practical effect is a **strong nudge per
  work-stretch + the MAX_BLOCKS backstop, with Erfan's sign-off the final gate** — not an inescapable wall. SKILL
  prose reconciled to say exactly this (the "terminator"/"anti-fabrication" overclaims were removed).
- **`ship` clears the gate state** (active/blocks/residual/verdicts) but preserves `approvals.json` (gate_state's
  F16 store in the same dir) — bounds state growth + kills the stale-residual-on-collision surface (oracle MF-4).

**P2-D-4 — the F16 gate via `AskUserQuestion`.** SKILL-only (the `gate_state.py` floor is built + tested,
unchanged). Rewrote the **GATE · F16** section to use the real `AskUserQuestion` approval primitive. Three nets
green (gate_state selftest intact · opus oracle ACCEPT-WITH-CAVEAT, MF-1..3 + boundary fixed · fresh `claude -p`
**5/5 PASS**). Durable decisions:
- **The presented package == the hashed projection, exactly** (oracle MF-1, load-bearing): the human must approve
  every field `gate_state._projection` hashes — so the GATE summary now lists **register (F17 exemplars)**
  alongside message/frame/contribution_type/reader-model/claims(+scope+is_central+acks)/warrants/skeleton/figures.
  A field that is gated but not shown = a silent term in a contract the human signs. Fixed.
- **The `Approve` trigger is a literal exact-match** (oracle MF-3): only an exact selection of the option labelled
  `Approve` authorizes `gate_state approve`; the agent's own read, a paraphrase, any other selection, or a
  **cancelled/unanswered dialog** is NOT approval → loop back to stages 1–3 and re-present (closes the
  self-approval seam + the dismissed-dialog boundary).
- **Revise options must cover the full gated set** (oracle MF-2): derive them from the package fields so no field
  is un-revisable (a human can't be forced to Approve to change a field the options omit).
- **`AskUserQuestion` over `ExitPlanMode`:** it returns a discrete decision token; ExitPlanMode conflates
  "plan is fine" with "approve this exact package." `AskUserQuestion` makes the yes unambiguous; enforcement still
  belongs to the `gate_state check` floor (the gate primitive doesn't enforce ordering — the hook does).
- **Stage-6 re-gate enumeration generalized** to "any gated field" (was a 4-field list, which an agent could read
  as exempting frame/register/reader-model) — consistent with `_projection`.

**P2-D-5 — SC-XS-3 caption ≤ figure, folded into F5.** Added a `caption` + **`shows`** field to the lattice
figure object and extended the **F5 scope judge** to size each caption against `shows` (re-tag F19→F5). No 8th
subagent, no required-set growth — SC-XS-3 rides F5's `SCOPE-VERDICT` (already a convergence reader). Three nets
green (DET floor selftest · example validates · opus oracle ACCEPT-WITH-CAVEAT, MF-1 fixed · fresh `claude -p`
3/3). Durable decisions:
- **The fold is sound because caption-over-claim IS a scope question** — same axis F5 already judges, so a
  dedicated judge would be redundant. SC-XS-3 rides `scope`'s verdict; the convergence set stays 7.
- **The load-bearing oracle fix (MF-1):** SC-XS-3 is caption ≤ **what the figure PLOTS**, not caption ≤ the
  **bound claim's scope** — they diverge exactly in the SC-XS-3 case (a broad *true* claim, a figure showing a
  subset, a caption that generalizes). My first cut operationalized it as ≤ bound-claim and would have **missed
  the scenario**. Fixed by the **`shows`** field (what the figure actually displays) as the reference: F5 judges
  `caption ≤ shows`, flagging a generalization past a partial-view figure **even when the bound claim is true and
  broader**. (No new scenario needed — SC-XS-3 *is* the partial-view case once `shows` exists.)
- **Verdict rule extended** (oracle MF-2): F5's `ready_to_ship` is false iff any claim's **or figure-caption's**
  scope exceeds evidence — so a caption-only over-claim provably flips the verdict.
- **Missing-caption is out of SC-XS-3 scope** (oracle MF-3, decided): a figure with no `caption`/`shows` has
  nothing to judge on this axis (not a flag); `lattice_integrity` stays permissive (no caption-presence DET) —
  the prose `\caption` is what F5 ultimately reads, sized against `shows`.
- Killed the now-stale "caption is a coverage hole owned by P2-D-5" comments in `verdicts.py` + `consistency_check.py`.

**P2-D-6 — fluidity / deviation-log enforcement (SC-PROC-8/9/10/11).** The "fluid, never silent" layer. Built
the **F11 enforce clause** (a *silent* template force-fit in the work it judges → FLAG; a *logged* deviation is
the clean escape) + a **`deviation_log` well-formedness DET** in `lattice_integrity`. Three nets green (selftest
incl. 5 dev-log cases · opus oracle ACCEPT-WITH-CAVEAT, 3 fixes · fresh `claude -p` 5/5). Durable decisions:
- **SC-PROC-11 (a `\gap`-skip via "fluidity") is ALREADY the rigid DET floor** — `claim_binding` flags `[unbound]`
  for a claim with no bound evidence and no `\gap`; an agent cannot argue past a hook. No new code. (Caveat,
  honestly scoped: this is closed only for sentences *entered as claims* — the known framing-sentence prose→lattice
  escape, SKILL honest-limits, is the separate Phase-2 residual, NOT closed here.)
- **SC-PROC-8/9/10 (silent force-fit) ride F11's STRUCTURE-VERDICT** (already a convergence reader): F11 flags a
  section that silently force-fits a non-fitting template (CARS-on-Methods, OCAR-on-a-null, a silent invented
  hybrid). The flag is for the **silence**, not the deviation.
- **"Logged" is now mechanically real** (oracle MF-1): the DET requires non-**blank** `{functionality, method,
  why, did}` (uses `_has_content`, which strips — a whitespace-only field no longer counts as logged).
- **A logged deviation excuses ONLY the misfit it names** (oracle MF-2, the over-broad-escape hole): added an
  optional `section_id` to the entry + an F11 clause that a force-fit not covered by a matching entry still FLAGs
  — one generic entry can't wave through every misfit.
- **Scope stated (oracle MF-3):** F11 enforces no-silent-force-fit for **structure** templates only; a Voice or
  Argument default force-fit is out of its lane (rests on the SKILL fluidity discipline + the human gate).

**P2-D COMPLETE (1..6).** Phase 2 is done. Next is **P3 cutover** (full 119-suite → retire old flow → repoint
docs → record D048-complete) — IRREVERSIBLE, explicit Erfan go required.

**P2-E — authoring/quality review (S38, gated BEFORE P3 so the components are clean before they become the
default).** Three reviewers fanned out, each against its proper authority; fixes applied as the single writer.
- **SKILL + 3 references vs `writing-great-skills`** (`75d37ac`): the skill had accumulated **build-process
  sediment** over four append-edit sessions that duplicated this build-plan (single-source-of-truth violation)
  and went stale each chunk. Cut the build-chronology back-third + every inline `P2-x`/Phase tag; rewrote the
  frontmatter description (11→6 lines, triggers + reach clause). **263 → 206 lines.** 3 references clean.
- **9 `sw-*` agents vs official CC sub-agent docs** (`8235a1a`): `sw-voice-realize` dropped `Write` (contradicted
  its in-place preservation contract → Read, Edit, Bash); `sw-acknowledgment` + `sw-claim-fidelity-judge`
  descriptions reconciled (claimed "never touches a verdict" but emit ACK-/FIDELITY-VERDICT); verdict-key
  placeholder unified `<n>`→`<int>`. Kept `Bash` on read-only judges (read-only by contract; several shell out).
- **`stop_sw_converge.py` + settings vs official CC hook docs:** **fully compliant, fit to ship** — no changes
  (JSON `{decision:block}` + `stop_hook_active` handling match the current spec; fail-safe; cheap no-op path).
- **Effort frontmatter adopted FLEET-WIDE** (`7d60063`, Erfan-approved, D049): all 24 agents declare `effort:` —
  **xhigh** for F4/F5/F11 (the real fix: they were silently inheriting session `high` despite their descriptions
  promising xhigh), **high** for the rest (= current session effort, now explicit/self-contained). CLAUDE.md
  routing note updated to document the convention.
- **`${CLAUDE_PROJECT_DIR}` brace form** (`4114c8f`, Erfan-approved): uniform across all 6 hook commands
  (doc-canonical; functionally identical here).
- **Open for P3 (flagged, not built):** the 119-suite has no **RUB-grading harness / pass-threshold** for the
  ~41 RUB scenarios and no named sign-off mechanic beyond "Erfan signs" — define this at P3 start. The
  framing-sentence prose→lattice escape stays the known Phase-2 residual.

**P2-D + P2-E COMPLETE — Phase 2 done. P3 is the next session (Erfan drives; IRREVERSIBLE).**

---

### Cross-stance handoff build (D050, X1–X4, S40) — three-net loop per chunk

**X1 — `evidence_status: suspect` at all four sites.** Added the new enum value (distinct from
demoted/superseded: no later verdict overruled it, but a `/write` reader doubts it; set by
`/interpret`→`/work`+Erfan, never by `/write`). Sites: `lattice_integrity.EVIDENCE_STATUS` (schema-valid),
`claim_binding.STALE` (suspect ∈ STALE → cite-as-live fires `[stale-evidence]`+`[status-mismatch]`),
`claim_binding.check_register` resolve-tuple (a recorded suspect key must resolve on disk like live/demoted),
`LATTICE.md` (row + Enums gloss), `evidence-register.json` `_meta` (`status_values` + gloss). Three nets green
(both selftests · opus oracle **PASS** first pass — only a comment-clarity nice-to-have, applied · fresh
`claude -p` ALL-PASS on 6 independent fixtures). Durable decisions:
- **`suspect` joins `STALE`, it is not a fourth branch.** A suspect result reuses the demoted/superseded
  "not citable as live" path — same over-claim, so the existing `[stale-evidence]`+`[status-mismatch]` flags
  carry it with no new code path. A suspect-labeled-suspect claim still fires `[stale-evidence]` (a reader
  cannot self-clear a suspect by stamping the claim suspect) but correctly suppresses the false mismatch.
- **`check_register` requires a suspect key to resolve on disk** (unlike fileless-OK `superseded`): suspect is a
  real recorded status with a file. A fileless suspect is an anomaly the reconciler catches as `[register-orphan]`,
  NOT duplicated in `check()` as `[dangling-cite]` (the stale-path already flags the binding loudly). Comment at
  `claim_binding.py:82-89` updated to say this honestly (oracle nice-to-have).
- **No other enum-switch site existed** (oracle grep): `gate_state.py` only projects the key for change-detection,
  never validates the value; no hardcoded `{live,demoted,superseded}` set survives anywhere that would reject suspect.

**X2 — `verdicts.py` handoff store + the sticky `handoffs-open` blocker.** ONE store
`.claude/state/sw-gate/handoffs.json` keyed by `handoff_id`; `handoff open/resolve/status/check --lattice`
subcommands; the `handoffs-open` clause in `status()` (read independently of the prose hash); `ship`/`accept-residual`
refuse past an open handoff (MF-A); `clear_gate_state` now clears `handoffs.json`. Three nets green (selftest 23
new asserts · opus oracle **FIX-THEN-PASS** · fresh `claude -p` 7/7 integration PASS incl. the M1 reword test).
Durable decisions:
- **The M1 keystone is hash-independence.** The blocker is a `status()` CLAUSE, **NOT** an 8th `REQUIRED` reader —
  adding it to `REQUIRED` would re-key it to the prose hash and a reword could clear a substrate defect. Verified:
  reword + re-record all 7 readers ready → still blocked; only `handoff resolve` (the upstream stance recording its
  output) clears it. The two gates are independent (MF2): clearing the handoff ≠ converged; the readers must re-run.
- **Fail toward blocking, everywhere (L059).** `_load_handoffs` returns `{}` ONLY for a truly absent file (the
  no-op invariant: every pre-X2 draft converges byte-identically); a corrupt/non-dict store returns `None` →
  `status()` blocks. `_is_resolved` requires the exact `status == "resolved"` — `"Resolved"`, a trailing space,
  `True`, missing, or junk all stay open. A missing/junk status can never authorize convergence.
- **MF-A is enforced in code, at the CLI dispatch layer** (the right layer — the internal `clear_gate_state`/
  `accept_residual` are only reached *after* the guard). Both `ship` and `accept-residual` exit nonzero listing the
  open handoff; a handoff is not a residual the human may wave through — only its upstream stance closes it.
- **Oracle MUST-FIX (applied):** `resolve_handoff` raw-crashed (`TypeError`) on a corrupt non-dict record instead
  of the clean `SystemExit` every sibling guard emits → added the `isinstance(d[hid], dict)` guard + a selftest;
  also added the empty-`hid` guard at the function layer (CLI already guarded it). Repo-root-mismatch on `ship`
  (resolves from `$CLAUDE_PROJECT_DIR`) is a shared-by-all-state-ops surface, not an X2 regression — flagged, the
  production caller passes the armed `--repo-root`. JSON write non-atomicity left as-is (single-process CLI; a
  corrupt store fails toward blocking; consistent with `blocks.json`/`residual.json`).

**X3 — SKILL.md "Stage 5.5 · Handoff triage" section.** Instructions-only (no DET code). Inserted between
stage-5 audit and stage-6 revise: the three outcomes (PASS / WRITING-REVISE / NEEDS-STANCE), the reader self-tag
(RUB half), the M3 backstop force-rule (a panel `SURVIVES-IF-NARROWED`/`DOES-NOT-SURVIVE` needing an out-of-`docs/`
number is FORCED to needs-stance — catches the E006 anchor), the 7-row trigger taxonomy, the 6-step
detect-and-recommend (open handoff → sticky block → surface → never auto-spawn → never adopt a number), the two-gate
rebind contract (MF3), and `suspect` ownership. "Honest limits" amended (D050 does NOT close the framing-sentence
escape; classification is RUB-with-one-DET-backstop). SKILL 206→~285 lines — justified functional spec, not
sediment. Three nets green (CLI-flag consistency + run_checks regression · opus oracle **FIX-THEN-PASS** · fresh
`claude -p` actionability ALL-correct). Durable decisions:
- **"5.5" is a doc label only, never `meta.stage`** (a validated int 1–6).
- **Fail toward `needs-stance` only on genuine ambiguity about whether the evidence exists** — NOT on every hard
  sentence. Paired with the over-routing guard (SC-XSTANCE-08: a reword within recorded evidence is writing-revise).
- **Oracle G1 (applied):** surfaced `handoff check --lattice` (the NH4 orphan guard, to run after a stage-6
  re-skeleton drops/renames a claim_id) + `handoff status` (human surface) — the SKILL had instructed only
  `handoff open`, the one gap with a silent-defect consequence (an orphaned open handoff blocking forever).
- **Oracle G2 (applied):** the premortem (F13) reader has no self-tag line — "7 readers self-tag" was false; scoped
  the self-tag to the 6 prose readers; premortem's signal is the panel `CONCLUSION-STATUS` the M3 backstop reads.
- **Fresh-verify-found disambiguation (applied):** the row-1-vs-row-2 boundary was ambiguous for "a result exists
  but a specific sub-statistic was never computed" (E006's fold-level CI). Tightened: a recorded result with a
  contested aggregation is **row 1 → /interpret** (chains to /work); row 2 (/work + \gap) is only for NO recorded
  result at all. The third net caught what the oracle didn't — the point of running it.
