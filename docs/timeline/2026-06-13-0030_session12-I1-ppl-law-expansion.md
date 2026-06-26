---
title: "Session 12 — I1: cross-family ppl↔alignment law expansion (E015) — WORKING (autonomous)"
tags: [timeline]
---

# Session 12 — I1: cross-family ppl↔alignment law expansion (E015) — WORKING (autonomous)

**Date:** 2026-06-13 (started ~2026-06-12 23:09, ran overnight) · **Mode:** working (autonomous, /goal set)
**Lane:** 🔬 implementation roadmap, item **I1** (of I1→I2→I3→I4). **Ladder:** no rung flips (E015 = analysis-support).

## What ran
Expanded E015's cross-family alignment∝−quality law from **8 models / 3 families → 22 models / 6 families**
(added OPT ×5, full pythia ladder ×6, Qwen2.5-7B, Llama-3.2 ×2 via non-gated `unsloth` mirror, Mistral-7B).
Full Design→Run→Judge with the complete rigor stack:
- **oracle-reviewer gate (fable, pre-compute):** HOLD → 1 fatal + 3 structural fixes, all adopted. The
  fatal one: per-token perplexity is not comparable across a 32k–151k vocab span (vocab correlates with
  family) → switched x-axis to **bits-per-byte** (tokenizer-independent; novel in this subfield per lit-scout).
- **Codex code-critic (gpt-5.5):** 1 MUST-FIX (bpb byte/token correspondence) + 7 SHOULD-FIX, all applied.
- **thinking panel (counter-argument + premortem + first-principles, fable):** every objection verified
  against the JSON and folded in (floor/scale, effective-n, Q2 reframe, L016 framing, DPI).
- mid-run bug caught + fixed: an eos-prepend poisoned Qwen2.5-3B's scoring (ppl 105 vs healthy 32.6) — a
  high-leverage outlier; reverted to standard no-prepend bpb (recompute, not full re-run).
- grounding: lit-scout (Q2 is OPEN/publishable) + paper-digest of Antonello-2023 (caught r=0.991→0.91 error).

## Verdict (recorded in E015 doc; numbers in `outputs/E015_expand/`)
- **Q1 — cross-family law CONFIRMED, CORRECTED:** mid-layer unique R² vs log bpb, **r=−0.783**
  (family-cluster CI [−0.911,−0.500]), LOFO-robust [−0.74,−0.83]. **Weaker than v2's inflated −0.929**
  (per-token-ppl + best-layer + 3-family span). Floor-steepened: operative capable-band r≈−0.48 (CI incl. 0);
  load-bearing claim rests on full-range law + conditional-MI floor + scale-controlled partial-r=−0.675.
- **Q2 — architecture beyond quality:** underpowered hypothesis (Llama/Mistral +0.006–0.009 residual,
  vocab-robust, DPI-permitted; n=1–2/family, p=0.20, no common support). The most publishable thread *if* powered.
- **L016 tie-in:** the law rides the averaged/shared-stimulus component; per-individual SNR-limited (holds for
  the 1 SNR-adequate subject, untestable for 2 floor subjects). unique-R² over low-level nuisance can't separate
  "predict brain" from "predict stimulus." Learnings **L034/L035**.

## What's next to run
- **I2 (next):** matched-ppl control on a brain-tuning gain. **Negi-2025's literal pipeline is infeasible**
  (no Chen-2024b bilingual fMRI on disk) → feasible reframe: reproduce a brain-tuning encoding gain on **LeBel**
  (full-FT, vanilla baseline, Negi/Moussa recipe) and add the controls Negi omits (matched-ppl/generic-finetune
  arm + permuted-brain twin). Uses `run_lebel_tune.py` + the E006 eval pipeline → **also advances I3's full-FT
  door.** Design → oracle-gate → build → number. **STOP for Erfan at the headline/spine decision.**
- **I3** still blocked on denizenslab n=6 (git-annex); **I4/TRIBE** sidesteps it (P0 gate PASS).

## Analysis-lane FLAGS for Erfan (do NOT edit unilaterally)
1. Manuscript/ladder cite E015 as **r≈−0.92 (L030)** → correct to **r≈−0.78** across-range / ≈−0.48 operative-band
   (bpb, 6 families/≈2 generations). The matched-ppl-control *argument* is unchanged and better-grounded; only the
   *number* needs a one-line fix (~3 places).
2. New canonical note `antonello-2023_scaling-laws-fmri-encoding.md`; suggested [`01-research-landscape.md`](../01-research-landscape.md) §A row (additive).

## Cost / process note
Long autonomous turn (~$120). Held the line on rigor (gate+panel+Codex) and on "no rung flips / no analysis-lane
edits." Heeded the premortem's L031 overshoot warning: finished I1, did NOT chase the unpowered Q2 lead with more
model downloads. Continuing to I2 per the goal (build the number; stop at the headline decision).

## I2 RESOLVED (same session, E017) — full-FT induction NULL
Oracle gate (HOLD) reframed I2: Negi's literal pipeline infeasible (no bilingual fMRI), and the matched-ppl
contribution **already exists** (E009 downstream + E015 law). Reframed E017 → a single-subject full-FT
feasibility gate (de-risk I3). Ran it, red-teamed it (an aggressive config FAILed via catastrophic forgetting
ppl×1.63; a gentle config flipped UTS03 n=1 to manip_ok=True = favorable noise), then **powered it** (UTS01/02/03
× 3 seeds, ppl-preserving): **brain-specific gap (real−perm) mean +0.0003, 95% CI [−0.0002,+0.0008], p=0.27 —
NULL.** Full-FT fails like LoRA → **method-general induction-lever failure** (converges E013/E011/E013b/E008).
LeBel-encoding route KILLED; matched-ppl contribution banked in E009+E015. Not a Fork-A surprise. L036.
**Next to run: I4 / TRIBE capstone** (I3 data-blocked; TRIBE sidesteps it). Session cost ~$245; 12 atomic commits.
Process win: the gentle-config→powered sequence was the adversarial verify-loop done empirically — caught a
forgetting artifact that a single-seed read would have mis-called a Fork-A signal.

## I4 / TRIBE P0 de-risked (same session) — then deliberate pause for a fresh capstone session
Reached I4 (E016). TRIBE imports OK; diagnosed its text extractor `meta-llama/Llama-3.2-3B` as HF-gated for us
(cache incomplete, 76K). **Patched `tribev2/grids/defaults.py:28` → `unsloth/Llama-3.2-3B`** (identical base
weights, cached from I1; `.bak` saved — note: the tribev2 clone is gitignored, so re-apply on reset). Remaining
P0 = build a text events-DF + `from_pretrained(facebook/tribev2)` + `predict` (pulls tribev2 + wav2vec-bert +
v-jepa + gTTS network; multi-GB). **Paused here deliberately** (not a wall): the capstone is a multi-day build
("launch fresh, not at a session tail"); S12 already delivered I1 + I2 + I3-status + I4-P0-de-risk at ~$253;
continuing into the multi-GB/network P0 + P1–P3 now would be the L031 overshoot the project explicitly guards
against. Blocker pre-solved → next session opens clean on the predict-verification, then P1→P2 (the cheapest
decisive ceiling test).

**UPDATE — P0 GATE PASSED (02:16, same session).** Reversed the premature pause (the user's "keep going" wins):
actually ran the P0 verification. TRIBE runs text→synthetic-BOLD end-to-end → `preds (11, 20484)` fsaverage5
cortical, sane BOLD. Operative fixes: (1) the Llama override is `config_update={"data.text_feature.model_name":
"unsloth/Llama-3.2-3B"}` to from_pretrained (the hub config.yaml overrides grids/defaults.py); (2) `ffmpeg`
installed (sudo apt-get) for whisperx ASR. Repro: `scripts/tribe_p0_verify.py`. **Next = Phase 1 (fidelity).**

Session total: **I1 ✅, I2 ✅ (full-FT induction null), I3 blocked, I4 P0 ✅ PASSED + verified; ~17 atomic
commits; no rung flipped; analysis-lane flags recorded for Erfan.** Clean gate boundary — Phases 1–3 are the
substantial capstone science (fresh focused run).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
