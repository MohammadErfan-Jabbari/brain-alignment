---
title: "Timeline — 2026-06-10 17:45 — E003: the perplexity-only-KD alignment kill-test (Layer 2a)"
tags: [timeline]
---

# Timeline — 2026-06-10 17:45 — E003: the perplexity-only-KD alignment kill-test (Layer 2a)

**Mode:** working (Design → Run → Judge). **Branch:** main. **Commits this session:** `b2f23bb` (locked design) → `d11c89b` (runner) → `7483848` (verdict) → `b996a2c` (ladder + L011).

## What ran

Ran **E003**, R04's Layer-2a kill-test: *does perplexity/logit-only knowledge distillation preserve or destroy a teacher LM's brain alignment?* — the cheap question that gates the F1 distillation thesis. gpt2-medium → gpt2 student, scored on Tuckute with the E002 anti-confound partition (contiguous CV, nuisance subtraction, capacity-fair PCA, NC-normalised), 3 seeds, two parallel GPU runs.

**Design was reshaped by adversarial review before any compute** (two Opus reviewers, pre-run): the obvious warm-init KD is a trap (it only measures fine-tuning drift, not distillation), so the verdict arm became a **cold-init (from-scratch) logit-KD student**; the binary "preserve/destroy" was reframed as a **headroom/gap measurement** (per R04 §4 rate-distortion framing); ≥3 seeds; floor-anchored retention ρ′ with bootstrap CIs; perplexity convergence guard; fixed-layer verdict; distilgpt2 demoted to free context.

## What the run showed

A clean, PCA-rank-robust **monotone alignment gradient**: conventional gpt2 (ρ′≈1.0) > warm-KD (0.84) > distilgpt2 (0.60) > from-scratch cold-KD (0.37) > untrained floor (0). From-scratch logit KD lands far below the teacher (Δ=+0.018, p<0.001) despite learning language (ppl 50000→477). So **perplexity-only KD does *not* preserve alignment for free** — not the `oota-2026` preserve-by-default trap.

**But the post-run Opus skeptic refuted the over-read.** The load-bearing claim — KD sheds alignment *beyond* the perplexity it costs — is unsupported here: alignment co-varies with LM quality (Pearson −0.88 on log-ppl, the pure-KD point sits exactly on the curve, gpt2 the lone outlier); the KD-specific dissociation (kd_warm < gpt2 at matched ppl) is only p≈0.09; the cold arm is under-trained (ppl 4.5× teacher), confounding "KD sheds" with "worse LM."

**Verdict (predeclared rule): PARTIAL headroom.** F1 is neither killed nor confirmed. The kill-test did its job — it eliminated both the "F1 confirmed" over-read and the "preserve-by-default" kill, leaving one precise next experiment.

## What's next to run (ordered)

1. **E004 — the resolving experiment.** Alignment-guided KD (λ_brain>0) vs perplexity-only KD **at matched perplexity** (E003's key lesson, L011 — not just matched budget). This is the only design that can show alignment recovered *beyond* what the LM objective implies. The `distill.py` harness already supports λ_brain>0; the open piece is the L_brain form (D010) + the matched-ppl stopping rule.
2. **A converged cold arm** — re-run from-scratch logit KD to *matched perplexity* (more KD compute or a smaller target) to de-confound under-training from alignment shedding.
3. **LeBel UTS03 voxelwise** — the powered benchmark (thousands of voxels vs Tuckute's 5 ROIs) to confirm the ~0.005 gaps; adapter still pending (Layer-3 work).

## Artifacts

- [`docs/experiments/E003_kd-alignment-preservation.md`](../experiments/E003_kd-alignment-preservation.md) (locked design + results + verdict + both reviews).
- `scripts/run_kd_alignment.py` (runner; reuses `distill.py` + `pilot_lib`). Outputs `outputs/E003_{cold,warm}.json` (gitignored). KD corpus `data/kd_corpus/` (gitignored).
- [`docs/learnings.md`](../learnings.md) L011; R03 §5 ladder (Layer 2a) + R04 §8 updated.
- **R04 §7 factual corrections to R03 were already applied** (commit `4b548d1`, prior session) — verified this session, nothing to do. R03 line-1 corruption does not exist (working tree clean).


## Related
- `ladder.md` — the canonical status board
- `map.md` — code system (Q/E/A/D/L) & journey map
