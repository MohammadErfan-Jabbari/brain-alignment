#!/usr/bin/env python3
"""Write the post-E016 matched-information text-feature control launcher.

This script prepares a bash pipeline only; it does not launch the control. The
control should be run after the active TRIBE Phase-3 result is positive enough
to require a matched-information non-brain target comparison.
"""
from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "outputs/E016_tribe/phase3/run_textfeat_control_20260703.sh"


def script_text(root: Path, gpu: int, model: str, batch_size: int) -> str:
    root_s = str(root)
    model_tag = model.replace("/", "--")
    return f"""#!/usr/bin/env bash
set -euo pipefail

ROOT={root_s}
GPU="${{GPU:-{gpu}}}"
export HF_HOME="${{HF_HOME:-/home/centcom/data/hf-cache}}"

TRAIN_CACHE="$ROOT/outputs/E016_tribe/kd_targets/text_feature/{model_tag}/train_start0_n95999_d20484_full.npz"
HELDOUT_CACHE="$ROOT/outputs/E016_tribe/kd_targets/text_feature/{model_tag}/heldout_start0_n1999_d20484_full.npz"
RUN_JSON="$ROOT/outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.json"
ANALYSIS_JSON="$ROOT/outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.analysis.json"
MODEL_DIR="$ROOT/outputs/E016_tribe/phase3/model_artifacts/textfeat_gpt2_n95999_s0-1-2_lam0.1"
LOG="$ROOT/outputs/E016_tribe/phase3/phase3_full_textfeat_gpt2_n95999_s0-1-2_lam0.1.log"

mkdir -p "$(dirname "$TRAIN_CACHE")" "$(dirname "$RUN_JSON")"
exec > >(tee -a "$LOG") 2>&1

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] E016 textfeat matched-information control starting on GPU $GPU"
echo "ROOT=$ROOT"
echo "TRAIN_CACHE=$TRAIN_CACHE"
echo "HELDOUT_CACHE=$HELDOUT_CACHE"
echo "RUN_JSON=$RUN_JSON"
echo "ANALYSIS_JSON=$ANALYSIS_JSON"
echo "MODEL_DIR=$MODEL_DIR"

cd "$ROOT"
if [[ ! -f "$TRAIN_CACHE" ]]; then
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Building full train text-feature cache"
  CUDA_VISIBLE_DEVICES="$GPU" uv run python scripts/build_text_feature_target_cache.py \\
    --split train \\
    --start 0 \\
    --limit 95999 \\
    --model {model} \\
    --target-dim 20484 \\
    --projection random \\
    --projection-seed 0 \\
    --batch-size {batch_size} \\
    --device auto \\
    --out "$TRAIN_CACHE"
else
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Train text-feature cache exists; skipping"
fi

if [[ ! -f "$HELDOUT_CACHE" ]]; then
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Building full heldout text-feature cache"
  CUDA_VISIBLE_DEVICES="$GPU" uv run python scripts/build_text_feature_target_cache.py \\
    --split heldout \\
    --start 0 \\
    --limit 1999 \\
    --model {model} \\
    --target-dim 20484 \\
    --projection random \\
    --projection-seed 0 \\
    --batch-size {batch_size} \\
    --device auto \\
    --out "$HELDOUT_CACHE"
else
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Heldout text-feature cache exists; skipping"
fi

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Validating full text-feature caches"
python - <<'PY'
import json
from pathlib import Path
import numpy as np

for path in [
    Path("outputs/E016_tribe/kd_targets/text_feature/{model_tag}/train_start0_n95999_d20484_full.npz"),
    Path("outputs/E016_tribe/kd_targets/text_feature/{model_tag}/heldout_start0_n1999_d20484_full.npz"),
]:
    raw = np.load(path, allow_pickle=True)
    targets = raw["targets"]
    counts = raw["segment_counts"]
    meta = json.loads(path.with_suffix(".json").read_text())
    print(path)
    print(f"  shape={{targets.shape}} elapsed_s={{meta.get('elapsed_s')}} size_gb={{path.stat().st_size / 1e9:.3f}}")
    print(f"  counts min={{int(counts.min())}} mean={{counts.mean():.2f}} max={{int(counts.max())}} missing={{int((counts <= 0).sum())}}")
    print(f"  finite={{bool(np.isfinite(targets).all())}}")
    if targets.shape[1] != 20484:
        raise SystemExit(f"wrong target dimension for {{path}}: {{targets.shape}}")
    if np.any(counts <= 0):
        raise SystemExit(f"missing text-feature targets in {{path}}")
    if not np.isfinite(targets).all():
        raise SystemExit(f"non-finite targets in {{path}}")
    if "non-brain control" not in meta.get("science_status", ""):
        raise SystemExit(f"unexpected science_status for {{path}}: {{meta.get('science_status')}}")
PY

if [[ ! -f "$RUN_JSON" ]]; then
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Running full GPT-2 textfeat control arms"
  CUDA_VISIBLE_DEVICES="$GPU" uv run python scripts/run_tribe_phase3.py \\
    --target-cache "$TRAIN_CACHE" \\
    --heldout-target-cache "$HELDOUT_CACHE" \\
    --target-label textfeat \\
    --out "$RUN_JSON" \\
    --teacher gpt2-medium \\
    --student gpt2 \\
    --seeds 0,1,2 \\
    --lambda-brain-grid 0.1 \\
    --epochs 1 \\
    --lr 5e-5 \\
    --batch-size 4 \\
    --max-length 64 \\
    --limit-heldout 1999 \\
    --save-model-dir "$MODEL_DIR"
else
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Run JSON exists; skipping training"
fi

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Running analyzer"
uv run python scripts/analyze_tribe_phase3.py "$RUN_JSON" --out "$ANALYSIS_JSON"

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] E016 textfeat matched-information control complete"
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--gpu", type=int, default=1)
    ap.add_argument("--model", default="gpt2-medium")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if args.batch_size <= 0:
        raise ValueError("--batch-size must be positive")
    out = args.out
    if out.exists() and not args.force:
        raise FileExistsError(f"refusing to overwrite existing launcher: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(script_text(ROOT, args.gpu, args.model, args.batch_size), encoding="utf-8")
    out.chmod(0o755)
    print(out)
    print("Launcher written only; not executed.")


if __name__ == "__main__":
    main()
