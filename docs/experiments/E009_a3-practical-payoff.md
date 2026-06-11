# Experiment — E009 (A3 / L2b): does brain-alignment buy anything PRACTICAL at matched perplexity?

**Created:** 2026-06-11 · **Status:** DESIGN DRAFT (gate with oracle AFTER E008's verdict — the verdict shapes the framing) · **Mode:** working
**Direction:** L2b / A3 — the ladder's "real thesis risk" (the untested assumption) and the genuine open gap. The escape from the Tuckute stimulus-fold power ceiling (A3 is measured on downstream NLP, not fMRI stimuli — so it is not capped at ~5 folds).
**Predecessors:** `E005` (in-domain F1, small/borderline — L015) · `E008` (per-participant solidification — its verdict sets whether we say "a brain-specific signal we induced" or "a tiny signal") · lit-scout A3 sweep (S8)
**Output:** `outputs/E009_a3_*.json`

---

## The question (the one a reviewer actually asks)

> Take two students distilled to **matched perplexity** — one with the brain-alignment objective
> (`kd_brain`), one without (`kd_ppl`) — plus the brain-specificity null (`kd_brain_permuted`). Does
> `kd_brain` **generalize better, more robustly, or more sample-efficiently** on downstream language
> tasks than `kd_ppl`, and is any such gain **brain-specific** (beats the permuted twin)? Or do the
> gains stay **confined to the alignment metric** (the predeclared kill — Fork-B-honest)?

This is A3, the untested assumption every precedent skipped or under-controlled. It does not depend on
the in-domain effect being large — it asks whether *whatever* representational change the brain term
induces has downstream value.

## Why this is the gap (grounded in the S8 lit-scout)

- **Negi et al. 2025 (NeurIPS):** brain-tuning improves multilingual downstream NLP — BUT baseline =
  vanilla pretrained, **NOT perplexity-matched**, and no compression. We add the matched-ppl + permuted
  controls and the compression frame. (The positive prior art to outdo in rigor.)
- **Schwartz/Toneva/Wehbe 2019:** founding "no harm + modest gains," weak control (no matched-ppl).
- **pirlot-2022 (in canon):** a brain-RSA regularizer's *accuracy* gain was reproduced by a **shuffled-label
  control** — only the **robustness** gain needed real neural structure. → **primary outcome = robustness/OOD,
  not accuracy**, and the permuted-brain twin is the load-bearing control.
- **Hoak et al. 2025:** *aggregate* alignment does NOT predict robustness; *feature-specific* alignment does.
  → don't claim robustness from a gross brain-score bump; tie it to the specific representational change.
- **Guo et al. 2024 (EEG):** brain-co-training robustness gains are "limited but consistent" → predeclare a
  small MDE and a power analysis; expect a small effect (consistent with our A+B framing).

## Arms (reuse the E005/E008 KD students — no new tuning needed for the first pass)

| Student | From | Role |
|---|---|---|
| `kd_brain` (mse, λ=10) | E005/E008 | the brain-tuned student |
| `kd_ppl` (lm_only) | E005/E008 | matched-perplexity baseline (the L011 control) |
| `kd_brain_permuted` (mse_perm) | E005/E008 | brain-specificity null (matched-ppl by construction) |
| base Qwen2.5-0.5B (untuned) | — | reference |

**Caveat to resolve at gate:** the E005/E008 students are LoRA-tuned on ~800 Tuckute sentences (a *light*
touch; ppl 55 vs base 45). A downstream signal from so light a touch may be nil — in which case A3 needs a
*more substantial* brain-tuning regime (more data / higher λ / full schedule) to give the effect a chance.
The first pass tests the existing students; if null, escalate the tuning before concluding (predeclare this).

## Outcomes (PRIMARY = robustness/OOD; predeclared)

1. **OOD / robustness (primary, per pirlot/Hoak):** zero-shot perplexity or task accuracy under
   distribution shift / input perturbation (e.g. a held-out-domain corpus; character/word noise;
   syntactic perturbation). Metric: `kd_brain − kd_ppl` AND `kd_brain − kd_brain_permuted`.
2. **Sample-efficiency (secondary):** few-shot fine-tune each student on a small downstream task; does
   `kd_brain` reach a target metric with fewer examples (area-under-the-learning-curve)?
3. **In-distribution accuracy (tertiary, expected null per pirlot):** standard task accuracy — predeclared
   to likely show nothing brain-specific; reported for completeness, not as the headline.

## Claim tuple / decision rule (PREDECLARED — to finalize at oracle gate)

- **Metric:** paired `kd_brain − kd_brain_permuted` (brain-specific) and `kd_brain − kd_ppl` (beyond-LM) on
  the PRIMARY robustness/OOD outcome, bootstrap CI over seeds × tasks; ≥3 seeds.
- **A3 CONFIRMED:** `kd_brain` beats the permuted twin on robustness/OOD, CI excludes 0, brain-specifically,
  at matched perplexity. → preserving/inducing alignment buys practical robustness — the thesis's "so what."
- **A3 NULL (the honest Fork-B kill):** gains confined to the alignment metric (no robustness/OOD/sample-eff
  difference beyond the permuted twin). → "brain-alignment, at this scale, does not buy downstream value" —
  a clean, publishable negative that closes the assumption the field left open.
- **Controls:** matched perplexity (report per student); permuted-brain twin (brain-specificity); base
  reference; ≥3 seeds.
- **Predeclared MDE = 2–4pp** absolute robustness (grounded: Guo 2024 saw ~4pp mean / 8pp max in vision-EEG;
  language/fMRI is noisier → expect the low end; predeclare so a small effect isn't over-read and a null
  is honestly power-bounded).
- **The contribution, made explicit (grounded by the S8 digests):** *every* A3 prior lacks the two controls
  we add. Negi 2025 (closest positive) baselines against vanilla pretrained — no matched-ppl, no shuffled-brain
  downstream null. Schwartz 2019 claims only "does not harm," no controls. Guo 2024 ran shuffled controls but
  never quantified the brain-specific increment. → **our novelty is the matched-perplexity + permuted-brain
  paired contrast** (is the downstream gain brain-specific and not just "a different/better LM?"), the same
  confound-clean design that carried E005/E008.

## Open questions (resolve at oracle gate)

- **Which offline benchmark?** Needs to run with cached models, no network. Candidates: a held-out-domain
  perplexity OOD test (cheapest, reuses the ppl harness); a small GLUE-style task via few-shot; a
  perturbation-robustness probe. Pick the one that is (a) offline-runnable and (b) sensitive to a ~0.5B
  representational change. (Likely start with OOD perplexity robustness — closest to our existing harness.)
- **Light-touch students vs a stronger brain-tuning regime** (see Arms caveat) — predeclare the escalation.
- **Does A3 even need E008 to pass?** No — A3 is informative either way. But E008's verdict frames it
  ("we induced a brain-specific signal; does it transfer to utility?" vs "the signal is tiny; does any
  downstream value survive?").

## Status

DESIGN DRAFT — written during the E008 run. **Gate with oracle-reviewer after E008's verdict**, then build
the offline robustness harness, then run + thinking panel. This is the candidate next headline (the
practical-payoff gap), pending E008.
