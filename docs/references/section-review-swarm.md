---
title: "Section review swarm — pipeline, process, and prompts"
tags: [reference, manuscript, review, subagents]
---

# Section review swarm — pipeline, process, and prompts

The apparatus behind the section-by-section submission review (2026-08-27 onward). This is a process reference, not a status board: what was run and accepted lives in Git commits and the deferred list; [`../status.md`](../status.md) owns operations.

Lineage: v1 ran Section 2 (2026-08-27, 9 children: 4 analysts, 4 counter-reviewers, judge + re-run judge). v2 ran Section 3 (2026-08-28, 17 children: live-text embed, 5+5, dual parallel judges, round-2 blind pass + resolution judge). v3 folds the Section-3 learnings below and is the current recipe; it is implemented in [`../../.claude/scripts/section_swarm.js`](../../.claude/scripts/section_swarm.js).

## Why a swarm at all

One reviewer pass produces prose-swap churn and misses design-fact errors; one judge rubber-stamps its own reading. The swarm separates four jobs that one context cannot hold: exhaustive per-paragraph analysis, adversarial defense of precision, independent adjudication (twice, on decorrelated providers), and evidence verification for design facts. Only the parent writes files.

## Pipeline

```
live .tex ──generator──► /tmp/sN-swarm.js (text embedded, sha256 stamped)
   Phase 1   N analysts (one per subsection scope)      review-only, read the section cold
   Phase 2   N counter-reviewers                        IMPROVE/WORSEN per proposal + MISSED items
   Phase 3   2-3 judges in parallel (decorrelated providers)   APPLY/REJECT/MODIFY/ROUTE-EVIDENCE per ID
   EVIDENCE  routed design-fact items → evidence judge (repo access, must cite records)
   PARENT    parse → agreement → post-filters → evidence judge → apply → sync → round 2 → commit
```

Model routing is the session's declared constraint. v3.1 (Section 4, Erfan 2026-08-29): workers = deepseek-v4-flash + kimi-k3 (one analyst and one counter per scope per model), judges = kimi-k3:high + deepseek-v4-flash:high; earlier rounds used glm-5.3-flash workers and a glm-5.3 judge, but ollama-cloud glm children proved unreliable in this role: the judge burned its entire 32k output cap on `:high` thinking and produced no output (twice — the model family is then exclusion-listed for hours), and one counter derailed into off-task content. Lesson: a judge model needs enough output-token headroom for the full decision list after thinking, and the thinking level must be set explicitly, never inherited.

Children never edit files; the parent is the sole writer and decision-maker. Two Section-4 hazards the prompts cannot fully prevent and the parent must check: (a) native children have repo read access and some anchored quotes on the canonical rewrite twin instead of the embedded review text — verify every anchor against the reviewed file, not against whichever copy a child happened to read; (b) judges occasionally write finals as instructions ("insert after the Unresolved entry: ...") — interpret them against the live region instead of pasting.

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
| 10 | v3.1: dual-model workers and judges, both from the session's declared model constraint; explicit thinking levels on every child | glm-5.3 children failed twice (output-cap death, off-task derailment); the inherited `:high` thinking level was the hidden cause of the cap death |

Kept from v2 because they worked: live-text extraction at generation time with sha256 stamp, anchor assertions at generation (each `\subsection` title found exactly once), dual parallel judges, counter-reviewer "guardian of precision" role, CLEAN as an acceptable answer, deferred splits flagged but never fixed by children.

## Build and launch

From the repo root:

```bash
node .claude/scripts/section_swarm.js 4                     # round-1 workflow → /tmp/s4-swarm.js
node .claude/scripts/section_swarm.js 4 --verify /tmp/s4-swarm.js   # byte-identical check
```

Then launch with the subagent tool: `workflowScriptPath=/tmp/s4-swarm.js`, `async: true`, arm the wake subscription, and process the return value on completion.

After the parent applies round-1 changes (and syncs the rewrite twin, runs the checker, rebuilds, commits):

```bash
node .claude/scripts/section_swarm.js 4 --round2            # blind reviewer on the revised text
node .claude/scripts/section_swarm.js 4 --round2-judge FINDINGS.md   # resolution judge (repo access)
```

## Parent procedure after the swarm returns

1. Parse analyst, counter, and both judge outputs with the strict block parser. Verify: every ID present in the judges' outputs, zero unmatched blocks. If a judge's parse yields fewer blocks than expected, re-extract with the tolerant parser before touching anything else — never proceed on an empty parse.
2. Build the agreement matrix keyed by ID: compare DECISION labels and FINAL TEXTs. Only items whose FINAL TEXTs differ are real divergences; reconcile each against the live text, documenting the reason and any parent override.
3. Run the mechanical deferred-split post-filter over every accepted FINAL (deferred terms, full-form assay names, `-specific`/`-content`); anything that trips goes back to reconciliation, not into the apply-set.
4. Run the adjacency scan over the apply-set in file order: repeated words or phrases across neighboring accepted finals, overlapping anchors, edits that interact once composed.
5. Collect every ROUTE-EVIDENCE item and run the evidence judge on them: strongest available model, read-only repo access, must verify against the owning E record, runner code, or appendix table and return APPLY/REJECT with the verified fact. The parent reviews its verdict before applying.
6. Apply accepted edits to the submission, sync the canonical rewrite twin (respecting the known deliberate variant spots), run `uv run python .claude/scripts/manuscript_check.py docs/manuscript/rewrite`, rebuild both PDFs, commit atomically.
7. Generate and run the round-2 blind pass on the revised text, then the resolution judge with repo access. Apply its APPLY/MODIFY verdicts after parent review; record OWNER-CONFIRM items in [`../manuscript/submission/deferred-review-items.md`](../manuscript/submission/deferred-review-items.md).
8. Produce the owner-preference surface for Erfan's paragraph-by-paragraph pass: register-word density (the words that have drawn allergic reactions: substrate, standard, naturalistic, assay, leverage-class suspects) and a coinage census (compounds appearing before their gloss).
9. Convergence: the prose sweep is done when a round returns all-CLEAN or only low-severity items that are rejected or owner-pending. Never let the swarm settle a global naming policy or a scientific verdict; those are owner decisions routed to the deferred list or `/interpret`.

## Adding the next section

Add an entry to `SECTIONS` in [`../../.claude/scripts/section_swarm.js`](../../.claude/scripts/section_swarm.js): file, label, the section-type rules (what that section declares and must never lose), analyst criteria, the counter-reviewer guardian line, and scopes (one per subsection, anchored on the exact `\subsection{...}` title; preamble joins the first scope). Update `SHARED.settled` and `SHARED.deferred` with what the latest review settled or deferred. The anchor assertion fails loudly if the manuscript drifted, which is the point.

## Related

- [Supervisor feedback](supervisor-feedback.md)
- [Deferred submission review items](../manuscript/submission/deferred-review-items.md)
- [Methodology and authority contract](../03-methodology.md)
- [Project status](../status.md)
