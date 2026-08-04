# Style guardrails and repair patterns

Use this reference during line editing, terminology audits, and a final line-level pass. Aim for prose that is precise, restrained, and easy to reconstruct. A lexical match alone is not a finding. Flag or repair a form only when it creates ambiguity, unsupported strength, unstable terminology, or avoidable reader effort. Retain a suspect form when it expresses an exact relationship more clearly than the direct alternative.

This reference is a lexical and line-editing checklist. It does not determine evidence strength, statistical meaning, novelty, scientific terminology, or claim scope. Preserve those decisions from their governing authority. When a repair would change one of them, report and route the issue instead of making the change during the style pass.

## Convention repairs

| Review trigger | Positive repair | Retain when |
|---|---|---|
| Contrast-first definitions such as “X is not Y,” “X rather than Y,” or “not merely X but Y” | Define X positively by its source, role, operation, or estimand. Give Y its own direct statement when the distinction remains necessary. | The alternative itself carries the inference, identifies a control, or prevents a material misreading. |
| Negative category labels such as “non-X” | Name the object's actual source, construction, role, or tested alternative. | The field has an established, unambiguous technical term and replacing it would reduce precision. |
| Several claims joined by `and`, `or`, `while`, or `respectively` | Use parallel grammar or separate sentences so the logical relation and scope of each claim are explicit. | The coordination has one unmistakable logical reading. |
| Em dashes | Replace with a full stop, comma, colon, semicolon, or parentheses according to the relationship between the clauses. | Do not retain them in this style. |
| Placeholder referents such as “this,” “these findings,” “the former,” or “the latter” | Name the result, method, comparison, or limitation being referenced. | The referent is adjacent and uniquely identifiable. |
| Empty importance markers such as “Importantly,” “Notably,” “Interestingly,” or “It is important to note that” | State the consequence that makes the claim important. Delete the marker when the sentence already carries its own weight. | The word encodes a defined statistical or technical status. |
| Author choreography such as “We now turn to,” “This section will discuss,” “As mentioned above,” or “It can be seen that” | State the next answer or the dependency that makes the next question follow. | Navigation is genuinely needed in a long document and names a useful destination. |
| Synonym variation for an established concept | Reuse the stable term. Introduce a new term only for a real distinction. | The terms have different definitions that matter to the current claim. |
| Experiment chronology, internal identifiers, or implementation narration in explanatory prose | Organize by the scientific or argumentative role the material serves. | Chronology or implementation order is itself part of the claim. |
| A limitation added by reflex | State only the limitation that changes the conclusion, bounds interpretation, or prepares the next question. | The limitation performs one of those roles. |
| Unqualified praise or evaluation | Name the measured property, comparison, mechanism, or consequence. | The evaluation is a defined term with an explicit criterion. |

## Suspect-language review list

Review these words when they are used for tone rather than exact meaning. The positive target is in the right column.

| Suspect words | Prefer |
|---|---|
| delve, embark, realm, landscape, tapestry | Name the action, topic, population, or boundary directly. |
| leverage, utilize, harness | use, apply, estimate, compare, or test, whichever names the operation. |
| pivotal, crucial, cornerstone, testament, showcase | State the decision, dependency, measured consequence, or evidence. |
| foster, facilitate, enable | Name the mechanism or use “supports” or “allows” only when the evidence warrants it. |
| underscore, highlight, reveal | State the implication directly and identify the evidence that supports it. |
| demonstrate, prove | Use “supports,” “establishes under the stated assumptions,” or “is consistent with” at the warranted strength. Reserve “prove” for a proof and “demonstrate” for evidence that identifies the stated claim. |
| multifaceted, nuanced, intricate, holistic | Name the relevant dimensions, distinctions, dependencies, or coverage. |
| paradigm, synergy | Name the model, framework, interaction, or joint effect. |
| streamline, cutting-edge, groundbreaking, transformative, unprecedented, revolutionary | State the baseline and the measured change. |
| comprehensive | Name the covered set. Retain only when the coverage is exhaustive relative to that declared set. |
| robust | Name the perturbation, sensitivity analysis, or statistical property and its result. |
| significant | Use “statistically significant” with the named test, or state the practical consequence instead. |
| novel | State the difference from prior work only when the governing literature record establishes that boundary. Otherwise route the claim to the literature owner; do not settle novelty during a style pass. |
| clearly, obviously, simply | State the reason or omit the modifier. |

## Repair examples

Contrast used as a definition:

- Compressed: “Brain alignment is a measurement rather than a training objective.”
- Direct: “Brain alignment measures held-out predictivity. Brain-response supervision uses responses in the training objective.”
- Material contrast: “The permutation tests stimulus--response pairing, not target content.” The contrast remains because it states the identifying boundary.

Empty evaluation:

- Inflated: “Importantly, these findings underscore the robustness of the proposed approach.”
- Direct: “Performance changed by less than the declared tolerance under the three sensitivity analyses.”

Negative category label:

- Vague: “a nonbrain control”
- Direct: “a text-derived control constructed from language-model features”

Unsupported strength:

- Overstated: “The experiment proves that the method generalizes.”
- Scoped: “Accuracy remained above the declared threshold on the held-out dataset; transfer to other domains was not tested.”

## Completion criterion

Complete the style pass when every triggered form has been reviewed, every retained exception carries exact meaning, each concept has one stable term, and the repairs preserve the claim, comparison, scope, and uncertainty. Stop when further changes would affect only taste, not meaning, inferential continuity, referent clarity, or reading effort.
