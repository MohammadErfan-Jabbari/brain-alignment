# Write mode

Turn settled findings into report or manuscript prose. The engine is the `sci-write-v2` skill (D048,
cut over from `scientific-writing` at S43/P3); this stance loads it and works inside it.

Load `sci-write-v2` and follow its gated-loop spine: separate the four concerns (Trust / Argument /
Structure / Voice); build the claim-lattice + skeleton, **gate the whole package as one** (F16, via
`AskUserQuestion`) *before* any prose; then draft (emitting one `\evd{claim}{strength}` per claim
sentence), audit with the parallel stage-5 readers, and revise to convergence. Draft from evidence only;
a needed-but-missing number is a `\gap`. Run `scripts/run_checks.py --lattice <lattice> [--prose <p>]`
after each stage write — any DET failure is a stop. Reports are stored verdict-first with a plain-language
lead; the simple-first walk is `/teach`'s job, not a second shape of the file. Knowledge flows down only:
evidence into a report, report into the extended manuscript, extended into a public cut, and the
manuscripts are rebuilt only at a checkpoint Erfan calls.

## The gate and convergence (the v2 spine)

A manuscript build or revision is its own logged `/write` session, never an add-on at the tail of a
`/meta` or analysis session — that bypass is exactly how v0.1 storytelling prose reached a supervisor
un-reviewed (L054). No prose is generated before the **F16 human gate** approves the coupled package
(message + reader-model + register + lattice + skeleton); `gate_state.py` blocks drafting without a
matching approval and re-blocks if any gated field changed (a logic revision re-enters the gate).

**Convergence is enforced by `stop_sw_converge` (the v2 Stop-hook, supersedes the D047 register gate).**
Once the F8b draft is armed (`verdicts.py activate`), the hook holds your turn-end while the draft is
unconverged — "done" = every required stage-5 reader (`sw-argument-judge`, `sw-scope-judge`,
`sw-claim-fidelity-judge`, `sw-structure-judge`, `sw-voice-auditor`, the F13 panel, `sw-acknowledgment`)
returns `ready_to_ship` on the current draft bytes, recorded via `verdicts.py record`. A reworded edit
re-stales every verdict (hash-keyed). The always-on `ai_tell_lint` + `honesty_writecheck` PostToolUse
hooks are the per-edit tripwires; a clean deterministic run is not a clearance, because the linters cannot
catch the register/argument class — that is the readers' job. Disarm with `verdicts.py ship` only after
convergence **and** Erfan's final approval.

## Boundary

Writes, checks, and routes prose that already traces to recorded evidence. It never invents a result,
adjudicates a hypothesis, or flips a rung. A needed-but-missing number is a `\gap`, never a guess. A defect
the prose **cannot** fix because it lives in the evidence/argument substrate routes upstream via the
**cross-stance handoff (D050)** — `/write` detects it, emits the handoff, blocks convergence stickily, and
recommends the stance; it never papers over and never adopts an unrecorded number.
