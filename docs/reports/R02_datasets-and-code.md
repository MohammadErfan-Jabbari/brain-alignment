---
title: "R02 — Datasets & code provenance across the reading list"
tags: [report]
aliases: [R02]
---

# R02 — Datasets & code provenance across the reading list

**Last updated:** 2026-06-09

**Status:** Extracted by 20 parallel subagents reading the actual local PDFs (in `nexus.bak-2026-06-08/assets/literature-fetch/full-read/`). Every dataset/repo below is stated in its paper; "not stated"/"none found" means the paper did not provide it.

**Why this report exists:** the thesis's #1 blocker is *real neural data on disk* (`upspeed.md`). This maps which fMRI/ECoG datasets each paper used, whether they are open, and where to pull them — plus reusable code for both the brain-alignment side and the distillation side.

---

## 1. Brain datasets — the ones that matter (★ = directly pullable, open)

| Dataset | Modality | Size | Open? / access | Used by |
|---|---|---|---|---|
| ★ **Narratives** (Nastase 2021) | fMRI, spoken stories | 345 subj, 27 stories (~4.6 h) | Open, OpenNeuro | oota-2023, yin-2025, alkhamissi-2025 |
| ★ **Narratives reading-listening** (denizenslab) | fMRI, paired read+listen | 9 subj, Moth Radio Hour, 3737+291 samples | **Open, CC0** — `gin.g-node.org/denizenslab/narratives_reading_listening_fmri` | oota-2024, oota-2026 |
| ★ **Pereira 2018** | fMRI, sentences | 9 subj (exp1) / 6 subj (exp2) | Open, **CC BY** — via `neural-nlp` repo | feghhi-2024, alkhamissi-2025 |
| ★ **Fedorenko ECoG** | ECoG, sentences | 5 subj, ~97 electrodes | Open, **MIT** — via `neural-nlp` repo | feghhi-2024, alkhamissi-2025 |
| ★ **Blank 2014** | fMRI, Natural Stories | 5 subj, 8 stories, 60 fROIs | Open, CC BY-NC-SA — via `neural-nlp` | feghhi-2024, alkhamissi-2025 |
| ★ **Harry Potter** (Wehbe 2014) | fMRI, narrative reading | 8 subj, ~1300 samples each | Open, public | merlin-2024, aw-2023 |
| ★ **Reading Brain** (ds003974) | fMRI + eye-tracking, STEM reading | 50 subj | Open, OpenNeuro `ds003974` | gao-2024 |
| **Tuckute 2024** | fMRI, sentences | 5 subj, 1000 sentences | "publicly available" | alkhamissi-2025 |
| **Futrell 2018** | self-paced reading times (behavioral) | 180 ppl, 10 stories | public | alkhamissi-2025 |

**Takeaways for our blocker:**

- The fastest open pull is **Narratives reading-listening (denizenslab, CC0, 9 subjects)** — it's the exact set `oota-2024`/`oota-2026` used, downloadable from a g-node GIN URL with no login, and `oota-2024`'s code already wires LLM→fMRI on it. That is a strong alternative to the LeBel `ds003020` plan in `upspeed.md`, and arguably faster.
- **Pereira / Fedorenko / Blank** all come bundled through the `neural-nlp` repo (the Brain-Score lineage) with explicit open licenses — note `feghhi-2024`'s own anti-confound code (`beyond-brainscore`) is built against exactly these.
- None of these 20 papers actually used **LeBel ds003020** (our current D008 primary). Worth knowing: the powered-primary choice is *our* call, not something inherited from this literature. Narratives is the more common substrate here.

---

## 2. Code we can reuse

### Brain-alignment pipelines (encoding model + anti-confound)

| Repo | What it gives us | Paper |
|---|---|---|
| `github.com/subbareddy248/linguistic-properties-brain-alignment` | Ridge voxelwise encoding + linear property-removal, BERT/GPT-2, Glasser parcellation | oota-2023 |
| `github.com/subbareddy248/speech-llm-brain` | Feature-removal / residualization pipeline on the reading-listening set | oota-2024 |
| `github.com/gab709/brain-llm-beyond-next-word` | Two-perturbation contrast (scramble + stimulus-tune) + alignment analysis | merlin-2024 |
| `github.com/awwkl/brain_language_summarization` | Ridge encoding + LM-loss controls across layers/context-lengths | aw-2023 |
| `beyond-brainscore` (GitHub) | **Banded ridge + contiguous splits + nuisance baselines** — the L003 protocol, reference impl | feghhi-2024 |
| `github.com/RiverGao/scaling_finetuning` | Attention/hidden-state → eye+fMRI regression (torch 2.2, mne) | gao-2024 |
| `github.com/lemonsis/Association` | Brain-alignment scoring (GPT-2/LLaMA-2→fMRI) + LoRA/frozen fine-tune + Association dataset | yin-2025 |
| `github.com/zhuyu-cs/PNBA` | Probabilistic neural-behavioral alignment (non-language, monkey/mouse) | zhu-2025 |
| Brain-Score framework + `language-to-cognition.epfl.ch` | Standardized linear-predictivity brain-scoring; checkpoint trajectory study | alkhamissi-2025 |

### Representation-similarity / candidate alignment-loss

| Repo | What it gives us | Paper |
|---|---|---|
| `github.com/minyoungg/platonic-rep` | **CKA + mutual-kNN alignment metrics** — direct candidates for $\mathcal{L}_{\text{brain}}$ (D010) | huh-2024 |
| (no repo) | CKA defined in-paper (linear + RBF); reimplement from eqns | kornblith-2019 |

### Distillation / compression baselines

| Repo | What it gives us | Paper |
|---|---|---|
| `aka.ms/minilm` (microsoft/unilm) | KD code **+ released distilled checkpoints** (6L/768, 12L/384, …) | wang-2020 |
| `github.com/LC97-pku/MGSKD` | Multi-granularity structural KD (token/span/sample) | liu-2022 |
| `github.com/JetRunner/MetaDistil` | Meta-learning teacher adaptation | zhou-2022 |
| `github.com/jiachenwestlake/MMKD` | Adversarial moment-matching KD training loop | jia-2024 |
| built on `OpenRLHF` (no own repo) | Token-level alignment-as-distillation recipe | zhang-2025 |
| none found | LRC-BERT contrastive KD (reimplement) | fu-2021 |
| none found (uses lm-eval-harness) | calibration-data-for-pruning findings only | ji-2025 |
| none found | RazorAttention is training-free; algorithm in-paper | tang-2025 |

---

## 3. Distillation/compression — datasets used (so we match baselines fairly)

These are standard NLP benchmarks, all open: **GLUE** (wang-2020, liu-2022, fu-2021, zhou-2022), **SQuAD 2.0 / CNN-DM / XSum / XNLI** (wang-2020), **Dolly-15K / OpenWebText / SAMSum / IWSLT'17 / StrategyQA** (jia-2024), **UltraFeedback / TL;DR** (zhang-2025), **C4 / Wikipedia / SlimPajama / DCLM** as pruning calibration corpora (ji-2025), **LongBench / Needle-in-Haystack** (tang-2025). CKA/Platonic use vision sets (CIFAR, ImageNet, VTAB, Places-365) — not relevant to us except the metric code.

---

## 4. What to actually pull (actionable)

1. **Real neural data, fastest open path:** clone the reading-listening fMRI set from `gin.g-node.org/denizenslab/narratives_reading_listening_fmri` (CC0, 9 subj) and pair it with `oota-2024`'s `speech-llm-brain` pipeline. This unblocks E001's real-data run without waiting on the LeBel S3 pull — re-evaluate D008's "LeBel primary" against this.
2. **Anti-confound reference:** read `beyond-brainscore` (feghhi) against our `pilot_lib.py` to confirm our banded-ridge / contiguous-split impl matches the field's reference.
3. **Alignment-loss prototyping (D010):** lift CKA + mutual-kNN from `platonic-rep` as the first $\mathcal{L}_{\text{brain}}$ proxy candidates.
4. **Distillation baseline:** start from MiniLM's released checkpoints (`aka.ms/minilm`) rather than distilling from scratch.

---

## 5. Gaps / caveats

- **Repos not yet verified live.** URLs are as stated in the papers; none have been cloned or checked for license/runnability this pass. Verify before depending on one.
- **`feghhi` repo URL is a name, not a full link** ("beyond-brainscore on GitHub") — resolve the exact org before use.
- **`oota-2026` released no code** — only "models on HuggingFace." Reproducing its compression sweep means reimplementing.
- **`zhu-2025` datasets are non-language** (monkey M1/PMd, mouse V1) and referenced, not directly linked — low priority for us.
- This report is provenance only; it does not re-verify any *result*. Numbers stay in the canonical notes / R01.
</content>


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
