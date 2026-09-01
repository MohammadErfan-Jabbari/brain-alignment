---
title: "Manuscript Agent Guidance"
tags: [manuscript, reference]
aliases: [manuscript-agents]
---

# Manuscript Agent Guidance

This file is the repository gate layer for every manuscript tree in this folder: which tree to edit, evidence provenance, the review set, approval routing, acceptance checks, terminology, prose, structure, table, and figure rules learned during the thesis rewrite. The writing *method* is owned solely by the [`question-led-writing`](../../.claude/skills/question-led-writing/SKILL.md) skill and is never restated here. Folder `AGENTS.md` files hold only tree-specific instructions: [`rewrite/AGENTS.md`](rewrite/AGENTS.md) owns the canonical thesis's scientific position, argument structure, and role contract, with the question tree itself in the sibling [`rewrite/question-tree.md`](rewrite/question-tree.md); [`submission/AGENTS.md`](submission/AGENTS.md) owns the supervisor-review derivative's format and synchronization rules.

## Layout

| Path | Purpose |
| --- | --- |
| `rewrite/` | Canonical LaTeX thesis master and authority for current scientific interpretation |
| `submission/` | Supervisor-review derivative with local prose sources (UC3M cover + NeurIPS body); accepted scientific changes synchronize to `rewrite/` **Suspended until further notice; see the sync-suspension note in the [root operating contract](../../AGENTS.md).** |
| `figures/` | Historical committed figure set (fig01–fig09) from the removed extended layer, referenced by older timeline notes; the active figures live in each tree's own `figures/` directory, and generation code lives in `scripts/figures/` |

Legacy layers (`extended/`, `public/v0.9/`) were removed from HEAD on 2026-08-25 and survive only in Git history (last commits `7c445b0` and `6026021`). Do not recreate them; immutable-cut policy applies to any future cut.

## Question-led writing protocol

The **method** is owned by the [`question-led-writing`](../../.claude/skills/question-led-writing/SKILL.md) skill: the question tree, the guided inference path, the Plan / Draft / Review / Revise branches, pass scopes, evidence states, and the Step 5 audits. Do not restate or paraphrase that method here or anywhere else. This section owns only what the skill deliberately leaves to the repository: which tree to edit, evidence provenance, the review set, the deterministic checks, and approval routing.

**Order.** Work forward through the manuscript section by section, and inside a section paragraph by paragraph. The abstract is the last thing drafted, after every section it summarizes has settled.

1. Select the active tree and read in. `rewrite/` for any canonical scientific change; `submission/` only for supervisor-review format and condensation edits. Read the active leaf questions and their parent from the [maintained question tree](rewrite/question-tree.md), the owning evidence records, and the relevant canonical literature notes.
2. Run the skill's Plan or Draft branch on the active scope. Its Step 1 output (reader, starting understanding, governing question, provisional answer, claim, scope, source constraints, evidence states) is the precondition for prose, not a formality: a leaf whose evidence state is unsupported, unresolved, or in authority conflict is not drafted as settled.
3. Locate every existing paragraph that answers the active leaf, then draft one complete proposed replacement. Propose moving overlapping prose rather than appending a duplicate.
4. Draft adjacent leaf questions together only when they form one natural argumentative unit. Do not draft across a section boundary.
5. Use `\evd{Ennn}` as non-printing source provenance and keyed values from `numbers.tex`. A missing manuscript value is a `\gap`, never a reconstruction or guess. Evidence identifiers are hidden in the thesis build and may be displayed only for internal review.
6. When a pass, failure, or continuation statement depends on a frozen rule, reproduce the exact criterion from its owning evidence record. Never replace it with a generic positive-contrast rule, infer temporal predeclaration from manuscript order, or write *preregistered* unless an external registration supports that term.
7. Scale the review set to the stakes. Use the smallest applicable set during ordinary paragraph work. Run all four [`thinking-panel`](../../.claude/skills/thinking-panel/SKILL.md) reviews at a load-bearing subsection or section boundary, or when framing, scope, ownership, or attention allocation changes materially:
   - claim support and scope with `test-claims`;
   - reader and argument bottlenecks with `remove-bottlenecks`;
   - attention, length, and opportunity cost with `allocate-for-compounding`;
   - terminology, handoffs, ownership, and whole-manuscript fit with `coordinate-strategy`.

   Independence is the point: a reviewer that shares the drafting context under-detects. The demonstrated failure is three residuals found in-session against roughly thirteen found by a fresh pass (L055).
8. Reconcile multiple reviews into one proposed revision. Address each accepted item or explain concretely why it conflicts with evidence or a higher-level question.
9. Route to Erfan only a changed scientific verdict, a material change in claim scope, a new governing terminology or naming policy, an external commitment, or a genuinely preference-dependent choice among evidence-equivalent alternatives. Under [D067](../decisions/decisions.md) the parent applies reviewed, evidence-grounded edits that improve readability, clarity, or precision without changing scientific meaning.
10. At subsection close, run the skill's Step 5a reverse outline over both structures: every leaf answered once, every paragraph with one owner, every inference supported before use, every transition preparing the next reader question. Update the question tree in the same change whenever the argument's structure moved.
11. Apply the skeptical-reader test: the prose must be understandable sentence by sentence without an unsupported jump, an unexplained result, or dependence on project history.
12. Repeat for at most four rounds, stopping earlier when no reviewer identifies a material claim, structure, prose, citation, terminology, density, or handoff defect.
13. After all units are complete, run the same four reviews over the whole manuscript and revise until the remaining findings are non-material.
14. Run `uv run python scripts/manuscript_check.py` on the edited tree, then dispatch [`evidence-number-auditor`](../../.claude/agents/evidence-number-auditor.md) and [`citation-support-auditor`](../../.claude/agents/citation-support-auditor.md) over the edited scope. The script confirms that a cited E record exists and a keyed number is declared; it never opens the record, so a sentence carrying `\evd{E008}` that contradicts E008 passes it cleanly. The auditors are that half. Before sharing the `submission/` tree, or to clear `manuscript-sync-pending`, also dispatch [`manuscript-twin-auditor`](../../.claude/agents/manuscript-twin-auditor.md). **Not while the sync suspension in the [root operating contract](../../AGENTS.md) is in force: the trees are forked on purpose, so every divergence it reports is intended.**
15. Compute coverage yourself rather than trusting a child's claim: grep the scope, require one `ID:` block per item, reject `RESULT: PASS` with `CHECKED: 0`, and spot-check two `RECORD: file:line` values against the file. Retry a degenerate reply once with the reason appended, then surface it to Erfan. The full gate is in [`.claude/AGENTS.md`](../../.claude/AGENTS.md).
16. Build the PDF and inspect every rendered page before calling the candidate complete.

Use `--share-ready` only when no `\gap` remains and the manuscript is intended to ship; the skill's own completion criteria do not make prose share-ready. A contradiction found while writing stops that claim, sets `docs/status.md` to `manuscript-sync-pending`, and routes to `/interpret`. Scientific changes accepted in `submission/` synchronize to `rewrite/` before they become authoritative; see [`submission/AGENTS.md`](submission/AGENTS.md). **Suspended until further notice; see the sync-suspension note in the [root operating contract](../../AGENTS.md).**

## Section acceptance checks

- **Introduction:** A reader can state the exact tested claim, the claim dependencies, and the scoped answer without knowing an E identifier.
- **Section 2:** A reader can distinguish measurement, manipulation, attribution, transfer, and utility, and can name the comparator required for each.
- **Section 3:** Every canonical scientific role has one design tuple, and the reader can identify its data or response construction, intervention or assay, comparator, estimand, endpoint, and inference unit without reading implementation detail.
- **Section 4:** Every canonical scientific role has one result and verdict location, carries the correct evidence status, and avoids causal or universal claims unsupported by its evidence record.
- **Section 5:** The discussion explains the pattern without replaying Results or turning failure localization into a causal explanation.
- **Section 6:** Limitations bound the conclusion without inventing a new results narrative or repeating all caveats.
- **Section 7:** The conclusion answers the governing question directly and contains no new evidence.
- **Appendices:** A technical reader can reconstruct provenance, data and target construction, interventions, estimators, variants, and sensitivities without forcing the main text back into evidence-record chronology.

## Manuscript-wide terminology

Use the following terms throughout manuscript prose in every tree, including abstracts, captions, and appendices:

| Referent | Fixed term |
| --- | --- |
| General biological phenomenon | **brain activity** or **brain responses** |
| Actual measurements | **recorded fMRI responses** |
| Language-model internals | **model representations** or **model activations** |
| TRIBE outputs used in this work | **synthetic brain responses generated from text** |
| Training question | **whether brain responses can help train a smaller model** |
| Brain alignment | Held-out predictivity of recorded fMRI responses from model representations under a declared readout and controls |
| Controlled brain predictivity | Brain alignment after the specified nuisance, split, and control-model checks |
| Recorded brain-response target | A recorded fMRI response when it is used in a training objective; otherwise write *recorded fMRI response* |
| Synthetic brain-response target | A synthetic brain response generated from text when it is used in a training objective |
| Target uptake | Recoverability of an optimized training target from retained student representations by a fresh post-training readout |
| Retained-student movement | Parameter or representation difference from the declared training baseline that remains after temporary training components are discarded |
| 50-component linear target-projection measurability | Whether the declared fold-local PCA-50 target representation adds controlled predictivity of recorded fMRI responses beyond nuisance and the frozen row-twin control; this qualifies only that linear pathway, not full-dimensional or nonlinear access to the 20,484-coordinate training target |
| Brain-response-specific attribution | Whether the brain-response-target arm outperforms its route-appropriate control on the outcome being claimed: correctly paired versus permuted responses for the recorded-response route, or synthetic brain responses versus a matched text-derived target for the synthetic-response route |
| Biological transfer | Improvement on independently recorded fMRI responses that were not optimized as the training endpoint |
| Brain-specific advantage | Incremental benefit beyond an appropriate text-derived or permuted control, at comparable language-model quality and the correct biological inference unit. Reserve this term for identified contrasts |
| Claim dependency | Evidence required for one named claim. Do not impose a universal stage order when direct transfer, attribution, linear-pathway evidence, and utility have different dependencies |

Avoid unqualified *neural activity*, *neural representation*, *neural response*, and *neural target* when they could refer either to the biological brain or to a neural network. fMRI records a hemodynamic response associated with brain activity, not neuronal firing directly. Use *response* for what is measured, predicted, or evaluated. Reserve *target* for a response used in a training objective; write *recorded brain-response target* or *synthetic brain-response target* only after identifying its source. Do not write the generic phrase *response target*. Name a control by its construction and the alternative explanation it tests: use *text-feature control*, *text-derived control*, or *matched auxiliary target derived from language-model features*, not *nonbrain control*. Precision comes from naming the source, measurement, role, and comparison of an object, not from the adjective *neural* or a negation such as *nonbrain*.

### Thesis-facing experimental vocabulary

Organize manuscript prose by the scientific role that a procedure plays in the argument, never by execution date or evidence-record number.

| Level | Meaning | Canonical terms |
| --- | --- | --- |
| Route | Major source of training supervision | **recorded-response route**, **synthetic-response route** |
| Intervention | Paired training family defined by the manipulated supervision | **recorded-response intervention**, **synthetic-response intervention** |
| Arm or control | Condition within an intervention or assay | **ordinary KD arm**, **permuted-response control**, **frozen row-twin control**, **text-derived auxiliary-control arm** |
| Assay | Protocol that measures a declared quantity | **controlled regional predictivity assay**, **controlled naturalistic voxelwise predictivity assay**, **50-component linear target-projection measurability assay** (short form **target-projection assay**), **synthetic-target recovery assay**, **saved-student biological-transfer assay** |
| Analysis or audit | Contrast, diagnostic, or validity examination | **distillation-headroom analysis**, **retained-student movement audit**, **comparator-adequacy audit and attribution assessment**, **saved-student target-retention analysis**, **composed-path diagnostic**, **response-averaging analysis** |
| Evaluation | Recurring external endpoint | **language-quality evaluation**, **practical-utility evaluation** |
| Evidence record | Internal provenance owner | `E###` appears only in source provenance, an internal-review build, or the provenance appendix |

Use the shortest canonical term after its first definition. Dataset, model, layer, target dimension, and response construction are qualifiers used only when they distinguish variants. Participant-specific and participant-averaged identify response construction or inference level, not standalone experiments. TRIBE identifies the generator. A text-derived auxiliary target, frozen row twin, or permutation is a control within its owning comparison.

The main thesis argument uses claim-specific dependencies. Controlled predictivity supplies measurement context; route-specific headroom describes opportunity. The 50-component linear target-projection assay qualifies only the declared linear pathway. Direct transfer compares the synthetic-response arm with ordinary KD independently of the text-derived comparator, while brain-response-content attribution additionally requires an adequate nonbrain comparator. Practical utility has its own matched endpoint and, when framed as the payoff of improved controlled predictivity, requires a reliable prerequisite change. Post-training movement is diagnostic, not a comparator-matching condition.

Do not expose evidence-record identifiers in ordinary thesis prose, headings, captions, tables, or result statements. Preserve `\evd{E###}` in source and suppress it in the thesis build. A single provenance appendix may map descriptive scientific roles to evidence records, artifacts, and status.

In LaTeX sources, define each recurring acronym once in the manuscript's acronym registry and use `\ac{key}` or its plural/forced variants in prose. Do not manually write either `full term (SHORT)` or a raw registered short form. Reset acronym state after the abstract with `\acresetall` so the abstract and main text each expand their first use independently.

## Reader-first prose

Precision comes from making the relationship among the claim, comparison, evidence, and scope explicit, not from compressing them into technical labels. Open each paragraph with its answer in language available to the intended reader, then add only nonredundant support. When one sentence carries several independent claims, use parallel grammar or separate sentences so that conjunctions and inference boundaries are unmistakable.

Use formal academic prose: state the claim or procedure directly, and remove meta-commentary about framing or writing unless that framing is itself the claim. Guide rather than announce. Keep one principal conceptual move per sentence, explain why a mechanism or comparison matters before relying on it, provide local bridges for required premises, and make each paragraph prepare the next.

Define a technical object locally far enough for the reader to understand its role. If its exact construction or estimator belongs in Methods, add a concise forward reference rather than either duplicating the procedure or leaving the term unexplained. Describe a comparator by what both arms share and the single component that differs; this makes the alternative explanation being tested visible.

Use mathematical notation when it clarifies an estimand, comparison, aggregation, constraint, or dependency. Introduce symbols before a display. Unless its meaning is already unmistakable, follow each claim-bearing equation with one or two plain-language sentences that state what it computes and why the resulting quantity matters for the current question. Keep compact claim-bearing formulas in the main text when they help the reader follow the argument; place standard machinery, derivations, estimator variants, and implementation details in their owning technical section or appendix. Avoid decorative mathematics and notation that is used only once without improving precision.

Define an object's role positively and assign adjacent roles to their actual section or evidence owner. Avoid repeated “X rather than Y” or “X is not Y” constructions when two direct statements communicate the distinction more clearly.

Introduce each concept once, operationalize it once, and report its result once. Later sections should synthesize rather than restate. Do not present reserved, unexecuted, or precondition-stopped experiments as results.

Match each citation to the claim it actually supports. A general theoretical source does not support an optimization or learnability claim unless it analyzes that mechanism; present an untested mechanism as a hypothesis and cite the closest empirical or methodological literature. Describe permutations by their actual invariants: target permutation preserves target values and their marginal distribution while destroying stimulus--target pairing and joint structure.

After changing prose, recheck the whole active section against the terminology and acronym contracts rather than validating only the edited sentence. Split a paragraph when it serves distinct reader questions, such as reporting findings and stating contributions, and synchronize the maintained question tree when that changes the argument's structure.

### Banned tokens, and the split that decides the tool

A closed token list is complete by construction, so it is enforced deterministically by `uv run python scripts/prose_lint.py`. Register, taste, hedging, and rhythm are not lintable and belong to the fresh independent review ([L052](../learnings.md)). That split decides the tool for every prose defect: if a banned token betrays it, it is a lint rule; if it does not, no script will ever find it, and writing one is wasted work.

Banned outright in manuscript and report prose: the em dash in every form (Unicode `—`, and `---` in LaTeX source), *kill-gated*, *standardly*, and *prose* and *verdict* as generic nouns. `prose_lint.py` also carries a wider heuristic set that warns without gating.

This section is the list's only home, and the list is open by intent. Add an entry here and mirror it into `prose_lint.py`'s `OWNER_BANNED` in the same change; a ban that is stated and not mirrored is a ban that does not hold.

## Structure, tables, and figures

- A subsection normally owns three to five related paragraph questions. A two-paragraph subsection is allowed only when it marks a real conceptual boundary. Merge a one-paragraph subsection into its parent.
- Split a subsection if it exceeds about 1,000 to 1,200 words, contains more than six or seven substantive paragraphs, or answers more than one parent question.
- Use tables for analysis or evidence-record disposition, many-to-many evidence mappings, and repeated variant results.
- For dense mapping tables, separate compact identifiers from descriptive labels, give the flexible-width column to the substantive comparison, and use the full text width before reducing font size. Keep conceptually distinct evidence stages in separate rows.
- Keep table and figure captions to one rendered line whenever possible. Use the caption to identify the object; place interpretation, caveats, and reading instructions in the surrounding prose.
- In process figures, use equal-sized boxes based on the longest required item. Give parallel box labels that name the claim and the test that supports it; shorten wording before shrinking type or accepting distracting line breaks.
- When color groups related stages in a figure, repeat the grouping with visible text labels and use light fills that preserve contrast; color must reinforce structure rather than carry it alone.
- Treat every arrow as a scientific statement: make its relation explicit through a readable arrow label, adjacent text, or column heading, and never let geometry alone imply causation, mediation, successful attribution, or population generalization.
- When prose introduces a multi-part figure, explicitly map the figure's groups or stages to the surrounding paragraph questions. Do not make the reader infer whether the figure illustrates one paragraph or the whole subsection.

## Maintained question map

The intended reader, governing question, and provisional answer live in [`rewrite/AGENTS.md`](rewrite/AGENTS.md), the canonical scientific-interpretation authority. The complete question tree for the main text and appendices lives in [`rewrite/question-tree.md`](rewrite/question-tree.md), which is its single source; do not duplicate or paraphrase its questions here.

Treat the tree as a maintained reverse outline. Every main-text paragraph must answer a leaf question that contributes to its section question and ultimately to the governing question. Whenever a manuscript edit changes a section's purpose, evidentiary role, scope, or conclusion, update the affected question in the same commit. When a changed E-record verdict alters the argument, correct the E record first, route the change through `/interpret`, update the manuscript, and then synchronize the tree. Remove questions that no longer serve the governing question and add a question when the manuscript gains a necessary argumentative dependency. Review the complete tree before declaring the manuscript share-ready.

## Rules

- Do not create a manuscript report, claim lattice, checkpoint log, convergence store, or any additional alternate draft tree beyond the explicitly authorized `rewrite/` candidate and its declared derivatives.
- There is no public tree at HEAD. Creating one is a separate decision requiring Erfan's approval, and any future cut is frozen on creation.
- Every scientific number and figure value traces to an owning E record; only load-bearing artifacts receive recorded paths and SHA-256 values.
- If a keyed value does not exist in `numbers.tex`, write `\gap` and say so. Adding a `\DeclareResult` macro is an owner-confirm question, never something to fabricate, and never an occasion to change an epistemic verdict.
- Use the correct inference unit, uncertainty, and named test.
- Keep internal provenance in non-printing BibLaTeX fields such as `annotation`, not printable `note` fields.
- Keep source search-friendly: one sentence or paragraph per line, minimal custom macros, and no deep content nesting.
- Do not create a README; folder guidance belongs here.

## Figure path

`scripts/figures/ → outputs/figures/ (gitignored) → docs/manuscript/figures/ (selected and committed)`

## Related

- [Canonical thesis contract](rewrite/AGENTS.md)
- [Maintained question tree](rewrite/question-tree.md)
- [Supervisor submission derivative](submission/AGENTS.md)
- [Authority contract](../03-methodology.md)
- [Current status](../status.md)
