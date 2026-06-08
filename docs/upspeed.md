# Upspeed — read first, write last

**Last updated:** 2026-06-08 (Session 1 — bootstrap + scope lock)

## Current state

Repo is set up, git-tracked, and scope is locked. Phase = **Map → Claim boundary**, but reframed:
the first objective is a **fundamental feasibility question — does the LLM↔brain alignment signal
carry usable, confound-free information that helps a downstream task?** Deployment/"edge" is deferred
until that holds. No experiments yet. Next concrete step is the language-fMRI benchmark survey, which
gates the toy pilot.

## What was done (Session 1)

1. Swarm reconnaissance of Nexus + the brain-alignment idea; built the `docs/` knowledge base.
2. Minimal uv environment (`uv run`, Python 3.11, no scaffolding); 20 canonical paper notes vendored.
3. Curated subagents (`lit-scout`, `paper-digest`, `oracle-reviewer`, `session-logger`) + CLAUDE.md.
4. Git initialized; 5 atomic scoped commits; adopted continuous-atomic-commit norm (D007).
5. Scope locked with Erfan (D006): MSc/UC3M, ~end-Aug-2026 deadline, feasibility-first, edge deferred.

## What to do next

1. **Survey + pick the language-fMRI benchmark, with a power analysis** (the #1 SPOF) — Pereira /
   Narratives / LeBel / Fedorenko; license, N, noise ceiling, power for a +0.05 effect. Use
   `lit-scout`; write `docs/04-data-benchmarks.md` with a recommendation. Commit atomically as you go.
2. Decide the form of $\mathcal{L}_{\text{brain}}$ (frozen encoding model / CKA proxy / differentiable).
3. Scaffold + run the toy pilot (GPT-2 medium → small, encoding fit before/after an alignment loss).

## Blockers

- No language-fMRI dataset staged on disk — the benchmark survey resolves where to get one.
- Exact thesis deadline TBD (tentative end of August 2026).

## Key facts

- **Run Python:** always `uv run` (`.venv`, Python 3.11). `export HF_HOME=/home/centcom/data/hf-cache`.
- **Compute:** 4× L40S (184 GB VRAM), 96 cores, 503 GB RAM, ~1.2 T free. Single node.
- **Closest code cousin:** `/home/centcom/data/brain-jepa` (uv + cu128, 3-seed pilot pattern).
- **Git:** initialized on `main`. Commit continuously and atomically (D007); push only when asked.
- **Deadline:** ~end of August 2026 (tentative).
