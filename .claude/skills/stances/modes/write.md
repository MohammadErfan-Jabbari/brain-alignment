# Write mode

Turn a settled, paper-relevant finding directly into the canonical rewrite manuscript.

## Loop

1. Read the owning E records and current manuscript section.
2. Apply [`question-led-writing`](../../question-led-writing/SKILL.md) and complete its question tree for the active scope.
3. State the intended answer, claim, scope, caveats, and evidence.
4. Draft directly into `docs/manuscript/rewrite/`; do not create a report, lattice, convergence store, or checkpoint log.
5. Keep `\evd{Ennn}` evidence markers and keyed values in `numbers.tex`. A missing value is a `\gap`.
6. Run `uv run python scripts/manuscript_check.py docs/manuscript/rewrite`.
7. Ask one fresh independent reviewer to assess the question chain, prose, and scientific scope. Verify the findings, revise, and obtain Erfan’s approval for load-bearing framing.

If a source is contradictory or statistically suspect, stop writing that claim, set `manuscript-sync-pending` in `docs/status.md`, and hand it to `/interpret`.

## Boundary

`/write` reports settled evidence. It does not create a science number, adjudicate an experiment, apply scientific changes against the submission derivative, or mark the manuscript share-ready before all deterministic checks and fresh review pass.
