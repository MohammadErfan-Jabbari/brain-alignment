---
title: "Language-fMRI Benchmarks — Survey, Power, and Recommendation"
tags: [dataset]
---

# Language-fMRI Benchmarks — Survey, Power, and Recommendation

**Last updated:** 2026-06-09 (Session 2). Source: `lit-scout` survey + direct OSF/OpenNeuro
inspection. This resolves the #1 single-point-of-failure flagged in [`01-research-landscape.md`](01-research-landscape.md)
(an open, adequately powered language-fMRI benchmark must be accessible).

## Bottom line

**The SPOF is resolved, and resolved well.** Three adequately powered, openly licensed,
**no-login-required** English language-fMRI benchmarks exist. The charter's data-access kill
condition ("no powered open benchmark accessible") is **not** triggered.

- **Primary (powered, naturalistic): LeBel et al. 2023 — OpenNeuro `ds003020`.** CC0/CC-BY,
  anonymous S3 / DataLad, purpose-built for voxelwise encoding, reported noise ceiling.
- **Generalisation / breadth: Nastase "Narratives" — OpenNeuro `ds002345`.** CC0, 345 subjects.
- **Lightweight plumbing sanity-check: Pereira et al. 2018 — OSF `crwz7`.** CC-BY, tiny, sentence-level.

**One reframe flag (not a kill):** a March-2026 Merlin & Toneva paper already proved the *premise*
behind assumption A3 (brain alignment is functionally load-bearing). We must now differentiate hard
on **compression/distillation at matched budget**, or the novelty narrows. See "Gap check" below.

## The four families

### 1. LeBel et al. 2023 — deep natural-language listening — **PRIMARY** (`ds003020`)
- **License / host:** CC0 in the OpenNeuro snapshot; the paper says CC-BY-4.0, code MIT. Treat data
  as openly reusable; **cite the paper** to be safe. Hosted on OpenNeuro (mirrored to AWS S3 + DataLad).
- **Download friction:** **Zero login, no DUA.** Anonymous S3 (`aws s3 sync --no-sign-request
  s3://openneuro.org/ds003020/ …`), DataLad, or direct HTTPS. Huth lab ships `load_dataset.py`.
- **Size:** ~136 GB full. **Smallest useful slice:** one subject's preprocessed runs ≈ a few GB;
  the GitHub preprocessed bundle ≈ 20 GB. A single subject is pullable in one session.
- **N / depth:** 8 subjects (~27 stories, ~6.2 h each); **3 subjects (UTS01–03) deep-sampled to
  ~82 stories, ~20+ h each**; ~81 h total. TR = **2.0 s**, 3T.
- **Noise ceiling:** **Yes** — regularised normalised correlation (CC_norm), floor 0.3, from
  repeated test-story presentations. This makes the +0.05 win criterion well defined.
- **Language / modality:** English; naturalistic spoken-story listening (The Moth, Modern Love).
- **Power for +0.05 R²:** **Strongly yes — within-subject deep-sampling regime.** ~36k TRs/subject;
  power comes from TRs/voxels per subject, not subject count. A +0.05 R² shift on held-out contiguous
  test stories is comfortably detectable per subject; n=3 gives subject-level replication.
- **Why it matters:** The canonical voxelwise-encoding benchmark; exactly the encoding-model target
  $\mathcal{L}_{\text{brain}}$ needs (A1/A2). Contiguous story-level held-out splits make the
  Feghhi/L003 anti-confound protocol natural.
- **Links:** [Nature Sci Data](https://www.nature.com/articles/s41597-023-02437-z) ·
  [ds003020](https://openneuro.org/datasets/ds003020) ·
  [HuthLab/deep-fMRI-dataset](https://github.com/HuthLab/deep-fMRI-dataset)

### 2. Nastase et al. 2021 — "Narratives" — generalisation/breadth (`ds002345`)
- **License / host:** CC0, OpenNeuro (S3 + DataLad). **No login, no DUA.** 141.8 GB, 4,164 files.
- **N / depth:** **345 subjects, 891 scans, 27 stories**, ~4.6 h unique stimuli. Shallow many-subject.
  TR **mixed across constituent studies (mostly 1.5 s, some 1.0 s)** — heterogeneity is a real cost.
- **Noise ceiling:** Whole-brain vertex-wise leave-one-out **ISC** (a reliability proxy, not a
  per-voxel CC_norm encoding ceiling — you'd convert).
- **Power for +0.05 R²:** **Yes, but across-subject regime** (power from N=345). Best as a
  *generalisation / external-validity* second benchmark, not the primary within-subject testbed.
- **Why it matters:** If a LeBel-trained effect replicates across 345 brains, it directly answers the
  charter's "no universal robustness from one benchmark family" caveat. Mixed TR is a confound to control.
- **Links:** [Nature Sci Data](https://www.nature.com/articles/s41597-021-01033-3) ·
  [ds002345](https://openneuro.org/datasets/ds002345) · [snastase/narratives](https://github.com/snastase/narratives)

### 3. Pereira et al. 2018 — universal decoder — lightweight sanity-check (OSF `crwz7`)
- **License / host:** CC-BY-4.0, OSF (`osf.io/crwz7`). **No login / no DUA**, direct HTTP / `osfclient`.
- **What's actually at crwz7 (verified this session):** `Pereira_Materials.zip` (276 MB) ships the
  **stimulus sentences** (`stimuli_{384,243}sentences.txt`), GloVe sentence vectors
  (`vectors_*.GV42B300.average.txt`), ROI overlap masks (Language/MD/DMN), and the presentation
  materials — but **NOT the per-subject neural responses.** The voxel response matrices
  (`examples_*` per subject) live on a **separate host** (e.g. the brain-score packaging). ⚠️
- **N / depth:** Exp 2: 9 subjects, **384 sentences**, ~12,195 language voxels; Exp 3: 6 subjects,
  **243 sentences**, ~8,121 voxels. One averaged response per sentence per voxel; sentences read 4 s each.
- **Noise ceiling:** Not a per-voxel CC_norm; reliability handled via the in-paper decoding framing.
- **Power for +0.05 R²:** **Marginal / different design.** 384 (Exp2) / 243 (Exp3) stimulus points
  per subject — a sentence-embedding regression, not dense-TR encoding. A clean, cheap sanity-check, not
  the powered primary. Isolated-sentence design sidesteps the temporal-autocorrelation leakage that
  plagues naturalistic data (a Feghhi-relevant plus).
- **Why it matters:** Widely used as the brain-alignment benchmark (Schrimpf, Gao, instruction-tuning
  papers). The lightest possible way to wire and unit-test the $\mathcal{L}_{\text{brain}}$ plumbing.
- **Links:** [Nature Comms](https://www.nature.com/articles/s41467-018-03068-4) · [OSF crwz7](https://osf.io/crwz7/)

### 4. Le Petit Prince multilingual fMRI — cross-lingual bonus (`ds003643`)
- OpenNeuro, no login. **49 EN + 35 ZH + 28 FR** subjects, same audiobook in native language,
  multi-echo fMRI, rich linguistic annotations. Moderate per-subject power (~1.5–2 h). The unique value
  is **multilingual** (the thesis's stated bonus). A newer 7T multi-talker variant exists (`ds005345`).
- **Link:** [Nature Sci Data](https://www.nature.com/articles/s41597-022-01625-7) · [ds003643](https://openneuro.org/datasets/ds003643)

### (Not a fit) Fedorenko / EvLab recent releases
Lipkin et al. 2022 probabilistic language atlas (>800 individuals), EvLab localizer tasks, and the
2025 iFC paper (1,199 brains) are **localizer/atlas resources, not per-stimulus encoding data.** Useful
as a **tool** — restrict $\mathcal{L}_{\text{brain}}$ to language-network voxels via the atlas — but not
a benchmark. Their encoding-grade stimulus data is largely the Pereira set.
[Lipkin 2022](https://www.nature.com/articles/s41597-022-01645-3)

## Comparison table

| Benchmark | License | Login/DUA | Smallest slice | N (regime) | Noise ceiling | Modality / TR | +0.05 R² power | Role |
|---|---|---|---|---|---|---|---|---|
| **LeBel ds003020** | CC0/CC-BY | none | ~few GB (1 subj) | 3 deep + 5 (within-subj) | CC_norm (yes) | fMRI 2.0 s, stories | **Strong** | **Primary** |
| Narratives ds002345 | CC0 | none | ~GB (1 subj) | 345 (across-subj) | ISC | fMRI 1.0–1.5 s, stories | Yes (group) | Generalisation |
| Pereira crwz7 | CC-BY | none | <300 MB (stimuli only) | 9 / 6 (sentence) | in-paper | sentence-avg, 4 s | Marginal | Plumbing test |
| Petit Prince ds003643 | CC0-class | none | ~GB (1 subj) | 49/35/28 | — | multi-echo fMRI | Moderate | Multilingual bonus |

## Recommendation

1. **Primary benchmark: LeBel `ds003020`.** Powered, naturalistic, noise-ceiling reported, open,
   no-login. Pull **one deep-sampled subject (UTS03)** for the first real encoding pilot. This is the
   data the thesis result should be built on.
2. **Generalisation check: Narratives `ds002345`** once an effect exists on LeBel.
3. **Plumbing: Pereira sentences** (already downloaded) for fast harness iteration; needs its neural
   responses fetched from the separate host before it can give a real number.

### Download order (no manual login, executable now)
1. ✅ **Pereira `Pereira_Materials.zip`** (done this session, 276 MB) — gives the real sentences;
   neural responses still to source.
2. **LeBel `ds003020`, one subject** via `aws s3 cp --no-sign-request` or the Huth loader — the real
   powered pilot data. ~few GB; check size before sync, keep under the budget on `/home/centcom/data`.

## Kill / reframe flags

- **No kill on data access.** Every adequately powered English benchmark is CC0/CC-BY, anonymous
  S3/DataLad/OSF, no DUA.
- **⚠️ Reframe — [Merlin & Toneva 2026](literature/canonical/merlin-2026_when-lms-lose-their-mind.md), "When Language Models Lose Their Mind"** ([arXiv 2603.23091](https://arxiv.org/abs/2603.23091)).
  Causally manipulates brain alignment at matched perplexity; brain-misaligned models do substantially
  worse on 200+ downstream tasks. This is the closest published work to **A3** (preserved alignment
  buys something practical) and **supports our premise** — but it is *adversarial fine-tuning of one
  fixed-size model, not distillation/compression*. Our specific loop (alignment as a distillation
  objective beating perplexity-only KD at matched compression budget) is **still untested → gap holds.**
  Action: cite it as the work that proved the premise; sharpen our contribution to the *compression*
  angle so A3 doesn't look scooped. **NOT the `merlin-2024_beyond-next-word` note already on disk.**
- **Adjacent — Moussa/Oota/Toneva 2025 "brain-tuning"** ([ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/95b7a93e60fdfd10cc202f44fd6adf5f-Paper-Conference.pdf),
  [arXiv 2510.21520](https://arxiv.org/abs/2510.21520)). fMRI fine-tuning improves downstream semantics
  and lowers low-level-feature reliance — but **speech, and fine-tuning not distillation.** Pre-empt
  "isn't this just brain-tuning?": our differentiation is text-LLM + compression.
- **Baseline to beat — "Feature Alignment-Based KD"** ([arXiv 2412.19449](https://arxiv.org/abs/2412.19449)),
  model-to-model feature-alignment KD. Slots beside MiniLM/MGSKD in the baseline matrix; our novelty is
  model-to-*brain*.
- **Minor:** LeBel license is reported inconsistently (CC0 snapshot vs CC-BY paper) — cite the paper.
- **Pereira gotcha:** crwz7 is stimuli-only; budget time to source the neural response matrices.

## Hand-off to `paper-digest` (deep notes pending — none yet in `literature/canonical/`)
1. **LeBel et al. 2023** — noise-ceiling computation + preprocessing details (primary benchmark).
2. **Merlin & Toneva 2026 "When LMs Lose Their Mind"** — exactly what it claims vs A3 (reframe trigger).
3. **Nastase et al. 2021 Narratives** — per-study TR table + ISC reliability (generalisation benchmark).


## Related
- [`status.md`](./status.md) — the canonical status board
