# Experiment — E012: per-individual brain-tuning on the POWERED voxelwise substrate (closes the substrate-mismatch limitation)

**Created:** 2026-06-12 · **Status:** DESIGN (oracle-gate pending — power is the crux) · **Mode:** working
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

## Status
DESIGN — **oracle-gate first** (the build is large + E006 cast power doubt; let the gate decide build-or-defer on power evidence, not a unilateral call). Data acquired (UTS01/02/03). If PASS → build the TR-level voxelwise tuning loop + run. If HOLD/KILL on power → the substrate-mismatch limitation is honestly characterized as "feasible but power-limited at n=3" (evidence-based, not a false stop).
