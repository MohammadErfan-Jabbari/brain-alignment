# Upspeed — read first, write last

**Last updated:** 2026-06-08 (Session 1 — repo bootstrap)

## Current state

The repo is freshly set up. Phase = **Map → Claim boundary**. The brain-alignment idea is
literature-strong (digest in `01-research-landscape.md`) but execution-light; the prior work ended on
a **HOLD** verdict pending operational specificity. No code, no experiments yet. Minimal uv env is
live; `docs/` knowledge base is seeded.

## What was done (Session 1)

1. Swarm reconnaissance of the Nexus repo (v1/v2/archives) and the brain-alignment idea; pulled the
   origin idea, literature dossier, H001, frontier map, and oracle review.
2. Surveyed centcom (4× L40S, 1.2 T free, uv, cached Qwen2.5 + GPT-2 + pythia; only ABIDE on disk).
3. Built the minimal uv environment (`uv run` verified, Python 3.11, no scaffolding).
4. Seeded `docs/`: charter, landscape, environment, methodology, decisions, tasks, learnings,
   20 canonical paper notes + prior dossier/oracle review.
5. Wrote `CLAUDE.md` and curated subagents (`lit-scout`, `paper-digest`, `oracle-reviewer`,
   `session-logger`) + the reasoning-frame reference.

## What to do next

1. **Confirm scope facts** (deadline, program, "edge" scenario) — see top of `00-charter.md`.
2. **Pick the language-fMRI benchmark + power analysis** — the #1 SPOF (`tasks.md` → Next).
3. **Run the toy pilot** (GPT-2 medium → small, encoding fit before/after alignment loss).

## Blockers

- No language-fMRI dataset staged on disk — gating resource for any real experiment.
- A few scope facts unconfirmed with Erfan (deadline, program, deployment target).

## Key facts

- **Run Python:** always `uv run` (env: `.venv`, Python 3.11). Set `HF_HOME=/home/centcom/data/hf-cache`.
- **Compute:** 4× L40S (184 GB VRAM), 96 cores, 503 GB RAM, ~1.2 T free on `/home/centcom/data`. Single node.
- **Closest code cousin:** `/home/centcom/data/brain-jepa` (uv + cu128, 3-seed pilot pattern).
- **Git:** not yet initialized.
- **Deadline:** TBD (confirm).
