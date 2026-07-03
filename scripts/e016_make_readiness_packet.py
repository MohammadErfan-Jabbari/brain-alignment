#!/usr/bin/env python3
"""Build a compact E016 post-analyzer readiness packet.

This is a routing/audit helper, not a verdict engine. It reads the conservative
Phase-3 analyzer JSON and extracts the fields that /interpret needs to inspect
first: gate status, branch hint, paired effects, and reviewer-burden flags.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


POST_POSITIVE_BURDEN_NOTE = (
    "Even after a TRIBE-vs-textfeat win, the 2026-07-03 privileged-signal adjacency audit means a top-tier "
    "positive may need extra seeds plus a long-context/on-policy distillation comparator or a real-brain follow-up "
    "before a brain-specific claim."
)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return data


def failed_gate_fields(gate: dict[str, Any]) -> list[str]:
    return [key for key, value in gate.items() if isinstance(value, bool) and not value]


def normalized_branch_hint(analysis: dict[str, Any]) -> dict[str, Any]:
    hint = analysis.get("paper_branch_hint")
    if isinstance(hint, dict) and hint.get("branch"):
        return hint
    gate = analysis.get("gate") or {}
    if not gate.get("science_ready"):
        return {
            "branch": "not_ready",
            "reason": "Analyzer gate is not science-ready, or this analyzer predates paper_branch_hint.",
            "failed_gate_fields": failed_gate_fields(gate),
        }
    return {
        "branch": "missing",
        "reason": "Analyzer is science-ready but has no paper_branch_hint; inspect manually before routing.",
    }


def out_path_for(path: Path) -> Path:
    name = path.name
    if name.endswith(".analysis.json"):
        return path.with_name(name[: -len(".analysis.json")] + ".readiness.json")
    return path.with_suffix(path.suffix + ".readiness.json")


def contrast_record(rec: dict[str, Any]) -> dict[str, Any]:
    return {
        "mean": rec.get("mean"),
        "ci95": rec.get("ci95"),
        "n": rec.get("n"),
        "values": rec.get("values"),
        "all_positive": rec.get("all_positive"),
        "sign_flip_p_two_sided": rec.get("sign_flip_p_two_sided"),
    }


def paired_packet(paired: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for lam_key, rec in sorted(paired.items()):
        target_minus_perm = contrast_record(rec.get("target_r2_target_minus_perm") or {})
        target_minus_kd = contrast_record(rec.get("target_r2_target_minus_kd") or {})
        target_positive = (
            (target_minus_perm.get("mean") is not None and target_minus_perm["mean"] > 0.0)
            and (target_minus_kd.get("mean") is not None and target_minus_kd["mean"] > 0.0)
        )
        all_seed_positive = bool(target_minus_perm.get("all_positive")) and bool(target_minus_kd.get("all_positive"))
        out[lam_key] = {
            "ppl_matched": bool(rec.get("ppl_matched")),
            "common_seeds": rec.get("common_seeds") or [],
            "common_seeds_complete": bool(rec.get("common_seeds_complete")),
            "target_r2_target_minus_perm": target_minus_perm,
            "target_r2_target_minus_kd": target_minus_kd,
            "target_positive_on_means": bool(target_positive),
            "target_positive_on_all_common_seeds": bool(all_seed_positive),
        }
    return out


def target_cache_scope(analysis: dict[str, Any]) -> dict[str, Any]:
    label = analysis.get("target_label")
    meta = analysis.get("target_cache_meta") or {}
    if not isinstance(meta, dict):
        meta = {}
    scope: dict[str, Any] = {
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


def reviewer_burden(analysis: dict[str, Any], packet: dict[str, Any]) -> list[str]:
    burdens: list[str] = []
    gate = analysis.get("gate") or {}
    branch = normalized_branch_hint(analysis).get("branch") or "missing"
    target_label = analysis.get("target_label")
    n_seeds = int(analysis.get("n_seeds") or 0)

    if not gate.get("science_ready"):
        burdens.append("Analyzer gate is not science-ready; do not interpret as a Phase-3 result.")
    if n_seeds <= 3:
        burdens.append("Three-or-fewer seeds give low sign-flip p-value resolution; a top-tier positive needs extra inference strength.")
    if branch == "tribe_positive_needs_textfeat":
        burdens.append("TRIBE-only positive cannot support brain-specificity; run the matched-information textfeat control first.")
        burdens.append(POST_POSITIVE_BURDEN_NOTE)
    if branch == "matched_information_control_ready":
        burdens.append(
            "This non-TRIBE control only becomes interpretable after TRIBE-vs-control comparison; a TRIBE win still inherits the post-positive reviewer burden."
        )
        scope = packet.get("target_cache_scope") or {}
        if scope.get("does_not_clear"):
            burdens.append(
                "This control's scope is limited; unresolved comparators include "
                + ", ".join(str(x) for x in scope["does_not_clear"])
                + "."
            )
    if branch == "controlled_null_candidate":
        burdens.append("Controlled-null branch still needs /interpret, seed-level paired audit, and code/stat review before paper framing.")
    if branch == "mixed_requires_interpretation":
        burdens.append("Mixed branch requires seed-level inspection; do not force it into the null or positive paper branch.")
    if target_label and target_label != "tribe":
        burdens.append("Non-TRIBE target analysis must be compared against the completed TRIBE analysis before any brain-specific claim.")
    if packet.get("failed_gate_fields"):
        burdens.append("Failed gate fields must be fixed or explicitly scoped before any result claim.")
    return burdens


def next_actions(analysis: dict[str, Any]) -> list[str]:
    gate = analysis.get("gate") or {}
    branch = normalized_branch_hint(analysis).get("branch") or "missing"
    if not gate.get("science_ready"):
        return [
            "Stay in /work.",
            "Debug or complete the failed analyzer gate fields before interpretation.",
            "Do not record an E016 science result.",
        ]
    if branch == "controlled_null_candidate":
        return [
            "Switch to /interpret.",
            "Audit paired deltas, PPL matching, sign-flip sanity checks, and code/stat assumptions.",
            "Only after audit, decide whether the controlled-negative paper branch is real.",
        ]
    if branch == "tribe_positive_needs_textfeat":
        return [
            "Do not claim brain specificity.",
            "Confirm the active TRIBE run is complete and resources are free.",
            "Run the queued text-feature control, then compare ready analyzer JSONs.",
            "Before positive paper framing, inspect docs/top-venue-privileged-signal-adjacency-audit-2026-07-03.md.",
        ]
    if branch == "matched_information_control_ready":
        return [
            "Compare this non-TRIBE analysis against the ready TRIBE analyzer JSON.",
            "Use e016_compare_target_controls.py before any brain-specific paper claim.",
            "If TRIBE exceeds the control, treat that as a post-positive review input rather than brain-specific clearance.",
        ]
    return [
        "Switch to /interpret.",
        "Inspect seed-level mixedness and write down the mixed finding rather than forcing a preferred branch.",
    ]


def make_packet(analysis_path: Path, comparison_path: Path | None = None) -> dict[str, Any]:
    analysis = load_json(analysis_path)
    gate = analysis.get("gate") or {}
    branch_hint = normalized_branch_hint(analysis)
    packet: dict[str, Any] = {
        "analysis_json": str(analysis_path),
        "science_status": "readiness packet only; not a verdict or rung flip",
        "target_label": analysis.get("target_label"),
        "target_arm": analysis.get("target_arm"),
        "permuted_arm": analysis.get("permuted_arm"),
        "target_cache_scope": target_cache_scope(analysis),
        "n_seeds": analysis.get("n_seeds"),
        "expected_seeds": analysis.get("expected_seeds"),
        "observed_seeds": analysis.get("observed_seeds"),
        "expected_lambdas": analysis.get("expected_lambdas"),
        "observed_lambdas": analysis.get("observed_lambdas"),
        "gate": gate,
        "failed_gate_fields": failed_gate_fields(gate),
        "paper_branch_hint": branch_hint,
        "grid": analysis.get("grid"),
        "scale": {
            "n_train": analysis.get("n_train"),
            "n_heldout_ppl": analysis.get("n_heldout_ppl"),
            "target_dim": analysis.get("target_dim"),
        },
        "paired": paired_packet(analysis.get("paired") or {}),
        "must_not_claim": [
            "Do not claim an E016 null or positive unless gate.science_ready=true and /interpret audits it.",
            "Do not claim brain specificity from TRIBE alone.",
            "Do not treat TRIBE>textfeat as brain-specific clearance without post-positive review and adjacency-burden follow-up.",
            "Do not treat synthetic target-R2 as downstream utility.",
            "Do not flip a ladder rung from this packet.",
        ],
    }
    if comparison_path is not None:
        comparison = load_json(comparison_path)
        packet["comparison_json"] = str(comparison_path)
        packet["comparison_ready"] = comparison.get("ready")
        packet["comparison_branch_hint"] = comparison.get("branch_hint")
        packet["comparison_readiness_failures"] = comparison.get("readiness_failures")

    packet["reviewer_burden_flags"] = reviewer_burden(analysis, packet)
    packet["next_actions"] = next_actions(analysis)
    return packet


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("analysis_json", type=Path)
    ap.add_argument("--comparison-json", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    packet = make_packet(args.analysis_json, args.comparison_json)
    out = args.out or out_path_for(args.analysis_json)
    out.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(f"saved {out}")
    print(
        json.dumps(
            {
                "science_status": packet["science_status"],
                "science_ready": bool((packet.get("gate") or {}).get("science_ready")),
                "failed_gate_fields": packet["failed_gate_fields"],
                "paper_branch_hint": packet.get("paper_branch_hint"),
                "reviewer_burden_flags": packet["reviewer_burden_flags"],
                "next_actions": packet["next_actions"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
