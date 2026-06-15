#!/usr/bin/env python3
"""Deterministic anti-AI-tell linter for scientific prose (the C1 floor).

Scans Markdown or LaTeX files for the mechanical tells of LLM-generated academic
writing: an em-dash habit, a fixed set of filler/jargon words, throat-clearing
sentence openers, wordy phrases with shorter equivalents, and meta-commentary.

It does NOT judge voice, paragraph rhythm, or whether a hedge matches the
evidence. Those are judgment calls and live in references/writing-style.md and the
review pass. This script is the greppable floor only.

The goal is clarity and precision, not evading a detector. A finding is a prompt
to look, not always a defect: a flagged word can be the right word. Read the line.

Usage:
    python ai_tell_lint.py FILE [FILE ...] [--max-emdash N] [--quiet]

Exit code: 0 if clean, 1 if any finding (so it composes into one gate).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Single words that signal default-to-impressive prose. Word-boundary, case-insensitive.
# "robust" and "comprehensive" carry domain exceptions handled below.
JARGON = [
    "delve", "tapestry", "pivotal", "foster", "showcase", "testament",
    "leverage", "realm", "embark", "underscore", "multifaceted", "nuanced",
    "intricate", "cornerstone", "paradigm", "synergy", "holistic", "streamline",
    "cutting-edge", "groundbreaking", "crucial",
]
# "robust" is fine in statistics; flag only when not near a stats term.
ROBUST_OK = re.compile(r"robust\s+(estimat|standard error|regression|statistic|covariance|to\s)", re.I)
ROBUST = re.compile(r"\brobust\b", re.I)

# Phrases (cliche / throat-clearing / meta-commentary). Matched anywhere in a line.
PHRASES = {
    "throat-clearing": [
        r"it is important to note", r"it'?s important to note", r"it is worth (noting|mentioning)",
        r"it'?s worth (noting|mentioning)", r"it should be noted", r"in the realm of",
        r"in today'?s (rapidly )?(evolving|changing)", r"needless to say", r"it goes without saying",
        r"with that (being|said)", r"when it comes to", r"as a matter of fact",
        r"at the end of the day", r"this serves as a testament",
    ],
    "meta-commentary": [
        r"in this section,? we will", r"this section will (discuss|present|cover|examine)",
        r"we now turn our attention to", r"the following (paragraph|section) (examines|discusses|presents)",
    ],
    "cliche": [
        r"plays? an? (crucial|pivotal|key|important|vital) role", r"rich representations?",
        r"a wide (range|array) of", r"sheds? light on",
    ],
}
# Wordy phrase -> shorter equivalent.
WORDINESS = {
    r"in order to": "to",
    r"due to the fact that": "because",
    r"in spite of the fact that": "although",
    r"has the ability to": "can",
    r"at the present time": "now",
    r"a (large|great) number of": "many",
    r"in the event that": "if",
    r"for the purpose of": "to",
}

CODE_FENCE = re.compile(r"^\s*```")
TEX_COMMENT = re.compile(r"^\s*%")


def iter_prose_lines(path: Path):
    """Yield (lineno, text) for prose lines, skipping md code fences and tex comments."""
    in_fence = False
    suffix = path.suffix.lower()
    for i, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if suffix in (".md", ".markdown"):
            if CODE_FENCE.match(raw):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
        elif suffix == ".tex":
            if TEX_COMMENT.match(raw):
                continue
        yield i, raw


def lint_file(path: Path, max_emdash: int):
    findings = []  # (lineno, category, message)
    emdash_lines = []
    for lineno, text in iter_prose_lines(path):
        low = text.lower()
        if "—" in text:
            emdash_lines.append(lineno)
        for w in JARGON:
            if re.search(rf"\b{re.escape(w)}\b", text, re.I):
                findings.append((lineno, "jargon", f"'{w}': is this the most precise word, or a default?"))
        if ROBUST.search(text) and not ROBUST_OK.search(text):
            findings.append((lineno, "jargon", "'robust': outside a statistics sense, prefer a precise word"))
        if re.search(r"\bcomprehensive\b", text, re.I):
            findings.append((lineno, "jargon", "'comprehensive': usually filler; state the actual scope"))
        for cat, pats in PHRASES.items():
            for p in pats:
                if re.search(p, low):
                    findings.append((lineno, cat, f"matched /{p}/  delete or rewrite"))
        for p, repl in WORDINESS.items():
            if re.search(p, low):
                findings.append((lineno, "wordiness", f"/{p}/ -> '{repl}'"))
    if len(emdash_lines) > max_emdash:
        findings.append((emdash_lines[max_emdash], "em-dash",
                         f"{len(emdash_lines)} em-dashes (budget {max_emdash}); lines {emdash_lines}"))
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Anti-AI-tell linter for scientific prose.")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--max-emdash", type=int, default=3, help="em-dash budget per file (default 3)")
    ap.add_argument("--quiet", action="store_true", help="only print on findings")
    args = ap.parse_args(argv)

    total = 0
    for path in args.files:
        if not path.exists():
            print(f"{path}: NOT FOUND", file=sys.stderr)
            total += 1
            continue
        findings = lint_file(path, args.max_emdash)
        if findings:
            print(f"\n{path}  ({len(findings)} finding(s)):")
            for lineno, cat, msg in sorted(findings):
                print(f"  {path}:{lineno}: [{cat}] {msg}")
            total += len(findings)
        elif not args.quiet:
            print(f"{path}: clean")
    if total:
        print(f"\nai_tell_lint: {total} finding(s). Fix silently, then re-run.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
