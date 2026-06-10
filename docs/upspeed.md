# Upspeed — read first, write last

**Last updated:** 2026-06-10 (Session 5 — analysis — course material adopted as theory-grounding source)

## Current state

Phase = **Run → Judge**, climbing the R03 ladder. **The premise survived its first real-data test** (E002, A2 PASS on Tuckute), and as of this session the thesis now has an explicit **theory-grounding source**: Erfan's MSc coursework (Information Theory for ML + Probabilistic ML), curated in `docs/06-theory-grounding.md`. The math R03 was invoking informally now has its exact, proved, citable form — the weak-prior bound IS the MI generalization bound, "unique R²" IS conditional MI, the compression brake IS the data-processing inequality, the F1 trade-off IS rate-distortion. This is scaffolding for *writing* the thesis, not new evidence; the experimental ladder is unchanged. The open scientific risk is still **A3** (does the signal *buy* anything practical).

## What was done (Session 5 — analysis)

1. **Adopted the coursework as a third source of truth (D014).** Recon via 3 subagents established it needs **no re-OCR** — the existing `*_study.md`/`*_OCR.md` notes beat any fresh extraction (L010). The job was curation, not extraction.
2. **Wrote `docs/06-theory-grounding.md`** — the concept→thesis map (load-bearing: MI bound, DPI, conditional MI, rate-distortion; plus the ridge=Bayesian-MAP and TabPFN=F2 links), syllabus inventory, gap list. Plus a gitignored `data/course-material/INDEX.md` for navigation.
3. **Folded the math into the live docs.** R03 §2 gained **Step 7** anchoring the bounds to the course theorems; `01-research-landscape.md` §E and `CLAUDE.md` now point at 06; `docs/README.md` map updated.
4. **Fixed R03 line-1 corruption** (pasted IT-lecture transcript in front of the heading; HEAD was clean, working tree was not).

## What to do next (R03 ladder order — unchanged)

1. **Layer 1 — is the signal a lever?** Brain-tune Qwen2.5-0.5B (or GPT-2) on Tuckute; verify unique R² *rises* with the brain loss. Cheapest next step — Tuckute wired, harness exists. The first **working** experiment of the next session.
2. **LeBel time-series adapter** (FIR/lag, contiguous story splits) — makes the powered voxelwise benchmark runnable. Data on disk; loader is the work. **Not a config swap.**
3. **Layer 2 (A3)** — does induced/preserved alignment buy OOD generalisation or low-data sample-efficiency? The untested assumption; the thesis's real risk now.
4. **Decide $\mathcal{L}_{\text{brain}}$ form** on real Tuckute data (frozen encoding map vs CKA proxy vs trainable head — D010 still open).
5. **Reconcile the concurrent literature pass.** A parallel session committed (while Session 5 ran) full-read digests of the 12 brain-as-training-signal papers (`9c6dcb7`), a landscape-map update (`93db8ae`), and a **new `reports/R04` gap analysis** (`d5314b2`). Next session: read R04, and make sure R03 §2 Step 7 (new theory grounding) + R04 + the updated landscape tell one consistent story. LeBel 2023 + arXiv 2602.07547 may still want dedicated digests — check against what the 12-paper pass already covered.

## Blockers

- **None rate-limiting.** Data is staged, signal is confirmed real, theory grounding is now mapped. Next steps are method/experiment work.
- Framing watch: pitch as **alignment-guided distillation at matched budget (F1) / low-data regularizer (F2)**, NOT "use fMRI to train an LM" (scooped). Compete on the rate-distortion trade-off curve (now formally grounded — 06 §4), not a preserve-vs-destroy binary.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`. GPUs: 4× L40S (free index via `CUDA_VISIBLE_DEVICES`). Long runs via the harness background runner (plain `nohup &` died silently once — prefer the harness mechanism).
- **E002 rerun:** `CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 uv run python scripts/run_encoding_feasibility.py --models gpt2 gpt2-medium Qwen/Qwen2.5-0.5B --untrained-seeds 0 1 2`
- **Datasets on disk:** Tuckute (`data/tuckute2024/data/`), LeBel UTS03 (`data/lebel_ds003020/preprocessed_data/UTS03/`), Pereira stimuli, 21 paper repos. All gitignored.
- **Course material:** `data/course-material/` (gitignored, ~292 MB). **Do not re-OCR** — use the `*_study.md`/`*_OCR.md` notes. Thesis map: `docs/06-theory-grounding.md`.
- **Direction doc:** `reports/R03_brain-as-training-signal.md` is the live map of the idea + ladder; §2 Step 7 now carries the formal grounding.
- **Git:** `main`. Commit continuously/atomically (D007); push only when asked. GateGuard hooks disabled (D012).
