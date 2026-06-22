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
- **Scientific register: does the prose state the claim, or narrate it?** The storytelling tells from
  writing-style.md §1 ("Register: state the claim, do not narrate it") as a review lens — the class a
  supervisor caught on v0.1 (L054, D046) and the deterministic linter cannot reach. Flag every:
  anthropomorphized abstraction (a question/result/manuscript that "earns/survives/reports/locates"),
  self-narration of a rhetorical move ("saying so plainly is what locates…"), internal-metaphor leakage
  (the ladder/rung/door/lever as reader-facing prose), dramatized framing, and reflex passive *density*
  (not any single justified passive). This lens is owned by the **`prose-register-auditor`** agent, which
  reads against these exact rules and returns located findings; see "How to run it".

## The Clarity Test (paired with section 4 of writing-style.md)

For each paragraph: if I delete it, does the section still make sense? Delete what is lost-less, compress
what merely supports, invest in what carries. This is the antidote to the uniform-paragraph tell and it
focuses the writing on the load-bearing argument.

## How to run it

For a short section, run the lenses inline yourself. For a full manuscript draft, or anything going
to a committee, spawn the repo's adversarial agents (`counter-argument`, `premortem-analyst`,
`first-principles-grounder`) on the draft for the first three lenses, **and `prose-register-auditor` for
the register + first-pass-readability lenses** (it is the dedicated voice reader — the claim-panel attacks
the argument, the auditor attacks the prose). Then verify each objection against the evidence and address
the ones that hold. Re-run until no hole survives. A finding the draft cannot answer is either a real gap
(flag it with `\gap`) or an over-claim (fix the verb or the scope). Do not wave it away. The register
findings are prose fixes, not evidence questions: drop the framing and assert the content.

## The convergence gate (D047) — you cannot finish dirty

The review pass is not done when you have *run* the auditor; it is done when a **fresh, independent**
audit of the **final bytes** comes back with **zero findings** (not zero load-bearing — zero). This is
enforced, not trusted: a `Stop` hook (`.claude/hooks/stop_register_gate.py`) blocks the agent from ending
its turn while an edited `docs/manuscript/` or `docs/reports/` deliverable has no clean verdict keyed to
its current content hash. The v0.2 session failed precisely here — it stopped at `REGISTER-CLEAN: NO`,
fixed three things, and never re-audited; an in-session self-review found 3 residuals where a fresh strict
pass found ~13 (L055). So the terminating procedure is fixed:

1. Make your fixes.
2. Spawn a **quorum of ≥2 FRESH `prose-register-auditor` agents** on the final draft — fresh meaning new
   `Agent` spawns with no writing context (the writer grading its own edits is the failure mode). Save each
   agent's raw output to a file.
3. Every auditor must return `REGISTER-CLEAN: YES` with zero findings. Any finding → fix and re-spawn fresh.
   Do not triage "minor" findings away; the pass bar is zero, and deferral is only via an explicit
   Erfan-approved accepted-residual.
4. Record the verdict: `uv run python scripts/record_register_verdict.py --group <group> --audits a1.txt a2.txt`.
   It refuses unless ≥2 fresh outputs all say YES, and stamps the verdict to the current content hash. This
   is the only thing that releases the `Stop` gate. (Accepted-residual escape: `--accept-residual --note`,
   used only with Erfan's explicit sign-off.)

For a LaTeX manuscript, run the first-pass-readability lens on the **rendered PDF**, not only the source.
A dense equation-laden passage or an inline number-dump can pass the source-level linter and still stop a
reader cold on the page; the source style (one sentence per line) is for grep and diff, not for reading.
Read the compiled output the way the supervisor will.
