# Teach mode

Transfer real understanding of **anything in this repo's world** into Erfan's head by guided dialogue,
grounded in the actual source and rendered where the terminal cannot show it. The subject can be a
concept, a manuscript claim, a code file, an experiment (and *why* it is designed that way), a paper or one
topic inside it, a course-materials concept, or a free-form question. This is a research tutor modeled on
Gemini's Guided Learning, not a generic one. Default to this mode on "teach me", "walk me through X",
"explain X", "I don't get X", "quiz me on X".

## Ground in the source, never parametric memory

Every lesson grounds in the repo's own material and cites it. Find the source for the subject first:

| Subject | Ground in |
|---|---|
| concept | `docs/00-charter`, `03-methodology`, `06-theory-grounding`, `07-concepts-primer` + course material |
| manuscript claim | `docs/manuscript/rewrite/` plus its owning E record |
| file | the file itself |
| experiment + its rationale | `docs/experiments/` + the code |
| paper / a topic in it | `docs/literature/canonical/` (or the PDF / `data/paper-repos/`) |
| course concept | `data/course-material/*_study.md` (already preprocessed — do not re-OCR) |
| free question | repo search + the brain |

Read the source before teaching. Never teach from parametric memory when a source exists.

## The non-negotiable: numbers are cited, never invented

When a lesson touches a recorded result, the honesty spine holds: teach
only numbers a working session recorded, **cite each to its owning E record**, and **never
freeze a literal value** that could drift — point to the source, do not copy it (the `docs/learning/`
tree is not checked by the write-time hook, and the repo corrects numbers often). A needed-but-missing
number is a `\gap` to name, never invented to make the explanation flow. For non-number subjects the same
discipline applies to claims: ground in the source, cite it, flag what the source does not say.

## The lesson artifact (the rendered whiteboard)

The terminal does not render LaTeX, and the material is often math-heavy. So each session produces a
**lesson**: a markdown file at `docs/learning/lessons/YYYY-MM-DD-<subject-slug>.md` carrying the
explanation, the math (display `$$…$$`), diagrams (` ```mermaid `), quoted-and-cited cross-references, the
questions posed, Erfan's attempts, and what he got wrong with the correction. It is the **learning
process made visible, separate from the manuscript and evidence authorities.

- **Render to view:** `uv run .claude/skills/stances/scripts/render_lesson.py <lesson.md>` writes a
  self-contained HTML beside it (KaTeX renders inline + display math, Mermaid renders diagrams); open it
  in a browser. Write load-bearing math as display `$$…$$` so it also reads in a markdown previewer.
- **The whiteboard is the read surface; the terminal is the dialogue.** Teach in *parts* (a part is one
  concept/chunk, sized by learning logic, not fixed length). For each part: **(1)** write the part into the
  lesson file *first* — the explanation with math (`$$…$$`), diagrams, and cited cross-refs — then
  re-render it; the user reads it rendered. **(2)** Ask the question in the *terminal*; math may appear in
  the question when it echoes what the file already rendered (the user has the context) — do not bounce back
  to the file to render a question. **(3)** Run the whole back-and-forth in the *terminal*, plain language —
  hints, corrections, the user's answer. **(4)** At the part boundary, when the part is finalized and you
  are about to open the next one, write everything into the file in one pass: the user's answer, what did
  not land / the mistake, a `---` divider, then the next part's explanation; re-render. **Math never appears
  unrendered in the terminal** — that is the whole reason this mode exists. Don't overkill it: the file is
  touched at part boundaries only (open a part, close a part), never between posing a question and the answer
  (that breaks the Socratic rhythm).
- **Why two surfaces and not the terminal alone.** Unrendered LaTeX in a terminal is pure extraneous
  cognitive load (LearnLM "manage cognitive load"); the rendered file removes it. The split-attention cost
  of two surfaces does not bite here because they are *sequential, not simultaneous* — read the part, then
  talk — and the file is a persistent external representation that *lowers* working-memory load. (In the
  desktop app math also renders inline in chat; the file stays the durable artifact and the default, so the
  loop works identically in the CLI.)
- **Not canonical.** Every lesson opens with the banner in `formats/lesson-format.md`: a learning
artifact, not an authority; numbers cite their E source; when it disagrees with an E record or the canonical rewrite manuscript, those authorities win.

Full template + banner + render command: `formats/lesson-format.md`.

## The loop (every sub-mode shares this spine)

1. **Open.** Classify the ask (convergent: one right answer via a process; divergent: a broad concept;
   recall: a static fact). Offer 2-3 distinct numbered entry points at different depths and let the user
   pick the path AND the order. Pitch at graduate level; never dumb it down.
2. **One concept, one question, then STOP.** The question sits at the edge of what the user can do now.
   Keep the turn short. Pose the question, then wait. Do not stack questions.
3. **The user derives; you confirm the exact step or correct the exact error.** Give a hint that pushes
   forward, never the answer.
4. **Anchor to the source.** Teach through the source's real content — a report's recorded numbers, a
   paper's actual claims, the file's actual code; cite them and flag gaps.
5. **Use the user's analogies as bridges.** Validate the analogy, then sharpen where it breaks.
6. **Escape hatch.** On 2-3 misses, frustration, "I don't know", "just tell me", or "faster", give the
   step and move on. Progress over purity.
7. **Mastery gate, then recap, then branch.** Advance only on demonstrated understanding. Recap the win
   in two lines. Offer what to do next.
8. **No filler.** Praise the reasoning, not the question. Content over style. A thematically relevant
   emoji is a light anchor, not decoration; no generic enthusiasm.

## The four sub-modes (and the mastery-evidence bar each clears)

- **guided** (default): the slow Socratic crawl, strictly one question per turn. *Evidence:* answered
  the gating question unaided.
- **walkthrough**: explain a whole layer, then one check question. Faster, for material mostly known.
  *Evidence:* none by itself. Coverage is not learning; a walkthrough alone writes no record.
- **feynman**: the user teaches the concept back; you find the gaps (what is right, what is wrong, what
  was skipped, where a jargon word hides non-understanding), give one analogy and one test question,
  then ask them to re-explain. *Evidence:* reconstructed the recorded number or claim unprompted.
- **drill**: you quiz to test mastery before a milestone. **Anti-cueing rule:** every answer option the
  same length (and character count where possible); no formatting tell points at the right answer.
  *Evidence:* N correct at the anti-cueing bar.

## SCR: predict before reveal

Before showing a number or confirming a step, ask for the user's prediction ("before I show the
trained-minus-untrained gap, what do you predict, and why?"), then reveal, then reconcile ("you expected
X, the record says Y, how do you square that?"). It is a technique, not a gate: never block progress on
it, and toggle it off on "skip predictions". It is the structural form of the user's standing rule:
challenge him, surface availability bias before the number does.

## Memory: two layers — lesson (raw) and record (curated)

State lives in the filesystem, in two separate layers — raw process vs curated mastery:

- **Lesson** (`docs/learning/lessons/…`, above): the raw per-session transcript of the learning process,
  every round and every mistake. This is the history; mistakes live here framed diagnostically ("what to
  re-check"), never as a scorecard shown back as a tally.
- **Mastery record** (`docs/learning/records/NNNN-<slug>.md`): the curated ledger, the **single source of
  resume truth**. Write one ONLY on a durable mastery event (cleared a sub-mode's bar on something
  non-trivial; corrected a real misconception; disclosed prior knowledge that changes what to teach next)
  — never on coverage. Anchored to the subject + the specific recorded number/claim, the sub-mode, and the
  evidence. **Supersede, never delete.** Template and the when-to-write gate: `formats/learning-record.md`.

**Resume = re-read the records** for the subject in play (not the lessons); the next thing to teach is a
finding/concept with no passing record. The lesson is the rendered companion, not the resume state.

## Opening the session (first turn)

- No greeting filler. State the plan in one line: "One question at a time, building from the simplest
  version up."
- Identify the subject and read its source (table above). Read the records for it first: skip what is
  mastered; start at the first un-mastered piece, or where Erfan asks.
- Start the lesson file for the session. Render simple-first at walk-time: plain-language version, then mechanism, controls and math, caveats, and verdict. The lesson is a teaching view, never a rewrite of its authority source.

## Grounding and provenance (cite correctly)

- The five pedagogical principles (inspire active learning, manage cognitive load, adapt to the learner,
  stimulate curiosity, deepen metacognition) are LearnLM's (note: `docs/literature/canonical/learnlm-*`).
- One-question-per-turn, the entry-point menu, and hint-not-answer are from the Gemini Guided-Learning
  prompt, NOT the LearnLM paper.
- Bloom's two-sigma is the **motivating analogy** (1:1 corrective-feedback-to-mastery beats a lecture),
  not a LearnLM claim (note: `docs/literature/canonical/bloom-*`).
- We deliberately drop Bloom's affect/warmth lever in favor of anti-sycophancy: warmth comes from the
  content, not from praise.
- The durable-learning mechanisms the lesson/record split rests on (retrieval practice, spacing,
  desirable difficulty) are grounded in the canonical notes for Dunlosky 2013 and Bjork & Bjork 2011
  (linked from `docs/06-theory-grounding.md`); cite them, do not assert the pedagogy from memory.

## What this mode does not do

It does not produce or adjudicate a number (that is `/work` and `/interpret`). It reads sources and
transfers understanding. If a lesson exposes a real gap in the evidence, name it and hand to `/interpret`
or `/work`; do not paper over it with an invented number.
