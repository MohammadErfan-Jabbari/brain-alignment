#!/usr/bin/env python3
"""Compare ready E016 TRIBE and text-feature analyzer outputs.

This is a post-positive routing aid, not a verdict engine. It compares
within-target gains over KD/permuted controls and refuses interpretation unless
both analyzer JSONs are science-ready.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_tribe_phase3 import paired_delta_stats


POST_TEXTFEAT_POSITIVE_REVIEWER_BURDEN = [
    (
        "TRIBE stronger than textfeat clears a sentence-local frozen-LM hidden-state target, not the full "
        "context/self-distillation or rich-feedback privileged-signal adjacency raised in "
        "docs/top-venue-privileged-signal-adjacency-audit-2026-07-03.md."
    ),
    (
        "A top-tier positive needs /interpret plus stat/code review, and likely extra seeds because n<=3 gives "
        "low sign-flip p-value resolution."
    ),
    (
        "Before a brain-specific claim, decide whether the paper needs a stronger non-brain/context-distillation "
        "comparator or a real-brain follow-up."
    ),
]

POST_TEXTFEAT_POSITIVE_NEXT_ACTIONS = [
    "Switch to /interpret; do not record a verdict from this comparator alone.",
    "Audit seed-aligned TRIBE-minus-textfeat margins, PPL matching, analyzer gates, and code/stat assumptions.",
    "Read docs/top-venue-privileged-signal-adjacency-audit-2026-07-03.md before choosing the positive paper framing.",
    "Choose the next evidence burden: extra seeds, stronger non-brain/context comparator, real-brain follow-up, or controlled-scoping of the claim.",
]

DENSE_GENERIC_NEXT_ACTIONS = [
    "Switch to /interpret.",
    "Treat the positive utility, if any, as dense privileged-target or text-feature supervision rather than brain-specific.",
    "Do not use this branch as evidence for the top-tier brain-alignment claim.",
]


def load_analysis(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return data


def not_ready_reason(name: str, analysis: dict, expected_label: str) -> list[str]:
    reasons: list[str] = []
    gate = analysis.get("gate") or {}
    if not gate.get("science_ready"):
        failed = [key for key, value in gate.items() if isinstance(value, bool) and not value]
        reasons.append(f"{name}: gate.science_ready=false; failed={failed}")
    label = analysis.get("target_label")
    if label != expected_label:
        reasons.append(f"{name}: target_label={label!r}, expected {expected_label!r}")
    if not analysis.get("paired"):
        reasons.append(f"{name}: no paired contrasts present")
    return reasons


def paired_values(analysis: dict, lam_key: str, contrast: str) -> tuple[list[int], list[float]]:
    paired = (analysis.get("paired") or {}).get(lam_key) or {}
    seeds = [int(seed) for seed in paired.get("common_seeds") or []]
    values = ((paired.get(contrast) or {}).get("values")) or []
    return seeds, [float(v) for v in values]


def values_by_seed(seeds: list[int], values: list[float]) -> dict[int, float]:
    return {seed: values[i] for i, seed in enumerate(seeds) if i < len(values)}


def seed_aligned_delta(a_seeds: list[int], a_vals: list[float], b_seeds: list[int], b_vals: list[float]) -> dict:
    a = values_by_seed(a_seeds, a_vals)
    b = values_by_seed(b_seeds, b_vals)
    common = sorted(set(a) & set(b))
    deltas = [a[seed] - b[seed] for seed in common]
    out = paired_delta_stats(deltas)
    out["common_seeds"] = common
    return out


def target_scope(analysis: dict) -> dict:
    meta = analysis.get("target_cache_meta") or {}
    if not isinstance(meta, dict):
        meta = {}
    label = analysis.get("target_label")
    scope = {
        "target_label": label,
        "target_cache": analysis.get("target_cache"),
        "heldout_target_cache": analysis.get("heldout_target_cache"),
        "cache_experiment": meta.get("experiment"),
        "model": meta.get("model"),
        "layer": meta.get("layer"),
        "pool": meta.get("pool"),
        "max_length": meta.get("max_length"),
        "projection": meta.get("projection"),
        "features": meta.get("features"),
        "event_mode": meta.get("event_mode"),
    }
    if label == "textfeat":
        scope["control_family"] = "sentence_local_teacher_hidden_state"
        scope["clears"] = [
            "non-brain frozen-LM hidden-state target under the same KD budget",
            "dense stimulus-text feature target with a permuted dense-target twin",
        ]
        scope["does_not_clear"] = [
            "long-document context distillation",
            "on-policy/self-distillation with privileged rationales or answers",
            "real-brain evaluation",
        ]
    elif label == "tribe":
        scope["control_family"] = "synthetic_brain_target"
    elif label:
        scope["control_family"] = "non_tribe_target"
    return {key: value for key, value in scope.items() if value not in (None, {}, [])}


def lambda_comparison(tribe: dict, textfeat: dict, lam_key: str) -> dict:
    t_seed_kd, t_kd = paired_values(tribe, lam_key, "target_r2_target_minus_kd")
    x_seed_kd, x_kd = paired_values(textfeat, lam_key, "target_r2_target_minus_kd")
    t_seed_perm, t_perm = paired_values(tribe, lam_key, "target_r2_target_minus_perm")
    x_seed_perm, x_perm = paired_values(textfeat, lam_key, "target_r2_target_minus_perm")
    tribe_paired = (tribe.get("paired") or {}).get(lam_key) or {}
    text_paired = (textfeat.get("paired") or {}).get(lam_key) or {}
    return {
        "tribe_ppl_matched": bool(tribe_paired.get("ppl_matched")),
        "textfeat_ppl_matched": bool(text_paired.get("ppl_matched")),
        "tribe_gain_vs_kd": tribe_paired.get("target_r2_target_minus_kd"),
        "tribe_gain_vs_permuted": tribe_paired.get("target_r2_target_minus_perm"),
        "textfeat_gain_vs_kd": text_paired.get("target_r2_target_minus_kd"),
        "textfeat_gain_vs_permuted": text_paired.get("target_r2_target_minus_perm"),
        "tribe_minus_textfeat_gain_vs_kd": seed_aligned_delta(t_seed_kd, t_kd, x_seed_kd, x_kd),
        "tribe_minus_textfeat_gain_vs_permuted": seed_aligned_delta(t_seed_perm, t_perm, x_seed_perm, x_perm),
    }


def branch_hint(summary: dict) -> dict:
    if not summary.get("ready"):
        return {
            "branch": "not_ready",
            "reason": "At least one analyzer output is not science-ready or has the wrong target label.",
        }

    votes = []
    for lam_key, rec in sorted((summary.get("lambda_comparisons") or {}).items()):
        tribe_kd = (rec.get("tribe_gain_vs_kd") or {}).get("mean")
        tribe_perm = (rec.get("tribe_gain_vs_permuted") or {}).get("mean")
        text_kd = (rec.get("textfeat_gain_vs_kd") or {}).get("mean")
        text_perm = (rec.get("textfeat_gain_vs_permuted") or {}).get("mean")
        margin_kd = rec.get("tribe_minus_textfeat_gain_vs_kd") or {}
        margin_perm = rec.get("tribe_minus_textfeat_gain_vs_permuted") or {}
        if tribe_kd is None or tribe_perm is None or text_kd is None or text_perm is None:
            vote = "missing_effect"
        elif tribe_kd <= 0.0 or tribe_perm <= 0.0:
            vote = "tribe_not_positive"
        elif text_kd > 0.0 and text_perm > 0.0 and (margin_kd.get("mean") or 0.0) <= 0.0:
            vote = "dense_target_generic"
        elif (margin_kd.get("all_positive") and margin_perm.get("all_positive")):
            vote = "tribe_stronger_than_textfeat"
        else:
            vote = "mixed"
        votes.append(
            {
                "lambda": lam_key,
                "vote": vote,
                "tribe_gain_vs_kd_mean": tribe_kd,
                "tribe_gain_vs_permuted_mean": tribe_perm,
                "textfeat_gain_vs_kd_mean": text_kd,
                "textfeat_gain_vs_permuted_mean": text_perm,
                "tribe_minus_textfeat_gain_vs_kd_mean": margin_kd.get("mean"),
                "tribe_minus_textfeat_gain_vs_permuted_mean": margin_perm.get("mean"),
            }
        )

    vote_set = {vote["vote"] for vote in votes}
    if vote_set <= {"tribe_not_positive"}:
        branch = "tribe_not_positive"
        reason = "TRIBE does not clear its own KD/permuted contrasts; compare-control interpretation is unnecessary."
    elif vote_set <= {"dense_target_generic"}:
        branch = "dense_privileged_target_generic"
        reason = "Text-feature target gains match or exceed TRIBE gains; brain specificity is unsupported."
    elif vote_set == {"tribe_stronger_than_textfeat"}:
        branch = "tribe_stronger_than_textfeat_needs_review"
        reason = "TRIBE gains exceed text-feature gains seed-aligned, but this still needs /interpret, stats/code review, and likely extra evidence."
    else:
        branch = "mixed_requires_interpretation"
        reason = "Control comparison differs across lambdas or contrasts; inspect seed-level margins."
    hint = {"branch": branch, "reason": reason, "lambda_votes": votes}
    if branch == "tribe_stronger_than_textfeat_needs_review":
        hint["post_positive_reviewer_burden"] = POST_TEXTFEAT_POSITIVE_REVIEWER_BURDEN
        hint["next_actions"] = POST_TEXTFEAT_POSITIVE_NEXT_ACTIONS
    elif branch == "dense_privileged_target_generic":
        hint["next_actions"] = DENSE_GENERIC_NEXT_ACTIONS
    elif branch == "mixed_requires_interpretation":
        hint["next_actions"] = [
            "Switch to /interpret.",
            "Inspect seed-level margins instead of forcing a null or positive branch.",
            "Do not claim brain specificity unless the mixedness is resolved by predeclared criteria.",
        ]
    return hint


def compare(tribe_path: Path, textfeat_path: Path) -> dict:
    tribe = load_analysis(tribe_path)
    textfeat = load_analysis(textfeat_path)
    readiness_failures = []
    readiness_failures.extend(not_ready_reason("tribe", tribe, "tribe"))
    readiness_failures.extend(not_ready_reason("textfeat", textfeat, "textfeat"))
    tribe_lams = set((tribe.get("paired") or {}).keys())
    text_lams = set((textfeat.get("paired") or {}).keys())
    common_lams = sorted(tribe_lams & text_lams)
    if not common_lams:
        readiness_failures.append("no common lambda keys between TRIBE and textfeat analyses")

    summary = {
        "tribe_analysis": str(tribe_path),
        "textfeat_analysis": str(textfeat_path),
        "ready": not readiness_failures,
        "readiness_failures": readiness_failures,
        "comparison_note": (
            "Compares within-target paired gains over KD/permuted controls. It does not turn synthetic "
            "target-R2 into downstream utility or replace /interpret."
        ),
        "target_scopes": {
            "tribe": target_scope(tribe),
            "textfeat": target_scope(textfeat),
        },
        "common_lambdas": common_lams,
        "lambda_comparisons": {},
    }
    if not readiness_failures:
        for lam_key in common_lams:
            summary["lambda_comparisons"][lam_key] = lambda_comparison(tribe, textfeat, lam_key)
    summary["branch_hint"] = branch_hint(summary)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tribe-analysis", type=Path, required=True)
    ap.add_argument("--textfeat-analysis", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    summary = compare(args.tribe_analysis, args.textfeat_analysis)
    if args.out:
        args.out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"saved {args.out}")
    print(json.dumps({"ready": summary["ready"], "branch_hint": summary["branch_hint"]}, indent=2))


if __name__ == "__main__":
    main()
