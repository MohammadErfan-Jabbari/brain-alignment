---
title: "E028 synthetic Stage-1 development slice implemented"
tags: [timeline, experiment, work, review, e028]
aliases: [e028-synthetic-stage1-development]
---

# E028 synthetic Stage-1 development slice implemented

## Stance

`/work` → `/review` → `/meta`

## What changed

The oracle-cleared, outcome-blind E028 synthetic Stage-1 corrected-evaluator slice now has a canonical development config, a command-denying runner, and a fail-closed analyzer.
The implementation covers absolute-tick/gap-preserving folds, simultaneous embargo, train-only standardization, one-thread float64 grouped ridge, shared nuisance fits, pooled SSE/SST scoring, equal-electrode/equal-source patient aggregation, no-refit leave-outs, and exact Bonferroni sign-flip bound inversion with the literal tie rule.
Both executables run under path/network sentinels and hard-code neural endpoint readiness and Stage-2 licensing false.

## Validation

- Both scripts compile and their built-in fixture suites pass.
- Two 108-cell synthetic replays were byte-identical; the analyzer accepted the schema/support/hash contracts and the deliberately positive fixture exercised the passing statistical branch without licensing Stage 2.
- The local one-thread regression-kernel benchmark passed, but it is not a production-shape benchmark.
- Independent code/conformance and statistical reviews found and drove repairs to config-path safety, zero-variance rejection, analyzer sentinel coverage, sign-root classification, literal-constant freezing, pooled-estimator/RNG/ridge fixtures, and support-bound `n_test` validation.
- Final independent rereviews returned `PANEL-CLEAN: YES` for the synthetic slice and `ENDPOINT-READY: NO`, with no remaining findings.

## Boundary

This milestone validates development plumbing only.
No neural endpoint or author result was downloaded, opened, or scored; no thesis number or manuscript claim was created; and the exact lane, production provider, RFC 8785 chain, factual dimension benchmark, and endpoint-bundle review remain unresolved.

## Related

- [Project status](../status.md)
- [E028 protocol and development evidence](../experiments/E028_vaidya-crossmodal-intervention-falsification.md)
- [E028 canonical development config](../../configs/e028_vaidya_crossmodal_falsification.json)
- [Scripts guidance](../../scripts/AGENTS.md)
