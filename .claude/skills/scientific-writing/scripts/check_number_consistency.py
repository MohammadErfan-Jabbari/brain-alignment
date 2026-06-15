"""Public-cut gate: keyed numbers must agree with the extended source.

The load-bearing numbers live once as `\\DeclareResult{key}{value}` in a
numbers.tex registry, and both layers cite them with `\\result{key}`. A public
cut vendors its own frozen copy of numbers.tex. This check confirms that for
every key the public cut actually uses, the value in the public's vendored
numbers.tex equals the value in the extended source's numbers.tex. That makes a
number impossible to drift between the layers during compression.

Inline (non-keyed) numbers are out of scope here; they are covered by
check_evd_resolution. This check is about the headline numbers that a committee
will quote, which is exactly why they are keyed.

Usage:
    python check_number_consistency.py PUBLIC_PATH --extended-root EXTENDED_DIR

Exit code: 0 if every used key agrees, 1 on any mismatch or missing definition.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DECLARE = re.compile(r"\\DeclareResult\{([^}]+)\}\{(.*)\}\s*$")
USE = re.compile(r"\\result\{([^}]+)\}")


def parse_registry(numbers_tex: Path) -> dict:
    out = {}
    if not numbers_tex.exists():
        return out
    for raw in numbers_tex.read_text(encoding="utf-8", errors="replace").splitlines():
        m = DECLARE.search(raw)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out


def find_numbers_tex(root: Path) -> Path | None:
    hits = sorted(root.rglob("numbers.tex"))
    return hits[0] if hits else None


def used_keys(public_path: Path) -> set:
    keys = set()
    files = [public_path] if public_path.is_file() else sorted(public_path.rglob("*.tex"))
    for f in files:
        for m in USE.finditer(f.read_text(encoding="utf-8", errors="replace")):
            keys.add(m.group(1).strip())
    return keys


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check keyed numbers agree between public cut and extended.")
    ap.add_argument("public", type=Path)
    ap.add_argument("--extended-root", type=Path, required=True)
    args = ap.parse_args(argv)

    pub_root = args.public if args.public.is_dir() else args.public.parent
    pub_reg_path = find_numbers_tex(pub_root)
    ext_reg_path = find_numbers_tex(args.extended_root)
    if ext_reg_path is None:
        print(f"check_number_consistency: no numbers.tex under extended root {args.extended_root}",
              file=sys.stderr)
        return 1
    pub_reg = parse_registry(pub_reg_path) if pub_reg_path else {}
    ext_reg = parse_registry(ext_reg_path)

    keys = used_keys(args.public)
    if not keys:
        print("check_number_consistency: no \\result{} keys used in the public cut; nothing to compare.")
        return 0

    failed = False
    for k in sorted(keys):
        ev, pv = ext_reg.get(k), pub_reg.get(k)
        if ev is None:
            print(f"  MISSING in extended registry: {k}")
            failed = True
        elif pv is None:
            print(f"  MISSING in public vendored registry: {k}  (extended has '{ev}')")
            failed = True
        elif ev != pv:
            print(f"  MISMATCH {k}: extended '{ev}' != public '{pv}'")
            failed = True
    if failed:
        print("\ncheck_number_consistency: a public cut must carry the same numbers as the extended.",
              file=sys.stderr)
        return 1
    print(f"check_number_consistency: {len(keys)} keyed number(s) agree with the extended source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
