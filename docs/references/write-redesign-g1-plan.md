# /write redesign — G1 build plan: the RUB-grading harness (the P3 blocker)

**Status: BUILD-READY** (hardened across 2 opus `oracle-reviewer` rounds: round 1 HOLD → 5 must-fixes + 3
nice-to-haves folded → round 2 PASS, 1 routing correction + 2 watch-items folded into G1-a). This is the plan to
build G1, the one hard blocker
before the P3 cutover can *run*. It follows the same discipline the rest of this rebuild followed (the redesign
session drafted+hardened a plan before building; every build session executed in atomic, dependency-ordered
chunks under a three-net loop). The harness it produces should be the *minimum* that actually grades the RUB
scenarios — a twin of the apparatus we already have, not a new species.

## The problem (corrected — `tasks.md` G1 undercounts)

The 135-scenario suite has **~90 RUB-containing rows** (a live parse: 93 rows tagged RUB, 4 of them RUB+DET
duals; 40 DET-only) with **no scorer**. Only the DET halves are machine-verified (the per-script `--selftest`s).
So "135 scenarios" is **not** "135 auto-passing" — the RUB half is ungraded.

> **Count correction (a real defect this plan surfaces, oracle MF-1).** `tasks.md` G1, the scenarios-doc close
> (line ~321), and this plan's first draft all say "~51 RUB (41 prior + 10 SC-XSTANCE)". That silently excludes
> the **36 `SC-EX-*`/`SC-VIO-*` real-prose-mined RUB scenarios** (`scenarios.md:166-207`) — which are RUB-tagged,
> judge-graded, and explicitly in the suite — plus the hardening near-miss guards (`SC-F4-OK`, `SC-VOICE-14/15`,
> `SC-RM-1/2`, `SC-CITE-1`, …). The true RUB set is ~90. **Fix `tasks.md` + `scenarios.md` to the corrected count
> as part of G1-a.** A harness scoped to 51 would grade 60% of the RUB suite and call it done — the exact "135 is
> not 135-passing" trap, reproduced one level down.

Until a harness grades all ~90 with a stated pass-threshold and a sign-off mechanic, the cutover would freeze a
suite whose taste/argument/structure/voice half has never been run.

## The estimand (what "G1 done" must mean)

For every RUB scenario: run its INPUT through the functionality that owns it, and decide PASS/FAIL against the
scenario's stated EXPECT (a `MUST flag <reason>` or a `MUST NOT flag` near-miss). Then: a stated threshold over
the whole suite, and a recorded human sign-off. Nothing invented; the judge is the grader, the harness is the
scorer and the bookkeeper.

## The key design fact that sizes everything — RUB scenarios grade by FOUR mechanisms, not one

The first draft said "a RUB scenario is graded by running its functionality's judge and comparing flag/no-flag to
EXPECT." That is true for **most** of the suite but **not all** (oracle MF-2/MF-3). The judges already exist, but
they do not all emit one uniform verdict, and several scenarios' EXPECT is not a judge verdict at all. So each
scenario record carries a **`grading_mechanism`** field, and the scorer has one deterministic reader per
mechanism (each with its own synthetic in the `--selftest`):

| `grading_mechanism` | Which scenarios | How the harness reads PASS/FAIL |
|---|---|---|
| `verdict-line` | the 6 prose judges (F4/F5/F9b/F11/F12/F18) | the uniform final line `<TAG>-VERDICT: {"ready_to_ship":bool,"findings":int}` (verified present in all six `sw-*` agents). **Flag signal = `ready_to_ship:false` (equivalently `findings>0`); no-flag = `ready_to_ship:true ∧ findings:0`.** PASS ⇔ flag-signal == `(expect=="flag")`. |
| `panel-synthesis` | F13 panel scenarios (`SC-ARG-5`, `SC-ARG-10`) | the panel emits `PANEL-VERDICT`/`CONCLUSION-STATUS: SURVIVES\|SURVIVES-IF-NARROWED\|DOES-NOT-SURVIVE` — **no `ready_to_ship`**. The harness applies the **verdicts.py synthesis rule** (bare `SURVIVES` ∧ every objection claim-mapped = no-flag; else flag) — a ternary, not a boolean. |
| `lattice-classification` | F1 reader-model (`SC-RM-1/2`; `SC-STR-03` — see G1-a watch-item) | `sw-reader-model` writes the lattice `reader_model` field; EXPECT is "term classified OLD vs NEW". The harness reads the classification, not a verdict line. (`SC-STR-12` is NOT here — it is owned by the F11 structure judge → `verdict-line`; oracle re-review correction.) |
| `handoff-state` | the 10 RUB `SC-XSTANCE-*` triage scenarios | EXPECT is an **orchestrator behavior**, not a judge verdict: the stage-5.5 triage emits the right `needs-stance(<stance>)` handoff (or correctly does NOT, for the over-routing guards 08/16), and does not narrow prose with an unrecorded number. The harness runs the **triage step on the fixture** and inspects `handoffs.json` + the prose — *not the full pipeline* (this is what keeps G1 a scenario-runner, not a pipeline-runner; see "KILL-risk closed" below). |

Two structural consequences hold across all four:

1. Grading requires **spawning a subagent / running a step** (LLM calls) — there is no Python API harness in this
   repo, and we are not adding one. The "runner" is an **orchestration procedure the agent executes** (mirror of
   the SKILL stage-5 fan-out), plus a Python layer that holds the scenario data, records the per-scenario result,
   and computes the tally. The Python layer is DET-testable; the spawning layer is a SKILL/doc protocol.
2. The Python scorer is a **direct twin of `verdicts.py`** — same "record one judge's output → score against a
   required set → fail-safe everywhere" shape, same `.claude/state/sw-gate/`-style store, same `--selftest`
   discipline. We lift that pattern; we do not reinvent it.

**KILL-risk closed (oracle).** The oracle flagged that if the XSTANCE-triage and reader-model scenarios could only
be graded by re-running the whole `/write` orchestrator, G1 would be a *pipeline*-runner and the twin-verdicts.py
sizing would be wrong for ~13 scenarios. They can't be — each is gradeable by running its **one owning step** on a
synthetic fixture (the triage decision; the reader-model classification), then reading the resulting state. So the
decomposition holds; the run-protocol (G1-c) just carries four readers instead of one.

## Migration map — existing apparatus → G1 (the "tags")

| Existing item | G1 role | Action |
|---|---|---|
| `verdicts.py` (record→score→fail-safe, content-hash store, `--selftest`) | the **scorer's** pattern | **lift the pattern** (new script, same shape) |
| `run_checks.py --selftest` (runs every DET script's selftest, rc=0 ⇔ DET floor green) | the **"every DET green"** half of the threshold | **call it** |
| SKILL stage-5 parallel fan-out (spawn N `sw-*` judges in one message, capture verdicts) | the **run protocol** | **adapt** (per-scenario, INPUT as fixture) |
| the 6 `sw-*` RUB judges + the F13 panel | the **graders** | **reuse unchanged** |
| `write-redesign-scenarios.md` (the RUB rows, INPUT/EXPECT/tag) | the **scenario source of truth** | **extract to a machine-readable store + keep markdown as the human spec** |
| `accept-residual` / Erfan-token pattern in `verdicts.py` | the **sign-off** mechanic | **lift** (a recorded sign-off, anchors never waivable) |
| — (none today) | `rub_scenarios.json` (the store) · `rub_harness.py` (scorer+CLI) · the SKILL "RUB-suite" protocol section | **build new** |

## Build order — atomic, dependency-ordered chunks (G1-a → G1-d)

Each chunk is one independently-verifiable deliverable; ordered so the next can assume the prior as a stable base.

**G1-a — the scenario store + a live-parse consistency DET.** Extract **all ~90 RUB rows** from
`write-redesign-scenarios.md` into `rub_scenarios.json`, one record each: `{id, functionality, grading_mechanism
(verdict-line|panel-synthesis|lattice-classification|handoff-state), grader (the sw-* agent / panel / triage-step),
input, expect: "flag"|"noflag", expect_reason, is_anchor}`. Build `rub_harness.py validate-suite`: a **DET** that
**parses `scenarios.md` live and diffs** against the JSON (oracle N-1 — never a hardcoded id list, or the drift
just moves) — every RUB row present (count + ids), each `grader` maps to a real `sw-*` agent / the panel / the
triage step, every record's `grading_mechanism` is one of the four, the anchors (`SC-VOICE-01..04`,
`SC-XSTANCE-01`) carry `is_anchor`. Also fix the `~51`→`~90` count in `tasks.md` + `scenarios.md`. **Derive
`grading_mechanism` from the functionality column + the 2d remaps — never hand-assign** (oracle re-review: a
hand-assignment is exactly how `SC-STR-12` got misfiled; the live-parse DET catches a wrong owner only if the
mechanism is derived, not copied). *Foundation: every later chunk reads this. Pure data + a Python consistency
check, no LLM — fully `--selftest`-able.*

**Three corrections to apply during G1-a extraction (oracle re-review):**
- **`SC-STR-12` → `verdict-line` (F11), not `lattice-classification`.** It is tagged `F1,F11` and the F11
  structure judge owns the flag (`sw-structure-judge.md:49` names it); grading it by the reader-model field would
  ask the wrong artifact and silent-pass. Route to the F11 `STRUCTURE-VERDICT`.
- **`SC-STR-03` — pin its flag-owner explicitly before extracting.** Tagged `F1`, EXPECT "jargon glossed on first
  use." `sw-reader-model` only *writes* the OLD/NEW field; something downstream must turn "classified NEW + no
  gloss" into a flag. Decide which step owns that flag decision (reader-model classification vs an F11/F12 prose
  flag) and record that mechanism — don't leave it ambiguous (same wrong-reader risk as SC-STR-12, less obvious).
- **`handoff-state` negative anchors (`SC-XSTANCE-08/16`) read TWO signals.** Their MUST-NOT-flag synthetic must
  assert *both* halves — **no handoff opened AND the `writing-revise` classification recorded** — so a triage step
  that does nothing at all cannot pass the negative anchor for the wrong reason. Consider extending the MF-4
  binding-reason rule (anchors must name the right defect) to these two negative anchors as well.

**G1-b — the scorer.** `rub_harness.py score`: given per-scenario recorded results in a store, score each PASS/FAIL
**by its `grading_mechanism`** (the four readers in the table above — each with its own synthetic in the selftest),
then apply the **threshold** (G1(b)): *every DET green (`run_checks --selftest` rc=0) AND every RUB PASS*, anchors
**hard-required and never waivable**. Two sharpened rules from the oracle:
- **Flag signal is named per mechanism** (oracle MF-5), not hand-waved: `verdict-line` reads `ready_to_ship`
  (`findings>0` ⇒ flag); `panel-synthesis` applies the ternary synthesis rule; `lattice-classification` reads the
  OLD/NEW field; `handoff-state` reads whether the expected `needs-stance` handoff is present in `handoffs.json`
  and prose was not narrowed. The selftest carries **both a MUST-flag and a MUST-NOT-flag synthetic per mechanism**
  (the near-miss symmetry verdicts.py has no analog for).
- **Reason-correctness is binding for the anchor set, advisory elsewhere** (oracle MF-4): for `SC-VOICE-01..04` +
  `SC-XSTANCE-01`, a flag must also name the right defect (keyword-match on `expect_reason`) or it FAILs — else a
  reason-blind flag could let a regression through the very anchors that exist to catch it. Non-anchor flag
  scenarios stay advisory-match (judgment stays with the judge/human, per the DET-mechanical / RUB-judgment split).

`--selftest` drives all of this with **synthetic recorded results** (no live judges) — the verdicts.py twin. *The
bulk of the DET-testable logic lives here.*

**G1-c — the run protocol + the sign-off mechanic.** (i) A SKILL/reference section: how the orchestrator, per
scenario, runs the **owning step fresh** by mechanism — spawn the `sw-*` judge / the F13 panel / the reader-model /
the stage-5.5 triage — feeds the INPUT as a synthetic prose/lattice/F13-state fixture, and captures the result
into the store (mirror stage-5 fan-out; parallel where independent). (ii) `rub_harness.py sign-off`: a recorded
Erfan token over the current suite-result hash (lift `accept-residual`), refusing if any anchor failed. **Honest
limit, stated (oracle N-3):** like `gate_state`/`accept-residual`, this is TRUSTED-not-verified — the store records
*which* results were entered; it cannot prove a recorded RUB result came from a real judge run rather than a
hand-typed PASS. Same fabrication surface the rest of the pipeline accepted; equally fabricable, named not hidden.
*Mostly instructions + a thin CLI — the X3-analog chunk.*

**G1-d (REQUIRED, not optional — oracle N-2) — a live converged dry-run.** Run the harness end-to-end with **real
judges** over a small slice (the 4 Claudio anchors + `SC-XSTANCE-01`, one per mechanism). This is the **only net
that exercises the spawning layer** the Python selftest cannot reach — for a harness whose whole job is to spawn
live judges, it is not skippable. Confirms the loop closes and each mechanism's reader returns a gradeable result
on a real fixture. May be run as one exercise with the separate G3 demo, but it ships with G1.

## The three-net loop — per chunk, before its commit (unchanged, the proven method)

1. **Embedded `--selftest`** (regression net) — green first. For an instructions-only chunk (G1-c), the analog
   is "`run_checks`/`rub_harness` selftest still green + the SKILL's named CLI flags actually exist."
2. **Opus `oracle-reviewer`** (discovery net) — run on **every** chunk regardless of selftest greenness (it has
   caught a load-bearing silent-pass on 5/5 prior chunks). A **REJECT requires a re-review** after the fix; never
   self-assert. Apply must-fixes + re-test; **fold the oracle's new boundary scenarios into the `--selftest`**.
3. **Fresh `claude -p` clean-room verify** (subprocess — loads the new on-disk artifact an in-process Agent can't;
   builds its OWN fixtures, never `--selftest`). For a pure-Python+data chunk, an honest black-box CLI test with
   independent fixtures stands in (as it did for P2-D-1).

Then **one atomic commit + one build-log entry** (entry written *before* the commit), appended to
`write-redesign-build-plan.md` so that doc stays the single build-log.

**Mechanics not to re-hit (L059–L062):** `CLAUDE_WRAP_SNAPSHOT_SKIP=1` on every `claude -p` child; Bash tool
`timeout` ≥ 540000 ms; `cd /home/centcom/data/brain-alignment` inside subprocess commands; scoped staging only
(explicit paths, no `-A`); remove stray fixtures before committing; fail-safe everywhere (missing/corrupt →
block, never silent-pass); a DET floor binds to ground truth and fails toward *more* checking on ambiguity.

## Effort / model
Python chunks (a, b): build at session effort; oracle `oracle-reviewer` opus. G1-c instructions: same. The live
judges in G1-d run at their own frontmatter effort (the `sw-*` agents).

## Open questions for Erfan (before BUILD-READY)
Resolved by the oracle pass (no longer open): G1-d is **required** (ships with G1); reason-match is **binding for
anchors / advisory elsewhere**; the four grading mechanisms are settled. Remaining genuine forks for you:
- **Sign-off granularity:** one token over the whole suite-result hash (recommended) vs per-scenario sign-off?
- **The ~90 real RUB scope:** the 36 `SC-EX-*`/`SC-VIO-*` real-prose scenarios roughly double G1's grading work
  vs the "~51" the docs assumed. Grade all ~90 (recommended — it's the honest suite), or scope G1 to a defended
  subset now and backfill the real-prose set as a fast-follow? (This changes how big the first run is, not the
  design.)
- **Cost note:** grading ~90 RUB scenarios = ~90 live judge spawns per full suite run. Fine for a P3 gate run, but
  worth knowing it is not free to re-run casually. (DET stays instant.)
```
