# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

> **New to the codes?** → **[`map.md`](map.md)** is the visual map (legend + the whole journey as a tree). Quick legend: **Q**n = ladder rung / research question (Q0→Q5, in climb order); **E**nnn = experiment (the evidence); **A**1–A3 = the three assumptions; **D**nnn = decision; **L**nnn = learning. Rungs were renamed **L→Q** on 2026-06-15 (D036, execution-order numbering); pre-2026-06-15 timeline logs still use the old L labels — see `map.md` for the L↔Q table.

**Last updated:** 2026-06-16 (S18 — tooling/process. Hardened the `scientific-writing` skill from the R06 clarity audit (L046, D037); added a methodology non-negotiable (record-the-why of a design choice); built the swarm-wrap system (SessionStart hook + `wrap-auditor` + tier-scaled `/wrap`, D038). **NO experiment ran, NO science rung changed — ladder unchanged from S17.** — prior: S17 — analysis. **R06 precision sweep complete (thinking panel ×3, 8 fixes — semipartial/partial, untrained sign, tables, controls label, quality ordering, E006 CC_norm threshold); NO science rung changed.** — prior: S16 — analysis. **Restructured the write-up layer; NO science rung changed**, the ladder
is unchanged from S14. Renamed the ladder rungs **L→Q** in execution order and added `map.md` (legend + journey tree);
adopted the **finding-report convention** (D036 — one durable claim per file, flat append-only `R<NN>` IDs,
current-truth-only, Q-tagged, each mapping 1:1 to a manuscript Results section). **Retired R05** (frozen for history).
Wrote **R06** (Q0/A2 — the alignment signal is real beyond confounds), formalized as conditional-MI with a math-grounded
report convention; added a "presenting a measured quantity" + math-voice rule to the `scientific-writing` skill and the
**estimand-first lens** to the reasoning toolkit. **Resume point for the analysis lane = the finding-report set in
reading order (`reports/README.md`): R06 ✅ done → next R07 (Q1, plain KD does not preserve alignment).**
— prior: S15 — analysis/infrastructure. Built the three-layer deliverable model (D035) + the `scientific-writing`
skill; **NO science rung changed**, ladder unchanged from S14.
— prior: S14 autonomous working — **F1-close (E020 empirical-E[Y|S] ceiling) DONE → bounded-not-closed.**
Ran story_11 n=6: **NO Fork-A** (apparent A_resid=+0.090 = confirmed leaked-stimulus+autocorrelation; after fold-gaps +
eng1000-partial the trained−untrained residual gap = −0.018≈0). Ceiling **bounded-not-closed** — the empirical n=6 E[Y|S]
reference is too noisy (LOO ref-rel 0.33, ε split-half NC 0.17 = the oracle's KILL regime), the 2nd ceiling instrument to
wall at n=6 (after TRIBE). The nuisance-partial control is partly vacuous (symmetric partial collapses A_shared too — L040).
**E020 demoted to convergent corroboration; the spine rests on the POWERED per-individual nulls E008/E011/E017.** Five panels
run (oracle+socratic+first-principles+counter-argument+premortem); D029/D030, L039/L040. **NO rung flip; Q3/F1 stays ❌.**
**NEXT = F2 (E019), paper-critical.** — prior: S13 autonomous working — **F1 Phase-1 (TRIBE fidelity) ✅ PASS.** TRIBE-v2 validated
as a faithful in-pipeline fMRI stand-in: beats a strong nuisance floor (rate+articulatory+eng1000-PCA) in
higher-order language **Δ=+0.113 [+0.045,+0.181], 6/6, p≈0.03**; correct spatial profile. Two blockers solved:
voxel-space mapping → denizenslab mapper (D027); a TRIBE long-audio timestamp bug (L037). Oracle-gated +
counter-argument-hardened (rate-only floor was a strawman → Δ corrected from +0.165). **NO rung flip — Phase 1 is a
tool-validation gate, not a science rung; Q3/F1 stays ❌.** **F1 Phase 2 (ceiling) = INCONCLUSIVE** — single-story
group-avg TRIBE explains too little per-vertex variance (LM→TRIBE≈0.03 vs LM→real≈0.18) for the stimulus-subtraction;
the runner's "Fork-A" flag FAILED the predeclared vacuity gate ⇒ **confirmed ARTIFACT, NOT escalated** (the oracle's
pre-compute warning + the vacuity control worked). A2 reconfirmed on denizenslab. **Real wall hit → Phase-2 needs a
redesign** (stronger TRIBE target + ≥3 stories + frame-valid estimand), next focused session. — prior: S12
**I1 ✅ + I2 ✅ DONE.** I1: E015 → 22 models/6 families, cross-family law corrected to **r≈−0.78** bits-per-byte (was inflated −0.92); Q2 architecture-residual = underpowered hypothesis; L016 tie-in. I2 (E017): full-FT induction **NULL** (real−perm +0.0003, CI [−0.0002,+0.0008], p=0.27) — full-FT fails like LoRA → **method-general lever failure** (converges E013/E011/E013b/E008); matched-ppl contribution banked in E009+E015. **No rung flipped** (reinforces Q3/F1 ❌). I3 data✅ DOWNLOADED (35G, 6 subj). **Forward program landed (Erfan-approved, 100% rule): F1 TRIBE-ceiling (next) → F2 external reproduce-and-control (E019) → F3 I3 powered n=6 → F4 Q2 ext.** Roadmap I1✅→I2✅→I4-P0✅→forward-program. Analysis lane frozen at R05 §9. **Analysis-lane FLAG: manuscript "r≈−0.92" → ≈−0.78; induction now NULL across LoRA+full-FT+objective+capacity.**)

---

## Current position

**The honest story (post-E008 reframe).** Brain alignment is **robustly real and measurable** (Q0/A2, powered at voxel scale — E006). But **optimizing it does NOT produce a per-individual brain-specific alignment gain**: E008 (per-participant, n=9, well-powered, MDE≈+0.0006) returns a clean **NULL** (mean +0.00010, CI [−0.0004,+0.0006]). E005's headline +0.0081 was a **group-averaged-target** measurement — a higher-SNR read of the *shared stimulus-evoked response*, inflated ~1.7× by averaging and ~2.4× by one outlier fold — **not** per-person brain alignment.

**The POSITIVE contribution (the paper's spine — S8 panel, do not bury it as a "null"):** a **methodological finding + a confound-clean protocol**. The finding: **cross-subject target-averaging manufactures apparent brain-specificity** — a gain measured against a group-averaged fMRI target reads as "brain-specific" (beats a permuted twin) even when *no individual subject shows it*, because averaging amplifies the shared stimulus-evoked component at an inflated noise ceiling (the +0.0081→+0.00010 ~80× collapse, E008/L016). The protocol that detects it — **matched-perplexity + per-kind permuted-twin + per-subject inference with crossed subject/fold clustering** — explains a class of overclaims in the alignment-*training* literature (Negi/Schwartz baseline against non-ppl-matched vanilla models; this is the control they lack). **Fork B = a positive method + corrected claims:** (1) A2 real & powered; (2) **the averaging-confound finding + protocol** (the positive contribution); (3) the well-powered per-subject null; (4) **A3 — practical payoff** (E009, in progress).

**→ The experimental program is CLOSED, and the per-individual null is ROBUST across every axis we could probe.** A2 holds (powered); F1 and A3 are characterized nulls; the null survived four escape attempts run + panel-bounded this session — **LoRA capacity** (E011, heavy LoRA leaves it intact), **objective** (E013b, contrastive/InfoNCE ≈ MSE, both null), **substrate** (E013, the voxelwise distillation lever fails to take hold at any λ — a mechanism failure, not a power limit), and the **measurement side** (E014, averaging the *encoding* score is legitimate-SNR/estimand, not a second confound). Q5/F3 is moot. The manuscript (v0.9) is **complete as an artifact** (panel-converged, references verified, cross-refs resolve; gate = READY thesis/workshop). **We are now in the write-up phase.** The one untested door is a *different induction method* (full-FT on multi-subject naturalistic voxelwise — scoped as the next major build, §"Next session"). Details below.

> **Audit trail (S8, 2026-06-11, Erfan-confirmed):** the thinking-panel (counter-argument + premortem + first-principles, fable) caught — *before* compute — that E005's "CI excludes 0" was pseudo-replicated (15 cells over one 5-UID-averaged target) and that the planned LeBel transfer test was underpowered (`scripts/reanalyze_e005_e006.py`, L015). The pivot to a per-subject solidification (E008) then returned a well-powered null (L016), confirmed by a second panel. Rigor before compute caught an overclaim that would have been the thesis headline.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **Q0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS (powered)** | **E002** (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 nuisance, story-CV. Clears the Hadidi/Feghhi 2026 bar. |
| **Q1** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **Q2** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | 🟡 **PARTIAL** | **E004** — brain loss built (loss family; D010 → co-trained MSE leaning). Brain-SPECIFIC lever exists on the strong aligner (Qwen mse − its permuted twin = **+0.0032 [+0.0006,+0.0058]**), but small/fragile (fold-4 carries half) & sub-threshold on the 5-ROI screen (no arm raised Δ above base; MDE limits). `frozen`=non-specific regularizer; cka/cos worst. Co-varies w/ perplexity (L011/L012). |
| **Q3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → per-individual brain-specific gain? | brain term buys ~0 alignment at matched perplexity (paired, powered) | ❌ **NULL per-subject — ROBUST across capacity/objective/substrate** (averaged-target-only artifact) | **E008** (n=9, MDE≈+0.0006): mean +0.00010, t-CI **[−0.0004,+0.0006]**, fold-clustered incl 0, the 4 E005-averaged subjects individually null. Sensitivity sim: power 1.0 at δ=+0.003 → a TRUE null. **Robust to every escape:** **E011** (heavy LoRA r64/6ep) — null holds, +0.0004 (capacity didn't move the rep; λ that does wrecks ppl, L019); **E013b** (contrastive/InfoNCE objective, n=9) — null holds, −0.0002 at matched ppl (L025); **E013** (voxelwise same-substrate, λ-sweep UTS01/02/03) — the distillation lever never improves held-out alignment over base and never beats its permuted twin, a single-subject *mechanism* failure so n≥5 is moot (L026/L027). E005's +0.0081 was a group-averaged / shared-stimulus-response artifact, NOT per-person alignment. → Fork B. **One untested door:** a *different induction method* — full-FT (not a LoRA distillation readout) on multi-subject naturalistic voxelwise (denizenslab n=6; queued as next major build). |
| **Q4 · A3** | Does induced alignment *buy something practical* (OOD) at matched perplexity? | gains stay confined to the alignment metric | ❌ **bounded NULL** (E009, n=8, panel-adjudicated) | No brain-specific OOD-ppl payoff (kd_brain ≈ kd_brain_permuted ≈ textfeat ≈ kd_ppl, all within measured MDE 0.03–0.13) — AND **null-by-construction**: the fulcrum (brain-specific repr change at matched ppl) is itself ~0 (median +0.004, seed-0-outlier-driven; can't grow it without collapsing ppl). Ties to E008/L016. Negi-2025's positive is vs a non-ppl-matched baseline (L011 confound) — our matched-ppl+permuted control is the contribution. Limits: OOD-ppl is a weak proxy; perturbation/sample-eff axes not run (moot with fulcrum ~0). L017. |
| **Q5 · F3** | An fMRI-free *proxy* (neighborhood-overlap / LID surrogate) that recovers most of the benefit | surrogate recovers little of the Q3 benefit | ⬜ **not started** | stretch / PhD seed. LID sign is unsettled (cheng vs yu) — validate direction against real fMRI first. |

## Supporting tracks (not rungs, but gate the rungs)

| Track | Status | Note |
|---|---|---|
| Data — Tuckute 2024 | ✅ staged + in use | ROI-level screen (5 LH lang ROIs), `data/tuckute2024/` |
| Data — LeBel UTS03 voxelwise | ✅ **built + run (E006)** | adapter `scripts/lebel_adapter.py` (reuses official deep-fMRI-dataset pipeline); CC_norm voxel selection; powered A2 confirmed |
| Literature | ✅ done | R03, R04, 14 canonical notes (+ hadidi-2024 anti-confound bar; lit-fork sweep leans B) |
| Manuscript v0.9 | ✅ artifact-complete + mock-peer-reviewed | PASS thesis / borderline-PASS workshop (oracle+premortem+counter-argument, fable, L029). Power claim hardened with a real-residual bootstrap positive-control (group test power 0.92@uniform-δ=+0.002, first-principles VALID). **E015** folded in: cross-family alignment∝−ppl law (v2 cited r≈−0.92 — **CORRECTED by I1 to r≈−0.78** bits-per-byte, 6 families/≈2 generations; operative-band ≈−0.48; the v2 −0.92 was inflated by per-token-ppl + best-layer + 3-family span; manuscript update pending = analysis-lane FLAG) strengthens the matched-ppl control (L030→L034). **E014** (`experiments/E014`): averaging the *encoding* brain-score is legitimate higher-SNR/estimand (per-subject positive), NOT a second confound → verified NOT-a-lift, correctly kept OUT of the paper (L028). **Open (Erfan/fresh build):** the premortem's spine reframe → matched-ppl-as-missing-control demonstrated on an external result. |
| Theory grounding | ✅ done | `06-theory-grounding.md` (MI bound, DPI, conditional-MI, rate-distortion) |
| Harness | ✅ **`$\mathcal{L}_{\text{brain}}$` built** | `brain_loss.py` (mse/cos/pearson/frozen/cka + block_permute); `run_brain_lever.py` (LoRA brain-tune); `run_lebel_encoding.py` (powered voxelwise); `distill.py` λ_brain |

Legend: ✅ done · 🟡 partial / in progress · 🔵 next (designed) · ❌ tested-negative / kill fired · ⬜ not started.

---

## Next session (what `/orient` surfaces)

### ▶ THE FORWARD PROGRAM — REORDERED S13 (D028). Sequence: **F1-close (E020) → F2 (E019) → F3 (I3) → F4 (E015 Q2)**; TRIBE Phase 3 = optional.
The forward path, kill-gated; **no rung flips without Erfan.** The spine (SCOPED — L041, S14): the OPERATIONAL claim
the evidence supports is *no brain-specific alignment gain is **inducible** beyond perplexity via the readouts tested
(linear-ridge/MSE/contrastive), across LoRA/full-FT/objective/capacity* (powered: E008 + E011/E013/E017) — unifying
the averaging confound + the matched-ppl quality law + the induction null + the (bounded) ceiling. The stronger
information-theoretic reading (*the brain's training-useful signal IS E[Y|S]; the residual is task-independent noise*)
rests on **Y⊥θ\*|S as an ASSUMPTION** (the DPI ceiling premise), not a result — state it as such. **Unmeasured side-channel
(L041):** a brain-as-selection/regularization prior could improve OOD without injecting θ\*-information or moving the
alignment metric (a different MI object, lecture-26 I(W;Z^n)); argued-shut by E009's ~0 fulcrum, NOT measured-shut.

**⏭️ NEXT: the IMPLEMENTATION lane's decisive work is COMPLETE (D033) — the next high-value work is the ANALYSIS lane
(Erfan): scope correction (operational claim; Y⊥θ\*|S as assumption; the DPI selection side-channel — L041), manuscript
reframe to the refocused headline, lit positioning (Jia-L-PACT/Raugel/Hadidi→Nature-Comms), figures.** Remaining
forward-program rungs: **F3 (I3 denizenslab n=6 full-FT) = SUPERSEDED/moot** (the powered full-FT induction null is
already in hand via E017 + corroborated by E019; denizenslab n=6 is reliability-walled + blind-ruler — run only for
literal 100%-rule coverage); **F4 (E015 Q2) = analysis-lane extension.** **DO NOT retry ceiling-closure (D034):** the
E[Y|S] ceiling is instrument-limited on ALL substrates (TRIBE weak, denizenslab n=6 walled, LeBel n=3 worse + no
cross-subject mapper) — it rests as a bounded corroboration; closing it would need acquiring ≥3 more deep LeBel subjects
with the 10-rep story (a data-acquisition decision, not a re-run). **The DPI selection-channel is null-by-construction
(matched-ppl brain-tuning doesn't move the representation → no manifold selection — E009/E019-gentle).** Every
implementation door is verified-closed; the decisive science is COMPLETE. F2 (E019) DONE → corroboration (S14,
panel+positive-control-survived, D032):** built a faithful Negi head (differentiable
Lanczos+FIR+NT-Xent full-FT, Lanczos verified) on LeBel UTS01/02/03; NO positive encoding gain at any lr (gentle
gain_r −0.0006±0.0027 n=9; sweep monotone-negative; 1e-4 catastrophic). NOT a clean external clincher (the raw-mean-r
ruler is quality-insensitive — enc_r 0.5B≈3B; gentle regime didn't move the LM; decoder≠Negi's BERT). **E019 =
corroboration of the E008/E011/E017 lever-failure spine, not the clincher; the stale "NON-NEGOTIABLE" framing is
RETIRED — the spine rests on the POWERED nulls.** No rung flip; no Fork-A. (Below, the old F2 pointer kept for the table.)

**(superseded) F2 = E019 external reproduce-and-control** (paper-critical,
ceiling-independent). **F1-close (E020) = DONE → bounded-not-closed (S14, panel-survived; D030):** NO Fork-A (the
apparent A_resid=+0.090 was confirmed leaked-stimulus+autocorrelation, controlled away → gapped+partialled gap
−0.018≈0); the empirical n=6 E[Y|S] reference is too noisy (ref-rel 0.33, ε-NC 0.17 = the KILL regime) — the SECOND
ceiling instrument to wall at n=6 (after TRIBE). E020 demoted to convergent corroboration; the spine rests on the
POWERED per-individual nulls E008/E011/E017. **No rung flip; Q3/F1 stays ❌.** Manuscript framing of the bounded
ceiling = analysis-lane / Erfan call (flagged).

| Seq | Experiment | Question / decision rule | Status |
|---|---|---|---|
| **F1 P1 ✅ (done)** | **E016 TRIBE Phase 1 — fidelity** | TRIBE validated as a faithful in-pipeline fMRI stand-in: beats a strong nuisance floor in higher-order language Δ=+0.113 [+0.045,+0.181], 6/6 (tool-gate, no rung flip). Prereqs solved: voxel mapping → denizenslab (D027), TRIBE long-audio bug (L037). | **PASS (S13)** |
| **F1-close — E020 ✅ (bounded)** | **empirical-E[Y|S] ceiling (TRIBE-free)** | Ran story_11 n=6. **NO Fork-A** (A_resid=+0.090 = confirmed leaked-stimulus+autocorr; gapped+eng1000-partialled trained−untrained gap −0.018≈0). **Ceiling bounded-not-closed** — n=6 E[Y|S] reference too noisy (ref-rel 0.33, ε-NC 0.17 = KILL regime); 2nd instrument walled at n=6 (after TRIBE). Demoted to convergent corroboration of E008/E011/E017. Oracle+socratic+first-principles+counter-argument+premortem all run; D030/L040. No rung flip. | **DONE — bounded (S14)** |
| **TRIBE Phase 3 (optional)** | **E016 §5 Phase 3 — synthetic-target KD** | TRIBE's only irreplaceable use: dense brain targets for the real KD corpus (no fMRI; averaging impossible), matched-ppl vs permuted. Null at scale = strongest Fork-B (removes scarcity excuse). Optional booster, slot after F2. | designed (E016 §5) |
| **F2 — E019 ✅ (corroboration)** | **E019 external reproduce-and-control** | Built a faithful Negi head (differentiable Lanczos+FIR+NT-Xent full-FT, Lanczos verified vs source) on LeBel UTS01/02/03. **No positive encoding gain at any lr** (gentle gain_r −0.0006±0.0027 n=9, uR² −0.0001±0.001; sweep 2e-5/3e-5/5e-5 monotone-negative; 1e-4 catastrophic ppl→11.5k). **NOT a clean external clincher** (counter-argument + premortem + eval-positive-control): the raw-mean-r ruler is quality-insensitive (enc_r 0.5B+0.150≈3B+0.143), the gentle regime didn't move the LM (Δppl≈0), decoder≠Negi's BERT. **= corroboration of the E008/E011/E017 lever-failure spine** (L036), not the clincher; "NON-NEGOTIABLE" framing RETIRED. D031/D032, L041/L042. No rung flip; no Fork-A. | **DONE — corroboration (S14)** |
| **F3** | **E013/I3 denizenslab n=6 full-FT** (data downloaded) | the POWERED multi-subject induction test (closes the door at adequate power, not n=3 probe). Predeclared E013 protocol. Likely-null per 5 converging nulls; run per the 100% rule. | data ready |
| **F4** | **E015 Q2 architecture-residual extension** | add ≥3 modern-family sizes (Llama/Mistral) + base-vs-instruct ablation at matched bpb → claim or bury the architecture-beyond-quality residual (now p=0.20, underpowered). | designed (E015) |
| **A** | **Manuscript corrections (analysis lane, Erfan)** | r≈−0.92→−0.78 (3-part argument, drop standalone in-band −0.48); state Y⊥θ\*|S as assumption; narrow matched-ppl framing pending F2. | flagged |

**TWO PARALLEL LANES (D020) toward the dual meta-goal (D022): finish the MSc thesis AND extract ≥1 top-venue
AI paper.** The closed-rung *verdicts* (the per-individual null etc.) stand — what reopened (Erfan, 2026-06-12)
is an **implementation roadmap** that pursues the remaining *untested doors* and a new capstone, run autonomously
while Erfan studies in the analysis lane.

- **🔬 IMPLEMENTATION lane (autonomous working sessions) — an ORDERED ROADMAP, do in sequence (`tasks.md`):**
  **I1 ✅ DONE (2026-06-13)** — E015 expanded to 22 models/6 families; cross-family law corrected to **r≈−0.78**
  (bits-per-byte; v2's −0.92 was inflated by per-token-ppl + best-layer + 3-family span); operative-band ≈−0.48;
  Q2 architecture-residual = underpowered hypothesis (Llama/Mistral +0.006–0.009, n=1–2/family); L016 tie-in.
  Full oracle+panel+Codex audit; L034/L035; no rung flip (analysis-support). →
  **I2 ✅ DONE (2026-06-13, E017)** — oracle reframed it: Negi's literal pipeline infeasible + the matched-ppl
  contribution already lives in **E009 (downstream null) + E015 (the law)**. Ran a full-FT feasibility gate →
  **NULL** (real−perm +0.0003, CI [−0.0002,+0.0008], p=0.27, n=9): full-FT fails like LoRA → **method-general
  induction-lever failure** (LeBel-encoding route KILLED; converges E013/E011/E013b/E008). L036. Not Fork-A. →
  **I3 (BLOCKED)** full-FT multi-subject voxelwise (denizenslab n=6, git-annex not installed; E017's full-FT
  null lowers its prior) → **I4 CAPSTONE (NOW)** E016 TRIBE-v2 synthetic brain targets (D021; sidesteps I3's data
  blocker). **P0 GATE PASSED + VERIFIED end-to-end (S12):** TRIBE runs text→synthetic-BOLD (`preds (11,20484)`)
  via `config_update` unsloth-Llama override + ffmpeg. **Next: Phase 1 fidelity → Phase 2 ceiling (cheapest
  decisive).** **A TRIBE null = strongest publishable Fork-B; a TRIBE positive reopens Fork-A → STOP for Erfan.** After every step: panel (D017) + Codex (D019); record;
  **no rung flips without Erfan.**
- **📖 ANALYSIS lane (Erfan) — ACTIVE, now the finding-report set (D036):** R05 is retired; the analysis lane writes
  the **finding-reports** (`reports/R06`–`R14`), each a single Q-tagged claim mapping 1:1 to a manuscript Results
  section, in the reading order of `reports/README.md`. **R06 ✅ (Q0/A2) done; next = R07 (Q1).** The parked Q3 draft
  (`reports/_pending-Q3_*.md`) reclaims **R09** at read-position 4. Working sessions must NOT edit the analysis-lane
  docs (the finding-reports, manuscript, E005–E014 records).

**The manuscript (v0.9) is content-complete + panel-converged + artifact-complete** (`docs/manuscript/00_paper-draft-v0.md`): references verified, cross-refs resolve, gate = READY (thesis/workshop). Headline = the well-powered per-individual NULL + the averaging-confound measurement-validity result; the dose-response (E010/E010b) is hedged, not load-bearing.

**Analysis-session backlog (write the finding-report set, in reading order — `reports/README.md`):**
1. **The finding-reports (D036)** — each Q-tagged, current-truth-only, 1:1 with a manuscript Results section, written through the `scientific-writing` skill. Deep reading order, concepts, and self-checks per report live in `docs/analysis-roadmap.md`; source evidence in `docs/experiments/ENNN_*.md` + `learnings.md`.
   - **R06** (Q0/A2 — signal real beyond confounds) ✅ **written**.
   - **R07** (Q1 — plain KD does not preserve alignment) ⬜ **NEXT**.
   - **R08** (Q2 — the lever is real but weak and ppl-confounded) ⬜.
   - **R09** (Q3 — no per-individual gain; the averaging confound) — the parked draft `reports/_pending-Q3_*.md` reclaims this number.
   - **R10** (Q3 — null is method-general) · **R11** (Q3 — the quality law) · **R12** (Q3 — the ceiling, scoped; keystone) · **R13** (Q3 — external reproduction corroborates) · **R14** (Q4/A3 — no practical payoff) ⬜.
2. **Figures:** confirm the 4 figures (`scripts/figures/make_figures.py`) render the recorded numbers — averaging-collapse (Fig 2), powered A2 (Fig 3), A3 nulls (Fig 4), dose-response-with-caveat (Fig 1).
3. **Extended manuscript:** consolidate the finding-reports into the extended manuscript at a checkpoint Erfan calls (never auto-updated, D035); seed from v0.9 (`manuscript/00_paper-draft-v0.md`). The 5 reference [VERIFY] flags are cleared (lit-scout, 2026-06-12).

**Queued next MAJOR build (item 2, a fresh WORKING session — Erfan-approved as a possible next step):** the one untested door — **full fine-tuning (not a LoRA distillation readout) on multi-subject naturalistic voxelwise targets** (denizenslab n=6; `data/paper-repos/speech-llm-brain`). Scoped in `docs/experiments/E013_*.md`. The distillation-readout lever's failure (E013) is n-independent, so the ~5-deep-subject power (L024) applies only to this full-FT route, *conditional on it first inducing an above-base improvement*. Mechanism evidence suggests likely-null, but it is the only path that could move the per-individual verdict toward Fork-A. **A multi-day build — launch fresh, not at a session tail.**

**Deferred/moot:** Q5/F3 (fMRI-free proxy — moot, predicated on a null Q3 benefit). **Not built:** LeBel transfer (underpowered, S8); E007 TR-lever superseded by E013's voxelwise loop.

## Doc-consistency — CLEARED (S8)
- `feghhi-2024` → `hadidi-2024` canonical redirect added (same paper). ✅
- R03/R04 checked: **no stale "E004 = headline" references** exist (0 E004 mentions). ✅

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
