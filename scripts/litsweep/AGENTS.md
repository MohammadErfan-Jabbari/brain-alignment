---
title: "Literature Sweep Agent Guidance"
tags: [reference, literature]
aliases: [litsweep-agents]
---

# Literature Sweep Agent Guidance

This folder contains scripts to enumerate, enrich, and download papers from top AI/ML venues for downstream analysis.

## Rules

- Do not create a `README.md` here. Folder guidance belongs in `AGENTS.md`.
- Run scripts with `uv run`.
- All sweep data belongs under gitignored `data/papers/litsweep/`.
- Treat venue coverage as source-specific; do not assume abstracts/PDFs exist for every venue-year.
- Respect rate limits. Set `S2_API_KEY` only in the environment, never in tracked files.

## Pipeline

```text
DBLP XML TOC -> dblp_venue_papers.py -> <venue>/<year>.papers.jsonl
OpenReview   -> openreview_papers.py   -> <venue>/<year>.or_papers.jsonl
                                      -> enrich_abstracts.py
                                      -> fetch_pdf.py
```

## Data Layout

```text
data/papers/litsweep/
  <venue>/
    <year>.papers.jsonl
    <year>.or_papers.jsonl
    <year>.abstract_cache.json
    <year>/pdf/
```

## Tools

| Tool | Use |
|---|---|
| `venues.yaml` | Registry of covered venues, DBLP keys, and OpenReview patterns. |
| `dblp_venue_papers.py` | Enumerate complete DBLP-covered venue/year paper lists via TOC XML. |
| `openreview_papers.py` | Pull accepted papers with abstracts and PDF URLs from OpenReview. |
| `enrich_abstracts.py` | Add abstracts to DBLP rows via OpenAlex, Crossref, and Semantic Scholar. |
| `fetch_pdf.py` | Resolve/download PDFs using direct URLs, arXiv, OpenAlex OA URLs, then DBLP links. |

## Commands

```bash
uv run scripts/litsweep/dblp_venue_papers.py neurips 2023
uv run scripts/litsweep/openreview_papers.py iclr 2024
uv run scripts/litsweep/enrich_abstracts.py data/papers/litsweep/neurips/2023.papers.jsonl
uv run scripts/litsweep/fetch_pdf.py data/papers/litsweep/iclr/2024.or_papers.jsonl --limit 50
```

## Venue Sources

| Venue | Source | Notes |
|---|---|---|
| ICLR | OpenReview | Abstracts and PDFs included. |
| NeurIPS | OpenReview for 2021+, DBLP fallback earlier | DBLP often lacks DOI for 2022+. |
| ICML / CVPR / AAAI / IJCAI / KDD | DBLP | Abstract enrichment needed. |
| ACL / EMNLP / NAACL | ACL Anthology | Scraper not yet implemented. |

## Known Gaps

- NeurIPS 2023 DBLP has no DOI fields; OpenAlex title search is partial.
- Semantic Scholar is rate-limited without `S2_API_KEY`.
- CVPR pre-2013 DBLP coverage is thin.
- NAACL is not annual; check `venues.yaml` and DBLP before assuming a year exists.
