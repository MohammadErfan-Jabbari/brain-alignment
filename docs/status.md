---
title: "Project status"
tags: [status]
aliases: [current-status]
---

# Project status

**Updated:** 2026-08-30

**Manuscript:** `Section 5 argument repairs applied; prose-swarm residual parked by Erfan`. The 70-page thesis in `docs/manuscript/rewrite/` remains the sole scientific-interpretation authority; `docs/manuscript/submission/` is its university-template derivative. Introduction through Results have completed the reader-first review, and the six blocking Discussion-through-Conclusion [argument findings](manuscript/submission/deferred-review-items.md#6-discussion-through-conclusion-argument-review-hold) are resolved in both trees without changing a scientific verdict or number. Under [D067](decisions/decisions.md) the parent applied 15 corroborated rule-backed normalizations canonical-first (fixed role terms, settled phrasings, register, banned words); the canonical tree, submission twin, and both PDFs are current on `main`. A residual set of judgment-call findings (voice on the two argument-repair sentences, section-as-agent register, referent naming, verdict-verb variation, glosses, E026-dependent checklist names) was collected by the analyst and counter runs but left unadjudicated when Erfan stopped the swarm on 2026-08-31; they remain recoverable from that session's transcripts or a fresh swarm relaunch. Its professor-approved title is *Evaluating Brain Alignment as a Training Signal for Language Models* ([D066](decisions/decisions.md)).

**Legacy layers removed from HEAD (2026-08-25):** the `extended/` legacy snapshot and the frozen public v0.9 cut are preserved only in Git history (last commits: `extended/` at `7c445b0`, `public/v0.9/` at `6026021`). Do not recreate them as directories; cite the commits when historical access is needed.

## Research state

| Rung | State | Owning evidence | Manuscript location (legacy extended numbering) |
| --- | --- | --- | --- |
| Q0 / A2 | CONDITIONAL PASS: trained-model controlled predictivity is supported under the executed assays; E002's learned-parameter attribution from the trained-minus-untrained gap is unresolved because the static nuisance block was model-specific; no E006 participant/population inference | [E002](experiments/E002_tuckute-encoding-feasibility.md), [E006](experiments/E006_lebel-voxelwise-feasibility.md) | Methods; Results §4.1 |
| Q1 | PARTIAL: plain KD shows alignment headroom, but KD-specific shedding is not isolated from LM quality | [E003](experiments/E003_kd-alignment-preservation.md) | Results §4.2 |
| Q2 | NO DEMONSTRATED INTERVENTION EFFECT at the valid inference unit; small effects are not ruled out | [E004](experiments/E004_brain-loss-lever-test.md) | Results §4.3 |
| Q3 | NO DEMONSTRATED PARTICIPANT-GENERAL GAIN across tested ROI/objective variants; E025's direct TRIBE-minus-KD contrast is near zero. Its preregistered relative upper bound falls below the internal `+0.002` continuation threshold, but E026 shows that the saved cross-target comparator fails pre-outcome and KD-baseline comparability, so the relative contrast is not content-identifying. E030's 50-component linear target-projection assay does not meet its internal continuation rule: aligned TRIBE above nuisance is `-0.004494`, with family-95% upper endpoint `+0.001707 < +0.002`; the frozen-twin contrast remains unresolved | [E008](experiments/E008_per-participant-f1-solidification.md), [E011](experiments/E011_strong-regime-per-individual.md), [E013](experiments/E013_open-frontier-multisubject-naturalistic.md), [E025](experiments/E025_participant-e016-biological-transfer.md), [E026](experiments/E026_tribe-textfeat-target-comparability.md), [E030](experiments/E030_exact-substrate-transport-diagnostic.md) | Results §4.4 and §4.6 through E030 |
| Q4 / A3 | PRACTICAL UTILITY NOT DEMONSTRATED: the controlled-predictivity prerequisite was seed-unstable and the downstream utility contrasts remain descriptive; the observed MDE is a sensitivity quantity, not a null or equivalence test; gaze privileged-information substrate failed its preconditions | [E009](experiments/E009_a3-practical-payoff.md), [E024](experiments/E024_zuco-lupi-sample-efficiency.md) | Results §4.7; Discussion |
| Q5 | NOT STARTED and currently moot because it depends on a Q3 benefit | No active E record | Deliberately excluded |

## Active work

- New experiment development is closed by Erfan's direction ([D065](decisions/decisions.md), 2026-08-25). The prospective program below (E033, E032, E028 exact-lane resolution, queued dimensionality work) is paused, not executed, unless Erfan reopens it. The university-template derivative exists; the immediate task is resolving the six argument-review findings before the Section-5 prose swarm.
- E033 remains design-locked but inactive under D065. Its prospective L12-versus-final-hidden recorded-response placement test has not opened an outcome and has no compute license unless Erfan reopens development.
- Erfan's reader-first review is complete through Results. The rewrite distinguishes claim-specific dependencies, uses explicit Methods and appendix handoffs, and applies the fixed brain-response terminology and central `acronyms.tex` registry throughout. Discussion through Conclusion now have a bounded argument-review hold before their prose passes.
- The rewrite manuscript is the canonical thesis and current scientific-interpretation authority. All future manuscript writing, checks, builds, and supervisor-facing exports use `docs/manuscript/rewrite/`. The legacy extended manuscript and frozen public v0.9 cut are Git-history-only layers (see the manuscript note above).
- E025 is complete and result-oracle clean. All language-quality, target-learning, and representation-movement gates passed. The direct TRIBE-minus-KD mean is `-0.000014`, CI95 `[-0.000739,+0.000711]`. The preregistered participant-first relative contrast is `+0.000136`, CI95 `[-0.000505,+0.000777]`, with one-sided UCB `+0.000653 < +0.002`; this relative estimand does not identify content after E026. UID 837 carries the sole clear participant positive in both views.
- E026 is complete and independently audited. In the corrected identification set, 16/37 checks fail, 20 pass, and one is unresolved. The decisive mismatches are KD baseline/headroom, covariance spectrum/effective rank, and low-level nuisance predictability. Separately, 14/18 post-training diagnostic margins depart and four remain within margin; these outcomes describe the realized interventions but do not determine comparator identification. The raw cross-target difference remains non-identifying without invalidating TRIBE's within-target learnability or E025's direct TRIBE-minus-KD contrast.
- E030 is complete, author-confirmed, independently recomputed, and synchronized into the canonical rewrite manuscript. All `270/360/6,480` C1/C2/C3 rows, `748` independently recomputed load-bearing leaves, and the full provenance chain are panel-clean. The target is strongly extractable from TRIBE students (`M=+0.040725`, family-95% CI `[+0.039053,+0.042398]`), but its aligned unique participant predictivity above nuisances fails first. The frozen-twin contrast, incremental retention over KD, and all bridge contrasts remain unresolved. No post-outcome E030 variant is licensed.
- E031 is complete and independently audited. C1 is `NO CONSENSUS INCREMENT`: the residualized consensus target has fixed-cohort predictivity `+0.004379`, but its improvement over uniform averaging is `+0.000936`, below the frozen `+0.002` gate. C2 is `BUILDER INSTRUMENT FLOOR`: \(R_{\mathrm{builder}}=0.000116<0.01\), so its five independent evaluation repeats remained sealed. These classifications reject the frozen consensus-weighting and whole-cortex-median linear instruments, not denoising in general. No target-gradient, repeat-aware LeBel, or student-training license was issued. The load-bearing values and classifications are audit-clean; Erfan's confirmation remains required before manuscript synchronization.
- H002 and E032 now define the next prospective information-recovery test. E032 freezes a one-component, shrinkage-regularized CorrCA filter on Kymata English participant E2, with builder runs 1 and 3, evaluation runs 2 and 4, MEG gradiometers primary, EEG secondary, PCA-1 and shifted controls, and builder-only decisions. Live metadata support four runs and eight exposures for E2 but expose an event-duration contradiction, an English machine/calibration contradiction, 64 rather than 70 EEG channels, and a CC BY 4.0 versus CC0 license mismatch. Raw-header, `STI101`, complete-window, channel, and calibration checks therefore precede every neural score. The exact acquisition-integrity slice compiles, passes 14 synthetic tests, and is independently `PANEL-CLEAN`; participant neural FIF values remain unopened and authorization is false. Builder, score, and analysis stages remain deliberately unimplemented, so E032 is not endpoint-ready.
- The prospective dimensionality experiment remains queued behind the current biological-information design and manuscript review. Its estimand, controls, inference, and anti-confound contract remain unchanged and no compute is licensed.
- The working conference route remains a focused methodological/falsification paper built around source-target validity, target uptake, student movement, control identification, biological transfer, and utility. E028 is the primary external gate; a controlled reproduction of Xiao et al. 2026 is the lower-dependency feasibility backup. A theory-first route remains HOLD, and the positive-mechanism route is closed.
- The [E028 author-artifact request](references/e028-vaidya-artifact-request-email.md) was sent on 2026-07-22 to the corresponding author with both coauthors copied. The first response checkpoint is 2026-08-05; one concise follow-up is permitted, and 2026-08-12 is the exact-lane decision checkpoint. Silence means exact reproduction is unavailable, not that the reported result failed.
- E028's outcome-blind synthetic Stage-1 corrected-evaluator slice is implemented and independently panel-clean. Two 108-cell replays were byte-identical; schema, support, nuisance-sharing, pooled aggregation, exact sign-flip inversion, sentinels, and adversarial fixtures passed. The deliberately positive synthetic branch passed while `stage2_licensed=false` and `ready_for_endpoint_access=false`. This is plumbing evidence only. The production provider, RFC 8785 chain, factual dimensions, production-shape benchmark, exact lane, and endpoint-bundle review remain absent.
- The package strategy is recorded in [D057](decisions/decisions.md) and traces to the non-authoritative [initial Pro audit](external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md) and [corrected Pro audit](external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md).

## Conference packages

| Package | Identity | State | Next gate |
| --- | --- | --- | --- |
| A | Methodological/falsification protocol | **Strengthened default route; internal dissociation complete, external gate missing** | Run a 10-business-day E028 access/executable feasibility gate in parallel with a smallest-setting Xiao reproduction design; choose the external lane before expensive compute |
| B | Conditional theoretical boundary | **HOLD** | Generic theorems are occupied; proceed only if an observable directional certificate prospectively predicts both failure and success regimes |
| C | Positive brain-guided mechanism | **Closed; E025 continuation rule failed** | No E027: E025 failed the conjunctive participant-positive continuation rule, and direct TRIBE-minus-KD is near zero for this cohort |

## Blockers

- No scientific-evidence or argument-review blocker remains. The Section 5 prose swarm is parked by Erfan's 2026-08-31 stop after four fail-loud infrastructure stops (GLM output-cap deaths; OpenAI-Codex usage limit; kimi-coding weekly quota; counter output-format drift, since fixed by the v3.4 gate hardening). The openai-codex models are removed from routing; kimi is served by ollama-cloud/kimi-k3 when the swarm is next used. Creating a new immutable public cut remains a separate decision requiring Erfan's approval.
- E028's exact lane remains blocked by author-controlled code, checkpoints, masks/folds, dataset facts, and result-regeneration artifacts. Its synthetic Stage-1 development slice is implemented, tested, and independently `PANEL-CLEAN`, but the production provider/chain/dimension benchmark and sealed endpoint-bundle review are absent; `ENDPOINT-READY: NO` remains unchanged.
- A top-AI-conference claim is not currently supported. It requires a non-inconclusive prospective external adjudication and a reusable intervention-audit implementation; the unchanged thesis should not consume a top-tier main-track cycle.

## Next actions

1. On Erfan's direction, finish the Section 5 residual prose findings — relaunch the hardened v3.4 swarm (`node .claude/scripts/section_swarm.js 5`, DeepSeek + Ollama Kimi K3) or adjudicate the recorded judgment calls directly — then run the Limitations and Conclusion swarms, then close the deferred abstract and figure/typography passes.
2. Rebuild the university-template derivative and send it to the supervisors without adding results from the closed experiment program.
3. After supervisor feedback, decide whether to create a new immutable public cut.

Former experiment next actions (E033 implementation, E031 confirmation with E032 authorization, E028 lane resolution) are closed under D065 unless Erfan reopens them.

## Related

- [Methodology and authority contract](03-methodology.md)
- [Canonical thesis source](manuscript/rewrite/main-rewrite.tex)
- [D057 conference package decision](decisions/decisions.md)
