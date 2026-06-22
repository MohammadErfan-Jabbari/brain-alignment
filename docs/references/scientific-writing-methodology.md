# Scientific-writing methodology — the established body of practice

Research pass (2026-06-22, `/meta`, S35) for the `/write` + `scientific-writing` redesign. Question Erfan
posed: is there a well-regarded methodology for *writing a scientific paper* — beyond the surface mechanics
(em-dashes, register tells) the current apparatus polices — that `/write` could be rebuilt on, so he stops
having to check every line because he can't trust the prose?

**Answer: yes, and it is unusually convergent.** There is no single branded "method," but ~6 canonical
sources, written independently across decades and fields, agree on the same core. The agreement is the
finding. Almost none of it is about word choice; it is about **structure and reader-processing at every
scale**, plus a **process** (structure before prose). This is exactly the positive model the current
apparatus lacks — it built a defect detector ("immune system"), never a model of health.

---

## The canonical sources

| Source | The core claim | Operational core |
|---|---|---|
| **Gopen & Swan, "The Science of Scientific Writing"** (American Scientist, 1990) | Readers interpret prose using its *structure*, not just its words. Writing quality = does the structure match where the reader expects meaning. | **Topic position** (sentence start) = old/linking info; **stress position** (sentence end) = the new info to emphasize. Subject→verb fast. One unit = one point. |
| **Williams, "Style: Lessons in Clarity and Grace"** | Clarity and cohesion are *derivable*, not taste. Same reader-processing basis as Gopen-Swan, fuller. | **Given-new contract** (old-to-new is the #1 cohesion principle); characters→subjects, actions→verbs; consistent **topic strings** down a paragraph; each paragraph has one **point sentence**. |
| **McEnerney, "The Craft of Writing Effectively"** (UChicago) | Writing's job is not to explain your thinking; it is to deliver **value to a community of expert readers**. Value is defined by *them*, not you. | Open with what the reader *needs / is wrong about*, not "here's what this paper is about." Know the community's value-words and its current doubts. |
| **Mensh & Kording, "Ten Simple Rules for Structuring Papers"** (PLOS Comp Biol, 2017) | A paper is a story built on **one central contribution**, told in a **fractal** structure. | **Context–Content–Conclusion (C-C-C)** at *every* scale: whole paper, each section, each paragraph. One paper = one message. The funnel/hourglass. |
| **Schimel, "Writing Science"** | A paper is a **story** with narrative structure; readers fund/cite what they can follow and retell. | **OCAR** (Opening, Challenge, Action, Resolution) — an hourglass where Opening-width must equal Resolution-width (else over/under-claim). Drives IMRaD (Intro=OC, Methods/Results=A, Discussion=R). Make it Simple, Unexpected, Concrete. |
| **Whitesides, "Writing a Paper"** + **Osuji "skeleton"** | Writing is **part of the research, not a post-step**. Outline first to manage the work. | Build a data+claims **outline/skeleton first**; write the opening paragraph in full early; organize **by importance, not chronology**; cut history-of-struggles; shorter is always better. |
| **Swales, CARS model** ("Create A Research Space") | Introductions follow a fixed **3-move** rhetorical pattern. | Move 1 establish the **territory** → Move 2 establish the **niche** (the gap/flaw/question) → Move 3 **occupy** it (this work). Our manuscript's "empty cell" is a Move-2 niche. |
| **Booth/Colomb/Williams, "The Craft of Research"** | A research argument has a fixed **skeleton of parts**. | **Claim ← Reasons ← Evidence**, plus **Acknowledgment/response** to other views, plus the **Warrant** (why the reason bears on the claim). A paragraph or section is checkable against these slots. |

---

## What they converge on (the positive model)

1. **Reader-expectation is the foundation, and it is mechanistic, not taste.** Gopen-Swan, Williams, McEnerney
   all say the same thing: a sentence/paragraph is clear when its *structure* puts old before new, topic before
   stress, character-as-subject, action-as-verb, and one-point-per-unit. These are checkable conditions, not
   opinions. Most "this reads badly" reactions are *violations of these*, not failures of flair.

2. **Structure is fractal and identical at every scale.** Context→Content→Conclusion / OCAR / hourglass holds
   for the whole paper, each section, and each paragraph (Mensh-Kording, Schimel). So a paragraph can be audited
   the same way a paper can: does it open with context, deliver content, close on a conclusion that links forward?

3. **One paper, one message.** Both Schimel and Mensh-Kording insist the paper exists to land a single central
   contribution; everything is subordinate. The message must be stateable in one sentence *before* drafting.

4. **Value to the reader, not a dump of what you did.** McEnerney (and Whitesides' "who cares?") — the writer's
   instinct is to narrate their process; the reader wants the contribution and why it matters to *their*
   conversation. "Leave out the history of your struggles."

5. **Structure before prose, and writing manages the research.** Whitesides, Schimel's "key story points"
   exercise, Osuji's skeleton: you lock the outline/message/skeleton *first*; prose is the last step and is
   constrained by the locked structure. This is the single biggest process lever.

6. **Fixed templates exist for the hard parts.** Intros → CARS 3 moves. Arguments → claim/reason/evidence/
   warrant/acknowledgment. These are slot-fillers an agent can check for completeness.

---

## Why this solves the trust problem

The reason Erfan reads every line is that the current `/write` only checks the **lexical floor** (tells,
em-dashes, register) and has no notion of whether the *structure* is right. But the methodologies above show
that **most of what he catches by reading is structural, and structure is checkable**:

- "this opening has no taste / no stakes" → CARS Move-2 / McEnerney value-open is missing → **checkable**.
- "what is this 60-word sentence doing?" → one-unit-one-point violated; stress position buried → **checkable**.
- "this paragraph is unclear" → old-to-new / topic-string / point-sentence broken → **checkable**.
- "why are full CIs in the abstract?" → layer-convention violation → **checkable** (already partly known).

So the genuinely subjective residual ("taste") is **small** once structure is enforced — register, rhythm,
the quality of the opening line. That residual is where exemplars + an opus taste-reader earn their place. The
redesign that follows from this: **make `/write` structure-first**, with a layered check stack —

1. **Structural conformance** (the bulk, near-objective): message-in-one-sentence locked; C-C-C / OCAR at each
   scale; CARS for intros; argument slots filled; old-to-new + point-sentence per paragraph.
2. **Exemplar-matched register** (the residual taste): draft against real venue exemplars + opus taste-reader.
3. **Defect floor** (what exists today): `ai_tell_lint` + `prose-register-auditor`, demoted to a floor.

And the human gate moves: **Erfan approves the locked structure/skeleton (cheap, high-leverage), not the prose
line-by-line.** If the structure is right and the floor is clean, the prose is trustworthy by construction.

---

## Primary sources (for deep-read if we build on this)

- Gopen & Swan 1990 — https://www.americanscientist.org/blog/the-long-view/the-science-of-scientific-writing (PDF mirror: gatsby.ucl.ac.uk/~pel/misc/gopen_swan.pdf)
- Mensh & Kording 2017, *Ten Simple Rules for Structuring Papers* — https://pmc.ncbi.nlm.nih.gov/articles/PMC5619685/
- Schimel, *Writing Science* (2012, OUP) — book
- Williams & Bizup, *Style: Lessons in Clarity and Grace* — book
- McEnerney, *The Craft of Writing Effectively* (UChicago lecture) — https://www.youtube.com/watch?v=vtIzMaLkCaM
- Whitesides 2004, *Writing a Paper* (Adv. Mater.) — https://www.chemistry.nat.fau.eu/files/2019/07/whitesides.pdf
- Swales CARS — https://en.wikipedia.org/wiki/CARS_model ; usc.edu writing guide
- Booth/Colomb/Williams, *The Craft of Research* — book
