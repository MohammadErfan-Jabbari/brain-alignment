# Experiment — E019: reproduce a PUBLISHED brain-tuning positive, then collapse it with the matched-ppl + permuted-twin control

**Created:** 2026-06-13 · **Status:** PLANNED (forward program; design to be oracle-gated before compute) · **Mode:** working
**Roadmap:** the **external-validity demonstration** — the "100% version" of I2 (Erfan's complete-work rule). The premortem (S12 swarm) flagged this as **NON-NEGOTIABLE for the paper to survive review**: our matched-ppl contribution is currently demonstrated only on our OWN nulls (E009/E017); a top-venue reviewer will demand we apply the control to a *published positive* and show what it costs.

## The question
> Take a published brain-tuning result that reports a downstream/encoding GAIN vs a vanilla baseline (Bilgin-2026 ICLR; Negi-2025 NeurIPS; Moussa-2025; or Schwartz-2019). **Reproduce their gain under their original (uncontrolled) conditions**, then **add the controls they omit** — a perplexity-matched fine-tune arm + a permuted-brain twin — and measure how much of the gain survives. Predicted (from E015's r≈−0.78 law + our nulls): the gain **shrinks toward / into the matched-ppl + permuted band** → the published positive is largely an LM-quality / fine-tuning-step effect, not brain-specific.

## Why this is the load-bearing external demonstration (not redundant with E009/E017)
- E009/E017 are OUR nulls on OUR pipeline — they show the control *produces* a null, but not that an *existing published positive* would *vanish* under it. The counterfactual "Bilgin/Negi would be null at matched ppl" is currently an **inference**, not a measurement (counter-argument + premortem, S12). E019 converts "we have a better protocol" → "here is what the protocol costs the prior literature."
- It directly engages the field's live positives: **Bilgin-2026 (ICLR)** brain-informed training beats text-only baselines (no permuted/matched-ppl control); **Negi-2025 (NeurIPS)** bilingual brain-tuning downstream gains (vanilla baseline only). Both confirmed (canonical notes) to lack the matched-ppl + downstream-permuted control.

## Design sketch (to be locked + oracle-gated)
1. **Pick the target** by feasibility: literal pipeline (Negi bilingual fMRI = infeasible, no data) vs. a recipe reproducible on data we HAVE (LeBel + **denizenslab n=6, now downloaded** — 6 subjects, reading+listening naturalistic). Leading candidate: a **Bilgin/Moussa-style full-FT brain-tuning recipe on denizenslab/LeBel**, evaluated their way (vanilla baseline, their split convention) to **reproduce the qualitative positive**, then re-evaluated under our controls.
2. **Arms (≥3 seeds, per-subject inference):** (a) vanilla baseline; (b) brain-tuned (their recipe) — the reproduced gain; (c) **perplexity-matched generic-text fine-tune** (matched by construction — anchor/early-stop to the brain arm's held-out ppl); (d) **permuted-brain twin**.
3. **Outcome:** the gain (b−a) and how much survives the controls — (b−c) at matched ppl, and (b−d) brain-specificity. Anti-confound: contiguous/story splits, nuisance subtraction, the bpb quality axis (L034/D023). 
4. **Predeclared readings:** gain collapses to within the matched-ppl + permuted band → **the field's positive is a quality/fine-tuning artifact** (the paper's external-validity clincher). Gain SURVIVES matched-ppl + permuted (CI excludes the control band) → a **genuine brain-specific training effect at scale** → Fork-A-qualifying → STOP for Erfan.

## Open risks (pre-flag for the oracle gate)
- **Reproducing their positive may itself fail** (our E017 full-FT gave null even before controls). If we can't reproduce the gain even under their loose conditions, the honest finding is "the published positive is method-fragile / doesn't replicate under careful eval" — weaker but still publishable; the cleaner demonstration needs us to first *match their result* under *their* conditions, then break it with the controls. The design must replicate their exact (uncontrolled) protocol to get the positive, not our rigorous one.
- **Whose result + which data** is a feasibility-driven choice (Negi data unavailable). Headline framing (does E019 become the paper's spine) = **Erfan's call when the number lands.**

**Status: PLANNED.** Sequence (forward program): after the TRIBE Phase 1/2 ceiling (E016) — or in parallel if compute allows. No rung flips without Erfan; numbers come only from recorded runs.

---

## v2 — LOCKED design (S14, 2026-06-14, grounded in the canonical notes + our data/infra). Oracle-gate before compute.

**Target chosen by feasibility (first-principles design-grounding, S14):** a **Negi-2025-style text-LM brain-tuning
recipe, run on denizenslab listening fMRI** (6 real subjects 01/02/03/05/07/08; 04/06/09 are 64-byte annex stubs).
Negi is the only candidate that is simultaneously (a) a **text LM** (our thesis target + our infra), (b) on **data we
physically have** (denizenslab = the Deniz-2019 monolingual set Negi themselves use as a control arm), and (c)
**already coded** (`brain_loss.py` has NT-Xent = Negi's `contrastive`; `run_lebel_tune.py` has the real-vs-permuted
twin + KD-ppl-anchor + per-subject + seeds; `run_eys_ceiling.py` has the denizenslab loader). Bilgin (CNeuroMod
Friends), Schwartz (Harry Potter), Freteault (Friends audio CNN) need datasets **not on disk**; Negi's bilingual
headline needs bilingual fMRI **we lack**. **Honest framing:** we reproduce Negi's *monolingual* brain-tuning
**encoding** gain (the loss/architecture they validate, on the monolingual fMRI they use as a control), NOT their
cross-lingual headline. Fair published-positive recipe, not a strawman.

**THE LOAD-BEARING ESTIMAND INSIGHT.** Negi's positive is an **encoding Δr gain vs VANILLA** (tuned−vanilla, ppl
left to drift; their Δr up to ≈0.15) — a *different, easier* contrast than the **brain-specific (real−permuted) gap**
that our E017 full-FT NULLED (L036). The (tuned−vanilla) gain SHOULD reproduce because *any* fine-tune moves the
features and changes ridge-encoding r — that is exactly the confound. So **arm (b) must reproduce the gain WITHOUT a
KD anchor** (let ppl drift, as Negi did); if the gate forces matched-ppl into arm (b) there is nothing to break.
Primary outcome = **held-out encoding Δr** (the metric where Negi's positive lives), NOT downstream (which E017-class
nulls say won't reproduce — do not lead with it).

**Negi's exact uncontrolled protocol (to replicate to GET the positive):** full fine-tune (all layers + projection),
objective **NT-Xent contrastive** between predicted & recorded BOLD; last-hidden-layer → dropout 0.2 → 3-lobe Lanczos
to TR → 4-delay FIR (2/4/6/8s) → linear voxel projection; baseline = **vanilla pretrained only**; eval = voxelwise
Pearson r on a held-out story, ridge 5-fold CV for λ, story-level holdout. **Controls they OMIT:** matched-ppl (fully
absent); permuted-brain on **downstream** (absent) — note: on *encoding* they DO run a TR-shuffle and survive it
(Δr≈0.133), so for the encoding metric the control they lack is **matched-ppl**, which is exactly our contribution.

**Arms** (Qwen2.5-0.5B, layer 12, denizenslab listening, 6 subjects, per-subject FT, ≥3 seeds, bpb-matched):
- **(a) vanilla** — untuned Qwen, encoding ridge only (`run_lebel_tune.py` `base_u`).
- **(b) brain-tuned [reproduce]** — full-FT, `kind="contrastive"`, NO KD anchor, gentle lr 1e-5 (`run_lebel_tune.py --no-lora`).
- **(c) ppl-matched generic-text FT** — full-FT on WikiText, early-stopped to arm (b)'s held-out **bpb** (L034: bpb,
  not per-token ppl). Match by construction.
- **(d) permuted-brain twin** — arm (b) recipe on block-permuted BOLD (`BL.block_permute`, n_blocks=10 = Negi's 10-TR shuffle).
**Outcome:** (b−a) the reproduced gain; (b−c) survival at matched ppl; (b−d) brain-specificity. **Predicted (E015 law +
DPI + E008/E011/E013/E017 nulls):** (b−a) collapses into the (c)+(d) band ⇒ the field's positive is a quality/FT-step
effect (the external-validity clincher). **SURVIVES** (b−d excludes the control band, symmetric-partial passed,
contiguous splits) ⇒ brain supervision is a better *teacher* for stimulus-relevant structure (DPI: still
stimulus-derivable, not non-stimulus brain signal) ⇒ Fork-A-qualifying → **STOP for Erfan.**

**New code (the one material build):** `deniz_adapter.py` (denizenslab story text/transcript → LM word features +
listening BOLD targets + reliability mask), cloned from `lebel_adapter.py` using the loaders already in
`run_eys_ceiling.py`. **Timing risk:** denizenslab story↔BOLD alignment is the exact L037 surface (the S13 TRIBE
audio bug) — verify the time axis against stimulus duration before trusting any number.

**Oracle gate must scrutinize (3):** (1) **estimand honesty** — reproduce Negi's *encoding tuned−vanilla* (ppl
unanchored), do NOT silently re-run E017's real−permuted gap and rediscover the null; arm (b) carries no KD anchor.
(2) **target reliability at n=6 denizenslab** — the recurring wall (TRIBE L038, E020 L040 both walled at n=6);
predeclare a noise-ceiling/MDE gate on the listening BOLD + the **eng1000-symmetric-partial** and **permuted-feature**
controls (L040) so a nuisance-partial collapse isn't misread. (3) **matched-ppl validity** — arm (c) matched on the
same OOD **bpb** probe, early-stopped to arm (b)'s held-out bpb, same compute/steps.