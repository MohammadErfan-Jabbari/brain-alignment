# Scientific writing: pointer to the skill

All the detail lives in the **`scientific-writing` skill** (`.claude/skills/scientific-writing/`). This
page is a one-screen summary so the docs index can point at it; read the skill for anything real.

**What it is.** The single governor of how recorded evidence becomes written argument across the three
deliverable layers (defined in `03-methodology.md` "Deliverable layers"): markdown reports, the LaTeX
extended manuscript, and frozen LaTeX public cuts. It keeps prose in a real scientific voice with no AI
tells, makes every number trace to recorded evidence (D011), hedges by what was measured, and runs
deterministic checks before a manuscript ships. It never invents a result.

**When it fires.** Any time you write, draft, edit, consolidate, compress, or review a report, manuscript
section, abstract, results paragraph, or checkpoint-log entry. Small report edits take a fast path (style
floor plus the cite rule); section writes, consolidations, and public cuts take the full loop.

**The verifiers** (run before a section or cut ships):

```
uv run python .claude/skills/scientific-writing/scripts/run_checks.py --layer <report|extended|public> <path>
```

`ai_tell_lint` (anti-AI-tell floor), `check_evd_resolution` (D011: every number cited, every cite
resolves), and for a public cut also `check_gap_survival`, `check_number_consistency`, and
`check_claim_survival` (the compression gate).

**The reference docs inside the skill:** `writing-style.md` (voice + the anti-AI-tell rules),
`provenance-d011.md` (`\evd`/`\gap`, keyed numbers), `latex-conventions.md` (source style, the shared
preamble, the build), `review-pass.md` (the Devil's-Advocate review). The LaTeX assets (preamble,
templates, keyed-number registry, bib, build config) live under the skill's `assets/`.
