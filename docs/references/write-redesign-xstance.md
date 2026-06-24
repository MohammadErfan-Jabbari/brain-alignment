# /write cross-stance handoff — design addition (D050, BUILD-READY)

**Status:** design complete, BUILD-READY (hardened across 4 clean-context opus reviews, the L058 discipline).
Builds next session as chunks X1–X4 (§H), alongside P3. Companion to `write-redesign-design.html` (the
canvas) and `write-redesign-build-plan.md` (the build). Regression anchor: SC-XSTANCE-01 = the dry-run.

Adds to the D048 `/write` pipeline the capability the dry-run proved missing: when an auditor finds a
defect the prose **cannot** fix because it lives in the evidence/argument substrate (not the writing),
`/write` must route it to the owning stance and stop — never paper over, never produce/adopt a number.
Regression anchor: the **E006 voxel-bootstrap CI** the F13 panel caught in the dry-run (a `live`, sourced,
not-demoted number that is actually mis-aggregated — invisible to every existing guard).

---

## B · Ideal-system framing

The four concerns (Trust / Argument / Structure / Voice) all judge the **prose**. None answers: *what
happens when an auditor finds something the prose cannot fix?* Today the audit has only two outcomes —
**converged** (ship) or **writing-revise** (loop). It is missing a third.

**The addition is a cross-cutting ORCHESTRATION function, not a 5th concern** (Erfan-approved). It sits
between the stage-5 audit and the stage-6 revise loop, exactly where `/write` is the place the manuscript
meets the evidence — so it is the natural **detector** of "the evidence is not ready for this claim."

**Principle (the hard line, turned into a pipeline behavior):** `/write` detects evidence-unreadiness,
routes it to the owning stance, and blocks — it never papers over, and never produces or adopts a number.
This *extends* "trust by gate + audit": the audit's per-finding verdict space gains a third value.

**Three audit outcomes per finding:**
| Outcome | Meaning | Action |
|---|---|---|
| `PASS` | ready | converge |
| `WRITING-REVISE` | a prose defect (voice / structure / scope-wording / fidelity-wording) | stage-6 revise loop (existing) |
| `NEEDS-STANCE(S)` **NEW** | the defect is in the evidence/argument substrate, not the prose | emit handoff · block convergence · surface stance S + command |

**What `/write` does on `NEEDS-STANCE` (detect-and-recommend — fork-1 decision):**
1. Classify the finding's target stance.
2. Emit a structured **handoff record** (schema below).
3. **Block convergence — stickily.** A prose edit cannot close a handoff; only the upstream stance's
   *recorded* output can. (This is what stops the convergence loop from "fixing" a science problem by
   rewording.) **Mechanism (M1, realized in §F):** the existing `verdicts.py` convergence is keyed to the
   *prose hash* — so a reword + re-record would flip a reader's `ready_to_ship` to true and silently close
   the issue. The fix is an **8th convergence blocker, `handoffs-open`, keyed to handoff-resolution state,
   NOT the prose hash**: `status` is converged only if all 7 readers are ready *and* zero open handoffs
   remain; a handoff resolves only when the upstream stance records its output (a new/corrected number,
   an adjudication, a `suspect` status, a citation), never by a redraft. Without this, the sticky-block is
   prose, not a mechanism — it is the gating build-readiness requirement.
4. Surface to the human: the finding, the claim it threatens, *why writing can't fix it*, the target
   stance, and the recommended command (e.g. `/interpret` on E006).
5. **Never** auto-spawn the stance. **Never** adopt a number a reader computed — the existing honesty
   floor already blocks citing an unrecorded number; the recompute is carried in the handoff as
   `proposed_unverified`, to be born in `/work`/`/interpret`.

---

## C · The cross-stance trigger taxonomy

A finding is `NEEDS-STANCE` **iff no rewording within the currently recorded evidence could resolve it.**

Distinguishing axis for the two "number" rows (1 vs 4): **does a cited number already exist?** Row 1
*corrects/re-judges an existing record*; row 4 *records a new one*.

| # | Finding type | Caught by | Routes to | What that stance must produce |
|---|---|---|---|---|
| 1 | A **cited number is broken OR its aggregation/contrast is contested** (pseudoreplication / wrong unit / artifact / wrong bootstrap unit) — the number *exists* | F13 panel · F5 · F9b · `stat-aggregation-auditor` | `/interpret` (re-adjudicate) → `/work` (recompute if needed) | a corrected/re-judged recorded number + an `evidence_status` decision |
| 2 | A **load-bearing claim has no recorded evidence** the argument needs | F3 (`\gap`) · F4 (broken warrant) | `/work` | the experiment / the recorded result |
| 3a | A claim **contradicts another report / cross-section number** (internal) | F4 grounding · F19 cross-artifact | `/interpret` (or `/review`) | an adjudicated reconciliation |
| 3b | A claim **contradicts an external source** (literature) | F4 grounding (external) | `/scout` (pull the source) → `/interpret` | the source, then the adjudication |
| 4 | A **new number surfaces during writing** (a reader recompute) — no cited number existed | any computing reader | `/work` to record, then resume | the number, born and recorded |
| 5 | A **related-work / literature claim needs a source we lack** | F4 grounding (external) | `/scout` (lit-scout) | the canonical note / citation |
| 6 | A **frame / scope decision only the human owns** (basic-science vs technology) | F5 frame · F2 | `/plan` / human gate | a decision, recorded |
| 7 | A **cited result was recorded but never adjudicated** (no panel verdict) | `evidence_status` extension | `/interpret` | the adjudication |

**Anchor:** row 1 = the **E006 voxel-bootstrap CI** = the regression seed for this addition (Claudio's-4-
sentences analog). Note it is the *contested-aggregation* form, not "the number is wrong" — the gap is the
bootstrap unit (voxel vs fold), which only re-judging settles; this is why `stat-aggregation-auditor` is
named as a co-detector and the route is `/interpret`-first.

**Boundary rules (the over/under-routing guards):**
- **Over-routing guard:** if a reword *within recorded evidence* resolves the finding → `WRITING-REVISE`,
  not a handoff. (A merely-hard sentence is not a handoff.)
- **Under-routing guard:** a panel objection that is `SURVIVES-IF-NARROWED` / `DOES-NOT-SURVIVE`, where
  the narrowing needs a number or claim **not in `docs/`**, is `NEEDS-STANCE` — it may **not** be silently
  narrowed in prose. (This is the exact dry-run trap: the panel's fold-level CI recompute.)
- **Fail-safe direction (L059):** on ambiguity, fail toward `NEEDS-STANCE` (block + surface), never toward
  `WRITING-REVISE`. Papering-over is the dangerous failure; over-routing is caught cheaply at the human
  gate (the human can always say "no, just reword").

**Where the classification lives (M3 — self-tag + a mechanical backstop):** each **reader tags its own
finding** with `{class: writing-revise | needs-stance, target_stance?, why_not_writing?}` as the first,
cheap, expert pass. But self-tagging is weak in the dangerous direction: a *voice* or *structure* reader
that meets a substrate defect is the one most likely to file it as `writing-revise` in its native frame,
and that mislabel is otherwise invisible. So the orchestrator runs a **deterministic backstop** over the
aggregated findings: **any panel verdict that is `SURVIVES-IF-NARROWED` or `DOES-NOT-SURVIVE`, where the
narrowing needs a number/claim not in `docs/`, is FORCED to `needs-stance` regardless of how a reader
tagged it.** (This is the under-routing guard made mechanical — it is exactly what catches the E006
anchor, which the F13 panel surfaces as `SURVIVES-IF-NARROWED`.) The DET/RUB split: *classifying* is RUB
(readers judge); the *consequence* and the *backstop force-rule* are DET.

**Boundary rules (the over/under-routing guards):**
- **Over-routing guard:** if a reword *within recorded evidence* resolves the finding → `WRITING-REVISE`,
  not a handoff. (A merely-hard sentence is not a handoff.)
- **Under-routing guard:** see the M3 backstop — a panel narrowing that needs out-of-`docs/` material is
  `needs-stance`, mechanically, not at a reader's discretion.
- **Fail-safe direction (L059):** on ambiguity, fail toward `needs-stance` (block + surface), never toward
  `writing-revise`. Papering-over is the dangerous failure; over-routing is caught cheaply at the human
  gate ("no, just reword").

**Boundaries with existing mechanisms (do not overlap or regress):**
- **F16 gate (S2):** `needs-stance` is a **third stage-5/6 exit** alongside *converge* and *logic-revision-
  re-enters-the-gate*. A handoff is **stronger** than gate re-entry: the human cannot *approve away* a
  missing/broken number at F16. Emitting a handoff does **not** by itself void the F16 approval (a handoff
  need not change a gated field); it blocks **ship**, via the `handoffs-open` blocker, until resolved.
- **`evidence_status: suspect` (M2):** a genuinely **new enum value**, distinct from `demoted`/`superseded`
  (those mean *a newer verdict overruled this*; `suspect` means *no verdict has overruled it but a reader
  has reason to doubt it*). It is a schema + `claim_binding.py` change and **belongs in the STALE set**
  (citing a `suspect` number as live → DET flag — that is what makes the lesson sticky across sessions).
  **Who writes it:** `/write` only **emits the handoff recommending** it; `/interpret` **proposes**
  `suspect`; the actual write to the register and any rung consequence stay with `/work` + Erfan. `/write`
  never stamps a status (it touches no number).
- **The "framing-sentence escape" (S3):** this addition does **NOT** close that known hole — a load-bearing
  assertion never *entered as a claim* is invisible to both the Trust floor and this detector. The human
  gate remains the only catch. (Stated so no one assumes the handoff detector subsumes it.)
- **`\gap` (S4):** row 2 **complements** `\gap`, does not replace it — write the honest `\gap` in the prose
  now *and* emit a handoff to go fill it. The handoff is the routing; the `\gap` is the honest in-prose
  acknowledgment. Neither removes the other.

---

## D · Functionality-matrix addition

**F20 — Cross-stance handoff (router + artifact + convergence blocker).** Orchestration; sits at a new
**stage 5.5**, between the stage-5 audit and the stage-6 revise loop.

| Field | Value |
|---|---|
| In plain words | When an auditor finds a defect the prose can't fix, route it to the right stance and stop. |
| Stage · concern | 5.5 · *orchestration* (no concern color; like F14 revise / F16 gate) |
| Input | the aggregated stage-5 reader findings (each self-tagged `class`) + the F13 panel verdicts |
| Output | per finding: a confirmed class; per `needs-stance` finding: a **handoff record** in `.claude/state/sw-gate/handoffs.json`; convergence + ship blocked while any handoff is `open` |
| DET half | (a) the **`handoffs-open`** convergence blocker (8th gate in `verdicts.py`, keyed to handoff-resolution, not prose-hash — M1); (b) the **backstop force-rule** (panel `SURVIVES-IF-NARROWED`/`DOES-NOT-SURVIVE` + out-of-`docs/` narrowing → `needs-stance`, M3); (c) a **handoff-schema** check (every `needs-stance` finding has a well-formed record); (d) **ship blocked** while any handoff is `open` |
| RUB half | the **classification** (writing-revise vs needs-stance, and the target stance) — readers self-tag + router judgment |
| Seed scenario | the E006 CI → `needs-stance(/interpret)`, handoff emitted, convergence blocked, prose NOT narrowed with the recompute |

**Handoff record schema** (in `.claude/state/sw-gate/handoffs.json`):
```
{ handoff_id, finding (file:line + rule), threatens_claim (claim_id), why_not_writing,
  target_stance (work|interpret|review|scout|plan), what_to_produce, recommended_command,
  proposed_unverified (a reader's recompute, NEVER adopted into prose) | null,
  status: open | resolved, resolution_ref (the recorded upstream output that closed it) | null }
```

**Supporting changes (not new F-numbers — extensions to existing functionalities):**
- **`evidence_status: suspect` (M2) — add at ALL FOUR sites or a `suspect` claim trips the schema floor
  instead of the stale flag (MF1):** `lattice_integrity.py` `EVIDENCE_STATUS`, `claim_binding.py` `STALE`
  (citing it as live → DET flag) **and** the `check_register` resolve-tuple (a recorded suspect key, like
  live/demoted), `LATTICE.md`, and the evidence-register's allowed `status` values. Set by `/interpret`
  (proposes) → `/work`+Erfan (records); never by `/write`.
- **ONE store for handoffs (ponytail / review-3 MF-C):** handoffs live ONLY in
  `.claude/state/sw-gate/handoffs.json` (keyed by `handoff_id`), carrying the full record incl.
  `threatens_claim` — **not** a lattice field. This deletes the two-store sync contract and the `TOP_KEYS`
  collision (MF-B) outright. `lattice_integrity` is therefore **unchanged for handoffs** (it changes only
  for the `suspect` enum).
- **`verdicts.py`:** a `handoff` subcommand — `open` / `resolve <id> --ref <output>` / `status` /
  **`check --lattice L`** (validates every open handoff's `threatens_claim` against the lattice's claim ids
  — the NH4 dangling-handoff guard, now living with the store, not in `lattice_integrity`) — plus the
  `handoffs-open` clause inside `status()` (NOT an 8th `REQUIRED` reader) and the `ship` refusal (§F).
- **SKILL.md:** a **stage 5.5 · Handoff triage** section (a documentation label — triage runs within
  stage 5 before stage 6; `5.5` is **never** written to `meta.stage`, which is a validated int 1–6, NH3).

## E · Scenarios (TDD — `SC-XSTANCE-*`)

`DET` = assertable; `RUB` = judge-graded. Seeded from the dry-run (the anchor) + one per trigger row +
the two false-direction guards + the two DET keystones.

| ID | tests | D/R | INPUT | EXPECT | grounded |
|---|---|---|---|---|---|
| SC-XSTANCE-01 | F20 | RUB+DET | central claim cites E006's voxel-bootstrap CI; F13 panel = `SURVIVES-IF-NARROWED`, narrowing needs the unrecorded fold-level CI | finding **forced** to `needs-stance(/interpret)` by the backstop; handoff names E006 + `stat-aggregation-auditor`; convergence blocked; prose **not** narrowed with the recompute; recompute carried as `proposed_unverified` | **the dry-run, verbatim** |
| SC-XSTANCE-02 | F20 row 2 | RUB+DET | a load-bearing claim has no recorded evidence (a `\gap` a warrant depends on) | `\gap` **stays in prose** AND a `needs-stance(/work)` handoff emitted; convergence blocked; nothing invented | `\gap` + row 2 |
| SC-XSTANCE-03 | F20 row 3a | RUB | two reports give different numbers for one quantity (F19 cross-artifact) | `needs-stance(/interpret)` handoff; not silently picking one | row 3a |
| SC-XSTANCE-04 | F20 row 5 | RUB | a related-work claim cites a paper not in `canonical/` | `needs-stance(/scout)` handoff | row 5 |
| SC-XSTANCE-05 | F20 row 6 | RUB | a finding is sold in the technology frame but the frame is genuinely undecided | `needs-stance(/plan)` / surfaced at the human gate | row 6 |
| SC-XSTANCE-06 | F20 row 7 | RUB | a claim cites a result recorded but never adjudicated (no panel verdict) | `needs-stance(/interpret)` | row 7 (RUB — "adjudicated?" is a judgment, no new enum) |
| SC-XSTANCE-07 | F3 suspect | DET | after `/interpret` marks E006 `suspect`, a NEW `/write` run cites E006 as live | `claim_binding` DET-flags it (suspect ∈ STALE); must rebind/resolve | M2, sticky lesson |
| SC-XSTANCE-08 | F20 guard | RUB | a finding that IS writing-fixable (a scope over-read a reword within recorded evidence fixes) | classify **`writing-revise`, NOT a handoff**; goes to the revise loop | over-routing guard (false-positive) |
| SC-XSTANCE-09 | `handoffs-open` | DET | a `needs-stance` handoff is open; the agent rewords the prose (new hash) and re-records the reader `ready` | convergence **still blocked** — a reword cannot resolve a handoff (only the upstream recorded output can) | **M1 regression** |
| SC-XSTANCE-10 | `handoffs-open` | DET | the upstream stance records its output, marks the handoff `resolved`, AND the claim is rebound; readers ready | convergence **passes** — only after real resolution + rebind | M1 happy path |
| SC-XSTANCE-11 | F20 row 3b | RUB | a related-work claim **contradicts** a paper not in `canonical/` (not mere absence) | `needs-stance(/scout)` → `/interpret` (pull, then adjudicate) | row 3b |
| SC-XSTANCE-12 | F20 row 4 | RUB+DET | a reader **computes a number** that no cited record contained | `needs-stance(/work)` to record it; the number carried `proposed_unverified`; honesty floor blocks citing it until recorded | row 4 |
| SC-XSTANCE-13 | two-gate | DET | a handoff is `resolved` but a reader still returns `ready_to_ship:false` (a real prose defect remains) | convergence **still blocked** by the reader — handoff-clear ≠ converged (the two gates are independent) | MF2 independence |
| SC-XSTANCE-14 | `handoff check` | DET | an open handoff's `threatens_claim` is deleted by a re-skeleton | `verdicts.py handoff check --lattice` flags the dangling `threatens_claim` (no unkillable orphan handoff) | NH4 |
| SC-XSTANCE-15 | `handoffs-open` | DET | two open handoffs; one resolved, one still open | convergence **still blocked** until **all** clear | NH1 multiple |
| SC-XSTANCE-16 | F20 guard | RUB | F13 = `SURVIVES-IF-NARROWED` **but the narrowing IS satisfiable within `docs/`** (a recorded result already supports the narrower claim) | classify **`writing-revise`** (narrow in prose), **NOT** `needs-stance` — the backstop fires only on out-of-`docs/` narrowings | over-routing guard (in-`docs/` side of M3) |

**Negative anchors:** SC-XSTANCE-08 and -16 are to over-routing what the SC-VOICE near-misses are to the
voice linter — they pin that a merely-hard-but-writing-fixable finding (08) and an in-`docs/`-satisfiable
narrowing (16) are NOT handoffs. -16 specifically tests the *in-`docs/`* side of the M3 backstop, the
boundary the whole force-rule turns on.

## F · Projection onto Claude Code

Like F16 (gate), **F20 maps to MULTIPLE primitives**, not one (NH3):

| Piece | CC primitive | New / reuse |
|---|---|---|
| stage-5.5 triage orchestration | **SKILL** section (doc label "5.5"; never written to `meta.stage`) | build |
| handoff records + resolution state (ONE store) | **ARTIFACT** — `.claude/state/sw-gate/handoffs.json`, keyed by `handoff_id` | build |
| classification (writing-revise vs needs-stance + target) | the 7 **SUBAGENT** readers self-tag + orchestrator | reuse readers |
| the M3 backstop force-rule | **SKILL**/orchestrator DET step over aggregated findings | build |
| `handoffs-open` convergence + `handoff open/resolve/status/check` | **HOOK-adjacent** — `verdicts.py` | extend |
| `handoff check --lattice` (threatens_claim resolves to a claim) | **`verdicts.py`** (lives with the store, not `lattice_integrity`) | build |
| `evidence_status: suspect` | **HOOK** — `lattice_integrity` enum + `claim_binding` STALE/register | extend |
| surface the recommendation to the human | **GATE**-surface (the existing F16/AskUserQuestion path or a plain summary); **never** auto-spawn | reuse |

**M1 realized, precisely (MF2):**
- Handoff state lives in `.claude/state/sw-gate/handoffs.json` keyed by `handoff_id` — **not** under
  `verdicts/<prose-hash>/`. That hash-independence **is** the sticky property.
- `verdicts.py status` converged-iff becomes: **(all 7 readers `ready_to_ship` for the current prose-hash)
  AND (zero handoffs with `status:open`).** The handoff check is an **added clause in `status()`**, NOT an
  8th entry in `REQUIRED` (adding it to `REQUIRED` would re-key it to the prose-hash and defeat M1).
- A prose edit changes the prose-hash → the 7 readers go stale → but `handoffs.json` is untouched → still
  blocked. The reword cannot clear it. ✔ (SC-XSTANCE-09)
- `verdicts.py handoff open <id> …` writes an open record; `handoff resolve <id> --ref <recorded-output>`
  flips it to `resolved`.
- **`ship` must REFUSE with an open handoff — enforced, not procedural (MF-A).** Today `ship` calls
  `clear_gate_state` unconditionally, and `accept-residual` suppresses the Stop-hook while leaving
  `handoffs.json` untouched — so without a guard a human could `accept-residual` → `ship` and silently wipe
  an open handoff. Fix: **both `ship` AND `accept-residual` first check open handoffs and exit nonzero,
  listing them, if any are open** (a handoff is not a "residual" the human may wave through — only its
  upstream stance closes it). Only then does `ship` clear `handoffs.json` alongside
  active/blocks/residual/verdicts. **You cannot `ship` or `accept-residual` past an open handoff.**
- **The Stop-hook needs NO change** — it already calls `status`; the new clause rides inside it (free).
- **No-op invariant (must be a selftest, NH):** a **missing** `handoffs.json` reads as zero-open, so
  `status` is unchanged for every existing draft and all current selftests. This is the load-bearing
  "doesn't break the existing guarantee" property — assert it explicitly.

**Resolution contract — two independent gates (MF3):**
- A handoff **resolves** when the upstream stance **records** its output; `resolution_ref` points to it
  (an experiment key `E006` · a decision id `D050` · a commit hash · an `evidence_status` change).
- Resolving the handoff clears only the `handoffs-open` clause. The draft **still** will not converge until
  the writer **rebinds the lattice claim** to the corrected evidence (so `claim_binding` passes) and the
  readers re-run clean — a **logic revision that re-enters the F16 gate**. (SC-XSTANCE-13 pins this
  independence.) The transient `claim_binding` **`status-mismatch`** (claim says `live`, register now says
  `suspect`) is **intended** — it keeps blocking until the rebind. So: `/interpret` records → handoff
  `resolved` → writer rebinds (re-gate) → readers re-run → converge.

**Handoff record fields (NH4 — completed):** `{ handoff_id, finding (file:line+rule), threatens_claim,
why_not_writing, target_stance, what_to_produce, recommended_command, proposed_unverified|null,
resolution_ref (experiment-key | decision-id | commit | status-change) | null, status: open|resolved,
opened_by_reader, detected_at (session/timestamp via the recording call) }`.

## G · Reverse coverage check (2d)

Every `SC-XSTANCE-*` EXPECT walked against its mapped primitive:

| Scenario | EXPECT satisfiable by | OK? |
|---|---|---|
| 07 (suspect sticky) | `claim_binding` (suspect ∈ STALE) DET | ✔ |
| 09 / 10 / 13 / 15 (handoffs-open) | `verdicts.py status` handoff clause DET | ✔ |
| 14 (dangling handoff) | `verdicts.py handoff check --lattice` DET | ✔ |
| 12 (new number) | existing honesty floor (can't cite unrecorded) + handoff DET | ✔ |
| 01 (anchor) | **DET half** = M3 backstop force-rule; **RUB half** = F13 panel judgment | ✔ |
| 02 / 03 / 04 / 05 / 06 / 08 / 11 / 16 | reader classification (RUB) + orchestrator | ✔ (judge-graded) |

**Confirmed clean:** every pure-DET scenario maps to a real check; no DET scenario secretly needs a judge.
The two over-routing guards (08, 16) are RUB — they cannot be pure-DET regression anchors, **but** the
load-bearing assertable part (the in-`docs/` vs out-`docs/` boundary the M3 force-rule turns on) is testable
via 16's setup vs 01's.

**Meta-finding (the 2d-style symmetry):** the recurring shape here is **"RUB classifies, DET enforces the
consequence"** — the fluidity boundary applied to routing. The reader *judges* whether a finding is a
substrate problem (fluid); the `handoffs-open` blocker, the backstop force-rule, the `handoff-ref` check,
and `suspect ∈ STALE` *enforce* the consequence (rigid). Same DET-floor/RUB-judge line the whole pipeline
runs on.

**Honest limits (carried forward, not closed):**
- This does **NOT** close the **framing-sentence escape** — a load-bearing assertion never entered as a
  claim is invisible to the detector; the human gate remains the only catch.
- The classification is RUB, so a reader *could* mislabel a needs-stance finding as writing-revise —
  **except** where the M3 backstop fires (a panel `SURVIVES-IF-NARROWED`/`DOES-NOT-SURVIVE` needing
  out-of-`docs/` material is mechanically forced). So the guarantee is: **panel-detectable science
  problems are mechanically caught; non-panel ones rest on reader honesty + the human gate.** Stated so the
  guarantee is not over-read.

## H · Build chunks (for next session, alongside P3 — the three-net loop per chunk)
Single-store collapse merged the old X2+X3 → four chunks. Each: *embedded selftest → opus oracle → fresh
`claude -p` clean-room → atomic commit + build-log entry.* Dependency order X1 → X2 → X3 → X4.
- **X1** — `evidence_status: suspect` at all four sites (`lattice_integrity.EVIDENCE_STATUS`,
  `claim_binding.STALE` + `check_register` tuple, `LATTICE.md`, register) (SC-07).
- **X2** — `verdicts.py`: the `handoffs.json` store + `handoff open/resolve/status/check --lattice` + the
  `handoffs-open` clause in `status()` + the `ship`/`accept-residual` refusal + the **no-op-when-missing**
  selftest assertion (SC-09/10/13/14/15). No `lattice_integrity` change (single store).
- **X3** — SKILL **stage-5.5 triage** section: reader self-tag schema, the M3 backstop force-rule, the
  handoff emit + human surface, the two-gate rebind contract (SC-01/02/03/04/05/06/08/11/12/16).
- **X4** — wire the regression anchor (SC-XSTANCE-01 = the dry-run) end-to-end; fold all 16 `SC-XSTANCE-*`
  into the suite (119 → 135) and the coverage table.
