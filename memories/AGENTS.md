---
title: "Memories Agent Guidance"
tags: [reference, memory]
aliases: [memories, claude-memories]
---

# Memories Agent Guidance

This folder mirrors the saved Claude project memories for `brain-alignment` from `/home/centcom/.claude/projects/-home-centcom-data-brain-alignment/memory/`. The point is portability: agents should not need hidden harness state to remember Erfan's collaboration and writing preferences.

These files are behavior guidance, not evidence. They can shape how an agent asks questions, writes, teaches, or reviews, but they do not authorize numbers or verdicts. For results, use [`docs/experiments/`](../docs/experiments) and the [canonical rewrite manuscript](../docs/manuscript/rewrite/); for current operations use [`docs/status.md`](../docs/status.md).

Do not add a `README.md` in this folder. Folder-local agent guidance belongs in `AGENTS.md`.

## Parity is the contract

This folder mirrors the harness memory directory one file to one file. A memory that exists there and not here is invisible to every harness that is not Claude Code, which is where most of this project's sessions have run. Check parity before trusting the index:

```bash
diff <(ls memories/*.md | xargs -n1 basename | grep -v -e AGENTS -e CLAUDE) \
     <(ls ~/.claude/projects/-home-centcom-data-brain-alignment/memory/*.md | xargs -n1 basename | grep -v MEMORY)
```

When a memory is added, changed, or retired in the harness, mirror it here in the same change. This folder once sat six of fourteen files behind, all of them manuscript-work memories, during a manuscript-only phase; Codex and Pi sessions ran on 57% of the stated preferences without any signal that the rest existed.

Converting a harness file to this folder's format means Obsidian frontmatter (`title`, `tags`, `aliases`, `origin_session`, `source_memory`), `[[wikilinks]]` rewritten as relative Markdown links, a `## Related` footer, and no em dashes.

## Index

| Memory | Use it when |
|---|---|
| [`ask-specific-not-vague-questions.md`](ask-specific-not-vague-questions.md) | Asking Erfan for direction. |
| [`continuous-critique-while-writing.md`](continuous-critique-while-writing.md) | Drafting manuscript prose. |
| [`manuscript-cutting-method.md`](manuscript-cutting-method.md) | Cutting a section that already carries its message. |
| [`manuscript-prose-taste.md`](manuscript-prose-taste.md) | Editing `docs/manuscript/` prose for taste. |
| [`manuscript-readability-lessons.md`](manuscript-readability-lessons.md) | Sentence-level manuscript revisions. |
| [`manuscript-revision-philosophy.md`](manuscript-revision-philosophy.md) | Deciding which layer to fix: claim, structure, or wording. |
| [`manuscript-typesetting-preferences.md`](manuscript-typesetting-preferences.md) | Judging page layout, tables, floats, and vertical space in a built PDF. |
| [`no-walls-of-text.md`](no-walls-of-text.md) | Sending progress updates or final summaries. |
| [`pause-when-scope-morphs.md`](pause-when-scope-morphs.md) | Scope changes across back-and-forth messages. |
| [`push-harder-and-watch-availability-bias.md`](push-harder-and-watch-availability-bias.md) | Judging whether a capability, search, or workflow is actually needed. |
| [`quiz-style-preference.md`](quiz-style-preference.md) | Teaching or checking Erfan's understanding. |
| [`report-writing-style.md`](report-writing-style.md) | Writing a `/teach` lesson or any long-form explanatory answer. |
| [`subagent-orchestration-for-manuscript-review.md`](subagent-orchestration-for-manuscript-review.md) | Briefing and dispatching agents for a manuscript review or cut round. |
| [`verify-the-premise-not-the-logic.md`](verify-the-premise-not-the-logic.md) | Judging a finding returned by an agent or a review. |

## Related

- [`../CLAUDE.md`](../CLAUDE.md)
- [`../docs/status.md`](../docs/status.md)
