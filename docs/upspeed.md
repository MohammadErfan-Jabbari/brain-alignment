# Upspeed — read first, write last

**Last updated:** 2026-06-13 (Session 12 — autonomous working session, /goal set: implementation roadmap
I1→I2→I3→I4. **I1 DONE** (E015 expanded to 22 models/6 families, cross-family law corrected to r≈−0.78).
Now on **I2** (matched-ppl control). Erfan away ~24h.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (rung board + roadmap, D015). This is last-session prose.
> No rung moved this session. With no task, run `/orient`.

## Current state

Autonomous run through the implementation roadmap (D020/D021/D022). **Science verdicts UNCHANGED — no rung flipped.**

**I1 COMPLETE (2026-06-13).** Expanded E015's cross-family alignment∝−quality law from 8 models/3 families →
**22/6** (OPT, full pythia ladder, Qwen-7B, Llama-3.2 [unsloth mirror — meta-llama is gated], Mistral). Full
oracle+Codex+panel audit. **Verdict: r=−0.783** (bpb x-axis — per-token ppl is tokenizer-contaminated; family-
cluster CI [−0.911,−0.500], LOFO-robust). **Weaker than v2's −0.929** (which was inflated by per-token-ppl +
best-layer + 3-family span); floor-steepened, operative-band ≈−0.48, scale-controlled partial −0.675. **Q2 (arch
beyond quality): underpowered hypothesis** (Llama/Mistral +0.006–0.009 residual, vocab-robust, DPI-permitted;
n=1–2/family, p=0.20). **L016 tie-in:** law rides the averaged/shared-stimulus component. Learnings L034/L035.
Records: `docs/experiments/E015_*.md`, `outputs/E015_expand/`.

## What to do next (autonomous loop)

**I2 — matched-ppl control on a brain-tuning gain (in progress).** Negi-2025's literal multilingual pipeline is
INFEASIBLE (no Chen-2024b bilingual fMRI on disk). **Feasible reframe:** reproduce a brain-tuning *encoding* gain
on **LeBel** (full-FT an LM to predict voxelwise BOLD, vanilla baseline — the Negi/Moussa recipe), then add the
controls Negi explicitly omits: a **matched-ppl / generic-text-finetune** arm + the **permuted-brain twin**; show
the gain shrinks / loses brain-specificity. Uses `run_lebel_tune.py` + the E006 eval pipeline → **also advances
I3's full-FT door** (n=3 LeBel; the LoRA-readout lever already failed in E013, full-FT is the untested route).
Next concrete step: **design I2 → oracle-gate → build → get the number.** **STOP for Erfan at: does this become
the paper's headline/spine?** (his reserved call). After the verdict: thinking panel + Codex, record, commit.

## Blockers / open loops

- **I2 data:** Negi bilingual fMRI unavailable → reframed to LeBel full-FT (data on disk, E006 used it).
- **I3:** denizenslab n=6 still blocked (git-annex not installed); I4/TRIBE sidesteps it (P0 gate PASS).
- **ANALYSIS-lane flags for Erfan (do NOT edit unilaterally):** (1) manuscript "r≈−0.92" → correct to ≈−0.78
  (operative-band ≈−0.48); (2) new canonical `antonello-2023_*.md` + suggested `01-research-landscape.md` §A row.
- **Carry-forward:** reapply the `codex.mjs` sandbox patch after any codex plugin update.

## Key facts

- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs 4× L40S free.
- **bits-per-byte > per-token ppl** for cross-family LM-quality (vocab correlates with family). For a fixed probe,
  Δbpb = ΔKL. Use **no-prepend / skip-first-token** bpb (an eos-prepend poisoned Qwen2.5-3B). `run_ppl_alignment_law_expand.py`.
- **Subagent routing:** fable = adversarial/counter + oracle; sonnet = lit-scout/paper-digest/socratic/logger;
  haiku = mechanical fan-out. Codex = code-critic + rescue. Run the full panel after each verdict; verify objections
  vs data, then address. Spin up subagents liberally.
- **Llama-3.2 is HF-gated** (token lacks approval) → use `unsloth/Llama-3.2-{1B,3B}` (identical weights, non-gated).
- **Corrected numbers:** Tuckute functional NC ceiling 0.491/0.559 (not 0.353); Antonello OPT scaling r=0.91 (not 0.991).
- **Git:** `main`, push only when asked. **TRIBE env isolated** (`.venv-tribe`, torch<2.7) — never into thesis venv.