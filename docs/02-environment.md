---
title: "Environment — centcom"
tags: [reference]
---

# Environment — centcom

**Surveyed:** 2026-06-08. Treat as fact until the box changes; re-verify GPU/data before a long run.

## Hardware

| Resource | Spec |
|---|---|
| CPU | Intel Xeon Gold 6542Y — **96 logical cores** |
| RAM | **503 GiB** total, ~478 GiB free, no swap |
| GPU | **4× NVIDIA L40S**, 46 GB VRAM each (~184 GB aggregate) |
| GPU arch | Ada Lovelace, compute capability **8.9**, **bf16 supported** |
| Driver / CUDA | Driver 580.95.05; CUDA runtime 13.0; **wheels use the cu128 index** |

This comfortably trains/distills up to ~7B models and runs many fMRI-encoding regressions in
parallel. GPUs are usually idle (some resident memory from other namespaces occasionally).

## Disk

| Mount | Size | Free | Use for |
|---|---|---|---|
| `/home/centcom/data` (`/dev/sda`) | 3.5 T | **~1.2 T free** | all heavy artifacts (data, outputs, checkpoints) |
| `/` (overlay) | 436 G | ~204 G | do **not** put heavy artifacts here |
| `/dev/shm` | 32 G | 32 G | scratch |

Keep everything heavy under `/home/centcom/data/brain-alignment/{data,outputs}` (gitignored).

## Python / ML stack

- **Package manager: `uv` 0.10.11.** This repo is a minimal uv project (`pyproject.toml` with
  `[tool.uv] package = false` → no `src/`, no sample modules). **Always run code with `uv run`.**
- Venv: `.venv/`, Python **3.11.15** (matches brain-jepa).
- torch is **not installed yet** — add it pinned to the cu128 index (already configured in
  `pyproject.toml` under `[tool.uv.sources]`): `uv add torch`. Confirmed working elsewhere on this
  box: `torch 2.7.1+cu128`, `cuda.is_available() == True`, 4 devices, device name `NVIDIA L40S`.
- The HF + neuro stack is **not yet present**; add as needed:
  `uv add transformers datasets accelerate scikit-learn scipy nibabel nilearn` (and `wandb` if used).
- No conda/mamba, no Docker/Podman, no Slurm, no tmux/screen binary. **Long runs = background
  processes** (`nohup`, or this harness's background-run), not a multiplexer.
- Node v22.22.3 available.

## Cached models — reuse, don't re-download

Set `HF_HOME=/home/centcom/data/hf-cache` (32 G cache). Already present:

- **Qwen2.5: 0.5B, 1.5B, 3B, 7B** — a ready teacher→student ladder.
- **GPT-2 family: gpt2, gpt2-medium, gpt2-large, distilgpt2** — exactly the toy-pilot ladder the
  oracle recommended (medium → small).
- **EleutherAI pythia-1b**.

## Datasets on disk

- **Only neural dataset present: ABIDE** at `/home/centcom/data/brain-jepa/data/abide` (194 MB) —
  resting-state autism fMRI, CC200-atlas ROI timeseries (507 `.1D` files). This is **brain-jepa's**
  data and is **not** a language-fMRI corpus.
- **No language-fMRI dataset is staged** (no Pereira / Narratives / LeBel). Budget time to download
  one onto the 1.2 T volume — this is the gating resource for the thesis (see [`01-research-landscape.md`](01-research-landscape.md)).

## Network / remote

- **No Tailscale binary, no `~/.ssh/config` host aliases, no remote GPU pods** reachable from here.
- Treat centcom as a **single self-contained node**. No fleet dispatch.

## Practical run pattern

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache      # reuse cached models
uv add <packages>                                # add deps as the project grows
uv run python scripts/<name>.py --seed 42        # always via uv run
```

Closest working reference for layout, configs, and a 3-seed pilot runner:
`/home/centcom/data/brain-jepa` (uv + cu128, `scripts/objective_pilot.py`, `configs/*.json`).


## Related
- [`status.md`](./status.md) — the canonical status board
