#!/usr/bin/env node
// Section review swarm generator (v3.1) — folds Section-3 learnings into prompts and process.
// Lineage: v1 ran Section 2 (9 children, /tmp/s2-swarm.js), v2 ran Section 3 (17 children,
// /tmp/s3-swarm.js + /tmp/s3-round2.js + /tmp/s3-round2-judge.js). v3 added ID contracts,
// ROUTE-EVIDENCE, strict judge format. v3.1 (Erfan, 2026-08-28): dual-model workers
// (deepseek-v4-flash + glm-5.3-flash, one analyst AND one counter per scope per model)
// and triple judges (deepseek-v4-pro, kimi-k3, glm-5.3).
//
// Usage (from repo root):
//   node .claude/scripts/section_swarm.js 4                    → /tmp/s4-swarm.js      (round-1 workflow)
//   node .claude/scripts/section_swarm.js 4 --round2           → /tmp/s4-round2.js     (blind-reviewer workflow, run AFTER parent applies)
//   node .claude/scripts/section_swarm.js 4 --round2-judge F   → /tmp/s4-round2-judge.js (resolution judge; F = findings file)
//   node .claude/scripts/section_swarm.js 4 --verify OUT      → re-extract live text, compare sha256 with OUT's embed
//
// Then launch: subagent tool, workflowScriptPath=/tmp/s4-swarm.js, async:true.
// Section text is extracted from the LIVE file at generation time (v2 upgrade 1) and its
// sha256 is stamped in the emitted header; --verify re-checks it at any later moment.

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "..", "..");
const sha256 = (s) =>
  crypto.createHash("sha256").update(s, "utf8").digest("hex");

// ---------------------------------------------------------------------------
// Shared prompt blocks (stable across sections; settled phrasings grow per review)
// ---------------------------------------------------------------------------

const SHARED = {
  thesisCtx: `THESIS CONTEXT. MSc thesis: does the linear mapping between LLM middle layers and recorded human brain activation (fMRI, via encoding models) form a usable training signal, tested by brain-alignment-guided distillation? Endpoint: inconclusive; the contribution is controlled measurement plus an evidence framework that separates supported results, claims not demonstrated, unresolved questions, and comparisons that cannot attribute a difference to brain-response content. The thesis must NOT overclaim (no "from measurement to application" promise) and NOT over-negate (it does not show brain responses can never help).`,

  profLessons: `PROFESSOR FEEDBACK, MINED LESSONS (apply to every paragraph):
1. No undefined coinage before its definition: every sentence a first-time expert reader meets must parse without forward references; gloss coined compounds in plain language at first use.
2. Promises must match delivery: calibrate claims to what the thesis actually delivers.
3. Repeated numbers must render from one source (the \\result{...} macros from numbers.tex); never propose replacing a macro with a literal number; never restate a superseded count.
4. Layout polish is part of review (one-word paragraph endings, overfull lines) — flag only; the parent handles layout.
5. Clarity standard: precise, neat, one message per unit.
6. Structure is approved: do NOT propose restructuring, reordering, merging, or splitting paragraphs. Prose- and polish-level only.`,

  claudio: `ADDITIONAL DEFECT CLASSES FROM A SECOND SUPERVISOR (Claudio):
A. Storytelling register: sentences that give agency/stakes to abstractions (a question "earns", a manuscript "reports", an idea "locates"). The thesis is a scientific document, not a story.
B. Unmotivated passive voice: passive that loses the agent for no reason ("Alignment is measured..." -> "We assess..."). Keep passive only where the agent is genuinely irrelevant or unknown, or where the field's assay is being defined.`,

  settled: `SETTLED PHRASINGS FROM SECTIONS 1-3 (unify with them, do not reintroduce variants):
- "controlled brain predictivity" is THE canonical term, glossed at first use in Section 1.
- "nuisance features (simple stimulus properties such as position and length)".
- "the controlled-predictivity prerequisite was unstable across technical seeds" — never "technically unstable".
- "Feature-distillation and LUPI research support this possibility"; "an auxiliary target can produce a similar improvement for reasons unrelated to whether it contains information about brain responses".
- Numbered inline claims "(1)\\ ...(2)\\ ...(3)\\ ..." for claim lists of three.
- "the training target, after compression to 50 principal components" (process visible, not "the exact 50-component training target").
- "On the practical endpoint, the downstream task where a brain-specific advantage should pay off" — "practical endpoint" kept but glossed at first use.
- Active voice with "we" where the agent is the authors; author design decisions (prespecifications, exclusions, status applications) are never demoted to agent-less passive.
- From Section 2: "brain-response training data per participant"; "Post-training target uptake and retained-student movement" (keep "Post-training"); antecedent "training with these responses" (name what varies); "components used only during training"; "This flexibility allows brain-response targets to serve as privileged information"; "(the permuted-response control)" anchored at the operational definition.
- From Section 3: "evidence criteria" is the canonical concept name (renamed from "evidence standard"; internal label sec:evidence-criteria). Coined compounds carry a plain-language gloss at first use (design tuple, saved students, fresh readouts, cellwise, derangement, duplicate-extraction noise, matched analysis cell, mde). Indices and symbols are declared at first use. "routes" in prose; "lane" is a tikz-internal style name only. No "substrate": write "the same sentences", "continuous story stimuli". Seeds combined for stability are stated separately from the inference unit. Table math uses the table's $...$ delimiter convention.`,

  roleTerms: `FIXED ROLE TERMS (the manuscript's contract; NEVER rename, NEVER introduce variants; Section 4 applies them, so usage sentences are load-bearing):
recorded-response route, synthetic-response route, ordinary KD arm, permuted-response control, frozen row-twin control, text-derived auxiliary(-control) arm/target, controlled brain predictivity, practical endpoint, target uptake, retained-student movement, biological transfer, evidence criteria, continuation rule, route-specific headroom, matched analysis cell, the target-projection assay (short form of the 50-component linear target-projection assay), the naturalistic assay (short form of the controlled naturalistic voxelwise predictivity assay).
NAMING POLICY (settled 2026-08-28): full contract names are reserved for first use in Section 2, Table 1, and the abstract; the operative short forms above are used everywhere else. Normalize any later full-form occurrence to the declared short form — this is settled policy, not a deferred split.`,

  deferred: `DEFERRED REPO-WIDE SPLITS (do NOT resolve in this section; if you encounter them, FLAG in your closing summary only, never propose a change):
- "brain-response-specific attribution" (prose) vs "brain-response-content attribution" (figure node, abstract) — pending global settlement.
- "brain-specific benefit" is a Section 6 item (unify to "brain-specific training advantage" when Section 6 is reviewed); flag, do not fix here.`,

  hard: `HARD CONSTRAINTS ON EVERY PROPOSAL:
- Keep all LaTeX intact: \\ac{...}, \\autocite{...}, \\textcite{...}, \\ref{...}, \\emph{...}, \\label{...}, math \\(...\\), \\result{...} macros. Keep % \\evd{...} comments untouched. No em dashes. No reordering of paragraphs, sentences, table rows, or figure nodes.
- A proposal must never change the epistemic verdict of a sentence (supported / not demonstrated / unresolved / non-identifying / not established).
- Prefer the smallest diff that fixes the defect. Do not propose a rewrite when a one-phrase fix suffices. If a paragraph is already good, say CLEAN — churn is a defect.
- Do not propose changes to tikzpicture node code (already audited). Table cell text, figure captions, and prose are in scope.`,
};

// ---------------------------------------------------------------------------
// Per-section config. Add an entry when its turn comes in the 01→07 + appendices review.
// scopes: anchor must match a \\subsection{...} line verbatim (asserted at generation).
// routing.workers: one analyst AND one counter-reviewer per scope per worker model.
// routing.judges: every judge sees the identical full bundle (decorrelated providers).
// ---------------------------------------------------------------------------

const SECTIONS = {
  4: {
    file: "docs/manuscript/submission/sections/04_results.tex",
    label: "Section 4 (Results)",
    routing: {
      workers: [
        { tag: "ds", id: "deepseek/deepseek-v4-flash" },
        { tag: "glm", id: "ollama-cloud/glm-5.3-flash" },
      ],
      judges: [
        { tag: "deepseek", id: "deepseek/deepseek-v4-pro:medium" },
        { tag: "kimi", id: "kimi-coding/k3" },
        { tag: "glm", id: "ollama-cloud/glm-5.3" },
      ],
    },
    criteria: `(d) number fidelity: every estimate must render through \\result{...} macros and carry its uncertainty and the named test (the three-technical-seed convention); flag literal numbers, missing uncertainty, or missing test names;
(e) verdict fidelity: every status sentence must preserve the owning experiment record's epistemic verdict (supported / not demonstrated / unresolved / non-identifying); never propose strengthening or weakening a verdict, and flag any status sentence whose wording could read stronger or weaker than the record;
(f) consistency: counts and names repeated across prose, table cells, and captions within this text must agree; flag any mismatch;
(g) precision and scope: flag any wording whose simplification would change a scoped claim; flag interpretation or mechanism sentences (Results states what was observed; interpretation belongs to the Discussion) rather than rewriting them.`,
    rules: `SECTION-4-SPECIFIC RULES (this is the Results section):
- Status sentences are verdict-fidelity-critical: each must match the owning experiment record. If a status sentence could be read differently from its \\evd record, FLAG it for the parent instead of proposing prose.
- All numbers render through \\result{...} macros (single source, numbers.tex). Never introduce a literal number; flag any literal that should be a macro.
- Specific estimates carry uncertainty and the named test. Flag an estimate reported without its uncertainty or test name.
- Counts must agree across prose, tables, and figure captions visible in this text (a past defect: a figure annotated 55 checks where the table recorded 37).
- No new interpretation: do not propose adding mechanism stories or implications; flag interpretation sentences for the parent.
- Table cell text and captions are in scope; tikz code is out of scope.`,
    guardian: `You are the guardian of precision: this is a Results section, so a smoother sentence that blurs a reported estimate, its uncertainty, its test, or its verdict is WORSE even if it reads better.`,
    scopes: [
      {
        key: "pre41",
        anchor:
          "\\subsection{Controlled brain predictivity under regional and naturalistic assays}",
        scope: `the section preamble (from \\section{Results} up to subsection 4.1) AND subsection 'Controlled brain predictivity under regional and naturalistic assays' (including any table cell text and captions; not tikz code). Number prose paragraphs P1.. in order across preamble then subsection.`,
      },
      {
        key: "s42",
        anchor:
          "\\subsection{Observed distillation headroom and its association with language quality}",
        scope: `subsection 'Observed distillation headroom and its association with language quality' (including any table cell text and captions; not tikz code). Number prose paragraphs P1.. in order.`,
      },
      {
        key: "s43",
        anchor:
          "\\subsection{Recorded-response intervention at valid inference units}",
        scope: `subsection 'Recorded-response intervention at valid inference units' (including any table cell text and captions; not tikz code). Number prose paragraphs P1.. in order.`,
      },
      {
        key: "s44",
        anchor:
          "\\subsection{Measurability of the 50-component linear target projection}",
        scope: `subsection 'Measurability of the 50-component linear target projection' (including any table cell text and captions; not tikz code). Number prose paragraphs P1.. in order.`,
      },
      {
        key: "s45",
        anchor:
          "\\subsection{Synthetic-response manipulation checks and attribution status}",
        scope: `subsection 'Synthetic-response manipulation checks and attribution status' (including any table cell text and captions; not tikz code). Number prose paragraphs P1.. in order.`,
      },
      {
        key: "s46",
        anchor: "\\subsection{Saved-student biological-transfer assays}",
        scope: `subsection 'Saved-student biological-transfer assays' (including any table cell text and captions; not tikz code). Number prose paragraphs P1.. in order.`,
      },
      {
        key: "s47",
        anchor: "\\subsection{Practical-utility evaluation}",
        scope: `subsection 'Practical-utility evaluation' (including any table cell text and captions; not tikz code). Number prose paragraphs P1.. in order.`,
      },
    ],
  },
};

// ---------------------------------------------------------------------------
// Build
// ---------------------------------------------------------------------------

function extractSection(cfg) {
  const full = fs.readFileSync(path.join(ROOT, cfg.file), "utf8");
  for (const s of cfg.scopes) {
    const hits = full.split(s.anchor).length - 1;
    if (hits !== 1)
      throw new Error(
        `anchor for scope ${s.key} found ${hits} times (expected 1): ${s.anchor}`,
      );
  }
  return full;
}

function buildContext(cfg) {
  return [
    SHARED.thesisCtx,
    SHARED.profLessons,
    SHARED.claudio,
    SHARED.settled,
    SHARED.roleTerms,
    SHARED.deferred,
    cfg.rules,
    SHARED.hard,
  ].join("\n\n");
}

function stamp(label, text, kind) {
  return `// ${label} ${kind} — generated ${new Date().toISOString()} by .claude/scripts/section_swarm.js (v3.1)
// Live-text embed sha256: ${sha256(text)}  (verify: node .claude/scripts/section_swarm.js 4 --verify <this file>)
// Review-only children: no file edits. The parent applies accepted changes.
`;
}

function emitRound1(cfg, text) {
  const CONTEXT = buildContext(cfg);
  const L = cfg.label;
  if (!cfg.routing || !cfg.routing.workers || !cfg.routing.judges) {
    throw new Error("section config needs routing.workers and routing.judges");
  }
  return `${stamp(L, text, "review swarm (round 1)")}
const SECTION = ${JSON.stringify(text)};
const CONTEXT = ${JSON.stringify(CONTEXT)};
const SUBS = ${JSON.stringify(
    cfg.scopes.map(({ key, scope }) => ({ key, scope })),
    null,
    0,
  )};
const CRITERIA = ${JSON.stringify(cfg.criteria)};
const WORKERS = ${JSON.stringify(cfg.routing.workers)};
const JUDGES = ${JSON.stringify(cfg.routing.judges)};

function analystPrompt(sub, w) {
  return CONTEXT + "\\n\\nYOUR TASK. You are analyst '" + w.tag + "' reviewing ONE part of ${L} of the thesis, paragraph by paragraph, with the whole section below for context. Review ONLY: " + sub.scope + "\\n\\n" +
  "Give every finding a unique ID: " + sub.key + "-" + w.tag + "-P<paragraph>.<k> (k = 1, 2, ... within that paragraph). Counter-reviewers and judges will refer to these IDs; a malformed ID cannot be applied.\\n\\n" +
  "For EVERY paragraph in scope, judge:\\n(a) readability and flow for a first-time expert reader;\\n(b) term first-use: any coined compound used before a plain-language gloss (in this section or Sections 1-3);\\n(c) supervisor defect classes A and B;\\n" +
  CRITERIA + "\\n\\n" +
  "OUTPUT FORMAT (plain text, no markdown headers): one block per finding:\\n" +
  "ID: " + sub.key + "-" + w.tag + "-P<n>.<k> TYPE=<term-first-use|storytelling|passive|readability|flow|number-fidelity|verdict-fidelity|consistency|precision|design-fact> SEVERITY=<high|med|low>\\n" +
  "QUOTE: <verbatim fragment from the text>\\n" +
  "PROBLEM: <one sentence>\\n" +
  "PROPOSAL: <exact replacement LaTeX text, or NONE-keep>\\n" +
  "RATIONALE: <one sentence>\\n" +
  "If a paragraph has no defect write: " + sub.key + "-" + w.tag + "-P<n> CLEAN.\\n" +
  "TYPE=design-fact marks any proposal that asserts, removes, or changes a design fact (arm inventories, grid or corpus values, seed counts, declared rules or tolerances, what a control permutes or matches). Raise them; they will be verified against experiment records, not judged as prose.\\n" +
  "Close with: TOP3: the three highest-value changes in your scope. Then FLAG-LINE: any deferred repo-wide split you encountered (or 'none').\\n" +
  "DO NOT EDIT ANY FILE; you have no file access; your output is your only product.\\n\\n" +
  "FULL SECTION TEXT FOLLOWS:\\n\\n" + SECTION;
}

// ---- Phase 1: one analyst per scope per worker model, all in parallel ----
const analystRuns = [];
SUBS.forEach(s => WORKERS.forEach(w => analystRuns.push({ key: "a-" + s.key + "-" + w.tag, agent: "reviewer", model: w.id, task: analystPrompt(s, w) })));
const analystResults = await runs.all(analystRuns);
const analystOut = {};
SUBS.forEach((s, si) => {
  analystOut[s.key] = {};
  WORKERS.forEach((w, wi) => {
    const r = analystResults[si * WORKERS.length + wi];
    analystOut[s.key][w.tag] = (typeof r === "string" ? r : (r && (r.output || r.result)) || JSON.stringify(r)).slice(0, 12000);
  });
});
emit("PHASE1 DONE: " + SUBS.map(s => s.key + "(" + WORKERS.map(w => w.tag + "=" + analystOut[s.key][w.tag].length).join(",") + "ch)").join(" "));

function counterPrompt(sub, w) {
  const merged = WORKERS.map(x => "--- ANALYST " + x.tag + " PROPOSALS ---\\n" + analystOut[sub.key][x.tag]).join("\\n\\n");
  return CONTEXT + "\\n\\nYOUR TASK. You are adversarial counter-reviewer '" + w.tag + "' for: " + sub.scope + "\\n\\n" +
  "Two independent analysts proposed the changes below, each item with a unique ID. Give a verdict for EVERY proposal ID from BOTH analysts, and catch defects they both missed. ${cfg.guardian}\\n\\n" +
  "For EACH proposal give:\\n" +
  "ID: <the proposal's ID>\\n" +
  "VERDICT: IMPROVE | WORSEN | UNCLEAR\\n" +
  "ARGUMENT: 1-3 sentences (name the exact failure if WORSEN: precision loss, term-contract break, design-fact loss, verdict drift, register drop, churn, meaning drift).\\n" +
  "FINAL TEXT (only if you propose a modified version that fixes the same defect more safely).\\n\\n" +
  "Then add: MISSED: up to 3 defects both analysts missed in this scope, same block format, with fresh IDs " + sub.key + "-" + w.tag + "-M<k> (or 'none').\\n" +
  "DO NOT EDIT ANY FILE; your output is your only product.\\n\\n" +
  "FULL SECTION TEXT (context):\\n\\n" + SECTION + "\\n\\nALL PROPOSALS FOR YOUR SCOPE:\\n\\n" + merged;
}

// ---- Phase 2: one counter-reviewer per scope per worker model, all in parallel ----
const counterRuns = [];
SUBS.forEach(s => WORKERS.forEach(w => counterRuns.push({ key: "c-" + s.key + "-" + w.tag, agent: "reviewer", model: w.id, task: counterPrompt(s, w) })));
const counterResults = await runs.all(counterRuns);
const counterOut = {};
SUBS.forEach((s, si) => {
  counterOut[s.key] = {};
  WORKERS.forEach((w, wi) => {
    const r = counterResults[si * WORKERS.length + wi];
    counterOut[s.key][w.tag] = (typeof r === "string" ? r : (r && (r.output || r.result)) || JSON.stringify(r)).slice(0, 12000);
  });
});
emit("PHASE2 DONE: " + SUBS.map(s => s.key + "(" + WORKERS.map(w => w.tag + "=" + counterOut[s.key][w.tag].length).join(",") + "ch)").join(" "));

// ---- Phase 3: every judge sees the identical bundle (decorrelated providers, in parallel) ----
const jBundle = SUBS.map(s => {
  const inner = WORKERS.map(w => "\\n--- ANALYST " + w.tag + " PROPOSALS ---\\n" + analystOut[s.key][w.tag] + "\\n--- COUNTER " + w.tag + " VERDICTS ---\\n" + counterOut[s.key][w.tag]).join("\\n");
  return "\\n\\n########## SCOPE " + s.key + " (" + s.scope + ") ##########" + inner;
}).join("");
const judgeBody = CONTEXT +
  "\\n\\nYOUR TASK. You are an independent judge for a revision of ${L} of the thesis. Below, for each scope, are proposals from two independent analysts and verdicts from two adversarial counter-reviewers; every item carries a unique ID (scope-workertag-P...). Different analysts may independently flag the same defect under different IDs; output one decision block per ID anyway (identical FINAL TEXTs are fine; note the overlap in WHY).\\n" +
  "Output EXACTLY one decision block per ID, in the order IDs first appear, and nothing before the first block:\\n" +
  "ID: <id>\\n" +
  "DECISION: APPLY | REJECT | MODIFY | ROUTE-EVIDENCE\\n" +
  "FINAL TEXT: (APPLY/MODIFY only) the exact replacement LaTeX text; for MODIFY give your safer version.\\n" +
  "WHY: one sentence.\\n" +
  "Rules: prefer precision-preserving improvements; REJECT churn (stylistic swaps with no readability win) and anything that blurs a reported estimate or verdict, renames a fixed role term, violates the settled naming policy, resolves a deferred repo-wide split, or changes an epistemic verdict. Reject proposals touching tikz node code. ROUTE-EVIDENCE: if an item's correctness depends on a design fact (arm inventories, grid or corpus values, seed counts, declared rules, what a control permutes or matches), do NOT adjudicate it and do NOT write FINAL TEXT; name in WHY the experiment record or appendix that must verify it. When reviewers disagree, side with the one whose argument protects scientific precision, unless the readability gain is large and precision-neutral.\\n" +
  "After all blocks close with: CLOSING SUMMARY: counts per decision and any cross-scope consistency issues you spotted (e.g. two scopes proposing different wording for the same term).\\n" +
  "Your entire output must consist of the decision blocks plus the closing summary. No preamble, no other sections.\\n\\n" +
  "FULL SECTION TEXT (context):\\n\\n" + SECTION + jBundle;

const judgeResults = await runs.all(JUDGES.map(j => ({ key: "judge-" + j.tag, agent: "reviewer", model: j.id, task: judgeBody })));
const judges = {};
JUDGES.forEach((j, i) => {
  const r = judgeResults[i];
  judges[j.tag] = (typeof r === "string" ? r : (r && (r.output || r.result)) || JSON.stringify(r)).slice(0, 25000);
});
emit("PHASE3 DONE: " + JUDGES.map(j => j.tag + "=" + judges[j.tag].length + "ch").join(", "));

return { analyst: analystOut, counter: counterOut, judges: judges };
`;
}

function emitRound2(cfg, text) {
  const CONTEXT = buildContext(cfg);
  return `${stamp(cfg.label, text, "round-2 blind review")}
const SECTION = ${JSON.stringify(text)};
const CONTEXT = ${JSON.stringify(CONTEXT)};
const task = CONTEXT + "\\n\\nYOUR TASK. You are a fresh-eyes reviewer for ${cfg.label} of the thesis. You have NOT seen any earlier version; read the section below cold, as a first-time expert reader would, and report any REMAINING defects in readability, flow, term first-use, register (storytelling/passive), number fidelity, verdict fidelity, or precision. This is a FINAL residual-defect sweep, so do not manufacture findings: a mostly-clean section is the expected outcome.\\n\\n" +
  "OUTPUT FORMAT: one block per finding, numbered R2-<k> (k = 1, 2, ...):\\n" +
  "ID: R2-<k> TYPE=<term-first-use|storytelling|passive|readability|flow|number-fidelity|verdict-fidelity|consistency|precision> SEVERITY=<high|med|low>\\n" +
  "QUOTE: <verbatim fragment>\\n" +
  "PROBLEM: <one sentence>\\n" +
  "PROPOSAL: <exact replacement LaTeX text, or NONE-keep>\\n" +
  "RATIONALE: <one sentence>\\n" +
  "Close with: FLAG-LINE: any deferred repo-wide split you encountered (or 'none'). If the section is clean, say so.\\n" +
  "DO NOT EDIT ANY FILE; your output is your only product.\\n\\n" +
  "FULL SECTION TEXT FOLLOWS:\\n\\n" + SECTION;

const r = await runs.run("round2-blind", { agent: "reviewer", task });
const out = (typeof r === "string" ? r : (r && (r.output || r.result)) || JSON.stringify(r));
emit("ROUND2 DONE: " + out.length + "ch");
return { round2: out };
`;
}

function emitRound2Judge(cfg, text, findings) {
  const CONTEXT = buildContext(cfg);
  return `${stamp(cfg.label, text, "round-2 resolution judge")}
// One judge (deepseek-v4-pro, repo access) adjudicates the blind reviewer's residual findings
// against the live files. Parent applies only APPLY/MODIFY after its own review.
const CONTEXT = ${JSON.stringify(`You are the resolution judge for a round-2 residual-defect sweep of ${cfg.label} of an MSc thesis on brain-alignment-guided distillation. A fresh-eyes reviewer read the REVISED section cold and reported findings. You have repo access: verify every QUOTE against the live file ${cfg.file} and any appendix (docs/manuscript/submission/sections/B_data_targets_preprocessing.tex, C_training_architecture.tex, D_estimators_inference.tex, E_secondary_experiments.tex, F_sensitivities_tables.tex) or figure (docs/manuscript/submission/figures/*.tikz) before deciding.\\n\\n${CONTEXT}`)};

const FINDINGS = ${JSON.stringify(findings)};

const task = CONTEXT + "\\n\\nFINDINGS TO ADJUDICATE (verbatim from the round-2 reviewer):\\n\\n" + FINDINGS + "\\n\\n" +
  "For EACH finding output one block:\\n" +
  "ID: <the finding's ID>\\n" +
  "DECISION: APPLY | REJECT | MODIFY | OWNER-CONFIRM\\n" +
  "FINAL TEXT: (APPLY/MODIFY only) the exact replacement LaTeX, verified against the live files.\\n" +
  "WHY: one sentence, citing the file or record you verified against.\\n" +
  "OWNER-CONFIRM: for anything that needs a design decision only Erfan can make (naming policy, scope of a defined family, a declared tolerance) — never settle it yourself.\\n" +
  "Your entire output must consist of these blocks. No preamble.";

const r = await runs.run("round2-judge", { agent: "reviewer", model: "deepseek/deepseek-v4-pro:medium", task });
const out = (typeof r === "string" ? r : (r && (r.output || r.result)) || JSON.stringify(r));
emit("ROUND2-JUDGE DONE: " + out.length + "ch");
return { verdicts: out };
`;
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function main() {
  const [secArg, mode, arg3] = process.argv.slice(2);
  const n = parseInt(secArg, 10);
  if (!SECTIONS[n]) {
    console.error(
      `No config for section ${secArg}. Configured: ${Object.keys(SECTIONS).join(", ")}`,
    );
    console.error(
      "Add an entry to SECTIONS in .claude/scripts/section_swarm.js when its review turn comes.",
    );
    process.exit(1);
  }
  const cfg = SECTIONS[n];
  const text = extractSection(cfg);

  if (mode === "--verify") {
    const target = fs.readFileSync(arg3, "utf8");
    const m = target.match(/Live-text embed sha256: ([0-9a-f]{64})/);
    const live = sha256(text);
    if (!m) {
      console.error(`No sha256 stamp found in ${arg3}`);
      process.exit(1);
    }
    console.log(`live: ${live}`);
    console.log(`embed: ${m[1]}`);
    console.log(
      live === m[1]
        ? "MATCH — embedded text is byte-identical to the live file"
        : "MISMATCH — regenerate before launching",
    );
    process.exit(live === m[1] ? 0 : 2);
  }

  let outPath, out;
  if (mode === "--round2") {
    outPath = `/tmp/s${n}-round2.js`;
    out = emitRound2(cfg, text);
  } else if (mode === "--round2-judge") {
    if (!arg3 || !fs.existsSync(arg3)) {
      console.error(`findings file missing: ${arg3}`);
      process.exit(1);
    }
    outPath = `/tmp/s${n}-round2-judge.js`;
    out = emitRound2Judge(cfg, text, fs.readFileSync(arg3, "utf8"));
  } else {
    outPath = `/tmp/s${n}-swarm.js`;
    out = emitRound1(cfg, text);
  }
  fs.writeFileSync(outPath, out);
  console.log(`wrote ${outPath} (${out.length} bytes)`);
  console.log(`section: ${cfg.file} | sha256: ${sha256(text)}`);
  console.log(`scopes: ${cfg.scopes.map((s) => s.key).join(", ")}`);
  if (cfg.routing) {
    console.log(
      `workers: ${cfg.routing.workers.map((w) => `${w.tag}=${w.id}`).join(", ")}`,
    );
    console.log(
      `judges: ${cfg.routing.judges.map((j) => `${j.tag}=${j.id}`).join(", ")}`,
    );
  }
}

main();
