# Upspeed — read first, write last

**Last updated:** 2026-06-12 (Session 8 — working→analysis, autonomous — per-subject NULL robustified across all axes; manuscript v0.9 COMPLETE-AS-ARTIFACT)

> **Canonical state lives in [`ladder.md`](ladder.md)** (the rung board + next step, D015). This file is
> the last-session prose; if it disagrees with the ladder, the ladder wins. With no task, run `/orient`.

## Current state

Phase = **Judge → Argue/Compound (write-up)**. The experimental program is **complete and the per-individual null is robust across every axis we could probe**. The manuscript is content-complete, panel-converged, and now **complete as an artifact** (references close, cross-refs resolve). The thesis is honestly **Fork B**: a measurement-validity result + the well-powered nulls.

- **L0/A2 — alignment is real & measurable — ✅ PASS (powered).** E006 (LeBel voxelwise) trained−untrained gap +0.0207/+0.0277, 95–99% of 11,442 reliable voxels positive. Unchanged.
- **L3/F1 — the former in-domain headline — ❌ NULL per-subject, well-powered, ROBUST.** E005's +0.0081 (5-UID-averaged target) collapses to **+0.00010 per individual (n=9, t-CI [−0.0004,+0.0006], sign 5/9)**. Sensitivity sim: power 1.0 at δ=+0.003 → a TRUE null. **Robust across every axis tested:** light + heavy LoRA (E011), MSE + contrastive/InfoNCE objective (E013b), ROI + voxelwise substrate (E013).
- **L2b/A3 — practical payoff — ❌ bounded NULL (E009, n=8), null-by-construction** (the matched-ppl fulcrum is ~0; λ that grows it wrecks ppl).
- **POSITIVE contribution (the paper's spine):** a cross-subject-averaged fMRI target inflates apparent brain-specificity; the per-individual reality is a well-powered *zero* (sharper than Moussa's "averaged = suboptimal"). The matched-ppl + permuted-twin + **per-individual** protocol detects it. Mechanism: averaging amplifies the shared stimulus-evoked component g at an inflated noise ceiling (known fMRI methods, Lage-Castellanos/Nili); the *consequence for brain-tuning-claim validity* is ours.

## What was done (Session 8 — long autonomous run)

1. Built the **thinking panel** (D017) + ran it after every result. It caught and corrected three of my own overclaims (E005 pseudo-replication → L015; E013 v1 failed-manipulation → retracted; E014 "confound-lift" → deflated to legitimate-SNR). **This adversarial loop is the session's methodological result.**
2. **E008** (per-participant n=9, 4-GPU): well-powered per-individual NULL (L016). Reframed ladder to Fork-B (D018, Erfan-confirmed).
3. **E009** (A3): bounded practical null, null-by-construction (L017).
4. **E010/E010b** (averaging dose-response): nested curve clean but subject-confounded; random-subset curve noisy/non-monotone → hedged to "suggestive, not a clean causal law" (L020). Headline rests on E005-vs-E008, not the dose-response.
5. **E011** (heavy LoRA): null holds; robustness to LoRA *capacity* (heavy LoRA didn't move the rep more — L019).
6. **E013b** (contrastive/InfoNCE objective, n=9): null holds across objectives at matched ppl (L025).
7. **E013** (voxelwise same-substrate, UTS01/02/03 + λ-sweep): the voxelwise distillation lever **does not take hold at any λ** (neutral→degrading, never beats permuted twin) — a single-subject *mechanism* failure, not a power limit, so n≥5 is moot (L026/L027). v1 failed-manipulation retracted.
8. **E014** (averaging on the ENCODING brain-score): per-subject mean +0.0069 (positive!) → 5-UID-avg +0.0357 (~5×). Panel verdict: **NOT a main-track lift** — per-subject scores are positive (unlike E008), so it's legitimate higher-SNR + estimand-shift, not a confound. Found+fixed an unseeded-PCA determinism bug (`pilot_lib.py`). **Verified BEFORE folding in → paper correctly unchanged** (L028).
9. **Manuscript → v0.9, COMPLETE-AS-ARTIFACT:** added a References section (21 entries, `[VERIFY]` flags on memory-sourced); a completeness-critic pass closed orphan citations (Hoak, Li/Brendel) + fixed dangling §6.5/§6.6 pointers. Every in-text citation resolves; gate = READY (thesis/workshop).

## What to do next (Erfan's call — two genuine decision points)

**The experiments are exhausted and panel-bounded; the paper is artifact-complete and gate-READY.** The remaining moves are decisions, not autonomous work:

1. **Ladder confirmation (needs Erfan, per CLAUDE.md):** the board should reflect E013/E013b/E014 done and the null robust across all axes. The flip to "experimental program complete; write-up phase" awaits Erfan's agreement.
2. **The one open scientific door (multi-day build, investment decision):** a *different induction method* — full fine-tuning (not a LoRA distillation readout) on multi-subject naturalistic voxelwise targets. The distillation-readout lever's failure is n-independent (mechanism, E013), so the ~5-deep-subject power requirement (L024) applies only to a full-FT route, and only conditional on it inducing an above-base improvement at all. denizenslab (n=6) is the data path. This is a fresh-session major build, not a tail-of-session rush.
3. **Submission:** v0.9 is submission-shaped (thesis/workshop). Resolve the 5 `[VERIFY]` reference flags, final venue/length, optional §2 prose polish. Authorship → Erfan's call.

**Recommendation:** submit v0.9 as a measurement-validity / protocol contribution (the well-powered nulls show the protocol bites), OR commit a fresh session to the full-FT multi-subject build if a Fork-A rescue is worth the investment (the mechanism evidence suggests it is likely also null, but it's the only untested door).

## Blockers

- **None rate-limiting.** GPUs free; full harness + analyzers + panel built. The remaining items are decisions (ladder confirmation, build investment, submission), not blocked work.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs: 4× L40S (free). Background jobs harness-tracked via `run_in_background`; 4-GPU split by UID works well.
- **Determinism fix:** `pilot_lib.py` PCA now seeded (`random_state=0`). Headline results (E006/E008) are robust to it — they aggregate over many folds/voxels/seeds; E014's single-shot scores were the exposed ones.
- **Manuscript:** `docs/manuscript/00_paper-draft-v0.md` (v0.9, artifact-complete). 5 `[VERIFY]` reference flags to clear pre-submission (Nili/Schrimpf/Caucheteux/Antonello/Tuckute) + Li-Brendel/Hoak.
- **E014:** `scripts/run_averaging_encoding.py`; outputs `outputs/E014_averaging_encoding_seeded.json`.
- **Panel agents:** `.claude/agents/{counter-argument,socratic-thinker,premortem-analyst,first-principles-grounder}.md` (registered as agent types).
- **Git:** `main`, ~53 atomic commits this session. Push only when asked. Cost ~$1217 (authorized, long autonomous run).
