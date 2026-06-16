# S18 — scientific-writing skill hardening + the swarm-wrap system

**Date:** 2026-06-16 · **Session:** 18 · **Branch:** main

## Purpose

Before starting the extended manuscript, learn from R06's clarity rework: diagnose whether the
clarity/accuracy misses traced to the `scientific-writing` skill's design or to agent execution, harden
the skill accordingly, and build a session-close audit system so the docs brain cannot silently drift.

## Session mode

**Tooling / process** — no science evidence was produced or consumed, no rung touched. (Framed like a
working session for "what was built / next," but on the meta layer.)

## What happened

1. **Oriented** (analysis session intended). Confirmed the finding-report set R06→R14; only R06 is written.
   Challenged the premise of jumping to the extended manuscript: its Results spine can reach only the end
   of **Q0** (R06), while the front matter draws on R01–R04. Erfan agreed and first asked for a clarity
   audit of the R06 rework.

2. **R06 clarity audit (4-lens thinking panel, opus, parallel).** Extracted every R06 rewrite Erfan drove
   from the session transcripts (jq over the `.jsonl`), grouped into six failure categories, and handed
   them + the skill to counter-argument + first-principles-grounder + socratic-thinker + premortem-analyst.
   **Verdict: mostly skill DESIGN, not execution.** Two sharp findings: the skill's own worked example
   *taught* the L045 "unique R² is exactly the partial" error; and the report fast-path's review-skip let
   over-claims reach a reader. The socratic lens correctly pushed back that some rewrites are the report
   loop working as designed — incorporated by making fixes audience-graded and manuscript-scale-targeted.

3. **Hardened the skill (D037).** Amended the Clarity Test (necessity + sufficiency; invest = unpack);
   added the reader-comprehension floor; made path selection a user interview with a hard manuscript =
   full-loop boundary; review pass non-skippable for manuscript-bound work; report→extended consolidation
   guards; number-freshness obligation; neutralized the biasing example. Added an upstream methodology
   non-negotiable (record the why of a design choice at choice-time). L046.

4. **Built the swarm-wrap system (D038).** SessionStart hook snapshots `{start_sha, transcript_path}` per
   worktree; `wrap-auditor` read-only agent (5 scopes); `/wrap` tier-scaled (trivial inline; heavy fans out
   auditors → single writer → atomic-per-scope commits). Declined a `git add` guard hook (D039). Decided
   auditor model routing: sonnet by default, `ladder-integrity` → opus only when an experiment ran (the
   opus orchestrator is the reasoning backstop, so the fan-out stays cheap — answers Erfan's routing Q).

5. **First-run-tested the swarm-wrap on this very session.** Five auditors ran in parallel over the
   `4a311d0..HEAD` changeset (fallback path, since the hook post-dated session start). Findings verified;
   applied the founded ones (D037–D039 records, S18 stamps on ladder/upspeed/tasks, a `wrap-auditor` row in
   CLAUDE.md, a CC_norm cite fix and a real semipartial/partial terminology fix in the skill, the
   number-freshness task); dropped three as unfounded (hardcoding the hook path would break worktree
   portability; the "+0.021" teaching examples are fine; pre-existing script-path prose).

## Decisions made

- **D037** — harden the `scientific-writing` skill from the R06 clarity audit.
- **D038** — build the scaled swarm-wrap system.
- **D039** — no `git add` guard hook (fits the no-nag stance).

## Current truth

The skill is hardened and the swarm-wrap is live and tested. No science changed; the ladder is unchanged
from S17 (Q0 ✅ powered; Q1 ✅ partial; Q2 🟡; Q3 ❌ null; Q4 ❌ bounded null; Q5 ⬜). The analysis lane's
next step (extended manuscript front matter + Methods + Results-Q0, and/or R07) is unchanged — now to be
written through the improved skill.

## Next session

**Analysis, fresh session:** start the extended manuscript (front matter from R01–R04 + R06; Methods +
Results §1 = Q0 from R06; scaffold beyond Q0) and/or write R07 (Q1, source E003). Manuscript/supervisor-
facing → full loop mandatory; the skill will interview for the path. If parallel R07 work runs, use a
separate git worktree.

## Friction & improvements

- **The SessionStart hook post-dated this session**, so `/wrap` used the fallback changeset — expected
  once, fine going forward.
- **Cost ran high** ($75+): two large opus fan-outs (the 4-lens audit, then the 5-auditor swarm) in one
  session. The new sonnet-default routing for wrap auditors will cut future wrap cost; the audit fan-out
  was a one-off design exercise.
- **New task filed:** `check_number_freshness.py` (the one mechanical check the freshness rule needs).
