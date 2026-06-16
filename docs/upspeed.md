# Upspeed — read first, write last

**Last updated:** 2026-06-16 (Session 18 — tooling/process. **Hardened the `scientific-writing` skill from the R06 clarity audit (L046, D037); built the swarm-wrap system (D038).** NO experiment ran, NO science rung changed; the analysis lane is still active. Next: R07 / the extended manuscript, in a fresh session.)

> **Canonical state lives in [`ladder.md`](ladder.md).** This is last-session prose. With no task, run `/orient`.

## What got understood / built this session

1. **The `scientific-writing` skill was hardened (D037, commit `0647188`).** A four-lens thinking panel (counter-argument + first-principles-grounder + socratic-thinker + premortem-analyst, opus) audited every clarity/accuracy rewrite Erfan drove on R06 against the skill. Diagnosis: **mostly skill design, not execution.** Fixes:
   - **Clarity Test** now has two halves: necessity (delete-able?) *and* sufficiency (parse-able on first read?); the "invest" verb means *unpack into one-hop steps*, not pack more in.
   - **Reader-comprehension floor** added: define-on-first-use (audience-graded by layer), one-clause rationale-or-`\gap` per non-obvious method choice, table for any ≥3-number comparison, formula-vs-prose decision rule.
   - **Path selection is now a user interview** (roadmap + cost of fast vs full loop), with a hard rule that manuscript / supervisor-facing work always takes the full loop and the **review pass is non-skippable** there.
   - **Consolidation guards** for the report→extended fold (notation-collision, document-wide glossary, rationale-survival); a **number-freshness** obligation (cite resolves *and* still matches the record); the biasing worked example **neutralized** (it taught the L045 "exactly the partial" error).
   - Upstream methodology non-negotiable (D037, commit `3e15ecd`): record the why of a design choice at choice-time.

2. **The swarm-wrap system was built and first-run-tested on this session (D038, commit `e19cc69`).** SessionStart hook (`wrap_session_snapshot.py`) snapshots the start SHA + transcript path per worktree; `wrap-auditor` read-only agent (5 scopes); `/wrap` is tier-scaled (trivial = inline, heavy = parallel auditors → single writer, atomic-per-scope commits). Declined a `git add` guard hook (D039 — fights the no-nag stance). **Wrap-auditor model routing:** sonnet by default; `ladder-integrity` → opus only when an experiment ran.

## What's next — analysis lane

**NEXT: the extended manuscript (front matter + Methods + Results-Q0) and/or R07**, in a **fresh session**, now written through the hardened skill. Erfan's plan: the extended manuscript Results spine can only reach the end of **Q0** (R06 is the only finding-report written); the front matter draws on R01–R04 + R06. R07 (Q1, source E003) is the next finding-report. Either is manuscript/supervisor-facing → **full loop mandatory** (no fast path). The skill will now interview for the path at the start.

## Blockers / open loops

- No blockers, no background jobs. Working tree clean except `untitled.md` (pre-existing scratch, intentionally untracked).
- **The SessionStart hook helps from the *next* session on** — it was added mid-session, so this session's `/wrap` used the documented fallback (diff from the session's first commit). `start.json` currently holds smoke-test data; the next session will populate it for real.
- **Open task:** build the `check_number_freshness.py` verifier (tasks.md, Infrastructure) — the skill now requires the freshness check manually until it exists.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. 4× L40S.
- **Codes (D036):** `Q`n = ladder rung (Q0→Q5, climb order); `E`/`D`/`L`/`A` = flat immutable artifact IDs. Legend + journey tree in `docs/map.md`; canonical status in `docs/ladder.md`.
- **Writing:** route all report/manuscript prose through the `scientific-writing` skill (D035/D036/D037). It now interviews for the path (fast vs full loop); manuscript/supervisor-facing = full loop, review pass mandatory.
- **Wrap:** `/wrap` scales — heavy sessions fan out `wrap-auditor` agents over the git changeset, then a single writer applies (D038).
- **Subagent routing (D026):** opus = think/analysis/design; sonnet = doc-nav (incl. wrap auditors); haiku = mechanical. fable BANNED.
- **Git:** `main`, push only when asked.
