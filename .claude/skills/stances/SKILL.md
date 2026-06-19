---
name: stances
description: >-
  The operating model for this repo. Work in interaction STANCES, invoked at any moment and switched
  freely. Eight stances (work, interpret, write, teach, scout, meta, plan, review), each setting a tone,
  an autonomy level, and a set of procedures over one shared scientific-honesty spine. Auto-activates
  when intent matches a stance ("teach me X", "walk me through the Qi report", "is this verdict real",
  "digest this result", "find papers on X", "what should we run next") and STATES which stance it
  entered so the user can redirect. Explicit /teach /interpret /write /scout /meta /plan /review force a
  stance; /work is explicit-only and never auto-fires.
---

# Interaction stances

This repo runs by interaction stance, not by session type. There is no "working vs analysis" label
(that split is retired, D044). At any moment you are in one stance; you may switch as the work turns.
A stance fixes three things, plus one it does not touch:

- **tone and autonomy** (how the agent talks and how far it runs unattended),
- **the procedures** it auto-arms,
- **the honesty standard** it is held to,
- and NOT the fabrication guard: that is armed at write-time, independent of any stance (see below).

## The stances (the operating map)

| Stance | What it does | Autonomy | Touches a number? | Mode file (wraps) |
|---|---|---|---|---|
| `/work` | produce evidence: lock a design, run it, judge it, record it | high (long `/goal` runs) | yes, produces | `modes/work.md` (precheck + goalsmith + ritual) |
| `/interpret` | turn recorded evidence into an adjudicated verdict | medium | yes, adjudicates | `modes/interpret.md` |
| `/write` | turn settled findings into report or manuscript prose | low-medium | reports them | `modes/write.md` (scientific-writing) |
| `/teach` | transfer understanding of a finding into the user's head | low, conversational | reads them | `modes/teach.md` |
| `/scout` | bring external literature and data into the brain | medium | external evidence | `modes/scout.md` (lit-scout / dataset-scout / paper-digest) |
| `/meta` | build or maintain the apparatus (tooling, methodology, records) | variable | no | `modes/meta.md` |
| `/plan` | set direction: roadmap, kill-gate triage, what to run next | medium | no | `modes/plan.md` |
| `/review` | critique a result, claim, or design on demand | medium | no | `modes/review.md` (panel + Codex) |

The vertical seam is whether the stance **touches a science number**. `/work` and `/interpret` are
truth-producing (the strict standard below applies). `/write`, `/teach`, `/scout` report or consume
numbers (cite-or-flag applies). `/plan` and `/meta` touch no number.

The human-facing version of this map (how to operate day to day) is `docs/operating-map.md`.

## Invocation

- **Explicit** `/teach`, `/interpret`, `/write`, `/scout`, `/meta`, `/plan`, `/review` force that stance.
- **Auto** otherwise: when the user just talks, infer the stance from intent, **state it in one line**
  ("Entering /teach on R07. Say otherwise to redirect."), then proceed. Never enter a stance silently.
- **`/work` is explicit-only.** A heavy autonomous run never auto-fires from a passing remark.
- **Switching mid-session is normal.** When the work turns (a teach session hits a hole that needs a
  run, a write pass needs a verdict first), state the switch in one line and continue.

## The honesty spine (shared, non-negotiable, stance-independent)

The thesis rests on never inventing a result. That guard does not depend on which stance is active:

- **A number is born in a working session and recorded in `docs/`** (`experiments/`, `learnings.md`,
  `ladder.md`, `decisions/`). No stance may state a result a working session did not record.
- **A needed-but-missing number is a `\gap`, never a guess.** Flag it; do not estimate, round, or
  infer it from a stand-in.
- **The actuator is a write-time hook**, not stance prose. Any write to `docs/reports/` or
  `docs/manuscript/` (the prose deliverables that use the inline-cite convention) runs the D011 check
  (`scientific-writing/scripts/check_evd_resolution.py`); a result-like number with no cite is flagged.
  The flag fires no matter the stance, so it cannot be skipped by mislabeling the work. The `/wrap`
  number-provenance audit is the backstop. (The ladder/learnings/experiments docs reference results by
  bare code and are not checked this way — L052.)

Each truth-producing stance also carries its own **standard** (the threshold it must clear), which is a
judgment obligation, not the fabrication guard:

- `/work`: kill criteria locked before the run, contiguous splits, nuisance baselines, ≥3 seeds,
  numbers reported with uncertainty and the named test.
- `/interpret`: adjudication uses the strict standard, never loose analysis. Re-judging a recorded
  number is `/work`-grade, not casual reading.

## Routing

Each stance has a deep mode file in `modes/`. Enter the stance (explicitly, or by stated inference),
then follow its file:

- `/teach` → `modes/teach.md` · `/interpret` → `modes/interpret.md` · `/write` → `modes/write.md`
- `/work` → `modes/work.md` · `/scout` → `modes/scout.md` · `/review` → `modes/review.md`
- `/plan` → `modes/plan.md` · `/meta` → `modes/meta.md`

The six files other than teach and interpret are thin: each states the stance's standard and routes to
the existing agents, commands, or skill that do the work.

## References

- `formats/learning-record.md`: the learning-ledger record template (read before writing a record).
- `docs/operating-map.md`: the human-facing operating picture.
- `docs/03-methodology.md`: the canonical definition of the stance model and the deliverable layers.
