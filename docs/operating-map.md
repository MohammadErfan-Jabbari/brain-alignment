# Operating map — how to work in this repo

This is the day-to-day picture of how Erfan and the agent work together. It replaces the old
working/analysis session split (D044). You no longer declare a session "mode"; you **invoke a stance**
when you want one, and switch freely as the work turns. The mechanics live in the `stances` skill
(`.claude/skills/stances/`); this page is the human-facing version.

## A session is bracketed, not typed

- **Open with `/orient`** (where we are, the single next step, what stance it suggests).
- **Work in stances** (below). Switch any time; the agent states the stance it is in.
- **Close with `/wrap`** (logs which stances ran and what each produced, sets the next-session stance).

## The eight stances

| Invoke | When you want to... | How it behaves | Touches a number? |
|---|---|---|---|
| `/work` | run an experiment and get a verdict-grade result | high autonomy, long `/goal` runs; locks design, runs, judges | yes (produces) |
| `/interpret` | decide what a result means | pins a claim-manifest, re-computes the contrast, runs the panel | yes (adjudicates) |
| `/write` | turn a settled finding into report or manuscript prose | the `scientific-writing` skill; verdict-first, cite-or-flag | reports them |
| `/teach` | understand a finding deeply (your own work) | a guided-learning crawl over a report, one question at a time | reads them |
| `/scout` | bring in outside papers or datasets | `lit-scout` / `dataset-scout` / `paper-digest` to canonical notes | external evidence |
| `/plan` | decide what to do next | roadmap, kill-gate triage, sequencing | no |
| `/review` | stress-test a result, claim, or design | the thinking panel + Codex on demand | no |
| `/meta` | improve the apparatus | tooling, methodology, record maintenance | no |

The dividing line is **does the stance touch a science number.** `/work` and `/interpret` produce or
adjudicate numbers, so they carry the strict standard (kill criteria, ≥3 seeds, strict adjudication).
`/write`, `/teach`, `/scout` report or consume numbers under the cite-or-flag rule. `/plan` and `/meta`
touch none.

## Invoking

- Type `/teach`, `/interpret`, `/write`, `/scout`, `/plan`, `/review`, `/meta` to force a stance.
- Or just talk: the agent infers the stance, **states it** ("Entering /teach on R07"), and you can
  redirect. `/work` is the exception: it is explicit-only, so a heavy run never fires from a remark.
- Switching mid-session is normal. A `/teach` walk that hits a hole can switch to `/interpret`; the
  agent names the switch.

## The honesty spine (always on, independent of stance)

The thesis rests on never inventing a result. A number is born in a `/work` session and recorded in
`docs/`; no stance may state a result that was not recorded; a needed-but-missing number is a `\gap`,
never a guess. This is enforced by a **write-time hook** (not by remembering a rule): any write to
`docs/reports/` or `docs/manuscript/` (the prose deliverables) is checked, and an unsourced result-like
number is flagged. The `/wrap` provenance audit is the backstop. (The ladder/learnings/experiments docs
reference results by bare code, so they are not checked this way — L052.)

## The report → teach loop (the common path)

1. A `Q` rung is ready. Say "write the report for Qi."
2. `/write` produces the finding-report (verdict-first, with a plain-language lead).
3. Invoke `/teach` **before reading it**. It renders the report simple-first and walks you through, one
   question at a time, anchored to the report's real numbers, and logs what you master to the learning
   ledger (`docs/learning/`).

## How `/teach` remembers

`/teach` keeps a learning ledger at `docs/learning/NNNN-*.md`: one record per thing you demonstrably
master, anchored to the report and the number it concerns. It writes a record only on demonstrated
mastery, never on coverage. On a later session it re-reads the ledger to know what to skip and what to
teach next. Four sub-modes: `guided` (Socratic crawl, default), `walkthrough` (faster), `feynman` (you
teach it back), `drill` (it quizzes you).
