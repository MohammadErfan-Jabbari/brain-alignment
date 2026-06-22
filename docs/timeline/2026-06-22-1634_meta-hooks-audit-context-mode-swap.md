# 2026-06-22 16:34 — S34 · /meta: hook-layering audit + graphify→context-mode CLAUDE.md swap

**Stance:** `/meta` (apparatus only). No experiment, no science number, no manuscript prose authored, no ladder rung touched. Q0–Q5 stand exactly as S33.

## What this session did

1. **Audited the hook stack across all layers** for conflicts — global `~/.claude/settings.json`, project `.claude/settings.json` + `.local.json`, and every active plugin (context-mode, ecc, ponytail, codex, plannotator). Finding: **no blocking conflicts.**
   - Only two event types can block a turn (PreToolUse, Stop). On **Stop**, exactly one hook emits `decision:block` — our own `stop_register_gate.py` (D047), which carries a `MAX_BLOCKS` loop guard. ECC's 6 Stop hooks are non-blocking telemetry; the Codex stop-review gate is OFF; context-mode's Stop is capture-only. No dueling blockers.
   - **PostToolUse Edit|Write** is the heaviest stack (~9 hooks); our `honesty_writecheck.py` + `prose_writecheck.py` are flag-only, never block. No conflict.
   - ECC's one dangerous overlap (`gateguard-fact-force`, which would block bash/edits in a docs repo) is **already disabled** via the project's `ECC_DISABLED_HOOKS` env — the conflict was anticipated and defused.
   - Two configs are **inert** here: `plannotator/apps/copilot/hooks.json` (old lowercase `preToolUse` schema, Copilot variant) and the `.codex-plugin/hooks.json` files (Codex harness, not Claude Code).
   - Soft observation (not a break): ECC is the least-justified plugin in a docs/LaTeX/Python repo — ~25 software-project telemetry hooks that find nothing to act on; context-mode's Bash→ctx nudge fires on every Bash, mild friction against the Read/Edit docs workflow.

2. **Confirmed context-mode's routing rules are auto-injected** by its `SessionStart` hook (`sessionstart.mjs → createRoutingBlock`) every session — the `<context_window_protection>` block. The repo's `configs/claude-code/CLAUDE.md` is the manual-install fallback for harnesses without the hook.

3. **Per Erfan's decision, swapped the apparatus guidance in `CLAUDE.md`:**
   - Replaced the `## graphify` section with context-mode's full MANDATORY routing rules (verbatim from the plugin's shipped `configs/claude-code/CLAUDE.md`, v1.0.165).
   - Dropped `/graphify` from the Skills line; fixed the "graphify/Codex" authority note → "Codex".
   - Deleted `.claude/CLAUDE.md` (it was only the `/graphify` trigger).
   - Gitignored `.claude/worktrees/` (transient agent worktree state).
   - graphify is NOT fully removed from the repo — the `/graphify` skill, `.graphifyignore`, and `graphify-out/` remain. Only the instruction files were cleaned (Erfan's scope).

4. **Committed pre-existing stragglers** that had been carried uncommitted (Erfan: "commit everything"): the rebuilt extended PDF, the R07 lesson note, and the June supervisor email.

## Commits (on `main`)
- `5faa1b5` docs(claude): replace graphify guidance with context-mode routing rules
- `a6d9e19` docs(manuscript): rebuild extended PDF
- `7b551c3` docs: add R07 lesson note and June supervisor email

## What's next
Unchanged from S33 — the live thread is the `/write` extended-manuscript clean, next unit **§1 Introduction ¶1**. This meta session did not advance it.

## Note
`/wrap` ran inline (light tier); the upspeed.md update was surgical (header + key fact + stragglers-now-committed), deliberately NOT a full replace, to preserve the S33 manuscript-clean resume state.
