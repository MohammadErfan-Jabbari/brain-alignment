---
title: "S45 — /write R07 rebuild (sci-write-v2 skill-eval) + /meta two-mode restore (D053)"
tags: [timeline]
---

# S45 — 2026-06-29 — /write (R07 rebuild) + /meta (sci-write-v2 two-mode restore)

**Stances:** `/write` (R07 finding-report rebuilt from scratch through the `sci-write-v2` pipeline, as a skill-eval) + `/meta` (restored the audience-by-layer rule into `sci-write-v2`). **No experiment, no science number, no rung change — Q0–Q5 stand exactly as S25.**

## What ran
- **Worktree.** Set up an isolated git worktree (`worktree-r07-write`, via `EnterWorktree`) so a parallel Q4 `/work` session could use the main checkout without git contention. Merged to main at close.
- **`/write` — R07 rebuild.** Re-derived R07 (Q1, "plain perplexity-only KD does not preserve alignment") from the frozen evidence ([E003](../experiments/E003_kd-alignment-preservation.md)) through the full `sci-write-v2` gated loop: Stage 0 evidence → Stage 1 message/reader/register → Stage 2 claim+argument lattice (6 claims, 5 warrants, F18 acks) → Stage 3 skeleton + figure plan → **F16 gate (Erfan-approved via `AskUserQuestion`)** → Stage 4 draft (`sw-drafter` → `sw-voice-realize`) → Stage 5/6 audit-revise. An opus `oracle-reviewer` ran at **every stage** (the three-net pattern) on top of the pipeline's intrinsic judges. **Converged after 4 revise rounds** (~40 opus reader-passes; all 7 stage-5 readers ready, F13 panel bare SURVIVES, draft hash `aed2b50a`). Rendered to [`reports/R07_sci-write-v2-rebuild.md`](../reports/R07_sci-write-v2-rebuild.md) (LaTeX math, frontmatter, Related footer; a NOTE marks it a comparison artifact, **not** wired into the reports ordering).
  - **The audit's real catch:** the first draft's headline over-claimed ("the *objective* sheds alignment"); the F13 panel pulled it back (SURVIVES-IF-NARROWED) to E003's recorded PARTIAL verdict — achievable entirely **within recorded evidence**, so `writing-revise`, not a `/work` handoff (the M3 backstop correctly did not fire).
- **Comparison analysis.** An opus academic-writing analysis of both R07s (ours: readability / intention / message-transfer / vocabulary / designed-AI-triggers; no ranking). Erfan ran a second, context-free opus on a top-venue rubric. Both converged: **baseline = internal-report register** (project-embedded, codes in prose), **rebuild = public/manuscript register** (standalone, codes stripped); both bound claims correctly.
- **`/meta` — D053.** Erfan identified that the rebuild's external register was caused by the reader-model audience being set to an external reviewer — because the **D048 cutover silently dropped** the archived skill's "internal codes descend by layer" rule (it was guidance, not a DET check, so nothing carried it over). Restored surgically: `meta.layer` ∈ {`report`|`extended`|`public`} set at Stage 1, drives the reader-model OLD/NEW split + gloss; `sw-reader-model` honors it. 3 files, ~25 lines, **zero script-logic change**, default `report` (backward-compatible — all selftests + the example lattice pass). **D053**; lesson **L069**.
  - **Render caution (L069):** the LaTeX render re-introduced 21 em-dashes (the pipeline draft used `" - "`, 0 em-dashes; budget is 0) — caught and fixed; an earlier lint check had missed it via `tail`-truncation.

## State at close
- Worktree committed and merged to `main` (this wrap).
- Erfan will run the **report-mode validation** (re-run R07 with `meta.layer: report`) in a new session.

## Next
- **Validate D053 end-to-end (Erfan, new session):** re-run the R07 rebuild with `meta.layer: report` → expect report-register prose (Q1/R06/E003 used in prose, closer to the baseline).
- **Live science thread UNCHANGED since S25:** `/work` Q4 sample-efficiency E024, OR `/write` R08 (Q2), OR `/interpret` the parked E006 voxelwise-CI item.

## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`decisions/decisions.md`](../decisions/decisions.md) — D053
- [`reports/R07_sci-write-v2-rebuild.md`](../reports/R07_sci-write-v2-rebuild.md) — the comparison rebuild
- [`learnings.md`](../learnings.md) — L069
