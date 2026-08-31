---
name: manuscript-check
description: >-
  Run the deterministic manuscript gate: evidence-marker resolution, keyed-number resolution
  across the input graph, bare result-like numbers, gap survival under --share-ready, and the
  LaTeX build.
tools: Bash
---

Run the single deterministic manuscript gate:

```bash
uv run python scripts/manuscript_check.py ${ARGUMENTS:-docs/manuscript/rewrite}
```

Use `--share-ready` only for a manuscript that is intended to ship; it additionally rejects every unresolved `\gap`. Report the exact findings. Do not weaken or bypass the checker to make it pass.
