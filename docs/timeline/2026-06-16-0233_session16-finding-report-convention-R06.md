# Session 16 — analysis: rungs renamed L→Q, the finding-report convention (D036), R05 retired, R06 written

**Date:** 2026-06-15 17:46 → 2026-06-16 02:33 (+0200) · **Mode:** ANALYSIS (no new evidence; no rung changed).

> **Reconstructed log (written 2026-06-16 by the next session).** S16 was committed to git but never formally
> `/wrap`ped, so the state boards (`ladder.md`, `upspeed.md`, `tasks.md`, `analysis-roadmap.md`) went stale. This log
> is reconstructed from the git history (`4763f97`→`1fc19d5`) and `decisions/decisions.md` D036, not from a live
> session transcript. It exists to complete the immutable record.

## What happened (in order, by commit)

1. **Renamed the scientific-ladder rungs `L`→`Q` in execution (climb) order** (`4763f97`). The old `L` collided with
   learning IDs (`L001+`) and ran out of climb order (L2a before L1). Mapping: `L0→Q0` (signal real, A2) · `L2a→Q1`
   (KD-preservation gate) · `L1→Q2` (the lever) · `L3→Q3` (headline, F1) · `L2b→Q4` (practical payoff, A3) · `L4→Q5`
   (fMRI-free proxy). Repo-wide relabel via a folder-by-folder subagent swarm with an exact mapping contract; verified
   clean (norms / λ / transformer layers / lecture numbers untouched; learnings count unchanged). Timeline logs stay
   immutable (old `L`).
2. **Added `docs/map.md`** (`7695ed4`) — a one-screen orientation aid: the naming legend (`Q`/`E`/`A`/`D`/`L`/`F`) and
   the whole experimental journey as a tree, plus the L↔Q table. It is **not** the status board (`ladder.md` still wins).
   Wired the convention into `CLAUDE.md`.
3. **Adopted the finding-report convention + piloted R06** (`adf270a`, `e8e472f`). A report is now **one durable claim
   per file**, flat append-only `R<NN>` IDs (issue-number rule — never renumbered), **current-truth-only** (history
   lives in `map.md`/`timeline/`/`decisions/`, not in the report), Q-tagged, each mapping **1:1 to a manuscript Results
   section**. Reading order + Q→report map live in `reports/README.md`. R06 = Q0/A2, "the LM↔brain alignment signal is
   real, beyond confounds."
4. **Retired R05** (`67f1c34`) — frozen for history across the living docs, superseded by the finding-reports + `map.md`.
5. **Formalized R06 as conditional-MI + a math-grounded report convention** (`d5731ca`); then **scientific voice for the
   R06 math + a voice rule in the skill** (`e75240e`), and a **"presenting a measured quantity"** rule
   (`373fe1a`). Reports now formalize their core quantity and foundational concepts in real LaTeX and cite the course
   note (`06-theory-grounding.md`) rather than re-derive.
6. **Added the estimand-first lens to the reasoning toolkit** (`dbef679`) — name the estimand, the estimator, and the
   identifying assumption that ties them; plus a rule to grow the toolkit as new lenses prove themselves.
7. **Clarified the R06 design section** (`1fc19d5`) — the gap and the three controls (matched perplexity, a per-kind
   permuted-brain twin, per-subject inference).

## Verdict / science state

**No rung flipped. No new evidence.** The ladder is unchanged from S14: Q0/A2 ✅ (powered, E006); Q3/F1 ❌ per-individual
null (E008, robust across capacity/objective/substrate/parameterisation); Q4/A3 ❌ bounded null. This session restructured
the **write-up layer**, not the science.

## Decisions / learnings

- **D036** — rungs renamed L→Q in execution order; the naming convention + `map.md`; the finding-report convention;
  codes never enter the public manuscript. Erfan-approved. Recorded in `decisions/decisions.md`.

## Open loops carried out of S16

- **Not formally `/wrap`ped** → state boards were stale (reconciled 2026-06-16; see the next log).
- **Brain mirror** of D035/D036 to gbrain `projects/brain-alignment` still pending (carried from S15).
- The parked Q3 draft `reports/_pending-Q3_*.md` still carries a stale "# R06 —" title; it becomes R09 when promoted.
- **Next:** R07 (Q1 — plain KD does not preserve alignment), the next finding-report in reading order.
