# Upspeed — read first, write last

**Last updated:** 2026-06-18 (S24 — analysis→tooling/design. **NO experiment ran, NO rung changed.** Reopened the forward direction to **brain-as-privileged-information → sample-efficiency** (expansion-program §8); designed E023; built **/goalsmith** + a full **agent-fleet redesign** — the working fleet now self-activates per CLAUDE.md. Handed back for Erfan.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **Forward direction = [`expansion-program.md`](expansion-program.md) §8** (the S24 PI/sample-efficiency trajectory) + [`idea-tree.md`](idea-tree.md). Fleet self-activation map: `CLAUDE.md`. With no task, run `/orient`.

## What this session built (S24)
- **The pivot (Erfan):** brain signal as **privileged information (LUPI)** for the **learning curve / sample-efficiency**, not the encoding-R² metric — the charter's F2 returned to with theory + higher-SNR regimes + a control battery. **LUPI = the bound to beat** (weak fMRI likely violates its precondition; the win, if any, lives in higher-SNR regimes — ZuCo EEG+gaze, CNeuroMod deep fMRI). Critique-loop-hardened (counter-argument + lit-scout + Codex). Full tiered trajectory: **`expansion-program.md` §8**.
- **E023 designed** (KD objective-vs-quality, δ_obj manifold-residual) — not run.
- **/goalsmith** — turns a /orient item into the ≤4000-char single-line **/goal** condition (pointer to the PRD + resolve-or-root-cause completion). Cold-tested.
- **Agent-fleet redesign (implemented):** the thinker/oracle panel now emits machine-readable `PANEL-VERDICT` blocks aligned to goalsmith's resolve-or-root-cause Judge; **+5 agents** (stat-aggregation-auditor, anti-confound-designer, dataset-verifier, dataset-scout, paper-repo-extractor); **/precheck**; **confound-catalog**; **wrap-auditor** scopes + mid-session; **routing-lint hook**; CLAUDE.md **self-activation map**. Spec: `docs/references/agent-fleet-redesign.md`.

## What's next (Erfan's call)
- **Working lane (reopened forward direction):** Tier 1 of expansion-program §8 — **first concrete step = E023a** (build the alignment-vs-ppl manifold, forward-passes only, no training) → `/precheck`-gate E023b. Then the rest of Tier 1, the 5 method ideas, then P1 (ZuCo PI learning-curve).
- **Analysis lane (Erfan, D011):** R08–R14 + the extended manuscript — untouched, still the thesis floor.
- **Calibration:** a strong methodology/negative paper is most likely; a top-venue positive is the tail (real PI must beat all 5 controls + move the rep + bend the curve).

## Blockers / open loops
- **Fleet untested in action** — the 5 new agents + `PANEL-VERDICT` formats + routing hook are built (hook unit-tested), not yet exercised on a real run; expect small wording fixes.
- **.mcp.json deferred** — no Exa transport config findable (global harness); needs the real connection details, then a 1-file add.
- Pre-existing untracked (not ours this session): `untitled.md`, `docs/manuscript/supervisor-email_2026-06.md`, `.claude/worktrees/`.

## Key facts
- **Workflow:** `/orient` → `/precheck` (battery + oracle gate) → `/goalsmith <item>` → paste into `/goal`; after a run, `stat-aggregation-auditor` + the panel → reconcile to `PANEL-CLEAN:YES`; `wrap-auditor` invocable mid-session (single scope).
- **Routing (refined S24):** opus = think/design/judge + `paper-digest`; **`lit-scout`/`dataset-scout` task-dependent** (sonnet to gather, opus to analyze a specific paper); sonnet = doc-nav/eng; haiku = mechanical; **fable banned** (the routing-lint hook nudges).
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. **Git:** `main`, push only when asked.
- **Cost note:** ~$400 session — a big tooling/audit + a research pivot are cheaper run in a FRESH session (fresh context); the Workflow tool's fresh-context agents help.
