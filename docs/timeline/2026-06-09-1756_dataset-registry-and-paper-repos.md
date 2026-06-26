---
title: "Session log — 2026-06-09-1756 — Dataset registry and paper-repos corpus"
tags: [timeline]
---

# Session log — 2026-06-09-1756 — Dataset registry and paper-repos corpus

## Purpose

Build a durable, broad-coverage dataset watchlist and a local reference corpus of paper code repos so that the next working session can pull data and inspect implementations without re-doing reconnaissance.

## Session mode

**Analysis** — consumed and catalogued existing evidence; produced two reference artifacts. No new scientific numbers generated.

## What happened

**1. Continuity check via gbrain.**
Recalled the prior session ("Establishment of Research Reports and Literature Synthesis"), confirming R01/R02 reports and the no-hard-wrap prose convention were the last committed work. Picked up from that baseline.

**2. Built `docs/05-dataset-registry.md` — living dataset watchlist.**
Catalogued every dataset that might be relevant (neural / behavioral / NLP-baseline). 11 neural/behavioral datasets received full feature profiles: modality, subjects, stimuli, license, access, size, noise ceiling, use-case fit, status. Low-priority/out-of-scope candidates got compact entries. Registered the file in `docs/README.md`'s map.

Research method: 8 parallel Sonnet subagents did direct page/paper fetches for the 6 datasets not already covered by [`04-data-benchmarks.md`](../04-data-benchmarks.md). Strict accuracy rubric — NOT-STATED for genuinely unknown fields, all sources cited. The 4 committed benchmarks (LeBel, Narratives ds002345, Pereira, Le Petit Prince) cross-reference `04` instead of duplicating its power analysis.

Division of labour now explicit: `04` = decision (powered benchmarks, D008); [`R02`](../reports/R02_datasets-and-code.md) = provenance (which paper used what + repos); `05` = broad availability watchlist. Each file states what it is and isn't.

Committed: cd79447.

**Key findings recorded in the registry:**
- zhu-2025 data is non-language (monkey motor / mouse visual) — out of scope.
- yin-2025 "Association" dataset is synthetic GPT-4 NLP fine-tuning, not a neural dataset; its neural ground truth is just Narratives — marked AUX.
- Highest noise ceilings: Tuckute 2024 (r≈0.56, curated-diverse sentences — serious PRIMARY candidate) and Fedorenko ECoG (r=0.17–0.22, ms temporal resolution but only 52 sentences).
- denizenslab CC0 reading-listening is the fastest open path to real data (regression-ready, working code in speech-llm-brain). Re-evaluating D008's "LeBel primary" against it flagged as a live, undecided question.
- Many subject-count discrepancies between packaged benchmark data and original papers, all flagged per-entry. Several licenses genuinely NOT STATED (Fedorenko, Blank, Tuckute OSF, Le Petit Prince).

**3. Built the paper-repos reference corpus.**
- `scripts/paper-repos.tsv`: tracked manifest (url, category, paper key) for all 21 repos referenced in R02.
- `scripts/clone_paper_repos.sh`: tracked, idempotent shallow-clone script; `UPDATE=1` to pull; logs SHAs to gitignored `data/paper-repos/MANIFEST.tsv`.
- Ran the script: 21 repos shallow-cloned into `data/paper-repos/` (~8.6 GB total, gitignored), 0 failures.
- Resolved two URLs R02 had left open: feghhi = `ebrahimfeghhi/beyond-brainscore`, merlin = `gab709/brain-llm-beyond-next-word`.

Committed: 8178046.

## Decisions made

No new formal decisions (no D0xx entries warranted — the re-evaluation of D008 LeBel-primary vs denizenslab is a live open question, not yet decided).

## Current truth

- `docs/05-dataset-registry.md` exists and is current. Tuckute 2024 is now a serious PRIMARY candidate (noise ceiling r≈0.56) that wasn't formally on radar before this session.
- 21 paper repos are shallow-cloned under `data/paper-repos/` (gitignored). Two previously-open URLs in R02 are resolved.
- Real neural data is still NOT on disk. The harness (E001) is still waiting for a real-data run.
- The D008 LeBel-primary decision should be re-evaluated against denizenslab CC0 before the first real-data pull. This is the first live decision item for the next working session.

## Next session

This should be a **working session**. Priority order:

1. Re-evaluate D008: LeBel ds003020 vs denizenslab CC0 (noise ceiling, subjects, download size, existing loader code). Make a decision, record it, then pull the winner.
2. Pull the chosen dataset (one subject to start). Verify the fMRI matrix is actually in the download before treating it as ready (L005 lesson).
3. Re-run E001 on real neural data — `--backend pereira` or the new backend. This is the actual scientific verdict on A1/A2.
4. Digest Merlin & Toneva 2026 and Toneva (paper-digest agent) for the G1 reframe check — still pending from prior sessions.

## Friction and improvements

No notable friction this session. The parallel subagent approach for dataset research worked well (8 agents, strict rubric, NOT-STATED discipline kept the registry honest). The division-of-labour clarification between `04`/`R02`/`05` should be maintained going forward.


## Related
- [`ladder.md`](../ladder.md) — the canonical status board
- [`map.md`](../map.md) — code system (Q/E/A/D/L) & journey map
