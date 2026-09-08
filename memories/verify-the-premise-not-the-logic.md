---
title: "Verify the Premise, Not the Logic"
tags: [memory, feedback, judgment]
aliases: [verify-the-premise-not-the-logic]
origin_session: "45dd7665-6d83-4be4-a44f-3b94b3bb570d"
source_memory: "/home/centcom/.claude/projects/-home-centcom-data-brain-alignment/memory/verify-the-premise-not-the-logic.md"
---

# Verify the Premise, Not the Logic

A finding almost always arrives as an argument whose premise is a factual claim about somewhere else in the repo: "this is the only place that defines X", "this record supports that", "these labels are inconsistent". The argument is usually sound. **The premise is what fails.** Checking the reasoning finds nothing; opening the cited file settles it in one command.

**Reversals this bought (Sections 4 and 5, 2026-09-01/02):**
- A cold reader reported three canonical roles with no verdict location. The premise conflated the terminology list with the 13-row role inventory; the three were supporting analyses, not claim-bearing rows.
- A composite-figure-label finding dissolved on opening `main-submission.aux`: subfigure labels already resolve to `7a`, `8a`, so the reader sees correct panel letters and the inconsistency was source-only.
- `first-principles-grounder` protected a sentence as Section 5's only home for the direct-transfer/attribution distinction. `07:19` is **verbatim identical** to it and `02:171-172` declares it, so it was the third copy, not the only one. The protection was rejected and the cut kept.
- I narrowed a question-tree leaf on a correct round-1 finding, then had to restore it: the deleted sentences really were third copies, but *applying* those rules to prior studies is a post-results judgment no other section performs. Correct finding, wrong inference about what it licensed.
- An agent cited `01:100` for a sentence that exists at `01:38`; the file is 52 lines. Quoted text right, line wrong.
- Two specialists split on whether Section 6 misattributed a threshold exclusion. The auditor showed both bounds fall below the threshold, so no number was overstated; that was true and beside the point, because Section 4 never performed the read and Section 6 was not entitled to perform it. **Check whether the manuscript actually made the claim, not only whether the claim would survive arithmetic.**

**Verify what kind of location a citation is, not only what it says.** A medium-confidence finding argued a bound was false because Section 5 compares the two routes. It does, at `05:55`, under `\subsection{Design implications...}`, which makes it an interpretation and not a reported result, so the bound stood. One `sed -n` of the surrounding lines showed the subsection heading and settled it.

**The sharpest version of this rule: a premise that gets WRITTEN INTO the manuscript needs more verification than one that only decides whether to apply a finding.** A cold reader stated that one location held "the single genuine ordering constraint in the thesis". I wrote a repair encoding that as prose. The claim-dependency figure draws three "must pass first" arrows, so the thesis's final page asserted independence against its own figure until verification caught it. A rejected finding costs nothing; a premise written into the text ships. Grep before writing, not after.

**A uniqueness claim must be tested against the rule, not a phrasing.** An agent defended a sentence as the only home of its bound by grepping its exact phrase and finding nothing; the rule lived in two other sections in different words. "Grep finds no other" means nothing unless the grep was for the concept.

**My own briefings carry premises too.** I told three agents that two sentences were sole owners of bounds that earlier cuts depended on. An agent grepped and disproved both. A briefing error is worse than a finding error, because every child inherits it and reasons for an hour inside it.

**`git log -S` is a premise check, not just a safety rule.** Before replacing an existing sentence on an agent's advice, search the history for it. A bound I rewrote turned out to have been added deliberately in its own commit; the finding that prompted the rewrite was arguing against a decision, not against an accident.

**The measurement version of the same discipline.** A number that does not move is data. Three tables reported byte-identical overflow (217.26898pt) after being set to `\scriptsize`; identical to five decimals is not a small effect, it is *no* effect, and it exposed that `\@floatboxreset` resets the font inside a float. Separately, a cut depth of "12.1%" turned out to be two different word-count filters compared against each other: **a percentage is meaningless unless the same denominator method is applied to every version.** The same word counter was later found to skip every line starting with a backslash, dropping prose that merely began with `\looseness=-1` or `\ac{...}` and undercounting one section by 22 words; the reported percentages survived because both versions used the same broken method, but every absolute count was wrong. A `\looseness=-1` hint left on a paragraph that a cut had shrunk from ten sentences to three was shown inert the same way: identical page count *and* identical box count before and after removing it.

**Why:** agents are good at reasoning and unreliable about what a file actually contains, and so am I after a long session. Agreement between agents is not evidence; two agreed on a wrong figure arrow that only `E025:52` settled.

**How to apply:** before applying or rejecting any finding whose force depends on what another file says, `grep`/`sed` that file. Spot-check at least two `file:line` citations per agent report. When a metric refuses to move, suspect the instrument before the subject. Pairs with [Subagent Orchestration for Manuscript Review](subagent-orchestration-for-manuscript-review.md).

## Related

- [Subagent Orchestration for Manuscript Review](subagent-orchestration-for-manuscript-review.md)
