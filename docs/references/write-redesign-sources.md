---
title: "/write redesign — source index"
tags: [reference]
---

# /write redesign — source index

The canonical context for the `/write` redesign. Point every subagent here as its source set. Eight asset groups.

## 1. The methodology research (the canon — most important for the ideal-design step)
- [`docs/references/scientific-writing-methodology.md`](scientific-writing-methodology.md) — the established writing canon: Gopen-Swan (topic/stress,
  reader-expectation), Williams (old-to-new/given-new), Schimel (OCAR/narrative), Swales (CARS intro moves),
  McEnerney (value-to-reader), Mensh-Kording (Context-Content-Conclusion fractal), Whitesides (outline-first).

## 2. The ecosystem audit (what 11 repos implement — the juice)
- [`docs/references/writing-skills-ecosystem-audit.md`](writing-skills-ecosystem-audit.md) — per-repo scorecard, the convergent model, and the ranked
  catalog of transferable mechanisms (groups A claim-grounding · B structure · C voice · D review · E ideation).

## 3. Supervisor feedback (the ground-truth failure)
- [`docs/references/supervisor-feedback.md`](supervisor-feedback.md) — Claudio's (IMDEA) feedback on the v0.1 manuscript: storytelling
  register (pts 1-3) + unmotivated passive (pt 4). The defect class the redesign must make unshippable.

## 4. The current apparatus (prior art = what's being redesigned)
- `.claude/skills/scientific-writing/` (SKILL.md + references + scripts + assets) — the current skill.
- `.claude/hooks/prose_writecheck.py` (D046 anti-AI-tell linter) · `.claude/hooks/honesty_writecheck.py` (D044
  unsourced-number flag).
- `.claude/agents/prose-register-auditor.md` (D046 register reader).
- D047 register convergence-gate (Stop hook, content-hash-keyed verdict).
- [`docs/references/scientific-writing.md`](scientific-writing.md) — short stub/pointer (29 lines; not a real asset, flagged).

## 5. The S33 diagnosis (analysis already paid for)
- "Immune system, not a notion of health": the apparatus detects defects but encodes no positive model of good
  writing. Three defect classes: A register/storytelling (semantic, no banned token) · B passive (hybrid) · C
  lexical AI-tells (deterministic). Lives in this session's history + [`docs/upspeed.md`](../upspeed.md) (S33) + [`learnings.md`](../learnings.md) L054/L057.

## 6. Our own writing as test cases (before/after)
- `docs/manuscript/extended/main-extended.tex` — the v0.1 that drew Claudio's feedback (bad), now mid-clean with
  the finalized abstract (good). Real before/after to test any redesign against.
- `docs/reports/R06*.md`, `docs/reports/R07*.md` — finished finding-reports.

## 7. External exemplars + raw repos
- `data/papers/` — real ICLR/venue brain-LM papers (Moussa, Oota, bilgin) = the style anchors.
- `data/reference-repos/` — the 11 cloned skill repos (richest: `evoskills`, `bahayonghang/academic-writing-skills`,
  `k-dense-ai/scientific-agent-skills`, `imbad0202/academic-research-skills`, `jamditis/claude-skills-journalism`).

## 8. Brain memories on writing taste
- `manuscript-prose-taste` · `continuous-critique-while-writing` · `report-writing-style` (gbrain + project-local
  memory). Erfan's standing prose preferences.

---
**Working artifact:** `docs/references/write-redesign-design.html` — the living design canvas (ideal system first,
then projected to Claude Code reality).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
