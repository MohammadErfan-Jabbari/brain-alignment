# Upspeed — read first, write last

**Last updated:** 2026-06-22 (S31 — **/write: extended manuscript v0.2 (checkpoint 2) — folded R07 (Q1) + repaired the v0.1 register. NO experiment ran, NO science number produced, NO rung flipped (Q0–Q5 stand exactly as S25/S27).** Also catches up the unwrapped S30 (the D046 prose-ship-gate). The live science thread is unchanged and still the next step.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **How to operate = [`operating-map.md`](operating-map.md)** (the 8 stances). **Forward science = [`expansion-program.md`](expansion-program.md) §8** (Q4 PI/sample-efficiency). With no task, run `/orient`.

## What the last two sessions did
- **S31 (/write) — extended manuscript v0.2 (checkpoint 2).** Folded **R07 (Q1)** into the extended manuscript: plain perplexity-only KD does not preserve alignment by default (the 7-arm retention table, the monotone gradient, `r=−0.88` quality co-variation held as the reason the objective-specific shedding claim stays unsupported). Abstract + intro state Q1 with that hedge; downstream gaps narrowed R07–R14 → **R08–R14**. **Repaired the v0.1 register** (L054/D046) across the whole body — the storytelling tells the supervisor flagged. Verified: `run_checks` PASS, claim panel clean, `prose-register-auditor` ×2. **R07 was the only report-layer finding not yet consolidated**; R08–R14 don't exist yet, so Discussion/Limitations/Conclusion stay `\gap`. Commits `7fa629b`, `5e4f561` (+ wrap precision fix).
- **S30 (/meta, was unwrapped) — the prose ship-gate (D046).** Built the gate that stops un-reviewed storytelling prose reaching a human: register rules in the `scientific-writing` skill, the linter tripwire/meter, the `prose-register-auditor` agent, the always-on `prose_writecheck.py` hook. Recorded D046 + L054. Reconstructed timeline written at the S31 wrap.

## What's next (Erfan's call)
- **Next `/write`:** **R08 (Q2)** finding-report (the lever is real but weak and ppl-confounded), then fold it at manuscript **checkpoint 3**. Reading order in `reports/README.md`.
- **Live science thread (unchanged from S25):** Q4 sample-efficiency E024 — pick the re-substrate (oracle default: eye-tracking-first higher-N gaze corpus) → synthetic-PI MDE positive-control FIRST → fix control-5 + per-word loader → re-gate → build. Q2 stays ❌; Q3's full-FT door stays CLOSED (n=6 too small, D042/L051).

## Blockers / open loops
- **Pre-existing finding (unchanged):** `R06:96` has a bare `+0.0280` with no cite — needs `[E0nn]` or `\gap` (analysis-lane, Erfan's call).
- **Firecrawl MCP `⏸ Pending approval`** (carried S26–S27) — approve on next `claude` start before `firecrawl_*`.
- **ZuCo 1.0 clone (carried S25–S27)** — `data/zuco1` ~61G; bare `nohup`, no completion notify; verify with `du -sh data/zuco1` / `pgrep -f 'osf.*q3zws'`.
- Untracked (pre-existing, not ours): `docs/manuscript/supervisor-email_2026-06.md`, `.claude/worktrees/`, `docs/learning/lessons/2026-06-20-report-R07.md` (Erfan's `/teach` test — leave it).

## Key facts
- **LaTeX builds (S31, NEW).** No system TeX engine here (the installed "LaTeX" is the VS Code extension → compiles via Docker, which this container can't run). Build the extended manuscript with **tectonic** (`~/.local/bin`): `cd docs/manuscript/extended && tectonic -X compile main-extended.tex --keep-intermediates`. **Version trap:** tectonic 0.16.9 bundles biblatex 3.17, which needs **biber 2.17** — apt's biber 2.19 is INCOMPATIBLE (control-file mismatch). A standalone biber 2.17 is installed in `~/.local/bin` and shadows apt's. `.bbl` + `.pdf` are committed on purpose (latex-conventions.md). **Never put bare `^`/`_` in a printed bib field** (note/title) — it fails `\printbibliography` with "Missing $ inserted" (was a latent bug in `references.bib`). See L055.
- **Manuscript ship-gate (D046):** a manuscript build/revision is its own logged `/write` session with the non-skippable review pass (spawns `prose-register-auditor`); a clean deterministic linter run is NOT a clearance.
- **Subagent model routing (S28):** an agent's `model:` frontmatter default applies when a spawn omits `model`; only set `model:` explicitly for agents with NO default (generic `claude`/`general-purpose`/`Explore`/`Plan`/custom).
- **Format scannable, never walls of text** (Erfan, S28): lead with the point, whitespace + short lines, or just do the work silently.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
