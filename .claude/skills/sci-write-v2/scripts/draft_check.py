#!/usr/bin/env python3
r"""draft_check — the prose-side DET floor over F8a's output (stage 4).

lattice_integrity sees only the JSON lattice; SC-PROC-3/4 are about the PROSE the drafter writes,
so this check reads the prose file and reconciles it against the lattice. F8a (the drafter) emits,
as it places content:
  - one section marker per skeleton node:   %%SECTION <section_id>   (a line by itself)
  - one inline provenance tag per claim sentence:   \evd{<claim-id>}{<strength>}

This check asserts:
  missing-section   every lattice section has a %%SECTION marker in the prose            (SC-PROC-3)
  empty-prose       every marked section has non-empty prose under it                    (SC-PROC-3)
  unknown-section   a %%SECTION marker names a section not in the lattice
  untagged-claim    every realized claim (one with a section) appears as an \evd tag      (SC-PROC-4)
  unknown-tag       every \evd claim-id resolves to a lattice claim
  bad-strength      every \evd strength is a valid enum
  tag-desync        every inline \evd{cid}{s} is mirrored in that claim's lattice tags[]  (the drafter
                    writes both representations; they must agree, or F9a reads a stale strength)

PARTNER CHECK (do not run standalone and trust a PASS): draft_check is blind to a claim with section=null
(untagged-claim only fires for a placed claim). lattice_integrity validate at stage 4 catches that. F8a runs both.
LaTeX comments are stripped before tag/prose detection (a commented-out \evd is NOT shipped provenance), but
%%SECTION marker lines are preserved; line endings are normalized (CRLF must not false-flag a section).

Usage:
    python draft_check.py validate PROSE_FILE LATTICE.json
    python draft_check.py --selftest

Exit code: 0 clean, 1 on any finding (or bad input).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STRENGTH = {"unsupported", "observed", "supported", "strong"}
SEC_RE = re.compile(r"^%%SECTION[ \t]+(\S+)[ \t]*$", re.M)
SEC_LINE = re.compile(r"%%SECTION[ \t]+\S")
EVD_RE = re.compile(r"\\evd\{([^}]*)\}\{([^}]*)\}")
PCT = re.compile(r"(?<!\\)%")  # an unescaped LaTeX comment start


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_tex_comments(text: str) -> str:
    """Drop LaTeX comments (% to end of line) so a commented-out \\evd is not counted as shipped
    provenance — but preserve %%SECTION marker lines (themselves comments by design)."""
    out = []
    for line in text.split("\n"):
        if SEC_LINE.match(line):
            out.append(line)
            continue
        m = PCT.search(line)
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def parse_sections(prose: str):
    """-> list of (section_id, body) in document order."""
    marks = [(m.group(1), m.start(), m.end()) for m in SEC_RE.finditer(prose)]
    out = []
    for i, (sid, _s, e) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(prose)
        out.append((sid, prose[e:end].strip()))
    return out


def check(prose: str, lattice: dict) -> list[str]:
    f = []
    # normalize line endings, then strip comments (so a commented-out \evd is not real provenance).
    code = strip_tex_comments(normalize(prose))
    claims = [c for c in lattice.get("claims", []) if isinstance(c, dict)]
    claim_by_id = {c.get("claim_id"): c for c in claims}
    section_ids = {s.get("section_id") for s in lattice.get("sections", []) if isinstance(s, dict)}

    sec_blocks = parse_sections(code)
    marked = {sid for sid, _ in sec_blocks}

    # SC-PROC-3: every lattice section realized as a non-empty prose block.
    for sid in section_ids:
        if sid not in marked:
            f.append(f"[missing-section] lattice section '{sid}' has no %%SECTION block in the prose")
    for sid, body in sec_blocks:
        if sid not in section_ids:
            f.append(f"[unknown-section] %%SECTION '{sid}' is not a lattice section")
        # judge emptiness on real words: a section must carry alphanumeric prose, not just tags/punctuation.
        if not re.search(r"[A-Za-z0-9]", EVD_RE.sub("", body)):
            f.append(f"[empty-prose] section '{sid}' has a marker but no prose")

    # parse inline provenance (from the comment-stripped view).
    evd = EVD_RE.findall(code)  # list of (cid, strength)
    tagged = {cid for cid, _ in evd}

    # SC-PROC-4: every realized claim (assigned a section) is tagged in the prose.
    for c in claims:
        cid = c.get("claim_id")
        if c.get("section") and cid not in tagged:
            f.append(f"[untagged-claim] claim {cid} is placed (section '{c.get('section')}') but carries no \\evd tag")

    for cid, strength in evd:
        if cid not in claim_by_id:
            f.append(f"[unknown-tag] \\evd cites claim-id '{cid}' which is not in the lattice")
            continue
        if strength not in STRENGTH:
            f.append(f"[bad-strength] \\evd{{{cid}}} strength '{strength}' not in {sorted(STRENGTH)}")
            continue
        # tag-desync: the inline tag must be mirrored in the lattice tags[] the drafter wrote.
        lat_tags = claim_by_id[cid].get("tags") or []
        if not any(isinstance(t, dict) and t.get("strength") == strength for t in lat_tags):
            f.append(f"[tag-desync] inline \\evd{{{cid}}}{{{strength}}} has no matching entry in the lattice tags[]")
    return f


def report(findings: list[str]) -> int:
    if findings:
        print(f"\ndraft_check — {len(findings)} finding(s):")
        for m in findings:
            print(f"  {m}")
        print("\ndraft_check: FAIL")
        return 1
    print("draft_check: PASS")
    return 0


# --------------------------------------------------------------------------- selftest
def _selftest() -> int:
    ok = True

    def lat():
        def claim(cid, strength, section, tagstrength=None):
            return {"claim_id": cid, "text": "t", "bound_experiment": "E006", "evidence_status": "live",
                    "strength": strength, "scope": None, "is_central": False, "acknowledgments": [],
                    "section": section, "tags": ([{"strength": tagstrength or strength, "sentence_ref": "s"}])}
        return {"meta": {"stage": 4, "schema_version": "1"}, "message": "m", "reader_model": None,
                "claims": [claim("C1", "strong", "results"), claim("C2", "observed", "results")],
                "warrants": [], "figures": [], "sections": [{"section_id": "results", "title": "Results",
                "claim_ids": ["C1", "C2"]}], "deviation_log": []}

    good_prose = ("%%SECTION results\n"
                  "The signal is real beyond confounds. \\evd{C1}{strong}\n"
                  "Plain KD does not preserve alignment. \\evd{C2}{observed}\n")

    def expect(name, findings, want_flag, rule=None):
        nonlocal ok
        flagged = len(findings) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in findings)
        good = (flagged == want_flag) and (rule_hit if want_flag else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name
              + ("" if good else f" -> want={want_flag} rule={rule}, got {findings}"))
        ok = ok and good

    # SC-F8a-OK: clean draft.
    expect("SC-F8a-OK clean", check(good_prose, lat()), False)
    # SC-PROC-4: a claim placed but untagged.
    expect("SC-PROC-4 untagged claim", check("%%SECTION results\nThe signal is real. \\evd{C1}{strong}\nKD claim with no tag.\n", lat()), True, "untagged-claim")
    # SC-PROC-3: a lattice section with no prose block.
    two_sec = lat(); two_sec["sections"].append({"section_id": "intro", "title": "Intro", "claim_ids": ["C1"]})
    expect("SC-PROC-3 missing section", check(good_prose, two_sec), True, "missing-section")
    # empty-prose: marker present, no prose.
    expect("empty-prose", check("%%SECTION results\n\\evd{C1}{strong}\\evd{C2}{observed}\n", lat()), True, "empty-prose")
    # unknown-tag: an \evd cid not in lattice.
    expect("unknown-tag", check(good_prose + "Extra. \\evd{C9}{strong}\n", lat()), True, "unknown-tag")
    # bad-strength: invalid enum.
    expect("bad-strength", check("%%SECTION results\nA. \\evd{C1}{huge}\nB. \\evd{C2}{observed}\n", lat()), True, "bad-strength")
    # unknown-section: a marker for a section not in the lattice.
    expect("unknown-section", check("%%SECTION results\nA. \\evd{C1}{strong}\nB. \\evd{C2}{observed}\n%%SECTION ghost\nx\n", lat()), True, "unknown-section")
    # tag-desync: inline strength differs from the lattice tag the drafter recorded.
    desync = lat(); desync["claims"][0]["tags"] = [{"strength": "observed", "sentence_ref": "s"}]  # lattice says observed
    expect("tag-desync", check(good_prose, desync), True, "tag-desync")  # prose says C1 strong

    # --- oracle's new scenarios (regression + precision) ---
    # SC-F8a-CRLF: a clean draft with CRLF line endings must NOT false-flag (defect A).
    expect("SC-F8a-CRLF clean", check(good_prose.replace("\n", "\r\n"), lat()), False)
    # SC-F8a-COMMENT: C2's only tag is inside a LaTeX comment -> not shipped -> untagged-claim (defect B).
    commented = "%%SECTION results\nThe signal is real. \\evd{C1}{strong}\nKD claim.\n% TODO \\evd{C2}{observed}\n"
    expect("SC-F8a-COMMENT commented tag", check(commented, lat()), True, "untagged-claim")
    # SC-F8a-STRAY: section body is a lone brace after the tags -> empty-prose (defect C).
    expect("SC-F8a-STRAY stray glyph", check("%%SECTION results\n} \\evd{C1}{strong}\\evd{C2}{observed}\n", lat()), True, "empty-prose")
    # SC-F8a-TERSE: minimal real prose must NOT flag (brevity != empty).
    expect("SC-F8a-TERSE terse real", check("%%SECTION results\nDepth helps. \\evd{C1}{strong}\nKD hurts. \\evd{C2}{observed}\n", lat()), False)
    # SC-F8a-DUPTAG: a second conflicting inline tag for C1 not in the lattice -> tag-desync.
    dup = "%%SECTION results\nA. \\evd{C1}{strong}\nB. \\evd{C2}{observed}\nC. \\evd{C1}{observed}\n"
    expect("SC-F8a-DUPTAG conflicting inline", check(dup, lat()), True, "tag-desync")
    # SC-F8a-MULTI: 3 sections written out of lattice order, all marked + tagged -> no flag (set-based coverage).
    m3 = lat()
    m3["sections"] = [{"section_id": "methods", "title": "M", "claim_ids": ["C1"]},
                      {"section_id": "results", "title": "R", "claim_ids": ["C2"]}]
    m3["claims"][0]["section"] = "methods"; m3["claims"][1]["section"] = "results"
    out_of_order = ("%%SECTION results\nKD result. \\evd{C2}{observed}\n"
                    "%%SECTION methods\nWe probe depth. \\evd{C1}{strong}\n")
    expect("SC-F8a-MULTI out-of-order", check(out_of_order, m3), False)
    # escaped percent must survive (a real "50\% gain" line is not a comment).
    expect("escaped-percent survives", check("%%SECTION results\n50\\% gain seen. \\evd{C1}{strong}\nKD. \\evd{C2}{observed}\n", lat()), False)

    print("draft_check selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F8a prose-side DET check (prose <-> lattice).")
    sub = ap.add_subparsers(dest="cmd")
    ap.add_argument("--selftest", action="store_true")
    pv = sub.add_parser("validate")
    pv.add_argument("prose", type=Path)
    pv.add_argument("lattice", type=Path)
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.cmd == "validate":
        try:
            prose = args.prose.read_text(encoding="utf-8")
            lattice = json.loads(args.lattice.read_text(encoding="utf-8"))
        except FileNotFoundError as e:
            raise SystemExit(f"draft_check: {e}")
        except json.JSONDecodeError as e:
            raise SystemExit(f"draft_check: {args.lattice}: invalid JSON ({e})")
        return report(check(prose, lattice))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
