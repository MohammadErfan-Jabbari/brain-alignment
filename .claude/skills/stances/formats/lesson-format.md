# Lesson format (the teach whiteboard)

A **lesson** is the rendered learning surface for one `/teach` session: a markdown file at
`docs/learning/lessons/YYYY-MM-DD-<subject-slug>.md` carrying the explanation, the math, diagrams, cited
cross-references, the questions posed, Erfan's attempts, and his mistakes with the correction. It is the
**learning process made visible**, kept here so it stays out of the reports — the firewall R05's
retirement taught us to build (a learning narrative must never leak into a report).

It is the RAW layer. The curated mastery state lives separately in `docs/learning/records/`
(`learning-record.md`); the lesson is never the resume source of truth.

## Render to view

The terminal does not render LaTeX. To see the math and diagrams:

    uv run .claude/skills/stances/scripts/render_lesson.py docs/learning/lessons/<file>.md

writes `<file>.html` beside it — open it in a browser (KaTeX renders `$…$` and `$$…$$`, Mermaid renders
` ```mermaid ` blocks; both load from a CDN, so the browser needs internet). Write load-bearing math as
display `$$…$$` so it also reads in a plain markdown previewer without the render step.

## The non-canonical banner (every lesson opens with this, verbatim)

> **Learning artifact — not canonical, not a report.** This is the process record of a teaching session.
> Every number is cited to its source by code; nothing here is a source of truth. When this disagrees
> with `ladder.md` or a finding-report, they win.

## Template

```markdown
---
subject: <concept | report Rxx | file path | experiment Exxx | paper slug | question>
mode: guided | walkthrough | feynman | drill
date: YYYY-MM-DD
sources: [<the repo files this grounds in, by path/code>]
---

> **Learning artifact — not canonical, not a report.** (banner above, verbatim)

# {Subject}

{Plain-language version first: the one-paragraph "what this is and why it matters", caveat included.}

---

## Round 1 — {the concept this round}

{Explanation: prose + display math $$…$$ + a ```mermaid diagram + quoted, cited cross-refs.}

**Question.** {the question; math allowed here}

**Your answer.** {recorded after he responds}

**Where it landed.** {what was right · what was missed · the mistake · the correction — diagnostic, not a grade}

---

## Round 2 — …
```

## Rules

- **Cite, do not cache.** Every recorded number points to its source by code (R07 / E0nn), never a
  frozen literal — `docs/learning/` is not checked by the write-time honesty hook and source numbers move.
- **Write at boundaries.** Update the lesson at the end of a round/concept or at session end, never
  between posing a question and getting the answer (it breaks the Socratic rhythm).
- **Mistakes are diagnostic.** Record what was missed and the correction as "what to re-check", never as
  an accumulating scorecard. The durable, forward-looking version goes in a mastery record only when it
  clears the gate (`learning-record.md`).
- **One lesson per session.** A new session on the same subject is a new dated file; the history is the
  set of files. The compact resume index is the records layer, not these.
