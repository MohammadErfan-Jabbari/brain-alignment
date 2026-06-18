# S24 — 2026-06-18: R07/theory analysis → PI/sample-efficiency pivot → /goalsmith + agent-fleet redesign

**Mode:** analysis → tooling/design. **NO experiment ran. NO Q-rung changed (Q0–Q5 stand).**
**Note:** `start.json` `start_sha=9787b97` reflects a mid-conversation resume (HEAD at the 18:26 resume), so diff-since-start covers only the fleet tail; the full arc below is logged from session context.

## The arc

### 1. Analysis on R07 / KD theory
Explained on request: warm- vs cold-init KD (init = the *student's own* pretraining, never "start from the teacher" — impossible across sizes); quantization vs pruning vs distillation (perturb-a-fixed-function vs refit-a-new-one → why only KD breaks the DPI ceiling). Added **`06-theory-grounding.md` row 6** — perplexity-only training and KD are the *same KL objective* against different references; output-KL under-constrains the representation (many-to-one readout) → KD-preservation is empirical, not a corollary. Panel-reviewed (counter-argument + first-principles + prose): demoted the overclaim, hedged to R07's r=−0.88. R07 §design gained a pointer. (commit 512f39e)

### 2. E023 designed
`docs/experiments/E023` — KD objective-vs-quality identification: δ_obj = A_S − f(p_S) (drop below the same-family alignment-vs-ppl manifold); matched-ppl KD−LMft residual in the saturated regime; 6 sub-experiments, predeclared kills, exclusion ledger, cold-vs-warm feasibility fork. DESIGNED, not run. (commit 1c37e5a)

### 3. The S24 forward-direction pivot (Erfan-directed)
Reframe: brain/biosignal as **privileged information (LUPI)** → **sample-efficiency / the learning curve**, not the static encoding-R² metric. It is the charter's original **F2**, returned to with a theory + higher-SNR regimes + a control battery it never had — grounded on all prior work, nothing discarded. Critique loop (counter-argument + lit-scout + Codex): **LUPI is "the bound to beat"** (its fast-rate precondition — low-noise/high-information PI — is likely violated by weak fMRI, so it predicts the null there); the win, if any, lives in **higher-SNR regimes** (ZuCo EEG+gaze, CNeuroMod deep fMRI). Lit: Provodin'24 (LUPI gains can be artifacts → a zeroed-PI control is mandatory), Hollenstein/ZuCo (closest prior art — partial scoop + existence proof), Freteault (the sample-efficiency CONFIRM we already hold, its missing matched-control = our opening). Folded into **`expansion-program.md` §8** + **`idea-tree.md`** (Erfan's calls: extend expansion-program; TRUE-100% Tier 1; headline deferred to results). The **5-control battery** — phase-randomized shape-twin · zeroed/shuffled-PI · did-the-rep-move gate · matched-ppl · **matched-information non-brain teacher (Codex)** — is the contribution even under a full null. (commits d94da33, 9a6454a)

### 4. /goalsmith command (3 iterations)
A repo command that turns one /orient item into the **goal text** for Claude Code's built-in **`/goal`**. Grounded in the official `/goal` docs (read firsthand): the condition IS the directive, a fast model checks it each turn, **≤4000-char** cap. Final form: ONE single-line ≤4000-char condition = directive + **pointer to the PRD (the experiment doc, not restated)** + compressed standing discipline + a **resolve-or-root-cause** DONE condition (hypothesis confirmed, OR shortfall root-caused to a bug, else theory/literature — panel-survived, never a bare null) + a blocker escape (no fixed turn count). Cold-tested on Sonnet (2331 chars, single-line). (commits 1905c25, d157081, f5bf28f)

### 5. Agent-fleet redesign (two-pass audit → implemented top-to-bottom)
Audited the corpus: a narrative workflow (6 agents) + an empirical mining of all **266 subagent runs / 27 sessions** + the precedent-engine reference session. Proposal: `docs/references/agent-fleet-redesign.md`. Implemented:
- **§4 thinker/oracle prompts aligned to goalsmith's resolve-or-root-cause Judge** — VERIFIED-vs-SPECULATIVE labels, IMPL/THEORY-NULL/SCOPE-MISMATCH fork, machine-readable `PANEL-VERDICT` blocks; oracle gained DESIGN/RESULT mode; /goalsmith panel-clean clause. (02be369)
- **5 new agents:** stat-aggregation-auditor, anti-confound-designer, dataset-verifier, dataset-scout, paper-repo-extractor. (498f658)
- **confound-catalog.md** (one source of truth) + **/precheck** (pre-compute gate). (e9b3067)
- **wrap-auditor** scopes (provenance-completeness, doc-status-sync) + mid-session invocability; **/orient** working-tree + missing-wrap checks; **agent_routing_lint.py** PreToolUse hook (unit-tested); **CLAUDE.md** routing refinement (lit-scout task-dependent) + the fleet **self-activation map**. (dad2324, acfe605, + CLAUDE.md self-activation commit)

Empirical findings: model-routing drift (fable 41×, paper-digest-on-sonnet 24×) with nothing enforcing it at spawn → the hook; `general-purpose` was the overloaded catch-all (77 runs).

## NO rung changed
Q0–Q5 stand. No experiment ran; no new science number. The forward direction reopened (a roadmap change in expansion-program §8); the rung verdicts are untouched. Headline (PI/sample-efficiency as thesis-headline vs parallel arm) deferred to results.

## Continuity / open loops
- **Fleet untested in action** — the 5 new agents, the PANEL-VERDICT formats, and the routing hook are built (hook unit-tested) but not yet exercised on a real run; expect small wording fixes next working session.
- **.mcp.json deferred** — no Exa transport config findable under `~/.claude` (it's injected by the global harness); a guessed one risks shadowing the working Exa. Needs the real connection details (then a 1-file add). Recorded in `agent-fleet-redesign.md`.
- **Cost:** ~$400 session (a big tooling/audit + a research pivot bolted onto a long analysis session). Lesson: standalone audits/builds are cheaper + cleaner run in a FRESH session (fresh context); the Workflow tool's fresh-context agents mitigated part of it.
- Memory: saved + gbrain-mirrored "ask specific, not vague, questions."

## Commits
512f39e · 1c37e5a · d94da33 · 1905c25 · d157081 · f5bf28f · 9a6454a · 02be369 · 498f658 · e9b3067 · dad2324 · acfe605 · (+ CLAUDE.md self-activation, + this wrap's records).
