# scripts/ — toy brain-alignment distillation pilot

The make-or-break feasibility pilot (charter §"highest-value next action", oracle
review): **does adding a brain-alignment loss during GPT-2-medium → GPT-2
distillation improve the student's encoding-model fit to fMRI — measured under
the anti-confound protocol — versus an identical brain-blind distillation?**

This is deliberately toy-scale and reversible. It exists to force the real
`L_brain` pipeline into existence and de-risk assumptions A1/A2, not to produce a
publishable number. Run everything with `uv run` and `HF_HOME=/home/centcom/data/hf-cache`.

## Files

| File | Role |
|---|---|
| `pilot_lib.py` | Scientific spine: seeding, hidden-state extraction, scalar + static nuisance baselines, contiguous-block CV, ridge encoding, and the capacity-fair variance partition. Data-source agnostic. |
| `distill.py` | GPT-2-medium → GPT-2 distillation loop. Logit-KD (KL, shared vocab) + optional brain-alignment loss (a trainable linear head from the student's middle layer to the training fMRI). |
| `data_adapters.py` | One interface `(texts, fmri, meta)`, swappable backends: `make_synthetic_fmri` (known-structure stand-in), `load_sentences_txt` (real Pereira sentences), `load_pereira` (real neural responses — ready for tomorrow). |
| `run_toy_pilot.py` | Orchestrator: loads data, runs both arms × seeds at matched budget, evaluates, writes `outputs/toy-pilot/<run>/{summary.json,results.csv}`. |
| `../configs/toy_pilot.json` | All hyperparameters + `smoke_overrides` for a fast CPU-friendly pipeline check. |

## The anti-confound protocol (non-negotiable — Feghhi 2024, learnings L003)

Baked in from day one, not bolted on at review time:

1. **Contiguous block CV, never shuffled** (`contiguous_folds`). Shuffling leaks
   via temporal autocorrelation and inflates R².
2. **Nuisance baselines.** Scalar block = token length + item position. Static
   block = mean *non-contextual* input embedding per item (the "bag of word
   vectors, no context" control).
3. **Capacity-fair variance partition** (`variance_partition`). The static block
   and the contextual LM features are PCA-reduced to the *same* number of
   components per fold, so neither gets an unfair dimensionality advantage:
   ```
   unique_R² = R²([length, position, PCA(static), PCA(context)])
             - R²([length, position, PCA(static)])
   ```
   `unique_R²` — the variance only the *contextual* representation explains, after
   length/position/lexical confounds — is the ONLY number we are allowed to call
   brain alignment. Raw R² is reported alongside but is the inflatable one.

## No-leakage split

Items are kept in stimulus order and split into a contiguous **train** block
(first `1 - eval_frac`) and a contiguous **eval** block (last `eval_frac`). The
brain-alignment loss only ever sees train fMRI. All encoding metrics are computed
by contiguous K-fold *within the eval block*, so no item used to shape the
student's representation appears in any encoding fold. The arms differ only in
`lambda_brain`; the teacher (and thus the static-embedding nuisance) is frozen and
identical across arms.

## Running

```bash
export HF_HOME=/home/centcom/data/hf-cache

# Fast pipeline smoke test (tiny, ~1 min):
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json --smoke

# Full hybrid run: REAL Pereira sentences + SYNTHETIC fMRI, 3 seeds:
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json

# Tomorrow — REAL neural responses (drop-in), once the Pereira .mat files land:
uv run python scripts/run_toy_pilot.py --config configs/toy_pilot.json \
    --backend pereira --data-dir data/pereira/<neural-responses>
```

## Data status (2026-06-09)

`docs/04-data-benchmarks.md` has the full survey. Short version: the SPOF is
resolved — LeBel ds003020 / Narratives ds002345 / Pereira are all open and
no-login. We pulled Pereira's `Pereira_Materials.zip` (OSF crwz7, 276 MB): it
ships the **stimulus sentences** and GloVe vectors but **not** the per-subject
neural responses, which live on a separate host. So tonight's run is the **hybrid
path**: real Pereira sentences, synthetic fMRI built from teacher features +
length/position confound + noise. A positive brain-loss effect on synthetic data
proves the **pipeline and the anti-confound machinery**, not the science. The
real neural matrix plugs into `load_pereira` row-for-row against these same
sentences.

## What this pilot is NOT

- Not a result. Synthetic responses cannot test whether real brain alignment is
  preservable — that needs the neural data (next session).
- Not the final `L_brain`. The trainable-head form is the simplest defensible
  option; frozen-encoding-map and CKA-style proxies are the next design decision
  (`docs/tasks.md`, `docs/hypotheses/`).
