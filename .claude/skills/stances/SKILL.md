---
name: stances
description: >-
  Lightweight operating vocabulary for this repo: work, interpret, write, teach, scout, plan, review,
  and meta. Auto-activate on matching intent and state the stance; /work remains explicit-only.
---

# Interaction stances

State the active stance in one line and switch when the work changes. Stances set behavior; they do not create separate truth stores or mandatory artifacts.

| Stance | Job | Boundary |
|---|---|---|
| `/work` | lock, run, and record evidence | explicit-only; produces numbers in E records |
| `/interpret` | recompute and adjudicate recorded evidence | proposes a verdict; does not invent data |
| `/write` | put settled claims directly into the extended manuscript | reports evidence; does not adjudicate it |
| `/teach` | transfer understanding from repo sources | produces no scientific truth |
| `/scout` | retrieve external papers or datasets into canonical records | external evidence only |
| `/plan` | choose direction | no numbers produced or adjudicated |
| `/review` | stress-test a result, claim, design, or manuscript | read-only judgment by default |
| `/meta` | build, simplify, or repair apparatus | no science adjudication |

## Invocation

- Explicit `/teach`, `/interpret`, `/write`, `/scout`, `/meta`, `/plan`, and `/review` force the stance.
- Otherwise infer from intent, state the stance, and proceed.
- `/work` never auto-fires from a passing remark.
- Switching mid-session is normal; state the switch.

## Honesty spine

- Scientific numbers originate in `/work` and are recorded in an owning E record.
- A missing number is a `\gap`, never a guess or synthetic stand-in.
- The extended manuscript reports only recorded evidence with `\evd{Ennn}` or keyed `\result{...}` provenance.
- A contradiction found during writing routes upstream to `/interpret`; set `docs/status.md` to `manuscript-sync-pending` until resolved and synchronized.
- `/work` locks kill criteria, controls, splits, inference units, and at least three seeds before compute.
- `/interpret` independently recomputes load-bearing statistics and uses fresh adversarial review before a verdict is settled.

## Routing

Read the matching file under `modes/`:

- `work.md`, `interpret.md`, `write.md`, `teach.md`
- `scout.md`, `plan.md`, `review.md`, `meta.md`

The authority contract is [`docs/03-methodology.md`](../../../docs/03-methodology.md); current operations are in [`docs/status.md`](../../../docs/status.md).
