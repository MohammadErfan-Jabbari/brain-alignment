# Upspeed — read first, write last

**Last updated:** 2026-06-15 (Session 15 — analysis / infrastructure. **Built the writing system the analysis week
runs on: the three-layer deliverable model (D035) + the `scientific-writing` skill.** No science rung changed; the
ladder is unchanged from S14. The original analysis task, R05 §9, is still pending and is now the next step.)

> **Canonical state lives in [`ladder.md`](ladder.md).** This is last-session prose. With no task, run `/orient`.

## What got built this session (not science — infrastructure)

1. **The three-layer deliverable model (D035, `03-methodology.md` "Deliverable layers").** Reports (Markdown, the
   *continuous* write-layer) → extended manuscript (LaTeX, internal master: always-current paper body + append-only
   checkpoint log) → public manuscript (LaTeX, frozen `vN` cuts compressed from the extended). Knowledge flows down
   only. **Reports are written continuously; the extended and public manuscripts are rebuilt only at a checkpoint
   Erfan explicitly calls — never auto-updated.**
2. **The `scientific-writing` skill (`.claude/skills/scientific-writing/`, 17 files).** Governs all three layers.
   Enforces anti-AI-tell scientific voice, graded hedging tied to what was measured, the `\evd`/`\gap` D011
   provenance discipline, and deterministic verifiers. **Run it for any report or manuscript writing.** Entry point:
   `uv run python .claude/skills/scientific-writing/scripts/run_checks.py --layer <report|extended|public> <path>`.
   Verifiers tested; the LaTeX assets pass a full `latexmk`+`biber` build.
3. **R05 §8 scaffolding refreshed** (the stale `r≈−0.92`→`−0.78` fixed; §11–§16 placeholders now name E017/E019/E020
   + L041). R05 narrative frontier unchanged: next is §9.

## What's next — resume the analysis lane (the original task)

> **📍 START HERE: [`docs/analysis-roadmap.md`](analysis-roadmap.md)**, Session A. Resume **R05 §9 (E005 → E008,
> the averaging-confound collapse)**, now written *through* the `scientific-writing` skill (it will lint the prose and
> check every number against the evidence). R05 is a report, so it takes the skill's report-layer path.
- The skill is in place, so the analysis week can produce reports + (at a checkpoint Erfan calls) the first extended
  manuscript. The first extended-manuscript checkpoint would seed from v0.9 (`manuscript/00_paper-draft-v0.md`).
- Forward-program rungs remain low-priority/parked (F3 superseded, F4 analysis-lane); no new compute needed for the paper.

## Blockers / open loops

- **Brain mirror pending:** D035 (the deliverable model + skill) should be mirrored to gbrain `projects/brain-alignment`;
  deferred this session for budget, do it at the next session start.
- No background jobs running. Nothing half-finished.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. 4× L40S.
- **Writing:** route all report/manuscript prose through the `scientific-writing` skill (D035). Reports = `docs/reports/`
  (md); manuscripts = `docs/manuscript/{extended,public}/` (LaTeX, checkpoint-derived). Short pointer:
  `docs/references/scientific-writing.md`.
- **Tooling (L043):** `/skill-create` (`ecc:skill-create`) is a git-history pattern extractor, NOT a skill-authoring
  tool. To author a designed skill, write it to spec or use `skill-creator:skill-creator` (the official plugin).
- **Reference framework:** `academic-research-skills` cloned read-only to `data/reference-repos/` (gitignored); we
  adopted patterns (C1–C6), not the plugin.
- **Subagent routing (D026):** opus = think/analysis/design; sonnet = doc-nav; haiku = mechanical. fable BANNED.
- **Git:** `main`, push only when asked. ~10 atomic commits this session. Untracked-and-harmless: `untitled.md`
  (scratch copy of an old `/goal` prompt). The coursework LaTeX templates were removed (S15) — the skill ships its own.
