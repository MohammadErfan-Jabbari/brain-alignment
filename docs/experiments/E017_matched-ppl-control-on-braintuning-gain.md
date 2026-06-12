# Experiment — E017 (I2): the matched-perplexity control on a REPRODUCED brain-tuning gain

**Created:** 2026-06-13 · **Status:** DESIGN (locked before run; oracle gate pending) · **Mode:** working (autonomous)
**Roadmap:** implementation lane **I2** — "the matched-ppl control on an external published result (the main-track lift, premortem #1)." **Headline/spine call = Erfan (STOP at the verdict).**

## Why this, and why reframed from "external published result"
The brain-tuning literature (Negi-2025 NeurIPS, Schwartz-2019, Moussa-2025) reports gains from tuning an LM against fMRI, but **compares only to a vanilla pretrained baseline** — no perplexity-matched / generic-text-finetune arm, and (Negi) no permuted-brain *downstream* null (canonical `negi-2025_*`, "Assumptions and Limits"). E015/I1 showed cross-family alignment tracks LM quality (r≈−0.78 bpb; operative-band ≈−0.48), so **a brain-tuning gain measured against a non-ppl-matched baseline is exposed to the LM-quality confound** — the missing control.

**Literal reproduction of Negi-2025 is INFEASIBLE here** (its Chen-2024b *bilingual* EN+ZH fMRI is not on disk; we have LeBel English naturalistic voxelwise + Tuckute). **Reframe (data-driven, not a scope decision for Erfan):** reproduce a brain-tuning **encoding** gain on **LeBel** in the Negi/Moussa recipe (full fine-tune an LM to predict voxelwise BOLD, vanilla baseline), then add the two controls the field omits — a **matched-ppl / generic-text-finetune** arm and the **permuted-brain twin** — and ask whether the gain is brain-specific or a fine-tuning/quality artifact. **This also executes I3's untested "full-FT door"** on the available n=3 LeBel subjects (the denizenslab n=6 extension stays I3's blocked part); E013 already showed the *LoRA-readout* lever fails, so full-FT is the genuinely untested route.

## Design (arms, per subject UTS01/02/03; ≥3 seeds)
Build on `scripts/run_lebel_tune.py` (E013: brain_tune + permuted twin + E006 held-out-story unique-R² eval). **Add:** (1) a FULL fine-tuning mode (not LoRA), (2) a generic-text-finetune arm, (3) per-arm held-out perplexity.
1. **vanilla** — untuned base LM (Qwen2.5-0.5B; the field's only baseline).
2. **brain-FT** — full fine-tune to predict voxelwise BOLD (MSE readout over pooled segment features; HRF-delayed, the E013 recipe but full-FT) — the reproduced "gain."
3. **brain-perm-FT** — identical but block-permuted BOLD targets — brain-specificity null.
4. **generic-FT** — full fine-tune on the SAME stimulus text with the LM next-token objective, matched steps/compute — the **matched-ppl control Negi lacks** (does plain fine-tuning on the stimulus text buy the same encoding gain?).
**Measure per arm:** held-out-STORY unique R² (E006 pipeline: Lanczos→TR→FIR contextual features, phone-tier+eng1000 nuisance, story-CV ridge, NC-reliable voxels) AND held-out perplexity (to confirm arms 2 & 4 are ppl-matched; if not, use E015's law as the ppl-intercept).

## Predeclared readings (handles BOTH outcomes — premortem PM2 guard)
- **If brain-FT shows an above-vanilla encoding gain:** the I2 contribution is whether it survives the controls. **Brain-specific** only if brain-FT > generic-FT *at matched ppl* AND brain-FT > brain-perm-FT (per-subject, ≥3 seeds, bootstrap CI). If generic-FT matches it → the gain is a fine-tuning/quality effect (the field's missing control bites). If it doesn't beat the permuted twin → not brain-specific.
- **If brain-FT shows NO above-vanilla gain** (likely per E013 lever-failure + the E008/E011/E013b mechanism evidence): the finding is "the field's reported brain-tuning encoding gain does not reproduce under rigorous held-out-story + full-nuisance evaluation" — a publishable negative converging with E013, NOT a failure of the experiment.
- **Kill criterion (predeclared):** no claim of a brain-specific gain unless brain-FT beats BOTH generic-FT (matched ppl) AND brain-perm-FT with a per-subject gap whose ≥3-seed bootstrap CI excludes 0; n=3 LeBel = a per-subject existence probe (L021/L024), not a population claim.

## Anti-confound (mandatory, L003 / Hadidi bar)
Contiguous story-level held-out split (E006); phone-tier + eng1000 + length/position nuisance; per-kind permuted twin; report gains AFTER nuisance subtraction; per-subject inference (no cross-subject pseudo-replication).

## Open design questions for the oracle gate
- Is full-FT of a 0.5B LM on ~14 LeBel stories (small data) going to overfit / collapse ppl — and does the generic-FT arm correctly isolate "fine-tuning per se" from "brain signal"? Is matched-compute or matched-ppl the right matching variable?
- Is n=3 LeBel + ≥3 seeds enough for the per-subject existence claim, given E013's lever-failure suggests likely-null?
- Does reproducing on LeBel (English monolingual) fairly stand in for the Negi (bilingual) gain it's meant to control — or must the framing be "a representative brain-tuning gain," not "Negi's gain"?

**Output:** `outputs/E017_matched_ppl_control/`. **No rung flips without Erfan; headline/spine decision = Erfan (STOP at verdict).**