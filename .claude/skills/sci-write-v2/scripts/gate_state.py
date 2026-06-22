#!/usr/bin/env python3
r"""gate_state (F16) — the no-prose-before-approval ordering floor (D047 content-hash pattern).

The human gates the COUPLED PACKAGE as one unit: message + reader-model + the claim/argument lattice +
the skeleton. No prose (stage >= 4) may exist before a matching approval. A stage-6 LOGIC revision (F14)
that changes a gated field changes the package hash, so the prior approval goes stale and the gate must
re-fire — exactly the D047 "a YES dies the moment a byte changes" behaviour, but over the lattice package.

The hash is over a CANONICAL PROJECTION of the gated fields, NOT the raw file: meta.stage, tags[] (written
at stage 4, post-gate) and deviation_log are EXCLUDED, so advancing the stage or adding \evd tags does not
invalidate an approval (SC-PROC-12), while changing a claim/warrant/skeleton field does (SC-PROC-5 / F14).

  approve <lattice>   record the current package hash as approved (the GATE moment writes this; the
                      orchestrator presents the package via AskUserQuestion/ExitPlanMode, then calls this).
  check <lattice>     the ordering floor: if stage >= 4, the current package hash MUST be approved, else block.

GATE (the human approval moment, AskUserQuestion/ExitPlanMode) is the orchestrator's job; THIS is the
mechanical floor that the orchestrator cannot argue past.

Usage:
    python gate_state.py approve LATTICE.json
    python gate_state.py check   LATTICE.json
    python gate_state.py --selftest

Exit code: check -> 0 clean / 1 blocked; approve -> 0; bad input -> nonzero.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

DRAFT_STAGE = 4  # prose generation begins here
GATED_CLAIM_KEYS = ["claim_id", "text", "bound_experiment", "evidence_status",
                    "strength", "scope", "is_central", "section", "acknowledgments"]  # NOT tags


def repo_root(explicit: str | None = None) -> Path:
    return Path(explicit or os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()


def _coerce_stage(stage):
    """int stage, or None if unparseable. (bool is not a stage.)"""
    if isinstance(stage, bool):
        return None
    if isinstance(stage, int):
        return stage
    if isinstance(stage, str) and stage.strip().lstrip("-").isdigit():
        return int(stage)
    return None


def _canon(members: list) -> list:
    """Sort a member list by its FULL canonical content, so a colliding partial key cannot reorder-flip
    the hash (two warrants/figures sharing from/to or figure_id but differing elsewhere)."""
    return sorted(members, key=lambda m: json.dumps(m, sort_keys=True, ensure_ascii=False))


def _projection(lattice: dict) -> dict:
    """The gated coupled package, canonicalized so the hash is stable across non-gated changes.
    Trusts lattice_integrity to have run first (it guarantees required keys present + claim_id unique);
    a missing claim key here defaults to None, which would collide with an explicit null — not reachable
    through a valid lattice."""
    claims = [c for c in lattice.get("claims", []) if isinstance(c, dict)]
    proj_claims = [{k: c.get(k) for k in GATED_CLAIM_KEYS} for c in claims]
    # sections: claim_ids is set-membership per LATTICE rule 4 (node->section), so within-section ORDER is
    # presentation, not logic — sort it so a benign reorder does not needlessly re-fire the human gate.
    sections = [{"section_id": s.get("section_id"), "title": s.get("title"),
                 "claim_ids": sorted(str(x) for x in (s.get("claim_ids") or []))}
                for s in lattice.get("sections", []) if isinstance(s, dict)]
    return {
        "message": lattice.get("message"),
        "reader_model": lattice.get("reader_model"),
        "claims": _canon(proj_claims),
        "warrants": _canon([w for w in lattice.get("warrants", []) if isinstance(w, dict)]),
        "figures": _canon([f for f in lattice.get("figures", []) if isinstance(f, dict)]),
        "sections": _canon(sections),
    }


def package_hash(lattice: dict) -> str:
    blob = json.dumps(_projection(lattice), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def _approvals_path(root: Path) -> Path:
    d = root / ".claude/state/sw-gate"
    d.mkdir(parents=True, exist_ok=True)
    return d / "approvals.json"


def _load(root: Path) -> dict:
    p = _approvals_path(root)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def approve(lattice: dict, root: Path) -> tuple[str, list[str]]:
    # The store is TRUSTED, not verified (same model as D047's verdict.json) — an agent that can write
    # approvals.json has already defeated the gate. Keyed by the package hash itself (no group_key): the
    # projection includes the message + full claim set, so a cross-deliverable hash collision is not a
    # practical risk. Read-modify-write is not atomic (single-agent serial use only).
    notes = []
    stage = _coerce_stage((lattice.get("meta") or {}).get("stage"))
    if stage is None or stage < 3:
        notes.append(f"[premature-approval] stage={stage}: the coupled package is approved at stage 3 (after "
                     f"the skeleton); this approval will not match the full package and drafting will block.")
    elif stage >= DRAFT_STAGE:
        notes.append(f"[late-approval] stage={stage}: approving a package that is already drafting; the gate "
                     f"is meant to precede prose. (Recorded anyway; check() still enforces hash match.)")
    h = package_hash(lattice)
    d = _load(root)
    d[h] = {"approved": True}
    _approvals_path(root).write_text(json.dumps(d, indent=2))
    return h, notes


def check(lattice: dict, root: Path, drafting: bool = False) -> list[str]:
    """The ordering floor. Findings (non-empty => block).

    `drafting` is the GROUND TRUTH that prose exists (run_checks passes it when given --prose). The floor
    binds to prose-existence, NOT to the agent-self-reported meta.stage: an agent that writes prose but
    leaves stage=3 must not slip past the gate. So we enforce when drafting=True OR the stage reads >= 4 OR
    the stage is unparseable (fail safe). Only a genuine pre-draft lattice (real int stage < 4, no prose)
    is exempt.
    """
    f = []
    stage = _coerce_stage((lattice.get("meta") or {}).get("stage"))
    if not drafting and stage is not None and stage < DRAFT_STAGE:
        return f  # no prose signal and stage is pre-draft; ordering not in play
    h = package_hash(lattice)
    if not _load(root).get(h, {}).get("approved"):
        f.append(f"[no-prose-before-approval] stage {stage}: the coupled package (hash {h}) was not "
                 f"approved before drafting. Either it was never gated (SC-PROC-1), only partially gated "
                 f"(SC-PROC-2), or a gated field changed since approval and the case must re-enter the gate "
                 f"(F14 / SC-PROC-5).")
    return f


def report(findings: list[str]) -> int:
    if findings:
        print(f"\ngate_state — BLOCKED:")
        for m in findings:
            print(f"  {m}")
        return 1
    print("gate_state: PASS (ordering ok)")
    return 0


# --------------------------------------------------------------------------- selftest
def _selftest() -> int:
    import tempfile
    ok = True

    def claim(cid, section="results", strength="observed", tags=None):
        return {"claim_id": cid, "text": f"claim {cid}", "bound_experiment": "E006", "evidence_status": "live",
                "strength": strength, "scope": "scoped", "is_central": False, "acknowledgments": [],
                "section": section, "tags": tags or []}

    def lat(stage, sections, *claims, warrants=None, message="m"):
        return {"meta": {"stage": stage, "schema_version": "1"}, "message": message, "reader_model": {"v": "ml"},
                "claims": list(claims), "warrants": warrants or [], "figures": [],
                "sections": sections, "deviation_log": []}

    def expect(name, findings, want_block, rule=None):
        nonlocal ok
        blocked = len(findings) > 0
        rule_hit = rule is None or any(f"[{rule}]" in x for x in findings)
        good = (blocked == want_block) and (rule_hit if want_block else True)
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name
              + ("" if good else f" -> want_block={want_block} rule={rule}, got {findings}"))
        ok = ok and good

    secs = [{"section_id": "results", "title": "R", "claim_ids": ["C1"]}]

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # SC-PROC-1: stage-4 prose, never approved -> block.
        expect("SC-PROC-1 prose-before-gate", check(lat(4, secs, claim("C1")), root), True, "no-prose-before-approval")
        # the stage=3-with-prose bypass: drafting=True must enforce even though stage reads pre-draft.
        expect("prose-exists overrides stage=3", check(lat(3, secs, claim("C1")), root, drafting=True), True, "no-prose-before-approval")
        # but a genuine pre-draft (no prose signal, stage 3) is NOT blocked.
        expect("genuine pre-draft not blocked", check(lat(3, secs, claim("C1")), root, drafting=False), False)

        # happy: approve the stage-3 package, then draft (stage 4, tags added) -> PASS.
        pkg3 = lat(3, secs, claim("C1"))
        approve(pkg3, root)
        drafted = lat(4, secs, claim("C1", tags=[{"strength": "observed", "sentence_ref": "s"}]))
        expect("approved then drafted (tags added) -> pass", check(drafted, root), False)

        # SC-PROC-12: post-gate internal re-check, no gated-field change, no new prose -> MUST NOT block.
        expect("SC-PROC-12 internal recheck no-change", check(pkg3, root), False)  # stage 3, not even drafting

        # SC-PROC-5 / F14: a gated field (a warrant) changes at stage 4 -> hash mismatch -> block.
        changed = lat(4, secs, claim("C1", tags=[{"strength": "observed", "sentence_ref": "s"}]),
                      warrants=[{"from": "C1", "to": "C1", "warrant": "new warrant added post-approval"}])
        expect("SC-PROC-5 logic-change re-enters gate", check(changed, root), True, "no-prose-before-approval")

        # a gated TEXT change (claim re-scoped) at stage 4 -> block.
        rescoped = lat(4, secs, claim("C1", tags=[{"strength": "observed", "sentence_ref": "s"}]))
        rescoped["claims"][0]["scope"] = "WIDER scope than approved"
        expect("gated scope-change re-enters gate", check(rescoped, root), True)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # SC-PROC-2: approval recorded over a PARTIAL package (no skeleton) -> drafting the full package blocks.
        partial = lat(2, [], claim("C1", section=None))  # stage 2, no sections
        _h, notes = approve(partial, root)
        partial_warned = any("premature-approval" in n for n in notes)
        print(("  ok: " if partial_warned else "  SELFTEST FAIL: ") + "SC-PROC-2 approve warns on partial package"
              + ("" if partial_warned else f" -> {notes}"))
        ok = ok and partial_warned
        full4 = lat(4, secs, claim("C1"))  # the full package, now drafting
        expect("SC-PROC-2 partial approval != full package", check(full4, root), True, "no-prose-before-approval")

        # stage-2 lattice (pre-draft) is never blocked regardless of approval.
        expect("stage<4 never blocked", check(lat(2, [], claim("C1", section=None)), root), False)

    # --- oracle's new regression guards ---
    clone = lambda d: json.loads(json.dumps(d))
    sec2 = [{"section_id": "results", "title": "R", "claim_ids": ["C1", "C2"]}]
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # SC-C7-A: a stringified stage="4" with prose must FAIL SAFE -> block (the open-fail bypass).
        strpkg = lat(4, secs, claim("C1")); strpkg["meta"]["stage"] = "4"
        expect("SC-C7-A string-stage fails safe", check(strpkg, root), True, "no-prose-before-approval")

        # approve a 2-claim stage-3 package, then exercise benign-reorder precision guards.
        base3 = lat(3, sec2, claim("C1"), claim("C2"),
                    warrants=[{"from": "C1", "to": "C2", "warrant": "a"}, {"from": "C1", "to": "C2", "warrant": "b"}])
        base3["figures"] = [{"figure_id": "f", "claim_id": "C1"}, {"figure_id": "f", "claim_id": "C2"}]
        base3["reader_model"] = {"a": 1, "b": 2}
        approve(base3, root)
        draft = clone(base3); draft["meta"]["stage"] = 4
        for c in draft["claims"]:
            c["tags"] = [{"strength": "observed", "sentence_ref": "s"}]
        expect("clean drafted package passes", check(draft, root), False)

        # SC-C7-B: reorder a section's claim_ids (no membership change) -> set-membership -> PASS.
        b = clone(draft); b["sections"][0]["claim_ids"] = ["C2", "C1"]
        expect("SC-C7-B claim_ids reorder benign", check(b, root), False)
        # SC-C7-C: reorder two warrants sharing (from,to) -> full-object canon -> PASS.
        c = clone(draft); c["warrants"] = list(reversed(c["warrants"]))
        expect("SC-C7-C warrant collision reorder benign", check(c, root), False)
        # SC-C7-D: reorder two figures sharing figure_id -> PASS.
        d = clone(draft); d["figures"] = list(reversed(d["figures"]))
        expect("SC-C7-D figure collision reorder benign", check(d, root), False)
        # SC-C7-H: reorder reader_model keys -> sort_keys -> PASS.
        h = clone(draft); h["reader_model"] = {"b": 2, "a": 1}
        expect("SC-C7-H reader_model key order benign", check(h, root), False)
        # SC-C7-G: add tags + a deviation_log entry (both non-gated) -> PASS.
        g = clone(draft); g["deviation_log"] = [{"functionality": "F8a", "method": "m", "why": "w", "did": "d"}]
        expect("SC-C7-G non-gated additions benign", check(g, root), False)
        # SC-C7-E: change a claim's acknowledgments (gated) -> BLOCK.
        e = clone(draft); e["claims"][0]["acknowledgments"] = ["a new limitation not approved"]
        expect("SC-C7-E acks change re-gates", check(e, root), True, "no-prose-before-approval")
        # SC-C7-F: add a brand-new claim + section (new package) -> BLOCK.
        ff = clone(draft)
        ff["claims"].append(claim("C3")); ff["sections"][0]["claim_ids"].append("C3")
        expect("SC-C7-F new claim re-gates", check(ff, root), True, "no-prose-before-approval")

    print("gate_state selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F16 no-prose-before-approval ordering floor (D047 pattern).")
    sub = ap.add_subparsers(dest="cmd")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--repo-root", type=Path, default=None)
    pa = sub.add_parser("approve")
    pa.add_argument("lattice", type=Path)
    pc = sub.add_parser("check")
    pc.add_argument("lattice", type=Path)
    pc.add_argument("--drafting", action="store_true",
                    help="prose exists (the ground-truth drafting signal): enforce regardless of meta.stage")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    root = repo_root(str(args.repo_root) if args.repo_root else None)
    if args.cmd in ("approve", "check"):
        try:
            lattice = json.loads(args.lattice.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise SystemExit(f"gate_state: {args.lattice}: NOT FOUND")
        except json.JSONDecodeError as e:
            raise SystemExit(f"gate_state: {args.lattice}: invalid JSON ({e})")
        if args.cmd == "approve":
            h, notes = approve(lattice, root)
            for n in notes:
                print(n)
            print(f"gate_state: approved package hash {h}")
            return 0
        return report(check(lattice, root, drafting=args.drafting))
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
