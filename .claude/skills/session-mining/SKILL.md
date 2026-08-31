---
name: session-mining
description: >-
  Answer a question from the repo's own session transcripts (Codex, Pi, Claude Code) without reading
  them into context. Use when asked what was done or decided in past sessions, why a choice was made,
  whether a piece of apparatus was actually used, or when docs and Git do not explain something. Also
  when asked to mine, audit, or measure the sessions, or to "check the old sessions".
tools: Read, Grep, Glob, Bash, Task, Skill
---

# Session mining

Most of this repo's work happened in Codex sessions. The transcripts are process evidence: they explain how a decision was reached, while the four authorities still record what stands. The root contract says where they are and warns they are far too large to read into context. This skill is the how.

**The rule that makes this work: define the questions first, then extract answers. Never read a transcript to see what is in it.** 2.3 GB of rollouts will fill any context window with the least informative bytes available.

## Where they are

| Corpus | Path | Notes |
| --- | --- | --- |
| Codex rollouts | `~/.codex/sessions/**/rollout-*.jsonl` and `~/.codex/archived_sessions/` | several hundred; filter with `grep -l brain-alignment` |
| Codex prompt log | `~/.codex/history.jsonl` | typed prompts only, cheapest first look |
| Claude Code | `~/.claude/projects/-home-centcom-data-brain-alignment/*.jsonl` | this harness |
| Pi | `~/.pi/agent/` | check the layout before assuming it matches Codex |

The Codex record shape:

```
{"type":"response_item","payload":{"type":"message","role":"user","content":[{"text":"…"}]}}
```

## Procedure

1. **Write the questions down before touching a file.** Three to six specific, answerable questions. "Was `/write` ever invoked" is answerable. "What was the writing workflow like" is not.
2. **Inspect the shape cheaply, once.** `jq -r .type | sort | uniq -c` on one file, or `head -c 2000`. Then stop looking at raw records.
3. **Build the file list first**, and reuse it: `grep -l brain-alignment <paths> > list.txt`. Keep it in the scratchpad, not in context.
4. **Stream, count, and print only aggregates.** Write a small script that opens files one at a time, filters to the record type you need, and prints a table. Never print a tool-result payload unbounded. Keep every output under about 4 KB. Prefer `mcp__plugin_context-mode_context-mode__ctx_execute` or a scratchpad script over inline heredocs when the analysis is more than a few lines.
5. **Print verbatim samples for every count you intend to report** — a handful, truncated to about 110 characters. This is the step that catches a wrong count, and it has caught one: see the hazard below.
6. **Anchor against Git.** Contrast what was asked with what was committed: `git log --since --until --oneline`. A transcript says what was intended; the commit says what landed. Where they disagree, the commit is the fact and the disagreement is the finding.
7. **Report the answers, not the method.** Aggregate tables, the samples, and what each answer licenses. If a finding is durable it goes to `decisions.md` or `learnings.md`; if it changes operations it goes to `status.md`. Do not create a mining report file.

For breadth, dispatch subagents per question rather than doing every question yourself, and give each one the file list and the exact output shape you want back. Declare `model:` and `effort:` on every dispatch and gate degenerate replies, per the [dispatch contract](../../AGENTS.md).

## The hazard that invalidates naive counts

**The injected instruction preamble rides inside a user-role message.** `AGENTS.md` and `CLAUDE.md` are delivered as user content, and this repo's contract names its own skills, so a frequency count over user messages measures *the instructions*, not the behaviour.

This is not hypothetical. A first pass here reported 10,197 stance invocations across the rewrite era. The verbatim samples printed beside the count showed nearly every hit was the preamble. Two filters fixed it: drop any message containing an injected marker, and require the `/name` inside the opening 60 characters of the prompt. That cut 45 apparent invocations to 0 ([L078](../../../docs/learnings.md)).

The general form: **mention is not invocation, and a plan document that names a command is not a use of it.** A residual set that all traces to one message beginning "PLEASE IMPLEMENT THIS PLAN" is measuring the plan.

Match the window to the question before drawing a conclusion. A writing-era window cannot tell you whether the evidence spine is used, because low `/work` usage in it is expected.

## Boundary

Transcripts are process evidence, never an authority. They do not produce a thesis number, settle a verdict, or override an E record, the canonical manuscript, or `status.md`. A number found in a transcript is a lead to check against its owning record, not a value to quote.

## Related

- [Root operating contract](../../../AGENTS.md)
- [Claude apparatus and the dispatch contract](../../AGENTS.md)
- [Learnings](../../../docs/learnings.md)
