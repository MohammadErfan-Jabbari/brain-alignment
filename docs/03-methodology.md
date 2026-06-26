---
title: "Methodology — how we work in this repo"
tags: [methodology]
---

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

| Phase        | Converts                                             | Artifact here                                                                |
| ------------ | ---------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Notice**   | a signal → a captured idea                           | a note (already done: the origin idea)                                       |
| **Commit**   | an idea → a real, anchored problem                   | [`00-charter.md`](00-charter.md) (problem reality anchor)                    |
| **Map**      | unknown landscape → bounded frontier                 | [`01-research-landscape.md`](01-research-landscape.md)                       |
| **Claim**    | uncertainty → falsifiable hypotheses + kill criteria | `hypotheses/HNNN_*.md`                                                       |
| **Design**   | a claim → a fair test (locked before running)        | `experiments/*.md` (design section)                                          |
| **Run**      | a protocol → traceable evidence (not conclusions)    | `experiments/*.md` (iteration log)                                           |
| **Judge**    | evidence → adjudicated claim status                  | hypothesis update + [`learnings.md`](learnings.md)                           |
| **Argue**    | judged claims → a written argument                   | reports (continuous) → manuscripts at checkpoints (see "Deliverable layers") |
| **Compound** | a finished effort → reusable residue                 | `learnings.md`, updated landscape                                            |

The non-negotiables (these are where solo research most easily self-deceives):
- **Multiple competing hypotheses**, not one cherished one.
- **Kill criteria predeclared** before running anything.
- **Design locked before evidence** — protocol, baselines, controls, stop rules, what counts as
  promotable vs exploratory.
- **Raw evidence kept separate from interpretation.**
- **Specific numbers with uncertainty** — "Δ = +0.06 ± 0.01, n=3, contiguous split" not "better."
- **Record the *why* of each non-obvious design choice** — a pooling rule, a resampling kernel, a
  threshold, a delay count — in the experiment doc when you make it. The writing layer can only cite a
  rationale a working session recorded; it must never invent one (D011). An unrecorded why becomes a
  `\gap` downstream, so recording it at choice-time is what keeps the eventual write-up honest. (D037.)

## Session stances (the unit of work)

Work runs by **interaction stance**, invoked at any moment and switched freely, not by a session-level
mode (the working/analysis split is retired, D044). The epistemic path still has its natural seam, and
the stances sit along it. There are eight (full map and mechanics: `docs/operating-map.md` and the
`stances` skill); the methodologically load-bearing distinction is whether a stance **touches a science
number**:

- **Truth-producing stances** carry the strict anti-self-deception standard:
  - **`/work` — produce evidence (Design → Run → Judge).** Lock a design, run it, judge the result,
    store it: code, runs, numbers-with-uncertainty in `experiments/*.md`, decisions, learnings. The
    failure mode is *fitting the hoped-for result*, so predeclared kill criteria, locked design,
    contiguous splits, and nuisance baselines live here.
  - **`/interpret` — adjudicate a recorded result into a verdict.** Re-judging a number is
    `/work`-grade, not loose reading: a claim-manifest pinned first, the load-bearing contrast
    re-computed, the thinking panel run to clean.
- **Reporting / consuming stances** (`/write`, `/teach`, `/scout`) turn recorded or external evidence
  into prose, understanding, or canonical notes. Their failure mode is *narrating past the evidence*:
  a confident sentence around a number never measured, or a null rounded into a trend.
- **Apparatus stances** (`/plan`, `/meta`) touch no number.

The binding rule across all of them is unchanged and now mechanically enforced: **a stance may only
state a number a `/work` session actually recorded in `docs/`.** A needed-but-missing number is a `\gap`
to flag (and a candidate `/work` task), never a value to invent, estimate, or infer from a stand-in.
This is armed at write-time by a hook (`.claude/hooks/honesty_writecheck.py`), independent of which
stance is active, so it cannot be skipped by mislabeling the work.

A real piece of work crosses stances (you finish a run, then write it up, then get taught it). That is
the normal case: state the stance you are in at each step, because the standard differs, and the
write-time guard holds regardless.

## Deliverable layers: reports → extended manuscript → public manuscript

We produce written knowledge in **three layers**, not one document. The layers differ on a single axis
— **how far the work is from a reader** — and that axis fixes everything else about them (audience,
depth, format, cadence, who triggers a write). The point of naming three is that each has a *different
job* and a *different update rhythm*; collapsing them is what makes a research write-up rot (a paper you
edit continuously drifts from the evidence; a narrative you only touch at submission goes stale). This
section is the **single source of truth** for what each layer is and when it changes. (Durable decision;
logged in `decisions/decisions.md`.)

**The cascade — knowledge flows one way, DOWN.** A lower layer is *derived from* the layers above it by
compression; an upper layer is never edited to match a lower one. A number or claim is born in the
evidence, narrated in a report, consolidated into the extended manuscript, and finally compressed into a
public cut — never the reverse.

```
CONTINUOUS — every session, working OR analysis
  experiments/ · ladder.md · learnings.md · decisions/    the evidence + the state of truth (numbers are BORN here)
  reports/  (R06+ finding-reports)                        living single-topic syntheses — iterated AS we work
        │
        │   ── CHECKPOINT (Erfan calls it): "update the extended manuscript" ──
        ▼
  EXTENDED MANUSCRIPT          = consolidate( work-state + experiments + reports )
  docs/manuscript/extended/      internal · living · LaTeX · git-TAGGED when shared with supervisors
    ├─ paper body      always-current; compresses cleanly → public
    └─ checkpoint log  append-only; the deep interval-by-interval history
        │
        │   ── CHECKPOINT (Erfan calls it): "cut a public version" ──
        ▼
  PUBLIC MANUSCRIPT  v0, v1…    = derive( extended manuscript + reports )
  docs/manuscript/public/        external · FROZEN snapshots · LaTeX · venue / thesis-grade
```

### The layer spec (the deterministic part)

| | **Report** | **Extended manuscript** | **Public manuscript vN** |
|---|---|---|---|
| **Job** | deep synthesis of ONE focused topic | the WHOLE story, end-to-end, fully explained | a submission/sharing CUT, compressed |
| **Audience** | us + whoever needs that topic | supervisors + collaborators | reviewers / committee / venue |
| **Scope** | one topic (may overlap manuscript content) | everything | everything, compressed |
| **Depth** | medium–deep, explained | **maximal** — nothing hedged-away | minimal — claims + headline evidence only |
| **Format** | **Markdown** | **LaTeX** (search-friendly source style) | **LaTeX** (venue/thesis class) |
| **Lifecycle** | living; rewritten in place; bump `Last updated` | always-current paper body + append-only checkpoint log; git-**tagged** when shared | **frozen** snapshots (v0, v1, …) |
| **Cadence** | continuous — written/iterated as we work | **checkpoint** — only when Erfan calls it | **checkpoint** — only at a submission/share milestone |
| **Derivation** | feeds ↑ into both manuscripts; stands alone | **the master** (consolidated from reports+evidence) | compressed **down** from extended (+reports) |
| **Who triggers a write** | the agent, as work touches the topic | **Erfan**, explicitly | **Erfan**, explicitly |

### What each layer is, concretely

**Reports (`docs/reports/*.md`) — the continuous synthesis layer.** A report is a single focused topic
kept current: a literature area (R01), a dataset/tooling survey (R02), a gap analysis (R04), or
one finding with its current verdict (R06+). It is the layer we actually *work in* — written and
rewritten across both session modes as the work moves. Reports are Markdown because they are my **source
of search**: the consolidation passes that build the extended manuscript grep across them constantly, and
Markdown is where my search/edit tools are strongest (see "Why these formats"). A report states the one
question it answers at the top, is honest about its gaps, obeys the numbers rule (below), and cites
literature to canonical notes and results to `experiments/`. Each report owns one finding and feeds up
into the extended manuscript at a checkpoint: the reports are the working syntheses, the extended
manuscript the consolidated supervisor-facing telling.

**Extended manuscript (`docs/manuscript/extended/`) — the internal master.** Two parts living in one
LaTeX project, a **synchronic** body and a **diachronic** log:

- **(a) The paper body — always-current.** The whole thesis told at the paper's skeleton (Abstract →
  Introduction → Related work → Methods → Results → Discussion → Limitations → Conclusion), at **5× the
  depth and nothing hedged away.** This is the part that compresses cleanly to a public cut (section →
  section). It always states the **current corrected** understanding: a claim later overturned is
  *rewritten*, never left standing. This is the source of truth for the public manuscript.
- **(b) The checkpoint log — append-only.** At each checkpoint, a new **dated segment** narrates that
  interval's work start-to-finish in full depth — what we did since the last checkpoint, why, what we
  found, what we abandoned. It is the **intellectual history in time order**, and it doubles as the
  "what's new since last time" a supervisor reads. It is **never rewritten**; the body holds the current
  truth, the log holds how we got there. (It does not duplicate `docs/timeline/`: that is per-session
  bookkeeping; this is checkpoint-cadence, manuscript-depth, and tied to the argument.)

Both parts carry the depth a public cut must drop:

1. **Full math derivations** in line — the DPI ceiling, the noise-ceiling channel-capacity bound, MDE /
   statistical power, conditional-MI = unique $R^2$ — derived, not just cited.
2. **Design-choice justifications** — why each control, baseline, split, and estimand was chosen, and
   what it rules out (the reasoning, not only the method).
3. **Dead-ends and pivots, narrated** — the E007 reroute, the robustness escapes, the Fork-A → Fork-B
   pivot, the decision history — told in full rather than footnoted.
4. **Per-experiment mechanics** — how each experiment actually ran, the catch the panel found, at a depth
   a collaborator could reproduce or critique.
5. **The reasoning, and the reasons behind the approach** — *why we framed the problem the way we did*,
   the meta-rationale that a terse paper erases.

The extended manuscript is updated **only at a checkpoint Erfan calls** ("update the extended
manuscript"), and the update is two moves: **fold** the interval's new evidence into the right *sections*
of the paper body (keeping it current and derive-ready), and **append** a dated segment to the checkpoint
log. Sources for both: the current work-state + experiment records + reports.

It is LaTeX (supervisors read a clean PDF; the math must typeset; and matching the public layer's format
makes the public cut a pure compression, not a format port). To keep it from fighting my search/edit
loop, its **source obeys a search-friendly style** — one paragraph (or one sentence) per source line,
minimal custom macros, semantic `\newcommand`s for the recurring objects (e.g. `\Lbrain`,
`\uniqueR`) so concepts stay greppable, content kept out of deep environment nesting. The scientific-
writing skill enforces this style.

**Public manuscript (`docs/manuscript/public/`) — the frozen cuts.** Each `vN` is a versioned snapshot
derived (compressed + hedged + length-disciplined) from the extended manuscript and reports for a
specific destination: a thesis chapter, a workshop/conference submission, a supervisor checkpoint that
needs a stable copy to cite. Public cuts are **frozen** — a new milestone produces a new `vN`, it does
not rewrite an old one. They are LaTeX in the target venue/thesis class. (The existing
`docs/manuscript/00_paper-draft-v0.md` is the current public draft, v0.9, in the pre-decision Markdown
era; it is the **seed** for the extended manuscript and is retained as the last md-era cut. The first
LaTeX public cut is a later `vN` derived from the extended master.)

### Why these formats (grounded, not asserted)

The format per layer was decided on measurable criteria, weighted by **how often I touch the file**:
(1) my search/edit ergonomics, (2) edit-safety, (3) typeset/output quality, (4) format-match across the
derivation seam, (5) git-diffability, (6) math fidelity, (7) audience. A test on this repo's real files
(a real LaTeX file vs the `R05.md` report) settled it: grepping the LaTeX file returns mostly **scaffolding**
(`\subsection{}`, `\caption{}`, `\label{}`, comments) with prose fragmented by commands (≈ half the file
is pure-markup lines), while grepping the Markdown report returns **whole paragraphs** — one match line =
one complete idea, which is exactly what a consolidation pass needs. And a Markdown edit cannot break a
compile, whereas a LaTeX edit can. So: the layer I touch **continuously** (reports) is Markdown, to
maximize search/edit throughput; the layers I touch only at **checkpoints** (both manuscripts) are LaTeX,
where rare-edit friction is an acceptable price for publication-grade output and a clean
extended→public derivation. The extended manuscript's search-friendly source style claws back most of the
LaTeX search penalty at the one layer where it would otherwise hurt.

### The numbers rule (D011) holds in all three layers

Every number in a sentence and every value in a figure must trace to a result a **working session
actually recorded** in `docs/` (an `experiments/ENNN` entry, a decision, a learning). A report, the
extended manuscript, and a public cut may **only** carry numbers that exist upstream; a needed-but-missing
number is a **gap to flag** (and a candidate working-session task), never a value to invent, estimate, or
round a null up from. Because derivation flows one way, a number cannot enter at the manuscript layer —
if it is not in the evidence/reports, it cannot appear downstream.

### Triggers — when to write/suggest each (the decision rules)

- **Update a report** — when new information lands on *that report's single topic*. Rewrite in place,
  bump `Last updated`. (Continuous; the agent does this as work touches the topic.)
- **Add a NEW report** — when a focused topic needs sustained, standalone synthesis: it recurs, it is
  too deep or tangential to sit inline in a manuscript, or it is worth sharing/citing on its own. The
  agent **suggests** one when it notices a topic being re-derived repeatedly, or a synthesis that does not
  fit an existing report.
- **Update the extended manuscript** — **only when Erfan calls a checkpoint** ("update the extended
  manuscript"). Then, two moves: **fold** the interval's new evidence into the right sections of the
  always-current paper body, and **append** a dated segment to the checkpoint log. This is *not* a
  default session output — never silently extend it. The agent may **suggest** a checkpoint when enough
  new evidence has accumulated that the body is materially behind the reports.
- **Cut a public version** — **only when Erfan calls a submission/share milestone.** Then: derive a new
  frozen `vN` from the extended manuscript + reports for the named destination. The agent **suggests** a
  cut when Erfan signals he is sending/submitting to someone.

### Drift discipline (reports ‖ extended manuscript)

Because the extended manuscript is rebuilt *from* the reports at checkpoints (not maintained live), the
reports are always the freshest synthesis and the extended manuscript is expected to lag between
checkpoints — that lag is normal, not drift. When a report gains a result the extended manuscript lacks,
record the debt explicitly at session close (a one-line "sync: extended behind R<NN> at §X") so the gap
is visible rather than silently rotting.

## Working preferences (Erfan's, stable across the history)

- Direct, no ceremony. Challenge when there are grounds; don't agree by default.
- ≥ 3 seeds for stochastic experiments. Strongest available baseline, never a strawman.
- Report CIs / std dev; name the statistical test. "X achieves Y under condition Z."
- Root cause, not symptom — never silently work around a blocker.
- Git: scoped staging only (never `git add -A`/`.`), no `--amend`, no destructive ops without
  explicit approval, push only when asked. (Git norm: decision D007; the repo is on `main`.)
- Prompts may have typos; infer intent.

## Reasoning frame

When designing or deciding, use the Elon / Feynman / Naval frame in `references/reasoning-frame.md`:
reduce to the real goal and delete false constraints (Elon); explain the mechanism plainly and state
where it breaks (Feynman); prefer the smallest durable change that compounds (Naval).

## Session ritual (the anti-amnesia loop)

- **Start:** `/orient` reads [`upspeed.md`](upspeed.md), [`tasks.md`](tasks.md), and the ladder, and proposes the stance to open
  in. Re-verify GPU/data only if a `/work` run is imminent.
- **During a truth-producing stance** (`/work`, `/interpret`): capture decisions in
  `decisions/decisions.md` as they happen; capture surprises immediately; keep raw evidence in
  `experiments/` separate from interpretation.
- **During a reporting stance** (`/write`, `/teach`, `/scout`): cite the `docs/` source for every number
  you state or plot; flag any needed number that isn't recorded rather than inventing it; write prose
  into `reports/` (continuous), and into the `manuscript/` layers only at a checkpoint Erfan calls (see
  "Deliverable layers").
- **End (always):** `/wrap` runs the `session-logger`, which writes an immutable
  `timeline/YYYY-MM-DD-HHMM.md`, REPLACES `upspeed.md`, moves items in `tasks.md`, appends any hard-won
  lesson to `learnings.md`, and updates the ladder. The log records which stances ran; the `upspeed.md`
  framing follows the dominant one (`/work`: *what ran / next to run*; reporting stances: *what's now
  understood / written / figured*).

## Self-maintenance clause

This methodology, `CLAUDE.md`, the agents, and the docs are **living**. When a workflow keeps getting
reconstructed in chat, or a mistake repeats, update the relevant file. When a task is done twice
without a tool, consider a new subagent or script. Per Erfan's global rule: propose changes to *his*
private/global instructions before editing them — but this repo's own docs are ours to keep current.


## Related
- [`ladder.md`](./ladder.md) — the canonical status board
- [`map.md`](./map.md) — code system (Q/E/A/D/L) & journey map
