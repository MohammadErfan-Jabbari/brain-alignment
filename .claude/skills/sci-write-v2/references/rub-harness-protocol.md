# RUB-grading harness — the run protocol (the P3 suite-grading gate)

How to grade the 94 RUB scenarios of the `/write` acceptance suite and sign the result off. The DET floor
(`run_checks.py --selftest`) is instant and machine-verified; this protocol is the RUB half — it runs each
scenario's owning step on the scenario INPUT and records the result, so `rub_harness.py score` can decide
PASS/FAIL and `sign-off` can gate. Run it at P3 (the full suite) and whenever a scenario or a judge changes
(the changed scenarios re-run; a changed INPUT makes its old result stale → re-run forced).

Scripts: `scripts/rub_harness.py` (store + scorer + sign-off), `scripts/rub_scenarios.json` (the store, 94 rows).
Design + rationale: `docs/references/write-redesign-g1-plan.md`.

## Step 0 — preconditions
```
uv run python rub_harness.py validate-suite     # store <-> live markdown agree (must PASS first)
uv run python run_checks.py --selftest          # the DET floor is green (the other half of the threshold)
```

## Step 1 — grade each RUB scenario by its `grading_mechanism`
Read `rub_scenarios.json`. Each record has `{id, grading_mechanism, grader, input, expect, expect_class,
expect_reason, is_anchor}`. For each, run the **one owning step** on the scenario INPUT (as a synthetic
fixture — a minimal prose snippet / lattice / F13-state that carries the INPUT), capture the result, and record
it. **Spawn the independent judges in parallel batches** (mirror the SKILL stage-5 fan-out); do not serialize.

| `grading_mechanism` | Run this | Record (`rub_harness.py record --id <ID> --result '<json>'`) |
|---|---|---|
| `verdict-line` | spawn the `grader` agent (`sw-argument-judge` / `sw-scope-judge` / `sw-claim-fidelity-judge` / `sw-structure-judge` / `sw-voice-auditor` / `sw-acknowledgment`) on the INPUT | `{"ready_to_ship": <bool>, "findings": <int>, "finding_text": "<what it flagged>"}` — copy the verdict line verbatim; `finding_text` is required for the anchors (binding reason-match) |
| `panel-synthesis` | spawn the F13 panel (`premortem-analyst` + `counter-argument`) on the INPUT. **`conclusion_status` is `counter-argument`'s `CONCLUSION-STATUS` verbatim** (uppercase enum, exact) — `premortem-analyst` emits only `TOP-RISK` and has no status; fold its TOP-RISK in as an advisory objection when judging `all_objections_mapped` (the `verdicts.py:27-35` rule). | `{"conclusion_status": "SURVIVES\|SURVIVES-IF-NARROWED\|DOES-NOT-SURVIVE", "all_objections_mapped": <bool>, "finding_text": "..."}` |
| `lattice-classification` | spawn `sw-reader-model` on the INPUT (venue + term); read which list the term landed in (`terms_old` vs `terms_new`) | `{"classified": "OLD\|NEW"}` |
| `handoff-state` | run the stage-5.5 triage on the INPUT fixture (its F13 state + lattice); then inspect `verdicts.py handoff status` / the prose | `{"handoff_opened": <bool>, "handoff_stance": "interpret\|work\|scout\|plan\|null", "prose_narrowed": <bool>, "classified_writing_revise": <bool>, "finding_text": "..."}` — for **SC-XSTANCE-01** (an anchor), `finding_text` must name **E006** (the binding reason-match requires it) |

`record` stamps each result with the hash of the scenario's current INPUT — so if the INPUT later changes, the
old result is **stale** and `score` forces a re-run (it never silently counts).

## Step 2 — score against the threshold
```
uv run python rub_harness.py score          # validate + DET-green (via run_checks) + every RUB recorded-fresh-and-PASS
```
PASS requires: store valid ∧ DET floor green ∧ every RUB scenario has a fresh recorded result that PASSes ∧ no
anchor failure. An ungraded or stale scenario is a FAIL (never a silent pass). The **anchors**
(`SC-VOICE-01..04`, `SC-XSTANCE-01`) are **never waivable** — a flag must also name the right defect or it FAILs.

For each FAILURE the tally lists: either (a) a real `/write` pipeline defect — fix the owning component and
re-run that scenario's grader; or (b) a judge that graded wrong on a fair fixture — fix the fixture/agent and
re-run. Do **not** waive; the suite is the regression guarantee.

## Step 3 — sign off (only when green)
```
uv run python rub_harness.py sign-off --status        # SIGNED / STALE / UNSIGNED for the current suite
uv run python rub_harness.py sign-off --by Erfan --note "P3 suite-grading"
```
`sign-off` **refuses** a failing suite. The token binds to the suite content hash, so it goes **STALE** the
moment any result or the suite changes — a sign-off can never silently cover a later edit; re-sign after a change.

## Honest scope (TRUSTED-not-verified)
The store records *which* result was entered and the INPUT it was bound to; it **cannot prove** a recorded
result came from a real judge run rather than a hand-typed one — the same trust model as `gate_state.py` /
`verdicts.py`. The freshness binding stops a stale result counting; it does not stop a fabricated one. The
human running the gate is the backstop, exactly as elsewhere in the pipeline.
