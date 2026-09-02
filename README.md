---
title: "brain-alignment — MSc thesis research repo"
tags: [reference, charter]
aliases: [brain-alignment, home]
---

# Evaluating Brain Alignment as a Training Signal for Language Models

Research code, evidence records, and manuscript source for an MSc thesis (Machine Learning for
Health, Universidad Carlos III de Madrid).

[![Thesis PDF](https://img.shields.io/badge/thesis-PDF%20(57%20pp.)-8A2BE2)](docs/manuscript/submission/main-submission.pdf)
[![Python](https://img.shields.io/badge/python-3.11-blue)](pyproject.toml)
[![Package manager](https://img.shields.io/badge/deps-uv-261230)](https://docs.astral.sh/uv/)

---

## The question

Language-model representations can predict human brain responses to language recorded with fMRI.
That is a measurement result. It does not show the responses can *improve model training*.

This thesis tests the training claim directly: does adding recorded fMRI responses — or synthetic
brain responses generated from text — as an auxiliary objective alongside knowledge distillation
give a smaller student model an advantage that comes **specifically from brain-response content**?

## What was found

Five claims are kept apart, because none of them establishes another.

| Claim | Question | Status |
| --- | --- | --- |
| **Measurement** | Can frozen LM representations predict held-out recorded responses beyond nuisance features? | **Supported** on both datasets |
| **Manipulation** | Does the auxiliary objective change the retained student? | **Supported** for the synthetic route |
| **Attribution** | Is that change specific to brain-response content? | **Non-identifying comparator** |
| **Transfer** | Does it improve prediction of independently recorded responses beyond plain KD? | **Not demonstrated** |
| **Utility** | Does it help a practical endpoint at comparable LM quality? | **Not demonstrated** |

Neither route establishes brain alignment as a usable training signal, and neither rules out a
benefit from different targets, interventions, or populations. The contribution is the separation
that keeps a valid positive result at one stage from being read as support for the training claim.

Full statuses, estimands, and uncertainty are in
[Section 4 of the thesis](docs/manuscript/submission/main-submission.pdf).

## Repository layout

| Path | Contents |
| --- | --- |
| [`docs/manuscript/submission/`](docs/manuscript/submission/) | The submitted thesis: LaTeX source and `main-submission.pdf` |
| [`docs/manuscript/rewrite/`](docs/manuscript/rewrite/) | Canonical manuscript source; single source of `numbers.tex`, `acronyms.tex`, `references.bib` |
| [`docs/experiments/`](docs/experiments/) | One evidence record (`E001`–`E033`) per experiment: design, kill criteria, results, verdict |
| [`docs/status.md`](docs/status.md) | Operational state and next actions |
| [`docs/decisions/`](docs/decisions/) · [`docs/learnings.md`](docs/learnings.md) | Why the project changed course, and what went wrong on the way |
| [`docs/literature/`](docs/literature/) | Canonical notes on the papers the thesis relies on |
| [`scripts/`](scripts/) | Experiment runners, analysis, figure builders, manuscript gate |
| [`configs/`](configs/) | Experiment configurations |
| [`tests/`](tests/) | Apparatus checks |
| `data/`, `outputs/` | Heavy artifacts — gitignored, not distributed |

`docs/` is both GitHub Markdown and an Obsidian vault. Folder-level contracts live in `AGENTS.md`
files, not in READMEs.

## Setup

```bash
uv sync                                        # Python 3.11, torch cu128
export HF_HOME=/path/to/your/hf-cache          # reuse cached models
uv run python -c "import torch; print(torch.cuda.device_count())"
```

Everything runs through `uv run`. The reference environment is a single node with 4× NVIDIA L40S
(46 GB each); no Slurm, Docker, or job scheduler is involved.

## Running an experiment

Each runner belongs to an evidence record, which owns its exact command, seeds, and decision rules.
**Read the record first** — the runner alone does not tell you what the numbers are allowed to mean.

| Runner | Experiment |
| --- | --- |
| `scripts/run_toy_pilot.py` | [E001](docs/experiments/E001_toy-pilot-gpt2.md) — end-to-end pipeline validation on synthetic responses |
| `scripts/run_kd_alignment.py` | [E003](docs/experiments/E003_kd-alignment-preservation.md) — distillation headroom |
| `scripts/run_brain_lever.py` | [E005](docs/experiments/E005_alignment-guided-kd-tradeoff.md), [E008](docs/experiments/E008_per-participant-f1-solidification.md) — recorded-response intervention |
| `scripts/run_lebel_tune.py` | [E013](docs/experiments/E013_open-frontier-multisubject-naturalistic.md), [E017](docs/experiments/E017_matched-ppl-control-on-braintuning-gain.md) — naturalistic voxelwise routes |
| `scripts/run_tribe_phase3.py` | [E016](docs/experiments/E016_tribe-synthetic-brain-targets.md) — synthetic-response intervention |
| `scripts/e025_participant_transfer.py` | [E025](docs/experiments/E025_participant-e016-biological-transfer.md) — saved-student biological transfer |
| `scripts/e030_exact_substrate_transport.py` | [E030](docs/experiments/E030_exact-substrate-transport-diagnostic.md) — linear target-projection assay |

### What is not reproducible from this repository alone

Stated plainly, because it bounds what you can check:

- **The fMRI data is not redistributed.** The Tuckute condition-B and LeBel story-listening corpora
  must be obtained from their original sources. Appendix B of the thesis specifies the exact
  inclusion, preprocessing, and partition rules applied to them.
- **Model weights and run outputs are gitignored.** `data/` and `outputs/` hold hundreds of
  gigabytes and are not distributed.
- **Early runs do not pin Hugging Face model revisions.** Exact historical replay depends on a
  retained model cache, as Appendix C records.

## Where the numbers come from

Every load-bearing number in the thesis is traceable in one direction:

```
run artifact  →  E-record (docs/experiments/ENNN_*.md)  →  numbers.tex key  →  \result{key} in the manuscript
```

A number is born in an experiment, adjudicated in its record, declared once as a key, and cited by
key in the prose. A missing value is a visible `\gap`, never a reconstruction. To chase any figure
in the PDF, grep its key in [`docs/manuscript/rewrite/numbers.tex`](docs/manuscript/rewrite/numbers.tex)
and follow the `% [ENNN]` provenance tag to the owning record.

## Building the thesis

```bash
cd docs/manuscript/submission
latexmk -pdf main-submission.tex     # run twice: float placement needs a second pass to converge
```

Requires TeX Live 2023 or newer. **Use `latexmk` only** — Tectonic ships a `biblatex` that
disagrees with the system `biber` and silently corrupts the build. Verify with
`pdfinfo main-submission.pdf | grep Producer`, which must read `pdfTeX`.

Checks:

```bash
uv run python scripts/manuscript_check.py docs/manuscript/submission   # evidence + number + build gate
uv run python scripts/prose_lint.py --selftest
uv run python tests/test_bash_gate.py
```

## Citation

```bibtex
@mastersthesis{jabbari2026brainalignment,
  author = {Jabbari, MohammadErfan},
  title  = {Evaluating Brain Alignment as a Training Signal for Language Models},
  school = {Universidad Carlos III de Madrid},
  year   = {2026},
  type   = {Master's thesis},
  note   = {MSc in Machine Learning for Health}
}
```

## License

The thesis text is licensed under Creative Commons **Attribution–NonCommercial–NoDerivatives**, as
stated on its cover page. No license is currently set for the code in this repository.

## Contact

MohammadErfan Jabbari — `mohammaderfan.jabbari@networks.imdea.org`

<sub>Supervised by Alejandro Lancho Serrano and Pablo Martínez Olmos (UC3M), with Marco Fiore and
Claudio Fiandrino (IMDEA Networks).</sub>
