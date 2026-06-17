# Upspeed — read first, write last

**Last updated:** 2026-06-17 (Session 20 — working, provenance-only. **Repaired E003's four record-provenance gaps + a 5th (epoch asymmetry); NO science, NO rung changed.** Prior: S19 (analysis, not formally wrapped) wrote R07. Next: analysis lane — R08 / extended manuscript.)

> **Canonical state lives in [`ladder.md`](ladder.md).** This is last-session prose. With no task, run `/orient`.

## What ran this session

**E003 record-provenance repair (working; provenance-only).** Run as a gather → counter-critique panel → plan → critique-plan → execute orchestration Erfan asked for. The decisive step: a gpt2 perplexity dry-run showed the "unsourced" reference ppls (74/105/169) recompute on the cached slice to 74.0/104.9/169.0 — they *were* on-slice measurements, just never written to the JSON. So recompute **confirms** rather than replaces, and nothing moved the fit/verdict.

Built two scripts + sidecars (gitignored, regenerable):
- `scripts/recompute_e003_reference_ppl.py` → `outputs/E003_perplexity.json` (reference-arm held-out ppls, run's own estimator).
- `scripts/reanalyze_e003_dissociation.py` → `outputs/E003_dissociation.json` (r=−0.88 fit/residuals/44%-fold reproduce; P-values reproduce ≈0.09 under a fold×seed bootstrap, flagged construction-sensitive; within-family r archived as a hedge with its wide CI + an E015 forward-pointer, not a result).

Repaired E003.md (dead pointer; untrained ppl → order-of-magnitude; "4.5× the teacher" → "≈6.4× the teacher (≈4.5× the gpt2 student)"; dissociation citations; epoch-asymmetry note; a Provenance-repair section) and L011 (multiplier + citation). **R07 byte-identical** — left to the analysis lane.

## What's next

**Analysis lane.** R07 (Q1) is written; E003's record is now clean. Next analysis steps: **R08** (Q2 — the lever is real but weak and ppl-confounded), or the **extended manuscript** (front matter from R01–R04 + Methods + Results Q0–Q1 from R06/R07), through the `scientific-writing` skill, full loop. Working lane has no queued decisive work.

## Blockers / open loops

- **R07 "matched budget" wording** needs a one-line analysis-lane edit (cold ran 2 epochs vs warm 1 → step count not matched). A complete paste-ready handoff was produced this session for the R07-writing session. Not edited here (D011 — working sessions don't touch R06–R14).
- No background jobs. Tree clean (pre-existing `untitled.md`, `docs/manuscript/supervisor-email_2026-06.md` left untracked).

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. 4× L40S.
- **E003 sidecars are gitignored** (like `E003_cold/warm.json`); the two scripts regenerate them deterministically from the cached held-out slice (`data/kd_corpus/wikitext103_sentences_heldout.txt`).
- **E003 estimator:** `eval_perplexity` is single-window, `max_length=64`, NO sliding-window stride — match it (import, don't reimplement) for any cross-arm ppl comparison.
- **Codes (D036):** `Q`n = ladder rung; `E`/`D`/`L`/`A` = flat artifact IDs. Map + status in `docs/map.md` / `docs/ladder.md`.
- **Writing:** route report/manuscript prose through the `scientific-writing` skill (D035/D036/D037); manuscript/supervisor-facing = full loop.
- **Subagent routing (D026):** opus = think/analysis/design; sonnet = doc-nav; haiku = mechanical. fable BANNED.
- **Git:** `main`, push only when asked.
