"""Outcome-blind E031 C1 power calibration from recorded E030 variance."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from scipy.stats import nct, t


EXPECTED_E030_SHA256 = (
    "43a4f3b01641072345149e651cdd0b1ae0c903bb74366db2006f31b89d8dd818"
)
EVALUATION_PARTICIPANTS = ("797", "837", "841", "856", "880")
METRICS = ("A_aligned_above_nuisance", "Q_aligned_minus_twin")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def detectable_excess(
    *,
    sd: float,
    n: int,
    alpha: float,
    target_power: float,
) -> float:
    """Return the mean excess above a null needed for one-sided t-test power."""
    degrees_freedom = n - 1
    critical = t.ppf(1.0 - alpha, degrees_freedom)
    lower = 0.0
    upper = max(0.1, 20.0 * sd)
    for _ in range(200):
        midpoint = (lower + upper) / 2.0
        noncentrality = midpoint / (sd / math.sqrt(n))
        power = 1.0 - nct.cdf(critical, degrees_freedom, noncentrality)
        if power < target_power:
            lower = midpoint
        else:
            upper = midpoint
    return upper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--e030-analysis",
        type=Path,
        default=Path("outputs/E030/analysis.json"),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--family-size", type=int, default=4)
    parser.add_argument("--family-alpha", type=float, default=0.05)
    parser.add_argument("--target-power", type=float, default=0.80)
    parser.add_argument("--sesoi", type=float, default=0.002)
    args = parser.parse_args()

    source_hash = sha256(args.e030_analysis)
    if source_hash != EXPECTED_E030_SHA256:
        raise SystemExit(
            "E030 analysis hash mismatch: "
            f"expected {EXPECTED_E030_SHA256}, observed {source_hash}"
        )

    with args.e030_analysis.open("r", encoding="utf-8") as handle:
        analysis = json.load(handle)

    cell = analysis["c1"]["cells"]["imageability_primary"]
    per_contrast_alpha = args.family_alpha / args.family_size
    n = len(EVALUATION_PARTICIPANTS)
    critical = t.ppf(1.0 - per_contrast_alpha, n - 1)
    metrics: dict[str, dict[str, float | list[float]]] = {}

    for metric in METRICS:
        values = [
            float(cell[metric]["by_unit"][participant])
            for participant in EVALUATION_PARTICIPANTS
        ]
        mean = sum(values) / n
        sd = math.sqrt(sum((value - mean) ** 2 for value in values) / (n - 1))
        excess = detectable_excess(
            sd=sd,
            n=n,
            alpha=per_contrast_alpha,
            target_power=args.target_power,
        )
        metrics[metric] = {
            "values": values,
            "mean": mean,
            "sample_sd": sd,
            "one_sided_lower_bound_halfwidth": critical * sd / math.sqrt(n),
            "detectable_excess_over_null": excess,
            "true_mean_needed_above_sesoi_null": args.sesoi + excess,
        }

    result = {
        "scope": (
            "Historical E030 variance calibration only; not an E031 outcome "
            "or an estimate of an E031 target-arm mean."
        ),
        "source": {
            "path": str(args.e030_analysis.resolve()),
            "sha256": source_hash,
            "cell": "c1.cells.imageability_primary",
            "participants": list(EVALUATION_PARTICIPANTS),
        },
        "design": {
            "n": n,
            "family_alpha": args.family_alpha,
            "family_size": args.family_size,
            "per_contrast_one_sided_alpha": per_contrast_alpha,
            "target_power": args.target_power,
            "sesoi": args.sesoi,
        },
        "metrics": metrics,
    }

    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
