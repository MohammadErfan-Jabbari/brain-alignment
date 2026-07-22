---
title: "E028 Vaidya artifact-request email"
tags: [reference]
aliases: [e028-vaidya-artifact-request-email]
---

# E028 Vaidya artifact-request email

**Status:** Sent 2026-07-22 from the connected Gmail account to corresponding author Aditya R. Vaidya (`avaidya@utexas.edu`), with Richard J. Antonello (`rja2163@columbia.edu`) and Alexander G. Huth (`alex.huth@berkeley.edu`) copied, after Erfan's explicit approval. Gmail message/thread ID: `19f88eb5e4dffa8a`.

**Response checkpoints:** Inspect the thread on 2026-08-05, ten business days after sending. If there is no substantive response, send one concise follow-up in the same thread. On 2026-08-12, fifteen business days after sending, choose explicitly between a labeled independent reimplementation and closing the exact lane as unavailable; silence is never recorded as reproduction failure.

## Subject

Artifact request for a preregistered reproduction of arXiv:2605.19224

## Draft

Dear Aditya, Richard, and Alexander,

I am preparing an independent, preregistered reproduction and controlled extension of your preprint, "Fine-tuning Language Encoding Models on Slow fMRI Improves Prediction for Fast ECoG" (arXiv:2605.19224). The first goal is to reproduce your reported fMRI-to-ECoG result exactly before applying participant-level inference, nested lag selection, and auxiliary-target controls. I will clearly distinguish an exact reproduction from a public-data reimplementation and will cite your paper and released resources.

Would you be willing to share the following artifacts, or point me to their public location?

1. The exact training and ECoG-evaluation code commit, environment lock, launch commands, and any uncommitted patch used for the preprint.
2. The initial WavLM Base+ model identifier and revision, processor/configuration, file hashes, LoRA target modules and hyperparameters, layer indexing, audio windowing/downsampling, and alignment offsets.
3. The exact OpenNeuro snapshots, source-participant mapping, voxel masks, and train/validation/test story lists.
4. The three principal subject-specific LoRA checkpoints, selected epoch and validation record for each, plus any downsampled-fMRI or data-scaling checkpoints needed for the reported panels.
5. The ECoG preprocessing manifest, 1,268-electrode inclusion and ROI table, four-fold boundaries, ridge grid, 81-lag grid, lag-selection code and scope, and random states.
6. A full-precision electrode-by-participant result table containing pretrained and each fMRI-source-model score, selected lag, ROI, and fold-level score or out-of-fold prediction pointer, together with the numeric values behind the load-bearing figures.
7. SHA-256 values and redistribution terms for the supplied code, checkpoints, tables, and manifests.

I will freeze the study design before opening the disaggregated ECoG outcomes. If sharing patient-level tables is inconvenient, a script that regenerates them from ds005574 would be sufficient. I would also be glad to share the preregistration and exact reproduction discrepancies with you before public release.

Thank you for considering the request, and for making both the scientific question and underlying datasets accessible.

Best,

Erfan

## Related

- [E028 design](../experiments/E028_vaidya-crossmodal-intervention-falsification.md)
- [Canonical Vaidya et al. note](../literature/canonical/vaidya-2026_slow-fmri-fast-ecog-transfer.md)
