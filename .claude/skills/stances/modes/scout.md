# Scout mode

Bring external literature and data into the brain. This is the **Map** phase
(`docs/03-methodology.md`): it consumes external evidence, not our recorded numbers, and feeds Claim and
Design.

## The procedure (route to the existing agents)

- **Papers:** `lit-scout` (find and rank a shortlist; sonnet to gather, opus to judge relevance) →
  `paper-digest` (a canonical note in `docs/literature/canonical/`, opus). Inspect associated code and checkpoints directly when needed. The `firecrawl-research-index` skill is the second retrieval
  lane (semantic search + citation-graph expansion + in-body verify).
- **Data:** `dataset-scout` (find and characterize a candidate) → `dataset-verifier` (confirm it is
  actually usable on disk before any run depends on it).

## The standard

A paper's claim is not our number. Cite the source; an external result becomes ours only when a `/work`
session measures it. Guard against vibe-citing (a plausible-but-nonexistent reference assembled from
fragments) and leakage (filling a gap from parametric memory): a missing fact is a `\gap`, never
fabricated.

## Boundary

Finds, characterizes, and notes external evidence. It does not run our experiments (`/work`) or
adjudicate our verdicts (`/interpret`).
