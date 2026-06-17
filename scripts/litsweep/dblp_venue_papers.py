#!/usr/bin/env python3
"""
dblp_venue_papers.py <venue> <year>

Enumerate the COMPLETE paper list for a venue/year from DBLP using the
venue TOC XML stream. Writes JSONL to:
  data/papers/litsweep/<venue>/<year>.papers.jsonl

Uses the DBLP TOC XML (e.g. https://dblp.org/db/conf/nips/neurips2023.bht)
instead of the search API so the result is complete — not capped at 1000.

Rate-limit: 1 req/sec; backs off on 429.
"""
import argparse
import json
import os
import sys
import time
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).parent
REPO_ROOT = HERE.parent.parent
VENUES_FILE = HERE / "venues.yaml"
BASE_DATA_DIR = REPO_ROOT / "data" / "papers" / "litsweep"

DBLP_BASE = "https://dblp.org"
REQUEST_DELAY = 1.1  # seconds between requests
MAX_RETRIES = 5


def load_venues():
    with open(VENUES_FILE) as f:
        return yaml.safe_load(f)["venues"]


def get(url, params=None, stream=False, timeout=30):
    """GET with retry + backoff on 429/5xx."""
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, stream=stream,
                             timeout=timeout,
                             headers={"User-Agent": "brain-alignment-litsweep/1.0 (mailto:mohammaderfanjabbari@gmail.com)"})
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 10)) + 5
                print(f"  429 — sleeping {wait}s …", file=sys.stderr)
                time.sleep(wait)
                continue
            if r.status_code in (500, 502, 503, 504):
                wait = 5 * (attempt + 1)
                print(f"  {r.status_code} — sleeping {wait}s …", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                raise
            print(f"  request error ({e}) — retry {attempt+1}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    return None


def venue_toc_url(venue_info, year):
    """
    Build the DBLP TOC XML URL for a venue-year.
    DBLP uses <prefix><year>.xml for the machine-readable dump,
    but the HTML path is more reliably discovered.

    Strategy: try the XML TOC directly; the naming convention differs per venue.
    For nips/neurips: neurips<year>.xml (2019+), nips<year>.xml (earlier)
    For others: <key-last-segment><year>.xml
    """
    prefix = venue_info["dblp_toc_prefix"]  # e.g. https://dblp.org/db/conf/nips/neurips
    year = int(year)

    # NeurIPS special case: pre-2019 uses "nips", 2019+ uses "neurips"
    if "conf/nips" in prefix and "neurips" in prefix and year < 2019:
        prefix = prefix.replace("neurips", "nips")

    return f"{prefix}{year}.xml"


def parse_dblp_xml(xml_text, venue_key, year):
    """Parse DBLP TOC XML and return list of paper dicts."""
    papers = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"  XML parse error: {e}", file=sys.stderr)
        return papers

    # DBLP XML has <r> elements each containing one publication type element
    pub_types = {"inproceedings", "article", "incollection"}
    for r_elem in root.iter("r"):
        for pub_elem in r_elem:
            if pub_elem.tag not in pub_types:
                continue

            def text(tag):
                el = pub_elem.find(tag)
                return el.text.strip() if el is not None and el.text else None

            def all_text(tag):
                return [el.text.strip() for el in pub_elem.findall(tag)
                        if el.text]

            dblp_key = pub_elem.get("key", "")
            title = text("title")
            if not title:
                continue

            authors = all_text("author")
            year_found = text("year")
            doi = text("doi")

            # ee can be multiple (DOI link, arXiv, etc.)
            ee_vals = all_text("ee")
            ee = ee_vals[0] if ee_vals else None

            # Skip non-papers (workshops, front matter)
            if not authors:
                continue

            papers.append({
                "dblp_key": dblp_key,
                "title": title,
                "authors": authors,
                "year": int(year_found) if year_found else year,
                "doi": doi,
                "ee": ee,
                "ee_all": ee_vals,
                "venue": venue_key,
            })

    return papers


def fetch_dblp_toc(venue_key, year, venue_info):
    """Fetch DBLP TOC XML and return parsed papers."""
    toc_url = venue_toc_url(venue_info, year)
    print(f"Fetching DBLP TOC: {toc_url}", file=sys.stderr)
    time.sleep(REQUEST_DELAY)
    r = get(toc_url)
    if r is None:
        print("  Failed to fetch TOC", file=sys.stderr)
        return []
    papers = parse_dblp_xml(r.text, venue_key, int(year))
    print(f"  Parsed {len(papers)} entries from TOC", file=sys.stderr)
    return papers


def fetch_dblp_search_paginated(venue_key, year, venue_info):
    """
    Fallback: use DBLP search API with toc: filter + pagination.
    Handles up to ~10000 results via f/h params.
    """
    # Build toc: filter from the prefix
    # e.g. toc:conf/nips/neurips2023.bht:
    prefix = venue_info["dblp_toc_prefix"]
    if "conf/nips" in prefix and "neurips" in prefix and int(year) < 2019:
        prefix = prefix.replace("neurips", "nips")
    toc_filter = f"toc:{prefix.split('/db/')[-1]}{year}.bht:"

    url = "https://dblp.org/search/publ/api"
    papers = []
    page_size = 1000
    offset = 0

    while True:
        params = {
            "q": toc_filter,
            "format": "json",
            "h": page_size,
            "f": offset,
        }
        print(f"  Search API offset={offset} …", file=sys.stderr)
        time.sleep(REQUEST_DELAY)
        r = get(url, params=params)
        if r is None:
            break
        data = r.json()
        hits = data.get("result", {}).get("hits", {})
        total = int(hits.get("@total", 0))
        hit_list = hits.get("hit", [])
        if not hit_list:
            break

        for h in hit_list:
            info = h.get("info", {})
            authors_raw = info.get("authors", {}).get("author", [])
            if isinstance(authors_raw, dict):
                authors_raw = [authors_raw]
            authors = [a.get("text", "") if isinstance(a, dict) else str(a)
                       for a in authors_raw]
            title = info.get("title", "").rstrip(".")
            if not title or not authors:
                continue
            papers.append({
                "dblp_key": info.get("key", ""),
                "title": title,
                "authors": authors,
                "year": int(info.get("year", year)),
                "doi": info.get("doi"),
                "ee": info.get("ee"),
                "ee_all": [info.get("ee")] if info.get("ee") else [],
                "venue": venue_key,
            })

        offset += len(hit_list)
        if offset >= total or len(hit_list) < page_size:
            break

    print(f"  Search API returned {len(papers)} entries total", file=sys.stderr)
    return papers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("venue", help="Venue key (e.g. neurips, icml, cvpr)")
    parser.add_argument("year", type=int, help="Year (e.g. 2023)")
    parser.add_argument("--method", choices=["toc", "search", "auto"],
                        default="auto",
                        help="Fetch method: toc (XML), search (API), auto (try toc first)")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Override output directory")
    args = parser.parse_args()

    venues = load_venues()
    venue_key = args.venue.lower()
    if venue_key not in venues:
        print(f"Unknown venue '{venue_key}'. Known: {', '.join(venues)}", file=sys.stderr)
        sys.exit(1)

    venue_info = venues[venue_key]
    year = args.year

    out_dir = args.out_dir or (BASE_DATA_DIR / venue_key)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{year}.papers.jsonl"

    papers = []
    if args.method in ("toc", "auto"):
        papers = fetch_dblp_toc(venue_key, year, venue_info)
        if not papers and args.method == "auto":
            print("  TOC returned 0 — falling back to search API", file=sys.stderr)
            papers = fetch_dblp_search_paginated(venue_key, year, venue_info)
    else:
        papers = fetch_dblp_search_paginated(venue_key, year, venue_info)

    if not papers:
        print(f"WARNING: no papers found for {venue_key} {year}", file=sys.stderr)

    with open(out_path, "w") as f:
        for p in papers:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"Wrote {len(papers)} papers to {out_path}")


if __name__ == "__main__":
    main()
