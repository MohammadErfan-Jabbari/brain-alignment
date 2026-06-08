# Learnings — the anti-amnesia file

Hard-won lessons, corrected mistakes, and dead ends worth remembering. The rule (from Nexus):
*"If the system does not remember the lesson, the same pain will return disguised as a new problem."*

Each entry: date, the lesson, and the evidence/why. Newest at the bottom.

---

### L001 — 2026-06-08 — Inherit the thinking from Nexus, not the machinery

Nexus failed twice in opposite directions: v1 over-specified (constitutional sprawl), v2 over-coupled
(a stage-machine demanding constant cross-surface synchronization). The durable lesson is *adaptive
semistructure* — add structure only when its absence costs truth. Applied here: no stage gates, no
dual-surface mirror; a plain `docs/` brain instead.

### L002 — 2026-06-08 — Brain-alignment is literature-strong but execution-light, and held a HOLD

The prior oracle review returned **HOLD, not PASS**: excellent Stage-2 reasoning, but zero
operational specificity (no named benchmark + power analysis, no concrete $\mathcal{L}_{\text{brain}}$,
no compute budget, no pilot, no deployment scenario). The fix is not more reading — it is a toy-scale
pilot. Don't repeat the literature loop; build the pipeline.

### L003 — 2026-06-08 — The dominant risk is measurement, not modeling

Two counter-evidence papers (Feghhi 2024, Oota 2024) show brain-alignment scores are easy to inflate
(split leakage, nuisance features, low-level confounds). Any result that doesn't survive contiguous
splits + nuisance subtraction is not a result. Bake the anti-confound protocol in from day one, not
at review time.

<!-- Add new lessons below as we hit them. Negative results count. -->
