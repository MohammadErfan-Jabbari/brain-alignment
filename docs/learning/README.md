# The learning ledger

This directory is the memory of the `/teach` stance. Each `NNNN-<slug>.md` file is one durable mastery
event: a finding the user demonstrably understands now, anchored to the report and the recorded number
it concerns. The filesystem is the state. On resuming a teaching session, `/teach` re-reads the records
for the report in play to know what is already mastered and what to teach next.

- **Format and the when-to-write gate**: `.claude/skills/stances/formats/learning-record.md`.
- **Records are evidence-gated**: written only on demonstrated mastery (or a corrected misconception),
  never on mere coverage.
- **Supersede, never delete**: a corrected understanding marks the old record `superseded by NNNN`.

Records accumulate as `0001-*.md`, `0002-*.md`, and so on. This README is not a record.
