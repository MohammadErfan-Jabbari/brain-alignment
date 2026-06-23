#!/usr/bin/env python3
"""lattice_integrity — the rigid DET floor over claim-lattice.json (F15).

The /write spine is a single shared object (the claim-lattice) passed stage to stage.
This check is the thing an agent cannot argue with: it asserts the lattice is well-formed,
referentially consistent, and that no stage silently drops or empties what an earlier stage
wrote. A floor an agent can walk around is not a floor, so the checks below are deliberately
strict about the silent-corruption paths (id collision, content gutting, dangling edges,
coverage being switched off by a malformed stage field).

Two modes:

  validate <lattice.json>
      Single-snapshot rules, stage-aware via meta.stage:
        schema            top-level + per-claim required keys; enums; unique claim_id;
                          schema_version; stage type+range; tag-object shape; is_central bool  (always)
        orphan-claim      every claim.section is set and names a real section                  (stage >= 3)
        empty-section     every section has >=1 existing claim                                 (stage >= 3)
        node->section     claim<->section map agrees BOTH directions; no dangling member       (stage >= 3)
        central-figure    every is_central claim has >=1 figure referencing it                  (stage >= 3)
        warrant-ref       every warrant from/to resolves to an existing claim                   (always)
        figure-ref        every figure.claim_id resolves to an existing claim                   (always)
        every-claim-tagged every claim has >=1 well-formed \\evd tag                            (stage >= 4)

  diff <before.json> <after.json>
        round-trip /      no claim dropped; no key dropped from a claim; no field that HAD
        append-safe       content in `before` is emptied in `after` (incl. a list whose members
                          are gutted to empty strings). Values may change; they may not be cleared
                          by a later stage. Then validate(after) is composed in, so a single diff
                          call is self-sufficient (an after-only malformed claim is still caught).

`bound_experiment` and `section` may be legitimately re-nulled (a \\gap; a re-skeleton), so they are
exempt from the content-emptying check — but the KEY must still survive. `scope` is provenance and is
NOT exempt: once set, clearing it is the mechanical half of an SC-TRUST-10 scope-loss.

Empty-warrant (F4) and lexical scope-words (F5) are SEPARATE hooks, not part of this floor.

Usage:
    python lattice_integrity.py validate LATTICE.json
    python lattice_integrity.py diff BEFORE.json AFTER.json
    python lattice_integrity.py --selftest

Exit code: 0 clean, 1 on any finding (or bad input).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EVIDENCE_STATUS = {"live", "demoted", "superseded"}
STRENGTH = {"unsupported", "observed", "supported", "strong"}
FRAME = {"basic-science", "technology"}        # F2: the evaluation frame (name which game you are playing)
READER_MODEL_KEYS = {"venue", "old", "new", "prior_beliefs", "doubts"}  # F1: who the reader is
SCHEMA_VERSION = "1"
TOP_KEYS = {"meta", "claims", "warrants", "figures", "sections", "deviation_log"}
CLAIM_KEYS = {
    "claim_id", "text", "bound_experiment", "evidence_status", "strength",
    "scope", "is_central", "acknowledgments", "section", "tags",
}
# Fields a later stage may legitimately re-null (key must still survive): a \gap re-nulls
# bound_experiment; a re-skeleton re-nulls section. `scope` is deliberately NOT here.
APPEND_SAFE_NULLABLE = {"bound_experiment", "section"}


def _empty(v) -> bool:
    return v is None or v == "" or v == [] or v == {}


def _has_content(v) -> bool:
    """True if v carries real information (recursing into lists/dicts; '' and whitespace do not)."""
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, tuple)):
        return any(_has_content(x) for x in v)
    if isinstance(v, dict):
        return any(_has_content(x) for x in v.values())
    return True  # numbers, True/False are real values


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"lattice_integrity: {path}: NOT FOUND")
    except json.JSONDecodeError as e:
        raise SystemExit(f"lattice_integrity: {path}: invalid JSON ({e})")


def validate(lattice: dict) -> list[str]:
    f = []  # findings

    # --- schema: top level ---
    missing_top = TOP_KEYS - set(lattice)
    if missing_top:
        f.append(f"[schema] top-level keys missing: {sorted(missing_top)}")
    meta = lattice.get("meta") or {}
    if meta.get("schema_version") != SCHEMA_VERSION:
        f.append(f"[schema] meta.schema_version '{meta.get('schema_version')}' != '{SCHEMA_VERSION}'")

    # stage: coerce a digit-string, flag wrong type, NEVER silently disable coverage.
    raw = meta.get("stage")
    stage = None
    if isinstance(raw, bool):
        f.append("[schema] meta.stage is a bool, not an int")
    elif isinstance(raw, int):
        stage = raw
    elif isinstance(raw, str) and raw.strip().lstrip("-").isdigit():
        stage = int(raw)
        f.append("[schema] meta.stage is a string; should be an int")
    else:
        f.append("[schema] meta.stage missing or not an int")
    if stage is not None and not (1 <= stage <= 6):
        f.append(f"[schema] meta.stage {stage} out of range 1-6")
    cov_stage = stage if isinstance(stage, int) else 6  # fail-safe: run ALL coverage, never skip silently

    claims = lattice.get("claims")
    if not isinstance(claims, list):
        f.append("[schema] `claims` missing or not a list")
        return f
    sections = lattice.get("sections") or []
    figures = lattice.get("figures") or []
    warrants = lattice.get("warrants") or []
    section_ids = {s.get("section_id") for s in sections if isinstance(s, dict)}
    sec_members = {s.get("section_id"): (s.get("claim_ids") or [])
                   for s in sections if isinstance(s, dict)}
    claim_ids = [c.get("claim_id") for c in claims if isinstance(c, dict)]
    claim_id_set = set(claim_ids)

    # duplicate claim_id (uniqueness is the identity the whole diff relies on)
    for cid in {x for x in claim_ids if claim_ids.count(x) > 1 and x is not None}:
        f.append(f"[schema] duplicate claim_id '{cid}'")
    # duplicate section_id (F6 owns the sections[] namespace; a collision silently misattributes coverage)
    sec_id_list = [s.get("section_id") for s in sections if isinstance(s, dict)]
    for sid in {x for x in sec_id_list if sec_id_list.count(x) > 1 and x is not None}:
        f.append(f"[schema] duplicate section_id '{sid}'")

    # --- schema: per claim ---
    for i, c in enumerate(claims):
        if not isinstance(c, dict):
            f.append(f"[schema] claim #{i} is not an object")
            continue
        cid = c.get("claim_id", f"#{i}")
        missing = CLAIM_KEYS - set(c)
        if missing:
            f.append(f"[schema] claim {cid}: missing keys {sorted(missing)}")
        if "evidence_status" in c and c["evidence_status"] not in EVIDENCE_STATUS:
            f.append(f"[schema] claim {cid}: evidence_status '{c['evidence_status']}' not in {sorted(EVIDENCE_STATUS)}")
        if "strength" in c and c["strength"] not in STRENGTH:
            f.append(f"[schema] claim {cid}: strength '{c['strength']}' not in {sorted(STRENGTH)}")
        if "is_central" in c and not isinstance(c["is_central"], bool):
            f.append(f"[schema] claim {cid}: is_central must be a bool, got {c['is_central']!r}")

    # --- referential integrity (always; edges must not dangle) ---
    for w in warrants:
        if not isinstance(w, dict):
            f.append("[warrant-ref] a warrant is not an object")
            continue
        for end in ("from", "to"):
            if w.get(end) not in claim_id_set:
                f.append(f"[warrant-ref] warrant {end}='{w.get(end)}' does not resolve to a claim")
    for fig in figures:
        if not isinstance(fig, dict):
            f.append("[figure-ref] a figure is not an object")
            continue
        if fig.get("claim_id") not in claim_id_set:
            f.append(f"[figure-ref] figure '{fig.get('figure_id')}' claim_id='{fig.get('claim_id')}' does not resolve")

    # --- coverage rules (stage-gated) ---
    if cov_stage >= 3:
        # a stage-3+ lattice with nothing to structure is malformed, not merely low-quality.
        # NOTE (L060): "message is ONE sentence" (Mensh-Kording) is a stylistic norm, not a ground-truth
        # invariant, and a sentence-counter false-positives on "Sec.", "U.S.", ellipses. It is NOT a DET check
        # — the human gates the one-sentence message at F16. The floor only asserts the message EXISTS.
        if _empty(lattice.get("message")):
            f.append("[schema] message is empty at stage >= 3 (nothing to structure around)")
        # F2 stage-1 outputs, required by the gate (the stage-3 coupled package):
        frame = lattice.get("frame")
        if _empty(frame):
            f.append("[schema] frame is empty at stage >= 3 (F2: declare basic-science | technology)")
        elif frame not in FRAME:
            f.append(f"[schema] frame '{frame}' not in {sorted(FRAME)}")
        if _empty(lattice.get("contribution_type")):
            f.append("[schema] contribution_type is empty at stage >= 3 (F2: name the contribution)")
        # F1 reader-model, required by the gate (old-vs-new is meaningless without a named reader):
        rm = lattice.get("reader_model")
        if _empty(rm):
            f.append("[schema] reader_model is empty at stage >= 3 (F1: who is the reader)")
        elif not isinstance(rm, dict):
            f.append("[schema] reader_model is not an object")
        else:
            rm_missing = READER_MODEL_KEYS - set(rm)
            if rm_missing:
                f.append(f"[schema] reader_model: missing keys {sorted(rm_missing)} (F1 needs {sorted(READER_MODEL_KEYS)})")
            if "venue" in rm and _empty(rm.get("venue")):
                f.append("[schema] reader_model.venue is empty (old/new is reader-relative — name the reader)")
            for k in ("old", "new", "prior_beliefs", "doubts"):
                if k in rm and not isinstance(rm.get(k), list):
                    f.append(f"[schema] reader_model.{k} must be a list")
        if not claims:
            f.append("[empty-skeleton] stage >= 3 with no claims")
        if not sections:
            f.append("[empty-skeleton] stage >= 3 with no sections")
        for c in claims:
            if not isinstance(c, dict):
                continue
            cid = c.get("claim_id")
            sec = c.get("section")
            if _empty(sec):
                f.append(f"[orphan-claim] claim {cid}: not assigned to any section")
            elif sec not in section_ids:
                f.append(f"[node->section] claim {cid}: section '{sec}' not in `sections`")
            elif cid not in sec_members.get(sec, []):
                f.append(f"[node->section] claim {cid}: names section '{sec}' but that section omits it")
            # by drafting (stage >= 4) a central claim must carry a figure; dormant at stage 3 (pre-F7).
            if c.get("is_central") and cov_stage >= 4:
                if not any(isinstance(fig, dict) and fig.get("claim_id") == cid for fig in figures):
                    f.append(f"[central-figure] central claim {cid}: no figure references it")
        for s in sections:
            if not isinstance(s, dict):
                f.append("[schema] a section is not an object")
                continue
            sid = s.get("section_id")
            members = s.get("claim_ids") or []
            for m in members:
                if m not in claim_id_set:
                    f.append(f"[node->section] section '{sid}': claim_id '{m}' does not resolve")
            if not [m for m in members if m in claim_id_set]:
                f.append(f"[empty-section] section '{sid}': no existing claim bound to it")

    if cov_stage >= 4:
        for c in claims:
            if not isinstance(c, dict):
                continue
            cid = c.get("claim_id")
            tags = c.get("tags") or []
            if not tags:
                f.append(f"[every-claim-tagged] claim {cid}: no \\evd tags (untagged claim sentence)")
                continue
            for t in tags:
                if not isinstance(t, dict) or t.get("strength") not in STRENGTH or _empty(t.get("sentence_ref")):
                    f.append(f"[every-claim-tagged] claim {cid}: malformed \\evd tag {t!r} (need strength enum + sentence_ref)")

    return f


def diff(before: dict, after: dict) -> list[str]:
    f = []
    # Top-level content-bearing provenance fields. message/frame/contribution_type/reader_model are part of the
    # gated package; a later stage write (incl. a stage REGRESSION that skips the stage>=3 validate block) must
    # not silently empty them. validate(after) alone misses this when after is staged < 3, so guard it here.
    for k in ("message", "frame", "contribution_type", "reader_model"):
        if _has_content(before.get(k)) and not _has_content(after.get(k)):
            f.append(f"[append-safe] top-level '{k}' had content and is now empty (destructive overwrite)")
    # reader_model is a dict of provenance sub-fields (old/new term classifications, beliefs, doubts) the
    # drafter F8a and the structure judge F11 depend on; guard each sub-field, like the per-claim key check.
    b_rm, a_rm = before.get("reader_model"), after.get("reader_model")
    if isinstance(b_rm, dict) and isinstance(a_rm, dict):
        for k, bv in b_rm.items():
            if _has_content(bv) and not _has_content(a_rm.get(k)):
                f.append(f"[append-safe] reader_model.{k} had content and is now empty (destructive overwrite)")

    b_claims = {c.get("claim_id"): c for c in before.get("claims", []) if isinstance(c, dict)}
    a_claims = {c.get("claim_id"): c for c in after.get("claims", []) if isinstance(c, dict)}

    for cid, bc in b_claims.items():
        ac = a_claims.get(cid)
        if ac is None:
            f.append(f"[round-trip] claim {cid}: dropped between writes")
            continue
        for k, bv in bc.items():
            if k not in ac:
                f.append(f"[round-trip] claim {cid}: key '{k}' dropped between writes")
                continue
            if _has_content(bv) and not _has_content(ac[k]) and k not in APPEND_SAFE_NULLABLE:
                f.append(f"[append-safe] claim {cid}: field '{k}' had content and is now empty (destructive overwrite)")

    # compose validate(after) so a single diff call is self-sufficient (after-only malformed claims caught)
    f += validate(after)
    return f


def report(findings: list[str], label: str) -> int:
    if findings:
        print(f"\nlattice_integrity ({label}) — {len(findings)} finding(s):")
        for msg in findings:
            print(f"  {msg}")
        print("\nlattice_integrity: FAIL")
        return 1
    print(f"lattice_integrity ({label}): PASS")
    return 0


# --------------------------------------------------------------------------- selftest
def _selftest() -> int:
    ok = True

    def expect(name, findings, want_flag, rule=None):
        nonlocal ok
        flagged = len(findings) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in findings)
        good = (flagged == want_flag) and (rule_hit if want_flag else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name
              + ("" if good else f" -> want_flag={want_flag} rule={rule}, got {findings}"))
        ok = ok and good

    here = Path(__file__).resolve().parent
    good = json.loads((here.parent / "schema" / "claim-lattice.example.json").read_text())
    clone = lambda: json.loads(json.dumps(good))

    # happy paths
    expect("SC-F15-OK validate", validate(good), False)
    expect("SC-F15-OK round-trip", diff(good, clone()), False)

    # original scenarios
    d = clone(); del d["claims"][0]["bound_experiment"]
    expect("SC-TRUST-9 validate", validate(d), True, "schema")
    expect("SC-TRUST-9 diff", diff(good, d), True, "round-trip")
    d = clone(); del d["claims"][1]["strength"]
    expect("SC-PROC-6", validate(d), True, "schema")
    d = clone(); d["claims"][0]["acknowledgments"] = []
    expect("SC-PROC-7", diff(good, d), True, "append-safe")
    d = clone(); d["claims"][0]["evidence_status"] = "current"
    expect("bad evidence_status enum", validate(d), True, "schema")
    d = clone(); d["claims"][0]["section"] = None
    expect("orphan-claim", validate(d), True, "orphan-claim")
    d = clone(); d["claims"][0]["tags"] = []
    expect("every-claim-tagged", validate(d), True, "every-claim-tagged")
    d = clone(); d["figures"] = []
    expect("central-figure (stage4, no fig)", validate(d), True, "central-figure")
    # SC-STR-05: a section with no bound claim -> empty-section.
    d = clone(); d["sections"].append({"section_id": "related", "title": "Related Work", "claim_ids": ["C1"]})
    # 'related' lists C1 but C1.section='results' -> node->section reverse mismatch is expected here too;
    # use a truly empty section instead to isolate empty-section:
    d = clone(); d["sections"].append({"section_id": "related", "title": "Related Work", "claim_ids": []})
    expect("SC-STR-05 empty-section", validate(d), True, "empty-section")
    # SC-STR-13: stage 3, is_central claim, no figures -> central-figure DORMANT (pre-drafting). No-flag.
    d = clone(); d["meta"]["stage"] = 3; d["figures"] = []
    expect("SC-STR-13 central-figure dormant at stage3", validate(d), False)
    # SC-STR-14: stage 4 (drafting), is_central claim, no figures -> MUST flag central-figure (can't die silently).
    d = clone(); d["meta"]["stage"] = 4; d["figures"] = []
    expect("SC-STR-14 central-figure live at stage4", validate(d), True, "central-figure")
    # SC-STR-15: duplicate section_id -> schema (the F6 namespace guard).
    d = clone(); d["sections"].append({"section_id": "results", "title": "dup", "claim_ids": ["C1"]})
    expect("SC-STR-15 duplicate section_id", validate(d), True, "schema")
    # SC-STR-16: message null at stage >= 3 -> schema (F6 step-1 backstop).
    d = clone(); d["message"] = None
    expect("SC-STR-16 null message at stage>=3", validate(d), True, "schema")
    # SC-STR-17: empty skeleton at stage 3 -> empty-skeleton (malformed, not merely low-quality).
    d = clone(); d["meta"]["stage"] = 3; d["claims"] = []; d["sections"] = []; d["figures"] = []; d["warrants"] = []
    expect("SC-STR-17 empty skeleton", validate(d), True, "empty-skeleton")

    # oracle's new boundary scenarios
    d = clone(); d["sections"][0]["claim_ids"] = ["C1"]  # omits C2 which still says section=results
    expect("SC-F15-NODE-REV", validate(d), True, "node->section")
    d = clone(); d["sections"][0]["claim_ids"] = ["C1", "C2", "CZZ"]
    expect("SC-F15-SEC-DANGLE", validate(d), True, "node->section")
    d = clone(); d["warrants"][0]["to"] = "C99"
    expect("SC-F15-WARR-DANGLE", validate(d), True, "warrant-ref")
    d = clone(); d["figures"][0]["claim_id"] = "C99"; d["claims"][0]["is_central"] = False
    expect("SC-F15-FIG-DANGLE", validate(d), True, "figure-ref")
    d = clone(); d["claims"].append(clone()["claims"][0])  # second C1
    expect("SC-F15-DUPID", validate(d), True, "schema")
    d = clone(); d["claims"][0]["acknowledgments"] = [""]
    expect("SC-F15-ACK-GUT", diff(good, d), True, "append-safe")
    d = clone(); d["claims"][0]["scope"] = None
    expect("SC-F15-SCOPE-CLEAR", diff(good, d), True, "append-safe")
    d = clone(); d["meta"]["stage"] = "4"; d["claims"][0]["section"] = None  # string stage + an orphan
    fnd = validate(d)
    expect("SC-F15-STAGE-STR schema-flag", fnd, True, "schema")
    expect("SC-F15-STAGE-STR coverage-still-on", fnd, True, "orphan-claim")
    d = clone(); d["meta"]["stage"] = 7
    expect("SC-F15-STAGE-RANGE", validate(d), True, "schema")
    d = clone(); d["claims"][0]["tags"] = [{"foo": 1}]
    expect("SC-F15-TAG-MALFORMED", validate(d), True, "every-claim-tagged")
    bad_after = clone(); bad_after["claims"].append({"claim_id": "C9", "text": "x"})  # after-only, missing keys
    expect("SC-F15-AFTERONLY-BAD", diff(good, bad_after), True, "schema")

    # --- F1/F2 stage-1 front-end (P2-B-i) ---
    d = clone(); del d["frame"]
    expect("F2 frame missing at stage>=3", validate(d), True, "schema")
    d = clone(); d["frame"] = "deployment"
    expect("F2 frame bad enum", validate(d), True, "schema")
    d = clone(); del d["contribution_type"]
    expect("F2 contribution_type missing", validate(d), True, "schema")
    d = clone(); del d["reader_model"]["doubts"]
    expect("F1 reader_model missing a key", validate(d), True, "schema")
    d = clone(); d["reader_model"] = "ML reader"
    expect("F1 reader_model not an object", validate(d), True, "schema")
    d = clone(); d["reader_model"]["old"] = "linear probe"
    expect("F1 reader_model.old not a list", validate(d), True, "schema")
    d = clone(); d["reader_model"]["venue"] = ""
    expect("F1 reader_model.venue empty", validate(d), True, "schema")
    # F1/F2 outputs are NOT required before the gate (stage 2): absence is fine, not a flag.
    d = clone(); d["meta"]["stage"] = 2; del d["frame"]; del d["contribution_type"]; del d["reader_model"]
    expect("F1/F2 absent at stage 2 is fine (no-flag)", validate(d), False)
    # message-one-sentence (F2) is NOT a DET check (L060: stylistic norm, FP-prone; gated by the human at F16).
    # A multi-sentence message must NOT be flagged by the floor:
    d = clone(); d["message"] = "We show the signal is real. We then show it is not a lever."
    expect("F2 multi-sentence message is NOT a floor flag (gate-owned)", validate(d), False)
    # SC-RM-1/2 (ICLR reader: "linear probe"=OLD, "voxelwise noise ceiling"=NEW) are RUB — verified against the
    # sw-reader-model agent, not in this DET selftest (old-vs-new is a judgment, not a schema check).

    # D2 (oracle): the new content-bearing top-level fields are diff-protected, incl. across a stage regression
    # (the path that skips the stage>=3 validate block) — F15's append-safe guarantee must cover them too.
    a = clone()
    for k in ("old", "new", "prior_beliefs", "doubts"):
        a["reader_model"][k] = []
    expect("D2 reader_model fully gutted -> append-safe", diff(good, a), True, "append-safe")
    a = clone(); a["meta"]["stage"] = 2; a["message"] = ""
    expect("D2 stage-regression empties message -> append-safe", diff(good, a), True, "append-safe")
    a = clone(); a["meta"]["stage"] = 2; a["frame"] = None
    expect("D2 stage-regression nulls frame -> append-safe", diff(good, a), True, "append-safe")
    a = clone(); a["message"] = "A different but still legitimate single-sentence message."
    expect("D2 message legitimately changed (no-flag)", diff(good, a), False)

    # precision guards (MUST NOT flag)
    s2 = clone()
    s2["meta"]["stage"] = 2
    for c in s2["claims"]:
        c["section"] = None; c["tags"] = []; c["acknowledgments"] = []
    s2["sections"] = []; s2["figures"] = []; s2["warrants"] = []
    expect("SC-F15-CLEAN-S2 (no-flag)", validate(s2), False)
    b = clone(); b["claims"][0]["scope"] = "n=9"
    a = clone(); a["claims"][0]["scope"] = "n=9, UTS03"
    expect("SC-F15-RESCOPE-OK (no-flag)", diff(b, a), False)
    # is_central:null decision = flag
    d = clone(); d["meta"]["stage"] = 3; d["claims"][0]["is_central"] = None
    expect("SC-F15-CENTRAL-NULL", validate(d), True, "schema")

    print("lattice_integrity selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="DET integrity floor over claim-lattice.json (F15).")
    sub = ap.add_subparsers(dest="cmd")
    ap.add_argument("--selftest", action="store_true", help="run embedded scenario asserts")
    p_val = sub.add_parser("validate")
    p_val.add_argument("lattice", type=Path)
    p_diff = sub.add_parser("diff")
    p_diff.add_argument("before", type=Path)
    p_diff.add_argument("after", type=Path)
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.cmd == "validate":
        return report(validate(load(args.lattice)), f"validate {args.lattice.name}")
    if args.cmd == "diff":
        return report(diff(load(args.before), load(args.after)), f"diff {args.before.name}->{args.after.name}")
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
