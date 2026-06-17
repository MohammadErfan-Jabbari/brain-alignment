#!/usr/bin/env python3
"""
openreview_papers.py <venue> <year>

Pull the accepted paper list from OpenReview for venues covered by it
(ICLR all years; NeurIPS 2021+). Writes JSONL with abstracts + pdf_url to:
  data/papers/litsweep/<venue>/<year>.or_papers.jsonl

OpenReview API:
  api1 (older): https://api.openreview.net
  api2 (newer): https://api2.openreview.net  (ICLR 2023+; NeurIPS 2022+)

Venue-id patterns (from venues.yaml):
  ICLR.cc/{year}/Conference
  NeurIPS.cc/{year}/Conference

Decision filtering:
  - api2: notes?content.venueid=<venue_id> gives accepted only when the venue
    uses the venueid field (ICLR 2024+, NeurIPS 2023+).
  - Fallback: fetch all Submission notes, then filter by decision note or
    meta-review accept tag.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).parent
REPO_ROOT = HERE.parent.parent
VENUES_FILE = HERE / "venues.yaml"
BASE_DATA_DIR = REPO_ROOT / "data" / "papers" / "litsweep"

API1 = "https://api.openreview.net"
API2 = "https://api2.openreview.net"
REQUEST_DELAY = 0.5
MAX_RETRIES = 5
PAGE_SIZE = 1000


def load_venues():
    with open(VENUES_FILE) as f:
        return yaml.safe_load(f)["venues"]


def get_json(url, params=None, timeout=60):
    """GET JSON with retry + backoff on 429/5xx."""
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(
                url, params=params, timeout=timeout,
                headers={"User-Agent": "brain-alignment-litsweep/1.0 (mailto:mohammaderfanjabbari@gmail.com)"}
            )
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 15)) + 5
                print(f"  429 — sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if r.status_code in (500, 502, 503, 504):
                wait = 5 * (attempt + 1)
                print(f"  {r.status_code} — sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                raise
            print(f"  request error ({e}) — retry {attempt+1}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    return None


def paginate_api2(base_url, params, page_size=PAGE_SIZE):
    """Paginate api2 /notes endpoint, yielding all notes."""
    offset = 0
    total = None
    while True:
        p = dict(params)
        p["limit"] = page_size
        p["offset"] = offset
        time.sleep(REQUEST_DELAY)
        data = get_json(base_url, params=p)
        if data is None:
            break
        notes = data.get("notes", [])
        if total is None:
            total = data.get("count", 0)
            print(f"  api2 total={total}", file=sys.stderr)
        for n in notes:
            yield n
        offset += len(notes)
        if not notes or offset >= (total or 0):
            break


def paginate_api1(base_url, params, page_size=PAGE_SIZE):
    """Paginate api1 /notes endpoint, yielding all notes."""
    offset = 0
    total = None
    while True:
        p = dict(params)
        p["limit"] = page_size
        p["offset"] = offset
        time.sleep(REQUEST_DELAY)
        data = get_json(base_url, params=p)
        if data is None:
            break
        notes = data.get("notes", [])
        if total is None:
            total = data.get("count", 0)
            print(f"  api1 total={total}", file=sys.stderr)
        for n in notes:
            yield n
        offset += len(notes)
        if not notes or offset >= (total or 0):
            break


def extract_abstract(content):
    """Extract abstract text from OpenReview content dict."""
    for key in ("abstract", "Abstract", "ABSTRACT"):
        val = content.get(key)
        if isinstance(val, dict):
            val = val.get("value", "")
        if val:
            return str(val).strip()
    return ""


def extract_title(content):
    for key in ("title", "Title"):
        val = content.get(key)
        if isinstance(val, dict):
            val = val.get("value", "")
        if val:
            return str(val).strip()
    return ""


def extract_authors(content):
    for key in ("authors", "Authors"):
        val = content.get(key)
        if isinstance(val, dict):
            val = val.get("value", [])
        if val:
            return list(val) if isinstance(val, list) else [str(val)]
    return []


def pdf_url_from_note(note, api_base):
    """Build the PDF URL from an OpenReview note."""
    content = note.get("content", {})
    for key in ("pdf", "PDF"):
        val = content.get(key)
        if isinstance(val, dict):
            val = val.get("value", "")
        if val and isinstance(val, str) and val.startswith("/pdf/"):
            return f"https://openreview.net{val}"
    # Try note-level forum/id
    nid = note.get("id") or note.get("forum")
    if nid:
        return f"https://openreview.net/pdf?id={nid}"
    return None


def fetch_api2(venue_id, year):
    """
    Fetch accepted papers from api2.openreview.net.
    Strategy 1: content.venueid = venue_id (gives accepted only in newer venues).
    Strategy 2: invitation = venue_id/-/Submission, then filter accepted.
    """
    base = f"{API2}/notes"
    papers = []

    # Strategy 1: direct venueid filter
    print(f"  api2 strategy1: content.venueid={venue_id}", file=sys.stderr)
    params = {"content.venueid": venue_id}
    count = 0
    for note in paginate_api2(base, params):
        count += 1
        content = note.get("content", {})
        title = extract_title(content)
        if not title:
            continue
        papers.append({
            "or_id": note.get("id", ""),
            "forum": note.get("forum", ""),
            "title": title,
            "authors": extract_authors(content),
            "year": year,
            "abstract": extract_abstract(content),
            "pdf_url": pdf_url_from_note(note, API2),
            "venue": venue_id,
            "source": "openreview_api2_venueid",
        })

    if papers:
        print(f"  strategy1 found {len(papers)} accepted papers", file=sys.stderr)
        return papers

    # Strategy 2: fetch all submissions, filter by decision
    print(f"  api2 strategy2: invitation={venue_id}/-/Submission", file=sys.stderr)
    sub_params = {"invitation": f"{venue_id}/-/Submission"}
    submissions = {}
    for note in paginate_api2(base, sub_params):
        submissions[note.get("id", "")] = note

    print(f"  fetched {len(submissions)} submissions, fetching decisions …", file=sys.stderr)

    # Fetch decision notes
    time.sleep(REQUEST_DELAY)
    dec_params = {"invitation": f"{venue_id}/-/Decision"}
    decisions = {}
    for note in paginate_api2(base, dec_params):
        forum = note.get("forum", "")
        content = note.get("content", {})
        decision = content.get("decision", {})
        if isinstance(decision, dict):
            decision = decision.get("value", "")
        decisions[forum] = str(decision).lower()

    for sid, note in submissions.items():
        dec = decisions.get(sid, "")
        if "accept" not in dec:
            continue
        content = note.get("content", {})
        title = extract_title(content)
        if not title:
            continue
        papers.append({
            "or_id": sid,
            "forum": note.get("forum", sid),
            "title": title,
            "authors": extract_authors(content),
            "year": year,
            "abstract": extract_abstract(content),
            "pdf_url": pdf_url_from_note(note, API2),
            "venue": venue_id,
            "decision": dec,
            "source": "openreview_api2_decision",
        })

    print(f"  strategy2 found {len(papers)} accepted papers", file=sys.stderr)
    return papers


def fetch_api1(venue_id, year):
    """
    Fetch accepted papers from api.openreview.net (older venues).
    """
    base = f"{API1}/notes"
    papers = []

    # Strategy 1: invitation = venue_id/-/Blind_Submission or /-/Submission
    for inv_suffix in ("/-/Blind_Submission", "/-/Submission"):
        inv = f"{venue_id}{inv_suffix}"
        print(f"  api1 invitation={inv}", file=sys.stderr)
        sub_params = {"invitation": inv}
        submissions = {}
        for note in paginate_api1(base, sub_params):
            submissions[note.get("id", "")] = note
        if submissions:
            break

    if not submissions:
        print("  api1: no submissions found", file=sys.stderr)
        return papers

    print(f"  fetched {len(submissions)} submissions", file=sys.stderr)

    # Fetch decisions
    time.sleep(REQUEST_DELAY)
    decisions = {}
    for dec_inv in (f"{venue_id}/-/Decision",
                    f"{venue_id}/-/Paper_Decision",
                    f"{venue_id}/-/Acceptance_Decision"):
        dec_data = get_json(f"{API1}/notes", params={"invitation": dec_inv, "limit": 10})
        if dec_data and dec_data.get("notes"):
            for note in paginate_api1(f"{API1}/notes", {"invitation": dec_inv}):
                forum = note.get("forum", "")
                content = note.get("content", {})
                dec = content.get("decision", "")
                decisions[forum] = str(dec).lower()
            break

    accepted_count = sum(1 for d in decisions.values() if "accept" in d)
    print(f"  found {len(decisions)} decisions, {accepted_count} accepted", file=sys.stderr)

    for sid, note in submissions.items():
        dec = decisions.get(sid, "")
        # If no decisions found, include all (some OR venues don't have explicit decisions)
        if decisions and "accept" not in dec:
            continue
        content = note.get("content", {})
        title = extract_title(content)
        if not title:
            continue
        papers.append({
            "or_id": sid,
            "forum": note.get("forum", sid),
            "title": title,
            "authors": extract_authors(content),
            "year": year,
            "abstract": extract_abstract(content),
            "pdf_url": pdf_url_from_note(note, API1),
            "venue": venue_id,
            "decision": dec,
            "source": "openreview_api1",
        })

    print(f"  returning {len(papers)} accepted papers", file=sys.stderr)
    return papers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("venue", help="Venue key (e.g. iclr, neurips)")
    parser.add_argument("year", type=int, help="Year (e.g. 2024)")
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--api", choices=["api1", "api2", "auto"], default="auto")
    args = parser.parse_args()

    venues = load_venues()
    venue_key = args.venue.lower()
    if venue_key not in venues:
        print(f"Unknown venue '{venue_key}'. Known: {', '.join(venues)}", file=sys.stderr)
        sys.exit(1)

    venue_info = venues[venue_key]
    if venue_info.get("authoritative_source") not in ("openreview",):
        print(f"WARNING: {venue_key} is not listed as an OpenReview venue (source={venue_info.get('authoritative_source')})",
              file=sys.stderr)

    tmpl = venue_info.get("openreview_venue_id_template")
    if not tmpl:
        print(f"No OpenReview venue ID template for {venue_key}", file=sys.stderr)
        sys.exit(1)

    venue_id = tmpl.format(year=args.year)
    year = args.year

    # Decide API version
    api_ver = args.api
    if api_ver == "auto":
        configured = venue_info.get("openreview_api_version", 2)
        # api2 for ICLR 2023+, NeurIPS 2022+
        if venue_key == "iclr" and year >= 2023:
            api_ver = "api2"
        elif venue_key == "neurips" and year >= 2022:
            api_ver = "api2"
        elif configured == 2:
            api_ver = "api2"
        else:
            api_ver = "api1"

    print(f"OpenReview: venue_id={venue_id}, api={api_ver}", file=sys.stderr)

    if api_ver == "api2":
        papers = fetch_api2(venue_id, year)
        # If api2 returns nothing, fall back to api1
        if not papers:
            print("  api2 returned 0 — trying api1 fallback", file=sys.stderr)
            papers = fetch_api1(venue_id, year)
    else:
        papers = fetch_api1(venue_id, year)
        if not papers:
            print("  api1 returned 0 — trying api2 fallback", file=sys.stderr)
            papers = fetch_api2(venue_id, year)

    out_dir = args.out_dir or (BASE_DATA_DIR / venue_key)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{year}.or_papers.jsonl"

    with open(out_path, "w") as f:
        for p in papers:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"Wrote {len(papers)} papers to {out_path}")


if __name__ == "__main__":
    main()
