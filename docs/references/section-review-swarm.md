---
title: "Section review swarm — pipeline, process, and prompts"
tags: [reference, manuscript, review, subagents]
---

# Section review swarm — pipeline, process, and prompts

The apparatus behind the section-by-section submission review (2026-08-27 onward). This is a process reference, not a status board: what was run and accepted lives in Git commits and the deferred list; [`../status.md`](../status.md) owns operations.

Lineage: v1 ran Section 2 (2026-08-27, 9 children: 4 analysts, 4 counter-reviewers, judge + re-run judge). v2 ran Section 3 (2026-08-28, 17 children: live-text embed, 5+5, dual parallel judges, round-2 blind pass + resolution judge). v3.1 ran Section 4 with dual-model workers and judges. v3.2 added explicit routing, fail-loud phase gates, exact `OLD`→`NEW` anchors against the canonical rewrite, neutral round two, and canonical-first application. v3.4 was the final recipe: it applies [D067](../decisions/decisions.md), keeps evidence-grounded clarity repairs out of the owner-confirm route, canonically parses bold-format drift before gating, and rejects duplicate IDs, discarded drafts, placeholder blocks, and no-op edits at admission. Its implementation (`.claude/scripts/section_swarm.js`) was retired by [D068](../decisions/decisions.md): it grew across five sessions with no authorizing decision, and its last four launches all ended in fail-loud infrastructure stops. This file is retained as a process record of what was run and what the routing failures taught, not as a live recipe. Recover the code from Git history if it is ever rebuilt under a recorded decision.

## Why a swarm at all

One reviewer pass produces prose-swap churn and misses design-fact errors; one judge rubber-stamps its own reading. The swarm separates four jobs that one context cannot hold: exhaustive per-paragraph analysis, adversarial defense of precision, independent adjudication (twice, on decorrelated providers), and evidence verification for design facts. Only the parent writes files.

## Pipeline

```text
canonical rewrite .tex ──generator──► /tmp/sN-swarm.js (text embedded, sha256 stamped)
   Phase 1   N analysts (one per subsection scope)      review-only, read the section cold
   GATE      complete blocks + exact unique OLD anchors; retry once, otherwise stop
   Phase 2   N counter-reviewers                        IMPROVE/WORSEN per proposal + MISSED items
   GATE      every expected ID covered; retry once, otherwise stop
   Phase 3   2 judges in parallel (decorrelated providers)   APPLY/REJECT/MODIFY/ROUTE-EVIDENCE per ID
   GATE      every ID covered + APPLY/MODIFY has exact unique OLD→NEW; retry once, otherwise stop
   EVIDENCE  routed design-fact items → evidence judge (repo access, must cite records)
   PARENT    agreement → post-filters → evidence judge → apply canonical → sync derivative → round 2 → commit
```

Model routing is the session's declared constraint. v3.1 (Section 4, Erfan 2026-08-29): workers = deepseek-v4-flash + kimi-k3 (one analyst and one counter per scope per model), judges = kimi-k3:high + deepseek-v4-flash:high. v3.3 (Section 5, final route 2026-08-31): the same proven role structure with kimi served by `ollama-cloud/kimi-k3` (the kimi-coding provider hit its weekly quota mid-launch and Erfan directed the ollama-cloud model) — workers = deepseek-v4-flash:medium + ollama-cloud kimi-k3:medium, judges = ollama-cloud kimi-k3:high + deepseek-v4-flash:high; deepseek performs the blind pass and ollama-cloud kimi the resolution judge. Erfan removed the openai-codex models on 2026-08-31 after the Luna/Sol tier hit its usage limit and exclusion-locked the swarm for roughly a day. Ollama-cloud GLM is excluded from the swarm recipe entirely: a glm-5.3 judge burned its entire 32k output cap on `:high` thinking and produced no output twice (Section 4 era), one glm counter derailed off-task, and on 2026-08-31 all three glm-5.3:medium Section-5 analysts terminated at stopReason `length` with no output, tripping the phase-1 gate as designed. Lesson: ollama-cloud GLM cannot carry any long-output phase in this pipeline at any explicit thinking level; every routed model needs output-token headroom for its complete deliverable after thinking.

Children never edit files; the parent is the sole writer and decision-maker. v3.2 instructs review-only children to use only the supplied canonical text and mechanically rejects APPLY/MODIFY blocks unless their one-line `OLD` anchor occurs exactly once in that text and a one-line `NEW` replacement is present. A malformed phase retries once and then stops; it never silently drops review coverage. Routed evidence items and the composition of multiple individually valid edits still require parent review.

## The v3 upgrades (each fixes a Section-3 defect)

| # | Upgrade | Section-3 defect it fixes |
| --- | --- | --- |
| 1 | Unique finding IDs from the analyst (`<scope>-P<n>.<k>`, MISSED items `<scope>-M<k>`), referenced by counters and judges | Judges returned different item counts (77 vs 67) and numbering shifted, so agreement comparison produced false divergences |
| 2 | Judge output contract: one block per ID, no preamble; parent verifies parsed count before proceeding | Judge-2 output failed the first parse silently (32-byte parse artifact); format drift cost a re-extraction |
| 3 | Agreement computed on FINAL TEXT matched by ID, not on labels | Most "disagreements" were label noise with byte-identical finals |
| 4 | Mechanical deferred-split post-filter on accepted finals (before applying) | Both judges wrote the full "measurability assay" form into finals where the submission deliberately used the short form |
| 5 | Mechanical adjacency scan over the apply-set | Two accepted edits produced adjacent "instead...instead"; the parent caught it by luck |
| 6 | `TYPE=design-fact` in analyst output + `DECISION: ROUTE-EVIDENCE` for judges; routed items go to an evidence judge (strong model, repo access, must cite the E record / runner / appendix) | The "scaled synthetic-target family" gloss would have inserted a false design fact (no loss-weight sweep; λ = 0.1 fixed); "auxiliary-target family" needed E025's code to settle; both were prose-prompt questions that were really evidence questions |
| 7 | Round-2 blind pass + resolution judge are standard, not optional; the resolution judge must verify every QUOTE against live files and may return `OWNER-CONFIRM` | Round 2 caught 3 real defects (lane→route, row-twin antecedent with a wrong proposed referent, delimiter) and rejected 6 with verified reasons |
| 8 | Settled-phrasings block regenerated per section from the current manuscript state, including the settled naming policy (full contract name at first use; short forms after) and "evidence criteria" | Hand-copied prompt constants drift from the manuscript as each section lands |
| 9 | Owner-preference surface: parent runs a cheap register-word density and coinage census per paragraph and hands it to Erfan's paragraph-by-paragraph pass | Erfan's post-swarm pass surfaced owner allergies the swarm cannot adjudicate ("substrate" ×3 in one paragraph, "evidence standard" too harsh) |
| 10 | v3.1: dual-model workers and judges, both from the session's declared model constraint | glm-5.3 children failed twice (output-cap death, off-task derailment) |
| 11 | v3.2: explicit model and thinking suffix on every analyst, counter, judge, round-2 reviewer, and resolution judge | Inherited `:high` thinking exhausted a judge's output allowance and stalled Section 4 |
| 12 | v3.2: no silent output slicing; phase gates require complete IDs and exact unique `OLD`→`NEW` anchors, retry once, then stop | Character slicing could cut a valid response mid-block; degenerate 114-character and off-task outputs previously flowed downstream |
| 13 | v3.2: canonical rewrite is reviewed and edited first; the submission derivative is synchronized afterward | Reviewing or applying against the derivative inverted the repository's authority direction and let children anchor on the wrong twin |
| 14 | v3.2: owner-word census is embedded before review and repeated after application; round two uses a neutral coverage checklist | Owner allergies surfaced only after the swarm, while “mostly clean is expected” biased the residual pass toward stopping |
| 15 | v3.3: `OWNER-CONFIRM` is limited to changed scientific meaning, governing policy, external commitments, or genuinely preference-dependent choices | Evidence-grounded clarity and scope repairs were being routed to Erfan despite his standing delegation of those edits to the reviewed recommendation |
| 16 | v3.4: gates canonically strip `**` wrappers and rewrite inline `ID — VERDICT:` headers before parsing; phase-1 admission rejects duplicate IDs, discarded drafts, placeholder blocks, and OLD==NEW no-ops; every prompt demands literal plain-text block format | Ollama-kimi analysts emitted inline self-corrections (a duplicate discarded P2.2, a placeholder P4.1) that passed format checks and broke phase-2 coverage; counters drifted into `**ID:**` markdown that the strict parser read as zero blocks |

Kept from v2 because they worked: live-text extraction at generation time with sha256 stamp, anchor assertions at generation (each `\subsection` title found exactly once), dual parallel judges, counter-reviewer "guardian of precision" role, CLEAN as an acceptable answer, deferred splits flagged but never fixed by children.

## Retired implementation

The generator, its `--selftest` / `--verify` / `--round2` / `--round2-judge` entry points, and the `SECTIONS` routing table lived in `.claude/scripts/section_swarm.js` and were deleted by [D068](../decisions/decisions.md). Recover the file from Git history if the pipeline is ever rebuilt under a recorded decision; do not reconstruct it from this document, which records intent and defects rather than the code.

Two properties of it are worth carrying into any replacement, because both were earned the hard way: children never write files and the parent is the sole writer; and a phase stops after exactly one malformed-output retry rather than continuing with reduced review coverage. Never auto-substitute a model after a failure.

## Parent procedure after the swarm returns

1. Confirm that every generated phase passed its mechanical gate. The gate enforces complete expected IDs and exact unique `OLD` anchors for proposed edits; a failed retry stops the workflow. Never continue with reduced review coverage.
2. Build the agreement matrix keyed by ID: compare DECISION labels and `NEW` texts after normalizing only Markdown fences, line endings, and trailing whitespace. Case and punctuation remain meaningful. Only items whose normalized `NEW` texts differ are real divergences; reconcile each against the canonical live text, documenting the reason and any parent override.
3. Run the mechanical deferred-split post-filter over every accepted FINAL (deferred terms, full-form assay names, `-specific`/`-content`); anything that trips goes back to reconciliation, not into the apply-set.
4. Run the adjacency scan over the apply-set in file order: repeated words or phrases across neighboring accepted finals, overlapping anchors, edits that interact once composed.
5. Collect every ROUTE-EVIDENCE item and run the evidence judge on them: strongest available model, read-only repo access, must verify against the owning E record, runner code, or appendix table and return APPLY/REJECT with the verified fact. The parent reviews its verdict before applying.
6. Apply accepted content edits to the canonical rewrite, propagate formatting-neutral changes deliberately to the submission derivative (respecting known variant spots), run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/rewrite`, and rebuild both PDFs once per accepted subsection batch before committing atomically.
7. Generate and run the neutral round-2 blind pass on the revised canonical text, then the resolution judge with repo access. Apply its APPLY/MODIFY verdicts after parent review. Before recording an `OWNER-CONFIRM`, apply D067: evidence-grounded clarity or scope repairs that preserve scientific meaning remain parent decisions; only genuinely owner-dependent items go to [`../manuscript/submission/deferred-review-items.md`](../manuscript/submission/deferred-review-items.md).
8. Inspect the register-word surface embedded in the pre-pass, then repeat the density and coinage census after application. The parent resolves readability issues under D067 and asks Erfan only when evidence cannot decide among materially different preferences.
9. Convergence: the prose sweep is done when a neutral checklist returns all-CLEAN or only low-severity items that are rejected or genuinely owner-pending. Never let the swarm settle a global naming policy or a scientific verdict; those remain owner decisions routed to the deferred list or `/interpret`.

Before applying the prose swarm to Discussion, Limitations, or Conclusion, run a separate read-only scientific-scope and argument review. The prose swarm deliberately forbids restructuring and verdict changes, so it cannot detect missing synthesis, citation insufficiency, conclusion overreach, or a weak inference chain.

## What replaces it

Judgment is the `/review` panel's job: `counter-argument`, `socratic-thinker`, `premortem-analyst`, and `first-principles-grounder`, with `oracle-reviewer` when a design gate is in scope. Mechanical verification that prose matches the record is a separate job from judging the prose, and belongs to read-only verification agents rather than to a prose swarm.

The parent procedure above is retained because it is the bar any replacement still has to meet.

## Related

- [Supervisor feedback](supervisor-feedback.md)
- [Deferred submission review items](../manuscript/submission/deferred-review-items.md)
- [Methodology and authority contract](../03-methodology.md)
- [Project status](../status.md)
