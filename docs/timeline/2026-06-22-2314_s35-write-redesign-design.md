---
title: "S35 — 2026-06-22 — /write pipeline redesign: full design → BUILD-READY"
tags: [timeline]
---

# S35 — 2026-06-22 — /write pipeline redesign: full design → BUILD-READY

**Stances:** dominant **/meta** (build/maintain the apparatus). Crossed into **/scout** (cloned + mined 12 external
skill repos and 7 venue papers) and **/review** (5 clean-context opus critiques + 1 Codex pass). **NO /work, NO
science number, NO rung change — Q0–Q5 stand exactly as S33/S34.**

## What this session did

Took the `/write` stance + `scientific-writing` skill from "an immune system, not a notion of health" (the S33
diagnosis: it detects defects but encodes no positive model of good writing) to a complete, build-ready redesign.

1. **Established the methodology** (`docs/references/scientific-writing-methodology.md`). Researched the real canon
   of how to write a scientific paper (exa + firecrawl + web): Gopen-Swan (topic/stress, reader-expectation),
   Williams (old-to-new), Schimel (OCAR), Swales (CARS), McEnerney (value-to-reader), Mensh-Kording (C-C-C),
   Whitesides (outline-first); + Pinker (curse of knowledge) and Toulmin (warrant) pulled mid-session.
2. **Audited the ecosystem** ([`writing-skills-ecosystem-audit.md`](../references/writing-skills-ecosystem-audit.md)). Cloned 11 skill repos to `data/reference-repos/`,
   fanned out 13 readers. Finding: the whole ecosystem has our same shape (thick integrity/process, thin craft);
   the canon is almost entirely absent from tooling; the juice is the macro structure + claim-evidence machinery
   (evoskills, bahayonghang, k-dense, imbad0202, jamditis are the richest).
3. **Recorded the ground-truth failure** ([`supervisor-feedback.md`](../references/supervisor-feedback.md)): Claudio's 4 flagged sentences (storytelling
   register + unmotivated passive) — the permanent regression anchor.
4. **Designed the ideal system** (`write-redesign-design.html`, the living canvas, → v1.1). Four concerns —
   **Trust / Argument / Structure / Voice** — separated; a gated-loop spine (Evidence → Message&Reader → Claim&
   Argument Lattice → Architecture+Figures → Draft → Audit → Revise); human gates stages 1–3, convergence loop on
   4–6; "trust by gate + audit", not "by construction". Fluidity principle: methods are defaults not laws (RUB
   layer fluid, DET floor rigid).
5. **Projected to Claude Code (step 2):** 2a 21 functionalities → 2b 119-scenario TDD suite (`write-redesign-
   scenarios.md`, incl. real prose mined from venue papers + the F17 exemplar set) → 2c CC-primitive mapping
   (~10 subagents, ~6 hooks, 4 skill-sections, 2 gates, 4 artifacts) → 2d reverse coverage check (113/119 clean,
   6 re-mapped, no new agent). CC-power upgrades folded: parallel stage-5 audits, Stop-hook convergence,
   structured-output verdicts, gate via AskUserQuestion. `evidence.status` field + F19 consistency added.
6. **Recorded the build plan** ([`write-redesign-build-plan.md`](../references/write-redesign-build-plan.md)): the old→new migration map (lift the 9 DET scripts,
   rewrite the SKILL.md body, build the new spine), the Phase-1 walking skeleton (one section, full spine, the
   abstract case), build order, effort tiers.

**Adversarial discipline throughout:** every step independently opus-reviewed and hardened (clean-context
counter-critiques on the ideal design, the 2a matrix, the agent cohesion, the scenario suite, and a CC-power
review), Codex once. Each review's objections were adjudicated, not rubber-stamped (e.g. kept F8a un-split and
F9b separate against reviewer suggestions; conceded the 4th concern, the agent merges, the DET re-tags).

## Decisions / learnings
- **D048** — adopt the redesigned `/write` pipeline (4 concerns, gated-loop spine), build from scratch while
  lifting the existing DET scripts; walking-skeleton-first; effort HIGH (XHIGH for F4/F5/F11). Erfan-approved.
- **L058** — a quality/writing skill needs a *positive model of health*, not only defect detection; and the
  recurring design shape is "one judge, two sites" (read the plan, then the prose).

## Effort tiers (set, Erfan-approved)
HIGH all subagents; XHIGH for F4 (argument), F5 (scope), F11 (structure).

## Next
**Phase 1 — the walking skeleton** (`/meta`→`/work` build): lattice schema (F15) + claim-binding (F3, lift) +
minimal skeleton (F6) + drafter-with-\evd (F8a) + two audits (F12 voice lift + F9a/b) + gate (F16), run on the
abstract. Acceptance: catches Claudio's class (SC-VOICE-01–04), passes the near-misses, every claim \evd-bound.

## Notes / friction
- Parallel `git clone` of 9 repos all failed (anonymous-clone throttling); sequential clone worked. (Tooling note.)
- The HTML design canvas as a continuously-redeployed Artifact worked well as a living shared-read surface.
- Live science thread UNCHANGED since S25: Q4 sample-efficiency E024 (re-substrate → MDE positive-control → re-gate
  → build). Q2 ❌, Q3 ❌ stand.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
