# Writing style: scientific voice and the anti-AI-tell rules

The aim is clear, precise, varied academic prose. It is not to fool an AI detector. Every rule here
earns its place by making the writing easier to trust and easier to read, not by disguising authorship.
Apply the rules while drafting and once more before handoff, and fix what you find without narrating it.

Two kinds of rule live here. The **deterministic** ones are enforced by `scripts/ai_tell_lint.py`; you
do not need to remember them, but you should understand them so you stop producing the tell in the first
place. The **judgment** ones cannot be greppable; they are yours to apply and the review pass double
checks them. Each rule below is tagged `[linter]` or `[judgment]`.

## Contents

1. Anti-AI-tell rules (the tells, and why each is a tell)
2. Scientific voice (paragraph shape, tense, precision, register, presenting a measured quantity, the reader-comprehension floor)
3. Graded hedging tied to the evidence (C2)
4. The Clarity Test and non-uniform investment
5. Running the sweep

---

## 1. Anti-AI-tell rules

### Deterministic (the linter catches these; learn them so you stop emitting them)

- **Em-dash budget `[linter]`.** Keep it near zero, three at most per document. LLM prose reaches for the
  em-dash on every parenthetical aside. A comma, a parenthesis, or a full stop almost always reads better.
  Quoted text keeps its original punctuation.
- **Filler and impressive-by-default words `[linter]`.** `delve, leverage, pivotal, crucial, foster,
  showcase, testament, realm, embark, underscore, multifaceted, nuanced, intricate, cornerstone, paradigm,
  synergy, holistic, streamline, cutting-edge, groundbreaking, tapestry`, and `comprehensive`. The fix is
  not a synonym, it is precision: say what you mean. `robust` is fine in its statistical sense (a robust
  estimator), flagged otherwise.
- **Throat-clearing openers `[linter]`.** "It is important to note that", "It is worth noting", "In the
  realm of", "In today's rapidly evolving", "Needless to say", "With that said", "When it comes to". Delete
  the opener and state the sentence.
- **Meta-commentary `[linter]`.** "In this section we will", "This section will discuss", "We now turn our
  attention to". Just discuss it. The one exception is an Introduction roadmap ("Section 2 reviews ..."),
  which is a real convention.
- **Wordiness `[linter]`.** "in order to" becomes "to"; "due to the fact that" becomes "because"; "has the
  ability to" becomes "can"; "a large number of" becomes "many". Shorter is clearer.

### Judgment (yours to apply; the review pass double checks)

- **Burstiness `[judgment]`.** If five or more sentences in a row sit in a narrow length band, the prose
  reads as machine-flat. Break it with a short sentence. Methods sections are allowed to be uniform; the
  Discussion should vary most.
- **One term per concept `[judgment]`.** This is the rule that fights generic "vary your wording" advice,
  and for technical prose the generic advice is wrong. Pick one name for a quantity ("unique R²", "the
  trained minus untrained gap", "the permuted twin") and repeat it. A reader tracking a precise object
  needs the same handle each time. Synonym-cycling reads as AI prose and leaks precision.
- **No forced rule of three `[judgment]`.** Two strong points beat three padded ones. Do not pad a list to
  three for rhythm.
- **Vary paragraph length `[judgment]`.** A two-sentence paragraph after a ten-sentence one creates rhythm.
  Uniform paragraph length is a tell and a sign that every paragraph was given equal weight (see section 4).
- **Binary-contrast tic `[judgment]`.** "Not X. Y." and "It is not about X, it is about Y." are fine once or
  twice; a paper full of them is a tell.

---

## 2. Scientific voice

- **TEEL paragraph shape `[judgment]`.** Most body paragraphs follow Topic (one sentence), Evidence (two or
  three sentences, cited), Explanation (one or two sentences where you do the analytical work, not just
  restate the data), Link (one sentence of transition). Introduction-first and Conclusion-last paragraphs
  are exempt. The Explanation move is what separates a scientist from a summarizer: say what the evidence
  means, not only what it is.
- **Tense by section `[judgment]`.** Prior findings and your own methods and results are past tense ("the
  gap was +0.021", "we held out whole stories"). Standing theory and interpretation are present ("averaging
  raises the noise ceiling"). The Conclusion may use present or future.
- **Vague to precise `[judgment]`.** "many studies" becomes "several studies (e.g., Hadidi 2024)"; "a
  significant impact" becomes the number; "in recent years" becomes a date range; "some researchers"
  becomes their names. A reader cannot check a vague claim.
- **Let topic sentences carry the flow `[judgment]`.** Reach for an explicit transition word ("however",
  "moreover") only when the relationship between paragraphs is genuinely non-obvious. Most of the time the
  topic sentence does the work, and a transition word on top is scaffolding.
- **Register.** This is a sciences/ML thesis, so impersonal phrasing and the passive are acceptable where
  they read naturally. Do not force "We argue" into a methods description that wants "The encoder was fit".

### Presenting a measured quantity: estimand → estimator → identifying assumption `[judgment]`

When a section is built on a metric, do not let the metric stand in for the thing you actually care about.
Open with the target quantity, then the measurement, then the condition that ties them. This three-move
spine is the **estimand-first** discipline from statistics and causal inference (the ICH E9(R1) estimand
framework; Hernán and Pearl's "define the target quantity before you estimate it"). The three moves:

- **Estimand first.** Name the population quantity you want, before any procedure: *what we are after*.
  (R06: the conditional mutual information $I(\text{LM};B\mid Z)$.)
- **Estimator second.** Give the concrete procedure that measures it: *how we measure it*. (R06: unique R²
  from cross-validated ridge.)
- **Identifying assumption third.** State the condition under which the estimator recovers the estimand:
  *when the two coincide*. (R06: joint Gaussianity / linearity, which makes unique R² a monotone function
  of the conditional mutual information.) The resulting number is the *estimate*.
- **Plain-language version.** The non-fancy name for getting this right is **operationalization** and
  **construct validity**: does the measure actually map to the construct it claims? The expository
  direction is **concrete-to-abstract grounding**: start from the thing you can compute, then lift it to
  the principle.

Two lenses that sharpen the same move:

- **Marr's three levels of analysis `[judgment]`.** Marr separates the **computational level** (what is
  being computed, and why: the estimand) from the **algorithmic level** (the representation and procedure:
  the estimator); the third, the **implementational level** (the physical substrate), is rarely relevant
  here. Reach for this vocabulary when separating "what we measure" from "what it means" earns its keep;
  skip it when it is overhead.
- **The characterization move `[judgment]`.** When a metric is provably *equal* to a principled quantity,
  state the equality as a small result, a **characterization** (equivalently an **equivalence** or
  **representation result**), not as an analogy. The schema is "metric $M$ equals principled quantity $Q$
  under stated conditions, so a positive $M$ is exactly a positive $Q$"; the weak version, "$M$ is like
  $Q$", earns nothing. It is the "it is secretly $X$" unification move: lead with the familiar object, then
  reveal the deeper one it instantiates. **Assert the equality only at the strength the math actually
  licenses** — an exact identity, a monotone relation, and a shared sign are three different claims, and
  using the wrong one (writing "exactly equals" where only a shared sign holds) is a correctness error, not
  a style choice. The examples in this skill illustrate the *move*, not vetted domain facts: never lift a
  specific equation from an example into your prose without re-deriving it for your own case.

- **Vocabulary, use the exact term (ties "one term per concept").** Reach for the precise name so the
  reader tracks a single object across the section:
  - **semipartial (part) correlation** for the variance an added regressor contributes beyond a baseline;
    its square is the raw increment $R^2([Z,X]) - R^2([Z])$, the **incremental R²** (what this repo calls
    *unique R²*). The **partial correlation** $\rho_{XY\cdot Z}$ is the normalized version, differing by the
    factor $1/(1-R^2([Z]))$; the two share a sign and vanish together but are not equal (L045);
  - **Gaussian mutual information** for the closed form $-\tfrac{1}{2}\ln(1-\rho^2)$;
  - **Reichenbach's common-cause principle** for "two variables are dependent because they share a parent",
    and its conditional-independence form **d-separation** (the applied phrasing is **controlling for a
    confounder**).

The worked exemplar is R06's "The design (and the apparatus the whole program reuses)": estimand
$I(\text{LM};B\mid Z_{\text{nuis}})$, estimator unique R² via ridge, identifying assumption Gaussianity,
with the common-cause logic naming why conditioning on $Z$ is the whole point.

### Reader-comprehension floor `[judgment]`

The rules above make prose precise and unflashy; these four make it *resolvable on a first read*. They are
the floor a reader needs to follow the argument without stopping to ask, and each was a real miss caught
late on R06 (L046). They are graded by the layer's named audience (`03-methodology.md`, "Deliverable
layers"): define for the reader you actually have, do not over-define for one you don't.

- **Define on first use.** Every acronym and domain term is expanded or glossed at its first occurrence
  ("BOLD = blood-oxygen-level-dependent signal"; "TR = repetition time"), at the level the audience needs:
  a report or extended manuscript for a supervisor defines fMRI terms an outside reader would miss; a cut
  for an fMRI committee does not gloss BOLD. In a multi-section manuscript, "first use" is **document-wide**,
  not per-section, and a recurring term also gets a glossary/notation entry (latex-conventions.md). The rule
  that the central construct is formalized (SKILL.md) covers *your* objects; this rule covers the *borrowed*
  terms that rule does not reach.
- **Motivate every non-obvious method choice.** A feature-construction or preprocessing choice a reader
  could reasonably question (a pooling rule, a resampling kernel, a threshold, a delay count) carries a
  one-clause "why this, and not the obvious alternative", with a prior-art cite where one exists. If the
  working session never recorded the rationale, that is a `\gap{rationale for X not recorded}`, not a
  sentence written from guesswork — the writing layer never invents a justification (D011). Recording the
  why at choice-time is a working-session obligation (`03-methodology.md`).
- **Table a genuine comparison.** When three or more comparable numbers vary across conditions (models ×
  metric, arms × effect), present them as a table, not an inline list the reader has to assemble mentally.
  The exception is a single headline effect with its CI and test, which stays inline ("the gap was +0.021
  [CI …], 95% of voxels positive") — do not tabularize one result for its own sake.
- **Show the formula only when it pins something down.** The core construct gets prose *and* display math.
  A secondary relation gets a formula when the reader must verify the algebra (an identity, a cancellation),
  and gets prose when a term merely supports or cancels ("the nuisance term is identical in both arms, so it
  drops out of the difference") — do not render a wall of symbols the prose already states, and do not
  gesture at math you never write.

---

## 3. Graded hedging tied to the evidence (C2)

The hedge verb must track what the evidence actually supports. This is the single rule that prevents both
AI over-hedging and scientific over-claiming, and it is wired to D011: the strength of the verb is set by
what a working session recorded, not by reflex.

| Evidence in hand | Verb | Example |
|---|---|---|
| A measured effect with its CI and named test | **demonstrates / establishes / shows** | "E006 demonstrates a +0.021 trained minus untrained gap [CI ...]" |
| A consistent but correlational or indirect pattern | **suggests / indicates / is consistent with** | "the cross-family law suggests alignment tracks quality" |
| A claim resting on an assumption, not a result | **would imply / under the assumption that** | "under Y ⊥ θ* | S, the residual would carry no task signal" |

Two hard edges:

- **Never hedge a number you recorded.** Write "the gap was +0.021", not "the gap appeared to be roughly
  +0.021". Hedging your own measurement understates your evidence and reads as AI uncertainty-padding.
- **Never upgrade an assumption to a result.** If the claim depends on Y ⊥ θ* | S, say so in the sentence.
  Promoting it to "demonstrates" is the over-claim the whole thesis is built to avoid.

When the evidence and the verb disagree, the evidence wins: change the verb, not the number.

---

## 4. The Clarity Test and non-uniform investment

The test has two halves, and a paragraph must pass both. **Necessity:** if I delete this, does the section
still make sense? **Sufficiency:** if I keep it, can a first-time reader parse it in a single pass?
Necessity decides what stays; sufficiency decides whether what stays is legible. The two are independent —
a paragraph can be load-bearing (necessity says keep) and still unreadable (sufficiency says fix), which is
exactly the dense sentence that makes a reader stop and reconstruct your logic for themselves. Run both.

The necessity half has three outcomes:

- **Delete.** Nothing is lost. Cut it.
- **Compress.** It supports but does not carry. Two sentences, not ten.
- **Invest.** It is load-bearing (the averaging-confound mechanism, the per-individual null). Draft it
  several times until it is exact *and* one-pass-readable. Investing means **unpacking** the logic into
  ordered steps, one inferential hop per sentence — not packing more clauses into a single sentence. A
  sentence that chains "A, so B by construction, and C throughout" is three sentences trying to be one;
  split it. (Density on a load-bearing sentence is the failure the sufficiency half exists to catch.)

Most AI prose fails this test because every paragraph gets equal weight, which produces the uniform-length
tell from section 1. Varying your investment by what the paragraph carries fixes the rhythm as a side
effect, and it puts your effort where the argument lives.

A companion question for ordering: each section answers one reader question. Introduction, why care.
Related work, what is missing. Methods, can I trust this. Results, what did you find (lead with the
finding, not the test). Discussion, what does it mean. Conclusion, what should I remember.

---

## 5. Running the sweep

Apply sections 1 to 4 while drafting each section, then once more across the whole piece before handoff.
Run `scripts/ai_tell_lint.py` on the file to catch the deterministic tells you missed. Fix everything
silently: do not announce the fixes and do not report a "style score" to the user. Score the violations to
yourself only as a sense of how clean a section is (zero is clean, a handful is minor, many means the
section's approach needs a rethink), and act on it without surfacing the number. The reader should see good
prose, not a changelog of the tells you removed.
