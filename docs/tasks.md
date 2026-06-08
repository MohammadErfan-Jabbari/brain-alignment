# Tasks — the path behind and ahead

Durable backlog. The session task tracker is ephemeral; this file is the source of truth across
sessions. Move items between sections; don't delete (strike completed ones with a date).

## Now (current focus)

- [ ] **Stage real neural responses + re-run E001 for the real verdict.** The harness is built and
      synthetic-validated; the scientific question is still open. Pull **LeBel `ds003020` one subject**
      (anonymous S3 `--no-sign-request`, check size first, ≤ few GB) or source the **Pereira neural
      responses** (crwz7 was stimuli-only, L005), then run `--backend pereira`/lebel. De-risks A1/A2.
- [ ] **Decide the form of $\mathcal{L}_{\text{brain}}$** on real data. Trainable head (current
      placeholder, overfits — D010) vs frozen encoding-map loss vs CKA proxy. Write as a design note.

## Next (de-risk the thesis — ordered by leverage)

- [ ] **`paper-digest` the finalists** → `docs/literature/canonical/`: LeBel 2023 (primary benchmark),
      Merlin & Toneva 2026 "When LMs Lose Their Mind" (reframe trigger), Narratives (generalisation).
- [ ] **Address the reframe flag (D008/`04`):** Merlin & Toneva 2026 proved the A3 premise via
      fine-tuning; sharpen the contribution to **compression/distillation at matched budget** so A3
      isn't scooped. Fold into `01-research-landscape.md` and H001.

## Later (once the pilot says go)

- [ ] Lock the baseline matrix runs (perplexity-only KD, structure-aware KD, alignment-guided, hybrid).
- [ ] Build the anti-confound evaluation harness (contiguous splits, nuisance baselines).
- [ ] Promote H001 to a Design with a locked protocol; add competing hypotheses H002/H003.
- [ ] **(DEFERRED until feasibility holds)** Define the "edge" deployment scenario concretely
      (FLOPs/latency/params target). Not in scope until the fundamental question is answered.

## Infrastructure / housekeeping

- [ ] Consider disabling the GateGuard fact-forcing hook for long autonomous runs (Session-2 friction).

## Done

- [x] 2026-06-09 — **Language-fMRI benchmark survey + power analysis** → `docs/04-data-benchmarks.md`.
      SPOF resolved (D008): LeBel ds003020 primary, Narratives generalisation, Pereira plumbing.
- [x] 2026-06-09 — **Toy pilot harness built + validated** (synthetic): GPT-2-medium→small distillation,
      encoding model, anti-confound partition, ≥3 seeds → `scripts/`, `configs/`, `docs/experiments/E001`.
      (Real-data run moved to "Now"; synthetic cannot answer the science — L004.)
- [x] 2026-06-09 — `uv add torch transformers datasets scikit-learn scipy nibabel nilearn` (pilot deps).
- [x] 2026-06-08 — Swarm reconnaissance of Nexus + brain-alignment idea; built `docs/` knowledge base.
- [x] 2026-06-08 — Minimal uv environment (`uv run` verified, Python 3.11, no scaffolding).
- [x] 2026-06-08 — Repo `CLAUDE.md`, curated subagents, reasoning-frame reference.
- [x] 2026-06-08 — Git initialized; 5 atomic scoped commits; continuous-commit norm adopted (D007).
- [x] 2026-06-08 — Scope locked (D006): MSc/UC3M, ~end-Aug-2026, feasibility-first, edge deferred.
