# Upspeed — read first, write last

**Last updated:** 2026-06-19 (S27 — **/meta session: the operating model was rebuilt. NO science ran, NO number produced, NO rung flipped (Q0–Q5 stand exactly as S25/S26).** Replaced the working/analysis session split with **eight invokable interaction stances** (D044, supersedes D011) plus a LearnLM/Gemini-style `/teach` stance. **The science thread from S25 below is unchanged and still the live next step.**)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **How to operate now = [`operating-map.md`](operating-map.md)** (the 8 stances). **Forward science direction = [`expansion-program.md`](expansion-program.md) §8** (PI/sample-efficiency) + [`idea-tree.md`](idea-tree.md). With no task, run `/orient`.

## What this session did (S27 — /meta: rebuilt the operating model)
- **Stances replace working/analysis (D044).** Eight invokable stances — `/work` `/interpret` `/write` `/teach` `/scout` `/meta` `/plan` `/review` — one fat skill (`.claude/skills/stances/`, `SKILL.md` spine → 8 mode files + the learning-record format). You invoke a stance (explicit, or auto with the agent stating it) and switch freely; `/work` is explicit-only. Day-to-day picture: `operating-map.md`.
- **`/teach`** (headline): LearnLM five principles + the Gemini guided-learning loop, four sub-modes (guided/walkthrough/feynman/drill), a learning-record ledger at `docs/learning/` (evidence-gated, anchored to report+number, re-read on resume). Grounded in new canonical notes `learnlm-2024_*` + `bloom-1984_*`. **`/interpret`** = claim-manifest + panel + stat-auditor + SCR.
- **Honesty armed at write-time, not in-stance:** `.claude/hooks/honesty_writecheck.py` flags an unsourced result-like number on writes to **reports + manuscript** (the prose deliverables), regardless of stance (non-blocking). **Fired live this session** — first scoped to 5 paths, narrowed to 2 after the ladder false-positived 41× (L052).
- **Reports** keep verdict-first + caveats-in-claim, gain a plain-language lead; `/teach` renders simple-first. Canonical docs (`CLAUDE.md`, `03-methodology.md`, `orient`/`wrap`/`session-logger`) rewritten to stances. 6 atomic commits (`6760f46` → `b0a5da3`).

## What's next (Erfan's call — the live science thread, UNCHANGED from S25)
- **Test `/teach` live** on a real report (planned) — the only real proof of the guided loop.
- **Q4 (next science `/work` session):** pick the re-substrate (oracle default = eye-tracking-first on a higher-N gaze corpus: pooled ZuCo NR or GECO/Provo/Dundee) → **synthetic-PI MDE positive-control FIRST** → fix control-5 + per-word loader → re-gate E024 → build. Q2 stays ❌; Q3's full-FT door stays CLOSED (n=6 too small, D042/L051).

## Blockers / open loops
- **Honesty hook is live** (fired this session) and scoped to `docs/reports/` + `docs/manuscript/` (L052).
- **Pre-existing finding the new hook surfaces:** `R06:96` has a bare `+0.0280` with no cite — needs an `[E0nn]` or `\gap` (analysis-lane, Erfan's call).
- **Cleanup follow-up:** sweep the remaining "working/analysis" mentions in `CLAUDE.md`'s fleet/self-activation section, `goalsmith` ("working sessions only"), and agent descriptions (D044 maps them, but it is drift).
- **Firecrawl MCP `⏸ Pending approval`** (S26, carried) — approve on next `claude` start before `firecrawl_*` fires.
- **ZuCo 1.0 clone (carried from S25/S26)** — `data/zuco1` ~61G; bare `nohup`, no completion notify; verify with `du -sh data/zuco1` / `pgrep -f 'osf.*q3zws'`.
- Pre-existing untracked (not ours): `untitled.md`, `docs/manuscript/supervisor-email_2026-06.md`, `.claude/worktrees/`.

## Key facts
- **Operating model (new, S27):** invoke a stance, switch freely; honesty is hook-armed at write-time, independent of stance. Map: `operating-map.md`; mechanics: `.claude/skills/stances/`; decision D044.
- **`/wrap` gotcha (S27):** `.claude/state/wrap/start.json` can hold a mid-session re-fire SHA (it did this session: `07e344e`, one of the session's own commits) — sanity-check `start_sha` against the session's commits; fall back to the prior session's last commit if it is wrong.
- **Firecrawl (S26):** reach for the cheap path first (WebFetch/exa) — credits are billed per call.
- **Data on disk:** denizenslab n=6 (~35G), ZuCo 2.0 features (`data/zuco-benchmark/`), ZuCo 1.0 partial (61G).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
