---
title: "The Map — codes & the journey"
tags: [reference, methodology]
aliases: [map]
---

# The Map — the codes, and the path we have travelled

**What this is.** A one-screen orientation aid: the naming system (what `Q`, `E`, `A`, `D`, `L`, `F` mean) and the whole experimental journey as a tree, so you never lose the track. **It is not the status board** — canonical, always-current status lives in [`ladder.md`](ladder.md); when this map and the ladder disagree, the ladder wins and this map gets fixed. Read this when the codes or the path stop making sense; read [`ladder.md`](ladder.md) for "where exactly are we now."

---

## 1. The legend — what each letter means

The system separates **stable artifacts** (flat, immutable IDs, like issue numbers — they never get renumbered when we reinterpret them) from the **conceptual structure** (the ladder of questions, which is a separate hierarchical view).

| Code | Name | What it is | Numbering |
|---|---|---|---|
| **Q**n | **rung** / research **Q**uestion | a kill-gated question on the ladder — the conceptual spine | `Q0`→`Q5`, **in climb order** (do Q0 first, only climb if it holds) |
| **E**nnn | **E**xperiment | a concrete run that happened — the *evidence* | flat, chronological (`E001`, `E002`, …); never renumbered |
| **A**n | **A**ssumption | one of the three falsifiable bets the thesis rests on | `A1`, `A2`, `A3` (A2 gates the others) |
| **D**nnn | **D**ecision | a recorded choice, in [`decisions/decisions.md`](decisions/decisions.md) | flat, chronological |
| **L**nnn | **L**earning | a hard-won lesson, in [`learnings.md`](learnings.md) | flat, chronological (`L001`–`L0xx`) |
| **F**n | **F**ork / surviving slice | the headline research slice (F1) + forward-program steps | see note §5 |

**The rule of thumb:** `Q` = a *question* we ask; `E` = an *experiment* that answers it; `A` = an *assumption* a question tests; `D`/`L` = the decisions and lessons logged along the way. A single experiment can serve more than one rung (the structure is a DAG, not a tree), which is exactly why `E`-IDs are flat and the `Q`-ladder is a separate view on top.

---

## 2. The journey — the path we have travelled

The climb is kill-gated: each rung has a predeclared kill criterion, and we only climb if the rung below holds. The spine that organises everything: **REAL ≠ MOVABLE ≠ USEFUL** — a strong PASS on "the signal is real" says *nothing* about whether it is movable or useful.

```
THE BET:  the LM↔brain linear map is not just to MEASURE — it is a usable TRAINING SIGNAL
   │
   E001  synthetic-fMRI pilot ── could not answer by construction (L004) ── discarded
   │
   ▼
 Q0 · A2   IS THE SIGNAL REAL (beyond confounds, on real data)?           ✅ PASS (powered)
   ├─ E002  Tuckute 5-ROI ................. trained−untrained gap +0.03–0.05
   └─ E006  LeBel UTS03 voxelwise ......... gap +0.021 (gpt2) / +0.028 (Qwen), 95–99% of voxels
   │                                         └─(also computes the Q2 lever MDE → cancels E007)
   ▼
 Q1        DOES PLAIN KD PRESERVE/DESTROY ALIGNMENT?  (cheap gate: is Q3 even a problem?)   🟡 PARTIAL
   └─ E003  KD gradient ................... not preserved-for-free; births the matched-ppl control (L011)
   │
   ▼
 Q2        IS L_brain A LEVER — can we MOVE alignment by optimising it?    ❌ NO DEMONSTRATED LEVER
   └─ E004  brain-tune (LoRA) ............. +0.0032 vs permuted twin, but fold-level CI includes 0
   │
   ▼
 Q3 · F1   BRAIN-GUIDED KD vs matched-ppl baseline → per-individual gain?  ❌ NULL (powered) ◄ THE TURN
   ├─ E005  apparent +0.0081 .............. looked like a WIN — but measured vs a GROUP-AVERAGED target
   ├─ E008  per-individual (n=9) .......... ❌ NULL +0.00010, CI [−0.0004,+0.0006] — the collapse (L016)
   └─ robustness escapes — null survives every axis:
        E011 capacity · E013b objective · E013 substrate · E017 full-FT  → all ❌
   │
   ▼
 Q4 · A3   DOES INDUCED ALIGNMENT BUY ANYTHING PRACTICAL (OOD)?            ❌ bounded NULL
   └─ E009  OOD payoff .................... null-by-construction (the fulcrum is ~0; L017)
   │
   ▼
 Q5 · F3   AN fMRI-FREE PROXY that recovers most of the benefit?          ⬜ deferred (moot — needs a Q3 win)

SUPPORTING TRACKS (not rungs; they explain WHY the spine holds):
   E015  the quality law — alignment ∝ −bits-per-byte, r≈−0.78 (why matched-ppl is the load-bearing control)
   E020  the E[Y|S] ceiling — bounded-not-closed (an LM aligns ~only to the stimulus-predictable part)
   E019  external reproduction (Negi) — corroborates the lever-failure spine, not a clean clincher
```

**The honest one-line story:** the signal is **real** (Q0) and **measurable**, but **not inducible** beyond perplexity via any readout we tried (Q2/Q3) and buys **nothing practical** at matched perplexity (Q4). The positive contribution is methodological: cross-subject target-averaging *manufactures* apparent brain-specificity, and the missing controls are matched-perplexity + a permuted-brain twin.

---

## 3. The rungs at a glance

| Rung | Question | Verdict | Decided by |
|---|---|---|---|
| **Q0 · A2** | Is the signal real beyond confounds? | ✅ **PASS (powered)** | E002, **E006** |
| **Q1** | Does plain perplexity-only KD preserve/destroy alignment? | 🟡 PARTIAL (headroom; not free) | E003 |
| **Q2** | Is `L_brain` a lever — can we move it? | ❌ **NO DEMONSTRATED LEVER** (undemonstrated, not proven zero) | E004 |
| **Q3 · F1** | Brain-guided KD → per-individual gain at matched ppl? | ❌ **NULL per-subject** (robust) | **E008** (+E011/E013/E017) |
| **Q4 · A3** | Does induced alignment buy something practical (OOD)? | ❌ bounded NULL | E009 |
| **Q5 · F3** | An fMRI-free proxy that recovers the benefit? | ⬜ deferred (moot) | — |

Legend: ✅ done · 🟡 partial · ❌ tested-negative · ⬜ not started. Full verdicts with numbers and tests: [`ladder.md`](ladder.md).

---

## 4. The L→Q translation (for old logs)

The rungs were renamed `L`→`Q` on 2026-06-15 (D036), renumbered into execution order. Pre-2026-06-15 timeline logs (immutable) and any external notes still use the old `L` labels. To translate:

| old | new | rung |
|---|---|---|
| `L0` | **Q0** | signal real (A2) |
| `L2a` | **Q1** | KD-preservation gate |
| `L1` | **Q2** | the lever |
| `L3` | **Q3** | the headline (F1) |
| `L2b` | **Q4** | practical payoff (A3) |
| `L4` | **Q5** | fMRI-free proxy |

---

## 5. Notes — the things that used to confuse

- **"Layer N" is retired as a rung synonym.** Early docs (R03/R04) called the rungs "Layer 0…Layer 4"; that vocabulary is historical (those docs keep it with a mapping note). In active docs the only rung label is `Q`n. The one legitimate surviving use of "Layer N" is in the tutoring checklist, where it means a *teaching chapter* (a coarse lesson unit), not a rung.
- **`F`-labels.** `F1` is the headline question (= rung Q3); it is kept as an alias because it is deeply embedded ("Fork B", "F1-close"). In the *forward program*, `F2`/`F3`/`F4` are follow-on experiment-sequence steps, not rungs — a separate namespace. "Fork A / Fork B" are the two narrative outcomes (optimistic win vs honest-null), prose not IDs.
- **What is NOT a rung:** transformer layers (`L7`, `L12`), `L2`/`L∞` norms and "L2 loss", lecture numbers, `λ`/`L_brain`/`L²`. These keep their `L` and are unrelated to the ladder.
- **Where things live:** canonical status → `ladder.md`; **current-truth findings → the finding-reports `reports/R*.md`, one claim each, Q-tagged (D036)** — Q0/A2 = `R06` (the signal is real beyond confounds); the rest are written in reading order as each finding is covered (index + reading order + Q→report map in [`reports/AGENTS.md`](reports/AGENTS.md)); the history/journey of the whole arc → this `map.md` tree + `timeline/`; the analysis-week plan → [`analysis-roadmap.md`](analysis-roadmap.md) (being repointed from R05-sections to the finding-report set); experiments → `experiments/E*.md`; decisions/lessons → `decisions/decisions.md` + `learnings.md`. (`R05` = the retired chronological narrative, frozen for history.)
- **Report convention (D036):** a report owns one claim, tagged with the question it answers, states current truth only (no "obsolete / not yet narrated" scaffolding — history lives here in `map.md` + `timeline/` + `decisions/`), and follows the skeleton header→question→design→evidence→verdict→caveats. Spec in the `sci-write-v2` skill.
