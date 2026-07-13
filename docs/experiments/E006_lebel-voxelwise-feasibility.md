---
title: "Experiment — E006: LeBel UTS03 voxelwise A2-feasibility"
tags: [experiment]
aliases: [E006]
---

# Experiment — E006: LeBel UTS03 voxelwise A2-feasibility

**Created:** 2026-06-11 · **Status:** COMPLETE, CORRECTED 2026-07-13 — conditional UTS03 result: trained−untrained gap +0.0207/+0.0277, 95–99% of 11,442 selected voxels positive, and positive on all five held-out story blocks. The original voxel-bootstrap intervals and E007 MDE claim are invalid and retracted. · **Mode:** working → interpret
**Direction:** R03 Q0/A2 at *powered* (voxelwise) resolution — the prerequisite substrate for the LeBel lever re-test (E007) that confirms E004's fragile PARTIAL.
**Predecessors:** [`E002`](E002_tuckute-encoding-feasibility.md) (A2 PASS on Tuckute, 5 ROIs) · [`E004`](E004_brain-loss-lever-test.md) (Tuckute lever = PARTIAL/fragile — routes here per its predeclared, power-limited rule)
**Code:** `scripts/lebel_adapter.py` (built, CPU+GPU-validated), `scripts/run_lebel_encoding.py` (TBD after oracle PASS), reuses `data/paper-repos/deep-fMRI-dataset/encoding/ridge_utils`
**Outputs:** `outputs/E006_lebel_gpt2.json`, `outputs/E006_lebel_Qwen.json`

---

## Why this exists (and why A2-only, not the lever)

E004 found a *fragile* brain-specific lever on Tuckute (Qwen co-trained-MSE − its permuted twin = +0.0032 [CI +0.0006,+0.0058], but fold 4 carries ~half; the absolute lever-vs-base CI includes 0). The 5-ROI screen (MDE≈+0.006) is underpowered for a +0.003 effect. Its predeclared rule routes to LeBel UTS03 voxelwise (~95k voxels, within-subject deep-sampling) for the powered confirmation.

**But a powered lever re-test is only meaningful if the substrate carries the signal at all.** E006 establishes that — the E002/A2 question at voxel scale: does a *trained* LM's middle-layer representation predict UTS03 BOLD *beyond nuisance*, under contiguous **story-level** splits, materially above an *untrained* control? This is pure measurement (no brain-tuning), cheaper, and a clean kill-gate: if it fails, LeBel is a dead substrate for our pipeline and E004's routing is moot (reframe per charter). If it passes, **E007** (the lever re-test: brain-tune Qwen co-trained-MSE at TR level, held-out-story unique R² vs its permuted twin) becomes worth the heavier TR-level training loop.

## Claim tuple (predeclared)

- **Metric:** voxelwise encoding R² (ridge, story-grouped CV), then **unique R²** = R²([nuisance, LM-features]) − R²([nuisance]), averaged over voxels and over the NC-reliable voxel subset; trained−untrained gap is the honest signal (L007). CC_norm-normalised where repeats permit.
- **Anti-confound (L003, naturalistic variant — nuisance expanded after oracle review):** contiguous **story-level** held-out CV (whole stories out — no within-story TR leakage; the time-series analogue of contiguous blocks, and the fix for bilgin-2026's TR-shuffle inflation). FIR delays 1–4 TRs (hemodynamics). Nuisance (all downsampled to TR + FIR-delayed identically, byte-identical across the trained/untrained contrast) = **word-rate** (words/TR) + **phoneme-rate** (phones/TR, from the TextGrid *phone* tier) + **mean word-duration** + **word-length** (phonemes & chars) + **log word-frequency** (static lexical scalar) + **static/non-contextual embedding** (mean input-embedding per word). The phone-tier rate/duration confounds are Feghhi's headline low-level features and load hard on auditory/STG voxels at voxel scale — omitting them would repeat the L012 hole (imageability/surprisal ate ⅓–⅔ of Tuckute's "unique" R²). **Surprisal stays OUT** (LM-derived → over-subtracts the construct; log-frequency is a *static* lexical scalar, distinct from surprisal, and IS subtracted).
- **Pass:** trained-LM unique R² > 0 AND materially exceeds the untrained-same-architecture control (≥3 seeds), on the NC-reliable voxels.
- **Kill:** trained ≈ untrained or ≈ 0 after nuisance → LeBel does not carry the signal for our pipeline at voxel scale.

## Design (LOCKED pending oracle review)

- **Subject/data:** UTS03, 84 stories on disk (`preprocessed_data/UTS03/*.hf5`, (TRs, 95556 voxels)); 84 TextGrids staged; `english1000sm.hf5` + `respdict.json` staged. Adapter validated: `ridge_utils` reuse for TextGrid→wordseq→Lanczos(window=3)→trim(feat[10:-5])→FIR(make_delayed 1..4); BOLD as-is (verified alignment, e.g. adollshouse 256→241=BOLD 241). LM word-features GPU-validated (697 words→768d, 0.2s, non-degenerate).
- **Stories used:** a fixed set of **~20 stories** (the LeBel "train" pool minus a held-out test set), leave-**N-stories**-out CV (e.g. 5 folds of 4 held-out stories) — keeps compute tractable while powered (each story ~150–300 TRs → thousands of TRs total, ≫ Tuckute's 1000 items × 5 ROIs). Story list pinned for reproducibility.
- **Models:** gpt2 (L7) + Qwen2.5-0.5B (L12), matching E002/E004; untrained same-arch control (≥3 seeds, the Feghhi control).
- **Encoding:** ridge per voxel (RidgeCV with a fixed alpha grid at first pass; banded/bootstrap-alpha is a refinement). Voxel chunks to bound memory over 95k voxels. Report mean-voxel R², **top-NC-voxel** R² (CC_norm>0.05, à la merlin-2026), and unique-over-nuisance.
- **NC / reliability + voxel selection (oracle fix — no double-dipping):** `wheretheressmoke.hf5` carries `individual_repeats` shape **(10, 291, 95556)** — 10 repeats of the canonical LeBel test story (verified on disk). **Hold `wheretheressmoke` OUT of the CV pool entirely**; compute per-voxel split-half reliability (Spearman–Brown corrected) from its 10 repeats; **select NC-reliable voxels (split-half reliability > 0.5, as-run) on THIS held-out story** (independent of the encoding fit → no Kriegeskorte double-dip); report unique R² as a fraction of that ceiling. `load_response` must gain explicit repeated-story handling before the runner.
- **Stories:** use a larger pinned set (toward all 84, compute-permitting) — not just 20 — to maximise power for the E007-MDE deliverable (oracle #6: don't leave power on the table for the question that actually matters).
- **Alignment guard (oracle fix):** assert `abs(len(feat) − len(BOLD)) ≤ 1` per story and log it (don't let `build_xy`'s `min()` silently mask a 1-TR slip). Do **not** reintroduce a global `position` regressor (it would encode story identity across concatenated stories) — rely on FIR + drift handling.
- **Compute:** LM feature extraction over the story set × {gpt2,Qwen} × {trained, 3×untrained} (~minutes/config, GPU); ridge over 95k voxels × CV (the heavy part, chunked). Est. ~1–3 h. GPUs 0/3 free.
- **Stop rule:** fixed story set, fixed layers (E002 peaks), fixed CV, fixed nuisance, fixed seed count. Pure measurement — no training, no tuning toward the outcome.

## System architecture (the measurement apparatus, visual + intuitive)

The whole experiment is one machine: it turns a *story the subject heard* and a *language model* into a single number — how much the model's middle layer explains about the subject's brain response that low-level structure cannot. Everything below is in service of making that one number honest. The diagram is the data flow; the walkthrough is why each stage exists.

```mermaid
flowchart TD
  STORY["~20 naturalistic stories<br/>TextGrid: word tier + phone tier"] --> WORDS["per-word sequence<br/>+ word/phone onset times"]

  %% --- two feature streams from the same words ---
  WORDS --> LM["LM forward pass, overlapping<br/>256-tok chunks (stride 128);<br/>read verdict layer at each word's<br/>last sub-token, max left-context"]
  LM --> LMW["per-word LM features<br/>(n_words × d_model)"]
  WORDS --> LOW["low-level nuisance (5-d, raw):<br/>word-rate · phone-rate · duration<br/>· word-length · log word-freq"]
  WORDS --> ENG["eng1000 static (985-d):<br/>mean lexical-semantic vector / word"]

  %% --- shared temporal pipeline: word-rate → BOLD-rate ---
  LMW --> TR["Lanczos resample → TR grid<br/>· trim edges · z-score<br/>· FIR delays 1–4 TR (hemodynamics)"]
  LOW --> TR
  ENG --> TR
  TR --> PCA["capacity-fair PCA, rank 100<br/>on LM and eng1000 blocks<br/>(low-level kept raw; fit on train only)"]

  %% --- target + honest voxel selection ---
  REP["held-out repeated story<br/>wheretheressmoke × 10 repeats"] --> REL["split-half reliability<br/>(Spearman–Brown), keep rel &gt; 0.5"]
  BOLD["UTS03 BOLD .hf5<br/>(TRs × 95,556 voxels)"] --> REL
  REL --> VOX["11,442 NC-reliable voxels"]

  %% --- the fit, twice, on whole-story-out folds ---
  PCA --> CV["story-grouped CV (whole stories held out)<br/>RidgeCV per voxel, two designs:<br/>nuisance = [low, PCA-eng]<br/>full = [low, PCA-eng, PCA-LM]"]
  VOX --> CV
  CV --> UNIQ["unique R² per voxel<br/>= R²(full) − R²(nuisance)"]

  %% --- two arms → the verdict ---
  UNIQ --> ARMS{"run the whole pipeline twice:<br/>trained LM · untrained same-arch (3 seeds)"}
  ARMS --> GAP["trained − untrained gap<br/>point estimate and fold-block sensitivity;<br/>% voxels with gap &gt; 0"]
```

**1. One stimulus, two feature streams.** Every story becomes two parallel descriptions of the same word sequence. The **LM stream** is the thing under test: each word's contextual representation, read from the model's middle layer. The **nuisance stream** is everything we want to *not* credit the model for — a 5-dimensional low-level block (how fast words and phonemes arrive, how long and frequent each word is) and the 985-dimensional eng1000 static block (a word's meaning *without context*, a fixed lookup). The intuition: if the LM only "aligns" because longer or rarer words happen to drive both the model and the brain, the nuisance stream already captures that, and the LM gets no credit for it.

**2. The temporal pipeline turns word-rate into brain-rate.** Words arrive several per second; the scanner samples the brain once every TR (≈2 s), and the blood-flow response (BOLD) is a slow, smeared echo of neural activity peaking ~5 s late. Three steps bridge that gap, and they are applied *identically* to every stream so nothing is advantaged: **Lanczos resampling** lands word-level features on the TR grid; **z-scoring** puts every feature on the same scale; and the **FIR delays (1–4 TRs)** hand the ridge model copies of each feature shifted forward in time, so it can line a word up with the lagged BOLD response it caused. FIR is applied within each story, never across the seam between two stories.

**3. Capacity-fair PCA stops a dimension-count win.** The LM block is ~768–896 dimensions; the eng1000 block is 985; the low-level block is 5. A wider block can absorb more variance just by having more knobs, regardless of content. So before the fit, the LM and eng1000 blocks are each reduced to the **same rank (100)**, fit on the training fold only. The low-level block is small and stays raw. This is the L004 fix: it guarantees that if the LM wins, it wins on *content*, not on carrying more columns into the regression.

**4. The noise ceiling is chosen on data the fit never sees.** A voxel that is pure noise can still be "explained" a little by chance, so we only score voxels that reliably repeat. Reliability is measured on a *separate* story (`wheretheressmoke`) the subject heard ten times: split-half agreement across those repeats, Spearman–Brown corrected, keep the 11,442 voxels above 0.5. Because that story is held entirely out of the encoding fit, selecting on it cannot inflate the score — the alternative (picking voxels on the same data you then score) is double-dipping and biases everything upward.

**5. The fit happens twice per fold, and the difference is the honest number.** Cross-validation holds out *whole stories* (no within-story timepoints leak across the train/test seam). On each fold a per-voxel ridge is fit twice: once on the **nuisance design** `[low, PCA(eng1000)]`, once on the **full design** `[low, PCA(eng1000), PCA(LM)]`. The **unique R²** is the difference — the variance the contextual LM adds *on top of* everything the nuisance already explains. A raw R² would conflate the two; the subtraction is what isolates context.

**6. Two arms, and the gap is the estimand.** The entire pipeline above runs twice: once with the trained LM, once with a randomly-initialised network of the *same architecture* (three seeds). Both arms see byte-identical nuisance, identical splits, identical PCA. The reported statistic is the **trained − untrained gap**. The 2026-07-13 audit established that voxels are spatially dependent and come from one subject, so their count cannot be used as replication. The defensible scope is conditional on UTS03, the fixed stories, and this control pipeline; fold-block signs are sensitivity evidence, not a population confidence interval.

The same six ideas define the apparatus the whole report set reuses; E002 is the simpler, isolated-sentence ancestor of this machine (no temporal pipeline, a coarser nuisance, ROI targets instead of voxels), and its own architecture section draws the reduced version.

## Decision rule (predeclared)

**The verdict statistic is the trained−untrained GAP** (not the trained absolute — on naturalistic timeseries an untrained net can score positive via rate/temporal structure even after nuisance; the gap is the normaliser-invariant signal, L007). Both arms pass through the *identical* expanded nuisance subtraction.

- **PASS (powered A2 holds) — IFF both:** (a) trained−untrained gap on NC-reliable voxels > 0 with bootstrap CI excluding 0; **and (b) the E007-lever MDE deliverable (below) is comfortably < +0.003.** → LeBel both carries the signal *and* can resolve the lever; **proceed to E007.**
- **PARTIAL / lever-line-underpowered (the oracle's "quiet kill" — watch for it):** gap > 0 (substrate carries signal) BUT the E007-lever MDE sits **above +0.003** even on the full story set. → A2 holds but LeBel cannot resolve the +0.003-scale lever; building the TR-level training loop (E007) would be structurally underpowered. Honest move: **do not build E007**; the lever line stops at "real signal, not cleanly optimizable/resolvable" and the thesis reframes toward measurement rigor / the trade-off-curve framing (charter).
- **KILL (substrate dead).** Trained ≈ untrained or ≈ 0 after the *expanded* nuisance. → LeBel cannot resolve our question at all; E004's PARTIAL cannot be confirmed. Reframe (charter).

**Predeclared E007 design (locked NOW to avoid garden-of-forking-paths):** if E006 PASSes, E007 brain-tunes Qwen co-trained-MSE (the E004 front-runner) at TR level; **PRIMARY specificity statistic = the PAIRED `arm − its-own-block-permuted-twin` contrast** (matched on fold/seed — the test that detected E004's effect; removes per-fold common-mode), with the absolute-vs-base as a *secondary descriptive only*; the unpaired `>perm95` is **retired** (it was E004's mis-specification). Block-permutation scheme + seed count + a perplexity-matched/gentler training regime (E004's LoRA degraded ppl ~2×) are part of that lock.

**Predeclared deliverable (oracle #6):** E006 must output an **empirical MDE for the E007 lever statistic**, computed from E006's fold-level variance of unique R² on the NC-reliable voxels. This is what licenses (or refuses) E007 — not the A2 gap alone.

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_lebel_encoding.py --model gpt2 --untrained-seeds 0 1 2
CUDA_VISIBLE_DEVICES=3 uv run python scripts/run_lebel_encoding.py --model Qwen/Qwen2.5-0.5B --untrained-seeds 0 1 2
```

## Status

`lebel_adapter.py` built + validated (non-LM path CPU; LM-feature path GPU). `run_lebel_encoding.py` + the oracle review are the remaining work before a run. Scope deliberately A2-only (kill-gate); the lever re-test is E007, gated on this passing. The E004→E006 routing and the corrected paired-primary predeclaration are the load-bearing carry-forwards.

## Results (ran 2026-06-11; UTS03, 20 stories, 5 story-folds, 11442 NC-reliable voxels rel>0.5)

| Model · layer | trained unique R² | untrained unique R² | **trained−untrained gap** | % voxels gap>0 | held-out story blocks positive |
|---|---|---|---|---|---|
| gpt2 · L7 | +0.0038 | −0.0169 | **+0.0207** | 95% | 5/5 |
| Qwen2.5-0.5B · L12 | +0.0103 | −0.0173 | **+0.0277** | 99% | 5/5 |

Both ran ~9–10 min. Nuisance = low-level (word-rate, phoneme-rate, word-duration, word-length, log-freq) + eng1000 (985-d static), capacity-fair PCA(100) on LM & eng1000 blocks, low-level raw, FIR(1–4); BOLD aligned (assert passed). Voxels selected on the held-out `wheretheressmoke` 10 repeats (split-half reliability > 0.5) — no double-dipping.

## Interpretation (corrected 2026-07-13)

**Conditional result.** For UTS03 and this fixed story/control pipeline, trained models exceeded their untrained controls on all five held-out story blocks. The point gaps are +0.0207 for gpt2 and +0.0277 for Qwen; 95% and 99% of the selected voxels have positive gaps. This establishes a within-subject existence result on this dataset. It does not provide participant- or population-level inference.

**Retracted inference.** The original 95% intervals resampled 11,442 spatially dependent voxels from one subject as if they were independent. They are therefore anti-conservative and must not be cited. The five fold gaps are all positive—gpt2 `[0.0167065, 0.0234877, 0.0171265, 0.0190724, 0.0271819]`; Qwen `[0.0288241, 0.0214104, 0.0172086, 0.0384345, 0.0323849]`—but folds share training stories, so they are sensitivity checks rather than independent replicates.

**Retracted E007 power claim.** The reported +0.0129/+0.0150 “MDE” was built from unmatched absolute fold summaries rather than the future paired tuned-versus-permuted contrast. It neither estimates the intended E007 variance nor licenses the statement that E007 was structurally underpowered. The historical decision not to build E007 remains a project decision, but E006 no longer supplies its statistical justification.

**Load-bearing artifacts.** `outputs/E006_lebel_gpt2.json` has SHA-256 `ea424b7d2f8a32dd289e8ef8066c8609749f4edc1b4cdd132373a78bd6b6830b`; `outputs/E006_lebel_Qwen.json` has SHA-256 `09b77b8801e937d8232ce7e7f16435e490f0b9300c78ce4ede23d00bf07d2581`.

## Status / next

E006 = conditional UTS03 A2 evidence, not a powered population PASS. The manuscript must remove the voxel-bootstrap intervals, “powered” language, and E006-derived E007 MDE claim. A population claim would require independent participants; a formal story-level interval would require a dependence-aware design with retained fold/story-level data.

## Iteration log

| Date | Run / seed | Command / config | Result | Observation | Next |
|---|---|---|---|---|---|
| 2026-06-11 | design | — | adapter validated; design locked pending oracle | scoped A2-only (lever→E007) | oracle review → build runner → run |
| 2026-06-11 | oracle HOLD→resolved | — | 2 fatal fixes (phone-tier nuisance; held-out CC_norm voxel selection) + E007-MDE deliverable + paired-primary E007 lock | flagged the "quiet kill": lever line may be structurally underpowered if MDE > +0.003 | build runner → run |
| 2026-06-11 | FULL run | gpt2 + Qwen, 20 stories, 5 folds, rel>0.5 | **A2 STRONG PASS** (gap +0.021/+0.028, 95–99% voxels+); **E007-lever MDE +0.013/+0.015 → can't resolve +0.003** | substrate alive; lever line underpowered → pivot to E005 trade-off curve | design E005 (matched-ppl KD) |
| 2026-07-13 | inference audit | retained JSON + runner review | point estimates retained; voxel CIs and E007 MDE claim retracted | one subject and spatially dependent voxels cannot support the original inference | synchronize manuscript; retain conditional UTS03 scope |


## Related
- [`status.md`](../status.md) — current project state
- [`03-methodology.md`](../03-methodology.md) — authority and inference contract
