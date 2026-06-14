# Upspeed — read first, write last

**Last updated:** 2026-06-14 (Session 14 — autonomous working, forward program. **The IMPLEMENTATION lane's decisive
work is COMPLETE.** F1-close (E020 ceiling) DONE → bounded-not-closed, NO Fork-A. F2 (E019 reproduce-and-control) DONE
→ corroboration. Idea refined + literature-grounded + scope-corrected. Forward program: F3 superseded, F4 = analysis-lane.
~12 subagent runs (oracle×2, socratic, first-principles×3, counter-argument×2, premortem×2, lit-scout, paper-digest,
Explore). No rung flips; L3/F1 stays ❌; the spine is fully supported by POWERED evidence.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (rung board + forward program). This is last-session prose.
> With no task, run `/orient`. **The next high-value work is the ANALYSIS lane (Erfan).**

## What ran this session (working) — and the verdicts

### 1. F1-close = E020 (empirical-E[Y|S] ceiling) — DONE, panel-survived: NO Fork-A; ceiling bounded-not-closed.
`scripts/run_eys_ceiling.py` + `run_eys_diagnose{,2}.py`. Naive flag fired (A_resid=+0.090, apparent Fork-A) — NOT
escalated; diagnosed. After fold-gaps + eng1000-partial the trained−untrained residual gap = **−0.018 ≈ 0** ⇒
confirmed artifact (leaked stimulus via a too-noisy n=5 reference + autocorrelation). The eng1000 nuisance-partial is
partly vacuous (symmetric partial collapses A_shared too — L040). **2nd instrument to wall at n=6 (after TRIBE).** E020
= convergent corroboration; spine rests on E008/E011/E017. D029/D030, L039/L040.

### 2. F2 = E019 (external reproduce-and-control) — DONE, panel+positive-control-survived: corroboration, not clincher.
Built the **faithful Negi head** (`scripts/run_e019_negi.py`: per-word LM feats → differentiable Lanczos (verified vs
source, max|Δ|=2e-6) → FIR → linear voxel proj → NT-Xent, full-FT) on LeBel UTS01/02/03. **No positive encoding gain at
any lr** (gentle gain_r −0.0006±0.0027 n=9; sweep 2e-5/3e-5/5e-5 monotone-negative; 1e-4 catastrophic ppl→11.5k).
**NOT a clean "Negi doesn't reproduce"** — the raw-mean-r ruler is quality-insensitive (eval positive-control:
enc_r 0.5B +0.150 ≈ 3B +0.143), the gentle regime didn't move the LM (Δppl≈0), and decoder≠Negi's BERT. **E019 =
corroboration of the E008/E011/E017 lever-failure spine** (L036). "NON-NEGOTIABLE" framing RETIRED. D031/D032, L041/L042.

### 3. Idea refinement + literature grounding (lit-scout + first-principles + paper-digest).
- **SCOPE correction (L041, keystone):** the evidence supports the OPERATIONAL claim ("no brain-specific gain is
  INDUCIBLE beyond perplexity via the readouts tried"), NOT the information-theoretic "ε is task-independent noise."
  **Y⊥θ\*|S is an ASSUMPTION**, not a result. Applied to the ladder spine wording.
- **DPI side-channel (the remaining hole):** a brain-as-selection/regularization prior could improve OOD without
  injecting θ\*-info or moving the alignment metric (lecture-26 I(W;Z^n)); argued-shut by E009 (~0 fulcrum), NOT measured-shut.
- **Negi passes the permuted twin (Δr=0.133)** — so for ENCODING the only missing control is matched-ppl (E019 clincher = b−c, not b−d).
- **Lit positioning:** NOT scooped. New must-cites: **Jia-2026 L-PACT** (frozen-only, no ppl-match — scope-fence, canonical
  note written), **Raugel/King NeurIPS-spotlight** (size+context, not bpb-quality), **Hadidi/Feghhi → Nature Comms 2026**.
  **Refocused headline:** "brain-tuning gains are an LM-quality/FT-regime artifact, not per-individual brain signal —
  the missing controls + the powered per-individual null where averaging manufactures specificity + the E[Y|S] ceiling."

## What's next — the ANALYSIS lane (Erfan); implementation lane decisive work is DONE
1. **Scope correction in the manuscript** (the keystone analysis-lane fix, L041): restate the spine as the operational/
   inducibility claim; name Y⊥θ\*|S as an assumption; carve out the unmeasured DPI selection side-channel.
2. **Manuscript reframe to the refocused headline** + lit positioning (Jia-L-PACT, Raugel, Hadidi→Nature-Comms cite).
3. **Figures** confirm the recorded numbers; the E020 bounded ceiling + E019 corroboration as supporting boxes.
4. **Forward-program rungs (low priority):** F3 (denizenslab n=6 full-FT) = superseded/moot (run only for 100%-rule
   coverage, D033); F4 (E015 Q2) = analysis-lane extension.
**The spine rests on POWERED evidence already in hand — no new compute is needed to write the paper.**

## Blockers / open loops
- **ANALYSIS-lane flags (Erfan, unchanged + new):** manuscript r≈−0.92→−0.78; induction null robust across
  LoRA+full-FT+objective+capacity (now + Negi head); E020 bounded ceiling (convergent corroboration); **the scope
  correction (L041) + the refocused headline + the new-paper positioning are the keystone analysis-lane work.**
- E019/E020 substrates: E020 = denizenslab (TRIBE mapper); E019 = LeBel (D031, off the walled denizenslab).

## Key facts
- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. 4× L40S (this session ran
  3 GPUs in parallel: gentle run GPU0, strong probe GPU1, lr-sweep GPU2). `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.
- **Subagent routing (D026):** opus = think/analysis/design; sonnet = doc-nav; haiku = mechanical. fable BANNED.
- **Git:** `main`, push only when asked. ~22 atomic commits this session.
- New canonical note: `docs/literature/canonical/jia-2026_lpact-prediction-scores-not-enough.md`.
