#!/usr/bin/env python3
r"""warrant_schema (F4 DET) — the one mechanical half of the argument-validity check.

An argument is claim <- grounds <- WARRANT (Toulmin): the warrant is the stated license from the `from`
claim to the `to` claim. The only thing that is DET about it is PRESENCE: a warrant edge with an empty (or
whitespace-only / missing) warrant string is a silent inferential jump — flag it (SC-ARG-1). Whether a
NON-empty warrant is actually VALID (circular, correlation-as-causation, restates the claim — SC-ARG-6/8/11)
is a judgment and belongs to the RUB argument judge (sw-argument-judge), not here.

(Referential integrity — from/to resolve to real claims — is lattice_integrity's job, not this.)

Usage:
    python warrant_schema.py validate LATTICE.json
    python warrant_schema.py --selftest

Exit code: 0 clean, 1 on any empty-warrant edge (or bad input).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def check(lattice: dict) -> list[str]:
    f = []
    for w in lattice.get("warrants", []):
        if not isinstance(w, dict):
            continue  # malformed-shape is lattice_integrity's report (rule 6); don't double-flag
        if not str(w.get("warrant") or "").strip():
            f.append(f"[empty-warrant] edge {w.get('from')}->{w.get('to')}: no stated warrant "
                     f"(a silent jump from one claim to the next; state the inferential license)")
    return f


def report(findings: list[str]) -> int:
    if findings:
        print(f"\nwarrant_schema (F4 DET) — {len(findings)} finding(s):")
        for m in findings:
            print(f"  {m}")
        print("\nwarrant_schema: FAIL")
        return 1
    print("warrant_schema: PASS")
    return 0


def _selftest() -> int:
    ok = True

    def lat(*warrants):
        return {"meta": {"stage": 2, "schema_version": "1"}, "message": "m", "reader_model": None,
                "claims": [], "warrants": list(warrants), "figures": [], "sections": [], "deviation_log": []}

    def expect(name, findings, want_flag, rule=None):
        nonlocal ok
        flagged = len(findings) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in findings)
        good = (flagged == want_flag) and (rule_hit if want_flag else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name + ("" if good else f" -> got {findings}"))
        ok = ok and good

    # SC-ARG-1: the thesis's primary inference with an empty warrant -> flag.
    expect("SC-ARG-1 empty warrant", check(lat(
        {"from": "C-map-exists", "to": "C-usable-signal", "warrant": ""})), True, "empty-warrant")
    # whitespace-only warrant -> flag.
    expect("whitespace warrant", check(lat({"from": "C1", "to": "C2", "warrant": "   "})), True, "empty-warrant")
    # SC-F4-OK: a real, non-circular warrant with a stated mechanism -> MUST NOT flag (validity is the RUB judge's call).
    expect("SC-F4-OK valid warrant", check(lat(
        {"from": "C-differentiable", "to": "C-trainable",
         "warrant": "a differentiable signal can be optimized by gradient descent"})), False)
    # SC-ARG-8: a CIRCULAR but non-empty warrant -> MUST NOT flag HERE (it is RUB, owned by sw-argument-judge).
    expect("SC-ARG-8 circular non-empty (RUB, not DET)", check(lat(
        {"from": "C-kd-degrades", "to": "C-loss-recovers",
         "warrant": "degrades, so adding supervision restores it"})), False)
    # no warrants -> clean.
    expect("no warrants", check(lat()), False)

    print("warrant_schema selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F4 DET: empty-warrant check over the lattice.")
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
            raise SystemExit(f"warrant_schema: {args.lattice}: NOT FOUND")
        except json.JSONDecodeError as e:
            raise SystemExit(f"warrant_schema: {args.lattice}: invalid JSON ({e})")
        return report(check(lattice))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
