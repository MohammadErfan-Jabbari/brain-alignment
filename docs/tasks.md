# Tasks — the path behind and ahead

Durable backlog. The session task tracker is ephemeral; this file is the source of truth across
sessions. Move items between sections; don't delete (strike completed ones with a date).

## Now (current focus — ANALYSIS: get Erfan up to speed R03→now, then submit-polish)

**Experimental program is CLOSED (Erfan-confirmed 2026-06-12).** The next 2–3 sessions are ANALYSIS — Erfan needs to be walked through everything after R03. No new evidence; consume + communicate it.

- [ ] **Walk R03→now (the get-up-to-speed arc):** R03 hypothesis → E005 apparent +0.0081 → E008 per-individual null → the four robustness escapes (E011 capacity / E013b objective / E013 voxelwise substrate / E014 measurement-side) → Fork-B reframe. Source: `docs/experiments/ENNN`, `learnings.md` L011–L028, `upspeed.md`.
- [ ] **Figures:** confirm `scripts/figures/make_figures.py` renders the recorded numbers (averaging-collapse / powered A2 / A3 nulls / dose-response-with-caveat).
- [ ] **Manuscript read-through → submit:** venue/length; optional §2 prose polish. (References verified + [VERIFY] flags cleared, lit-scout 2026-06-12.)

### Queued — next MAJOR working build (a fresh session; Erfan-approved as possible next step)
- [ ] **Full-FT multi-subject naturalistic voxelwise (the one untested door).** Full fine-tuning (NOT a LoRA distillation readout) on denizenslab n=6 (`data/paper-repos/speech-llm-brain`), under the protocol. Scoped in `docs/experiments/E013_*.md`. n-conditional on inducing an above-base improvement (the distillation lever's failure is a mechanism failure, E013/L027). Multi-day build — launch fresh.

### Done this session (S8 continuation, 2026-06-12)
- [x] 2026-06-12 — **E011** heavy LoRA: per-individual null robust to capacity (+0.0004, incl 0; L019).
- [x] 2026-06-12 — **E013b** contrastive/InfoNCE objective (n=9): null holds across objectives at matched ppl (−0.0002; L025).
- [x] 2026-06-12 — **E013** voxelwise same-substrate (UTS01/02/03 + λ-sweep): distillation lever doesn't take hold at any λ; v1 failed-manipulation retracted; mechanism failure (n≥5 moot); L026/L027.
- [x] 2026-06-12 — **E014** averaging on the encoding brain-score: NOT a confound-lift (per-subject positive → legitimate-SNR/estimand); fixed unseeded-PCA bug; verified before folding → paper unchanged; L028.
- [x] 2026-06-12 — **Manuscript v0.9 COMPLETE-AS-ARTIFACT:** References (verified vs primary sources, lit-scout); completeness-critic closed orphan citations + dangling §-pointers.
- [x] 2026-06-12 — **Ladder FLIPPED (Erfan-confirmed):** experimental program closed → analysis/write-up phase.

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
