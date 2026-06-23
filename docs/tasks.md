# Tasks — the path behind and ahead

Durable backlog. The session task tracker is ephemeral; this file is the source of truth across
sessions. Move items between sections; don't delete (strike completed ones with a date).

## Now — TWO PARALLEL LANES (D020, Erfan-agreed 2026-06-12)

Work runs in two independent queues that share the `docs/` evidence brain but do **not** block each
other. Each session picks ONE lane and pulls from it. **The binding rule (D011):** analysis may only
report numbers a working session recorded — so working sessions *add* evidence/rungs; they must
**not edit the docs the analysis lane is reading** (the finding-reports `reports/R06`–`R14`, the manuscript, the
E005–E014 experiment records). Rungs flip only on Erfan's confirmation.

> **Context:** Erfan is away ~1–2 days from 2026-06-12; implementation runs autonomously in that window.
> **The meta-goal (D022):** finish the MSc thesis AND extract **≥1 top-venue AI paper** (ICML/ICLR/NeurIPS/
> AAAI-class) from this work. The implementation lane below is an **ordered roadmap** that clears the
> remaining experimental train *first, in sequence*, then ends with the TRIBE capstone — each step's
> results/docs/learnings/decisions/ladder updated along the way. TRIBE is the **last** task added at the end
> of the train, **not** the first. The analysis lane is frozen at its resume point, ready for Erfan.

### 🛠 S27 META follow-ups (tooling, not science — do opportunistically; D044)

- [ ] **Test `/teach` live** on a real report (Erfan) — the proof of the guided loop.
- [ ] **Sweep remaining "working/analysis" mentions → stances:** `CLAUDE.md` fleet/self-activation section, `goalsmith` ("working sessions only"), agent descriptions. D044 documents the mapping; this removes the residual drift.
- [ ] **Resolve `R06:96`** — a bare `+0.0280` with no cite (add `[E0nn]` or `\gap`); the new write-time hook will flag it on the next R06 edit.
- [x] **Ingest the `/teach` pedagogy `\gap` papers** (S28, 2026-06-20) — Erfan supplied the 4 unreachable PDFs; all read first-hand. Filled Moser 2011 + B&M 2001 `\gap`s; new notes for B&M 2006, Bodily 2018, Long & Aleven 2017. Corrected Long & Aleven N=302→**301** and "OLM-only-with-control"→Exp-2 interaction. No `\gap` left in the pedagogy set.
- [x] **Prose ship-gate (D046)** (S30, 2026-06-22) — register rules in `scientific-writing`, linter tripwire/meter, the `prose-register-auditor` agent, the always-on `prose_writecheck.py` hook; L054. (Session was unwrapped; logged retroactively at the S31 wrap.)
- [x] **Extended manuscript v0.2 / checkpoint 2** (S31, 2026-06-22) — folded **R07 (Q1)** + repaired the v0.1 register (L054/D046); installed a working LaTeX toolchain (tectonic 0.16.9 + biber 2.17, L056) and fixed a latent `references.bib` build bug; PDF built (15 pp). Verified: `run_checks` PASS, claim panel clean, `prose-register-auditor` ×2. No science number, no rung change.
- [ ] **Extended-manuscript deep clean — IN PROGRESS (S33, started 2026-06-22).** Paragraph-by-paragraph with Erfan. **Done:** abstract (conference register, single paragraph, no numbers/CIs, em-dash-free, results deferred to a `\gap`). **Remaining:** §1 Intro (¶1 teed up; ¶2 = push weak-prior/MAP formalism down to Methods §3.3), §2 related-work (dedup the "empty cell" stated 3×), §3 methods, §4 results (name the E006 voxel-bootstrap CI unit in `tab:vox`). Per-paragraph suite: `run_checks` + `prose-register-auditor` + taste-reader; real ≥2-auditor clean register verdict at pass END.
- [ ] **Build the `taste-reader` subagent** (Erfan, S33) — **NOW SUBSUMED by the /write rebuild (D048):** taste/readability is the Voice concern (F12 + the panel F13) in the new design; build it as part of Phase 2, not as a standalone agent. Run inline per paragraph until the pipeline exists.
- [ ] **Promote `kill-gated` to a hard ban** (Erfan, S33) — it is only soft-caught today (`ai_tell_lint` METAPHOR_RE, exit-neutral); Erfan wants it gone from all prose. Move it to a hard finding (or its own banned-token list).
- [x] **Em-dash guardrail fix** (S33, 2026-06-22) — `ai_tell_lint` now catches LaTeX `---` (was unicode-`—`-only) and budget is 0; `writing-style.md` updated. L057.
- [ ] **(low priority, parked S28) Global "subagent must set `model`" hook**
<!-- placeholder anchor for the /write rebuild block below -->

### ✍️ /write PIPELINE REBUILD — BUILDING (D048; new skill `.claude/skills/sci-write-v2/`; design in `docs/references/write-redesign-*`)
Built as a new self-contained skill; the old `scientific-writing` flow stays live until Phase 3 cutover. Per-chunk discipline: log-mine (S35 log + docs) → build → **opus oracle review** → **fresh `claude -p` verify** → atomic commit. Each chunk has an embedded `--selftest`; `run_checks.py --selftest` is the integration smoke.
- [x] **Phase 1 — walking skeleton (C1–C8). DONE 2026-06-23 (S36), green e2e on the abstract.** lattice+`lattice_integrity` (C1) · claim-binding F3 + `evidence-register.json` (C2) · skeleton F6 (C3) · drafter F8a `sw-drafter`+`draft_check` (C4) · voice F12 `ai_tell_lint`+`sw-voice-auditor` — **catches the Claudio anchor** (C5) · claim-fidelity F9a/F9b+`sw-claim-fidelity-judge` (C6) · gate F16 `gate_state` (C7) · orchestrator `SKILL.md`+`run_checks` (C8). Acceptance met. Key fix: the gate binds to **prose-existence**, not the self-reported `meta.stage` (L059).
- [x] **P2-A — Argument concern. DONE 2026-06-23 (S36).** F4 `warrant_schema`+`sw-argument-judge` + F5 `scope_lint`+`sw-scope-judge` (opus xhigh, 2 sites each). Dual-use scope-words demoted to the judge (L060).
- [x] **P2-B — DONE 2026-06-23 (S37).** F1 reader-model (`sw-reader-model`) + F2 message&frame (`frame`/`contribution_type` lattice fields + stage-≥3 schema floor) + F11 structure judge (`sw-structure-judge`, sonnet xhigh, 2 sites). Fresh-verified SC-STR-01..12 + SC-RM-1/2. Oracle fixes: message-one-sentence is a gate concern not a DET (L060); F11 reads `reader_model` at stage 5 (else SC-STR-12 silently passes); width counted by claim-ID.
- [x] **P2-C — DONE 2026-06-23 (S37).** F7 figures (reuses the existing `central-claim-figure` DET — the `figures_planned` flag was abandoned in C3) + F13 premortem panel (reuses the D017 `premortem-analyst`/`counter-argument`; the orchestrator maps each objection → claim-id, SC-ARG-5) + F18 acknowledgment (`sw-acknowledgment`, opus, two-pass; future-work delegation ≠ acknowledgment, SC-ARG-12) + F17 exemplar pin (`references/F17-exemplars.md` + `register` field/DET) + F8b voice-realize (`sw-voice-realize`; **number-conservation DET** `draft_check --prev-prose` enforces it changes no number) + F19 consistency (`consistency_check.py`; abstract↔body RESULT-numbers + CI-in-abstract; **caption≤figure deferred** — no caption artifact). NB: F19 is **not** a lift of `check_number_consistency` (that does keyed public-vs-extended; F19 is within-doc abstract-vs-body — new logic).
- [ ] **P2-D — NEXT (the last Phase-2 work; orchestration/hook plumbing).** Parallel stage-5 fan-out + structured `ready_to_ship` verdicts + D047 Stop-hook convergence + AskUserQuestion gate. (The stage-5 judges already emit `*-VERDICT: {ready_to_ship, findings}` lines.)
- [ ] **TOOLING FIX — `start.json` clobber (L062).** A fresh `claude -p` verifier child overwrites the parent's `.claude/state/wrap/start.json` despite `CLAUDE_WRAP_SNAPSHOT_SKIP=1` (commit `1a7f186`); bit S36 and S37. Either the env var isn't reaching the child's SessionStart hook subprocess, or the hook should be write-once-per-session. `/wrap` currently works around it by checking `session_id` and falling back to the first-commit diff. Lives in `~/.claude/` hooks, not this repo.
- [ ] **Phase 3 — cutover (IRREVERSIBLE; confirm with Erfan).** Run the FULL 119-scenario suite (`write-redesign-scenarios.md`) + opus-designed additions; when green, retire the old draft flow (via git), wire the DET checks as always-on hooks, update `CLAUDE.md` + `docs/03-methodology.md`, record D048-complete. **Known residual — STILL OPEN after P2-C:** an assertive sentence the drafter models as "framing" (not a claim) escapes the Trust floor — the Argument concern (F4/F5) is built, but the design's *prose→lattice claim-coverage check* (every load-bearing prose sentence is entered as a claim) was NOT built in P2-B/C; today only the human gate catches it (marked in SKILL.md). Close it in P2-D or P3.
- Effort (set, D048): HIGH all subagents; XHIGH for F4/F5/F11. — strict version: a global `PreToolUse` hook on `Task|Agent` that blocks any spawn with no explicit `model` (enforces the global "always set model, never inherit" rule; robust to a fleet agent whose definition forgot its `model:` default). Verify it doesn't break harness-internal spawns before enabling. Lives in `~/.claude/`, not this repo. Not urgent — the fleet agents self-route via frontmatter defaults today.

### 🔬 IMPLEMENTATION lane — the ORDERED ROADMAP (do in sequence; TRIBE is the capstone, LAST)

Work top-to-bottom. Each item: run → judge with the panel + Codex → record (experiment doc, learnings,
decisions, ladder/tasks) → only then advance. Numbers come from runs; **no rung flips without Erfan.**

- [x] **I1 · Expand E015 — cross-family alignment∝−ppl law (OPT/Llama/Mistral). DONE 2026-06-13.**
  22 models / 6 families, **bits-per-byte** x-axis (oracle F1 fix; per-token ppl is tokenizer-contaminated).
  Verdict: cross-family law **r=−0.783** (family-cluster CI [−0.911,−0.500]), LOFO-robust, scale-controlled
  partial −0.675 — but floor-steepened (operative capable-band r≈−0.48, CI incl. 0). v2's −0.92 was inflated
  (per-token-ppl + best-layer + 3-family span). **Q2 (arch beyond quality): underpowered hypothesis** (Llama/
  Mistral +0.006–0.009 residual, vocab-robust, DPI-permitted; n=1–2/family, p=0.20, no common support).
  **L016 tie-in:** law rides the averaged/shared-stimulus component (per-individual SNR-limited). Full
  oracle+panel(counter/premortem/first-principles)+Codex audit in E015 doc; learnings L034/L035. No rung flips.
  **→ Analysis-lane FLAG (Erfan): manuscript's "r≈−0.92" needs correction to ≈−0.78. Antonello-2023 digested.**
- [x] **I2 · matched-ppl control — RESOLVED 2026-06-13 (E017).** Oracle gate (HOLD) established that Negi's
  literal pipeline is infeasible (no bilingual fMRI) AND that the I2 contribution **already exists**: Negi's
  *stated* gap is the **downstream** matched-ppl control = **E009** (bounded null), and the cross-family quality
  law = **E015/I1**. Reframed E017 → a single-subject full-FT feasibility gate (de-risk I3). **Result: NULL** —
  full-FT (the last untested induction *method*) fails to induce a brain-specific gain at matched ppl
  (real−perm mean +0.0003, 95% CI [−0.0002,+0.0008], p=0.27, n=9; manip_ok mostly False), converging with
  E013/E011/E013b/E008 → **method-general lever failure; LeBel-encoding induction route KILLED.** Matched-ppl
  contribution banked in E009+E015. Learning L036. Not a Fork-A surprise. Sole untested induction variants left:
  n≥5 multi-subject (I3, data-blocked) + TRIBE-synthetic (I4). **No headline/spine decision forced** (E017 is a
  negative feasibility datum, not a new headline) — but the manuscript framing "matched-ppl is the missing
  control" is now empirically backed by E009+E015+E017 (Erfan to weigh for emphasis).
### 🔭 FORWARD PROGRAM — REORDERED S13 (D028). New sequence: **F1-close (E020) → F2 (E019) → F3 (I3) → F4 (E015 Q2)**; TRIBE Phase 3 = optional booster.
The research corpus continuing the path (full table + decision rules in `ladder.md` → "THE FORWARD PROGRAM").

> **⏭️ NEXT SESSION = ANALYSIS lane (Erfan).** The IMPLEMENTATION lane's decisive forward-program work is COMPLETE
> (S14): F1-close (E020) DONE → bounded-not-closed; F2 (E019) DONE → corroboration. F3 superseded (D033), F4 =
> analysis-lane, ceiling-closure KILLED on all substrates (D034). **No new compute is needed to write the paper** —
> the spine rests on the powered nulls (E008/E011/E017) + E015 + L016 + the bounded E020 ceiling + E019 corroboration.
> The next high-value work is the analysis-lane roadmap (`docs/analysis-roadmap.md`).

- [x] **F1-close · E020 — empirical-E[Y|S] ceiling. DONE 2026-06-14 (S14), panel-survived.** Ran story_11 (n=6,
  Qwen2.5-0.5B L12). Naive flag fired (A_resid=+0.090, ρ=0.51, apparent Fork-A) — **NOT escalated, diagnosed.** After
  fold-gaps + eng1000-partial the trained−untrained residual gap = **−0.018≈0** ⇒ confirmed ARTIFACT (leaked stimulus
  via too-noisy n=5 reference, ref-rel 0.33 + autocorrelation). The eng1000 nuisance-partial is partly vacuous
  (symmetric partial collapses A_shared too — L040). **Verdict: NO Fork-A; ceiling bounded-not-closed** (2nd
  instrument to wall at n=6 after TRIBE). Convergent corroboration; spine rests on E008/E011/E017. Oracle + socratic +
  first-principles + counter-argument + premortem all run. `outputs/E020_eys/`. D029/D030, L039/L040. No rung flip.
- [ ] **TRIBE Phase 3 (OPTIONAL Fork-B booster, slot after F2 if pursued)** — distill toward TRIBE-generated dense
  brain targets on the REAL KD corpus (where no fMRI exists; empirical averaging impossible — TRIBE's only
  irreplaceable use), matched-ppl vs permuted twin. Phase 1 validated TRIBE is faithful enough to be a target. A
  null at scale removes the scarcity/SNR excuse = strongest Fork-B. NOT a blocker. (E016 §5 Phase 3.)

The research corpus continuing the path (full table + decision rules in `ladder.md` → "THE FORWARD PROGRAM"):
- **F1 · E016 TRIBE Phase 1→2 — the ceiling.** Prereq **voxel-space mapping SOLVED** (substrate → denizenslab,
  D027; TRIBE long-audio timestamp bug fixed, L037).
  - [x] **P1 FIDELITY = PASS (S13, 2026-06-14).** TRIBE beats a strong nuisance floor (rate+articulatory+eng1000
    -PCA) in higher-order language **Δ=+0.113 [+0.045,+0.181], 6/6, p≈0.03** (denizenslab story_11, n=6 listening);
    correct spatial profile. Oracle-gated + counter-argument-hardened (rate-only floor was a strawman). **Tool-gate,
    NO rung flip.** `scripts/{fsaverage_mapping,tribe_predict_deniz,run_tribe_fidelity}.py`; both TRIBE preds cached.
  - [~] **P2 (ceiling) ATTEMPTED S13 = INCONCLUSIVE (methodological wall).** `run_tribe_ceiling.py` (capacity-fair
    estimand B + untrained floor, oracle-gated Step 8) ran; runner flagged "Fork-A" but it **FAILS the predeclared
    vacuity gate** (trained LM→TRIBE≈0.03 vs LM→real≈0.18) ⇒ **confirmed ARTIFACT** — TRIBE explains only ~7% of
    per-vertex real-BOLD variance, too weak to subtract; the gap is the A2 trained>untrained real-alignment, NOT
    non-stimulus signal. **NOT escalated as Fork-A** (controls worked). A2 reconfirmed on denizenslab. (E016 Step 9.)
  - [x] **P2 ceiling REFRAMED (S13, D028) — TRIBE stimulus-subtraction RETIRED for the ceiling.** The fix is not to
    grind a weak TRIBE harder; it is to use the ground-truth empirical E[Y|S] instead → **the ceiling moves to E020**
    (above, the F1-close NEXT step). TRIBE kept only for Phase 3 (optional booster). F1 closes via E020, then F2.
- [x] **F2 · E019 external reproduce-and-control. DONE 2026-06-14 (S14), panel+positive-control-survived.** Built a
  faithful Negi head (differentiable Lanczos+FIR+NT-Xent full-FT, Lanczos verified vs source) on **LeBel** (substrate
  moved off denizenslab, D031). **No positive encoding gain at any lr** (gentle gain_r −0.0006±0.0027 n=9; sweep
  2e-5/3e-5/5e-5 monotone-negative; 1e-4 catastrophic ppl→11.5k). **NOT a clean clincher** — the raw-mean-r ruler is
  quality-insensitive (eval positive-control: enc_r 0.5B+0.150≈3B+0.143), gentle regime didn't move the LM, decoder≠Negi's
  BERT. **= corroboration of the E008/E011/E017 lever-failure spine; "NON-NEGOTIABLE" framing RETIRED.** `outputs/E019_negi/`.
  D031/D032, L041/L042. No rung flip.
- **F3 · E013/I3 denizenslab n=6 — SUPERSEDED/moot (D033).** The powered full-FT induction null is already in hand
  (E017, n=9) + corroborated (E019); denizenslab n=6 is reliability-walled + blind-ruler. Run ONLY for literal
  100%-rule coverage; otherwise skip. (Not a science change — the induction null is powered + corroborated.)
- **F4 · E015 Q2 architecture-residual extension** — analysis-lane extension (≥3 modern-family sizes + base-vs-instruct
  at matched bpb); underpowered hypothesis (p=0.20). Not a decisive rung.
- **ceiling-closure — KILLED on ALL substrates (D034).** TRIBE weak (L038), denizenslab n=6 walled (L040), LeBel n=3
  worse + no cross-subject mapper. The E[Y|S] ceiling rests as bounded corroboration; closing it would need acquiring
  ≥3 more deep LeBel subjects with the 10-rep story (a data-acquisition decision, not a re-run).
- **A (analysis lane, Erfan):** the keystone scope correction (L041 — operational claim; Y⊥θ*|S as ASSUMPTION; the
  unmeasured DPI selection side-channel); manuscript reframe to the refocused headline; lit positioning (Jia-L-PACT,
  Raugel, Hadidi→Nature-Comms cite); manuscript r≈−0.92→−0.78; figures. See `docs/analysis-roadmap.md`.

- [~] **I3/F3 · Full-FT multi-subject naturalistic voxelwise — SUPERSEDED/moot (D033, S14).** The powered full-FT
  induction null is already in hand (E017, n=9 LeBel) + corroborated by E019 (faithful Negi head); denizenslab n=6 is
  reliability-walled (E020/TRIBE, ref-rel 0.33) + its raw-r ruler is quality-insensitive. Run ONLY for literal 100%-rule
  coverage. Original spec (predeclared E013 protocol: per-individual n≥5, permuted twin, matched-ppl intercept,
  spatially-blocked inference) retained below for reference if Erfan wants the coverage run. **Steps:** (a) ✅ DONE — data acquired: `data/denizenslab/`
  (35G, 6 subjects [01,02,03,05,07,08] × reading/listening × trn/val, GIN `/raw/` + apt git-annex; verified valid
  HDF5, 10 train + 1 val stories each, ~80–93k voxels); (b) adapt `run_lebel_tune.py` full-FT loop to denizenslab
  HDFs (+ matched-ppl readout + permuted twin + spatial blocking); (c) run n=6 + judge → record in E013.
- [ ] **I4 · CAPSTONE — E016 TRIBE-v2 synthetic brain targets (the NEW task at the end of the train).**
  Meta's brain foundation model (`facebook/tribev2`) generates fMRI for *any* text. Key insight: TRIBE
  estimates E[Y|S], which **UNDER THE ASSUMPTION Y⊥θ*|S** (NOT an established result — scope correction L041) would be
  the θ*-relevant brain signal → an upper bound on brain-guided LM training (a null = the strongest, *publishable*
  Fork-B; a positive reopens Fork-A). NB: the E[Y|S] ceiling is now instrument-limited on all substrates (D034) and
  TRIBE Phase 1 already validated the synthetic-target path; this capstone is optional, not on the critical path.
  **Note: I4 sidesteps I3's data-acquisition blocker** (TRIBE *generates* the fMRI), so if I3 walls on
  denizenslab, proceed to I4. Full kill-gated program in `docs/experiments/E016_*.md`. Phases:
  - [x] **P0 GATE PASSED (2026-06-13)** — TRIBE runs text→synthetic-BOLD end-to-end (`preds (11,20484)`).
    Fixes: Llama override via `config_update={"data.text_feature.model_name":"unsloth/Llama-3.2-3B"}` (meta-llama
    gated); `ffmpeg` installed for whisperx ASR. Repro `scripts/tribe_p0_verify.py`. Isolated `.venv-tribe`.
  - [ ] **F1 = P1 FIDELITY (spatial-specificity) → P2 CEILING (cheapest decisive; + no-text ablation) → P3 CLINCHER**
    — prereq: voxel-space mapping (LeBel-vol↔fsaverage5). Refined design in E016 "PHASE 1/2 DESIGN — REFINED".
- [ ] **(Opportunistic Fork-B rigor, slot anywhere)** λ-sweep / rate-distortion curve on the averaged target
  (`run_brain_lever.py --lambda-grid`) — the "how small" magnitude characterization, if A3 needs context.

### 📖 ANALYSIS lane (Erfan's queue — ACTIVE: write the finding-report set; working sessions DO NOT edit these docs)

R05 retired (D036); the analysis lane now writes the **finding-reports** (`reports/R06`–`R14`), one Q-tagged claim
per file, each 1:1 with a manuscript Results section, in the reading order of `reports/README.md`. Deep reading
order + concepts + self-checks per report: `docs/analysis-roadmap.md`. Each written through the `scientific-writing` skill.
- [x] 2026-06-16 — **R06** (Q0/A2 — the alignment signal is real beyond confounds) ✅ written.
- [x] 2026-06-17 — **R07** (Q1 — plain KD does not preserve alignment, from E003) ✅ written (full loop + panel review pass: counter-argument/premortem/first-principles, opus; DPI reframed to fixed-function-compression ceiling, rate-distortion demoted to analogy, objective-attribution over-reach removed).
- [ ] **R08** (Q2 — the lever is real but weak and ppl-confounded).
- [ ] **R09** (Q3 — no per-individual gain; the averaging confound) — the parked `reports/_pending-Q3_*.md` draft reclaims this number.
- [ ] **R10** (Q3 — null is method-general) · **R11** (Q3 — the quality law) · **R12** (Q3 — the ceiling, scoped; keystone) · **R13** (Q3 — external reproduction) · **R14** (Q4/A3 — no practical payoff).
- [ ] **Figures:** confirm `scripts/figures/make_figures.py` renders the recorded numbers
  (averaging-collapse / powered A2 / A3 nulls / dose-response-with-caveat).
- [~] **Extended manuscript (running log; checkpoints called by Erfan, never auto-updated, D035):**
  - [x] **Checkpoint 1** (2026-06-16) — opened; R06 (Q0/A2) + front matter (R01/R03/R04) folded in.
  - [x] **Checkpoint 2 / v0.2** (S31, 2026-06-22) — R07 (Q1) folded in + v0.1 register repair (L054/D046); PDF built (tectonic+biber, L056).
  - [ ] **Checkpoint 3** — fold R08 (Q2) once its finding-report is written; then R09–R14 as they land. (References verified + [VERIFY] flags cleared, lit-scout 2026-06-12.)

### Done this session (S26 — tooling; NO science, NO number, NO rung moved)
- [x] 2026-06-19 — **Firecrawl set up for the repo** (`71c0894`, `c868446`; D043). Cloud MCP only (Docker unusable → self-host impossible); project-scoped `.mcp.json` (remote transport, `${FIRECRAWL_API_KEY}` interpolated, no secret committed); `firecrawl-research-index` skill installed repo-local (`.claude/skills/`, drives `firecrawl_research_*`, complements lit-scout); `## Firecrawl` section in `CLAUDE.md`. The 5 build-* skills skipped; estack untouched (Erfan-directed). Partially resolves D041's deferred `.mcp.json` (does not shadow Exa).
- **OPEN LOOP:** Firecrawl MCP server is `⏸ Pending approval` — approve on next `claude` start before `firecrawl_*` tools fire. **NEXT science step is unchanged from S25: Q4 re-substrate** (see `upspeed.md`).

### Done this session (S24 — analysis→tooling/design; PI/sample-efficiency pivot + agent-fleet redesign; NO experiment ran, NO rung moved)
- [x] 2026-06-18 — **Forward direction reopened (Erfan):** brain-as-privileged-information → sample-efficiency (the charter's F2, returned-to with theory + higher-SNR regimes + the 5-control battery). Trajectory in `expansion-program.md` §8 (TRUE-100% Tier 1; the 5 method ideas; P1 ZuCo). Critique-loop-hardened (counter-argument + lit-scout + Codex). D040.
- [x] 2026-06-18 — **E023 designed** (`experiments/E023`): KD objective-vs-quality identification (δ_obj manifold-residual). Not run.
- [x] 2026-06-18 — **/goalsmith** (`.claude/commands/goalsmith.md`): /orient item → ≤4000-char single-line `/goal` condition (PRD-pointer + resolve-or-root-cause completion). Cold-tested.
- [x] 2026-06-18 — **Agent-fleet redesign** (`docs/references/agent-fleet-redesign.md`, D041): +5 agents (stat-aggregation-auditor, anti-confound-designer, dataset-verifier, dataset-scout, paper-repo-extractor); /precheck; confound-catalog; wrap-auditor scopes + mid-session; routing-lint hook; §4 thinker/oracle panel aligned to goalsmith; CLAUDE.md self-activation map.
- [x] 2026-06-18 — **06 row 6** (perplexity/KD = KL minimization; output-vs-representation gap) + R07 §design pointer.
- **NEXT working step:** expansion-program §8 Tier-1 → **E023a** (manifold, forward-passes only) → `/precheck`-gate E023b. **Deferred:** `.mcp.json` (no Exa transport config). **Untested:** the new fleet (first real exercise next run).

### Done this session (S22–S23 — autonomous expansion program, working; 2 exploratory negatives, no rung moved)
- [x] 2026-06-18 — **E021 (cognitive-signal / reading-time training) → CLEAN NULL on cognition.** n=10 + learnability-matched controls + a phase-randomized shape-matched twin: the RT edge over all controls is signal *shape* (autocorr+kurtosis), not content; surprisal-orthogonality null. Arc v2→v3→v4→v5. L048/L049. `experiments/E021`, `scripts/run_e021_v{3,4,5}.py`.
- [x] 2026-06-18 — **E022 (Moussa Path-A external demonstration) → NON-REPRODUCTION (STOP).** Oracle-gated reproduction pilot: brain−pretrained phoneme-F1 +0.52 [−0.36,+1.40], below the +2 gate → shrink-test vacuous, not built. External "main-track lift" off the table. `experiments/E022`, `scripts/e022_pilot.py`.
- [x] 2026-06-17 — **Expansion-program scaffolding:** `expansion-program.md` (two-path strategy + venue list), `idea-tree.md` (solution-altitude tree), `litsweep-relevance.md`; conference-scout tooling `scripts/litsweep/` (built+tested, NOT run at scale); 2 canonical notes (Deng'24, BabyLM). Strategy premortem re-sequenced the plan honestly.
- **Net:** the expansion program's experimental phase is CLOSED with negatives; no top-10 main-track positive. Honest deliverable = Path-A negative paper + thesis. **Open loop:** 2 external panels (E021 confirmatory) were running at close.

### Done this session (S18 — tooling/process, 2026-06-16; no science, no rung moved)
- [x] 2026-06-16 — **Audited R06's clarity misses with a 4-lens thinking panel** (counter-argument + first-principles-grounder + socratic-thinker + premortem-analyst, opus). Diagnosis: mostly skill DESIGN, not execution. L046, D037.
- [x] 2026-06-16 — **Hardened the `scientific-writing` skill** (commit `0647188`): amended the Clarity Test (necessity + sufficiency; invest = unpack not pack); added the reader-comprehension floor (define-on-first-use audience-graded, rationale-or-`\gap`, table-trigger, formula-vs-prose); made path selection a deliberate user interview with a hard "manuscript/supervisor-facing = full loop" boundary; review pass non-skippable for manuscript-bound work; report→extended consolidation guards; number-freshness obligation; neutralized the biasing worked example.
- [x] 2026-06-16 — **Methodology non-negotiable** added (`docs/03-methodology.md`, commit `3e15ecd`): record the why of a non-obvious design choice at choice-time (D037).
- [x] 2026-06-16 — **Built the swarm-wrap system** (commit `e19cc69`, D038): SessionStart hook (`wrap_session_snapshot.py`) records `{start_sha, transcript_path}` per worktree; `wrap-auditor` read-only agent (5 scopes); tier-scaled `/wrap` (trivial = inline, heavy = parallel auditors → single writer). First-run-tested on this session.
- [x] 2026-06-16 — **L046** appended to `learnings.md`; **D037/D038/D039** recorded.

### Done this session (S17 — analysis, 2026-06-16; no science, no rung moved)
- [x] 2026-06-16 — **R06 precision sweep (thinking panel ×3 opus in parallel).** Three parallel opus agents (counter-argument, socratic-thinker, first-principles-grounder) found 8 real issues; all fixed: tables for E002/E006 numbers; semipartial vs partial R² corrected; untrained sign mechanism rewritten (−0.017, strong nuisance absorbs shared-cause floor); "gpt2-medium in between" → "comparable"; "mid-layer-peaked" → "broad plateau"; temporal-leakage and voxel-selection-bias paragraphs rewritten with explicit mechanisms; language-network caveat added; "Two controls" → "Three controls"; quality ordering grounded in our data; duplicate gap formula removed.
- [x] 2026-06-16 — **CC_norm > 0.05 stale threshold in E006 design section** corrected to split-half reliability > 0.5, as-run. Section header updated.
- [x] 2026-06-16 — **Architecture sections added to E002 and E006** — Mermaid flowcharts + stage-by-stage walkthroughs; last-sub-token rationale, Lanczos, FIR delays, capacity-fair PCA, two-arm gap structure documented.
- [x] 2026-06-16 — **`docs/explainer_pipeline.html` created** — dark-mode HTML pipeline explainer with color-coded diagrams and E006 numbers.
- [x] 2026-06-16 — **L043** appended to `learnings.md` (semipartial vs partial R² distinction).

### Done this session (S16 — analysis, 2026-06-16; no science, no rung moved)
- [x] 2026-06-16 — **Renamed ladder rungs L→Q in execution order + added `map.md`** (legend + journey tree; L↔Q table). D036.
- [x] 2026-06-16 — **Adopted the finding-report convention (D036):** one durable claim per file, flat append-only `R<NN>` IDs, current-truth-only, Q-tagged, 1:1 with a manuscript Results section; index + reading order in `reports/README.md`. **Retired R05** (frozen for history).
- [x] 2026-06-16 — **Wrote R06** (Q0/A2 — the alignment signal is real beyond confounds), formalized as conditional-MI with a math-grounded report convention.
- [x] 2026-06-16 — **scientific-writing skill:** added a math-voice rule + a "presenting a measured quantity" rule.
- [x] 2026-06-16 — **reasoning toolkit:** added the **estimand-first lens** + a rule to grow the toolkit (`docs/references/reasoning-frame.md`).
- [x] 2026-06-16 — **Reconciled the stale state boards** (ladder/upspeed/tasks/analysis-roadmap) to the committed S16 work; wrote a reconstructed S16 timeline log. (S16 itself was not formally `/wrap`ped.)

### Done this session (S15 — analysis/infrastructure, 2026-06-15; no science, no rung moved)
- [x] 2026-06-15 — **R05 §8 scaffolding refreshed** (stale `r≈−0.92`→`−0.78`; §11–§16 placeholders now name E017/E019/E020 + L041). Narrative frontier unchanged: next is §9.
- [x] 2026-06-15 — **Designed + documented the three-layer deliverable model (D035)**: reports (md, continuous) → extended manuscript (LaTeX) → public manuscript (LaTeX, frozen `vN`). `03-methodology.md` "Deliverable layers".
- [x] 2026-06-15 — **Built the `scientific-writing` skill** (17 files: SKILL.md + 4 references + 6 verifier scripts + 6 LaTeX assets + pointer doc). Panel-hardened ×2; verifiers tested; full `latexmk`+`biber` build passes.
- [x] 2026-06-15 — **Cloned `academic-research-skills`** (read-only, gitignored, `data/reference-repos/`); swarm-mapped it; adopted patterns C1–C6, declined the heavy plugin machinery.
- [x] 2026-06-15 — **Fused D035** into `CLAUDE.md`, the doc map, and the manuscript/reports READMEs (removed the false "paper = report" / "no latest copy" lines).
- [x] 2026-06-16 — **Carry-forward (S15→S16): resumed the analysis lane** via the finding-report convention (R05 retired, R06 written).
- [x] 2026-06-16 — **Mirrored D035/D036 to gbrain** — D035 page (`brain-alignment-deliverable-system`) already current; D036 page (`brain-alignment-naming-convention`) updated with the finding-report convention + R06 + the estimand-first lens (`write_through: written`). The bare `projects/brain-alignment` hub stub still wants enrichment (future).

### Done this session (S9 — analysis, 2026-06-12)
- [x] 2026-06-12 — **Taught Q0 + Q2** of the thesis arc (Socratic, native `socratic-tutor`); Erfan mastered the frame/bet + measurement/lever/MDE/reroute.
- [x] 2026-06-12 — **`docs/07-concepts-primer.md`** created — DRY home for reusable primitives (voxel/ROI, encoding model, unique R², noise ceiling, perplexity, datasets, E/R/L/D-numbering); E002/R03/README point at it.
- [x] 2026-06-12 — **`docs/reports/R05`** created (LIVING first-principles narrative, Q0–Q2); **panel-reviewed** (counter-argument/first-principles/socratic/premortem) + revised (ceiling 0.353→0.49/~7%, ρ′ relabel, A3 novelty scope, DPI chain, §3 per-rung verdicts, theory hedges, pedagogical glosses).
- [x] 2026-06-12 — **Doc-shortfall audit swarm** (5 haiku) → fixed README missing-ladder-row, charter stale "Activating" status; filed the rest below.
- [x] 2026-06-12 — Quiz-style feedback saved to memory + gbrain (vary correct-answer position; prefer open-ended).

### Done this session (S10 — TOOLING/infrastructure, 2026-06-12; no science, no rung moved)
- [x] 2026-06-12 — **Codex wired as a second model:** `docs/references/codex-usage.md` + `CLAUDE.md` Codex section. Two jobs — (1) code-level critic that ADDS to the thinking panel (`/codex:adversarial-review` + a 1–4-persona background read-only panel); (2) rescue/second-implementation. Hard line: no numbers/verdicts from Codex.
- [x] 2026-06-12 — **Reasoning = xhigh** (`~/.codex/config.toml`); asymmetric "medium worker / xhigh critic" (reviews inherit xhigh; tasks pass `--effort medium`). VERIFIED live (`reasoning effort: xhigh`).
- [x] 2026-06-12 — **bwrap sandbox DISABLED** (container can't init namespaces; `/proc/sys` read-only; system bubblewrap didn't help). Fix = config (`approval_policy=never`, `sandbox_mode=danger-full-access`) + `codex.mjs` patch forcing `danger-full-access`. Plugin + config live outside the repo. L033; D019.
- [x] 2026-06-12 — **Live comparison:** Codex (xhigh) independently re-ran `reanalyze_e005_e006.py`, reproduced the S8 panel's core finding (t-CI incl 0, bootstrap-excl-0, `(fold4,seed0)` +0.0636 outlier) → independent corroboration of L015.

### Tooling carry-forward
- [ ] **Reapply the `codex.mjs` sandbox patch after any codex plugin update** (forces `danger-full-access` in `buildThreadParams`/`buildResumeParams`; in-file comment + `codex-usage.md` flag it). One-time, only when the plugin version bumps.

### Doc-audit follow-ups (S9 swarm) — DONE 2026-06-12
- [x] 2026-06-12 — **Experiment Status-line cleanup:** E003/E004/E006/E008/E009/E011/E012/E013 headers updated to COMPLETE/DEFERRED/PARTIAL with the recorded verdict.
- [x] 2026-06-12 — **E005 verdict lead:** added a top "read the ADDENDUM first" banner + a SUPERSEDED flag on §Interpretation + fixed the Status line; the honest per-individual-null verdict now leads.
- [x] 2026-06-12 — **Literature freshness:** R03 already self-corrects via inline ↳ Correction notes (haiku audit double-counted the original-claim text); added an R04-wins freshness pointer to **R01** (Pirlot/V1 not Federer/IT; Merlin&Toneva 2026).

### Done this session (S8 continuation, 2026-06-12)
- [x] 2026-06-12 — **E011** heavy LoRA: per-individual null robust to capacity (+0.0004, incl 0; L019).
- [x] 2026-06-12 — **E013b** contrastive/InfoNCE objective (n=9): null holds across objectives at matched ppl (−0.0002; L025).
- [x] 2026-06-12 — **E013** voxelwise same-substrate (UTS01/02/03 + λ-sweep): distillation lever doesn't take hold at any λ; v1 failed-manipulation retracted; mechanism failure (n≥5 moot); L026/L027.
- [x] 2026-06-12 — **E014** averaging on the encoding brain-score: NOT a confound-lift (per-subject positive → legitimate-SNR/estimand); fixed unseeded-PCA bug; verified before folding → paper unchanged; L028.
- [x] 2026-06-12 — **Manuscript v0.9 COMPLETE-AS-ARTIFACT:** References (verified vs primary sources, lit-scout); completeness-critic closed orphan citations + dangling §-pointers.
- [x] 2026-06-12 — **Ladder FLIPPED (Erfan-confirmed):** experimental program closed → analysis/write-up phase.
- [x] 2026-06-12 — **Mock peer-review of complete v0.9** (oracle+premortem+counter-argument, fable): PASS thesis / borderline-PASS workshop; fixed 5 abstract overclaims (the "every individual brain" category error chief); L029.
- [x] 2026-06-12 — **Power positive-control** (`sensitivity_e008.py`): real-residual bootstrap propagating within-subject noise → group test power 0.92@uniform-δ=+0.002, FPR 0.01; first-principles VALID; defends the load-bearing null. L029.
- [x] 2026-06-12 — **E015: cross-family alignment∝−ppl LAW** (r≈−0.92, n=8, gpt2/pythia/Qwen) — generalizes E003's within-gpt2 r=−0.88; matched-ppl control shown to bite cross-family; folded into §1+evidence-map. Broken-probe caught by counter-argument (L030).
- [x] 2026-06-12 — **E015 novelty grounded (lit-scout):** alignment∝quality is ESTABLISHED (Schrimpf 2021/Hong 2024/Antonello 2023/Gao 2024) — NOT a discovery; novel step is the normative matched-ppl control. §1 fixed to cite prior art. E015 best-layer robustness check done (r=−0.917, layer-invariant).

### Open questions / following tasks (for the analysis sessions — all need Erfan or online/build resources)
- [ ] **(Erfan's strategic call) The premortem's spine reframe:** move the paper's headline from the averaging confound → **matched-perplexity as the missing control in the brain-tuning literature** (the contribution that survives our own scoping; E015 now gives it cross-family bite). Premortem says this is the highest-leverage move; the averaging-confound headline has a weak external target. L029.
- [ ] **(Fresh working build / online) Demonstrate the matched-ppl control on ONE external published result** — show a Negi/Schwartz-style gain shrinks at matched ppl. The "main-track lift." Multi-day.
- [ ] **(Online) Expand E015** to more families (OPT/Llama/Mistral) to beat the n=8/3-family-cluster caveat; the law is currently a capability-range law within modern decoder transformers (Pasquiou 2022: non-monotone across RNN/transformer classes).
- [x] ~~**(Fresh working session) Full-FT multi-subject naturalistic voxelwise** (denizenslab n=6)~~ — **KILLED / NOT BUILT (S25, 2026-06-19, Erfan-directed).** Driven through the pre-compute gate (panel + anti-confound-designer + oracle-reviewer = KILL the build). **Decisive reason: dataset too small** — denizenslab n=6 cannot power the per-individual *population* claim (σ unmeasured, oracle est. n≈8 may be needed; the deep subjects we'd need don't exist on disk → a data-acquisition decision, not a re-run). Compounding: full-FT already tested null in E017; manipulation gate 0-for-5. The Fork-1 cheap 1-subject gate was feasibility-confirmed but abandoned for the same size reason. → E013 S25 verdict + L051. The "one untested door" hedge is retired (line 224 polish now moot — the manuscript can drop it).
- [x] 2026-06-12 — **(L031) Operating rule for Stop-hook re-fires** — Erfan-approved + ADDED to repo `CLAUDE.md` ("Working with Erfan": auto re-fires aren't fresh intent; most recent explicit message wins; on "wrap/stop", wrap).
- [ ] **(Analysis polish) Manuscript pre-submission:** trim "one untested door" repetition (premortem #5, reads as unfinished Fork-A); venue/length; optional §2 prose.

### Done earlier this session (S8, 2026-06-11)
- [x] 2026-06-11 — ~~LeBel voxelwise TRANSFER test~~ **DROPPED** — S8 panel showed it underpowered (paired-LeBel MDE needs ρ≥0.9 to see even +0.0081; `reanalyze_e005_e006.py`).
- [x] 2026-06-11 — **E008 per-participant solidification** ran → in-domain F1 is a **per-subject NULL** (well-powered); E005's +0.0081 = group-averaged-target artifact. Ladder Q3/F1 ❌, Fork-B reframe (D018, Erfan-confirmed). L016.
- [x] 2026-06-11 — **Doc-consistency:** feghhi-2024 → hadidi-2024 canonical redirect; verified R03/R04 have **no** stale "E004=headline" refs (0 mentions).
- [x] 2026-06-11 — Built the **thinking panel** (D017) + digested A3 prior art (Negi 2025, Guo 2024, Schwartz 2019) + Proietti 2025.
- [ ] **(Optional, Fork-B rigor) λ-sweep / multi-rate rate-distortion curve** on the averaged target — the "how small" characterization, if A3 needs magnitude context. `run_brain_lever.py --lambda-grid` supports it.

## Next (de-risk the thesis — ordered by leverage)

- [ ] **`paper-digest` remaining finalists** if needed for A3 related-work: Merlin & Toneva 2026 "When LMs Lose Their Mind" (arXiv 2603.23091), Bilgin/Wehbe 2026. (Negi/Schwartz/Guo/Proietti digested S8.)
- [ ] **Sharpen the contribution per the Fork-B reframe:** the thesis is now A2-powered-real + the well-powered per-subject null (in-domain F1 doesn't generalize to individuals) + the anti-confound methodology + A3 (practical payoff). Update R03/R04 §-framing to Fork-B + D018. Position vs Negi/Schwartz (the matched-ppl + permuted-brain control is our novelty).

## Later (once the pilot says go)

- [ ] **(FAR-FUTURE BUILD, Erfan-owned) The "fetch-once, query-forever" conference corpus.** Run the literature sweep ONCE, exhaustively: all top-10 AI/ML venues × 2020→now → normalized metadata + abstracts → dedup → a permanent queryable store (SQLite/parquet + a local embedding index) → wrap as a `conference-corpus` skill. Tooling already built + tested this session (`scripts/litsweep/`); full spec, venue list, coverage gaps, and the store/skill design are in **`docs/references/literature-sweep-system.md`**; relevance taxonomy in `docs/litsweep-relevance.md`. Deliberately deferred S22 (the targeted searches sufficed for the current analysis; this is a day+ engineering project, not on the thesis critical path).
- [ ] Lock the baseline matrix runs (perplexity-only KD, structure-aware KD, alignment-guided, hybrid).
- [ ] Build the anti-confound evaluation harness (contiguous splits, nuisance baselines).
- [ ] Promote H001 to a Design with a locked protocol; add competing hypotheses H002/H003.
- [ ] **(DEFERRED until feasibility holds)** Define the "edge" deployment scenario concretely
      (FLOPs/latency/params target). Not in scope until the fundamental question is answered.

## Infrastructure / housekeeping

### [x] DONE 2026-06-17 — E003 record-provenance repair (working session; provenance-only, no science changed)

**Resolved.** Multi-round gather + counter-critique panel (counter-argument/premortem/first-principles/socratic, opus) + plan-critique, then executed. Built `scripts/recompute_e003_reference_ppl.py` → `outputs/E003_perplexity.json` and `scripts/reanalyze_e003_dissociation.py` → `outputs/E003_dissociation.json`. **Decisive de-risk:** the four reference ppls (74/105/169) recompute on the cached slice to 74.0/104.9/169.0 — they *were* on-slice measurements, just never written to the JSON — so recompute confirms rather than replaces, and the r=−0.88 fit/residuals/44%-fold reproduce. R07 byte-identical (untouched); all E003.md/R07 alignment numbers byte-identical (verdict rows not in the diff). Two findings surfaced: (i) the dissociation P-values are **construction-sensitive** (fold×seed ≈0.09 reproduces the prose; fold-only ≈0.00) — archived honestly, qualitative "not clean-significant" holds; (ii) a **5th gap** — cold ran 2 epochs vs warm 1 ("matched budget" false on step count) — recorded in E003.md.

> **→ Analysis-lane FLAG (Erfan):** R07 phrases the screen as "matched budget"; given the cold=2/warm=1 epoch asymmetry, that wording wants a one-line analysis-lane review (not edited from this working session, per D011).

<details><summary>Original task spec (kept for the record)</summary>

**Mode: working session (it edits the science record and may re-run cheap forward passes). Provenance-only — it must NOT change any verdict, any alignment number, or flip a rung.** The R07 write-up's adversarial panel (counter-argument + premortem + first-principles, opus) cross-checked E003's recorded numbers against `outputs/E003_cold.json` / `outputs/E003_warm.json` and found that the *alignment* numbers (unique R², ρ′, Δ, CIs, p) all trace faithfully — but four provenance gaps remain. R07 itself was written to not depend on the unsourced numbers (its under-training caveat leans only on the measured 477-vs-44–95 comparison; `r=-0.88` is cited as the recorded L011 caveat), so **this repairs E003's own record, not R07.**

**The four gaps (each with evidence verified S19):**

1. **Reference-arm perplexities are unmeasured (`null`).** In *both* JSONs, `models.{teacher,gpt2,distilgpt2,untrained}.[*].perplexity = None`. Only the three trained arms carry a measured ppl: `kd_cold` mean **476.5** (per-seed 455.5/480.7/493.4), `kd_warm` mean **94.9** (93.9/96.9/93.9), `lmft_warm` mean **44.0** (44.18/43.63/44.13). Yet E003.md's headline table and R07's transcription quote teacher **74**, gpt2 **105**, distilgpt2 **169**, untrained **~50000** as if measured on the same held-out slice. Those four are not in the run.
2. **The dissociation analysis is prose-only, never archived.** The `r=-0.88` log-ppl fit, its coefficients `align = 0.050 − 0.0079·ln(ppl)`, the residuals (kd_warm +0.0001 on the line; gpt2 +0.006 outlier), the two bootstrap dissociation P-values `P(gpt2≤kd_warm)=0.092` and `P(lmft≤kd_warm)=0.085`, and "one fold carries ~44% of the signal" exist only as prose in E003.md's post-run review and L011. They are load-bearing *against* the strong claim (they are why R07 refuses objective-specific shedding), so they need to be as reproducible as the claim they guard.
3. **E003.md header points to a dead output file.** Line ~8 `Output: outputs/E003_kd_alignment.json` does not exist; the real artifacts are `outputs/E003_cold.json` + `outputs/E003_warm.json` (+ `.log`).
4. **The "4.5× the teacher" multiplier is mislabelled, not a typo.** Verified S19: `476.5 / 105 (gpt2) = 4.54`, while `476.5 / 74 (gpt2-medium, the teacher) = 6.45`. So the "4.5×" in E003.md/L011 was computed against the **gpt2 student baseline (105)**, not the teacher — the reference is wrong, the arithmetic is right for the wrong denominator.

**The fix (do all four; pick recompute *or* annotate per item, but leave no number un-traceable):**

- **Reference ppls.** Recompute held-out perplexity for `teacher`, `gpt2`, `distilgpt2`, `untrained` on the *exact same* held-out slice E003 used (the 2k wikitext-103 sentences held out of the 96k KD corpus, deduped against Tuckute — confirm the slice/seed in `scripts/run_kd_alignment.py`), with the same tokenization and stride, and write them into the JSONs (or a sidecar `outputs/E003_perplexity.json`). If a model's ppl genuinely cannot be reproduced on that slice (e.g. `untrained`'s ~50000 is a near-vocab-size floor, not a stable measurement), mark it in E003.md as *theoretical / order-of-magnitude, not measured* rather than quoting a precise figure. **Then reconcile E003.md's and R07's table values to whatever is measured** (R07's table is a faithful copy of E003's, so if a reference ppl changes, R07's ppl column changes with it — re-run the report-layer check after).
- **Dissociation stats.** Add a small reanalysis script (e.g. `scripts/reanalyze_e003_dissociation.py`) that reads the per-fold/per-seed alignment arrays already in the JSONs plus the now-measured ppls, recomputes the log-ppl fit (`r`, slope, intercept), the per-point residuals, the two bootstrap dissociation P-values, and the per-fold variance decomposition (the "~44%"), and writes `outputs/E003_dissociation.json`. Cite that artifact from E003.md and L011.
- **Dead pointer.** Fix the `Output:` line in E003.md to list the real files.
- **The multiplier.** Replace "4.5× the teacher" with the correct statement against the measured teacher ppl once known (≈6.4× gpt2-medium), or restate against the gpt2 baseline with the *correct label* ("≈4.5× the gpt2 student's perplexity"), and propagate the fix to L011. Decide which framing E003 actually meant and make it consistent everywhere.

**Acceptance / verification — all hold:**

- [x] Every perplexity in E003.md's table equals a value in an `outputs/E003_*.json` artifact (refs → `E003_perplexity.json`; trained arms → run JSONs), or is labelled order-of-magnitude (untrained, with reason).
- [x] `r=-0.88`, fit coefficients, and the ~44%-fold reproduce from `outputs/E003_dissociation.json`; the two P-values reproduce (0.091/0.083) under the fold×seed bootstrap and are flagged construction-sensitive (not a within-rounding promise — Erfan-approved qualitative criterion). E003.md/L011 cite the file.
- [x] Every `outputs/...` path named in E003.md resolves on disk (4/4 OK).
- [x] The multiplier is arithmetically consistent everywhere it appears: E003.md + L011 now read "≈6.4× the teacher (≈4.5× the gpt2 student)"; R07 has no multiplier.
- [x] **No alignment number, verdict, or rung changed** — R07 md5 byte-identical (`39160c8…`); E003.md verdict rows (unique-R²/ρ′/Δ/CI/p) not in the diff.
- [N/A] `run_checks.py --layer report` on R07 — R07 was not edited (references already matched), so no report-layer re-check was triggered.
- [x] Provenance spot-check: every E003.md table ppl traces to an artifact or is labelled; no untraceable number remains.

- ~~(Tooling) Build a number-freshness verifier (`check_number_freshness.py`)~~ — **dropped 2026-06-16 (S18).** No honest deterministic check exists: records are prose with many numbers, so matching a cited value to the current one is comprehension, not regex — a script would give false confidence. **Reframed as a subagent spot-check** (provenance-d011.md): at a full-loop handoff for manuscript-bound work, a cheap subagent (sonnet; haiku if numbers are cleanly keyed) verifies each load-bearing number against its current record and flags mismatches. The `number-provenance` `wrap-auditor` already covers this at session close. No script to build.

- [ ] **Get to the bottom of graphify** (deferred — tooling, not science). Integrated 2026-06-11 as a
      code navigator (`.claude/skills/graphify/`, `.graphifyignore`, CLI via uv tool; see timeline
      `2026-06-11-2257`). Code graph = useful/accurate/free; semantic doc-graph via Flash-Lite = thin
      (file-level, redundant with gbrain). **If revisited:** try `--mode deep` + Gemini 3.1 Pro on
      `docs/`, and name the use it serves that gbrain doesn't — else the code-graph-only conclusion
      stands. Full 2500-file semantic build NOT run. For any Gemini run use the Antigravity subscription
      quota or a billing-off key (never the training-on-inputs free tier).
- [x] 2026-06-11 — **Integrated graphify** (CLI + `/graphify` skill + Antigravity config + scoped
      `.graphifyignore`; stripped its nag PreToolUse hooks; `CLAUDE.md` section subordinate to ladder+gbrain).
      `ea22aa4`, `077eef2`.
- [x] 2026-06-09 — **Disabled the GateGuard fact-forcing + doc-file-warning ECC hooks** for this repo via
      `.claude/settings.json` `ECC_DISABLED_HOOKS` (D012). Settles the Session-2 friction.

## Done

- [x] 2026-06-11 — **E005: F1 headline → CONFIRMED in-domain.** Qwen2.5-1.5B→0.5B KD (LoRA, KD-KL), alignment-guided vs perplexity-only. Paired (kd_brain − kd_brain_permuted) at **matched perplexity** = **+0.0081 [+0.0023,+0.0171]**, CI excludes 0, 4/5 folds + (leave-fold-4-out +0.0042), brain-specific, holds despite worse ppl (rules out L011). The dissociation E003/E004 couldn't establish. Small (~1.6% NC) → A+B synthesis. Q3/F1 → 🟡 PARTIAL-PASS (Erfan-confirmed). `experiments/E005_*.md`, L014. (`2a78171`→`7a1375c`)
- [x] 2026-06-11 — **E006: powered voxelwise A2 → STRONG PASS.** Built LeBel UTS03 voxelwise harness (`lebel_adapter.py`, `run_lebel_encoding.py`; reuses official deep-fMRI-dataset pipeline; staged TextGrids+eng1000; CC_norm voxel selection from `wheretheressmoke` repeats; phone-tier+eng1000 nuisance). Trained−untrained gap +0.021/+0.028 on 11.4k NC voxels, 95–99% +; clears Hadidi/Feghhi bar. Lever statistic underpowered (MDE +0.013) → E007 not built. Q0/A2 → ✅ PASS (powered). L013. (`27e2763`→`e39eea8`)
- [x] 2026-06-11 — **E004: L_brain lever test (R03 Q2) + D010 → PARTIAL.** Built `brain_loss.py` (loss family) + `run_brain_lever.py` (LoRA, rotating folds, per-kind permuted twins). 2 pre-run oracle reviews (HOLD→PASS) caught the covariate-shift confound (→rotating folds), full-FT ppl-collapse (→LoRA), readout absorption (→permuted twins). Brain-specific lever +0.0032 (Qwen mse vs permuted) but small/fragile, sub-threshold on 5 ROIs. D010 → co-trained MSE. Q2 → 🟡 PARTIAL. L012. (`888b446`→`668fc9f`)
- [x] 2026-06-11 — **paper-digest Hadidi/Feghhi 2026 (NatComms)** → `literature/canonical/hadidi-2024_*.md` (the anti-confound bar: >80% of GPT-2XL variance is PWR+GloVe; residual ≤10%). lit-scout sweep → lean toward trade-off-curve framing. (Note: dup of `feghhi-2024` stub — dedup pending.)
- [x] 2026-06-10 — **E003: perplexity-only-KD alignment kill-test (R04 Q1) → PARTIAL headroom.** Two pre-run Opus reviews reshaped the design (cold-init verdict arm escaping the warm-init trap; headroom not binary; ≥3 seeds; floor-anchored ρ′). Ran cold/warm logit-KD + LM-finetune control (gpt2-medium→gpt2, Tuckute, 3 seeds). Monotone alignment gradient (conventional ≈ teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37 > floor) rules out preserve-for-free; from-scratch KD far below teacher (Δ=0.018, p<0.001). A post-run Opus skeptic refuted the "F1 confirmed" over-read — alignment tracks ppl (r=−0.88), KD-specific dissociation only p≈0.1, cold arm under-trained. F1 neither killed nor confirmed; resolving experiment = E004 (matched-perplexity). `experiments/E003_*.md`, L011, R03/R04 ladder. (`b2f23bb`→`b996a2c`)
- [x] 2026-06-10 — **R04 §7 factual corrections to R03 verified already applied** (prior session `4b548d1`): Moussa, Bilgin cosine-not-L2, Merlin, Oota softening, Pirlot + Cheng/Yu sign conflict. R03 line-1 corruption confirmed absent. Nothing to do.
- [x] 2026-06-10 — **Filled the deferred course-material note gaps.** 6 Sonnet subagents wrote 7 agent-digest notes (gitignored, co-located with PDFs): Block-4 VAEs `3_IWAE` / `4_GMVAE` / `7_VQ-VAE` / `8_NVAE` / `9_VampPrior`, and info-theory `16_Fisher/CR` / `17_CramerRaoII`. All adjacent (not load-bearing), each with a Thesis hook + Source audit. `06-theory-grounding.md` + INDEX updated; peripherals (2 multimodal VAEs, gamma-Poisson, Occam, ARDM) deliberately skipped.
- [x] 2026-06-10 — **Course material adopted as theory-grounding source (D014).** Recon via 3 subagents → no re-OCR needed (existing `*_study.md`/`*_OCR.md` beat any extraction; L010). Wrote `docs/06-theory-grounding.md` (concept→thesis map), `data/course-material/INDEX.md`; folded the formal math into R03 §2 (new Step 7: MI generalization bound, DPI, conditional MI, rate-distortion) + landscape §E + CLAUDE.md + README. Fixed R03 line-1 transcript-paste corruption.
- [x] 2026-06-10 — **Two real datasets staged (D013):** Tuckute 2024 (`data/tuckute2024/`, real ROI-level) + LeBel UTS03 (`data/lebel_ds003020/`, ~20 GB voxelwise, response matrix verified L005). Via osfclient + anonymous S3. Resolves the D008 "re-evaluate before pulling" task.
- [x] 2026-06-10 — **E002 real-data encoding feasibility → A2 PASS.** Trained LM mid-layer unique R² positive (gpt2 +0.020, gpt2-medium +0.019, Qwen2.5-0.5B +0.036), untrained controls negative (3 seeds). `experiments/E002_*.md`. The verdict synthetic E001 could not give. (L007)
- [x] 2026-06-10 — **R03 brain-as-training-signal direction doc** + brain-tuning prior-art sweep (2 subagents): the inversion is largely scooped (L008); unscooped slice = distillation-at-matched-budget / low-data. Canonical note `moussa-2025`, landscape updated.
- [x] 2026-06-09 — **Dataset registry** → `docs/05-dataset-registry.md`. 11 neural/behavioral datasets with full feature profiles. Key finds: zhu-2025 out of scope (non-language), yin-2025 "Association" is synthetic NLP not neural (AUX), Tuckute 2024 elevated to PRIMARY candidate (noise ceiling r≈0.56). Division of labour clarified across `04`/`R02`/`05`. (cd79447)
- [x] 2026-06-09 — **Paper-repos corpus** → `scripts/paper-repos.tsv` + `scripts/clone_paper_repos.sh`. 21 repos shallow-cloned into `data/paper-repos/` (~8.6 GB, gitignored), 0 failures. Two open R02 URLs resolved (feghhi, merlin). (8178046)
- [x] 2026-06-09 — **Language-fMRI benchmark survey + power analysis** → `docs/04-data-benchmarks.md`.
      SPOF resolved (D008): LeBel ds003020 primary, Narratives generalisation, Pereira plumbing.
- [x] 2026-06-09 — **Toy pilot harness built + validated** (synthetic): GPT-2-medium→small distillation,
      encoding model, anti-confound partition, ≥3 seeds → `scripts/`, `configs/`, `docs/experiments/E001`.
      (Real-data run moved to "Now"; synthetic cannot answer the science — L004.)
- [x] 2026-06-09 — `uv add torch transformers datasets scikit-learn scipy nibabel nilearn` (pilot deps).
- [x] 2026-06-08 — Swarm reconnaissance of Nexus + brain-alignment idea; built `docs/` knowledge base.
- [x] 2026-06-08 — Minimal uv environment (`uv run` verified, Python 3.11, no scaffolding).
- [x] 2026-06-08 — Repo `CLAUDE.md`, curated subagents, reasoning-frame reference.
- [x] 2026-06-08 — Git initialized; 5 atomic scoped commits; continuous-commit norm adopted (D007).
- [x] 2026-06-08 — Scope locked (D006): MSc/UC3M, ~end-Aug-2026, feasibility-first, edge deferred.
