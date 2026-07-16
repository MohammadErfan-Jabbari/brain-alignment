---
title: "E026 target-control identification audit"
tags: [timeline, work, interpret, E026]
aliases: [E026-control-identification]
---

# E026 target-control identification audit

## Stance

`/work` → `/interpret` → `/write`

## What happened

- Froze and independently reviewed the complete E026 manifest, then ran the no-training target-geometry and retained-student movement audit on GPU 3.
- Compared the saved 20,484-dimensional TRIBE and projected text-feature targets on two disjoint deterministic 4,096-item samples, the untouched E016 train/held-out split, and six retained training seeds.
- Added a separate checker that does not import the evidence runner. It reconstructed all 55 check states and rehashed 128 dependencies totaling 34,958,676,977 bytes.
- Integrated the settled result into the E record, D059, project status, extended manuscript, and a new four-panel identification-chain figure. The frozen public cut was not changed.

## Evidence

- Reviewed manifest: `outputs/E026/e026_manifest.json`, SHA-256 `a2bbf93f839b8e787716e325b198062e159dd7089e5725249647d806f425ad1f`.
- Main audit: `outputs/E026/e026_audit.json`, SHA-256 `dfac7498d89d488483f129ebd30f36013d98778a8304f0d3d97d9e0a8c1932ad`.
- Independent audit: `outputs/E026/e026_independent_result_audit.json`, SHA-256 `b2dca54c87efeca60c78a0de8287b4571991dcf3e653ce17dacc60583d2fda9f`.
- Independent checker: `scripts/e026_independent_result_audit.py`, SHA-256 `cf701aa8bab3016701ac7a6575ea58c36d9153ae048dae5e4fb3dd6580635f26`.
- Verification: PASS, zero mismatches and zero dependency-hash failures; 24 PASS, 30 FAIL, one UNRESOLVED.

## Verdict

The saved text-feature comparator is non-comparable to TRIBE on the frozen measured pretraining and trained-movement axes. The largest failures are KD target baseline and remaining headroom, covariance spectrum and effective rank, low-level nuisance predictability, global parameter movement, and layer-6 centered-Frobenius movement. Standardized global scale, most valid order diagnostics, power-spectrum shape, static-unique predictability, and four of six CKA checks pass, so the result is a specific identification failure rather than total non-parity.

E016 retains a valid within-TRIBE target-learning result, but its cross-target TRIBE-minus-textfeat gain cannot identify brain-derived content. E026 does not prove information inequivalence or explain E025's endpoint results. Together, E025 and E026 establish the internal Package A dissociation: target learning and model movement pass, comparator identification fails, the primary relative activation contrast is bounded below its predeclared effect, and direct TRIBE-minus-KD is near zero for the tested cohort.

## Next

Keep E027 and Package C closed. Keep Package B on HOLD. Use an exact-substrate Tuckute transport diagnostic to distinguish proxy/domain nontransport from directional-utility failure, and make E028's faithful external reproduction plus corrected participant analysis the binding top-venue gate.

## Related

- [E026](../experiments/E026_tribe-textfeat-target-comparability.md)
- [E025](../experiments/E025_participant-e016-biological-transfer.md)
- [D059](../decisions/decisions.md#d059-e026-closes-the-saved-text-feature-comparator-as-an-identified-cross-target-control-2026-07-17-work--interpret)
- [Project status](../status.md)
