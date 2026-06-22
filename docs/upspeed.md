# Upspeed — read first, write last

**Last updated:** 2026-06-22 (S35 — **/meta: redesigned the `/write` pipeline end-to-end and took it to BUILD-READY.** From the S33 diagnosis ("an immune system, not a notion of health") to a complete design: methodology canon + 11-repo ecosystem audit + Claudio's supervisor feedback → an ideal 4-concern system (Trust/Argument/Structure/Voice, gated-loop spine) → 21-functionality matrix → 119-scenario TDD suite → Claude-Code-primitive mapping → coverage check, **each step independently opus-reviewed**. **NO experiment, NO science number, NO rung change — Q0–Q5 stand exactly as S33/S34.** Prior: S34 — /meta hook-stack audit + graphify→context-mode swap in CLAUDE.md.)

> **Canonical Q-rung state lives in [`ladder.md`](ladder.md)** (Q0–Q5 unchanged). **How to operate = [`operating-map.md`](operating-map.md)** (8 stances). With no task, run `/orient`.

## What this session did (all /meta — design, no code yet)
- **Designed the new `/write` pipeline.** The artifacts (all in `docs/references/`, committed):
  - `write-redesign-design.html` — the **living design canvas** (v1.1, BUILD-READY): the 4 concerns, the gated-loop spine, the 21-functionality matrix (2a), the fluidity principle, the CC-primitive mapping (2c), the coverage check (2d), the CC-power upgrades. **This is the master design doc — open it first.**
  - `write-redesign-build-plan.md` — the migration map (existing item → F-number → keep/lift/rewrite/retire), the Phase-1 walking skeleton, build order.
  - `write-redesign-scenarios.md` — the 119-scenario TDD suite (full F1–F19 coverage, near-misses, Claudio anchor, F17 exemplar set).
  - `write-redesign-sources.md` (8 asset groups) · `scientific-writing-methodology.md` (the canon) · `writing-skills-ecosystem-audit.md` (11 repos) · `write-redesign-citations.md` (design→source) · `supervisor-feedback.md` (Claudio).
- **The core reframe:** separate the four concerns we currently tangle. **Trust** + **Argument** = the case is true, sound, honestly-scoped. **Structure** + **Voice** = delivered well. The human gates the *case + plan*, not the prose lines; trust comes from a claim-lattice locked at the gate + audited for drift. The claim-grounding loop (a Claim-Intent-Manifest extending our D011) is what lets Erfan stop reading every line.

## What's next (Erfan's call — design is done, build is next)
- **Phase 1 — the walking skeleton.** Build the minimum vertical slice through the whole spine, reusing the lifted DET scripts: `claim-lattice.json` (F15) → claim-binding (F3) → minimal skeleton (F6) → drafter-with-\evd (F8a) → two audits (F12 voice + F9a/b) → gate (F16). **Run it on the abstract** (a case we hand-cleaned in S33). Acceptance: catches Claudio's class (SC-VOICE-01–04), passes the near-misses, every claim \evd-bound. Then expand (Phase 2) and cut over (Phase 3, after the 119-suite passes).
- **Live science thread (UNCHANGED since S25):** Q4 sample-efficiency E024 — re-substrate to higher-N gaze → synthetic-PI MDE positive-control → re-gate → build. Q2 ❌, Q3 ❌ stand.

## Blockers / open loops
- **The `/write` build has not started** — the design is BUILD-READY but no code written. Resume at Phase 1.
- The redesign **does not change the existing skill yet**; the old `scientific-writing` flow stays live until the new pipeline passes the 119-scenario suite (then retire it — Phase 3).
- `taste-reader` opus agent still unbuilt — but it's now subsumed by the new design (F12 voice + the panel), so build it as part of the pipeline, not separately.

## Key facts
- **Design master doc:** `docs/references/write-redesign-design.html` (render it as an Artifact to read; it's the canvas). The 7 sibling `write-redesign-*` / methodology / audit / feedback docs are the source set — `write-redesign-sources.md` indexes all.
- **Effort tiers (set, Erfan-approved):** all `/write` subagents HIGH; F4 (argument), F5 (scope), F11 (structure) at XHIGH.
- **~⅕ of the build is reuse-not-build:** the 9 DET scripts (`ai_tell_lint`, the evd/gap/number checks, register_state), `prose-register-auditor`, the thinking panel, honesty_writecheck — lift them, don't rewrite.
- **Tooling note:** parallel `git clone` of many repos hits anonymous throttling → clone sequentially.
- **Run code:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`; 4× L40S. Git: `main`, push only when asked.
- Cloned reference repos live in gitignored `data/reference-repos/` (11 repos).
