# Upspeed — read first, write last

**Last updated:** 2026-06-11 (Session 8 — working, autonomous — thinking-panel audit + E008 per-subject NULL → Fork-B reframe)

> **Canonical state lives in [`ladder.md`](ladder.md)** (the rung board + next step, D015). This file is
> the last-session prose; if it disagrees with the ladder, the ladder wins. With no task, run `/orient`.

## Current state

Phase = **Judge → (next) Design**. The session's result is an **evidence-driven course correction**: the in-domain F1 "headline" did not survive a per-subject test, and the thesis is now honestly **Fork B**.

- **L0/A2 — alignment is real & measurable — ✅ PASS (powered).** E006 (LeBel voxelwise) gap +0.021/+0.028, unchanged.
- **L3/F1 — the former headline — ❌ NULL per-subject (E008, well-powered).** Running the E005 brain-specific contrast **per individual** (n=9 UIDs, not the 5-UID average) gives **+0.00010, t-CI [−0.0004,+0.0006]**, sign 5/9; MDE≈+0.0006 (well-powered). **E005's +0.0081 was a group-averaged-target / shared-stimulus-response measurement** (~1.7× averaging + 2.4× fold-4 inflation), NOT per-person brain alignment — the 4 subjects E005 averaged are individually null. Two-panel-adjudicated. (L015/L016, D018, Erfan-confirmed.)
- **L2b/A3 — does it buy anything PRACTICAL — ❌ bounded NULL (E009, n=8).** No brain-specific OOD-ppl payoff (kd_brain ≈ permuted ≈ textfeat ≈ kd_ppl, within measured MDE); **null-by-construction** — the fulcrum (brain-specific repr change at matched ppl) is itself ~0 (median +0.004, seed-0-outlier-driven). L017.
- **POSITIVE contribution (the paper's spine): L016** — cross-subject target-averaging *manufactures* apparent brain-specificity; the matched-ppl + permuted-twin + per-subject protocol detects it (+0.0081→+0.0001 collapse). The experimental ladder is **complete**; next is write-up.

## What was done (Session 8 — working, autonomous)

1. Built the **thinking panel** (D017): `counter-argument` / `socratic-thinker` / `premortem-analyst` / `first-principles-grounder` + model routing.
2. Ran the panel **before compute** → caught E005's pseudo-replicated CI + the underpowered transfer test (re-analysis `scripts/reanalyze_e005_e006.py`, L015). Pivoted.
3. Designed + oracle-gated + ran **E008** (per-participant, n=9, 945 runs, 4-GPU): **well-powered NULL** (L016). Panel-adjudicated the averaging steelman → rejected.
4. Reframed the ladder to **Fork-B** (D018, Erfan-confirmed): A2-powered + the per-subject null + anti-confound methodology + A3.
5. Designed + grounded + oracle-gated **A3/E009**; cleared doc-consistency (feghhi→hadidi redirect).

## What to do next (manuscript v0.7 — REFRAMED to protocol-headline; panel-verified; experimental ladder complete)

**Headline reframe (S8, grounded):** a final premortem + a decisive lit-scout pass moved the paper's headline from "averaging manufactures specificity" to **the matched-ppl + permuted-twin + per-individual PROTOCOL** (no prior brain-tuning paper runs it end-to-end; it *bites* → well-powered nulls). The averaging confound is now the concrete motivating instance — and it has **real live targets**: Tuckute 2024 (our benchmark — participant-averaged BOLD) + group-average RSA; the per-subject tuning works (Schrimpf/Negi/Bilgin/Moussa) are untouched, so the scope is honest (L022). **E012** (per-individual voxelwise on the powered substrate) is **deferred-power-limited at n=3** (oracle-gated; data UTS01/02/03 acquired + retained for a future n≳8–10 cohort; L021).

The **manuscript (v0.7) is drafted, figured, and panel-verified** (`docs/manuscript/00_paper-draft-v0.md`): counter-argument ×2, first-principles ×2, socratic, premortem ×2. Every claim is either solid or honestly scoped:
- **A2** real & measurable, powered (E006). **Per-individual F1 null** (E008, well-powered; **regime-robust to LoRA capacity**, E011). **A3** practical null (E009). **Headline (positive contribution): averaging inflates apparent brain-specificity** — averaged target +0.008 (E005) vs per-individual ~0 (E008) — + the matched-ppl/permuted-twin/per-subject protocol. The subjects-averaged **dose-response (E010/E010b) is hedged** to "suggestive but noisy" (the clean nested curve was a design artifact; random subsets are non-monotone — L020).

Remaining (genuine forks / polish — Erfan's call):
1. **The one open scientific door — now SCOPED + feasible (E013).** The full-FT/contrastive + multi-subject naturalistic regime under our protocol — the only path that can move the per-individual verdict. **Feasible:** the power sim (L024) says ~5 deep subjects suffice for δ=+0.003, and the **denizenslab dataset has 6** (`data/paper-repos/speech-llm-brain`). The cost is the heavy build (the deferred E007 voxelwise-tuning loop + a contrastive-loss arm + denizenslab download) — a fresh-session major unit, not a tail-of-session rush. Designed in `docs/experiments/E013_*.md`; ready to launch.
   - Submission-gate (oracle, v0.8): SUBMISSION-READY as thesis, READY-WITH-MINOR-EDITS as workshop (edits done: abstract tightened, stale footer fixed, §2 external-validity added). Main-track ceiling = the confound's external validity, honestly handled as a benchmark-validity warning (the tuning lineage is per-subject; none averages targets).
2. **Manuscript polish toward submission:** §1 intro + §2 related-work prose to match the protocol-headline; the A2 voxel-map figure; venue/length. The load-bearing frame (title/abstract/§4.2/§5/§7) is reframed and consistent.
3. **Write-up against the live target:** make the Tuckute-averaged-target critique concrete (it's the standard sentence benchmark) — strengthens the protocol motivation.

**Recommendation:** the paper is submission-shaped as a **protocol/measurement-standard contribution** (broad, survives the adversarial reviewers) with the averaging confound as a grounded cautionary instance + the well-powered nulls as evidence the protocol bites. Next move is polish→submit, or acquire the multi-subject naturalistic cohort for the open-frontier test. Both are Erfan's call (authorship + data/resource).

## Blockers

- **None rate-limiting.** GPUs free; harness + analyzer built; A3 design oracle-gated and execution-ready.
- **Watch:** A3 must run OFFLINE (no GLUE cached → OOD-ppl-ratio primary); the brain-specific change at matched ppl is small (E008) → quantify the achievable Δ first or A3 is null-by-construction; permuted-brain + text-feature controls are load-bearing (pirlot-2022 redux). A clean A3 null is the anticipated, publishable Fork-B result.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs: 4× L40S (all free at session end). Background jobs harness-tracked via `run_in_background` (notify on completion); 4-GPU split by UID works well.
- **E008 rerun:** `scripts/run_brain_lever.py --uids 797 837 841 848 856 865 875 876 880 --arms mse lm_only --permute-kinds mse --kd-teacher Qwen/Qwen2.5-1.5B --seeds 0 1 2 --folds 5 --n-perm 5` (split across GPUs by UID subset). Verdict: `scripts/analyze_e008.py outputs/E008_g*.json` (crossed inference). **uid 853 excluded** (incomplete ROI).
- **Outputs** (gitignored): `outputs/E008_g{0,1,2,3}.json` (945 runs), `E008_plumbing_smoke.json`. Re-analysis: `scripts/reanalyze_e005_e006.py`.
- **New agents:** `.claude/agents/{counter-argument,socratic-thinker,premortem-analyst,first-principles-grounder}.md` (need a session reload to register as types; usable as `general-purpose`+persona meanwhile).
- **Git:** `main`, ~16 atomic commits this session. Push only when asked. Cost ~$160 (authorized).
