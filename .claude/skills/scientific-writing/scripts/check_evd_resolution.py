#!/usr/bin/env python3
"""D011 provenance checker: numbers trace to evidence, and every cite resolves.

Two checks, both mechanical:

1. Cite resolution. Every evidence reference in the file must resolve to a real
   record. In LaTeX that is `\\evd{E006}` / `\\evd{L016}`; in Markdown it is an
   inline `[E006]` / `[L016]`. An experiment key resolves to a file under
   docs/experiments/<KEY>*.md; a learning key resolves to an `L<NN>` entry in
   docs/learnings.md. A dangling cite is a fail.

2. Number-driven bare-number scan. The real D011 failure is a number with NO
   cite, which a cite-only checker reads as clean. So we scan result-like numbers
   (decimals, percentages, n=, +/-) and require a cite on the same source line.
   Our line conventions make this sound: a report paragraph is one line, and the
   LaTeX source is one sentence per line. Years, section/figure/table/equation
   numbers, and version tags are whitelisted.

Heuristic by nature: it flags candidates to look at, and it is conservative to
keep the noise low. Read the flagged line.

Usage:
    python check_evd_resolution.py FILE [--repo-root DIR]

Exit code: 0 clean, 1 if any dangling cite or any bare result-number.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EVD_TEX = re.compile(r"\\evd\{([ELel]\d+)\}")
GAP_TEX = re.compile(r"\\gap\{")
CITE_MD = re.compile(r"\[([ELel]\d+)\]")
ANY_CITE_LINE = re.compile(r"\\evd\{[ELel]\d+\}|\[[ELel]\d+\]")

# Result-like numbers: decimals, percentages, n=, +/- effect sizes.
RESULT_NUM = re.compile(r"(?<![\w.])([+\-]?\d+\.\d+|\d+(?:\.\d+)?%|n\s*=\s*\d+|±\s*\d|\+/-\s*\d)")
# Whitelist contexts that look numeric but are not empirical claims.
WHITELIST = re.compile(
    r"\b(19|20)\d{2}\b"                                  # years
    r"|\b(section|sec|figure|fig|table|tab|eq|equation|page|p|chapter|ch|appendix)\.?\s*\d"
    r"|\bv\d+(\.\d+)*\b"                                 # version tags
    r"|\b[ELSD]\d+\b",                                    # E/L/S/D record ids
    re.I,
)
CODE_FENCE = re.compile(r"^\s*```")
TEX_COMMENT = re.compile(r"^\s*%")


def find_repo_root(start: Path) -> Path:
    for p in [start.resolve(), *start.resolve().parents]:
        if (p / "docs" / "experiments").is_dir():
            return p
    raise SystemExit(f"could not find repo root (a parent with docs/experiments/) from {start}")


def resolve_key(key: str, root: Path) -> bool:
    kind, num = key[0].upper(), key[1:]
    if kind == "E":
        return any(root.glob(f"docs/experiments/{kind}{num}*.md")) or \
               any(root.glob(f"docs/experiments/{kind}{int(num):03d}*.md"))
    if kind == "L":
        learnings = root / "docs" / "learnings.md"
        if not learnings.exists():
            return False
        return re.search(rf"\bL{int(num):03d}\b|\bL{num}\b",
                         learnings.read_text(encoding="utf-8", errors="replace")) is not None
    return False


def iter_prose_lines(path: Path):
    in_fence = False
    is_md = path.suffix.lower() in (".md", ".markdown")
    for i, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if is_md and CODE_FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if path.suffix.lower() == ".tex" and TEX_COMMENT.match(raw):
            continue
        yield i, raw


def check(path: Path, root: Path):
    findings = []
    is_tex = path.suffix.lower() == ".tex"
    cite_re = EVD_TEX if is_tex else CITE_MD
    for lineno, text in iter_prose_lines(path):
        # 1. resolution
        for key in cite_re.findall(text):
            if not resolve_key(key, root):
                findings.append((lineno, "dangling-cite", f"{key} does not resolve under docs/"))
        # 2. bare result-number
        for m in RESULT_NUM.finditer(text):
            span_lo = max(0, m.start() - 16)
            ctx = text[span_lo:m.end() + 16]
            if WHITELIST.search(ctx):
                continue
            if not ANY_CITE_LINE.search(text):
                findings.append((lineno, "bare-number",
                                 f"'{m.group(0).strip()}' has no \\evd/[E0nn] cite on this line"))
                break  # one flag per line is enough to send you there
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="D011 provenance checker (cite resolution + bare numbers).")
    ap.add_argument("file", type=Path)
    ap.add_argument("--repo-root", type=Path, default=None)
    args = ap.parse_args(argv)
    if not args.file.exists():
        print(f"{args.file}: NOT FOUND", file=sys.stderr)
        return 1
    root = args.repo_root or find_repo_root(args.file)
    findings = check(args.file, root)
    if findings:
        print(f"\n{args.file}  ({len(findings)} D011 finding(s)):")
        for lineno, cat, msg in sorted(findings):
            print(f"  {args.file}:{lineno}: [{cat}] {msg}")
        print("\ncheck_evd_resolution: fill the gap or add the cite; do not delete the number.",
              file=sys.stderr)
        return 1
    print(f"{args.file}: D011 clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
