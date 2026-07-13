---
title: "Speech language models lack important brain-relevant semantics"
tags: [literature]
aliases: [oota-2024_speech-lms-lack-brain-semantics]
---

# Speech language models lack important brain-relevant semantics

**Authors:** Subba Reddy Oota; Emin Celik; Fatma Deniz; Mariya Toneva
**Year:** 2024
**Venue:** ACL 2024
**DOI/arXiv:** 10.18653/v1/2024.acl-long.462
**Canonical ID:** oota-2024_speech-lms-lack-brain-semantics

**Tags:** #literature #canonical

---

## Read Method [REQUIRED]

- [x] Full PDF read (page-by-page comprehension)
- [ ] Full PDF scanned (search + targeted read)
- [ ] Extracted text only

PDF verified: 2026-03-02
Comprehension self-check passed: Y

## Comprehension Summary [REQUIRED]

1. Problem solved: The paper asks what information text-based versus speech-based language models are actually mapping to when they align with reading/listening fMRI signals.
2. Core insight: Text models retain late-language alignment after low-level feature removal, but speech models lose late-language alignment to chance once low-level features are removed, while still retaining extra explanatory power in early auditory cortex.
3. If-wrong breakage: If the feature-removal framework does not isolate low-level contributions, the "speech models lack brain-relevant semantics" conclusion is overstated.
4. Main result location: Section 5 with Figure 3 (p.7), Figure 4 and Figure 5 (p.8), Figure 6 and conclusion synthesis (p.9).

## Source Grounding

The study applies a residualization pipeline to remove textual, speech, and visual low-level features from representations of three text-based models (BERT, GPT2, FLAN-T5) and two speech-based models (Wav2Vec2.0, Whisper), then re-estimates voxelwise brain alignment on a paired reading-listening fMRI dataset. Results are reported by early sensory and late language regions, with normalized alignment and significance testing against chance.

## Core Claims

- `C1`: Text-based models keep strong, above-chance alignment in late language regions after low-level feature removal, while their early sensory alignment is largely low-level-feature driven.
- `C2`: Speech-based models lose late-language alignment to chance after low-level feature removal, implying that their late-language predictivity is mostly low-level rather than semantic.
- `C3`: In early auditory cortex, speech models retain substantial alignment even after broad low-level removal, indicating additional captured information beyond the tested feature set; phonological features are the strongest single contributor.

## Evidence Pointers

- `C1` evidence: Section 5.1; Figure 3a (p.7) and feature-removal outcomes in Figure 4a and Figure 5a (p.8).
- `C2` evidence: Section 5.2; Figure 3b (p.7) and late-language residual collapse in Figure 4b and Figure 5b (p.8), reiterated in Section 6 discussion (p.9).
- `C3` evidence: Section 5.2 text and auditory-region analysis (pp.7-8), plus voxelwise phonological-removal impact in Figure 6 (p.9).

## Assumptions and Limits

Feature removal is linear and may leave nonlinear traces; model families are not matched on architecture/training data/objectives; and conclusions are currently anchored to English stimuli and one dataset. The authors explicitly frame these as interpretation limits.

## Interpretation Notes

This paper is a high-value caution for speech-neuro alignment claims: strong raw alignment in late language ROIs is not sufficient evidence of semantic-style processing. For thesis framing, it supports modality-aware evaluation where we separate sensory-feature matching from language-level mapping before making mechanistic claims.

## Open Questions

What training changes let speech models retain late-language alignment after low-level controls? Which additional auditory abstractions explain the residual early-auditory signal beyond the tested feature set? Can jointly trained text-speech models combine text-model late-language strength with speech-model early-auditory strength?


## Read Date

2026-03-02


## Related
- [`status.md`](../../status.md) — the canonical status board
