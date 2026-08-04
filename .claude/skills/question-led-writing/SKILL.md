---
name: question-led-writing
description: Question-led guided writing for explanatory, academic, and scientific prose. Use to plan from reader questions, draft supported inference paths, review by reverse outline and inference audit, revise dense or discontinuous prose, align claim-bearing equations or visuals with prose, audit terminology or stock AI-like phrasing, or supply another writing workflow with reader questions.
---

# Question-led guided writing

Use two connected structures:

- The **question tree** determines what the reader must understand. Its governing question is the root, structural questions are branches, and paragraph questions are leaves.
- The **guided inference path** determines how the reader reaches each answer. Move from shared ground through only the distinctions and evidence needed for the scoped conclusion.

The tree chooses the destination. The path makes the conclusion understandable and earned.

## 1. Frame the reader, root, and authorities

Set the working unit to the smallest paragraph, section, or document that can answer the request. Inspect its parent and adjacent context for dependencies. When a prerequisite crosses the boundary, preserve its owning location and supply the smallest local bridge or cross-reference that restores continuity.

Name the intended reader, what they already understand, and the model they are likely to form before reading the unit. Write one governing question in that reader's terms. Follow it with a one-sentence provisional answer stating the intended claim and scope. Use technical notation only when the governing question requires it.

Before the first claim-bearing judgment, identify the source constraints. For every source-governed or support-disputed required claim, name the governing authority and classify the evidence state:

- **Supported:** the named authority backs the claim; the claim may be retained within that support.
- **Unsupported:** the consulted authority does not back the claim; remove or narrow it.
- **Unresolved:** the required authority or decision is absent or pending; route it and do not present the claim as settled.
- **Authority conflict:** governing sources disagree; route the conflict to the governing adjudication process without resolving it during writing.

In this repository, apply the [authority contract](../../../docs/03-methodology.md). The owning E record records result support and adjudicated verdicts; contradictions route through `/interpret`; and the extended manuscript owns current scientific interpretation. Use `\gap` only for a required missing manuscript value, never for a missing premise, absent citation, unsupported claim, or disputed verdict.

**Complete when:** the working unit, reader, starting understanding, governing question, provisional answer, claim, scope, source constraints, and governing authorities are explicit.

## 2. Choose the branch and pass scope

Determine one primary branch from the requested output and a pass scope of **structure/inference**, **line/style**, or **both**. Use only valid combinations:

- Plan uses structure/inference.
- Draft uses structure/inference or both.
- Review and Revise may use any pass scope.
- A line/style-only Review or Revise preserves the existing tree and inference path. Inspect only enough context to identify a material inference blocker, which Review reports and Revise leaves pending rather than silently redesigning.
- When both scopes apply, complete the structure/inference work before line/style work.

- **Plan:** derive the question tree from the root and constraints. Produce the nested questions, provisional root answer, source needs, and all non-supported evidence states. Audit the tree in Step 5a and stop without producing prose.
- **Draft:** start from the agreed question tree and source constraints. If no tree exists, derive the smallest internal tree that can support the requested unit. Add only questions required by the developing answer, then continue to Steps 3 and 4.
- **Review:** reverse-outline the existing prose and key every finding to its paragraph question. Record the failure, its effect on the reader or inference, the governing boundary, and the smallest valid repair. Add a primary class only when it helps grouping or routing: **structure**, **inference**, **scope**, **evidence**, **terminology or alignment**, or **style**. Record an evidence state for claim-bearing findings. Run the requested Step 5 scope and return findings while preserving the prose.
- **Revise:** start from the prose and accepted findings. If no findings exist, perform the necessary Review internally first. For structure/inference or both, update the question tree and continue to Steps 3 and 4. For line/style only, preserve the tree and inference path, perform the minimum prerequisite check, then continue to the line-level work in Steps 4 and 5b.

For a combined diagnosis-and-change request, run Review before Revise. Record the Review findings before mutation; the prose-preservation rule holds until Revise begins. The revise request implicitly accepts only repairs within the declared mutation boundary. A request to revise authorizes rhetorical, terminology, and style repairs that preserve the stated claim, scope, and evidence. A proposed change to scientific interpretation, evidence status, verdict, or load-bearing scope remains pending until the decision owner named by the governing contract accepts it and the decision is recorded in its governing authority.

Create a subsection when grouping distinct child questions improves navigation. Order every child after its conceptual prerequisites. Phrase questions as reader needs, such as “What does this score establish?”, rather than author topics such as “Discuss the score.”

Expose the tree for Plan and for Review when structure/inference is in scope. Keep it internal during a line/style-only Review or a single-agent Draft or Revise unless the user requests it or a material inference blocker depends on it.

When another agent or later task will continue the work, expose only the coordination state needed to continue: active branch and pass scope, mutation boundary, accepted and pending findings keyed to their questions, named authorities and non-supported evidence states, next branch, and acceptance test. Include the active tree when structure/inference is in scope or changed. This packet is not authority; the receiver must reopen the current authorities before acting.

Load [Style guardrails and repair patterns](references/style-guardrails.md) only when line/style work is in scope. When structure/inference is also in scope, complete its branch-permitted audit or repair first. For Draft, and for Revise with structure/inference in scope, read the reference after Step 3 and before the first line-level change. For line/style-only Revise or Review, read it after the minimum prerequisite check and before the first line-level action. Do not load it for planning-only work.

**Complete when:** the primary branch, pass scope, mutation boundary, prerequisites, and requested deliverable are explicit. When structure/inference is in scope, every planned or retained paragraph has one primary question, the child questions jointly answer their parent, every child contributes to the root, and all prerequisites precede the questions that depend on them.

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

Use only the steps the leaf requires. A definition or procedural paragraph may need shared ground, a distinction, and a mechanism but no result. A result paragraph normally needs the mechanism or comparison before the evidence and interpretation. Include a limitation only when it changes the claim or prepares a necessary handoff.

When a comparison carries the inference, establish what the conditions share, all identified claim-relevant differences, and which alternative explanation the comparison tests. State when the difference inventory is incomplete. When several relevant dimensions differ, state what the comparison cannot isolate.

Each step must establish the premise used by the next. A path has a gap when the reader must guess why a comparison matters, remember an unstated definition, or accept a conclusion before seeing its support.

**Complete when:** the route contains no unsupported jump, unnecessary detour, or step that depends on information introduced later.

## 4. Answer the leaves

Draft and Revise use this step. Orient the reader immediately to the leaf answer. Open with the direct answer when its premises are already available; otherwise begin with the shared ground needed to earn it.

Add only the reasoning, evidence, definition, example, or scope needed to support the answer. Introduce a technical term, symbol, or derivation when the current question requires it. Place later material under the question it answers. Use one stable term for each concept.

Guide rather than announce. Draft first in the intended reader's conceptual language, then reconcile the wording against the evidence and necessary technical distinctions. Reveal one necessary distinction at a time. Explain why a method or comparison matters before relying on its result. Interpret evidence explicitly instead of leaving the reader to infer its role.

Keep one principal conceptual move per sentence. Split a sentence when it asks the reader to absorb multiple new comparisons, exceptions, mechanisms, or scopes at once. Prefer an extra short sentence over a compressed sentence that hides the relation between its clauses. Precision preserves the claim's meaning, scope, comparison, and uncertainty.

When compressing, remove secondary detail without removing the relationship that makes the answer intelligible. State an otherwise hidden method, comparison, or causal link before shortening it. End at the narrowest conclusion the path supports, then name only the limitation or next question needed for the handoff.

Use mathematical notation when it makes an estimand, comparison, aggregation, constraint, or dependency easier to verify. Introduce every symbol in prose before its equation. Unless the meaning is already unmistakable, follow each claim-bearing display with one or two plain-language sentences stating what it computes and why that quantity answers the current question. Keep compact claim-bearing formulas near the question they answer. Route standard machinery, derivations, and implementation detail to the existing document location that owns the method or derivation. When no such location exists, flag the placement decision rather than creating a new authority by default.

For each claim-bearing figure or table, identify the reader question it answers, the comparison or relationship to inspect, and the narrow conclusion the display supports. Introduce necessary terms before the reference. Keep referents, conditions, and comparison labels consistent across prose, caption, and visual, or map unavoidable label differences explicitly.

When structure/inference is in scope, draft source-governed or support-disputed claims only within the support of the named authority, remove or narrow unsupported claims, and route unresolved or authority-conflict states instead of presenting them as settled. During line/style-only work, preserve the claim, scope, and evidence state; record and route any support problem without making an unauthorized semantic repair.

**Complete when:** every sentence has one inspectable role, and each paragraph either prepares the next reader question or closes its branch at the narrowest supported scope.

## 5. Audit the requested pass

### 5a. Audit the tree and inference path

Plan runs Step 5a only. Draft, Review, and Revise run Step 5a when structure/inference is in scope. A line/style-only Review or Revise performs only the minimum prerequisite check defined in Step 2 before Step 5b.

Trace every leaf through its branch to the root. Split a paragraph or planned leaf that answers unrelated questions. Merge duplicated answers that lack distinct roles. Relocate an answer under the question it serves. Remove material that serves no necessary question. Make every transition show why the next reader question follows now. Revise the provisional root answer to match the supported leaves.

Plan, Draft, and Revise apply the required structural repairs. Review reports the same repairs as keyed findings without changing the prose.

Audit as a skeptical first-time reader:

- Can the reader follow each inference without supplying a missing premise?
- Is every distinction introduced before it changes the interpretation?
- Does every method or result arrive after the reader understands why it matters?
- Does the conclusion state exactly what the evidence establishes, weakens, leaves unresolved, or does not test?
- Is each claim's evidence state traceable to a named authority, with no conflict silently resolved?
- When a claim-bearing equation carries an inference, are the quantity it computes, its required assumptions, the reader question it answers, and its narrow conclusion aligned with the prose?
- When a figure or table carries an inference, does it answer a named reader question, expose the relevant comparison and its isolability limits, use labels that map to the prose, and support the same narrow conclusion?

### 5b. Audit prose and style

Run Step 5b for Draft, Review, or Revise only when line/style is in scope. A line/style-only pass preserves the existing structure unless it discovers a material inference problem, which it reports rather than silently redesigning.

Apply the disclosed style reference when required by Step 2. Then audit:

- Does any sentence contain more conceptual work than its neighbors prepare the reader to absorb?
- Would a compact equation make an important relationship easier to verify, and is every retained equation introduced and interpreted?
- Does each retained figure or table earn its place by reducing reader effort, enabling verification, or carrying necessary evidence?
- Are the visual's presentation and caption clear enough for the inferential role established in Step 5a?
- Could the reader explain why each paragraph is present and why the next one follows or the branch ends?

### Completion by branch

- **Plan:** the audited tree answers the governing question, orders every prerequisite, names source needs, and records every non-supported evidence state.
- **Review:** every material finding is keyed, actionable, and routed; claim-bearing findings have an evidence state; and the prose remains unchanged until any requested Revise begins.
- **Draft or Revise with structure/inference in scope:** every retained sentence serves the answer or inference path; every retained source-governed or support-disputed claim-bearing leaf is supported by a named authority; unsupported claims are removed or narrowed; unresolved and authority-conflict states remain routed rather than drafted as settled; and every inference path is continuous.
- **Line/style-only Revise:** every authorized edit improves the requested line-level property while preserving the claim, scope, evidence state, question tree, and inference path; any structural or support blocker is recorded and routed without semantic repair.
- **Combined Review then Revise:** the Review findings are recorded before mutation, and the final output satisfies the Revise criteria within the authorized mutation boundary.

A final-ready question-led pass contains no unsupported required claim, unresolved required support, authority conflict, or required `\gap`. Completion of this skill does not mark repository manuscript prose share-ready; deterministic checks, independent review, and required author approval remain governed by repository `AGENTS.md`.
