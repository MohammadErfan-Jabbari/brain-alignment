#!/usr/bin/env python3
"""Per-layer verifier dispatcher for the scientific-writing skill.

Runs the deterministic checks that apply to a given deliverable layer and returns
one aggregate exit code, so the whole gate is a single call.

    report   : ai_tell_lint, check_evd_resolution        (Markdown)
    extended : ai_tell_lint, check_evd_resolution        (LaTeX)
    public   : the above, plus check_gap_survival, check_number_consistency,
               check_claim_survival                       (the compression gate)

A public cut is the highest-stakes layer, so a public-layer check that is not yet
implemented BLOCKS rather than passing silently: shipping a public cut through an
incomplete gate is exactly the failure the gate exists to prevent.

Usage:
    python run_checks.py --layer {report|extended|public} PATH [--extended-root DIR]

PATH may be a file or a directory (the directory is globbed for the layer's file
type). For the public layer, --extended-root points at the extended source so the
number/claim survival checks can diff against it.

Exit code: 0 if every applicable check passed, 1 otherwise.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC_ONLY = ["check_gap_survival.py", "check_number_consistency.py", "check_claim_survival.py"]


def files_for(layer: str, path: Path):
    if path.is_file():
        return [path]
    pattern = "*.md" if layer == "report" else "*.tex"
    return sorted(path.rglob(pattern))


def run(script: str, *script_args) -> int:
    target = HERE / script
    if not target.exists():
        return 127  # signal "not implemented" to the caller
    proc = subprocess.run([sys.executable, str(target), *map(str, script_args)])
    return proc.returncode


def main(argv=None):
    ap = argparse.ArgumentParser(description="Per-layer scientific-writing verifier gate.")
    ap.add_argument("--layer", required=True, choices=["report", "extended", "public"])
    ap.add_argument("path", type=Path)
    ap.add_argument("--extended-root", type=Path, default=None,
                    help="extended source dir (public layer, for number/claim survival)")
    args = ap.parse_args(argv)

    targets = files_for(args.layer, args.path)
    if not targets:
        print(f"run_checks: no files to check at {args.path} for layer '{args.layer}'", file=sys.stderr)
        return 1

    failed = False
    emdash = "--max-emdash=3"

    for f in targets:
        print(f"\n=== {args.layer}: {f} ===")
        if run("ai_tell_lint.py", f, emdash) != 0:
            failed = True
        if run("check_evd_resolution.py", f) != 0:
            failed = True

    if args.layer == "public":
        print("\n=== public compression gate ===")
        for script in PUBLIC_ONLY:
            rc = run(script, *( [args.path, "--extended-root", args.extended_root]
                                if args.extended_root else [args.path] ))
            if rc == 127:
                print(f"BLOCKED: {script} is not yet implemented. A public cut may not ship through "
                      f"an incomplete compression gate (D011 / compression-preserves-truth).",
                      file=sys.stderr)
                failed = True
            elif rc != 0:
                failed = True

    print("\n" + ("run_checks: FAIL (fix findings above)" if failed else "run_checks: PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
