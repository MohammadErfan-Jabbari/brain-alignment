---
title: "Supervisor feedback closed; the submission derivative is ready to send"
tags: [timeline]
aliases: [submission-ready-supervisor-feedback-closed]
---

# Supervisor feedback closed; the submission derivative is ready to send

## Stance

`/write` → `/review` → `/wrap`

## What changed

Every item in the UC3M supervisor's 2026-08-27 feedback is closed in both manuscript trees, and no scientific verdict or number moved.

The supervisor named eight terms as unreadable jargon. `brain-response-content attribution`, `50-component linear target-projection measurability assay`, and `internal continuation criterion` now have zero occurrences in main-text prose; the rest are glossed in plain language at first use. `target uptake` and `retained-student movement` are defined where Section 2 first needs them, along with the fact that they are outcomes of an intervention rather than conditions its comparator has to satisfy. The abstract was rewritten once and shared byte-identically by both trees: it now states what was measured, what was compared against what, and what the comparison did and did not establish, without a single coined term.

The supervisor reported that Figure 10b and Table 22 disagreed. They did, and the defect was live in the canonical tree, not only in the derivative that had been sent: the bars were sized from the corrected keys while their labels were hardcoded with the superseded `24 passed` and `30 failed`. The labels are now the same keys, and the figure reads `37 = 20 + 16 + 1` in both trees. This is [L080](../learnings.md) and verification corpus rule 19.

The remaining figure and typography remarks are closed. Figure 1 no longer routes an arrow over its own blocks and no longer has touching boxes; two dependency arrows that geometry had hidden are visible. Figure 2's small-font bottom block is gone from the canonical tree, its text moved into the caption. Widow lines went from twenty in the rendered derivative to none in prose or captions, fixed with `\finalhyphendemerits`, per-paragraph `\looseness`, and ties rather than a global `\parfillskip` floor, which was tried first and made forty-five lines underfull without re-breaking any of them. Table and figure captions carry bold labels.

The four verification-layer defects from the layer's first live run are closed. Two over-attributed citations were narrowed to what their canonical notes actually support: `lage2019` to the repetition-averaging and reliability ceiling it derives, and `freteault2025` off the held-out-participant clause, which `moussa2025b` grounds instead. `lazic2010` was read and now has a canonical note, and the clause it supports is the inference-unit clause alone. The fourth, a derivative-only interpretive clause in Section 4, is the one item left for Erfan, because deleting prose that entered through the wrong tree is his call rather than a silent repair.

Two audits ran over the finished trees. The twin auditor returned the Figure 10b inversion plus twelve drift findings that were all one defect, the derivative using the short assay name where the canonical tree used the registered full one; both trees now use the full name once at its definition and the short form after, and both `AGENTS.md` files register that policy beside the term. The number auditor verified all seventy-eight keyed values against their owning records at each record's own precision and found one misattributed marker: Section 6 credited `E002` with establishing learned predictive access, which `E002`'s own 2026-08-04 correction records as unresolved because the untrained arm's static-embedding nuisance was built from its own model. That sentence is split so `E006` carries the byte-identical-nuisance claim and `E002` carries its own caveat, matching what the Results table already said.

## Durable next direction

The derivative builds at 67 pages with zero overfull boxes, passes `manuscript_check.py --share-ready` with no `\gap`, and is clean under `prose_lint.py`. Three cover-page fields cannot be verified from the repository and are the only thing between it and the supervisors: the exact master's degree name, the tutor ordering, and the place and date.

## Related

- [`status.md`](../status.md): current operational state
- [L080](../learnings.md): a keyed figure can still be hardcoded
- [`supervisor-feedback.md`](../references/supervisor-feedback.md): the verbatim feedback this closes
- [`manuscript-verification-rules.md`](../references/manuscript-verification-rules.md): rule 19
