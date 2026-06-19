# Learning-record format

A learning record is the **curated mastery layer** of `/teach` memory — the teaching equivalent of a
decision record: it captures a durable mastery event and why it changes what to teach next, so a later
session (post context reset) reconstructs where the user is by re-reading the records. It is NOT a session
journal. The raw per-session transcript — the learning process, every round and mistake — is the separate
**lesson** layer in `docs/learning/lessons/` (`lesson-format.md`). Records are distilled from lessons, and
records (not lessons) are the resume source of truth.

## Location and numbering

- Path: `docs/learning/records/NNNN-<dash-case-slug>.md`.
- Scan `docs/learning/records/` for the highest existing number and increment by one. Create the
  directory lazily if absent.

## When to write one (and when not)

Write a record ONLY when a durable, decision-grade thing happened:

1. the user cleared a sub-mode's mastery bar on something non-trivial (guided: answered the gating
   question unaided; feynman: reconstructed the recorded number unprompted; drill: N correct at the
   anti-cueing bar),
2. a real misconception was corrected (high value: predicts future stumbles on related topics),
3. the user disclosed prior knowledge that resets what to teach next.

Do NOT write a record for material that was merely covered. **Coverage is not learning. Wait for
evidence.** A `walkthrough` with no check passed writes nothing.

## The template

```markdown
---
subject: <concept | report Rxx | file path | experiment Exxx | paper slug | question>
number: <the specific recorded value, e.g. trained-minus-untrained gap = +0.021>
mode: guided|walkthrough|feynman|drill
status: active         # or: superseded by NNNN
date: YYYY-MM-DD
---

# {Short title of what was learned or established}

{1-3 sentences: what the user now understands (or what prior knowledge was established), the evidence
that demonstrated it, and why it changes what to teach next.}
```

The `number` anchor is what makes the ledger auditable against ground truth: a record claims the user
mastered a real recorded result, not a vibe. If the lesson concerned a mechanism with no single number,
put the source's claim handle (e.g. "per-individual null") in `number`.

## Supersession, not deletion

When a later record contradicts an earlier one (the user's reading was corrected, or understanding
deepened past the old record), mark the old one `status: superseded by NNNN` rather than deleting it.
The history of how understanding changed is itself signal.

## How the ledger is used

- **Resume**: on entering `/teach` for a report, re-read its records first; skip mastered findings.
- **Next topic**: the next thing to teach is a report finding with no passing record.
