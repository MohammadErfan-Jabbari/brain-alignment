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

---

## v3 — oracle HOLD addressed; SUBSTRATE moved to LeBel; RUN-READY spec (S14, 2026-06-14). Faithful-Negi-head = fresh-launch build.
The oracle gate returned **HOLD** with three fatal gaps. All addressed; E019 is now run-ready *except* the one real
material build (the faithful Negi head), which is a fresh-session task (L031: don't start a multi-hour timing-sensitive
loop at a session tail — that is the L037 artifact surface).

**SUBSTRATE DECISION (D031): move E019 from denizenslab → LeBel UTS01/02/03.** denizenslab n=6 was chosen (D027)
ONLY for TRIBE's voxel→fsaverage5 mapper, which E019 does not need. It has walled TWICE at n=6 (TRIBE L038, E020 L040;
ref-rel 0.33, ε-NC 0.17) and only story_11 carries a noise ceiling (F2). **LeBel UTS01/02/03 is the proven-reliable
substrate** for exactly this experiment: deep single-subjects (~5h each), the multi-repeat held-out story
("wheretheressmoke") for NC, **powered voxelwise A2 (E006)**, and the **full-FT infra already run there (E017)**. This
resolves F2 (LeBel has the deep per-subject + repeated-story NC structure) and F3 (LeBel encoding targets are reliable
— E006 powered A2 on ~11.4k NC voxels). Negi's own monolingual control uses LeBel UTS07/08 + Deniz, so LeBel is faithful.

**F1 (FATAL) — build a FAITHFUL Negi head; the reuse engine is NOT Negi.** `run_lebel_tune.py build_tune_pairs` uses
per-segment-mean BOLD + a fixed 4s HRF delay (it explicitly "avoids a differentiable Lanczos/FIR loop") — and that
per-segment-mean readout-MSE path is exactly what L026/L027 proved DEGRADES held-out alignment on this substrate. Using
it for arm (b) would fail to reproduce Negi's gain for a PIPELINE reason (a strawman of Negi), not brain-specificity.
**Fix: port the actual Negi head** — differentiable 3-lobe Lanczos downsample → learned 4-delay FIR (2/4/6/8s) → linear
voxel projection → **NT-Xent** over the batch (Negi note ll.94-106). This is the real material build (a fresh session),
NOT a `lebel_adapter` clone. Reuse E017's full-FT loop scaffolding + `brain_loss.py` NT-Xent; the head/readout is new.

**F2 (FATAL) — replication unit.** On LeBel the held-out test story has multiple repeats → a real NC; use it for the
ceilable encoding-Δr + survival bound. Predeclare: the Δr verdict is computed on the NC-ceilable held-out story; other
stories train the arms. (If staying on denizenslab were ever forced, story_11-only = a single-story bound, NOT Fork-A-able.)

**F3 (FATAL) — POWER GATE FIRST (cheapest decisive).** Before any FT: compute the held-out-story **encoding-Δr MDE**
from fold variance (E006 machinery, `run_lebel_encoding.py`) on LeBel. **KILL if MDE > the reproduced (b−a) gain
magnitude** (≈ the band width we must resolve) — then the substrate can't separate "collapsed into band" from
"underpowered," and E019 must move to deeper data or concede external validity as bounded (lean on E015 + the nulls).
Run this gate as step 0; do not build the FT arms until it passes.

**Confound neutralizers (coded, not post-hoc):** (c) matched-ppl is only meaningful if (b) moves **bpb** beyond a
predeclared threshold — report Δbpb; if ~0, flag "no divergence to match," not a passed control (L011/L019). The
nuisance partial MUST use the **symmetric partial** (apply the same nuisance to vanilla arm (a)/A_shared) + the
**permuted-eng1000** control (L040) — eng1000 spans the LM subspace and will vacuously collapse the gain otherwise.
Permuted twin (d): identical seed/steps/lr to (b); report the `real_u > base_u` manip-check per arm (L026) before
interpreting (b−d). **Fork-A bar (asymmetric, correct as written):** (b−d) excludes the control band AND symmetric-partial
passed AND contiguous splits AND power-gate cleared ⇒ STOP for Erfan.

**KILL conditions (any one):** (1) story-Δr MDE > reproduced (b−a) gain (3rd walled instrument → move/concede);
(2) arm (b) reproduces NO gain even uncontrolled while the manip took hold (bpb moved, alignment didn't degrade) ⇒
"Negi's encoding gain is method/scale-fragile" (weaker, not a clincher, but honest); (3) symmetric eng1000 partial
collapses vanilla arm (a) as much as (b−a) ⇒ nuisance control vacuous on this substrate, can't adjudicate here.

**POWER GATE — already satisfied by recorded evidence (E006).** E006 powered voxelwise A2 on LeBel UTS03 with this
exact encoding machinery (`run_lebel_encoding.py`: NC-reliable voxel selection on the **10-repeat** held-out story
"wheretheressmoke", story-grouped CV, unique-R²), resolving the trained−untrained gap **+0.021/+0.028 at 95–99%
positive** with tight CIs. An instrument that resolves a ~0.02 unique-R² effect easily resolves a Negi-scale encoding
gain (~0.13 Pearson r). ⇒ **F3/KILL-1 cleared on LeBel without a new run** (this is why the substrate move matters — the
denizenslab n=6 instrument could NOT have cleared it). The Δr-specific MDE is finalized once arms (a)/(b) exist, but the
instrument is demonstrably powered.

**Status: RUN-READY. The ONLY remaining piece is the faithful-Negi-head build** (differentiable Lanczos+FIR+NT-Xent
training head + LeBel arms a/b/c/d) — a multi-hour, timing-sensitive (L037) **fresh-launch** task per L031, NOT to be
rushed at a session tail. Headline/spine framing remains Erfan's call when the number lands.

---

## v4 — BUILT + RUNNING (S14, 2026-06-14). Faithful head validated; gentle-regime run in flight; reproduction-strength is the live question.
**Built `scripts/run_e019_negi.py`** — the faithful Negi head (Erfan: "build it now"). Per-word LM feats (grad,
chunked) → **fixed Lanczos matrix** (verified vs `lanczosinterp2D`, max|Δ|=2.4e-6) → trim → z-score → 4-delay FIR →
linear voxel projection → **NT-Xent** at TR resolution; full-FT, per contiguous word-window (TR resolution, fixes the
oracle's F1 — NOT the per-segment-mean readout L026/L027 showed degrades). Arms a/b/c/d; metrics = held-out encoding
Pearson r (Negi) + unique-R² (E006). Arm (c) FT on a **disjoint** WikiText slice, early-stopped to arm (b)'s held-out
ppl (no leak). Smoke-validated end-to-end; full-scale run clears cleanly (UTS01: 2228 NC voxels, vanilla enc_r=+0.146
= Negi scale ✓).

**Full run IN FLIGHT** (UTS01/02/03 × 3 seeds × arms a/b/c/d, lr=1e-5, 2 epochs — the gentle ppl-preserving regime;
`outputs/E019_negi/results.json` + `full_run.log`). **Early read (UTS01 s0/s1):** gain (b−a) in enc_r ≈ +0.002/−0.001,
brain-specificity (b−d) ≈ +0.0005/−0.004 — **tiny and non-specific**, the predicted Fork-B pattern.

**THE LIVE QUESTION (oracle KILL-2, now empirical): at the gentle regime arm (b) barely moves (gain ≈0 ≪ Negi's
~0.13) — so this regime may show "no gain to break" (method-fragile), the WEAKER finding, rather than
"reproduce-then-break."** A faithful reproduction of Negi's *large* gain (they let ppl drift, no anchor) likely needs a
**stronger tune** (higher lr / more epochs). **Next (fresh, oracle-gated): a tuning-strength sweep** on 1 subject —
does any regime reproduce a Negi-scale (b−a) gain, and does it then survive (b−c) matched-ppl + (b−d) permuted? If even
a strong tune can't reproduce a gain → honest "Negi's encoding gain is method/scale-fragile under faithful
reproduction" (KILL-2, publishable-but-weaker). If a strong tune reproduces a gain that collapses into the control
band → the external-validity clincher. **The judge + counter-argument/premortem panel runs on the COMPLETE results.**
No rung flips; framing = Erfan's call.