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


def _derive_expect(expect_text: str, mechanism: str) -> str:
    """flag / noflag / classify. noflag = a near-miss ('MUST NOT flag') OR an over-routing GUARD — the handoff
    guards SC-XSTANCE-08/16 phrase it as 'classify writing-revise, NOT a handoff' / 'NOT needs-stance', with no
    literal 'MUST NOT' (oracle G1-c MF-1: testing only 'MUST NOT' inverted these two and rewarded the regression)."""
    if mechanism == "lattice-classification":
        return "classify"
    up = expect_text.upper()
    if "MUST NOT" in up or re.search(r"NOT\s+(?:A\s+)?(?:HANDOFF|NEEDS-STANCE)", up):
        return "noflag"
    return "flag"


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
        sid, func, typ, inp, expect = parts[0], parts[1], parts[2], parts[3], parts[4]
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
            "input": inp,                      # the fixture text fed to the grader (freshness-bound, MF-3)
            # flag/noflag is the verdict-line/panel/handoff signal; lattice rows grade on expect_class instead.
            "expect": _derive_expect(expect, mech),
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
            for fld in ("grading_mechanism", "grader", "expect", "expect_class", "expect_reason", "input", "is_anchor"):
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


# ─────────────────────────────────────────────────────────────────────────────
# G1-b — the scorer. Given per-scenario recorded grader RESULTS, score each by its
# grading_mechanism, apply the threshold, emit the tally. The DRAFT-side twin of
# verdicts.py: pure scoring functions the selftest drives with synthetic results; the
# CLI wires the real result store + the real DET-green signal (run_checks --selftest).
#
# TRUSTED-not-verified (same surface as verdicts.py / gate_state): the store records WHICH
# result was entered and the INPUT it was produced from (the input_hash freshness binding,
# so an INPUT edit makes a result stale -> FAIL), but it CANNOT prove a recorded result came
# from a real judge run rather than a hand-typed one. The sign-off (G1-c) keys on suite_hash;
# `score` printing "PASS" attests the recorded results pass, not that they are unfabricated.
# ─────────────────────────────────────────────────────────────────────────────

RESULTS_DIR = HERE.parent / "state" / "rub-results"  # one <scenario-id>.json per recorded result


def _coerce_bool(v):
    """verdicts.py twin (verdicts.py:_coerce_bool): a real bool, or the strings 'true'/'false'; anything else
    (None, a number, junk) is None -> the caller fails toward flagging (L059). Stops a string 'false' silently
    reading as not-flagged."""
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.strip().lower() in ("true", "false"):
        return v.strip().lower() == "true"
    return None


def _input_hash(input_text: str) -> str:
    import hashlib
    return hashlib.sha256((input_text or "").strip().encode()).hexdigest()[:12]

_STOP = {"flag", "must", "with", "that", "this", "from", "over", "name", "names", "than",
         "into", "they", "their", "when", "what", "which", "where", "have", "been", "also",
         "only", "true", "false", "scope", "claim", "prose", "result", "results"}


def _expect_stance(reason: str) -> str | None:
    """The stance a handoff-state flag scenario must route to, parsed from EXPECT (needs-stance(/X))."""
    m = re.search(r"needs-stance\(/?(interpret|work|scout|plan|review)\)", reason.lower())
    if m:
        return m.group(1)
    m = re.search(r"/(interpret|work|scout|plan|review)\b", reason.lower())
    return m.group(1) if m else None


def _reason_keywords(reason: str) -> set[str]:
    """Salient defect terms for the binding anchor reason-match (MF-4). Keep ids (e006) + content words."""
    toks = re.findall(r"[a-z0-9][a-z0-9-]{3,}", reason.lower())
    return {t for t in toks if t not in _STOP}


def score_one(rec: dict, result: dict | None) -> tuple[bool, str]:
    """Score ONE scenario from its recorded grader result. Returns (passed, why). Fail-safe: a missing or
    malformed result is never a PASS (L059)."""
    mech, expect = rec["grading_mechanism"], rec["expect"]
    if result is None:
        return False, "no recorded result (ungraded)"

    if mech == "verdict-line":
        rs = _coerce_bool(result.get("ready_to_ship"))   # MF-1: a string 'false' must not read as not-flagged
        f = result.get("findings")
        f_is_int = isinstance(f, int) and not isinstance(f, bool)   # bool is an int subclass — exclude it
        if rs is None and not f_is_int:
            return False, "malformed verdict (no usable ready_to_ship / findings) -> treated not-ready (flag)"
        # a found defect = the judge flagged it. An uncoercible ready_to_ship already failed above; here rs is a
        # real bool or None-with-a-real-findings-count, so fail toward flag when ready_to_ship is anything but True.
        flagged = (rs is not True) or (f_is_int and f > 0)
        passed = (flagged == (expect == "flag"))
        why = f"judge {'flagged' if flagged else 'clean'}; expect={expect}"

    elif mech == "panel-synthesis":
        cs, mapped = result.get("conclusion_status"), bool(result.get("all_objections_mapped"))
        # bare SURVIVES with every objection claim-mapped = no-flag; SURVIVES-IF-NARROWED / DOES-NOT-SURVIVE /
        # unmapped = flag (the verdicts.py synthesis rule — ternary, not boolean).
        flagged = not (cs == "SURVIVES" and mapped)
        passed = (flagged == (expect == "flag"))
        why = f"panel={cs} mapped={mapped} -> {'flag' if flagged else 'clean'}; expect={expect}"

    elif mech == "lattice-classification":
        cls, exp = result.get("classified"), rec.get("expect_class")
        # MF-2: a missing classification or a None expect_class must NOT pass via None==None.
        passed = (cls is not None and exp is not None and cls == exp)
        why = f"classified {cls!r}; expect_class={exp!r}"

    elif mech == "handoff-state":
        opened, stance = bool(result.get("handoff_opened")), result.get("handoff_stance")
        narrowed, wrev = bool(result.get("prose_narrowed")), bool(result.get("classified_writing_revise"))
        if expect == "flag":  # MUST emit a needs-stance handoff to the right stance, and NOT narrow prose
            exp = _expect_stance(rec["expect_reason"])
            passed = opened and (exp is None or stance == exp) and not narrowed
            why = f"opened={opened} stance={stance!r}(exp {exp!r}) narrowed={narrowed}"
        else:  # over-routing guard (SC-XSTANCE-08/16): MUST NOT emit AND must classify writing-revise (both halves)
            passed = (not opened) and wrev
            why = f"opened={opened} writing-revise={wrev} (both halves required)"

    else:
        return False, f"unknown grading_mechanism {mech!r}"

    # MF-4: for the never-waivable anchors, a flag must NAME the right defect, not merely fire.
    if passed and rec.get("is_anchor") and expect == "flag":
        kws = _reason_keywords(rec["expect_reason"])
        ftext = (result.get("finding_text") or "").lower()
        if kws and not any(k in ftext for k in kws):
            return False, f"ANCHOR flagged but finding did not name the expected defect ({why})"
    return passed, why


def score_suite(records: list[dict], entries: dict[str, dict], det_green: bool) -> dict:
    """Apply the threshold: every DET green AND every RUB recorded-fresh-and-PASS, anchors never waivable.
    `entries` maps id -> the full recorded record {"result", "input_hash"}; a result whose input_hash no longer
    matches the live scenario INPUT is STALE -> treated missing -> FAIL (MF-3, the verdicts.py freshness twin)."""
    per_mech: dict[str, list[int]] = {}   # mechanism -> [pass, total]
    failures: list[tuple[str, str]] = []
    missing: list[str] = []
    stale: list[str] = []
    anchor_fail: list[str] = []
    for rec in records:
        sid = rec["id"]
        entry = entries.get(sid)
        res = None
        if entry is None:
            missing.append(sid)
        elif entry.get("input_hash") != _input_hash(rec.get("input", "")):
            stale.append(sid)            # recorded against an old INPUT -> must be re-run, never counts as current
        else:
            res = entry.get("result")
        passed, why = score_one(rec, res)
        if entry is not None and res is None and sid in stale:
            why = "STALE result (scenario INPUT changed since it was recorded) -> re-run required"
        m = rec["grading_mechanism"]
        per_mech.setdefault(m, [0, 0])
        per_mech[m][1] += 1
        if passed:
            per_mech[m][0] += 1
        else:
            failures.append((sid, why))
            if rec.get("is_anchor"):
                anchor_fail.append(sid)
    rub_clean = not failures            # missing/stale rows are already failures (score_one returns False)
    overall = bool(det_green and rub_clean)
    return {
        "overall": overall, "det_green": det_green, "rub_clean": rub_clean,
        "n": len(records), "missing": missing, "stale": stale, "failures": failures,
        "anchor_fail": anchor_fail, "per_mechanism": per_mech,
    }


def _load_results(results_dir: Path) -> dict[str, dict]:
    """id -> {"result", "input_hash"}. A corrupt file = a missing result = a FAIL (fail-safe), never a PASS."""
    out: dict[str, dict] = {}
    if not results_dir.exists():
        return out
    for p in sorted(results_dir.glob("*.json")):
        try:
            d = json.loads(p.read_text())
            out[d["id"]] = {"result": d.get("result", {}), "input_hash": d.get("input_hash")}
        except Exception:
            continue
    return out


def record_result(sid: str, result: dict, results_dir: Path, input_text: str) -> int:
    """Stamp the result with the hash of the INPUT it was produced from, so a later INPUT edit makes it stale."""
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / f"{sid}.json").write_text(
        json.dumps({"id": sid, "result": result, "input_hash": _input_hash(input_text)}) + "\n")
    print(f"record: {sid} (input_hash {_input_hash(input_text)}) -> {results_dir / (sid + '.json')}")
    return 0


def suite_hash(records: list[dict], entries: dict[str, dict], outcome: dict) -> str:
    """The content hash the G1-c sign-off token keys on (so a sign-off dies when any result/outcome changes)."""
    import hashlib
    payload = json.dumps({
        "ids": sorted(r["id"] for r in records),
        "entries": {k: entries[k] for k in sorted(entries)},
        "overall": outcome["overall"],
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


SIGNOFF = HERE.parent / "state" / "rub-signoff.json"


def _compute(scenarios: Path, store: Path, results_dir: Path, det_green: bool | None):
    """Shared by `score` and `sign-off`: validate the store, get the DET-green signal, load results, score.
    Returns (records, entries, outcome, suite_hash) or None if the store is invalid (a hard precondition)."""
    if validate_suite(scenarios, store) != 0:
        return None
    records = json.loads(store.read_text())["scenarios"]
    if det_green is None:  # the real every-DET-green signal: run_checks runs every DET script's --selftest
        import subprocess
        rc = subprocess.run([sys.executable, str(HERE / "run_checks.py"), "--selftest"],
                            capture_output=True, text=True).returncode
        det_green = (rc == 0)
    entries = _load_results(results_dir)
    out = score_suite(records, entries, det_green)
    return records, entries, out, suite_hash(records, entries, out)


def score(scenarios: Path, store: Path, results_dir: Path, det_green: bool | None) -> int:
    """CLI: validate the store, get the DET-green signal, load recorded results, score, print the tally + hash."""
    computed = _compute(scenarios, store, results_dir, det_green)
    if computed is None:
        print("score: FAIL — fix validate-suite first (store integrity is a precondition).")
        return 1
    records, entries, out, h = computed
    print(f"\nRUB suite score  (hash {h})")
    print(f"  DET floor green : {out['det_green']}")
    for m, (p, t) in sorted(out["per_mechanism"].items()):
        print(f"  {m:22} {p}/{t}")
    if out["missing"]:
        print(f"  UNGRADED (no result, => FAIL): {len(out['missing'])}  e.g. {out['missing'][:5]}")
    if out["stale"]:
        print(f"  STALE (INPUT changed since recorded, => FAIL): {len(out['stale'])}  e.g. {out['stale'][:5]}")
    if out["failures"]:
        print(f"  FAILURES ({len(out['failures'])}):")
        for sid, why in out["failures"][:20]:
            tag = "  ANCHOR" if sid in out["anchor_fail"] else ""
            print(f"     {sid}{tag}: {why}")
    print(f"\nrub_harness score: {'PASS — suite ready' if out['overall'] else 'FAIL'}"
          + ("" if out["overall"] else f"  (det_green={out['det_green']}, anchor_fail={out['anchor_fail']})"))
    return 0 if out["overall"] else 1


# ─── G1-c sign-off: a recorded Erfan token over the current suite hash (lift of accept-residual). ───
# It REFUSES a failing suite, and goes STALE the moment the suite changes (the token's suite_hash no longer
# matches) — so a sign-off can never silently cover a later edit. TRUSTED-not-verified, same as the rest.

def signoff_decision(outcome: dict) -> tuple[bool, str]:
    """A sign-off is allowed iff the whole threshold passed (DET green ∧ every RUB PASS ∧ no anchor failure)."""
    if not outcome["overall"]:
        return False, (f"REFUSED — suite not passing (det_green={outcome['det_green']}, "
                       f"{len(outcome['failures'])} RUB failure(s), anchor_fail={outcome['anchor_fail']})")
    return True, "all RUB PASS, DET floor green, no anchor failure"


def read_signoff(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def signoff_status(current_hash: str, path: Path) -> tuple[str, str]:
    """SIGNED (token matches the current suite) / STALE (suite changed since) / UNSIGNED."""
    tok = read_signoff(path)
    if not tok or not isinstance(tok, dict) or "suite_hash" not in tok:
        return "UNSIGNED", "no valid sign-off token"
    if tok["suite_hash"] == current_hash:
        return "SIGNED", f"signed by {tok.get('by')!r} for suite {current_hash}"
    return "STALE", f"token is for suite {tok['suite_hash']}, current is {current_hash} — re-sign required"


def sign_off(scenarios: Path, store: Path, results_dir: Path, det_green: bool | None,
             by: str | None, note: str, status_only: bool, signoff_path: Path) -> int:
    computed = _compute(scenarios, store, results_dir, det_green)
    if computed is None:
        print("sign-off: FAIL — store invalid (fix validate-suite).")
        return 1
    _records, _entries, out, h = computed
    if status_only:
        state, msg = signoff_status(h, signoff_path)
        print(f"sign-off status: {state} — {msg}")
        return 0 if state == "SIGNED" else 1
    ok_to_sign, why = signoff_decision(out)
    if not ok_to_sign:
        print(f"sign-off: {why}")
        return 1
    if not by:
        print("sign-off: --by is required to record who signed.")
        return 1
    import time
    signoff_path.parent.mkdir(parents=True, exist_ok=True)
    signoff_path.write_text(json.dumps(
        {"by": by, "note": note, "suite_hash": h, "n": out["n"], "at": int(time.time())}) + "\n")
    print(f"sign-off: RECORDED — {by} signed suite {h} ({out['n']} RUB scenarios, all PASS). -> {signoff_path}")
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
    # oracle G1-c MF-1: the over-routing guards must derive expect=noflag (they phrase it without 'MUST NOT').
    guards = {r["id"]: r["expect"] for r in live if r["id"] in ("SC-XSTANCE-08", "SC-XSTANCE-16")}
    check("over-routing guards SC-XSTANCE-08/16 derive expect=noflag (MF-1)",
          guards == {"SC-XSTANCE-08": "noflag", "SC-XSTANCE-16": "noflag"})
    check("the handoff flag rows (e.g. 01,02) stay expect=flag",
          all(r["expect"] == "flag" for r in live if r["id"] in ("SC-XSTANCE-01", "SC-XSTANCE-02")))
    check("_derive_expect: 'NOT a handoff' -> noflag", _derive_expect("classify writing-revise, NOT a handoff", "handoff-state") == "noflag")
    check("_derive_expect: 'prose NOT narrowed' stays flag", _derive_expect("needs-stance(/interpret); prose NOT narrowed", "handoff-state") == "flag")
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

    # 4. G1-b scoring — one MUST-flag AND one MUST-NOT-flag synthetic per mechanism (oracle MF-5 symmetry),
    #    plus the anchor reason-binding, the missing-result fail-safe, and the threshold.
    def rec(mech, expect, **kw):
        return {"id": kw.pop("id", "SC-X"), "grading_mechanism": mech, "expect": expect,
                "expect_reason": kw.pop("reason", ""), "is_anchor": kw.pop("anchor", False),
                "expect_class": kw.pop("expect_class", None), "input": kw.pop("input", "fixture")}

    def entry(rec_, result):  # wrap a result as a fresh recorded entry (matching input_hash)
        return {"result": result, "input_hash": _input_hash(rec_["input"])}

    # verdict-line: flag <=> not ready / findings>0
    check("verdict-line MUST-flag PASS", score_one(rec("verdict-line", "flag"), {"ready_to_ship": False, "findings": 1})[0])
    check("verdict-line MUST-flag FAIL when judge says clean",
          not score_one(rec("verdict-line", "flag"), {"ready_to_ship": True, "findings": 0})[0])
    check("verdict-line MUST-NOT-flag PASS (near-miss clean)",
          score_one(rec("verdict-line", "noflag"), {"ready_to_ship": True, "findings": 0})[0])
    check("verdict-line MUST-NOT-flag FAIL when judge flags a near-miss",
          not score_one(rec("verdict-line", "noflag"), {"ready_to_ship": False, "findings": 2})[0])
    check("verdict-line malformed result -> FAIL (fail-safe)",
          not score_one(rec("verdict-line", "noflag"), {})[0])
    # MF-1: a string 'false' / 0 must NOT read as not-flagged (the _coerce_bool silent-pass)
    check("verdict-line string 'false' on a near-miss -> FAIL (MF-1)",
          not score_one(rec("verdict-line", "noflag"), {"ready_to_ship": "false", "findings": 0})[0])
    check("verdict-line string 'true' on a near-miss -> PASS (MF-1 coerces)",
          score_one(rec("verdict-line", "noflag"), {"ready_to_ship": "true", "findings": 0})[0])
    check("verdict-line findings:True (bool) is not a finding count",
          score_one(rec("verdict-line", "noflag"), {"ready_to_ship": "true", "findings": True})[0])
    # panel-synthesis: bare SURVIVES + mapped = clean; else flag (ternary)
    check("panel MUST-NOT-flag PASS on bare SURVIVES+mapped",
          score_one(rec("panel-synthesis", "noflag"), {"conclusion_status": "SURVIVES", "all_objections_mapped": True})[0])
    check("panel SURVIVES-IF-NARROWED counts as flag",
          score_one(rec("panel-synthesis", "flag"), {"conclusion_status": "SURVIVES-IF-NARROWED", "all_objections_mapped": True})[0])
    check("panel unmapped objection counts as flag",
          score_one(rec("panel-synthesis", "flag"), {"conclusion_status": "SURVIVES", "all_objections_mapped": False})[0])
    # lattice-classification: graded on expect_class
    check("lattice MUST-classify-NEW PASS", score_one(rec("lattice-classification", "classify", expect_class="NEW"), {"classified": "NEW"})[0])
    check("lattice wrong classification FAIL", not score_one(rec("lattice-classification", "classify", expect_class="OLD"), {"classified": "NEW"})[0])
    # MF-2: missing classification + None expect_class must NOT pass via None==None
    check("lattice None==None -> FAIL (MF-2)", not score_one(rec("lattice-classification", "classify", expect_class=None), {})[0])
    check("lattice missing classification -> FAIL", not score_one(rec("lattice-classification", "classify", expect_class="OLD"), {})[0])
    # handoff-state: flag scenario needs the right stance + no narrowing; guard needs absent + writing-revise
    check("handoff flag PASS (right stance, not narrowed)",
          score_one(rec("handoff-state", "flag", reason="needs-stance(/interpret) names E006"),
                    {"handoff_opened": True, "handoff_stance": "interpret", "prose_narrowed": False, "finding_text": "E006"})[0])
    check("handoff flag FAIL when prose narrowed anyway",
          not score_one(rec("handoff-state", "flag", reason="needs-stance(/interpret)"),
                        {"handoff_opened": True, "handoff_stance": "interpret", "prose_narrowed": True})[0])
    check("handoff flag FAIL on wrong stance",
          not score_one(rec("handoff-state", "flag", reason="needs-stance(/work)"),
                        {"handoff_opened": True, "handoff_stance": "scout", "prose_narrowed": False})[0])
    check("handoff guard PASS (no handoff + writing-revise)",
          score_one(rec("handoff-state", "noflag"), {"handoff_opened": False, "classified_writing_revise": True})[0])
    check("handoff guard FAIL when triage did NOTHING (both halves required)",
          not score_one(rec("handoff-state", "noflag"), {"handoff_opened": False, "classified_writing_revise": False})[0])
    # MF-4: anchor flagged but for the WRONG reason -> FAIL even though it flagged
    voa = rec("verdict-line", "flag", id="SC-VOICE-01", anchor=True, reason="MUST flag storytelling / agency-to-abstraction")
    check("ANCHOR flag PASS when finding names the defect",
          score_one(voa, {"ready_to_ship": False, "findings": 1, "finding_text": "storytelling: the question 'earns'"})[0])
    check("ANCHOR flag FAIL when finding names the WRONG defect (MF-4 binding)",
          not score_one(voa, {"ready_to_ship": False, "findings": 1, "finding_text": "em-dash splice"})[0])
    # threshold via score_suite (entries are id -> {result, input_hash})
    rA, rB = rec("verdict-line", "flag", id="A"), rec("verdict-line", "noflag", id="B")
    good = {"A": entry(rA, {"ready_to_ship": False, "findings": 1}), "B": entry(rB, {"ready_to_ship": True, "findings": 0})}
    check("score_suite PASS when DET green + all RUB pass", score_suite([rA, rB], good, True)["overall"])
    check("score_suite FAIL when DET not green", not score_suite([rA, rB], good, False)["overall"])
    check("score_suite FAIL on a missing result", not score_suite([rA, rB], {"A": good["A"]}, True)["overall"])
    # MF-3: a result recorded against an OLD input is stale -> FAIL, even though it would otherwise PASS
    stale_entries = {"A": {"result": {"ready_to_ship": False, "findings": 1}, "input_hash": _input_hash("OLD INPUT")},
                     "B": good["B"]}
    so = score_suite([rA, rB], stale_entries, True)
    check("score_suite FAIL on a stale (input changed) result (MF-3)", (not so["overall"]) and so["stale"] == ["A"])
    arec = [rec("verdict-line", "flag", id="SC-VOICE-01", anchor=True, reason="MUST flag storytelling")]
    bad = {"SC-VOICE-01": entry(arec[0], {"ready_to_ship": False, "findings": 1, "finding_text": "wrong reason"})}
    out = score_suite(arec, bad, True)
    check("score_suite reports an anchor failure", out["anchor_fail"] == ["SC-VOICE-01"] and not out["overall"])
    # record/_load round-trip (now stamps + returns input_hash)
    with tempfile.TemporaryDirectory() as td:
        rd = Path(td) / "r"
        record_result("SC-Z", {"ready_to_ship": True, "findings": 0}, rd, "the fixture")
        loaded = _load_results(rd).get("SC-Z")
        check("record/_load round-trip carries result + input_hash",
              loaded["result"] == {"ready_to_ship": True, "findings": 0} and loaded["input_hash"] == _input_hash("the fixture"))
        (rd / "SC-bad.json").write_text("{ nope")
        check("corrupt result file -> not loaded (=> missing => FAIL)", "SC-bad" not in _load_results(rd))

    # 5. G1-c sign-off: refuse a failing suite; SIGNED only when the token matches the current hash; STALE after.
    passing = {"overall": True, "det_green": True, "failures": [], "anchor_fail": []}
    failing = {"overall": False, "det_green": True, "failures": [("X", "y")], "anchor_fail": ["SC-VOICE-01"]}
    check("sign-off ALLOWED on a passing suite", signoff_decision(passing)[0])
    check("sign-off REFUSED on a failing suite", not signoff_decision(failing)[0])
    with tempfile.TemporaryDirectory() as td:
        sp = Path(td) / "signoff.json"
        check("UNSIGNED when no token", signoff_status("abc123", sp)[0] == "UNSIGNED")
        sp.write_text(json.dumps({"by": "Erfan", "suite_hash": "abc123"}))
        check("SIGNED when token matches current hash", signoff_status("abc123", sp)[0] == "SIGNED")
        check("STALE when suite changed (hash differs)", signoff_status("def456", sp)[0] == "STALE")
        sp.write_text("{ corrupt")
        check("UNSIGNED on a corrupt token (fail-safe)", signoff_status("abc123", sp)[0] == "UNSIGNED")

    print("rub_harness selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="RUB-grading harness for the /write pipeline (G1).")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("validate-suite", "gen-store", "score"):
        p = sub.add_parser(name)
        p.add_argument("--scenarios", type=Path, default=SCENARIOS_MD)
        p.add_argument("--store", type=Path, default=STORE)
    score_p = sub.choices["score"]
    score_p.add_argument("--results-dir", type=Path, default=RESULTS_DIR)
    score_p.add_argument("--det-green", dest="det_green", action="store_true", default=None,
                         help="assert the DET floor is green instead of running run_checks --selftest (testing)")
    rp = sub.add_parser("record")
    rp.add_argument("--id", required=True)
    rp.add_argument("--result", required=True, help="the grader result as a JSON object")
    rp.add_argument("--results-dir", type=Path, default=RESULTS_DIR)
    rp.add_argument("--store", type=Path, default=STORE)
    so = sub.add_parser("sign-off")
    so.add_argument("--scenarios", type=Path, default=SCENARIOS_MD)
    so.add_argument("--store", type=Path, default=STORE)
    so.add_argument("--results-dir", type=Path, default=RESULTS_DIR)
    so.add_argument("--det-green", dest="det_green", action="store_true", default=None)
    so.add_argument("--by", default=None, help="who is signing (required to record a sign-off)")
    so.add_argument("--note", default="")
    so.add_argument("--status", action="store_true", help="report SIGNED/STALE/UNSIGNED for the current suite")
    so.add_argument("--signoff-path", type=Path, default=SIGNOFF)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest()
    if args.cmd == "validate-suite":
        return validate_suite(args.scenarios, args.store)
    if args.cmd == "gen-store":
        return gen_store(args.scenarios, args.store)
    if args.cmd == "score":
        return score(args.scenarios, args.store, args.results_dir, args.det_green)
    if args.cmd == "record":
        try:
            result = json.loads(args.result)
        except Exception as e:
            ap.error(f"--result must be a JSON object: {e}")
        # bind the result to the scenario's CURRENT input (so a later INPUT edit makes it stale, MF-3).
        try:
            store_recs = json.loads(args.store.read_text())["scenarios"]
        except Exception as e:
            ap.error(f"cannot read store {args.store}: {e}")
        match = [r for r in store_recs if r["id"] == args.id]
        if not match:
            ap.error(f"{args.id} is not a RUB scenario in {args.store}")
        return record_result(args.id, result, args.results_dir, match[0].get("input", ""))
    if args.cmd == "sign-off":
        return sign_off(args.scenarios, args.store, args.results_dir, args.det_green,
                        args.by, args.note, args.status, args.signoff_path)
    ap.error("a subcommand or --selftest is required")


if __name__ == "__main__":
    sys.exit(main())
