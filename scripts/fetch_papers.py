#!/usr/bin/env python3
"""Fetch the brain-as-training-signal reading list as PDFs, VERIFYING each
arXiv title before trusting the id (the ids came from a web-search agent, so a
wrong/hallucinated id must be caught, not silently downloaded).

For each row in scripts/papers.tsv: hit the arXiv abstract page, extract the
real title, check the expected substring appears (case-insensitive), and only
then download the PDF into data/papers/. Logs a verdict per paper. Non-arXiv
sources (OpenReview / bioRxiv / journals) are listed at the end for manual
WebFetch in the analysis session.
"""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TSV = ROOT / "scripts" / "papers.tsv"
OUT = ROOT / "data" / "papers"
UA = {"User-Agent": "Mozilla/5.0 (research paper fetch)"}

# Non-arXiv items to fetch by hand in the analysis session (no stable PDF URL).
MANUAL = [
    ("Bilgin, St-Laurent, Bellec, Wehbe — Brain-Informed LM Training (ICLR 2026)",
     "https://openreview.net/forum?id=07S1CPoQYP"),
    ("Freteault et al. — Auditory ANN alignment (Imaging Neuroscience 2025)",
     "https://direct.mit.edu/imag/article/doi/10.1162/imag_a_00525/128455/"),
]


def fetch(url: str, binary: bool = False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if binary else r.read().decode("utf-8", "ignore")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [l.split("\t") for l in TSV.read_text().splitlines()[1:] if l.strip()]
    ok, bad = [], []
    for aid, expect, group, why in rows:
        aid, expect = aid.strip(), expect.strip().lower()
        try:
            html = fetch(f"https://arxiv.org/abs/{aid}")
            m = re.search(r'<title>\s*(.*?)\s*</title>', html, re.S)
            title = re.sub(r'\s+', ' ', m.group(1)) if m else "(no title)"
            title = title.replace("[", "").split("] ", 1)[-1] if "] " in title else title
            verified = expect in title.lower()
            status = "OK " if verified else "MISMATCH"
            print(f"[{status}] {aid}  ({group})  ->  {title}")
            if not verified:
                print(f"          expected substring: '{expect}'  -- DO NOT TRUST, verify in analysis session")
                bad.append((aid, expect, title))
                continue
            pdf = fetch(f"https://arxiv.org/pdf/{aid}", binary=True)
            if pdf[:4] != b"%PDF":
                print(f"          downloaded bytes are not a PDF; skipping")
                bad.append((aid, expect, title)); continue
            dest = OUT / f"{aid}.pdf"
            dest.write_bytes(pdf)
            print(f"          saved {dest.relative_to(ROOT)}  ({len(pdf)//1024} KB)")
            ok.append((aid, title))
        except Exception as e:
            print(f"[ERROR ] {aid}  ({group})  ->  {e}")
            bad.append((aid, expect, str(e)))
    print(f"\n=== {len(ok)} verified+downloaded, {len(bad)} need manual check ===")
    print("\nManual (non-arXiv, fetch via WebFetch in the analysis session):")
    for name, url in MANUAL:
        print(f"  - {name}\n      {url}")
    if bad:
        print("\nFlagged arXiv ids (id, expected, got/error):")
        for b in bad:
            print(f"  - {b[0]}: expected '{b[1]}' | got '{b[2][:80]}'")


if __name__ == "__main__":
    sys.exit(main())
