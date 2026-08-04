---
title: "Decision Log"
tags: [decision]
---

# Decision Log

Append-only. One entry per real decision. Newest at the bottom. Format: ID, date, decision,
rationale, and what would reverse it. Reference other docs with relative links.

---

### D001 — 2026-06-08 — Repo is a single-thesis research workspace, not a Nexus port

**Decision:** Build `brain-alignment` as a self-contained, lightweight research repo. Do **not** port
the Nexus v2 `.nexus/` stage-machine (`config.yaml` gates, dual `AGENTS.md`/`CLAUDE.md` surfaces,
reconciliation).
**Rationale:** Nexus v2's documented failure mode was over-coupling; v1's was over-specification. For
one owner / one paper / one node, that machinery is pure overhead. We keep the epistemic spine, drop
the bureaucracy. See [`../03-methodology.md`](../03-methodology.md).
**Reverses if:** this grows into a multi-paper program needing cross-project memory.

### D002 — 2026-06-08 — Knowledge base lives in `docs/`, not `.nexus/`

**Decision:** All durable research memory (charter, landscape, decisions, timeline, hypotheses,
experiments, literature, learnings, upspeed) lives in `docs/`, per Erfan's explicit request.
**Rationale:** One obvious place; plain markdown; survives across sessions; no hidden control plane.
**Reverses if:** Erfan prefers a different top-level location.

### D003 — 2026-06-08 — Minimal uv environment, always `uv run`

**Decision:** `pyproject.toml` with `[tool.uv] package = false`, Python 3.11, `.venv/`, no `src/`
scaffolding or sample modules. Add libraries with `uv add` as needed; torch pinned to the cu128
index. All Python runs via `uv run`.
**Rationale:** Erfan's request for a minimal env; mirrors the proven brain-jepa setup on this box.
**Reverses if:** we need to package/distribute code (then flip `package`).

### D004 — 2026-06-08 — Self-contained literature: copy canonical notes in

**Decision:** Copy the 20 brain-alignment/distillation canonical paper notes and the prior dossier +
oracle review from the Nexus v1 archive into `docs/literature/`.
**Rationale:** The repo should not depend on the soon-to-be-overhauled Nexus tree to be useful.
**Reverses if:** never; provenance preserved in `literature/_prior-work/`.

### D005 — 2026-06-08 — Curated subagents, adapted to this repo

**Decision:** Define a small set of research subagents (`lit-scout`, `paper-digest`,
`oracle-reviewer`, `session-logger`) in `.claude/agents/`, adapted to the `docs/` layout. Skip the
~9 Nexus stage-bound agents wholesale; add more only when a need recurs.
**Rationale:** Adaptive semistructure — earn each agent. The adversarial `oracle-reviewer` reproduces
the single most valuable artifact from the prior work (the HOLD review that exposed the gaps).
**Reverses if:** a dropped agent proves repeatedly needed.

### D006 — 2026-06-08 — Scope lock: MSc thesis, feasibility-first, edge deferred

**Decision:** This repo serves Erfan's **MSc thesis (ML for Health, UC3M)** — the NeurIPS track is
dropped. Tentative deadline **~end of August 2026** (exact TBD). The first objective is a
**fundamental feasibility question — does the LLM↔brain alignment signal actually carry usable
information that helps a downstream task, beyond confounds?** The "edge"/deployment framing is
**explicitly deferred** until that question is answered.
**Rationale:** Erfan's direction: establish whether the claim holds before designing for deployment.
Matches the prior oracle review (operationalize + de-risk first) and avoids over-claiming.
**Reverses if:** the feasibility question resolves positively and we move to the deployment story.

### D007 — 2026-06-08 — Continuous atomic commits as the granular project timeline

**Decision:** Commit changes **continuously and atomically** — each meaningful step is its own scoped
commit with a proper conventional-commit message — so git history is a fine-grained, inspectable
record of file changes over time. This is **in addition to, never a replacement for, the docs
record:** decisions still go in this file and every session still gets a `../timeline/` log. Docs
carry the *why* (reasoning, narrative); git carries the *what/when* (mechanical diffs). Rules
unchanged: scoped staging only (never `git add -A`/`.`), no `--amend`. **Amended by D054 for
session close:** wrap commits are pushed to `origin` by default unless Erfan explicitly says not to
or the push is blocked.
**Rationale:** Erfan wants a detailed, granular overview of how the repo evolved — and the decision
log + timeline remain the canonical research record.
**Reverses if:** never expected — it is a working norm.

### D008 — 2026-06-09 — Benchmark choice: LeBel ds003020 primary, Narratives generalisation, Pereira plumbing

**Decision:** Adopt **LeBel et al. 2023 (OpenNeuro `ds003020`)** as the primary language-fMRI benchmark
for the thesis result (powered within-subject deep-sampling, reported noise ceiling, CC0/CC-BY, anonymous
S3/DataLad — no login). Use **Narratives (`ds002345`)** as the cross-subject generalisation check and
**Pereira 2018 (OSF `crwz7`)** as the lightweight plumbing sanity-test. Full survey + power analysis in
[`../04-data-benchmarks.md`](../04-data-benchmarks.md).
**Rationale:** Resolves the #1 SPOF ([`01-research-landscape.md`](../01-research-landscape.md)): an open, adequately powered benchmark
must exist. Three do, none gated. The charter's data-access kill condition is not triggered.
**Reverses if:** the LeBel neural data proves impractical to stage, or a better-powered open benchmark
appears; then promote Narratives or pull a second LeBel subject.

### D009 — 2026-06-09 — E001 pilot ran the hybrid path (real sentences + synthetic fMRI), not real neural data

**Decision:** The toy pilot (E001) was built data-independent and validated on **real Pereira sentences
paired with synthetic fMRI**, because the cleanly-downloadable Pereira bundle (crwz7) contains stimuli
but not neural responses (L005). We did **not** fabricate a real-data result; the harness is left
one config swap from the real neural matrix.
**Rationale:** Follows the overnight instruction to be adaptive about the data dependency and not block:
build everything, smoke-test on a synthetic stand-in, leave it ready to plug real data in. A synthetic
result is labelled as plumbing-only everywhere (E001, L004), never as evidence about the thesis.
**Reverses if:** never — it is a faithful record of what was run. The next step (real fMRI) supersedes it.

### D010 — 2026-06-09 — Brain-alignment loss form is still open; trainable head is a placeholder

**Decision:** E001 implements $\mathcal{L}_{\text{brain}}$ as a trainable linear head from the student's
middle layer to the training fMRI. This is a **placeholder**, not the locked design. The frozen
teacher-encoding-map loss and a CKA-style differentiable proxy remain live candidates to compare on real
data (still the open "decide the form of $\mathcal{L}_{\text{brain}}$" task).
**Rationale:** The head overfits the contiguous train block on synthetic data; a frozen map or geometric
(CKA) loss may generalise better and avoids a learned head. Decide empirically once neural data is staged.
**Reverses if:** the head form wins on real data, or a different proxy proves superior.

### D011 — 2026-06-09 — Two explicit session modes: working (produce evidence) vs analysis (communicate it)

**Decision:** Formalize that work in this repo runs in one of two declared modes. A **working session**
takes a task/goal and produces evidence — implement, run, analyze, store results (phases Design → Run →
Judge; outputs in `../experiments/`, decisions, learnings). An **analysis session** consumes and
communicates that evidence — recall what was done, explain concepts, digest results, produce figures,
write manuscript/report sections (phases Argue → Compound; outputs in `../manuscript/`). Each session
declares its mode at the start; the close ritual and `upspeed.md` framing follow the mode. Binding rule:
**an analysis session may only report numbers a working session actually recorded in `docs/`** — a
missing number is a gap to flag, never one to invent. Encoded in [`../../CLAUDE.md`](../../CLAUDE.md) ("Two kinds of
session") and [`../03-methodology.md`](../03-methodology.md) ("Two session modes"); analysis outputs home created at
`../manuscript/`.
**Rationale:** The two modes have opposite self-deception risks — a working session over-fits the hoped
result (guarded by kill criteria / locked design / anti-confound), an analysis session narrates past the
evidence (guarded by the cite-or-flag rule). Naming the seam keeps each honest and tells every session
which standard applies. Pure adaptive semistructure: the distinction recurs every session, so it earns a
rule. No new machinery — just a mode label and an output home.
**Reverses if:** the modes blur in practice (most sessions cross the seam anyway) and the label stops
adding clarity, or a third recurring mode appears that the binary doesn't capture.

### D012 — 2026-06-09 — Disable the noisy ECC fact-forcing/doc-warning hooks for this repo

**Decision:** Create tracked `../../.claude/settings.json` with
`env.ECC_DISABLED_HOOKS = pre:edit-write:gateguard-fact-force,pre:bash:gateguard-fact-force,pre:write:doc-file-warning`.
Hook profile stays `standard`; every other ECC hook (push guard, context monitor, MCP health, session
lifecycle/metrics) keeps running. Settles the Session-2 friction item.
**Rationale:** The GateGuard fact-forcing gate fires on the *first* Edit/Write/Bash and demands a
generic "list importers / data schemas / quote the instruction" preamble. In a docs-heavy solo research
repo (mostly markdown with occasional small Python scripts) those questions are near-empty and the gate
is pure latency — it fired 6× while editing markdown this session. Real rigor here is enforced by the
methodology (oracle-reviewer, predeclared kill criteria, anti-confound protocol, the D011 cite-or-flag
rule), not a per-edit gate. `doc-file-warning` is not a safety control and is noise in a repo whose
purpose is writing docs. Tradeoff accepted: the env var is static, so working sessions editing
`scripts/*.py` also lose the gate; judged acceptable for a single-owner repo.
**Reverses if:** we want the gate back for code-heavy working sessions (unset the relevant id, or set
it only in the gitignored `settings.local.json`), or a future incident shows the gate would have caught
a real mistake.

### D013 — 2026-06-10 — Stage TWO real datasets: Tuckute 2024 (fast Layer-0/1 testbed) + LeBel UTS03 (powered Layer-3 primary)

**Decision:** Re-evaluated D008's "LeBel primary, pull first" against the registry's denizenslab/Tuckute
candidates and chose to stage **both** ends of the design space rather than one. (1) **Tuckute et al. 2024**
(OSF `ru38b`, `data.tar`, ~8 MB) — 1000 isolated baseline sentences × 5 LH language ROIs, 5-train-participant
average, published noise ceiling; downloaded + extracted to `data/tuckute2024/`. (2) **LeBel `ds003020`,
subject UTS03** preprocessed responses (~20 GB, 84 story HDF5s) — synced from OpenNeuro S3
(`aws s3 sync --no-sign-request`, no login, no DataLad needed) to `data/lebel_ds003020/preprocessed_data/UTS03/`.
**Tools:** `osfclient` + `awscli` `uv pip install`ed into the venv (transient infra, not pyproject deps;
DataLad/git-annex were unavailable and unnecessary — anonymous S3 sufficed).
**Rationale:** Tuckute is tiny, real, ROI-level, highest-ceiling, and — being isolated sentences — sidesteps
the temporal-autocorrelation leakage of naturalistic data; it is the fastest path to a real-data A2 verdict
(E002, run this session) and matches the existing sentence-level harness almost directly. LeBel stays the
D008 *powered within-subject thesis-result* benchmark (CC_norm ceiling) but needs a time-series/FIR adapter,
so it is staged-not-run. Keeping both means Layer-0/1 work starts immediately (Tuckute) without blocking the
powered Layer-3 result (LeBel). **D008 is refined, not reversed:** LeBel remains primary-for-the-result;
Tuckute is primary-for-the-pilot. denizenslab was passed over for now (no published noise ceiling; Tuckute
gives a real one at comparable friction).
**Reverses if:** Tuckute's ROI-level coarseness proves too low-dimensional to discriminate the distillation
arms (then promote LeBel voxelwise sooner, or pull a denizenslab subject), or LeBel's adapter proves
impractical.

### D014 — 2026-06-10 — Adopt the MSc coursework as a third source of truth; index it, don't re-extract it

**Decision:** Erfan's master's coursework (Information Theory for ML + Probabilistic ML, UC3M 2025–26),
added to `data/course-material/` (125 files, ~292 MB, gitignored), is adopted as the thesis's **theory-grounding
source**, alongside the papers and the datasets. Three sub-decisions: **(1) No re-OCR / no PDF-extraction pass.**
The lecture decks already have Erfan's own `*_study.md` (teaching notes) and `*_OCR.md` (audited formula
reconstructions) from a `course-lecture-study` workflow; these are *higher quality* than any fresh OCR of the
sparse, image-heavy slides, so the markdown notes ARE the usable text and the PDFs are kept only as
source-of-record. The reframing is the point: this was never an extraction problem, it is a curation+integration
problem. **(2) Gitignored + indexed, not committed-as-text.** The notes stay under gitignored `data/` (canonical
copies live in Erfan's `~/uni/`); the committed, portable record is the curated index [`docs/06-theory-grounding.md`](../06-theory-grounding.md)
plus a navigation `data/course-material/INDEX.md`. **(3) Fold the load-bearing math into the live docs now.**
R03 §2 gains a Step 7 that anchors its first-principles bounds to the course's exact theorems (MI generalization
bound `gen ≤ √(2σ²I(W;Zⁿ)/n)`, data-processing inequality, conditional MI = "unique R²", rate-distortion = the F1
trade-off curve); [`01-research-landscape.md`](../01-research-landscape.md) §E and `CLAUDE.md` "Read this first" now point at the grounding doc.
**Rationale:** The course supplies, in proved textbook form, the exact math R03 was invoking informally — the
weak-prior bound IS the MI generalization bound, the unique-R² metric IS conditional MI, the compression brake IS
the DPI, the F1 trade-off IS rate-distortion. Capturing that lets future methods/related-work sections cite rather
than assert. Running a generic PDF/OCR skill would have *destroyed* value (worse than the existing notes) and burned
compute — the subagent recon established this before any extraction was attempted.
**Reverses if:** portability of the raw notes themselves becomes necessary (then un-ignore `*.md` under
`data/course-material/`, < 1 MB of text), or a course concept currently marked "adjacent" (Fisher/Cramér-Rao,
the Block-4 VAE papers) becomes load-bearing and needs a `paper-digest` pass.

### D015 — 2026-06-10 — State lives in a maintained ladder board + an `/orient` start command; stop hand-carrying it between sessions

**Decision:** Make `docs/ladder.md` the **single canonical status board** for project state: the kill-gated
scientific rungs (R03 §5 / R04 §8), each with status, the experiment + verdict that addressed it, and the next
action — plus a "Next session" block (mode + concrete step). It is the source of truth; when `upspeed.md`,
`tasks.md`, or R03/R04 disagree, the ladder wins and they get fixed. R03 §5 keeps the *narrative/why*; the ladder
holds the *live status*. Maintained at **every** session close, **after Erfan confirms the verdict** (a rung flips
to ✅ only on an agreed, `experiments/`-recorded result; partials stay 🟡). Wired into the CLAUDE.md "Read this
first" list (item 0) and close ritual, and into the `session-logger` agent (new step 5b). Add a project command
`/orient` (`.claude/commands/orient.md`): with no specific task, it reads the ladder + upspeed + tasks + latest
timeline, reports where we are and the single next step (implementation or analysis), and **waits for go-ahead** —
read-only, no work until Erfan confirms. Its bookend is **`/wrap`** (`.claude/commands/wrap.md`): the
close command that runs the `session-logger` ritual *plus* a continuity audit (friction worth fixing,
tooling that misbehaved, doc-consistency / source-of-truth check, new-artifact check, ladder integrity,
brain mirror, git hygiene, open loops), with the same confirm-before-flipping-the-ladder gate. So a
session is bracketed by two one-word commands: `/orient` to open, `/wrap` to close.
**Rationale:** Erfan's friction: passing experiment outputs and "what's next" between sessions by hand is
error-prone and confusing, and state was scattered across upspeed / tasks / R03 §5 / R04 §8. One maintained board +
a start command makes the docs the source of truth and removes the need to write a long bespoke implementation
prompt each session. The human-confirmation gate keeps the board honest (it is the one file the whole continuity
process trusts) and matches the methodology's "raw evidence separate from interpretation, verdicts adjudicated, not
assumed." Adaptive semistructure: this artifact is earned — the need recurred every session.
**Reverses if:** the board and upspeed.md prove redundant (collapse one into the other), or `/orient` drifts from
the docs and stops being trustworthy.

### D016 — 2026-06-11 — `$\mathcal{L}_{\text{brain}}$` form RESOLVED (co-trained MSE encoding loss); E007 not built; thesis framing = A+B synthesis

> **⚠️ PART (3) SUPERSEDED by D018 (2026-06-12).** The "A+B synthesis / F1 confirmed in-domain" framing in (3) below did **not** survive per-individual inference: E008 (n=9, well-powered) returned a per-subject NULL, and E005's +0.0081 was a group-averaged-target artifact. The thesis is now **Fork B** (per-individual null + measurement-validity result). The "Reverses if" condition effectively fired. **Parts (1) [L_brain = co-trained MSE] and (2) [E007 not built] still STAND.** Read (3) only as historical context.

**Decision:** Three coupled resolutions from Session 7 (E004 + E006 + E005):
**(1) D010 is resolved — the brain-alignment loss is a co-trained linear MSE encoding readout** from the student's
verdict-layer pooled hidden state to fMRI, the theory-preferred form (Gaussian lower bound on conditional MI =
the eval metric) and the empirical winner (E004: only co-trained MSE on the strong aligner was brain-specific;
`frozen` = non-specific regularizer, `cka`/`cos` weakest). The E001 "trainable head is a placeholder" framing is
superseded: it *is* the form (at scale, with a clean LM anchor, it transmits brain-specific structure — L012).
**(2) E007 (a TR-level LeBel brain-tuning *lever* loop) is NOT built** — E006 showed the mean-over-voxels lever
statistic is structurally underpowered (MDE +0.013 ≫ the +0.003–0.008 effect). The lever question is answered via
the powered *paired permuted-twin* contrast in the KD setting (E005), not a bespoke TR-loop.
**(3) Thesis framing = A+B synthesis.** F1 is confirmed in-domain (E005: alignment-guided KD recovers brain-specific
alignment beyond perplexity, +0.0081, CI excludes 0) — Fork A — AND the effect is small (~1.6% NC), so the
contribution explicitly includes the rigorous anti-confound characterization + the rate–distortion trade-off curve
(Fork B). Not "alignment-guided distillation wins big"; "it works, here is exactly how much, with the strongest controls."
**Rationale:** empirical (E004/E005/E006) + literature (Hadidi/Feghhi 2026, residual ≤10%). All three rung verdicts
Erfan-confirmed (D015). The A+B framing is more defensible than either an overclaim or a pure null.
**Reverses if:** the LeBel voxelwise **transfer** test (next gate, powered statistic) shows the in-domain gain does
*not* generalize (→ scope F1 to in-domain / reconsider), or a much larger effect appears at another compression rate
(→ lean harder into Fork A).

### D017 — 2026-06-11 — Standing "thinking panel" of four reasoning-methodology subagents (post-step adversarial loop)

**Decision:** Add four reasoning-methodology subagents in `.claude/agents/` — `counter-argument`,
`socratic-thinker`, `premortem-analyst`, `first-principles-grounder` — run *after a step produces a
result/verdict* (and before that verdict lands in the ladder/docs/manuscript), as a standing
adversarial panel. The loop: run the panel → verify each objection against the raw data → address the
ones that hold → re-run until no hole survives. They are deliberately MECE against `oracle-reviewer`,
which is a *pre-compute design gate* (PASS/HOLD/KILL); the panel are *post-step analysts* of an
existing result. Model routing per Erfan's rule [**routing SUPERSEDED by D026 (2026-06-13): fable banned → these panel agents +
socratic now run on opus**]: ~~`counter-argument`/`premortem-analyst`/`first-principles-grounder` default fable~~,
`socratic-thinker` and the existing search/digest/log agents **sonnet**, mechanical fan-out **haiku**. Model declared in each
agent's `model:` frontmatter; existing agents got an explicit `model:` too.
**Rationale:** Erfan's autonomous-mode directive ("after each phase, run counter-argument and Socratic
thinker and other methods of thinking, go back and forth, verify then address until there is no hole in
our arguments"). The four lenses are non-overlapping: external attack (counter-argument), assumption
exposure (socratic), prospective-hindsight failure (premortem), foundational re-derivation against the
math/papers (first-principles). The last directly serves the "everything must be grounded" mandate by
checking claims against [`06-theory-grounding.md`](../06-theory-grounding.md), the canonical notes, and the course material.
**Reverses if:** the panel becomes ceremony that doesn't change conclusions (collapse to the one or two
lenses that earn their keep), or a single combined reviewer proves as effective at lower cost.

### D018 — 2026-06-11 — In-domain F1 reframed to Fork-B: the per-subject effect is NULL (E008); A3 is now the central contribution

**Decision (Erfan-confirmed, D015 gate):** The Q3/F1 "headline" is downgraded from 🟡 PARTIAL-PASS to a
**per-subject NULL** (averaged-target-only trend). E008 (per-participant, n=9, well-powered MDE≈+0.0006,
two-panel-adjudicated) returns mean +0.00010, t-CI [−0.0004,+0.0006], sign 5/9; the 4 subjects E005
averaged are individually null. **E005's +0.0081 was a group-averaged-target measurement** — a higher-SNR
read of the *shared stimulus-evoked response*, inflated ~1.7× by averaging (NC≈0.49 noise-ceiling math)
and ~2.4× by one outlier fold (L015/L016) — **not per-person brain alignment.** The thesis adopts the
honest **Fork B**: contribution = (1) A2 real & measurable, powered (E006); (2) a rigorous, well-powered
per-subject null + the anti-confound characterization (literature-consistent, Hadidi/Feghhi ≤10%); (3)
**A3 / E009 (does brain-tuning buy anything practical at matched perplexity)** — at the time, the central open
question and next experiment. **[UPDATE 2026-06-12: A3/E009 has since RUN → bounded NULL, null-by-construction (L017); and the per-individual null was further hardened across capacity (E011), objective (E013b), and voxelwise substrate (E013). The experimental program is now CLOSED (ladder). So (3) is no longer "open" — it is a completed null. The live contribution is the measurement-validity result + the matched-ppl/permuted-twin/per-subject protocol, with E015 giving the matched-ppl control cross-family bite.]**
**Rationale:** the S8 thinking-panel (D017) caught the pseudo-replication *before* compute; the
oracle-gated per-subject test (E008) then settled it empirically; a second panel adjudicated the
averaging-SNR steelman and rejected it on the power numbers. This supersedes D016's "F1 confirmed
in-domain (A+B synthesis)" — the A-half does not survive per-individual inference. A well-powered null
that overturns an overclaimed prior is a clean, publishable result, not a failure.
**Reverses if:** a higher-per-subject-SNR design (within-subject repeats lifting the single-subject
ceiling, or surprisal/imageability conditioned into the nuisance) reveals a per-individual brain-specific
gain above MDE — the only grounded path to a per-person positive (more averaging is not).

---

## D019 — Codex as a second-model critic + rescue; its OS sandbox disabled (container) — 2026-06-12

**Decision.** Adopt Codex (OpenAI CLI, `gpt-5.5`) as an *independent second model* for this repo, with two
jobs only: **(1)** a **code-level critic that ADDS to the thinking panel** — `/codex:adversarial-review`
or a 1–4-persona background read-only `task` panel (statistical referee · reviewer-2 skeptic ·
first-principles re-deriver · reproducibility/leakage auditor); **(2)** **rescue / second-implementation**
of analysis scripts. Default reasoning **xhigh** (reviews inherit it; delegate a `task` with
`--effort medium` for the asymmetric "medium worker / xhigh critic"). **Hard line:** Codex never produces a
science number or flips a rung — numbers come only from the `docs/` brain, verdicts only from Erfan; it
reviews code correctness and proposes implementations.
**Sandbox posture.** Codex's bubblewrap sandbox **cannot run in this Docker container** (uid-map + loopback
`Operation not permitted`; `/proc/sys` read-only; system `bubblewrap` doesn't help — L033). So the inner
sandbox is **disabled** (config `approval_policy=never`, `sandbox_mode=danger-full-access`; plugin
`codex.mjs` patched to force `danger-full-access`). The Docker container is the external boundary — the
configuration Codex's own docs sanction for externally-sandboxed envs. Safety = container + git diff review
+ the hard line, not the inner sandbox.
**Rationale.** The thinking panel attacks the *conclusion*; Codex adds the *code* layer it can't reach (it
runs the script). Verified live: Codex (xhigh) independently re-ran `reanalyze_e005_e006.py` and reproduced
the S8 panel's diagnosis — independent corroboration, not redundancy.
**Reverses / revisits if:** the host stops being a container (then re-enable the real sandbox), or a codex
plugin update overwrites the `codex.mjs` patch (reapply it — `tasks.md` carry-forward). Full mechanics:
`docs/references/codex-usage.md`.

---

## D020 — Two parallel work lanes: implementation + analysis, sharing the docs brain — 2026-06-12

**Decision.** Run the repo as **two independent queues** (D011's two session modes, now run in parallel):
an **implementation lane** (working sessions — generate new evidence) and an **analysis lane** (Erfan
studies + communicates the recorded evidence). They share the `docs/` evidence brain but do not block
each other; each session picks ONE lane. Trigger: Erfan is away ~2 days from 2026-06-12 and does not want
that compute window idle — implementation proceeds autonomously while he resumes the analysis walk on return.

**The coordination rule (makes parallel safe).** The D011 non-negotiable already separates them: analysis
may only report numbers a working session *recorded*. So working sessions **add** evidence/experiment
docs/rungs; they must **not edit the docs the analysis lane is reading** — `reports/R05`, the manuscript,
and the E005–E014 experiment records stay frozen so Erfan's study ground doesn't shift under him. Rungs
flip only on Erfan's confirmation (unchanged, D015).

**Scope guard (science honesty).** "Keep experimenting" after an Erfan-confirmed null is only legitimate as
**predeclared, kill-gated hypotheses** — not fishing to rescue a positive. The active implementation item is
the **full-FT multi-subject voxelwise door** (E013 §"two routes"), whose kill criterion is already locked
(E013 §17). Anything beyond it needs a written Claim + kill criterion before compute.

**Reverses / revisits if:** the implementation lane runs dry (only the full-FT door + E015-expansion are
real impl work today — F3/Q5 is moot pending a positive Q3), or Erfan redirects on return.

---

## D021 — TRIBE-v2 synthetic brain targets as the CAPSTONE of the implementation roadmap (E016) — 2026-06-12

**Decision.** Adopt Meta FAIR's **TRIBE v2** brain foundation model (`facebook/tribev2`; d'Ascoli et al.,
ICLR 2026) as a new implementation build (E016) — the **capstone (I4), run LAST**, after the existing
experimental train (I1 E015-expand → I2 external matched-ppl control → I3 full-FT door). *(Corrected
2026-06-12: TRIBE is the newest task at the END of the train, NOT the first; an earlier same-day draft
mis-promoted it to "primary." It sidesteps I3's data-acquisition blocker by generating its own fMRI, so it is
the natural continuation if I3 walls.)*
Rationale: TRIBE generates fMRI for *arbitrary* text, removing the data-scarcity limitation that bounded
E001→E015. **The framing that makes it rigorous (not just "more data"):** TRIBE estimates E[Y|S], the
stimulus-predictable brain response; by the Markov chain Y⊥θ*|S (R05), the non-stimulus-predictable residual
is θ*-independent noise, so **E[Y|S] is the entire training-useful brain signal → TRIBE is an UPPER BOUND on
the utility of brain-guided LM training.** A null at the ceiling = strongest Fork-B with a clean DPI mechanism;
a positive = Fork-A reopens. Either outcome is publishable (the ceiling argument makes the null informative).

**Program (kill-gated, E016 §5):** P0 run TRIBE text-only · P1 fidelity (TRIBE faithful in our pipeline?) ·
P2 ceiling (stimulus-subtraction on real LeBel — cheapest decisive) · P3 scaled matched-ppl distillation.

**Env isolation (verified, answers "why not just install it").** TRIBE hard-pins torch>=2.5.1,<2.7 and
numpy==2.2.6; the thesis env runs torch **2.11.0+cu128** and numpy **2.4.6**. Installing TRIBE into the thesis
venv would downgrade torch (losing the cu128 GPU build) and numpy, breaking the experiment scripts we still
need (E006 harness, distill.py, …). So TRIBE lives in an **isolated venv** (`.venv-tribe`) and hands off via
disk (writes synthetic-BOLD .npy; our pipeline reads them). Confirmed install + import PASS 2026-06-12.

**Hard line (unchanged).** TRIBE is a *tool* (a denoised stimulus→brain oracle), not an adjudicator: it produces
no science number that flips a rung; verdicts are Erfan's, numbers come from the docs brain.
**Reverses / revisits if:** P0 walls (TRIBE unrunnable here) or P1 fails (TRIBE not a faithful fMRI stand-in)
→ fall back to the full-FT door (E013) or E015-expansion.

---

## D022 — The dual meta-goal: MSc thesis AND ≥1 top-venue AI paper — 2026-06-12

**Decision.** The repo's objective is explicitly **two-fold**: (1) complete Erfan's MSc thesis (UC3M, ML for
Health), and (2) extract **at least one top-venue AI publication** (ICML / ICLR / NeurIPS / AAAI-class) from
the work. (2) raises the bar on every implementation step: senior-researcher rigor, everything grounded in the
papers (`docs/literature/`, `data/papers`, `data/paper-repos`) and the course material ([`06-theory-grounding.md`](../06-theory-grounding.md)
+ `data/course-material`), and the *idea is not holy text* — it stays dynamic, refocused toward the genuine
under-researched literature gap as evidence accumulates.

**How it changes operating posture (not the science bar — that was always rigorous).** The implementation lane
runs as an **ordered roadmap** (I1→I4, TRIBE capstone last; `tasks.md`), and after **every** step/verdict the
**thinking panel** (D017: counter-argument · socratic-thinker · premortem-analyst · first-principles-grounder)
**+ the Codex code-critic** (D019) run as a continuous counter-critique loop — *verify each objection against the
data, address the ones that hold, re-run until no hole survives* — before any verdict lands in the ladder/docs/
manuscript. Subagents are used liberally [**model routing SUPERSEDED by D026: the panel + lit-scout/paper-digest
run on opus (thinking/analysis), doc-navigation/record on sonnet, mechanical fan-out on haiku — fable is banned**].
gbrain is read/written continuously.

**The hard line stays:** no rung flips without Erfan; numbers come only from runs recorded in the docs brain;
strategic framing calls (e.g. whether I2's external matched-ppl result becomes the paper's headline/spine) wait
for Erfan. Autonomy is bounded by the last explicit human instruction (L031).

## D023 — Cross-family LM-quality is measured in BITS-PER-BYTE, not per-token perplexity — 2026-06-13

**Decision.** For any *cross-family / cross-tokenizer* comparison of LM quality (the x-axis of the alignment∝−quality
law, the matched-ppl control), use **bits-per-byte** (total NLL in bits ÷ UTF-8 bytes of a fixed natural-text
probe; no-prepend, first-token unscored — the Pile/GPT-3 convention), **never per-token perplexity.**

**Why (oracle gate, fable, I1).** Per-token NLL is not comparable across tokenizers: vocab sizes span ~32k
(Mistral) → 50k (gpt2/OPT/pythia) → 128k (Llama) → 151k (Qwen), and **vocab correlates with family**, so per-token
ppl injects a family-correlated nuisance straight into the x-axis — fatal for the architecture-residual question
(Q2). For a fixed probe, cross-model Δbpb = ΔKL = a pure quality difference. bpb is also **absent from the
brain-alignment scaling literature** (lit-scout) → a small methodological contribution, not just hygiene. Episode:
an eos-prepend (an over-eager BOS-consistency fix) poisoned Qwen2.5-3B's scoring (ppl 105 vs healthy 32.6),
dragging the pooled r from −0.78 to −0.63 — caught by sibling-monotonicity. **Consequence:** E015's rigorous
cross-family law is **r≈−0.78** (bpb, 6 families), not the inflated −0.92 (per-token + best-layer + 3-family).
The manuscript's cited −0.92 needs an analysis-lane correction (Erfan's edit). See L034.

## D024 — The brain-guided induction lever fails METHOD-GENERALLY; I2's matched-ppl contribution is banked in E009+E015 (not a new external reproduction) — 2026-06-13

**Decision.** Stop treating "reproduce an external brain-tuning gain and control it" as an open build. The
matched-perplexity control that the brain-tuning literature lacks (Negi/Schwartz/Moussa compare only to a vanilla
baseline) is **already supplied** by the repo: **E009** (downstream matched-ppl + permuted-twin, bounded null) +
**E015/I1** (the cross-family quality→alignment law). Negi's *literal* pipeline is infeasible here (no Chen-2024b
bilingual fMRI). I2/E017 was therefore reframed (oracle HOLD) into a **full-FT feasibility gate** on LeBel.

**The finding that closes the door.** Full fine-tuning — the last untested *induction method* — fails to induce a
brain-specific alignment gain at matched perplexity: **real−permuted gap +0.0003, 95% CI [−0.0002,+0.0008], p=0.27**
(UTS01/02/03 × 3 seeds, ppl-preserving). The lever now fails across **parameterization (LoRA/full-FT), objective
(MSE/contrastive), and capacity** (E017 + E013 + E011 + E013b + E008) → a **method-general mechanism failure**, not
a tuning detail. **Fork-B is robust.** The only induction variants still untested: n≥5 multi-subject naturalistic
(I3, denizenslab — data-blocked) and TRIBE-synthetic targets (I4). Not a Fork-A surprise → no Erfan stop fired.
**Erfan's open call (unchanged):** whether E009+E015+E017 (matched-ppl as the field's missing control) becomes a
manuscript headline/emphasis. See L036.

## D025 — The forward research program (the corpus continuing the path) — 2026-06-13

**Decision (Erfan-approved, "100% / finish-the-job, not 99%" rule).** With I1✅+I2✅ done, I4-P0✅ passed, and the
I3 dataset✅ downloaded, the path forward is a sequenced, kill-gated **research corpus** (built by the S12 planning
swarm — 4 lenses + Codex + lit-landscape). Full table in `ladder.md` → "THE FORWARD PROGRAM". Sequence by value/cost:

> ⚠️ **SUPERSEDED IN PART by D028 (2026-06-14):** F1 Phase 1 = PASS; the TRIBE Phase-2 *stimulus-subtraction*
> ceiling walled out (artifact, not Fork-A) and is RETIRED. The F1-next step is now **E020** (empirical-E[Y|S]
> ceiling, TRIBE-free); TRIBE → Phase 3 only. New order: F1-close(E020) → F2 → F3 → F4. See D028.

- **F1 (next): E016 TRIBE Phase 1→2 — the information-theoretic CEILING.** Prereq: the **voxel-space mapping**
  (LeBel-volumetric ↔ TRIBE fsaverage5 — the real blocker per Codex). Phase 1 fidelity = **spatial-specificity**
  (the naive trained>untrained check is circular). Phase 2 = real−TRIBE residual **with a REQUIRED no-text-extractor
  ablation** (TRIBE's text extractor is Llama-3.2-3B → residual≈0 only counts if it holds vs no-text TRIBE; else
  it's Llama-shared-variance, not the DPI ceiling). residual>0 surviving no-text ⇒ Fork-A → STOP for Erfan.
- **F2: E019 external reproduce-and-control** — reproduce a published brain-tuning POSITIVE (Bilgin/Negi/Moussa
  recipe on LeBel/denizenslab) then collapse it with matched-ppl + permuted-twin. **The 100% version of I2; the
  premortem calls it non-negotiable for the paper** (E009/E017 are our own nulls, not a demonstration that a
  *published* positive vanishes). Headline/spine framing remains Erfan's call when the number lands.
- **F3: E013/I3 denizenslab n=6 full-FT** — the POWERED multi-subject induction test (data downloaded; 100% rule:
  close the induction question at adequate power, not the n=3 existence probe). Likely-null per 5 converging nulls.
- **F4: E015 Q2 architecture-residual extension** — ≥3 modern-family sizes + base-vs-instruct ablation; claim or bury.
- **A (analysis lane, Erfan):** the manuscript corrections (r≈−0.92→−0.78 via the 3-part argument; Y⊥θ*|S as an
  assumption; narrow the matched-ppl framing pending F2).
**The unifying spine (the paper):** *the brain's training-useful signal is its stimulus-predictable part E[Y|S];
beyond it, by Y⊥θ\*|S, the response is task-independent noise* — unifying the averaging confound + the matched-ppl
quality law + the method-general induction null + the TRIBE ceiling. The 3 framings (missing-control / TRIBE-ceiling
/ bpb-axis) are a HIERARCHY, not alternatives: missing-control = deliverable, bpb-law = mechanism, ceiling = closure.
**Hard line unchanged:** no rung flips without Erfan; numbers only from recorded runs; Fork-A surprise → STOP.

## D026 — fable model banned/removed; subagent routing = opus(think)/sonnet(doc-nav)/haiku(mechanical) — 2026-06-13

**Decision (Erfan, 2026-06-13).** The `fable` model no longer exists (banned) — it errored mid-session
("claude-fable-5 may not exist"). **New routing rule: anything that needs THINKING / ANALYSIS / DESIGN → opus;**
navigating OUR docs (status review, fact-finding across traces, record-writing) → sonnet; simpler mechanical
fan-out → haiku. Applied: the thinking panel (`counter-argument`, `socratic-thinker`, `premortem-analyst`,
`first-principles-grounder`), `oracle-reviewer`, AND `lit-scout` + `paper-digest` (relevance-judging / paper-
synthesis is analysis, not retrieval — Erfan's correction) → **opus**; `session-logger` → sonnet. All 8 agent
frontmatter + CLAUDE.md tables/routing + upspeed updated; historical "(fable)" annotations in timeline/learnings/
ladder left as accurate records of past runs. Supersedes the prior "fable for hard adversarial work" rule.

## D027 — F1/F2 substrate = denizenslab (turnkey voxel→fsaverage5 mapper); LeBel deferred — 2026-06-14

**Decision (autonomous, S13; oracle-gated; flagged for Erfan).** The F1 voxel-space blocker (TRIBE fsaverage5
surface ↔ real BOLD voxels) is resolved by using **denizenslab** (Deniz 2019) as the F1/F2 substrate instead of
LeBel. Reason — "look for an existing transform before building one" (the goal's own instruction): LeBel ds003020
ships only a `pycortex-db/` + `freesurfer_subjdir/` (no precomputed mapper → would need a full pycortex+FreeSurfer
build to reach fsaverage). **denizenslab ships the existing transform**: per-subject sparse `voxel_to_fsaverage`
CSR mappers (327684×n_vox), local and verified, **plus per-subject functional ROI localizers** (V1–V4/AC/Broca/
pSTS/FFA/EBA/…) in the *same* voxel space → the language-high/visual-low labels Phase-1 needs, for free, at **n=6**
(vs LeBel n=3). fsaverage5 is the verified sphere-prefix of fsaverage (nilearn sphere coords, max diff 0), so
fsa5 = a direct 20,484-column subset. It is also the F3 dataset → the loader/adapter built here compounds into F3.

`scripts/fsaverage_mapping.py` implements + verifies the bridge: fsa5⊂fsa prefix (diff 0), 93% fsa5 coverage, and
the validating sanity check that **listening split-half reliability lands in lang/aud ROIs (0.108) ≫ early-visual
(0.026)** — correct spatial pattern. This is a methods choice within F1 (not a rung flip / Fork-A / E019 framing),
so taken autonomously per the 100% rule; **deviates from the literal "LeBel" instruction** — Erfan may redirect to
also run LeBel via its pycortex-db on return (kept as an optional robustness substrate). No science number changes.

## D028 — TRIBE-ceiling reframe: empirical E[Y|S] is the right instrument; TRIBE reserved for Phase 3; F2 prioritized — 2026-06-14 (Erfan-agreed)

**Decision (S13, Erfan-agreed).** The F1 Phase-2 TRIBE *stimulus-subtraction* ceiling hit a methodological wall:
TRIBE explains only ~7% of per-vertex real-BOLD variance on story-listening (LM→TRIBE≈0.03 vs LM→real≈0.18), so it
is too weak to subtract; the runner's "Fork-A" flag was a CONFIRMED ARTIFACT of that weakness (caught by the
predeclared vacuity gate, NOT escalated — E016 Step 9, L038). The reframe separates the two questions TRIBE was
conflating and routes each to the right instrument:

1. **The ceiling question** ("is there LM-alignable brain signal beyond the stimulus-predictable E[Y|S]?") is
   answered with the **GROUND-TRUTH empirical E[Y|S]** = the cross-subject (+cross-repeat) average of real fMRI,
   which *is* the stimulus-evoked expectation by definition and is strictly stronger than TRIBE's model estimate on
   data where many subjects heard the same stimulus (denizenslab: 6 subjects, story_11 has 2 repeats). → **new
   experiment E020** (TRIBE-free). This is the rigorous closure; it is close to E008 (per-individual null) + L016
   (averaging confound) — its value is stating the ceiling cleanly as a spine result, not a brand-new finding.
2. **TRIBE's irreplaceable role is NOT the ceiling — it is Phase 3** (dense synthetic brain targets for the *real
   KD training corpus*, where no real fMRI exists and empirical averaging is impossible). Phase 1 already validated
   TRIBE is faithful enough to BE such a target (Δ+0.113 over a strong floor). Phase 3 = a strong OPTIONAL Fork-B
   booster (a null at scale removes the scarcity/SNR excuse), not a blocker.

**Reorder (new forward-program sequence):** **F1-close = E020 empirical-E[Y|S] ceiling (NEXT, cheap, TRIBE-free)**
→ **F2 = E019 external reproduce-and-control (paper-critical; the premortem's NON-NEGOTIABLE)** → **F3 = I3
denizenslab n=6 full-FT** → **F4 = E015 Q2**. **TRIBE Phase 3** = optional booster, slot after F2 if pursued.
Rationale: the TRIBE stimulus-subtraction was the weak, partly-redundant rung; the paper's actual unfilled gap is
F2 (showing a *published* positive collapses under matched-ppl+permuted), which needs no TRIBE fidelity. Do NOT
sink effort into per-subject-fine-tuned TRIBE or switch to video (abandons the language-LM↔language-fMRI substrate).
**Hard lines unchanged:** no rung flips without Erfan; numbers only from recorded runs; a Fork-A SURVIVING the
controls → STOP; E019 headline/spine framing is Erfan's call.

## D029 — E020 hardened after oracle HOLD: ratio claim (A_resid≪A_shared), repeat-split, story-as-replication-unit, power-gate-first — 2026-06-14 (S14, autonomous)

**Decision (S14, autonomous, oracle-gated).** The locked E020 skeleton (D028) passed the *idea* but the oracle gate
returned **HOLD** on the *implementation* — three fatal gaps that would have manufactured a false verdict. Hardened
to v2 (`docs/experiments/E020_*.md` §v2) before any compute:
1. **Claim reframed to a RATIO, not a femto-null.** A_resid is expected at +0.0001–+0.001; a femto-precise null is
   unachievable at n=6/~3 stories and unnecessary. The defensible claim is **A_resid ≪ A_shared** (A_shared =
   LM→E[Y|S] ≈ 0.355 NC-norm in higher-language, S13). Primary statistic ρ = A_resid/A_shared with a bound; ρ≲6%
   ⇒ >94% of LM brain-alignment is to the stimulus-predictable part ⇒ Fork-B, informatively.
2. **G1 repeat-split (story_11's 2 repeats):** stop collapsing both into one mean (the old `load_real` does), which
   left ε's noise ceiling uncomputable. Use repeat-1 for E[Y|S]/ε; validate against repeat-2 (leave-repeat-out + ε NC).
3. **G2 reference-reliability gate:** the 5-subject LOO mean E[Y|S]_{-s} carries ~17% noise that can spuriously
   zero-out A_resid; jackknife its reliability and gate on it (L038 applied to the reference's stability).
4. **G3 story = replication unit, coded:** run ≥3 stories (story_11 + train 01–10), across-story test hard-coded in
   the runner; the printed MDE is the across-story MDE, not untrained-seed spread.
5. **Confounds:** C1 add the strong eng1000 nuisance floor as a *second* floor (L035 — trained−untrained alone
   under-controls the lexical-semantic stimulus-locked path); C2 fold-boundary gaps; C3 lag fit on the LOO mean only;
   C4 off-story = point-estimate only (no NC bound).
6. **Power-gate FIRST (cheapest decisive):** measure the across-story MDE empirically before committing to the full
   verdict. **KILL branch:** if the across-story MDE exceeds the largest plausible non-stimulus signal, concede the
   ceiling as **bounded-not-closed** (honest L021 move) and go straight to F2 (E019), which does not depend on this
   residual. Do not spend a fourth compute cycle below the instrument floor.

**Hard lines unchanged:** all four Fork-A gates coded in the runner (matching the TRIBE-false-Fork-A discipline);
no rung flip without Erfan; a Fork-A surviving all controls → STOP. This is an implementation hardening of D028, not
a change of direction.

## D030 — E020 verdict: NO Fork-A; ceiling bounded-not-closed; invoke KILL → F2 (E019); spine re-anchored on E008-convergence — 2026-06-14 (S14, autonomous, panel-survived)

**Decision (S14, autonomous; oracle + socratic + first-principles + counter-argument + premortem all run).** E020
stage-1 (story_11, n=6, Qwen2.5-0.5B L12) ran. The naive flag fired (A_resid LM→ε = +0.090, ρ vs A_shared 0.51) but
the diagnostics prove it a **confirmed ARTIFACT, NOT Fork-A** (leaked stimulus through a too-noisy n=5 reference +
HRF autocorrelation, both controlled away → gapped+partialled trained−untrained gap = −0.018 ≈ 0). The panel caught
that the eng1000 nuisance-partial is **partly vacuous** (symmetric partial collapses A_shared +0.176→+0.033 too), and
that the instrument is in the predeclared **KILL regime** (LOO reference reliability 0.33, ε split-half NC 0.17).
**Verdict:**
1. **No Fork-A → nothing escalates to Erfan** (the Fork-A guard worked, as designed; same discipline that caught the
   TRIBE false Fork-A — L038/L040).
2. **Ceiling BOUNDED-NOT-CLOSED, not closed.** E020 is the SECOND ceiling instrument to wall at n=6 denizenslab
   (after TRIBE) — the empirical E[Y|S] reference is too noisy to interpret a residual; more stories can't fix it
   (subject-count limit). Per the oracle KILL branch: concede bounded-not-closed, **do not spend a fourth compute
   cycle below the instrument floor.**
3. **Spine re-anchored.** The universal Fork-B ("the brain's training-useful signal IS its stimulus-predictable part")
   rests on the POWERED per-individual nulls **E008/E011/E017** — NOT on the ceiling experiments. E020 is demoted to
   **convergent corroboration + a successful Fork-A guard + the mechanism** (no non-stimulus residual signal for a
   shared stimulus rep to grab). L039/L040.
4. **Next compute = F2 (E019 external reproduce-and-control)** — paper-critical (premortem NON-NEGOTIABLE),
   ceiling-independent, needs no TRIBE/E[Y|S]. Forward order now: ~~F1-close(E020)~~ **F1-close DONE (bounded) → F2
   (NEXT) → F3 (I3 n=6 full-FT) → F4 (E015 Q2).**
5. **No rung flip.** Q3/F1 stays ❌ (robust per-individual null). The manuscript framing of E020 (how/whether to
   present the bounded ceiling) is an **analysis-lane / Erfan call** — flagged, not edited.

**Hard lines unchanged:** numbers only from recorded runs (above, in `outputs/E020_eys/`); no rung flips without
Erfan; ladder "next session" block updated to F2 but rung statuses untouched pending Erfan.

## D031 — E019 substrate moved denizenslab → LeBel; design hardened to run-ready after oracle HOLD; faithful-Negi-head = fresh-launch build — 2026-06-14 (S14, autonomous, oracle-gated)

**Decision (S14, autonomous; first-principles design-grounding + oracle gate).** E019 (the paper-critical external
reproduce-and-control) was grounded, locked (v2), and oracle-gated. The oracle returned **HOLD** with three fatal gaps;
all addressed in E019 v3. The load-bearing changes:
1. **Substrate: denizenslab → LeBel UTS01/02/03.** denizenslab was chosen (D027) ONLY for TRIBE's voxel→fsaverage5
   mapper, which E019 doesn't need; it has walled TWICE at n=6 (TRIBE L038, E020 L040) and only story_11 carries a noise
   ceiling. **LeBel is the proven-reliable substrate**: deep single-subjects, a multi-repeat held-out story for NC,
   powered voxelwise A2 (E006), full-FT infra already run there (E017), and Negi's own monolingual control uses LeBel.
   This resolves the oracle's F2 (replication/NC) + F3 (power). **This narrows D027 to "denizenslab for TRIBE-dependent
   F1 work only"; E019/F2 runs on LeBel.**
2. **Target = reproduce Negi-2025's ENCODING gain (tuned−vanilla, ppl-unanchored)** — a different, easier contrast than
   E017's (real−permuted) null, so it should reproduce; then dissect with arm (c) bpb-matched generic-text FT + arm (d)
   permuted twin. Primary outcome = held-out encoding Δr.
3. **F1 (the real build): a FAITHFUL Negi head** — differentiable Lanczos+FIR+NT-Xent, NOT the `run_lebel_tune.py`
   per-segment-mean readout (which L026/L027 proved degrades alignment — using it would strawman Negi). This is a
   fresh-session build (L031; the L037 timing-bug surface — do not rush at a session tail).
4. **Power gate FIRST (step 0, cheap):** encoding-Δr MDE on LeBel's held-out story; KILL if MDE > the reproduced gain.
5. **Confounds coded:** bpb-match validity check on arm (c); the L040 **symmetric-partial + permuted-eng1000** controls
   on the nuisance partial; identical optimization + manip-check on the permuted twin.

**Status:** E019 RUN-READY pending the power gate + the faithful-head build. **Headline/spine framing remains Erfan's
call when the number lands** (per the E019 doc). No rung flips. Forward order: F1-close DONE (bounded) → **F2/E019
(NEXT, on LeBel)** → F3 (I3) → F4 (E015 Q2).

## D032 — E019 verdict: corroboration not clincher; "NON-NEGOTIABLE" framing retired; spine rests on the powered nulls; do NOT build the BERT port — 2026-06-14 (S14, autonomous, panel+positive-control-survived)

**Decision (S14, autonomous; counter-argument + premortem + an eval positive-control all run).** The faithful Negi
head (differentiable Lanczos+FIR+NT-Xent full-FT, Lanczos verified) on LeBel UTS01/02/03 produced **no positive
encoding gain at any lr** (gentle gain_r −0.0006±0.0027 n=9; sweep 2e-5/3e-5/5e-5 monotone-negative; 1e-4 catastrophic).
The first read ("Negi's gain doesn't reproduce") was **over-claimed** and the panel demolished it:
1. **The raw-mean-r encoding ruler is quality-INSENSITIVE** — eval positive-control: enc_r for Qwen2.5-0.5B/1.5B/3B =
   +0.150/+0.147/+0.143 (flat-decreasing), so the metric can't register the quality-driven alignment differences E015
   found. A "no enc_r gain" claim is confounded by a partly-blind ruler. (The unique-R² metric IS E006-validated; its
   null gain_u −0.0001 is real, but the gentle regime barely moved the LM (Δppl≈0) ⇒ "no manipulation," not "no gain.")
2. **Faithfulness gaps** (Qwen decoder vs Negi's BERT encoder; window-TR vs batch NT-Xent; 2 vs 30 epochs; monolingual
   vs bilingual) make any claim about *Negi* a category error.
3. **Do NOT build the faithful BERT port** — multi-day, off-thesis-target, and a surviving reproduction = Fork-A that
   could CONTRADICT the spine. Highest-risk/lowest-leverage to rescue an already-demoted leg.
**Verdict:** E019 establishes the SCOPED claim — *"on a faithful-as-feasible Negi-head + 0.5B decoder, no full-FT
regime induces a brain-specific alignment gain (gentle = no movement, stronger = catastrophic forgetting), converging
with the E008/E011/E017 method-general lever failure (L036), now on the Negi head."* **E019 = CORROBORATION, not the
external clincher. The stale v1 "NON-NEGOTIABLE" framing is RETIRED (L041/L042): the paper's spine rests on the POWERED
per-individual nulls (E008/E011/E017) + E015 + the (bounded) E020 ceiling.** No rung flip; no Fork-A. Forward order:
F1-close DONE → F2 DONE (corroboration) → **F3 (I3 denizenslab n=6 full-FT, NEXT) → F4 (E015 Q2).** Framing = Erfan's call.

## D033 — Forward-program decisive work COMPLETE; F3 (denizenslab n=6 full-FT) superseded/moot; F4 = analysis-lane — 2026-06-14 (S14, autonomous)

**Decision (S14, autonomous; grounded in this session's results + the panels).** With F1-close (E020, bounded
ceiling) and F2 (E019, corroboration) DONE, the implementation lane's **decisive** forward-program work is complete.
Assessment of the remaining items:
- **F3 (I3 = denizenslab n=6 full-FT induction) is SUPERSEDED / moot, not worth the compute.** The powered full-FT
  induction null is ALREADY in hand: **E017** ran full fine-tuning on LeBel (UTS01/02/03 × 3 seeds, ppl-preserving) →
  null (gap +0.0003, CI [−0.0002,+0.0008], p=0.27, L036), and **E019** just corroborated it on the faithful Negi head.
  denizenslab n=6 is reliability-walled (E020/TRIBE: ref-rel 0.33) AND its raw-mean-r ruler is quality-insensitive
  (S14 eval positive-control: enc_r 0.5B+0.150≈3B+0.143) — so F3 would be a LESS-powered, blind-ruler, walled-substrate
  repeat of an already-decided verdict. Marginal decision value ≈ 0 at multi-hour cost. **Run ONLY if Erfan wants
  literal 100%-rule coverage; otherwise skip.** (Not a science change — the induction null is powered + corroborated.)
- **F4 (E015 Q2 architecture-residual extension) = analysis-lane** (add Llama/Mistral sizes to the bpb law; underpowered
  hypothesis, p=0.20). An extension of the recorded law, best done in the analysis lane, not a decisive rung.
**The spine, fully supported by POWERED evidence (no new compute needed):** A2 real (E006) · per-individual induction
NULL robust across LoRA/full-FT/objective/capacity (E008 powered + E011/E013/E013b/E017) · averaging confound (L016) ·
bounded E[Y|S] ceiling (E020) · cross-family bpb law (E015, r≈−0.78) · E019 corroboration. **Refocused headline (L041):**
"brain-tuning gains are an LM-quality/FT-regime artifact, not per-individual brain signal — the missing controls + the
powered per-individual null where averaging manufactures specificity + the stimulus-predictability (E[Y|S]) ceiling."
**The remaining high-value work is ANALYSIS-LANE (Erfan):** the scope correction (operational claim; Y⊥θ\*|S as
assumption; the unmeasured DPI selection side-channel — L041), the manuscript reframe, the lit positioning (Jia-L-PACT,
Raugel, Hadidi→Nature-Comms), and figures. No rung flips without Erfan.

## D034 — E020-on-LeBel ceiling-closure KILLED (oracle + mapper blocker); the E[Y|S] ceiling is instrument-limited on ALL substrates → rests as bounded corroboration — 2026-06-14 (S14, autonomous, oracle-gated)

**Decision (S14, autonomous; oracle KILL + a data-fact check).** Considered re-running the E020 empirical-E[Y|S]
ceiling on LeBel UTS01/02/03 (10-repeat NC story → far more reliable per-subject responses) to convert the denizenslab
"bounded-not-closed" into a clean closure. **KILLED before compute, on two independent grounds:**
1. **Reference-reliability arithmetic (oracle, quantitative):** LeBel n=3 → the leave-one-subject-out reference has only
   **n_ref=2 subjects**, so its cross-subject reliability is capped by the between-subject shared fraction and is
   *lower* than denizenslab's n=5 (predicted 0.28–0.42 vs denizenslab's measured 0.33). The 10-repeat advantage buys
   per-subject self-reliability, but the binding constraint is the 2-subject mean — LeBel would be the THIRD walled
   instrument, worse not better. (The real lever would be acquiring ≥3 MORE deep LeBel subjects with the 10-rep story —
   a data-acquisition decision, not a re-run.)
2. **No cross-subject mapper (data fact):** LeBel is native-voxel (E006 was within-subject); it ships NO fsaverage/
   cross-subject surface mapper (grep empty; `load_response` returns native voxels). Cross-subject E[Y|S] isn't buildable
   without the pycortex/FreeSurfer surface build that D027 explicitly avoided by choosing denizenslab for F1.
Also: even a clean A_resid≈0 would be a tighter bound on a near-tautology (A_resid≈0 by construction, L039), not new
evidence. **Conclusion: the E[Y|S] ceiling is FUNDAMENTALLY instrument-limited on all available substrates** (TRIBE:
weak E[Y|S] ~7% var, L038; denizenslab n=6: ref-rel 0.33, L040; LeBel n=3: worse + no mapper, this entry). **It rests as
a BOUNDED corroboration; the spine rests on the powered per-individual nulls (E008/E011/E017) + E015 + L016.** No rung flip.

**Implementation-lane status (final, verified):** every remaining forward-program door is closed or moot, each verified
— F1-close ceiling (instrument-limited, bounded; this entry + D030), F2 reproduction (corroboration, D032), F3
(superseded, D033), F4 (analysis-lane), the DPI selection-channel (null-by-construction: matched-ppl brain-tuning doesn't
move the representation, so no manifold-point selection is possible — E009/E019-gentle). **The decisive implementation
science is COMPLETE; the spine is fully supported by powered evidence; remaining work is the ANALYSIS lane (Erfan).**

## D035 — Three-layer written-deliverable model (reports → extended → public) + the scientific-writing skill — 2026-06-15 (Erfan-approved)

**Decision.** All written output flows through three layers, governed by one fat `scientific-writing` skill (`.claude/skills/scientific-writing/`). Full spec in [`docs/03-methodology.md`](../03-methodology.md) "Deliverable layers"; short pointer in `docs/references/scientific-writing.md`.

- **Reports** (`docs/reports/*.md`, Markdown): the **continuous** single-topic synthesis layer, written and iterated as work happens in both session modes. Markdown because it is the agent's search surface — a grep test on real repo files settled it (md returns whole-paragraph matches; an edit cannot break a build).
- **Extended manuscript** (`docs/manuscript/extended/`, LaTeX): the internal, supervisor-facing master. Hybrid structure = an always-current paper body (compresses cleanly into a public cut) plus an append-only dated checkpoint log. Updated **only at a checkpoint Erfan calls**.
- **Public manuscript** (`docs/manuscript/public/vN/`, LaTeX): frozen versioned cuts, derived by **compression** from the extended manuscript + reports, only at a submission/share milestone. A `vN` vendors its own preamble and bib so it stays frozen.

Knowledge flows **down only** (evidence → report → extended → public); a number never enters at a lower layer than where it was recorded. D011 holds in all three.

**The skill enforces (capabilities C1–C6, panel-hardened over two adversarial critique rounds informed by the skill-creator standard):** anti-AI-tell scientific voice (deterministic `ai_tell_lint` + a judgment review pass), graded hedging tied to measured-vs-correlational, the `\evd`/`\gap` D011 provenance discipline, deterministic verifiers (`run_checks.py` dispatches evd-resolution / gap-survival / number-consistency / claim-survival per layer), silent-fix drafting, and a Devil's-Advocate review pass. Patterns were adapted (not imported wholesale) from the `academic-research-skills` framework, cloned read-only to `data/reference-repos/academic-research-skills/`.

## D036 — Rung labels renamed L→Q in execution order; the naming convention + `map.md`; codes never enter the public manuscript — 2026-06-15 (Erfan-approved)

**Decision.** The scientific-ladder rungs are renamed from `L` to `Q` and renumbered into execution (climb) order. The old `L` collided with learning IDs (`L001–L043`) and ran out of execution order (L2a before L1). Mapping: `L0→Q0` (signal real, A2) · `L2a→Q1` (KD-preservation gate) · `L1→Q2` (the lever) · `L3→Q3` (headline, F1) · `L2b→Q4` (practical payoff, A3) · `L4→Q5` (fMRI-free proxy). Climb order is now `Q0→Q5`.

**The naming convention (canonical, in `docs/map.md` + `CLAUDE.md`):**
- **Stable artifacts keep flat, immutable, chronological IDs** — `E`nnn (experiment), `D`nnn (decision), `L`nnn (learning), `A`1–A3 (assumption). They are like issue numbers: never renumbered when interpretation shifts, and one experiment may serve several rungs (the structure is a DAG, not a tree — which is *why* fusing identity with ladder-position via hierarchical IDs like `E0.1` was rejected).
- **The ladder is a separate hierarchical view**: rungs are `Q`n, the only rung vocabulary. "Layer N" is retired as a rung synonym (kept historically in R03/R04 with a mapping note; in the tutoring checklist it means a *teaching chapter*, not a rung).
- Not rungs, left untouched: transformer layers (`L7`/`L12`), `L2`/`L∞` norms, lecture numbers, `λ`/`L_brain`/`L²`.

**Manuscript rule (enforced by the `scientific-writing` skill).** Codes are internal scaffolding. Reports use them freely; the extended manuscript uses a code only as a parenthetical pointer; the **public manuscript carries zero codes** — pure prose, so a reviewer never needs the repo to parse the paper.

**Why no new skill.** A naming convention is an always-in-effect rule, not a triggered procedure, so it lives in `CLAUDE.md` (always read) + `docs/map.md` (the canonical reference); the manuscript code-usage rule lives in the existing `scientific-writing` skill. A separate skill would lazy-load a rule that must always hold. (Ties D035.)

**Execution.** Repo-wide relabel via a folder-by-folder subagent swarm with an exact mapping contract + guardrails; verified clean (learnings count unchanged at 579; norms / λ / layers / lecture numbers untouched). Timeline logs stay immutable (old `L`; `map.md` carries the L↔Q table). No science, number, or verdict changed — a labeling decision only.

**Why three.** Each layer has a different cadence and reader, and collapsing them is what rots a write-up: a paper edited continuously drifts from the evidence; a narrative touched only at submission goes stale. Reports stay cheap and searchable; the extended stays deep and current; public cuts stay frozen and venue-grade. **The behavioral rule for the agent: reports are the continuous write-layer; the extended and public manuscripts are checkpoint-derived only on Erfan's explicit call, never auto-updated.** (Supersedes the old "paper and report are the same document" framing in the manuscript README.)

## D037 — Harden the `scientific-writing` skill from the R06 clarity audit — 2026-06-16 (S18, Erfan-approved)

**Decision.** A four-lens thinking panel (counter-argument + first-principles-grounder + socratic-thinker + premortem-analyst, opus) audited every clarity/accuracy rewrite Erfan drove on R06, against the skill, to decide whether the misses were skill **design** or agent **execution**. Verdict: mostly design. Applied (commit `0647188`): (1) amended the **Clarity Test** to two halves — necessity (delete-able?) *and* sufficiency (parse-able on first read?), and fixed the "invest" nudge from *pack more* to *unpack into one-hop steps*; (2) added a **reader-comprehension floor** — define-on-first-use (audience-graded by layer), a one-clause rationale-or-`\gap` on every non-obvious method choice, a table for any ≥3-number comparison, and a formula-vs-prose decision rule; (3) made path selection a **deliberate user interview** (roadmap + cost of each path) with a hard boundary that the extended manuscript / supervisor-facing work always takes the full loop; (4) made the **review pass non-skippable** for manuscript-bound work; (5) added **consolidation guards** (notation-collision, document-wide glossary, rationale-survival) for the report→extended fold; (6) added a **number-freshness** obligation (a cite must resolve *and* still match the current record); (7) **neutralized the biasing worked example** (it had taught the L045 "exactly the partial" error — an example illustrates the move, never asserts a liftable fact). Plus an upstream methodology non-negotiable: record the why of a design choice at choice-time (so the writing layer can cite it, never invent it).

**Why.** The skill enforced anti-AI-tells and provenance mechanically but left reader comprehension to a single necessity-only test, and its own example reproduced a known error. These are design gaps a competent agent following the skill would still hit. Hardening before the extended manuscript is written stops the manuscript repeating R06's rework. (L046.)

## D038 — Build the scaled swarm-wrap system — 2026-06-16 (S18, Erfan-approved)

**Decision.** `/wrap` now scales to the session. A **SessionStart hook** (`.claude/hooks/wrap_session_snapshot.py`) records `{start_sha, transcript_path, session_id}` per worktree to a gitignored `.claude/state/wrap/start.json`, giving `/wrap` an exact changeset (`git diff start..HEAD`) and the authoritative transcript path without mtime-guessing. A **trivial** session closes inline (Part A+B). A **heavy** session (multiple docs, or ladder/experiments/reports/manuscript/skill/decisions/learnings touched) fans out five read-only **`wrap-auditor`** agents in parallel (one per scope: ladder-integrity, number-provenance, continuity-docs, records-completeness, git-and-artifacts), then the orchestrator is the **single writer**, verifying each finding before applying and committing atomically per scope. Auditors never write and never flip a rung; flips stay `REQUIRES-ERFAN` (D015); the brain mirror stays with the orchestrator.

**Why.** Self-review by the agent that did the work is the weakest review; an independent parallel audit over the git changeset catches doc drift the self-summary rationalizes (the D036/S16 stale-board failure, L044). Fan-out-read then single-write avoids parallel writes clobbering shared docs. Model routing follows the global rule: auditors default sonnet (the opus orchestrator is the reasoning backstop), `ladder-integrity` escalates to opus only when a real experiment ran. First-run-tested on this session.

## D039 — No `git add` guard hook — 2026-06-16 (S18)

**Decision.** Declined a PreToolUse/commit hook that blocks or warns on `git add -A`/`.`. The scoped-staging norm lives in D007 + CLAUDE.md, and atomicity is enforced where it belongs: the swarm-wrap writer commits per-scope and the `git-and-artifacts` auditor checks it. A per-action git hook would fight the repo's deliberate no-nag stance (D012 and the Codex notes that keep PreToolUse hooks off). The one hook we *did* add (D038's SessionStart snapshot) only records state — it never gates.

## D040 — Forward direction reopened: brain-as-privileged-information → sample-efficiency — 2026-06-18 (S24)

**Decision.** Erfan reopened the forward research direction (the closed-rung verdicts stand). New thrust: use the brain/biosignal signal as train-only **privileged information (LUPI)** to improve an LLM's **sample-efficiency / learning curve**, not the static encoding-R² metric (which every prior null answered). This is the charter's original **F2**, returned to with a theory (LUPI), higher-SNR regimes (ZuCo/CNeuroMod), and a control battery it never had — grounded on all prior work, nothing discarded. Folded into `expansion-program.md` §8 (Erfan's calls: extend expansion-program, not a new file; TRUE-100% Tier 1; the headline — PI-as-thesis-headline vs a parallel arm — **deferred to results**).

**Why.** R03's PAC-Bayes weak-prior bound says a weak well-aimed prior helps most in low-data and washes out as data grows — the one regime never tested (every null measured the metric at fixed data). LUPI gives that a learning-theory backbone. Critique-loop-hardened (counter-argument + lit-scout + Codex): LUPI is the bound to beat (likely-null on weak fMRI), so the realistic deliverable is a methodology/negative paper with upside. L050.

## D041 — Agent-fleet redesign + /goalsmith — 2026-06-18 (S24)

**Decision.** Implemented a repo-tooling redesign (spec: `docs/references/agent-fleet-redesign.md`, from a two-pass audit — a narrative workflow + an empirical mining of 266 subagent runs + the precedent-engine reference session). Added 5 atomic agents (`stat-aggregation-auditor`, `anti-confound-designer`, `dataset-verifier`, `dataset-scout`, `paper-repo-extractor`); the `/precheck` pre-compute gate; [`confound-catalog.md`](../references/confound-catalog.md) (single source of truth); extended `wrap-auditor` (provenance-completeness + doc-status-sync scopes, mid-session invocable); `/orient` working-tree + missing-wrap checks; the `agent_routing_lint.py` PreToolUse hook (nudges fable-banned + judgment-heavy→opus; `lit-scout`/`dataset-scout` task-dependent). Aligned the thinker/oracle panel to **goalsmith's resolve-or-root-cause Judge** (machine-readable `PANEL-VERDICT` blocks; oracle DESIGN/RESULT mode). Built **`/goalsmith`** (a /orient item → the ≤4000-char single-line `/goal` condition: PRD-pointer + resolve-or-root-cause completion). Added the fleet **self-activation map** to CLAUDE.md.

**Why.** The corpus showed recurring re-derivations + costly errors (the E021-v4 aggregation mistake, the L011/L012 re-derivation tax, multi-session doc drift, model-routing drift: fable 41× / paper-digest-on-sonnet 24×) with nothing enforcing the workflow. The fleet commoditizes the recurring tasks so Erfan stops re-explaining. **Deferred:** `.mcp.json` (no Exa transport config findable; a guessed one risks shadowing the global Exa). **Untested:** the new agents/hook get their first real exercise next working session.

## D042 — Q3's "one untested door" (full-FT denizenslab n=6) CLOSED / NOT BUILT — dataset too small — 2026-06-19 (S25)

**Decision.** The remaining open Q3 door — full fine-tuning (not a LoRA distillation readout) on multi-subject naturalistic voxelwise targets (denizenslab) — is **assessed CLOSED and NOT BUILT.** It was driven through the full pre-compute gate this session (four-lens panel on the Q3 verdict + `anti-confound-designer` battery + `oracle-reviewer` DESIGN mode = KILL the build). The Fork-1 cheap single-subject manipulation gate (Erfan-greenlit, feasibility-confirmed — TextGrids/mapper/NC all on disk) is **abandoned** for the same reason. **Q3's verdict is unchanged (still ❌); this only retires the open hedge.** Erfan-directed.

**Why.** Decisive reason = **dataset size/power:** denizenslab is n=6 subjects (6 real on disk); the per-individual claim is a *population* test (inference unit = subject), and the L024 power sim's "power 1.0 at n=5" holds only if between-subject σ≈0.001 — unmeasured on denizenslab, oracle estimated σ could be 2× (→ n≈8 needed). At n=6 with unknown σ the MDE may exceed the δ we seek, so even a clean run (or the cheap 1-subject gate) could not yield a powered population verdict; the deep subjects we'd need don't exist on disk (acquiring them is a data decision, not a re-run). Compounding (not decisive): the full-FT parameterization was already tested null (E017/L036); the manipulation-check gate is 0-for-5 (E013 v1/v2, E017 gentle/aggressive, E019). Recorded in E013 (S25 verdict), ladder (4 locations), tasks.md, and **L051** — the unifying lesson that **data scale, not the hypothesis, is the binding constraint on the remaining brain-alignment doors** (Q4's 400-sentence substrate is the same wall from the other side).

## D043 — Adopt Firecrawl as a web-data provider (cloud MCP + repo-local research skill) — 2026-06-19 (S26, tooling)

**Decision.** Set up Firecrawl for the repo. **Cloud API only** — the self-hosted stack needs Docker, which this container can't run; `FIRECRAWL_API_KEY` was already in `~/.config/secrets/env` (live-tested: scrape HTTP 200, `creditsUsed:1`; remote MCP `firecrawl-fastmcp v3.0.0`). Wired as a **project-scoped MCP server** in `.mcp.json` at repo root using the **remote transport** with `${FIRECRAWL_API_KEY}` interpolated (no secret committed; exposes `firecrawl_scrape/map/crawl/extract/search`, the research index `firecrawl_research_*`, and agent/interact/monitors). Installed the **`firecrawl-research-index`** skill repo-local under `.claude/skills/` to drive the research tools, complementing `lit-scout`. **Skipped the 5 `firecrawl-build-*` skills** (they onboard building apps *on* Firecrawl; irrelevant, and their aggressive triggers would mis-fire on normal web tasks). Documented in a `## Firecrawl` section of `CLAUDE.md` under the same hard line as Codex: subordinate to the docs brain, never a science number, never a rung flip; **cheap path (WebFetch/exa) first — credits are billed.**

**Why.** Adds clean-markdown extraction from JS-heavy/anti-bot pages, whole-site crawl/map, schema'd extraction, and a research index (papers + GitHub history) the existing web stack (exa/WebFetch/perplexity/lit-scout/academic APIs) doesn't cover — used selectively where it earns the credit. This creates the repo's **first `.mcp.json`**, scoped to Firecrawl only, which **partially resolves D041's deferred MCP-config item** and does **not** shadow the global Exa server (separate server name); D041's open Exa-transport question is untouched. **Open loop:** the project-scoped server is `⏸ Pending approval` until the next `claude` start. No science, number, or verdict changed — a tooling adoption only.

## D044 — Operating model = invokable interaction stances; the working/analysis split (D011) retired — 2026-06-19 (S27)

**Decision (Erfan-approved, atomic walk).** Replace the two-mode working/analysis session split (D011) with **eight invokable interaction stances**, implemented as one fat skill (`.claude/skills/stances/`) whose `SKILL.md` spine routes to deep per-mode files. The stances: **`/work`** (produce evidence), **`/interpret`** (evidence→verdict), **`/write`** (communicate), **`/teach`** (transfer understanding), **`/scout`** (literature+data intake), **`/meta`** (build/maintain apparatus), **`/plan`** (strategy/roadmap), **`/review`** (thinking panel + Codex on demand). You invoke a stance (explicitly, or by intent with the agent **stating** which it entered) and switch freely mid-session; `/work` is explicit-only and never auto-fires. The day-to-day picture is `docs/operating-map.md`; the model is defined in [`docs/03-methodology.md`](../03-methodology.md).

**The honesty spine is armed at write-time, not in the stance.** A PostToolUse hook (`.claude/hooks/honesty_writecheck.py`) runs the D011 number-check on writes to `docs/reports/` and `docs/manuscript/` (the prose deliverables that use the inline-cite convention; **scope corrected on the S27 trial** — `docs/ladder.md`/[`docs/learnings.md`](../learnings.md)/`docs/experiments/` reference results by bare code and false-positived 41× on the first edit, so they are excluded; they need a different check, L052), flagging an unsourced result-like number regardless of which stance is active (non-blocking; the `/wrap` provenance audit is the backstop). This was the adversarial panel's load-bearing fix: the fabrication guard cannot be skipped by mislabeling the work. Each truth-producing stance still carries its own *standard* (the threshold: `/work` = kill-criteria + contiguous splits + ≥3 seeds; `/interpret` = strict adjudication, never loose reading).

**Mapping for legacy references.** Where older docs/agents say "working session" read `/work`; "analysis session" splits into `/interpret` (adjudicate), `/write` (communicate), `/teach` (understand). The D011 numbers rule (an analysis act may only state recorded numbers) is unchanged and now hook-enforced. `goalsmith` and `precheck` remain `/work`-only gates.

**Why.** D011's two-mode label was a proxy for "what are you doing right now"; the eight stances are the precise version, and a real session routinely crosses the old seam (~6/29 timeline logs used arrow/slash mode compounds). A stance is a **durable, traceable, optimizable artifact** (Erfan's point, which overruled the panel's "a skill is just a prompt"), which a re-typed prompt is not. The design was atomic-walked with Erfan (stance list, replace-vs-coexist, fat-skill-with-modes architecture, explicit+auto invocation, the write-time hook, the `/teach` LearnLM/Gemini guided loop + four sub-modes + learning-record ledger, SCR predict-before-reveal, a light claim-manifest in `/interpret`) and twice adversarially paneled (four opus lenses + Codex); the panels' surviving fixes are baked in: write-time honesty, keep verdict-first reports and render simple-first at teach-time, Matt Pocock's filesystem-as-memory ledger (`docs/learning/`), decoupled stances rather than a Nexus-style coupled pipeline. Build sequence: **Pass 1 (this session)** = scaffold + `/teach` + `/interpret` + the hook + the report-clarity amendment + `operating-map.md` + the LearnLM/Bloom canonical notes + these doc/methodology updates; **Pass 2** = the other six mode files (`/write`, `/work`, `/scout`, `/meta`, `/plan`, `/review`) as thin wraps over existing agents/commands.

**Reverses if:** the stance vocabulary stops being used (Erfan just talks and the skills sit idle), or a stance boundary needs policing often enough to be a tax — then collapse toward the acts that earn their keep. **Supersedes D011.**

## D045 — /teach surface contract: explanation→file, dialogue→terminal, written at part boundaries — 2026-06-20 (S29, /meta)

**Decision (Erfan-directed).** Fix the `/teach` surface rule that the v2 build encoded wrong. The skill exists because the CLI cannot render LaTeX, yet `modes/teach.md` line 47 said *"the live Q&A is in the terminal; update the lesson at the end of a round"* — which inverted Erfan's explicit instruction (teach v2 session, msg 227) and made the R07 live test (session `c4b6fb0d`) dump the whole DPI derivation as raw `$$…$$` into the terminal, the exact failure the mode was built to prevent. The corrected loop, per part (one concept/chunk, sized by learning logic): **(1)** write the part's explanation + math + diagrams into the lesson file first and re-render — the user reads it rendered; **(2)** ask the question in the *terminal* (math allowed when it echoes the rendered file); **(3)** run the whole back-and-forth in the *terminal*, plain language; **(4)** at the part boundary, write the answer + what-did-not-land + a `---` divider + the next part's explanation into the file in one pass, re-render. The file is touched **at part boundaries only**, never mid-question; math never appears unrendered in the terminal. Edits: the surface-contract passages of `modes/teach.md` and `formats/lesson-format.md`, and the lesson template (unit = "part", not "round"). No file-tree, script, or other-behavior change; the two-layer memory (`lessons/` raw + `records/` OLM), pedagogy grounding, SCR, and sub-modes are untouched.

**Why.** Resolves the one tension the v2 counter-critique raised against the two-surface idea (split-attention / cognitive load, msg 1198): the surfaces are *sequential, not simultaneous* — read the rendered part, then talk in the terminal — so the file *lowers* working-memory load (a persistent external representation; LearnLM "manage cognitive load") rather than raising it, and unrendered terminal LaTeX (pure extraneous load) is eliminated. The sequence mirrors Erfan's own prior `course-lecture-study` skill: teach a chunk into the rendered note, interact, stabilize, advance. Pedagogy grounding unchanged (LearnLM, Bloom, Gemini guided-learning, [Dunlosky 2013](../literature/canonical/dunlosky-2013_effective-learning-techniques.md), [Bjork & Bjork 2011](../literature/canonical/bjork-2011_desirable-difficulties.md), the hypercorrection/OLM cluster). **Reverses if:** the part-boundary cadence proves too coarse in live use (then allow finer in-part file writes) — but only on observed friction, not pre-emptively.

## D046 — Prose ship-gate: a three-layer defense against LLM-register tells reaching a human — 2026-06-22 (S30, /meta)

**Decision (Erfan-directed, two forks confirmed).** After the IMDEA supervisor (Claudio) flagged the v0.1 extended manuscript for "llm-specific sentence constructions" (four example sentences, all narration/storytelling register), root-cause the failure and install a standing defense. **The diagnosis (evidence-backed, L054):** two independent breaks. **(1) Process** — the entire extended manuscript was written in one unlogged burst (commit `3145140`, 2026-06-16 18:57, all four flagged sentences) tacked onto the end of a `/meta` tooling session (S18), with no `/write` session, no `session-logger`, no review pass; the `scientific-writing` full loop never ran. **(2) Content** — even had the loop run, the skill would have caught at most one of the four: Group C (lexical tells) is fully encoded with a linter, but Group B (passive) pointed the *wrong way* ("passive is acceptable") and Group A (storytelling/register: anthropomorphized abstractions, self-narrated rhetorical moves, internal-metaphor leakage, dramatized framing) was *never encoded* — and the linter returned "clean" on the exact file Claudio flagged, because Group A carries no banned token.

**The remedy — four prose-defect classes placed on the deterministic↔agentic axis (the axis = "does a banned token betray it"):**
- **Layer 3 (content):** `writing-style.md` §1 gains the "Register: state the claim, do not narrate it" judgment block (the four tells, with Claudio's four sentences as worked Before/After failures); §2's passive rule is flipped from permissive to deliberate-choice + density; `review-pass.md` gains a "Scientific register" lens.
- **Layer 1 (deterministic):** `ai_tell_lint.py` gains a Class-A tripwire (agency-verb-on-abstraction, self-narration patterns, metaphor leakage) + a Class-B passive-density meter, as **soft warnings** (exit-neutral; the tripwire is intentionally incomplete — the agentic gate is the real Class-A catch).
- **Layer 2 (agentic):** a new **`prose-register-auditor`** agent (sonnet, read-only), spawned by the review pass for supervisor-facing prose — the dedicated voice reader (the claim panel attacks the argument; the auditor attacks the prose). Validated on the v0.1 intro: caught all four flagged sentences + two more, with rewrites, and kept the one justified passive.
- **Process / ship-gate:** a `prose_writecheck.py` PostToolUse hook (sibling to the D044 honesty hook) runs the linter on every `docs/{manuscript,reports}` write — the one check the unlogged-burst bypass *cannot* skip; plus a hard rule in SKILL.md + `modes/write.md` (a manuscript build is its own logged `/write` session; no `docs/manuscript/` prose reaches a human un-full-looped; a clean deterministic run is not a clearance); plus a `/wrap` B.3 backstop.

**Two forks Erfan chose:** the semantic catch is a **dedicated auditor agent** (not a lens bolted onto the opus claim panel — voice is a distinct job and sonnet fits it); the deterministic check **fires via the always-on hook** (not run_checks-only), so the bypass that caused this can't recur silently.

**Scope note.** This session built the *apparatus only* — the v0.1 manuscript prose is **not** rewritten here; the v0.2 register sweep is the first job that runs *through* this gate, as a logged `/write` session. Fixing it now without the gate would repeat the diagnosed sin.

**Why.** "Such as" in Claudio's note meant a *class*, not four sentences (the auditor confirmed it — 6 issues, not 4); a four-sentence patch would draw the same note next round. The deterministic/agentic split is forced by the data: Group C is a token list (cheap, complete), Group A is semantic (no token, needs a model). The hook is the structural lever because it is the only check independent of whether the ritual ran — the actual cause here. **Reverses if:** the soft-warning tripwire proves too noisy in practice (tighten the verb/subject lists or gate it behind the manuscript layer only), or the dedicated auditor proves redundant with the panel (fold its lens back in) — on observed friction, not pre-emptively.

## D047 — Register convergence gate: a Stop hook keyed to content hash, decoupled from /wrap — 2026-06-22 (S32, /meta)

**Decision (Erfan-directed, architecture-first).** The v0.2 session used the D046 apparatus correctly (logged `/write`, ship gate cited, hook fired, auditor spawned) yet still shipped a manuscript a fresh strict audit rated dirty, and the wrap recorded it "all resolved" (L055). Root cause: the review pass had no enforced *terminator* — "re-run until no hole survives" is prose, and the session treated "I made the fixes" as equivalent to "verified clean," stopping at `REGISTER-CLEAN: NO` with no final re-audit, on a *self-review* that under-detected (3 residuals found vs ~13 fresh). Fix: make a clean verdict on the **final bytes** a mechanically enforced precondition to finishing, **at the write actuator, not at `/wrap`** (Erfan's load-bearing point: `/wrap` is a generic session finalizer and must not own write-stance quality).

**Mechanism (verified against the Claude Code hook contract).** A **`Stop` hook** (`stop_register_gate.py`) blocks the agent from ending its turn (`{"decision":"block","reason":...}`) while a `docs/{manuscript,reports}` deliverable it edited this session lacks a clean register verdict **keyed to the current content hash** — so a stale YES dies the instant a byte changes. The verdict is produced only by `record_register_verdict.py`, which refuses unless **≥2 FRESH `prose-register-auditor` outputs all say `REGISTER-CLEAN: YES`** with zero findings (fresh = new `Agent` spawns with no writing context; in-session self-review is the demonstrated failure). Claude Code has **no native stance trigger and no automatic stop-loop guard**, so: the gate keys on *what changed* (read from the transcript), not on a "stance"; and the loop guard is hand-built (block at most `MAX_BLOCKS=3` per hash, then escalate to Erfan rather than trap the agent). Escape: an Erfan-approved accepted-residual sentinel for the exact bytes. The deterministic `prose_writecheck.py` hook (D046) remains the per-edit tripwire; this is the terminator. Tripwire also gained the leaked repo jargon (`load-bearing`, `kill-gated`, `lever`). Self-tested end-to-end (dirty→block, record→allow, byte-edit→stale-block, revert→allow, loop-guard escalates, sign-off→allow, non-deliverable→allow).

**Honest limit (recorded, not hidden).** The auditor is an LLM judging LLM prose; fresh context + a ≥2 quorum + a zero-findings bar raise the floor a lot but do not equal a human's ear. The claim is "no fresh reader-proxy flags the shipped bytes, recorded truthfully" — plus a periodic human read (Erfan/Claudio) whose catches become new rules in `writing-style.md`. That feedback loop is what makes the taxonomy approach complete over time. **Reverses if:** the Stop gate proves too disruptive on legitimate mid-write pauses (then narrow its trigger or raise `MAX_BLOCKS`), or a 2-auditor quorum proves insufficiently strict (raise the quorum) — on observed friction. **Builds on D046; does not supersede it.**

## D048 — Redesigned `/write` pipeline: a 4-concern, gated-loop, claim-grounded system (BUILD-READY) — 2026-06-22 (S35, /meta)

**Decision (Erfan-approved).** Replace the current `scientific-writing` "draft → full-loop → ship-gate" flow with a redesigned `/write` pipeline built on a *positive model of good writing*, not only defect detection (the S33 "immune system, not a notion of health" diagnosis). Four separated concerns — **Trust** (claims↔evidence, strength-tagged), **Argument** (warrants between claims + honest scope/acknowledgment), **Structure** (reader-expectation at every scale), **Voice** (scientific register). A gated-loop spine: Evidence → Message&Reader → Claim&Argument Lattice → Architecture+Figures → Draft → Audit → Revise; the human gates stages 1–3 (the *case + plan*), a convergence loop runs 4–6; trust comes from a `claim-lattice.json` locked at the gate + audited for drift ("trust by gate+audit", not "by construction"). Grounded in the writing canon (Gopen-Swan/Williams/Schimel/Swales/McEnerney/Mensh-Kording/Whitesides/Pinker/Toulmin) + an 11-repo ecosystem audit; the ground-truth target is Claudio's flagged sentence class ([`supervisor-feedback.md`](../references/supervisor-feedback.md)).

**Design + projection (build-ready).** 21 functionalities (2a) → 119-scenario TDD suite (2b — Claudio anchor locked + near-misses + real-prose exemplars mined from venue papers) → CC-primitive mapping (2c: ~10 subagents, ~6 hooks, 4 skill-sections, 2 gates, 4 artifacts) → reverse coverage check (2d: 6 mismatches found + re-mapped, no new agent). CC-power upgrades: parallel stage-5 audits, Stop-hook convergence, structured-output verdicts (`ready_to_ship`), gate via AskUserQuestion. Each step independently opus-reviewed and **adjudicated, not rubber-stamped** (kept F8a un-split + F9b separate against reviewer suggestions; conceded the 4th concern, the agent merges, the DET re-tags). All artifacts in `docs/references/write-redesign-*` (master canvas `write-redesign-design.html` v1.1).

**Build approach.** Build the new orchestration + new components from scratch; **lift the 9 existing DET scripts** (the floor — tested, the strongest part per every review), don't rewrite them; **walking-skeleton first** (one section, full spine, the abstract case) before the full build; **retire the old flow only once the 119-scenario suite passes** (Phase 3). Effort: HIGH all subagents, XHIGH for F4 (argument), F5 (scope), F11 (structure). Migration map + phases in `write-redesign-build-plan.md`. **Reverses if:** the walking skeleton fails to produce trustworthy prose on the abstract case (then revisit the spine, not just tune). **Builds on D035/D037/D044/D046/D047; supersedes the current skill's drafting flow only once cut over.**

**Amendment — D048 COMPLETE: cutover executed (S43/P3, 2026-06-26).** All three build phases done (Phase 1 walking skeleton S35–36, Phase 2 full coverage S36–38, X1–X4 cross-stance handoff S40); the acceptance suite is built and **PASSES** — 94 RUB scenarios graded by real subagent spawns + the 13 DET checks green (`rub_harness score: PASS`), **signed by Erfan** (suite `e49865ea3939f212`). P3 ran as: **P3-0** committed 12-scenario dress rehearsal (fixture-fairness audited by opus oracle, 4 rebuilt); **P3-1** the full suite in 7 grader batches, each committed, with two scenario corrections Erfan adjudicated (SC-VIO-2511-1 → noflag, idiom; SC-EX-2510-4 → flag, "ruling out" overclaim) and a recurring fixture-craft lesson (grouped-spawn context can cross-prime false fails → per-scenario context); **P3-2** the cutover — `/write` routing repointed scientific-writing → `sci-write-v2` across the live surface (command, stances, CLAUDE.md, methodology/reports/roadmap), the old skill **tombstoned** (read-only ~1 week, then delete), the hook layer cut over (retire the D047 `stop_register_gate`; convergence is now `stop_sw_converge`; the always-on prose linter upgraded to v2's `ai_tell_lint`). **`sci-write-v2` is now the default `/write` engine.** Honest limits carry forward unchanged (D051 framing-sentence escape; D050 bounded handoff guarantee; TRUSTED-not-verified provenance). **No experiment, no science number, no rung change — Q0–Q5 stand.**

## D049 — Agent effort declared in frontmatter (fleet-wide convention) — 2026-06-23 (S38, /meta)

**Decision (Erfan-approved).** Adopt an `effort:` field in agent frontmatter as the fleet-wide convention, alongside `model:`. Trigger: the P2-E authoring review found the sci-write judges' descriptions claimed "opus, xhigh" but **no agent set `effort:` anywhere** — so the xhigh judges silently inherited session effort (`high`); the stated policy was prose-only and inert (L064). All 24 agents now declare `effort:` after `model:` — **`xhigh`** for the three hardest sci-write judges (F4 argument, F5 scope, F11 structure — the real fix), **`high`** for the rest (= current session effort, now explicit/self-contained, behaviour-preserving). `CLAUDE.md`'s model-routing note updated to document the convention (model + effort in frontmatter; fleet default high, xhigh for the hardest judges; override per call when warranted). Supersedes the prior "model in frontmatter, effort per-call" reading of the routing rule. An effort *tuning* pass (e.g. bumping the truth-gating panel/oracle to xhigh) was deliberately deferred — this decision is about putting the existing intent into config, not re-tuning. No science touched.

## D050 — `/write` cross-stance handoff: route a substrate defect to its stance instead of papering over (BUILD-READY) — 2026-06-24 (S39, /meta)

**Decision (Erfan-approved).** Add to the D048 `/write` pipeline a cross-cutting **orchestration** function (not a 5th concern) that gives the stage-5 audit a **third per-finding outcome** beyond *converged* and *writing-revise*: **`NEEDS-STANCE(S)`**. When an auditor finds a defect the prose cannot fix because it lives in the evidence/argument substrate, `/write` **detects, classifies the target stance, emits a structured handoff, blocks convergence stickily, and recommends the stance + command** — it never auto-spawns another stance, never papers over, and never produces or adopts an unrecorded number. This turns the standing hard line ("a number is born in `/work` and recorded in `docs/`; re-enter the stance, don't invent") from a human instruction into a pipeline behavior. Forks Erfan settled: **detect-and-recommend, not auto-initiate**; **design-to-BUILD-READY this pass, build next session**; **orchestration function, not a 5th concern**.

**Trigger (the dry-run).** A `/meta` dry-run of `sci-write-v2` on R06/§4.1 ran the full pipeline end-to-end; the F13 panel (and F5/F9b) surfaced that the E006 voxelwise CI is a **within-subject voxel bootstrap** (pseudo-replicated — the L015 error caught on E005, uncorrected on E006): a `live`, sourced, not-demoted number that is *actually mis-aggregated*, invisible to every existing guard (`\gap`, `evidence_status`, `honesty_writecheck`). The pipeline blocked convergence but had no path to route it — and the convergence loop would have "fixed" it by rewording with the panel's *unrecorded* recompute, crossing the hard line. (The E006 CI itself is a parked `/interpret` item — **not** adjudicated by this `/meta` decision; no science number was produced or consumed here.)

**Design (BUILD-READY, full spec `docs/references/write-redesign-xstance.md`, hardened across 4 clean-context opus reviews — the L058 discipline).** A 7-row trigger taxonomy (broken/contested number → `/interpret`·`/work`; load-bearing `\gap` → `/work`; internal/external contradiction → `/interpret`·`/scout`; new number → `/work`; missing source → `/scout`; frame decision → `/plan`; unadjudicated cite → `/interpret`). The keystone is the **sticky block** (M1): a `handoffs-open` clause in `verdicts.py status()` keyed to a **separate `handoffs.json`** (the single store), *not* the prose hash — so a reword cannot close a substrate problem, only the upstream stance's **recorded** output can; `ship`/`accept-residual` refuse while any handoff is open. A **DET backstop** (M3) forces `NEEDS-STANCE` whenever a panel verdict is `SURVIVES-IF-NARROWED`/`DOES-NOT-SURVIVE` and the narrowing needs material not in `docs/` (so a reader cannot mislabel the anchor as a wording fix). A new **`evidence_status: suspect`** (set by `/interpret`, never `/write`) makes a future cite of the broken number a DET flag — the sticky lesson. Builds as four three-net chunks **X1–X4** (suspect enum · `verdicts.py` handoff store+ops+clause+ship-guard · SKILL stage-5.5 triage · wire the anchor + fold 16 `SC-XSTANCE-*` into the suite, 119→135); should land **before** P3 cutover. The recurring shape is **"RUB classifies, DET enforces the consequence"** — the same fluidity boundary the pipeline already runs on.

**Honest limits (recorded, not hidden).** This does **not** close the **framing-sentence escape** (a load-bearing assertion never entered as a claim is invisible to the detector; the human gate remains the only catch). The classification is RUB, so the guarantee is bounded: **panel-detectable substrate problems are mechanically caught (via the M3 backstop); non-panel ones rest on reader honesty + the human gate.** Provenance stays the accepted TRUSTED-not-verified model (a hand-typed verdict is indistinguishable from a real one — same as the sibling hooks). **Reverses if:** the over-routing guard proves too noisy in practice (every hard finding becomes a handoff and the gate drowns — then tighten the out-of-`docs/` force-rule or bias the classifier toward writing-revise), or the sticky block proves too rigid on a legitimately-narrowable claim (raise the bar for what forces `NEEDS-STANCE`) — on observed friction, not pre-emptively. **Builds on D048 (the pipeline) + D044/D046/D047 (the floor/gate/Stop-hook pattern); extends, does not supersede.**

## D051 — `/write` framing-sentence escape: ACCEPT as a documented cutover limit, do not build a prose→lattice check — 2026-06-25 (S42, /meta)

**Decision (agent judgment under Erfan's standing delegation; surfaced for override at the P3 readiness review).** The `sci-write-v2` Trust floor checks "every *claim* in the lattice binds to recorded evidence"; it cannot see a load-bearing assertion the agent places as *framing* and never enters as a claim (the standing Phase-2 residual, SKILL "Honest limits"). As the pre-P3 checklist item **G2** ("decide, don't drift"), this is resolved by **accepting it as a documented limit**, not by building the prose→lattice claim-coverage check.

**Rationale.** (1) **The residual is narrow.** The F5 scope judge and F12 voice auditor both read *all* prose at the stage-5 site, not only `\evd`-tagged claims (verified against their agent contracts) — so an *over-scoped* framing sentence (SC-HON-06) and a *badly-voiced* one are already caught, and the Claudio regression anchors (SC-VOICE-01..04) **are** framing sentences caught by F12. What slips is only a **cleanly-voiced, plausibly-scoped empirical assertion** in framing position that was never entered as a claim. (2) **Closing it is a high-false-positive judge, not a DET invariant.** Distinguishing a load-bearing empirical assertion from legitimate framing/transition prose is a judgment; a check that flags every untagged sentence flattens legitimate framing — the exact L060 over-flagging trap the build has repeatedly had to walk back. (3) **The F16 human gate is the designed backstop** for this narrow residual; the human approves the case+plan and reads the shipped prose. (4) `tasks.md` G2 explicitly offers accept-as-documented-limit as a valid clearance; the gate is making the decision *explicit and recorded*, which this does.

**Honest limit (recorded, not hidden).** A cleanly-voiced, well-scoped, unsupported empirical assertion placed as framing and never entered as a claim can ship without the Trust floor catching it; the human gate is the only catch. This is bounded by the F5/F12 all-prose reads (over-claim + voice subsets covered) but not eliminated. **Reverses if:** a real framing-sentence escape is observed shipping (an unsupported framing claim that passed the human gate) — then build the prose→lattice claim-coverage check (necessarily as an RUB judge, with a precision guard against flagging legitimate framing). Until observed, the check is YAGNI. **Builds on D048/D050; does not supersede — it closes the G2 checklist item by decision.**

**Amendment (S42, same session, after the P3-readiness premortem).** The premortem flagged that "accept" skipped a cheap middle option between the high-FP auto-judge (rightly rejected) and doing nothing. D051 is amended: the F16 human gate gains a **forcing-function** — enumerate framing/transition sentences carrying an empirical verb (tracks/predicts/improves/outperforms/aligns/generalizes) and force a per-sentence *claim* (→ enter+bind in the lattice) vs *cited-background* (→ citation) tag. This bounds the residual into a human checklist rather than leaving it to unaided noticing. Recorded in the SKILL "Honest limits". Does not change the accept decision; strengthens its backstop.


## D052 — the repo is an Obsidian-native vault; markdown conventions are codified and binding — 2026-06-26 (S44, /meta)

**Decision (Erfan-directed).** Make the repo a first-class Obsidian vault while keeping it GitHub-clean, and codify how every `.md` file is written in [`../references/obsidian-conventions.md`](../references/obsidian-conventions.md) (the binding container-layer spec). The repo is now read primarily in Obsidian.

**The settled rules.** Internal references are **standard relative Markdown links, never `[[wikilinks]]`** (wikilinks render as junk on GitHub, and standard links make the same Obsidian graph edges; Erfan's call after seeing that the all-GitHub `awesome-llm-apps` graph is fully connected). Every in-repo reference is a link, never a bare backtick path. Evidence cites are clickable (`[E003]` to its experiment file; still passes the honesty checker). Literature citations link to their canonical note on first mention. Frontmatter (title/tags/aliases) on every doc; `## Related` footers + `map.md`/`README.md` hubs drive the graph. One line per paragraph, `-` bullets, escaped `\|` in tables, one H1, no emoji in headings, the 5 cross-compatible callouts only. **Em-dashes are banned in new prose only** (Erfan, option A); the existing uses are left, no repo-wide cleanup. Exemption: `_prior-work/`.

**Tooling reality (recorded).** `obsidian-linter` is app-only (no CLI; its `yaml-title-alias` rule dirties frontmatter on save, so disable it). The agent/CI enforcement layer is `markdownlint-cli2` + `lychee` + an internal link-checker; Prettier is banned (it re-wraps prose).

**Rationale.** Obsidian needs near-zero conversion to be useful (it reads plain Markdown + relative links), so the work was about making references clickable and the graph connected, not switching syntax. Markdown links deliver Obsidian clickability AND GitHub rendering, so there is no fork to make. **Reverses if** Erfan decides GitHub rendering no longer matters, in which case wikilinks become viable. **Boundary:** this governs markdown structure (the container); `/write` (sci-write-v2) still owns report/manuscript prose bodies and their numbers/cites (D048).

## D053 — `sci-write-v2` audience-by-layer ("two modes") restored: `meta.layer` sets the reader-model's internal-code/gloss policy — 2026-06-29 (S45, /meta)

**Decision (Erfan-directed).** Restore into `sci-write-v2` the layered-audience rule the **D048 cutover silently dropped**. A new optional lattice field `meta.layer` ∈ {`report` | `extended` | `public`} is set first at Stage 1 and drives the **reader-model's OLD/NEW split and gloss depth**, so the deliverable's audience is a *declared input*, not a per-session guess: **`report`** → reader is internal (us + supervisor), the repo's codes (`Qn`/`Ennn`/`Dnnn`/`Lnnn`/`Rnn`) and established results are OLD (used freely in prose, unglossed); **`extended`** → supervisor, codes only as parenthetical pointers; **`public`** → external reviewer, zero codes, every result named in prose. Surgical: 3 files (`SKILL.md` Stage 1, `schema/LATTICE.md`, `agents/sw-reader-model.md`), ~25 lines, **zero script-logic change**; default `report` (backward-compatible — existing lattices + the example validate, all selftests pass).

**Trigger.** The R07 `sci-write-v2` rebuild (built this session to compare against the baseline R07) came out in **external/manuscript register** — context-independent, internal codes stripped from the prose — because the orchestrator set the reader-model's audience to an external ML-workshop reader. Two blind analyses (our 5-dimension reader + an independent opus on a top-venue rubric) converged: baseline = internal-report register, rebuild = public/manuscript register. Erfan identified the cause: the archived `scientific-writing` skill carried an explicit *"internal codes descend by layer"* rule (reports use codes freely; extended = parenthetical; public = zero) that did **not** survive the cutover into `sci-write-v2`.

**Rationale.** The report layer's job (D035) is internal synthesis wired to the docs brain; for an internal reader the repo's codes and established results **are** OLD, and re-explaining them in every report is the curse-of-knowledge in reverse. Manuscript-readiness is bought **once** at the compression step (extended → public strips codes), not by taxing every report. So reports *should* be project-embedded — the cutover regression had made `sci-write-v2` unable to write in that register. The two-mode behavior was always a **reader-model + RUB-judge** concern, never a DET gate (`ai_tell_lint` never policed internal codes), so the one lever is the reader-model audience — which is exactly what `meta.layer` now sets.

**Honest limit (recorded, not hidden).** `meta.layer` is **guidance, not DET-validated** (kept surgical; the F16 human gate surfaces a wrong audience as the backstop). **Per-layer register exemplars (F17) were NOT added** — the voice rules apply at all layers; an internal-report exemplar set is a future refinement. **Reverses if:** the layer gets routinely mis-set in practice (then add light validation), or report-mode proves to need its own register anchors (then build the per-layer F17 set). **Provenance:** the rule lived in the archived `scientific-writing` `SKILL.md` ("Internal codes are scaffolding… descend by layer. Reports may use them freely.") + [`../03-methodology.md`](../03-methodology.md) Deliverable layers (audience per layer). **Builds on D048** (the pipeline) **+ D035** (the layer model); extends, does not supersede. This session also produced the R07 comparison rebuild (`../reports/R07_sci-write-v2-rebuild.md`) — a skill-eval artifact, not a canonical finding-report, not wired into the reports ordering. **No science number, no rung change — Q0–Q5 stand.**

## D054 — Wrap commits are pushed to origin by default — 2026-07-02 (S46, /meta)

**Decision (Erfan-directed).** Session close now includes a push by default: after `/wrap` records the timeline, refreshes continuity docs, stages only the touched files, and commits the wrap changes atomically, the agent pushes the committed work on `main` to `origin`. The old rule, "push only when asked," is superseded for wrap/close behavior.

**Rationale.** The Codex sidebar showed a clean working tree but a large `main...origin/main` delta. That was not uncommitted work; it was committed local history that had not been pushed. For this repo, a clean close should mean both the working tree and the remote handoff are clean enough for the next session or machine to resume.

**Boundary.** Scoped staging remains unchanged: never `git add -A`/`.`; no `--amend`; no destructive operation without explicit approval. The push is skipped only if Erfan explicitly says not to, the network/auth/remote rejects it, or pushing would require resolving a non-fast-forward situation. Any skipped or failed push is reported in the close summary. **Builds on D007** (atomic scoped commits); supersedes only the previous "push only when asked" close-session rule.

## D055 — E016 goal route narrows to synthetic-target/control plus real-brain transfer failure — 2026-07-08 (S99, /interpret)

**Decision.** Close the current E016 experimental goal as a synthetic-target/control plus real-brain transfer-failure route, not a brain-specific positive KD route. The six-seed synthetic TRIBE-vs-textfeat comparator remains positive on the synthetic target endpoint, but the combined seed `0-5` Tuckute `/interpret` closeout rejects the real-brain positive branch for this goal: TRIBE-minus-textfeat real-brain gain versus KD-only is `-0.001213`, CI `[-0.001846, -0.000580]`, `n=6`, all seed margins negative; versus permuted-control gains it is `-0.001005`, CI `[-0.001643, -0.000368]`. The official audit passed and routed to `real_brain_warning_needs_claim_scope_review`, and a local row-level recompute matched the recorded analysis and audit artifacts. Recorded in `../e016-combined-tuckute-interpretation-2026-07-08.md` and [`../experiments/E016_tribe-synthetic-brain-targets.md`](../experiments/E016_tribe-synthetic-brain-targets.md) Step 69.

**Why.** The decisive scientific distinction is synthetic-proxy success versus real-brain transfer. Beating a sentence-local text-feature target on synthetic target-R2 does not license a brain-specific claim when the saved students fail the real Tuckute endpoint under the same seed-aligned control ladder. Launching `contextfeat`, OPRD-lite, PHF-lite, or a new dataset now would answer a different positive-branch confound while the current blocking fact is transfer failure. The next useful work is `/plan` and then `/write`: turn this into a careful controlled paper package, likely AAAI-first, with independent code/stat review only if the Tuckute diagnostic becomes publication-load-bearing.

**Boundary.** This decision does not flip a Q-rung and does not update the extended or public manuscript. It also does not prove that all neural/cognitive privileged targets fail, only that this E016 TRIBE synthetic target did not transfer to the recorded Tuckute endpoint under the current controls. Reopens only on a new predeclared endpoint/dataset or a found evaluator/stat error, not by reinterpreting these artifacts.

## D056 — Usage-evidenced source-of-truth cutover — 2026-07-13 (S100, /meta)

**Decision (Erfan-directed).** Replace the report-plus-three-board operating model with four authorities: E records plus retained artifacts own evidence; the extended manuscript owns current scientific interpretation; [`status.md`](../status.md) owns operational state; decisions, learnings, selected consequential timelines, and Git own history. Public cuts are immutable. Writing goes directly from E records into the extended manuscript. No replacement archive, claim database, dashboard, report system, or generalized cleanup framework will be built.

**Usage evidence.** A streaming audit processed all 757 Claude JSONL files in the six repository project stores and 35 deduplicated repo-related Codex sessions (792 total), 177,782 JSONL records, and 22,869 tool invocations, with zero malformed records. Raw transcripts remained read-only and outside Git. Seventy-four sessions read at least two of `ladder`/`upspeed`/`tasks` merely to reconstruct state; 40 read all three. Of 19 verified direct `/wrap` sessions, 16 rewrote all three boards and 18 wrote a timeline. Those boards accumulated 369 commits. Reports were read in 92 sessions while the extended manuscript was read in 21, demonstrating that the intermediate synthesis layer displaced the deliverable. The writing systems had seven verified `scientific-writing` invocations and five-session fan-out across several `sci-write-v2` judges, but user feedback identified unsatisfactory openings, unclear sentences, overlong prose, and a system that enforced defect removal without producing taste; Erfan explicitly abandoned both pipelines. Science-review agents, in contrast, caught verified issues including the Q1 quality confound and the E004/E006 inference-unit problem.

**Disposition registry.** Historical components already absent at cutover remain absent. Current surfaces are classified below; grouped rows share one owner and fate.

| Components | Disposition | Evidence and migration |
|---|---|---|
| `orient`, `wrap` | KEEP, simplify | 42 and 19 verified direct command sessions; rewire to `status.md` and changed-authority-only close |
| `work`, `interpret`, `write`, `teach`, `scout`, `plan`, `review`, `meta`, `precheck` | KEEP as thin stance entry points | Distinct scientific/interaction purposes; remove report/checkpoint/logging dependencies |
| `goalsmith` | DELETE | No verified direct invocation; duplicates ordinary goal specification |
| `stances` | KEEP, simplify | 56 observed sessions and repeated explicit stance use; retain vocabulary, remove old board/report ritual |
| `firecrawl-research-index` | KEEP | Distinct literature-retrieval capability, outside the redundant writing/state apparatus |
| `scientific-writing`, `sci-write-v2`, `writing-great-skills` | DELETE | Explicit abandonment; large self-maintenance history; salvage only deterministic manuscript checks |
| `counter-argument`, `premortem-analyst`, `oracle-reviewer`, `first-principles-grounder`, `socratic-thinker` | KEEP | 26/19/17/17/10 verified invocation sessions; verified scientific catches and distinct review lenses |
| `anti-confound-designer`, `stat-aggregation-auditor`, `dataset-verifier`, `dataset-scout`, `lit-scout`, `paper-digest` | KEEP | Low-frequency but phase-specific science controls; single-use retention is justified by severity or non-overlapping function |
| `paper-repo-extractor` | DELETE | No verified invocation and no durable downstream reuse |
| `sw-*`, `prose-register-auditor` | DELETE | Writing-pipeline fan-out; replaced by one fresh independent manuscript review |
| `session-logger`, `wrap-auditor` | DELETE | One and six verified invocations; primarily synchronized redundant boards/logs and added close friction |
| `agent_routing_lint` | KEEP | Small deterministic guard for model routing |
| `honesty_writecheck`, `prose_writecheck` | KEEP, narrow | Deterministic manuscript provenance/register floors; remove report and retired-pipeline dependencies |
| `stop_register_gate`, `stop_sw_converge`, `wrap_session_snapshot` | DELETE | Retired writing convergence and compulsory wrap-state machinery; documented false-block risk and high repair burden |
| E records and load-bearing artifacts | KEEP as evidence authority | Source of recorded numbers, designs, provenance, and verdicts |
| Extended manuscript and frozen public cuts | KEEP as scientific/public authorities | Direct destination for settled paper-relevant interpretation |
| `status.md` | CREATE as operational authority | Replaces multi-board reconstruction; capped at 120 lines and five actions |
| `ladder`, `upspeed`, `tasks` | DELETE after status cutover | 74 multi-read sessions, 37 multi-write sessions, 369 commits; same state copied across owners |
| `reports/` | DELETE after manuscript migration | 92 read sessions versus 21 for the manuscript; intermediate synthesis became a competing truth layer |
| `map`, roadmaps, idea tree, litsweep plan, dated top-venue/E016 memos | DELETE after unique-content routing | Planning/status overlap and stale successor chains; current operations move to `status.md`, science to E/manuscript/landscape |
| checkpoint log and duplicate manuscript archive | DELETE after coverage check | Git, decisions, and selected timelines already own history; public v0.9 becomes a frozen cut |
| decisions, learnings, consequential timelines, Git | KEEP as history authority | Durable rationale, general lessons, milestones, and recoverability |
| routine/no-op/monitor/orient/wrap timelines | DELETE in one conservative pass | No durable decision or scientific content; ambiguous logs remain |

**Reverses if:** `status.md` cannot support orientation alone, direct manuscript writing repeatedly loses unique scientific context, or a deleted deterministic guard is shown to have caught a high-severity issue with no surviving equivalent. Recovery is from Git tag `pre-source-truth-cutover-2026-07-13`, not a new archive tree. Supersedes D015, D035, D038, D047, D048, D050, D051, and D053 where they require multiple status boards, reports, checkpoint logs, writing orchestration, or routine wrap swarms; D011’s evidence provenance rule remains and is simplified.

## D057: Canonical three-package conference-extension strategy and provenance (2026-07-14, /plan + /meta)

**Decision (Erfan-directed).** Internalize three alternative conference-paper packages as the durable strategy for work beyond the share-ready thesis. The canonical labels follow the corrected Pro audit: **Package A = methodological/falsification protocol**, **Package B = conditional theoretical boundary**, and **Package C = positive brain-guided mechanism**. Package A is the default active route, Package B is a conditional alternative, and Package C is closed for the tested regimes unless new gates reopen it. These are alternative paper identities with shared prerequisite analyses, not three simultaneous claims that the final paper should make.

**Relation to D055.** This decision preserves D055’s scientific E016 verdict and transfer-failure boundary. It supersedes only D055’s tentative “AAAI-first” planning implication by replacing it with package-specific evidence and venue gates.

**Naming boundary.** The [initial Pro audit](../external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md#7-paper-identity) used a different identity order, with its methodological route called “C.” Future work must use the corrected package order above, which comes from [Part VI of the corrected Pro audit](../external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md#part-vi-three-top-conference-paper-packages). This decision supersedes only the package letters, not the preserved source text.

**Provenance and authority.** The package concepts and much of their proposed burden came from the [initial strategic audit](../external-reviews/chatgpt-pro/2026-07-14-01-initial-manuscript-strategy-audit.md) and the [corrected research audit](../external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md). Those documents are non-authoritative external reviews. This decision records the subset accepted after checking the repository, saved E016 artifacts, participant data, and canonical literature notes. Scientific results still originate only in E records and enter the extended manuscript only after settlement.

| Package | Canonical identity | Current state | Activation condition | Pro source |
|---|---|---|---|---|
| A | Methodological and falsification protocol | **Default active route** | E025 participant E016 scope, E026 target comparability, clear novelty beyond L-PACT, and one prospective external application or faithful positive reproduction | [Corrected audit §24](../external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md#24-package-a-methodological-and-falsification-protocol) |
| B | Conditional theoretical boundary | **Conditional feasibility route** | A nontrivial finite-sample theorem or bound with observable terms that distinguishes at least one failure regime from one success regime | [Corrected audit §25](../external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md#25-package-b-conditional-theoretical-boundary) |
| C | Positive brain-guided mechanism | **Closed for tested regimes** | E025 is participant-positive and stable, E026 supports a defensible learning-matched control, and a predeclared E027 clears target-specific transfer before any expensive new substrate | [Corrected audit §26](../external-reviews/chatgpt-pro/2026-07-14-02-corrected-research-audit.md#26-package-c-positive-brain-guided-mechanism) |

**Package A burden.** The central claim is that controlled predictivity, target-specific student movement, participant-level biological transfer, and external utility are distinct evidential requirements, and that the current distillation program terminates at different gates. The internal evidence spine is the E004/E005 inference-unit correction, [E008](../experiments/E008_per-participant-f1-solidification.md), [E014](../experiments/E014_averaging-encoding-confound.md), and [E016](../experiments/E016_tribe-synthetic-brain-targets.md). It becomes a competitive conference package only if E025 and E026 sharpen the E016 scope, the novelty is distinguished from L-PACT and standard experimental logic, and the protocol is applied prospectively to an external positive or faithful reproduction. Kill this route as a top-conference identity if it yields no prediction or adjudication beyond existing frameworks; retain the evidence as a narrower thesis or journal contribution.

**Package B burden.** The central claim is a conditional boundary on the incremental value of brain-derived training supervision for finite learners. Standard conditional independence, deterministic-proxy redundancy, and unrestricted-learner arguments are background, not a publishable theorem. Activation requires a finite-sample statement with measurable reliability, conditional-information, hypothesis-class, sample-size, or optimization terms, plus at least one predicted failure regime and one predicted success regime. Kill the theory-paper route if the strongest result remains a restatement of conditional independence or contains unidentifiable terms that do not guide an experiment.

**Package C burden.** The central claim is that brain supervision contributes participant-general, task-relevant structure beyond teacher and text controls, improves a fixed-budget student at matched quality and compute, and transfers to an independent biological or practical endpoint. E025 and E026 are cheap reopening gates, not positive evidence in advance. If they pass, one geometry- and learnability-matched non-brain control may be trained as E027. A high-cost repeated-fMRI, ECoG, MEG, downstream, or compression experiment is authorized only after that matched control clears. Kill Package C if a target is learnable but again fails stable participant-level recorded-brain transfer.

**Provisional venue fit.** Package A points first to a later ACL or EMNLP cycle, with TMLR as a non-conference fallback and broad ML venues requiring a multi-study reusable protocol. Package B points to AISTATS or UAI, with ICML or NeurIPS requiring a much stronger general result. Package C is the route most naturally aimed at NeurIPS, ICML, or ICLR, but only after the positive mechanism and independent endpoint exist. AAAI remains a cross-cutting option only if the selected package becomes a general AI contribution. Venue calendars and calls must be reverified when a package activates; the external audits are not scheduling authorities.

**Execution order.** First run E025 and E026 because they inform all three packages. Then use separate `/plan` sessions to specify Package A’s external prospective test, Package B’s theorem-feasibility target, and Package C’s activation audit. Planning all three is allowed; compute is not. Evidence-producing work proceeds only when the corresponding activation gate is explicitly locked in `/work`. Package A remains the default paper route unless Erfan records a different strategic choice.

**Reverses if:** E025/E026 overturn the current E016 scope, a genuinely new theorem makes Package B clearly dominant, a participant-general positive reopens Package C, or a full novelty audit shows Package A is fully subsumed by prior work.

## D058: E025 kills the participant-positive continuation and sharpens Package A (2026-07-16, /work + /interpret)

**Decision.** Do not construct or train E027. E025 passed its language-quality, target-directed-learning, and representation-movement gates, but failed the participant-general biological-transfer gate: TRIBE-minus-text-feature was `+0.000136` unique-R2 across nine Tuckute participants, CI95 `[-0.000505,+0.000777]`, with a one-sided upper bound of `+0.000653` below the predeclared `+0.002` SESOI. Only 4/9 participants were positive; UID 837 supplied the sole clear positive and dropping it reversed the mean. TRIBE-minus-KD itself was `-0.000014`. Observed 80% MDE was `0.000890`, so this is not a power-limited failure to activate. Independent aggregation reproduced every reported statistic and the result oracle returned PASS / positive-branch KILL / `PANEL-CLEAN: YES`.

**Scientific scope.** This primary TRIBE-minus-textfeat interval excludes a mean `+0.002` relative participant-level effect only for the fixed nine-participant Tuckute sentence/ROI substrate. Direct TRIBE-minus-KD is separately near zero. Neither result establishes an exact zero, universal impossibility, or brain specificity. The existing text-feature control remains dimension-matched rather than geometry-, information-, or learnability-matched; the saved permutation remains defective.

**Package consequence.** Package C remains closed and its E025-dependent E027 activation route is killed. Package A is strengthened because E025 provides a clean intervention-chain separation: auxiliary-target learning succeeds, the student moves, language quality is matched, yet the predeclared participant-general biological-transfer gate fails. Continue E026 only as a retrospective target-comparability/identification audit for Package A, not as a license to train a matched control. Package B remains on HOLD pending a genuinely observable certificate with prospective failure/success predictions.

**External consequence.** Make the strongest current positive collision the next Package A test: preregister a corrected, participant-level falsification of Vaidya et al.'s cross-person, cross-stimulus fMRI-to-ECoG transfer. Begin with artifact access and faithful reproduction/corrected reanalysis; phase-randomized and optimization/geometry-matched interventions remain conditional on the corrected participant result surviving.

**Reverses if:** a new predeclared independent substrate shows stable participant-general transfer beyond a learning/geometry-matched nonbrain control at matched quality, or E025's frozen artifacts/statistical reconstruction are invalidated. A positive in one participant, target learnability alone, or model movement alone does not reverse this decision.

## D059: E026 closes the saved text-feature comparator as an identified cross-target control (2026-07-17, /work + /interpret)

**Decision.** Under E026's predeclared engineering conjunction, the saved projected text-feature arm is non-comparable to TRIBE on the measured pretraining and trained-movement axes. The independent result checker reconstructed all 55 states without importing the main runner and returned 24 PASS, 30 FAIL, one UNRESOLVED, and zero mismatches while rehashing all 128 bound dependencies.

**Evidence.** Mean KD-only target $R^2$ is `0.595327` for TRIBE and `0.911687` for textfeat, producing a `0.316360` gap against margin `0.02` and a remaining-headroom ratio of `4.582` against `[0.90,1.10]`. Normalized spectrum log-RMS differences are `5.524/5.535` against `0.10`; stable-rank log-ratios are `0.634/0.616` against `0.10`; low-level nuisance-predictability gaps are `0.192/0.183` against `0.02`; and all six global parameter-update and centered-Frobenius movement margins fail. Standardized global scale, most valid temporal-order diagnostics, power-spectrum shape, and static-unique predictability pass; four of six CKA-distance margins pass. Initial gradients are unavailable, and lag 1024 has no valid within-document pairs.

**Scientific scope.** E026 does not show that target geometry caused E025's biological failure, prove information inequivalence, or establish that TRIBE contains unique biological information. It shows that E016's between-target gain difference cannot isolate target content. E016's within-TRIBE learnability result remains valid. E025's predeclared `+0.002` exclusion belongs to its primary TRIBE-minus-textfeat activation contrast; separately, direct TRIBE-minus-KD is `-0.000014`, CI95 `[-0.000739,+0.000711]`, and shows no demonstrated direct gain.

**Package consequence.** Package A is strengthened by a four-way empirical separation among target learning, retained-model movement, control identification, and participant transfer. Package C and E027 remain closed because E025's prospective activation failed. Package B remains HOLD because E026 is retrospective and does not test an endpoint-directional certificate prospectively. E028 is Package A's binding external route, subject to author-artifact access, executable-boundary completion, a dimension-scale synthetic benchmark, anti-confound review, and final oracle.

**Reverses if:** the frozen E026 audit or its dependency bindings are invalidated, or a prospectively fixed comparator matches the required axes, including initial gradients, and then survives participant-level independent biological transfer. Matching output width or obtaining target learnability alone does not reverse this decision.

## D060: E030 localizes the exact-substrate failure and gates the external conference portfolio (2026-07-21, /work + /interpret + /plan)

**Mechanical evidence.** E030 passed its full validity chain and independent result audit. The aligned text-only TRIBE target's participant-mean unique linear increment above the frozen nuisance model was `-0.004494`, with a Bonferroni family-95% two-sided t interval of `[-0.010695,+0.001707]`; the simultaneous upper bound was below the inherited `+0.002` continuation reference. All participant- and block-leave-out means were negative. The aligned-minus-frozen-twin contrast was unresolved. Absolute target extractability from TRIBE students was positive and stable at `+0.040725`, interval `[+0.039053,+0.042398]`, but TRIBE-minus-KD retention and all bridge increments were unresolved. An independent recomputation matched all `748` load-bearing analysis leaves with zero differences, and a separate provenance audit returned `PANEL-CLEAN: YES`.

**Scientific boundary.** The frozen mechanical label is `NO PRACTICALLY RELEVANT LINEAR MEASURABILITY`, but its defensible prose scope is narrower: the PCA-50 TRIBE target did not add a participant-mean unique linear increment of at least `+0.002` beyond the specified nuisance model on this fixed sentence, participant, and ROI substrate. This does not exclude nuisance-redundant or total predictivity, lower-variance target directions, nonlinear readouts, other endpoints, other cohorts, or row-specific advantage over the one frozen twin. The `+0.002` reference is internally predeclared rather than externally validated for C1. Erfan confirmation remains required before this framing enters the manuscript.

**Research decision.** Stop E030 without layer, target, nuisance, seed, threshold, or readout rescue. It does not reopen Package C and does not change the existing thesis verdict that the tested distillation regimes show no reliable brain-guided benefit. It sharpens Package A by locating a source-target validity failure before student-to-brain overlap.

**Conference allocation.** Keep E028 as Package A's primary prospective external gate, but do not commit its approximately `1,120` GPU-hour full matrix before corrected Stage 1 passes. Run a 10-business-day outcome-blind feasibility window with two parallel lanes: pursue E028 author artifacts plus its parameterized Stage-1 executable boundary, and freeze a smallest-setting controlled reproduction design for Xiao et al. 2026 as the lower-dependency backup. If complete hashable E028 artifacts arrive, E028 Stage 1 runs first. If the exact lane remains unavailable at the checkpoint, label it unavailable rather than failed and move the main allocation to Xiao unless Erfan explicitly authorizes an independent E028 reimplementation. Preserve the share-ready thesis through E026 as circulation and publication insurance.

**External-action boundary.** The prepared E028 author request and any follow-up require Erfan's explicit communication approval. Outcome-blind local implementation does not authorize endpoint acquisition, result opening, or evidence-producing compute. A Xiao run likewise requires its own prospective E record, reproduction tolerance, matched-control design, precheck, and `/work` authorization.

**Reverses if:** E030's artifact chain or independent recomputation is invalidated; an independent, prospectively fixed substrate establishes source-target validity and participant-general transfer; complete E028 artifacts make its exact lane immediately dominant; or a genuinely estimable theoretical certificate prospectively separates positive, null, and harmful regimes at lower total cost.

## D061: Lock the outcome-blind E028 development boundary before code (2026-07-22, /review + /work)

**Decision.** Accept Erfan's explicit authorization to send the E028 author-artifact request, synchronize the confirmed E030 framing, and implement only an outcome-blind synthetic Stage-1 E028 slice. The author request was sent on 2026-07-22. No neural payload, author-result value, endpoint score, model training, or readiness claim is authorized by this decision.

**Design correction.** Two independent outcome-blind reviews found that the first E028 record was not executable as sealed. Exact fold arrays depended on unopened finite-response support; the all-contiguous rule made one bad bin fatal; movement and aggregation metrics were underspecified; the proposed audio arm was inaccurately called nonbrain despite using aggregate fMRI geometry; and the first adjusted max-T repair broke the common-sign randomization orbit. The locked correction uses an append-only `C0`--`C8` fact/result chain, absolute 50 ms ticks with recorded gaps and simultaneous outer/inner embargo roles, fail-closed cell semantics, gauge-invariant effective LoRA movement, exact CKA/RMS/TIMIT definitions, no-refit pooled-SSE/SST leave-one-block recomputation, and Bonferroni singleton studentized sign-flip inversions with exact enumeration. Stage 3 is now an itemwise-audio target calibrated to training-fMRI aggregate geometry, not a brain-free control.

**Gate.** The anti-confound review and corrected oracle recheck both remained outcome-blind. The oracle returned `PANEL-CLEAN: YES` and `READY-TO-IMPLEMENT: YES` only for the synthetic Stage-1 development slice, with `ENDPOINT-READY: NO`. Implementation must expose no endpoint, training, download, unseal, score, or readiness command; missing author facts remain explicit nulls, and every development artifact must say it is synthetic and not ready.

**Why this is the bottleneck.** The conference route does not currently wait on another internal model variant. It waits on whether E028 can become a faithful, computationally credible external adjudication. The smallest useful test is therefore the sufficient-statistics Stage-1 evaluator plus its synthetic analyzer and production-shape benchmark. A passing synthetic slice removes an implementation uncertainty; it does not substitute for author artifacts, full bundle review, or biological evidence.

**Reverses if:** the synthetic implementation cannot reproduce its locked fixtures or fit the compute ceiling; an outcome-blind review finds another design defect; author artifacts contradict a corrected-lane choice and force a retained new `C0`; or Erfan withdraws authorization before endpoint access.

## D062: Adopt question-led writing as the manuscript composition method (2026-07-22, /plan + /meta)

**Decision.** Plan and revise explanatory prose as a hierarchy of reader questions: one governing document question, section questions that directly advance it, optional subsection questions only when they improve navigation, and one primary question per paragraph. Order questions by conceptual dependency and write each paragraph as a direct answer supported by only the necessary reasoning, evidence, and scope. The reusable procedure lives in [`.claude/skills/question-led-writing/SKILL.md`](../../.claude/skills/question-led-writing/SKILL.md) and is part of `/write`.

**Rationale.** Topic-led drafting makes it easy to include locally relevant technical material before the reader needs it and difficult to detect missing prerequisites or paragraphs with no argumentative role. A reader-question hierarchy makes those failures inspectable. The triggering example was the introduction's unexplained use of $R^2$: the paragraph's actual question is what “predict the brain” licenses, so naming the metric there adds a prerequisite without helping answer that question. The narrower claim is supported: this method improves argument visibility and exposes likely gaps; it does not by itself guarantee truth, completeness, or readable prose.

**Safeguards.** Questions are working structure, not a new scientific authority. Evidence provenance, estimands, inference units, uncertainty, citations, and identifying assumptions remain mandatory. Use a declared reader model, define prerequisites before use, answer before elaborating, keep one stable term per concept, match technical detail to the current question, and delete material that answers no necessary question. Stop decomposing when the paragraph question is directly answerable so the method does not become bureaucracy.

**Reverses if:** repeated use produces forced fragmentation, hides cross-cutting arguments, or costs more attention than it saves. In that case retain reverse outlining as a diagnostic and relax the drafting hierarchy.

## D063: Separate comparator identification from post-training diagnostics and correct the utility disposition (2026-08-04, /interpret + /write)

**Decision.** Supersede D059's use of post-training movement as a comparator-identification gate while preserving its raw audit arithmetic and non-identifying verdict. The corrected E026 identification set contains 37 pre-outcome or KD-baseline checks: 20 pass, 16 fail, and one is unresolved. The other 18 states are post-training diagnostics: 14 fall outside the original engineering margins and four fall within them. The saved text-derived auxiliary control remains non-identifying because target geometry, effective rank, nuisance predictability, KD-baseline recovery, and remaining headroom differ; movement describes the realized interventions but does not determine whether the comparator identifies brain-response content.

**Utility correction.** Supersede E009's bounded-null interpretation. Its recorded Pereira and LeBel endpoint means favor the recorded-response arm, but the completed analysis retained no paired endpoint interval, test, or equivalence analysis. The endpoint is therefore inconclusive. Brain-specific practical utility is not established because the endpoint uncertainty is unreported and the prerequisite controlled-predictivity contrast is technically unstable. The MDE remains a sensitivity quantity, not a null or equivalence decision.

**Thesis consequence.** Replace the universal evidence chain with claim-specific dependencies. Route-specific headroom supplies opportunity context rather than a universal gate. The 50-component linear target-projection measurability assay qualifies only the declared linear pathway. Direct synthetic-response versus ordinary-KD biological transfer remains interpretable independently of the text-derived comparator; the comparator is required only for brain-response-content attribution.

**Reverses if:** the frozen E026 state classification is invalidated; a prospectively matched comparator passes the pre-outcome and baseline conditions; or a declared paired E009 endpoint analysis changes the endpoint disposition. No raw result, artifact hash, or direct-transfer estimate changes under this decision.

## Related

- [`status.md`](../status.md) — operational authority
- [`03-methodology.md`](../03-methodology.md) — four-authority contract
- [`../manuscript/extended/main-extended.tex`](../manuscript/extended/main-extended.tex) — scientific authority
