---
title: "brain-alignment — MSc thesis research repo"
tags: [reference, charter]
aliases: [brain-alignment, home]
---

# brain-alignment

Master's thesis (ML for Health, UC3M): **using the linear mapping between LLM middle layers and brain
activation as a usable signal.** Brain-alignment-guided distillation is the first concrete use case.

- **Start here:** [`docs/status.md`](docs/status.md) — current state and next steps.
- **Canonical thesis:** [`docs/manuscript/rewrite/main-rewrite.tex`](docs/manuscript/rewrite/main-rewrite.tex) — source; [`PDF`](docs/manuscript/rewrite/main-rewrite.pdf).
- **The idea & scope:** [`docs/00-charter.md`](docs/00-charter.md)
- **Literature & the gap:** [`docs/01-research-landscape.md`](docs/01-research-landscape.md)
- **Compute & how to run:** [`docs/02-environment.md`](docs/02-environment.md)
- **How we work (and why):** [`docs/03-methodology.md`](docs/03-methodology.md)
- **Knowledge-base map:** [`docs/AGENTS.md`](docs/AGENTS.md)
- **Repo-local Claude memories:** [`memories/AGENTS.md`](memories/AGENTS.md)

Agent operating contract: [`AGENTS.md`](AGENTS.md). Claude Code reads [`CLAUDE.md`](CLAUDE.md), a symlink to the same file. Run Python with `uv run`.
