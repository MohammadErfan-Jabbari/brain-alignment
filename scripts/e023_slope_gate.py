#!/usr/bin/env python3
"""E023a-prime: slope/knee gate for objective-specific KD compute.

Reads the existing E015 expansion output and asks the specific E023 gate:
is there a same-lineage, flat-enough, locally supported operating regime where
a saturated-regime KD-vs-LMFT residual could be identified?

This is analysis-only. It does not run KD training.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def local_slopes(rows: list[dict], y_key: str) -> list[dict]:
    out = []
    rs = sorted(rows, key=lambda r: r["bpb"])
    for a, b in zip(rs[:-1], rs[1:]):
        dx = math.log(b["bpb"]) - math.log(a["bpb"])
        dy = b[y_key] - a[y_key]
        out.append({
            "left": a["model"],
            "right": b["model"],
            "bpb_left": a["bpb"],
            "bpb_right": b["bpb"],
            "y_left": a[y_key],
            "y_right": b[y_key],
            "slope": dy / dx if abs(dx) > 1e-12 else float("nan"),
            "abs_delta_y": abs(dy),
            "abs_delta_bpb": abs(b["bpb"] - a["bpb"]),
        })
    return out


def family_gate(
    rows: list[dict],
    family: str,
    y_key: str,
    flat_abs_slope: float,
    max_pair_delta_y: float,
    max_decisive_bpb: float,
) -> dict:
    fam = [r for r in rows if r["family"] == family]
    slopes = local_slopes(fam, y_key)
    flat_pairs = [
        s for s in slopes
        if abs(s["slope"]) <= flat_abs_slope and s["abs_delta_y"] <= max_pair_delta_y
    ]
    decisive_flat_pairs = [
        s for s in flat_pairs
        if max(s["bpb_left"], s["bpb_right"]) <= max_decisive_bpb
    ]
    return {
        "family": family,
        "n": len(fam),
        "models": [r["model"] for r in sorted(fam, key=lambda r: r["bpb"])],
        "bpb_range": [min(r["bpb"] for r in fam), max(r["bpb"] for r in fam)] if fam else [None, None],
        "unique_r2_range": [min(r[y_key] for r in fam), max(r[y_key] for r in fam)] if fam else [None, None],
        "local_slopes": slopes,
        "flat_pairs": flat_pairs,
        "decisive_flat_pairs": decisive_flat_pairs,
        "passes": len(fam) >= 3 and bool(flat_pairs),
        "decisive_passes": len(fam) >= 3 and bool(decisive_flat_pairs),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="outputs/E015_expand/E015_expand_merged.json")
    ap.add_argument("--out", default="outputs/E023/e023a_slope_gate.json")
    ap.add_argument("--y-key", default="unique_r2_mid", choices=["unique_r2_mid", "unique_r2_best"])
    ap.add_argument("--families", nargs="+", default=["pythia", "qwen"])
    ap.add_argument("--flat-abs-slope", type=float, default=0.02,
                    help="Max |d unique-R2 / d log-bpb| for an E023b-supporting local flat pair.")
    ap.add_argument("--max-pair-delta-y", type=float, default=0.006,
                    help="Max local alignment swing tolerated inside a candidate flat pair.")
    ap.add_argument("--max-decisive-bpb", type=float, default=1.30,
                    help="Worst BPB allowed inside a decisive saturated/high-quality flat pair.")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text())
    rows = data["models"]
    gates = [
        family_gate(rows, fam, args.y_key, args.flat_abs_slope, args.max_pair_delta_y, args.max_decisive_bpb)
        for fam in args.families
    ]
    passed = [g for g in gates if g["passes"]]
    decisive_passed = [g for g in gates if g["decisive_passes"]]
    result = {
        "source": args.input,
        "y_key": args.y_key,
        "flat_abs_slope_threshold": args.flat_abs_slope,
        "max_pair_delta_y_threshold": args.max_pair_delta_y,
        "max_decisive_bpb_threshold": args.max_decisive_bpb,
        "gates": gates,
        "ready_for_e023b_pilot": bool(passed),
        "ready_for_decisive_e023b_training": bool(decisive_passed),
        "recommended_next": (
            "Build and gate an E023b/E023f same-lineage KD-vs-LMFT runner for the decisive passing pair(s)."
            if decisive_passed else
            "Do not run decisive E023b/E023f KD training; only lower-quality pilot support exists."
            if passed else
            "Do not run E023b/E023f KD training; the same-lineage saturated-regime support is not gate-clean."
        ),
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2))

    print(f"E023a-prime slope gate from {args.input}")
    for g in gates:
        print(f"\n{g['family']} n={g['n']} bpb={g['bpb_range'][0]:.3f}..{g['bpb_range'][1]:.3f} "
              f"uR2={g['unique_r2_range'][0]:+.4f}..{g['unique_r2_range'][1]:+.4f}")
        for s in g["local_slopes"]:
            print(f"  {Path(s['left']).name} -> {Path(s['right']).name}: "
                  f"slope={s['slope']:+.3f}, dy={s['y_right']-s['y_left']:+.4f}, dbpb={s['abs_delta_bpb']:.3f}")
        print(f"  PILOT_PASS={g['passes']} flat_pairs={len(g['flat_pairs'])}; "
              f"DECISIVE_PASS={g['decisive_passes']} decisive_flat_pairs={len(g['decisive_flat_pairs'])}")
    print(f"\nREADY_FOR_E023B_PILOT: {result['ready_for_e023b_pilot']}")
    print(f"READY_FOR_DECISIVE_E023B_TRAINING: {result['ready_for_decisive_e023b_training']}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
