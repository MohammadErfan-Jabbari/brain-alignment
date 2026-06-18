# Upspeed — read first, write last

**Last updated:** 2026-06-18 (S23 — working. Did **A + B to completion** under Erfan's direction. **A: E021 keystone → CLEAN NULL on cognition** (the RT edge over controls is signal SHAPE, not content — a phase-randomized twin ties it; surprisal-orthogonality null). **B: Moussa Path-A demonstration → NON-REPRODUCTION** (brain-tuning's downstream gain doesn't reproduce on our data → external demo off the table). Both negative. No rung flipped. Lit-sweep path recorded for a future build. Handed back for Erfan's report-reading.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (unchanged — Q0–Q5 stand). Expansion-program state: [`expansion-program.md`](expansion-program.md) + [`idea-tree.md`](idea-tree.md). With no task, run `/orient`.

## What ran (S23)
- **A — resolve E021 (keystone):** n=10 + learnability-matched controls (+ a phase-randomized shape control). **CLEAN NULL on cognition.** Human reading-time signal helps a frozen-probe more than its learnability predicts, but that edge is the target's *temporal/distributional shape* (autocorr 0.62 + kurtosis 13), reproduced entirely by a content-free phase-randomized twin (172.1 vs residual 177.4, tied). Surprisal-orthogonality null (raw≈residual). Mechanism pinned → a *stronger* negative. Arc: v2 bug-positive → v3 inconclusive → v4 likely-positive → v5 clean-null (each step corrected the last; L048/L049).
- **B — Moussa external demonstration (E022):** oracle-gated → reproduction pilot. brain−pretrained phoneme-F1 = +0.52 [−0.36,+1.40] (below the +2 gate). **NON-REPRODUCTION** → the matched-twin shrink-test is vacuous, not built. Honest scope: reduced single-subject setup, not a refutation. Path-A's external "main-track lift" is off the table on our data.
- **Recording:** `docs/references/literature-sweep-system.md` + far-future task + gbrain (the fetch-once conference corpus, Erfan-owned).

## What's next (Erfan's call — handed back)
- **The expansion program's experimental phase is closed with negatives.** No top-10 main-track positive materialized; the honest deliverable is the Path-A negative-results/methodology paper (now extendable to behavioral RT via E021, mechanism pinned) + the thesis.
- **Analysis-lane floor (R08–R14 + extended manuscript) is the thesis priority** — untouched, Erfan's lane (D011).
- If Erfan wants: a learnability+shape-matched replication of E021 on a different LM/probe to make the negative airtight (cheap), or fold the narrow negative into Path A.

## Blockers / open loops
- **Two external thinking-panel agents** (counter-argument + first-principles on E021 v4) were still running at close — CONFIRMATORY of the clean-null (the A agent's internal panel + v5 already settled it). If they dissent on the shape-vs-cognition call, next session addresses it.
- A stray small GPT-2 process (A agent's redundant extra run) was finishing on GPU 2 — harmless; couldn't kill (different PID namespace).
- Tree clean except the pre-existing untracked `untitled.md` + `docs/manuscript/supervisor-email_2026-06.md` + `.claude/worktrees/`.

## Key facts
- **E021 trustworthy harnesses:** `scripts/run_e021_v{3,4,5}.py` + `e021_targets_v{3,4,5}.py`; results `outputs/e021/arms_v{4,5}_results.json`, `v4_within_seed_learnability.json` (gitignored). v2 is bug-tainted — use v4/v5. **Reusable rigor pattern:** for aux-target experiments, control with a **phase-randomized shape-matched twin** (matches autocorr + marginal, zero content) — distributional/temporal shape regularizes independent of content.
- **E022/Moussa:** `scripts/e022_pilot.py` (self-contained; TIMIT acquired from `kylelovesllms/timit_asr` HF mirror); `scripts/run_moussa_arms.py` (3-arm harness, NOT run — oracle HOLD). Both arms must start from the SAME init.
- **Stat lesson:** an experiment agent's auto-verdict can be statistically wrong — a *pooled* regression over seeds washes out a real effect that a *within-seed paired* test finds. Re-derive load-bearing contrasts yourself.
- **Conference-scout:** `scripts/litsweep/` (built, tested, not run at scale); spec in `docs/references/literature-sweep-system.md`.
- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`. 4× L40S. **Subagent routing (D026):** opus=think/design; sonnet=doc-nav/engineering; haiku=mechanical. fable BANNED.
- **Git:** `main`, push only when asked. **No ladder rung changed this session.**
