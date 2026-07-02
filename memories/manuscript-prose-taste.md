---
title: "Manuscript Prose Taste"
tags: [memory, feedback, writing]
aliases: [manuscript-prose-taste]
origin_session: "0ff50b38-fa72-439e-9520-f896a054b043"
source_memory: "/home/centcom/.claude/projects/-home-centcom-data-brain-alignment/memory/manuscript-prose-taste.md"
---

# Manuscript Prose Taste

Standing prose preferences for `docs/manuscript/` and `docs/reports/`, given in S32 on 2026-06-22 during the extended-manuscript cleanup pass:

- **"kill-gated" is banned** from every manuscript and report. It is repo scaffolding/jargon, not reader-facing prose. Promote to the `ai_tell_lint` banned-register list as a `/meta` follow-up.
- **Openings must have taste.** An opening sentence that states a dry technical fact, such as "A reliable linear map predicts...", with no stakes is rejected. Lead with the idea/tension, for this repo often that the LM-to-brain correspondence has only ever been measured, never used.
- **Abstracts should not carry full numbers plus CIs.** Point estimates with bracketed CIs belong in Results; the abstract carries the qualitative headline.
- **Erfan wants a `taste-reader` subagent (opus)** that reads each paragraph and judges readability/taste, distinct from `prose-register-auditor`, which detects tells. Build at `.claude/agents/taste-reader.md`. Until built, run it inline per paragraph during a `/write` pass.

**Why:** the v0.1 manuscript reached the supervisor with storytelling-register prose (L054). Erfan is now driving a strict paragraph-by-paragraph clean and these are the taste standards he is enforcing.

**How to apply:** during any `/write` pass, after drafting a paragraph, run the taste read and fix clunk, murk, or flatness before moving on. Never put "kill-gated" in reader-facing prose.

## Related

- [Continuous Critique While Writing](continuous-critique-while-writing.md)
- [Manuscript Readability Lessons](manuscript-readability-lessons.md)
- [No Walls of Text](no-walls-of-text.md)
