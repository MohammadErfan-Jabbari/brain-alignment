# Experiment — E015: the alignment ∝ −perplexity LAW across model families (matched-ppl control, generalized)

**Created:** 2026-06-12 · **Status:** COMPLETE · **Mode:** working (analysis-support)
**Question:** Does brain-alignment track LM perplexity *across* architectures/families (gpt2 / pythia / Qwen), or only *within* the gpt2 lineage (E003's r=−0.88)? If cross-family, then any brain-tuning gain reported vs a non-perplexity-matched baseline is exposed to the L011 LM-quality confound — which is what makes matched-perplexity the load-bearing control (the paper's genuinely-novel control, per the v0.9 premortem).

## Design
8 off-the-shelf LMs, 3 families (distilgpt2, gpt2, gpt2-medium, gpt2-large; pythia-1b; Qwen2.5-0.5B/1.5B/3B). For each: (a) held-out perplexity on a **fair natural-text probe** (WikiText-103 test sentences), (b) brain-alignment = unique R² (mid-layer `n//2`, beyond length/position/static nuisance) on the standard participant-averaged Tuckute target. Fit unique-R² vs log-ppl across models (Pearson r + Fisher CI + OLS). `scripts/run_ppl_alignment_law.py` → `outputs/E015_ppl_alignment_law.json`.

## The methodological catch (counter-argument, fable — caught BEFORE recording a wrong conclusion)
**v1 measured perplexity on the 1000 Tuckute STIMULUS sentences** (short, designed "baseline-set" text). That probe **misranked capability**: it rated Qwen2.5-3B (18T tokens, 2024) at ppl 106 — *worse* than gpt2-large (40B tokens, 2019) at 72 — a clear quality inversion (a 151k-vocab model spreads softmax mass over a larger support on atypical English). The token-count check ruled out a tokenizer fix (Qwen 7847 vs gpt2 7864 tokens). v1 cross-family r was a misleading **−0.235**, and I (wrongly) read it as "the coupling is within-lineage only." The counter-argument predicted that a fair x-axis would push r *more negative*. **It was exactly right.**

## VERDICT (v2, fair WikiText perplexity probe): a STRONG cross-family alignment∝−ppl law
| model | family | ppl (WikiText) | unique R² |
|---|---|---|---|
| distilgpt2 | gpt2 | 175.0 | +0.0071 |
| gpt2 | gpt2 | 111.6 | +0.0170 |
| gpt2-medium | gpt2 | 83.2 | +0.0177 |
| gpt2-large | gpt2 | 72.6 | +0.0173 |
| pythia-1b | pythia | 60.3 | +0.0226 |
| Qwen2.5-0.5B | Qwen | 49.1 | +0.0356 |
| Qwen2.5-1.5B | Qwen | 36.8 | +0.0297 |
| Qwen2.5-3B | Qwen | 32.6 | +0.0371 |

**Pearson r(log-ppl, unique R²) = −0.929, 95% CI [−0.987, −0.650] (n=8, 3 families).** OLS slope −0.017 per nat of log-ppl. The fair probe also fixes the capability ordering (Qwen2.5-3B best ppl, distilgpt2 worst). Alignment is monotone in (approx) training-data scale: distilgpt2 < gpt2 < pythia < Qwen.

**What it licenses (scoped honestly):**
- **Cross-family, brain-alignment on the standard averaged benchmark is largely a function of LM quality (perplexity)** — generalizing E003's within-gpt2 r=−0.88 to architectures/families/scales. So a brain-tuning study reporting an alignment (or downstream) gain vs a *non-perplexity-matched* baseline can be reporting an LM-quality effect, not a brain-specific one → **matched-perplexity is the necessary control** (L011 generalized; the paper's novel control, now shown to bite cross-family).
- **Caveats (counter-argument):** (1) n=8 = 3 family clusters; the CI excludes 0 but the cross-family signal rides the capability/data axis (Qwen high-data aligns higher AND lower-ppl than gpt2). (2) Within-family r's are flat/noisy (gpt2 −0.58, Qwen +0.04, n=3 each, saturated narrow ppl range) — the law is a *capability-range* law, not a within-saturated-family one. (3) y-axis uses the geometric middle layer; a per-model best-layer sweep is the refinement (not expected to weaken r given it's already −0.93). (4) The "Qwen aligns better" gap is most parsimoniously training-data scale, not architecture.

## Best-layer robustness check (counter-argument caveat #6 — CLOSED)
Re-ran with each model at its **peak-alignment layer** over a depth grid {0.4,0.5,0.6,0.7,0.8}·nlayers (not the geometric middle): cross-family **r = −0.917, 95% CI [−0.985, −0.600]** — essentially identical to the middle-layer −0.929 (`outputs/E015_ppl_alignment_law_bestlayer.json`). Peak layers shifted (e.g. Qwen2.5-3B best at L25 not L18; alignment values rose slightly) but **the cross-family law is invariant to the layer choice.** Importantly, the **within-family r's flip sign** with layer choice (gpt2 +0.38 best-layer vs −0.58 middle; Qwen −0.20 vs +0.04) — confirming the within-family correlations are noise (n=3, saturated narrow ppl range); **only the cross-family/capability law is robust.** So claim ONLY the cross-family law, never a within-family one.

## Novelty (lit-scout grounded, 2026-06-12 — do NOT overclaim)
The raw finding (alignment tracks LM quality/perplexity) is **established, not novel**: Schrimpf 2021 (43 models, brain-predictivity ∝ next-word-prediction r=0.44), Hong 2024 (4 families, log-linear ppl↓→encoding↑), Antonello & Huth 2023 (scaling law, r=0.991 within OPT; LLaMA>OPT at matched size), Caucheteux & King 2022, Gao 2024 (alignment↑ with scale). E015's r≈−0.92 is a *tighter cross-modern-family + unique-R²* characterization, not a discovery. **The genuinely novel step is normative:** no brain-tuning paper (Schwartz/Aw/Moussa/Negi/Bilgin) perplexity-matches its baseline or raises the LM-quality-confound; E015 turns the established correlation into a *required control* for brain-tuning claims. (Caveat: Aw & Toneva 2023 showed gain-WITHOUT-better-ppl — the inverse direction; our control tests gain-BECAUSE-of-better-ppl, untested.) Pasquiou 2022: the ppl↔brain relation is non-monotone when RNN+transformer classes mix — so claim the law only within modern decoder transformers.

## Status
COMPLETE + robustness-checked + novelty-grounded. A clean cross-family demonstration (r≈−0.92, robust to middle vs peak-alignment layer + to the fair-vs-broken ppl probe once the probe is natural text) that the standard brain-score is largely LM-quality — directly supports the matched-perplexity control (paper §1/§2/§5). Both counter-argument caveats addressed (fair ppl probe + best-layer). The broken-probe→fair-probe episode is L030. Remaining optional refinement (more families OPT/Llama/Mistral) needs online access; the n=8/3-family-cluster caveat stands (the law rides the capability axis).
