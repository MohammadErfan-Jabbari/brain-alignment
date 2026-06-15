"""Public-cut gate: a claim's hedge must not strengthen under compression.

"Compression preserves truth" means the claims and their hedge levels survive,
not only the numbers. A public cut can keep every digit and still quietly upgrade
a "suggests" to a "demonstrates", which is the over-claim the whole thesis guards
against. This check compares, per evidence key, the strongest hedge verb attached
to that key in the extended source versus the public cut.

- A hedge UPGRADE (extended "suggests" -> public "demonstrates") is a hard fail:
  the evidence did not change, so the verb may not.
- A DROPPED key (cited in the extended, absent from the public) is reported as an
  advisory note, not a failure, because dropping a claim is often legitimate
  compression. Confirm each drop was intentional.

Heuristic by design: it pairs claims by their \\evd key and reads the hedge verb
on the same source line. A fuller version would mark claims with a dedicated
macro; this catches the common, high-damage case (a silent verb upgrade) now.

Usage:
    python check_claim_survival.py PUBLIC_PATH --extended-root EXTENDED_DIR

Exit code: 0 if no hedge was upgraded, 1 on any upgrade.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EVD = re.compile(r"\\evd\{([ELel]\d+)\}")
STRENGTH = {
    "strong": ["demonstrate", "establish", "show", "confirm", "prove"],
    "moderate": ["suggest", "indicate", "appear", "consistent with"],
    "weak": ["may", "might", "could", "possibly", "would imply", "under the assumption"],
}
RANK = {"weak": 1, "moderate": 2, "strong": 3, None: 0}


def line_strength(text: str):
    low = text.lower()
    best = None
    for level, words in STRENGTH.items():
        for w in words:
            if re.search(rf"\b{re.escape(w)}", low):
                if RANK[level] > RANK[best]:
                    best = level
    return best


def key_strengths(root: Path, single: Path | None = None) -> dict:
    files = [single] if single else sorted(root.rglob("*.tex"))
    out = {}
    for f in files:
        for lineno, raw in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for key in EVD.findall(raw):
                s = line_strength(raw)
                if RANK[s] > RANK[out.get(key)]:
                    out[key] = s
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check claim hedge levels survive extended->public compression.")
    ap.add_argument("public", type=Path)
    ap.add_argument("--extended-root", type=Path, required=True)
    args = ap.parse_args(argv)

    ext = key_strengths(args.extended_root)
    pub = key_strengths(None, args.public) if args.public.is_file() else key_strengths(args.public)

    upgrades, drops = [], []
    for key, pub_s in pub.items():
        ext_s = ext.get(key)
        if RANK[pub_s] > RANK[ext_s]:
            upgrades.append((key, ext_s, pub_s))
    for key in ext:
        if key not in pub:
            drops.append(key)

    if drops:
        print(f"note: {len(drops)} claim(s) cited in the extended are absent from the public cut "
              f"(confirm each was intentionally compressed): {', '.join(sorted(drops))}")
    if upgrades:
        print(f"\n{len(upgrades)} hedge UPGRADE(S) (over-claim under compression):")
        for key, e, p in sorted(upgrades):
            print(f"  {key}: extended hedge '{e}' -> public hedge '{p}'  (evidence unchanged)")
        print("\ncheck_claim_survival: a public cut may not strengthen a claim's hedge.", file=sys.stderr)
        return 1
    print("check_claim_survival: no hedge upgraded under compression.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
