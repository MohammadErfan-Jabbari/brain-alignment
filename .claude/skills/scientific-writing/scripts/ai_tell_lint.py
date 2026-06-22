#!/usr/bin/env python3
"""Deterministic anti-AI-tell linter for scientific prose (the C1 floor).

Scans Markdown or LaTeX files for the mechanical tells of LLM-generated academic
writing: an em-dash habit, a fixed set of filler/jargon words, throat-clearing
sentence openers, wordy phrases with shorter equivalents, and meta-commentary.

It does NOT fully judge voice, paragraph rhythm, or whether a hedge matches the
evidence. Those are judgment calls and live in references/writing-style.md and the
review pass. This script is the greppable floor only.

It also emits SOFT WARNINGS for two classes the linter can only partially reach:
the storytelling/register tells (Class A: an abstraction handed an agency verb, a
self-narrated rhetorical move, internal-metaphor leakage) and reflex passive
density (Class B). These are heuristic tripwires, not the gate — they carry no
banned token and need human/agent judgment, so they print but do NOT affect the
exit code. The real Class-A catch is the prose-register-auditor agent (review pass).

The goal is clarity and precision, not evading a detector. A finding is a prompt
to look, not always a defect: a flagged word can be the right word. Read the line.

Usage:
    python ai_tell_lint.py FILE [FILE ...] [--max-emdash N] [--quiet] [--no-warn]

Exit code: 0 if no HARD finding, 1 if any hard finding (so it composes into one
gate). Soft warnings never change the exit code.
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

# --- Soft-warning detectors (Class A register + Class B passive). Heuristic; exit-code-neutral. ---
# Class A1: an abstraction given a verb of agency/stakes. Subject, then 0-3 words, then verb.
_AGENCY_SUBJECTS = (
    "question", "idea", "thesis", "manuscript", "paper", "study", "result", "finding",
    "analysis", "contribution", "story", "argument", "narrative", "approach", "framework",
    "hypothesis", "notion", "concept", "claim",
)
_AGENCY_VERBS = (
    "earns?", "earned", "survives?", "survived", "wants?", "wanted", "knows?", "knew",
    "believes?", "believed", "wishes?", "hopes?", "hoped", "seeks?", "sought", "struggles?",
    "fights?", "fought", "climbs?", "climbed", "decides?", "decided", "cares?", "refuses?",
    "demands?", "deserves?", "deserved", "locates?", "located",
)
AGENCY_RE = re.compile(
    rf"\b(?P<subj>{'|'.join(_AGENCY_SUBJECTS)})\b(?:\s+\w+){{0,3}}?\s+(?P<verb>{'|'.join(_AGENCY_VERBS)})\b",
    re.I,
)
# Class A2: self-narration of the rhetorical move.
SELF_NARRATION = [
    r"saying\s+(so|this|that|it)\s+(plainly|clearly|out loud|directly)",
    r"is\s+what\s+(locates|reveals|makes|defines|tells\s+us|earns|matters|gives)",
    r"what\s+(locates|reveals|defines)\s+the\s+(real\s+)?(contribution|point|question|stake|story)",
    r"only\s+earns\s+a\s+(thesis|paper|place|spot|seat)",
]
# Class A3: internal-scaffolding metaphors leaking into reader-facing prose.
# Includes the repo's own methodology jargon, which leaked into the v0.1/v0.2 manuscript.
METAPHOR_RE = re.compile(r"\b(ladder|rungs?|kill-gated|load-bearing|lever)\b", re.I)
# Class B: reflex passive. A meter, not a per-sentence judgment.
PASSIVE_RE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(\w+ed|done|made|shown|found|measured|given|taken|"
    r"seen|known|built|drawn|held|set|written|fit|cast|run|chosen|computed|derived|defined|"
    r"reported|observed|obtained|applied|performed|conducted|used)\b",
    re.I,
)
SENT_SPLIT = re.compile(r"[.!?]+")
PASSIVE_MIN_SENTENCES = 6
PASSIVE_RATIO_WARN = 0.33

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
    is_tex = path.suffix.lower() == ".tex"
    for lineno, text in iter_prose_lines(path):
        low = text.lower()
        # Unicode em-dash anywhere; in LaTeX an em-dash is written `---`, which the
        # unicode-only check missed entirely (the v0.2 abstract slipped two through).
        if "—" in text or (is_tex and "---" in text):
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


def register_warnings(path: Path):
    """Heuristic Class-A (register/storytelling) warnings. Soft; never a hard fail."""
    warnings = []  # (lineno, category, message)
    for lineno, text in iter_prose_lines(path):
        m = AGENCY_RE.search(text)
        if m:
            warnings.append((lineno, "register/agency",
                             f"'{m.group('subj')} … {m.group('verb')}': an abstraction given a verb of "
                             f"agency — you or the evidence act, not the abstraction"))
        low = text.lower()
        for p in SELF_NARRATION:
            if re.search(p, low):
                warnings.append((lineno, "register/self-narration",
                                 f"matched /{p}/  state the claim, do not narrate the move"))
        if METAPHOR_RE.search(text):
            warnings.append((lineno, "register/metaphor",
                             "'ladder'/'rung' is repo scaffolding — name the thing in prose for the reader"))
    return warnings


def passive_density(path: Path):
    """Whole-file reflex-passive meter (Class B). Returns one soft warning or None."""
    prose = " ".join(t for _, t in iter_prose_lines(path))
    sentences = [s for s in SENT_SPLIT.split(prose) if s.strip()]
    n_sent = len(sentences)
    n_passive = len(PASSIVE_RE.findall(prose))
    if n_sent < PASSIVE_MIN_SENTENCES:
        return None
    ratio = n_passive / n_sent
    if ratio >= PASSIVE_RATIO_WARN:
        return (1, "passive-density",
                f"~{n_passive} passive constructions over {n_sent} sentences "
                f"(ratio {ratio:.2f} >= {PASSIVE_RATIO_WARN}); passive as a reflex flattens the prose — "
                f"vary it where the agent is the topic (not a per-sentence verdict)")
    return None


def collect_warnings(path: Path):
    ws = register_warnings(path)
    pd = passive_density(path)
    if pd:
        ws.append(pd)
    return sorted(ws)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Anti-AI-tell linter for scientific prose.")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--max-emdash", type=int, default=0,
                    help="em-dash budget per file (default 0: em-dashes are banned in this repo's prose)")
    ap.add_argument("--quiet", action="store_true", help="only print on findings")
    ap.add_argument("--no-warn", action="store_true",
                    help="suppress the soft register/passive warnings (heuristic, exit-neutral)")
    args = ap.parse_args(argv)

    total = 0
    warn_total = 0
    for path in args.files:
        if not path.exists():
            print(f"{path}: NOT FOUND", file=sys.stderr)
            total += 1
            continue
        findings = lint_file(path, args.max_emdash)
        warnings = [] if args.no_warn else collect_warnings(path)
        if findings:
            print(f"\n{path}  ({len(findings)} finding(s)):")
            for lineno, cat, msg in sorted(findings):
                print(f"  {path}:{lineno}: [{cat}] {msg}")
            total += len(findings)
        elif not args.quiet and not warnings:
            print(f"{path}: clean")
        if warnings:
            print(f"\n{path}  ({len(warnings)} soft warning(s) — heuristic; the prose-register-auditor "
                  f"is the real gate):")
            for lineno, cat, msg in warnings:
                print(f"  {path}:{lineno}: [{cat}] {msg}")
            warn_total += len(warnings)
    if warn_total:
        print(f"\nai_tell_lint: {warn_total} soft warning(s) (register/passive). These do not fail the "
              f"gate; route the draft through the prose-register-auditor.")
    if total:
        print(f"\nai_tell_lint: {total} finding(s). Fix silently, then re-run.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
