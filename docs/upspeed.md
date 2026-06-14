# Upspeed — read first, write last

**Last updated:** 2026-06-14 (Session 14 — autonomous working, forward program. **F1-close (E020 empirical-E[Y|S]
ceiling) DONE → bounded-not-closed, NO Fork-A.** Then built + launched **F2 (E019 faithful Negi reproduce-and-control)**
on LeBel; gentle-regime run in flight, strong-tune probe shows reproduction is fragile. Five thinking panels run
across the session; no rung flips; L3/F1 stays ❌.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (rung board + forward program). This is last-session prose.
> With no task, run `/orient`.

## What ran this session (working) — and the verdicts

### 1. F1-close = E020 (empirical-E[Y|S] ceiling) — DONE, panel-survived: NO Fork-A; ceiling bounded-not-closed.
Question: does the trained LM align to brain signal BEYOND the stimulus-predictable E[Y|S]? Decompose per-subject
BOLD Y_s = E[Y|S] + ε_s (LOO cross-subject mean); measure A_resid = LM→ε_s. denizenslab story_11, n=6, Qwen2.5-0.5B
L12, higher-language, ridge encoding (`scripts/run_eys_ceiling.py` + `run_eys_diagnose{,2}.py`).
- Oracle HOLD → hardened (ratio claim, repeat-split, reference-reliability gate, story=replication-unit). Pre-lock
  socratic + first-principles caught the claim was over-scoped → corrected to linear-channel + convergence (L039).
- Ran: naive flag fired (A_resid=+0.090, ρ=0.51 — apparent Fork-A). **NOT escalated — diagnosed.** Two diagnostic
  rounds + counter-argument + premortem: the +0.090 is **confirmed ARTIFACT** (leaked stimulus through a too-noisy
  n=5 reference + HRF autocorrelation). After fold-gaps + eng1000-partial the trained−untrained residual gap =
  **−0.018 ≈ 0**. The eng1000 nuisance-partial is partly **vacuous** (symmetric partial collapses A_shared too — L040).
- **Verdict:** NO Fork-A; ceiling **bounded-not-closed** (2nd instrument to wall at n=6, after TRIBE — ref-rel 0.33,
  ε-NC 0.17 = the KILL regime). E020 demoted to convergent corroboration; the spine rests on the POWERED
  per-individual nulls E008/E011/E017. **No rung flip.** D029/D030, L039/L040.

### 2. F2 = E019 (external reproduce-and-control) — BUILT + validated + launched (LeBel).
Reproduce **Negi-2025's ENCODING gain (tuned−vanilla)** — a different/easier contrast than E017's (real−permuted)
null — then break it with bpb-matched (arm c) + permuted (arm d). Oracle HOLD → **substrate moved denizenslab→LeBel**
(D031: deep subjects, 10-repeat NC, E006-powered; denizenslab walled twice). Power gate satisfied by E006.
- Built `scripts/run_e019_negi.py`: the **faithful Negi head** — per-word LM feats (grad) → **fixed Lanczos matrix
  (verified vs lanczosinterp2D, max|Δ|=2e-6)** → trim → zscore → 4-delay FIR → linear voxel proj → **NT-Xent** at TR
  resolution, full-FT (NOT the per-segment-mean readout L026/L027 showed degrades — the oracle's F1). Arms a/b/c/d;
  metrics enc-r (Negi) + uR² (E006). Smoke-validated; full-scale clears (vanilla enc_r=+0.146 = Negi scale).
- **Early read:** gentle regime (lr=1e-5) → gain (b−a)≈0, non-specific (b−d)≈0 — the predicted Fork-B. Strong probe
  (lr=1e-4) → **catastrophic forgetting** (ppl 50→11.5k), enc_r degrades. **Neither regime reproduces Negi's +0.13**
  → oracle's KILL-2 ("method/scale-fragile reproduction") emerging.

## What's next to run (fresh session)
1. **E019 gentle 3×3 run completes** in background (`outputs/E019_negi/results.json`; PID was 2257971 on GPU0) — the
   ppl-preserving baseline arm. Check it landed.
2. **E019 intermediate-lr sweep (oracle-gate first):** lr ∈ {2e-5,3e-5,5e-5}, track b_ppl + b_enc_r — find any
   regime that reproduces a Negi-scale gain without catastrophic forgetting. If none → honest verdict "Negi's encoding
   gain does not reproduce under faithful full-FT on LeBel+Qwen-0.5B" (publishable external-validity result, weaker
   than reproduce-then-break). If a regime reproduces a gain → test survival (b−c)/(b−d) → Fork-A check.
3. **Judge + counter-argument/premortem panel** on the COMPLETE E019 results. **Framing/headline = Erfan's call.**
4. Then F3 (I3 denizenslab n=6 full-FT) → F4 (E015 Q2).

## Blockers / open loops
- **E019 gentle run in flight** (GPU0); judge waits on completion + the intermediate sweep.
- **Reproduction faithfulness caveats** (note for the verdict): Qwen-0.5B vs Negi's BERT; our window-TR NT-Xent vs
  their batch; LeBel vs their data. Flag in any "non-reproduction" claim.
- **ANALYSIS-lane flags for Erfan (unchanged):** manuscript r≈−0.92→−0.78; induction null robust across
  LoRA+full-FT+objective+capacity; E020 adds the bounded ceiling (convergent corroboration); manuscript framing of
  the bounded ceiling + the E019 reproduction result are Erfan's analysis-lane calls.

## Key facts
- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. 4× L40S (used GPU0 gentle
  run, GPU1 probe in parallel). `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.
- **E020 substrate** = denizenslab (TRIBE mapper). **E019 substrate = LeBel UTS01/02/03** (D031 — off denizenslab).
- **Subagent routing (D026):** opus = think/analysis/design (panels, oracle, design-grounding); sonnet = doc-nav;
  haiku = mechanical. fable BANNED. This session: oracle×2, socratic, first-principles×2, counter-argument, premortem.
- **Git:** `main`, push only when asked. ~16 atomic commits this session.
