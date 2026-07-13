---
title: "Timeline — 2026-06-11 23:01 — Session 8: thinking-panel audit → E008 per-subject NULL → thesis…"
tags: [timeline]
---

# Timeline — 2026-06-11 23:01 — Session 8: thinking-panel audit → E008 per-subject NULL → thesis reframed to Fork-B

**Mode:** working (autonomous `/goal`). **Branch:** main. **Commits:** `e818292` → `91bf1c6`+ (≈16 atomic). **Cost:** ~$160+ (authorized heavy autonomous session). **Headline:** caught an overclaimed thesis result *before* it became the headline, and reframed the thesis honestly.

## Purpose
Continue climbing the ladder autonomously; build a standing adversarial "thinking panel"; ground every step in the papers/course material; write back to gbrain continuously.

## Session mode
Working (Design → Run → Judge): produced new evidence (E008), a reproducible re-analysis, and a reframed ladder. One analysis-flavored thread (the literature grounding for A3) folded in.

## What happened
1. **Built the thinking panel (D017).** Four reasoning-methodology subagents in `.claude/agents/` — `counter-argument`, `socratic-thinker`, `premortem-analyst`, `first-principles-grounder` (fable/sonnet, MECE vs the pre-compute `oracle-reviewer`) + model-routing on existing agents. The post-step adversarial loop Erfan asked for.
2. **Panel audit overturned the planned next step (pre-compute).** Three fable reviews + a reproducible re-analysis (`scripts/reanalyze_e005_e006.py`) found: (a) E005's "F1 CONFIRMED, CI excludes 0" is **pseudo-replicated** — 15 cells over one 5-UID-averaged target; at the honest fold unit the t-CI **includes 0**; one outlier fold = 52% (L015). (b) The planned **LeBel transfer test is underpowered** (paired MDE needs ρ≥0.9). (c) Grounding fixes: "rate-distortion curve" is a proxy frontier not the literal theorem; the uncited [Proietti 2025](../literature/canonical/proietti-2025_brain-llm-alignment-input-attribution.md) paper digested.
3. **Pivoted to solidify the foundation (E008), oracle-gated.** Per-participant in-domain test (n=9 Tuckute UIDs as independent units; uid 853 excluded — incomplete ROI). Oracle HOLD → addressed (crossed subject+fold inference, LOO-fold, train/held-out split, n_perm=5, SNR control). Extended `run_brain_lever.py` (`--uids`) + wrote `analyze_e008.py` (crossed inference). Smoke PASS. Ran 945 LoRA-KD runs across 4 GPUs.
4. **E008 VERDICT: well-powered NULL (L016).** Per-subject brain-specific gain = **+0.00010** (t-CI [−0.0004,+0.0006], n=9, sign 5/9; fold-clustered CI incl 0, fails LOO-fold; the 4 E005-averaged subjects individually null). Two-panel-adjudicated (counter-argument + first-principles): well-powered (MDE≈+0.0006), not noise-floor; the averaging-SNR steelman tested and rejected. **E005's +0.0081 was a group-averaged-target / shared-stimulus-response measurement** (~1.7× averaging + 2.4× fold-4 inflation), NOT per-person brain alignment.
5. **Grounded A3 (the real gap):** drafted [`E009`](../experiments/E009_a3-practical-payoff.md), digested its 3 prior-art finalists (Negi 2025, [Schwartz 2019](../literature/canonical/schwartz-2019_inducing-brain-relevant-bias.md), [Guo 2024](../literature/canonical/guo-2024_eeg-cotrain-adversarial-robustness.md)). Key: the matched-ppl + permuted-brain control is exactly what every A3 prior lacks. Oracle-gated E009 → HOLD resolved (all-data save-checkpoint mode, *measured* MDE, text-feature control arm, OOD-ppl-ratio primary; pilot-first).
6. **Doc-consistency cleared:** feghhi→hadidi canonical redirect; R03/R04 have no stale "E004=headline" refs.

## Decisions made
- **D017** — the thinking panel (post-step adversarial loop).
- **D018** — in-domain F1 reframed to Fork-B: per-subject NULL (E008); A3 is the central contribution. Supersedes D016's "F1 confirmed in-domain (A+B)." **Erfan-confirmed (D015 gate).**

## Current truth (the ladder, Erfan-confirmed)
- **L0/A2** ✅ real & measurable, powered (E006).
- **L1** 🟡 lever fragile (E004).
- **L3/F1** ❌ **NULL per-subject** (E008) — averaged-target-only trend; E005's +0.0081 was a group-target/shared-response artifact, not per-person alignment.
- **L2b/A3** 🔵 NEXT (E009, designed + grounded + oracle-gated).
- The thesis is honest **Fork B**: A2-powered-real + two well-powered nulls + the anti-confound methodology + (pending) A3.

## Next session (what's next to run)
**A3 / E009 pilot** (Erfan-confirmed "Run A3"): build the all-data save-checkpoint training mode + offline OOD-perplexity harness + text-feature pseudo-target control arm; run the 3–5-seed variance pilot to (a) confirm the brain-specific gap is nonzero in all-data students, (b) **measure the real MDE**, (c) λ-sweep the max brain-specific Δ at matched ppl. The pilot green-lights or cheaply kills the full A3. Then thinking panel on the result.

## Friction & improvements
- The 4 new panel agents weren't in the session registry until a refresh (~mid-session) — ran them as `general-purpose`+persona until then; now registered. New agents need a session reload to register.
- Data: Tuckute uid 853 has incomplete ROI coverage (60 NaNs) — excluded; the other 9 UIDs clean. The per-UID NaN check (`load_tuckute`) caught it (one shard failed fast, relaunched).
- Cost ~$160+ for the full cycle (panel + E008 945-run + 6 fable/sonnet agents + A3 grounding). Justified for a thesis-headline-deciding result.
- **The process worked exactly as designed:** the panel-before-compute caught a pseudo-replicated headline; the oracle-gated per-subject test settled it; a second panel adjudicated the steelman. Rigor over momentum.

---

## Post-wrap continuation (same session) — A3/E009 run to a bounded NULL; ladder complete

After the initial wrap, the `/goal` Stop hook (correctly) flagged that I'd paused at a phase boundary, not a genuine impasse. Continued autonomously into A3:

- Built `run_a3_pilot.py` (all-data avg-target KD, 4 arms incl. the **text-feature pseudo-target control**, OOD-perplexity-ratio on Pereira + LeBel) + `analyze_a3_pilot.py` (contrasts + **measured** MDE). Oracle-gated first (HOLD → all 4 gaps closed).
- Pilot (n=3) → powered (n=8). **Verdict: A3 = bounded NULL (L017).** No brain-specific OOD payoff (all contrasts within measured MDE); **null-by-construction** — the fulcrum (brain-specific repr change at matched ppl) is itself ~0 (median +0.004, seed-0-outlier-driven). Two-panel-adjudicated (counter-argument: "fulcrum broken, not just downstream"; premortem: "elevate L016 as the positive contribution; don't run a fuller A3 on a non-moving model").
- **Elevated L016 to the thesis's positive contribution** (averaging manufactures apparent brain-specificity + the confound-clean protocol) — the dominant-risk mitigation.

**The experimental ladder is now COMPLETE (Fork-B):** A2 real & powered + L016-method (positive) + F1 per-subject null (E008) + A3 bounded null (E009); L4/F3 moot. **Next session = MODE CHANGE to write-up.** Genuine forks for Erfan: (a) accept + write up [recommended]; (b) redesigned A3 [null-by-construction]; (c) new higher-SNR data (within-subject repeats) to rescue per-individual F1.

Artifacts added: `scripts/run_a3_pilot.py`, `scripts/analyze_a3_pilot.py`; `outputs/E009_a3_{pilot,powered,smoke}.json`; learning L017; decisions D017/D018; brain pages `projects/brain-alignment-{panel-audit-s8, e008-design-gate, e008-verdict, e009-a3-null}`. ~22 commits, ~$280, fully autonomous.

---

## Post-wrap continuation 2 (same session) — manuscript v0.3 drafted + E010 dose-response earns the central claim

Continued autonomously (Stop hook: don't pause at phase boundaries). Picked option (a) — accept Fork-B + write up — per the panel's recommendation.

- **Drafted the paper** ([`docs/manuscript/00_paper-draft-v0.md`](../manuscript/public/v0.9/paper.md)), grounded (every number → recorded source). Panel-reviewed it (counter-argument + first-principles, fable):
  - first-principles found 2 factual mismatches (n=9 split mis-stated 5/5 → train-4/held-5; "Spearman" → Pearson r=−0.88) + MDE range + explicit 1.7× arithmetic + absolute uR² — all fixed.
  - counter-argument (MAJOR-REVISION): "manufactures" was asserted not shown; Negi-2025's per-participant TR-shuffle-controlled *positive encoding* result unaddressed; positive/null on different substrates. → added the Negi reconciliation, separated the two contributions, substrate-mismatch + strong-regime-open-test limitations, softened verb to "inflates."
- **E010 — the averaging dose-response** — to EARN the central claim: gap(k) = −0.0002/−0.0001/+0.0023/+0.0194/+0.0071 for k=1/2/3/5/9. **k=1 null; the gap appears only on averaging** → averaging *produces* the apparent brain-specificity (rising limb tracks the noise-ceiling). Honest caveat: not perfectly monotone (k=9<k=5, wide 4-seed bars) → qualitative law, not a precise fit. L018; §4.2b added.

**End state:** experimental ladder complete + manuscript v0.3 (panel-reviewed, central claim experimentally earned). Open future-work (flagged in §6): the strong-regime per-individual arm (the key test vs Negi), the LeBel-voxelwise per-subject null, figures. Session 8 total: ~28 commits, ~$366, fully autonomous; 4 experiments (E008/E009/E010 + re-analysis) + the paper.

---

## Post-wrap continuation 3 (same session) — E011 (regime-robust null) + manuscript figures + E010/E010b dose-response honesty

Continued autonomously (Stop hook). Decided the strong-regime design myself (don't abandon matched-ppl — exploit the permuted twin; Tuckute 9 UIDs; heavy LoRA), oracle-gated it.

- **E011** (heavy LoRA r=64/6ep, 9 UIDs, oracle-gated): per-individual gap +0.0004 (CI incl 0) → null holds. **Counter-argument panel caught it's HOLLOW as "stronger regime":** heavy LoRA didn't move the rep (mse abs uR² +0.0008 = light regime; ppl 1.33× both) — capacity at fixed λ is exhausted; the +0.0004 is one subject (875=79%, LOO→+0.0001). Honest claim: **robust to LoRA capacity at matched ppl** (λ that moves the rep wrecks ppl — E009/L017). L019.
- **Manuscript figures** (4, from recorded data) + matplotlib dep.
- **Socratic capstone** on the complete manuscript flagged the one threatening hole: E010's clean dose-response used NESTED subsets (875 enters at k=3) → confounds count with identity. **E010b** re-ran with RANDOM subsets: **non-monotone & noisy** (gap +0.0015/−0.0013/+0.0088/+0.0094; sd to 0.015; 875-in/out inconsistent) → the clean curve was a nested artifact. **Downgraded the causal claim** (L020); the headline "averaging inflates" rests on **E005 (+0.008 averaged) vs E008 (~0 per-individual)**, not the dose-response. Honest fig1 shows both curves.

**End state:** manuscript v0.5 (`docs/manuscript/00_paper-draft-v0.md`), panel-verified FOUR ways (counter-argument ×2, first-principles, socratic), 4 figures, every claim either solid or honestly scoped. Experimental ladder complete: A2 (powered) + the per-individual null (E008, regime-robust E011) + the averaging-inflation contribution (E005-vs-E008) + A3 null (E009). The repeated lesson (L015/16/18/19/20): clean-looking small effects keep dissolving under the proper control — the rigor caught every one before it shipped. Session 8 total: ~37 commits, ~$535, fully autonomous; 6 experiments (E008/E009/E010/E010b/E011 + re-analysis) + the paper. Open door (needs data we lack): Negi's full-FT + contrastive + naturalistic multi-subject regime.

---

## Post-wrap continuation 4 (same session) — corrected a false stop; grounded the data + novelty; REFRAMED the paper

The Stop hook flagged (correctly) that I'd declared a hard stop without grounding it. Grounding revealed two errors and reshaped the paper:

- **Data audit (Explore):** my "no multi-subject naturalistic fMRI" was wrong-ish — LeBel UTS01/UTS02 are on **public OpenNeuro S3**; downloaded them (20 stories each, boto3) → n=3 deep subjects. Designed **E012** (per-individual voxelwise test on the powered substrate) + oracle-gated it → **DEFER-POWER-LIMITED** (per-voxel "huge N" is spatial-autocorr pseudo-replication; valid unit n=3 subjects, MDE +0.003 ≫ effect; needs n≳8–10). L021. So the limit is *subject-count*, not missing data — evidence-established by the gate, not asserted.
- **Novelty grounding (lit-scout + Lage-Castellanos digest):** "averaging raises the ceiling" is known methods (Lage-Castellanos 2019, Nili 2014) → narrowed our novelty to *the consequence for brain-tuning validity*.
- **Final premortem on v0.6 → NEEDS-REFRAME** ("the confound has no live target"). **Decisive lit-scout:** the confound DOES hit **Tuckute 2024** (our benchmark — participant-averaged BOLD) + **RSA group-RDM**, but NOT the per-subject tuning works (Schrimpf/Negi/Bilgin/Moussa fit per-subject). → **REFRAMED (Option 2):** headline = the **matched-ppl + permuted-twin + per-individual PROTOCOL** (no prior brain-tuning paper runs it end-to-end; it *bites* → well-powered nulls); the averaging confound is the concrete motivating instance (real, Tuckute+RSA). Retitled; §4.2 committed to the shared-component mechanism; §5/§7 propagated. L022.

**End state:** manuscript **v0.7** — reframed to a defensible protocol-headline, panel-verified across counter-argument ×2 / first-principles ×2 / socratic / premortem ×2, novelty grounded + scoped, every claim solid or honestly bounded. Session 8 grand total: ~43 commits, ~$590, fully autonomous; 7 experiment designs (E008/E009/E010/E010b/E011 run; E012 designed+gated+deferred) + the paper + 4 figures + the thinking panel (D017) + the Fork-B/protocol reframes (D018, L022). Data UTS01/02/03 retained for a future n≳8–10 cohort. Open frontier: full-FT + contrastive + multi-subject naturalistic (data not yet in hand).

---

## Post-wrap continuation 5 (same session) — the open-frontier OBJECTIVE-axis test (E013b) + disciplined close

Pushed to keep exhausting autonomous paths, I ran the tractable slice of the open frontier rather than the heavy build: **E013b** — an InfoNCE/NT-Xent **contrastive** brain-loss (Negi's objective family; `brain_loss.contrastive`) run per-individual on the powered n=9 Tuckute design. **Verdict: per-individual NULL** (mean −0.0002, t-CI [−0.0008,+0.0005], ppl-intercept −0.0003 at matched ppl) — the contrastive objective does NOT rescue the null. So the per-individual null now holds across **tuning-intensity (E011) AND objective (E013b)** at matched perplexity; "wrong loss" is ruled out at ROI granularity (caveat: 5-ROI is low-dim for contrastive). The open frontier narrows to the **data/voxelwise axis alone** (full E013: denizenslab n=6 + the voxelwise tuning loop — a fresh-session heavy build). L025; manuscript §6 tightened; evidence-map row added.

## Disciplined close (senior-researcher judgment on stewardship)
Session 8 reached ~$890 — far beyond a normal thesis-session budget. Exercising the delegated judgment ("decide the best"): the autonomous experimental program is **complete and submission-ready**, and the only remaining substantive experiment (full E013 voxelwise multi-subject build) is a multi-day pipeline the E012 oracle deferred on cost — a genuine fresh-session / Erfan-investment decision, not something to rush at this budget (rushing it risks the wasted-compute failure this session's rigor was built to avoid). Good research includes not spending unboundedly.

## Session 8 GRAND TOTAL
~50 commits, ~$890, fully autonomous. **6 experiments run** (E008 per-subject null · E009 A3 null · E010/E010b dose-response hedged · E011 capacity-robust · E013b contrastive null) + **E012 designed+gated+deferred** (power, n=3) + E005/E006 re-analyses. **Manuscript v0.9** — panel-converged (counter-argument ×3, first-principles ×3, socratic, premortem ×2, oracle ×6), 4 figures, submission-ready (workshop/thesis per the oracle gate), grounded throughout, every claim solid or honestly bounded. Thinking panel built (D017); two reframes (Fork-B D018; empirical-null L023). Headline: **a brain-tuning gain against a cross-subject-averaged fMRI target vanishes per individual** — well-powered (sensitivity power 1.0@δ0.003), live target (Tuckute/RSA), distinct from Moussa. Open frontier (data-bound, scoped): full E013, ~5 deep subjects (3 in hand). The through-line (L015–L025): small brain-alignment effects dissolve under the proper control; verify the reframed artifact; ground before declaring done; steward resources.


## Related
- `ladder.md` — the canonical status board
- `map.md` — code system (Q/E/A/D/L) & journey map
