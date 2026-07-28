---
name: question-led-writing
description: Question-led guided writing. Use to plan explanatory prose from reader questions, draft each answer as a supported path from the reader's current understanding, review by reverse outline and inference audit, revise dense or discontinuous prose, or supply another writing workflow with reader questions.
---

# Question-led guided writing

Use two connected structures:

- The **question tree** determines what the reader must understand. Its governing question is the root, structural questions are branches, and paragraph questions are leaves.
- The **guided inference path** determines how the reader reaches each answer. Move from shared ground through only the distinctions and evidence needed for the scoped conclusion.

The tree chooses the destination. The path makes the conclusion understandable and earned.

## 1. Frame the reader and root

Set the working unit to the smallest paragraph, section, or document that can answer the request. Inspect its parent and adjacent context for dependencies. Expand the review context when a prerequisite crosses the boundary, but preserve the prerequisite's owning location and use a local bridge or cross-reference unless the active unit owns it.

Name the intended reader, what they already understand, and the model they are likely to form before reading the unit. Write one governing question in that reader's terms, followed by a one-sentence provisional answer stating the intended claim and scope. Use technical notation only when the governing question requires it.

**Complete when:** the working unit, reader, starting understanding, governing question, provisional answer, claim, and scope are explicit.

## 2. Choose and build the branch

- **Plan:** derive the question tree from the root and constraints. Produce nested questions and the provisional root answer, audit them in Step 5, and stop when prose was not requested.
- **Draft:** start from the agreed question tree and source constraints, adding only questions required by the developing answer; continue to Step 3.
- **Review:** reverse-outline the existing prose, key each finding to its paragraph question and support-or-gap state, audit it in Step 5, and return findings while preserving the prose.
- **Revise:** start from the prose and accepted findings, update its question tree, and continue to Step 3.

Create a subsection when grouping distinct child questions improves navigation. Order every child after its conceptual prerequisites. Phrase questions as reader needs, such as “What does this score establish?”, rather than author topics such as “Discuss the score.”

Expose the tree when Plan or Review is the requested output. Use it as an internal scaffold during Draft or Revise unless the user requests it.

**Complete when:** every planned or retained paragraph has one primary question; the child questions jointly answer their parent; every child contributes to the root; and all prerequisites appear before the questions that depend on them.

## 3. Build the guided inference path

Before drafting a leaf answer, identify the shortest supported route from the reader's starting understanding to the answer:

\[
\text{shared ground}
\rightarrow
\text{missing distinction}
\rightarrow
\text{mechanism or design}
\rightarrow
\text{evidence}
\rightarrow
\text{scoped conclusion}
\rightarrow
\text{limitation or handoff}.
\]

Use only the steps the leaf requires. A definition or procedural paragraph may need shared ground, a distinction, and a mechanism but no result. A result paragraph normally needs the mechanism or comparison before the evidence and interpretation. Never insert a limitation mechanically when it does not change the claim.

Each step must establish the premise used by the next. If a reader must guess why a comparison matters, remember an unstated definition, or accept a conclusion before seeing its support, the path has a gap.

**Complete when:** the route contains no unsupported jump, no unnecessary detour, and no step that depends on information introduced later.

## 4. Answer the leaves

For Draft and Revise, open each paragraph with its direct answer. Add only the reasoning, evidence, definition, example, or scope needed to support that answer. Introduce a technical term, symbol, or derivation when the current question requires it; otherwise place it under the question it answers. Use one stable term for each concept.

Guide rather than announce. Draft first in the intended reader's conceptual language, then reconcile the wording against the evidence and necessary technical distinctions. Reveal one necessary distinction at a time. Explain why a method or comparison matters before relying on its result. Interpret evidence explicitly instead of leaving the reader to infer its role.

Keep one principal conceptual move per sentence. Split a sentence when it asks the reader to absorb multiple new comparisons, exceptions, mechanisms, or scopes at once. Prefer an extra short sentence over a compressed sentence that hides the relation between its clauses. Precision means preserving the claim's meaning, scope, comparison, and uncertainty, not preserving the source's labels or packing all qualifications into one sentence.

When compressing, remove secondary detail without removing the relationship that makes the answer intelligible. If the intended reader would need to unpack an unstated method, comparison, or causal link, state that relationship plainly before shortening it. End at the narrowest conclusion the path supports, then name only the limitation or next question needed for the following paragraph.

Route a required but unsupported claim to its governing evidence owner and do not draft it as supported. In this repository, use `\gap` only for a required missing manuscript value.

**Complete when:** every sentence makes one inspectable contribution to the answer or inference path, and the paragraph prepares the reader for the next question.

## 5. Audit the tree and path

Trace every leaf through its branch to the root. Split a paragraph whose sentences answer unrelated questions. Merge paragraphs that duplicate one answer without distinct roles. Relocate an answer under the question it serves. Remove material that serves no necessary question. Make each transition show why the next reader question follows now. Revise the root answer to match the supported leaf answers.

Then read the prose as a skeptical first-time reader:

- Can the reader follow each inference without supplying a missing premise?
- Is every distinction introduced before it changes the interpretation?
- Does every method or result arrive after the reader understands why it matters?
- Does any sentence contain more conceptual work than its neighbors prepare the reader to absorb?
- Could the reader explain why each paragraph is present and why the next one follows?
- Does the conclusion state exactly what the evidence establishes, weakens, leaves unresolved, or does not test?

Apply the governing evidence contract when judging support. For this repository's manuscript, use [`docs/03-methodology.md`](../../../docs/03-methodology.md). The question tree organizes claims; the document and its evidence owners originate and adjudicate them.

**Complete when:** every retained sentence has one inspectable role; every required leaf is supported or explicitly marked as a gap; every inference path is continuous; every branch answers its parent; and the combined branches answer the root without an undefined prerequisite. Final-ready prose has no unresolved required gap.
