---
name: scientific-writing
description: >-
  Write, draft, edit, or review scientific prose for this thesis: a results paragraph, an abstract, a
  related-work or discussion section, or any edit to a docs/reports/R*.md report. Use it on the everyday
  cases ("write up X", "update R05", "add a paragraph on the gap", "draft the intro", "tighten this
  section") as much as the heavy ones ("consolidate the extended manuscript", "cut a public version",
  "review this section"). It keeps prose in a real scientific voice with no AI tells, makes every number
  trace to recorded evidence (the D011 rule), hedges by what was actually measured, and runs deterministic
  checks before a manuscript ships. Reach for it before writing, not after.
---

# Scientific Writing

The science is produced in working sessions and recorded in `docs/experiments/`, `docs/learnings.md`,
`docs/ladder.md`, `docs/decisions/`. This skill governs how that recorded evidence becomes written
argument across the three deliverable layers. It never invents a result. It shapes, checks, and routes
prose that already traces to evidence.

Two jobs run through everything here: make the prose read like a careful scientist wrote it, and make
every number defensible. The first job is mostly judgment with a deterministic floor (the linter); the
second is mostly mechanical (a number resolves to a record, or it does not).

## Pick the path first

Most writing in this repo is a small edit to a report. That case should stay cheap, or it gets skipped.

- **Fast path** (a one-paragraph add or a sentence fix in a `docs/reports/R*.md`): apply the style floor
  and the cite rule, nothing else. Run `scripts/ai_tell_lint.py` on the file, and make sure every number
  you wrote carries a cite (`[E0nn]`). Skip precommitment, the review pass, and the LaTeX checks. Two
  obligations, no ceremony.
- **Full loop** (writing or rewriting a whole section; consolidating the extended manuscript; cutting a
  public version): the loop below.

## The three layers (route, then read the spec)

The layer model, cadence, and triggers are defined once in `docs/03-methodology.md` ("Deliverable
layers"), which is the source of truth. Routing only:

| Layer | Where | Format | You touch it |
|---|---|---|---|
| Report | `docs/reports/R*.md` | Markdown | continuously, as work happens |
| Extended manuscript | `docs/manuscript/extended/` | LaTeX | at a checkpoint the user calls (fold into the paper body, append to the checkpoint log) |
| Public manuscript | `docs/manuscript/public/vN/` | LaTeX | at a submission milestone (compress the extended into a frozen cut) |

Knowledge flows down only: evidence into a report, report into the extended, extended into a public cut.
A number never enters at a lower layer than where it was recorded.

## Report scope and shape (the report layer — D036)

- **Scope = one durable claim, tagged with the question it answers — not a topic, a phase, or the whole arc.**
  A report owns exactly one finding (e.g. "the per-individual null + the averaging confound"), tagged with the
  ladder question(s) `Q0`–`Q5` it resolves. **Single-owner:** a claim lives in one report, so a new experiment
  updates one file, and the `Q → owning report` index (in `docs/map.md`) answers "which report for what" in one hop.
- **Current truth only — no chronological spoilers.** A report states what we believe *now*, rewritten in place.
  It does NOT narrate discovery order, mark a section "obsolete", or carry a "coverage frontier / not yet narrated".
  An overturned result is replaced by the current one; the *history* (the wrong turns, the order they happened)
  lives in `map.md` (the journey tree), `timeline/`, and `decisions/` — never as back-and-forth inside the synthesis.
- **Shape:** a one-line header (the claim + its current verdict + the `Q` it answers), then **question → design**
  (baselines, controls, stop rule) **→ evidence** (each number with its uncertainty and the named test) **→ verdict
  → caveats**. Caveats live *in* the claim sentence, not a footnote.
- **One exception — the teaching companion (`R05`).** R05 is deliberately a chronological narrative (the lesson is
  often in the wrong turn), so it may walk the arc in order. It is a learning aid, explicitly NOT the synthesis
  layer, and it still avoids the self-referential "frontier/obsolete" scaffolding.

## The full loop

1. **Check the results-prose standard.** Empirical prose has to report the effect with its uncertainty
   and the named test, on contiguous splits, with the nuisance or confound subtraction shown, over the
   recorded seeds. These are fixed repo standards, not per-section choices, so treat them as a checklist
   the section must satisfy rather than a ritual to perform first. (`references/provenance-d011.md`.)
2. **Draft from the evidence.** Tag every empirical claim with its source: `\evd{Ennn}`/`\evd{Lnnn}` in
   LaTeX, an inline `[E0nn]` in a report. A number you need but cannot source becomes a `\gap{...}`, never
   a guess. (`references/provenance-d011.md`.)
3. **Style sweep, silently.** Apply `references/writing-style.md` while drafting and once more before
   handoff. Fix what you find without narrating it and without reporting a score. The point is clarity and
   precision, not evading a detector.
4. **Verify.** Run `scripts/run_checks.py --layer <report|extended|public> <path>`. It dispatches the
   checks that apply to the layer and returns one exit code. A failure is a stop: fill the gap or fix the
   cite. Do not disable a check.
5. **Compression (public cut only).** Deriving a public `vN` from the extended drops depth, not claims or
   numbers. Cut derivations, mechanics, and the checkpoint log; keep every claim, its hedge level, and its
   number. `check_number_consistency.py` and `check_claim_survival.py` confirm nothing changed under you.
6. **Review (anything a supervisor or committee sees).** Run the Devil's-Advocate pass in
   `references/review-pass.md` before it lands.

## Five things that hold, and why

- **Every number traces to recorded evidence (D011).** The thesis rests on not inventing results, so an
  unsourced number is the one error that breaks credibility. That is why a number with no source becomes a
  `\gap{}` and why the verifier flags a bare number, not just a broken cite.
- **Hedge by what was measured.** A measured effect with its CI "demonstrates"; a correlational or
  assumption-dependent claim "suggests". Hedging a number you recorded understates your own evidence;
  upgrading an assumption to a result overstates it. Both are failures, so the verb tracks the evidence.
  Ladder and examples in `references/writing-style.md`.
- **One term per concept.** "Unique R²", "the trained−untrained gap", "the permuted twin": pick the term
  and repeat it. A reader tracking a precise quantity needs the same name each time; synonym-cycling reads
  as AI prose and leaks precision.
- **Compression preserves truth.** A public cut can keep every number and still drop a caveat or upgrade a
  "suggests" to a "demonstrates". Truth is the claims and their hedges, not only the digits, so the
  compression gate checks claims, not just numbers.
- **Internal codes are scaffolding, not prose, and they descend by layer.** The rung/experiment codes
  (`Q0–Q5`, `E0nn`, `A1–A3`, `D0nn`, `L0nn`; legend in `docs/map.md`) are the repo's working shorthand, not
  reader-facing language. **Reports** may use them freely. The **extended manuscript** is prose-first: a code
  appears only as a parenthetical pointer ("a well-powered per-individual null (E008)"), never as the subject
  of a sentence. The **public manuscript** carries **zero** codes — every result is named in prose ("a
  well-powered per-individual null"), because a reviewer must never need the repo to parse the paper.

## References (read the one that fits the moment)

- `references/writing-style.md`: read before any style sweep and before handoff. The anti-AI-tell rules
  (which are deterministic, which are judgment), the scientific-voice machinery (TEEL paragraphs, the
  graded-hedging ladder, tense by section, vague→precise), and the Clarity Test. Has a table of contents.
- `references/provenance-d011.md`: read the first time you tag a number or hit one you cannot source. The
  `\evd`/`\gap` conventions, the claim↔evidence orphan discipline, the keyed-numbers policy (which numbers
  go in `assets/numbers.tex` via `\result{}`), and the results-prose standard.
- `references/latex-conventions.md`: read when writing or consolidating an extended or public manuscript.
  The search-friendly source style (one sentence per line), the shared preamble and its semantic macros,
  the vendored-frozen-cut rule, and the build. Points to `docs/03-methodology.md` for the layer model.
- `references/review-pass.md`: read only for a section a supervisor or committee will see. The
  Devil's-Advocate three-lens review (internal validity, external validity, so-what) and the Clarity Test.

## Verifiers

Each script is a pure function over files: it prints findings and exits `0` (clean) or `1` (violations),
so they compose into one gate. Invoke them through the orchestrator; you rarely call one directly.

```
uv run python .claude/skills/scientific-writing/scripts/run_checks.py --layer report   docs/reports/R05_*.md
uv run python .claude/skills/scientific-writing/scripts/run_checks.py --layer extended docs/manuscript/extended/
uv run python .claude/skills/scientific-writing/scripts/run_checks.py --layer public   docs/manuscript/public/v1/
```

| Layer | Checks run |
|---|---|
| report | `ai_tell_lint`, `check_evd_resolution` (markdown `[E0nn]` mode) |
| extended | `ai_tell_lint`, `check_evd_resolution` (LaTeX `\evd` mode) |
| public | the above, plus `check_gap_survival`, `check_number_consistency`, `check_claim_survival` |

## Examples

A number with its source and a flagged gap:

```
Input:  The trained model beat the untrained control.
Output: The trained−untrained unique-R² gap was +0.021 [95% CI +0.0205, +0.0209], 95% of reliable
        voxels positive \evd{E006}. The per-individual effect, if any, is below \gap{per-subject MDE
        not yet recorded for this substrate}.
```

An AI-tell rewrite (clarity, not evasion):

```
Before: It is important to note that our comprehensive analysis delves into the multifaceted and
        nuanced ways in which alignment plays a crucial role — a testament to the robustness of the
        signal.
After:  Alignment survives the full nuisance regression on real fMRI (E006), so the signal is not an
        artifact of length or rate.
```

## What this skill does not do

It does not produce evidence, and it does not adjudicate a hypothesis or flip a ladder rung. Those are a
working session and the user's call. It writes, checks, and routes prose that already traces to evidence.
