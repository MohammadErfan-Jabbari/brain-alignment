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
| [Merlin, Moussa, and Toneva, 2026](literature/canonical/merlin-2026_what-brain-data-adds.md), "What Brain Data Adds to Language Model Training" ([ACL Anthology](https://aclanthology.org/2026.conll-main.12/), [PDF](https://aclanthology.org/2026.conll-main.12.pdf)) | Full ACL PDF extracted and scout-digested. | Closes the broad "brain data adds beyond stimulus text" story for BERT/GPT-2 LoRA fine-tuning: Brain-Tuned beats Stimulus-Tuned, and Jointly-Tuned beats pretrained on Holmes/FlashHolmes probes. | No compression, no KD-only student, no matched-perplexity or matched-information twin, and no permuted/shuffled-brain control. The open cell is now specifically the matched student-budget distillation frontier, not generic brain-tuning. |
| [Zhang et al., 2026](literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md), "Temporal Precision Matters" ([ACL PDF](https://aclanthology.org/2026.acl-long.1911.pdf)) | Live PDF scan plus code-repo inspection. | ECoG temporal precision is a credible positive brain-tuning path for speech models, including comparison to distillation baselines. | Text-LM KD and fMRI-derived compression remain open; this is a future modality expansion, not an immediate repo-ready path. |
| [Xiao et al., 2026](literature/canonical/xiao-2026_brain-guided-llm-reasoning.md), "Beyond representational alignment with brain-guided language models for robust reasoning" ([arXiv](https://arxiv.org/abs/2606.11893), [code](https://github.com/pkuxmq/Brain-guided_LLM)) | Live arXiv HTML scan plus public code-repo inspection. | Closes more of the broad utility story: task-fMRI-derived representation directions can guide inference-time interventions and fine-tuning for LLM reasoning, with random-signal and label-only controls. | No compression, no KD-only student, no matched-perplexity or matched-information control. The remaining opening is not "brain signals can help LLMs", but whether they help **smaller students** under strict compression controls. |
| Chen and Sivakumar, 2026, "The Mind's Transformer" ([GitHub](https://github.com/cheng-yeh/MindTransformer), [OpenReview](https://openreview.net/forum?id=PgIlCCNxdB)) | Search result plus public code README; OpenReview PDF fetch was blocked. | ICLR 2026 alignment measurement has moved inside transformer blocks: 13 intermediate states and multi-state integration improve encoding, with the README claiming a 31% primary-auditory-cortex gain. | Measurement pressure only. It does not train LMs, distill students, or test whether alignment guidance changes utility under compression. It does suggest our final paper should be careful about which representation state the alignment objective/evaluator uses. |
| [Oota et al., 2026](literature/canonical/oota-2026_brain-encoding-scale-compression.md) ([arXiv](https://arxiv.org/abs/2602.07547)) | Canonical note plus live source. | Post-hoc quantization/pruning often preserve brain predictivity at sufficient scale, so "compression destroys alignment" is false as a blanket claim. | It does not test KD or brain-guided optimization at fixed student budget. This is the strongest reason our paper must be about the frontier, not raw preservation. |
| [Jia, 2026](literature/canonical/jia-2026_lpact-prediction-scores-not-enough.md) ([arXiv](https://arxiv.org/abs/2605.14025)) | Canonical note plus live source. | Generic "prediction scores are not enough" is already a strong 2026 critique. | It audits frozen representations, not training interventions, distillation, or brain-guided compression. |
| "Stimulus dependencies rather than next-word prediction..." ([eLife](https://elifesciences.org/articles/106543)) | Live source. | Naturalistic listening designs can show predictive-looking effects through stimulus dependencies and control-system confounds. | It strengthens our control requirements, but does not close training or compression. |

## Ranked contribution bets

1. **Brain-alignment-guided compression/distillation frontier.** This is the best AAAI/ICML/ICLR/NeurIPS-shaped claim left in scope: take student compression seriously, compare KD-only, brain-guided KD, permuted/synthetic controls, and matched-quality twins, and report the full alignment/utility trade-off rather than a single score. The immediate work item is the active [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) Phase-3 full run, because it tests whether dense synthetic brain targets can move a KD student at corpus scale without fMRI scarcity or target-averaging confounds.

2. **Control-audit paper for recent brain-tuning positives.** If the full CoNLL 2026 paper or Bilgin/Negi code exposes a missing matched-information or permuted-twin control, a careful re-run could be publishable as a field-correcting methodology paper. This is valuable but slower, adversarial, and less thesis-native than E016.

3. **Temporal-precision modality pivot.** ECoG-tuning is now a real positive path, and the ACL 2026 paper makes temporal windows look important. This could lead to a text/KD extension, but it needs dataset and code acquisition before it is a responsible compute bet.

4. **E023 objective-specific shedding.** This remains scientifically relevant, but the current gate only supports a lower-quality Pythia pilot. It should not displace E016 until it has a decisive matched-quality regime.

## Locked next actions

1. **Do not launch another heavy run while E016 is active.** The full E016 Phase-3 run is the live gateway experiment. Use `uv run python scripts/e016_phase3_status.py --pretty` to monitor it, then let it finish train cache, heldout cache, validation, training, and analyzer before starting another GPU-heavy branch.

2. **Use the E016 analyzer as a gate, not a verdict.** A publishable positive requires at minimum the predeclared analyzer readiness gates: at least 3 seeds, scale-ready cache sizes, heldout target metric present, and perplexity within the matched threshold. Even then, the result still needs a post-run stats audit and code review before any science claim.

3. **Treat CoNLL 2026 as frontier closure for generic brain-tuning.** The full paper is now digested. Any paper pitch must concede that brain data beyond stimulus text has been tested for text-LM LoRA fine-tuning, then move immediately to the unmatched compression question: fixed student budget, KD-only, brain-guided KD, permuted target, matched-information non-brain target, matched perplexity or matched utility.

4. **Scout the ACL 2026 ECoG-tuning repo only after E016 clears or fails.** It is the highest-upside modality pivot, but currently not the cheapest path.

## Post-CoNLL experiment logic

The full CoNLL read changes the burden of proof but not the next run. E016 Phase 3 remains the cheapest live gateway because it asks the one question CoNLL, Bilgin, Negi, Moussa, and Oota still do not answer: what happens at a fixed student budget under KD?

Interpret E016 asymmetrically:
- **Null at matched PPL:** strong evidence for the controlled negative paper. Dense TRIBE targets remove the fMRI scarcity/SNR excuse, and the permuted twin checks whether the auxiliary target acts as a generic dense regularizer.
- **Positive at matched PPL:** promising but not yet top-tier-clean. The next arm must be a matched-information non-brain privileged target, for example a stimulus-derived LLM/acoustic/text-feature teacher target with the same dimensionality budget and KD schedule. CoNLL's Stimulus-Tuned arm makes this control non-optional for any "brain-specific" claim.

## Scout updates

- **CoNLL 2026 brain-data-adds target.** The ACL page and PDF are now accessible. The full PDF was extracted locally with PyMuPDF and recorded as [`merlin-2026_what-brain-data-adds`](literature/canonical/merlin-2026_what-brain-data-adds.md). This strengthens the negative novelty verdict on generic brain-tuning: the paper directly compares Brain-Tuned, Stimulus-Tuned, and Jointly-Tuned text LMs. It still leaves the compression/distillation frontier open because it never trains a smaller student, never matches perplexity, and never runs KD-only/permuted/matched-information controls.
- **ACL 2026 ECoG-tuning pivot.** The [`Mochizuki-BUPT/ECoG-Tuning-main`](https://github.com/Mochizuki-BUPT/ECoG-Tuning-main) repo is public, MIT-licensed, and contains trainer code plus expected preprocessing formats. It uses the public [Podcast ECoG dataset](https://openneuro.org/datasets/ds005574), word-level 30 s audio windows, and per-word 200 ms high-gamma ECoG windows for language and speech latencies. This makes the modality pivot feasible to scout, but it remains speech-model ECoG work, not immediate text-LM compression/KD. Canonical note: [`zhang-2026_temporal-precision-ecog-tuning`](literature/canonical/zhang-2026_temporal-precision-ecog-tuning.md).
- **June 2026 brain-guided reasoning paper.** The arXiv paper and [`pkuxmq/Brain-guided_LLM`](https://github.com/pkuxmq/Brain-guided_LLM) code are public. The method uses fMRI-derived representation directions for NARI/NARF intervention and fine-tuning on LLM reasoning. This further rules out a broad "first brain-guided LLM utility" pitch, but it does not touch fixed-budget compression or KD. Canonical note: [`xiao-2026_brain-guided-llm-reasoning`](literature/canonical/xiao-2026_brain-guided-llm-reasoning.md).
- **AAAI/ICML measurement-only scan.** AAAI 2026 includes ["Do Large Language Models Think like the Brain? Sentence-Level Evidences from Layer-Wise Embeddings and fMRI"](https://ojs.aaai.org/index.php/AAAI/article/view/37022), a sentence-level encoding analysis over 14 LLMs and The Little Prince fMRI. The ICML-facing ["Fine-grained Analysis of Brain-LLM Alignment through Input Attribution"](https://arxiv.org/abs/2510.12355) appears on arXiv/OpenReview with public code and an author acceptance notice, but no indexed official ICML proceedings page was found in this scan. Both sharpen measurement and attribution: they do not train, compress, distill, or test fixed student budgets.
- **ICLR 2026 MindTransformer target.** The OpenReview page is browser-challenge blocked and direct PDF fetch returned HTTP 403, but the public repo README is available. Record it as a measurement-method pressure, not as closure of the training contribution: it may change the best alignment readout state, while leaving the student-budget training question untouched.

## Must-not-claim

- Do not claim "brain data improves LMs" as novel.
- Do not claim "brain-derived representation guidance improves LLM behavior" as novel.
- Do not claim "prediction scores are insufficient" as novel.
- Do not claim E016 proves brain alignment improves downstream utility unless a real downstream or real-brain evaluation is added beyond synthetic target matching.
- Do not claim a null from E016 until the full run, analyzer, and review gates have actually completed.

## Related

- [`ladder.md`](ladder.md) - canonical project status
- [`expansion-program.md`](expansion-program.md) - standing top-venue expansion program
- [`01-research-landscape.md`](01-research-landscape.md) - literature map
- [`E016`](experiments/E016_tribe-synthetic-brain-targets.md) - TRIBE synthetic target experiment
- [`E023`](experiments/E023_kd-alignment-objective-vs-quality.md) - objective-vs-quality experiment
