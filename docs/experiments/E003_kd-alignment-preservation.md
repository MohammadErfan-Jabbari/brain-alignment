# Experiment — E003: does perplexity-only knowledge distillation preserve or destroy brain alignment? (R04 Layer 2a kill-test)

**Created:** 2026-06-10 · **Status:** DESIGN LOCKED (pre-run) · **Mode:** working
**Direction:** `../reports/R04_gap-analysis.md` §6(a) / §8 (Layer 2a) · `../reports/R03_brain-as-training-signal.md` (ladder)
**Theory:** `../06-theory-grounding.md` §2 (data-processing inequality) + §4 (rate–distortion = the F1 trade-off curve)
**Predecessor:** `E002_tuckute-encoding-feasibility.md` (A2 PASS — the encoding signal is real on Tuckute)
**Code:** `scripts/run_kd_alignment.py` (E003 runner), reuses `scripts/distill.py`, `scripts/pilot_lib.py`, `scripts/data_adapters.py:load_tuckute`
**Output:** `outputs/E003_kd_alignment.json`

---

## Objective — the single sharpest cheap question on the R04 ladder

R04's structural map (§1) places the thesis (F1) in the empty *shrink × optimize* cell, and §6 factors the sharpest question into a cheap decisive half and a thesis half:

> **6(a) — cheap, decisive, nobody has run it:** Does standard perplexity/logit-only knowledge distillation into a smaller student **preserve** or **destroy** the teacher's brain alignment? `oota-2026` answered this for quantization and pruning; it is *unmeasured for KD* — a far more destructive transform (KD re-fits a smaller function from scratch, rather than perturbing a fixed function).

This experiment is 6(a). It builds **no** `L_brain` and runs **no** alignment-guided KD — that is 6(b)/E004, and only happens if E003 shows headroom. E003 is pure measurement plus cheap perplexity-only KD runs.

## What E003 actually measures (reframed after adversarial review — see "Review" below)

Two Opus reviews (oracle-reviewer + an independent counter-argument) flagged that a naive "preserve vs destroy" binary **contradicts R04 §4 itself** (compete on the rate–distortion *curve*, not the binary) and that the data-processing inequality (`06` §2) makes "a compressed student loses *some* alignment" near-certain *in the limit* — so the scientific content is **how much**, not **whether**. E003 is therefore framed as a **gap / headroom measurement**:

- The teacher sits at an alignment level $A_T$ (the DPI ceiling a compressed student can inherit).
- Perplexity-only KD lands the student at $A_S \le A_T$.
- The **gap $\Delta = A_T - A_S$ is the headroom** an alignment-guided objective ($\lambda_{\text{brain}}>0$, E004) could recover. It is the vertical distance on the rate–distortion curve (`06` §4) between perplexity-only KD and the loss-free point at the same rate.
- **Large gap** ⇒ KD sheds alignment ⇒ F1 has a confirmed job. **~Zero gap** ⇒ perplexity-only KD is already near the DPI-tight bound ⇒ F1's win would be marginal (it survives only as a trade-off-curve / measurement-rigor note, the way `oota-2026` complicates the quantization story — *not* a headline).

E003 does **not** by itself kill or confirm F1 (that needs the two-curve comparison in E004). It **sizes the headroom** and answers 6(a).

## The initialization trap (the flaw the review caught — and the fix)

The obvious cheap design — fine-tune a **pretrained** `gpt2` student toward `gpt2-medium` with KD — is a **trap**. E002 already measured pretrained gpt2 at unique R² ≈ +0.020: such a student *starts at full teacher-grade alignment*, so a high retention just means "a few KD epochs didn't erase the alignment it was born with from pretraining." That is fine-tuning drift, not distillation, and it would yield a false "preserve" with ~80% probability. The DPI argument is about a *function fit from scratch* against teacher outputs; warm-start never instantiates that function.

**Fix (locked):** the verdict-bearing arm is a **cold-init (randomly-initialised) gpt2 student trained only via logit-KD** — the only arm where any alignment the student ends with was *transmitted through the KD channel*, not inherited from pretraining. Warm-init KD is kept as a labelled *fine-tuning-drift control*, and a *fine-tune-only (no-teacher)* arm separates corpus-drift from the KD objective.

## Models scored (all on Tuckute, full anti-confound, NC-normalised unique R²)

The **primary verdict comparison is entirely within 12-layer gpt2-architecture models at a fixed layer (L7, E002's gpt2 peak)** — so there is *no* cross-architecture layer confound and *no* winner's-curse layer selection for the comparison that decides the verdict.

| Tag | Model | Role | Init | Layer for verdict |
|---|---|---|---|---|
| **teacher** | gpt2-medium (24L, 355M) | DPI ceiling $A_T$ | pretrained | L14 (matched frac. depth ≈0.58; E002 peak) |
| **gpt2** | gpt2 (12L, 124M) | conventional same-arch reference | pretrained | L7 |
| **kd_cold** | gpt2 ← KD(gpt2-medium) | **THE 6(a) arm** | **random** | L7 |
| **kd_warm** | gpt2 ← KD(gpt2-medium) | fine-tuning-drift control | pretrained | L7 |
| **lmft_warm** | gpt2 ← plain-LM finetune | corpus-drift control (no teacher) | pretrained | L7 |
| **untrained** | gpt2 (random) | floor $A_0$ (≥3 seeds) | random | L7 |
| **distilgpt2** | distilgpt2 (6L, 82M) | FREE real-distillation *context* | distilled-from-gpt2 | L3 (frac. depth ≈0.5) |

Trained arms (`kd_cold`, `kd_warm`, `lmft_warm`) are run over **≥3 seeds** at **matched budget** (same corpus, same optimizer-step count) — single-run would leave a real 50% drop at p≈0.10 (review Objection 3). `distilgpt2` is scored against **gpt2** (its real teacher), never gpt2-medium (lineage-meaningless ratio); it is **context, not the verdict** — it carries a capacity confound (82M/6L vs 124M/12L) and its training included a hidden-state cosine term, so it is *not* perplexity-only and is upper-bound-friendly for retention.

## Claim tuple (predeclared, locked before running)

- **Metric:** NC-normalised unique encoding R² = [R²([len, pos, PCA(static), PCA(context)]) − R²([len, pos, PCA(static)])] / NC, contiguous 5-fold CV, capacity-fair PCA. Identical protocol to E002 (L003 anti-confound). NC(LangNetw) ≈ 0.353.
- **Floor-anchored retention** (the well-conditioned statistic — review Objection 4): $\rho' = \dfrac{A_S - A_0}{A_T - A_0}$, where $A_0$ = untrained floor, $A_T$ = gpt2-medium teacher. Denominator $A_T-A_0 \approx 0.029$ (vs the raw teacher ≈0.019), so it is far better conditioned than the naive ratio, and $\rho'=0$ correctly means "fell back to the floor" = destroyed. Bootstrap the CI over folds×seeds; **decide on $\rho'$ with its CI and on $\Delta=A_T-A_S$ with a paired CI + p — never on a raw point ratio.**
- **Convergence guard:** report each student's **held-out perplexity**. A cold student that never converged (perplexity ≫ teacher's) makes its alignment number *preliminary* (under-training confound, review Objection 5), not a clean verdict.
- **Robustness:** report unique R² at **n_pca ∈ {25, 50, 100}**; the verdict must be stable across PCA rank (else it is a representational-geometry artifact, not brain structure). Report the **full layer sweep**, not only the peak.

### Decision rule (headroom, conditioned on convergence)

Primary read on **`kd_cold`** (the only arm that answers 6(a)); corroborated by `distilgpt2` and interpreted via `kd_warm`/`lmft_warm`.

- **LARGE HEADROOM — KD sheds alignment, F1 has a confirmed job.** `kd_cold` unique-R² CI includes 0 / sits at the floor ($\rho' \le 0.33$) **and** $\Delta=A_T-A_S$ is significant (>2σ). An alignment-guided objective has clear room to recover.
- **SMALL HEADROOM — KD preserves alignment, F1 motivation is weak.** `kd_cold` CI overlaps the teacher ($\rho' \ge 0.80$), $\Delta$ not significant. Perplexity-only KD is already near the DPI-tight bound; F1 survives only as a trade-off-curve / rigor note, not a headline (the `oota-2026`-complicates-quantization outcome).
- **MODERATE HEADROOM (PARTIAL):** $0.33 < \rho' < 0.80$, $\Delta$ real but modest ⇒ headroom exists but is partial; **triggers confirmation on LeBel UTS03 voxelwise** (Layer 3, the powered benchmark — Tuckute is ROI-coarse, 5 dims, NC≈0.35, adequate only for a cheap screen).

Negative results count (D007 / charter). A SMALL-HEADROOM verdict is a real, publishable finding that re-weights the thesis, and it ends F1 *as a headline* cheaply — exactly what a kill-test is for.

## Design (locked)

- **Data (alignment):** Tuckute 2024 (`data/tuckute2024/`), 1000 isolated baseline sentences × 5 LH language ROIs, averaged over the 5 train UIDs (848/853/865/875/876). Rows ordered by `item_id` (contiguous-split friendly). Identical to E002.
- **KD corpus:** wikitext-103-raw-v1, split into sentences, **disjoint from Tuckute's sentences** (no train/eval leakage of the stimulus distribution; broad English to minimise domain shift). A held-out slice is reserved for perplexity. Capped to a fixed sentence budget shared by all trained arms.
- **KD objective:** `distill.py` with `lambda_kd=1.0`, `lambda_brain=0`, `lambda_hidden=0` — temperature-scaled (T=2) KL on next-token logits over the shared GPT-2 BPE vocab (token-aligned, no remapping). This is the *purest* perplexity-only KD — purer than distilgpt2 (which adds a hidden-state cosine term that would protect mid-layer structure). `lmft_warm` uses plain causal-LM loss (no teacher).
- **Matched budget:** identical optimizer-step count, batch size, max_length, lr across all trained arms. Compression ratio gpt2-medium→gpt2 ≈ **2.9×**.
- **Anti-confound (mandatory, L003):** contiguous-block CV only; unique variance after length+position+static-embedding subtraction is the only number claimed; untrained same-architecture control over ≥3 seeds; static-nuisance from the frozen reference so it is byte-identical across arms.
- **Stop rule:** fixed model set, fixed layer for the verdict (L7 for all 12L gpt2-arch models), fixed seed count (≥3), fixed step budget. No tuning toward a desired outcome.

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache
# one-time corpus fetch (network on; models stay cached/offline):
uv run python scripts/run_kd_alignment.py --prepare-corpus
# the experiment (GPU 0; teacher+student fit easily in 46 GB):
CUDA_VISIBLE_DEVICES=0 uv run python scripts/run_kd_alignment.py --seeds 0 1 2
```

## Results

_(pending run)_

## Interpretation

_(pending run)_

## Review (adversarial, pre-run — integrated into the locked design above)

Two Opus reviews stress-tested the draft before compute. Both independently identified the **initialization trap** as near-fatal (warm-init can only show drift, not distillation) → fixed by the **cold-init arm**. Both flagged the **binary-vs-curve** framing as contradicting R04 §4 → fixed by reframing E003 as **headroom/gap measurement**, with the F1 verdict deferred to the E004 two-curve comparison. Both quantified **underpower** (a 50% drop at p≈0.10 single-run) → fixed by **≥3 seeds** on verdict arms. Both showed the **raw ratio ρ is ill-conditioned** near the cutoffs → fixed by the **floor-anchored ρ′ with bootstrap CI**, deciding on Δ. Additional fixes: distilgpt2 scored vs gpt2 (correct lineage) and demoted to context; perplexity reported (convergence guard); fixed-layer verdict (no winner's curse) + PCA-rank robustness. Verdict after fixes: the design can give a trustworthy *gap* read for a clean preserve or a clean destroy; a PARTIAL outcome is the expected hard case and routes to LeBel voxelwise.
