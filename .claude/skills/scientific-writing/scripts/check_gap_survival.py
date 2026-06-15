#!/usr/bin/env python3
"""Public-cut gate: no \\gap{} may survive into a public manuscript.

A \\gap{} is an honest open slot, allowed and expected in a report or the extended
manuscript. A public cut is a frozen, externally-shared artifact, so an unfilled
gap shipping in one is exactly the D011 failure the gap mechanism exists to flag.
Either fill the gap (with a recorded number) or remove the claim before cutting.

Usage:
    python check_gap_survival.py PATH       # PATH is a public .tex file or dir

Exit code: 0 if no gap survives, 1 if any \\gap{ is present.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GAP = re.compile(r"\\gap\{")
TEX_COMMENT = re.compile(r"^\s*%")


def scan(path: Path):
    findings = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if TEX_COMMENT.match(raw):
            continue
        if GAP.search(raw):
            findings.append((lineno, raw.strip()[:100]))
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Block \\gap{} from surviving into a public cut.")
    ap.add_argument("path", type=Path)
    args = ap.parse_args(argv)
    targets = [args.path] if args.path.is_file() else sorted(args.path.rglob("*.tex"))
    if not targets:
        print(f"check_gap_survival: no .tex under {args.path}", file=sys.stderr)
        return 1
    failed = False
    for f in targets:
        gaps = scan(f)
        if gaps:
            failed = True
            print(f"\n{f}: {len(gaps)} surviving \\gap{{}} (must be filled or removed before a public cut):")
            for lineno, snip in gaps:
                print(f"  {f}:{lineno}: {snip}")
        else:
            print(f"{f}: no surviving gaps")
    if failed:
        print("\ncheck_gap_survival: a public cut may not ship an unfilled gap.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
