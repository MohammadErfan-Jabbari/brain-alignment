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
import datetime
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

# X2 (D050): the stances a cross-stance handoff may route to (the owning truth-producing / direction stances).
HANDOFF_STANCES = {"work", "interpret", "review", "scout", "plan"}


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

    # X2 (D050): the sticky cross-stance-handoff blocker. Read the store INDEPENDENTLY of the prose hash —
    # a reword (new hash -> stale readers) must never clear a substrate defect; only the upstream stance
    # recording its output (handoff resolve) can. A MISSING store == zero open (the no-op invariant: every
    # pre-X2 draft converges exactly as before); a CORRUPT store fails toward blocking (can't prove zero-open).
    # This is an extra clause, NOT an 8th REQUIRED reader — adding it to REQUIRED would re-key it to the prose
    # hash and defeat the whole point (that is the M1 keystone).
    handoffs = _load_handoffs(root)
    if handoffs is None:
        lines.append("  [handoffs-open] handoffs.json unreadable -> treated as blocking (fail-safe)")
        converged = False
    else:
        for hid, rec in handoffs.items():
            if _is_resolved(rec):
                continue
            stance = rec.get("target_stance", "?") if isinstance(rec, dict) else "?"
            lines.append(f"  [handoffs-open] {hid}: unresolved handoff -> /{stance} "
                         f"(blocks convergence; a reword cannot clear it — only the upstream stance can)")
            converged = False

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
    for name in ("active.json", "blocks.json", "residual.json", "handoffs.json"):
        p = base / name
        if p.exists():
            p.unlink()
    vdir = base / "verdicts"
    if vdir.exists():
        shutil.rmtree(vdir, ignore_errors=True)


# --------------------------------------------------------------------------- X2: cross-stance handoff store (D050)
# ONE store, keyed by handoff_id, at .claude/state/sw-gate/handoffs.json — NOT a lattice field. A handoff records a
# substrate defect a /write reader cannot fix by rewording, routes it to the owning stance, and (via status()'s
# handoffs-open clause) STICKILY blocks convergence until the upstream stance records its output. /write never
# resolves a handoff and never adopts the reader's number (carried as proposed_unverified, born later in /work).

def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_resolved(rec) -> bool:
    """Resolved iff explicitly stamped so. Anything else (open, a missing/junk status, a non-dict record) BLOCKS —
    a handoff clears only when its upstream stance records the fix, never by default (fail toward more checking)."""
    return isinstance(rec, dict) and rec.get("status") == "resolved"


def _load_handoffs(root: Path) -> dict | None:
    """Read the handoff store. {} when ABSENT (the no-op invariant: a missing store == zero open, so every pre-X2
    draft and selftest is unchanged). None when present-but-unreadable (the caller fails toward blocking)."""
    p = root / ".claude/state/sw-gate/handoffs.json"
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text())
    except Exception:
        return None
    return d if isinstance(d, dict) else None


def _save_handoffs(root: Path, d: dict) -> Path:
    p = _state(root, "handoffs.json")
    p.write_text(json.dumps(d, indent=2))
    return p


def open_handoffs(root: Path) -> tuple[list[str], bool]:
    """(open-handoff-ids, store_unreadable). Used by status()'s sibling callers ship/accept-residual to refuse
    past an open handoff. A corrupt store reports unreadable=True so those callers also fail toward blocking."""
    d = _load_handoffs(root)
    if d is None:
        return [], True
    return [hid for hid, rec in d.items() if not _is_resolved(rec)], False


def open_handoff(root: Path, hid: str, *, finding: str, threatens_claim: str, target_stance: str,
                 why_not_writing: str, what_to_produce: str, recommended_command: str,
                 proposed_unverified: str | None = None, opened_by_reader: str | None = None) -> Path:
    if not hid or not str(hid).strip():
        raise SystemExit("verdicts: handoff open requires a non-empty handoff_id")
    if target_stance not in HANDOFF_STANCES:
        raise SystemExit(f"verdicts: target_stance {target_stance!r} not in {sorted(HANDOFF_STANCES)}")
    d = _load_handoffs(root)
    if d is None:
        raise SystemExit("verdicts: handoffs.json is corrupt — fix or remove it before opening a handoff")
    d[hid] = {
        "handoff_id": hid,
        "finding": finding,
        "threatens_claim": threatens_claim,
        "why_not_writing": why_not_writing,
        "target_stance": target_stance,
        "what_to_produce": what_to_produce,
        "recommended_command": recommended_command,
        "proposed_unverified": proposed_unverified,   # a reader's recompute; carried, NEVER adopted into prose
        "resolution_ref": None,
        "status": "open",
        "opened_by_reader": opened_by_reader,
        "detected_at": {"session": os.environ.get("CLAUDE_CODE_SESSION_ID", ""), "at": _now_iso()},
    }
    return _save_handoffs(root, d)


def resolve_handoff(root: Path, hid: str, ref: str) -> None:
    if not ref or not str(ref).strip():
        raise SystemExit("verdicts: resolve requires --ref (the recorded upstream output: experiment key / "
                         "decision id / commit / evidence_status change)")
    d = _load_handoffs(root)
    if d is None:
        raise SystemExit("verdicts: handoffs.json is corrupt — fix or remove it before resolving a handoff")
    if hid not in d:
        raise SystemExit(f"verdicts: no handoff {hid!r} to resolve")
    if not isinstance(d[hid], dict):
        # a corrupt/hand-edited non-dict record: refuse with a clean SystemExit like every sibling guard,
        # never a bare TypeError (and never a partial write). The handoff stays open until the store is fixed.
        raise SystemExit(f"verdicts: handoff {hid!r} record is corrupt (not an object) — fix or remove it")
    d[hid]["status"] = "resolved"
    d[hid]["resolution_ref"] = str(ref).strip()
    _save_handoffs(root, d)


def check_handoffs_vs_lattice(root: Path, lattice: dict) -> list[str]:
    """NH4 dangling-handoff guard: an OPEN handoff whose threatens_claim was deleted by a re-skeleton would be an
    unkillable orphan. Flag it so it is re-pointed or resolved. Lives WITH the store, not in lattice_integrity."""
    d = _load_handoffs(root)
    if d is None:
        return ["[handoff-store] handoffs.json unreadable"]
    claim_ids = {c.get("claim_id") for c in lattice.get("claims", []) if isinstance(c, dict)}
    f = []
    for hid, rec in d.items():
        if not isinstance(rec, dict) or _is_resolved(rec):
            continue
        tc = rec.get("threatens_claim")
        if tc is not None and tc not in claim_ids:
            f.append(f"[dangling-handoff] {hid}: threatens_claim '{tc}' is not in the lattice "
                     f"(re-skeletoned away?) — re-point or resolve it")
    return f


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
        open_handoff(root, "HX", finding="f", threatens_claim="C1", target_stance="interpret",
                     why_not_writing="w", what_to_produce="p", recommended_command="/interpret")
        clear_gate_state(root)
        expect("clear: active gone", active_draft(root), None)
        expect("clear: blocks gone", (root / ".claude/state/sw-gate/blocks.json").exists(), False)
        expect("clear: residual gone", (root / ".claude/state/sw-gate/residual.json").exists(), False)
        expect("clear: verdicts gone", (root / ".claude/state/sw-gate/verdicts").exists(), False)
        expect("clear: handoffs gone", (root / ".claude/state/sw-gate/handoffs.json").exists(), False)
        expect("clear: approvals preserved (F16)", (root / ".claude/state/sw-gate/approvals.json").exists(), True)

    # --- X2 (D050): cross-stance handoff store + the sticky `handoffs-open` blocker ---
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prose = root / "d.tex"; prose.write_text("v1\n")
        # NO-OP INVARIANT: with no handoffs.json, 7-ready -> converged exactly as pre-X2 (a missing store is silent).
        for r in REQUIRED:
            record(root, prose, r, True, 0)
        conv, lines = status(root, prose)
        expect("X2 no store -> converged (no-op invariant)", conv, True)
        expect("X2 no store -> no [handoffs-open] line", any("[handoffs-open]" in l for l in lines), False)

        # open a handoff while all 7 are ready -> convergence blocked by the handoff alone.
        open_handoff(root, "H1", finding="E006 CI is a voxel bootstrap (F13)", threatens_claim="C1",
                     target_stance="interpret", why_not_writing="wrong inferential unit, not a wording fix",
                     what_to_produce="fold-level CI", recommended_command="/interpret E006",
                     proposed_unverified="fold CI still excludes 0", opened_by_reader="premortem")
        conv, lines = status(root, prose)
        expect("X2 open handoff blocks convergence", conv, False)
        expect("X2 [handoffs-open] H1 flagged", any("[handoffs-open] H1" in l for l in lines), True)

        # SC-XSTANCE-09 (M1 keystone): reword the prose (new hash) + re-record every reader ready -> STILL blocked.
        prose.write_text("v2 reworded\n")
        for r in REQUIRED:
            record(root, prose, r, True, 0)
        conv, _ = status(root, prose)
        expect("SC-XSTANCE-09 reword cannot clear a handoff", conv, False)

        # SC-XSTANCE-13 (two gates independent): resolve the handoff but leave a reader not-ready -> blocked by reader.
        resolve_handoff(root, "H1", "E006-suspect-recorded")
        record(root, prose, "fidelity", False, 1)
        conv, lines = status(root, prose)
        expect("SC-XSTANCE-13 resolved handoff + not-ready reader -> blocked", conv, False)
        expect("SC-XSTANCE-13 blocked by the reader, not the handoff",
               any("[not-ready] fidelity" in l for l in lines) and not any("[handoffs-open]" in l for l in lines), True)

        # SC-XSTANCE-10 (happy path): resolved handoff + all readers ready -> converged.
        record(root, prose, "fidelity", True, 0)
        conv, _ = status(root, prose)
        expect("SC-XSTANCE-10 resolved + readers ready -> converged", conv, True)

        # SC-XSTANCE-15 (multiple): two handoffs, one open -> blocked until ALL clear.
        open_handoff(root, "H2", finding="needs a source", threatens_claim="C1", target_stance="scout",
                     why_not_writing="cited paper absent from canonical/", what_to_produce="canonical note",
                     recommended_command="/scout")
        conv, _ = status(root, prose)
        expect("SC-XSTANCE-15 one open of two -> blocked", conv, False)
        resolve_handoff(root, "H2", "canonical/foo.md")
        conv, _ = status(root, prose)
        expect("SC-XSTANCE-15 all resolved -> converged", conv, True)

        # SC-XSTANCE-14 (NH4 dangling-handoff guard): an OPEN handoff whose threatens_claim is gone -> flagged.
        open_handoff(root, "H3", finding="orphaned", threatens_claim="CZZ", target_stance="interpret",
                     why_not_writing="w", what_to_produce="p", recommended_command="/interpret")
        lattice = {"claims": [{"claim_id": "C1"}, {"claim_id": "C2"}]}
        fnd = check_handoffs_vs_lattice(root, lattice)
        expect("SC-XSTANCE-14 dangling threatens_claim flagged", any("[dangling-handoff] H3" in x for x in fnd), True)
        # an OPEN handoff pointing at a real claim is NOT flagged.
        open_handoff(root, "H4", finding="real", threatens_claim="C2", target_stance="interpret",
                     why_not_writing="w", what_to_produce="p", recommended_command="/interpret")
        expect("SC-XSTANCE-14 open+valid claim -> not dangling",
               any("H4" in x for x in check_handoffs_vs_lattice(root, lattice)), False)
        # a RESOLVED dangling handoff is NOT flagged (only open ones can block/orphan).
        resolve_handoff(root, "H3", "ref"); resolve_handoff(root, "H4", "ref")
        expect("SC-XSTANCE-14 resolved dangling not flagged",
               any("H3" in x for x in check_handoffs_vs_lattice(root, lattice)), False)

        # target_stance typo guard.
        try:
            open_handoff(root, "HBAD", finding="f", threatens_claim="C1", target_stance="writing",
                         why_not_writing="w", what_to_produce="p", recommended_command="/x")
            expect("X2 bad target_stance rejected", "no-raise", "raise")
        except SystemExit:
            expect("X2 bad target_stance rejected", "raise", "raise")
        # empty handoff_id guard (oracle nice-to-have: as defensive as the CLI wrapper).
        try:
            open_handoff(root, "", finding="f", threatens_claim="C1", target_stance="interpret",
                         why_not_writing="w", what_to_produce="p", recommended_command="/x")
            expect("X2 empty hid rejected", "no-raise", "raise")
        except SystemExit:
            expect("X2 empty hid rejected", "raise", "raise")

    # oracle MUST-FIX: resolve on a CORRUPT (non-dict) record raises a clean SystemExit, never a bare TypeError.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _state(root, "handoffs.json").write_text(json.dumps({"H1": "i am not an object"}))
        try:
            resolve_handoff(root, "H1", "ref")
            expect("X2 resolve on corrupt record -> SystemExit", "no-raise", "raise")
        except SystemExit:
            expect("X2 resolve on corrupt record -> SystemExit", "raise", "raise")
        except Exception as e:
            expect("X2 resolve on corrupt record -> SystemExit", f"raw-{type(e).__name__}", "raise")

    # corrupt store -> fail-safe BLOCK (cannot prove zero-open).
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prose = root / "d.tex"; prose.write_text("p\n")
        for r in REQUIRED:
            record(root, prose, r, True, 0)
        (_state(root, "handoffs.json")).write_text("{not json")
        conv, lines = status(root, prose)
        expect("X2 corrupt store -> blocked (fail-safe)", conv, False)
        expect("X2 corrupt store flagged unreadable",
               any("[handoffs-open]" in l and "unreadable" in l for l in lines), True)

    # MF-A: ship / accept-residual REFUSE past an open handoff (tested through main()'s dispatch + exit codes).
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prose = root / "d.tex"; prose.write_text("p\n")
        open_handoff(root, "H1", finding="f", threatens_claim="C1", target_stance="interpret",
                     why_not_writing="w", what_to_produce="p", recommended_command="/interpret")
        expect("MF-A ship refuses with open handoff", main(["ship", "--repo-root", str(root)]), 1)
        expect("MF-A accept-residual refuses with open handoff",
               main(["accept-residual", "--prose", str(prose), "--repo-root", str(root)]), 1)
        expect("MF-A refused ship did NOT clear the store",
               (root / ".claude/state/sw-gate/handoffs.json").exists(), True)
        resolve_handoff(root, "H1", "ref")
        expect("MF-A ship succeeds once resolved", main(["ship", "--repo-root", str(root)]), 0)
        expect("MF-A ship then cleared the store", (root / ".claude/state/sw-gate/handoffs.json").exists(), False)

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
    ph = sub.add_parser("handoff", parents=[common])    # X2 (D050): cross-stance handoff store ops
    ph.add_argument("action", choices=["open", "resolve", "status", "check"])
    ph.add_argument("hid", nargs="?", help="handoff id (required for open/resolve)")
    ph.add_argument("--finding"); ph.add_argument("--threatens-claim"); ph.add_argument("--target-stance")
    ph.add_argument("--why"); ph.add_argument("--what-to-produce"); ph.add_argument("--recommended-command")
    ph.add_argument("--proposed-unverified", default=None); ph.add_argument("--reader", default=None)
    ph.add_argument("--ref", help="resolve: the recorded upstream output (experiment key / decision id / commit)")
    ph.add_argument("--lattice", type=Path, help="check: the claim-lattice to validate threatens_claim against")
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
        blocking, bad = open_handoffs(root)
        if bad or blocking:
            sys.stderr.write("verdicts: cannot ship — open cross-stance handoff(s): "
                             + (", ".join(blocking) if blocking else "<store unreadable>") + "\n"
                             "Resolve each via its upstream stance first: "
                             "verdicts.py handoff resolve <id> --ref <recorded-output>\n")
            return 1
        clear_gate_state(root)
        print("verdicts: shipped — convergence Stop-hook disarmed + gate state cleared")
        return 0
    if args.cmd == "accept-residual":
        if not args.prose.is_file():
            raise SystemExit(f"verdicts: prose {args.prose}: not a file")
        blocking, bad = open_handoffs(root)
        if bad or blocking:
            sys.stderr.write("verdicts: cannot accept-residual — an open handoff is not a residual the human may "
                             "wave through; only its upstream stance closes it. Open: "
                             + (", ".join(blocking) if blocking else "<store unreadable>") + "\n")
            return 1
        h = accept_residual(root, args.prose)
        print(f"verdicts: accepted-residual sign-off recorded for draft {h}")
        return 0
    if args.cmd == "handoff":
        if args.action == "open":
            if not args.hid:
                raise SystemExit("verdicts: handoff open requires an <id>")
            req = {"--finding": args.finding, "--threatens-claim": args.threatens_claim,
                   "--target-stance": args.target_stance, "--why": args.why,
                   "--what-to-produce": args.what_to_produce, "--recommended-command": args.recommended_command}
            missing = [k for k, v in req.items() if not v]
            if missing:
                raise SystemExit(f"verdicts: handoff open missing required fields: {missing}")
            open_handoff(root, args.hid, finding=args.finding, threatens_claim=args.threatens_claim,
                         target_stance=args.target_stance, why_not_writing=args.why,
                         what_to_produce=args.what_to_produce, recommended_command=args.recommended_command,
                         proposed_unverified=args.proposed_unverified, opened_by_reader=args.reader)
            print(f"verdicts: opened handoff {args.hid} -> /{args.target_stance} "
                  f"(convergence now blocked until the upstream stance resolves it)")
            return 0
        if args.action == "resolve":
            if not args.hid:
                raise SystemExit("verdicts: handoff resolve requires an <id>")
            resolve_handoff(root, args.hid, args.ref)
            print(f"verdicts: resolved handoff {args.hid} (ref {args.ref}) — the writer must still rebind the "
                  f"claim and the readers re-run clean before it converges")
            return 0
        if args.action == "status":
            d = _load_handoffs(root)
            if d is None:
                print("verdicts handoff: handoffs.json UNREADABLE (treated as blocking)")
                return 1
            openk = [h for h, r in d.items() if not _is_resolved(r)]
            donek = [h for h, r in d.items() if _is_resolved(r)]
            print(f"verdicts handoff: {len(openk)} open, {len(donek)} resolved")
            for h in openk:
                rec = d[h] if isinstance(d[h], dict) else {}
                print(f"  [open]     {h} -> /{rec.get('target_stance', '?')}: {rec.get('finding', '')}")
            for h in donek:
                rec = d[h] if isinstance(d[h], dict) else {}
                print(f"  [resolved] {h} (ref {rec.get('resolution_ref')})")
            return 1 if openk else 0
        if args.action == "check":
            if not args.lattice:
                raise SystemExit("verdicts: handoff check requires --lattice <claim-lattice.json>")
            try:
                lattice = json.loads(args.lattice.read_text(encoding="utf-8"))
            except FileNotFoundError:
                raise SystemExit(f"verdicts: {args.lattice}: NOT FOUND")
            except json.JSONDecodeError as e:
                raise SystemExit(f"verdicts: {args.lattice}: invalid JSON ({e})")
            findings = check_handoffs_vs_lattice(root, lattice)
            if findings:
                print("verdicts handoff check — dangling:")
                for x in findings:
                    print(f"  {x}")
                return 1
            print("verdicts handoff check: PASS (no dangling open handoff)")
            return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
