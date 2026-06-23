---
name: sci-write-v2
description: >-
  The redesigned /write pipeline (D048) — turn recorded findings into proper, tasteful academic prose by
  separating four concerns (Trust / Argument / Structure / Voice) over a staged gated loop: build the case
  and the plan, get them approved as one package, THEN draft, audit, and revise. Trust is earned by a gate
  plus a high-recall audit, not asserted by construction. Walking-skeleton phase: the Trust + Structure +
  Voice spine is live (claim-lattice, claim-binding, skeleton, drafter-with-\evd, voice audit, claim-fidelity,
  the ordering gate); the Argument concern (warrants, scope) and the message/frame + reader-model front-end are
  built too. The structure judge, figures, acknowledgment, consistency, exemplar pin, and the parallel-audit /
  Stop-hook convergence are still being added (Phase 2). Until this passes the 119-scenario suite, the live
  `scientific-writing` skill stays the default; this is built and tested alongside it.
---

# /write — the gated-loop pipeline

Good academic writing is the **separation of four normally-tangled concerns**: *what* you claim and whether it
is evidence-bound (**Trust**); *why* it follows and whether it is honestly sized (**Argument**); *how* it is
ordered for a reader (**Structure**); the **Voice** it is said in. Tangle them and you get the failure this
redesign exists to kill: prose that is true but reads like a story, over-reaches its scope, and that no one can
trust without re-reading every line.

The spine is a **gated loop, then a draft funnel**: stages 1–3 co-determine each other and the human gates them
as **one coupled package**; only then is prose generated, audited, and revised. The human gates the *case and
the plan*, never the lines.

**The non-negotiable honesty floor (rigid, every phase):** every claim binds to a recorded result or is a
`\gap`; a claim's wording is bounded by its evidence strength; scope never exceeds evidence; no prose ships
before the gate. These are deterministic hooks an agent cannot argue past (`scripts/`). Everything else — the
craft, the method choices — is where the agent thinks for itself (the RUB judges). See "Fluidity" below.

## The spine (stage by stage)

The lattice (`claim-lattice.json`, schema in `schema/LATTICE.md`) is the single shared object every stage
reads and writes; `meta.stage` tracks position. **`scripts/run_checks.py --lattice L [--prose P]` runs the
whole DET floor in one call** — run it after every stage write and treat any failure as a stop.

**Stage 0 · Evidence (input).** Read `docs/ladder.md` + `docs/reports/` + `docs/experiments/`. Never invent a
number; the evidence is frozen. Seed `.../evidence-register.json` status from the ladder if a cited experiment
is missing (it is keyed live/demoted/superseded).

**Stage 1 · Message & Reader (F2 + F1).** State the **one-sentence message** (Mensh-Kording: one paper, one
message — a norm the human gates at F16, *not* a DET check: a sentence-counter false-positives on "Sec.",
"U.S.", ellipses, so it stays a judgment), the **`frame`** (`basic-science | technology` — name which game you
are playing; for this thesis the technology frame is closed by the Q3 null), and the **`contribution_type`**;
write `message`, `frame`, `contribution_type` to the lattice. Then spawn **`sw-reader-model`** (sonnet) to build
the **reader-model** — `{venue, old, new, prior_beliefs, doubts}`, with old-vs-new judged *relative to that
venue's reader* (Pinker's curse-of-knowledge) — and write it to `reader_model`. Set `meta.stage=1`.
**`run_checks`** then enforces the stage-1 floor at the gate (message *present*, `frame` in enum,
`contribution_type` present, `reader_model` shaped — the append-safe diff also blocks a later stage from
emptying any of these). *F2 only **sets and gates**
the frame here; frame-consistency in the drafted prose is audited by the **F5 scope judge at stage 5** (not F2).
F17 exemplar pin is still **Phase 2**.*

**Stage 2 · Claim & Argument Lattice (Trust + Argument).** Extract every claim from the message; bind each to a
recorded experiment + a strength (`unsupported|observed|supported|strong`), reading `evidence_status`; an
unbound claim becomes a `\gap`. Write the claims; set `meta.stage=2`. Then **`run_checks`** →
`claim_binding` must pass (no stale/dangling/unbound-without-gap). *Phase 1: binding + strength + gap.
The Argument half — F4 warrants, F5 scope (opus, xhigh) — is **Phase 2**.*

**Stage 3 · Architecture (Structure).** Build the skeleton per `references/F6-skeleton.md`: OCAR macro, CARS
intro moves, CCC fractal, organize-by-importance; assign every claim a `section`, populate `sections[].claim_ids`
both directions; set `meta.stage=3`. **`run_checks`** → `lattice_integrity` must pass (orphan-claim,
empty-section, node↔section). *Phase 1: the skeleton + coverage. F7 figures, F11 structure judge, F18
acknowledgments are **Phase 2** (central-figure is dormant until stage 4 / F7).*

**↻ Stages 1–3 iterate freely** — binding may revise the message; the skeleton may reveal a missing claim.
Nothing is locked until the gate. No prose is generated in stages 1–3.

**GATE · F16.** Present the **coupled package** (message + reader-model + lattice + skeleton) to Erfan and get
one approval over the whole thing — *Phase 1: present it as a clear summary and confirm; the real
AskUserQuestion/ExitPlanMode primitive is **Phase 2**.* **Do not call `scripts/gate_state.py approve <lattice>`
until Erfan has actually said yes** — calling approve is recording his approval, not granting your own. **No
prose before this** — `gate_state check` blocks drafting without a matching approval, and re-blocks if a gated
field changed (a logic revision re-enters the gate). The floor binds to **prose existence**, not the
self-reported stage: `run_checks --prose …` passes `--drafting` so an agent that writes prose while leaving
`meta.stage=3` is still blocked.

**Stage 4 · Draft (Structure + Trust).** Spawn the **`sw-drafter`** subagent (opus): it realizes each skeleton
node as prose (old-to-new to the reader, mechanism before metrics, methods/results first), emitting one
`\evd{claim-id}{strength}` per claim sentence as it places it and mirroring each into `lattice.tags[]`, then
sets `meta.stage=4`. **The orchestrator MUST ensure the stage advances to 4 the moment prose exists** — that
coupling is what makes the gate's ordering floor real. *Phase 1: F8a. The F8b voice-realize pass is **Phase 2**
(F12 audits voice instead).* Then **`run_checks --lattice L --prose P`** → `draft_check` + `lattice_integrity`
(every-claim-tagged) + `claim_fidelity` (F9a, tag ≤ strength) + `ai_tell_lint` (F12 lexical) must pass.

**Stage 5 · Audit.** The DET floor already ran in `run_checks`. Now the **RUB readers**, in parallel (one
message, multiple subagents):
- **`sw-voice-auditor`** (F12 RUB, sonnet) — the register/voice gate; the real catch for the storytelling
  class (the Claudio anchor) the linter cannot reach.
- **`sw-claim-fidelity-judge`** (F9b, opus) — does any sentence's assertion exceed its own `\evd` tag.
*Phase 1: these two. F4/F5-on-prose, F11 structure, F13 premortem panel, F19 consistency, and the
structured-output `ready_to_ship` verdicts + parallel fan-out of all seven are **Phase 2**.*

**Stage 6 · Revise.** Fix coarse-to-fine, **never reversed**: logic → sentence → lexical. A **logic** fix
(it changes a gated field: a claim, a warrant, the skeleton, the message) **re-enters the gate** — re-run the
relevant stages, re-approve, `gate_state` will block until you do. A sentence/lexical fix loops back to the
stage-5 audit. Re-run `run_checks` + the RUB readers until **both the DET floor and the RUB readers are clean**.
Pass `run_checks --prev <prior-lattice>` on a stage write to run the append-safe / round-trip diff guard (no
claim or content-bearing field dropped between stages).
*Phase 1: this manual converge-until-clean loop, and **Erfan signs the final converge** — without the Phase-2
D047 Stop-hook + structured `ready_to_ship` verdicts, "clean" on the two RUB readers is a human call.*

## The DET floor vs the RUB judges (the fluidity boundary)

- **Rigid (hooks/scripts — `run_checks`):** the trust/honesty floor. A claim always needs bound evidence or a
  `\gap`; a tag never exceeds its claim's strength; scope never exceeds evidence; no prose before the gate;
  provenance tags always emitted; the lattice schema/coverage always holds. An agent **cannot** disable these.
- **Fluid (the RUB subagents + the craft choices):** the method choices in each stage (CCC/OCAR/CARS, the
  register call, the structure) are **defaults, not laws**. If a default does not fit the case, **stop,
  diagnose why, then adapt/combine/invent — or flag Erfan when the choice is load-bearing — and log the
  deviation** in `lattice.deviation_log` (`{functionality, method, why, did}`). Fluid, never silent: you may
  not invoke "fluidity" to skip the rigid floor (a `\gap` is not optional).

## What the Phase-1 floor does NOT yet catch (honest limits)
- **A `\gap` lives in the prose, not the lattice.** A claim with no recorded evidence is not entered as a
  lattice claim with `bound_experiment: null` — that is an *error* the floor flags (`[unbound]`). It is written
  as a `\gap{reason}` macro in the prose instead, allowed at the report/extended layer; the public-cut gate
  that blocks a surviving `\gap` (a lifted `check_gap_survival`) is wired at cutover.
- **An assertive sentence modeled as *framing* escapes the Trust floor.** The floor checks "every *claim*
  binds"; it cannot see a load-bearing sentence the agent simply chose not to enter as a claim (e.g. a stated
  hypothesis like "at most a weak prior"). **In Phase 1 the human gate is the only catch for this.** The
  Argument concern (F4 warrants / F5 scope) plus a prose→lattice claim-coverage check close it in **Phase 2**.

## Components (built in Phase 1)

| Stage | Component | Kind | Where |
|---|---|---|---|
| 2 | claim-binding (F3) | DET | `scripts/claim_binding.py` + `evidence-register.json` |
| 3 | skeleton (F6) | SKILL + DET | `references/F6-skeleton.md` + `scripts/lattice_integrity.py` |
| gate | ordering (F16) | DET | `scripts/gate_state.py` |
| 4 | drafter (F8a) | subagent (opus) | `agents/sw-drafter.md` + `scripts/draft_check.py` |
| 5 | claim-fidelity tag (F9a) | DET | `scripts/claim_fidelity.py` |
| 5 | claim-fidelity assertion (F9b) | subagent (opus) | `agents/sw-claim-fidelity-judge.md` |
| 5 | voice (F12) | DET + subagent (sonnet) | `scripts/ai_tell_lint.py` + `agents/sw-voice-auditor.md` |
| — | the spine artifact (F15) | ARTIFACT | `schema/claim-lattice.json` |
| — | DET dispatcher | — | `scripts/run_checks.py` |

**Added in Phase 2** (alongside the Phase-1 spine): **F4** argument-validity (`scripts/warrant_schema.py` DET +
`agents/sw-argument-judge.md`) · **F5** scope (`scripts/scope_lint.py` DET + `agents/sw-scope-judge.md`) — *P2-A,
opus xhigh, 2 sites each*. **F1** reader-model (`agents/sw-reader-model.md`, sonnet) + **F2** message&frame (this
skill's stage-1 section + the `frame`/`contribution_type`/`reader_model`/message-one-sentence checks in
`lattice_integrity.py`) — *P2-B-i*. Still to come: **F11** structure judge (P2-B-ii), then F7 figures, F18
acknowledgment, F13 panel, F19 consistency, F17 exemplar pin, F8b voice-realize, and the P2-D CC-power upgrades.

**Effort:** all subagents HIGH; the three hardest judges (F4 argument, F5 scope — built P2-A; F11 structure —
P2-B-ii) run XHIGH. The orchestrator runs at the session model.

## Phase-1 acceptance (the bar this walking skeleton must clear)
Run the spine on the manuscript **abstract**: every claim is `\evd`-bound (or an explicit `\gap`); the voice
audit **catches the Claudio storytelling class** (SC-VOICE-01–04) and **does not flag** the legitimate
near-misses (SC-VOICE-12/13); the DET floor (`run_checks`) is clean. If the skeleton makes trustworthy prose on
one case, expand to Phase 2; if not, the cost was one case.

## Relationship to the live skill
The live `scientific-writing` skill (path-select → full-loop → ship-gate) stays the default and is **untouched**
until cutover. This pipeline is built and tested in `.claude/skills/sci-write-v2/`. Phase 3 cutover (after the
119-scenario suite is green): retire the old flow, wire the DET checks as always-on hooks, point `CLAUDE.md`
and `docs/03-methodology.md` here, record the decision. Full design: `docs/references/write-redesign-design.html`.
