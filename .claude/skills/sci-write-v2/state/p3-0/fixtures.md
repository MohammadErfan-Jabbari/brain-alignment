# P3-0 dress rehearsal — fixtures + fairness audit (12 scenarios)

A committed, reproducible dress rehearsal of the RUB-grading harness before the full 94-run (P3-1). Each fixture
carries its scenario's `input` from `rub_scenarios.json`, wrapped into the minimal artifact its grader reads.
Graders were **real subagent spawns**; results in `../rub-results/`. Run: S43 (P3-0), 2026-06-25.

**Outcome: all 12 graded PASS in the expected direction**, across all 4 grading mechanisms. An opus
`oracle-reviewer` fairness audit flagged 4 fixtures as answer-leaking / self-graded; **all 4 were rebuilt clean
and re-run** (the versions below are the corrected ones). The full-suite `score` is still FAIL — expected, since
only 12 of 94 are recorded; the signal is that none of the 12 is in the failure list and `anchor_fail` dropped
from 5 to the 3 ungraded voice anchors.

| # | Scenario | Mechanism | Grader | Expect | Result |
|---|---|---|---|---|---|
| 1 | SC-VOICE-01 | verdict-line | sw-voice-auditor | flag (ANCHOR) | PASS, named defect |
| 2 | SC-HON-06 | verdict-line | sw-scope-judge | flag | PASS |
| 3 | SC-F4-OK | verdict-line | sw-argument-judge | noflag | PASS |
| 4 | SC-TRUST-6 | verdict-line | sw-claim-fidelity-judge | flag | PASS |
| 5 | SC-STR-01 | verdict-line | sw-structure-judge | flag | PASS |
| 6 | SC-ARG-4 | verdict-line | sw-acknowledgment | flag | PASS (rebuilt) |
| 7 | SC-ARG-5 | panel-synthesis | counter-argument + premortem | flag | PASS (rebuilt) |
| 8 | SC-ARG-10 | panel-synthesis | counter-argument + premortem | noflag | PASS (rebuilt) |
| 9 | SC-RM-1 | lattice-classification | sw-reader-model | OLD | PASS |
| 10 | SC-RM-2 | lattice-classification | sw-reader-model | NEW | PASS |
| 11 | SC-XSTANCE-01 | handoff-state | triage + real verdicts.py handoff | flag (ANCHOR) | PASS, named E006 |
| 12 | SC-XSTANCE-08 | handoff-state | sw-scope-judge self-tag → triage | noflag | PASS (rebuilt) |

## Fixtures (verbatim — the corrected, cue-free versions)

**SC-VOICE-01** (voice) — prose snippet, graded as-is:
> The inverted question only earns a thesis if it survives a hard prior:

**SC-HON-06** (scope) — prose snippet; lattice frame = `basic-science`:
> Brain alignment is a new training objective that improves model quality for deployment.

**SC-F4-OK** (argument, stage-2 edge) — one warrant edge, verbatim from the store:
> from: "the signal is differentiable & gradient-accessible (shown)"; to: "usable as a training loss";
> warrant: "a differentiable signal can be optimized by gradient descent"

**SC-TRUST-6** (claim-fidelity) — a claim sentence carrying an `observed` tag:
> \evd{c1}{observed} These results demonstrate that brain-alignment training causes more faithful representations.

**SC-STR-01** (structure) — a paragraph + reader-model (ML/NeurIPS reader):
> This paper presents a method that maps language-model activations to brain recordings. The mapping is linear.
> We trained models of several sizes. Alignment was then measured across layers.

**SC-ARG-4** (acknowledgment) — REBUILT cue-free: the defended claim ONLY, no hint about the limitation:
> Defended claim c1 (bound E002/E006, strength=supported): "The brain-alignment loss is a usable distillation
> signal." Acknowledgments present: none.
> (Original fixture leaked the answer by appending "(Known live limit: the Q2 lever is undemonstrated)". Removed.
> The agent now infers the missing acknowledgment itself.)

**SC-ARG-5** (panel) — SCENARIO FIXED (the suite scenario itself was rewritten, not just the fixture): the
objection now threatens NO enumerated claim, so it exercises the intended `all_objections_mapped = false` path:
> Lattice has ONE enumerated claim c1 = "the brain-alignment encoding signal is real beyond confounds (E006)".
> Supplied premortem objection: "the distillation use-case shows no practical payoff (Q4)" — orthogonal to c1
> (signal-reality vs downstream-utility). Both panel agents independently ruled it threatens no enumerated claim →
> `all_objections_mapped = false` → flag, via the intended unmapped path (not the conclusion-status route).
> (The original scenario's single broad claim let the panel map every objection, so it could only flag via
> SURVIVES-IF-NARROWED — it never tested the unmapped path. Fixed in `write-redesign-scenarios.md` + regenerated
> store; validate-suite PASS, 94 rows unchanged.)

**SC-ARG-10** (panel) — REBUILT: claim reference embedded naturally in the objection, not pre-labeled:
> Draft (honestly hedged): "We do not claim a demonstrated Q2 lever. The E004 association ... rests on a
> pseudo-replicated bootstrap (3 seeds × 5 folds as 15 draws); at n=5 folds the CI includes zero. ... undemonstrated,
> not proven-zero." Claim c7 = "held-out alignment gain from the Q2 lever". Objection: "the bootstrap in E004
> pseudo-replicates, inflating the held-out alignment-gain CI" (panel extracts → threatens c7).

**SC-RM-1 / SC-RM-2** (reader-model) — one reader-model build, two terms classified:
> Venue: ICLR/NeurIPS ML reader. "linear probe" → OLD/assumable; "voxelwise noise ceiling" → NEW/gloss.

**SC-XSTANCE-01** (handoff triage, ANCHOR) — F13 state given; handoff machinery exercised for real:
> Central claim cites E006's voxel-bootstrap CI. F13 panel = SURVIVES-IF-NARROWED; narrowing needs the unrecorded
> fold-level CI → M3 backstop forces needs-stance(/interpret). `verdicts.py handoff open hf-e006 → /interpret` run
> for real (isolated repo-root); status confirmed open + convergence blocked. Handoff names E006; prose NOT
> narrowed; recompute carried as proposed_unverified for stat-aggregation-auditor.

**SC-XSTANCE-08** (handoff triage) — REBUILT: a real reader produces the finding and self-tags the class:
> Draft: "Brain alignment generalizes across datasets." Recorded evidence: only LeBel UTS03 (E006); a live result
> supports the narrower "measurable on LeBel UTS03". `sw-scope-judge` flagged the over-scope (findings=1) and
> emitted `TRIAGE-TAG {class: writing-revise, why: narrower recorded claim exists, target_stance: null}`. M3 did
> NOT fire → no handoff. (Original fixture was self-graded by the orchestrator with no detection step. Fixed.)

## Oracle fairness audit (opus oracle-reviewer, S43)
Verdict: 7/12 FAIR on first pass; SC-XSTANCE-08 RIGGED (self-graded), SC-ARG-4/5/10 WEAK (answer leaked into the
grader input). All 4 rebuilt cue-free and re-run — every one still PASS, now on a genuine detection step.
**Lesson for P3-1 (L0xx candidate): build every fixture input-only — never embed the expected finding/label in
the prose handed to the grader; for triage-noflag, a real reader must produce + self-tag the finding, not the
orchestrator.** Plus the SC-ARG-5 scenario-quality note above.
