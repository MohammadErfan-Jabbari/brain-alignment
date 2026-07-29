---
title: "Kymata Soto Language Dataset: an electro-magnetoencephalographic dataset for natural speech processing"
tags: [literature]
aliases: [soto-2026_kymata-soto, kymata-soto, kymata-2026]
---

# Kymata Soto Language Dataset: an electro-magnetoencephalographic dataset for natural speech processing

**ChenTianyi Yang, Oliver Parish, Anastasia Klimovich-Gray, Cai Wingfield, William D. Marslen-Wilson, Chao Zhang, Alexandra Woolgar, and Andrew Thwaites / 2026 / Scientific Data** · **Paper:** [DOI: 10.1038/s41597-026-06579-8](https://doi.org/10.1038/s41597-026-06579-8) · **Data:** [OSF `qdzgh`](https://osf.io/qdzgh/)

## TL;DR

Kymata Soto provides simultaneous EEG and MEG while native English and Russian speakers repeatedly hear one approximately seven-minute conversation. The paper reports four presentations for 15 Russian participants and eight for 20 English participants, with six for English participant E8 and a second eight-presentation session for E3. Two presentations occur in each recording block. This repeated, time-resolved, within-participant design makes the dataset unusually well suited to testing whether a spatial estimator can recover a repeat-stable latent signal on recording blocks that were not used to fit it.

The live archive is usable only after an acquisition-integrity gate. E1 is incomplete, E6 has fewer code-3 presentation events than its file count implies, E8 has the reported six presentations, and E2 is the lowest-numbered participant with four task FIFs and eight public presentation events. E2's event onsets nevertheless place every nominal second presentation past the corresponding sidecar `RecordingDuration`. The paper and archive also disagree about the English MEG system, EEG channel count, and license. These are release facts and unresolved metadata problems, not repository evidence that denoising succeeds or fails.

## Paper claims

### The dataset repeats natural conversational speech during simultaneous EEG and MEG

The paper describes raw recordings from 15 native Russian speakers and 20 native English speakers listening to a conversation in their native language. English participants hear an English BBC conversation about ice cream, while Russian participants hear a Russian BBC conversation about coffee. EEG and MEG are recorded simultaneously at 1,000 Hz.

The MEG system has 306 channels arranged as 102 sensor triplets, with one magnetometer and two orthogonal planar gradiometers per triplet. The paper describes EEG acquisition from 70 Ag-AgCl electrodes with a nose reference and also records ECG, horizontal EOG, and vertical EOG for artifact correction.

### Independent presentations are grouped by recording block

The Russian conversation is presented four times in one session. The English conversation is presented eight times in one session, except that E8 receives six presentations. E3 returns for a second session containing another eight presentations. Each recording block groups two presentations with a break between them, and two forced-choice comprehension questions follow each presentation.

Trigger value `3` on `STI101` marks the onset of each conversation presentation. Trigger value `2` marks each second of the visual stimulus, and value `1` marks practice-audio onset. This structure can separate presentation-level repeat agreement from recording-block drift only if the estimator is fitted on some blocks and evaluated on different blocks.

### The release is raw and requires acquisition-aware preprocessing

The paper states that participant recordings are distributed as raw BIDS data and require Signal-Space Separation and/or Maxwell filtering for environmental artifact removal. Five HPI coils and digitized head shapes support head-position monitoring and coregistration. Defaced structural MRI files are supplied for the English cohort, while Russian structural MRI files are withheld under the participant consent language.

## Live archive verification

### The public English cohort does not exactly match the paper's repeat summary

The live English archive contains the regular folders `sub-E1` through `sub-E20` plus `sub-E3b` for E3's second session. Metadata-only traversal found the following load-bearing exceptions:

| Participant | Task FIFs | Code-3 presentation events | Interpretation |
|---|---:|---:|---|
| E1 | 2 | 4 | Incomplete relative to the paper's eight-presentation English design; runs 3 and 4 are absent |
| E2 | 4 | 8 | Lowest-numbered metadata-complete candidate |
| E6 | 4 | 6 | File count implies four blocks, but the public event tables expose only six presentation onsets |
| E8 | 3 | 6 | Matches the exception reported by the paper |

The archived BIDS-validator report explicitly warns that E1 runs 3 and 4 and E8 run 4 are missing. It does not flag E2. This establishes metadata completeness, not neural-data validity.

### E2 has a complete file set and a consistent recorded channel inventory

The E2 folder contains 23 files totaling 6,215,138,610 bytes. It includes four task FIFs, one empty-room FIF, four task event tables, four channel tables, four MEG JSON sidecars, a coordinate-system file, and a defaced T1 image with sidecar. The four task FIFs total 5,895,102,564 bytes, and every live object exposes both a byte count and SHA-256 value through the OSF API.

Every E2 task sidecar reports 1,000 Hz sampling, 306 MEG channels, 64 EEG channels, 2 EOG channels, 1 ECG channel, 17 trigger channels, continuous head localization, five HPI frequencies, and no premarked bad channels. The channel tables refine the MEG inventory to 102 magnetometers and 204 planar gradiometers. They contain 398 rows: the neural and physiological channels, 17 triggers, and eight `MISC` rows including `SYS201`.

The same 64-channel EEG count appears in the channel metadata for all 20 regular English participants. The live computation surface is therefore 64 EEG channels, regardless of the paper's 70-electrode acquisition description.

### The stimulus package supports exact repeat alignment and nuisance construction

The live English stimulus package includes a 154,197,892-byte stereo WAV sampled at 48 kHz as 32-bit floating-point audio. Its RIFF header gives an exact duration of 401.5281667 seconds and SHA-256 `996e9930e24930bb40602651616412b436964d59d6dc765dbb6c3996ef813972`.

The archive provides 1,656 word tokens with 1,656 onset times and 5,097 phoneme tokens with 5,097 onset times. Both timing series extend to 401.5 seconds. The live filenames are `mfa_word.txt`, `mfa_word_stime.txt`, `mfa_phoneme.txt`, and `mfa_phoneme_stime.txt`; the paper instead names the phoneme files with `mfa_phone`. A 2,713,442,247-byte frame archive, SHA-256 `93b17643b80fed3dd0a14c5152baa7cc83e927aa9b4c430be7003707abbdcb19`, contains the visual stimulus frames.

These files make acoustic-envelope, word-onset, phoneme-onset, and visual nuisance models possible. They do not by themselves distinguish linguistic or semantic brain activity from stable sensory responses.

## Release contradictions and blockers

### E2's public event times do not fit its declared run durations

Each E2 task event table contains two code-3 presentation onsets, but the second onset plus the exact WAV duration exceeds the sidecar `RecordingDuration` in every run:

| Run | Code-3 onsets, seconds | Sidecar duration, seconds | Second onset plus WAV duration, seconds |
|---|---|---:|---:|
| 1 | `205.905`, `645.838` | `970.999` | `1047.366` |
| 2 | `66.744`, `512.764` | `906.999` | `914.292` |
| 3 | `73.716`, `513.250` | `904.999` | `914.778` |
| 4 | `74.827`, `521.180` | `903.999` | `922.708` |

One plausible explanation is that the event tables retain a `first_samp / sfreq` offset that `RecordingDuration` does not include. That explanation remains an inference until raw FIF headers and `STI101` are checked. No analysis should crop neural data directly from the public event times or silently subtract a hand-chosen offset.

### The English MEG-system labels conflict

The paper's acquisition section assigns VectorView to the English cohort and Triux to the Russian cohort. The same paper's data-record section and the live archive instead provide `sss_cal_triux.dat` and `ct_sparse_triux.fif` under English, while Russian receives VectorView-named files. The live MEG JSON identifies the manufacturer only as `Elekta Neuromag`, so it does not settle the model.

The English calibration files are small and hashable, but their names are not sufficient evidence of compatibility. Raw sensor names and coil information must match the supplied files, and MNE must accept them during Maxwell filtering. The prose label cannot override the raw header.

### The paper and release disagree about EEG count and license

The paper says 70 EEG electrodes, while all examined English sidecars say 64 recorded EEG channels. The missing distinction may reflect reference, ground, auxiliary, or unreleased channels, but the public files do not establish which explanation is correct. Downstream work must use and report the 64 channels that actually exist.

The paper and OSF node specify CC BY 4.0, while the live `dataset_description.json` says CC0. The conservative interpretation is CC BY 4.0. The stimulus is an excerpted BBC podcast, so local scientific analysis and redistribution should be treated separately; this repository should not redistribute the audio without resolving any underlying third-party rights.

## Relevance to E032

[`E032`](../../experiments/E032_kymata-cross-run-repeat-recovery.md) uses Kymata to ask a narrower question than the paper: can one common spatial filter fitted only on builder recording blocks recover more cross-block repeat-stable MEG signal than a same-dimensional PCA filter and content-destroyed controls? E2 is fixed because it is the lowest-numbered metadata-complete English participant. Runs 1 and 3 are builder blocks, and runs 2 and 4 remain sealed for evaluation.

Kymata is a good substrate for this test because the same participant hears the same 401.528-second audiovisual stimulus eight times, with two presentations per block. A filter that only captures block-local drift, head position, or artifacts should not generalize cleanly to different recording blocks. Simultaneous EEG provides a secondary view under the same acquisition, but it is not an independent replication because both modalities observe the same participant, stimulus, session, motion, attention, and physiology.

The release does not license a denoising score yet. E032 must first verify file hashes, read all four FIF headers without opening neural samples, recover two code-3 triggers per run directly from `STI101`, identify a single prospective timing convention that aligns raw and TSV events within one sample, prove that both full stimulus windows fit, and validate calibration compatibility. Failure ends the experiment at `ACQUISITION/PREPROCESSING FLOOR`; it does not permit switching participants after seeing neural outcomes.

Even a clean E032 pass would establish only a fixed-participant, fixed-story engineering result. It would not establish semantic information, language specificity, participant-population generalization, independent EEG replication, an effective biological loss, a useful loss attachment layer, or a student-training benefit. Those claims require later nuisance-controlled, cross-participant, gradient, layer-placement, and intervention tests under [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md).

## Limitations

1. **One repeated conversation cannot separate every stable cause.** Acoustic structure, visual stimulation, word and phoneme timing, expectation, attention, and adaptation all repeat with the content. Stable neural activity is not automatically language-specific or brain-specific information for a model.
2. **Repetition changes the response.** Habituation, prediction, fatigue, and comprehension can vary systematically across the eight presentations. Alternating builder and evaluation blocks reduces order imbalance but does not make presentations exchangeable.
3. **The first pilot is one participant.** E2 can test whether the estimator is technically viable. It cannot support a participant-population claim.
4. **EEG and MEG are dependent views.** Their agreement can strengthen an acquisition interpretation, but simultaneous measurement is not independent replication.
5. **The data are raw.** Maxwell filtering, head-position handling, bad-channel detection, physiological artifact correction, rereferencing, temporal filtering, and resampling can change repeat agreement. These choices must be fixed before evaluation data are opened.
6. **Metadata completeness is not acquisition integrity.** E2 has the expected files and event count, but the timing contradiction remains unresolved until the raw header and trigger checks pass.
7. **No language-model intervention is tested.** The paper releases a dataset, and E032 tests target recovery. Neither establishes where a biological loss should attach or whether it improves a student model.

## Verified

The paper was read through the full Scientific Data text, including participants, procedure, BIDS data records, MRI, stimuli, trigger definitions, and calibration-file descriptions. The live OSF tree was traversed through its public API without downloading or opening participant neural FIF values. Verification included cohort-level task-file and event counts, all English channel sidecars, E1 and E2 file manifests, E2 event, channel, and MEG JSON files, calibration metadata, BIDS-validator output, timing annotations, and a range read of the WAV header. These checks are external release verification, not a scientific result of this repository.

## Related

- [`01-research-landscape.md`](../../01-research-landscape.md) - authoritative literature frontier map
- [`05-dataset-registry.md`](../../05-dataset-registry.md) - dataset ranking and access record
- [`H002`](../../hypotheses/H002_repeat-stable-biological-supervision.md) - repeat-stable, participant-preserving biological supervision
- [`E032`](../../experiments/E032_kymata-cross-run-repeat-recovery.md) - prospective Kymata cross-run repeat-recovery test
- [`literature/AGENTS.md`](../AGENTS.md) - canonical literature-note contract
