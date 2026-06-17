# S22 — 2026-06-17 — Autonomous expansion program + the E021 keystone (working session)

**Mode:** working (generated new evidence: E021, G0/G1, the clean v3 arms). Autonomous (`/goal`: expand the idea set toward a top-venue result). Long, heavy session (~$140+, ~15 subagents). Ended by handing the strategic fork to Erfan.

## What this session set out to do
Erfan set an autonomous goal: analyze all open ideas, build a conference-paper sweep system, build a hierarchical idea tree, then climb the untested nodes (≤4 parallel on the L40S), questioning assumptions, until the project holds a >75%-shot-at-a-top-10-venue result.

## What was built / what ran
- **Program scaffolding (committed):** `docs/expansion-program.md` (master tracker + honest two-path strategy + locked top-10 venue list), `docs/idea-tree.md` (full possibility space by *solution altitude* + climb queue), `docs/litsweep-relevance.md` (sweep taxonomy). 
- **Conference-scout tooling (committed, `scripts/litsweep/`):** DBLP TOC + OpenReview + OpenAlex/Crossref/S2 enrichment + arXiv/OpenReview PDF fetch. Live-tested (DBLP 3540 NeurIPS'23, OpenReview 2260 ICLR'24 w/ abstracts+PDFs). Reusable; the climb did NOT block on a full sweep.
- **Strategy premortem (opus)** re-sequenced the plan: killed the structural-null metric nodes (T4.3/4/5 — fulcrum ~0), demoted the relabeled-regularizer (T2.2 ≈ E004 `frozen`), promoted **T1.3 (non-fMRI cognitive signal)** as the only mechanically-viable main-track bet, and inverted "scaffolding-first" to "run the load-bearing experiment first." Honest venue-bar recalibration: realistic ceiling = strong workshop/Findings + thesis; top-10 main-track conditional on a T1.3 positive.
- **Two canonical notes (committed):** Deng'24 (gaze supervision) + BabyLM (cognitive-objective findings) — E021 positioning + prior.
- **E021 (the keystone) — designed, oracle-gated (HOLD→fixed), and run end-to-end.** Gating chain: **G0/G1 PASS** (surprisal-orthogonal RT residual is reliable, 0.72 vs 0.77 ceiling, Natural Stories n=180) → **G2v1 FAILED** (fine-tune-AULC metric biased toward least-learnable target — caught before the arms) → metric revised to **frozen-probe AULC**, **G2v2/v3 PASS** → 5-arm run fired a "triple-dissociation positive" → panels (counter-argument + first-principles) + **Codex review found a real pad-label bug + control flaws** → **clean v3 rerun** (Codex fixes + log-freq control).
- **Moussa/TA.4 (Path-A) made launch-ready:** repos cloned, fMRI + audio acquired, 3-arm harness `scripts/run_moussa_arms.py` built + dry-run (not run). The external matched-perplexity demonstration is one command from a full run.

## The keystone verdict (E021, clean v3 — trustworthy numbers)
**INCONCLUSIVE at n=3, with one clean sub-result. No rung flipped.**
- **Surprisal-orthogonality is NULL (clean):** raw ≈ residual (+4.3 [−3.9,+12.6]) — removing the surprisal-predictable component changes nothing; the specific novelty buys nothing.
- **Generic word-aligned aux-regularization dominates:** baseline 628 → structured ~177–250 AULC (~450 gap), the E004 `frozen` effect at scale.
- **The broader cognition question is underpowered/unresolved:** residual is the best arm and beats both surrogates on the mean, but CIs touch 0 at n=3 (residual−random [−52.7,+0.3]); the intended cognition-exclusion control (log-frequency) is confounded by learnability (most-learnable → most-disruptive), so it does not adjudicate.
- The v2 "triple-dissociation positive" was a **harness-bug artifact** (the clean rerun changed the verdict twice). Lessons in **L048**.

## Bottom line for the goal
The keystone did **not** deliver a clean main-track positive. It delivered a *narrow* clean negative (surprisal-residualization buys nothing) + a generic-regularization finding + an honestly-inconclusive broader question. The main-track bet did not land; the realistic deliverable remains a strong Path-A negative-results paper (now extendable toward behavioral data) + the thesis. **The >75%-top-10-main-track goal was not reached and, on this evidence, is unlikely without new data/regime.**

## State / next (Erfan's call — handed back, autonomous mode paused)
- **Open decision:** resolve E021 cleanly (more seeds + a *learnability-matched* non-cognitive control) vs. fold the narrow negative into Path A and stop chasing the main-track positive.
- **Path-A floor is ready to execute** (`run_moussa_arms.py`) if Erfan wants the external matched-ppl demonstration for the negative-results paper.
- **No ladder rung changed** (Q0–Q5 unchanged; E021 is a new exploratory experiment, not a rung). Analysis lane (R08–R14 + extended manuscript) untouched and still the thesis floor — it is Erfan's lane (D011).
- Tree clean except deps (`pyproject.toml`/`uv.lock`) + pre-existing untracked files; E021 v3 outputs gitignored under `outputs/e021/`.
