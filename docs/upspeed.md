# Upspeed — read first, write last

**Last updated:** 2026-06-12 (Session 10 — TOOLING: Codex wired as second-model critic + rescue; bwrap sandbox disabled; reasoning=xhigh. No science touched.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (the rung board + next step, D015). This file is
> the last-session prose; if it disagrees with the ladder, the ladder wins. With no task, run `/orient`.

## Current state

Science is **UNCHANGED from S9** — experimental program CLOSED (Fork B), manuscript v0.9 artifact-complete, per-individual null robust. **No rung moved this session — it was tooling/infrastructure only.** What changed is that **Codex is now a usable second model** for this repo (a code-level critic that adds to the thinking panel, + a rescue/second-implementation tool), and the container's bwrap-sandbox blocker is fixed.

- **L0/A2 ✅ PASS** (E006). **L3/F1 ❌ NULL per-subject (robust). L2b/A3 ❌ bounded NULL.** All unchanged.

## What was set up this session (tooling)

1. **Codex integration** — `docs/references/codex-usage.md` (full procedure) + a Codex section in `CLAUDE.md`. Two jobs: (1) critic that *adds to* the thinking panel — `/codex:adversarial-review` or a **persona panel** (1–4 background read-only `task` runs with distinct personalities); (2) **rescue / second-implementation** of analysis scripts. **Hard line:** Codex never emits a science number or flips a rung (code correctness only); numbers come from the `docs/` brain, verdicts from Erfan.
2. **Reasoning = xhigh** (global `model_reasoning_effort` in `~/.codex/config.toml`) → reviews run xhigh by inheritance; delegate a `task` with `--effort medium` to get the asymmetric "medium worker / xhigh critic".
3. **Sandbox DISABLED** (see Key facts) — bwrap can't run in this container; config + a plugin patch make Codex run unsandboxed (the Docker container is the boundary).
4. **Live validation:** Codex (xhigh) independently re-ran `reanalyze_e005_e006.py` and reproduced the S8 panel's core finding (t-CI includes 0, bootstrap-excludes-0 contradiction, the `(fold4,seed0)` +0.0636 outlier driving the +0.0081) — independent corroboration of L015.

## What to do next (Erfan's call)

**Mode = ANALYSIS, as before.** Resume the get-up-to-speed walk at **Layer 3 = E005** (apparent +0.0081 → E008 per-individual null) = writing **R05 §9**, then §10 (E008) → §11 (Fork-B) → §12 (robustness) → §13 (E009+E015) → §14. After R05 reaches the end: figures-check (`scripts/figures/make_figures.py`) + manuscript read-through. Codex is available as a code-level critic/rescue if a script needs it — but analysis sessions touch no science.

## Blockers / open loops

- **No running jobs; working tree clean** (3 atomic commits this session, all docs/tooling).
- **Carry-forward:** the `codex.mjs` sandbox patch lives in the plugin cache → **reapply after a codex plugin update** (in-file comment + `codex-usage.md` flag it).
- **Still open (from S8/S9):** doc-audit follow-ups in `tasks.md` (stale Status headers on ~8 experiment docs; E005 body still leads with retracted "F1 CONFIRMED"; R03/R01 pre-R04 phrasings). Untouched this session.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs 4× L40S free.
- **Codex (how to use):** full guide = `docs/references/codex-usage.md`. Default `gpt-5.5`, reasoning **xhigh**. **Sandbox is DISABLED** — bwrap can't init namespaces in this container (`RTM_NEWADDR`/uid-map *Operation not permitted*; `/proc/sys` read-only; system bubblewrap doesn't help). Config: `approval_policy=never`, `sandbox_mode=danger-full-access`; plugin `codex.mjs` patched to force `danger-full-access` (reapply after plugin update). **Test Codex with a prompt that forces a shell command** (read a file) — text-only replies don't exercise the sandbox and falsely pass (L033). For direct `codex exec` automation pass `--sandbox danger-full-access` explicitly.
- **R05 vs manuscript:** R05 = teach-from-scratch narrative (math at length); manuscript = terse submission artifact. Keep role-distinct.
- **Corrected number to carry:** Tuckute functional NC ceiling = 0.491 (mean) / 0.559 (network); 0.353 was the anatomical-mask mislabel (L012). E002's "~10%" → honest ~7%.
- **Tooling gotcha (carried):** offline `load_dataset("wikitext",...)` FAILS — use `"Salesforce/wikitext"`. `outputs/` is gitignored.
- **Git:** `main`, push only when asked.
