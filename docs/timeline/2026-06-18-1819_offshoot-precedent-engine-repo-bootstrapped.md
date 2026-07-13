---
title: "Timeline — 2026-06-18 18:19 — Offshoot: precedent-engine repo bootstrapped"
tags: [timeline]
---

# Timeline — 2026-06-18 18:19 — Offshoot: precedent-engine repo bootstrapped

**Breadcrumb (not a thesis-evidence session).** This session did **no** brain-alignment science — the ladder is unchanged. It designed and scaffolded a separate tooling project spun out of this thesis's needs.

- **What:** a **research precedent engine** (ask a research-situation question → papers across venues that faced/solved/noted it, full-text passage-level retrieval). Born from this repo's own pain points; the 12 seed use cases were mined from this repo's timeline/decisions/learnings.
- **Where it lives now:** its own git repo at **`/home/centcom/data/precedent-engine/`** (own `CLAUDE.md`, `/orient`+`/wrap`, 12 agents, docs brain, self-healing rules ported from this repo's learnings).
- **Reused from here:** the `scripts/litsweep/` fetch package was **copied** into the new repo (now repo-owned there); 20 NeurIPS 2025 PDFs were fetched as a parser test set.
- **Decision:** kept it a **separate repo**, not a track inside this thesis repo (would pollute the science source-of-truth).
- **Full story:** `precedent-engine/docs/journey/2026-06-18_session-01_design-and-problem-analysis.md`.

Nothing here needs follow-up in the thesis. Pointer only, so a future brain-alignment session knows where that tooling went.


## Related
- `ladder.md` — the canonical status board
- `map.md` — code system (Q/E/A/D/L) & journey map
