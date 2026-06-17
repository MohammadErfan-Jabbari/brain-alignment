# Upspeed — read first, write last

**Last updated:** 2026-06-17 (Session 22 — autonomous working. Ran the expansion program + the **E021 keystone** end-to-end. **Verdict: INCONCLUSIVE at n=3 — surprisal-orthogonality is cleanly NULL (raw≈residual), generic regularization dominates, the broader cognition question is underpowered, and the v2 "positive" was a harness-bug artifact.** The main-track positive did NOT materialize. No rung flipped. Handed the next decision to Erfan.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (unchanged this session — Q0–Q5 stand). New program state: [`expansion-program.md`](expansion-program.md) + [`idea-tree.md`](idea-tree.md). With no task, run `/orient`.

## What ran (S22)
Erfan set an autonomous `/goal`: expand the idea set toward a top-venue result. The session built the program scaffolding, a working **conference-scout** lit-sweep tool (`scripts/litsweep/`), ran a **strategy premortem** that honestly re-sequenced the plan (kill the structural-null nodes, promote **T1.3 = non-fMRI cognitive signal** as the only mechanically-viable main-track bet), and ran the keystone experiment **E021** end-to-end through a full gating chain (G0/G1 → G2 → 5 arms → panels + Codex → clean v3 rerun). It also made the **Path-A Moussa/TA.4** external demonstration launch-ready (`scripts/run_moussa_arms.py`, dry-run only).

## The keystone result (E021, clean v3 — the trustworthy numbers)
- **Surprisal-orthogonality = NULL (clean):** raw ≈ residual (+4.3 [−3.9,+12.6]). The specific novelty buys nothing.
- **Generic regularization dominates:** baseline 628 → structured ~177–250 AULC (~450 gap; E004 `frozen` at scale).
- **Cognition question = underpowered/inconclusive:** residual best on the mean but CIs touch 0 (n=3); the log-freq exclusion control is confounded by learnability.
- The v2 "triple-dissociation positive" was a **bug artifact** (Codex caught a pad-label bug; the clean rerun flipped the verdict twice). Lessons → **L048**.

## What's next (Erfan's call — autonomous mode paused, cost ~$212)
1. **Resolve E021 cleanly** (more seeds + a *learnability-matched* non-cognitive control) — OR **fold the narrow negative into Path A** and stop chasing the main-track positive. The honest read: the >75%-top-10-main-track goal was not reached and is unlikely on this evidence without new data/regime.
2. **Path-A floor is ready to run** (`run_moussa_arms.py`) — the external matched-perplexity demonstration for the negative-results paper, if wanted.
3. **Analysis lane (R08–R14 + extended manuscript) remains the thesis floor** — untouched (Erfan's lane, D011).

## Key facts
- **E021 trustworthy harness:** `scripts/run_e021_v3.py` + `e021_targets_v3.py`; results `outputs/e021/arms_v3_results.json` (gitignored). v2 is bug-tainted — use v3.
- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`. 4× L40S.
- **Conference-scout:** `scripts/litsweep/` (DBLP/OpenReview/OpenAlex/arXiv); full-sweep commands in its README. Not run at scale (the lit-scouts grounded each node directly).
- **Subagent routing (D026):** opus = think/analysis/design; sonnet = doc-nav/engineering; haiku = mechanical. fable BANNED.
- **Git:** `main`, push only when asked. ~13 commits this session.
- **No ladder rung changed.** E021 is a new exploratory experiment, not a rung flip.
