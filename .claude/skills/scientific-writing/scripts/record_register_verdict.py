#!/usr/bin/env python3
"""Record a clean register verdict for a deliverable group (D047).

This is the ONLY way to satisfy the Stop-hook register gate. It refuses to record
a clean verdict unless it is handed >= N fresh prose-register-auditor outputs that
ALL say `REGISTER-CLEAN: YES`. It then stamps the verdict keyed to the CURRENT
content hash of the deliverable group, so the verdict dies the moment a byte changes.

The verdict is therefore never a bare self-claim: it is parsed from real auditor
outputs and bound to specific bytes. (The auditors must be FRESH spawns — separate
Agent calls with no writing context — because in-session self-review is exactly what
under-detected in the v0.2 session: 3 residuals found vs ~13 on a fresh strict pass.)

Usage:
    # record a clean verdict from fresh auditor outputs saved to files:
    record_register_verdict.py --group manuscript-extended --audits a1.txt a2.txt [--min 2]

    # log an Erfan-approved accepted-residual sign-off for the current bytes:
    record_register_verdict.py --group manuscript-extended --accept-residual --note "..."
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import register_state as rs  # noqa: E402

VERDICT_RE = re.compile(r"REGISTER-CLEAN:\s*(YES|NO)", re.I)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Record the register convergence verdict (D047).")
    ap.add_argument("--group", required=True, help="e.g. manuscript-extended or report:docs/reports/R08_*.md")
    ap.add_argument("--audits", nargs="*", default=[], help="files holding each FRESH auditor's raw output")
    ap.add_argument("--min", type=int, default=2, help="minimum fresh auditors required (default 2)")
    ap.add_argument("--accept-residual", action="store_true", help="log an Erfan-approved residual sign-off instead")
    ap.add_argument("--note", default="", help="note for the accepted-residual sign-off")
    ap.add_argument("--repo-root", default=None)
    a = ap.parse_args(argv)
    root = rs.repo_root(a.repo_root)
    h = rs.content_hash(a.group, root)

    if not rs.group_files(a.group, root):
        print(f"REFUSED: group '{a.group}' resolves to no files under {root}", file=sys.stderr)
        return 1

    if a.accept_residual:
        sp = rs.sentinel_path(a.group, root, h)
        sp.write_text(f"accepted-residual\ngroup={a.group}\nhash={h}\nts={int(time.time())}\nnote={a.note}\n")
        print(f"LOGGED accepted-residual for {a.group} @ {h}. Stop gate will pass for these exact bytes.")
        return 0

    if not a.audits:
        print("REFUSED: pass --audits with the fresh auditor output files (or --accept-residual).", file=sys.stderr)
        return 1

    total = 0
    yes = 0
    bad: list[str] = []
    for f in a.audits:
        try:
            txt = Path(f).read_text(errors="replace")
        except Exception as e:
            bad.append(f"{f}: unreadable ({e})")
            total += 1
            continue
        total += 1
        verdicts = VERDICT_RE.findall(txt)
        if not verdicts:
            bad.append(f"{f}: no REGISTER-CLEAN line")
            continue
        # clean only if a YES is present and NO NO appears anywhere
        if any(v.upper() == "NO" for v in verdicts):
            bad.append(f"{f}: verdict NO")
            continue
        if any(v.upper() == "YES" for v in verdicts):
            yes += 1
        else:
            bad.append(f"{f}: ambiguous verdict")

    if total < a.min:
        print(f"REFUSED: need >= {a.min} fresh auditor outputs, got {total}.", file=sys.stderr)
        return 1
    if yes != total:
        print(f"REFUSED: not all auditors clean ({yes}/{total} YES). " + "; ".join(bad), file=sys.stderr)
        return 1

    v = rs.load_verdicts(root)
    v[a.group] = {"verdict": "YES", "hash": h, "n_auditors": total, "ts": int(time.time())}
    rs.save_verdicts(root, v)
    print(f"RECORDED clean register verdict: {a.group} @ {h} ({total} fresh auditors, all YES).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
