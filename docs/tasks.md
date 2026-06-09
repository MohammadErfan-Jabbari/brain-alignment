# Tasks — the path behind and ahead

Durable backlog. The session task tracker is ephemeral; this file is the source of truth across
sessions. Move items between sections; don't delete (strike completed ones with a date).

## Now (current focus — climbing the R03 ladder)

- [ ] **Layer 1 — is the signal a *lever*?** Brain-tune Qwen2.5-0.5B (or GPT-2) on Tuckute; verify unique R² *rises* with the brain loss vs baseline. Cheapest next experiment — Tuckute wired, harness built. First working experiment of next session.
- [ ] **LeBel time-series adapter** (FIR/lag, contiguous story splits) so the powered voxelwise benchmark (UTS03, on disk, response matrix verified) is runnable. **Not a config swap** — real loader work.
- [ ] **Decide the form of $\mathcal{L}_{\text{brain}}$** on real Tuckute data. Trainable head (placeholder, overfits — D010) vs frozen encoding-map loss vs CKA/abstraction proxy. Now decidable on real data; write as a design note.

## Next (de-risk the thesis — ordered by leverage)

- [ ] **Layer 2 (A3) — does alignment buy something practical?** OOD generalisation and/or low-data sample-efficiency of a brain-regularized small model vs matched baseline (R03 F2). The untested assumption and the thesis's real risk now that A2 holds.
- [ ] **`paper-digest` the finalists** → `docs/literature/canonical/`: Merlin & Toneva 2026 "When LMs Lose Their Mind", Bilgin/Wehbe 2026 (text-LM brain-tuning), LeBel 2023, arXiv 2602.07547 (compression-already-preserves-alignment counter-evidence).
- [ ] **Sharpen the contribution per R03:** pitch as alignment-guided **distillation at matched budget (F1)** / **low-data regularizer (F2)** — NOT "use fMRI to train an LM" (scooped, L008). Engage arXiv 2602.07547 (compete on the trade-off curve). Fold into `01-research-landscape.md` and H001. Consider F3 (fMRI-free abstraction/LID proxy) as stretch.

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

- [x] 2026-06-10 — **Two real datasets staged (D013):** Tuckute 2024 (`data/tuckute2024/`, real ROI-level) + LeBel UTS03 (`data/lebel_ds003020/`, ~20 GB voxelwise, response matrix verified L005). Via osfclient + anonymous S3. Resolves the D008 "re-evaluate before pulling" task.
- [x] 2026-06-10 — **E002 real-data encoding feasibility → A2 PASS.** Trained LM mid-layer unique R² positive (gpt2 +0.020, gpt2-medium +0.019, Qwen2.5-0.5B +0.036), untrained controls negative (3 seeds). `experiments/E002_*.md`. The verdict synthetic E001 could not give. (L007)
- [x] 2026-06-10 — **R03 brain-as-training-signal direction doc** + brain-tuning prior-art sweep (2 subagents): the inversion is largely scooped (L008); unscooped slice = distillation-at-matched-budget / low-data. Canonical note `moussa-2025`, landscape updated.
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
