---
title: "Top-venue frontier refresh, 2026-07-02"
tags: [reference]
aliases: [top-venue-frontier-refresh-2026-07-02, venue-refresh]
---

# Top-venue frontier refresh, 2026-07-02

**Status.** This is a `/scout` plus `/plan` memo, not a science verdict and not a ladder update. It records the top-venue contribution search Erfan asked for on 2026-07-02 after orienting on [`ladder.md`](ladder.md), [`expansion-program.md`](expansion-program.md), the current experiment docs, canonical notes, and a live arXiv/conference search.

**Bottom line.** The generic paper is no longer ours: "brain-tuning improves language models" has been taken by speech, text, multilingual, causal-misalignment, and now brain-versus-stimulus comparisons. The defensible open contribution is narrower and stronger: **brain-alignment-guided compression/distillation under severe controls**, asking whether neural supervision changes the alignment/utility frontier at fixed student budget, fixed compute, matched perplexity, and with permuted or non-brain privileged-information twins. That is still not closed by the 2025 to 2026 literature.

## Current repo state

| Area | What we have | Consequence for a paper |
|---|---|---|
| Q0/A2 | [`ladder.md`](ladder.md) records that the linear LM-brain signal survives the project's anti-confound bar. | The measurement signal is real enough to use as an experimental object. |
| Q1/Q2/Q3/Q4 | [`ladder.md`](ladder.md) records partial or negative results for plain KD preservation, induced alignment, per-subject levers, and practical utility. | A naive positive paper is unlikely; the project is currently a rigorous null/methodology spine. |
| Expansion program | [`expansion-program.md`](expansion-program.md) already identified Path A as controlled negative/methodology and Path B as a narrow search for a survivor regime. | The paper should be framed as a frontier test or control protocol, not as "we found brain magic." |
| E016 | [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) made TRIBE synthetic targets usable enough for a Phase-3 KD-scale test, after Phase 2 warned against treating weak synthetic regression targets as a ceiling. | This is the best live gateway experiment: if it is null, the scarcity excuse weakens; if it is positive, it reopens a controlled compression story. |
| E023 | [`E023`](experiments/E023_kd-alignment-objective-vs-quality.md) has only a lower-quality Pythia pilot gate, not a decisive high-quality flat regime. | E023 is useful, but lower priority than the already-running E016 full test. |

## Literature frontier

| Source | Status checked | What it closes | What it leaves open for us |
|---|---|---|---|
| [Moussa et al., 2025](literature/canonical/moussa-2025_brain-tuning-speech-lms.md) ([ICLR/arXiv](https://arxiv.org/abs/2410.09230)) | Canonical note plus live source. | Speech-model fMRI brain-tuning can improve alignment and semantics. | Speech only, no matched student compression/distillation frontier. |
| [Moussa and Toneva, 2025](literature/canonical/moussa-2025b_multi-participant-brain-tuning.md) ([NeurIPS PDF](https://papers.nips.cc/paper_files/paper/2025/file/b0dfbc465fa47c7c31cbfc0f454df460-Paper-Conference.pdf), [arXiv](https://arxiv.org/abs/2510.21520)) | Canonical note plus live source. | Multi-participant fMRI brain-tuning gives a strong data-efficiency story in speech models. | Text-LM compression, KD, and strict matched-budget student baselines remain open. |
| [Negi et al., 2025](literature/canonical/negi-2025_brain-informed-finetuning-multilingual.md) ([NeurIPS/Microsoft](https://www.microsoft.com/en-us/research/publication/brain-informed-fine-tuning-for-improved-multilingual-understanding-in-language-models/), [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.07.07.662360v1)) | Canonical note plus live source. | Brain-informed fine-tuning can improve multilingual downstream metrics. | No compression, and the key downstream comparison is not a perplexity-matched or non-brain-target matched control. |
| [Bilgin et al., 2026](literature/canonical/bilgin-2026_brain-informed-lm-training.md) ([OpenReview](https://openreview.net/forum?id=07S1CPoQYP)) | Canonical note; OpenReview live page was browser-challenge blocked. | Text-LM brain-informed training itself is no longer novel. | Their setup grows or adapts models rather than compressing them; strict shuffled/permuted and matched-quality controls remain the opening. |
| [Merlin and Toneva, 2026](literature/canonical/merlin-2026_when-lms-lose-their-mind.md) ([arXiv](https://arxiv.org/abs/2603.23091)) | Canonical note plus live source. | Causal brain misalignment can preserve LM performance while damaging downstream competence, so alignment can matter causally. | It does not answer whether distillation preserves or can intentionally transfer this factor under student-budget constraints. |
| Merlin, Moussa, and Toneva, 2026, "What Brain Data Adds to Language Model Training" ([ACL Anthology](https://aclanthology.org/2026.conll-main.12/), [OpenReview](https://openreview.net/forum?id=DnBd2X3G5Y)) | Abstract and metadata only; full paper still needs digesting. | Likely closes the broad "does brain data add beyond stimulus tuning?" story for language-model training. | Compression/distillation and the repo's full matched-perplexity, permuted-twin, matched-information control battery are still not covered by the abstract. |
| Zhang et al., 2026, "Temporal Precision Matters" ([ACL PDF](https://aclanthology.org/2026.acl-long.1911.pdf)) | Live PDF skim. | ECoG temporal precision is a credible positive brain-tuning path for speech models, including comparison to distillation baselines. | Text-LM KD and fMRI-derived compression remain open; this is a future modality expansion, not an immediate repo-ready path. |
| [Oota et al., 2026](literature/canonical/oota-2026_brain-encoding-scale-compression.md) ([arXiv](https://arxiv.org/abs/2602.07547)) | Canonical note plus live source. | Post-hoc quantization/pruning often preserve brain predictivity at sufficient scale, so "compression destroys alignment" is false as a blanket claim. | It does not test KD or brain-guided optimization at fixed student budget. This is the strongest reason our paper must be about the frontier, not raw preservation. |
| [Jia, 2026](literature/canonical/jia-2026_lpact-prediction-scores-not-enough.md) ([arXiv](https://arxiv.org/abs/2605.14025)) | Canonical note plus live source. | Generic "prediction scores are not enough" is already a strong 2026 critique. | It audits frozen representations, not training interventions, distillation, or brain-guided compression. |
| "Stimulus dependencies rather than next-word prediction..." ([eLife](https://elifesciences.org/articles/106543)) | Live source. | Naturalistic listening designs can show predictive-looking effects through stimulus dependencies and control-system confounds. | It strengthens our control requirements, but does not close training or compression. |

## Ranked contribution bets

1. **Brain-alignment-guided compression/distillation frontier.** This is the best AAAI/ICML/ICLR/NeurIPS-shaped claim left in scope: take student compression seriously, compare KD-only, brain-guided KD, permuted/synthetic controls, and matched-quality twins, and report the full alignment/utility trade-off rather than a single score. The immediate work item is the active [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) Phase-3 full run, because it tests whether dense synthetic brain targets can move a KD student at corpus scale without fMRI scarcity or target-averaging confounds.

2. **Control-audit paper for recent brain-tuning positives.** If the full CoNLL 2026 paper or Bilgin/Negi code exposes a missing matched-information or permuted-twin control, a careful re-run could be publishable as a field-correcting methodology paper. This is valuable but slower, adversarial, and less thesis-native than E016.

3. **Temporal-precision modality pivot.** ECoG-tuning is now a real positive path, and the ACL 2026 paper makes temporal windows look important. This could lead to a text/KD extension, but it needs dataset and code acquisition before it is a responsible compute bet.

4. **E023 objective-specific shedding.** This remains scientifically relevant, but the current gate only supports a lower-quality Pythia pilot. It should not displace E016 until it has a decisive matched-quality regime.

## Locked next actions

1. **Do not launch another heavy run while E016 is active.** The full E016 Phase-3 run was already alive on 2026-07-02 23:13 UTC, still generating the train cache at roughly 78,688 of 95,999 items. Let it finish train cache, heldout cache, validation, training, and analyzer before starting another GPU-heavy branch.

2. **Use the E016 analyzer as a gate, not a verdict.** A publishable positive requires at minimum the predeclared analyzer readiness gates: at least 3 seeds, scale-ready cache sizes, heldout target metric present, and perplexity within the matched threshold. Even then, the result still needs a post-run stats audit and code review before any science claim.

3. **Read the full CoNLL 2026 paper as soon as the PDF is accessible.** The abstract likely narrows our novelty, but it may also provide the best external control target. A canonical note is needed before it becomes a claim in any report or manuscript.

4. **Scout the ACL 2026 ECoG-tuning repo only after E016 clears or fails.** It is the highest-upside modality pivot, but currently not the cheapest path.

## Must-not-claim

- Do not claim "brain data improves LMs" as novel.
- Do not claim "prediction scores are insufficient" as novel.
- Do not claim E016 proves brain alignment improves downstream utility unless a real downstream or real-brain evaluation is added beyond synthetic target matching.
- Do not claim a null from E016 until the full run, analyzer, and review gates have actually completed.

## Related

- [`ladder.md`](ladder.md) - canonical project status
- [`expansion-program.md`](expansion-program.md) - standing top-venue expansion program
- [`01-research-landscape.md`](01-research-landscape.md) - literature map
- [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) - TRIBE synthetic target experiment
- [`E023`](experiments/E023_kd-alignment-objective-vs-quality.md) - objective-vs-quality experiment
