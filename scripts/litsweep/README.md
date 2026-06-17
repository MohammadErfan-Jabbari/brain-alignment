# litsweep — Literature Sweep Pipeline

Enumerate, enrich, and download papers from top AI/ML venues for downstream analysis.

## Architecture

```
DBLP XML TOC  ──►  dblp_venue_papers.py   ──►  <venue>/<year>.papers.jsonl
OpenReview    ──►  openreview_papers.py   ──►  <venue>/<year>.or_papers.jsonl
                                                       │
                                        enrich_abstracts.py  (adds abstract field)
                                                       │
                                         fetch_pdf.py  (resolves + downloads PDFs)
```

## Data layout

```
data/papers/litsweep/
  <venue>/
    <year>.papers.jsonl       — DBLP paper list (no abstracts)
    <year>.or_papers.jsonl    — OpenReview paper list (with abstracts + pdf_url)
    <year>.abstract_cache.json — enrichment cache (keyed by doi or title prefix)
    <year>/pdf/               — downloaded PDFs
```

All data files are gitignored (`data/` is excluded).

## Tools

### venues.yaml

Registry of the 10 covered venues with their DBLP keys and OpenReview venue-id patterns.
Edit this to add venues or correct keys.

### dblp_venue_papers.py

Enumerate the complete paper list for a DBLP-covered venue/year. Uses the DBLP TOC XML
stream (not the search API) so the count is not capped at 1000.

```bash
uv run scripts/litsweep/dblp_venue_papers.py neurips 2023
uv run scripts/litsweep/dblp_venue_papers.py icml 2023
uv run scripts/litsweep/dblp_venue_papers.py cvpr 2023
# Override output dir:
uv run scripts/litsweep/dblp_venue_papers.py neurips 2023 --out-dir /tmp/test/
```

Output schema per row:
```json
{"dblp_key": "conf/nips/...", "title": "...", "authors": [...],
 "year": 2023, "doi": null, "ee": "http://...", "ee_all": [...], "venue": "neurips"}
```

**Coverage notes:**
- DBLP NeurIPS: `doi` is null for 2022+; `ee` points to papers.nips.cc.
- DBLP ICML: `doi` usually present (Springer or PMLR).
- TOC XML naming: `neurips<year>` for 2019+; `nips<year>` for earlier.

### openreview_papers.py

Pull accepted papers with abstracts + PDF URLs from OpenReview. Covers:
- ICLR: all years (2013+)
- NeurIPS: 2021+

```bash
uv run scripts/litsweep/openreview_papers.py iclr 2024
uv run scripts/litsweep/openreview_papers.py neurips 2023
uv run scripts/litsweep/openreview_papers.py iclr 2023 --api api1   # force api1
```

Uses api2.openreview.net for ICLR 2023+/NeurIPS 2022+; api1 for older.

Output schema per row:
```json
{"or_id": "...", "forum": "...", "title": "...", "authors": [...],
 "year": 2024, "abstract": "...", "pdf_url": "https://openreview.net/pdf?id=...",
 "venue": "ICLR.cc/2024/Conference", "source": "openreview_api2_venueid"}
```

### enrich_abstracts.py

Add `abstract` to DBLP rows via: OpenAlex title search → Crossref DOI → Semantic Scholar.

```bash
uv run scripts/litsweep/enrich_abstracts.py data/papers/litsweep/neurips/2023.papers.jsonl
uv run scripts/litsweep/enrich_abstracts.py data/papers/litsweep/neurips/2023.papers.jsonl --limit 100
```

- Idempotent: skips rows with an existing `abstract` field.
- Caches results in `<file>.abstract_cache.json` — safe to re-run.
- Writes enriched rows back in-place (atomic rename).
- Rate-limit aware: backs off per-source when it receives a 429.

**Hit rates observed:**
- NeurIPS 2023 (no DOIs in DBLP): ~50% via OpenAlex title search.
- Venues with DOIs (ICML, CVPR, AAAI): expect 70-90% via OpenAlex DOI.

Semantic Scholar adds ~5-15% additional coverage but has strict limits without an API key.
Register at semanticscholar.org/product/api and set `S2_API_KEY` env var to lift the limit.

### fetch_pdf.py

Resolve and download PDFs. Resolution order:
1. `pdf_url` field (OpenReview papers have this directly)
2. arXiv — title search via `export.arxiv.org/api/query`
3. OpenAlex OA URL
4. `ee`/`ee_all` links from DBLP

```bash
# Download 2 PDFs for testing:
uv run scripts/litsweep/fetch_pdf.py data/papers/litsweep/iclr/2024.or_papers.jsonl --limit 2
uv run scripts/litsweep/fetch_pdf.py data/papers/litsweep/neurips/2023.papers.jsonl --limit 5

# Override output dir:
uv run scripts/litsweep/fetch_pdf.py data/papers/litsweep/neurips/2023.papers.jsonl --out-dir /tmp/pdfs/ --limit 10
```

PDFs land in `data/papers/litsweep/<venue>/<year>/pdf/<title>.pdf`.
Status is cached in `<file>.pdf_status.json`.

## Full sweep commands

To enumerate + enrich a full venue-year, chain these:

```bash
# 1. Get paper list
uv run scripts/litsweep/dblp_venue_papers.py neurips 2023

# 2. Enrich abstracts (slow for large files — run in background)
uv run scripts/litsweep/enrich_abstracts.py data/papers/litsweep/neurips/2023.papers.jsonl &

# 3. For ICLR/NeurIPS 2021+: use OpenReview instead (already has abstracts)
uv run scripts/litsweep/openreview_papers.py iclr 2024

# 4. Fetch PDFs for a subset
uv run scripts/litsweep/fetch_pdf.py data/papers/litsweep/iclr/2024.or_papers.jsonl --limit 50
```

## Venues and authoritative sources

| Venue   | Authoritative source | Notes |
|---------|---------------------|-------|
| ICLR    | OpenReview          | All years; abstracts + PDFs included |
| NeurIPS | OpenReview (2021+)  | DBLP fallback for ≤2020 |
| ICML    | DBLP                | Abstract enrichment needed |
| CVPR    | DBLP                | Abstract enrichment needed |
| ACL     | ACL Anthology       | Abstracts in anthology |
| EMNLP   | ACL Anthology       | Abstracts in anthology |
| NAACL   | ACL Anthology       | Not held every year |
| AAAI    | DBLP                | Abstract enrichment needed |
| IJCAI   | DBLP                | Abstract enrichment needed |
| KDD     | DBLP                | Abstract enrichment needed |

## Known coverage gaps

- **NeurIPS 2023 DBLP**: no DOI fields — `ee` points to papers.nips.cc. OpenAlex title
  search covers ~50%; the rest are findable via arXiv or the NeurIPS proceedings directly.
- **Semantic Scholar**: rate-limited without an API key (1 req/~2s unauthenticated).
  Set `S2_API_KEY` env var if you have one.
- **CVPR pre-2013**: DBLP coverage thin.
- **NAACL**: Not annual — check `venues.yaml` and DBLP TOC before assuming a year exists.
- **ACL Anthology scraper**: not yet implemented; use `acl_anthology_url` from `venues.yaml`
  to build a scraper against `https://aclanthology.org/events/<venue>-<year>/`.
