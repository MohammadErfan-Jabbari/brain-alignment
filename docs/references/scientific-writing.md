# Scientific writing: pointer to the skill

**The `/write` engine is the `sci-write-v2` skill** (`.claude/skills/sci-write-v2/`) as of the D048
cutover (S43, 2026-06-26). The old `scientific-writing` skill is **tombstoned** (read-only ~1 week, then
deleted) — do not route new writing to it. Read the v2 skill for anything real; this page is a one-screen
index pointer.

**What it is.** The single governor of how recorded evidence becomes written argument across the three
deliverable layers (`03-methodology.md` "Deliverable layers": markdown reports, the LaTeX extended
manuscript, frozen LaTeX public cuts). It separates four concerns — **Trust** (claims↔evidence, strength-
tagged), **Argument** (warrants + honest scope/acknowledgment), **Structure** (reader-expectation),
**Voice** (scientific register) — over a **gated loop**: build the claim-lattice + skeleton, gate the whole
package as one (F16, before any prose), then draft (one `\evd{claim}{strength}` per claim sentence), audit
with the parallel stage-5 readers, and revise to convergence. Every number traces to recorded evidence
(D011); it never invents a result; a defect the prose can't fix routes upstream via the cross-stance
handoff (D050).

**When it fires.** Any time you write, draft, edit, consolidate, compress, or review a report, manuscript
section, abstract, results paragraph, or checkpoint-log entry.

**The verifiers** (the DET floor — run after each stage write):

```
uv run python .claude/skills/sci-write-v2/scripts/run_checks.py --lattice <claim-lattice.json> [--prose <path>]
```

dispatches `lattice_integrity` · `claim_binding` · `claim_fidelity` · `warrant_schema` · `gate_state` and
(with `--prose`) `draft_check` · `ai_tell_lint` · `scope_lint` · `consistency_check`. Convergence is
enforced by the `stop_sw_converge` Stop-hook + `verdicts.py`; the always-on per-edit tripwires are
`.claude/hooks/honesty_writecheck.py` (D011 numbers) + `prose_writecheck.py` (→ v2 `ai_tell_lint`).

**Design + spec.** `docs/references/write-redesign-design.html` (the canvas) + `write-redesign-build-plan.md`
(the build) + `decisions/decisions.md` D048/D050/D051. The reference docs inside the skill carry the voice
rules, the `\evd`/`\gap` provenance convention, the LaTeX conventions, and the review philosophy.
