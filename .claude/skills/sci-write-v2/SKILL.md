---
name: sci-write-v2
description: >-
  The redesigned /write pipeline (D048) — turn recorded findings into proper, tasteful academic prose by
  separating four concerns (Trust / Argument / Structure / Voice) over a staged gated loop: build the case
  and the plan, get them approved as one package, THEN draft, audit, and revise. Trust is earned by a gate
  plus a high-recall audit, not asserted by construction. Walking-skeleton phase: the Trust + Structure +
  Voice spine is live (claim-lattice, claim-binding, skeleton, drafter-with-\evd, voice audit, claim-fidelity,
  the ordering gate); the Argument concern (warrants, scope), the message/frame + reader-model front-end, the
  structure judge, figures, acknowledgment, the premortem panel, the exemplar pin, voice-realize, and the
  consistency check are built too. P2-D is landing the CC-power layer: the structured-verdict convergence machine,
  the parallel stage-5 fan-out, the convergence Stop-hook, the AskUserQuestion gate, the SC-XS-3 caption
  judge (folded into F5), and the fluidity/deviation-log enforcement are all in — **Phase 2 is complete**. The
  only remaining step is P3 cutover. Until this passes the 119-scenario suite, the live `scientific-writing` skill
  stays the default; this is built and tested alongside it.
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
venue's reader* (Pinker's curse-of-knowledge) — and write it to `reader_model`. Pin the **register (F17)**: pick
the venue's style anchors from `references/F17-exemplars.md` and write `register` = `{venue, exemplars:
[<section:paper>, …]}` — the voice pass cannot run without it. Set `meta.stage=1`. **`run_checks`** then enforces
the stage-1 floor at the gate (message *present*, `frame` in enum, `contribution_type` present, `reader_model`
shaped — the append-safe diff also blocks a later stage from emptying any of these; the `register` pin is
enforced at stage ≥ 4, before the voice pass). *F2 only **sets and gates**
the frame here; frame-consistency in the drafted prose is audited by the **F5 scope judge at stage 5** (not F2).
F17 exemplar pin is still **Phase 2**.*

**Stage 2 · Claim & Argument Lattice (Trust + Argument).** Extract every claim from the message; bind each to a
recorded experiment + a strength (`unsupported|observed|supported|strong`), reading `evidence_status`; an unbound
claim becomes a `\gap`. State the claim→claim **warrants** (the inference edges) in `warrants[]` and each claim's
`scope`. For each **defended claim** (bound + `strength ≥ observed`), spawn **`sw-acknowledgment`** (F18, opus) to draft a
limitation that **names the limitation and its mechanism** (a future-work pointer is *not* an acknowledgment) →
write `acknowledgments[]`. (At this stage there are no premortem objections yet — F18 plans from claims+scope.) Set
`meta.stage=2`. Then **`run_checks`** → `claim_binding` (no stale/dangling/unbound-without-gap) + `warrant_schema`
(no empty-warrant edge) must pass; spawn **`sw-argument-judge`** (F4) on the warrant edges and **`sw-scope-judge`**
(F5) on the claims' scope (both opus, xhigh, stage-2 site). *Acknowledgments are re-checked at stage 5 against the
F13 premortem.*

**Stage 3 · Architecture (Structure).** Build the skeleton per `references/F6-skeleton.md`: OCAR macro, CARS
intro moves, CCC fractal, organize-by-importance; assign every claim a `section`, populate `sections[].claim_ids`
both directions; set `meta.stage=3`. **`run_checks`** → `lattice_integrity` must pass (orphan-claim,
empty-section, node↔section). Plan the **key figures (F7)**: choose the figure that carries each *central* claim
and bind it in `figures[]` (`{figure_id, claim_id, caption, shows}`) — figures are the spine, chosen before prose;
write each figure's **`shows`** (what it actually plots) and a **`caption` sized to `shows`**, not to the broader
claim (the caption must not claim more than the figure displays — F5 judges caption ≤ `shows` at stage 5, SC-XS-3).
Then spawn
**`sw-structure-judge`** (sonnet, xhigh) at its **stage-3 site** to judge the skeleton: **opening-width =
resolution-width** (contributions promised in the opening ≤ those resolved in the discussion) and the **CARS
niche** (Move-2, the gap, is present — not territory→this-work). *The `central-claim-figure` DET (in
`lattice_integrity`) is dormant at stage 3 and **mandatory at stage ≥ 4** — by drafting, every `is_central` claim
must carry a figure.*

**↻ Stages 1–3 iterate freely** — binding may revise the message; the skeleton may reveal a missing claim.
Nothing is locked until the gate. No prose is generated in stages 1–3.

**GATE · F16.** Present the **whole coupled package as one** and get a single explicit approval over it — via the
**`AskUserQuestion` tool**, not free chat (a real approval primitive, so the yes is an unambiguous decision, not
inferred from conversation). The package is **every field the gate hashes** (so the human approves exactly what
gets locked — `gate_state._projection`): the one-sentence message, the frame + contribution_type, the
reader-model, the **pinned register (F17 exemplars)**, the full claim/argument lattice (each claim's
evidence+strength + scope + is_central + acknowledgments, and the warrants), and the skeleton + figure plan.
Summarize **each** of these, then ask **one** `AskUserQuestion`. The approve option's label must be exactly
**`Approve`**; the Revise options must between them cover the full package (derive them from the fields above —
e.g. `Revise claims/scope`, `Revise structure/skeleton`, `Revise message/reader/frame`, `Revise register/
acknowledgments`), so no part is un-revisable. Approving only part of it is **not** approval (SC-PROC-2) — present
and gate the whole package. **Only an exact selection of the `Approve` option authorizes
`scripts/gate_state.py approve <lattice>`** — that call *records his decision*, it does not grant your own; never
call it on your own read, and **a cancelled / unanswered dialog or any other selection is NOT approval** → loop
back into stages 1–3 and re-present. **No prose before this** — `gate_state check` blocks drafting without a
matching approval, and re-blocks if **any gated field** changed since approval (a logic revision re-enters the
gate). The floor binds to **prose existence**, not the self-reported stage: `run_checks --prose …` passes
`--drafting`, so an agent that writes prose while leaving `meta.stage=3` is still blocked.
*(Supervisor/reviewer feedback later also re-enters here, not the draft — it changes the approved case.)*

**Stage 4 · Draft (Structure + Trust).** Spawn the **`sw-drafter`** subagent (opus): it realizes each skeleton
node as prose (old-to-new to the reader, mechanism before metrics, methods/results first), emitting one
`\evd{claim-id}{strength}` per claim sentence as it places it and mirroring each into `lattice.tags[]`, then
sets `meta.stage=4`. **The orchestrator MUST ensure the stage advances to 4 the moment prose exists** — that
coupling is what makes the gate's ordering floor real. Then spawn **`sw-voice-realize`** (F8b, sonnet) to rewrite
the placed prose for register against the pinned F17 exemplars — **preserving every `\evd` tag, every `%%SECTION`
marker, and every number** (it is voice-only; it changes no claim and no structure). F8b is gated by F17: the
`no-exemplar-pin` DET blocks stage ≥ 4 without a `register`. Then **`run_checks --lattice L --prose P --prev-prose
<F8a-output>`** → `draft_check` (incl. **number-conservation**: F8b changed/added/dropped no number) +
`lattice_integrity` (every-claim-tagged + the F17 pin) + `claim_fidelity` (F9a, tag ≤ strength) + `ai_tell_lint`
(F12 lexical) + `scope_lint` (F5 lexical) + `consistency_check` (F19: abstract↔body numbers, no full CI in the
abstract) must pass. **The F8b output is the ONE canonical draft** — **arm the convergence Stop-hook on it now:**
`python3 .claude/skills/sci-write-v2/scripts/verdicts.py activate --prose <F8b-draft>`. From here the
`stop_sw_converge` hook **blocks your turn-end while the draft is unconverged** (loop-guarded — see stage 6; it is
a strong nudge backed by Erfan's final sign-off, not an inescapable wall); `activate` also pins this path so all
`record`/`status` use it. Disarm with `verdicts.py ship` only after convergence **and** Erfan's final approval.

**Stage 5 · Audit.** The DET floor already ran in `run_checks`. Now the **RUB readers**. **Fan the independent
readers out in ONE message** (P2-D true parallel — they share no state): spawn `sw-argument-judge` (F4),
`sw-scope-judge` (F5), `sw-claim-fidelity-judge` (F9b), `sw-structure-judge` (F11), `sw-voice-auditor` (F12), and
the F13 panel (`premortem-analyst` + `counter-argument`) — **seven subagents, one turn**. `sw-acknowledgment`
(F18) runs **after** the batch returns, because it consumes F13's mapped objections. The readers:
- **`sw-voice-auditor`** (F12, sonnet) — the register/voice gate; the real catch for the storytelling class (the
  Claudio anchor) the linter cannot reach.
- **`sw-claim-fidelity-judge`** (F9b, opus) — does any sentence's assertion exceed its own `\evd` tag.
- **`sw-argument-judge`** (F4, opus xhigh, stage-5 site) — does each "therefore" in the prose actually hold, and
  is the cited evidence the right receipt (grounding).
- **`sw-scope-judge`** (F5, opus xhigh, stage-5 site) — is each claim sized to its evidence, plus
  **frame-consistency** (a basic-science finding sold as a deployment/technology claim → flag, SC-HON-06) **and
  figure captions** (each `caption` must not claim more than its figure shows → flag, SC-XS-3).
- **`sw-structure-judge`** (F11, sonnet xhigh, stage-5 site; **input: the prose + the lattice's `reader_model`**)
  — per paragraph: point sentence? old→new to the reader-model? CCC?
- **F13 premortem panel** — spawn the D017 thinking panel (`premortem-analyst` + `counter-argument`) on the draft
  + lattice. These are the **shared repo panel agents**; they emit their native `PANEL-VERDICT` format, which has
  **no `claim_id` slot**. So the orchestrator then **maps each returned objection to the `claim_id` it threatens**
  (re-express it as `{threatens: <claim_id>, mechanism: …}` against the lattice). **An objection that cannot be
  mapped to a claim is itself the SC-ARG-5 defect — flag it; do not pass an unmapped objection to F18.** The mapped
  list is F18's stage-5 input.
- **`sw-acknowledgment`** (F18, opus) re-run — input = the defended claims + that **mapped** objection list; every
  surviving objection must be acknowledged on the claim it threatens (named limitation + mechanism, not a
  future-work pointer); a newly-required acknowledgment changes a gated field, so it is a **logic revision that
  re-enters the gate**.
**Record the verdicts, then check convergence — P2-D-2 is the *bookkeeping*; the convergence + staleness
*enforcement* is P2-D-3's Stop-hook.** (Provenance — proving a verdict came from a real reader run, not a
hand-typed boolean — is a **named accepted non-goal**: the store is trusted, exactly like `gate_state.py` and
`stop_register_gate.py`.) Use ONE canonical draft path for every record + status call: the **F8b voice-realize
output** (the final draft — not the F8a pre-voice draft, which also sits on disk at stage 4). Each judge emits its
`<TAG>-VERDICT: {"ready_to_ship": <bool>, "findings": <int>}` line; transcribe the judge's **own** boolean —
never substitute your read (honesty is on you; the hook enforces convergence, not provenance) — one call per reader:
`python3 .claude/skills/sci-write-v2/scripts/verdicts.py record --prose <F8b-draft> --reader <argument|scope|fidelity|structure|voice|acknowledgment> --ready <true|false> --findings <n>`.
The **`acknowledgment`** verdict recorded here MUST be F18's **stage-5 re-run** (the one that consumed the mapped
objections), never the vacuous stage-2 plan (which had no objections yet). The **`premortem`** verdict has no
agent line — **synthesize** it *identically to `verdicts.py`'s docstring* (keep the two in lockstep):
- `objections` = `counter-argument`'s objections **+** `premortem-analyst`'s TOP-RISK (fold the advisory risk in
  as an objection, or it is invisible to convergence);
- `ready=true` iff `counter-argument` `CONCLUSION-STATUS == SURVIVES` (bare — `SURVIVES-IF-NARROWED` and
  `DOES-NOT-SURVIVE` are **both not ready**) **and** every objection mapped to a claim (an unmapped objection is
  the SC-ARG-5 defect);
- `findings` = (# unmapped objections) + (1 if `CONCLUSION-STATUS != SURVIVES`) — never 0 when not ready;
record it as `--reader premortem`. Then `verdicts.py status --prose <F8b-draft>` → exit 0 = **converged** (every
required reader ready for *this* draft), exit 1 = not (the output names each missing / not-ready / contradicting
reader). A `ready_to_ship: true` line with `findings > 0` is rejected as not-ready, so emit the honest pair.
The **F19 consistency** DET (`consistency_check`: abstract↔body numbers + no full CI in the abstract) already ran
in `run_checks`; its RUB half — **caption ≤ figure** (SC-XS-3) — is now judged by **F5** at its stage-5 prose site
(caption ≤ what the figure plots is a scope question; re-mapped F19→F5, P2-D-5), sizing `figures[].caption` against
`figures[].shows` (NOT the broader bound claim). *The
**`stop_sw_converge` Stop-hook
(P2-D-3, landed)** now blocks turn-end while `status` is unconverged (loop-guarded; staleness + convergence
only — provenance is an accepted non-goal); see stage 6. Phase-2 remaining: **P2-D-4** AskUserQuestion gate,
**P2-D-5** caption, **P2-D-6** deviation-log.*

**Stage 6 · Revise.** Fix coarse-to-fine, **never reversed**: logic → sentence → lexical. A **logic** fix
(it changes **any gated field** — message, frame, contribution_type, reader-model, register, a claim, a warrant,
the skeleton, a figure: the full `gate_state._projection` set) **re-enters the gate** — re-run the relevant
stages, re-approve, `gate_state` will block until you do. A sentence/lexical fix loops back to the
stage-5 audit. Re-run `run_checks` + the RUB readers until **both the DET floor and the RUB readers are clean**.
Pass `run_checks --prev <prior-lattice>` on a stage write to run the append-safe / round-trip diff guard (no
claim or content-bearing field dropped between stages).
Re-record each reader's verdict after a revision (`verdicts.py record …`) and re-run `status` — a prose edit
changes the draft hash, so every prior verdict goes stale and the readers must re-run on the new draft.
The **`stop_sw_converge` Stop-hook (P2-D-3)** now automates this: while the draft is armed it **blocks your
turn-end** when `status` is not converged (loop-guarded — `MAX_BLOCKS=3` per draft hash, then it escalates to
Erfan instead of trapping you; and CC's `stop_hook_active` re-entrancy means the practical effect is a strong
nudge per work-stretch, **with Erfan's sign-off the final gate**, not the hook alone). Erfan's escape for an
accepted residual: `verdicts.py accept-residual --prose <draft>` (keyed to the current bytes; an edit voids it).
After converge + Erfan's approval, `verdicts.py ship` (disarms + clears the gate state).

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
`lattice_integrity.py`) — *P2-B-i*. **F11** structure judge (`agents/sw-structure-judge.md`, sonnet xhigh, 2
sites) — *P2-B-ii*. **F7** figures (stage-3 SKILL step; the `central-claim-figure` DET already lives in
`lattice_integrity`), **F13** premortem panel (reuses the D017 `premortem-analyst` + `counter-argument`), **F18**
acknowledgment (`agents/sw-acknowledgment.md`, opus) — *P2-C-1*. **F17** exemplar pin
(`references/F17-exemplars.md` + the `register` field/DET in `lattice_integrity`) + **F8b** voice-realize
(`agents/sw-voice-realize.md`, sonnet) — *P2-C-2a*. **F19** consistency (`scripts/consistency_check.py`:
abstract↔body + CI-in-abstract; the caption≤figure RUB is deferred) — *P2-C-2b*. **P2-D** CC-power upgrades:
the structured verdict schema + convergence state machine (`scripts/verdicts.py`, all 7 readers unified on
`*-VERDICT: {ready_to_ship, findings}`) — *P2-D-1*; the stage-5 parallel fan-out + verdict-recording
orchestration (this stage-5 section) — *P2-D-2*; the convergence Stop-hook (`.claude/hooks/stop_sw_converge.py`,
wired in `settings.json`, pipeline-scoped via `active.json` + session-scoped, D047 loop-guard) + the gate-state
ops in `verdicts.py` (`activate`/`ship`/`accept-residual`) — *P2-D-3*; the F16 gate via `AskUserQuestion` (the
GATE section) — *P2-D-4*; SC-XS-3 caption ≤ figure judged by F5 + the `caption`/`shows` figure fields — *P2-D-5*;
the fluidity/deviation-log enforcement (F11 flags a silent force-fit, the `deviation_log` well-formedness DET,
SC-PROC-8/9/10/11) — *P2-D-6*. **P2-D complete; Phase 2 done. Only P3 cutover remains (after the 119-suite,
Erfan's explicit go).**

**Effort:** all subagents HIGH; the three hardest judges (F4 argument, F5 scope, F11 structure — all built,
P2-A/P2-B) run XHIGH. The orchestrator runs at the session model.

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
