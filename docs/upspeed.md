# Upspeed — read first, write last

**Last updated:** 2026-06-20 (S28 — **/meta: the 4 supplied `/teach`-pedagogy `\gap` papers were ingested into canonical notes. NO science ran, NO number produced, NO rung flipped (Q0–Q5 stand exactly as S25/S27).** The live science thread is unchanged and still the next step.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **How to operate = [`operating-map.md`](operating-map.md)** (the 8 stances). **Forward science = [`expansion-program.md`](expansion-program.md) §8** (Q4 PI/sample-efficiency). With no task, run `/orient`.

## What this session did (S28 — /meta: pedagogy literature grounding completed)
- **Ingested the 4 PDFs Erfan supplied** (the ones S27 could not download), in two batches. All read first-hand; the 6 source PDFs are in `data/papers/` (gitignored). 5 atomic `docs(scout):` commits (`64cbfe6` → `126301d`).
- **Two `\gap`s closed** (Moser 2011, B&M 2001) + **3 new canonical notes** (B&M 2006 mechanism, Bodily 2018 OLM/LAD review, Long & Aleven 2017 OLM RCT). All are external pedagogy literature grounding the `/teach` apparatus — **cite-or-flag, NOT thesis science** (no A1/A2/A3, no rung).
- **Two corrections to repo's carried-over numbers:** Long & Aleven is **N=301, not 302** (abstract off-by-one); the OLM benefit is the larger **Exp 2's OLM×PS interaction** (F(1,236)=7.535, p=.007), not an unconditional main effect (Exp 1, N=56, found a plain main effect d=.56). B&M 2001's own gamma (+.36, N=19) differs from the 2006 paper's .06/.39/.89 gradient (that's a 2001 *poster*'s) — separation was right.

## What's next (Erfan's call — the live science thread, UNCHANGED from S25/S27)
- **Q4 (next science `/work` session):** pick the re-substrate (oracle default = eye-tracking-first on a higher-N gaze corpus) → **synthetic-PI MDE positive-control FIRST** → fix control-5 + per-word loader → re-gate E024 → build. Q2 stays ❌; Q3's full-FT door stays CLOSED (n=6 too small, D042/L051).
- **Or `/teach` live** on a real report — the S27 follow-up, now with the pedagogy notes fully grounded.

## Blockers / open loops
- **No `\gap` remains in the pedagogy set.** The one genuinely-unavailable number — Long & Aleven exact per-condition Ns — is not printed in the paper; correctly left `\gap`, not invented.
- **Pre-existing finding (unchanged):** `R06:96` has a bare `+0.0280` with no cite — needs `[E0nn]` or `\gap` (analysis-lane, Erfan's call).
- **Firecrawl MCP `⏸ Pending approval`** (carried S26/S27) — approve on next `claude` start before `firecrawl_*`.
- **ZuCo 1.0 clone (carried S25–S27)** — `data/zuco1` ~61G; bare `nohup`, no completion notify; verify with `du -sh data/zuco1` / `pgrep -f 'osf.*q3zws'`.
- Pre-existing untracked (not ours): `docs/manuscript/supervisor-email_2026-06.md`, `.claude/worktrees/`.

## Key facts
- **Always pass an explicit `model:` on subagent spawns** (S28 lapse): the wrap auditors omitted it and inherited the session model (opus) instead of the routed **sonnet**. For `wrap-auditor` / scoped doc-nav fan-out → sonnet (haiku for purely mechanical). Don't rely on inheritance.
- **Format scannable, never walls of text** (Erfan, S28): lead with the point, whitespace + short lines, or just do the work silently. Global Presentation rule.
- **`/wrap` gotcha (recurred S28):** `start.json` can hold a mid-session re-fire SHA (`source: "resume"`); sanity-check `start_sha` against the session's commits, fall back to the parent of the session's first commit.
- **Operating model (S27):** invoke a stance, switch freely; honesty hook-armed at write-time on `reports/`+`manuscript/` only. Map: `operating-map.md`; mechanics: `.claude/skills/stances/`.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
