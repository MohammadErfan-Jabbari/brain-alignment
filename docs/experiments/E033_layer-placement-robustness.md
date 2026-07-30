---
title: "Experiment - E033: recorded-response loss-placement robustness"
tags: [experiment]
aliases: [E033, layer-placement-robustness]
---

# Experiment - E033: recorded-response loss-placement robustness

**Created:** 2026-07-30 · **Status:** DESIGN LOCKED - anti-confound and oracle precheck PASS; no outcome opened · **Mode:** working
**Predecessors:** [`E002`](E002_tuckute-encoding-feasibility.md), [`E004`](E004_brain-loss-lever-test.md), [`E005`](E005_alignment-guided-kd-tradeoff.md), [`E008`](E008_per-participant-f1-solidification.md)
**Coverage gap:** [`H002`](../hypotheses/H002_repeat-stable-biological-supervision.md#where-the-loss-should-enter)

## Objective and claim boundary

Test whether the participant-level recorded-response result in E008 depends materially on attaching the temporary response-prediction branch at the Qwen student's layer-12 hidden state rather than at its final hidden state immediately before the language-model output matrix.

The confirmatory claim is about the **attachment configuration**:

> Under the otherwise fixed E008 Qwen knowledge-distillation intervention, moving the same co-trained linear response head from `hidden_states[12]` to the final pre-logit hidden state changes the participant-general, correctly-paired-minus-permuted held-out brain-predictivity effect.

E033 does not identify gradient reach as the cause of any placement difference because placement changes both computational reach and the representation presented to the temporary mapper. A builder-only gradient audit diagnoses those mechanisms separately.

E033 does not test vocabulary-logit supervision, every hidden layer, a learned layer mixture, multiple simultaneous losses, another student architecture, another neural target, another optimizer schedule, or a universal brain-guided-training claim.

`READY-TO-RUN: YES`

No held-out E033 unique-\(R^2\), perplexity, participant contrast, fold contrast, or outcome artifact existed when this design was locked.

## Why this experiment is decision-relevant

[`E002`](E002_tuckute-encoding-feasibility.md) selected Qwen layer 12 because it was the strongest controlled encoding layer in the fixed measurement grid.
[`E004`](E004_brain-loss-lever-test.md), [`E005`](E005_alignment-guided-kd-tradeoff.md), and [`E008`](E008_per-participant-f1-solidification.md) then reused that layer as the intervention attachment without a prospective placement comparison.
The implementation adds the response loss to the total scalar loss before one backward pass, but the response branch attached at `hidden_states[12]` can update only trainable ancestors of that state.
For a 24-block Hugging Face causal decoder, `hidden_states[0]` is the embedding output and `hidden_states[12]` follows blocks 0 through 11; blocks 12 through 23 receive only the knowledge-distillation gradient from that branch.
The final hidden state follows block 23 and exposes every LoRA block to the response-loss gradient.

The current rewrite correctly scopes its conclusion to tested configurations, so the missing comparison is not a contradiction.
It is nevertheless a live coverage alternative that could change the recorded-response intervention conclusion.

The design follows the repository's canonical literature grounding:

- middle and upper-middle representations are established measurement candidates, not proven intervention optima;
- brain-tuning precedents train transformer parameters through a temporary response-prediction head;
- correctly paired versus structure-matched random or permuted targets is required to separate brain-response content from generic auxiliary regularization; and
- the temporary head can absorb an objective, so trunk-gradient entry must be measured rather than inferred from the scalar loss.

## Fixed models, data, and parameters

- Student: `Qwen/Qwen2.5-0.5B`, 24 decoder blocks.
- Teacher: `Qwen/Qwen2.5-1.5B`, frozen.
- Student adaptation: rank-16 LoRA, scaling 32, dropout 0.05, on the existing Qwen attention and feed-forward projection set.
- Input embeddings, pretrained base, and tied language output matrix remain frozen.
- Text objective: masked output knowledge distillation, teacher-to-student KL, temperature 2, multiplied by \(T^2\).
- Optimizer: AdamW, learning rate \(2\times10^{-4}\), batch 16, three epochs, maximum length 64, gradient clipping 1.
- Response objective: MSE through a separately initialized, co-trained linear hidden-to-five-ROI head, identical capacity at both placements.
- Placements: `mid = hidden_states[12]`; `final = hidden_states[-1]`.
- Participant targets: the nine complete Tuckute participants `797, 837, 841, 848, 856, 865, 875, 876, 880`.
- UID `853` is excluded prospectively under E008's incomplete-five-ROI rule.
- Stimuli: the ordered 1,000 condition-B Tuckute sentences.
- Outer content split: five rotating contiguous folds; tune on four folds and score only the untouched fold.
- Technical seeds: `0, 1, 2`.
- Matched null: five block-permutation draws inside each training partition for every participant, fold, seed, and placement.
- Language probe: the same fixed 1,000-sentence WikiText held-out probe used by E008.

The exact participant list, stimulus order, fold boundaries, permutation row maps, model revisions, executable hashes, calibration artifact, and command configuration are bound by the E033 manifest before outcome scoring.

## Builder and confirmatory separation

Builder participants are `848, 865, 875, 876`.
They may set the placement dose and pass the gradient gate using outer-training complements only.
No builder-stage unique-\(R^2\), perplexity, or held-out response outcome may be computed.

The confirmatory participant population is the untouched set `797, 837, 841, 856, 880`.
All five observed participants form the primary biological inference axis.
Builder-four and all-nine summaries are secondary and cannot rescue a failed untouched-five result.

## E033A: outcome-blind gradient, reach, and dose gate

### Final-hidden identity and block indexing

The runner must assert `num_hidden_layers == 24`.
In evaluation mode, applying the frozen language output matrix to `hidden_states[-1]` must reproduce the model logits within maximum absolute error \(10^{-4}\).
The response loss is never applied to vocabulary logits.

With separately prefit and then frozen fold-local ridge heads:

- the layer-12 auxiliary gradient must be finite and nonzero in every expected LoRA block group 0 through 11;
- its gradient norm must be at most \(10^{-12}\) in block groups 12 through 23; and
- the final-hidden auxiliary gradient must be finite and nonzero through block group 23.

Failure stops E033 before outcome training.

### Placement-dose calibration

The actual E033B intervention retains E008's co-trained linear head.
Calibration therefore uses the actual co-trained-head initialization, with identical head and LoRA initial states, batches, and target row maps across placements.

For each builder participant, all five outer-training complements, seeds 0 through 2, the aligned target, and five matched permutations, compute the initial unweighted auxiliary LoRA-trunk gradient norm before any optimizer step.
Let \(m_{12}\) and \(m_F\) be the medians for the layer-12 and final-hidden placements.

The placement weights are frozen as

\[
\lambda_{12}=10,
\qquad
\lambda_F=10\frac{m_{12}}{m_F}.
\]

No clipping or outcome-dependent recalibration is allowed.
Calibration passes only when:

- \(m_{12}\) and \(m_F\) are finite and positive;
- \(\lambda_F\in[0.1,100]\);
- the median weighted auxiliary-to-KD trunk-gradient ratios differ by no more than 10 percent across placements; and
- each placement's median weighted auxiliary-to-KD trunk-gradient ratio is at least 0.01.

The frozen-head aligned-versus-permuted and permutation-versus-permutation gradient distances and auxiliary-versus-KD cosines are reported as mechanism diagnostics only.
They do not establish biological specificity and are not configuration selectors.

### Dynamic co-trained-head nonabsorption gate

Use builder participants, outer fold 0's training complement, seeds 0 through 2, the aligned target, and fixed matched permutation draw 0.
Run the exact 150-step schedule for both placements without computing unique-\(R^2\), perplexity, or any held-out response outcome.

At optimizer steps 1, 75, and 150, record:

- the weighted auxiliary LoRA-trunk gradient norm;
- the KD LoRA-trunk gradient norm;
- their ratio and cosine;
- the temporary-head gradient norm; and
- the LoRA update norm from initialization.

All values must be finite and nonzero.
For each placement, the median real-arm weighted auxiliary-to-KD trunk-gradient ratio across the 12 participant-by-seed runs must remain at least 0.01 at every checkpoint.
The permuted arm is diagnostic.
Failure stops E033 before outcome training.

### E033A stop rules

Stop before E033B on any of:

1. final-hidden/logit identity failure;
2. block-gradient reach failure;
3. nonfinite or zero calibration gradient;
4. \(\lambda_F\) outside the frozen admissible interval;
5. weighted placement ratios differing by more than 10 percent;
6. an initial or dynamic real-arm trunk/KD ratio below 0.01;
7. nonfinite or zero dynamic update values; or
8. mismatch between the locked permutation arrays, initial states, batches, or manifest identities across placements.

## E033B: confirmatory placement factorial

### Training arms

For every participant, outer fold, and seed:

1. train one shared `kd_only` student with no response head;
2. train `mid_real`;
3. train `mid_perm0` through `mid_perm4`;
4. train `final_real`; and
5. train `final_perm0` through `final_perm4`.

The shared KD-only model is trained once per fold and seed, then scored against every participant and both evaluation layers.
Target arms total \(9\times5\times3\times2\times6=1{,}620\) models; shared KD-only adds \(5\times3=15\), for 1,635 trained models.

No learned mixture, simultaneous multi-layer loss, additional attachment layer, loss-weight sweep, checkpoint selection, or post-outcome extension is part of E033.

### Fixed evaluation layers

Every trained student is scored at both fixed evaluation layers with a fresh ridge readout fitted only inside the held-out scoring folds:

- `eval_final = hidden_states[-1]`, the confirmatory rescue endpoint;
- `eval_mid = hidden_states[12]`, the historical sensitivity.

The better evaluation layer is never selected after results.
The confirmatory classification is controlled by `eval_final`.

The evaluation uses E008's unique-\(R^2\) assay: length and normalized position plus the untuned-base static-embedding block as nuisance, capacity-fair fold-local PCA rank 50, and contiguous scoring folds.
Static and scalar nuisance arrays are byte-identical across arms.

## Estimand, estimator, and identifying assumptions

For placement \(p\in\{12,F\}\), evaluation layer \(e\in\{12,F\}\), participant \(u\), outer fold \(k\), and seed \(s\), define

\[
d^{p,e}_{uks}
=
U^{p,e,\mathrm{real}}_{uks}
-
\frac{1}{5}\sum_{j=0}^{4}U^{p,e,\mathrm{perm}j}_{uks},
\]

where \(U\) is held-out unique-\(R^2\).

The cell-level placement interaction at evaluation layer \(e\) is

\[
c^e_{uks}=d^{F,e}_{uks}-d^{12,e}_{uks}.
\]

For each participant,

\[
c^e_u=\operatorname{median}_{k,s}c^e_{uks}.
\]

The confirmatory estimand is the mean over the untouched five participants,

\[
\Delta_{\mathrm{place}}^F
=
\operatorname{mean}_{u\in\mathrm{untouched5}}c^F_u.
\]

It is the participant-average change in the correctly-paired-minus-permuted effect caused by moving the attachment configuration, evaluated in one fixed final-hidden measurement space.
It is not a comparison of raw trained scores and not proof that gradient reach caused the change.

The direct final-placement estimand is defined analogously from \(d^{F,F}_{uks}\).

Identification assumes that shared initial states, batches, folds, permutation targets, optimizer schedule, target dimensions, and matched gradient dose leave attachment configuration as the only systematic difference between the paired placements.
The matched permutation subtracts generic auxiliary optimization but does not identify every possible nonbiological target property.
The fixed evaluation layer separates the attachment comparison from post-outcome measurement-layer selection.

## Inference

Seeds and permutation draws are technical repetitions, never biological or stimulus inference units.

For each fixed evaluation layer:

- participant axis: use the five untouched participant values \(c^e_u\); report the mean, two-sided 95 percent participant \(t\) interval, one-sided sign test, Wilcoxon signed-rank test, and leave-one-participant-out means;
- fold axis: define \(f^e_k=\operatorname{mean}_{u,s}c^e_{uks}\) over untouched participants; report the mean, two-sided 95 percent fold \(t\) interval, fold bootstrap, and leave-one-fold-out means;
- the more conservative lower and upper endpoints across participant and fold axes govern the decision;
- report the same crossed analyses for the direct final-placement effect \(d^{F,F}\);
- report builder-four and all-nine analyses as secondary; and
- do not flat-bootstrap participant-by-fold-by-seed cells.

## Language-quality guard

For placement \(p\), comparator \(q\), participant \(u\), fold \(k\), and seed \(s\), define

\[
r^{p,q}_{uks}
=
\log\operatorname{PPL}(p,\mathrm{real})
-
\log\operatorname{PPL}(q).
\]

For \(q=\mathrm{perm}\), the comparator is the mean log perplexity over the five matched permutation draws.
Collapse seeds first:

\[
r^{p,q}_{uk}=\operatorname{mean}_s r^{p,q}_{uks}.
\]

Participant-axis values average over folds; fold-axis values average over untouched participants.

For real versus shared KD-only, both participant-axis and fold-axis one-sided 95 percent upper bounds must not exceed \(\log(1.05)\).
For real versus its own permutations, both participant-axis and fold-axis two-sided 95 percent intervals must lie wholly inside \([-\log(1.05),+\log(1.05)]\).

If either placement fails, E033 receives `LANGUAGE-GUARD-FAIL`; no rescue or rejection classification is licensed.
No failed cell is silently dropped.
Any differential arm failure, or failure of more than 5 percent of planned cells, aborts the scientific placement classification.

## Decision rule

The minimum meaningful placement effect is \(+0.001\) unique-\(R^2\).
This lies inside E008's achieved participant-sensitivity range and below the historical approximately \(+0.003\) averaged-target signal that motivated the coverage question.

`PLACEMENT RESCUE` requires all of:

1. confirmatory final-evaluation placement mean \(\Delta_{\mathrm{place}}^F\ge+0.001\);
2. its conservative two-sided 95 percent lower endpoint is above zero;
3. every leave-one-fold-out placement mean is positive;
4. at least four of five untouched participant placement effects are positive;
5. the direct final-placement mean is at least \(+0.001\);
6. the direct final-placement conservative two-sided 95 percent lower endpoint is above zero; and
7. the language-quality guard passes.

`MEANINGFUL PLACEMENT RESCUE REJECTED` requires the conservative one-sided 95 percent upper bounds for both the final-evaluation placement interaction and the direct final-placement effect to lie below \(+0.001\), with the language-quality guard passing.

Every other complete result is `INCONCLUSIVE`.
The layer-12 evaluation sensitivity cannot rescue a failed confirmatory endpoint.
These are analysis fields, not an adjudicated scientific verdict until `/interpret`.

## Outcome seal and authorized order

The authorized transaction is:

1. commit this locked E033 record;
2. implement dedicated runner, analyzer, manifest, and tests;
3. run synthetic and deterministic tests;
4. run E033A and seal its calibration artifact;
5. stop on any E033A failure;
6. run a two-participant smoke through training, dual-layer scoring, and aggregation without changing the lock;
7. stop on any smoke or schema failure;
8. write and hash the manifest, frozen lambdas, permutation row maps, executable identities, and E033A artifact before full outcome scoring;
9. train the shared KD-only models;
10. run UID-disjoint target shards on available GPUs;
11. aggregate without selecting layers, arms, participants, folds, seeds, or permutations;
12. retain the raw and analysis artifacts and their SHA-256 values;
13. route the load-bearing contrast to `/interpret`, independent statistical aggregation audit, and adversarial review; and
14. update the E033 verdict, manuscript authority, and status only after adjudication.

## Precheck

The anti-confound designer returned `HOLD` before implementation and supplied the control, calibration, crossed-inference, and stop-rule requirements now locked above.

The independent oracle returned two `HOLD` reviews.
The first required a fixed evaluation layer, untouched confirmatory participants, matched reruns, actual-head calibration, exact crossed inference, an explicit SESOI, participant/fold language guards, and a shared KD-only implementation.
The second corrected Hugging Face hidden-state indexing, required a dynamic co-trained-head nonabsorption gate, fixed the perplexity inference unit, and applied the SESOI consistently to both the placement interaction and direct final-placement effect.

After these changes, the oracle returned:

`ORACLE-PRECHECK: PASS / READY-TO-RUN`

## Planned artifacts

- `scripts/e033_layer_placement.py`
- `scripts/e033_analyze_layer_placement.py`
- deterministic tests under `tests/`
- `outputs/E033/gradient_gate.json`
- `outputs/E033/manifest.json`
- `outputs/E033/kd_reference.json`
- UID-disjoint `outputs/E033/placement_*.json` shards
- `outputs/E033/analysis.json`

Only the load-bearing gitignored artifacts used by the adjudicated manuscript claim receive stable hashes in this record.

## Results

`\gap`

## Interpretation

Not opened. Route aggregated evidence to `/interpret`.

## Related

- [Project status](../status.md)
- [Methodology](../03-methodology.md)
- [H002 biological supervision hypothesis](../hypotheses/H002_repeat-stable-biological-supervision.md)
- [Rewrite training architecture](../manuscript/rewrite/sections/C_training_architecture.tex)
