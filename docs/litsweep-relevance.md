# Literature-Sweep Relevance Taxonomy — what counts as related, and how hard to read it

**Purpose.** The "what to look for" half of the conference sweep (P3). The `conference-scout` tooling fetches venue paper lists + abstracts; this file defines which titles/abstracts are *relevant to this thesis*, biased toward the gaps the idea tree wants filled, plus the digest-priority rubric so reading effort is spent where it pays. Judge on **title AND abstract**, never title alone (Erfan's explicit instruction). Dedupe every hit against the 40 canonical notes in `docs/literature/canonical/` before queuing a digest.

## Topic clusters (seed terms → the relevance signal)

A paper is *candidate-relevant* if its title+abstract hits ≥1 core cluster (C1–C6) or a Path-B cluster (C7–C8). Embedding rerank then orders within the candidate set.

| # | Cluster | Seed terms (high-recall) | Tree tie |
|---|---|---|---|
| **C1** | Brain–LM alignment / neural encoding of language | brain encoding model, voxelwise encoding, fMRI/MEG/EEG language, brain-score, neural predictivity, representational similarity to brain, neural alignment of language models | T1.1, T1.3 |
| **C2** | Brain-guided / brain-informed *training* (our exact niche — the inversion) | brain-tuning, brain-informed fine-tuning, neural-data-regularized training, fMRI/EEG-supervised representation, cognitively-guided / brain-relevant bias, training with neural signals | T2.1, T2.2, TA.4 |
| **C3** | Knowledge distillation & model compression | knowledge distillation, logit/feature/representation distillation, contrastive distillation, dataset distillation, what transfers in KD, MiniLM, model compression of LMs | T3.x |
| **C4** | Representation similarity / alignment metrics | CKA, RSA, Procrustes, SVCCA, platonic representation, model stitching, universal/convergent representations, optimal-transport alignment | T3.3 |
| **C5** | Scaling / quality laws of representation & brain alignment | scaling laws for fMRI encoding, alignment vs capability/loss, emergence of brain-like representations, compression vs brain-likeness | TA.3, T1.2 |
| **C6** | Information-theoretic training signals | information bottleneck, mutual-information regularization, MI estimation in deep nets, rate-distortion representation learning, data-processing inequality in training | T1.2, T2.2 |
| **C7** | Bio-inspired regularization for generalization/robustness (**Path-B**) | neural/brain regularizer, brain-inspired inductive bias, auxiliary neural task improving robustness/OOD/sample-efficiency, cognitively-plausible prior | T2.2, T4.3, T4.4 |
| **C8** | Evaluation beyond accuracy, tied to representation (**Path-B metrics**) | robustness/adversarial, calibration, OOD generalization, sample efficiency, compositional/structural generalization — *when linked to representation quality or brain/neural data* | T4.3–T4.6 |

**Exclude (negative filter):** pure clinical neuroimaging with no ML model; BCI/decoding-for-control with no representation-learning angle; vision-only with no representation-alignment or distillation content; pure systems/hardware (SIGMETRICS-style); pure RLHF/alignment-as-safety (the *other* "alignment" — only keep if it touches representation similarity or distillation).

## Digest-priority rubric (where to spend reading effort)

After the candidate set is built and embedding-ranked, tier each survivor:

- **Tier 1 — full `paper-digest` (opus).** Directly attacks, overlaps, or could overturn a tree node. Always Tier 1: any *positive* brain-guided-training result (C2 — feeds TA.4), any brain/neural result judged on a *non-encoding* metric (C7/C8 — feeds T2.2/T4.x), any method we could directly borrow to induce or measure (a new distillation or representation-alignment objective). These are the nodes-in-waiting.
- **Tier 2 — skim-digest (sonnet, ~1 paragraph).** Useful method or context we'd cite or adapt but that doesn't move a node by itself (a KD trick, an encoding-model improvement, a scaling-law refinement).
- **Tier 3 — metadata only.** Topically adjacent, citation-pool only; recorded in the sweep index, not read in full.

Cap Tier-1 digests per sweep batch and `log()` what was dropped to Tier 2/3 — never silently truncate (a dropped Tier-1 reads as "covered" when it wasn't).

## Output of the sweep
A ranked candidate index per venue/year (`data/papers/litsweep/INDEX.jsonl`: {venue,year,title,abstract,cluster_hits,embed_score,tier,dedupe_match}), and Tier-1 survivors handed to `paper-digest` → new canonical notes → new nodes/edges in `docs/idea-tree.md`. Every new node records the paper that spawned it.
