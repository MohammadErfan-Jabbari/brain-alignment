# Upspeed — read first, write last

**Last updated:** 2026-06-10 (Session 4 — working — real-data A2 pass + inversion reframe)

## Current state

Phase = **Run → Judge**, climbing the R03 ladder. **The premise survived its first real-data test.** Real neural data is now on disk (two datasets), and the foundational A2 question — does an LM's representation predict brain activity *beyond confounds* — is **answered YES on real data** (E002). The thesis is no longer blocked on data or on the feasibility-of-signal question. The open risk has moved up the ladder to **A3** (does the signal *buy* anything practical).

Erfan's overnight "use fMRI to train the LM" idea was interrogated from first principles and against the literature: it is **real but largely already published** (brain-tuning, text LMs included). The unscooped contribution is narrower and is written up in **`reports/R03`** — read it.

## What was done (Session 4 — working)

1. **Two real datasets staged (D013).** Tuckute 2024 (`data/tuckute2024/`, real ROI-level, 1000 sentences × 5 LH lang ROIs + noise ceilings) and LeBel ds003020 UTS03 (`data/lebel_ds003020/preprocessed_data/UTS03/`, ~20 GB voxelwise, **HDF5 response matrix verified present** — L005). Pulled via `osfclient` + anonymous S3 `awscli` (no DataLad needed).
2. **E002 ran — A2 PASS on real data.** `scripts/run_encoding_feasibility.py` + `load_tuckute`. Trained unique mid-layer R²: gpt2 +0.0200, gpt2-medium +0.0187, **Qwen2.5-0.5B +0.0362** (best, 10% of NC); untrained controls **negative** across 3 seeds. → `experiments/E002_*.md`, `outputs/E002_tuckute_feasibility.json`.
3. **R03 written** — first-principles direction doc: info-budget bound (brain = weak regularizer), the 2025–26 scooping map, 3 framings (F1 distillation / F2 low-data / F3 fMRI-free proxy), kill-gated ladder. + canonical note `moussa-2025_brain-tuning-speech-lms.md`, landscape update, L007/L008.

## What to do next (R03 ladder order)

1. **Layer 1 — is the signal a lever?** Brain-tune Qwen2.5-0.5B (or GPT-2) on Tuckute; verify unique R² *rises* with the brain loss. Cheapest next step — Tuckute is wired, harness exists. The first **working** experiment of the next session.
2. **LeBel time-series adapter** (FIR/lag, contiguous story splits) — makes the powered voxelwise benchmark runnable. Data on disk; loader is the work. **Not a config swap** (correcting earlier optimism).
3. **Layer 2 (A3)** — does induced/preserved alignment buy OOD generalisation or low-data sample-efficiency? The untested assumption; the thesis's real risk now.
4. **Decide $\mathcal{L}_{\text{brain}}$ form** on real Tuckute data (frozen encoding map vs CKA proxy vs trainable head — D010 still open).
5. **`paper-digest`** Merlin&Toneva 2026, Bilgin/Wehbe 2026 (text-LM brain-tuning), LeBel 2023, arXiv 2602.07547 (compression-robustness counter-evidence).

## Blockers

- **None rate-limiting.** Data is staged, signal is confirmed real. The next steps are method/experiment work, not data or feasibility gates.
- Framing watch: pitch the thesis as **alignment-guided distillation at matched budget (F1) / low-data regularizer (F2)**, NOT "use fMRI to train an LM" (scooped). Must engage arXiv 2602.07547 (compression already preserves alignment → compete on the trade-off curve).

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`. GPUs: 4× L40S (use a free index via `CUDA_VISIBLE_DEVICES`). Background long runs via the harness background runner (plain `nohup &` died silently once this session — prefer the harness mechanism).
- **E002 rerun:** `CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 uv run python scripts/run_encoding_feasibility.py --models gpt2 gpt2-medium Qwen/Qwen2.5-0.5B --untrained-seeds 0 1 2`
- **Datasets on disk:** Tuckute (`data/tuckute2024/data/`), LeBel UTS03 (`data/lebel_ds003020/preprocessed_data/UTS03/`), Pereira stimuli (`data/pereira/`), 21 paper repos (`data/paper-repos/`). All gitignored.
- **Download tooling** (`osfclient`, `awscli`, `boto3`, `h5py`) is `uv pip install`ed into `.venv` (not in pyproject — transient infra).
- **Direction doc:** `reports/R03_brain-as-training-signal.md` is now the live map of the idea + ladder.
- **Git:** `main`. Commit continuously/atomically (D007); push only when asked. GateGuard hooks disabled (D012).
