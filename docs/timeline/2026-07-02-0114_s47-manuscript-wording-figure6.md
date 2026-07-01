---
title: "S47 - manuscript wording cleanup and Figure 6 deferral"
tags: [timeline, session]
---

# S47 - manuscript wording cleanup and Figure 6 deferral

## Purpose

Close the manuscript cleanup session after Erfan flagged weak Section 4.2 wording and asked whether Figure 6 should be finalized now.

## Stances

Dominant stance: `/write`.

Also used: `/review` to inspect Figure 6's source, manuscript references, and the Q/E mapping.

## What happened

- Erfan flagged two Section 4.2 phrases: "the same screen also narrows the verdict" and "the cold-init student carries the verdict." The problem was both semantic and stylistic: "screen" did not name the benchmark, and "verdict" had become a vague default handle.
- The Section 4.2 sentence now states the intended meaning directly: the E003 comparison limits the claim because alignment tracks log-perplexity across the five non-teacher arms, so the retention gradient could reflect language-model quality rather than the distillation objective itself.
- The manuscript tree was swept for `prose`, `verdict`, and standalone `screen`. Visible text and manuscript comments were rewritten with context-specific terms such as `text`, `writing`, `result`, `claim`, `primary statistic`, `key test`, `Tuckute ROI benchmark`, and `comparison`.
- A temporary attempt to encode the new word preference in the skill/lint layer was reverted immediately after Erfan clarified that the skills should be rewritten from scratch rather than patched here.
- The extended manuscript PDF was rebuilt successfully. The only warnings were the existing overfull boxes at `main-extended.tex:54`.
- Commit `f7cd1e2 docs(manuscript): replace weak result wording` was pushed to `origin/main`.
- Figure 6 was inspected. It is not a finalized asset in `docs/manuscript/figures/`; it is the placeholder `fig:lever` in Section 4.3, currently loading `../figures/fig_lever.png`. It maps to Q2/E004, not to Section 4.2.

## Decisions made

No new durable decision. Erfan's instruction is local for this manuscript pass: avoid the weak handles `prose` and `verdict` in manuscript text, and do not patch the old writing skills for this rule because those skills need a from-scratch rewrite.

## Current truth

No experiment ran and no ladder status changed. Section 4.2 is cleaner and current for Q1. Figure 6 is deliberately deferred until the Q2/Section 4.3 pass.

## Next session

Write Section 4.3 (Q2 / E004) and finalize Figure 6 in that same pass. The figure should show the E004 lever question at the honest fold-level inference unit: interval includes zero, fold 4 carries much of the old apparent signal, and the claim is "undemonstrated, not proven zero."

## Friction & improvements

The useful correction was not a synonym swap but naming the actual object. "Screen" becomes a specific benchmark or comparison; "verdict" becomes result, claim, primary statistic, or key test depending on the sentence. The skill layer is intentionally left alone for now.
