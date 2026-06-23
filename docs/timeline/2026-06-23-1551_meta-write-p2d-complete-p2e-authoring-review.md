# 2026-06-23 15:51 — /meta: /write rebuild — P2-D complete + P2-E authoring review

**Stance:** `/meta` throughout (apparatus build + authoring/quality review). No other stance. **NO experiment, NO science number, NO Q-rung change — Q0–Q5 stand exactly as S37.** Session id `1b3b0846-9914-45ab-9ccf-b9d70bdecd10`. Changeset `930f441..HEAD` = 11 atomic commits, 35 files.

## What this session did

Continued the D048 `/write` rebuild (skill `.claude/skills/sci-write-v2/`; the live `scientific-writing` skill stays default until P3). Two blocks:

### P2-D — the CC-power upgrades (Phase 2 COMPLETE). Six atomic chunks, each via the three-net loop (`--selftest` → opus `oracle-reviewer` → fresh `claude -p`/event-pipe verify → commit + build-log entry):
- **P2-D-1** (`da51cba`) — `scripts/verdicts.py`: the stage-5 convergence state machine (D047 content-hash pattern keyed to the **draft prose hash**, sibling of `gate_state.py`). Unified all 7 stage-5 readers on `<TAG>-VERDICT: {ready_to_ship, findings}`. 30-check selftest. Oracle ACCEPT-WITH-CAVEAT (MF-2 contradiction fail-safe fixed; B1–B8 folded).
- **P2-D-2** (`7b04caf`) — SKILL stage-5 rewrite: 7 readers fanned out in ONE message, F18 after; record each verdict + synthesize `premortem`; `verdicts.py status` for convergence. Oracle fixed M1–M4 (ternary `SURVIVES-IF-NARROWED`; findings≠0 when not-ready; fold premortem-analyst TOP-RISK; ACK from stage-5 re-run; canonical F8b draft path). Fresh `claude -p` 5/5.
- **P2-D-3** (`7bc50ca`) — `.claude/hooks/stop_sw_converge.py`, wired live in `settings.json`: blocks turn-end until the armed draft converges. Pipeline-scoped + session-scoped, fail-INERT (no-op without `active.json`). **Oracle first pass REJECT — a real catastrophe**: the session guard failed toward *enforce* on a falsy session id → could block an unrelated session (repo-wide outage). Fixed to fail-toward-disarm via a unit-tested `session_matches`; value-space verified empirically (`CLAUDE_CODE_SESSION_ID` == transcript filename == event `session_id`). Re-review ACCEPT, FATAL cleared. `MAX_BLOCKS=3` loop guard; `accept-residual` escape; `ship` clears gate state.
- **P2-D-4** (`8e82164`) — F16 gate via `AskUserQuestion` (SKILL GATE section). Oracle fixes: the presented package == `gate_state._projection` exactly (register was gated-but-unshown); literal `Approve`-only authorizes the approve call; cancelled dialog ≠ approval; revise options cover the full gated set. Fresh `claude -p` 5/5.
- **P2-D-5** (`784f3f2`) — SC-XS-3 caption ≤ figure, **folded into F5** (a caption is a scope question; no 8th agent, no required-set growth). Added `caption` + **`shows`** figure fields. Oracle MF-1 (load-bearing): SC-XS-3 is caption ≤ what the figure PLOTS (`shows`), not ≤ the bound claim — re-operationalized. Fresh `claude -p` 3/3.
- **P2-D-6** (`e9955f1`) — fluidity / deviation-log (SC-PROC-8/9/10/11). F11 flags a *silent* template force-fit; a *logged* deviation is the escape. `deviation_log` well-formedness DET (non-blank fields, `_has_content`). SC-PROC-11 (a `\gap`-skip) is already the rigid `claim_binding` floor. Oracle MF-1 (whitespace = not logged), MF-2 (a logged deviation excuses only the misfit it names + `section_id`), MF-3 (structure-only scope). Fresh `claude -p` 5/5.

### P2-E — authoring/quality review BEFORE P3 (Erfan-gated decision: review first so the components are clean before they become the default). Three reviewers fanned out, each against its proper authority:
- **SKILL + 3 references** vs the `writing-great-skills` rubric → **de-sediment + description rewrite** (`75d37ac`): cut the build-chronology back-third (duplicated the build-plan, was sediment), stripped all `P2-x`/Phase tags, rewrote the frontmatter description (11→6 lines, triggers + reach clause). **263 → 206 lines.** 3 reference files reviewed clean.
- **9 `sw-*` agents** vs official CC sub-agent docs → fixes (`8235a1a`): `sw-voice-realize` dropped `Write` (contradicted its in-place preservation contract); `sw-acknowledgment` + `sw-claim-fidelity-judge` descriptions reconciled (claimed "never touches a verdict" but emit one); verdict-key `<n>`→`<int>` standardized. Kept `Bash` on read-only judges (read-only by contract; several shell out). 
- **`stop_sw_converge.py` + settings** vs official CC hook docs → **fully compliant, fit to ship**; no changes needed.
- **Effort frontmatter, fleet-wide** (`7d60063`, Erfan-approved): all 24 agents now declare `effort:` — **xhigh** for the 3 sci-write judges (F4/F5/F11; the real fix — they were silently running at session `high`), **high** for the other 21 (= current session effort, now explicit/self-contained). CLAUDE.md routing note updated. 
- **`${CLAUDE_PROJECT_DIR}` brace form** (`4114c8f`, Erfan-approved): uniform across all 6 hook commands (doc-canonical; functionally identical here).

## Key facts for next session
- **P2-D + P2-E complete. NEXT = P3 cutover** (next session, Erfan will drive): run the full **119-scenario suite** → if green, retire the old `scientific-writing` flow, repoint `CLAUDE.md` + `docs/03-methodology.md` at sci-write-v2, wire the DET checks as always-on hooks, record D048-complete. **IRREVERSIBLE — explicit go required.**
- The build's source-of-truth: `docs/references/write-redesign-build-plan.md` (Status + build log) + the 4 session logs in its provenance table (this session added as the 4th).
- The convergence hook is **live but inert** (no `active.json` in the real repo) — it only fires when a sci-write-v2 draft is armed via `verdicts.py activate`.
- Build method unchanged (mandatory for any P3 fixups): three nets per chunk — `--selftest` → opus oracle (catches a real hole every chunk; caught a repo-wide-outage catastrophe in P2-D-3) → fresh `claude -p` (≥540000 ms Bash timeout, `CLAUDE_WRAP_SNAPSHOT_SKIP=1`) → atomic commit.
- Known residual (honestly scoped, Phase-2 gap, NOT closed): the **framing-sentence escape** — an assertive sentence the agent models as "framing" rather than a claim never enters the lattice, so the Trust floor can't see it; the human gate is the only catch until a prose→lattice claim-coverage check exists.

## Live science thread (UNCHANGED since S25)
Q4 sample-efficiency E024; analysis lane next = R08 (Q2). Q2 ❌, Q3 ❌ stand. None touched this session.
