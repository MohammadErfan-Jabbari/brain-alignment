---
title: "Experiment — E009 (A3 / Q4): does brain-alignment buy anything PRACTICAL at matched perplexity?"
tags: [experiment]
aliases: [E009]
---

# Experiment — E009 (A3 / Q4): does brain-alignment buy anything PRACTICAL at matched perplexity?

**Created:** 2026-06-11 · **Status:** COMPLETE (ran 2026-06-11) — A3 bounded NULL, null-by-construction (n=8; no brain-specific OOD-ppl payoff; the matched-ppl fulcrum is itself ~0; L017) · **Mode:** working
**Direction:** Q4 / A3 — the ladder's "real thesis risk" (the untested assumption) and the genuine open gap. The escape from the Tuckute stimulus-fold power ceiling (A3 is measured on downstream NLP, not fMRI stimuli — so it is not capped at ~5 folds).
**Predecessors:** [`E005`](E005_alignment-guided-kd-tradeoff.md) (in-domain F1, small/borderline — L015) · [`E008`](E008_per-participant-f1-solidification.md) (per-participant solidification — its verdict sets whether we say "a brain-specific signal we induced" or "a tiny signal") · lit-scout A3 sweep (S8)
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

- **[Negi et al. 2025](../literature/canonical/negi-2025_brain-informed-finetuning-multilingual.md) (NeurIPS):** brain-tuning improves multilingual downstream NLP — BUT baseline =
  vanilla pretrained, **NOT perplexity-matched**, and no compression. We add the matched-ppl + permuted
  controls and the compression frame. (The positive prior art to outdo in rigor.)
- **Schwartz/Toneva/Wehbe 2019:** founding "no harm + modest gains," weak control (no matched-ppl).
- **pirlot-2022 (in canon):** a brain-RSA regularizer's *accuracy* gain was reproduced by a **shuffled-label
  control** — only the **robustness** gain needed real neural structure. → **primary outcome = robustness/OOD,
  not accuracy**, and the permuted-brain twin is the load-bearing control.
- **Hoak et al. 2025:** *aggregate* alignment does NOT predict robustness; *feature-specific* alignment does.
  → don't claim robustness from a gross brain-score bump; tie it to the specific representational change.
- **[Guo et al. 2024](../literature/canonical/guo-2024_eeg-cotrain-adversarial-robustness.md) (EEG):** brain-co-training robustness gains are "limited but consistent" → predeclare a
  small MDE and a power analysis; expect a small effect (consistent with our A+B framing).

## Arms (reuse the E005/E008 KD students — no new tuning needed for the first pass)

| Student | From | Role |
|---|---|---|
| `kd_brain` (mse, λ=10) | E005/E008 | the brain-tuned student |
| `kd_ppl` (lm_only) | E005/E008 | matched-perplexity baseline (the L011 control) |
| `kd_brain_permuted` (mse_perm) | E005/E008 | brain-specificity null (matched-ppl by construction) |
| base Qwen2.5-0.5B (untuned) | — | reference |

**E008-informed refinement (load-bearing):** E008 showed the *per-subject* brain-specific representational
change is ~0. Testing the downstream value of a ~0 change is uninformative. So A3 must brain-tune toward the
**group-averaged target** — the setting where there IS a measurable representational change (+0.008, the
shared stimulus-evoked component) — and ask whether *that* change buys downstream value, vs `kd_ppl`
(matched-ppl) and `kd_brain_permuted` (brain-specificity). If even the averaged-target change buys nothing
downstream → the clean Fork-B negative. Testing only the light-touch per-subject students would be a null
by construction.

**Caveat to resolve at gate:** the E005/E008 students are LoRA-tuned on ~800 Tuckute sentences (a *light*
touch; ppl 55 vs base 45). A downstream signal from so light a touch may be nil even on the averaged target
— in which case A3 needs a *more substantial* brain-tuning regime (more data / higher λ / full schedule) to
give the effect a chance. Predeclare the escalation; a null on a non-moving model is uninformative.

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
  downstream null. [Schwartz 2019](../literature/canonical/schwartz-2019_inducing-brain-relevant-bias.md) claims only "does not harm," no controls. Guo 2024 ran shuffled controls but
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

## Oracle HOLD → resolution (2026-06-11, fable) — 4 gaps closed in the design; PASS-ready as a PILOT-FIRST plan

The oracle HOLD was correct on all four points. The design now mandates:

1. **No saved students exist** (`run_brain_lever.py` does `del m`; the per-fold students are unusable downstream).
   → A3 needs a **new all-data, save-checkpoint training mode**: tune on all ~800 Tuckute sentences (no fold
   split, averaged target), `merge_and_unload`, save the merged checkpoint per arm × seed.
2. **MDE must be MEASURED, not borrowed.** Guo's 2–4pp is a *prior expectation*, not the predeclared MDE
   (using it would be the borrowed-number move L012/L015 forbid). → a **variance pilot** measures the
   seed-to-seed (and corpus-to-corpus) SD of the actual chosen benchmark → the real MDE → THEN lock the claim.
3. **Quantify the achievable brain-specific Δ at matched ppl FIRST** (a λ-sweep + representational probe).
   If the brain-specific increment is capped at ≈+0.008 and can't grow without breaking the ppl match, A3 may
   be null-by-construction — check the fulcrum before pulling the lever.
4. **Add a text-feature pseudo-target control arm** (regress toward a target predicted from
   surprisal+imageability+length, or static-embedding features). Averaged-target + permuted-twin only tests
   structure-vs-shuffle; this arm separates "brain-derived" from "any smooth text-correlated regressor"
   (the pirlot-2022 redux risk + the L011/L012 unsubtracted-nuisance confound).

**Offline benchmark (no network at run time):** PRIMARY = **OOD-perplexity ratio** (KD/train domain
WikiText-103 → shifted domains we have offline: LeBel TextGrid transcripts (strongest shift), Pereira/Tuckute
sentences); report OOD/in-domain ppl *ratio* so the arms' absolute-ppl differences don't confound.
SECONDARY = perturbation-robustness slope (Δppl per unit char/word noise). **DROP sample-efficiency v1** (no
GLUE/task cached). **Honest limitation (state up front):** offline forces perplexity-based outcomes — a weak
operationalization of "practical payoff"; Hoak 2025 (aggregate alignment doesn't predict robustness) is a
headwind. A clean null is the anticipated, publishable Fork-B result.

**→KILL A3 if:** the matched-ppl λ-sweep shows the brain-specific Δ can't exceed ≈+0.008 AND the downstream
primary is flat across that range within the *measured* MDE; OR any kd_brain−kd_ppl gain is fully reproduced
by the permuted twin / text-feature control (generic multi-task regularization, not brain value). Either is
the clean Fork-B negative — KILLing A3 does not KILL the thesis (A2-powered + two well-powered nulls + the
anti-confound methodology stand).

## Results — A3 pilot (ran 2026-06-11; all-data avg-target KD, 4 arms; pilot n=3 then powered n=8)

**Powered run (`outputs/E009_a3_powered.json`, 8 seeds, λ=10), panel-adjudicated:**

| arm | ppl_id | held-out uR² | OODr Pereira | OODr LeBel |
|---|---|---|---|---|
| lm_only (kd_ppl) | 51.5 | +0.0030 | 0.567 | 1.835 |
| **mse (kd_brain)** | 58.1 | +0.0173 | 0.576 | 1.887 |
| mse_perm (null) | 56.4 | +0.0063 | 0.594 | 1.955 |
| textfeat (control) | 54.3 | +0.0021 | 0.572 | 1.843 |

- **(a) The fulcrum is ~0.** Brain-specific repr gap (mse − mse_perm) = mean +0.011 but **median +0.0042, 5/8 seeds positive, MDE80 0.023 ≈ the mean → within noise**. Per-seed gap [+0.063, +0.014, +0.004, +0.016, +0.005, −0.006, −0.002, −0.005] — **seed-0 (+0.063) is the lone outlier; the other 7 average +0.004** (the L015/L016 outlier pathology, third occurrence). **A reliable brain-specific representational change at matched perplexity does not take hold at this scale.** λ=30 (pilot) couldn't grow it without collapsing ppl (53→92, one seed 148).
- **(d) No brain-specific downstream effect.** At n=8 every OOD contrast is within the measured MDE: mse − lm_only Pereira +0.009 / LeBel +0.053 (both ~equal); mse − mse_perm −0.019 / −0.068 (~equal); mse − textfeat +0.004 / +0.044 (~equal). The n=3 "mse worse than lm_only" was noise.

## Verdict: **A3 = bounded NULL (robustly characterized)** — practical payoff undemonstrated; the prerequisite fulcrum is itself ~0 at matched ppl (L017)

No brain-specific practical (OOD-perplexity) payoff, AND no reliable brain-specific representational change to test the payoff of — the manipulation doesn't take hold at matched perplexity at this scale (ties to E008/L016). Two-panel-adjudicated (counter-argument: "the fulcrum is broken, not just the downstream"; premortem: "null-by-construction — don't run a fuller A3 on a non-moving model; elevate L016 as the positive contribution instead"). **Stated limitations (honest, not hidden):** OOD-perplexity is a weak proxy (offline constraint); the perturbation-robustness slope + sample-efficiency axes were **not** run (with the fulcrum ~0, downstream tests are uninformative — a redesign that first induces a reliable brain-specific change would be needed, which the matched-ppl constraint + ~800 paired sentences + 0.5B scale structurally block); single student/teacher. **Negi 2025 reconciliation:** their positive downstream gains baseline against a *non-perplexity-matched* vanilla model — the L011 LM-quality confound our matched-ppl + permuted-twin control removes; our null is the brain-*specific* increment at matched ppl.

## Status — A3 line complete (bounded null); experimental ladder essentially complete

A3 recorded (bounded null). The thesis is **Fork B, complete**: A2 (real & powered) + **L016 the positive methodological contribution** (averaging manufactures apparent brain-specificity + the confound-clean protocol) + the well-powered per-subject F1 null (E008) + this A3 bounded null. **Next is a mode change → write-up** (or, if a per-individual positive is wanted, new higher-SNR data: within-subject fMRI repeats — not more averaging). Erfan's call.

---

### (superseded) original pilot-first plan
**Next step (the "run A3" Erfan confirmed): the all-data-students + variance pilot** — build the save-checkpoint training mode + OOD-ppl
harness + text-feature control arm, run the 3–5-seed pilot to (a) confirm the brain-specific gap is nonzero
in all-data students, (b) measure the real MDE, (c) λ-sweep the max brain-specific Δ at matched ppl. That
pilot green-lights or cheaply kills the full A3. (Deferred to next session per the S8 close — a fresh
multi-hour harness build is its own unit, not a tail-of-session rush; fully specified above.)


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
