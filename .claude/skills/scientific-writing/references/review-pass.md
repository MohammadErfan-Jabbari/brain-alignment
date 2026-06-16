# The review pass: Devil's Advocate and the Clarity Test

Run this before any section a supervisor or committee will see. It is a prose-level review of the written
argument, distinct from the repo's other adversaries: the thinking-panel agents attack a result before it
lands in the docs, Codex attacks code, and the oracle-reviewer gates a design before compute. This pass
attacks the writing: is the claim on the page actually supported by the evidence on the page.

## The three lenses

Read the section once through each lens. Each criticism must be specific: name what, where, and how to
fix. A vague note ("tighten this") is not a finding.

- **Internal validity: does the evidence support the claim?** Check every empirical sentence against its
  cite. Is the effect stated with its uncertainty and test (the results-prose standard)? Is the hedge verb
  right for the evidence (a measured effect "demonstrates", a correlation "suggests")? Is any number bare?
  Is any assumption (for us, Y ⊥ θ* | S) quietly promoted to a result?
- **External validity: does it generalize as stated?** Does the claim reach past what was measured? A
  per-individual null measured on n=9 is not "no brain signal exists"; a cross-family law over six
  families is not a universal law. Flag every place the scope of the sentence exceeds the scope of the
  evidence.
- **So what: why should the reader care?** Does the section answer its reader's question (Introduction why
  care, Results what did you find, Discussion what does it mean)? Cut a paragraph that survives the Clarity
  Test as deletable. A correct paragraph that carries no weight still costs the reader.
- **First-pass readability: can the reader follow it without stopping?** The reader-comprehension floor
  (writing-style.md §2) as a review lens: is every acronym/domain term defined on first use (document-wide
  for a manuscript)? Does every non-obvious method choice carry its one-clause rationale or a `\gap`? Is any
  load-bearing sentence carrying more than one inferential hop (the "so… and… by construction" tell)? Is any
  comparison of three or more numbers dumped inline where a table belongs? Each is a specific, locatable
  finding, not a "tighten this".

## The Clarity Test (paired with section 4 of writing-style.md)

For each paragraph: if I delete it, does the section still make sense? Delete what is lost-less, compress
what merely supports, invest in what carries. This is the antidote to the uniform-paragraph tell and it
focuses the writing on the load-bearing argument.

## How to run it

For a short section, run the lenses inline yourself. For a full manuscript draft, or anything going
to a committee, spawn the repo's adversarial agents (`counter-argument`, `premortem-analyst`,
`first-principles-grounder`) on the draft with these lenses as their brief, then verify each
objection against the evidence and address the ones that hold. Re-run until no hole survives. A finding the
draft cannot answer is either a real gap (flag it with `\gap`) or an over-claim (fix the verb or the
scope). Do not wave it away.

For a LaTeX manuscript, run the first-pass-readability lens on the **rendered PDF**, not only the source.
A dense equation-laden passage or an inline number-dump can pass the source-level linter and still stop a
reader cold on the page; the source style (one sentence per line) is for grep and diff, not for reading.
Read the compiled output the way the supervisor will.
