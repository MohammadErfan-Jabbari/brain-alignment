# S33 — 2026-06-22 15:41 — /write: extended-manuscript abstract clean + em-dash guardrail fix

**Stances:** `/write` (dominant — abstract rewrite via the `scientific-writing` skill), with a `/meta` sliver (linter guardrail fix). Opened with `/orient`.

**Numbering note:** this session is **S33**. The prior session (S32, the D047 convergence-gate work, committed `bf78142`/`589ce88`/`8115fff`) was never wrapped — no timeline, ladder left at S31 — and is reconciled in this wrap (a short S32 stub backfilled; `L055` was doubly-used, so the S31 LaTeX entry was renumbered to `L056`).

**One line:** Started a deep paragraph-by-paragraph clean of the extended manuscript with Erfan; finalized the **abstract** (conference register, single paragraph, no numbers/CIs, no em-dashes, results deferred to a `\gap`) and closed a real hole in the em-dash guardrail. **NO experiment, NO science number, NO rung change — Q0–Q5 stand exactly as S31.**

## What happened

- **Oriented**, then evaluated the extended manuscript (abstract + §1–§4). Found the dominant structural issue: two load-bearing arguments (the 2-axis "empty cell" framing and the weak-prior/MAP information-budget argument) are each stated ~3× across abstract/intro/related-work/methods, with verbatim repeats. Plus local issues (relentless long-sentence rhythm, voxel-level CI unit not named, "kill-gated" scaffolding). No claims/over-claim problems — the science prose is faithful.
- **Confirmed the E006 CI unit** from the E006 record: the razor-tight gap CI ([+0.0205, +0.0209]) is a **bootstrap over the 11,442 reliable voxels** (correct for the reality claim); the honest **fold-level** variance lives separately as the E007-lever MDE (+0.013/+0.015), which is why Q2's lever is "undemonstrated." Manuscript is epistemically clean; only needs the unit named in the caption (deferred to the §4 pass).
- **Rewrote the abstract** with Erfan, iterating live: new opening (the inversion as hook, not a dry "a linear map predicts…" fact); removed "kill-gated"; split the weak-prior sentence; **dropped the numeric gaps + CIs** (Erfan's option A — abstract carries the qualitative headline, numbers live in Results); **deferred the entire results summary** to a `\gap` (the two established findings + the downstream arc) at Erfan's call; collapsed source blank lines so it renders as **one paragraph**; removed em-dashes. Written into `main-extended.tex`. PDF rebuilt.
- **Taste-reader workflow:** ran an inline opus agent as a readability/taste judge on each abstract draft (distinct from `prose-register-auditor`, which only catches rule-level register tells). It drove the abstract 7→~8.5 via sentence-splitting. Erfan wants this promoted to a real `.claude/agents/taste-reader.md` (filed in tasks).
- **Fixed the em-dash guardrail (L057):** `ai_tell_lint` only matched the unicode `—`, so LaTeX `---` was invisible regardless of budget; and the budget was 3, not 0. Now detects `---` in `.tex` and the budget is 0 (em-dashes banned, per Erfan's standing rule). Regression-tested. `writing-style.md` updated.
- **Fixed a `/wrap`-paste corruption** at `main-extended.tex:32` (`\tableofcontents/wrap` → `\tableofcontents`).
- **Process:** the D047 Stop register gate re-fires on every manuscript edit; during an interactive clean the body is intentionally dirty, so each edit gets an Erfan-acknowledged **accepted-residual** sign-off. The real ≥2-fresh-auditor clean verdict runs once at the **end** of the full pass.

## Verdict / ladder

NO rung changed. Q0–Q5 stand. This is a write-layer (and meta) session.

## Next

Continue the manuscript clean: **§1 Introduction ¶1** is teed up (split the wall sentence-3; fix "rewards representations the brain would predict"; de-echo the abstract opening). Then §1 ¶2 carries the big intuition-up/formalism-down dedup decision (Erfan leans option 1). Then §2–§4, including naming the E006 voxel-bootstrap CI unit in the §4 caption.
