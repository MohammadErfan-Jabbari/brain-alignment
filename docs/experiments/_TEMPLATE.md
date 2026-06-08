# Experiment — <name>

**Created:** YYYY-MM-DD · **Status:** design | running | done | killed
**Hypothesis:** `../hypotheses/HNNN_*.md` · **Mode:** exploratory | promotable

---

## Objective

<One sentence: what this experiment decides.>

## Claim tuple (verbatim from the hypothesis)

- Metric · Threshold · Baseline · Condition

## Design (lock before running)

- **Models / data:** (cached? path? license?)
- **Baselines:** (matched budget — state the parity explicitly)
- **Metrics:** (+ the statistical test)
- **Seeds:** (≥ 3 for stochastic)
- **Confound controls:** contiguous splits; nuisance baselines (length, position, static embeddings);
  report gains after confound subtraction.
- **Stop rule / compute budget:**
- **What counts as promotable vs exploratory evidence:**

## How to run

```bash
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache
uv run python scripts/<name>.py --seed 42 --config configs/<name>.json
```

## Iteration log

| Date | Run / seed | Command / config | Result (numbers) | Observation / anomaly | Next |
|---|---|---|---|---|---|
| | | | | | |

## Results

<Table of final numbers with uncertainty.>

## Interpretation

<What the evidence licenses — and what it does not. Update the hypothesis status and `../learnings.md`.>
