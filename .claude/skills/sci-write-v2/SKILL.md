---
name: sci-write-v2
description: >-
  The redesigned /write pipeline (D048) — turn recorded findings into tasteful academic prose by separating
  four concerns (Trust / Argument / Structure / Voice) over a staged gated loop: build the claim-lattice and
  skeleton, gate them as one package, then draft, audit, and revise to convergence. Use when writing or
  revising a report or manuscript section, an abstract, or any prose that must bind every claim to recorded
  evidence. NOT yet the default — until it clears its acceptance suite, route everyday writing through
  `scientific-writing`.
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
enforced at stage ≥ 4, before the voice pass). *F2 only **sets and gates** the frame here; frame-consistency in
the drafted prose is audited by the **F5 scope judge at stage 5** (not F2).*

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
readers out in ONE message** (true parallel — they share no state): spawn `sw-argument-judge` (F4),
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
**Record the verdicts, then check convergence.** Use ONE canonical draft path for every record + status call:
the **F8b voice-realize output** (the final draft — not the F8a pre-voice draft, which also sits on disk at
stage 4). Each judge emits its
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
in `run_checks`; its RUB half — **caption ≤ figure** (SC-XS-3) — is judged by **F5** at its stage-5 prose site
(a caption is the same scope axis as a claim), sizing `figures[].caption` against `figures[].shows` (NOT the
broader bound claim). The convergence Stop-hook that gates this whole audit is described at stage 6.

**Stage 5.5 · Handoff triage (D050).** *("5.5" is a label for this step only — NEVER write it to `meta.stage`,
which is a validated int 1–6.)* Before you loop a finding back into the stage-6 revise, classify **why** it is
blocking. Some defects the prose **cannot** fix because they live in the evidence/argument substrate (the E006
voxel-bootstrap CI is the anchor): rewording would only paper over them, and the one repair — recomputing or
re-adjudicating a number — is forbidden here (a number is born in `/work` and recorded in `docs/`; `/write` may
not produce or alter it). Route those upstream instead of looping forever.

Each blocking finding gets **one of three outcomes**:
- **PASS** — not a defect; it converges.
- **WRITING-REVISE** — a reword *within the currently recorded evidence* fixes it → the stage-6 loop.
- **NEEDS-STANCE(s)** — no rewording within recorded evidence can resolve it → emit a handoff, block, surface.
A finding is `NEEDS-STANCE` **iff no rewording within the currently recorded evidence could resolve it.**

**The reader self-tag (the RUB half, M3).** As the cheap first pass, each of the **6 prose readers** (argument,
scope, fidelity, structure, voice, acknowledgment) tags its own finding `{class: writing-revise | needs-stance,
target_stance?, why_not_writing?}`. The 7th reader, **premortem (F13)**, has no self-tag line — its substrate-defect
signal is the panel `CONCLUSION-STATUS`, which the M3 backstop below reads directly. **On ambiguity, tag
`needs-stance`, never `writing-revise`** (fail toward more checking — L059; a missed substrate defect is the
catastrophe, an over-routed one only costs a human glance).

**The M3 backstop (the DET force-rule, the under-routing guard).** Over the aggregated findings: **any F13 panel
verdict that is `SURVIVES-IF-NARROWED` or `DOES-NOT-SURVIVE`, where the narrowing needs a number or claim NOT
already recorded in `docs/`, is FORCED to `needs-stance` regardless of how a reader tagged it.** This is exactly
what catches the E006 anchor (F13 surfaces it as `SURVIVES-IF-NARROWED`; the fold-level CI it would need is not
recorded). **The in-`docs/` side does NOT fire** (SC-XSTANCE-16): if a recorded result already supports the
narrower claim, narrow it in prose — that is `writing-revise`, not a handoff.

**The over-routing guard (SC-XSTANCE-08).** Conversely: a finding a reword *within the currently recorded evidence*
fixes is `writing-revise`, not a handoff — a merely-hard sentence is not a substrate defect. Fail toward
`needs-stance` only on genuine **ambiguity about whether the evidence exists**, not on every difficult sentence.

**The trigger taxonomy (route by what the finding is):**

| # | Finding | Routes to |
|---|---|---|
| 1 | a recorded result exists but a number is broken, OR its aggregation/contrast is contested | `/interpret` (re-adjudicate) → `/work` (recompute if needed) |
| 2 | a load-bearing claim has **no recorded result at all** (not even a contested one) | `/work` — **write the `\gap` in prose AND emit the handoff** (complement, never replace) |
| 3a | a claim contradicts another report/cross-section number (internal) | `/interpret` (or `/review`) |
| 3b | a claim contradicts an external source | `/scout` → `/interpret` |
| 4 | a reader computes a number no cited record contained | `/work` to record it first, then resume (the honesty floor blocks citing it meanwhile) |
| 5 | a related-work claim needs a source we lack | `/scout` (lit-scout) |
| 6 | a frame/scope decision only the human owns | `/plan` / human gate |
| 7 | a cited result is recorded but never adjudicated | `/interpret` |

**Row 1 vs row 2 — route by whether a recorded result exists.** If the experiment ran and its result is recorded
but a number is broken or its aggregation/contrast is contested — **the E006 anchor: the CI exists, only its
inferential unit (voxel bootstrap vs fold) is wrong** — that is **row 1 → `/interpret`** (re-adjudicate the unit),
which itself chains to `/work` if a recompute is needed. Reach for **row 2 → `/work` + `\gap`** only when there is
*no recorded result at all*. A specific sub-statistic that was never computed off an existing result is still row 1.

**On `NEEDS-STANCE`, the orchestrator (detect-and-recommend — it never acts upstream itself):**
1. classify the target stance from the taxonomy;
2. emit the handoff — `python3 .claude/skills/sci-write-v2/scripts/verdicts.py handoff open <id> --finding <…> --threatens-claim <claim_id> --target-stance <work|interpret|review|scout|plan> --why <why prose can't fix it> --what-to-produce <…> --recommended-command <e.g. "/interpret E006"> [--proposed-unverified <a reader's recompute>] [--reader <which reader>]`;
3. that **stickily blocks convergence** (X2's `handoffs-open` clause — a reword cannot clear it);
4. **surface to the human**: the finding, the claim it threatens, **why writing can't fix it**, the target stance, the recommended command;
5. **never auto-spawn** the stance — recommend it; Erfan drives;
6. **never adopt a reader's computed number** — carry it as `proposed_unverified` on the handoff, to be born in `/work`/`/interpret`. Record that reader's verdict as `--ready false` too, so the reader gate and the handoff gate both hold.

**`evidence_status: suspect` ownership.** `/write` only **emits the handoff recommending** `suspect`; `/interpret`
**proposes** it; `/work` + Erfan **record** it. `/write` never stamps a status (X1).

**The two-gate rebind contract (MF3) — resolving a handoff is NOT the end.** A handoff `resolve`s when the upstream
stance **records** its output (`--ref` points to the experiment key / decision id / commit / `evidence_status`
change). That clears only the `handoffs-open` clause. The draft **still** will not converge until the writer
**rebinds the lattice claim** to the corrected evidence (so `claim_binding` passes) and the readers re-run clean —
a **logic revision that re-enters the F16 gate**. The transient `claim_binding` `[status-mismatch]` (the claim
says `live` while the register now says `suspect`) is **intended** — it keeps blocking until the rebind. Flow:
`/interpret` records → `handoff resolve` → writer rebinds (re-gate) → readers re-run → converge.

**Orphan guard + human surface.** After any re-skeleton or claim-id change (a stage-6 logic revision drops/renames
a `claim_id`), run `verdicts.py handoff check --lattice <claim-lattice.json>`: a `[dangling-handoff]` flag means an
open handoff's `threatens-claim` was deleted — re-point or resolve it, or it becomes an unkillable orphan that
blocks convergence forever. `verdicts.py handoff status` lists open/resolved handoffs (the human-facing surface).

**Stage 6 · Revise.** Fix coarse-to-fine, **never reversed**: logic → sentence → lexical. A **logic** fix
(it changes **any gated field** — message, frame, contribution_type, reader-model, register, a claim, a warrant,
the skeleton, a figure: the full `gate_state._projection` set) **re-enters the gate** — re-run the relevant
stages, re-approve, `gate_state` will block until you do. A sentence/lexical fix loops back to the
stage-5 audit. Re-run `run_checks` + the RUB readers until **both the DET floor and the RUB readers are clean**.
Pass `run_checks --prev <prior-lattice>` on a stage write to run the append-safe / round-trip diff guard (no
claim or content-bearing field dropped between stages).
Re-record each reader's verdict after a revision (`verdicts.py record …`) and re-run `status` — a prose edit
changes the draft hash, so every prior verdict goes stale and the readers must re-run on the new draft.
The **`stop_sw_converge` Stop-hook** automates this: while the draft is armed it **blocks your
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

## Honest limits (what the floor does NOT catch)
- **A `\gap` lives in the prose, not the lattice.** A claim with no recorded evidence is an *error* the floor
  flags (`[unbound]`) — not a lattice claim with `bound_experiment: null`. An honest gap is written as a
  `\gap{reason}` macro in the prose (allowed at the report/extended layer).
- **An assertive sentence modeled as *framing* escapes the Trust floor.** The floor checks "every *claim*
  binds"; it cannot see a load-bearing sentence the agent chose not to enter as a claim (a stated hypothesis
  like "at most a weak prior"). The human gate is the catch until a prose→lattice claim-coverage check exists.
  **D050 does NOT close this** — the cross-stance handoff routes substrate defects *that surface as findings*; a
  framing sentence that was never entered as a claim surfaces as no finding, so the human gate remains its catch.
- **The stage-5.5 classification is RUB, with one DET backstop.** A voice/structure reader meeting a substrate
  defect could mislabel it `writing-revise` — **except** where the M3 force-rule fires (a panel verdict whose
  narrowing needs an out-of-`docs/` number). The guarantee is bounded: **panel-detectable science problems are
  caught mechanically; non-panel ones rest on reader honesty + the human gate.**

**Effort:** spawn all subagents at **HIGH**; the three hardest judges — F4 argument, F5 scope, F11 structure —
at **XHIGH**. The orchestrator runs at the session model.

## Relationship to the live skill
This pipeline is **not the default**: the live `scientific-writing` skill stays in force until cutover — route
everyday writing through it. Design, build state, and the cutover plan live in
`docs/references/write-redesign-design.html` and `docs/references/write-redesign-build-plan.md`.
