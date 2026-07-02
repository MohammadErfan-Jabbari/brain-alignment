---
title: "Repo Orientation for Agents"
tags: [reference, onboarding]
aliases: [repo-orientation, agent-orientation]
---

# Repo Orientation for Agents

This repository is a thesis research workspace, not a packaged software product. The durable source of truth is `docs/`; hidden harness memory, chat transcripts, and raw outputs are supporting context only.

## First Read

Read in this order when entering without a narrower task:

1. [`CLAUDE.md`](../CLAUDE.md) or [`AGENTS.md`](../AGENTS.md) for the operating contract and stance rules.
2. [`ladder.md`](ladder.md) for canonical current status and the next rung.
3. [`upspeed.md`](upspeed.md) for last-session continuity.
4. [`tasks.md`](tasks.md) for the granular backlog.
5. [`map.md`](map.md) when the `Q` / `E` / `D` / `L` codes or project arc are unclear.
6. [`../memories/AGENTS.md`](../memories/AGENTS.md) for repo-local copies of Claude's saved style and collaboration memories.

## Top-Level Structure

| Path | Role | Agent notes |
|---|---|---|
| [`CLAUDE.md`](../CLAUDE.md) | Main agent contract for this repo. | `AGENTS.md` points here so Codex-style agents and Claude share one contract. |
| [`README.md`](../README.md) | Root human entry point. | The only README that belongs in this repo. |
| [`docs/`](AGENTS.md) | Persistent research brain. | Status, decisions, reports, manuscript, literature, methodology, lessons. Prefer adding lasting research knowledge here. |
| [`memories/`](../memories/AGENTS.md) | Repo-local mirror of Claude project memories. | Collaboration and prose preferences. These guide behavior but do not replace evidence docs. |
| [`.claude/`](../.claude) | Claude Code apparatus. | Commands, agents, hooks, and skills. `.claude/state/` is ignored session state. |
| [`.agents/`](../.agents) | Alternate agent harness config. | Keep when useful, but do not treat it as the research source of truth. |
| [`scripts/`](../scripts/AGENTS.md) | Experiment runners, data adapters, analysis scripts, figure builders. | Use `uv run`; inspect the matching `docs/experiments/E*.md` before changing or running. |
| [`configs/`](../configs) | Small JSON configs. | Current example: toy pilot config. |
| `data/` | Heavy datasets and external corpora. | Gitignored. Do not move heavy data into tracked docs. |
| `outputs/` | Heavy experiment outputs and figures. | Gitignored except any deliberately copied report-ready artifact. |
| [`pyproject.toml`](../pyproject.toml) / [`uv.lock`](../uv.lock) | Python environment. | Minimal uv project, no package layout, Python >=3.11. |

## Evidence Trail

The research record is deliberately split:

| Artifact | Use |
|---|---|
| `docs/experiments/E*.md` | Designs, runs, and recorded results. Numbers should come from here or from scripts they cite. |
| `docs/reports/R*.md` | Current-truth finding reports, one major claim per report. |
| `docs/ladder.md` | Canonical verdict board. If another doc disagrees, fix the other doc. |
| `docs/decisions/decisions.md` | Decision log. |
| `docs/learnings.md` | Corrected mistakes and durable lessons. |
| `docs/timeline/` | Immutable session history. |

## Coding Conventions

- Always run Python through `uv run`.
- Use `HF_HOME=/home/centcom/data/hf-cache` for cached Hugging Face models when needed.
- Keep heavy artifacts in gitignored `data/`, `outputs/`, `checkpoints/`, `runs/`, or `wandb/`.
- Use scoped git staging only; do not stage the whole tree by habit.
- Before a compute run, read the relevant experiment doc and the controls/confound guidance named in `CLAUDE.md`.

## Related

- [`docs/AGENTS.md`](AGENTS.md)
- [`map.md`](map.md)
- [`../memories/AGENTS.md`](../memories/AGENTS.md)
