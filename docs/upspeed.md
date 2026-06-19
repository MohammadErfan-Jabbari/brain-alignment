# Upspeed — read first, write last

**Last updated:** 2026-06-19 (S25 — working/critique+gates. **NO experiment ran, NO rung flipped (Q0–Q5 stand).** Ran the four-lens panel + the full pre-compute gate on Q2/Q3/Q4. **Q2 recomputed** (cached E004) → the "lever exists" CI is the L015-condemned 15-cell bootstrap; at the honest fold unit it includes 0 → **demoted 🟡→❌ "no demonstrated lever"** (Erfan-confirmed; undemonstrated, not proven-zero). **Q3's "one untested door" CLOSED — dataset too small** (denizenslab n=6 can't power the per-individual population claim) → hedge retired, verdict unchanged ❌ (D042, L051). **Q4 sample-efficiency/LUPI** designed (E024) → oracle **HOLD** (400-sentence substrate underpowered → re-substrate; parked for next session).)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **Forward direction = [`expansion-program.md`](expansion-program.md) §8** (PI/sample-efficiency) + [`idea-tree.md`](idea-tree.md). With no task, run `/orient`.

## What this session did (S25)
- **Critique panel (counter-argument · first-principles · premortem · socratic, opus) on Q2/Q3/Q4** → finalized each as analysis / experiment / theory-proof. **Key result: none of the three is closable by theoretical proof** — the two nulls (Q3, Q4) rest on the unproven premise $Y\perp\theta^\*\mid S$ (L041) the cited math can't discharge.
- **Q2 — DONE.** Recompute from `outputs/E004_brain_lever_Qwen.json`: flat-15-cell +0.00316 [+0.00062,+0.00584] (excl 0) = the recorded number; honest fold unit (n=5) +0.00316 t-CI **[−0.00227,+0.00858] includes 0**; fold-4 = 64%; `beats_permuted_null=False`. → **proposed demote Q2 🟡→null** (the only number licensing "lever exists" is the discredited bootstrap). Makes Q2 consistent with the Q3 null.
- **Q3 — CLOSED (Erfan-directed).** "One untested door" (full-FT denizenslab n=6) gated (anti-confound-designer + oracle = KILL build) → **NOT BUILT, decisively dataset-too-small** (n=6, σ unmeasured, ~n≈8 needed; deep subjects we'd need not on disk). Compounding: E017 already null + gate 0-for-5. Fork-1 cheap gate feasibility-confirmed but abandoned for the same reason. D042, L051, E013 S25 verdict.
- **Q4 — designed + gated to HOLD.** E024 (ZuCo LUPI sample-efficiency) written + battery assembled + oracle HOLD: 400-sentence SR-sentiment substrate underpowered, loader is wrong-task + no per-word timeseries, control-5 unfair. Redesign in E024.
- **Forks (Erfan):** Fork 1=(a) then killed-for-size; Fork 2 = **on-roadmap** (eye-tracking-first + GECO/Provo are already in §8/idea-tree T1.3; synthetic-PI MDE positive-control is the L048 rigor step).

## What's next (Erfan's call)
- **Q2 demoted 🟡→❌ "no demonstrated lever"** (Erfan-confirmed S25; undemonstrated, not proven-zero — n=5 underpowered to rule out a small lever). Done; the next-session focus is Q4.
- **Q4 (next session):** pick the re-substrate (oracle default = eye-tracking-first on a higher-N gaze corpus: pooled ZuCo NR or GECO/Provo/Dundee) → **synthetic-PI MDE positive-control FIRST** (confirm detectability) → fix control-5 (measure biosignal reliability; add valence-lexicon teacher) → decide per-word loader → re-gate E024 → build. Each gated build = its own fresh session.

## Blockers / open loops
- **ZuCo 1.0 clone STILL RUNNING in background** (`data/zuco1`, ~61G, OSF q3zws, launched via bare `nohup` — **will NOT notify on completion**; check with `pgrep -f 'osf -p q3zws'` / `du -sh data/zuco1`). Pulled task3-TSR first (alphabetical); NR/SR arrive later. Useful for any Q4 substrate.
- (resolved) Q2 demoted to ❌ "no demonstrated lever" (Erfan-confirmed S25).
- Pre-existing untracked (not ours): `untitled.md`, `docs/manuscript/supervisor-email_2026-06.md`, `.claude/worktrees/`.

## Key facts
- **Data on disk:** denizenslab n=6 (responses + TextGrids + mapper + NC, ~35G) — git-annex IS installed (ladder's "not installed" was stale); ZuCo 2.0 features (`data/zuco-benchmark/src/features/`, 624 npy, NR/TSR task); ZuCo 1.0 partial (cloning).
- **Tooling lessons:** `osf clone` once exited 0 with an empty dir (transient OSF glitch — re-run + verify files land); bare `nohup &` background jobs don't re-invoke the agent on completion (use the Bash `run_in_background` tool if you need a notification).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
