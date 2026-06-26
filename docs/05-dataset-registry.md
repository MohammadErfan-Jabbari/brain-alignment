---
title: "05 — Dataset Registry (living watchlist)"
tags: [dataset]
---

# 05 — Dataset Registry (living watchlist)

**Last updated:** 2026-06-09

**What this doc is:** a continuously-updated catalogue of *every* dataset that might ever be relevant to this thesis — neural, behavioral, and the NLP corpora used by the distillation baselines. One row per dataset: what it is, its key features, how open it is, and our use-case fit + status. The point is that when we need data in the future, we already know what exists and what it costs to get.

**What this doc is *not*:** it is not the decision (that's `04-data-benchmarks.md`, the powered survey of the four language-fMRI benchmarks we committed to, with the power analysis behind D008), and it is not paper-by-paper provenance (that's `reports/R02_datasets-and-code.md`, which maps which paper used which dataset + the code repos). Where those cover an entry in depth, this doc links to them instead of duplicating.

**Accuracy rule (carried from R02 / L003):** every feature below is stated by the dataset's own page or paper. "NOT STATED" means the source genuinely did not give it — it is never an estimate. Where two sources disagree (subject counts especially), both numbers are shown and the conflict is flagged. Verified 2026-06-09 by direct fetch of dataset pages + papers; the four benchmarks marked → 04 were verified in Session 2.

**Status legend:** `PRIMARY` committed in D008 · `GENERALISATION` second benchmark · `PILOT` plumbing sanity-check · `CANDIDATE` open & viable, not yet chosen · `LOW` relevant only under a behavioral-alignment arm · `OUT` out of scope · `AUX` auxiliary recipe, not a neural dataset.

---

## Registry — neural & behavioral (the ones that get full treatment)

| Dataset | Modality | Subjects | Stimuli | Lang | License | Access (login/DUA) | Size | Noise ceiling | Status |
|---|---|---|---|---|---|---|---|---|---|
| LeBel 2023 (`ds003020`) | fMRI, spoken stories (deep) | 8 (3 deep-sampled ~20h) | 27–82 stories, ~81h total, TR 2.0s/3T | EN | CC0 (snapshot) / CC-BY (paper) | none / none — S3 `--no-sign-request`, DataLad | ~136 GB (1 subj ≈ few GB) | CC_norm, floor 0.3 | **PRIMARY** → 04 |
| Narratives (`ds002345`) | fMRI, spoken stories | 345 (891 scans) | 27 stories, ~4.6h, TR mixed 1.5/1.0s | EN | CC0 | none / none — S3, DataLad | 141.8 GB | vertex ISC (reliability proxy) | **GENERALISATION** → 04 |
| Pereira 2018 (OSF `crwz7`) | fMRI, isolated sentences | 9 (exp2) / 6 (exp3) | 384 / 243 sentences, ~12k / 8k voxels | EN | CC-BY | none / none — HTTP, osfclient | materials 276 MB; **neural responses on a separate host** | in-paper decoding framing | **PILOT** → 04 |
| Le Petit Prince (`ds003643`) | fMRI, audiobook, multi-echo | 49 EN + 35 ZH + 28 FR | same audiobook, native language, ~1.5–2h/subj | EN/ZH/FR | NOT STATED in 04 (OpenNeuro, verify) | none / none | NOT STATED in 04 | NOT STATED | **CANDIDATE** (multilingual bonus) → 04 |
| Narratives reading-listening (denizenslab) | fMRI, paired read+listen | 6 released (9 scanned, 3 withheld) | 11 Moth stories, TR 2.0045s/3T; 3737 train + 291 val TRs | EN | CC0 | none / none — GIN web / git-annex | NOT STATED (likely low-tens GB) | not published; cross-subject acc reported | **CANDIDATE** (fastest open pull) |
| Fedorenko ECoG (`Fedorenko2016`) | ECoG (high-gamma), word-by-word | 5 (neural-nlp) / 4 (paper main) | 52 common sentences, 416 word-presentations | EN | NOT STATED | no public DOI — pulled by neural-nlp from a non-public S3 | <100 MB (est., not stated) | 0.17 (Schrimpf'21) / 0.222 (AlKhamissi'25) | **CANDIDATE** (ms temporal res; small N) |
| Blank 2014 (`Blank2014fROI`) | fMRI, fROI-level, story listening | 5 packaged (22 in paper) | 8 stories, 1317 TRs, 60 neuroids (12 fROI × 5) | EN | NOT STATED | via neural-nlp / brain-score S3 | NOT STATED | ~0.20 / 0.178 (AlKhamissi'25) | **CANDIDATE** (coarse: fROI, not voxel) |
| Harry Potter (Wehbe 2014) | fMRI, word-by-word reading (0.5s/word) | 8 (9 scanned, 1 excluded) | Ch.9 HP, 5176 words, ~1294 stim-TRs, TR 2.0s/3T | EN | data CC0 (Dryad) / paper CC-BY | none / none — Dryad + Google Drive | 356 MB raw `.mat` / ~2.3 GB preproc `.npy` | NOT STATED | **CANDIDATE** (Toneva-standard benchmark) |
| Reading Brain (`ds003974`) | fMRI (TR 0.4s!) + eye-tracking | 52 deposited (Gao used 50) | 5 STEM texts, self-paced sentences | EN | CC0 | none / none — S3 `--no-sign-request`, DataLad | ~46.7 GB | NOT STATED | **CANDIDATE** (fast TR + gaze) |
| Tuckute 2024 | fMRI, isolated 6-word sentences | 14 total (benchmark uses 5-subj avg) | 1000 baseline (+1000 drive/suppress) sentences, TR 2.0s/3T | EN | paper CC-BY-NC-ND; data on OSF NOT STATED (verify) | none / none — OSF `ru38b` | ~28 MB core / ~1.6 GB w/ activations | r = 0.56 (highest of the set) | **CANDIDATE** (curated, high ceiling) |
| Futrell 2018 (Natural Stories) | behavioral self-paced reading times | 181 (uneven completion) | 10 stories, 10,245 tokens / 485 sentences | EN | CC BY-NC-SA 4.0 | none / none — GitHub | NOT STATED (text small; audio dominates) | leave-one-out ISC (graphical only) | **LOW** (no neural data) |

### Low-priority / out-of-scope (recorded once so we don't re-investigate)

| Dataset | Why here | Verdict |
|---|---|---|
| zhu-2025 PNBA data (Safaie macaque M1/PMd spiking; Sensorium-2023 mouse V1 calcium) | cited as alignment work | **OUT** — non-language neural; zero overlap with LLM→fMRI. Data is public (DANDI / g-node) if ever needed. |
| yin-2025 "Association" (`lemonsis/Association`) | brain-alignment paper, sounds like a dataset | **AUX** — it is a synthetic GPT-4 NLP fine-tuning set (1000 story→association samples), *not* neural data. The neural ground truth it aligns to is just Narratives (already above). License: "non-profit research only", no LICENSE file. |

---

## Detailed entries — the candidates worth knowing in depth

The four PRIMARY/GENERALISATION/PILOT/multilingual benchmarks (LeBel, Narratives ds002345, Pereira, Le Petit Prince) are documented in full in `04-data-benchmarks.md` with the power analysis — not repeated here. The six newly-profiled candidates follow.

### Narratives reading-listening — denizenslab (the fast open pull)
Same set `oota-2024`/`oota-2026` used; the one R02 flagged as arguably faster than the LeBel plan. Collected by **Deniz et al. 2019** (*J Neurosci* 39(39):7722, [link](https://www.jneurosci.org/content/39/39/7722)); used for LLM→brain by **Oota et al. 2024**, "Speech language models lack important brain-relevant semantics" (ACL 2024, [link](https://aclanthology.org/2024.acl-long.462/)).
6 subjects released (9 scanned; raw scans for 3 withheld for privacy — only preprocessed derivatives ship, so you cannot re-run preprocessing). 11 Moth Radio Hour stories, each presented as audio AND as RSVP reading at matched word timing — the paired read/listen structure is the unique value. TR 2.0045s, 3T Siemens TIM Trio. 3737 training TRs + 291 validation TRs per modality.
License **CC0** (GIN page, authoritative for the data). No login, no DUA; download via GIN web or git-annex (large files are annexed — a plain `git clone` gets pointer stubs, you need `git annex get`). Size NOT STATED (likely low-tens of GB). No published noise ceiling.
Working code: `github.com/subbareddy248/speech-llm-brain` already wires LLM→fMRI ridge encoding on this exact set. **Caveat:** Moth stories are copyrighted audio — the CC0 covers the fMRI responses/features, not necessarily downstream reuse of the raw WAV.
**Use-case fit:** excellent and low-friction — regression-ready (time × voxels HDF5), paired-modality design lets us test text-vs-speech alignment under confound controls, and there's a working ridge scaffold to build on. Strongest contender to unblock E001's real-data run.

### Fedorenko ECoG — Fedorenko2016
**Fedorenko et al. 2016**, "Neural correlate of the construction of sentence meaning" (*PNAS* 113(41):E6256, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5068329/)). Intracranial ECoG, high-gamma (~70–200 Hz) power averaged per word — direct cortical recording with ms-scale temporal resolution, far tighter than fMRI. Word-by-word RSVP reading (450 / 700 ms per word) with a probe-word memory task (so not pure passive reading).
Subjects: **5 in the neural-nlp package, 4 in the paper's main analysis** — the source of the 5th is undocumented (flag). Electrodes: the widely-cited "97 language-responsive" comes from neural-nlp's S>N criterion; the paper's stricter EOI set is ~51 — different criteria, both in the paper. 52 sentences common to all subjects (the matrix used for alignment), 416 word presentations.
License **NOT STATED**; no public DOI deposit. Access is effectively "use the neural-nlp / brain-score stack," which pulls from a non-public S3 bucket — outsiders would contact the Schrimpf lab. Size <100 MB (estimate, not stated). Noise ceiling **0.17** (Schrimpf'21) vs **0.222** (AlKhamissi'25) — differ, likely split/version. Code: `mschrimpf/neural-nlp` (`Fedorenko2016v3-encoding`), `brain-score/language`.
**Use-case fit:** clean low-noise language signal with word-level temporal detail — good to *validate* that layer-wise alignment is real and probe dynamics, but too few stimuli (52 sentences) to optimize a distillation objective at scale. **Feghhi 2024 specifically shows shuffled splits inflate scores on this set** — contiguous splits mandatory (L003).

### Blank 2014 — Blank2014fROI
**Blank, Kanwisher, Fedorenko 2014**, "A functional dissociation between language and multiple-demand systems…" (*J Neurophysiol* 112(5):1105, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4122731/)). fMRI, naturalistic story listening, **fROI-level** (voxels averaged within language ROIs). TR 2.0s, 3T Siemens Trio.
Subjects: **5 packaged** (22 in the original paper — subset reason undocumented). 8 stories (only 5 story names visible in neural-nlp source — flag), 1317 TRs, **60 "fROIs" = 12 fROIs × 5 subjects** (subject-region combos, not 60 brain regions). License **NOT STATED**; pulled via neural-nlp/brain-score S3. Size NOT STATED. Ceiling ~0.20 / 0.178 (AlKhamissi'25). A voxel-level variant (`Blank2014VoxelEncoding`) exists but is less documented.
**Use-case fit:** the fROI representation is spatially coarse — fine for head-to-head model comparison on a cited benchmark, **not** for voxelwise encoding (it cannot evidence voxel-level correspondence). Lower priority than the voxel-resolution sets.

### Harry Potter — Wehbe 2014
**Wehbe et al. 2014**, "Simultaneously uncovering the patterns of brain regions involved in different story reading subprocesses" (*PLoS ONE* 9(11):e112575, [link](https://doi.org/10.1371/journal.pone.0112575)). fMRI, silent word-by-word reading of Harry Potter Ch.9 at 0.5s/word (4 words/TR). TR 2.0s, 3T Siemens Verio, 3mm iso. 8 subjects (9 scanned, 1 excluded). 5176 words → ~1294 stimulus-locked TRs/subject (the "~1300" shorthand; exact raw TR count NOT STATED).
**Two open hosts, both no-login:** Dryad raw `.mat` (356 MB, minimally processed, CC0) and Google Drive preprocessed `.npy` (~2.3 GB, detrended/smoothed/trimmed; license not formally stated). Data is in native subject space (not MNI). No published noise ceiling. Code: `mtoneva/brain_language_nlp`, `awwkl/brain_language_summarization` (Aw & Toneva). Note: subject letter-codes (F,H,I,…) in the Drive/Toneva version don't map to the Dryad numeric labels — cross-reference carefully.
**Use-case fit:** the de facto standard LLM→fMRI benchmark, already used by both Toneva papers on our reading list — naturalistic narrative, whole-brain, ~1294 TRs/subject, CC0, low-friction. Limitation: single chapter/session, no noise ceiling.

### Reading Brain — ds003974
Acquisition described in **Hsu et al. 2019**, "Neurocognitive signatures of naturalistic reading of scientific texts" (*Sci Rep* 9:10678); used for LLM alignment by **Gao et al. 2025**, "Increasing alignment of LLMs with language processing in the human brain" (*Nat Comput Sci* 5:1080). No standalone data-descriptor paper — three required citations (Hsu'19, Li & Clariana'19, Follmer'18).
fMRI **at TR 0.4s** (multiband ×6, 3T Prisma) — much finer temporal structure than typical 2s sets — **plus co-registered eye-tracking** (fixation durations/saccades, stored in `_events.tsv` columns + a root `.xlsx`, not BIDS `_eyetrack.tsv`). 5 STEM expository texts, self-paced sentence-by-sentence reading. Subjects: **52 deposited, Gao used 50** (likely exclusions). License **CC0**; no login/DUA, S3 `--no-sign-request` or DataLad. Size **~46.7 GB**. Noise ceiling NOT STATED. Code: `RiverGao/scaling_finetuning`.
**Use-case fit:** strong for naturalistic-reading alignment with an independent behavioral channel (gaze) on the same trials, and the fast TR preserves temporal detail. Caveat: self-paced (button-press) means run length varies per subject — complicates time-locked FIR/TRF modeling, but tractable via the events sidecar.

### Tuckute 2024
**Tuckute et al. 2024**, "Driving and suppressing the human language network using large language models" (*Nat Hum Behav* 8:544, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10120732/)). fMRI, passive silent reading of **1000 isolated 6-word sentences deliberately curated for maximal semantic/stylistic diversity** (controls topic/register confounds). TR 2.0s, 3T Prisma, 2mm iso. 14 subjects total; the AlKhamissi benchmark uses the **5-subject training average**.
Noise ceiling **r = 0.56** — the highest of any neuroimaging set in AlKhamissi'25, i.e. real signal headroom for model comparison. Paper CC-BY-NC-ND; code MIT (`gretatuckute/drive_suppress_brains`); **data license on OSF (`ru38b`) NOT STATED — verify before redistribution** (a second OSF link `4tdcx` appeared in search; confirm canonical one). Size ~28 MB core / ~1.6 GB with activations.
**Use-case fit:** strong primary-grade candidate — curated diversity + the highest ceiling in the set make it a clean encoding-model testbed for distillation comparisons.

### Futrell 2018 — Natural Stories (behavioral)
**Futrell et al.** — LREC 2018 ([link](https://aclanthology.org/L18-1012/)) for the corpus; the full data description + reliability is the 2021 journal version (*LRE* 55(1):63, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8549930/)). **Behavioral only — self-paced reading times**, no neural data. 181 participants (uneven completion), 10 stories, 10,245 tokens / 485 sentences, English. License **CC BY-NC-SA 4.0**, public GitHub (`languageMIT/naturalstories`). Reliability via leave-one-out ISC (shown graphically, no summary stat). Known bug: Story-3 RTs were off-by-one before a Nov-2020 fix — avoid stale caches.
**Use-case fit:** relevant only if we add a behavioral-alignment arm (does layer→brain alignment track layer→reading-time alignment?). Otherwise LOW.

---

## Decisions & analysis (this doc)

1. **The literature's substrate is Narratives/Pereira/Fedorenko, not LeBel.** None of the 20 R02 papers used LeBel `ds003020` (our D008 primary). That choice is *ours* (powered deep-sampling), not inherited — worth remembering when we compare our numbers to theirs.
2. **Fastest path to real data is still denizenslab CC0** (R02's recommendation stands after verification): regression-ready, no login, working code. Re-evaluate D008's "LeBel primary" against it before the first real-data run — this is a live open question, not yet decided.
3. **Two highest-ceiling sets are Tuckute (r≈0.56) and the ECoG (0.17–0.22).** Tuckute's curated-diversity design + high ceiling makes it a serious primary candidate; the ECoG is a validation/temporal probe, not a scale target.
4. **Anti-confound is non-negotiable on every one of these (L003).** Feghhi 2024 names Fedorenko2016 and Pereira2018 explicitly as sets where shuffled splits inflate scores. Contiguous splits + nuisance baselines apply to all.
5. **fROI-level Blank is the weakest** of the neural candidates for our purpose (no voxel resolution). Keep as a comparison benchmark only.

## Caveats / open verifications

- **No dataset below has been downloaded or had its license confirmed by inspecting the files** — features are from pages/papers. Confirm before depending on one. Specifically unverified: Tuckute OSF data license, Le Petit Prince license, Fedorenko/Blank licenses (none stated).
- **Recurring subject-count discrepancies** (Fedorenko 4↔5, Blank 5↔22, Reading-Brain 50↔52, Tuckute 5↔14, denizenslab 6↔9) are all real and explained per entry — always state which subset a number refers to.
- This registry records *availability and fit*, not results. Numbers about model performance stay in the canonical notes / R01.
- Distillation-side NLP corpora (GLUE, SQuAD, C4, SlimPajama, DCLM, LongBench, …) are catalogued compactly in `reports/R02` §3 — they're standard HF datasets streamed for baseline matching, not profiled here.


## Related
- [`ladder.md`](./ladder.md) — the canonical status board
- [`map.md`](./map.md) — code system (Q/E/A/D/L) & journey map
