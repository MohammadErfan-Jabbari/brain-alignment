# Tasks — the path behind and ahead

Durable backlog. The session task tracker is ephemeral; this file is the source of truth across
sessions. Move items between sections; don't delete (strike completed ones with a date).

## Now (current focus — ANALYSIS: get Erfan up to speed R03→now, then submit-polish)

**Experimental program is CLOSED (Erfan-confirmed 2026-06-12).** The next 2–3 sessions are ANALYSIS — Erfan needs to be walked through everything after R03. No new evidence; consume + communicate it.

- [~] **Walk R03→now (the get-up-to-speed arc)** — IN PROGRESS (S9). Layer 0 (frame/bet) + Layer 1 (measurement/lever/E007-reroute) taught + captured in `docs/reports/R05` (LIVING). **Resume at Layer 3 = E005** (apparent +0.0081 → E008 per-individual null) → robustness escapes (E011/E013b/E013/E014) → Fork-B reframe. Teaching each = writing the next R05 section (§9–§14). Source: `docs/experiments/ENNN`, `learnings.md` L011–L030.
- [ ] **Figures:** confirm `scripts/figures/make_figures.py` renders the recorded numbers (averaging-collapse / powered A2 / A3 nulls / dose-response-with-caveat).
- [ ] **Manuscript read-through → submit:** venue/length; optional §2 prose polish. (References verified + [VERIFY] flags cleared, lit-scout 2026-06-12.)

### Queued — next MAJOR working build (a fresh session; Erfan-approved as possible next step)
- [ ] **Full-FT multi-subject naturalistic voxelwise (the one untested door).** Full fine-tuning (NOT a LoRA distillation readout) on denizenslab n=6 (`data/paper-repos/speech-llm-brain`), under the protocol. Scoped in `docs/experiments/E013_*.md`. n-conditional on inducing an above-base improvement (the distillation lever's failure is a mechanism failure, E013/L027). Multi-day build — launch fresh.

### Done this session (S9 — analysis, 2026-06-12)
- [x] 2026-06-12 — **Taught Layer 0 + Layer 1** of the thesis arc (Socratic, native `socratic-tutor`); Erfan mastered the frame/bet + measurement/lever/MDE/reroute.
- [x] 2026-06-12 — **`docs/07-concepts-primer.md`** created — DRY home for reusable primitives (voxel/ROI, encoding model, unique R², noise ceiling, perplexity, datasets, E/R/L/D-numbering); E002/R03/README point at it.
- [x] 2026-06-12 — **`docs/reports/R05`** created (LIVING first-principles narrative, Layer 0→1); **panel-reviewed** (counter-argument/first-principles/socratic/premortem) + revised (ceiling 0.353→0.49/~7%, ρ′ relabel, A3 novelty scope, DPI chain, §3 per-rung verdicts, theory hedges, pedagogical glosses).
- [x] 2026-06-12 — **Doc-shortfall audit swarm** (5 haiku) → fixed README missing-ladder-row, charter stale "Activating" status; filed the rest below.
- [x] 2026-06-12 — Quiz-style feedback saved to memory + gbrain (vary correct-answer position; prefer open-ended).

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
- [ ] **(Fresh working session) Full-FT multi-subject naturalistic voxelwise** (denizenslab n=6) — the one untested *induction method*; n-conditional on inducing an above-base improvement (E013/L027).
- [x] 2026-06-12 — **(L031) Operating rule for Stop-hook re-fires** — Erfan-approved + ADDED to repo `CLAUDE.md` ("Working with Erfan": auto re-fires aren't fresh intent; most recent explicit message wins; on "wrap/stop", wrap).
- [ ] **(Analysis polish) Manuscript pre-submission:** trim "one untested door" repetition (premortem #5, reads as unfinished Fork-A); venue/length; optional §2 prose.

### Done earlier this session (S8, 2026-06-11)
- [x] 2026-06-11 — ~~LeBel voxelwise TRANSFER test~~ **DROPPED** — S8 panel showed it underpowered (paired-LeBel MDE needs ρ≥0.9 to see even +0.0081; `reanalyze_e005_e006.py`).
- [x] 2026-06-11 — **E008 per-participant solidification** ran → in-domain F1 is a **per-subject NULL** (well-powered); E005's +0.0081 = group-averaged-target artifact. Ladder L3/F1 ❌, Fork-B reframe (D018, Erfan-confirmed). L016.
- [x] 2026-06-11 — **Doc-consistency:** feghhi-2024 → hadidi-2024 canonical redirect; verified R03/R04 have **no** stale "E004=headline" refs (0 mentions).
- [x] 2026-06-11 — Built the **thinking panel** (D017) + digested A3 prior art (Negi 2025, Guo 2024, Schwartz 2019) + Proietti 2025.
- [ ] **(Optional, Fork-B rigor) λ-sweep / multi-rate rate-distortion curve** on the averaged target — the "how small" characterization, if A3 needs magnitude context. `run_brain_lever.py --lambda-grid` supports it.

## Next (de-risk the thesis — ordered by leverage)

- [ ] **`paper-digest` remaining finalists** if needed for A3 related-work: Merlin & Toneva 2026 "When LMs Lose Their Mind" (arXiv 2603.23091), Bilgin/Wehbe 2026. (Negi/Schwartz/Guo/Proietti digested S8.)
- [ ] **Sharpen the contribution per the Fork-B reframe:** the thesis is now A2-powered-real + the well-powered per-subject null (in-domain F1 doesn't generalize to individuals) + the anti-confound methodology + A3 (practical payoff). Update R03/R04 §-framing to Fork-B + D018. Position vs Negi/Schwartz (the matched-ppl + permuted-brain control is our novelty).

## Later (once the pilot says go)

- [ ] Lock the baseline matrix runs (perplexity-only KD, structure-aware KD, alignment-guided, hybrid).
- [ ] Build the anti-confound evaluation harness (contiguous splits, nuisance baselines).
- [ ] Promote H001 to a Design with a locked protocol; add competing hypotheses H002/H003.
- [ ] **(DEFERRED until feasibility holds)** Define the "edge" deployment scenario concretely
      (FLOPs/latency/params target). Not in scope until the fundamental question is answered.

## Infrastructure / housekeeping

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

- [x] 2026-06-11 — **E005: F1 headline → CONFIRMED in-domain.** Qwen2.5-1.5B→0.5B KD (LoRA, KD-KL), alignment-guided vs perplexity-only. Paired (kd_brain − kd_brain_permuted) at **matched perplexity** = **+0.0081 [+0.0023,+0.0171]**, CI excludes 0, 4/5 folds + (leave-fold-4-out +0.0042), brain-specific, holds despite worse ppl (rules out L011). The dissociation E003/E004 couldn't establish. Small (~1.6% NC) → A+B synthesis. L3/F1 → 🟡 PARTIAL-PASS (Erfan-confirmed). `experiments/E005_*.md`, L014. (`2a78171`→`7a1375c`)
- [x] 2026-06-11 — **E006: powered voxelwise A2 → STRONG PASS.** Built LeBel UTS03 voxelwise harness (`lebel_adapter.py`, `run_lebel_encoding.py`; reuses official deep-fMRI-dataset pipeline; staged TextGrids+eng1000; CC_norm voxel selection from `wheretheressmoke` repeats; phone-tier+eng1000 nuisance). Trained−untrained gap +0.021/+0.028 on 11.4k NC voxels, 95–99% +; clears Hadidi/Feghhi bar. Lever statistic underpowered (MDE +0.013) → E007 not built. L0/A2 → ✅ PASS (powered). L013. (`27e2763`→`e39eea8`)
- [x] 2026-06-11 — **E004: L_brain lever test (R03 Layer 1) + D010 → PARTIAL.** Built `brain_loss.py` (loss family) + `run_brain_lever.py` (LoRA, rotating folds, per-kind permuted twins). 2 pre-run oracle reviews (HOLD→PASS) caught the covariate-shift confound (→rotating folds), full-FT ppl-collapse (→LoRA), readout absorption (→permuted twins). Brain-specific lever +0.0032 (Qwen mse vs permuted) but small/fragile, sub-threshold on 5 ROIs. D010 → co-trained MSE. L1 → 🟡 PARTIAL. L012. (`888b446`→`668fc9f`)
- [x] 2026-06-11 — **paper-digest Hadidi/Feghhi 2026 (NatComms)** → `literature/canonical/hadidi-2024_*.md` (the anti-confound bar: >80% of GPT-2XL variance is PWR+GloVe; residual ≤10%). lit-scout sweep → lean toward trade-off-curve framing. (Note: dup of `feghhi-2024` stub — dedup pending.)
- [x] 2026-06-10 — **E003: perplexity-only-KD alignment kill-test (R04 Layer 2a) → PARTIAL headroom.** Two pre-run Opus reviews reshaped the design (cold-init verdict arm escaping the warm-init trap; headroom not binary; ≥3 seeds; floor-anchored ρ′). Ran cold/warm logit-KD + LM-finetune control (gpt2-medium→gpt2, Tuckute, 3 seeds). Monotone alignment gradient (conventional ≈ teacher > warm-KD 0.84 > distilgpt2 0.60 > cold-KD 0.37 > floor) rules out preserve-for-free; from-scratch KD far below teacher (Δ=0.018, p<0.001). A post-run Opus skeptic refuted the "F1 confirmed" over-read — alignment tracks ppl (r=−0.88), KD-specific dissociation only p≈0.1, cold arm under-trained. F1 neither killed nor confirmed; resolving experiment = E004 (matched-perplexity). `experiments/E003_*.md`, L011, R03/R04 ladder. (`b2f23bb`→`b996a2c`)
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
