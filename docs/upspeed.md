# Upspeed — read first, write last

**Last updated:** 2026-06-10 (Session 6 — working — E003 KD-alignment kill-test, Layer 2a)

## Current state

Phase = **Run → Judge**, on the R03 ladder. Two rungs now hold on real data: **Layer 0/A2** (E002, the encoding signal is real) and now **Layer 2a** (E003, the perplexity-only-KD kill-test). E003's verdict is a **qualified PARTIAL**: ordinary perplexity/logit KD does **not** preserve a teacher's brain alignment for free — there is a clean monotone gradient (conventional gpt2 ≈ teacher > warm-KD ρ′=0.84 > distilgpt2 0.60 > from-scratch cold-KD 0.37 > floor), and from-scratch logit KD lands far below the teacher (Δ=0.018, p<0.001). So F1 is **not** in the `oota-2026` "preserve-by-default" trap. **But** the stronger claim — that KD sheds alignment *beyond* the perplexity it costs — is **unresolved**: alignment co-varies with LM quality (Pearson −0.88 on log-ppl), the KD-specific dissociation is only p≈0.1, and the cold arm is under-trained (ppl 4.5× teacher). F1 is therefore **neither killed nor confirmed** — it has plausible headroom worth one precise next experiment.

## What was done (Session 6 — working)

1. **Locked E003 design after two pre-run Opus adversarial reviews** (`b2f23bb`). The reviews caught the **initialization trap** (warm-init KD only measures fine-tuning drift) → added the **cold-init from-scratch arm** as the verdict; reframed preserve/destroy → **headroom/gap**; mandated ≥3 seeds, floor-anchored ρ′ with bootstrap CIs, a perplexity guard, fixed-layer verdict.
2. **Built `scripts/run_kd_alignment.py`** (`d11c89b`) — reuses `distill.py` (pure logit KD, λ_brain=0) + `pilot_lib` (the anti-confound partition). KD corpus = wikitext-103 sentences deduped against Tuckute.
3. **Ran it** (cold arm GPU 0 + warm controls GPU 3, parallel, ~1 h). References reproduced E002 to ~0.0003 across GPUs.
4. **Judged honestly** (`7483848`): a **post-run Opus skeptic refuted the preliminary "F1 confirmed" read** — the verdict is PARTIAL headroom, not a confirmed job. Recorded in `experiments/E003_*.md`, learnings **L011**, R03 ladder (Layer 2a) + R04 §8 (`b996a2c`).
5. **R04 §7 corrections to R03 were already applied** (prior session, `4b548d1`) — verified, nothing to do.

## What to do next (ordered — what's next to *run*)

1. **E004 — the resolving experiment (the real F1 test).** Alignment-guided KD (λ_brain>0) vs perplexity-only KD **at matched perplexity** (L011 — *not* just matched budget; that's the only design that attributes an alignment gain to the brain objective rather than to LM quality). The `distill.py` harness supports λ_brain>0 already; the open pieces are the $\mathcal{L}_{\text{brain}}$ form (**D010** — frozen encoding map vs CKA proxy vs trainable head) and a matched-perplexity stop rule. **This is the headline thesis experiment.**
2. **Converged cold arm** — re-run from-scratch logit KD to *matched perplexity* (more KD compute / smaller target) to de-confound under-training from alignment shedding. Cheap, settles whether cold-KD's near-floor alignment is real or a budget artifact.
3. **LeBel UTS03 voxelwise adapter** (FIR/lag, contiguous story splits) — the powered benchmark (thousands of voxels vs Tuckute's 5 ROIs) to confirm the ~0.005 gaps. Tuckute is a screen only. Data on disk; loader is the work, **not a config swap**.
4. **Layer 2 (A3)** still open — does induced/preserved alignment buy OOD generalisation or low-data sample-efficiency?

## Blockers

- **None rate-limiting.** Data staged, harness built, GPUs free. Next steps are method/experiment work.
- **Framing watch (sharpened by E003):** compete on the rate-distortion **trade-off curve** (R04 §4, 06 §4), and **always control perplexity** when comparing alignment across training objectives (L011). Do not quote E003's absolute shed fractions hard — they are PCA-rank-sensitive; only the gradient *ordering* is robust.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache`. GPUs: 4× L40S (0 + 3 free this session; 1 + 2 had other jobs). Long runs via the harness background runner (`run_in_background`), not bare nohup.
- **E003 rerun:** `CUDA_VISIBLE_DEVICES=0 HF_HOME=... HF_HUB_OFFLINE=1 uv run python scripts/run_kd_alignment.py --arms kd_cold kd_warm lmft_warm --seeds 0 1 2` (corpus prep: `--prepare-corpus`, needs network; uses `Salesforce/wikitext`).
- **E003 outputs:** `outputs/E003_{cold,warm}.json` (gitignored). KD corpus: `data/kd_corpus/` (gitignored).
- **Models cached:** gpt2, gpt2-medium, gpt2-large, distilgpt2, Qwen2.5 0.5/1.5/3/7B — all run offline.
- **Datasets on disk:** Tuckute (`data/tuckute2024/`), LeBel UTS03 (`data/lebel_ds003020/`), Pereira stimuli. Course material `data/course-material/` (do not re-OCR; `06-theory-grounding.md`).
- **Git:** `main`. Commit continuously/atomically (D007); push only when asked. GateGuard hooks disabled (D012).
