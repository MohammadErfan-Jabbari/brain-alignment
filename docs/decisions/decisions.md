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
