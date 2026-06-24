#!/usr/bin/env python3
r"""claim_binding — the F3 Trust-spine DET check over claim-lattice.json.

Every claim shows its receipt. F3 (a model step in the orchestrator) extracts claims from the
message and binds each to a recorded experiment + strength, writing them into the lattice. THIS
check is the deterministic floor over that binding: it asserts, mechanically, that no claim ships
on a missing, dangling, or stale receipt.

For each claim in the lattice:
  unbound        bound_experiment is null  -> the claim is an IOU; it must be a \gap (flag).
  dangling-cite  bound_experiment does not resolve to docs/experiments/<KEY>*.md (flag).
  unregistered   the experiment is not in evidence-register.json -> status unverifiable (flag);
                 forces the register to be kept current so a new result can't be cited statusless.
  status-mismatch the claim's evidence_status disagrees with the register's truth (flag).
  stale-evidence the cited experiment is `demoted` or `superseded` -> citing it as live support is
                 the D011 over-claim (SC-TRUST-2/3); rebind to the current verdict (flag).

What F3 does NOT do (by design, 2d re-map): judge whether the cited evidence *grounds* this specific
claim (forged-but-live receipt, SC-CITE-1). That is a Toulmin-warrant judgment -> the F4 judge. This
check is existence + status only, and stays pure-DET.

Usage:
    python claim_binding.py validate LATTICE.json [--register REG.json] [--repo-root DIR]
    python claim_binding.py --selftest

Exit code: 0 clean, 1 on any finding (or bad input).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evidence_resolve import find_repo_root, resolve_key

HERE = Path(__file__).resolve().parent
DEFAULT_REGISTER = HERE.parent / "evidence-register.json"
# `suspect` (X1/D050) joins STALE: a result a reader has flagged as doubtful is not citable as live
# support until the handoff resolves it — citing it as live is the same over-claim as citing a demoted one.
STALE = {"demoted", "superseded", "suspect"}


def _raw_register(path: Path = DEFAULT_REGISTER) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"claim_binding: evidence register not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"claim_binding: register invalid JSON: {e}")


def load_register(path: Path) -> dict:
    data = _raw_register(path)
    return data.get("experiments", data)  # tolerate a flat map too


def check(lattice: dict, register: dict, root: Path) -> list[str]:
    f = []
    reg_index = {str(k).upper(): v for k, v in register.items()}  # case-insensitive lookup
    for c in lattice.get("claims", []):
        if not isinstance(c, dict):
            continue
        cid = c.get("claim_id", "?")
        be = c.get("bound_experiment")
        if not be or not str(be).strip():  # None OR empty string -> the claim is a \gap
            f.append(f"[unbound] claim {cid}: no bound_experiment — bind to a recorded result or mark \\gap{{}}")
            continue
        be = str(be).strip()
        resolved = resolve_key(be, root)

        # Learning keys are syntheses, not verdict-bearing experiments: resolve, but no status tracking.
        if be[:1].upper() == "L":
            if not resolved:
                f.append(f"[dangling-cite] claim {cid}: '{be}' does not resolve under docs/")
            continue

        reg = reg_index.get(be.upper())
        reg_status = reg.get("status") if isinstance(reg, dict) else reg
        claim_status = c.get("evidence_status")

        if reg_status in STALE:
            # The binding itself is the problem; this holds whether or not the author mislabeled, and
            # whether or not the key has a file (the register knows it -> suppress dangling here). A
            # superseded key may legitimately be fileless; a fileless `suspect` is instead an anomaly that
            # check_register flags as [register-orphan], not duplicated here as [dangling-cite].
            f.append(f"[stale-evidence] claim {cid}: cites {be} which is '{reg_status}' — a "
                     f"{reg_status} result is not citable as live support; rebind to the current verdict (D011)")
            if claim_status != reg_status:
                f.append(f"[status-mismatch] claim {cid}: lattice evidence_status '{claim_status}' != register '{reg_status}' for {be}")
            continue

        if not resolved:
            f.append(f"[dangling-cite] claim {cid}: '{be}' does not resolve under docs/experiments/")
        if reg is None:
            f.append(f"[unregistered] claim {cid}: '{be}' is not in the evidence register — status unverifiable")
            continue
        if claim_status != reg_status:
            f.append(f"[status-mismatch] claim {cid}: lattice evidence_status '{claim_status}' != register '{reg_status}' for {be}")
    return f


def check_register(register_raw: dict, root: Path) -> list[str]:
    """Reconciler (half): every live/demoted register key must resolve on disk (superseded may be fileless)."""
    f = []
    exp = register_raw.get("experiments", register_raw)
    for key, rec in exp.items():
        status = rec.get("status") if isinstance(rec, dict) else rec
        if status in ("live", "demoted", "suspect") and not resolve_key(key, root):
            f.append(f"[register-orphan] {key} is '{status}' but no record resolves under docs/experiments/")
    return f


def report(findings: list[str]) -> int:
    if findings:
        print(f"\nclaim_binding — {len(findings)} finding(s):")
        for m in findings:
            print(f"  {m}")
        print("\nclaim_binding: FAIL")
        return 1
    print("claim_binding: PASS")
    return 0


# --------------------------------------------------------------------------- selftest
def _selftest() -> int:
    ok = True
    root = find_repo_root(HERE)
    reg = load_register(DEFAULT_REGISTER)

    def claim(cid, be, status, strength="observed"):
        return {"claim_id": cid, "text": "t", "bound_experiment": be, "evidence_status": status,
                "strength": strength, "scope": None, "is_central": False,
                "acknowledgments": [], "section": None, "tags": []}

    def lat(*claims):
        return {"meta": {"stage": 2, "schema_version": "1"}, "message": None, "reader_model": None,
                "claims": list(claims), "warrants": [], "figures": [], "sections": [], "deviation_log": []}

    def expect(name, findings, want_flag, rule=None):
        nonlocal ok
        flagged = len(findings) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in findings)
        good = (flagged == want_flag) and (rule_hit if want_flag else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name
              + ("" if good else f" -> want={want_flag} rule={rule}, got {findings}"))
        ok = ok and good

    def expect_no_rule(name, findings, want_flag, forbid_rule):
        nonlocal ok
        flagged = len(findings) > 0
        forbid_hit = any(f"[{forbid_rule}]" in x for x in findings)
        good = (flagged == want_flag) and not forbid_hit
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name
              + ("" if good else f" -> want={want_flag} forbid={forbid_rule}, got {findings}"))
        ok = ok and good

    # SC-TRUST-1: claim with no experiment -> unbound (\gap).
    expect("SC-TRUST-1 unbound->gap", check(lat(claim("C1", None, "unsupported", "unsupported")), reg, root), True, "unbound")
    # SC-TRUST-2: cites E005 (demoted) -> stale-evidence.
    expect("SC-TRUST-2 E005 demoted", check(lat(claim("C1", "E005", "demoted")), reg, root), True, "stale-evidence")
    # SC-TRUST-3: cites E004 (demoted) -> stale-evidence.
    expect("SC-TRUST-3 E004 demoted", check(lat(claim("C1", "E004", "demoted")), reg, root), True, "stale-evidence")
    # SC-TRUST-11: cites E003 (live) -> no flag.
    expect("SC-TRUST-11 E003 live", check(lat(claim("C1", "E003", "live")), reg, root), False)
    # status-mismatch: claim says live but register says demoted (E005).
    expect("status-mismatch", check(lat(claim("C1", "E005", "live")), reg, root), True, "status-mismatch")
    # dangling: a made-up experiment key.
    expect("dangling-cite", check(lat(claim("C1", "E999", "live")), reg, root), True, "dangling-cite")
    # clean multi-claim: two live claims -> no flag.
    expect("clean live multi", check(lat(claim("C1", "E006", "live", "strong"), claim("C2", "E008", "live")), reg, root), False)

    # --- oracle's new boundary scenarios ---
    # NEW-1: E013b (live, registered, sub-lettered) -> resolves via stem, clean.
    expect("SC-C2-NEW-1 E013b live (no crash)", check(lat(claim("C1", "E013b", "live")), reg, root), False)
    # NEW-2: empty-string bound_experiment -> unbound (not a crash).
    expect("SC-C2-NEW-2 empty-string -> unbound", check(lat(claim("C1", "", "unsupported", "unsupported")), reg, root), True, "unbound")
    # NEW-3: lowercase e005 -> case-insensitive register lookup -> stale.
    expect("SC-C2-NEW-3 lowercase e005 -> stale", check(lat(claim("C1", "e005", "demoted")), reg, root), True, "stale-evidence")
    # NEW-4: L-key (learning) cited as evidence -> resolves, no status flag (decision).
    expect("SC-C2-NEW-4 L016 learning -> no flag", check(lat(claim("C1", "L016", "live")), reg, root), False)
    # NEW-5: realistic mixed draft -> exactly the bad claims flagged, the clean one absent.
    mixed = check(lat(claim("C1", "E006", "live", "strong"),       # clean
                      claim("C2", "E005", "live"),                  # mismatch + stale
                      claim("C3", "E999", "live"),                  # dangling
                      claim("C4", None, "unsupported", "unsupported")), reg, root)  # unbound
    mixed_ok = (any("C2" in x and "stale" in x for x in mixed) and any("C3" in x and "dangling" in x for x in mixed)
                and any("C4" in x and "unbound" in x for x in mixed) and not any("claim C1" in x for x in mixed))
    print(("  ok: " if mixed_ok else "  SELFTEST FAIL: ") + "SC-C2-NEW-5 mixed draft"
          + ("" if mixed_ok else f" -> got {mixed}"))
    ok = ok and mixed_ok
    # NEW-6: E023 (designed, not run, intentionally unregistered) -> unregistered.
    expect("SC-C2-NEW-6 E023 unrun -> unregistered", check(lat(claim("C1", "E023", "live")), reg, root), True, "unregistered")
    # NEW-7 (F3/F4 boundary): E006 live, cited for a claim it does not ground -> F3 MUST NOT flag (grounding is F4).
    expect("SC-C2-NEW-7 grounding is F4 (no flag)", check(lat(claim("C1", "E006", "live")), reg, root), False)
    # NEW-8: honest superseded E007 -> stale fires, status-mismatch MUST NOT, dangling MUST NOT (fileless-but-known).
    s8 = check(lat(claim("C1", "E007", "superseded")), reg, root)
    expect("SC-C2-NEW-8 honest superseded -> stale", s8, True, "stale-evidence")
    expect_no_rule("SC-C2-NEW-8 no false mismatch", s8, True, "status-mismatch")
    expect_no_rule("SC-C2-NEW-8 no false dangling", s8, True, "dangling-cite")

    # register integrity: every live/demoted key resolves on disk (the reconciler half).
    expect("register reconcile (live/demoted resolve)", check_register(_raw_register(), root), False)

    # --- X1 (D050): `suspect` evidence_status (SC-XSTANCE-07) ---
    # a register key marked suspect, cited as live -> stale-evidence (suspect in STALE) + status-mismatch.
    sus_reg = {"E006": {"status": "suspect"}}
    s_sus = check(lat(claim("C1", "E006", "live")), sus_reg, root)
    expect("X1 SC-XSTANCE-07 suspect cited as live -> stale", s_sus, True, "stale-evidence")
    expect("X1 SC-XSTANCE-07 suspect cited as live -> mismatch", s_sus, True, "status-mismatch")
    # a suspect result, even labeled suspect, is STILL not citable as live support (stale fires; no false mismatch).
    s_sus2 = check(lat(claim("C1", "E006", "suspect")), sus_reg, root)
    expect("X1 suspect labeled suspect -> still stale (not citable)", s_sus2, True, "stale-evidence")
    expect_no_rule("X1 suspect labeled suspect -> no false mismatch", s_sus2, True, "status-mismatch")
    # check_register: a recorded suspect key must resolve on disk like live/demoted (E006 resolves -> clean).
    expect("X1 suspect resolves on disk -> clean", check_register({"experiments": {"E006": {"status": "suspect"}}}, root), False)
    # a fileless suspect key -> register-orphan (suspect is recorded, not fileless like superseded).
    expect("X1 fileless suspect -> register-orphan", check_register({"experiments": {"E999X": {"status": "suspect"}}}, root), True, "register-orphan")

    print("claim_binding selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F3 Trust-spine binding check over claim-lattice.json.")
    sub = ap.add_subparsers(dest="cmd")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check-register", action="store_true",
                    help="reconciler: every live/demoted register key must resolve on disk")
    pv = sub.add_parser("validate")
    pv.add_argument("lattice", type=Path)
    pv.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    pv.add_argument("--repo-root", type=Path, default=None)
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.check_register:
        root = find_repo_root(HERE)
        findings = check_register(_raw_register(), root)
        return report(findings) if findings else (print("claim_binding --check-register: PASS") or 0)
    if args.cmd == "validate":
        try:
            lattice = json.loads(args.lattice.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise SystemExit(f"claim_binding: {args.lattice}: NOT FOUND")
        except json.JSONDecodeError as e:
            raise SystemExit(f"claim_binding: {args.lattice}: invalid JSON ({e})")
        root = args.repo_root or find_repo_root(args.lattice)
        return report(check(lattice, load_register(args.register), root))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
