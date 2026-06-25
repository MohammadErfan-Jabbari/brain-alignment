#!/usr/bin/env python3
r"""rub_harness (G1 / P3) — the RUB-grading harness for the redesigned /write pipeline.

The DET floor (run_checks.py) machine-verifies the ~40 DET scenarios. This harness is its RUB twin:
it grades the ~94 RUB scenarios — the taste/argument/structure/voice/handoff half of the 135-scenario
suite that, before G1, had no scorer. Design + rationale: docs/references/write-redesign-g1-plan.md.

A RUB scenario is graded by running its ONE owning step on the scenario INPUT (as a fixture) and comparing
the result to EXPECT. The graders already exist (the sw-* judges, the F13 panel, the stage-5.5 triage). This
script does NOT call them — it is the DET-testable bookkeeping layer (parse the suite, hold the store, score
recorded results, apply the threshold), exactly as verdicts.py is for stage-5 convergence. The spawning layer
(run the owning step, capture the result) is the SKILL run-protocol (G1-c).

Four grading mechanisms (a scenario's EXPECT is read differently per mechanism):
  verdict-line          the 6 prose judges (F4/F5/F9a/F9b/F10/F11/F12/F18) emit  <TAG>-VERDICT: {ready_to_ship,findings}
                        flag <=> ready_to_ship:false (findings>0); no-flag <=> ready_to_ship:true & findings:0
  panel-synthesis       the F13 panel emits CONCLUSION-STATUS (ternary); flag unless bare SURVIVES & all objections mapped
  lattice-classification the F1 reader-model writes reader_model.{old,new}; the term must be classified OLD vs NEW
  handoff-state         the stage-5.5 triage writes handoffs.json; the expected needs-stance handoff present (or
                        for the over-routing guards: absent AND classified writing-revise), prose not narrowed

THIS CHUNK (G1-a): the suite parser, the rub_scenarios.json store, and `validate-suite` — the DET that parses
scenarios.md LIVE and diffs it against the store so the two never drift. `score` / `sign-off` land in G1-b/G1-c.

Usage:
    python rub_harness.py validate-suite [--scenarios PATH] [--store PATH]   # store <-> live-parsed md agree
    python rub_harness.py gen-store       [--scenarios PATH] [--store PATH]   # (re)generate the store from md
    python rub_harness.py --selftest

Exit code: 0 if the requested check passed, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
# repo-root-relative defaults; resolved from this script's location (scripts/ -> repo root is 4 up).
REPO = HERE.parents[3]
SCENARIOS_MD = REPO / "docs" / "references" / "write-redesign-scenarios.md"
STORE = HERE / "rub_scenarios.json"

# The permanent regression anchors (scenarios.md:8-12). is_anchor => reason-match is BINDING (G1-b, MF-4).
ANCHORS = {"SC-VOICE-01", "SC-VOICE-02", "SC-VOICE-03", "SC-VOICE-04", "SC-XSTANCE-01"}

# functionality code -> the grader that owns its flag decision (the agent / panel / triage step).
_JUDGE = {
    "F1": "sw-reader-model",
    "F2": "sw-scope-judge", "F5": "sw-scope-judge",
    "F3": "sw-argument-judge", "F4": "sw-argument-judge", "F10": "sw-argument-judge",
    "F9a": "sw-claim-fidelity-judge", "F9b": "sw-claim-fidelity-judge",
    "F6": "sw-structure-judge", "F11": "sw-structure-judge", "FLUIDITY": "sw-structure-judge",
    "F8b": "sw-voice-auditor", "F12": "sw-voice-auditor",
    "F18": "sw-acknowledgment",
    "F13": "panel",
    "F20": "triage",
}
# the real on-disk graders a derived `grader` must resolve to (validate-suite asserts this).
_AGENT_DIR = REPO / ".claude" / "agents"


def _split_tags(func: str) -> list[str]:
    """'F12/F5' or 'F4,F10' -> ['F12','F5'] / ['F4','F10'], order preserved."""
    return [t.strip() for t in re.split(r"[,/]", func) if t.strip()]


def derive_mechanism(tags: list[str], expect: str) -> str:
    if "F13" in tags:
        return "panel-synthesis"
    if "F20" in tags:
        return "handoff-state"
    # F1 is lattice-classification ONLY when its EXPECT is a term classification (SC-RM-1/2 "MUST classify
    # OLD/NEW"). An F1-tagged row whose EXPECT is a flag (SC-STR-03 "MUST flag jargon not glossed") is graded by
    # the F11 structure judge reading reader_model, NOT by the reader-model itself, which emits no flag — same
    # as SC-STR-12 (oracle G1-a MF-1). And F1 co-tagged with a prose judge always defers to that judge.
    if tags == ["F1"]:
        return "lattice-classification" if "CLASSIFY" in expect.upper() else "verdict-line"
    return "verdict-line"


def derive_grader(tags: list[str], mechanism: str) -> str:
    if mechanism == "panel-synthesis":
        return "panel"
    if mechanism == "handoff-state":
        return "triage"
    if mechanism == "lattice-classification":
        return "sw-reader-model"
    # verdict-line: the first tag that maps to a prose judge (skip a leading F1 — the prose judge owns the flag).
    for t in tags:
        j = _JUDGE.get(t)
        if j and j not in ("sw-reader-model", "panel", "triage"):
            return j
    # an F1-only verdict-line row (SC-STR-03): a reader-relative old->new failure is owned by the F11 structure
    # judge (it reads reader_model to flag it — sw-reader-model.md:43-45), exactly like SC-STR-12.
    return "sw-structure-judge"


def _expect_class(expect: str) -> str | None:
    """For a lattice-classification row, the expected term classification parsed from EXPECT (SC-RM-1/2)."""
    up = expect.upper()
    if "CLASSIFY" not in up:
        return None
    has_old, has_new = "OLD" in up, "NEW" in up
    if has_old and not has_new:
        return "OLD"
    if has_new and not has_old:
        return "NEW"
    return None  # ambiguous/both — validate-suite flags a lattice row with no clean class


def parse_scenarios_md(path: Path) -> list[dict]:
    """LIVE parse of the suite. Rows live in ``` fenced blocks: ID | F## | TYPE | INPUT | EXPECT | GROUNDED.
    Returns one record per RUB-containing row (TYPE contains 'RUB'), deduped by id (last wins is an error —
    validate-suite flags a dup)."""
    text = path.read_text()
    out: list[dict] = []
    seen: dict[str, int] = {}
    in_block = False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            in_block = not in_block
            continue
        if not in_block or not ln.strip().startswith("SC-"):
            continue
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < 5:
            continue
        sid, func, typ, expect = parts[0], parts[1], parts[2], parts[4]
        if "RUB" not in typ.upper():
            continue
        tags = _split_tags(func)
        mech = derive_mechanism(tags, expect)
        ecls = _expect_class(expect) if mech == "lattice-classification" else None
        rec = {
            "id": sid,
            "functionality": func,
            "type": typ,                       # RUB or RUB+DET / DET+RUB
            "grading_mechanism": mech,
            "grader": derive_grader(tags, mech),
            # flag/noflag is the verdict-line/panel/handoff signal; lattice rows grade on expect_class instead.
            "expect": "classify" if mech == "lattice-classification"
                      else ("noflag" if "MUST NOT" in expect.upper() else "flag"),
            "expect_class": ecls,              # OLD|NEW for lattice rows, else None
            "expect_reason": expect,
            "is_anchor": sid in ANCHORS,
            "_nfields": len(parts),            # parse-integrity (validate-suite asserts ==6); not stored
        }
        seen[sid] = seen.get(sid, 0) + 1
        rec["_dup"] = seen[sid] > 1
        out.append(rec)
    return out


def gen_store(scenarios: Path, store: Path) -> int:
    recs = parse_scenarios_md(scenarios)
    for r in recs:
        r.pop("_dup", None)
        r.pop("_nfields", None)
    store.write_text(json.dumps({"scenarios": recs}, indent=2) + "\n")
    print(f"gen-store: wrote {len(recs)} RUB records -> {store}")
    return 0


def validate_suite(scenarios: Path, store: Path) -> int:
    """The G1-a DET: the store and the LIVE-parsed markdown must agree, and every derived field must be sound."""
    fails: list[str] = []
    live = parse_scenarios_md(scenarios)
    live_ids = [r["id"] for r in live]
    dups = [r["id"] for r in live if r.get("_dup")]
    if dups:
        fails.append(f"[dup-id] duplicate scenario ids in markdown: {sorted(set(dups))}")
    # parse-integrity: a RUB row must be exactly 6 pipe-fields (id|F|TYPE|INPUT|EXPECT|GROUNDED). A literal '|'
    # inside an INPUT shifts EXPECT silently (NH-1) — fail toward flagging it, never silent-misread (L059).
    badf = [(r["id"], r["_nfields"]) for r in live if r.get("_nfields") != 6]
    if badf:
        fails.append(f"[parse-integrity] RUB rows whose field count != 6 (a stray '|'?): {badf}")
    # a lattice-classification row must carry a clean OLD|NEW expectation (MF-2).
    badc = [r["id"] for r in live if r["grading_mechanism"] == "lattice-classification"
            and r.get("expect_class") not in ("OLD", "NEW")]
    if badc:
        fails.append(f"[lattice-noclass] lattice rows with no clean OLD|NEW expect_class: {badc}")

    if not store.exists():
        fails.append(f"[no-store] {store} missing — run `gen-store`")
        return _report(fails, len(live))
    try:
        saved = json.loads(store.read_text())["scenarios"]
    except Exception as e:  # corrupt store fails toward blocking (L059)
        fails.append(f"[bad-store] {store} unreadable: {e}")
        return _report(fails, len(live))

    live_set, saved_set = set(live_ids), {r["id"] for r in saved}
    if live_set != saved_set:
        miss = sorted(live_set - saved_set)
        extra = sorted(saved_set - live_set)
        if miss:
            fails.append(f"[store-missing] RUB rows in md but not the store: {miss}")
        if extra:
            fails.append(f"[store-stale] ids in the store but not (RUB) in md: {extra}")

    # every record's derived fields must be self-consistent with a live re-derivation (catch a hand-edit drift).
    live_by_id = {r["id"]: r for r in live}
    valid_mech = {"verdict-line", "panel-synthesis", "lattice-classification", "handoff-state"}
    for r in saved:
        sid = r["id"]
        if r.get("grading_mechanism") not in valid_mech:
            fails.append(f"[bad-mechanism] {sid}: {r.get('grading_mechanism')!r} not one of {sorted(valid_mech)}")
        if sid in live_by_id:
            # expect_reason is in the tuple: it is the BINDING reason-match text for the 5 anchors (G1-b MF-4),
            # so a stale store reason would silently grade an anchor against drifted text (oracle G1-a MF-3).
            for fld in ("grading_mechanism", "grader", "expect", "expect_class", "expect_reason", "is_anchor"):
                if r.get(fld) != live_by_id[sid].get(fld):
                    fails.append(f"[drift] {sid}.{fld}: store={r.get(fld)!r} != derived={live_by_id[sid].get(fld)!r}")
        # the grader must resolve to a real on-disk owner.
        g = r.get("grader")
        if g not in ("panel", "triage") and not (_AGENT_DIR / f"{g}.md").exists():
            fails.append(f"[no-grader] {sid}: grader {g!r} has no agent file {_AGENT_DIR / (str(g) + '.md')}")

    # the anchors must be present and flagged.
    for a in ANCHORS:
        match = [r for r in saved if r["id"] == a]
        if not match:
            fails.append(f"[anchor-missing] {a} not in the store")
        elif not match[0].get("is_anchor"):
            fails.append(f"[anchor-unflagged] {a} present but is_anchor is false")

    return _report(fails, len(live))


def _report(fails: list[str], n_live: int) -> int:
    if fails:
        print(f"validate-suite: FAIL ({len(fails)} issue(s); {n_live} RUB rows live)")
        for f in fails:
            print(f"    {f}")
        return 1
    print(f"validate-suite: PASS ({n_live} RUB rows; store <-> live markdown agree)")
    return 0


def _selftest() -> int:
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("  ok: " if cond else "  SELFTEST FAIL: ") + name)
        ok = ok and cond

    # 1. derivation rules (the load-bearing logic).
    check("F13 -> panel-synthesis", derive_mechanism(["F13"], "x") == "panel-synthesis")
    check("F20 -> handoff-state", derive_mechanism(["F20"], "x") == "handoff-state")
    check("F1-only + 'MUST classify' -> lattice-classification",
          derive_mechanism(["F1"], "MUST classify OLD") == "lattice-classification")
    check("F1-only + 'MUST flag' -> verdict-line (SC-STR-03, oracle G1-a MF-1)",
          derive_mechanism(["F1"], "MUST flag jargon not glossed") == "verdict-line")
    check("F1,F11 -> verdict-line (SC-STR-12 correction)", derive_mechanism(["F1", "F11"], "MUST flag") == "verdict-line")
    check("F12/F5 -> verdict-line", derive_mechanism(["F12", "F5"], "MUST flag") == "verdict-line")
    check("F1,F11 grader is the F11 judge, NOT reader-model",
          derive_grader(["F1", "F11"], "verdict-line") == "sw-structure-judge")
    check("F1-only verdict-line grader = structure judge (SC-STR-03)",
          derive_grader(["F1"], "verdict-line") == "sw-structure-judge")
    check("F5,F9b grader = scope judge (first prose tag)",
          derive_grader(["F5", "F9b"], "verdict-line") == "sw-scope-judge")
    check("F4,F10 grader = argument judge", derive_grader(["F4", "F10"], "verdict-line") == "sw-argument-judge")
    check("panel grader", derive_grader(["F13"], "panel-synthesis") == "panel")
    check("triage grader", derive_grader(["F20"], "handoff-state") == "triage")
    check("expect_class OLD/NEW parsed", (_expect_class("MUST classify OLD"), _expect_class("MUST classify NEW")) == ("OLD", "NEW"))

    # 2. live parse of the REAL suite is non-trivial and every record well-formed.
    live = parse_scenarios_md(SCENARIOS_MD)
    check(f"live parse finds RUB rows (got {len(live)})", len(live) >= 90)
    check("no duplicate ids in the real suite", not any(r.get("_dup") for r in live))
    valid_mech = {"verdict-line", "panel-synthesis", "lattice-classification", "handoff-state"}
    check("every live record has a valid mechanism", all(r["grading_mechanism"] in valid_mech for r in live))
    check("every verdict-line grader resolves to an agent file",
          all((_AGENT_DIR / f"{r['grader']}.md").exists()
              for r in live if r["grading_mechanism"] in ("verdict-line", "lattice-classification")))
    check("all 5 anchors present & flagged in the live parse",
          {r["id"] for r in live if r["is_anchor"]} >= ANCHORS)
    check("SC-STR-12 is verdict-line/structure (the correction)",
          any(r["id"] == "SC-STR-12" and r["grading_mechanism"] == "verdict-line"
              and r["grader"] == "sw-structure-judge" for r in live))
    check("SC-STR-03 is verdict-line/structure, NOT lattice (oracle G1-a MF-1)",
          any(r["id"] == "SC-STR-03" and r["grading_mechanism"] == "verdict-line"
              and r["grader"] == "sw-structure-judge" for r in live))
    check("the 10 SC-XSTANCE RUB rows are handoff-state",
          sum(1 for r in live if r["id"].startswith("SC-XSTANCE") and r["grading_mechanism"] == "handoff-state") == 10)
    # MF-2: every lattice row's EXPECT is a real OLD/NEW classification, never a flag — the assert that would
    # have gone red on SC-STR-03's misroute.
    lat = [r for r in live if r["grading_mechanism"] == "lattice-classification"]
    check("lattice rows are exactly SC-RM-1/2", {r["id"] for r in lat} == {"SC-RM-1", "SC-RM-2"})
    check("every lattice row has a clean OLD|NEW expect_class, never a flag",
          all(r["expect_class"] in ("OLD", "NEW") and "FLAG" not in r["expect_reason"].upper() for r in lat))

    # 3. validate-suite against a freshly-generated store PASSES; a corrupted store FAILS (fail-safe).
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "store.json"
        gen_store(SCENARIOS_MD, tmp)
        check("validate-suite PASS on a fresh store", validate_suite(SCENARIOS_MD, tmp) == 0)
        # corrupt: drop one row -> store-missing must fire.
        data = json.loads(tmp.read_text())
        dropped = data["scenarios"].pop()
        tmp.write_text(json.dumps(data))
        check("validate-suite FAIL when a row is dropped from the store", validate_suite(SCENARIOS_MD, tmp) == 1)
        # corrupt: flip a mechanism -> drift must fire.
        data["scenarios"].append(dropped)
        data["scenarios"][0]["grading_mechanism"] = "handoff-state"
        tmp.write_text(json.dumps(data))
        check("validate-suite FAIL on a drifted mechanism", validate_suite(SCENARIOS_MD, tmp) == 1)
        # corrupt: unreadable store -> fail toward blocking.
        tmp.write_text("{ not json")
        check("validate-suite FAIL on a corrupt store", validate_suite(SCENARIOS_MD, tmp) == 1)

    print("rub_harness selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="RUB-grading harness for the /write pipeline (G1).")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("validate-suite", "gen-store"):
        p = sub.add_parser(name)
        p.add_argument("--scenarios", type=Path, default=SCENARIOS_MD)
        p.add_argument("--store", type=Path, default=STORE)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest()
    if args.cmd == "validate-suite":
        return validate_suite(args.scenarios, args.store)
    if args.cmd == "gen-store":
        return gen_store(args.scenarios, args.store)
    ap.error("a subcommand or --selftest is required")


if __name__ == "__main__":
    sys.exit(main())
