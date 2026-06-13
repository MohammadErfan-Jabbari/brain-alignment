# Upspeed — read first, write last

**Last updated:** 2026-06-13 (Session 12 — autonomous working run, /goal set. **I1 ✅ + I2 ✅ both DONE.**
I3 data-blocked → **next = I4 / TRIBE capstone.** Erfan away ~24h. No rung flipped this session.)

> **Canonical state lives in [`ladder.md`](ladder.md)** (rung board + roadmap, D015). This is last-session prose.
> With no task, run `/orient`.

## Current state — implementation roadmap (D020/D021/D022). Science verdicts UNCHANGED; no rung flipped.

**I1 ✅ (E015 expanded, 22 models/6 families).** Cross-family alignment∝−quality law corrected to **r≈−0.78**
on **bits-per-byte** (per-token ppl is tokenizer-contaminated; v2's −0.92 was inflated). Floor-steepened →
operative-band ≈−0.48; scale-controlled partial −0.675. Q2 (architecture beyond quality): underpowered
hypothesis (Llama/Mistral +0.006–0.009 residual). L016 tie-in: the law rides the averaged/shared component.
Full oracle+Codex+panel audit. L034/L035.

**I2 ✅ RESOLVED (E017) — full-FT induction NULL.** Oracle reframed I2: Negi's literal pipeline infeasible
(no bilingual fMRI), and the matched-ppl contribution **already lives in E009 (downstream bounded null) +
E015 (the law)**. Reframed E017 → a full-FT feasibility gate: does FULL fine-tuning beat vanilla where E013's
LoRA failed? **NULL** — brain-specific gap (real−perm) mean +0.0003, 95% CI [−0.0002,+0.0008], p=0.27 (n=9,
UTS01-03 ×3 seeds, ppl-preserving). Full-FT fails like LoRA → **method-general lever failure** (converges
E013/E011/E013b/E008). LeBel-encoding induction route KILLED. **Not a Fork-A surprise.** L036.

## What to do next (autonomous loop) → **I4 / TRIBE capstone (E016)**

I3 (full-FT multi-subject denizenslab n=6) stays **data-blocked** (git-annex), and E017's full-FT null lowers
its prior. Per the roadmap, **I4 sidesteps I3's data blocker** (TRIBE generates its own fMRI). **Start I4:**
read `docs/experiments/E016_*.md`; the **TRIBE env is ISOLATED** (`data/paper-repos/tribev2/.venv-tribe`,
torch<2.7/numpy 2.2.6 — NEVER install into the thesis venv; hand off via disk `.npy`). **P0 gate PASSED**
(install+import); next P0 step = `from_pretrained` + a `predict` on sample text (weights non-gated, Llama-3.2-3B
access — note: meta-llama is HF-gated for us, used `unsloth` mirror for I1; check if TRIBE needs meta-llama).
Then phases **P1 fidelity → P2 ceiling (cheapest decisive, run before P3) → P3 clincher** (predeclared gates in
E016 §5). Design→oracle-gate→run→panel+Codex→record. **A TRIBE null = strongest publishable Fork-B; a TRIBE
positive reopens Fork-A → STOP for Erfan.**

## Blockers / open loops
- **I3:** denizenslab n=6 BOLD on GIN git-annex (not installed) → GIN HTTP `/raw/` or `apt-get install git-annex`.
- **I4/TRIBE:** keep `.venv-tribe` isolated; confirm Llama-3.2-3B access on first real download (meta-llama gated → may need unsloth mirror or HF approval).
- **ANALYSIS-lane flags for Erfan (do NOT edit unilaterally):** (1) manuscript "r≈−0.92" → correct to ≈−0.78
  (operative-band ≈−0.48); (2) new canonical `antonello-2023_*.md` + suggested `01-research-landscape.md` §A row;
  (3) the induction lever is now NULL across LoRA+full-FT+objective+capacity (E017+E013+E011+E013b) — Fork-B is
  very robust; Erfan to weigh whether I2's matched-ppl framing (E009+E015+E017) becomes manuscript emphasis.
- **Carry-forward:** reapply the `codex.mjs` sandbox patch after any codex plugin update.

## Key facts
- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs 4× L40S free.
- **Cost discipline:** this session ran long (~$245). Lean on the empirical verify-loop (e.g. the gentle-config
  check that caught a forgetting artifact) over redundant fable panels on converging nulls; spin up panels for
  positive/surprising claims. Spin up subagents liberally for genuinely parallel/independent work.
- **Subagent routing:** fable = adversarial/counter + oracle; sonnet = lit-scout/digest/socratic/logger;
  haiku = mechanical fan-out. Codex = code-critic + rescue.
- **Llama-3.2 HF-gated** (token lacks approval) → `unsloth/Llama-3.2-*` mirror (identical weights). bits-per-byte
  (no-prepend, skip-first-token) > per-token ppl for cross-family quality. Antonello OPT scaling r=0.91 (not 0.991).
- **Git:** `main`, push only when asked. Commit atomically (this session: 12 commits I1+I2).