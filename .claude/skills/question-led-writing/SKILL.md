---
name: question-led-writing
description: Question-tree writing. Use to plan explanatory prose, draft from a question tree, review by reverse outline, revise from accepted findings, or supply another writing workflow with reader questions.
---

# Question-led writing

Build a **question tree** for the requested working unit. Its governing question is the root, structural child questions are branches, and paragraph questions are leaves. Every leaf answer must flow upward into the root answer.

## 1. Frame the root

Set the working unit to the smallest paragraph, section, or document that can answer the request. Inspect its parent and adjacent context for dependencies; expand the unit when a prerequisite crosses its boundary.

Name the intended reader and their assumed knowledge. Write one governing question in that reader's conceptual terms, followed by a one-sentence provisional answer stating the intended claim and scope. Use technical notation when the governing question requires it.

**Complete when:** the working unit, reader, assumed knowledge, governing question, provisional answer, claim, and scope are explicit.

## 2. Choose and build the branch

- **Plan:** derive the question tree from the root and constraints. Produce nested questions and the provisional root answer, audit them in Step 4, and stop when prose was not requested.
- **Draft:** start from the agreed question tree and source constraints, adding only questions required by the developing answer; continue to Step 3.
- **Review:** reverse-outline the existing prose, key each finding to its paragraph question and support-or-gap state, audit it in Step 4, and return findings while preserving the prose.
- **Revise:** start from the prose and accepted findings, update its question tree, and continue to Step 3.

Create a subsection when grouping distinct child questions improves navigation. Order every child after its conceptual prerequisites. Phrase questions as reader needs, such as “What does this score establish?”, rather than author topics such as “Discuss the score.”

Expose the tree when Plan or Review is the requested output. Use it as an internal scaffold during Draft or Revise unless the user requests it.

**Complete when:** every planned or retained paragraph has one primary question; the child questions jointly answer their parent; every child contributes to the root; and all prerequisites appear before the questions that depend on them.

## 3. Answer the leaves

For Draft and Revise, open each paragraph with its direct answer. Add only the reasoning, evidence, definition, example, or scope needed to support that answer. Introduce a technical term, symbol, or derivation when the current question requires it; otherwise place it under the question it answers. Use one stable term for each concept.

Draft first in the intended reader's conceptual language, then reconcile the wording against the evidence and necessary technical distinctions. Precision means preserving the claim's meaning, scope, comparison, and uncertainty, not preserving the source's labels. When compressing, remove secondary detail without removing the relationship that makes the answer intelligible. If the intended reader would need to unpack an unstated method, comparison, or causal link, state that relationship plainly before shortening it.

Represent a required but unsupported answer as a gap and route it to the governing evidence owner.

**Complete when:** every sentence supplies the answer, support, necessary scope, or a dependency-bearing transition for its paragraph question.

## 4. Audit upward

Trace every leaf through its branch to the root. Split a paragraph whose sentences answer unrelated questions. Merge paragraphs that duplicate one answer without distinct roles. Relocate an answer under the question it serves. Remove material that serves no necessary question. Make each transition show why the next reader question follows now. Revise the root answer to match the supported leaf answers.

Apply the governing evidence contract when judging support. For this repository's manuscript, use [`docs/03-methodology.md`](../../../docs/03-methodology.md). The question tree organizes claims; the document and its evidence owners originate and adjudicate them.

**Complete when:** every retained sentence has one inspectable role; every required leaf is supported or explicitly marked as a gap; every branch answers its parent; and the combined branches answer the root without an undefined prerequisite. Final-ready prose has no unresolved required gap.
