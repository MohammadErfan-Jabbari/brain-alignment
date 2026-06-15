# Session 15 — analysis / infrastructure: the three-layer deliverable model + the scientific-writing skill

**Date:** 2026-06-15 · **Mode:** ANALYSIS / INFRASTRUCTURE (no new evidence; no rung changed). Began as an analysis session (resume R05) and pivoted, at Erfan's direction, to building the writing system that the analysis week will run on.

## What happened (in order)

1. **R05 review (the original analysis task).** Confirmed R05 has been byte-stable since S9 (its only 3 commits are all S9; the four working sessions S10–S14 correctly never touched it). Cross-checked every written number (§0–§7) against `ladder.md`: all current. One stale number found and fixed: the §13 placeholder cited the E015 law as `r≈−0.92`, now corrected to `r≈−0.78` (bpb). Expanded the §8 placeholders (§11–§16) to name the post-S9 experiments (E017, E020, E019) and the L041 scope correction, and synced the §0 coverage-frontier sentence. Commit `6c51bd9`. Narrative frontier unchanged: next is §9 (E005→E008).

2. **Designed the three-layer written-deliverable model** (deep interview with Erfan): **reports** (Markdown, continuous) → **extended manuscript** (LaTeX, internal master) → **public manuscript** (LaTeX, frozen `vN` cuts). The extended is a hybrid: an always-current paper body (compresses cleanly to a public cut) plus an append-only dated checkpoint log. Knowledge flows down only; cadences differ (reports continuous; manuscripts checkpoint-derived only on Erfan's explicit call). Format decision grounded by a real grep test on `project.tex` vs `R05.md` (md returns whole-paragraph matches and cannot break a build → the continuous layer; LaTeX for the checkpoint manuscripts). Landed as the `docs/03-methodology.md` "Deliverable layers" section. Commit `27c7cae`.

3. **Cloned the `academic-research-skills` framework** (read-only, gitignored, `data/reference-repos/academic-research-skills/`) and mapped it with a swarm of 7 sonnet + 1 opus subagents. Extracted six adoptions (C1–C6): anti-AI-tell + scientific-voice rules, graded hedging tied to measured-vs-correlational, deterministic verifier patterns (`check_*.py` + PreToolUse-hook + gold-set), the `[MATERIAL GAP]`/`\evd`/`\gap` provenance discipline, silent-fix + precommitment, and a Devil's-Advocate review. Declined the heavy plugin machinery (Material Passport, 4-skill pipeline, bilingual/disclosure) per our adaptive-semistructure rule. Deep-dive on `draft_writer_agent.md` extracted the anti-AI-tell mechanism (em-dash budget, the jargon list, throat-clearing/meta-commentary bans, one-term-per-concept, burstiness, the Clarity Test, "clarity not detector-evasion", silent fixes).

4. **Built the `scientific-writing` skill** (`.claude/skills/scientific-writing/`, 17 files): `SKILL.md` + 4 references (writing-style, provenance-d011, latex-conventions, review-pass) + 6 scripts (ai_tell_lint, check_evd_resolution, check_gap_survival, check_number_consistency, check_claim_survival, run_checks) + 6 assets (preamble.sty, numbers.tex, two main skeletons, references.bib, latexmkrc) + a short pointer doc `docs/references/scientific-writing.md`. Design panel-hardened over **two adversarial critique rounds** (skill-creator-conformance, premortem, first-principles), each convergent; all surviving fixes integrated (report-first pushy description, fast-path vs full-loop tiering, per-layer loop + compression step, reframed precommitment, no global toggle, number-driven D011 check, the claim-survival compression gate, eat-our-own-dogfood prose). Verifiers tested on real files (linter caught R05's 58 em-dashes + jargon; evd-checker caught a bare number + a dangling `\evd{E999}`; gap/number/claim checks behave correctly). **Full `latexmk`+`biber` build of the assets passes** (80KB PDF, `.bbl`). Commits `c9e8df2`, `275ab87`, `3c75bde`, `2a0a644`, `b4375d2`.

5. **Fused the model into the repo's governing surfaces** (D035): the decision record, a `CLAUDE.md` behavioral rule (route writing through the skill; never auto-update the extended/public manuscript), the `docs/README.md` map rows, and the now-corrected `docs/manuscript/README.md` (dropped "paper and report are the same document" / "no separate latest copy") and `docs/reports/README.md`. Commit `0f101fe`.

## Verdict / science state

**No rung flipped. No new evidence.** The science ladder is unchanged from S14: A2 ✅ (powered, E006), L3/F1 ❌ per-individual null (E008, robust), L2b/A3 ❌ bounded null, the spine on the powered nulls + E015 + L016 + the bounded E020 ceiling + E019 corroboration. This session built the *writing infrastructure*, not the science.

## Decisions / learnings

- **D035** — the three-layer deliverable model + the scientific-writing skill (Erfan-approved). Recorded in `decisions/decisions.md`.
- **L043** — `ecc:skill-create` is a git-history pattern extractor, not a skill-authoring tool; author designed skills to spec (or via the official `skill-creator:skill-creator` plugin). Recorded in `learnings.md`.

## Continuity-audit notes

- **Tooling friction:** the `/skill-create` slash command (`ecc:skill-create`) turned out to be a git-pattern miner; caught before it produced garbage, switched to hand-authoring + `skill-creator:skill-creator` (→ L043).
- **Doc consistency:** fixed this session — methodology, decisions, CLAUDE.md, the doc map, and both folder READMEs now agree on D035; the manuscript README's two false claims removed. No new D011 violations (numbers.tex seeds trace to E006/E008/E005).
- **Brain mirror:** D035 warrants a gbrain `put_page` to `projects/brain-alignment`; deferred to conserve this (very long) session's budget, flagged for the next session start.
- **Git:** 8 atomic commits, tree clean except two pre-existing untracked items (`docs/manuscript/latex/` coursework templates; `untitled.md` scratch, harmless).
- **Open loop:** the original analysis task (R05 §9) is still pending; the writing system is now in place to do it well.
