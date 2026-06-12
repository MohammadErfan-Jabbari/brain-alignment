# Thesis-arc comprehension checklist (analysis-session teaching aid)

Running checklist for the Socratic walk-through of the brain-alignment thesis, R03 → now.
**Purpose:** verify Erfan deeply understands every layer before advancing. Updated live as we go.
Status: ⬜ not started · 🟡 in progress · ✅ mastered (demonstrated, not just read).

> This is a teaching artifact, not a source of truth. The science lives in `docs/ladder.md`,
> `docs/experiments/`, `docs/learnings.md`. If this ever disagrees with those, those win.

---

## The path (8 layers)

### Layer 0 — The frame & the bet ✅ (2026-06-12)
- [x] What "brain alignment" means: the *linear map* from LLM middle layers → brain activation.
- [x] MI = the lens; **encoding-model unique R²** = what we actually measure (corrected + verified).
- [x] Why *linear* on purpose: guardrail + tests linear-accessibility (verified).
- [x] The thesis bet: that map is a **usable signal**, not just a thing to measure.
- [x] Distillation = the first easy-to-measure **use case**, not the whole thesis (verified).
- [x] A1/A2/A3 and why A2 gates A1/A3 (dependent, not parallel — verified).

### Layer 1 — Measurement: is alignment even real? (L0/A2) ⬜
- [ ] Encoding model + unique R² — what we actually compute.
- [ ] The confound problem (Feghhi/Oota): length, position, low-level features, split leakage.
- [ ] The anti-confound kit: contiguous splits, nuisance baselines, permuted twin, noise ceiling.
- [ ] E002 (Tuckute ROI) + E006 (LeBel voxelwise) → why A2 PASSES, powered.

### Layer 2 — The lever: can you optimize it? (L1/E004) ⬜
- [ ] What `L_brain` is and the loss family (mse/cos/pearson/frozen/cka).
- [ ] "Lever" = does *optimizing* the loss *raise held-out* alignment (not just fit training)?
- [ ] Why E004 is only PARTIAL: brain-specific lever exists but fragile + perplexity-coupled.

### Layer 3 — The would-be headline and its collapse (L3/F1) ⬜
- [ ] E005's apparent +0.0081 — what target it was measured against (group-averaged).
- [ ] The panel catch: pseudo-replication (15 cells over ONE 5-UID-averaged target).
- [ ] E008: per-individual, n=9, well-powered → NULL (+0.00010, CI crosses 0).
- [ ] The protocol that bites: matched-perplexity + per-kind permuted-twin + per-subject inference.
- [ ] WHY matched-perplexity is the load-bearing control.

### Layer 4 — The reframe: Fork B & the averaging confound ⬜
- [ ] Why the NULL is the positive contribution, not a failure.
- [ ] The mechanism: averaging amplifies the shared stimulus-evoked component at an inflated ceiling.
- [ ] What "manufactures apparent brain-specificity" means and why prior work falls for it.

### Layer 5 — Robustness: closing every escape ⬜
- [ ] E011 (heavy LoRA — capacity): null holds; the knob that moves the rep wrecks ppl.
- [ ] E013b (contrastive/InfoNCE — objective): null holds.
- [ ] E013 (voxelwise — substrate): a *mechanism* failure, not a power limit → n≥5 moot.
- [ ] E014 (averaging on the ENCODING score): NOT a confound — why it's legitimate here.
- [ ] Why "robust across capacity/objective/substrate" makes the null trustworthy.

### Layer 6 — Practical payoff & the supporting law ⬜
- [ ] E009 (A3): bounded null, "null-by-construction" — what that phrase means.
- [ ] E015: alignment ∝ −perplexity law across families (r≈−0.92) and why it strengthens the control.

### Layer 7 — Where we stand & the open doors ⬜
- [ ] Manuscript v0.9 = the Fork-B story; what the headline is now.
- [ ] The one untested door: full-FT (not LoRA readout) on multi-subject naturalistic voxelwise.
- [ ] Why L4/F3 (fMRI-free proxy) is deferred/moot.

---

## Session log
- 2026-06-12 — path designed, checklist created. Assessing Erfan's starting point before Layer 0.
- 2026-06-12 — Layer 0 ✅ (frame, MI-vs-encoding-R², why-linear, A1/A2/A3 ordering, distillation-as-use-case).
- 2026-06-12 — Created `docs/07-concepts-primer.md` (plain primitives) after Erfan found E002 jargon opaque; pointers from E002/R03/README.
- 2026-06-12 — Taught E002 + E006 plainly (Tuckute/ROI/voxel/noise-ceiling/% of ceiling); taught statistical power + MDE (bathroom-scale analogy). Layer 1 content delivered; closing understanding-check still pending.
- 2026-06-12 — Created `docs/reports/R05_thesis-narrative-from-first-principles.md` (LIVING) covering the arc through Layer 1 / E007 reroute. Erfan wants it extended each session until it covers everything.
