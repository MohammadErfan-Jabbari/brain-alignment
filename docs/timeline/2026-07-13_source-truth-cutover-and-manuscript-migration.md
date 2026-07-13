---
title: "Source-truth cutover and manuscript migration"
tags: [timeline, methodology, manuscript]
aliases: [source-truth-cutover-2026-07-13]
---

# Source-truth cutover and manuscript migration

The repository was cut from overlapping report, board, roadmap, checkpoint, and writing-pipeline surfaces to four authorities: experiment records for evidence, the extended manuscript for current interpretation, `docs/status.md` for operations, and decisions/learnings/selected timelines/Git for history. The pre-cutover state is recoverable from tag `pre-source-truth-cutover-2026-07-13`.

The usage audit processed all 757 backed-up Claude JSONL sessions and 35 repo-related Codex sessions, with no malformed files after session-ID reconciliation. Its compact component dispositions and redundancy measurements are recorded in D056; raw transcripts stayed outside Git and the disposable parser/index were not retained.

The cutover retired both scientific-writing pipelines, report-mode orchestration, routine multi-board wrapping, redundant reports and plans, monitoring-only timelines, duplicate manuscript archives, and E016 monitoring/router helpers. It retained one deterministic manuscript gate, the prose linter, experiment/recomputation code, and load-bearing artifacts named by their owning E records. The completed Markdown v0.9 draft moved to the frozen public tree.

Scientific migration corrected E006 to a conditional UTS03 result without voxel-population intervals, independently reviewed E016 before making it load-bearing, and integrated Q2, Q3, Q4, and the scoped E016 proxy-to-transfer failure directly into the extended manuscript. The manuscript now distinguishes an undemonstrated Q2 lever from a zero-effect claim, the averaged-target estimand from participant inference, the E013 mechanism failure from a substrate-wide null, and synthetic target fit from real-brain transfer.

At close of the mechanical cutover, all tracked Markdown links resolved and the unified provenance/number/reference/LaTeX gate passed. The fresh independent scientific-scope/prose review then caught a stale E002/E003 noise-ceiling normalization, an over-broad E024 abstract clause, and an E003 architecture-control sentence; these were corrected upstream and in the manuscript, and the focused re-review passed. Erfan’s approval of the load-bearing framing remained required, so `share-ready` was not set during migration.

## Related

- [Project status](../status.md)
- [Decision D056](../decisions/decisions.md)
- [Extended manuscript](../manuscript/extended/main-extended.tex)
