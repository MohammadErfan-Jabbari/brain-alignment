#!/usr/bin/env python3
r"""verdicts (F14 / P2-D) — the stage-5 convergence state machine (D047 content-hash pattern).

Each stage-5 RUB reader emits, as its final line, a machine-readable verdict:

    <TAG>-VERDICT: {"ready_to_ship": <true|false>, "findings": <int>}

The orchestrator records each into  .claude/state/sw-gate/verdicts/<prose-hash>/<reader>.json
and the convergence Stop-hook (P2-D-3) calls `status` to decide: BLOCK the agent from
finishing while any reader is missing or not ready, RELEASE once every reader is ready.

Keyed to the PROSE CONTENT HASH, not the agent's say-so: edit one byte of the draft and every
prior verdict is stale (its hash no longer matches the new prose) -> not found -> re-block. This
is exactly the D047 "a YES dies the moment a byte changes" gate, applied to the draft instead of
the lattice package (gate_state.py is the F16 lattice-side twin).

The seven required readers (SKILL.md stage-5 RUB set that gates ready_to_ship):
  argument (F4) · scope (F5) · fidelity (F9b) · structure (F11) · voice (F12)
  · premortem (F13, synthesized by the orchestrator — see below) · acknowledgment (F18)
F19 (consistency) is a DET check inside run_checks, not a RUB subagent verdict, so it is NOT a reader
here; its only RUB half (caption <= figure, SC-XS-3) is now judged by the F5 scope reader (P2-D-5,
re-mapped F19->F5), so it rides `scope`'s verdict — no extra reader. (SKILL.md stage-5 ends the fan-out at F18.)

`findings` means UNRESOLVED BLOCKING findings, so `ready_to_ship: true` requires `findings: 0`. A verdict
with `ready_to_ship: true AND findings > 0` is self-contradictory and is treated NOT ready (fail-safe).

The `premortem` (F13) verdict has no agent line of its own — the shared panel (`premortem-analyst` +
`counter-argument`) emits `PANEL-VERDICT: …` with no `ready_to_ship` slot. The orchestrator SYNTHESIZES it
(this rule is duplicated verbatim in SKILL.md stage 5 — keep them identical):
  objections := counter-argument's objections + premortem-analyst's TOP-RISK (advisory risks are folded in
                as objections, else they are invisible to convergence).
  premortem ready := counter-argument CONCLUSION-STATUS == SURVIVES (bare; SURVIVES-IF-NARROWED and
                     DOES-NOT-SURVIVE are both NOT ready) AND every objection MAPPED to a claim (an unmapped
                     objection is the SC-ARG-5 defect).
  findings := (# unmapped objections) + (1 if CONCLUSION-STATUS != SURVIVES else 0)  -- never 0 when not ready.
This chunk records that synthesized boolean; verifying it was synthesized from a FRESH panel run (not
hand-typed) is the freshness control that P2-D-3's Stop-hook MUST add — without it the store is fabricable
in one turn (same TRUSTED-not-verified model as gate_state.py).

The draft `--prose` path MUST be the ONE canonical current draft (the F8b voice-realize output, not the F8a
pre-voice draft both of which exist on disk at stage 4). P2-D-3 pins this by reading `meta.draft_path` from
the lattice so the hook needs no orchestrator-supplied path. Tag-remapping in lattice.tags[] without a
prose-byte change is out of scope here (owned by the stage-write round-trip diff `run_checks --prev`).

  record --prose P --reader R --ready true|false [--findings N]   file one reader's verdict
  status --prose P                                                converged? (exit 0 yes / 1 no)

Exit code: status -> 0 converged / 1 not; record -> 0; bad input -> nonzero.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# The stage-5 RUB readers that must all be ready_to_ship for the draft to converge.
# reader-key -> the VERDICT label the agent emits (documentation; the orchestrator records by key).
READER_TAGS = {
    "argument": "ARGUMENT-VERDICT",      # F4 sw-argument-judge (prose site)
    "scope": "SCOPE-VERDICT",            # F5 sw-scope-judge (prose site)
    "fidelity": "FIDELITY-VERDICT",      # F9b sw-claim-fidelity-judge
    "structure": "STRUCTURE-VERDICT",    # F11 sw-structure-judge (prose site)
    "voice": "VOICE-VERDICT",            # F12 sw-voice-auditor
    "premortem": "PREMORTEM-VERDICT",    # F13 panel, synthesized by the orchestrator
    "acknowledgment": "ACK-VERDICT",     # F18 sw-acknowledgment (stage-5 re-run)
}
REQUIRED = list(READER_TAGS)


def repo_root(explicit: str | None = None) -> Path:
    return Path(explicit or os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()


def prose_hash(prose_path: Path) -> str:
    # ponytail: raw file bytes. A re-save with identical content keeps the hash (correct); a
    # whitespace-only churn re-fires the audit. Normalize here only if that churn ever bites.
    return hashlib.sha256(prose_path.read_bytes()).hexdigest()[:16]


def _vdir(root: Path, h: str) -> Path:
    d = root / ".claude/state/sw-gate/verdicts" / h
    d.mkdir(parents=True, exist_ok=True)
    return d


def _coerce_bool(v) -> bool | None:
    """A real bool, or a JSON-ish string; anything else is None (unparseable -> treated not-ready)."""
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.strip().lower() in ("true", "false"):
        return v.strip().lower() == "true"
    return None


def record(root: Path, prose_path: Path, reader: str, ready: bool, findings: int) -> Path:
    if reader not in REQUIRED:
        raise SystemExit(f"verdicts: unknown reader {reader!r}; expected one of {REQUIRED}")
    h = prose_hash(prose_path)
    p = _vdir(root, h) / f"{reader}.json"
    p.write_text(json.dumps({"reader": reader, "ready_to_ship": bool(ready), "findings": int(findings)}))
    return p


def status(root: Path, prose_path: Path) -> tuple[bool, list[str]]:
    """Converged iff every required reader has a verdict for the CURRENT prose hash and all are ready."""
    h = prose_hash(prose_path)
    d = root / ".claude/state/sw-gate/verdicts" / h
    lines, converged = [], True
    for reader in REQUIRED:
        f = d / f"{reader}.json"
        if not f.exists():
            lines.append(f"  [missing]   {reader}: no verdict for the current draft (hash {h})")
            converged = False
            continue
        r, n = None, None
        try:
            v = json.loads(f.read_text())
            if isinstance(v, dict):
                r = _coerce_bool(v.get("ready_to_ship"))
                fv = v.get("findings")
                n = fv if isinstance(fv, int) and not isinstance(fv, bool) else None
        except Exception:
            r = None
        if r is None:
            lines.append(f"  [unparsed]  {reader}: verdict unreadable -> treated not ready (fail-safe)")
            converged = False
        elif r and (n or 0) > 0:
            # self-contradiction: ready_to_ship but blocking findings remain -> fail-safe, never a silent pass.
            lines.append(f"  [contradiction] {reader}: ready_to_ship=true but findings={n} -> treated not ready")
            converged = False
        elif not r:
            lines.append(f"  [not-ready] {reader}: {n if n is not None else '?'} finding(s) unresolved")
            converged = False
        else:
            lines.append(f"  [ready]     {reader}")
    return converged, lines


# --------------------------------------------------------------------------- gate state (the Stop-hook reads these)
# The convergence Stop-hook (P2-D-3) is pipeline-scoped via `active.json`: the orchestrator writes it at stage 4
# with the ONE canonical draft (the F8b output), and the hook NO-OPS when it is absent — so it never blocks an
# unrelated session. active.json is also the canonical-path pin (the hook trusts it, not a per-call arg).
def _state(root: Path, name: str) -> Path:
    d = root / ".claude/state/sw-gate"
    d.mkdir(parents=True, exist_ok=True)
    return d / name


def activate(root: Path, draft: Path) -> Path:
    # Stamp the arming session so the Stop-hook enforces only for THIS session (a stale active.json from an
    # abandoned earlier session is disarmed, not nagged at unrelated future sessions). Same value space as the
    # Stop event's session_id — verified empirically 2026-06-23: CLAUDE_CODE_SESSION_ID == the transcript
    # filename == the event session_id. If a future CC build diverges these, the hook degrades to a no-op
    # (it disarms on the apparent mismatch) — fail-safe (never blocks a stranger), but silently off; re-verify.
    sess = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    if not sess:
        sys.stderr.write("verdicts: WARNING — CLAUDE_CODE_SESSION_ID unset; the convergence gate will self-disarm "
                         "(it cannot tie the draft to a session) and will NOT enforce. Arm from a real session.\n")
    p = _state(root, "active.json")
    p.write_text(json.dumps({"draft": str(draft.resolve()), "session": sess}))
    return p


def active_session(root: Path) -> str | None:
    p = root / ".claude/state/sw-gate/active.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text()).get("session")
    except Exception:
        return None


def deactivate(root: Path) -> None:
    p = root / ".claude/state/sw-gate/active.json"
    if p.exists():
        p.unlink()


def active_draft(root: Path) -> Path | None:
    p = root / ".claude/state/sw-gate/active.json"
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text()).get("draft")
        return Path(d) if d else None
    except Exception:
        return None


def bump_block(root: Path, h: str) -> int:
    """Count consecutive blocks for one draft hash (the Stop-hook's MAX_BLOCKS loop guard). An edit changes the
    hash and starts a fresh count, so real progress is never penalised."""
    p = _state(root, "blocks.json")
    try:
        d = json.loads(p.read_text()) if p.exists() else {}
    except Exception:
        d = {}
    d[h] = int(d.get(h, 0)) + 1
    p.write_text(json.dumps(d))
    return d[h]


def accept_residual(root: Path, draft: Path) -> str:
    """Erfan's escape hatch: sign off the CURRENT draft bytes so the hook stops blocking (keyed to the hash, so a
    later edit voids the sign-off)."""
    h = prose_hash(draft)
    p = _state(root, "residual.json")
    try:
        d = json.loads(p.read_text()) if p.exists() else {}
    except Exception:
        d = {}
    d[h] = True
    p.write_text(json.dumps(d))
    return h


def is_residual(root: Path, draft: Path) -> bool:
    p = root / ".claude/state/sw-gate/residual.json"
    if not p.exists():
        return False
    try:
        return bool(json.loads(p.read_text()).get(prose_hash(draft)))
    except Exception:
        return False


def session_matches(armed: str | None, event: str | None) -> bool:
    """True ONLY when both session ids are present and equal. The Stop-hook enforces iff this is True, so it
    must fail toward False (disarm/release) on ANY uncertainty: a wrongly-blocked unrelated session is a
    session-wide outage, so a missing/empty/mismatched id can never authorize a block."""
    return bool(armed) and bool(event) and armed == event


def clear_gate_state(root: Path) -> None:
    """End-of-run cleanup (called by `ship`): drop the convergence state for the finished run so it cannot
    grow unbounded or leave a stale residual. Leaves approvals.json (gate_state.py / F16 owns it)."""
    import shutil
    base = root / ".claude/state/sw-gate"
    for name in ("active.json", "blocks.json", "residual.json"):
        p = base / name
        if p.exists():
            p.unlink()
    vdir = base / "verdicts"
    if vdir.exists():
        shutil.rmtree(vdir, ignore_errors=True)


def report_status(converged: bool, lines: list[str], h: str) -> int:
    print(f"verdicts — draft {h}: {'CONVERGED' if converged else 'NOT CONVERGED'}")
    for ln in lines:
        print(ln)
    return 0 if converged else 1


# --------------------------------------------------------------------------- selftest
def _selftest() -> int:
    import tempfile
    ok = True

    def expect(name, got, want):
        nonlocal ok
        good = got == want
        print(("  ok: " if good else "  SELFTEST FAIL: ") + name + ("" if good else f" -> got {got!r} want {want!r}"))
        ok = ok and good

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prose = root / "draft.tex"
        prose.write_text("\\section{R} We observe a null. %%SECTION\n")

        # no verdicts at all -> not converged, all 7 missing.
        conv, lines = status(root, prose)
        expect("empty: not converged", conv, False)
        expect("empty: all 7 missing", sum("[missing]" in l for l in lines), 7)

        # partial: 3 of 7 ready -> not converged.
        for r in ("argument", "scope", "voice"):
            record(root, prose, r, True, 0)
        conv, lines = status(root, prose)
        expect("partial: not converged", conv, False)
        expect("partial: 4 still missing", sum("[missing]" in l for l in lines), 4)

        # all 7 ready -> converged (exit-0 condition).
        for r in REQUIRED:
            record(root, prose, r, True, 0)
        conv, _ = status(root, prose)
        expect("all ready: converged", conv, True)

        # one reader not ready -> not converged.
        record(root, prose, "fidelity", False, 2)
        conv, lines = status(root, prose)
        expect("one not-ready: not converged", conv, False)
        expect("one not-ready: flagged", any("[not-ready] fidelity" in l for l in lines), True)

        # STALENESS: edit the draft -> new hash -> the prior all-ready verdicts no longer count.
        record(root, prose, "fidelity", True, 0)  # heal it under the OLD hash
        conv, _ = status(root, prose)
        expect("healed under old hash: converged", conv, True)
        prose.write_text("\\section{R} We observe a null, edited. %%SECTION\n")
        conv, lines = status(root, prose)
        expect("edited draft: verdicts stale -> not converged", conv, False)
        expect("edited draft: all missing again", sum("[missing]" in l for l in lines), 7)

        # fail-safe: a corrupt verdict file counts as not-ready, never a silent pass (L059).
        for r in REQUIRED:
            record(root, prose, r, True, 0)
        h = prose_hash(prose)
        (root / ".claude/state/sw-gate/verdicts" / h / "voice.json").write_text("{not json")
        conv, lines = status(root, prose)
        expect("corrupt verdict: not converged", conv, False)
        expect("corrupt verdict: fail-safe flagged", any("[unparsed]" in l and "voice:" in l for l in lines), True)

        # a "true"/"false" string boolean is accepted; junk is not-ready.
        expect("coerce 'true'", _coerce_bool("true"), True)
        expect("coerce 'false'", _coerce_bool("false"), False)
        expect("coerce junk -> None", _coerce_bool("yes"), None)

        # record rejects an unknown reader (typo guard).
        try:
            record(root, prose, "voce", True, 0)
            expect("unknown reader rejected", "no-raise", "raise")
        except SystemExit:
            expect("unknown reader rejected", "raise", "raise")

    # --- oracle P2-D-1 boundary scenarios (B1–B8) ---
    def raw(root, prose, reader, text):
        """Drop a raw (possibly malformed) verdict file under the current prose hash."""
        (_vdir(root, prose_hash(prose)) / f"{reader}.json").write_text(text)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prose = root / "d.tex"
        prose.write_text("\\section{R} x\n")

        # B1: ready=true but findings>0 is a self-contradiction -> not converged.
        for r in REQUIRED:
            record(root, prose, r, True, 5)
        conv, lines = status(root, prose)
        expect("B1 ready+findings>0 contradiction", conv, False)
        expect("B1 flagged as contradiction", any("[contradiction]" in l for l in lines), True)

        # B2/B3/B4: malformed ready_to_ship and non-dict verdict files -> all [unparsed], never ready.
        for r in REQUIRED:  # reset to ready first, then corrupt some
            record(root, prose, r, True, 0)
        raw(root, prose, "argument", json.dumps({"ready_to_ship": 1, "findings": 0}))      # int
        raw(root, prose, "scope", json.dumps({"ready_to_ship": "ok"}))                      # junk str
        raw(root, prose, "voice", json.dumps({"ready_to_ship": [True]}))                    # list
        raw(root, prose, "fidelity", json.dumps({"findings": 0}))                           # key absent (B3)
        raw(root, prose, "structure", json.dumps([1, 2, 3]))                                # non-dict (B4)
        raw(root, prose, "premortem", "true")                                               # bare scalar (B4)
        conv, lines = status(root, prose)
        expect("B2/B3/B4 malformed -> not converged", conv, False)
        expect("B2/B3/B4 -> 6 unparsed", sum("[unparsed]" in l for l in lines), 6)

        # B5: a stray (non-required) verdict file is ignored; the required set still governs.
        for r in REQUIRED:
            record(root, prose, r, True, 0)
        raw(root, prose, "consistency", json.dumps({"ready_to_ship": False, "findings": 9}))
        conv, _ = status(root, prose)
        expect("B5 stray file ignored -> converged", conv, True)

        # B6: a 0-byte prose file still hashes and is not converged with no verdicts.
        empty = root / "empty.tex"
        empty.write_text("")
        conv, _ = status(root, empty)
        expect("B6 empty prose -> not converged", conv, False)

    # B7: the truthy set is exactly {true,false} (case-insensitive, whitespace-trimmed) — nothing wider.
    for s, want in [("1", None), ("yes", None), ("y", None), ("", None), ("True ", True), ("  false", False)]:
        expect(f"B7 coerce {s!r}", _coerce_bool(s), want)

    # B8: a verdict recorded under hash H never counts under a different hash H2 (prose changed).
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prose = root / "d.tex"
        prose.write_text("v1\n")
        for r in REQUIRED:
            record(root, prose, r, True, 0)
        prose.write_text("v2\n")  # hash changes; the v1 verdicts are now unreachable
        conv, lines = status(root, prose)
        expect("B8 verdicts under old hash don't count", conv, False)
        expect("B8 all missing under new hash", sum("[missing]" in l for l in lines), 7)

    # --- gate-state ops (the Stop-hook reads these) ---
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        d1 = root / "f8b.tex"; d1.write_text("draft one\n")
        d2 = root / "other.tex"; d2.write_text("draft two\n")
        expect("active_draft none before activate", active_draft(root), None)
        os.environ["CLAUDE_CODE_SESSION_ID"] = "sess-A"
        activate(root, d1)
        expect("active_draft after activate", active_draft(root) and active_draft(root).read_bytes(), b"draft one\n")
        expect("active_session stamped from env", active_session(root), "sess-A")
        deactivate(root)
        expect("active_draft none after ship", active_draft(root), None)
        deactivate(root)  # idempotent (no active.json) — must not raise
        expect("ship idempotent", active_draft(root), None)
        h = prose_hash(d1)
        expect("bump_block 1", bump_block(root, h), 1)
        expect("bump_block 2", bump_block(root, h), 2)
        expect("bump_block resets per hash", bump_block(root, prose_hash(d2)), 1)
        expect("residual false before sign-off", is_residual(root, d1), False)
        accept_residual(root, d1)
        expect("residual true after sign-off", is_residual(root, d1), True)
        expect("residual is per-draft (other draft not signed)", is_residual(root, d2), False)
        d1.write_text("draft one edited\n")  # editing the draft voids the sign-off (hash changed)
        expect("residual void after edit", is_residual(root, d1), False)

        # session_matches: enforce ONLY when both ids present and equal; fail toward disarm on ANY uncertainty
        # (these six are the catastrophe cases — a falsy fallthrough here would block unrelated sessions).
        expect("session_matches A==A", session_matches("A", "A"), True)
        expect("session_matches empty-armed -> False", session_matches("", "B"), False)
        expect("session_matches None-armed -> False", session_matches(None, "B"), False)
        expect("session_matches missing-event -> False", session_matches("A", None), False)
        expect("session_matches empty-event -> False", session_matches("A", ""), False)
        expect("session_matches mismatch -> False", session_matches("A", "B"), False)

        # clear_gate_state wipes the convergence state (active/blocks/residual/verdicts) but NOT approvals.json (F16).
        activate(root, d1); bump_block(root, prose_hash(d1)); accept_residual(root, d1)
        (root / ".claude/state/sw-gate/approvals.json").write_text("{}")
        record(root, d1, "voice", True, 0)
        clear_gate_state(root)
        expect("clear: active gone", active_draft(root), None)
        expect("clear: blocks gone", (root / ".claude/state/sw-gate/blocks.json").exists(), False)
        expect("clear: residual gone", (root / ".claude/state/sw-gate/residual.json").exists(), False)
        expect("clear: verdicts gone", (root / ".claude/state/sw-gate/verdicts").exists(), False)
        expect("clear: approvals preserved (F16)", (root / ".claude/state/sw-gate/approvals.json").exists(), True)

    print("verdicts selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="F14/P2-D stage-5 convergence state machine (D047 pattern).")
    ap.add_argument("--selftest", action="store_true")
    # --repo-root lives on the subcommands (pass it AFTER record/status); production falls back to
    # $CLAUDE_PROJECT_DIR via repo_root(), so the hook/orchestrator usually need not pass it at all.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", type=Path, default=None)
    sub = ap.add_subparsers(dest="cmd")
    pr = sub.add_parser("record", parents=[common])
    pr.add_argument("--prose", type=Path, required=True)
    pr.add_argument("--reader", required=True)
    pr.add_argument("--ready", required=True, choices=["true", "false"])
    pr.add_argument("--findings", type=int, default=0)
    ps = sub.add_parser("status", parents=[common])
    ps.add_argument("--prose", type=Path, required=True)
    pa = sub.add_parser("activate", parents=[common])   # orchestrator, stage 4: arm the Stop-hook on this draft
    pa.add_argument("--prose", type=Path, required=True)
    sub.add_parser("ship", parents=[common])            # orchestrator, after converge+approve: disarm the hook
    pres = sub.add_parser("accept-residual", parents=[common])  # Erfan: sign off the current draft bytes
    pres.add_argument("--prose", type=Path, required=True)
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()
    root = repo_root(str(args.repo_root) if args.repo_root else None)
    if args.cmd == "record":
        if not args.prose.is_file():
            raise SystemExit(f"verdicts: prose {args.prose}: not a file")
        p = record(root, args.prose, args.reader, args.ready == "true", args.findings)
        print(f"verdicts: recorded {args.reader} -> {p}")
        return 0
    if args.cmd == "status":
        if not args.prose.is_file():
            raise SystemExit(f"verdicts: prose {args.prose}: not a file")
        conv, lines = status(root, args.prose)
        return report_status(conv, lines, prose_hash(args.prose))
    if args.cmd == "activate":
        if not args.prose.is_file():
            raise SystemExit(f"verdicts: prose {args.prose}: not a file")
        activate(root, args.prose)
        print(f"verdicts: armed convergence Stop-hook on {args.prose}")
        return 0
    if args.cmd == "ship":
        clear_gate_state(root)
        print("verdicts: shipped — convergence Stop-hook disarmed + gate state cleared")
        return 0
    if args.cmd == "accept-residual":
        if not args.prose.is_file():
            raise SystemExit(f"verdicts: prose {args.prose}: not a file")
        h = accept_residual(root, args.prose)
        print(f"verdicts: accepted-residual sign-off recorded for draft {h}")
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
