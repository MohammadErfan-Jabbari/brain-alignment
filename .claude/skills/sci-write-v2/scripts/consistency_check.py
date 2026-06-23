#!/usr/bin/env python3
r"""consistency_check (F19 DET) — cross-section number consistency over the drafted prose.

Two deterministic checks — the #1 reviewer-catch and our abstract-taste rule:

  abstract-body-mismatch  every RESULT number (a DECIMAL — not a model name, version, or year) stated in the
                          ABSTRACT must also appear in the BODY. An abstract reporting a value the body does not
                          (SC-XS-1: abstract "+0.021" vs body "+0.028") is the #1 reviewer-catch. Model names
                          ("Qwen2.5-0.5B"), versions ("GPT-2"), and years/counts ("2024", "n=9") are excluded —
                          they are not results; a leading "+" is normalized so "+0.028" == "0.028". (Residual,
                          documented: a rounded abstract decimal that differs from the body, "0.02" vs "0.021",
                          still flags — use the body's number in the abstract.)
  ci-in-abstract          the abstract must NOT carry a full point-estimate + 95% CI string. The abstract states
                          direction/magnitude; the full CI lives in the body. (SC-XS-2; our manuscript-prose-taste
                          rule — abstracts drop full point-estimates+CIs.)

The abstract section is the %%SECTION whose id is (or contains) "abstract"; everything else is body. If there is
no abstract section, there is nothing cross-section to check (return clean).

NOT here: caption <= figure (SC-XS-3) is RUB — judged by the F5 scope reader (P2-D-5, re-mapped F19->F5),
sizing each figure's `caption` against its `shows` (what the figure plots). Not a DET / not this script.

Usage:
    python consistency_check.py validate PROSE_FILE
    python consistency_check.py --selftest

Exit code: 0 clean, 1 on any finding (or bad input).
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

SEC_RE = re.compile(r"^%%SECTION[ \t]+(\S+)[ \t]*$", re.M)
SEC_LINE = re.compile(r"%%SECTION[ \t]+\S")
EVD_RE = re.compile(r"\\evd\{[^}]*\}\{[^}]*\}")
PCT = re.compile(r"(?<!\\)%")
# A RESULT number: a DECIMAL (optionally signed/percent) that is NOT part of an identifier and NOT a bare integer.
# This is the estimand of the abstract<->body check — a result the abstract reports — isolated from a model name
# ("Qwen2.5-0.5B"), a version ("GPT-2"), or a year/count ("2024", "n=9"). The L060 fix: matching every numeric
# literal verbatim made the check an over-block (the first abstract naming a model tripped it). A leading '+' is
# normalized away at comparison so "+0.028" == "0.028". Residual (documented): a rounded abstract decimal that
# differs from the body ("0.02" vs "0.021") still flags — use the body's number in the abstract.
# lookahead: not part of an identifier (no trailing letter) and not a version (no ".<digit>" continuation),
# but a trailing SENTENCE period ("the gap is +0.028.") is fine — that period is not followed by a digit.
RESULT_NUM_RE = re.compile(r"(?<![\w.\-])[-+]?\d*\.\d+%?(?![\w])(?!\.\d)")
# A 95% confidence interval written out in the abstract (the full-CI tell). Tolerant of LaTeX % escaping,
# spacing, and the bracket/paren forms. "CI" followed by a bracket/colon, or a "95% CI", or a \pm / ± estimate.
CI_RE = re.compile(r"95\s*\\?%?\s*(confidence\s+interval|ci)|\bci\s*[\[:(]|\\pm\b|±", re.I)


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_tex_comments(text: str) -> str:
    out = []
    for line in text.split("\n"):
        if SEC_LINE.match(line):
            out.append(line)
            continue
        m = PCT.search(line)
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def split_abstract_body(prose: str) -> tuple[str, str]:
    """-> (abstract_text, body_text). The abstract section's id is exactly 'abstract' (case-insensitive); the
    id is reserved — a section like 'abstract-of-results' is NOT the abstract (substring match over-grabbed)."""
    marks = [(m.group(1), m.start(), m.end()) for m in SEC_RE.finditer(prose)]
    abstract, body = [], []
    for i, (sid, _s, e) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(prose)
        chunk = prose[e:end]
        (abstract if sid.lower() == "abstract" else body).append(chunk)
    return "".join(abstract), "".join(body)


def _result_nums(text: str) -> Counter:
    """Multiset of RESULT numbers (decimals, not identifier fragments); a leading '+' is normalized away."""
    code = EVD_RE.sub("", text)
    return Counter(m.group(0).lstrip("+") for m in RESULT_NUM_RE.finditer(code))


def check(prose: str) -> list[str]:
    f = []
    code = strip_tex_comments(normalize(prose))
    abstract, body = split_abstract_body(code)
    if not abstract.strip():
        return f  # no abstract section -> nothing cross-section to reconcile
    abs_nums, body_nums = _result_nums(abstract), _result_nums(body)
    for n in abs_nums:
        if n not in body_nums:
            f.append(f"[abstract-body-mismatch] the abstract reports the result '{n}' but the body does not — "
                     f"the #1 reviewer-catch; the abstract must carry the body's numbers, not a different value")
    if CI_RE.search(abstract):
        f.append("[ci-in-abstract] the abstract carries a full point-estimate + 95% CI — abstracts drop the "
                 "full CI (state direction/magnitude; the full CI lives in the body)")
    return f


def report(findings: list[str]) -> int:
    if findings:
        print(f"\nconsistency_check (F19 DET) — {len(findings)} finding(s):")
        for m in findings:
            print(f"  {m}")
        print("\nconsistency_check: FAIL")
        return 1
    print("consistency_check: PASS")
    return 0


# --------------------------------------------------------------------------- selftest
def _selftest() -> int:
    ok = True

    def expect(name, prose, want_flag, rule=None):
        nonlocal ok
        fnd = check(prose)
        flagged = len(fnd) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in fnd)
        good = (flagged == want_flag) and (rule_hit if want_flag else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name + ("" if good else f" -> got {fnd}"))
        ok = ok and good

    # real LaTeX escapes the percent ("95\%"); a raw "95%" is a comment and would truncate the line.
    body = ("%%SECTION results\nThe trained-untrained gap reached +0.028 over reliable voxels "
            "(95\\% CI [+0.018, +0.038]), with n=9 subjects. \\evd{C1}{strong}\n")
    # SC-XS-1: abstract states +0.021 but the body reports +0.028 -> mismatch.
    expect("SC-XS-1 abstract!=body number",
           "%%SECTION abstract\nWe find a +0.021 gain. \\evd{C1}{strong}\n" + body, True, "abstract-body-mismatch")
    # clean: abstract states +0.028 and n=9, both in the body, no CI -> PASS.
    expect("clean abstract subset of body",
           "%%SECTION abstract\nThe gap is +0.028 across n=9 subjects. \\evd{C1}{strong}\n" + body, False)
    # SC-XS-2: abstract carries a full 95% CI -> flag.
    expect("SC-XS-2 CI in abstract",
           "%%SECTION abstract\nThe gap is +0.028 (95\\% CI [+0.018, +0.038]). \\evd{C1}{strong}\n" + body,
           True, "ci-in-abstract")
    # CI written with \pm in the abstract -> flag.
    expect("SC-XS-2 pm-form CI in abstract",
           "%%SECTION abstract\nThe gap is +0.028 \\pm 0.010 across n=9. \\evd{C1}{strong}\n"
           "%%SECTION results\n+0.028 \\pm 0.010, n=9. \\evd{C1}{strong}\n", True, "ci-in-abstract")
    # no abstract section -> nothing to check (a body-only draft) -> PASS.
    expect("no abstract section -> clean", body, False)
    # abstract number IS in the body but reformatted? strict: "0.02" not present verbatim -> flag (documented).
    expect("rounded abstract number flagged (strict, documented)",
           "%%SECTION abstract\nThe gap is +0.02. \\evd{C1}{strong}\n" + body, True, "abstract-body-mismatch")
    # the body MAY carry the full CI (only the abstract may not) -> a body CI alone is clean.
    expect("body CI is fine",
           "%%SECTION abstract\nThe gap is +0.028 across n=9. \\evd{C1}{strong}\n" + body, False)
    # L060 fix (oracle D1): identifiers in the abstract are NOT results -> must NOT flag.
    expect("SC-XS-1-MODELNAME model name not a result",
           "%%SECTION abstract\nWe distill Qwen2.5-0.5B; the gap is +0.028. \\evd{C1}{strong}\n" + body, False)
    expect("SC-XS-1-YEAR citation year not a result",
           "%%SECTION abstract\nUnlike prior work (2024), the gap is +0.028. \\evd{C1}{strong}\n" + body, False)
    expect("SC-XS-1-SIGN leading + normalized vs body",
           "%%SECTION abstract\nThe gap is +0.028. \\evd{C1}{strong}\n" + body, False)
    # C2: a section whose id merely CONTAINS 'abstract' is NOT the abstract (exact match).
    expect("C2 abstract-of-results is not the abstract",
           "%%SECTION abstract-of-results\nThe gap is +0.021. \\evd{C1}{strong}\n" + body, False)

    print("consistency_check selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F19 DET: cross-section number consistency (abstract<->body, CI).")
    sub = ap.add_subparsers(dest="cmd")
    ap.add_argument("--selftest", action="store_true")
    pv = sub.add_parser("validate")
    pv.add_argument("prose", type=Path)
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest()
    if args.cmd == "validate":
        try:
            text = args.prose.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise SystemExit(f"consistency_check: {args.prose}: NOT FOUND")
        return report(check(text))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
