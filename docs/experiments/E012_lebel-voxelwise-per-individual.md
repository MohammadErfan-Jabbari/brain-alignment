# Experiment — E012: per-individual brain-tuning on the POWERED voxelwise substrate (closes the substrate-mismatch limitation)

**Created:** 2026-06-12 · **Status:** DEFERRED — oracle-adjudicated as power-limited at n=3 (2026-06-12); the voxelwise per-individual question is carried by E013's same-substrate loop instead · **Mode:** working
**Direction:** close the manuscript's substrate-mismatch limitation (§6.5): the A2 *positive* is on LeBel voxelwise (powered), but the optimization *null* (E008) is on Tuckute ROIs. Run the per-individual optimization test on the SAME powered substrate — and get closer to Negi's naturalistic regime.
**Predecessors:** `E006` (powered A2 on LeBel UTS03, measurement-only; flagged the TR-level tuning loop "E007" as mean-over-voxels-underpowered, MDE +0.013) · `E008` (per-individual null on Tuckute ROIs) · `E011` (regime-robust on Tuckute)
**New data (acquired this session):** LeBel deep subjects **UTS01, UTS02** downloaded (20 stories each) via `scripts/download_lebel_subjects.py` — joins UTS03 → **n=3 deep subjects** (E006 had only 1; this is what makes a per-individual test newly possible).
**Code:** would extend `run_lebel_encoding.py` (measurement) with a TR-level brain-tuning loop (the un-built "E007") — a MAJOR new pipeline; build ONLY if oracle PASS on power.

## The question
On the powered naturalistic voxelwise substrate, does per-individual brain-tuning (LM tuned toward subject S's voxelwise BOLD) raise held-out-story unique R² vs its permuted twin — for each of 3 deep subjects? I.e. does E008's per-individual null **generalize to the substrate where A2 is powered**, or does a per-individual effect appear there (which would make the null substrate-dependent → qualify toward Fork-A)?

## Design (sketch — to lock at oracle)
- Per subject (UTS01/02/03): brain-tune Qwen-0.5B (LoRA, KD- or LM-anchored) toward that subject's TR-level voxelwise BOLD on train stories; measure held-out-story unique R² (E006 protocol: story-CV, phone-tier+eng1000 nuisance, NC-reliable voxels, untrained ref) for `mse` vs `mse_perm` (matched-regime permuted twin). Report perplexity.
- **The powered statistic (the crux — NOT mean-over-voxels, which E006 showed MDE +0.013):** per-voxel-paired (mse − perm per NC-voxel) and/or LH-language-region-restricted. Per-subject within estimate, then across-subject (n=3) sign/consistency.

## Predeclared decision rule
- **Per-individual effect EXISTS on the powered substrate:** per-voxel-paired (or region-restricted) gap excludes 0 consistently across ≥2/3 subjects, brain-specifically, at matched ppl → the Tuckute-ROI null (E008) is substrate-dependent; a per-individual effect appears on powered naturalistic voxelwise data → **qualify the thesis toward Fork-A** (major; rewrite). 
- **NULL on the powered substrate too:** confirms the per-individual null generalizes to where A2 is powered → **closes the substrate-mismatch limitation, hardens Fork-B**.

## The CRUX for the oracle (build-or-not)
1. **Can per-voxel-paired on n=3 deep subjects be powered, or is it E006-redux?** E006: mean-over-voxels MDE +0.013. Per-voxel-paired across ~11k NC voxels has huge nominal N but **spatial autocorrelation** inflates effective n (the same spatial-autocorr trap the E008 oracle flagged for transfer). Is there a valid powered statistic, or does this repeat E006's "structurally underpowered" conclusion?
2. **Is the heavy build (TR-level voxelwise brain-tuning loop = the un-built E007) justified** given E006 advised against it — does n=3 (vs E006's n=1) change the calculus?
3. **The permuted-twin validity under voxelwise tuning** (real BOLD more learnable → ppl divergence, the E011 lesson — does it recur at voxel scale?).
4. n=3 subjects: enough for a per-individual claim, or only a per-subject existence demonstration?

## Verdict: DEFER — POWER-LIMITED AT n=3 (oracle-adjudicated, 2026-06-12; L021)

The oracle gate returned **DEFER-POWER-LIMITED**, quantitatively:
- **The per-voxel "huge N" is illusory.** ~11k voxels are read from a *single* (mse, perm) model-pair per fold and are **spatially autocorrelated** (effective independent units ≈ resel count, O(10²) not 10⁴) → a per-voxel-paired CI is pseudo-replicated and anti-conservative (the spatial twin of the L003/L015 trap). Not a valid powered statistic.
- **The valid replication unit is the subject: n=3, df=2 → across-subject MDE ≈ +0.003** (between-subject biological variance doesn't shrink with more TRs) — ~10× the +0.0001–0.0004 per-individual effect E008 (n=9) measures. n=3 supports at most a *per-subject existence demo*, never a generalization claim; sign test 3/3 → p=0.125 (no power).
- **The L011 ppl-confound recurs HARDER** at TR-voxel scale (richer regime, real BOLD more learnable than permuted → arms diverge in ppl), and the ppl-covariate-intercept control needs an n that n=3 can't support — double bind.
- **Build cost** (the deliberately-unbuilt E007 TR-level voxelwise tuning loop, multi-day) **vs near-zero expected information**: a null is redundant with the cross-substrate Fork-B claim; a "positive" is uninterpretable (outlier risk, spatially anti-conservative, possible L011 artifact). No achievable n=3 result changes the thesis.

**→ BUILD only with a higher-N deep cohort (n≳8–10 within-subject-repeat subjects)** — data we don't have. Until then the substrate-mismatch limitation is honestly stated (manuscript §6.5): feasible, data-ready, power-limited at n=3. This is an **evidence-based defer (the gate decided on power), not a false stop.** Correcting the earlier session error: the data was never the blocker (it's public/acquired) — the blocker is subject-count for a powered per-individual claim.

## Status
DEFER (oracle-adjudicated, power-limited at n=3). Data (UTS01/02/03) acquired + retained for a future n≳8–10 cohort. Manuscript §6.5 updated. The per-individual-at-matched-ppl line is now closed on every substrate we can power (Tuckute ROI n=9 + this); the remaining open door is Negi's distinct objective+data regime.
