---
description: Close a session by updating only authorities that changed, committing atomically, and pushing by default.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Close the session without routine documentation churn.

1. Inspect `git status --short` and the session changes.
2. Update only changed authorities: the owning E record, the extended manuscript, `docs/status.md`, and/or decisions/learnings.
3. Create a timeline only for a result, adjudication, correction, durable decision/learning, manuscript/public milestone, or lasting failure. Orientation, monitoring, continuation, formatting, and no-op sessions create none.
4. Confirm any new or changed scientific verdict with Erfan before recording it as settled.
5. Check the nearest `AGENTS.md` for changed folder contracts.
6. Run relevant tests, stage explicit paths only, make atomic conventional commits, and push to `origin` unless Erfan says not to or the push is blocked.

A no-op wrap may make no edits and no commit. Return only what changed, checks run, open blockers, Git state, and push result.
