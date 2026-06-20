# Upspeed — read first, write last

**Last updated:** 2026-06-20 (S29 — **/meta: fixed the `/teach` surface contract (D045). NO science ran, NO number produced, NO rung flipped (Q0–Q5 stand exactly as S25/S27/S28).** The live science thread is unchanged and still the next step.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **How to operate = [`operating-map.md`](operating-map.md)** (the 8 stances). **Forward science = [`expansion-program.md`](expansion-program.md) §8** (Q4 PI/sample-efficiency). With no task, run `/orient`.

## What this session did (S29 — /meta: /teach surface-contract fix)
- **Found and fixed a `/teach` regression (D045).** The teach v2 build had inverted Erfan's explicit instruction: `modes/teach.md` said *"the live Q&A is in the terminal; update the lesson at end of round"*, so the R07 live test dumped raw `$$…$$` into the CLI — the exact failure the mode exists to prevent. The agent had **agreed to the right rule live** (teach v2 session msg 227→237) then encoded the opposite. Design bug, not execution bug (L053).
- **The fix:** rewrote the surface contract in `modes/teach.md` + `formats/lesson-format.md` to the **part-boundary loop** — write each part's explanation+math+diagrams into the rendered lesson file *first*, ask in the terminal, run the whole back-and-forth there, record the answer/diagnosis + author the next part at the boundary. Math never appears unrendered in the terminal. Template unit = "part". Grounded in Erfan's own `data/course-lecture-study` skill + the pedagogy (split-attention avoided: surfaces are sequential, not simultaneous). Commit `d9ec687`.
- **Cleanup + a second diagnosis.** Removed the old R07 stub; gitignored `docs/learning/lessons/*.html` (disposable renders). Traced the "weak entry-point paths" Erfan flagged to source: D045 touched only line 44; the entry-point instruction (lines 72–74) is byte-identical across runs → **model generation variance, not the change.** The real lever (the thin "Open" step) is left for an optional future `/meta`.

## What's next (Erfan's call — the live science thread, UNCHANGED from S25/S27)
- **Q4 (next science `/work` session):** pick the re-substrate (oracle default = eye-tracking-first on a higher-N gaze corpus) → **synthetic-PI MDE positive-control FIRST** → fix control-5 + per-word loader → re-gate E024 → build. Q2 stays ❌; Q3's full-FT door stays CLOSED (n=6 too small, D042/L051).
- **Or `/teach` live** on a real report — now with the surface contract fixed (D045); explanation+math render in the lesson file, only the dialogue is in the terminal.
- **Optional `/meta`:** strengthen the `/teach` "Open" step so entry-point selection is specified (partition the report / MECE), not left to model luck — the cause of the weak path set Erfan saw this session.

## Blockers / open loops
- **No `\gap` remains in the pedagogy set.** The one genuinely-unavailable number — Long & Aleven exact per-condition Ns — is not printed in the paper; correctly left `\gap`, not invented.
- **Pre-existing finding (unchanged):** `R06:96` has a bare `+0.0280` with no cite — needs `[E0nn]` or `\gap` (analysis-lane, Erfan's call).
- **Firecrawl MCP `⏸ Pending approval`** (carried S26/S27) — approve on next `claude` start before `firecrawl_*`.
- **ZuCo 1.0 clone (carried S25–S27)** — `data/zuco1` ~61G; bare `nohup`, no completion notify; verify with `du -sh data/zuco1` / `pgrep -f 'osf.*q3zws'`.
- Untracked: `docs/manuscript/supervisor-email_2026-06.md` + `.claude/worktrees/` (pre-existing, not ours); `docs/learning/lessons/2026-06-20-report-R07.md` (Erfan's active `/teach` test — leave it).

## Key facts
- **Subagent model routing (S28, corrected from the subagent logs):** an agent's `model:` frontmatter default applies when a spawn omits `model` — so fleet agents self-route correctly. Verified this session: both `wrap-auditor`s ran **sonnet** (their default), the `paper-digest`s ran **opus** — all correct (an earlier in-session claim that the auditors "inherited opus" was wrong). The genuine inherit-the-session-model (opus) hazard is only agents with **no** frontmatter default — generic `claude`/`general-purpose`/`Explore`/`Plan`/custom. Set `model:` explicitly for *those*; the named fleet agents are already safe.
- **Format scannable, never walls of text** (Erfan, S28): lead with the point, whitespace + short lines, or just do the work silently. Global Presentation rule.
- **`/wrap` gotcha (recurred S28):** `start.json` can hold a mid-session re-fire SHA (`source: "resume"`); sanity-check `start_sha` against the session's commits, fall back to the parent of the session's first commit.
- **Operating model (S27):** invoke a stance, switch freely; honesty hook-armed at write-time on `reports/`+`manuscript/` only. Map: `operating-map.md`; mechanics: `.claude/skills/stances/`.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
