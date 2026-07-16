#!/usr/bin/env python3
"""E025 preregistered participant-level analysis.

Consumes raw, fold-level rows from ``e025_participant_transfer.py``.  This file
does no model inference and never changes a project verdict.  Its job is to
recompute the locked participant estimand, uncertainty, robustness axes, power,
and the mechanical Package-C activation gate in E025.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from scipy import optimize, stats


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "e025-participant-transfer.v1"
TRAIN_UIDS = (848, 865, 875, 876)
HELDOUT_UIDS = (797, 837, 841, 856, 880)
EXPECTED_UIDS = tuple(sorted(TRAIN_UIDS + HELDOUT_UIDS))
EXPECTED_SEEDS = tuple(range(6))
EXPECTED_FOLDS = tuple(range(5))
SESOI = 0.002
EXPECTED_LAYERS = (6, 7)
EXPECTED_NUISANCES = ("full_cov", "imageability", "primary")
EXPECTED_ARMS = {
    "tribe": ("kd_only", "tribe_mse", "tribe_perm"),
    "textfeat": ("kd_only", "textfeat_mse", "textfeat_perm"),
}
NUISANCE_VARIANTS = {
    "primary": "token length + normalized item position + fixed GPT-2-medium static embeddings",
    "imageability": "primary + Tuckute imageability",
    "full_cov": "imageability + GPT-2XL and PCFG surprisal, with primary nuisance",
}
RIDGE_ALPHAS = [1.0, 10.0, 100.0, 1000.0, 10000.0]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def finite(values: Iterable[float]) -> np.ndarray:
    x = np.asarray(list(values), dtype=np.float64)
    if x.size == 0 or not np.isfinite(x).all():
        raise ValueError("statistic received no values or non-finite values")
    return x


def mean_ci(values: Iterable[float], confidence: float = 0.95) -> dict[str, Any]:
    x = finite(values)
    mean = float(x.mean())
    if x.size == 1:
        lo = hi = mean
        sd = se = 0.0
    else:
        sd = float(x.std(ddof=1))
        se = sd / math.sqrt(x.size)
        q = float(stats.t.ppf((1.0 + confidence) / 2.0, x.size - 1))
        lo, hi = mean - q * se, mean + q * se
    return {
        "n": int(x.size), "mean": mean, "sd": sd, "se": se,
        "ci95": [float(lo), float(hi)], "values": x.tolist(),
    }


def one_sided_upper(values: Iterable[float], confidence: float = 0.95) -> float:
    x = finite(values)
    if x.size == 1:
        return float(x[0])
    se = float(x.std(ddof=1) / math.sqrt(x.size))
    return float(x.mean() + stats.t.ppf(confidence, x.size - 1) * se)


def exact_sign(values: Iterable[float]) -> dict[str, Any]:
    x = finite(values)
    nz = x[x != 0]
    pos = int((nz > 0).sum())
    p = float(stats.binomtest(pos, int(nz.size), 0.5, alternative="two-sided").pvalue) if nz.size else 1.0
    return {"positive": pos, "negative": int((nz < 0).sum()), "zero": int((x == 0).sum()),
            "n_nonzero": int(nz.size), "two_sided_p": p}


def wilcoxon(values: Iterable[float]) -> dict[str, Any]:
    x = finite(values)
    if np.all(x == 0):
        return {"statistic": 0.0, "two_sided_p": 1.0, "status": "all_zero"}
    try:
        r = stats.wilcoxon(x, alternative="two-sided", zero_method="wilcox")
        return {"statistic": float(r.statistic), "two_sided_p": float(r.pvalue), "status": "ok"}
    except ValueError as exc:
        return {"statistic": None, "two_sided_p": None, "status": f"unavailable: {exc}"}


def noncentral_power(delta: float, sd: float, n: int, alpha: float = 0.05) -> float:
    if sd <= 0:
        return 1.0 if delta != 0 else alpha
    crit = float(stats.t.ppf(1 - alpha / 2, n - 1))
    ncp = abs(delta) / (sd / math.sqrt(n))
    right = float(stats.nct.sf(crit, n - 1, ncp))
    left = float(stats.nct.cdf(-crit, n - 1, ncp))
    if not math.isfinite(left):
        left = 0.0
    return float(min(1.0, max(0.0, right + left)))


def mde_80(sd: float, n: int, alpha: float = 0.05) -> float:
    if sd <= 0:
        return 0.0
    f = lambda d: noncentral_power(d, sd, n, alpha) - 0.80
    hi = sd / math.sqrt(n)
    while f(hi) < 0 and hi < 100 * sd:
        hi *= 2
    return float(optimize.brentq(f, 0.0, hi))


def pick_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("score_rows", "rows", "raw_rows"):
        rows = payload.get(key)
        if isinstance(rows, list) and rows and "unique_r2" in rows[0]:
            return rows
    scoring = payload.get("scoring")
    if isinstance(scoring, dict):
        for key in ("score_rows", "rows", "raw_rows"):
            rows = scoring.get(key)
            if isinstance(rows, list) and rows and "unique_r2" in rows[0]:
                return rows
    raise ValueError("could not find raw fold score rows in evidence JSON")


def validate_bound_inputs(
    evidence: dict[str, Any], gates: dict[str, Any], evidence_path: Path, gates_path: Path
) -> tuple[list[dict[str, Any]], dict[str, bool]]:
    """Verify the complete manifest -> extraction -> raw-score provenance chain."""
    if evidence.get("schema_version") != SCHEMA_VERSION or evidence.get("stage") != "score":
        raise ValueError("evidence must be a v1 E025 score-stage artifact")
    if gates.get("schema_version") != SCHEMA_VERSION or gates.get("stage") != "extract":
        raise ValueError("gates must be the v1 E025 extraction-stage artifact")

    evidence_manifest = evidence.get("manifest")
    gates_manifest = gates.get("manifest")
    evidence_extraction = evidence.get("extraction")
    if not all(isinstance(x, dict) for x in (evidence_manifest, gates_manifest, evidence_extraction)):
        raise ValueError("evidence/gates provenance records are missing")
    if evidence_manifest.get("sha256") != gates_manifest.get("sha256"):
        raise ValueError("raw evidence and gate extraction refer to different manifests")
    manifest_path = Path(str(evidence_manifest.get("path", ""))).resolve()
    if not manifest_path.is_file() or sha256(manifest_path) != evidence_manifest.get("sha256"):
        raise ValueError("actual E025 manifest does not match the evidence provenance hash")
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema_version") != SCHEMA_VERSION or manifest.get("stage") != "manifest":
        raise ValueError("provenance target is not a v1 E025 manifest")
    analyzer = manifest.get("analyzer")
    if not isinstance(analyzer, dict) or analyzer.get("sha256") != sha256(Path(__file__)):
        raise ValueError("current analyzer differs from the preflight-frozen analyzer")

    if Path(str(evidence_extraction.get("path", ""))).resolve() != gates_path.resolve():
        raise ValueError("--gates is not the extraction artifact named by the raw evidence")
    actual_gate_sha = sha256(gates_path)
    if evidence_extraction.get("sha256") != actual_gate_sha:
        raise ValueError("actual gate extraction hash differs from the raw evidence provenance")
    if gates_manifest.get("sha256") != sha256(manifest_path):
        raise ValueError("gate extraction manifest hash differs from the actual frozen manifest")

    expected_scoring = {
        "layers": list(EXPECTED_LAYERS),
        "nuisance_variants": NUISANCE_VARIANTS,
        "n_folds": 5,
        "folding": "five deterministic contiguous heldout blocks",
        "pca_rank": 50,
        "pca_fit": "training fold only, separately for static and contextual blocks",
        "ridge_alphas": RIDGE_ALPHAS,
        "ridge_selection": "RidgeCV fit on the training fold only",
        "target_aggregation": "mean R2 across the five fixed LH language sub-ROIs within fold",
    }
    if evidence.get("scoring") != expected_scoring:
        raise ValueError("raw evidence scoring configuration differs from the preregistered lock")
    expected_extract = {
        "layers": list(EXPECTED_LAYERS),
        "pooling": "attention-mask mean",
        "max_length": 64,
        "batch_size": 16,
        "reference_model": "gpt2-medium",
    }
    if gates.get("configuration") != expected_extract:
        raise ValueError("gate extraction configuration differs from the preregistered lock")
    scorer_validation = evidence.get("scorer_validation")
    if not isinstance(scorer_validation, dict) or scorer_validation.get("pass") is not True:
        raise ValueError("raw evidence lacks a passing optimized/canonical scorer check")

    rows = pick_rows(evidence)
    expected_grid = {
        (uid, seed, fold, layer, nuisance, family, arm)
        for uid in EXPECTED_UIDS
        for seed in EXPECTED_SEEDS
        for fold in EXPECTED_FOLDS
        for layer in EXPECTED_LAYERS
        for nuisance in EXPECTED_NUISANCES
        for family, arms in EXPECTED_ARMS.items()
        for arm in arms
    }
    observed_grid: set[tuple[int, int, int, int, str, str, str]] = set()
    for row in rows:
        key = (
            int(row["uid"]), int(row["seed"]), int(row["fold"]), int(row["layer"]),
            str(row.get("nuisance_variant")), str(row.get("family")), str(row.get("arm")),
        )
        if key in observed_grid:
            raise ValueError(f"duplicate raw-grid row: {key}")
        observed_grid.add(key)
        fold = key[2]
        if (
            int(row.get("train_count", -1)) != 800
            or int(row.get("test_start", -1)) != 200 * fold
            or int(row.get("test_stop_exclusive", -1)) != 200 * (fold + 1)
            or int(row.get("test_count", -1)) != 200
        ):
            raise ValueError(f"raw row has a noncanonical contiguous fold: {key}")
        for metric in ("unique_r2", "r2_nuisance", "r2_full"):
            if not math.isfinite(float(row[metric])):
                raise ValueError(f"raw row has nonfinite {metric}: {key}")
    if observed_grid != expected_grid:
        missing = sorted(expected_grid - observed_grid)[:5]
        extra = sorted(observed_grid - expected_grid)[:5]
        raise ValueError(f"raw-grid mismatch: missing={missing} extra={extra}")
    if evidence.get("raw_row_count") != len(expected_grid) or len(rows) != len(expected_grid):
        raise ValueError("raw row count does not equal the exact preregistered grid")

    summary = gates.get("gate_summary")
    if not isinstance(summary, dict):
        raise ValueError("gate extraction lacks gate_summary")
    exact_gates: dict[str, bool] = {}
    for name in ("quality_equivalence", "target_direction", "representation_movement"):
        record = summary.get(name)
        if not isinstance(record, dict) or not isinstance(record.get("pass"), bool):
            raise ValueError(f"gate_summary.{name}.pass is absent or not boolean")
        exact_gates[name] = bool(record["pass"])
    return rows, exact_gates


def norm_family(row: dict[str, Any]) -> str:
    raw = str(row.get("family") or row.get("target_family") or "").lower().replace("-", "_")
    arm = str(row.get("arm", "")).lower()
    if "textfeat" in raw or "textfeat" in arm or "text_feature" in raw:
        return "textfeat"
    if "tribe" in raw or "tribe" in arm:
        return "tribe"
    if arm == "kd_only":
        return "shared"
    return raw or "unknown"


def index_scores(rows: list[dict[str, Any]]) -> dict[tuple, float]:
    grouped: dict[tuple, list[float]] = defaultdict(list)
    for r in rows:
        key = (
            int(r["uid"]), int(r["seed"]), int(r["fold"]), int(r["layer"]),
            str(r.get("nuisance_variant", "primary")), norm_family(r), str(r["arm"]),
        )
        grouped[key].append(float(r["unique_r2"]))
    out: dict[tuple, float] = {}
    for key, vals in grouped.items():
        if max(vals) - min(vals) > 1e-10:
            raise ValueError(f"duplicate score rows disagree for {key}: {vals}")
        out[key] = vals[0]
    return out


def get_score(idx: dict[tuple, float], uid: int, seed: int, fold: int, layer: int,
              nuisance: str, family: str, arm: str) -> float:
    key = (uid, seed, fold, layer, nuisance, family, arm)
    if key in idx:
        return idx[key]
    if arm == "kd_only":
        candidates = [v for k, v in idx.items()
                      if k[:5] == (uid, seed, fold, layer, nuisance) and k[6] == "kd_only"]
        if not candidates:
            raise KeyError(key)
        if max(candidates) - min(candidates) > 1e-10:
            raise ValueError(f"KD aliases disagree for {key}: {candidates}")
        return candidates[0]
    raise KeyError(key)


def cell_contrasts(idx: dict[tuple, float], layer: int, nuisance: str) -> list[dict[str, Any]]:
    rows = []
    for uid in EXPECTED_UIDS:
        for seed in EXPECTED_SEEDS:
            for fold in EXPECTED_FOLDS:
                kd = get_score(idx, uid, seed, fold, layer, nuisance, "shared", "kd_only")
                tribe = get_score(idx, uid, seed, fold, layer, nuisance, "tribe", "tribe_mse")
                text = get_score(idx, uid, seed, fold, layer, nuisance, "textfeat", "textfeat_mse")
                rows.append({
                    "uid": uid, "seed": seed, "fold": fold,
                    "tribe_minus_textfeat": tribe - text,
                    "tribe_minus_kd": tribe - kd,
                    "textfeat_minus_kd": text - kd,
                    "kd": kd, "tribe": tribe, "textfeat": text,
                })
    return rows


def aggregate(rows: list[dict[str, Any]], value: str) -> dict[str, Any]:
    by_uid = {u: float(np.mean([r[value] for r in rows if r["uid"] == u])) for u in EXPECTED_UIDS}
    by_fold = {f: float(np.mean([r[value] for r in rows if r["fold"] == f])) for f in EXPECTED_FOLDS}
    by_seed = {s: float(np.mean([r[value] for r in rows if r["seed"] == s])) for s in EXPECTED_SEEDS}
    x = [by_uid[u] for u in EXPECTED_UIDS]
    ci = mean_ci(x)
    loo_uid = {str(u): float(np.mean([by_uid[v] for v in EXPECTED_UIDS if v != u])) for u in EXPECTED_UIDS}
    loo_fold = {
        str(f): float(np.mean([r[value] for r in rows if r["fold"] != f])) for f in EXPECTED_FOLDS
    }
    train = [by_uid[u] for u in TRAIN_UIDS]
    held = [by_uid[u] for u in HELDOUT_UIDS]
    return {
        "participant": {**ci, "median": float(np.median(x)), "by_uid": {str(k): v for k, v in by_uid.items()},
                        "one_sided_upper95": one_sided_upper(x), "sign": exact_sign(x),
                        "wilcoxon": wilcoxon(x), "leave_one_uid_out_means": loo_uid},
        "block": {"by_fold": {str(k): v for k, v in by_fold.items()},
                  "leave_one_block_out_means": loo_fold},
        "seed": {"by_seed": {str(k): v for k, v in by_seed.items()}},
        "subgroups": {"train4": mean_ci(train), "heldout5": mean_ci(held)},
    }


def subgroup_stable(by_uid: dict[str, float], uids: tuple[int, ...]) -> bool:
    vals = [float(by_uid[str(u)]) for u in uids]
    st = mean_ci(vals)
    loo = [float(np.mean([by_uid[str(v)] for v in uids if v != u])) for u in uids]
    return st["mean"] >= SESOI and st["ci95"][0] > 0 and all(x > 0 for x in loo)


def suppress_inferential_output(analyses: dict[str, Any]) -> None:
    """Retain descriptive cells but remove tests/intervals after a failed pre-score gate."""
    for layer_result in analyses.values():
        for contrast in layer_result.values():
            participant = contrast["participant"]
            participant["se"] = None
            participant["ci95"] = None
            participant["one_sided_upper95"] = None
            participant["sign"]["two_sided_p"] = None
            participant["wilcoxon"] = {
                "statistic": None,
                "two_sided_p": None,
                "status": "suppressed_pre_scoring_gate_failure",
            }
            for subgroup in contrast["subgroups"].values():
                subgroup["se"] = None
                subgroup["ci95"] = None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence", type=Path, default=ROOT / "outputs/E025/raw_folds.json")
    ap.add_argument("--gates", type=Path, default=ROOT / "outputs/E025/extraction.json",
                    help="Extraction/gate JSON; defaults to the E025 runner output.")
    ap.add_argument("--out", type=Path, default=ROOT / "outputs/E025/analysis.json")
    args = ap.parse_args()

    evidence = json.loads(args.evidence.read_text())
    gate_payload = json.loads(args.gates.read_text())
    rows, gates = validate_bound_inputs(
        evidence, gate_payload, args.evidence.resolve(), args.gates.resolve()
    )
    idx = index_scores(rows)
    nuisances = sorted({k[4] for k in idx})
    if "primary" not in nuisances or "imageability" not in nuisances:
        raise ValueError(f"required nuisance variants primary/imageability absent: {nuisances}")

    analyses: dict[str, Any] = {}
    cells: dict[tuple[int, str], list[dict[str, Any]]] = {}
    for layer in (6, 7):
        for nuisance in nuisances:
            c = cell_contrasts(idx, layer, nuisance)
            cells[(layer, nuisance)] = c
            analyses[f"layer{layer}:{nuisance}"] = {
                contrast: aggregate(c, contrast)
                for contrast in ("tribe_minus_textfeat", "tribe_minus_kd", "textfeat_minus_kd")
            }

    primary = analyses["layer7:primary"]["tribe_minus_textfeat"]
    image = analyses["layer7:imageability"]["tribe_minus_textfeat"]
    tribe_kd = analyses["layer7:primary"]["tribe_minus_kd"]
    p = primary["participant"]
    by_uid = p["by_uid"]
    # SNR proxy is each participant's mean primary KD alignment over seed/fold.
    base_u = {
        u: float(np.mean([r["kd"] for r in cells[(7, "primary")] if r["uid"] == u]))
        for u in EXPECTED_UIDS
    }
    effects = [float(by_uid[str(u)]) for u in EXPECTED_UIDS]
    baselines = [base_u[u] for u in EXPECTED_UIDS]
    rho, rho_p = stats.spearmanr(effects, baselines)
    top_uid = max(EXPECTED_UIDS, key=lambda u: base_u[u])
    drop_top_mean = float(np.mean([by_uid[str(u)] for u in EXPECTED_UIDS if u != top_uid]))

    observed_sd = float(p["sd"])
    power = {
        "planning_sd_from_E008": 0.00062,
        "planning_mde80_approx": 0.00065,
        "observed_participant_sd": observed_sd,
        "observed_mde80": mde_80(observed_sd, len(EXPECTED_UIDS)),
        "observed_power_at_sesoi": noncentral_power(SESOI, observed_sd, len(EXPECTED_UIDS)),
    }

    gate_values_known = True
    gates_pass = gate_values_known and all(bool(v) for v in gates.values())
    if gates_pass:
        activation_checks: dict[str, bool | None] = {
            "all_pre_scoring_gates_pass": True,
            "participant_lower_ci_above_sesoi": p["ci95"][0] > SESOI,
            "at_least_8_of_9_positive": p["sign"]["positive"] >= 8,
            "all_six_seed_aggregates_positive": all(v > 0 for v in primary["seed"]["by_seed"].values()),
            "all_leave_one_participant_means_positive": all(v > 0 for v in p["leave_one_uid_out_means"].values()),
            "all_leave_one_block_means_positive": all(v > 0 for v in primary["block"]["leave_one_block_out_means"].values()),
            "heldout5_mean_positive": primary["subgroups"]["heldout5"]["mean"] > 0,
            "tribe_minus_kd_positive": tribe_kd["participant"]["mean"] > 0,
            "drop_highest_baseline_mean_at_least_sesoi": drop_top_mean >= SESOI,
            "imageability_mean_at_least_sesoi": image["participant"]["mean"] >= SESOI,
            "imageability_lower_ci_positive": image["participant"]["ci95"][0] > 0,
        }
        activation = all(bool(value) for value in activation_checks.values())
        train_stable: bool | None = subgroup_stable(by_uid, TRAIN_UIDS)
        held_stable: bool | None = subgroup_stable(by_uid, HELDOUT_UIDS)
        excludes_sesoi = p["one_sided_upper95"] < SESOI and not train_stable and not held_stable
        power_limited = (
            power["observed_mde80"] > SESOI and p["ci95"][0] <= SESOI <= p["ci95"][1]
        )
    else:
        activation_checks = {
            "all_pre_scoring_gates_pass": False,
            "participant_lower_ci_above_sesoi": None,
            "at_least_8_of_9_positive": None,
            "all_six_seed_aggregates_positive": None,
            "all_leave_one_participant_means_positive": None,
            "all_leave_one_block_means_positive": None,
            "heldout5_mean_positive": None,
            "tribe_minus_kd_positive": None,
            "drop_highest_baseline_mean_at_least_sesoi": None,
            "imageability_mean_at_least_sesoi": None,
            "imageability_lower_ci_positive": None,
        }
        activation = False
        train_stable = None
        held_stable = None
        excludes_sesoi = False
        power_limited = False

    if not gates_pass:
        classification = "uninformative_for_biological_benefit_gate_failure"
    elif activation:
        classification = "licenses_prospective_matched_control_design_not_brain_specificity"
    elif excludes_sesoi:
        classification = "practically_meaningful_positive_excluded_for_tested_cohort"
    elif power_limited:
        classification = "nonactivation_power_limited"
    else:
        classification = "does_not_activate_package_c"

    if not gates_pass:
        suppress_inferential_output(analyses)
        rho_p = None
        power["observed_mde80"] = None
        power["observed_power_at_sesoi"] = None

    out = {
        "experiment": "E025 participant-level E016 biological transfer",
        "science_status": "preregistered analysis output; requires /interpret and user confirmation; no verdict flip",
        "design": {"participants": list(EXPECTED_UIDS), "seeds": list(EXPECTED_SEEDS),
                   "folds": list(EXPECTED_FOLDS), "primary_layer": 7, "pca_rank": 50,
                   "sesoi_unique_r2": SESOI, "participant_is_population_inference_unit": True},
        "source": {"evidence": str(args.evidence), "evidence_sha256": sha256(args.evidence),
                   "gates": str(args.gates), "gates_sha256": sha256(args.gates),
                   "script_sha256": sha256(Path(__file__))},
        "analyses": analyses,
        "snr_sensitivity": {"baseline_by_uid": {str(k): v for k, v in base_u.items()},
                            "spearman_rho": float(rho),
                            "spearman_p": float(rho_p) if rho_p is not None else None,
                            "highest_baseline_uid": top_uid, "drop_highest_mean": drop_top_mean},
        "power": power,
        "pre_scoring_gates": gates,
        "activation_checks": activation_checks,
        "stable_predeclared_subgroups": {"train4": train_stable, "heldout5": held_stable},
        "mechanical_classification": classification,
        "inferential_status": (
            "enabled_all_pre_scoring_gates_passed"
            if gates_pass else "suppressed_pre_scoring_gate_failure_descriptive_cells_only"
        ),
        "boundary": "Primary TRIBE-minus-textfeat is dimension-matched only; E025 cannot establish biosignal specificity.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(args.out), "mechanical_classification": classification,
                      "participant_mean": p["mean"], "participant_ci95": p["ci95"]}, indent=2))


if __name__ == "__main__":
    main()
