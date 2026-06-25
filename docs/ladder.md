# Ladder — the canonical status board (where we are, what's next)

**This is the single source of truth for project state.** Read it first, every session. It is maintained at every session close, *after Erfan confirms the verdict*. The prose narrative of *why* the ladder is shaped this way lives in `reports/R03_brain-as-training-signal.md` §5 and `reports/R04_gap-analysis.md` §8; this file is the live status of it. `upspeed.md` is the last-session prose; `tasks.md` is the granular backlog. When they disagree, **this file wins** and the others get fixed.

> **New to the codes?** → **[`map.md`](map.md)** is the visual map (legend + the whole journey as a tree). Quick legend: **Q**n = ladder rung / research question (Q0→Q5, in climb order); **E**nnn = experiment (the evidence); **A**1–A3 = the three assumptions; **D**nnn = decision; **L**nnn = learning. Rungs were renamed **L→Q** on 2026-06-15 (D036, execution-order numbering); pre-2026-06-15 timeline logs still use the old L labels — see `map.md` for the L↔Q table.

**Last updated:** 2026-06-25 (S40 — /meta: **cross-stance handoff X1–X4 BUILT (D050); `/write` suite 119 → 135.**
Implemented the S39 BUILD-READY design as four atomic chunks under the three-net loop: X1 `evidence_status: suspect`
(4 sites) · X2 `verdicts.py` handoff store + the sticky `handoffs-open` blocker (M1, hash-independent) + `ship`/
`accept-residual` refusal · X3 SKILL Stage-5.5 triage (3 outcomes, M3 backstop, two-gate rebind) · X4 folded the 16
`SC-XSTANCE-*` into the suite + a P3 test-plan. The S39 cutover-blocking gap is closed. **NO experiment, NO science
number, NO rung change — Q0–Q5 stand.** NEXT = **P3 cutover** (Erfan drives, IRREVERSIBLE; first stand up the
RUB-grading harness). — prior: S39 — /meta: /write dry-run + cross-stance handoff designed to BUILD-READY (D050);
NO rung change. — prior: S38 — /meta: **/write rebuild — PHASE 2 COMPLETE.** Built **P2-D** (6 chunks: `verdicts.py` convergence machine, parallel stage-5 fan-out, the **live** `stop_sw_converge` Stop-hook [opus oracle caught + I fixed a repo-wide-outage catastrophe — the session guard failed toward *enforce* on a falsy id], the `AskUserQuestion` gate, SC-XS-3 caption, fluidity/deviation-log) + ran **P2-E** authoring/quality review vs `writing-great-skills` + official CC sub-agent/hook docs → SKILL de-sediment (263→206), agent fixes, **`effort` frontmatter adopted fleet-wide** (D049). 11 commits. **NO experiment, NO science number, NO rung change — Q0–Q5 stand.** NEXT = **P3 cutover** (next session, Erfan drives; IRREVERSIBLE). — prior: S37 — /meta: built **P2-B + P2-C** of the `/write` rebuild (F1/F2/F11; F7/F13/F18/F17/F8b/F19) under the three-net loop; NO rung change, Q0–Q5 stand. — prior: S36 — /meta: **BUILT the `/write` redesign (D048)** — Phase-1 walking skeleton (C1–C8) **green end-to-end on the abstract** (catches the Claudio anchor) + Phase-2 **P2-A** (Argument concern: F4 warrant-validity + F5 scope), in the new self-contained skill `.claude/skills/sci-write-v2/`; the live `scientific-writing` skill is untouched (cutover is P3). Per-chunk discipline: log-mine → opus oracle (all FIX-THEN-PASS) → fresh-`claude -p` verify → atomic commit (9 commits). NEXT = P2-B. **NO experiment, NO science number, NO rung change — Q0–Q5 stand exactly as S35.** — prior: S35 — /meta: **redesigned the `/write` pipeline end-to-end to BUILD-READY** — a 4-concern system (Trust/Argument/Structure/Voice) + gated-loop spine → 21-functionality matrix → 119-scenario TDD suite → CC-primitive mapping → coverage check, each step independently opus-reviewed; artifacts in `docs/references/write-redesign-*` (master: `write-redesign-design.html` v1.1); D048, L058. **NO experiment, NO science number, NO rung change (Q0–Q5 stand).** — prior: S34 — /meta: hook-stack audit + graphify→context-mode swap in `CLAUDE.md`; NO rung change. — prior: S33 — /write: **started the extended-manuscript deep clean (paragraph-by-paragraph with Erfan) — finalized the ABSTRACT (conference register, single paragraph, no numbers/CIs, no em-dashes, results deferred to a \gap) + fixed a real hole in the em-dash guardrail (L057: ai_tell_lint missed LaTeX `---`; now budget 0). NO experiment, NO science number, NO rung change (Q0–Q5 stand).** — prior: S32 — /meta (committed `bf78142` but its ladder/timeline update was deferred to S33): **built the register convergence gate (D047) — a Stop hook keyed to content hash that blocks finishing a manuscript/report edit without a fresh clean register verdict; recorded D047 + L055 (why v0.2 half-failed). NO experiment, NO rung change.** — prior: S31 — /write: **extended manuscript v0.2 (checkpoint 2)** — folded **R07 (Q1)** into the manuscript + repaired the v0.1 register (L054/D046); installed a working LaTeX toolchain (tectonic+biber, L056). **NO experiment, NO science number, NO rung change (Q0–Q5 stand).** — prior: S30 — /meta: built the **prose ship-gate (D046)** (register rules + linter tripwire + `prose-register-auditor` + always-on hook) + L054; NO experiment, NO rung change. — prior: S27 — /meta: the operating model was rebuilt — eight invokable stances replace the working/analysis split (D044, supersedes D011); see `operating-map.md`. **NO experiment ran, NO number produced, NO Q-rung changed (Q0–Q5 stand exactly as S25/S26).** — prior: S26 — tooling (Firecrawl, D043), no rung change. — prior: S25 — working/critique+gates. **NO experiment ran, NO Q-rung changed (Q0–Q5 stand).** Ran the four-lens panel + pre-compute gates on Q2/Q3/Q4. **Q2:** recompute (cached E004) shows the "lever exists" CI is the L015-condemned 15-cell bootstrap → at the honest fold unit it includes 0 (fold-4=64%) → **demoted 🟡→❌ "no demonstrated lever"** (Erfan-confirmed S25; *undemonstrated*, not proven-zero — n=5 underpowered to rule out a small lever). **Q3:** the "one untested door" (full-FT denizenslab n=6) **CLOSED / NOT BUILT — decisively because the dataset is too small** (n=6 can't power the per-individual population claim; full-FT already null in E017; gate 0-for-5) → hedge retired, Q3 verdict unchanged ❌ (E013 S25 verdict + L051). **Q4:** sample-efficiency/LUPI design E024 written → oracle HOLD (400-sentence substrate underpowered → re-substrate to higher-N gaze; on-roadmap per §8/idea-tree T1.3). **L051 = the unifying lesson: data scale, not the hypothesis, is the binding constraint on the remaining doors.** — prior: S24 — analysis→tooling/design. **NO experiment ran, NO Q-rung changed (Q0–Q5 stand).** Forward direction REOPENED (Erfan): **brain-as-privileged-information → sample-efficiency** (the charter's F2 returned-to; full trajectory `expansion-program.md` §8). Designed E023; built **/goalsmith** + the **agent-fleet redesign** (+5 agents, `/precheck`, routing-lint hook, the thinker/oracle panel aligned to goalsmith's resolve-or-root-cause Judge, CLAUDE.md self-activation map); added 06 row 6 (perplexity/KD = KL). — prior: S22–S23 — autonomous expansion program, working. Ran two new exploratory experiments toward a top-venue positive: **E021** (cognitive-signal / reading-time training) → **CLEAN NULL on cognition** (the RT edge over controls is signal *shape*, not content — a phase-randomized twin ties it; surprisal-orthogonality null) and **E022** (Moussa Path-A external demonstration) → **NON-REPRODUCTION** (brain-tuning's downstream gain doesn't reproduce on our reduced setup → external demo off the table). **NO Q-rung changed** — both are exploratory negatives off the Q-ladder, recorded in `expansion-program.md` + `experiments/E021,E022`; the main-track positive did not materialize. Also built conference-scout tooling + filed a fetch-once-corpus far-future task. — prior: 2026-06-17 (S21 — analysis. **Reviewed S20's E003 repair (resolves everything R07 needed) + made R07's one pending analysis-lane edit: "matched budget" → step count not matched (cold 2 epochs vs warm 1); NO number, verdict, or rung changed.** `2b0477b`. — prior: S20 — working, provenance-only. **Repaired E003's four record-provenance gaps + a 5th (cold 2 epochs vs warm 1) via recompute on the cached slice — references confirmed (74.0/104.9/169.0), dissociation re-derived to `outputs/E003_{perplexity,dissociation}.json`; NO alignment number, NO verdict, NO rung changed.** New scripts `recompute_e003_reference_ppl.py` + `reanalyze_e003_dissociation.py`; L047. R07 left byte-identical (its "matched budget" wording handed to the analysis lane). — prior: S19 — analysis (not formally wrapped). **Wrote R07 (Q1, from E003); NO science rung changed.** — prior: S18 — tooling/process. Hardened the `scientific-writing` skill from the R06 clarity audit (L046, D037); added a methodology non-negotiable (record-the-why of a design choice); built the swarm-wrap system (SessionStart hook + `wrap-auditor` + tier-scaled `/wrap`, D038). **NO experiment ran, NO science rung changed — ladder unchanged from S17.** — prior: S17 — analysis. **R06 precision sweep complete (thinking panel ×3, 8 fixes — semipartial/partial, untrained sign, tables, controls label, quality ordering, E006 CC_norm threshold); NO science rung changed.** — prior: S16 — analysis. **Restructured the write-up layer; NO science rung changed**, the ladder
is unchanged from S14. Renamed the ladder rungs **L→Q** in execution order and added `map.md` (legend + journey tree);
adopted the **finding-report convention** (D036 — one durable claim per file, flat append-only `R<NN>` IDs,
current-truth-only, Q-tagged, each mapping 1:1 to a manuscript Results section). **Retired R05** (frozen for history).
Wrote **R06** (Q0/A2 — the alignment signal is real beyond confounds), formalized as conditional-MI with a math-grounded
report convention; added a "presenting a measured quantity" + math-voice rule to the `scientific-writing` skill and the
**estimand-first lens** to the reasoning toolkit. **Resume point for the analysis lane = the finding-report set in
reading order (`reports/README.md`): R06 ✅ done → R07 ✅ done (S19; source E003 provenance-repaired S20) → next R08 (Q2, the lever is real but weak and ppl-confounded).**
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

**→ The experimental program is CLOSED, and the per-individual null is ROBUST across every axis we could probe.** A2 holds (powered); F1 and A3 are characterized nulls; the null survived four escape attempts run + panel-bounded this session — **LoRA capacity** (E011, heavy LoRA leaves it intact), **objective** (E013b, contrastive/InfoNCE ≈ MSE, both null), **substrate** (E013, the voxelwise distillation lever fails to take hold at any λ — a mechanism failure, not a power limit), and the **measurement side** (E014, averaging the *encoding* score is legitimate-SNR/estimand, not a second confound). Q5/F3 is moot. The manuscript (v0.9) is **complete as an artifact** (panel-converged, references verified, cross-refs resolve; gate = READY thesis/workshop). **We are now in the write-up phase.** The "one untested door" (a *different induction method* — full-FT on multi-subject naturalistic voxelwise) is **CLOSED as of S25 (2026-06-19), NOT BUILT — primarily because the dataset is too small** (denizenslab n=6 cannot power the per-individual population claim; the full-FT parameterization was already tested null in E017; the manipulation gate is 0-for-5). See E013 S25 verdict + L051. Details below.

> **Audit trail (S8, 2026-06-11, Erfan-confirmed):** the thinking-panel (counter-argument + premortem + first-principles, fable) caught — *before* compute — that E005's "CI excludes 0" was pseudo-replicated (15 cells over one 5-UID-averaged target) and that the planned LeBel transfer test was underpowered (`scripts/reanalyze_e005_e006.py`, L015). The pivot to a per-subject solidification (E008) then returned a well-powered null (L016), confirmed by a second panel. Rigor before compute caught an overclaim that would have been the thesis headline.

---

## The scientific ladder (kill-gated; climb only if the rung below holds)

| Rung | Question | Kill criterion | Status | Experiment / verdict |
|---|---|---|---|---|
| **Q0 · A2** | Is the LM↔brain alignment signal real *beyond confounds*, on real data? | trained unique R² ≈ 0, or ≈ untrained | ✅ **PASS (powered)** | **E002** (Tuckute 5-ROI) + **E006** (LeBel UTS03 voxelwise): trained−untrained gap **+0.021 (gpt2) / +0.028 (Qwen)** on ~11.4k NC-reliable voxels, 95–99% positive, after the full phone-tier+eng1000 nuisance, story-CV. Clears the Hadidi/Feghhi 2026 bar. |
| **Q1** | Does plain perplexity-only KD *preserve or destroy* a teacher's alignment? | student keeps ≈ teacher alignment → F1 is a non-problem | ✅ **PARTIAL** | **E003** — *not* preserve-by-default (monotone gradient teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37; cold-KD Δ=0.018, p<0.001 below teacher). BUT KD-specific shedding unproven: alignment co-varies with LM quality (ρ=−0.88 on log-ppl), dissociation only p≈0.1, cold arm under-trained. Headroom, not confirmation (L011). |
| **Q2** | Is `$\mathcal{L}_{\text{brain}}$` a usable *lever* — does optimizing it *raise* held-out alignment? | optimizing the loss does not move held-out unique R² | ❌ **NO DEMONSTRATED LEVER** (recompute, S25; *undemonstrated*, NOT proven-zero) | **E004** — the headline "brain-specific lever" (Qwen mse − permuted twin = +0.0032 [+0.0006,+0.0058], "excludes 0") was the **L015-pseudo-replicated 15-cell bootstrap** (3 seeds × 5 folds counted as 15 independent draws). At the honest inference unit (**n=5 folds**) the t-CI = **[−0.0023, +0.0086] — includes 0**; fold-4 carries **64%** (leave-fold-4-out → +0.0014); `beats_permuted_null = False`. So no valid-unit evidence the loss moves held-out alignment — the same pseudo-replication the project corrected for E005 (L015), never applied here until S25. **Caveat (in-cell, deliberate): n=5 folds is underpowered to rule out a small (~+0.003) lever — this is "undemonstrated," NOT "proven zero."** Consistent with the robust Q3 null. (Brain loss built, D010 co-trained MSE; co-varies w/ perplexity L011/L012.) Erfan-confirmed S25. |
| **Q3 · F1** | Alignment-guided KD vs perplexity-only KD **at matched perplexity** → per-individual brain-specific gain? | brain term buys ~0 alignment at matched perplexity (paired, powered) | ❌ **NULL per-subject — ROBUST across capacity/objective/substrate** (averaged-target-only artifact) | **E008** (n=9, MDE≈+0.0006): mean +0.00010, t-CI **[−0.0004,+0.0006]**, fold-clustered incl 0, the 4 E005-averaged subjects individually null. Sensitivity sim: power 1.0 at δ=+0.003 → a TRUE null. **Robust to every escape:** **E011** (heavy LoRA r64/6ep) — null holds, +0.0004 (capacity didn't move the rep; λ that does wrecks ppl, L019); **E013b** (contrastive/InfoNCE objective, n=9) — null holds, −0.0002 at matched ppl (L025); **E013** (voxelwise same-substrate, λ-sweep UTS01/02/03) — the distillation lever never improves held-out alignment over base and never beats its permuted twin, a single-subject *mechanism* failure so n≥5 is moot (L026/L027). E005's +0.0081 was a group-averaged / shared-stimulus-response artifact, NOT per-person alignment. → Fork B. **~~One untested door~~ CLOSED (S25): the full-FT-on-multi-subject-naturalistic-voxelwise door is NOT BUILT — decisively because the dataset is too small (denizenslab n=6 can't power the per-individual population claim; full-FT already null in E017; gate 0-for-5). The hedge is retired; verdict unchanged. E013 S25 verdict + L051.** |
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

> **S40 DONE → S41 NEXT (2026-06-25, stance: `/meta` build → next is P3 cutover, Erfan drives).** S40 BUILT the
> cross-stance handoff **X1–X4 (D050)** — the four chunks designed to BUILD-READY at S39 — each under the three-net
> loop (selftest → opus `oracle-reviewer` → fresh `claude -p` → atomic commit): **X1** `e1702a5` `evidence_status:
> suspect` (4 sites) · **X2** `fd07799` `verdicts.py` `handoffs.json` store + the sticky `handoffs-open` blocker
> (M1: keyed independently of the prose hash, so a reword can't clear a substrate defect) + `ship`/`accept-residual`
> refusal · **X3** `077a57b` SKILL Stage-5.5 triage · **X4** `d12c725` folded the 16 `SC-XSTANCE-*` into the suite
> (**119 → 135**) + a P3 test-plan. Oracles: X1 PASS, X2/X3/X4 FIX-THEN-PASS (findings folded; the X3 fresh net
> caught a routing ambiguity the oracle missed). **NO experiment, NO rung change — Q0–Q5 stand.** **NEXT = P3
> cutover (IRREVERSIBLE, Erfan drives): first stand up the RUB-grading harness** (~51 RUB scenarios incl. the 10 RUB
> `SC-XSTANCE-*`; none exists) + a sign-off mechanic; then run the full 135-suite → retire the old
> `scientific-writing` flow → repoint `CLAUDE.md` + `docs/03-methodology.md` → wire DET as always-on hooks → record
> D048-complete. Build state: `write-redesign-build-plan.md` (X1–X4 ✅). Live science thread unchanged: Q4 E024;
> analysis lane next = R08 (Q2). **Parked `/interpret` item:** the E006 voxelwise CI (a voxel-bootstrap unit; lead,
> not adjudicated) — now surfaceable via the handoff.
>
> **S39 NEXT (2026-06-24, stance: `/meta` → build X1–X4, then P3).** A `/meta` session that (1) folded the
> build into the design canvas (Step 3, v2.0); (2) ran a `/write` dry-run of `sci-write-v2` on R06/§4.1 that
> validated the pipeline **and** surfaced that the **E006 voxelwise CI is a pseudo-replicated voxel bootstrap**
> (a **parked `/interpret` item** — a lead to verify, NOT adjudicated here); (3) designed the **cross-stance
> handoff** to BUILD-READY (**D050**, `docs/references/write-redesign-xstance.md`; 4 opus reviews). **NEXT =
> build the four chunks X1–X4** (three-net loop): X1 `evidence_status: suspect` (4 sites) · X2 `verdicts.py`
> handoff store + `handoffs-open` clause + ship-guard · X3 SKILL stage-5.5 triage · X4 wire SC-XSTANCE-01 +
> fold 16 SC-XSTANCE scenarios (119→135). **X1–X4 must land BEFORE P3 cutover** (don't freeze the known gap).
> Then P3 (IRREVERSIBLE, Erfan drives — first define the RUB-grading harness). Build state:
> `write-redesign-build-plan.md`. **NO experiment, NO rung change; Q0–Q5 stand.** Live science thread
> unchanged: Q4 E024; analysis lane next = R08 (Q2).
>
> **S38 NEXT (2026-06-23, stance: `/meta` → P3 cutover, Erfan drives).** **`/write` rebuild Phase 2 is COMPLETE
> — next is P3 cutover.** S38 finished **P2-D** (D-1 `verdicts.py` convergence machine · D-2 parallel stage-5
> fan-out + verdict recording · D-3 the **live** `stop_sw_converge` Stop-hook, pipeline+session-scoped,
> loop-guarded · D-4 `AskUserQuestion` gate · D-5 SC-XS-3 caption≤figure folded into F5 · D-6 fluidity/
> deviation-log) **+ P2-E** (authoring review vs `writing-great-skills` + official CC docs → SKILL de-sediment
> 263→206, agent fixes, **effort frontmatter fleet-wide D049**, settings braces). 11 atomic commits.
> **Build state + per-chunk decisions = `docs/references/write-redesign-build-plan.md` (Status + build log +
> the 4-session provenance table).** **NEXT = P3 cutover (IRREVERSIBLE, Erfan drives):** run the full
> **119-scenario suite** → if green, retire old `scientific-writing` flow, repoint CLAUDE.md/03-methodology,
> wire DET as always-on hooks, record D048-complete. **First define** a RUB-grading harness/threshold + sign-off
> mechanic for the ~41 RUB scenarios (none exists). Resume from `upspeed.md` +
> `docs/timeline/2026-06-23-1551_*`. **NO experiment, NO rung change; Q0–Q5 stand.** Live science thread
> unchanged: Q4 sample-efficiency E024; analysis lane next = R08 (Q2).
>
> **S37 NEXT (2026-06-23, stance: `/meta`).** **Continue the `/write` build at P2-D.** S37 BUILT **Phase-2 P2-B +
> P2-C** of the redesigned `/write` pipeline (D048, skill `.claude/skills/sci-write-v2/`; live `scientific-writing`
> untouched): F1 reader-model + F2 message&frame + F11 structure judge (P2-B); F7 figures + F13 premortem panel +
> F18 acknowledgment + F17 exemplar pin + F8b voice-realize + F19 consistency (P2-C). Each chunk: `--selftest` →
> opus oracle (all FIX-THEN-PASS) → fresh-`claude -p` verify → atomic commit + build-log entry (7 commits).
> **Build state + per-chunk decisions = `docs/references/write-redesign-build-plan.md` (Status + the append-only
> build log).** **NEXT = P2-D** (parallel stage-5 fan-out + structured `ready_to_ship` Stop-hook convergence +
> AskUserQuestion gate), then **P3 cutover** (full 119-suite green → retire old flow → repoint
> CLAUDE.md/03-methodology → record D048-complete — **IRREVERSIBLE, confirm with Erfan**). Resume from
> `upspeed.md` + `docs/timeline/2026-06-23-1129_*`. **NO experiment, NO rung change; Q0–Q5 stand.** Live science
> thread unchanged: Q4 sample-efficiency E024; analysis lane next = R08 (Q2).
>
> **S36 NEXT (2026-06-23, stance: `/meta`).** **Continue the `/write` build at P2-B.** S36 BUILT the redesigned
> `/write` pipeline (D048) as a new self-contained skill `.claude/skills/sci-write-v2/` (the live
> `scientific-writing` skill is untouched): **Phase-1 walking skeleton (C1–C8) green end-to-end on the abstract**
> (lattice+integrity, claim-binding F3, skeleton F6, drafter F8a, voice F12 — **catches the Claudio anchor**,
> claim-fidelity F9a/F9b, gate F16, orchestrator+`run_checks`) **+ Phase-2 P2-A (Argument concern: F4
> warrant-validity + F5 scope)**. Each chunk: log-mine → opus oracle (all FIX-THEN-PASS) → fresh-`claude -p`
> verify → atomic commit (9 build commits). **NEXT = P2-B** (F11 structure judge 2-sites + F1 reader-model +
> F2 message&frame), then **P2-C** (F18/F13/F7/F17/F8b/F19), **P2-D** (parallel stage-5 + structured
> `ready_to_ship` + Stop-hook convergence + AskUserQuestion gate), then **P3 cutover** (full 119-suite green →
> retire old flow → point CLAUDE.md/03-methodology here → record D048-complete — **IRREVERSIBLE, confirm with
> Erfan**). Resume from `upspeed.md` + `docs/timeline/2026-06-23-0215_*`. **NO experiment, NO rung change; Q0–Q5
> stand.** Live science thread unchanged: Q4 sample-efficiency E024.
>
> **S35 NEXT (2026-06-22, stance: `/meta`→`/work` for the build, OR `/work` for the science).** The `/write` redesign is **BUILD-READY** — master design `docs/references/write-redesign-design.html` (v1.1), build plan `docs/references/write-redesign-build-plan.md`, 119-scenario suite `write-redesign-scenarios.md`. **Two lanes, Erfan's call:** **(a) Build the new `/write`** — Phase 1 walking skeleton: lattice (F15) + claim-binding (F3, lift) + minimal skeleton (F6) + drafter-with-`\evd` (F8a) + two audits (F12 voice + F9a/b) + gate (F16), run on the **abstract**; acceptance = catches Claudio's class (SC-VOICE-01–04) + passes the near-misses + every claim `\evd`-bound. Then Phase 2 (full concerns) → Phase 3 cutover after the 119-suite passes. **(b) Science lane (unchanged):** Q4 sample-efficiency E024 (re-substrate → MDE positive-control → re-gate → build). The old `scientific-writing` flow stays live until the new pipeline passes the suite. **NO rung changed; Q0–Q5 stand.**
>
> **S33 NEXT (2026-06-22, stance: `/write`).** Continue the extended-manuscript deep clean, paragraph by paragraph with Erfan. Only the ABSTRACT is finalized. Next unit = **§1 Introduction ¶1** (split the long sentence-3; fix "rewards representations the brain would predict"; de-echo the abstract opening), then **§1 ¶2** (push the weak-prior/MAP formalism down to Methods §3.3, keep only the intuition + falsifiable prediction in the intro — Erfan leans this way), then §2 (dedup the "empty cell" stated 3×), §3, §4 (name the E006 CI unit in the `tab:vox` caption = bootstrap over the 11,442 reliable voxels). Per finalized paragraph: run `run_checks` + `prose-register-auditor` + taste-reader, then write to the file; the real ≥2-fresh-auditor clean register verdict runs at the END of the pass (the file currently carries an accepted-residual WIP sign-off, not a clean verdict). **NO rung changed; Q0–Q5 stand.**
>
> **S31 NEXT (2026-06-22).** Two open lanes, Erfan's call which. **(a) Analysis lane (`/write`):** the next finding-report is **R08 (Q2 — the lever is real but weak and ppl-confounded)**, then fold it at extended-manuscript **checkpoint 3** (R07/Q1 is now consolidated at checkpoint 2). Reading order in `reports/README.md`. **(b) Science lane (`/work`):** unchanged — Q4 sample-efficiency E024 (re-substrate to higher-N gaze → synthetic-PI MDE positive-control first → re-gate → build). **NO rung changed this session; Q0–Q5 stand.** Build the manuscript PDF with tectonic (L056; recipe in `upspeed.md` Key facts).
>
> **S27 NEXT (2026-06-19, stance: `/work` for the science, or `/teach` to test the new tutor).** The operating model was rebuilt this session (eight stances replace working/analysis, D044; how-to-operate = `operating-map.md`) — NO science changed. The live science next-step is UNCHANGED from S25 below: **Q4 sample-efficiency (E024)** — re-substrate to a higher-N gaze corpus → synthetic-PI MDE positive-control FIRST → fix control-5 + per-word loader → re-gate → build. Also: test `/teach` live on a real report (the honesty hook activates on the next `claude` start).
>
> **S25 NEXT (2026-06-19, working).** Two concrete steps. **(1) Q2 demoted 🟡→❌ "no demonstrated lever"** (Erfan-confirmed S25; undemonstrated, not proven-zero) — DONE. **(2) Q4 sample-efficiency (E024), fresh session:** re-substrate off the 400-sentence ZuCo-SR (oracle HOLD) → eye-tracking-first on a higher-N gaze corpus (pooled ZuCo NR / GECO / Provo — on-roadmap per §8 + idea-tree T1.3) → **synthetic-PI MDE positive-control first** → fix control-5 + per-word loader → re-gate → build. **Q3's full-FT door is CLOSED (dataset too small, n=6; D042/L051)** — do not rebuild. Background: ZuCo 1.0 clone still running (bare nohup, no completion notify). Details in `upspeed.md`.
>
> **S24 UPDATE — forward direction reopened (Erfan, 2026-06-18).** The closed experimental program (below, F1–F4, DONE/bounded) stands; the NEW forward thrust is **brain-as-privileged-information → sample-efficiency** (the charter's F2, returned-to with a theory + higher-SNR regimes + a control battery it never had). Full tiered trajectory = **`expansion-program.md` §8**: Tier 1 = finish every open experimental + theoretical door (TRUE-100%) — **next concrete step = E023a** (build the alignment-vs-ppl manifold, forward-passes only, no training) → `/precheck`-gate E023b; Tier 2 = the 5 method ideas; Tier 3 = P1 ZuCo-first PI learning-curve. Calibration: a strong methodology/negative paper is most likely; a top-venue positive is the tail. **No rung flipped this session; Q0–Q5 stand.** The analysis lane (R08–R14 + extended manuscript) remains Erfan's (D011). The working fleet self-activates per `CLAUDE.md`.

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
| **F3** | **E013/I3 denizenslab n=6 full-FT** | ~~the POWERED multi-subject induction test~~ → **KILLED (S25, 2026-06-19): NOT the powered test we hoped — n=6 is too small to power the per-individual population claim (σ unmeasured, possibly n≈8 needed); full-FT already null in E017; gate 0-for-5.** Decisively a DATASET-SIZE kill. E013 S25 verdict + L051. | ❌ **KILLED — dataset too small (n=6)** |
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
  section, in the reading order of `reports/README.md`. **R06 ✅ (Q0/A2) + R07 ✅ (Q1) done; next = R08 (Q2).** The parked Q3 draft
  (`reports/_pending-Q3_*.md`) reclaims **R09** at read-position 4. Working sessions must NOT edit the analysis-lane
  docs (the finding-reports, manuscript, E005–E014 records).

**The manuscript (v0.9) is content-complete + panel-converged + artifact-complete** (`docs/manuscript/00_paper-draft-v0.md`): references verified, cross-refs resolve, gate = READY (thesis/workshop). Headline = the well-powered per-individual NULL + the averaging-confound measurement-validity result; the dose-response (E010/E010b) is hedged, not load-bearing.

**Analysis-session backlog (write the finding-report set, in reading order — `reports/README.md`):**
1. **The finding-reports (D036)** — each Q-tagged, current-truth-only, 1:1 with a manuscript Results section, written through the `scientific-writing` skill. Deep reading order, concepts, and self-checks per report live in `docs/analysis-roadmap.md`; source evidence in `docs/experiments/ENNN_*.md` + `learnings.md`.
   - **R06** (Q0/A2 — signal real beyond confounds) ✅ **written**.
   - **R07** (Q1 — plain KD does not preserve alignment) ✅ **written (S19); consolidated into the extended manuscript at checkpoint 2 (S31, 2026-06-22).** Its source E003's record was provenance-repaired (S20); R07's "matched budget" wording was corrected (S21) to record that the cold arm ran 2 epochs vs the warm arms' 1 (step count not matched — deepens the under-training caveat; no number/verdict changed).
   - **R08** (Q2 — the lever is real but weak and ppl-confounded) ⬜ **NEXT**.
   - **R09** (Q3 — no per-individual gain; the averaging confound) — the parked draft `reports/_pending-Q3_*.md` reclaims this number.
   - **R10** (Q3 — null is method-general) · **R11** (Q3 — the quality law) · **R12** (Q3 — the ceiling, scoped; keystone) · **R13** (Q3 — external reproduction corroborates) · **R14** (Q4/A3 — no practical payoff) ⬜.
2. **Figures:** confirm the 4 figures (`scripts/figures/make_figures.py`) render the recorded numbers — averaging-collapse (Fig 2), powered A2 (Fig 3), A3 nulls (Fig 4), dose-response-with-caveat (Fig 1).
3. **Extended manuscript:** consolidate the finding-reports into the extended manuscript at a checkpoint Erfan calls (never auto-updated, D035); seed from v0.9 (`manuscript/00_paper-draft-v0.md`). The 5 reference [VERIFY] flags are cleared (lit-scout, 2026-06-12).

**~~Queued next MAJOR build~~ → CLOSED / NOT BUILT (S25, 2026-06-19, Erfan-directed):** the "one untested door" — **full fine-tuning on multi-subject naturalistic voxelwise targets** (denizenslab n=6) — was driven through the pre-compute gate (panel + anti-confound-designer + oracle-reviewer = KILL the build) and **abandoned, decisively because the dataset is too small.** denizenslab n=6 cannot power the per-individual population claim (between-subject σ unmeasured, oracle estimated n≈8 may be needed; the deep subjects we'd need don't exist on disk — that's a data-acquisition decision, not a re-run). Compounding: the full-FT parameterization was already tested null (E017), and the manipulation gate is 0-for-5. The Fork-1 cheap 1-subject gate was feasibility-confirmed (TextGrids/mapper/NC on disk) but **abandoned for the same size reason** — a 1-subject gate can't move a claim n=6 can't power. Scoped + reasoned in `docs/experiments/E013_*.md` (S25 verdict) + **L051.**

**Deferred/moot:** Q5/F3 (fMRI-free proxy — moot, predicated on a null Q3 benefit). **Not built:** LeBel transfer (underpowered, S8); E007 TR-lever superseded by E013's voxelwise loop.

## Doc-consistency — CLEARED (S8)
- `feghhi-2024` → `hadidi-2024` canonical redirect added (same paper). ✅
- R03/R04 checked: **no stale "E004 = headline" references** exist (0 E004 mentions). ✅

---

## How this file is maintained

- Every session close updates the rung table (status + verdict) and the "Next session" block — *after Erfan confirms the verdict*, never on the agent's unilateral read.
- A rung flips to ✅ only when an experiment in `experiments/` recorded a number with uncertainty and a named test. Partial verdicts stay 🟡/PARTIAL with the caveat written in.
- The `session-logger` agent and the CLAUDE.md close ritual both point here; `/orient` reads here first.
