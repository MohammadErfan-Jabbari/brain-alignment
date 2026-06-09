# Upspeed — read first, write last

**Last updated:** 2026-06-09 (Session 3 — analysis — dataset registry + paper-repos corpus)

## Current state

Phase = **Map → Claim/Design**. The dataset landscape is now fully catalogued (`05-dataset-registry.md`). 21 paper repos are shallow-cloned locally for inspection. The pilot harness (E001) is built, anti-confound-baked, and validated on synthetic data — it is one real-data pull away from producing a scientific verdict. **Real neural data is still not on disk.**

One live decision is open before the first pull: **re-evaluate D008 (LeBel primary) against denizenslab CC0** — the registry surfaced denizenslab as the fastest open path (regression-ready, working code, CC0 license) and Tuckute 2024 as a high-noise-ceiling candidate (r≈0.56). This must be resolved before pulling anything.

## What was done (Session 3 — analysis)

1. **`docs/05-dataset-registry.md`** built and committed (cd79447). 11 neural/behavioral datasets with full feature profiles (modality, subjects, stimuli, license, access, noise ceiling, use-case fit, status). Key findings: zhu-2025 is non-language (out of scope), yin-2025 "Association" is synthetic NLP not a neural dataset (AUX), Tuckute 2024 is a serious PRIMARY candidate (noise ceiling r≈0.56). Division of labour between `04`/`R02`/`05` clarified and written into each file.
2. **Paper-repos reference corpus** built and committed (8178046): `scripts/paper-repos.tsv` (manifest) + `scripts/clone_paper_repos.sh` (idempotent shallow-clone). Ran it: 21 repos in `data/paper-repos/` (~8.6 GB, gitignored), 0 failures. Resolved two open URLs from R02 (feghhi, merlin).
3. **L006** appended to `docs/learnings.md` (dataset provenance discipline).

## What to do next

1. **Re-evaluate D008: LeBel ds003020 vs denizenslab CC0 vs Tuckute 2024.** Compare noise ceiling, subject count, download size, existing loader. Make the decision, record it. This is a short working-session task before any data pull.
2. **Pull the chosen dataset (one subject).** Verify the fMRI matrix is actually present in the download (L005 — don't assume). Keep under a few GB.
3. **Re-run E001 on real neural data** (`--backend <chosen>`) — this is the actual scientific verdict on A1/A2.
4. **Decide $\mathcal{L}_{\text{brain}}$** (frozen encoding-map loss vs CKA proxy vs trainable head) on real data. Write as a design note.
5. **`paper-digest`** Merlin & Toneva 2026 and LeBel 2023 — still pending from prior sessions. Needed for G1 reframe check and literature notes.

## Blockers

- **Real neural data not yet on disk.** This is the only blocker that matters. Nothing else is rate-limiting.
- D008 LeBel-primary decision should be re-examined before pulling (denizenslab CC0 and Tuckute 2024 are now credible alternatives).

## Key facts

- **Run Python:** always `uv run` (`.venv`, Python 3.11). `export HF_HOME=/home/centcom/data/hf-cache`.
- **Pilot:** `uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json [--smoke]`. See `scripts/README.md`.
- **Compute:** 4× L40S, single node, background processes for long runs.
- **Data staged:** `data/pereira/Pereira_Materials/` (stimuli, GloVe, ROI masks — no neural responses). `data/paper-repos/` (21 shallow-cloned repos, gitignored).
- **Dataset registry:** `docs/05-dataset-registry.md` — full landscape. Tuckute 2024 (r≈0.56 noise ceiling, 165 subjects, 2.7k sentences) is now a serious PRIMARY candidate alongside LeBel.
- **denizenslab CC0:** fastest open path — regression-ready, working code in `speech-llm-brain` repo, CC0 license, ~50 subjects, reading + listening. Re-evaluate before pulling LeBel.
- **Git:** `main`. Commit continuously and atomically (D007); push only when asked.
- **GateGuard hooks disabled** for this repo via `.claude/settings.json` (D012).
