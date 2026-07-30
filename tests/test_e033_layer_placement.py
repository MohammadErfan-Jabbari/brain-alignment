"""Synthetic regression tests for the locked E033 runner and analyzer."""
from __future__ import annotations

import copy
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import e033_analyze_layer_placement as A  # noqa: E402
import e033_layer_placement as E  # noqa: E402


def valid_calibration() -> dict:
    calibration = {
        "stage": "E033A",
        "science_outcomes_opened": False,
        "passed": True,
        "initial": {"passed": True},
        "dynamic": {"rows": [], "checks": []},
        "frozen_lambdas": {"mid": 10.0, "final": 12.0},
        "runner_sha256": E.sha256_file(E.__file__),
        "e_record_sha256": E.sha256_file(E.E_RECORD),
    }
    calibration["artifact_sha256"] = E.artifact_digest(calibration)
    return calibration


class RunnerTests(unittest.TestCase):
    def test_permutation_is_deterministic_and_draw_specific(self):
        target = np.arange(240, dtype=float).reshape(120, 2)
        first = E.block_permutation(target, fold=2, seed=1, draw=3)
        repeated = E.block_permutation(target, fold=2, seed=1, draw=3)
        other = E.block_permutation(target, fold=2, seed=1, draw=4)
        np.testing.assert_array_equal(first, repeated)
        self.assertFalse(np.array_equal(first, other))

    def test_block_number_matches_zero_based_transformer_blocks(self):
        name = "base_model.model.model.layers.23.self_attn.q_proj.lora_A.default.weight"
        self.assertEqual(E.block_number(name), 23)
        self.assertIsNone(E.block_number("lm_head.weight"))

    def test_manifest_digest_ignores_its_own_digest_field(self):
        manifest = {"version": 1, "nested": {"b": 2, "a": 1}}
        digest = E.manifest_digest(manifest)
        manifest["manifest_sha256"] = digest
        self.assertEqual(E.manifest_digest(manifest), digest)

    def test_strict_manifest_verification_accepts_lock_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            calibration_path = Path(directory) / "calibration.json"
            calibration = valid_calibration()
            calibration_path.write_text(json.dumps(calibration))
            manifest = {
                "config": E.locked_config(calibration),
                "files": {
                    "runner": E.sha256_file(E.__file__),
                    "analyzer": E.sha256_file(E.ANALYZER),
                    "e_record": E.sha256_file(E.E_RECORD),
                    "calibration": E.sha256_file(calibration_path),
                },
                "calibration_artifact_sha256": calibration["artifact_sha256"],
            }
            manifest["manifest_sha256"] = E.manifest_digest(manifest)
            manifest_path = Path(directory) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest))
            verified = E.load_and_verify_manifest(manifest_path, calibration_path)
            self.assertEqual(verified["manifest_sha256"], manifest["manifest_sha256"])

            manifest["files"]["analyzer"] = "tampered"
            manifest["manifest_sha256"] = E.manifest_digest(manifest)
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(RuntimeError, "hashes changed"):
                E.load_and_verify_manifest(manifest_path, calibration_path)

    def test_calibration_provenance_rejects_old_runner(self):
        calibration = valid_calibration()
        calibration["runner_sha256"] = "old-runner"
        calibration["artifact_sha256"] = E.artifact_digest(calibration)
        with self.assertRaisesRegex(RuntimeError, "different runner"):
            E.verify_calibration(calibration)

    def test_runtime_input_verification_fails_closed_on_drift(self):
        manifest = {
            "inputs": {"identity": "locked"},
            "model_identities": {"identity": "locked"},
        }
        with (
            mock.patch.object(
                E, "bound_input_identity", return_value={"identity": "changed"}
            ),
            mock.patch.object(
                E, "model_identities", return_value={"identity": "locked"}
            ),
        ):
            with self.assertRaisesRegex(RuntimeError, "runtime data"):
                E.verify_bound_inputs(manifest, "unused")


class AnalyzerTests(unittest.TestCase):
    @staticmethod
    def _scores(mid_effect: float, final_effect: float):
        scores = {}
        for uid in A.ALL_UIDS:
            for fold in A.FOLDS:
                for seed in A.SEEDS:
                    for eval_layer in A.EVAL_LAYERS:
                        for placement, effect in (
                            ("mid", mid_effect),
                            ("final", final_effect),
                        ):
                            scores[
                                (uid, fold, seed, placement, "real", eval_layer)
                            ] = effect
                            for draw in range(A.N_PERM):
                                scores[
                                    (
                                        uid,
                                        fold,
                                        seed,
                                        placement,
                                        f"perm{draw}",
                                        eval_layer,
                                    )
                                ] = 0.0
        return scores

    def test_effect_cells_recovers_known_difference_in_differences(self):
        direct, placement = A.effect_cells(
            self._scores(mid_effect=0.001, final_effect=0.004)
        )
        key = (A.ALL_UIDS[0], A.FOLDS[0], A.SEEDS[0])
        self.assertAlmostEqual(direct[24]["mid"][key], 0.001)
        self.assertAlmostEqual(direct[24]["final"][key], 0.004)
        self.assertAlmostEqual(placement[24][key], 0.003)

    def test_crossed_summary_collapses_seed_and_fold_at_declared_units(self):
        cells = {
            (uid, fold, seed): 0.001 * (uid_index + 1)
            for uid_index, uid in enumerate(A.HELDOUT_UIDS)
            for fold in A.FOLDS
            for seed in A.SEEDS
        }
        summary = A.crossed_summary(cells, A.HELDOUT_UIDS)
        self.assertEqual(summary["participant_axis"]["n"], len(A.HELDOUT_UIDS))
        self.assertEqual(summary["fold_axis"]["n"], len(A.FOLDS))
        self.assertAlmostEqual(summary["participant_axis"]["mean"], 0.003)
        self.assertAlmostEqual(summary["fold_axis"]["mean"], 0.003)

    @staticmethod
    def _decision_summary(mean: float, lower: float, upper: float):
        return {
            "participant_axis": {
                "mean": mean,
                "n_positive": 5,
            },
            "fold_axis": {
                "loo_means": {str(fold): mean for fold in A.FOLDS},
            },
            "conservative_ci95": [lower, upper],
            "conservative_one_sided_95_ucb": upper,
        }

    def test_decision_requires_language_guard_and_both_effects(self):
        positive = self._decision_summary(0.003, 0.0015, 0.0045)
        language = {"passed": True}
        self.assertEqual(
            A.decision(positive, positive, language)[
                "predeclared_analysis_classification"
            ],
            "PLACEMENT RESCUE",
        )

        weak = self._decision_summary(0.0002, -0.0001, 0.0008)
        self.assertEqual(
            A.decision(weak, weak, language)[
                "predeclared_analysis_classification"
            ],
            "MEANINGFUL PLACEMENT RESCUE REJECTED",
        )

        failed_language = copy.deepcopy(language)
        failed_language["passed"] = False
        self.assertEqual(
            A.decision(positive, positive, failed_language)[
                "predeclared_analysis_classification"
            ],
            "LANGUAGE-GUARD-FAIL",
        )

    def test_language_margin_is_exactly_five_percent_on_log_scale(self):
        self.assertAlmostEqual(A.LOG_PPL_MARGIN, math.log(1.05))

    def test_nonfinite_scientific_cell_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "nonfinite KD"):
            A.index_kd(
                [
                    {
                        "uid": A.ALL_UIDS[0],
                        "fold": 0,
                        "seed": 0,
                        "eval_layer": 12,
                        "arm": "kd_only",
                        "unique_r2": float("nan"),
                        "perplexity": 10.0,
                    }
                ]
            )

    def test_smoke_validator_exercises_dual_layer_paired_aggregation(self):
        runtime = {
            "uids": [797, 848],
            "folds": [0],
            "seeds": [0],
            "n_perm": 1,
            "limit_tune": 64,
            "smoke": True,
        }
        rows = []
        for uid in runtime["uids"]:
            for placement, train_layer in (("mid", 12), ("final", 24)):
                for target, draw in (("real", None), ("perm0", 0)):
                    ppl = 10.0 + 0.1 * (placement == "final")
                    for eval_layer in A.EVAL_LAYERS:
                        rows.append(
                            {
                                "uid": uid,
                                "fold": 0,
                                "seed": 0,
                                "placement": placement,
                                "train_layer": train_layer,
                                "target": target,
                                "perm_draw": draw,
                                "eval_layer": eval_layer,
                                "unique_r2": 0.002
                                + 0.001 * (placement == "final")
                                - 0.0005 * (target == "perm0"),
                                "perplexity": ppl,
                                "lambda_brain": 10.0
                                if placement == "mid"
                                else 12.0,
                            }
                        )
        artifact = {
            "stage": "placement-smoke",
            "science": False,
            "runtime": runtime,
            "rows": rows,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "smoke.json"
            calibration_path = Path(directory) / "calibration.json"
            calibration = valid_calibration()
            artifact["config"] = E.locked_config(calibration)
            artifact["calibration_artifact_sha256"] = calibration["artifact_sha256"]
            path.write_text(json.dumps(artifact))
            calibration_path.write_text(json.dumps(calibration))
            result = A.validate_smoke_artifact(path, calibration_path)
            broken = copy.deepcopy(artifact)
            broken["rows"][0]["train_layer"] = 24
            path.write_text(json.dumps(broken))
            with self.assertRaisesRegex(RuntimeError, "training metadata"):
                A.validate_smoke_artifact(path, calibration_path)
            broken = copy.deepcopy(artifact)
            perm_row = next(row for row in broken["rows"] if row["target"] == "perm0")
            perm_row["perm_draw"] = None
            path.write_text(json.dumps(broken))
            with self.assertRaisesRegex(RuntimeError, "training metadata"):
                A.validate_smoke_artifact(path, calibration_path)
            broken = copy.deepcopy(artifact)
            broken["runtime"]["uids"] = [797]
            broken["rows"] = [row for row in broken["rows"] if row["uid"] == 797]
            path.write_text(json.dumps(broken))
            with self.assertRaisesRegex(RuntimeError, "invalid smoke runtime"):
                A.validate_smoke_artifact(path, calibration_path)
        self.assertTrue(result["passed"])
        self.assertEqual(result["grid_cell_count"], 16)
        self.assertEqual(result["ppl_cell_count"], 8)
        self.assertEqual(result["paired_effect_cell_count"], 4)


if __name__ == "__main__":
    unittest.main()
