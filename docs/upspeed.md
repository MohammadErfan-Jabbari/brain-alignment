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

## What to do next (manuscript v0.3 exists; future-work experiments + figures)

The experimental ladder is **complete** and the **manuscript v0.3 draft is written + panel-reviewed** (`docs/manuscript/00_paper-draft-v0.md`): A2 (powered) + the positive L016 contribution (averaging produces apparent specificity, **earned by the E010 dose-response**) + F1 null (E008) + A3 null (E009). Remaining:

1. **(Future-work experiment, the key open test — §6 of the draft) Strong-regime per-individual arm:** full fine-tuning (not light LoRA) on naturalistic data, per individual, with the permuted twin — to directly engage Negi-2025's *positive* per-individual encoding result and determine whether the per-subject null is a property of brain-tuning or of the matched-ppl light regime. This is the one result that would most strengthen (or qualify) the paper.
2. **Per-subject optimization null on the LeBel voxelwise substrate** (common substrate with A2 — closes the substrate-mismatch limitation).
3. **Figures** (`scripts/figures/`): the E010 dose-response curve + the +0.0081→+0.0001 collapse, the E006 A2 voxel map, the A3/E009 nulls with measured MDEs.
4. Manuscript polish: final title, venue/length, related-work prose.

**Decision for Erfan:** the paper's honest story is solid as-is (Fork-B, positive contribution earned); the strong-regime arm (1) is the highest-value addition before submission but is a real new experiment — his call on whether to invest it now or submit the current scope.

## Blockers

- **None rate-limiting.** GPUs free; harness + analyzer built; A3 design oracle-gated and execution-ready.
- **Watch:** A3 must run OFFLINE (no GLUE cached → OOD-ppl-ratio primary); the brain-specific change at matched ppl is small (E008) → quantify the achievable Δ first or A3 is null-by-construction; permuted-brain + text-feature controls are load-bearing (pirlot-2022 redux). A clean A3 null is the anticipated, publishable Fork-B result.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs: 4× L40S (all free at session end). Background jobs harness-tracked via `run_in_background` (notify on completion); 4-GPU split by UID works well.
- **E008 rerun:** `scripts/run_brain_lever.py --uids 797 837 841 848 856 865 875 876 880 --arms mse lm_only --permute-kinds mse --kd-teacher Qwen/Qwen2.5-1.5B --seeds 0 1 2 --folds 5 --n-perm 5` (split across GPUs by UID subset). Verdict: `scripts/analyze_e008.py outputs/E008_g*.json` (crossed inference). **uid 853 excluded** (incomplete ROI).
- **Outputs** (gitignored): `outputs/E008_g{0,1,2,3}.json` (945 runs), `E008_plumbing_smoke.json`. Re-analysis: `scripts/reanalyze_e005_e006.py`.
- **New agents:** `.claude/agents/{counter-argument,socratic-thinker,premortem-analyst,first-principles-grounder}.md` (need a session reload to register as types; usable as `general-purpose`+persona meanwhile).
- **Git:** `main`, ~16 atomic commits this session. Push only when asked. Cost ~$160 (authorized).
