---
title: "Codex — second-model critic + rescue (how we use it in this repo)"
tags: [reference]
---

# Codex — second-model critic + rescue (how we use it in this repo)

Codex (OpenAI CLI, model `gpt-5.5`) is a **second model** we drive from Claude Code via the `codex`
plugin. In this repo it has exactly two jobs: **(1)** an independent critic that *adds to* our existing
critique subagents, and **(2)** a rescue / second-implementation pass on analysis code. It is a
code-and-reasoning tool, not a science oracle — see the hard line at the bottom.

This file is the procedure. The one-paragraph policy lives in `CLAUDE.md`; the deep "what flags exist"
truth is the plugin itself (`~/.claude/plugins/cache/openai-codex/codex/.../scripts/`).

## The command surface (verified against the plugin scripts, codex-cli 0.139.0)

| Surface | What it does | `--model`? | `--effort`? | Writes files? |
|---|---|---|---|---|
| `codex:codex-rescue` subagent → `task` | Hand Codex a coding/debug/research job (one forwarded `task`) | ✅ | ✅ `none·minimal·low·medium·high·xhigh` | ✅ defaults `--write`; read-only if asked |
| `/codex:review` | Built-in structured reviewer over git working-tree/branch | ✅ | ❌ **not exposed** | never |
| `/codex:adversarial-review [focus]` | Challenges design/approach, takes focus text | ✅ | ❌ **not exposed** | never |
| `/codex:status · result · cancel` | Manage background Codex jobs | — | — | — |
| `/codex:setup [--enable/--disable-review-gate]` | Health check + toggle stop-time review gate | — | — | — |

Extra `task` controls: `--background`/`--wait` (execution), `--resume`/`--fresh` (continue last thread
or start clean), `--write` (legacy; the OS sandbox is disabled here — see Sandbox below — so Codex can
write regardless; `--write` only affects the metadata label).

## Sandbox / environment — DISABLED here (verified 2026-06-12, this is load-bearing)

This host is a **Docker container** where Codex's bubblewrap (`bwrap`) sandbox **cannot run**: bwrap
can't initialise a user/network namespace (`bwrap: setting up uid map: Permission denied` and
`loopback: Failed RTM_NEWADDR: Operation not permitted`), because the container lacks the capability
and `/proc/sys` is read-only (can't flip `kernel.apparmor_restrict_unprivileged_userns`). Installing
system `bubblewrap` did **not** fix it — it's a container limit, not a missing binary. Any sandboxed
Codex run silently fails to execute commands (it can't even read a file → returns garbage like
`COUNT=0`). This is exactly the case Codex's own docs call "externally sandboxed," so we disable the
inner sandbox and let the **container be the boundary**:

- **`~/.codex/config.toml`:** `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`,
  `model_reasoning_effort = "xhigh"`. Fixes the interactive `codex` TUI and most `codex exec` runs.
- **Plugin patch:** `codex.mjs` `buildThreadParams`/`buildResumeParams` are patched to force
  `sandbox: "danger-full-access"` (the plugin otherwise hardcodes `read-only` and breaks). **This lives
  in the plugin cache (`~/.claude/plugins/cache/openai-codex/...`) and must be REAPPLIED after any
  `codex` plugin update** — the in-file comment flags it.
- **`codex exec` gotcha:** passing `-c <key>=<val>` can revert exec's sandbox to its `read-only`
  default; for direct `codex exec` automation pass **`--sandbox danger-full-access` explicitly**.
- **Net effect on safety:** Codex now has full filesystem access on every run. The protections are no
  longer the inner sandbox but (1) the outer container, (2) git (atomic commits + diff review catch any
  stray edit), and (3) the hard line below. For critique/review, still tell Codex "do not edit" in the
  prompt — it's no longer enforced, so trust git, not the sandbox.

## Model / effort policy (the asymmetric "medium worker, xhigh critic" setup)

- **Global default reasoning = `xhigh`** (`~/.codex/config.toml`, `model_reasoning_effort`) — VERIFIED
  applied (a live `codex exec` ran at `reasoning effort: xhigh`).
- **Critic side (reviews) runs xhigh by inheritance.** `/codex:review` and `/codex:adversarial-review`
  expose no per-call `--effort`; they inherit the config default → every review is xhigh automatically.
- **Worker side (task) runs at the effort you pass.** A delegated build/fix should pass `--effort
  medium` explicitly to override the global default *down* — fast worker, slow critic. Bump to `high`/
  `xhigh` only for a genuinely hard implementation.
- Model is `gpt-5.5` by default; pass `--model` only to change it (`spark` → `gpt-5.3-codex-spark`).

## Scenario 1 — Codex as an ADDITION to our critique subagents

Our thinking panel (`counter-argument`, `premortem-analyst`, `socratic-thinker`,
`first-principles-grounder`, all Claude/fable+sonnet) attacks the **conclusion**. Codex adds a
**code-level** second model that attacks the **implementation** — the layer the panel doesn't reach.
Two forms:

**1a. Single adversarial review.** For a focused pass over current git state:
```
/codex:adversarial-review <focus, e.g. "the fold-clustered bootstrap CI in reanalyze_e005_e006.py">
```
Review-only, xhigh by inheritance, returns Codex's verdict verbatim. Use on any analysis/stats script
before its number lands in the ladder/docs.

**1b. Codex persona panel (one or several Codex sessions with different personalities).** When one
review isn't enough, dispatch **N background, read-only `task` runs**, each via the `codex:codex-rescue`
subagent with a distinct reviewer persona prepended to the target (a diff or a file path). Run them in
parallel, then collect with `/codex:result <job-id>`. Each persona is a code-level analog of a panel
lens:

| Persona | Lens (what it hunts in the *code*) |
|---|---|
| **Statistical referee** | confound subtraction, CI bootstrap **unit** (seed/fold/voxel — not pseudo-replicated), clustering, multiple-comparisons exposure, power/MDE vs the effect. Does the code compute the statistic it claims? |
| **Reviewer-2 skeptic** | assume the output is an artifact; find the line of code that would let a confound (split leakage, ppl/LM-quality, length/position) masquerade as the construct. |
| **First-principles re-deriver** | re-derive the computation from the math (`docs/06-theory-grounding.md`, the canonical notes) and check the implementation matches intent — not just that it runs. |
| **Reproducibility / leakage auditor** | seeds & determinism, contiguous-split integrity, off-by-one in fold/story splits, whether the permuted-twin null is actually built correctly in code. |

Dispatch shape (read-only, background, persona-framed) — invoke the `codex:codex-rescue` subagent once
per persona with a prompt like:
```
[PERSONA: statistical referee — see docs/references/codex-usage.md]
Review (do NOT edit) scripts/reanalyze_e005_e006.py for <the specific concern>.
--background
```
The rescue subagent forwards a single read-only `task` (no `--write`). Use 1–4 personas sized to how
load-bearing the code is; `log`/note which personas you ran so a partial panel isn't read as a clean
sweep. Fold surviving findings back the same way the thinking panel does: verify each against the data,
fix, re-run until no objection holds.

## Scenario 2 — Codex rescue / second implementation

When an analysis script is buggy, stuck, or you want an independent rebuild to cross-check ours, hand
it to the `codex:codex-rescue` subagent. This is the one place `--write` is appropriate (the subagent
defaults to write-capable). gpt-5.5 is a strong coder; a fresh implementation that *agrees* with ours
is real evidence, and one that disagrees is a bug lead.

- Default to `--effort medium` for the worker; `--background` for anything multi-step.
- Good targets: `scripts/figures/make_figures.py`, the LeBel encoding/distill pipeline, a flaky
  reanalysis script. Bad targets: anything that would invent or edit a recorded **number**.

## The hard line (non-negotiable, from CLAUDE.md)

- **Codex never produces a science number or a verdict.** Numbers come only from the `docs/` brain;
  rungs flip only on an Erfan-confirmed verdict. Codex reviews **code correctness** and **proposes
  implementations** — it does not adjudicate a hypothesis or write a result into the docs.
- **Critique should not edit — but the sandbox no longer enforces it** (disabled, see Sandbox). Tell
  Codex "do not edit" in the prompt for Scenario 1, and rely on git (atomic commits, diff review) to
  catch any stray write. Full filesystem access is always on now.
- **Stop-review-gate stays OFF.** It would force a Codex review before Claude can stop, which fights
  the docs-first `/wrap` ritual and adds latency to our mostly-docs commits. Enable only during a heavy
  code-writing stretch (`/codex:setup --enable-review-gate`), and disable it after.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
