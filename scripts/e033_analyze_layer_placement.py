#!/usr/bin/env python3
"""Crossed participant/fold analysis for E033 layer-placement robustness."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, stdev

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e033_layer_placement as E  # noqa: E402

ALL_UIDS = (797, 837, 841, 848, 856, 865, 875, 876, 880)
BUILDER_UIDS = (848, 865, 875, 876)
HELDOUT_UIDS = (797, 837, 841, 856, 880)
SEEDS = (0, 1, 2)
FOLDS = (0, 1, 2, 3, 4)
PLACEMENTS = ("mid", "final")
EVAL_LAYERS = (12, 24)
N_PERM = 5
SESOI = 0.001
LOG_PPL_MARGIN = math.log(1.05)


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path: str | Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def t_summary(values, confidence: float = 0.95) -> dict:
    vals = [float(v) for v in values]
    n = len(vals)
    if n < 2:
        raise ValueError("t summary requires at least two values")
    avg = mean(vals)
    se = stdev(vals) / math.sqrt(n)
    critical = float(stats.t.ppf(0.5 + confidence / 2.0, n - 1))
    one_sided = float(stats.t.ppf(confidence, n - 1))
    return {
        "n": n,
        "values": vals,
        "mean": avg,
        "se": se,
        "ci95": [avg - critical * se, avg + critical * se],
        "one_sided_95_lcb": avg - one_sided * se,
        "one_sided_95_ucb": avg + one_sided * se,
    }


def fold_bootstrap(values, n_boot: int = 20000, seed: int = 33) -> dict:
    vals = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(vals, size=(n_boot, len(vals)), replace=True).mean(axis=1)
    return {
        "n_boot": n_boot,
        "ci95": [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))],
        "p_mean_le_zero": float(np.mean(draws <= 0)),
    }


def sign_p_greater(n_positive: int, n: int) -> float:
    return float(stats.binomtest(n_positive, n, 0.5, alternative="greater").pvalue)


def wilcoxon_greater(values) -> float:
    vals = np.asarray(values, dtype=float)
    if np.allclose(vals, 0):
        return 1.0
    try:
        return float(
            stats.wilcoxon(
                vals,
                alternative="greater",
                zero_method="wilcox",
                method="auto",
            ).pvalue
        )
    except ValueError:
        return 1.0


def crossed_summary(cells: dict, uids: tuple[int, ...]) -> dict:
    expected = {(u, fold, seed) for u in uids for fold in FOLDS for seed in SEEDS}
    missing = sorted(expected - set(cells))
    extra = sorted(set(cells) - expected)
    if missing or extra:
        raise RuntimeError(
            f"crossed grid mismatch missing={missing[:5]} ({len(missing)}) "
            f"extra={extra[:5]} ({len(extra)})"
        )
    participant_values = {
        str(uid): float(median(cells[(uid, fold, seed)] for fold in FOLDS for seed in SEEDS))
        for uid in uids
    }
    fold_values = {
        str(fold): float(mean(cells[(uid, fold, seed)] for uid in uids for seed in SEEDS))
        for fold in FOLDS
    }
    participant_stats = t_summary(list(participant_values.values()))
    fold_stats = t_summary(list(fold_values.values()))
    participant_stats["n_positive"] = sum(v > 0 for v in participant_values.values())
    participant_stats["sign_p_greater"] = sign_p_greater(
        participant_stats["n_positive"], len(uids)
    )
    participant_stats["wilcoxon_p_greater"] = wilcoxon_greater(
        list(participant_values.values())
    )
    participant_stats["loo_means"] = {
        str(drop): float(mean(v for uid, v in participant_values.items() if int(uid) != drop))
        for drop in uids
    }
    fold_stats["bootstrap"] = fold_bootstrap(list(fold_values.values()))
    fold_stats["loo_means"] = {
        str(drop): float(mean(v for fold, v in fold_values.items() if int(fold) != drop))
        for drop in FOLDS
    }
    return {
        "uids": list(uids),
        "participant_values": participant_values,
        "fold_values": fold_values,
        "participant_axis": participant_stats,
        "fold_axis": fold_stats,
        "conservative_ci95": [
            min(participant_stats["ci95"][0], fold_stats["ci95"][0]),
            max(participant_stats["ci95"][1], fold_stats["ci95"][1]),
        ],
        "conservative_one_sided_95_lcb": min(
            participant_stats["one_sided_95_lcb"],
            fold_stats["one_sided_95_lcb"],
        ),
        "conservative_one_sided_95_ucb": max(
            participant_stats["one_sided_95_ucb"],
            fold_stats["one_sided_95_ucb"],
        ),
    }


def seed_collapsed_crossed(values: dict, uids: tuple[int, ...]) -> dict:
    expected = {(u, fold, seed) for u in uids for fold in FOLDS for seed in SEEDS}
    if set(values) != expected:
        missing = expected - set(values)
        extra = set(values) - expected
        raise RuntimeError(
            f"language grid mismatch missing={len(missing)} extra={len(extra)}"
        )
    uid_fold = {
        (uid, fold): float(mean(values[(uid, fold, seed)] for seed in SEEDS))
        for uid in uids
        for fold in FOLDS
    }
    participant_values = {
        str(uid): float(mean(uid_fold[(uid, fold)] for fold in FOLDS)) for uid in uids
    }
    fold_values = {
        str(fold): float(mean(uid_fold[(uid, fold)] for uid in uids)) for fold in FOLDS
    }
    return {
        "uids": list(uids),
        "seed_collapsed_uid_fold": {
            f"{uid}:{fold}": value for (uid, fold), value in uid_fold.items()
        },
        "participant_values": participant_values,
        "fold_values": fold_values,
        "participant_axis": t_summary(list(participant_values.values())),
        "fold_axis": t_summary(list(fold_values.values())),
    }


def load_inputs(
    kd_path: str,
    placement_paths: list[str],
    manifest_path: str,
    calibration_path: str,
):
    manifest = E.load_and_verify_manifest(manifest_path, calibration_path)
    kd = json.loads(Path(kd_path).read_text())
    placements = [json.loads(Path(path).read_text()) for path in placement_paths]
    manifest_id = manifest["manifest_sha256"]
    if kd.get("manifest_sha256") != manifest_id:
        raise RuntimeError("KD reference manifest mismatch")
    if kd.get("config") != manifest["config"]:
        raise RuntimeError("KD reference config mismatch")
    if kd.get("calibration_artifact_sha256") != manifest["calibration_artifact_sha256"]:
        raise RuntimeError("KD reference calibration mismatch")
    for path, artifact in zip(placement_paths, placements):
        if not artifact.get("science"):
            raise RuntimeError(f"non-science placement artifact supplied: {path}")
        if artifact.get("manifest_sha256") != manifest_id:
            raise RuntimeError(f"placement manifest mismatch: {path}")
        if artifact.get("config") != manifest["config"]:
            raise RuntimeError(f"placement config mismatch: {path}")
        if (
            artifact.get("calibration_artifact_sha256")
            != manifest["calibration_artifact_sha256"]
        ):
            raise RuntimeError(f"placement calibration mismatch: {path}")
    return manifest, kd, placements


def index_kd(rows):
    scores = {}
    ppls = {}
    for row in rows:
        uid = int(row["uid"])
        fold = int(row["fold"])
        seed = int(row["seed"])
        eval_layer = int(row["eval_layer"])
        if (
            uid not in ALL_UIDS
            or fold not in FOLDS
            or seed not in SEEDS
            or eval_layer not in EVAL_LAYERS
            or row.get("arm") != "kd_only"
        ):
            raise RuntimeError(f"invalid KD categorical cell {row}")
        key = (uid, fold, seed, eval_layer)
        if key in scores:
            raise RuntimeError(f"duplicate KD score {key}")
        score = float(row["unique_r2"])
        if not math.isfinite(score):
            raise RuntimeError(f"nonfinite KD unique_r2 {key}")
        scores[key] = score
        ppl_key = key[:3]
        value = float(row["perplexity"])
        if not math.isfinite(value) or value <= 0:
            raise RuntimeError(f"invalid KD perplexity {ppl_key}: {value}")
        if ppl_key in ppls and not math.isclose(ppls[ppl_key], value, rel_tol=0, abs_tol=1e-10):
            raise RuntimeError(f"KD perplexity differs across eval layers {ppl_key}")
        ppls[ppl_key] = value
    expected_scores = len(ALL_UIDS) * len(FOLDS) * len(SEEDS) * len(EVAL_LAYERS)
    expected_ppls = len(ALL_UIDS) * len(FOLDS) * len(SEEDS)
    if len(scores) != expected_scores or len(ppls) != expected_ppls:
        raise RuntimeError(
            f"KD row grid wrong scores={len(scores)}/{expected_scores} "
            f"ppls={len(ppls)}/{expected_ppls}"
        )
    return scores, ppls


def index_placements(artifacts):
    scores = {}
    ppls = {}
    uids_seen = set()
    for artifact in artifacts:
        runtime_uids = set(int(uid) for uid in artifact["runtime"]["uids"])
        runtime = artifact["runtime"]
        if (
            set(int(seed) for seed in runtime["seeds"]) != set(SEEDS)
            or set(int(fold) for fold in runtime["folds"]) != set(FOLDS)
            or int(runtime["n_perm"]) != N_PERM
            or runtime.get("limit_tune") is not None
            or bool(runtime.get("smoke"))
            or not runtime_uids
            or not runtime_uids <= set(ALL_UIDS)
        ):
            raise RuntimeError(f"invalid scientific shard runtime {runtime}")
        if uids_seen & runtime_uids:
            raise RuntimeError(f"placement shards overlap: {uids_seen & runtime_uids}")
        uids_seen |= runtime_uids
        expected_rows = (
            len(runtime_uids)
            * len(FOLDS)
            * len(SEEDS)
            * len(PLACEMENTS)
            * (1 + N_PERM)
            * len(EVAL_LAYERS)
        )
        if len(artifact["rows"]) != expected_rows:
            raise RuntimeError(
                f"shard row count wrong {len(artifact['rows'])}/{expected_rows}"
            )
        lambdas = artifact["config"]["lambdas"]
        for row in artifact["rows"]:
            uid = int(row["uid"])
            fold = int(row["fold"])
            seed = int(row["seed"])
            placement = str(row["placement"])
            target = str(row["target"])
            eval_layer = int(row["eval_layer"])
            allowed_targets = {"real"} | {f"perm{draw}" for draw in range(N_PERM)}
            if target not in allowed_targets:
                raise RuntimeError(f"invalid placement target {target}")
            expected_draw = None if target == "real" else int(target.removeprefix("perm"))
            expected_train_layer = 12 if placement == "mid" else 24
            lambda_brain = float(row["lambda_brain"])
            if (
                uid not in ALL_UIDS
                or uid not in runtime_uids
                or fold not in FOLDS
                or seed not in SEEDS
                or placement not in PLACEMENTS
                or target not in allowed_targets
                or eval_layer not in EVAL_LAYERS
                or int(row["train_layer"]) != expected_train_layer
                or row.get("perm_draw") != expected_draw
                or not math.isfinite(lambda_brain)
                or not math.isclose(
                    lambda_brain,
                    float(lambdas[placement]),
                    rel_tol=0,
                    abs_tol=1e-12,
                )
            ):
                raise RuntimeError(f"invalid placement categorical cell {row}")
            key = (uid, fold, seed, placement, target, eval_layer)
            if key in scores:
                raise RuntimeError(f"duplicate placement score {key}")
            score = float(row["unique_r2"])
            if not math.isfinite(score):
                raise RuntimeError(f"nonfinite placement unique_r2 {key}")
            scores[key] = score
            ppl_key = key[:5]
            value = float(row["perplexity"])
            if not math.isfinite(value) or value <= 0:
                raise RuntimeError(f"invalid placement perplexity {ppl_key}: {value}")
            if ppl_key in ppls and not math.isclose(
                ppls[ppl_key], value, rel_tol=0, abs_tol=1e-10
            ):
                raise RuntimeError(f"placement perplexity differs across eval layers {ppl_key}")
            ppls[ppl_key] = value
    if uids_seen != set(ALL_UIDS):
        raise RuntimeError(f"placement UID grid wrong {sorted(uids_seen)}")
    expected_scores = (
        len(ALL_UIDS)
        * len(FOLDS)
        * len(SEEDS)
        * len(PLACEMENTS)
        * (1 + N_PERM)
        * len(EVAL_LAYERS)
    )
    expected_ppls = expected_scores // len(EVAL_LAYERS)
    if len(scores) != expected_scores or len(ppls) != expected_ppls:
        raise RuntimeError(
            f"placement row grid wrong scores={len(scores)}/{expected_scores} "
            f"ppls={len(ppls)}/{expected_ppls}"
        )
    return scores, ppls


def validate_smoke_artifact(
    path: str | Path, calibration_path: str | Path
) -> dict:
    artifact = json.loads(Path(path).read_text())
    calibration = json.loads(Path(calibration_path).read_text())
    E.verify_calibration(calibration)
    expected_config = E.locked_config(calibration)
    runtime = artifact.get("runtime", {})
    if (
        artifact.get("science") is not False
        or artifact.get("stage") != "placement-smoke"
        or not runtime.get("smoke")
        or artifact.get("config") != expected_config
        or artifact.get("calibration_artifact_sha256")
        != calibration["artifact_sha256"]
    ):
        raise RuntimeError("not an E033 smoke artifact")
    uids = tuple(int(uid) for uid in runtime["uids"])
    folds = tuple(int(fold) for fold in runtime["folds"])
    seeds = tuple(int(seed) for seed in runtime["seeds"])
    n_perm = int(runtime["n_perm"])
    if (
        len(uids) != 2
        or len(set(uids)) != len(uids)
        or not set(uids) <= set(ALL_UIDS)
        or not folds
        or not set(folds) <= set(FOLDS)
        or not seeds
        or not set(seeds) <= set(SEEDS)
        or n_perm < 1
        or n_perm > N_PERM
    ):
        raise RuntimeError(f"invalid smoke runtime {runtime}")
    targets = ("real",) + tuple(f"perm{draw}" for draw in range(n_perm))
    expected = {
        (uid, fold, seed, placement, target, eval_layer)
        for uid in uids
        for fold in folds
        for seed in seeds
        for placement in PLACEMENTS
        for target in targets
        for eval_layer in EVAL_LAYERS
    }
    scores = {}
    ppls = {}
    lambdas = artifact.get("config", {}).get("lambdas", {})
    for row in artifact["rows"]:
        key = (
            int(row["uid"]),
            int(row["fold"]),
            int(row["seed"]),
            str(row["placement"]),
            str(row["target"]),
            int(row["eval_layer"]),
        )
        if key not in expected or key in scores:
            raise RuntimeError(f"invalid or duplicate smoke cell {key}")
        placement = key[3]
        target = key[4]
        expected_draw = None if target == "real" else int(target.removeprefix("perm"))
        expected_layer = 12 if placement == "mid" else 24
        lambda_brain = float(row["lambda_brain"])
        if (
            int(row["train_layer"]) != expected_layer
            or row.get("perm_draw") != expected_draw
            or placement not in lambdas
            or not math.isfinite(lambda_brain)
            or not math.isclose(
                lambda_brain,
                float(lambdas[placement]),
                rel_tol=0,
                abs_tol=1e-12,
            )
        ):
            raise RuntimeError(f"invalid smoke training metadata {key}")
        score = float(row["unique_r2"])
        ppl = float(row["perplexity"])
        if not math.isfinite(score) or not math.isfinite(ppl) or ppl <= 0:
            raise RuntimeError(f"nonfinite smoke cell {key}")
        scores[key] = score
        ppl_key = key[:5]
        if ppl_key in ppls and not math.isclose(
            ppls[ppl_key], ppl, rel_tol=0, abs_tol=1e-10
        ):
            raise RuntimeError(f"smoke PPL pairing failure {ppl_key}")
        ppls[ppl_key] = ppl
    if set(scores) != expected:
        raise RuntimeError(f"smoke grid mismatch {len(scores)}/{len(expected)}")

    effects = []
    for uid in uids:
        for fold in folds:
            for seed in seeds:
                for eval_layer in EVAL_LAYERS:
                    direct = {}
                    for placement in PLACEMENTS:
                        real = scores[
                            (uid, fold, seed, placement, "real", eval_layer)
                        ]
                        perm_mean = mean(
                            scores[
                                (
                                    uid,
                                    fold,
                                    seed,
                                    placement,
                                    f"perm{draw}",
                                    eval_layer,
                                )
                            ]
                            for draw in range(n_perm)
                        )
                        direct[placement] = real - perm_mean
                    effects.append(
                        {
                            "uid": uid,
                            "fold": fold,
                            "seed": seed,
                            "eval_layer": eval_layer,
                            "placement_interaction": direct["final"] - direct["mid"],
                        }
                    )
    if not all(math.isfinite(row["placement_interaction"]) for row in effects):
        raise RuntimeError("nonfinite smoke aggregation")
    return {
        "stage": "placement-smoke-validation",
        "science": False,
        "passed": True,
        "source_sha256": sha256_file(path),
        "grid_cell_count": len(scores),
        "ppl_cell_count": len(ppls),
        "paired_effect_cell_count": len(effects),
        "aggregation_sha256": hashlib.sha256(
            json.dumps(effects, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    }


def effect_cells(scores):
    direct = {layer: {placement: {} for placement in PLACEMENTS} for layer in EVAL_LAYERS}
    placement = {layer: {} for layer in EVAL_LAYERS}
    for uid in ALL_UIDS:
        for fold in FOLDS:
            for seed in SEEDS:
                key3 = (uid, fold, seed)
                for eval_layer in EVAL_LAYERS:
                    for attach in PLACEMENTS:
                        real = scores[(uid, fold, seed, attach, "real", eval_layer)]
                        perms = [
                            scores[
                                (
                                    uid,
                                    fold,
                                    seed,
                                    attach,
                                    f"perm{draw}",
                                    eval_layer,
                                )
                            ]
                            for draw in range(N_PERM)
                        ]
                        direct[eval_layer][attach][key3] = real - mean(perms)
                    placement[eval_layer][key3] = (
                        direct[eval_layer]["final"][key3]
                        - direct[eval_layer]["mid"][key3]
                    )
    return direct, placement


def subset_cells(cells: dict, uids: tuple[int, ...]) -> dict:
    return {key: value for key, value in cells.items() if key[0] in uids}


def language_checks(kd_ppl: dict, placement_ppl: dict):
    output = {}
    all_pass = True
    for attach in PLACEMENTS:
        vs_kd = {}
        vs_perm = {}
        for uid in HELDOUT_UIDS:
            for fold in FOLDS:
                for seed in SEEDS:
                    key3 = (uid, fold, seed)
                    real = math.log(placement_ppl[(uid, fold, seed, attach, "real")])
                    kd = math.log(kd_ppl[key3])
                    perms = [
                        math.log(
                            placement_ppl[(uid, fold, seed, attach, f"perm{draw}")]
                        )
                        for draw in range(N_PERM)
                    ]
                    vs_kd[key3] = real - kd
                    vs_perm[key3] = real - mean(perms)
        kd_summary = seed_collapsed_crossed(vs_kd, HELDOUT_UIDS)
        perm_summary = seed_collapsed_crossed(vs_perm, HELDOUT_UIDS)
        kd_pass = (
            kd_summary["participant_axis"]["one_sided_95_ucb"] <= LOG_PPL_MARGIN
            and kd_summary["fold_axis"]["one_sided_95_ucb"] <= LOG_PPL_MARGIN
        )
        perm_pass = all(
            summary["ci95"][0] >= -LOG_PPL_MARGIN
            and summary["ci95"][1] <= LOG_PPL_MARGIN
            for summary in (
                perm_summary["participant_axis"],
                perm_summary["fold_axis"],
            )
        )
        placement_pass = bool(kd_pass and perm_pass)
        all_pass = all_pass and placement_pass
        output[attach] = {
            "real_vs_kd": kd_summary,
            "real_vs_perm": perm_summary,
            "real_vs_kd_pass": bool(kd_pass),
            "real_vs_perm_pass": bool(perm_pass),
            "passed": placement_pass,
        }
    output["passed"] = bool(all_pass)
    output["log_margin"] = LOG_PPL_MARGIN
    output["ratio_margin"] = 1.05
    return output


def decision(placement_final, direct_final, language):
    placement_mean = placement_final["participant_axis"]["mean"]
    direct_mean = direct_final["participant_axis"]["mean"]
    placement_lower = placement_final["conservative_ci95"][0]
    direct_lower = direct_final["conservative_ci95"][0]
    placement_ucb = placement_final["conservative_one_sided_95_ucb"]
    direct_ucb = direct_final["conservative_one_sided_95_ucb"]
    fold_loo_positive = all(
        value > 0 for value in placement_final["fold_axis"]["loo_means"].values()
    )
    participant_positive = placement_final["participant_axis"]["n_positive"]
    rescue = bool(
        language["passed"]
        and placement_mean >= SESOI
        and direct_mean >= SESOI
        and placement_lower > 0
        and direct_lower > 0
        and fold_loo_positive
        and participant_positive >= 4
    )
    rejected = bool(
        language["passed"] and placement_ucb < SESOI and direct_ucb < SESOI
    )
    if not language["passed"]:
        label = "LANGUAGE-GUARD-FAIL"
    elif rescue:
        label = "PLACEMENT RESCUE"
    elif rejected:
        label = "MEANINGFUL PLACEMENT RESCUE REJECTED"
    else:
        label = "INCONCLUSIVE"
    return {
        "predeclared_analysis_classification": label,
        "not_an_adjudicated_verdict": True,
        "sesoi": SESOI,
        "criteria": {
            "language_pass": language["passed"],
            "placement_mean_ge_sesoi": placement_mean >= SESOI,
            "direct_final_mean_ge_sesoi": direct_mean >= SESOI,
            "placement_conservative_lower_gt_zero": placement_lower > 0,
            "direct_final_conservative_lower_gt_zero": direct_lower > 0,
            "all_fold_loo_placement_means_positive": fold_loo_positive,
            "placement_positive_participants_ge_4": participant_positive >= 4,
            "placement_one_sided_ucb_lt_sesoi": placement_ucb < SESOI,
            "direct_final_one_sided_ucb_lt_sesoi": direct_ucb < SESOI,
        },
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kd")
    parser.add_argument("--placement", nargs="+")
    parser.add_argument("--manifest")
    parser.add_argument("--calibration")
    parser.add_argument("--smoke-artifact")
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.smoke_artifact:
        if any((args.kd, args.placement, args.manifest)):
            raise RuntimeError("smoke validation cannot be mixed with scientific inputs")
        if not args.calibration:
            raise RuntimeError("smoke validation requires --calibration")
        output = validate_smoke_artifact(args.smoke_artifact, args.calibration)
        write_json(args.out, output)
        print(f"E033 smoke aggregation PASS wrote {args.out}")
        return
    if not all((args.kd, args.placement, args.manifest, args.calibration)):
        raise RuntimeError(
            "scientific analysis requires --kd, --placement, --manifest, and --calibration"
        )
    manifest, kd, placements = load_inputs(
        args.kd,
        args.placement,
        args.manifest,
        args.calibration,
    )
    calibration = json.loads(Path(args.calibration).read_text())
    if manifest["calibration_artifact_sha256"] != calibration["artifact_sha256"]:
        raise RuntimeError("calibration identity mismatch")
    _kd_scores, kd_ppl = index_kd(kd["rows"])
    placement_scores, placement_ppl = index_placements(placements)
    direct, placement = effect_cells(placement_scores)

    analyses = {}
    groups = {
        "heldout5": HELDOUT_UIDS,
        "builder4": BUILDER_UIDS,
        "all9": ALL_UIDS,
    }
    for group, uids in groups.items():
        analyses[group] = {}
        for eval_layer in EVAL_LAYERS:
            analyses[group][str(eval_layer)] = {
                "placement_interaction": crossed_summary(
                    subset_cells(placement[eval_layer], uids), uids
                ),
                "direct_mid": crossed_summary(
                    subset_cells(direct[eval_layer]["mid"], uids), uids
                ),
                "direct_final": crossed_summary(
                    subset_cells(direct[eval_layer]["final"], uids), uids
                ),
            }

    language = language_checks(kd_ppl, placement_ppl)
    confirmatory = analyses["heldout5"]["24"]
    classification = decision(
        confirmatory["placement_interaction"],
        confirmatory["direct_final"],
        language,
    )
    output = {
        "experiment": "E033",
        "manifest_sha256": manifest["manifest_sha256"],
        "calibration_artifact_sha256": calibration["artifact_sha256"],
        "input_sha256": {
            "kd": sha256_file(args.kd),
            "placements": {path: sha256_file(path) for path in args.placement},
            "manifest": sha256_file(args.manifest),
            "calibration": sha256_file(args.calibration),
        },
        "grid": {
            "uids": list(ALL_UIDS),
            "builder_uids": list(BUILDER_UIDS),
            "heldout_uids": list(HELDOUT_UIDS),
            "folds": list(FOLDS),
            "seeds": list(SEEDS),
            "placements": list(PLACEMENTS),
            "eval_layers": list(EVAL_LAYERS),
            "n_perm": N_PERM,
        },
        "analysis": analyses,
        "language_guard": language,
        "classification": classification,
    }
    output["analysis_sha256"] = hashlib.sha256(
        json.dumps(output, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()
    write_json(args.out, output)
    print(
        f"E033 analysis {classification['predeclared_analysis_classification']} "
        f"wrote {args.out}"
    )


if __name__ == "__main__":
    main()
