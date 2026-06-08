# Instruction-tuned large language models misalign with natural language comprehension in humans

**Authors:** Changjiang Gao; Zhengwu Ma; Jiajun Chen; Ping Li; Shujian Huang; Jixing Li
**Year:** 2024
**Venue:** bioRxiv preprint
**DOI/arXiv:** 10.1101/2024.08.15.608196
**Canonical ID:** gao-2024_scaling-not-instruction-brain-alignment

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only -> **NOT ACCEPTABLE for canonical notes**

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper tests whether scaling and instruction tuning change how well LLM internal attention patterns align with human reading behavior and brain activity.
2. Core insight: Alignment with eye-tracking and fMRI increases with model scale, but instruction tuning does not improve that alignment in naturalistic reading and instead mainly changes instruction sensitivity.
3. If-wrong breakage: If this conclusion is wrong, model selection for neurocognitive encoding studies could over-prioritize larger base models and under-use instruction-tuned models in settings where they may actually match human processing.
4. Main result location: Results section, especially "Effects of scaling versus finetuning on model-behavior alignment" and "...model-brain alignment" (pp. 5-6), with Figures 3-4 and Table 2 (p. 17).

---

## Source Grounding

The source frames scaling and post-training alignment as two different interventions on language models, then evaluates both against the same human dataset (Reading Brain) using sentence-level attention-to-behavior and attention-to-fMRI regressions. The reported outcome is asymmetric: scale gives monotonic gains in alignment, while instruction tuning mainly changes response to instruction prefixes and does not yield better alignment to naturalistic human reading signals.

## Core Claims

- `C1`: Increasing model size from smaller GPT2/LLaMA variants to larger LLaMA variants improves alignment with both human eye-movement regressions and fMRI regressions during naturalistic reading.
- `C2`: Instruction tuning (Alpaca/Vicuna) does not provide statistically meaningful gains in human behavior or brain alignment over base LLaMA models at matched parameter size.
- `C3`: Instruction-tuned models are more attention-sensitive to explicit instruction prefixes than base models, indicating functional reweighting that is not expressed as better naturalistic alignment.

## Evidence Pointers

- `C1` evidence: Results subsections "Effects of scaling versus finetuning on model-behavior alignment" and "...model-brain alignment" (pp. 5-6); Figure 3A-3B and Figure 4B-4D (p. 17); Table 2 significant cluster contrasts by model size (p. 17).
- `C2` evidence: Same two Results subsections state no base-vs-finetuned advantage at equal size (pp. 5-6); Figure 3C and Figure 4C-4D (p. 17); Discussion summary reiteration (pp. 6-7).
- `C3` evidence: Results subsection "Sensitivity of model attention to instructions" (p. 4); Figure 2C (p. 16); Supplementary Table 3 (p. 19).

## Assumptions and Limits

The study is anchored to one naturalistic reading dataset (50 English readers, STEM texts), one representational channel (self-attention), and one task framing (naturalistic reading with later comprehension questions). It does not test whether instruction-tuned models align better under explicitly instruction-centric human tasks, and it is a preprint rather than a peer-reviewed final version.

## Interpretation Notes

For brain-alignment use cases in naturalistic reading, this source supports a "scale-first" model selection heuristic over an "instruction-tune-first" heuristic. The paper also implies that instruction tuning changes model control behavior in ways that may be orthogonal to core language-comprehension signals measured here.

## Open Questions

- Would the same base-vs-finetuned conclusion hold in experiments where humans process explicit instructions sentence by sentence?
- Does this scaling trend persist for hidden-state or residual-stream regressors, not only attention matrices?
- How robust is the effect across non-English reading datasets and non-STEM text domains?


## Read Date

2026-03-02
