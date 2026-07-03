---
title: "E016 interpretation protocol, 2026-07-03"
tags: [reference]
aliases: [E016-interpretation-protocol, e016-postrun-protocol]
---

# E016 interpretation protocol, 2026-07-03

**Status.** This is a `/plan` and `/work` precommitment for the active [E016](experiments/E016_tribe-synthetic-brain-targets.md) full Phase-3 run. It was written before the full run produced a run JSON or analyzer JSON. It is not a result, not a report, and not a ladder update.

## Purpose

The active top-venue question is whether brain-alignment-guided compression/distillation changes a fixed-budget KD student's frontier after strict controls. The relevant paper-plan artifacts are [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md), [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md), and [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md). This note freezes the post-run interpretation standard before the E016 numbers are visible.

## Pre-result prior

Before seeing the full E016 artifacts, the conservative prior is that the controlled-null or dense-target-generic branch is more likely than a brain-specific positive. The reason is not E016 evidence (none exists yet), but the recorded project state: [`ladder.md`](ladder.md) says Q2-Q4 have not produced a robust per-individual or practical brain-specific gain under matched controls. E016 can overturn that prior only by passing the analyzer gate and showing stable paired effects under the predeclared contrasts.

## Claim-intent manifests

Use these as the `/interpret` manifest before reading the full analyzer values.

| Branch | Claim to test | Evidence pointer | Overturn-if |
|---|---|---|---|
| Not ready | No E016 science claim is permitted. | Missing or failed `gate.science_ready` in the analyzer JSON. | The analyzer JSON exists and all readiness fields pass. |
| Controlled null | Dense TRIBE targets do not improve fixed-budget KD over KD-only and a block-permuted dense target at matched PPL. | Full run JSON plus analyzer: complete grid, expected seeds, heldout target metric, PPL matching, paired TRIBE-minus-KD and TRIBE-minus-permuted deltas. | TRIBE beats both KD-only and permuted target on the paired contrasts with stable seed-level signs and PPL still matched. |
| PPL-confounded positive | A larger TRIBE target score is not interpretable as a brain-alignment gain because the language-model quality/budget control failed. | Analyzer shows target improvement but `ppl_matched_all_lambdas=false` or per-lambda `ppl_matched=false`. | A rerun or stricter audit shows the target and permuted arms are PPL-matched to KD-only under the predeclared tolerance. |
| TRIBE positive, brain-specificity unproven | TRIBE improves the synthetic target metric beyond KD-only and permuted target, but this is not yet a brain-specific paper claim. | Analyzer gate passes and `paper_branch_hint.branch="tribe_positive_needs_textfeat"`. | The matched-information `textfeat` control also improves similarly, or the positive fails a stats/code audit. |
| Dense privileged-target finding | Dense privileged targets help KD, but brain specificity is unsupported. | TRIBE and text-feature analyzer outputs both pass gates and show similar target-vs-KD/permuted gains. | TRIBE beats the matched-information text-feature target and its permuted twin under the same budget and audit standard. |
| Candidate brain-specific positive | TRIBE beats KD-only, TRIBE-permuted, textfeat, and textfeat-permuted under matched budget. | Completed TRIBE and textfeat analyzer outputs plus post-run stats/code audits. | Extra seeds, real-brain evaluation, or code/stat review removes the effect or reveals a control failure. |

## Required gate checks

Do not interpret a full-run artifact unless [`scripts/analyze_tribe_phase3.py`](../scripts/analyze_tribe_phase3.py) writes `gate.science_ready=true`. Then inspect, not just trust, these fields:

- `gate.enough_seeds`
- `gate.has_lambda_grid`
- `gate.arm_seed_grid_complete`
- `gate.all_paired_common_seeds`
- `gate.ppl_matched_all_lambdas`
- `gate.has_heldout_target_metric`
- `gate.scale_ready`, including train size, heldout size, and target dimension subfields
- per-lambda `paired.*.ppl_matched`
- per-lambda paired delta `values`, `all_positive`, `mean`, `ci95`, and `sign_flip_p_two_sided`
- `paper_branch_hint`, as a routing label only

With three seeds, the sign-flip p-value is a sanity check, not sufficient evidence for a top-tier positive by itself. A positive branch needs either the textfeat control plus additional inference strength, or a careful bounded claim that stops before brain-specificity.

## Commands

Monitor the active run:

```bash
uv run python scripts/e016_phase3_status.py --pretty
```

Guarded post-run finalizer. This is safe to run before the full artifact exists; it exits with `run_json_missing` and tells you to keep monitoring. Once the run JSON exists, it runs or refreshes the analyzer and readiness-packet helper:

```bash
uv run python scripts/e016_finalize_phase3.py
```

If the run JSON exists but the analyzer JSON does not:

```bash
uv run python scripts/analyze_tribe_phase3.py \
  outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.json \
  --out outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json
```

Then read the analyzer JSON before any prose claim:

```bash
uv run python - <<'PY'
import json
from pathlib import Path

p = Path("outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json")
d = json.loads(p.read_text())
print(json.dumps({"gate": d["gate"], "paper_branch_hint": d.get("paper_branch_hint"), "paired": d.get("paired")}, indent=2))
PY
```

For a compact `/interpret` handoff packet:

```bash
uv run python scripts/e016_make_readiness_packet.py \
  outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json
```

## Branch actions

- If `paper_branch_hint.branch="not_ready"`, stay in `/work`: debug missing grid rows, failed scale gates, missing target metrics, or PPL mismatch before interpretation.
- If `paper_branch_hint.branch="controlled_null_candidate"`, switch to `/interpret`: run the stats/code audit, reconcile seed-level paired deltas, and only then decide whether the controlled-negative paper branch is real.
- If `paper_branch_hint.branch="tribe_positive_needs_textfeat"`, do not claim brain specificity. Confirm the active TRIBE run is complete and resources are free, then run the queued text-feature launcher.
- If a textfeat analyzer writes `matched_information_control_ready`, compare it against the completed TRIBE analyzer under the same manifest before making any paper claim. Use [`scripts/e016_compare_target_controls.py`](../scripts/e016_compare_target_controls.py) for this post-positive comparison.
- If any branch is mixed, write the mixedness down as the finding instead of forcing it into the desired paper shape.

After both TRIBE and textfeat analyzer JSONs are science-ready, run:

```bash
uv run python scripts/e016_compare_target_controls.py \
  --tribe-analysis outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json \
  --textfeat-analysis outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json \
  --out outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.tribe_vs_textfeat.json
```

The comparator compares within-target paired gains over KD and permuted controls. It does not turn synthetic target-R2 into downstream utility and does not replace `/interpret`.

If the comparator exists, include it in the readiness packet:

```bash
uv run python scripts/e016_make_readiness_packet.py \
  outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.analysis.json \
  --comparison-json outputs/E016_tribe/phase3/phase3_full_gpt2_n95999_s0-1-2_lam0.1.tribe_vs_textfeat.json
```

## Must-not-claim

- Do not claim an E016 null or positive until the full run JSON and analyzer JSON exist.
- Do not claim brain specificity from TRIBE alone.
- Do not treat synthetic target-R2 as downstream utility.
- Do not treat PPL-unmatched target gains as alignment gains.
- Do not treat the TRIBE-vs-textfeat comparator's branch hint as a verdict.
- Do not flip a ladder rung from this protocol or from the analyzer. E016 still requires `/interpret`, review, and Erfan confirmation before any board change.

## Related

- [`top-venue-frontier-refresh-2026-07-02.md`](top-venue-frontier-refresh-2026-07-02.md) - literature frontier
- [`top-venue-paper-plan-2026-07-03.md`](top-venue-paper-plan-2026-07-03.md) - result-contingent paper plan
- [`top-venue-evidence-ledger-2026-07-03.md`](top-venue-evidence-ledger-2026-07-03.md) - claim/readiness ledger
- [`experiments/E016_tribe-synthetic-brain-targets.md`](experiments/E016_tribe-synthetic-brain-targets.md) - active experiment record
- [`ladder.md`](ladder.md) - canonical thesis status
