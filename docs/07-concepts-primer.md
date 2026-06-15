# Concepts Primer — the reusable vocabulary every experiment assumes

**What this is.** A plain-language glossary of the primitives that recur across every experiment doc
and report. (Naming: **E-numbers** are experiment notebooks under `docs/experiments/` — E002 = the
Tuckute feasibility test, E006 = the LeBel voxelwise test, etc.; their live status is in `docs/ladder.md`,
the canonical board that wins any conflict. **R-numbers** are synthesis reports under `docs/reports/`.
**L-numbers** are lessons in `docs/learnings.md`; **D-numbers** are decisions in `docs/decisions/`.) The experiment docs deliberately stay terse and
assume these terms; this file is where they are defined *once*, clearly, so a reader new to a doc can
ground the vocabulary here instead of re-deriving it. The math/theory version of several of these
(MI bound, DPI, conditional-MI = unique R², rate-distortion) lives in `06-theory-grounding.md`; this
file is the intuition, not the formal treatment.

> If a definition here ever disagrees with `ladder.md` or an experiment's recorded numbers, those win.
> This is a teaching/reference aid, not a source of truth.

---

## The measurement

**Brain activation / fMRI.** When a person reads or listens to language in an fMRI scanner, we record
how strongly each piece of their brain responds. That recorded response is the "brain" side of every
alignment measurement.

**Voxel.** The finest unit fMRI measures: a small 3D cube of brain tissue (~2–3 mm per side), a
"volume pixel." A whole brain is ~100,000+ voxels. Each voxel gets one activation number per moment.

**ROI (Region Of Interest).** A functionally-defined brain *region* — a named group of voxels that do
a known job, e.g. "left-hemisphere inferior frontal gyrus, part of the language network." Analyzing
100k noisy voxels is hard, so neuroscientists often **average the voxels inside each region** and work
with a handful of region-averages instead. So:
- **ROI-level** data = a few numbers per stimulus (Tuckute: **5** language-region averages). Coarse,
  low-dimensional, statistically thin, but easy and robust.
- **Voxel-level** data = tens of thousands of numbers per stimulus (LeBel: ~95k voxels). Fine-grained,
  far more data, far more statistical power — at more compute and noise.

This ROI-vs-voxel distinction is exactly why we run *both* a coarse ROI screen (E002) and a powered
voxel-level confirmation (E006).

**Encoding model.** The thing we actually fit to measure alignment: a **regularized linear regression
(ridge)** that takes an LLM middle-layer representation of a stimulus and predicts the brain
activation for that same stimulus. Direction matters: **encoding** = LLM features → predict brain.
(The reverse, brain → predict stimulus, is "decoding" and is not our operative direction.) We keep the
map **linear on purpose** — a flexible nonlinear map could manufacture "alignment" out of almost any
representation, so linearity is a guardrail and tests whether the brain-relevant information is
*linearly accessible* in the LLM's features (a stronger, more falsifiable claim).

**R² (variance explained).** How well the encoding model's predictions match the real brain response
on held-out data. 1.0 = perfect; 0 = no better than predicting the mean; negative = worse than the
mean (which untrained-control models routinely are).

---

## Why a raw R² lies — and the four tools that fix it

A raw encoding R² can look high for reasons that have nothing to do with "the LLM is brain-like."
Four distinct lies, each with the tool that kills it:

| The lie (confound) | What inflates R² | The tool that kills it |
|---|---|---|
| **Nuisance / low-level features** | Sentence length, word/phoneme rate, position, static word embeddings — both the LLM *and* the brain track these | **Unique R²** (below) |
| **Split leakage** | Shuffled train/test puts autocorrelated near-twin samples on both sides → leaks the answer | **Contiguous splits** (below) |
| **It's just the architecture** | A random-init net of the same shape might predict the brain too | **Untrained control** + the **gap** (below) |
| **Brain data is noisy** | You can never explain the noise; raw R² has no scale | **Noise ceiling** (below) |

**Unique R².** Instead of the raw R², we report what the LLM adds *beyond* nuisance features:
`unique R² = R²(nuisance + LLM features) − R²(nuisance alone)`. Only the *extra* variance the LLM
explains over and above length/rate/position/static-embeddings counts. (Formally this is a conditional
mutual information — see `06-theory-grounding.md`.)

**Contiguous splits.** We never shuffle the train/test split. Adjacent samples are autocorrelated (in
time, or in position), so a shuffled split drops near-identical samples into both train and test,
leaking the answer and inflating held-out R². We hold out whole **contiguous blocks** (Tuckute) or
whole **stories** (LeBel) instead. This is a *separate* failure from nuisance features — fixing one
does not fix the other.

**Untrained control + the trained−untrained GAP.** We also fit the encoding model on a **random-init
network of the same architecture** (≥3 seeds; the Feghhi control). If random features already predict
the brain after nuisance, then "alignment" is just architecture + nuisance, not learned language. So
**the verdict statistic is the trained − untrained GAP**, not the trained model's absolute R² — the
gap isolates what *language training* added, over and above shape and nuisance.

**Permuted twin.** A stronger control used when we *optimize* alignment (the lever / distillation
experiments): run the identical procedure but with the brain targets permuted (shuffled so they no
longer match the right stimulus). A real brain-specific effect must beat its *own* permuted twin, not
just beat zero. This removes per-fold common-mode and is what detected (and later bounded) the lever.

---

## Noise ceiling — and what "% of the ceiling" means

fMRI is noisy: show the **same person the same sentence twice** and the recorded response is *not*
identical (scanner noise, blood-flow fluctuation, attention drift). So there is a hard upper bound on
how much of the brain signal *any* model could ever predict — you can never predict the random part.
That bound is the **noise ceiling**, estimated from repeated presentations of the same stimulus (how
well does the brain predict *itself* across repeats?). **CC_norm** is the specific normalized-
correlation estimator of it used on LeBel.

Because raw R² has no meaning without the ceiling, we report alignment **as a fraction of the ceiling**.
Example (Tuckute, ceiling R² ≈ 0.353): Qwen's unique R² of 0.036 is not "3.6% of all variance" — it is
`0.036 / 0.353 ≈ 0.10` = **~10% of the noise ceiling**. In plain words: *of the brain signal that is
even predictable in principle, the LLM's unique contribution captures about a tenth.* That normalized
number is the honest one; a raw R² of 0.036 against a ceiling of 0.35 is very different from the same
0.036 against a ceiling of 0.9.

**Voxel selection without double-dipping.** We only score voxels that are reliable (ceiling above a
threshold), and we pick that reliable set on a *held-out* repeated story — never on the same data we
fit the encoding model on — so the selection doesn't inflate the result (no Kriegeskorte double-dip).

---

## Perplexity — the language-model-quality axis

**Perplexity** measures how good a model is at predicting text: roughly, how "surprised" it is by
held-out tokens. Formally it is the exponential of the average per-token cross-entropy loss,
`PPL = exp(−(1/N) Σ log p(token | context))` — so it is the effective number of equally-likely choices
the model is hesitating between at each step. **Lower perplexity = better language model.** This axis is
load-bearing for the whole thesis because **alignment co-varies with perplexity** (better LM → more
brain-aligned, ρ ≈ −0.88 within GPT-2, ≈ −0.92 across families; E003/E015, L011/L030). That is why the
headline experiments must compare arms **at matched perplexity**: otherwise an "alignment went up" result
could just mean "we built a better language model," not "the brain objective did something brain-specific."

## The two datasets in play

**Tuckute 2024** (`data/tuckute2024/`). 1000 isolated English sentences shown one at a time; the brain
side is delivered as **5 left-hemisphere language-ROI averages**, averaged over 5 participants.
ROI-level (coarse), tiny, high-ceiling, and — being isolated sentences — free of the
temporal-autocorrelation leakage that plagues continuous stimuli. **Our Layer-0/Layer-1 fast screen.**

**LeBel ds003020, subject UTS03** (`data/lebel_ds003020/`). Naturalistic spoken-story listening, deep
within-subject sampling, ~95k **voxels** with a CC_norm noise ceiling. Fine-grained and powered.
**Our Layer-3 thesis-grade voxelwise benchmark.** (Full registry: `04-data-benchmarks.md`,
`05-dataset-registry.md`.)

---

## One distinction to carry everywhere

**"Real" is not the same as "movable" is not the same as "useful."** These are three separate
questions, established by three separate rungs:
- **Real** (A2 / Q0): does the alignment signal exist beyond confounds? (E002, E006 — yes, powered.)
- **Movable / a lever** (Q2): can you *raise* held-out alignment by optimizing for it? (E004 — fragile.)
- **Useful** (A3 / Q4): does induced alignment buy something practical? (E009 — bounded null.)

A strong PASS on "real" says nothing about "movable" or "useful." Keeping these separate is the spine
of the whole ladder — see `ladder.md`.
