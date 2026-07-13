---
title: "Timeline — 2026-06-10 — Real-data A2 pass (E002) + brain-as-training-signal reframe (R03)"
tags: [timeline]
---

# Timeline — 2026-06-10 — Real-data A2 pass (E002) + brain-as-training-signal reframe (R03)

**Mode:** working session (produced evidence) with an analysis deliverable (R03).
**Trigger:** Erfan, autonomous overnight: review prior session + files; decide & download 1–2 real datasets the literature uses; reason about his inversion idea (use fMRI + alignment map to *train* the LM) from first principles, read top-conference papers, build the idea layer by layer; use gbrain + subagents + model-sized delegation.

## What ran / what was produced

1. **Got up to speed** — read the full `docs/` brain (charter, landscape, methodology, decisions D001–D012, learnings L001–L006, E001) and the pilot code. gbrain query returned only the sessions already reflected in `docs/`; no new context there.

2. **Staged TWO real datasets (D013).** Tooling: `osfclient` + `awscli` `uv pip install`ed (DataLad/git-annex unavailable and unnecessary — anonymous S3 sufficed).
   - **Tuckute 2024** → `data/tuckute2024/` (OSF ru38b `data.tar`, 7.5 MB): 1000 baseline sentences × 5 LH language ROIs × 10 participants, + noise ceilings. Real ROI-level neural data.
   - **LeBel ds003020 / UTS03** → `data/lebel_ds003020/preprocessed_data/UTS03/` (~20 GB, 84 story HDF5s) synced from OpenNeuro S3. **Verified (L005):** each HDF5 holds `data` = (TRs × 95,556 voxels) — the real voxelwise response matrix is present.

3. **Built + ran E002 — real-data encoding feasibility (the A2 question).** New `load_tuckute` adapter + `scripts/run_encoding_feasibility.py` reusing the pilot's anti-confound machinery. Result: **A2 PASS** across gpt2 (+0.0200), gpt2-medium (+0.0187), Qwen2.5-0.5B (+0.0362) unique mid-layer R² beyond nuisance under contiguous splits; untrained controls **negative** across 3 seeds; trained−untrained +0.030 to +0.050; NC-normalised 5–10%. → `docs/experiments/E002_*.md`, `outputs/E002_tuckute_feasibility.json`. This is the verdict E001 (synthetic) could never give.

4. **Confronted the inversion idea with the literature (2 subagents: lit-scout + paper-digest, sonnet).** Finding: "use fMRI to train an LM" is **already published**, text LMs included (brain-tuning: Moussa/Toneva speech ICLR'25+NeurIPS'25; Bilgin/Wehbe text ICLR'26; Merlin/Toneva causal ICLR'26). Wrote canonical note [`moussa-2025_brain-tuning-speech-lms.md`](../literature/canonical/moussa-2025_brain-tuning-speech-lms.md); updated [`01-research-landscape.md`](../01-research-landscape.md) (rows + tightened gap).

5. **Wrote R03** (`docs/reports/R03_brain-as-training-signal.md`): first-principles interrogation (info-budget bound → brain = weak regularizer, valuable only in low-data/compressed regimes), the scooping map, 3 evolved framings (F1 distillation / F2 low-data / F3 fMRI-free abstraction proxy), and a kill-gated experimental ladder (Layer 0 = E002, done). Recorded learnings L007 (A2 pass) + L008 (idea partly scooped).

## What's next to run (ordered)

1. **Layer 1 — is the signal a lever?** Brain-tune a small model (Qwen-0.5B / GPT-2) on Tuckute, verify unique R² rises. Cheapest next experiment; Tuckute already wired.
2. **Build the LeBel time-series adapter** (FIR/lag, contiguous story splits) so the powered voxelwise benchmark is runnable — the Layer-3 thesis-result data is on disk but not yet loadable.
3. **Layer 2 (A3) — does induced/preserved alignment buy OOD or low-data gains?** This is the untested assumption and the thesis's real risk.
4. Decide $\mathcal{L}_{\text{brain}}$ form on real data (frozen map vs CKA vs trainable head; D010 still open) — now decidable on Tuckute.
5. `paper-digest` the remaining finalists (Merlin&Toneva 2026, Bilgin/Wehbe 2026, LeBel 2023, arXiv 2602.07547).

## Decisions / learnings this session
- **D013** — stage Tuckute (fast Layer-0/1) + LeBel UTS03 (powered Layer-3); refines D008, doesn't reverse it.
- **L007** — A2 holds on real data (trained > 0, untrained < 0).
- **L008** — the inversion is largely scooped; the open slice is distillation-at-matched-budget / low-data.

## Commits
`0072dad` feat(scripts) tuckute loader + E002 runner · `3ce434c` docs(lit) brain-tuning prior art · `c5f015c` docs R03 + D013 · (close commit to follow with E002 doc + learnings + upspeed + tasks).


## Related
- `ladder.md` — the canonical status board
- `map.md` — code system (Q/E/A/D/L) & journey map
