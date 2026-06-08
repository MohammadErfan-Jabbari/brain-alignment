# Tasks — the path behind and ahead

Durable backlog. The session task tracker is ephemeral; this file is the source of truth across
sessions. Move items between sections; don't delete (strike completed ones with a date).

## Now (current focus)

- [ ] **Survey + pick the language-fMRI benchmark, with a power analysis** — the #1 SPOF that gates
      everything. Survey Pereira 2018, Nastase *Narratives*, LeBel 2023, Fedorenko releases. Check:
      open license, N participants, noise ceiling, English/multilingual. Can the available N detect a
      +0.05 effect? Use `lit-scout` (+ `paper-digest` for the finalists). Write findings into a new
      `docs/04-data-benchmarks.md` with a clear recommendation. Commit atomically as you go.

## Next (de-risk the thesis — ordered by leverage)

- [ ] **Decide the form of $\mathcal{L}_{\text{brain}}$.** Frozen encoding model as fixed loss? CKA-style
      differentiable proxy? Compare candidates; write it up as a hypothesis-adjacent design note.
- [ ] **Run the toy pilot** (oracle's highest-value action): GPT-2 medium → small, measure
      encoding-model fit before/after an alignment loss. Forces the real pipeline; de-risks A1/A2.
      Models already cached (`02-environment.md`). → spawn `experiments/toy-pilot-gpt2.md`.
- [ ] **Fresh literature pass (2026):** confirm the gap is still open; pull any new
      brain-alignment-for-compression work. Use `lit-scout` + `paper-digest`.

## Later (once the pilot says go)

- [ ] Lock the baseline matrix runs (perplexity-only KD, structure-aware KD, alignment-guided, hybrid).
- [ ] Build the anti-confound evaluation harness (contiguous splits, nuisance baselines).
- [ ] Promote H001 to a Design with a locked protocol; add competing hypotheses H002/H003.
- [ ] **(DEFERRED until feasibility holds)** Define the "edge" deployment scenario concretely
      (FLOPs/latency/params target). Not in scope until the fundamental question is answered.

## Infrastructure / housekeeping

- [ ] **Initialize git** in this repo (currently not a git repo). Scoped commits only.
- [ ] First `uv add torch transformers datasets accelerate scikit-learn scipy` when the pilot starts.

## Done

- [x] 2026-06-08 — Swarm reconnaissance of Nexus + brain-alignment idea; built `docs/` knowledge base.
- [x] 2026-06-08 — Minimal uv environment (`uv run` verified, Python 3.11, no scaffolding).
- [x] 2026-06-08 — Repo `CLAUDE.md`, curated subagents, reasoning-frame reference.
- [x] 2026-06-08 — Git initialized; 5 atomic scoped commits; continuous-commit norm adopted (D007).
- [x] 2026-06-08 — Scope locked (D006): MSc/UC3M, ~end-Aug-2026, feasibility-first, edge deferred.
