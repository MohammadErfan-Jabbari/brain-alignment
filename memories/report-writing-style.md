---
title: "Report Writing Style"
tags: [memory, feedback, writing]
aliases: [report-writing-style]
origin_session: "71679faf-ce23-434a-8467-7e86f31eafbd"
source_memory: "/home/centcom/.claude/projects/-home-centcom-data-brain-alignment/memory/report-writing-style.md"
---

# Report Writing Style

> [!note] Currency
> The `docs/reports/` layer was retired in `6026021` and no longer exists at HEAD. The preference itself still stands and now applies wherever the project explains itself to Erfan: `/teach` lessons in [`docs/learning/lessons/`](../docs/learning/lessons/), and any long-form explanatory answer.

For `docs/reports/` in brain-alignment, Erfan wants the *same* technical proficiency but a slower pace: ground claims in explicit formulas / learning theory, add more math, and surround it with plenty of explanatory prose. He reads these reports to understand stages of the research, so favor clarity and step-by-step derivation over terse density. When a paragraph asserts a conclusion, prefer to *derive* it (e.g. R03 §2: the "weak prior" bound rebuilt as MAP → information budget → channel capacity → DPI → PAC-Bayes).

**Why:** the reports are his learning surface; he liked the content but found terse dense paragraphs hard to absorb.

**How to apply:** keep all rigor and citations; break dense claims into labeled steps with display equations and prose between them; cross-reference sibling docs (R01/R02/R03, experiments, learnings). Honesty caveats (e.g. "order-of-magnitude heuristic, not a theorem") are welcome, not a weakness.
