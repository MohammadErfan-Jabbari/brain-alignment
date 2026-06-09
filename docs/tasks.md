# Tasks — the path behind and ahead

Durable backlog. The session task tracker is ephemeral; this file is the source of truth across
sessions. Move items between sections; don't delete (strike completed ones with a date).

## Now (current focus)

- [ ] **Re-evaluate D008 dataset choice before pulling anything.** Registry (05) surfaced denizenslab CC0 (regression-ready, CC0, ~50 subjects, working loader in speech-llm-brain) and Tuckute 2024 (noise ceiling r≈0.56, 165 subjects, 2.7k sentences) as credible alternatives to LeBel ds003020. Compare on noise ceiling, subjects, download size, loader work. Make the decision and record it.
- [ ] **Stage real neural responses + re-run E001 for the real verdict.** Pull one subject from the chosen dataset; verify the fMRI matrix is actually in the download (L005) before treating it as ready. Run `--backend <chosen>`. De-risks A1/A2.
- [ ] **Decide the form of $\mathcal{L}_{\text{brain}}$** on real data. Trainable head (current placeholder, overfits — D010) vs frozen encoding-map loss vs CKA proxy. Write as a design note.

## Next (de-risk the thesis — ordered by leverage)

- [ ] **`paper-digest` the finalists** → `docs/literature/canonical/`: LeBel 2023 (primary benchmark), Merlin & Toneva 2026 "When LMs Lose Their Mind" (reframe trigger), Narratives (generalisation), Tuckute 2024 (newly elevated PRIMARY candidate).
- [ ] **Address the reframe flag (D008/`04`):** Merlin & Toneva 2026 proved the A3 premise via fine-tuning; sharpen the contribution to **compression/distillation at matched budget** so A3 isn't scooped. Fold into `01-research-landscape.md` and H001.

## Later (once the pilot says go)

- [ ] Lock the baseline matrix runs (perplexity-only KD, structure-aware KD, alignment-guided, hybrid).
- [ ] Build the anti-confound evaluation harness (contiguous splits, nuisance baselines).
- [ ] Promote H001 to a Design with a locked protocol; add competing hypotheses H002/H003.
- [ ] **(DEFERRED until feasibility holds)** Define the "edge" deployment scenario concretely
      (FLOPs/latency/params target). Not in scope until the fundamental question is answered.

## Infrastructure / housekeeping

- [x] 2026-06-09 — **Disabled the GateGuard fact-forcing + doc-file-warning ECC hooks** for this repo via
      `.claude/settings.json` `ECC_DISABLED_HOOKS` (D012). Settles the Session-2 friction.

## Done

- [x] 2026-06-09 — **Dataset registry** → `docs/05-dataset-registry.md`. 11 neural/behavioral datasets with full feature profiles. Key finds: zhu-2025 out of scope (non-language), yin-2025 "Association" is synthetic NLP not neural (AUX), Tuckute 2024 elevated to PRIMARY candidate (noise ceiling r≈0.56). Division of labour clarified across `04`/`R02`/`05`. (cd79447)
- [x] 2026-06-09 — **Paper-repos corpus** → `scripts/paper-repos.tsv` + `scripts/clone_paper_repos.sh`. 21 repos shallow-cloned into `data/paper-repos/` (~8.6 GB, gitignored), 0 failures. Two open R02 URLs resolved (feghhi, merlin). (8178046)
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
