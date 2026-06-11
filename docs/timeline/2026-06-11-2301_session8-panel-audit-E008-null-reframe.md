# Timeline — 2026-06-11 23:01 — Session 8: thinking-panel audit → E008 per-subject NULL → thesis reframed to Fork-B

**Mode:** working (autonomous `/goal`). **Branch:** main. **Commits:** `e818292` → `91bf1c6`+ (≈16 atomic). **Cost:** ~$160+ (authorized heavy autonomous session). **Headline:** caught an overclaimed thesis result *before* it became the headline, and reframed the thesis honestly.

## Purpose
Continue climbing the ladder autonomously; build a standing adversarial "thinking panel"; ground every step in the papers/course material; write back to gbrain continuously.

## Session mode
Working (Design → Run → Judge): produced new evidence (E008), a reproducible re-analysis, and a reframed ladder. One analysis-flavored thread (the literature grounding for A3) folded in.

## What happened
1. **Built the thinking panel (D017).** Four reasoning-methodology subagents in `.claude/agents/` — `counter-argument`, `socratic-thinker`, `premortem-analyst`, `first-principles-grounder` (fable/sonnet, MECE vs the pre-compute `oracle-reviewer`) + model-routing on existing agents. The post-step adversarial loop Erfan asked for.
2. **Panel audit overturned the planned next step (pre-compute).** Three fable reviews + a reproducible re-analysis (`scripts/reanalyze_e005_e006.py`) found: (a) E005's "F1 CONFIRMED, CI excludes 0" is **pseudo-replicated** — 15 cells over one 5-UID-averaged target; at the honest fold unit the t-CI **includes 0**; one outlier fold = 52% (L015). (b) The planned **LeBel transfer test is underpowered** (paired MDE needs ρ≥0.9). (c) Grounding fixes: "rate-distortion curve" is a proxy frontier not the literal theorem; the uncited Proietti 2025 paper digested.
3. **Pivoted to solidify the foundation (E008), oracle-gated.** Per-participant in-domain test (n=9 Tuckute UIDs as independent units; uid 853 excluded — incomplete ROI). Oracle HOLD → addressed (crossed subject+fold inference, LOO-fold, train/held-out split, n_perm=5, SNR control). Extended `run_brain_lever.py` (`--uids`) + wrote `analyze_e008.py` (crossed inference). Smoke PASS. Ran 945 LoRA-KD runs across 4 GPUs.
4. **E008 VERDICT: well-powered NULL (L016).** Per-subject brain-specific gain = **+0.00010** (t-CI [−0.0004,+0.0006], n=9, sign 5/9; fold-clustered CI incl 0, fails LOO-fold; the 4 E005-averaged subjects individually null). Two-panel-adjudicated (counter-argument + first-principles): well-powered (MDE≈+0.0006), not noise-floor; the averaging-SNR steelman tested and rejected. **E005's +0.0081 was a group-averaged-target / shared-stimulus-response measurement** (~1.7× averaging + 2.4× fold-4 inflation), NOT per-person brain alignment.
5. **Grounded A3 (the real gap):** drafted `E009`, digested its 3 prior-art finalists (Negi 2025, Schwartz 2019, Guo 2024). Key: the matched-ppl + permuted-brain control is exactly what every A3 prior lacks. Oracle-gated E009 → HOLD resolved (all-data save-checkpoint mode, *measured* MDE, text-feature control arm, OOD-ppl-ratio primary; pilot-first).
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
- Two `graphify` tooling commits appeared from subagent/hook activity (additive, harmless) — noted, not reverted.
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

- **Drafted the paper** (`docs/manuscript/00_paper-draft-v0.md`), grounded (every number → recorded source). Panel-reviewed it (counter-argument + first-principles, fable):
  - first-principles found 2 factual mismatches (n=9 split mis-stated 5/5 → train-4/held-5; "Spearman" → Pearson r=−0.88) + MDE range + explicit 1.7× arithmetic + absolute uR² — all fixed.
  - counter-argument (MAJOR-REVISION): "manufactures" was asserted not shown; Negi-2025's per-participant TR-shuffle-controlled *positive encoding* result unaddressed; positive/null on different substrates. → added the Negi reconciliation, separated the two contributions, substrate-mismatch + strong-regime-open-test limitations, softened verb to "inflates."
- **E010 — the averaging dose-response** — to EARN the central claim: gap(k) = −0.0002/−0.0001/+0.0023/+0.0194/+0.0071 for k=1/2/3/5/9. **k=1 null; the gap appears only on averaging** → averaging *produces* the apparent brain-specificity (rising limb tracks the noise-ceiling). Honest caveat: not perfectly monotone (k=9<k=5, wide 4-seed bars) → qualitative law, not a precise fit. L018; §4.2b added.

**End state:** experimental ladder complete + manuscript v0.3 (panel-reviewed, central claim experimentally earned). Open future-work (flagged in §6): the strong-regime per-individual arm (the key test vs Negi), the LeBel-voxelwise per-subject null, figures. Session 8 total: ~28 commits, ~$366, fully autonomous; 4 experiments (E008/E009/E010 + re-analysis) + the paper.
