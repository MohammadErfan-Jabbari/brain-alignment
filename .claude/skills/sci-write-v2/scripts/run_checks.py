#!/usr/bin/env python3
r"""run_checks — the DET floor dispatcher for the redesigned /write pipeline.

One call that runs every deterministic check over a (lattice, prose) pair and returns one aggregate
exit code, so the orchestrator gates the whole rigid floor in a single step. The RUB judges (the voice
auditor, the claim-fidelity assertion judge, the thinking panel) are model subagents and are NOT here —
this is the mechanical floor only.

Checks, in order:
  lattice_integrity validate <lattice>   schema/coverage/referential integrity of the spine (F15/F6/F7)
  claim_binding     validate <lattice>   every claim bound to a live recorded result, or a \gap (F3)
  claim_fidelity    validate <lattice>   every \evd tag <= its bound claim's strength (F9a)
  gate_state        check    <lattice>   no prose (stage>=4) without a matching package approval (F16)
  [if --prose]
  draft_check       validate <prose> <lattice>   sections realized, claims tagged, prose<->lattice agree (F8a)
  ai_tell_lint      <prose>               lexical voice tells: em-dash, jargon, authority-grab (F12 DET)

Usage:
    python run_checks.py --lattice LATTICE.json [--prose PROSE] [--repo-root DIR]
    python run_checks.py --selftest      # run every component's own --selftest (integration smoke)

Exit code: 0 if every applicable check passed, 1 otherwise.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _run(script: str, *args) -> tuple[int, str]:
    target = HERE / script
    if not target.exists():
        return 127, f"{script}: NOT FOUND"
    p = subprocess.run([sys.executable, str(target), *map(str, args)], capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def run_stack(lattice: Path, prose: Path | None, state_root: Path | None, prev: Path | None) -> int:
    # Two roots are DISTINCT: evidence (docs/experiments) is auto-resolved by claim_binding from the lattice's
    # own location; the gate-approval STATE root is the only thing --repo-root controls. Conflating them
    # (one flag for both) false-dangled evidence under a scratch root — fixed by not passing a root to
    # claim_binding at all.
    state_args = ["--repo-root", str(state_root)] if state_root else []
    drafting = ["--drafting"] if prose else []
    steps = [
        ("lattice_integrity.py", ["validate", str(lattice)]),
        ("claim_binding.py", ["validate", str(lattice)]),  # self-resolves the evidence repo root
        ("claim_fidelity.py", ["validate", str(lattice)]),
        ("warrant_schema.py", ["validate", str(lattice)]),  # F4 DET: no empty-warrant edges
        # gate ordering binds to prose-existence (--drafting), not the self-reported stage.
        ("gate_state.py", state_args + ["check", str(lattice)] + drafting),
    ]
    if prev:  # append-safe / round-trip guard: no claim/field dropped or content-emptied between writes
        steps.append(("lattice_integrity.py", ["diff", str(prev), str(lattice)]))
    if prose:
        steps += [
            ("draft_check.py", ["validate", str(prose), str(lattice)]),
            ("ai_tell_lint.py", [str(prose)]),
            ("scope_lint.py", ["validate", str(prose)]),  # F5 DET: scope-words + uncited novelty
        ]
    failed = False
    for script, args in steps:
        rc, out = _run(script, *args)
        tag = "PASS" if rc == 0 else ("MISSING" if rc == 127 else "FAIL")
        print(f"[{tag}] {script}")
        if rc != 0:
            failed = True
            for line in out.strip().splitlines():
                print(f"    {line}")
    print("\nrun_checks: " + ("FAIL (fix the floor above)" if failed else "PASS (DET floor clean)"))
    return 1 if failed else 0


def _selftest() -> int:
    ok = True
    for script in ("lattice_integrity.py", "claim_binding.py", "claim_fidelity.py",
                   "draft_check.py", "gate_state.py", "ai_tell_lint.py",
                   "warrant_schema.py", "scope_lint.py"):
        rc, _out = _run(script, "--selftest")
        good = rc == 0
        print(("  ok: " if good else "  SELFTEST FAIL: ") + f"{script} --selftest (rc={rc})")
        ok = ok and good
    print("run_checks selftest: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="DET floor dispatcher for the /write pipeline.")
    ap.add_argument("--lattice", type=Path)
    ap.add_argument("--prose", type=Path, default=None)
    ap.add_argument("--prev", type=Path, default=None,
                    help="the prior lattice snapshot; runs the append-safe/round-trip diff guard")
    ap.add_argument("--repo-root", type=Path, default=None,
                    help="gate-approval STATE root (gate_state only); evidence resolves automatically")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest()
    if not args.lattice:
        ap.error("--lattice is required (or use --selftest)")
    return run_stack(args.lattice, args.prose, args.repo_root, args.prev)


if __name__ == "__main__":
    sys.exit(main())
