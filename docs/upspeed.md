# Upspeed — read first, write last

**Last updated:** 2026-06-19 (S26 — **tooling interlude. NO science ran, NO number produced, NO rung flipped (Q0–Q5 stand exactly as S25 left them).** Set up Firecrawl for the repo: cloud MCP (self-host impossible — no Docker) wired in `.mcp.json`, `firecrawl-research-index` skill installed repo-local, capabilities documented in `CLAUDE.md`. **The science plan from S25 below is unchanged and still the live thread.**)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **Forward direction = [`expansion-program.md`](expansion-program.md) §8** (PI/sample-efficiency) + [`idea-tree.md`](idea-tree.md). With no task, run `/orient`.

## What this session did (S26 — tooling)
- **Firecrawl set up for the repo** (`71c0894`, `c868446`). Cloud API only — Docker isn't usable here, so the self-hosted stack is off the table; `FIRECRAWL_API_KEY` was already in secrets and live-tests pass (credits *are* billed). Project-scoped MCP server in `.mcp.json` (remote transport, key interpolated, no secret committed); `firecrawl-research-index` skill installed repo-local (`.claude/skills/`, drives `firecrawl_research_*`, complements `lit-scout`); `## Firecrawl` section added to `CLAUDE.md`. The 5 `firecrawl-build-*` skills were skipped (build-an-app-on-Firecrawl, irrelevant); estack untouched (Erfan-directed). Recorded as **D043** (partially resolves D041's deferred `.mcp.json`; does not shadow Exa).
- **Open loop:** the Firecrawl MCP server is `⏸ Pending approval` — approve on next `claude` start before `firecrawl_*` tools are callable.

## What's next (Erfan's call — UNCHANGED from S25, the live science thread)
- **Q2 is demoted 🟡→❌ "no demonstrated lever"** (Erfan-confirmed S25; undemonstrated, not proven-zero — n=5 underpowered to rule out a small lever). The next-session focus is **Q4**.
- **Q4 (next science working session):** pick the re-substrate (oracle default = eye-tracking-first on a higher-N gaze corpus: pooled ZuCo NR or GECO/Provo/Dundee) → **synthetic-PI MDE positive-control FIRST** (confirm detectability) → fix control-5 (measure biosignal reliability; add valence-lexicon teacher) → decide per-word loader → re-gate E024 → build. Each gated build = its own fresh session.

## Blockers / open loops
- **Firecrawl MCP `⏸ Pending approval`** (S26) — one-time project-server approval needed on next `claude` start; until then `firecrawl_*` tools won't fire.
- **ZuCo 1.0 clone (carried from S25)** — `data/zuco1` is **61G** on disk (unchanged size vs S25; process status unconfirmed this session — bare `nohup`, **will NOT notify on completion**; check with `pgrep -f 'osf.*q3zws'` / `du -sh data/zuco1`). Pulled task3-TSR first (alphabetical); NR/SR arrive later. Useful for any Q4 substrate.
- Pre-existing untracked (not ours): `untitled.md`, `docs/manuscript/supervisor-email_2026-06.md`, `.claude/worktrees/`.

## Key facts
- **Firecrawl (new, S26):** cloud MCP via `.mcp.json` (`firecrawl_scrape/map/crawl/extract/search`, research index `firecrawl_research_*`, agent/interact/monitors). **Reach for the cheap path first** (WebFetch/exa) — Firecrawl credits are billed per call; use it for JS-heavy/anti-bot pages, whole-site crawl/map, schema'd extraction, or the research index. Full index: `https://docs.firecrawl.dev/llms.txt`.
- **Data on disk:** denizenslab n=6 (responses + TextGrids + mapper + NC, ~35G) — git-annex IS installed; ZuCo 2.0 features (`data/zuco-benchmark/src/features/`, 624 npy, NR/TSR task); ZuCo 1.0 partial (61G, cloning/cloned).
- **Tooling lessons:** `osf clone` once exited 0 with an empty dir (transient OSF glitch — re-run + verify files land); bare `nohup &` background jobs don't re-invoke the agent on completion (use the Bash `run_in_background` tool if you need a notification).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
