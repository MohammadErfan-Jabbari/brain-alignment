#!/usr/bin/env python3
"""
enrich_abstracts.py <jsonl>

Adds an `abstract` field to each row in the input JSONL via a chain:
  1. OpenAlex (DOI lookup then title search) — primary
  2. Crossref (DOI lookup) — fallback
  3. Semantic Scholar (DOI or title) — best-effort (may 429 without key)

Idempotent: skips rows that already have a non-empty `abstract`.
Writes enriched rows back to the same file (atomic via temp file).
Caches results in a sidecar <file>.abstract_cache.json to avoid re-fetching.

Reports hit-rate per source at the end.

Usage:
  uv run scripts/litsweep/enrich_abstracts.py data/papers/litsweep/neurips/2023.papers.jsonl
  uv run scripts/litsweep/enrich_abstracts.py data/papers/litsweep/neurips/2023.papers.jsonl --limit 20
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests

OPENALEX_BASE = "https://api.openalex.org"
CROSSREF_BASE = "https://api.crossref.org"
S2_BASE = "https://api.semanticscholar.org/graph/v1"
MAILTO = "mohammaderfanjabbari@gmail.com"
USER_AGENT = f"brain-alignment-litsweep/1.0 (mailto:{MAILTO})"

# Per-source delays (seconds between requests)
OA_DELAY = 1.2     # OpenAlex: generous to avoid 429 bursts
CR_DELAY = 0.5     # Crossref
S2_DELAY = 2.0     # Semantic Scholar: strict without API key

# On 429, wait this many seconds then skip (don't retry endlessly)
RATE_LIMIT_SKIP_WAIT = 5  # short wait, then mark source as unavailable for this run

# Track source availability within this run
_source_backoff_until = {}  # source_name -> timestamp


def _is_backed_off(source):
    t = _source_backoff_until.get(source, 0)
    return time.time() < t


def _backoff(source, seconds=60):
    _source_backoff_until[source] = time.time() + seconds
    print(f"    [{source}] rate-limited — skipping for {seconds}s", file=sys.stderr)


def get_json(url, params=None, timeout=20, source_name="unknown"):
    """GET JSON. Returns data dict or None. Updates backoff state on 429."""
    if _is_backed_off(source_name):
        return None
    try:
        r = requests.get(url, params=params, timeout=timeout,
                         headers={"User-Agent": USER_AGENT})
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 60))
            _backoff(source_name, wait + 10)
            return None
        if r.status_code == 404:
            return None
        if r.status_code in (500, 502, 503, 504):
            return None
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None


def reconstruct_abstract(inv_idx):
    """Reconstruct abstract text from OpenAlex abstract_inverted_index."""
    if not inv_idx:
        return ""
    max_pos = max(pos for positions in inv_idx.values() for pos in positions)
    words = [""] * (max_pos + 1)
    for word, positions in inv_idx.items():
        for pos in positions:
            words[pos] = word
    return " ".join(w for w in words if w).strip()


def openalex_by_doi(doi):
    if not doi or _is_backed_off("openalex"):
        return None
    time.sleep(OA_DELAY)
    encoded = urllib.parse.quote(doi, safe="")
    data = get_json(f"{OPENALEX_BASE}/works/doi:{encoded}",
                    params={"mailto": MAILTO}, source_name="openalex")
    if not data:
        return None
    return reconstruct_abstract(data.get("abstract_inverted_index")) or None


def openalex_by_title(title):
    if not title or _is_backed_off("openalex"):
        return None
    time.sleep(OA_DELAY)
    # Clean the title for search (remove special chars)
    clean = re.sub(r"[^\w\s]", " ", title[:120]).strip()
    params = {"filter": f"title.search:{clean}", "mailto": MAILTO, "per-page": 1}
    data = get_json(f"{OPENALEX_BASE}/works", params=params, source_name="openalex")
    if not data:
        return None
    results = data.get("results", [])
    if not results:
        return None
    return reconstruct_abstract(results[0].get("abstract_inverted_index")) or None


def crossref_by_doi(doi):
    if not doi or _is_backed_off("crossref"):
        return None
    time.sleep(CR_DELAY)
    encoded = urllib.parse.quote(doi, safe="")
    data = get_json(f"{CROSSREF_BASE}/works/{encoded}", source_name="crossref")
    if not data:
        return None
    abstract = data.get("message", {}).get("abstract", "")
    if abstract:
        abstract = re.sub(r"<[^>]+>", " ", abstract).strip()
        return abstract if abstract else None
    return None


def s2_by_doi(doi):
    if not doi or _is_backed_off("s2"):
        return None
    time.sleep(S2_DELAY)
    encoded = urllib.parse.quote(doi, safe="")
    data = get_json(f"{S2_BASE}/paper/DOI:{encoded}",
                    params={"fields": "abstract"}, source_name="s2")
    if not data:
        return None
    return data.get("abstract") or None


def s2_by_title(title):
    if not title or _is_backed_off("s2"):
        return None
    time.sleep(S2_DELAY)
    data = get_json(f"{S2_BASE}/paper/search",
                    params={"query": title[:100], "fields": "abstract", "limit": 1},
                    source_name="s2")
    if not data:
        return None
    papers = data.get("data", [])
    return papers[0].get("abstract") if papers else None


def enrich_one(paper, cache):
    """
    Try enrichment chain. Returns (abstract, source) or ("", None).
    Uses cache keyed by doi or title prefix.
    """
    if paper.get("abstract", "").strip():
        return paper["abstract"], "existing"

    cache_key = (paper.get("doi") or paper.get("title", "")[:80])
    if cache_key in cache:
        entry = cache[cache_key]
        return entry.get("abstract", ""), entry.get("source")

    doi = paper.get("doi")
    title = paper.get("title", "")

    # Chain: OA-doi → OA-title → Crossref-doi → S2-doi → S2-title
    checks = [
        ("openalex_doi", lambda: openalex_by_doi(doi)),
        ("openalex_title", lambda: openalex_by_title(title)),
        ("crossref", lambda: crossref_by_doi(doi)),
        ("s2_doi", lambda: s2_by_doi(doi)),
        ("s2_title", lambda: s2_by_title(title)),
    ]

    for source_name, fn in checks:
        # Skip DOI-only steps when there is no DOI
        if "doi" in source_name and not doi:
            continue
        abstract = fn()
        if abstract and abstract.strip():
            cache[cache_key] = {"abstract": abstract, "source": source_name}
            return abstract, source_name

    cache[cache_key] = {"abstract": "", "source": None}
    return "", None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="Input JSONL file")
    parser.add_argument("--limit", type=int, default=None,
                        help="Process only first N rows (for testing)")
    args = parser.parse_args()

    if not args.jsonl.exists():
        print(f"File not found: {args.jsonl}", file=sys.stderr)
        sys.exit(1)

    cache_path = args.jsonl.with_suffix(".abstract_cache.json")
    cache = {}
    if cache_path.exists():
        with open(cache_path) as f:
            try:
                cache = json.load(f)
            except json.JSONDecodeError:
                cache = {}
        print(f"Loaded {len(cache)} cached entries", file=sys.stderr)

    papers = []
    with open(args.jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                papers.append(json.loads(line))

    if args.limit:
        papers = papers[: args.limit]

    print(f"Enriching {len(papers)} papers …", file=sys.stderr)

    stats = {}
    enriched = []

    for i, paper in enumerate(papers):
        if (i + 1) % 5 == 0:
            print(f"  {i+1}/{len(papers)} …", file=sys.stderr)
        abstract, source = enrich_one(paper, cache)
        paper = dict(paper)
        paper["abstract"] = abstract
        paper["abstract_source"] = source
        enriched.append(paper)
        key = source if source else "miss"
        stats[key] = stats.get(key, 0) + 1

        if (i + 1) % 10 == 0:
            with open(cache_path, "w") as f:
                json.dump(cache, f)

    with open(cache_path, "w") as f:
        json.dump(cache, f)

    tmp_path = args.jsonl.with_suffix(".tmp")
    with open(tmp_path, "w") as f:
        for p in enriched:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    tmp_path.rename(args.jsonl)

    total = len(enriched)
    print(f"\nEnrichment report ({total} papers):")
    for src in ("existing", "openalex_doi", "openalex_title", "crossref", "s2_doi", "s2_title"):
        n = stats.get(src, 0)
        if n:
            print(f"  {src:<20}: {n:>4} ({100*n/total:.1f}%)")
    miss = stats.get("miss", 0)
    hit = total - miss
    print(f"  {'miss':<20}: {miss:>4} ({100*miss/total:.1f}%)")
    print(f"  TOTAL HIT RATE       : {hit:>4}/{total} ({100*hit/total:.1f}%)")
    print(f"Written to {args.jsonl}")


if __name__ == "__main__":
    main()
