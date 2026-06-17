#!/usr/bin/env python3
"""
fetch_pdf.py <jsonl> [--limit N]

Resolves and downloads PDFs for papers in a JSONL file.

Resolution chain per paper:
  1. pdf_url field (from OpenReview)
  2. arXiv — search by title via export.arxiv.org API
  3. OpenAlex OA URL (oa_url from /works endpoint)
  4. ee/ee_all fields (may be direct PDF links)

Downloads to: data/papers/litsweep/<venue>/<year>/pdf/<sanitized_title>.pdf
Records download status in a sidecar <file>.pdf_status.json.

Usage:
  uv run scripts/litsweep/fetch_pdf.py data/papers/litsweep/iclr/2024.or_papers.jsonl --limit 2
  uv run scripts/litsweep/fetch_pdf.py data/papers/litsweep/neurips/2023.papers.jsonl --limit 5
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

USER_AGENT = "brain-alignment-litsweep/1.0 (mailto:mohammaderfanjabbari@gmail.com)"
ARXIV_API = "http://export.arxiv.org/api/query"
OPENALEX_BASE = "https://api.openalex.org"
MAILTO = "mohammaderfanjabbari@gmail.com"
REQUEST_DELAY = 1.1
MAX_RETRIES = 4
CHUNK_SIZE = 8192  # bytes


def sanitize_filename(title, max_len=80):
    """Make a filesystem-safe filename from a title."""
    s = re.sub(r"[^\w\s-]", "", title.lower())
    s = re.sub(r"[\s_-]+", "_", s).strip("_")
    return s[:max_len]


def get(url, params=None, stream=False, timeout=60):
    """GET with retry + backoff."""
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, stream=stream, timeout=timeout,
                             headers={"User-Agent": USER_AGENT})
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 15)) + 5
                print(f"    429 — sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if r.status_code == 404:
                return None
            if r.status_code in (500, 502, 503, 504):
                time.sleep(5 * (attempt + 1))
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                return None
            time.sleep(3 * (attempt + 1))
    return None


def arxiv_pdf_url_by_title(title):
    """
    Search arXiv by title, return PDF URL of the best match.
    Returns (pdf_url, arxiv_id) or (None, None).
    """
    params = {
        "search_query": f"ti:{title[:120]}",
        "max_results": 3,
        "sortBy": "relevance",
    }
    time.sleep(REQUEST_DELAY)
    r = get(ARXIV_API, params=params)
    if not r:
        return None, None
    try:
        root = ET.fromstring(r.text)
    except ET.ParseError:
        return None, None

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)
    if not entries:
        return None, None

    entry = entries[0]
    # Get arxiv ID
    arxiv_id = entry.find("atom:id", ns)
    arxiv_id = arxiv_id.text.split("/abs/")[-1] if arxiv_id is not None else None

    # Find PDF link
    for link in entry.findall("atom:link", ns):
        if link.get("title") == "pdf":
            return link.get("href"), arxiv_id

    # Fallback: construct from ID
    if arxiv_id:
        return f"https://arxiv.org/pdf/{arxiv_id}", arxiv_id

    return None, None


def openalex_oa_url_by_doi(doi):
    """Get open access PDF URL from OpenAlex."""
    if not doi:
        return None
    encoded = urllib.parse.quote(doi, safe="")
    time.sleep(0.15)
    r = get(f"{OPENALEX_BASE}/works/doi:{encoded}",
            params={"mailto": MAILTO, "select": "open_access,id"})
    if not r:
        return None
    data = r.json()
    oa = data.get("open_access", {})
    return oa.get("oa_url")


def download_pdf(url, dest_path):
    """
    Download a PDF from url to dest_path.
    Returns (success, file_size_bytes, actual_url_used).
    """
    # Follow redirects automatically
    time.sleep(REQUEST_DELAY)
    r = get(url, stream=True)
    if not r:
        return False, 0, url

    content_type = r.headers.get("content-type", "")
    if "pdf" not in content_type and "octet" not in content_type:
        # Check if it's a redirect to PDF or HTML with PDF link
        if "html" in content_type:
            return False, 0, url

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                size += len(chunk)

    # Sanity check: real PDFs start with %PDF
    if size > 0:
        with open(dest_path, "rb") as f:
            header = f.read(4)
        if header != b"%PDF":
            dest_path.unlink(missing_ok=True)
            return False, 0, url

    return size > 0, size, str(r.url)


def resolve_and_download(paper, pdf_dir):
    """
    Try each resolution strategy, download to pdf_dir.
    Returns dict with keys: resolved, source, path, size_bytes, url.
    """
    title = paper.get("title", "untitled")
    fname = sanitize_filename(title) + ".pdf"
    dest = pdf_dir / fname

    if dest.exists() and dest.stat().st_size > 1000:
        return {
            "resolved": True, "source": "cached",
            "path": str(dest), "size_bytes": dest.stat().st_size, "url": ""
        }

    # Strategy 1: pdf_url from OpenReview
    pdf_url = paper.get("pdf_url")
    if pdf_url:
        print(f"  [1] trying pdf_url: {pdf_url[:80]}", file=sys.stderr)
        ok, size, actual = download_pdf(pdf_url, dest)
        if ok:
            return {"resolved": True, "source": "openreview_pdf_url",
                    "path": str(dest), "size_bytes": size, "url": actual}

    # Strategy 2: arXiv by title
    print(f"  [2] trying arXiv title search …", file=sys.stderr)
    arxiv_url, arxiv_id = arxiv_pdf_url_by_title(title)
    if arxiv_url:
        print(f"    found arxiv: {arxiv_url}", file=sys.stderr)
        ok, size, actual = download_pdf(arxiv_url, dest)
        if ok:
            return {"resolved": True, "source": f"arxiv:{arxiv_id}",
                    "path": str(dest), "size_bytes": size, "url": actual}

    # Strategy 3: OpenAlex OA URL
    doi = paper.get("doi")
    if doi:
        print(f"  [3] trying OpenAlex OA URL for doi={doi}", file=sys.stderr)
        oa_url = openalex_oa_url_by_doi(doi)
        if oa_url:
            print(f"    oa_url: {oa_url[:80]}", file=sys.stderr)
            ok, size, actual = download_pdf(oa_url, dest)
            if ok:
                return {"resolved": True, "source": "openalex_oa",
                        "path": str(dest), "size_bytes": size, "url": actual}

    # Strategy 4: ee_all links (try each)
    for ee in paper.get("ee_all", []) or ([paper["ee"]] if paper.get("ee") else []):
        if not ee:
            continue
        if ee.endswith(".pdf") or "arxiv.org/pdf" in ee:
            print(f"  [4] trying ee link: {ee[:80]}", file=sys.stderr)
            ok, size, actual = download_pdf(ee, dest)
            if ok:
                return {"resolved": True, "source": "ee_link",
                        "path": str(dest), "size_bytes": size, "url": actual}

    return {"resolved": False, "source": None, "path": None, "size_bytes": 0, "url": ""}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="Input JSONL file")
    parser.add_argument("--limit", type=int, default=None,
                        help="Download at most N PDFs")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Override PDF output directory")
    args = parser.parse_args()

    if not args.jsonl.exists():
        print(f"File not found: {args.jsonl}", file=sys.stderr)
        sys.exit(1)

    papers = []
    with open(args.jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                papers.append(json.loads(line))

    if args.limit:
        papers = papers[: args.limit]

    # Determine PDF dir
    if args.out_dir:
        pdf_dir = args.out_dir
    else:
        # Infer from jsonl path: data/papers/litsweep/<venue>/<year>.*.jsonl
        # → data/papers/litsweep/<venue>/<year>/pdf/
        year_match = re.search(r"(\d{4})\.", args.jsonl.name)
        year = year_match.group(1) if year_match else "unknown"
        pdf_dir = args.jsonl.parent / year / "pdf"

    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Load status cache
    status_path = args.jsonl.with_suffix(".pdf_status.json")
    status = {}
    if status_path.exists():
        with open(status_path) as f:
            status = json.load(f)

    results = []
    for i, paper in enumerate(papers):
        title = paper.get("title", "")
        print(f"\n[{i+1}/{len(papers)}] {title[:70]}", file=sys.stderr)
        result = resolve_and_download(paper, pdf_dir)
        result["title"] = title
        results.append(result)
        status[title[:100]] = result

        # Save status
        with open(status_path, "w") as f:
            json.dump(status, f, indent=2)

    # Summary
    ok = [r for r in results if r["resolved"]]
    print(f"\nPDF download summary: {len(ok)}/{len(results)} succeeded")
    for r in results:
        size_kb = r["size_bytes"] / 1024 if r["size_bytes"] else 0
        status_str = f"OK ({size_kb:.0f} KB) [{r['source']}]" if r["resolved"] else "FAIL"
        print(f"  {r['title'][:60]:<62} {status_str}")
        if r["resolved"]:
            print(f"    → {r['path']}")


if __name__ == "__main__":
    main()
