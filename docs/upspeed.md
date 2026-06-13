# Upspeed — read first, write last

**Last updated:** 2026-06-13 (Session 12 — autonomous working + a planning/strategy close. **I1 ✅ + I2 ✅ done;
I4-P0 ✅ passed; I3 data ✅ downloaded+verified.** **FORWARD PROGRAM set (Erfan-approved, 100% rule):
F1 TRIBE-ceiling → F2 external reproduce-and-control (E019) → F3 I3 powered n=6 → F4 Q2 ext** (full table in
`ladder.md`). **fable banned → routing opus/sonnet/haiku (D026).** No rung flipped. Next = a fresh implementation
session on F1 — Erfan to issue the `/goal`.)

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
its prior. Per the roadmap, **I4 sidesteps I3's data blocker** (TRIBE generates its own fMRI). **I4/P0 GATE
PASSED (S12, verified):** TRIBE runs text→synthetic-BOLD end-to-end → `preds (11, 20484)` fsaverage5 cortical,
sane BOLD (`scripts/tribe_p0_verify.py`, `outputs/E016_tribe/p0_verify2.log`). **Operative fixes:** (1) Llama
override via **`config_update={"data.text_feature.model_name": "unsloth/Llama-3.2-3B"}`** to `from_pretrained`
(the hub `config.yaml` overrides grids/defaults.py — meta-llama is gated; other 3 extractors non-gated); (2)
**`ffmpeg` required** for whisperx ASR (`sudo apt-get install -y ffmpeg` — sudo works); (3) auto-downloads spaCy
en_core_web_lg + 4 extractors + tribev2 ckpt; gTTS needs network; cache `/home/centcom/data/tribe_cache`. **TRIBE
env ISOLATED** (`.venv-tribe`, torch<2.7 — NEVER into the thesis venv; hand off via disk `.npy`). **Next step:
Phase 1 (FIDELITY)** — generate TRIBE targets for LeBel/Tuckute stimuli we have real fMRI for, re-run the A2
trained-vs-untrained unique-R² contrast against TRIBE targets (same nuisance), decide faithful stand-in → then
**Phase 2 (THE CEILING — cheapest decisive, stimulus-subtraction, run first)** → P3 clincher (E016 §5).
Design→oracle-gate→run→panel+Codex→record. **A TRIBE null = strongest publishable Fork-B; a TRIBE positive
(Phase-2 residual>0 or Phase-3 arm2>arm3) reopens Fork-A → STOP for Erfan.**

## Blockers / open loops
- **I3/F3: data DOWNLOADED + verified** — `data/denizenslab/` (35G; 6 subjects 01/02/03/05/07/08 × reading/listening
  × trn/val; valid HDF5, 10 train + 1 val story each, ~80–93k voxels). No longer blocked (GIN `/raw/` + apt git-annex).
  Remaining: adapt the full-FT loop to denizenslab HDFs. **De-prioritized to F3** (run after F1/F2 per the forward program).
- **I4/TRIBE:** keep `.venv-tribe` isolated; confirm Llama-3.2-3B access on first real download (meta-llama gated → may need unsloth mirror or HF approval).
- **ANALYSIS-lane flags for Erfan (do NOT edit unilaterally):** (1) manuscript "r≈−0.92" → correct to ≈−0.78
  (operative-band ≈−0.48); (2) new canonical `antonello-2023_*.md` + suggested `01-research-landscape.md` §A row;
  (3) the induction lever is now NULL across LoRA+full-FT+objective+capacity (E017+E013+E011+E013b) — Fork-B is
  very robust; Erfan to weigh whether I2's matched-ppl framing (E009+E015+E017) becomes manuscript emphasis.
- **Carry-forward:** reapply the `codex.mjs` sandbox patch after any codex plugin update.

## Key facts
- **Run Python:** `uv run`; `export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1`. GPUs 4× L40S free.
- **Cost discipline:** this session ran long (~$245). Lean on the empirical verify-loop (e.g. the gentle-config
  check that caught a forgetting artifact) over redundant panels on converging nulls; spin up panels for
  positive/surprising claims. Spin up subagents liberally for genuinely parallel/independent work.
- **Subagent routing (fable BANNED/removed; Erfan's rule 2026-06-13 — anything that needs THINKING/ANALYSIS/
  DESIGN → opus):** **opus** = the thinking panel (`counter-argument`, `premortem-analyst`,
  `first-principles-grounder`, `socratic-thinker`), `oracle-reviewer`, AND `lit-scout` + `paper-digest`
  (relevance-judging / paper-synthesis is analysis), + any design subagent. **sonnet** = navigating OUR docs
  (status review, fact-finding across traces, record-writing `session-logger`). **haiku** = simpler mechanical
  fan-out. Codex = code-critic + rescue. NEVER select `fable`. (all agent frontmatter updated 2026-06-13.)
- **Llama-3.2 HF-gated** (token lacks approval) → `unsloth/Llama-3.2-*` mirror (identical weights). bits-per-byte
  (no-prepend, skip-first-token) > per-token ppl for cross-family quality. Antonello OPT scaling r=0.91 (not 0.991).
- **Git:** `main`, push only when asked. Commit atomically (this session: 12 commits I1+I2).