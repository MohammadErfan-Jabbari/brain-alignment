---
title: "Agent-fleet redesign — proposal (S24)"
tags: [reference]
---

# Agent-fleet redesign — proposal (S24)

**Status:** PROPOSAL for Erfan to review. **Nothing implemented.** Synthesis of two parallel audits of the repo's session corpus (2026-06-18): a timeline-narrative workflow (`repo-agent-audit`, 6 agents) + an empirical transcript-mining pass over all **266 subagent runs / 27 sessions**, plus the precedent-engine reference session (`b17c635e`). Every line is specific enough that applying it is mechanical.

**The fleet today (on disk):** 9 agents — `counter-argument`, `socratic-thinker`, `premortem-analyst`, `first-principles-grounder`, `oracle-reviewer`, `lit-scout`, `paper-digest`, `session-logger`, `wrap-auditor`. 3 commands — `/orient`, `/wrap`, `/goalsmith`. One hook — `wrap_session_snapshot.py`. No `.mcp.json`.

**Governing principle (from the precedent):** *when an agent holds two roles at once, the weaker role colonizes the stronger one.* Most frictions are fixed by adding a *behavior* to an existing agent or a command/hook — not by a new agent. Build an agent only when it removes a *priced* recurring cost.

**How the two audits relate:** the narrative pass sees costs paid in the *main loop* (re-derivations, the $374 stat error) → reasoning agents. The mining pass sees costs paid in *subagent spawns* (frequency) → mechanical agents + routing violations. The merged list below keeps both and marks which pass surfaced each.

---

## 1. Atomic-subagent fleet (merged)

| # | Name | Purpose | Model | Source | Decision |
|---|---|---|---|---|---|
| 1 | `stat-aggregation-auditor` | After a multi-arm/seed run, before the verdict: check aggregation matches hypothesis structure (within-seed vs pooled, paired vs unpaired, bootstrap-unit vs pseudo-replication, P-construction reproducibility). | opus | narrative | **BUILD.** The single most expensive error class: the E021-v4 "null" off a pooled regression that within-seed contradicted (the $374 session); + L047 P-construction sensitivity, L015/L016 pseudo-replication. `counter-argument` *names* this risk but never *recomputes*. Genuinely missing. |
| 2 | `anti-confound-designer` | At Claim→Design, *before* oracle: emit the full control battery — nuisance checklist + contiguous-split spec + capacity-fair PCA + matched-ppl/budget stop rule + bpb/in-distribution check. | opus | narrative | **BUILD.** Most-repeated re-derivation (L011/L012/L003 rebuilt at E001/E003/E004/E005/E006 and again for E021's shape-twin). Splits *assemble* from oracle's *critique* (oracle was doing both). Absorbs the would-be `metric-unit-validator`. |
| 3 | `dataset-verifier` | Given a dataset path: confirm the **neural response matrix** (not stimuli-only) is present, report shape, flag L005-class gaps; for TRIBE/LeBel probe the voxel mapper + audio-timestamp sanity. | sonnet | both | **BUILD.** L005 (stimuli≠fMRI) re-verified S2/S4; denizenslab git-annex wall blocked I3/F1/F3 across S12–14; TRIBE 11× timestamp bug (L037). "Is the substrate usable" — no agent touches this. |
| 4 | `dataset-scout` | Given a dataset name/paper: research access URL, format, fMRI pipeline, prior brain-encoding use → a structured card. The dataset mirror of `lit-scout`. | sonnet | mining | **BUILD.** 9 runs in the corpus, currently overloaded onto `general-purpose`. Distinct from #3 (verify data we HAVE) — this finds/researches NEW data. High value now (the S24 dataset hunt: ZuCo/CNeuroMod/Broderick/MEG-MASC). |
| 5 | `paper-repo-extractor` | One paper per agent: read its repo, extract data availability/format, preprocessing code, model checkpoints, license → a structured stub. | haiku | mining | **BUILD.** ~20 runs (a 20-agent fan-out in one session), wrongly on `Explore` with unset model. Pure mechanical extraction — distinct from `paper-digest` (comprehension → canonical note, opus). |
| 6 | `provenance-completeness` (wrap-auditor scope) | Walk one experiment `.md`, verify every Results number has an `outputs/*.json` field + a code path; flag measured-but-unsaved + stale headlines. | sonnet | both | **EXTEND wrap-auditor** (not a new agent). E003's 5 provenance gaps survived to S20; L047. Mining's ~20 doc-audit runs confirm the frequency. Make it **mid-session invocable** (see §3-C). |
| 7 | `doc-status-sync` (wrap-auditor scope) | Diff `experiments/E*.md` Status + report citations against [`ladder.md`](../ladder.md) verdicts + [`learnings.md`](../learnings.md) retractions → patch list (read-only). Calls the existing `scientific-writing/check_number_consistency.py`. | sonnet | both | **EXTEND wrap-auditor.** Most persistent friction: ~8 stale Status lines open S9→S15; E015 `r≈−0.92→−0.78` drifted 2 sessions. Folds R1's doc-status/number-propagation/retraction checkers into one. |

**SKIP as agents (lighter form instead):**
- `panel-consolidator` → a `/goalsmith` goal-string clause + a `/wrap` reconcile step (§2). A consolidator is not a thinker; making it one is the two-roles anti-pattern.
- `working-tree-commit-guard` → a `/orient` step (3-line `git status`).
- `stop-hook-intent-arbiter` → a Stop **hook** (L031 is already a CLAUDE.md rule; an agent can't own a turn-level decision).
- `metric-unit-validator` → folded into `anti-confound-designer` (#2).
- `experiment-runner` (mining, ~14 runs incl. the E021 4-retry chain) → **SUBSUMED by the new `/goal` loop**: build→run→fix→rerun-until-resolved is exactly what `/goalsmith`→`/goal` now provides. The retry-chain friction is the thing `/goal` eliminates; no agent needed.
- `content-miner` (mining, ~19 runs) → **defer**: too generic (risks just renaming `general-purpose`); revisit only if a *specific* extraction recurs with a fixed schema.
- `study-note-writer` (mining, ~6 runs) → **defer**: concentrated in one session; build if new coursework recurs.

**Net: build 3 reasoning/data agents (`stat-aggregation-auditor`, `anti-confound-designer`, `dataset-verifier`) + 2 mechanical (`dataset-scout`, `paper-repo-extractor`); extend `wrap-auditor` with 2 scopes; skip 7 in favor of command/hook/clause forms.**

---

## 2. Commands

**New `/precheck`** — the pre-compute gate (design-side mirror of `/wrap`): fans out `anti-confound-designer` (assemble battery) → `oracle-reviewer` (gate the now-complete design) → `READY-TO-RUN: YES/NO`. Makes "assemble→gate" one reproducible call.

**`/orient`** — add (a) uncommitted-tree report (`git status --porcelain`; warn on stray work — S17's uncommitted R06/E002/E006); (b) missing-wrap detector (commits after the last `timeline/` entry → "previous session may not have `/wrap`ped" — S16 skipped wrap → a full reconciliation session).

**`/wrap`** — add the 2 new `wrap-auditor` scopes (#6/#7); **verify the auditor swarm dispatches in one parallel fan-out** (S18 built it; parallelism unconfirmed); extend the opus-only-when-an-experiment-ran routing to the provenance scope.

**`/goalsmith`** — add a **panel-clean clause** to the goal-string template: *"panel-clean = every thinker's structured verdict block is collected and a single PANEL-CLEAN:YES reconciles them; contradictions (e.g. counter-argument SURVIVES vs premortem TOP-RISK-VISIBLE-NOW:YES) are resolved, not averaged."* Makes "survived the panel" checkable by the `/goal` evaluator via a single token.

---

## 3. Architecture / structure problems

- **A. Pre-compute vs post-result agents mixed in the CLAUDE.md table.** `oracle-reviewer` is invited to run post-result with a design-shaped prompt. **Fix:** BEFORE/AFTER labels in each agent's `description`; split the table into "Pre-compute gate" vs "Post-result panel."
- **B. Confound catalog duplicated in `counter-argument` + `oracle-reviewer`.** A new L-entry must be edited twice or they drift. **Fix:** extract to `docs/references/confound-catalog.md` (seed from L003/L011/L012/L013/L014); all three (incl. `anti-confound-designer`) read it. One source of truth.
- **C. `wrap-auditor` scopes only reachable from `/wrap`.** Provenance/doc-status are needed *mid-session* (when a verdict flips) — why E015's number drifted 2 sessions. **Fix:** make `wrap-auditor` independently invokable with `--scope`.
- **D. No `.mcp.json`.** Research agents rely on the global Exa/Firecrawl config. **Fix:** add a project `.mcp.json` wiring Exa so a fresh checkout reproduces them.
- **E. "Panel-clean" undefined / unowned.** Fixed by §2's `/goalsmith` clause + `/wrap` reconcile note; flagged here as the structural gap.
- **F. `lit-scout` doesn't state read-only/no-judge or its model tier.** **Fix:** (a) "finds and ranks papers, does not judge their claims (the panel's job)"; (b) routing note (Erfan, S24) — "**default sonnet** for gathering / breadth scouting (low judgment); **opus only** when judging relevance or analyzing a specific paper."
- **G. (mining) Nothing enforces model-routing at spawn time — and the rule itself needs refining (Erfan, S24).** Routing follows the *judgment the task needs*, not a blanket per-agent tier. **`lit-scout` is task-dependent** (sonnet to gather, opus to analyze a specific paper) — so the mining's "33× sonnet" is *mostly the correct call*: the real violations are **paper-digest on sonnet (24×)** — always comprehension+synthesis → opus — and **fable (41×, banned)**. `lit-scout` on sonnet (9×) is fine when it was gathering. **Fix:** (1) refine the CLAUDE.md routing rule to state lit-scout's task-dependence; (2) a PreToolUse hook on Task/Agent spawns that **hard-flags `fable`** and flags `paper-digest`/thinker/`oracle-reviewer` spawns not on opus, but **does NOT blanket-flag `lit-scout`** (its tier is the caller's task-judgment call).

---

## 4. Thinker-agent prompt updates to match goalsmith (the centerpiece)

Goal: every thinker (a) **verifies each objection against the data**, (b) for a null/shortfall **grounds the why in theory ([`06-theory-grounding.md`](../06-theory-grounding.md)) or literature**, (c) **emits a machine-readable verdict block** the `/goal` resolve-or-root-cause evaluator can consume. Common spine = goalsmith's two-branch DONE: **(A)** confirmed-with-value-CI-n-test-panelclean, or **(B)** root-caused to IMPLEMENTATION-BUG vs THEORY-NULL vs SCOPE-MISMATCH. Each block is an *append* to the named agent's `## Return` section.

### `counter-argument.md` (replace the four Return bullets)
```
- Strongest single attack — labeled VERIFIED-AGAINST-DATA (you read the number in outputs/ or
  experiments/ and it holds) | SPECULATIVE. Never report an attack without checking the number it rests on.
- 2-4 secondary attacks, ranked, each with confound/flaw + evidence line + VERIFIED|SPECULATIVE.
- For each surviving VERIFIED attack: the neutralizing control + root-cause fork —
  (A) IMPLEMENTATION-BUG (name script/split/seed; hunt & re-run), (B) THEORY-NULL (cite a theorem in
  06-theory-grounding.md or a paper in docs/literature/canonical/), or (C) NEEDS-CONTROL (name it).
- Verdict block (last line): PANEL-VERDICT: counter-argument | OBJECTIONS-SURVIVING: <n> |
  OBJECTION-i: <line> | VERIFIED|SPECULATIVE | ROOT-CAUSE: IMPL:<x>/THEORY-NULL:<cite>/NEEDS-CONTROL:<x> ... |
  CONCLUSION-STATUS: SURVIVES|SURVIVES-IF-NARROWED|DOES-NOT-SURVIVE | NARROWING: <one sentence>
```

### `socratic-thinker.md` (append a second phase; add `WebSearch, WebFetch` to tools)
```
After the question tree, take the single most direction-threatening question and ATTEMPT TO ANSWER IT
from repo evidence (docs/experiments/, outputs/, 06-theory-grounding.md, docs/literature/canonical/):
  ANSWERED-SAFE: <answer> (cite file:line) | ANSWERED-RISKY: <exposes a real gap> | UNANSWERABLE-FROM-REPO: <what would answer it>
- Verdict block: PANEL-VERDICT: socratic-thinker | CRITICAL-ASSUMPTION: <hidden premise> |
  CRITICAL-QUESTION: <it> | QUESTION-STATUS: ANSWERED-SAFE|ANSWERED-RISKY|UNANSWERABLE-FROM-REPO | IMPLICATION: <line>
(Keep "ask, don't answer" for the tree; the second phase answers only the one load-bearing question.)
```

### `premortem-analyst.md` (append per-premortem data-check)
```
For each premortem add: DATA-CHECK: is this leading indicator visible in the repo NOW? (read outputs/ /
experiments/) → VISIBLE-NOW (file:line + number) | NOT-YET-VISIBLE | REQUIRES-NEW-RUN.
  ROOT-CAUSE-TYPE: IMPLEMENTATION (code/split/seed) | THEORY-NULL (cite) | SCOPE-MISMATCH.
- Verdict block: PANEL-VERDICT: premortem-analyst | TOP-RISK: <headline> |
  TOP-RISK-VISIBLE-NOW: YES(file:line)|NO|PARTIAL | TOP-RISK-ROOT-CAUSE: IMPL|THEORY-NULL:<cite>|SCOPE-MISMATCH |
  MITIGATION-BEFORE-NEXT-STEP: <single action>
```

### `first-principles-grounder.md` (append root-cause classifier)
```
- Root-cause classification for NOT-GROUNDED/GROUNDED-WITH-CAVEAT: (A) THEORY-NULL (math/lit predicts this
  — cite — CLOSES the question, no re-run), (B) IMPLEMENTATION-ARTIFACT (name it; warrants re-run), or
  (C) OPEN-THEORY-QUESTION (name the derivation/paper that would settle it).
- Verdict block: PANEL-VERDICT: first-principles-grounder | THEORY-STATUS: GROUNDED|GROUNDED-WITH-CAVEAT|NOT-GROUNDED |
  CITED-TOOL: <theorem/course-note file:line/canonical slug> | ROOT-CAUSE-TYPE: THEORY-NULL|IMPLEMENTATION-ARTIFACT|OPEN-THEORY-QUESTION |
  RESOLUTION: <one sentence — re-run or close>
```

### `oracle-reviewer.md` (add a second operating mode — fixes §3-A)
```
## Operating mode
Decide from the input: DESIGN review (no result numbers — standard flow) or RESULT review (a run
completed; numbers in outputs/ or experiments/). For a RESULT, REPLACE the "operational specificity"
and "compute budget" checks with: interpretation validity (does the analysis answer the stated
estimand?); post-hoc flexibility (was the analysis predeclared?); confound residual (what pathway
remains after the controls run? name it); magnitude claim (large enough for the sentence, vs the
noise floor + the Hadidi/Feghhi ≤10% bound?).
RESULT-VERDICT: ACCEPT|ACCEPT-WITH-CAVEAT|REJECT | FATAL-GAPS: ... | CONFOUND-RESIDUAL: ... |
WHAT-WOULD-UPGRADE: ... | WHAT-WOULD-KILL: ...
```

**New thinker agent: none.** The gaps are behavioral inside existing agents; consolidation is a `/goalsmith` clause + `/wrap` step, not a 5th thinker.

---

## Implementation order (highest documented-cost-removed first)
1. **§4 prompt blocks (5 agents) + §2 `/goalsmith` panel-clean clause** — pure prompt edits, no new files; closes the goalsmith mismatch that touches every working session.
2. **`stat-aggregation-auditor`** — removes the $374 E021-v4 error class.
3. **`/wrap` provenance + doc-status scopes + §3-C mid-session invocability** — removes the multi-session stale-number/Status drift.
4. **`anti-confound-designer` + confound-catalog extraction (§3-B) + `/precheck`** — removes the L003/L011/L012 re-derivation tax.
5. **`dataset-verifier` + `dataset-scout` + `paper-repo-extractor` + `/orient` steps + `.mcp.json` + the routing hook (§3-G)** — data-wall prevention, fan-out mechanization, routing guardrail.

## Empirical grounding (transcript-mining, 266 runs)
`general-purpose` 77 (overloaded), `Explore` 38, `counter-argument` 29, `paper-digest` 25, `first-principles-grounder` 23, `oracle-reviewer` 22, `premortem-analyst` 17, `lit-scout` 14, `socratic-thinker` 7, `wrap-auditor` 5, `codex` 5. Routing: **fable 41×** (banned — real violations), **paper-digest on sonnet 24×** (violation — always opus), **lit-scout on sonnet 9×** = mostly *correct* (gathering mode is sonnet per the S24 task-dependence refinement; only analysis-mode is opus). Thinking panel = 37% of all subagent runs (justifies the §4 investment).

---

## Implementation status (S24 — implemented top-to-bottom on Erfan's go)

**DONE (committed):**
- **§4 thinker/oracle prompt blocks + `/goalsmith` panel-clean clause** — `02be369`. Each thinker now labels objections VERIFIED-AGAINST-DATA vs SPECULATIVE, forks nulls to IMPL/THEORY-NULL/SCOPE-MISMATCH, and emits a `PANEL-VERDICT:` block; oracle gained DESIGN-vs-RESULT mode.
- **The 5 new agents** (`stat-aggregation-auditor`, `anti-confound-designer`, `dataset-verifier`, `dataset-scout`, `paper-repo-extractor`) — `498f658`.
- **`confound-catalog.md` (single source of truth) + `/precheck`** — `e9b3067`.
- **`wrap-auditor` scope upgrades** (number-provenance→provenance-completeness; continuity-docs→doc-status-sync) **+ mid-session invocability**; **`/orient`** working-tree + missing-wrap checks; **`counter-argument`/`oracle-reviewer`** catalog pointers; **`lit-scout`** task-dependent tier + no-judge; **`agent_routing_lint.py`** PreToolUse hook + settings wiring; **CLAUDE.md** routing refinement + new-agent registration — `dad2324`.

**No edit needed:**
- **`/wrap`** already spawns the auditors in one parallel fan-out with sonnet-default + opus-escalation-for-ladder-integrity, and dispatches the five scopes — so the extended scope behaviour (now in `wrap-auditor.md`) flows through automatically. §2's `/wrap` items were already satisfied.
- **§3-A BEFORE/AFTER timing** — already encoded in each agent's description (oracle = DESIGN/RESULT mode, counter-argument = AFTER, anti-confound-designer = BEFORE, stat-aggregation-auditor = AFTER); the cosmetic CLAUDE.md table split was not done (low value).

**DEFERRED (with reason):**
- **`.mcp.json` (§3-D)** — no Exa transport config is findable under `~/.claude` (it comes from the global harness); writing a guessed one risks shadowing the working global Exa. Needs the actual Exa connection details — Erfan to provide/confirm, then it is a 1-file add.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
