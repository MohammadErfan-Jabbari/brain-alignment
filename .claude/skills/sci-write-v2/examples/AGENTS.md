# Sci-Write v2 Examples Agent Guidance

This folder holds worked examples for the `sci-write-v2` skill. It is example/evaluation material, not thesis evidence.

## Files

| File | Role |
|---|---|
| `abstract-lattice.json` | Claim lattice for the manuscript abstract walking skeleton. |
| `abstract.tex` | F3/F6/F8a abstract output used by the acceptance evidence. |

## Acceptance Evidence Context

The abstract example demonstrates:

- Every claim is evidence-bound, with C1 bound to E006.
- Deferred result summaries are prose gaps where appropriate.
- Budget-argument and weak-prior sentences are framing, not bound claims.
- The deterministic check path passed after gate approval.
- The voice auditor caught the Claudio-style agency-to-abstraction class on a dirtied copy and did not flag the clean abstract.

## Rules

- Do not create a `README.md` here. Folder guidance belongs in `AGENTS.md`.
- Keep examples small and tied to the skill acceptance suite.
- Do not cite these examples as project results.
- If the lattice/prose gate behavior changes, update this file and the relevant `../SKILL.md` acceptance notes together.
