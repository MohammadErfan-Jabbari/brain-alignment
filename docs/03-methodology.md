# Methodology — how we work in this repo

This is the operating philosophy. It is deliberately light. The reasoning for *why* it is light is
the most important part — it comes from watching the Nexus research-OS fail twice.

## The one principle

**Adaptive semistructure: specify only what is critical for shared truth; keep the rest adaptable.**
(Cherns' minimal critical specification; Brown & Eisenhardt's semistructure.) We add structure only
when its absence is actively costing us truth or continuity — never preemptively.

## What we inherited from Nexus, and what we threw away

Nexus is Erfan's research-OS, now on its third redesign. We harvested its *epistemic spine* and
dropped its *machinery*. The reasons are concrete:

- **Nexus v1 failed by over-specifying.** A vivid, powerful habitat, but "too much constitutional
  spread and continuity burden across too many surfaces" — it hardened a new rule/ritual/artifact
  every time ownership got fuzzy. → **We do not create a new artifact type or rule unless it earns
  its keep.**
- **Nexus v2 failed by over-coupling.** A principled control plane (a `.nexus/config.yaml`
  stage-machine, dual `AGENTS.md`/`CLAUDE.md` truth surfaces, gate reconciliation) that "demanded too
  much semantic coordination across too many surfaces." → **We do NOT run that stage-machine here.**
  No `config.yaml` stage gates, no dual-surface mirror, no reconciliation ceremony.
- **The correction that worked:** "prove one truthful loop before expanding the machinery." → **We
  start minimal and let real friction tell us what to add.**

For a **single thesis with a single owner on a single node**, the cross-project habitat and the
coupled control plane are pure overhead. We keep the thinking, not the bureaucracy.

## The epistemic path (kept, lightweight)

A paper is a truth-production pipeline, not a writing task. We follow these phases as a *guide*, not
a gated machine. Each converts one kind of uncertainty into one kind of knowledge:

| Phase | Converts | Artifact here |
|---|---|---|
| **Notice** | a signal → a captured idea | a note (already done: the origin idea) |
| **Commit** | an idea → a real, anchored problem | `00-charter.md` (problem reality anchor) |
| **Map** | unknown landscape → bounded frontier | `01-research-landscape.md` |
| **Claim** | uncertainty → falsifiable hypotheses + kill criteria | `hypotheses/HNNN_*.md` |
| **Design** | a claim → a fair test (locked before running) | `experiments/*.md` (design section) |
| **Run** | a protocol → traceable evidence (not conclusions) | `experiments/*.md` (iteration log) |
| **Judge** | evidence → adjudicated claim status | hypothesis update + `learnings.md` |
| **Argue** | judged claims → a public argument | the manuscript (built when evidence is in) |
| **Compound** | a finished effort → reusable residue | `learnings.md`, updated landscape |

The non-negotiables (these are where solo research most easily self-deceives):
- **Multiple competing hypotheses**, not one cherished one.
- **Kill criteria predeclared** before running anything.
- **Design locked before evidence** — protocol, baselines, controls, stop rules, what counts as
  promotable vs exploratory.
- **Raw evidence kept separate from interpretation.**
- **Specific numbers with uncertainty** — "Δ = +0.06 ± 0.01, n=3, contiguous split" not "better."

## Working preferences (Erfan's, stable across the history)

- Direct, no ceremony. Challenge when there are grounds; don't agree by default.
- ≥ 3 seeds for stochastic experiments. Strongest available baseline, never a strawman.
- Report CIs / std dev; name the statistical test. "X achieves Y under condition Z."
- Root cause, not symptom — never silently work around a blocker.
- Git: scoped staging only (never `git add -A`/`.`), no `--amend`, no destructive ops without
  explicit approval, push only when asked. (This repo is not yet a git repo — see `tasks.md`.)
- Prompts may have typos; infer intent.

## Reasoning frame

When designing or deciding, use the Elon / Feynman / Naval frame in `references/reasoning-frame.md`:
reduce to the real goal and delete false constraints (Elon); explain the mechanism plainly and state
where it breaks (Feynman); prefer the smallest durable change that compounds (Naval).

## Session ritual (the anti-amnesia loop)

- **Start:** read `upspeed.md` and `tasks.md` first. Re-verify GPU/data if a run is imminent.
- **During:** capture decisions in `decisions/decisions.md` as they happen; capture surprises immediately.
- **End:** the `session-logger` agent (or you) writes an immutable `timeline/YYYY-MM-DD-HHMM.md`,
  REPLACES `upspeed.md`, moves items in `tasks.md`, and appends any hard-won lesson to `learnings.md`.

## Self-maintenance clause

This methodology, `CLAUDE.md`, the agents, and the docs are **living**. When a workflow keeps getting
reconstructed in chat, or a mistake repeats, update the relevant file. When a task is done twice
without a tool, consider a new subagent or script. Per Erfan's global rule: propose changes to *his*
private/global instructions before editing them — but this repo's own docs are ours to keep current.
