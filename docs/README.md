# docs/ — the brain-alignment research brain

This folder is the **running knowledge base** for the thesis. It is the memory that survives
across Claude Code sessions. If something matters past the current session — a decision, a
result, a lesson, where we are, where we're going — it lives here, not in chat.

The governing principle (inherited from the Nexus redesign, and earned from its two failures):
**adaptive semistructure — specify only what is critical for shared truth, keep the rest light.**
We do *not* run the heavy Nexus stage-machine here. See `03-methodology.md` for why.

## Map

| File / dir | What it holds | Write cadence |
|---|---|---|
| `upspeed.md` | **Read first, write last.** Current state, next actions, blockers. | Every session (REPLACE) |
| `tasks.md` | The path behind and ahead: backlog → now → done. | As tasks move |
| `00-charter.md` | The idea, the real problem, scope, thesis context, success/kill criteria. | Rarely (on scope change) |
| `01-research-landscape.md` | Literature frontier map: prior art, the gap, the falsifiable assumptions, anti-confound protocol, baselines. | When literature shifts |
| `02-environment.md` | centcom facts: GPUs, disk, uv, cached models, datasets, how to run. | When the environment changes |
| `03-methodology.md` | The lightweight idea→evidence path we follow, and what we deliberately dropped from Nexus and why. | Rarely |
| `04-data-benchmarks.md` | Powered survey + decision (D008) on the four language-fMRI benchmarks we committed to. | When the benchmark choice shifts |
| `05-dataset-registry.md` | Living watchlist of *every* dataset that might be relevant (neural/behavioral/NLP), with features + use-case fit + status. | When a candidate dataset is found |
| `decisions/decisions.md` | Append-only decision log (ADR-style, D001…). | When a real decision is made |
| `timeline/` | Immutable session logs `YYYY-MM-DD-HHMM.md`. The path we actually walked. | End of each session |
| `hypotheses/` | One file per hypothesis (`HNNN_…`). Falsifiable claim + kill criteria. | Stage: Claim onward |
| `experiments/` | One file per experiment: design + iteration log + results. | Stage: Design onward |
| `reports/` | Living per-topic syntheses (`R01…`). Rewritten in place as new info lands. Distinct from canonical notes (per-paper) and the landscape map (frontier). **Analysis-session output.** | When a topic gains info |
| `manuscript/` | The thesis: drafted prose sections + final selected figures. **Analysis-session output.** | Analysis sessions |
| `literature/canonical/` | One note per paper actually read (self-contained copies). | When a paper is read |
| `literature/_prior-work/` | Provenance: the prior dossier, oracle review, origin idea (frozen, read-only history). | Never edited |
| `references/` | Reusable reasoning frames and conventions. | Rarely |
| `learnings.md` | Accumulated lessons and corrected mistakes. The anti-amnesia file. | When we learn something the hard way |

## Conventions

- **One source of truth.** Link, don't duplicate. If a fact lives in `02-environment.md`, point to it.
- **Specific numbers only.** "Retention ratio 0.91 ± 0.02, n=3 seeds" — never "it worked better."
- **Kill criteria are mandatory** for every hypothesis and every multi-day effort.
- **Negative results are results.** Record them in `learnings.md` and the relevant hypothesis.
- Dates are absolute (`2026-06-08`), never "today" / "last week".
- Session logs are immutable; `upspeed.md` is overwritten each session (history lives in `timeline/`).
- **Prose is not hard-wrapped: one line per paragraph (and per bullet/cell), let editors soft-wrap.** Hard wraps render as broken double-spaced text when an editor inserts blank lines between physical lines. New files follow this; existing hard-wrapped files get reflowed lazily when next edited.
