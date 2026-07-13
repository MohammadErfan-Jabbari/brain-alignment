---
title: "Experiment — E017 (I2): the matched-perplexity control on a REPRODUCED brain-tuning gain"
tags: [experiment]
aliases: [E017]
---

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

## ORACLE GATE → HOLD, REFRAMED (fable, 2026-06-13). All four fixes adopted; E017 re-scoped.
The pre-compute gate returned **HOLD** with a deep, correct critique. Reframe:
1. **E017 is NOT the I2 "supplied the field's missing control" claim — that already exists.** Negi's *stated* gap is the **downstream** matched-ppl control; on **encoding** Negi already ran the permuted/TR-shuffle null (his C2). E017 reproduces+controls an *encoding* gain → its permuted twin is largely redundant with Negi C2; only the generic-FT arm is new. **The downstream matched-ppl+permuted control already lives in E009 (bounded null); the cross-family quality law in E015/I1.** So the I2 contribution ("matched-ppl is the missing control") is **substantially already made by E009 + E015** — do not let the manuscript imply E017 closes Negi's downstream gap.
2. **Null-by-construction risk:** E013 ran this exact MSE-pooled-feature readout on these exact 3 subjects → mechanism failure at every λ (L027); E011 showed the binding constraint is the *objective*, not the *parameterization*. Full-FT is a parameterization change with worse catastrophic-forgetting risk → no mechanistic reason it beats vanilla where LoRA didn't. If no gain, the generic-FT control has nothing to control (the E009/L017 trap).
3. **E015-as-ppl-intercept is a category error** (it's a between-model correlation, operative-band CI includes 0 — not a within-model slope). Match ppl **by construction** (anchor/early-stop the generic-FT arm to the brain-FT arm's measured held-out ppl), not by covariate adjustment.
4. **E017 ≠ I3's door** (which is *multi-subject* denizenslab n=6); it's the closed n=3 LeBel readout with full-FT swapped for LoRA.

**→ RE-SCOPE: E017 = a cheap, single-subject FULL-FT FEASIBILITY GATE (a de-risking precursor to the I3 denizenslab build), NOT "the I2 control on a reproduced gain."** Predeclared (oracle PASS-path):
- Run **UTS03 (best SNR) full-FT** with the KD anchor (the E013-v2 rescue) + held-out OOD perplexity tracking. **`manip_ok` gate = does full-FT beat vanilla on held-out-story unique R² WITHOUT ppl collapse?**
- **PASS** (full-FT real_u > base_u, ppl not collapsed, and beats its permuted twin) → a **Fork-A-relevant surprise** (induction works via full-FT where LoRA failed) → **STOP for Erfan** before scaling to the full matrix.
- **FAIL** (full-FT can't clear `manip_ok` where LoRA couldn't, or only via ppl collapse) → **documented KILL of the LeBel-encoding/readout route** (converges with E013/E011); the I2 matched-ppl contribution is **banked in E009 + E015**; redirect remaining induction hope to I4/TRIBE (I3/denizenslab is data-blocked). This negative is itself a useful feasibility datum for the manuscript.
**Code:** `run_lebel_tune.py` extended with `--no-lora` (full-FT, lr 5e-5) + per-arm held-out ppl. **The matched-ppl `generic-FT` arm is built ONLY if `manip_ok` passes** (no gain ⇒ no control to run).

## VERDICT — full-FT induction NULL (the LeBel-encoding door is closed) — 2026-06-13
Ran the feasibility gate, then red-teamed it, then powered it (`outputs/E017_matched_ppl_control/`):
- **Aggressive full-FT (lr 5e-5, 3 ep), UTS03 ×3 seeds:** manip_ok **0/3** — full-FT real_u (mean +0.0057) < vanilla base_u (+0.0088), AND **catastrophic ppl collapse ×1.63** despite the KD anchor. Looked like a clean FAIL.
- **Adversarial check (the "under-tuned artifact" objection, verified against data):** a gentler ppl-preserving config (lr 1e-5, 2 ep) on UTS03 n=1 **flipped manip_ok to True** (real +0.0094 > base +0.0079, ppl ×1.22) — so the FAIL was partly a forgetting artifact. BUT the nudge was **not brain-specific** (permuted twin matched it: real−perm = +0.0014) and within base-run noise (±0.001). Borderline ⇒ powered it.
- **DECISIVE (gentle config, UTS01/02/03 × 3 seeds, n=9):** brain-specific gap (real − permuted twin) **mean +0.0003, 95% CI [−0.0002, +0.0008], p=0.274** (t=1.18). Per-subject: UTS01 +0.0005 (manip 0/3), UTS02 −0.0001 (0/3), UTS03 +0.0006 (2/3). **A clean NULL** — full-FT does NOT induce a brain-specific alignment gain at matched perplexity; the UTS03 n=1 flip was favorable noise.

**Reading (predeclared FAIL branch):** full-FT — the last untested *induction method* on the LeBel substrate — **fails like the LoRA readout did** (E013), converging with E011 (capacity-invariant), E013b (objective-invariant), E008 (per-individual null). The lever failure is **method-general, not parameterization-specific**. → **KILL the LeBel-encoding/readout induction route.** The matched-ppl-control *contribution* (I2's intent) is **banked where it actually lives: E009 (downstream matched-ppl + permuted-twin bounded null) + E015/I1 (the cross-family quality→alignment law).** E017 adds the confirmed negative that full-FT joins LoRA in failing.
**Honest caveats:** (1) n=3 LeBel = a per-subject existence probe (L021/L024), MDE-limited — but the point estimate is ~0 with manip_ok mostly False (full-FT doesn't even beat vanilla), not a power-limited "trending positive"; (2) the sole *still-untested* induction variant is **multi-subject naturalistic n≥5 (denizenslab — I3, data-blocked)**, and TRIBE-synthetic targets (I4). (3) Thinking-panel note: the gentle-config→powered sequence WAS the adversarial verify-then-address loop (it caught and resolved the forgetting-artifact objection empirically); given this is the 5th converging null with a clean CI/p, the full fable panel was not spun up — a cost-aware call, recorded for transparency.
**Status: COMPLETE (null). Not a Fork-A surprise → no Erfan stop required. No rung flips** (E013/Q3 already ❌; this reinforces it). **I3 stays data-blocked → proceed to I4/TRIBE** (the genuinely novel remaining induction-ceiling program).


## Related
- [`status.md`](../status.md) — the canonical status board
