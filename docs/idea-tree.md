# The Idea Tree — the full possibility space, by solution altitude

**What this is.** The forward-planning map of *every* idea this project could pursue, organized so the climb has a principled order. It is the complement of [`map.md`](map.md): `map.md` records the **journey we have travelled** (history, the E-nodes that ran); this tree records the **whole space including the untravelled branches**, so "climb the highest untested layer" is a well-defined instruction. Canonical *status* still lives in [`ladder.md`](ladder.md) and the program state in [`expansion-program.md`](expansion-program.md); when they disagree, the ladder wins and this gets fixed.

**Why "solution altitude" (the hierarchy choice).** Layers descend by *how fundamental the choice is*. The root is the thesis bet; L1 is the nature of the signal; L2 is what we *do* with it (the objective form); L3 is how we induce it (method); L4 is how we measure success (the metric); L5 are the concrete experiments. The higher the layer, the more a node *re-frames* the problem rather than tweaks a knob — and venue-worthy novelty lives in the high-altitude reframings, not the low-altitude knobs. So "start from the highest untested layer" = "attack the most fundamental untested reframing first," which is exactly where a new positive result (or a sharper paper) would come from. (Hierarchy to be panel-critiqued once the literature sweep adds nodes — P4.)

**Status legend:** ✅ tested-positive · 🟡 partial · ❌ tested-negative (null/kill) · ⬜ untested · ◻️ untested+low-prior (argued-shut, not measured).

---

## The tree (rendered)

```
T0  ROOT: the LM↔brain linear map is a usable TRAINING SIGNAL, not just a measurement
│
├─ L1 · WHAT IS THE SIGNAL?  (its nature)
│   ├─ T1.1  real beyond confounds? .................... ✅ Q0/A2  (E002, E006)
│   ├─ T1.2  what is the *trainable* part — E[Y|S] only, or θ*-relevant residual? . 🟡 (E020 bounded; residual UNTESTED)  ⟵ A-ceiling
│   ├─ T1.3  which MODALITY? fMRI vs MEG/EEG vs ECoG vs behavioral ..... ⬜ (only fMRI done)  ⟵ A-signal
│   └─ T1.4  whose brain — per-individual vs group-averaged? .......... ✅ the averaging confound (E008/L016) — the methodological finding
│
├─ L2 · WHAT DO WE DO WITH IT?  (objective form)
│   ├─ T2.1  MATCH it (LM rep → predict brain) ......... ❌ the whole induction null (Q2/Q3)
│   ├─ T2.2  REGULARIZER / SELECTION PRIOR (improve OOD without injecting θ*-info; a different MI object I(W;Zⁿ)) . ◻️ L041  ⟵ A-direction
│   ├─ T2.3  cheap PROXY / fMRI-free surrogate as a selection signal ... ⬜ Q5
│   └─ T2.4  AUXILIARY multi-task target judged by a non-encoding metric ⬜
│
├─ L3 · HOW DO WE INDUCE / COUPLE IT?  (method — children of T2.1)
│   ├─ T3.1  distillation readout (LoRA) ............... ❌ E004/E005/E008
│   ├─ T3.2  full fine-tuning ......................... ❌ E017/E019
│   ├─ T3.3  objective family: MSE/cos ❌, CKA ❌, InfoNCE ❌ (E013b); OT / RSA-loss / CKA-at-scale ⬜  ⟵ A-readout
│   ├─ T3.4  substrate: same-subject voxelwise ❌ (E013); multi-subject n≥5 full-FT ⬜ (O1, data ready)
│   └─ T3.5  synthetic dense targets (TRIBE) at KD scale ⬜ (O2, I4)
│
├─ L4 · HOW DO WE MEASURE SUCCESS?  (the metric — the most under-explored axis)
│   ├─ T4.1  encoding R² / unique R² .................. (all our work)  ⟵ A-metric (monoculture)
│   ├─ T4.2  OOD perplexity ........................... ❌ bounded (E009)
│   ├─ T4.3  robustness (adversarial / distribution shift) . ⬜ (Guo'24 used EEG for exactly this — prior art)
│   ├─ T4.4  sample efficiency / low-data regime ...... ⬜ (the unscooped slice, L008)
│   ├─ T4.5  calibration / uncertainty ................ ⬜
│   └─ T4.6  compositional / structural generalization  ⬜
│
└─ PATH-A · the methodology / negative-result paper  (parallel branch; the floor)
    ├─ TA.1  averaging manufactures apparent brain-specificity .. ✅ E008/L016
    ├─ TA.2  matched-ppl + permuted-twin = the missing control .. ✅ protocol
    ├─ TA.3  the quality law: alignment ∝ −bits-per-byte (r≈−0.78) ✅ E015
    └─ TA.4  demonstrate the control shrinks an EXTERNAL published positive .. ⬜ O5 — the load-bearing missing piece
```

---

## Node table (machine-readable)

| id | layer | parent | claim | status | evidence | prior | rests-on assumption |
|---|---|---|---|---|---|---|---|
| T0 | root | — | brain↔LM map is a usable training signal | 🟡 | whole repo | — | — |
| T1.1 | L1 | T0 | signal real beyond confounds | ✅ | E002,E006 | — | — |
| T1.2 | L1 | T0 | trainable part = E[Y|S] only vs θ\*-residual | 🟡 | E020 | residual likely small | Y⊥θ\*\|S |
| T1.3 | L1 | T0 | non-fMRI signal (MEG/EEG/ECoG/behavior) | ⬜ | — | open | A-signal |
| T1.4 | L1 | T0 | per-individual vs group-averaged | ✅ | E008,L016 | — | — |
| T2.1 | L2 | T0 | match the brain (induction) | ❌ | Q2/Q3 | null robust | — |
| T2.2 | L2 | T0 | brain as regularizer/selection prior | ◻️ | L041 | argued-shut | A-direction |
| T2.3 | L2 | T0 | cheap fMRI-free proxy as selection signal | ⬜ | Q5 | sign unsettled | — |
| T2.4 | L2 | T0 | auxiliary multi-task, non-encoding metric | ⬜ | — | open | A-metric |
| T3.1 | L3 | T2.1 | distillation readout (LoRA) | ❌ | E004/05/08 | — | — |
| T3.2 | L3 | T2.1 | full fine-tuning | ❌ | E017,E019 | — | — |
| T3.3 | L3 | T2.1 | objective family (OT/RSA/CKA-at-scale untested) | 🟡 | E013b | low | A-readout |
| T3.4 | L3 | T2.1 | multi-subject n≥5 full-FT voxelwise | ⬜ | O1 (data ready) | likely null | — |
| T3.5 | L3 | T2.1 | TRIBE synthetic dense targets at KD scale | ⬜ | O2/I4 | null=best Fork-B | — |
| T4.1 | L4 | T2.1 | encoding R² metric | — | all | — | A-metric |
| T4.2 | L4 | T2.1 | OOD perplexity | ❌ | E009 | — | — |
| T4.3 | L4 | T0 | robustness / distribution-shift | ⬜ | Guo'24 prior | open | A-metric |
| T4.4 | L4 | T0 | sample efficiency / low-data | ⬜ | L008 | open | A-metric |
| T4.5 | L4 | T0 | calibration / uncertainty | ⬜ | — | open | A-metric |
| T4.6 | L4 | T0 | compositional / structural generalization | ⬜ | — | open | A-metric |
| TA.1 | PathA | T0 | averaging manufactures brain-specificity | ✅ | E008,L016 | — | — |
| TA.2 | PathA | T0 | matched-ppl + permuted-twin control | ✅ | protocol | — | — |
| TA.3 | PathA | T0 | quality law alignment∝−ppl | ✅ | E015 | — | — |
| TA.4 | PathA | T0 | external published positive shrinks at matched-ppl | ⬜ | O5 | high value | — |

---

## The climb queue (prioritized untested nodes — provisional, pre-sweep)

Ordered by *(venue leverage × tractability ÷ prior-of-null)*. This is the provisional order; it will be re-ranked after the literature sweep (P3) adds nodes and the thinking panel critiques it. Compute budget = 4× L40S → up to 4 nodes in flight.

1. **TA.4 (O5) — external matched-ppl demonstration.** Highest leverage: it is the one missing load-bearing piece of the already-near-complete Path-A paper, and a confirmed shrink is a *positive* result (a confound exposed in a published claim), not another null. Tractable (re-analysis, not new science). *Lit-scout running now to pick the target.*
2. **T2.2 (O6) — brain as regularizer / selection prior.** Genuinely different objective (a different MI object); the one node that is *argued*-shut but not *measured*-shut. If it improves OOD/robustness without moving encoding-R², that is a new positive and a different paper. Needs a clean design (the L041 side-channel made testable).
3. **T4.3 / T4.4 — non-encoding success metrics (robustness, sample-efficiency).** Attacks the A-metric monoculture. Brain-guidance may help something encoding-R² can't see; Guo'24 (EEG→robustness) is prior art to position against. Re-uses our trained checkpoints → cheap.
4. **T1.3 — non-fMRI signal (MEG/EEG/behavior).** Higher-altitude reframing; more setup cost (new data). Gated on the sweep showing it is a real gap.
5. **T3.4 (O1) — multi-subject n=6 full-FT.** Data ready, but likely-null and low-leverage (coverage, not a new claim). Run as a cheap parallel filler, not a headline bet.
6. **T3.5 (O2) — TRIBE synthetic at scale.** Multi-day; slot as a capstone if a higher node opens a door.

**Discipline (non-negotiable):** every node climbed gets the full ritual — design lock → run → thinking panel (counter-argument + socratic + premortem + first-principles) → verify each objection against data → address survivors → record in `experiments/E*.md` + `learnings.md` + this tree + `ladder.md` (rung flips only on Erfan's confirmation). A node's result then spawns/prunes nodes here before the next climb.
