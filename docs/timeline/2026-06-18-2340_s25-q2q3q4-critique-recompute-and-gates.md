---
title: "S25 — 2026-06-18 (working session): critique panel on Q2–Q4, Q2 recompute, Q3/Q4 pre-compute gates"
tags: [timeline]
---

# S25 — 2026-06-18 (working session): critique panel on Q2–Q4, Q2 recompute, Q3/Q4 pre-compute gates

**Mode:** working. **Trigger:** Erfan — run the critique panel on Q2/Q3/Q4 and finalize, per rung, whether we need
(A) the verdict is safe + a theoretical proof of *why* it didn't work, (B) more analysis of existing data, or (C) a new
experiment. Then: do Q2, start Q3, start Q4 sequentially, autonomously, overnight.

**NO rung flipped. Q0–Q5 stand.** Everything below is *proposed* and awaits Erfan's confirm (D015).
Server crashed mid-session under download load; this is the recovery checkpoint.

---

## The four-lens panel (counter-argument · first-principles · premortem · socratic), all opus, swept Q2→Q4

Headline: **none of Q2/Q3/Q4 is closable by theoretical proof.** The two nulls (Q3, Q4) rest on the same unproven
premise — $Y \perp \theta^\* \mid S$ (the DPI-ceiling assumption, already flagged L041) — which the math we cite
(`06-theory-grounding.md`) cannot discharge. So the honest closes are one free recompute (Q2) and experiments (Q3/Q4),
not proofs.

| Rung | Reconciled bucket | One-line |
|---|---|---|
| **Q2** | **B — free recompute** | the "lever exists" CI is the L015-condemned 15-cell bootstrap; dissolves at the honest unit |
| **Q3** | **A as scoped · one C door · NOT theory-provable** | verdict safe as *scoped*; only open door = n=6 full-FT; oracle KILLed the build |
| **Q4** | **A as scoped · C to close · NOT theory-provable** | bounded-null honest for OOD-ppl; the selection/sample-efficiency channel is argued-shut, not measured-shut |

---

## Q2 — DONE (recompute, no compute). Proposed: demote 🟡 → null.

Independent recompute from `outputs/E004_brain_lever_Qwen.json` (the mse − permuted-twin paired contrast):

```
FLAT 15-cell (the recorded construction):  +0.00316  CI [+0.00062, +0.00584]   excludes 0   ← ladder's "+0.0032 [+0.0006,+0.0058]"
HONEST fold-level unit (n=5):               +0.00316  t-CI [-0.00227, +0.00858]  INCLUDES 0
per-fold: {0:-0.0007, 1:+0.0003, 2:+0.0045, 3:+0.0016, 4:+0.0101}
fold-4 share = 64% · leave-fold-4-out → +0.00141 · beats_permuted_null = False (recorded in JSON)
```

The single number licensing "a brain-specific lever exists" is the **exact 15-cell flat bootstrap this project
condemned for E005 (L015)** and never re-applied to E004. At the honest inference unit it includes zero; one fold
carries 64%; the unpaired permuted-null test already records `False`.

**Proposed Q2 verdict (awaits Erfan):** demote from "fragile brain-specific lever exists" →
**"no inference-unit-valid lever on the 5-ROI screen — a fold-driven 15-cell artifact that dissolves at the honest unit."**
This makes Q2 *consistent* with the robust Q3 null rather than in mild tension with it.
Fix is a recompute via `scripts/reanalyze_e005_e006.py` machinery; no rerun.

---

## Q3 — oracle gate: KILL the n=6 build; run the cheap single-subject gate instead. Data IS ready.

- **anti-confound-designer** assembled a battery-complete design (manipulation-check gate fires first: full-FT must
  improve held-out alignment over base `real_u > base_u` in ≥4/6 subjects + real Δbpb, else it's lever-failure #6, not
  a null; held-out-STORY leave-2-out CV; spatially-blocked permuted twin n_perm≥10; construction-matched ppl; n=6
  listening primary; subject02 NC max=6.04 anomaly bypassed via held-out-repeat split-half).
- **oracle-reviewer verdict: KILL the multi-day n=6 build** (not the rigor). Reason: E017 *already* ran full-FT
  voxelwise (LeBel n=3) → null with the manipulation mostly failing its gate; the manipulation-check is **0-for-5**
  across E013 v1/v2, E017 gentle/aggressive, E019. denizenslab adds naturalistic data + subject count, not a new
  mechanism. A gate-fail is recorded as lever-failure #6 (non-Q3-moving) → low information per multi-day compute.
- **Oracle's redirect (the action):** run the **cheap single-subject manipulation-check gate first** (~1 GPU-day) on
  one best-SNR subject (e.g. 01). PASS (real_u>base_u + real Δbpb) → genuine Fork-A surprise → **STOP for Erfan**.
  FAIL → lever-failure #6, the "one untested door" hedge is honestly retired, compute → Q4.
- **Pre-compute fixes flagged:** (1) replace the ppl-intercept-at-matched-bpb with a construction-matched generic-FT
  arm (the E017 fix; cross-family intercept ≠ within-model adjustment); (2) `git-annex get` the 3 stub subjects
  (04/06/09) or predeclare n=6 = {01,02,03,05,07,08}; add a phase-randomized shape-twin if the gate passes.

**Data readiness (corrects stale ladder):** git-annex IS installed (`/usr/bin/git-annex`); 6 real denizenslab listening
subjects on disk at `data/denizenslab/responses/` (~35G), mapper present. The "BLOCKED" / "git-annex not installed"
ladder notes are STALE.

**Erfan's call (S25): Fork 1 = (a)** — build the denizenslab adapter + run the cheap 1-subject manipulation gate
(for literal 100%-coverage of the "one untested door"), accepting the prior that it likely reproduces lever-failure #6.

**Feasibility CONFIRMED — all prerequisites on disk, no further data needed:**
- responses `data/denizenslab/responses/subjectNN_{listening,reading}_fmri_data_{trn,val}.hdf` — listening trn = keys
  `story_01..story_10`, each `(n_tr≈324–450, 81133 voxels)` float64; val = held-out story ×2 repeats (for NC).
- **stimulus word-timings: `data/denizenslab/stimuli/textgrids/stimulus_textgrids/*.TextGrid`** (the tune-pair
  prerequisite — present). Parsers: `data/paper-repos/speech-llm-brain/Brain_preditictions/{textgrid,stimulus_utils}.py`,
  `Feature_Extraction/extract_features_words.py`; denizenslab `code/`.
- mappers `data/denizenslab/mappers/`; NC arrays present (subject02 listening NC max=6.04 anomaly → use val-repeat split-half).
- `scripts/run_lebel_tune.py` already supports `--no-lora` (full-FT) + `--kd-teacher` (KD anchor); needs only a
  **denizenslab adapter** mirroring `lebel_adapter` (`get_wordseqs`/`load_response`/`build_story_data`).
- **One mapping gap:** HDF `story_NN` ↔ TextGrid story-name (life/avatar/…) — resolve from denizenslab `code/`/`features/`.

**Deferred to a FRESH session (not built in S25):** cost hit the ~$67 critical line + a long context; a verification-heavy
fMRI alignment adapter is the L037 silent-bug class and must be built incrementally with shape/timing asserts in a clean
context, not ground out here. **Fresh-session build order:** (1) story_NN↔name map + TextGrid parse → assert word-time
ranges vs TR count per story; (2) denizenslab adapter (mirror lebel_adapter); (3) NC voxels from val split-half; (4) the
cheap gate = full-FT toward subject01-listening real BOLD, KD-anchored, gentle lr → `real_u > base_u` + real Δbpb (the
oracle's pre-compute fix: construction-matched generic-FT arm, NOT the ppl-intercept). PASS on 1 subject → STOP for Erfan;
FAIL → lever-failure #6, retire the hedge.

---

## Q4 — the oracle-endorsed compute target. Design gap caught BEFORE compute. Data partially staged.

- **ZuCo 2.0 features ARE on disk** (`data/zuco-benchmark/src/features/`, 624 `.npy`, 26 subjects: EEG band means +
  eye-tracking, sentence-level). **But the benchmark task is NR-vs-TSR reading-task classification**
  (`class_task='tasks-cross-subj'`) — *decoding a cognitive state from brain features*, NOT a text-NLP task with the
  cognitive signal as train-only privileged information. **Wrong framing for the LUPI sample-efficiency test.**
- **The right substrate = ZuCo 1.0 task1-SR (SST sentiment)**: text → sentiment label, with per-word EEG+gaze as the
  privileged side-channel. That is the canonical LUPI setup (zeroed-PI/TRAM control + matched-information non-brain
  teacher + phase-randomized shape-twin, per L050).
- **ZuCo 1.0 download did NOT complete** — the full `osf -p q3zws clone` (40–70 GB) is the load that crashed the
  server; `data/zuco1/` is empty. **NOT re-launched unattended.**

**SAFE targeted fetch (hand to Erfan / supervised) — only the sentiment task, ~few GB not 40–70 GB:**
```
cd /home/centcom/data/brain-alignment/data/zuco1
for f in $(uv run --with osfclient osf -p q3zws ls | grep '^osfstorage/task1 - SR/'); do
  uv run --with osfclient osf -p q3zws fetch "$f" "./${f#osfstorage/}"
done
```
(ZuCo 1.0 = OSF `q3zws`, CC-BY, no credentials. task1-SR holds the sentiment labels + EEG/ET .mat per subject.)

**Q4 GATED (S25): design E024 written → anti-confound battery assembled → oracle = HOLD / NOT-YET.** The gate caught,
before compute: (1) **substrate underpowered** — ZuCo 1.0 SR sentiment is only 400 sentences; MDE at low-n swamps any
LUPI gain; a null would be underpowered, not informative. (2) the reference loader is **reading-task classification, not
sentiment**, and exposes **no per-word timeseries** → the decisive L049 shape-twin can't be built. (3) **control 5 unfair**
(reliability-matching → false null; affect-leakage → false positive). **Oracle redesign:** eye-tracking-first on a
larger-N gaze corpus (Provo/GECO/Natural-Stories or pooled ZuCo NR) + a **synthetic-PI MDE positive-control FIRST**
(one day) to confirm detectability before building five arms. Full fixes in `experiments/E024`. **Needs Erfan's substrate
call.** ZuCo 1.0 clone running (has task3-TSR so far; NR/SR later) — useful regardless of substrate.

---

## Fork resolutions (Erfan, S25)
- **Fork 1 = (a):** build denizenslab adapter + cheap 1-subject gate (feasibility confirmed above; fresh-session build).
- **Fork 2 — roadmap check (Erfan asked):** the oracle's Q4 redesign **IS on-roadmap**, a refinement of *how* to do P1, not
  a detour. P1 is locked as "ZuCo-first (EEG+eye-tracking) supervised low-data learning curve" (§8; idea-tree T4.4→ACTIVE
  LEAD, T1.3→ACTIVE). Eye-tracking-first = leading with the more-reliable half of that same substrate. GECO/Provo/Dundee
  are already named in idea-tree T1.3 ("+ GECO/Provo/Dundee for behavioral scale"). The synthetic-PI MDE positive-control
  is the roadmap's own rigor process (predeclared kill + planted-effect positive-control, L048). **The one real refinement:**
  ZuCo *sentiment* (400 sentences) is too small → "ZuCo-first" should mean ZuCo's higher-N gaze slice or the named
  GECO/Provo scale-up, not SR-sentiment. **Q4 substrate still Erfan's explicit pick before the build.**

## State of the board (proposed, for Erfan to confirm at /wrap)
- **Q2:** 🟡 → ❌/null (demote) — *recompute done, awaits confirm.*
- **Q3:** ❌ stays; "one untested door" hedge → cheap single-subject gate is the decisive cheap test; KILL the n=6 build.
- **Q4:** ❌ stays; the sample-efficiency/selection channel is the live forward bet; data being staged.

## Artifacts this session
- Q2 recompute (numbers above; reproducible from `outputs/E004_brain_lever_Qwen.json`).
- ZuCo 2.0 features staged: `data/zuco-benchmark/` + `src/features/` (624 npy).
- `data/zuco1/` (empty — ZuCo 1.0 fetch to be re-run targeted).
- Panel + anti-confound-designer + oracle transcripts (this session).

## Cost / process note
~$15+ session; server crashed once under the ZuCo-1.0 full-clone I/O load. Heavy downloads should be scoped + foreground.
The "all-night autonomous" frame met reality: Q3/Q4 are multi-day supervised builds, gated not rushed (rigor-before-compute, S8).


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
