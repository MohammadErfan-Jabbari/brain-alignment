---
description: Run the deterministic provenance, number, gap, citation/reference, and LaTeX checks for a manuscript.
argument-hint: [path] [--share-ready]
allowed-tools: Bash
---

Run the single deterministic manuscript gate:

```bash
uv run python .claude/scripts/manuscript_check.py ${ARGUMENTS:-docs/manuscript/extended}
```

Use `--share-ready` only for a manuscript that is intended to ship; it additionally rejects every unresolved `\gap`. Report the exact findings. Do not weaken or bypass the checker to make it pass.
