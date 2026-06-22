#!/usr/bin/env python3
r"""claim_fidelity (F9a) — the DET half of claim-fidelity: a sentence's \evd tag may not wear a
bigger badge than its bound claim earned.

F8a emits one \evd{claim-id}{strength} per claim sentence and mirrors it into that claim's
lattice tags[]. F9a is a pure rank comparison on the lattice: for every tag, assert
    RANK[tag.strength] <= RANK[claim.strength]
A tag at or BELOW the claim's earned strength is fine (conservative hedging, SC-TRUST-5 must NOT
flag); a tag ABOVE it is the over-claim (SC-TRUST-4). Pure JSON — no prose parsing.

This is distinct from two siblings:
  - tag-desync (draft_check, C4): the inline \evd and the lattice tags[] disagree. F9a assumes they
    already agree and reads the lattice tags[].
  - F9b (the RUB judge, sw-claim-fidelity-judge): does the prose ASSERTION exceed its own tag (a
    judgment, e.g. "demonstrate"+causal under an "observed" tag). F9a is mechanical; F9b is semantic.
  - F5 (scope judge): does the claim's scope exceed the evidence (claim vs world). Different referent.

Usage:
    python claim_fidelity.py validate LATTICE.json
    python claim_fidelity.py --selftest

Exit code: 0 clean, 1 on any finding (or bad input).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RANK = {"unsupported": 0, "observed": 1, "supported": 2, "strong": 3}


def check(lattice: dict) -> list[str]:
    f = []
    for c in lattice.get("claims", []):
        if not isinstance(c, dict):
            continue
        cid = c.get("claim_id", "?")
        cs = c.get("strength")
        # A present-but-unrankable strength is flagged loud, not skipped silently: a green PASS that
        # hides an unjudgeable badge is the standalone-mode trap. (lattice_integrity is the deeper guard.)
        if cs is not None and cs not in RANK:
            f.append(f"[unrankable] claim {cid}: claim strength '{cs}' not in the ladder — run lattice_integrity")
            continue
        tags = c.get("tags")
        if tags is None:
            tags = []
        elif not isinstance(tags, list):
            f.append(f"[malformed-tags] claim {cid}: tags is not a list — run lattice_integrity")
            tags = []
        for t in tags:
            if not isinstance(t, dict):
                f.append(f"[malformed-tags] claim {cid}: a tag is not an object — run lattice_integrity")
                continue
            ts = t.get("strength")
            if ts is not None and ts not in RANK:
                f.append(f"[unrankable] claim {cid}: \\evd tag strength '{ts}' not in the ladder — run lattice_integrity")
                continue
            if cs in RANK and ts in RANK and RANK[ts] > RANK[cs]:
                f.append(f"[over-tag] claim {cid}: \\evd tag '{ts}' exceeds the bound claim's earned "
                         f"strength '{cs}' — soften the sentence or re-bind the evidence")
    return f


def report(findings: list[str]) -> int:
    if findings:
        print(f"\nclaim_fidelity (F9a) — {len(findings)} finding(s):")
        for m in findings:
            print(f"  {m}")
        print("\nclaim_fidelity: FAIL")
        return 1
    print("claim_fidelity: PASS")
    return 0


# --------------------------------------------------------------------------- selftest
def _selftest() -> int:
    ok = True

    def claim(cid, strength, tag_strengths):
        return {"claim_id": cid, "text": "t", "bound_experiment": "E006", "evidence_status": "live",
                "strength": strength, "scope": None, "is_central": False, "acknowledgments": [],
                "section": "results", "tags": [{"strength": s, "sentence_ref": "s"} for s in tag_strengths]}

    def lat(*claims):
        return {"meta": {"stage": 5, "schema_version": "1"}, "message": "m", "reader_model": None,
                "claims": list(claims), "warrants": [], "figures": [], "sections": [], "deviation_log": []}

    def expect(name, findings, want_flag, rule=None):
        nonlocal ok
        flagged = len(findings) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in findings)
        good = (flagged == want_flag) and (rule_hit if want_flag else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name
              + ("" if good else f" -> want={want_flag} rule={rule}, got {findings}"))
        ok = ok and good

    # SC-TRUST-4: tag 'strong' on an 'observed' claim -> over-tag.
    expect("SC-TRUST-4 strong-tag on observed claim", check(lat(claim("C1", "observed", ["strong"]))), True, "over-tag")
    # SC-TRUST-5: tag 'observed' on a 'strong' claim -> conservative, MUST NOT flag.
    expect("SC-TRUST-5 conservative under-tag", check(lat(claim("C1", "strong", ["observed"]))), False)
    # exact-match tag == claim -> no flag.
    expect("exact match (no flag)", check(lat(claim("C1", "supported", ["supported"]))), False)
    # one-step over (supported tag on observed claim) -> flag.
    expect("one-step over-tag", check(lat(claim("C1", "observed", ["supported"]))), True, "over-tag")
    # multi-tag claim, one tag over -> flag only that.
    multi = check(lat(claim("C1", "observed", ["observed", "strong"])))
    expect("multi-tag one-over", multi, True, "over-tag")
    # clean multi-claim, all tags <= strength -> no flag.
    expect("clean multi-claim", check(lat(claim("C1", "strong", ["strong", "observed"]),
                                          claim("C2", "supported", ["observed"]))), False)
    # unsupported claim with an 'observed' tag -> over-tag (a \gap claim must not be tagged as observed).
    expect("unsupported claim over-tagged", check(lat(claim("C1", "unsupported", ["observed"]))), True, "over-tag")
    # C6-NEW-3: multi-tag at the bottom of the ladder — one exact, one over.
    expect("C6-NEW-3 unsupported claim, observed over-tag", check(lat(claim("C1", "unsupported", ["unsupported", "observed"]))), True, "over-tag")
    # C6-NEW-1: a present-but-unrankable tag strength is flagged loud, not silently skipped.
    expect("C6-NEW-1 unrankable tag enum", check(lat(claim("C1", "observed", ["STRONG"]))), True, "unrankable")
    expect("unrankable claim strength", check(lat(claim("C1", "proven", ["observed"]))), True, "unrankable")
    # C6-NEW-2: tags as a bare dict (serialization bug) -> malformed-tags, not a silent pass.
    bad = lat(claim("C1", "observed", []))
    bad["claims"][0]["tags"] = {"strength": "strong", "sentence_ref": "s"}
    expect("C6-NEW-2 non-list tags", check(bad), True, "malformed-tags")

    print("claim_fidelity selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F9a claim-fidelity (tag <= bound strength) over the lattice.")
    sub = ap.add_subparsers(dest="cmd")
    ap.add_argument("--selftest", action="store_true")
    pv = sub.add_parser("validate")
    pv.add_argument("lattice", type=Path)
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.cmd == "validate":
        try:
            lattice = json.loads(args.lattice.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise SystemExit(f"claim_fidelity: {args.lattice}: NOT FOUND")
        except json.JSONDecodeError as e:
            raise SystemExit(f"claim_fidelity: {args.lattice}: invalid JSON ({e})")
        return report(check(lattice))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
