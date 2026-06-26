---
title: "2026-06-19 10:56 — Firecrawl setup (S26, tooling)"
tags: [timeline]
---

# 2026-06-19 10:56 — Firecrawl setup (S26, tooling)

**Session mode:** Tooling / infrastructure. **No science ran, no number produced, no ladder rung moved (Q0–Q5 stand exactly as S25 left them).** A short interlude between S25 (Q2 demotion + Q3/Q4 gates) and the next science working session (Q4 re-substrate).

## What this session did

Set up Firecrawl (https://github.com/firecrawl/firecrawl) for the repo and documented its capabilities in `CLAUDE.md` so the agent is always aware of them.

**Environment facts that shaped the choice (verified live):**
- **Docker is not usable in this container** → the self-hosted Firecrawl stack (Redis + Playwright via `docker compose`) cannot run here. Cloud API only.
- `FIRECRAWL_API_KEY` was already present in `~/.config/secrets/env`; live-tested against `api.firecrawl.dev/v2/scrape` (HTTP 200, `creditsUsed:1` — credits are billed) and the remote MCP endpoint `mcp.firecrawl.dev/<key>/v2/mcp` (`firecrawl-fastmcp v3.0.0`, full tool list returned).
- Node v22 / `npx` available; `firecrawl-mcp@3.20.6` current.

**Landed (2 commits):**
- `71c0894` — `feat(tooling)`: Firecrawl as a **project-scoped MCP server** in `.mcp.json` at repo root, **remote transport** with `${FIRECRAWL_API_KEY}` interpolated (no secret committed). New `## Firecrawl` section in `CLAUDE.md` documenting the `firecrawl_*` tool surface (scrape/map/crawl/extract/search, the **research index**, agent/interact/monitors), the authority order (docs brain wins; never a science number, never a rung flip — same hard line as Codex/graphify), the cost discipline (cheap path WebFetch/exa first; credits billed), and add-ons.
- `c868446` — `feat(skills)`: installed the **`firecrawl-research-index`** skill **repo-local** at `.claude/skills/firecrawl-research-index/SKILL.md` (a real file, matching how `graphify`/`scientific-writing` are tracked here). It drives the `firecrawl_research_*` tools (semantic paper search → citation-graph expansion → in-body verify) and complements `lit-scout`. `CLAUDE.md` updated to reflect it's installed.

**Decisions in the work:**
- **Self-hosted: skipped** (no Docker). Cloud API instead.
- **The 5 `firecrawl-build-*` skills: skipped** — they onboard a developer to *build apps on* Firecrawl; irrelevant to a thesis, and their triggers ("use even if the user does not mention Firecrawl") would mis-fire on normal web tasks.
- **`firecrawl-research-index`: installed** (Erfan chose "research-index only" via a decision prompt). Accepts mild trigger overlap with `lit-scout`.
- **estack: not touched** (Erfan-directed mid-session). I had begun vendoring the skill into `~/.estack/skills/` for consistency with the 13 firecrawl skills already in the estack library; on Erfan's "don't get involved on the estack, just add the necessary firecrawl skills in this repo," I removed it and confirmed estack returned to clean, then installed repo-local instead.

This **partially resolves D041's deferred `.mcp.json` item** — the repo now has its first `.mcp.json`, scoped to Firecrawl only, which does **not** shadow the global Exa server (separate server name). The Exa transport-config question D041 flagged remains open and untouched. → recorded as **D043**.

## Open loop for next session

- **The Firecrawl MCP server is `⏸ Pending approval`** (project-scoped servers need a one-time in-session approval). It activates on the next `claude` start (or first `firecrawl_*` call). Until then the `firecrawl_*` tools are not callable.

## Continuity audit (Part B)

- **Friction:** none recurring. The estack-vs-repo install path was a one-time clarification (now settled: repo-local for project-specific external skills, matching graphify/scientific-writing).
- **Tooling that misbehaved:** none. (Note: the codex companion shell wrapper garbles `pgrep` output in compound commands — cosmetic; `du` was clean.)
- **Doc consistency:** `CLAUDE.md` corrected mid-session (the "research skill not auto-installed" line was made true once it was installed). No number-provenance issue — zero numbers produced. Ladder untouched and still accurate.
- **New artifact:** none warranted beyond what landed.
- **Ladder integrity:** unchanged; Q0–Q5 and the S25 "Next session = Q4 re-substrate" block stand.
- **Brain mirror:** deliberately **not** mirrored to gbrain — this is repo-recorded tooling plumbing (CLAUDE.md + .mcp.json + D043 + this log) with no cross-project knowledge signal that another session/project would need from the brain.
- **Git:** both commits atomic, conventional, scoped-staged. Working tree carries only the pre-existing non-ours untracked files (`untitled.md`, [`docs/manuscript/supervisor-email_2026-06.md`](../manuscript/supervisor-email_2026-06.md), `.claude/worktrees/`). Nothing pushed.
- **Background job (carried from S25):** ZuCo 1.0 clone — `data/zuco1` still **61G** on disk; process status unconfirmed this session. Blocker preserved in [`upspeed.md`](../upspeed.md).

## Tier note

`/wrap` nominally flags this **heavy** (`.claude/skills/` was touched), but the substance is tooling with no science, no ladder rung, no numbers, no manuscript, and full orchestrator context — so it was closed **inline** (Part A + B), no audit swarm. `start.json` was present (no fallback needed).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
