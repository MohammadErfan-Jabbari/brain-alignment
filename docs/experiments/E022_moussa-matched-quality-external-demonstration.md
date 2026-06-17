# Experiment E022 — Moussa brain-tuning, matched-quality external demonstration (Path-A)

**Created:** 2026-06-17 (S22) · **Status:** PILOT running (oracle HOLD on the full design; pilot-gate first)
**Tree:** TA.4 (Path-A external demonstration) · **Program:** `../expansion-program.md` §6b · **Mode:** promotable (if it clears the gates)

## Objective
Show that Moussa & Toneva's reported **brain-specific downstream gain** (phoneme-F1 / sentence-type-F1 from fMRI brain-tuning of a speech-LM) shrinks once compared against a **quality-matched non-brain twin** + a **permuted-brain twin**, rather than against the un-tuned pretrained baseline they use — i.e. the literature's brain-guided-training gains are quality-confounded. This is the external "main-track lift" for the Path-A negative paper.

## Oracle pre-compute review (S22) → HOLD; must-fixes (all to be honored before the full run)
The full design as built (`scripts/run_moussa_arms.py`) would reach "the gain shrinks" for reasons unrelated to the thesis. Must-fixes:
- **F1 — matched-quality must be OFF-METRIC.** Match the non-brain twin to the brain arm on an *independent* axis (held-out SSL validation loss; secondary: WER), NOT on the contested phoneme-F1 (matching on the test metric rigs the null by construction). Read phoneme-F1 / sent-type-F1 as outcomes downstream of the matched axis.
- **F2 — learnability-disruption confound (the E021 lesson).** Brain L2-regression (73M-param head) vs SSL contrastive differ in scale/learnability/trainable-params; the permuted arm controls fMRI *content*, not brain-vs-SSL learnability. Require a per-arm **trunk-drift readout (CKA vs pretrained)** + match trainable-param count or report the asymmetry.
- **F3 — reproduction-first gate + a pretrained baseline arm** (the harness lacked one). Predeclare: brain-tuned must beat pretrained by **≥+2 phoneme-F1, CI excluding 0, ≥3 seeds**, or the shrink-test is vacuous.
- **Confirmed defects:** synthetic TRFiles (regular 0,2,4,6,8 spacing — may inflate brain-target learnability); single-subject UTS03 (NOT the multi-participant headline — scope the claim honestly); single seed → ≥3; **checkpoint-init mismatch** (brain arm from ASR-fine-tuned `wav2vec2-base-960h`, twin from pretrain `wav2vec2-base` — bakes in an ASR head-start → start all arms from the same init); **TIMIT missing** (hard blocker — acquire first).
- **F4 — strategic:** Moussa's headline is generalization/efficiency, not a raw downstream gain; single-subject speech from a text-LM thesis = Findings-tier on the wrong substrate. Tens of GPU-hours is a large bet — de-risk with the pilot before committing.

## The gate sequence
1. **PILOT (running, ~6–10 GPU-hr):** two arms only — pretrained vs brain-tuned, SAME init (`wav2vec2-base`), TIMIT acquired, ≥3 seeds. Decision: does brain-tuning reproduce **≥+2 phoneme-F1 over pretrained** (CI excludes 0)? → `outputs/e022/`.
   - **REPRODUCES →** build the off-metric matched-SSL-loss twin + permuted + trunk-drift (CKA) + ≥3 seeds → the full shrink-test. (Flag the F4 cost to Erfan before the big run.)
   - **NON-REPRODUCTION →** the shrink-test is vacuous; record "Moussa's gain doesn't reproduce on our data scale/timing" as the Path-A finding; STOP.
2. **Full shrink-test (only if pilot reproduces):** brain vs matched-SSL-loss twin vs permuted, trunk-drift reported. Thesis-supporting outcome = brain−pretrained CI excludes 0 AND brain−twin CI includes 0 (shrinks to non-significant) at matched SSL loss.

## Iteration log
| Date | Run | Result | Verdict | Next |
|---|---|---|---|---|
| 2026-06-17 | design + oracle | HOLD (F1 circular, F2 learnability, F3 vacuity, checkpoint/TIMIT/seed/subject defects) | gate with a pilot first | run pilot |
| 2026-06-17 | PILOT | _running_ | _pending_ | — |

## Results / Interpretation
_pending the pilot._
