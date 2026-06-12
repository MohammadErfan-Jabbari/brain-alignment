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
the bureaucracy. See `../03-methodology.md`.
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
unchanged: scoped staging only (never `git add -A`/`.`), no `--amend`, push only when asked.
**Rationale:** Erfan wants a detailed, granular overview of how the repo evolved — and the decision
log + timeline remain the canonical research record.
**Reverses if:** never expected — it is a working norm.

### D008 — 2026-06-09 — Benchmark choice: LeBel ds003020 primary, Narratives generalisation, Pereira plumbing

**Decision:** Adopt **LeBel et al. 2023 (OpenNeuro `ds003020`)** as the primary language-fMRI benchmark
for the thesis result (powered within-subject deep-sampling, reported noise ceiling, CC0/CC-BY, anonymous
S3/DataLad — no login). Use **Narratives (`ds002345`)** as the cross-subject generalisation check and
**Pereira 2018 (OSF `crwz7`)** as the lightweight plumbing sanity-test. Full survey + power analysis in
`../04-data-benchmarks.md`.
**Rationale:** Resolves the #1 SPOF (`01-research-landscape.md`): an open, adequately powered benchmark
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
missing number is a gap to flag, never one to invent. Encoded in `../../CLAUDE.md` ("Two kinds of
session") and `../03-methodology.md` ("Two session modes"); analysis outputs home created at
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
copies live in Erfan's `~/uni/`); the committed, portable record is the curated index `docs/06-theory-grounding.md`
plus a navigation `data/course-material/INDEX.md`. **(3) Fold the load-bearing math into the live docs now.**
R03 §2 gains a Step 7 that anchors its first-principles bounds to the course's exact theorems (MI generalization
bound `gen ≤ √(2σ²I(W;Zⁿ)/n)`, data-processing inequality, conditional MI = "unique R²", rate-distortion = the F1
trade-off curve); `01-research-landscape.md` §E and `CLAUDE.md` "Read this first" now point at the grounding doc.
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

> **⚠️ PART (3) SUPERSEDED by [[D018]] (2026-06-12).** The "A+B synthesis / F1 confirmed in-domain" framing in (3) below did **not** survive per-individual inference: E008 (n=9, well-powered) returned a per-subject NULL, and E005's +0.0081 was a group-averaged-target artifact. The thesis is now **Fork B** (per-individual null + measurement-validity result). The "Reverses if" condition effectively fired. **Parts (1) [L_brain = co-trained MSE] and (2) [E007 not built] still STAND.** Read (3) only as historical context.

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
existing result. Model routing per Erfan's rule: `counter-argument`/`premortem-analyst`/
`first-principles-grounder` default **fable** (hard counter-arguing), `socratic-thinker` and the
existing search/digest/log agents **sonnet**, mechanical fan-out **haiku**. Model declared in each
agent's `model:` frontmatter; existing agents got an explicit `model:` too.
**Rationale:** Erfan's autonomous-mode directive ("after each phase, run counter-argument and Socratic
thinker and other methods of thinking, go back and forth, verify then address until there is no hole in
our arguments"). The four lenses are non-overlapping: external attack (counter-argument), assumption
exposure (socratic), prospective-hindsight failure (premortem), foundational re-derivation against the
math/papers (first-principles). The last directly serves the "everything must be grounded" mandate by
checking claims against `06-theory-grounding.md`, the canonical notes, and the course material.
**Reverses if:** the panel becomes ceremony that doesn't change conclusions (collapse to the one or two
lenses that earn their keep), or a single combined reviewer proves as effective at lower cost.

### D018 — 2026-06-11 — In-domain F1 reframed to Fork-B: the per-subject effect is NULL (E008); A3 is now the central contribution

**Decision (Erfan-confirmed, D015 gate):** The L3/F1 "headline" is downgraded from 🟡 PARTIAL-PASS to a
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
real impl work today — F3/L4 is moot pending a positive L3), or Erfan redirects on return.

---

## D021 — TRIBE-v2 synthetic brain targets as the primary implementation line (E016) — 2026-06-12

**Decision.** Adopt Meta FAIR's **TRIBE v2** brain foundation model (`facebook/tribev2`; d'Ascoli et al.,
ICLR 2026) as the primary implementation-lane build (E016), promoted above the denizenslab full-FT door.
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
