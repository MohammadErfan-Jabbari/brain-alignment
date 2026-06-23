#!/usr/bin/env python3
r"""scope_lint (F5 DET) — the lexical half of the scope/honesty check.

Scope creep has lexical tells that are mechanical to catch: a universal/cross-domain scope-word on what is an
in-domain, single-setting claim ("generalizes", "in general", "across model families", "the full ... curve"),
and a novelty claim with no bound survey citation ("to our knowledge, no prior work ...", uncited). These are
HARD findings (the wording over-reaches regardless of the prose around it). Whether a non-lexical claim's
SCOPE exceeds its EVIDENCE (SC-HON-02/04/05) is a judgment and belongs to the RUB scope judge (sw-scope-judge).

Like ai_tell_lint, a flag is a prompt to look: a flagged scope-word can be the right word ("generalizes to
held-out folds" is within-distribution) — but in this repo, on a single-dataset claim, it is almost always the
tell, and the scope judge adjudicates. The novelty check only fires when the phrase carries no \evd/[E] cite.

Usage:
    python scope_lint.py validate PROSE_FILE
    python scope_lint.py --selftest

Exit code: 0 clean, 1 on any finding (or bad input).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# UNAMBIGUOUS cross-domain scope words only. Deliberately EXCLUDED as dual-use (the C5 lesson — they
# hard-block routine prose, so the RUB scope judge owns them instead): bare "generalize(s)"
# ("generalizes to held-out folds"); "full ... curve" ("the full training curve is in Figure 2"); and
# "any/every model" (inverts on negation: "we do NOT claim this for any model"). One merged across-families
# pattern (no double-fire). "in general" excludes the meta-discourse "in general terms".
SCOPE_WORDS = [
    (r"\bin general\b(?!\s+(terms|agreement))", "in general"),
    (r"\b(generalis[ez]e?[sd]?\s+)?across (all |different )?"
     r"((model|language[- ]?model|architecture|language)\s+)?families\b", "across families"),
    (r"\buniversally\b", "universally"),
    (r"\bfor all (models|architectures|datasets|subjects|participants)\b", "for all ..."),
    (r"\bin all (cases|settings|domains|conditions)\b", "in all ..."),
]
NOVELTY = re.compile(r"\b(to our knowledge|to the best of our knowledge|no prior work|we are the first|"
                     r"the first (\w+ )?to|first work to)\b", re.I)
CITE = re.compile(r"\\evd\{[^}]*\}|\[[ELel]\d+\]")
CODE_FENCE = re.compile(r"^\s*```")
TEX_COMMENT = re.compile(r"^\s*%")


def _prose_lines(text: str, is_tex: bool):
    in_fence = False
    for i, raw in enumerate(text.split("\n"), 1):
        if not is_tex and CODE_FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if is_tex and TEX_COMMENT.match(raw):
            continue
        yield i, raw


def check(text: str, is_tex: bool = True) -> list[str]:
    f = []
    for lineno, line in _prose_lines(text, is_tex):
        low = line.lower()
        for pat, label in SCOPE_WORDS:
            if re.search(pat, low):
                f.append(f"line {lineno}: [scope-word] '{label}' — a universal/cross-domain reach; is the "
                         f"claim's scope actually this broad, or in-domain? (the scope judge adjudicates)")
        if NOVELTY.search(line) and not CITE.search(line):
            f.append(f"line {lineno}: [novelty-unbound] a novelty claim with no bound survey citation — "
                     f"novelty is a claim and needs a \\evd/[E] survey receipt")
    return f


def report(findings: list[str]) -> int:
    if findings:
        print(f"\nscope_lint (F5 DET) — {len(findings)} finding(s):")
        for m in findings:
            print(f"  {m}")
        print("\nscope_lint: FAIL")
        return 1
    print("scope_lint: PASS")
    return 0


def _selftest() -> int:
    ok = True

    def expect(name, text, want_flag, rule=None):
        nonlocal ok
        fnd = check(text, is_tex=True)
        flagged = len(fnd) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in fnd)
        good = (flagged == want_flag) and (rule_hit if want_flag else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name + ("" if good else f" -> got {fnd}"))
        ok = ok and good

    # MUST flag (DET scope-words / novelty)
    expect("SC-HON-01 generalize across families",
           "Brain-alignment scores generalize across language model families.", True, "scope-word")
    expect("SC-HON-03 in general", "In general, higher brain alignment correlates with better performance.", True, "scope-word")
    expect("SC-HON-07 novelty unbound", "To our knowledge, no prior work has used brain alignment as a distillation objective.", True, "novelty-unbound")
    expect("SC-SCOPE-FN-1 for all participants", "The effect held for all participants.", True, "scope-word")
    expect("first-study-to novelty", "This is the first study to use brain alignment as a distillation objective.", True, "novelty-unbound")
    # MUST NOT flag (dual-use / meta-discourse FP guards — the oracle's P2-A findings)
    expect("SC-SCOPE-FP full training curve", "The full training curve is shown in Figure 2.", False)
    expect("SC-SCOPE-FP negated any model", "We do not claim this holds for any model beyond Qwen2.5.", False)
    expect("in general terms (meta-discourse)", "In general terms, we describe the encoding pipeline.", False)
    # SC-HON-08 'full curve' is RUB-owned (the scope judge), not a DET trigger -> scope_lint MUST NOT flag it.
    expect("SC-HON-08 full curve is RUB not DET", "Varying lambda traces the full alignment-quality trade-off curve.", False)
    # de-dup: one phrase -> exactly one finding (was double-firing).
    one = check("Alignment generalises across model families.", is_tex=True)
    dbl_ok = len(one) == 1
    print(("  ok: " if dbl_ok else "  SELFTEST FAIL: ") + "SC-SCOPE-DBL one flag per phrase" + ("" if dbl_ok else f" -> {one}"))
    ok = ok and dbl_ok
    # MUST NOT flag (precision guards)
    expect("SC-HON-09 in-domain scoped",
           "Within the TRIBE dataset, alignment is higher for better-fit layers (R$^2$=0.34, CI[0.28,0.40], n=8 folds, contiguous split).", False)
    expect("SC-HON-10 undemonstrated null",
           "We did not observe a per-individual benefit across five subjects (0-for-5, powered at delta=0.15); a benefit above that threshold is undemonstrated rather than ruled out.", False)
    expect("target register scoped",
           "On UTS03, the trained-untrained gap was +0.028 over reliable voxels.", False)
    # novelty WITH a citation -> not flagged (the receipt is present).
    expect("novelty with citation",
           "To our knowledge, no prior work has used brain alignment as a distillation objective \\evd{L058}.", False)
    # bare "generalizes to held-out folds" is within-distribution and legitimate -> MUST NOT hard-flag
    # (dual-use word; only the cross-domain form is the tell — the C5 tricolon lesson).
    expect("within-dist generalize not flagged", "The probe generalizes to held-out folds.", False)
    # but "generalizes across families" IS the cross-domain tell -> flag.
    expect("generalize-across is the tell", "The probe generalizes across model families.", True, "scope-word")

    print("scope_lint selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F5 DET: lexical scope-word + novelty check over prose.")
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
            raise SystemExit(f"scope_lint: {args.prose}: NOT FOUND")
        return report(check(text, is_tex=args.prose.suffix.lower() == ".tex"))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
