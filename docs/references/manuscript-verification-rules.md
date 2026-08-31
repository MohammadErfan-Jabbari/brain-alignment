---
title: "Manuscript Verification Rules"
tags: [reference, manuscript, verification]
aliases: [verification-rules, l2-rules]
---

# Manuscript Verification Rules

The rule corpus the three read-only verification agents load at step 0: [`evidence-number-auditor`](../../.claude/agents/evidence-number-auditor.md), [`citation-support-auditor`](../../.claude/agents/citation-support-auditor.md), and [`manuscript-twin-auditor`](../../.claude/agents/manuscript-twin-auditor.md).

This file is data, not a contract. It exists so the verification layer can improve without any agent editing its own criteria.

## How it changes

**The corpus self-improves. No agent self-edits.** An agent that can rewrite its own criteria has a direct incentive to weaken them, because loosening a tolerance makes its own `PASS` cheaper. That is the violation [`.claude/AGENTS.md`](../../.claude/AGENTS.md) already forbids for evidence and writing gates, with the recorded reason missing.

The mechanism instead:

1. An auditor that meets a defect class it had no rule for emits, as part of its normal output, `PROPOSED-RULE: <defect class> | EVIDENCE: <file:line> | WOULD-HAVE-CAUGHT: <the miss>`.
2. The parent session evaluates the proposal against the cited evidence.
3. An accepted proposal is appended to the numbered list below, by the parent, with its evidence.

**The list is monotonic: it may only add checks.** A proposal that would relax, narrow, or add an exception to an existing rule is not appended. It routes to `/meta` and needs an entry in [`decisions.md`](../decisions/decisions.md), because that is a gate being loosened.

This is the same shape as [`confound-catalog.md`](confound-catalog.md): one file is the single source, and the prompts that use it read it rather than carrying hand-copied constants that drift.

## Rules

Each rule states the defect, how to detect it, and the evidence that earned it.

1. **A resolvable marker is not a supported marker.** `manuscript_check.py` confirms an E record *file exists* and a key *is declared*; it never opens the record. A sentence carrying `\evd{E008}` that contradicts E008 passes it cleanly. Every marker and every key must be checked against the record's content. *Evidence: `scripts/manuscript_check.py`, the `resolves()` existence test.*
2. **Compare numbers numerically, at the record's precision, never by string.** A rounded restatement is correct. `numbers.tex:44` declares `e008_ci` as `[$-0.00037$, $+0.00058$]` while `E008`'s own frontmatter shows `[−0.0004,+0.0006]`; both are right. A manuscript interval **tighter** than the record's, a sign flip, or a point estimate outside the record's interval is a mismatch. *Evidence: `docs/manuscript/rewrite/numbers.tex:44` against `docs/experiments/E008_per-participant-f1-solidification.md`.*
3. **A compound provenance tag means check every record it names.** Of 356 `\DeclareResult` declarations all carry a `% [ENNN]` tag; two are irregular, `% [E013b]` and `% [E025/E030]`. Neither is an error. *Evidence: `numbers.tex`, full scan.*
4. **The record's verdict word bounds the prose.** `E008` reads `WEAK / NULL`. A sentence with the right digits and a positive reading is still a mismatch. Check claim direction and strength, not only value. *Evidence: E008's verdict against the drafting failure mode it caused.*
5. **A specific estimate without its uncertainty and named test is incomplete**, where the owning record has them. This is the repo's evidence rule, not a style preference. *Evidence: root `AGENTS.md`, evidence rules.*
6. **A result-like literal typed into prose is a defect even when the value is right**, because nothing updates it when the record changes. Numbers enter prose through keys. *Evidence: the `numbers.tex` apparatus exists for exactly this.*
7. **A reconstructed number is the worst finding in the set.** Where the record has no such value, the manuscript takes a `\gap`. A `\gap` is never itself a finding. *Evidence: root `AGENTS.md`; L074's retracted power claim shows what a reconstruction costs once it is cited.*
8. **A general theoretical source does not support an optimization or learnability claim** unless it analyzes that mechanism. Judge the support relation against the exact sentence, and name which half of a compound claim the paper actually reaches. *Evidence: `docs/manuscript/AGENTS.md`, citation matching.*
9. **`hadidi-2024_case-against-brainscore-reliance.md` and `feghhi-2024_case-against-over-reliance-brain-scores.md` are one paper under two names.** Citing both in one place as independent support is alias double-counting. Check any new pair for the same aliasing. *Evidence: `docs/literature/canonical/`, both files.*
10. **An uncited paper is a gap to name, never a hole to fill from memory or the web.** No canonical note means `UNGROUNDED`, named for `paper-digest`. *Evidence: the repo's own grounding rule; a web-fetched summary is not a canonical note.*
11. **Describe a permutation by its actual invariants.** Target permutation preserves target values and their marginal distribution while destroying stimulus-target pairing and joint structure. A citation used to back a stronger invariance claim is partial at best. *Evidence: `docs/manuscript/AGENTS.md`, permutation language.*
12. **Prose the derivative has and the canonical tree lacks is an authority inversion, always a `FAIL`.** The content is applied to `rewrite/` first and then flows down. *Evidence: the recorded swarm failure, "reviewing or applying against the derivative inverted the repository's authority direction".*
13. **A keyed number declared locally in the derivative silently forks the value.** Both trees resolve keys through the canonical `numbers.tex`; a shadow declaration in the submission tree is a defect even when the value currently matches. *Evidence: `submission/main-submission.tex` reads the canonical `numbers` across the tree boundary by design.*
14. **Fixed role terms are not condensable.** A derivative that renames an assay, an arm, or a control has drifted, even when the rename reads better. *Evidence: the scientific-role contract in `manuscript/rewrite/AGENTS.md`.*
15. **`RESULT: PASS` with `CHECKED: 0` is an auto-reject, and `INCOMPLETE` is never `PASS`.** Coverage is computed by the parent, not claimed by the child. *Evidence: the degenerate-child gate in `.claude/AGENTS.md`; a 114-character reply and a 32-byte parse artifact both reached a merge before this existed.*
16. **Every `RECORD:` is `file:line` and must actually contain the cited content.** The parent spot-checks two at random; a line that does not contain the claimed value is an immediate reject, because a fabricated citation is worse than silence. *Evidence: the same gate.*
17. **Check for the uncertainty that is missing, not only the values that are present.** Rule 5 cannot fire under an item-driven walk, because a deleted interval leaves no item to inspect. So for every key resolved, look up whether its owning record has a companion uncertainty, interval, inference unit, or named test, and whether `numbers.tex` declares a key for it; if it does and the prose omits it, that is `INCOMPLETE-ESTIMATE`. *Evidence: the 2026-09-01 acceptance test. Six defects were seeded in one subsection and five were caught, including a fabricated interval and a verdict overreach; the only miss was `e008_fold_ci` and its fold unit deleted from a stated estimate, which both arms reported as `OK`.*
18. **A canonical note that documents a different title, DOI, or venue than the bib entry is unresolved until the correspondence is written down.** `gao2024` cites the Nature Computational Science 2025 version while its note documents the bioRxiv preprint under a different title; the content matches and the authors are the same, but nothing in either file says so, and an auditor cannot confirm from the note alone that it read the work the manuscript cites. Record the version correspondence in the note rather than inferring it. *Evidence: proposed by `citation-support-auditor` on the 2026-09-01 Section 2 audit; `references.bib` gao2024 against `docs/literature/canonical/gao-2024_scaling-not-instruction-brain-alignment.md`.*

19. **A result-like literal inside a figure source is rule 6's blind spot, and the deterministic gate cannot see it.** `manuscript_check.py` scans prose for bare result-like numbers and never opens a `.tikz`. The canonical Figure 10b sized its bars from `\result{e026_plot_check_pass}` and `\result{e026_plot_check_fail}` while labelling them with the hardcoded `24 passed` and `30 failed`, so the bars showed 20 and 16 and the labels contradicted both the bars and Table 22. That is the contradiction the supervisor reported, and it survived in the canonical tree until a twin diff compared figure sources. Diff figure sources between trees and check every literal in a figure against the key that governs the same quantity. *Evidence: proposed by `manuscript-twin-auditor` on the 2026-09-01 pre-share audit; `docs/manuscript/rewrite/figures/synthetic_comparator_audit.tikz` against `numbers.tex:199-202` and `docs/references/supervisor-feedback.md`.*


## Related

- [Manuscript writing protocol and gates](../manuscript/AGENTS.md)
- [Claude apparatus and the dispatch contract](../../.claude/AGENTS.md)
- [Confound catalog](confound-catalog.md)
- [Evidence and authority contract](../03-methodology.md)
