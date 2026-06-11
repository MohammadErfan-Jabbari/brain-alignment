# Experiment — E011: is the per-individual F1 null REGIME-SPECIFIC? (strong-regime per-subject test, vs Negi)

**Created:** 2026-06-12 · **Status:** DESIGN (oracle-gate pending) · **Mode:** working
**Direction:** the manuscript's key open test (§6). E008's per-individual null was under *light* LoRA (r=16, 3 epochs, frozen base → perplexity preserved). The counter-argument's live rebuttal: "you got null because you didn't tune hard enough — Negi 2025 got a *positive* per-individual encoding gain under full fine-tuning." E011 settles whether the null survives a strong regime.
**Predecessors:** `E008` (light-LoRA per-subject null, +0.0001) · `E004` (full-FT collapses perplexity 226→865) · `negi-2025` (positive per-individual encoding, full-FT, non-ppl-matched)
**Code:** **no new code** — `run_brain_lever.py` with `--uids` + `--lora-r 64`/`--no-lora` + `--epochs`. Verdict: `analyze_e008.py` (crossed inference).
**Output:** `outputs/E011_heavylora_Qwen.json`, `outputs/E011_fullft_Qwen.json`

## The question
Does a per-individual brain-specific alignment gain (kd_brain − kd_brain_permuted, held-out unique R²) emerge under a **stronger** brain-tuning regime than E008's light LoRA — and if it does, is it **perplexity-confounded** (L011)?

## The design insight (why we keep the control even under full-FT)
Both arms (kd_brain and its block-permuted twin) run under the **identical** regime, so the twin is matched on tuning-intensity *and* perplexity *by construction*. We can therefore crank the regime arbitrarily and the **paired (kd_brain − kd_brain_permuted) contrast stays a clean brain-specificity test** — we are not abandoning the matched-perplexity control, we are stress-testing it. We additionally **report perplexity per arm**: if a per-individual gain appears only when perplexity has degraded, that is the L011 LM-quality confound, not a brain-specific effect.

## Arms × regimes (9 Tuckute UIDs, the per-subject replication unit; crossed subject+fold inference)
- **Regime A — heavy LoRA:** `--lora-r 64 --epochs 6` (≈4× the light-LoRA capacity/steps; perplexity stays bounded but the representation moves much more).
- **Regime B — full fine-tuning:** `--no-lora` (Negi's regime; perplexity will degrade, per E004 — that is the point, and the twin controls for it).
- Arms each: `mse` (kd_brain) vs `mse_perm` (n_perm=3, the matched-regime brain-specificity null). `lm_only` reference.

## Claim tuple / decision rule (PREDECLARED)
- **Metric:** across-subject mean of per-subject e_u = median over folds×seeds of (uR²(mse) − uR²(mse_perm)), held-out; crossed subject(n=9)+fold inference (the conservative fold-clustered CI is the headline, as E008); report perplexity per arm/regime.
- **NULL is REGIME-ROBUST (strengthens the paper):** under BOTH heavy-LoRA and full-FT, the per-subject brain-specific gap CI still includes 0. → E008's null is not an artifact of light tuning; "you didn't tune hard enough" is refuted; the paper's claim hardens to "no per-individual brain-specific gain even under Negi-strength tuning."
- **Per-individual POSITIVE emerges (qualifies the paper toward Fork-A):** the gap CI excludes 0 under a strong regime, brain-specifically (beats the permuted twin), and survives LOO-fold/LOO-subject. → THEN check the perplexity: if the gain co-occurs with degraded perplexity and tracks it (L011), it is LM-quality not brain-specific (reconciles with our matched-ppl framing); if it holds at comparable perplexity to the twin, it is a genuine per-individual brain effect (a major positive — rewrite toward Fork-A-with-caveats).
- **Anti-confound:** unchanged (rotating folds, static nuisance from untuned base, permuted twin, per-subject). ≥2 seeds. Report perplexity (the L011 axis) prominently.

## Compute / scope
Heavy LoRA: 9 UIDs × 5 folds × 2 seeds × (mse + 3×perm + lm_only = 5) = 450 trains (heavier per-train than E008). Full-FT: slower per train + ppl-collapse risk → scope to a **subset (e.g. 3–4 UIDs) × 2 seeds** as a bracketing probe (if even full-FT on a few subjects shows nothing per-individual, the regime-robustness conclusion holds; if it shows a positive, expand). Stage across the 4 GPUs by UID. Pure in-domain; no new data.

## Status
DESIGN — oracle-gate pending (regime choice, full-FT scope, the ppl-confound read-out, LR for full-FT). Then run heavy-LoRA (all 9) + full-FT (subset), analyze with crossed inference, thinking panel, update the manuscript (this is the §6 open test).
