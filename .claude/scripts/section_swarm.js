#!/usr/bin/env node
// Section review swarm generator (v3.3) — reliability hardening after Sections 2-4.
// Lineage: v1 ran Section 2, v2 ran Section 3, v3.1 ran Section 4, and v3.2
// hardened routing, phase gates, exact anchors, and neutral round two. v3.3 keeps
// evidence-grounded editorial repairs out of the owner-confirm route.
//
// Usage (from repo root):
//   node .claude/scripts/section_swarm.js 4                    → /tmp/s4-swarm.js      (round-1 workflow)
//   node .claude/scripts/section_swarm.js 4 --round2           → /tmp/s4-round2.js     (blind-reviewer workflow, run AFTER parent applies)
//   node .claude/scripts/section_swarm.js 4 --round2-judge F   → /tmp/s4-round2-judge.js (resolution judge; F = findings file)
//   node .claude/scripts/section_swarm.js 4 --verify OUT      → re-extract live text, compare sha256 with OUT's embed
//   node .claude/scripts/section_swarm.js --selftest          → generate every mode and assert contracts/routing
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

  settled: `SETTLED PHRASINGS FROM SECTIONS 1-4 (unify with them, do not reintroduce variants):
- "controlled brain predictivity" is THE canonical term, glossed at first use in Section 1.
- "nuisance features (simple stimulus properties such as position and length)".
- "the controlled-predictivity prerequisite was unstable across technical seeds" — never "technically unstable".
- "Feature-distillation and LUPI research support this possibility"; "an auxiliary target can produce a similar improvement for reasons unrelated to whether it contains information about brain responses".
- Numbered inline claims "(1)\\ ...(2)\\ ...(3)\\ ..." for claim lists of three.
- "the training target, after compression to 50 principal components" (process visible, not "the exact 50-component training target").
- "On the practical endpoint, the downstream task where a brain-specific advantage should pay off" — "practical endpoint" kept but glossed at first use.
- Active voice with "we" where the agent is the authors; author design decisions (prespecifications, exclusions, status applications) are never demoted to agent-less passive.
- From Section 2: "brain-response training data per participant"; "Post-training target uptake and retained-student movement" (keep "Post-training"); antecedent "training with these responses" (name what varies); "components used only during training"; "This flexibility allows brain-response targets to serve as privileged information"; "(the permuted-response control)" anchored at the operational definition.
- From Section 3: "evidence criteria" is the canonical concept name (renamed from "evidence standard"; internal label sec:evidence-criteria). Coined compounds carry a plain-language gloss at first use (design tuple, saved students, fresh readouts, cellwise, derangement, duplicate-extraction noise, matched analysis cell, mde). Indices and symbols are declared at first use. "routes" in prose; "lane" is a tikz-internal style name only. No "substrate": write "the same sentences", "continuous story stimuli". Seeds combined for stability are stated separately from the inference unit. Table math uses the table's $...$ delimiter convention.
- From Section 4: use "Bonferroni family-95% interval" for the E030 interval and preserve the manuscript-wide contract phrase "declared linear pathway". Status wording follows the owning experiment record exactly; unresolved results are never restated as demonstrated nulls.`,

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
    number: 4,
    file: "docs/manuscript/rewrite/sections/04_results.tex",
    label: "Section 4 (Results)",
    routing: {
      // Erfan 2026-08-29: only kimi-k3 and deepseek-v4-flash (glm cloud children proved
      // unreliable: one judge died on the 32k output cap, one counter derailed).
      workers: [
        { tag: "ds", id: "deepseek/deepseek-v4-flash:medium" },
        { tag: "kimi", id: "kimi-coding/k3:medium" },
      ],
      judges: [
        { tag: "kimi", id: "kimi-coding/k3:high" },
        { tag: "ds", id: "deepseek/deepseek-v4-flash:high" },
      ],
      round2: { id: "deepseek/deepseek-v4-flash:medium" },
      round2Judge: { id: "kimi-coding/k3:high" },
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
  5: {
    number: 5,
    file: "docs/manuscript/rewrite/sections/05_discussion.tex",
    label: "Section 5 (Discussion)",
    routing: {
      workers: [
        { tag: "ds", id: "deepseek/deepseek-v4-flash:medium" },
        { tag: "kimi", id: "kimi-coding/k3:medium" },
      ],
      judges: [
        { tag: "kimi", id: "kimi-coding/k3:high" },
        { tag: "ds", id: "deepseek/deepseek-v4-flash:high" },
      ],
      round2: { id: "deepseek/deepseek-v4-flash:medium" },
      round2Judge: { id: "kimi-coding/k3:high" },
    },
    criteria: `(d) inference fidelity: every interpretation must remain inside the owning E-record verdict and distinguish observation from hypothesis;
(e) route fidelity: recorded-response and synthetic-response evidence must not be merged into one causal sequence or one utility claim;
(f) prior-work scope: compatibility claims may identify design and estimand non-equivalence but must not claim which difference caused divergent outcomes;
(g) recommendation scope: design implications must remain conditional recommendations from the observed diagnostic pattern, never experimentally validated universal rules.`,
    rules: `SECTION-5-SPECIFIC RULES (this is the Discussion):
- Preserve the separation among measurement, manipulation, attribution, biological transfer, and utility. A smoother sentence that collapses stages is a defect.
- Interpret only recorded results. Do not add mechanisms, causal explanations, or universal-null claims.
- Positive prior studies may be described as design-non-equivalent; do not adjudicate them from this thesis.
- Recommendations must preserve their conditions, inference unit, comparator, endpoint, and tested route.
- Structural or scientific-scope concerns are FLAG-only here because a separate argument review precedes this prose swarm.`,
    guardian: `You are the guardian of inference: this is a Discussion section, so readability never justifies converting a conditional interpretation into a causal explanation, universal claim, or stronger verdict.`,
    scopes: [
      {
        key: "pre51",
        anchor:
          "\\subsection{Where support is lost across the two intervention routes}",
        scope: `the section preamble AND subsection 'Where support is lost across the two intervention routes'. Number prose paragraphs P1.. in order across the preamble then subsection.`,
      },
      {
        key: "s52",
        anchor: "\\subsection{Compatibility with positive prior studies}",
        scope: `subsection 'Compatibility with positive prior studies'. Number prose paragraphs P1.. in order.`,
      },
      {
        key: "s53",
        anchor:
          "\\subsection{Design implications for future brain-response-guided training}",
        scope: `subsection 'Design implications for future brain-response-guided training'. Number prose paragraphs P1.. in order.`,
      },
    ],
  },
};

// ---------------------------------------------------------------------------
// Build
// ---------------------------------------------------------------------------

function ownerPreferenceSurface(text) {
  const terms = ["substrate", "standard", "naturalistic", "assay", "leverage"];
  const hits = [];
  text.split(/\n\s*\n/).forEach((paragraph, index) => {
    const counts = terms
      .map((term) => {
        const n = (
          paragraph.toLowerCase().match(new RegExp(`\\b${term}\\w*\\b`, "g")) ||
          []
        ).length;
        return n ? `${term}=${n}` : null;
      })
      .filter(Boolean);
    if (counts.length) hits.push(`P${index + 1}: ${counts.join(", ")}`);
  });
  return `REGISTER-WORD PRE-PASS (attention hints, not automatic defects):\n${
    hits.length ? hits.join("\n") : "no flagged register words"
  }`;
}

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

function buildContext(cfg, text) {
  return [
    SHARED.thesisCtx,
    SHARED.profLessons,
    SHARED.claudio,
    SHARED.settled,
    SHARED.roleTerms,
    SHARED.deferred,
    ownerPreferenceSurface(text),
    cfg.rules,
    SHARED.hard,
  ].join("\n\n");
}

function stamp(cfg, text, kind) {
  return `// ${cfg.label} ${kind} — generated ${new Date().toISOString()} by .claude/scripts/section_swarm.js (v3.3)
// Live-text embed sha256: ${sha256(text)}  (verify: node .claude/scripts/section_swarm.js ${cfg.number} --verify <this file>)
// Review-only children: no file edits. The parent applies accepted changes to canonical rewrite first.
`;
}

function runtimeHelpers() {
  return `
function resultText(r) {
  const value = typeof r === "string" ? r : (r && (r.output || r.result)) || r;
  return typeof value === "string" ? value : JSON.stringify(value);
}
function idsIn(text) {
  const ids = [];
  const re = /^ID:\\s*(\\S+)/gm;
  let match;
  while ((match = re.exec(text)) !== null) ids.push(match[1]);
  return ids;
}
function blocksIn(text) {
  const starts = [];
  const re = /^ID:\\s*(\\S+).*$/gm;
  let match;
  while ((match = re.exec(text)) !== null) starts.push({ id: match[1], start: match.index });
  return starts.map(function (entry, index) {
    const end = index + 1 < starts.length ? starts[index + 1].start : text.length;
    return { id: entry.id, body: text.slice(entry.start, end) };
  });
}
function fieldIn(block, name) {
  const match = block.match(new RegExp("^" + name + ":\\\\s*(.*)$", "m"));
  return match ? match[1].trim() : "";
}
function exactCount(text, needle) {
  return needle ? text.split(needle).length - 1 : 0;
}
function basicError(out, minChars, maxChars, requiredTokens) {
  if (out.length < minChars) return "output too short: " + out.length + " characters";
  if (out.length > maxChars) return "output too long: " + out.length + " characters; return complete concise blocks";
  for (const token of requiredTokens) if (!out.includes(token)) return "missing required token: " + token;
  return null;
}
function coverageError(out, expectedIds, allowExtra) {
  const seen = idsIn(out);
  const missing = expectedIds.filter(function (id) { return seen.filter(function (x) { return x === id; }).length !== 1; });
  if (missing.length) return "expected exactly one block for: " + missing.join(", ");
  const extra = allowExtra ? [] : seen.filter(function (id) { return !expectedIds.includes(id); });
  return extra.length ? "unexpected decision IDs: " + Array.from(new Set(extra)).join(", ") : null;
}
function proposalError(out, liveText, requiredTokens, maxChars) {
  const basic = basicError(out, 80, maxChars, requiredTokens);
  if (basic) return basic;
  const blocks = blocksIn(out);
  if (!blocks.length) return /\\bclean\\b/i.test(out) ? null : "no finding blocks and no CLEAN verdict";
  for (const block of blocks) {
    const oldText = fieldIn(block.body, "OLD");
    const newText = fieldIn(block.body, "NEW");
    if (!oldText || !newText) return block.id + " must contain one-line OLD and NEW fields";
    if (exactCount(liveText, oldText) !== 1) return block.id + " OLD anchor must occur exactly once in the canonical section";
  }
  return null;
}
function counterError(out, expectedIds, liveText) {
  const basic = basicError(out, 80, 30000, ["MISSED:"]);
  if (basic) return basic;
  const coverage = coverageError(out, expectedIds, true);
  if (coverage) return coverage;
  for (const block of blocksIn(out).filter(function (item) { return item.id.includes("-M"); })) {
    const oldText = fieldIn(block.body, "OLD");
    const newText = fieldIn(block.body, "NEW");
    if (!oldText || !newText) return block.id + " missed finding must contain one-line OLD and NEW fields";
    if (exactCount(liveText, oldText) !== 1) return block.id + " OLD anchor must occur exactly once in the canonical section";
  }
  return null;
}
function verdictError(out, expectedIds, liveText, requiredTokens) {
  const basic = basicError(out, 80, 60000, requiredTokens);
  if (basic) return basic;
  const coverage = coverageError(out, expectedIds, false);
  if (coverage) return coverage;
  for (const block of blocksIn(out)) {
    const decision = fieldIn(block.body, "DECISION");
    if (decision === "APPLY" || decision === "MODIFY") {
      const oldText = fieldIn(block.body, "OLD");
      const newText = fieldIn(block.body, "NEW");
      if (!oldText || !newText) return block.id + " APPLY/MODIFY must contain one-line OLD and NEW fields";
      if (exactCount(liveText, oldText) !== 1) return block.id + " OLD anchor must occur exactly once in the canonical section";
    }
  }
  return null;
}
function retrySpec(run, error) {
  return {
    key: run.key + "-retry",
    agent: run.agent,
    model: run.model,
    task: run.task + "\\n\\nRETRY ONCE. Your prior output failed the mechanical gate: " + error + ". Return a complete response that follows the contract exactly.",
  };
}
`;
}

function emitRound1(cfg, text) {
  const CONTEXT = buildContext(cfg, text);
  const L = cfg.label;
  if (!cfg.routing || !cfg.routing.workers || !cfg.routing.judges) {
    throw new Error("section config needs routing.workers and routing.judges");
  }
  return `${stamp(cfg, text, "review swarm (round 1)")}
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
${runtimeHelpers()}
function analystPrompt(sub, w) {
  return CONTEXT + "\\n\\nYOUR TASK. You are analyst '" + w.tag + "' reviewing ONE part of ${L} of the thesis, paragraph by paragraph, with the whole section below for context. Review ONLY: " + sub.scope + "\\n\\n" +
  "Give every finding a unique ID: " + sub.key + "-" + w.tag + "-P<paragraph>.<k> (k = 1, 2, ... within that paragraph). Counter-reviewers and judges will refer to these IDs; a malformed ID cannot be applied.\\n\\n" +
  "For EVERY paragraph in scope, judge:\\n(a) readability and flow for a first-time expert reader;\\n(b) term first-use: any coined compound used before a plain-language gloss (in this section or Sections 1-4);\\n(c) supervisor defect classes A and B;\\n" +
  CRITERIA + "\\n\\n" +
  "OUTPUT FORMAT (plain text, no markdown headers): one block per finding:\\n" +
  "ID: " + sub.key + "-" + w.tag + "-P<n>.<k> TYPE=<term-first-use|storytelling|passive|readability|flow|number-fidelity|verdict-fidelity|consistency|precision|design-fact> SEVERITY=<high|med|low>\\n" +
  "OLD: <one exact source line that occurs once in the supplied section>\\n" +
  "NEW: <one exact replacement LaTeX source line>\\n" +
  "PROBLEM: <one sentence>\\n" +
  "RATIONALE: <one sentence>\\n" +
  "If a paragraph has no defect write: " + sub.key + "-" + w.tag + "-P<n> CLEAN.\\n" +
  "TYPE=design-fact marks any proposal that asserts, removes, or changes a design fact (arm inventories, grid or corpus values, seed counts, declared rules or tolerances, what a control permutes or matches). Raise them; they will be verified against experiment records, not judged as prose.\\n" +
  "Close with: TOP3: the three highest-value changes in your scope. Then FLAG-LINE: any deferred repo-wide split you encountered (or 'none').\\n" +
  "DO NOT EDIT ANY FILE. Use only the supplied section text even if repository-reading tools are available; never anchor on another manuscript twin. Your output is your only product.\\n\\n" +
  "FULL SECTION TEXT FOLLOWS:\\n\\n" + SECTION;
}

// ---- Phase 1: one analyst per scope per worker model, all in parallel ----
const analystRuns = [];
SUBS.forEach(s => WORKERS.forEach(w => analystRuns.push({ key: "a-" + s.key + "-" + w.tag, agent: "reviewer", model: w.id, task: analystPrompt(s, w) })));
const analystResults = await runs.all(analystRuns);
const analystTexts = analystResults.map(resultText);
let analystFailures = analystTexts.map(function (out, index) {
  return { index, error: proposalError(out, SECTION, ["TOP3:", "FLAG-LINE:"], 20000) };
}).filter(function (item) { return item.error; });
if (analystFailures.length) {
  const retryResults = await runs.all(analystFailures.map(function (item) {
    return retrySpec(analystRuns[item.index], item.error);
  }));
  retryResults.forEach(function (result, index) {
    analystTexts[analystFailures[index].index] = resultText(result);
  });
}
analystFailures = analystTexts.map(function (out, index) {
  return { index, error: proposalError(out, SECTION, ["TOP3:", "FLAG-LINE:"], 20000) };
}).filter(function (item) { return item.error; });
if (analystFailures.length) throw new Error("PHASE1 gate failed after retry: " + JSON.stringify(analystFailures));
const analystOut = {};
SUBS.forEach((s, si) => {
  analystOut[s.key] = {};
  WORKERS.forEach((w, wi) => {
    analystOut[s.key][w.tag] = analystTexts[si * WORKERS.length + wi];
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
  "If you propose a safer replacement, add OLD: <one exact source line> and NEW: <one exact replacement source line>.\\n\\n" +
  "Then add: MISSED: up to 3 defects both analysts missed in this scope (or 'none'). Each missed defect uses a fresh ID " + sub.key + "-" + w.tag + "-M<k> plus OLD, NEW, PROBLEM, and RATIONALE fields.\\n" +
  "DO NOT EDIT ANY FILE. Use only the supplied section text even if repository-reading tools are available; never anchor on another manuscript twin. Your output is your only product.\\n\\n" +
  "FULL SECTION TEXT (context):\\n\\n" + SECTION + "\\n\\nALL PROPOSALS FOR YOUR SCOPE:\\n\\n" + merged;
}

// ---- Phase 2: one counter-reviewer per scope per worker model, all in parallel ----
const counterRuns = [];
SUBS.forEach(s => WORKERS.forEach(w => counterRuns.push({ key: "c-" + s.key + "-" + w.tag, agent: "reviewer", model: w.id, task: counterPrompt(s, w) })));
const analystIds = {};
SUBS.forEach(function (s) {
  analystIds[s.key] = Array.from(new Set(WORKERS.flatMap(function (w) { return idsIn(analystOut[s.key][w.tag]); })));
});
const counterResults = await runs.all(counterRuns);
const counterTexts = counterResults.map(resultText);
let counterFailures = counterTexts.map(function (out, index) {
  const scope = SUBS[Math.floor(index / WORKERS.length)];
  return { index, error: counterError(out, analystIds[scope.key], SECTION) };
}).filter(function (item) { return item.error; });
if (counterFailures.length) {
  const retryResults = await runs.all(counterFailures.map(function (item) {
    return retrySpec(counterRuns[item.index], item.error);
  }));
  retryResults.forEach(function (result, index) {
    counterTexts[counterFailures[index].index] = resultText(result);
  });
}
counterFailures = counterTexts.map(function (out, index) {
  const scope = SUBS[Math.floor(index / WORKERS.length)];
  return { index, error: counterError(out, analystIds[scope.key], SECTION) };
}).filter(function (item) { return item.error; });
if (counterFailures.length) throw new Error("PHASE2 gate failed after retry: " + JSON.stringify(counterFailures));
const counterOut = {};
SUBS.forEach((s, si) => {
  counterOut[s.key] = {};
  WORKERS.forEach((w, wi) => {
    counterOut[s.key][w.tag] = counterTexts[si * WORKERS.length + wi];
  });
});
emit("PHASE2 DONE: " + SUBS.map(s => s.key + "(" + WORKERS.map(w => w.tag + "=" + counterOut[s.key][w.tag].length).join(",") + "ch)").join(" "));

// ---- Phase 3: every judge sees the identical bundle (decorrelated providers, in parallel) ----
const jBundle = SUBS.map(s => {
  const inner = WORKERS.map(w => "\\n--- ANALYST " + w.tag + " PROPOSALS ---\\n" + analystOut[s.key][w.tag] + "\\n--- COUNTER " + w.tag + " VERDICTS ---\\n" + counterOut[s.key][w.tag]).join("\\n");
  return "\\n\\n########## SCOPE " + s.key + " (" + s.scope + ") ##########" + inner;
}).join("");
const expectedJudgeIds = Array.from(new Set(SUBS.flatMap(function (s) {
  return WORKERS.flatMap(function (w) {
    return idsIn(analystOut[s.key][w.tag]).concat(idsIn(counterOut[s.key][w.tag]));
  });
})));
const judgeBody = CONTEXT +
  "\\n\\nYOUR TASK. You are an independent judge for a revision of ${L} of the thesis. Below, for each scope, are proposals from two independent analysts and verdicts from two adversarial counter-reviewers; every item carries a unique ID (scope-workertag-P...). Different analysts may independently flag the same defect under different IDs; output one decision block per ID anyway (identical NEW fields are fine; note the overlap in WHY).\\n" +
  "Output EXACTLY one decision block per ID, in the order IDs first appear, and nothing before the first block:\\n" +
  "ID: <id>\\n" +
  "DECISION: APPLY | REJECT | MODIFY | ROUTE-EVIDENCE\\n" +
  "OLD: (APPLY/MODIFY only) one exact source line that occurs once in the supplied section.\\n" +
  "NEW: (APPLY/MODIFY only) one exact replacement LaTeX source line; for MODIFY give your safer version.\\n" +
  "WHY: one sentence.\\n" +
  "Rules: judge anchors against the supplied canonical section, never another manuscript twin. Prefer precision-preserving improvements; REJECT churn (stylistic swaps with no readability win) and anything that blurs a reported estimate or verdict, renames a fixed role term, violates the settled naming policy, resolves a deferred repo-wide split, or changes an epistemic verdict. Reject proposals touching tikz node code. ROUTE-EVIDENCE: if an item's correctness depends on a design fact (arm inventories, grid or corpus values, seed counts, declared rules, what a control permutes or matches), do NOT adjudicate it and do NOT write OLD or NEW; name in WHY the experiment record or appendix that must verify it. When reviewers disagree, side with the one whose argument protects scientific precision, unless the readability gain is large and precision-neutral.\\n" +
  "After all blocks close with: CLOSING SUMMARY: counts per decision and any cross-scope consistency issues you spotted (e.g. two scopes proposing different wording for the same term).\\n" +
  "Your entire output must consist of the decision blocks plus the closing summary. No preamble, no other sections.\\n\\n" +
  "FULL SECTION TEXT (context):\\n\\n" + SECTION + jBundle;

const judgeRuns = JUDGES.map(j => ({ key: "judge-" + j.tag, agent: "reviewer", model: j.id, task: judgeBody }));
const judgeResults = await runs.all(judgeRuns);
const judgeTexts = judgeResults.map(resultText);
let judgeFailures = judgeTexts.map(function (out, index) {
  return { index, error: verdictError(out, expectedJudgeIds, SECTION, ["CLOSING SUMMARY:"]) };
}).filter(function (item) { return item.error; });
if (judgeFailures.length) {
  const retryResults = await runs.all(judgeFailures.map(function (item) {
    return retrySpec(judgeRuns[item.index], item.error);
  }));
  retryResults.forEach(function (result, index) {
    judgeTexts[judgeFailures[index].index] = resultText(result);
  });
}
judgeFailures = judgeTexts.map(function (out, index) {
  return { index, error: verdictError(out, expectedJudgeIds, SECTION, ["CLOSING SUMMARY:"]) };
}).filter(function (item) { return item.error; });
if (judgeFailures.length) throw new Error("PHASE3 gate failed after retry: " + JSON.stringify(judgeFailures));
const judges = {};
JUDGES.forEach((j, i) => {
  judges[j.tag] = judgeTexts[i];
});
emit("PHASE3 DONE: " + JUDGES.map(j => j.tag + "=" + judges[j.tag].length + "ch").join(", "));

return { analyst: analystOut, counter: counterOut, judges: judges };
`;
}

function emitRound2(cfg, text) {
  const CONTEXT = buildContext(cfg, text);
  if (!cfg.routing || !cfg.routing.round2) {
    throw new Error("section config needs routing.round2");
  }
  return `${stamp(cfg, text, "round-2 blind review")}
const SECTION = ${JSON.stringify(text)};
const CONTEXT = ${JSON.stringify(CONTEXT)};
const MODEL = ${JSON.stringify(cfg.routing.round2.id)};
${runtimeHelpers()}
const task = CONTEXT + "\\n\\nYOUR TASK. You are a fresh-eyes reviewer for ${cfg.label} of the thesis. You have NOT seen any earlier version. Inspect the section independently against this neutral checklist: readability, flow, term first-use, storytelling/passive register, number fidelity, verdict fidelity, consistency, and precision. Report every residual defect you find; CLEAN is acceptable only after checking every class. Do not manufacture findings.\\n\\n" +
  "OUTPUT FORMAT: one block per finding, numbered R2-<k> (k = 1, 2, ...):\\n" +
  "ID: R2-<k> TYPE=<term-first-use|storytelling|passive|readability|flow|number-fidelity|verdict-fidelity|consistency|precision|design-fact> SEVERITY=<high|med|low>\\n" +
  "OLD: <one exact source line that occurs once in the supplied section>\\n" +
  "NEW: <one exact replacement LaTeX source line>\\n" +
  "PROBLEM: <one sentence>\\n" +
  "RATIONALE: <one sentence>\\n" +
  "Close with: FLAG-LINE: any deferred repo-wide split you encountered (or 'none'). If no defects remain, state that the section is CLEAN.\\n" +
  "DO NOT EDIT ANY FILE. Use only the supplied section text even if repository-reading tools are available; never anchor on another manuscript twin. Your output is your only product.\\n\\n" +
  "FULL SECTION TEXT FOLLOWS:\\n\\n" + SECTION;

const run = { key: "round2-blind", agent: "reviewer", model: MODEL, task };
let out = resultText(await runs.run(run.key, { agent: run.agent, model: run.model, task: run.task }));
let error = proposalError(out, SECTION, ["FLAG-LINE:"], 30000);
if (error) {
  const retry = retrySpec(run, error);
  out = resultText(await runs.run(retry.key, { agent: retry.agent, model: retry.model, task: retry.task }));
}
error = proposalError(out, SECTION, ["FLAG-LINE:"], 30000);
if (error) throw new Error("ROUND2 gate failed after retry: " + error);
emit("ROUND2 DONE: " + out.length + "ch");
return { round2: out };
`;
}

function emitRound2Judge(cfg, text, findings) {
  const CONTEXT = buildContext(cfg, text);
  if (!cfg.routing || !cfg.routing.round2Judge) {
    throw new Error("section config needs routing.round2Judge");
  }
  return `${stamp(cfg, text, "round-2 resolution judge")}
// One repo-grounded judge adjudicates the blind reviewer's residual findings.
// Parent applies only APPLY/MODIFY after its own review.
const SECTION = ${JSON.stringify(text)};
const CONTEXT = ${JSON.stringify(`You are the resolution judge for a round-2 residual-defect sweep of ${cfg.label} of an MSc thesis on brain-alignment-guided distillation. A fresh-eyes reviewer read the REVISED section cold and reported findings. You have repo access: verify every OLD anchor against the canonical live file ${cfg.file} and any appendix under docs/manuscript/rewrite/sections/ or figure under docs/manuscript/rewrite/figures/ before deciding.\\n\\n${CONTEXT}`)};
const MODEL = ${JSON.stringify(cfg.routing.round2Judge.id)};
const FINDINGS = ${JSON.stringify(findings)};
${runtimeHelpers()}
const expectedIds = Array.from(new Set(idsIn(FINDINGS)));
const task = CONTEXT + "\\n\\nFINDINGS TO ADJUDICATE (verbatim from the round-2 reviewer):\\n\\n" + FINDINGS + "\\n\\n" +
  "For EACH finding output one block:\\n" +
  "ID: <the finding's ID>\\n" +
  "DECISION: APPLY | REJECT | MODIFY | OWNER-CONFIRM\\n" +
  "OLD: (APPLY/MODIFY only) one exact source line that occurs once in the canonical live section.\\n" +
  "NEW: (APPLY/MODIFY only) one exact replacement LaTeX source line.\\n" +
  "WHY: one sentence, citing the file or record you verified against.\\n" +
  "OWNER-CONFIRM: use only when the choice changes a scientific verdict or factual claim, materially changes claim scope, establishes governing terminology, makes an external commitment, or requires a subjective preference among evidence-equivalent alternatives. Evidence-grounded clarity or precision repairs that preserve scientific meaning are APPLY/MODIFY, not OWNER-CONFIRM.\\n" +
  "Your entire output must consist of these blocks. No preamble.";

const run = { key: "round2-judge", agent: "reviewer", model: MODEL, task };
let out = resultText(await runs.run(run.key, { agent: run.agent, model: run.model, task: run.task }));
let error = verdictError(out, expectedIds, SECTION, []);
if (error) {
  const retry = retrySpec(run, error);
  out = resultText(await runs.run(retry.key, { agent: retry.agent, model: retry.model, task: retry.task }));
}
error = verdictError(out, expectedIds, SECTION, []);
if (error) throw new Error("ROUND2-JUDGE gate failed after retry: " + error);
emit("ROUND2-JUDGE DONE: " + out.length + "ch");
return { verdicts: out };
`;
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function validateConfig(cfg) {
  if (!cfg.number || !cfg.file.startsWith("docs/manuscript/rewrite/")) {
    throw new Error(
      `${cfg.label}: config must identify the canonical rewrite file`,
    );
  }
  const routing = cfg.routing || {};
  const models = [
    ...(routing.workers || []).map((item) => item.id),
    ...(routing.judges || []).map((item) => item.id),
    routing.round2 && routing.round2.id,
    routing.round2Judge && routing.round2Judge.id,
  ].filter(Boolean);
  if (
    models.length < 4 ||
    models.some((id) => !/:(off|minimal|low|medium|high|xhigh|max)$/.test(id))
  ) {
    throw new Error(
      `${cfg.label}: every child model needs an explicit thinking suffix`,
    );
  }
}

function selftest() {
  const required = {
    round1: ["PHASE1 gate failed", "OLD:", "NEW:", "expectedJudgeIds"],
    round2: [
      "ROUND2 gate failed after retry",
      "model: MODEL",
      "neutral checklist",
    ],
    judge: [
      "ROUND2-JUDGE gate failed after retry",
      "OLD:",
      "NEW:",
      "canonical live file",
    ],
  };
  for (const cfg of Object.values(SECTIONS)) {
    validateConfig(cfg);
    const text = extractSection(cfg);
    const outputs = {
      round1: emitRound1(cfg, text),
      round2: emitRound2(cfg, text),
      judge: emitRound2Judge(cfg, text, "ID: R2-1\nPROBLEM: smoke test"),
    };
    for (const [mode, markers] of Object.entries(required)) {
      for (const marker of markers) {
        if (!outputs[mode].includes(marker))
          throw new Error(`${cfg.label} ${mode}: missing ${marker}`);
      }
      if (outputs[mode].includes(".slice(0,"))
        throw new Error(`${cfg.label} ${mode}: silent truncation remains`);
    }
    console.log(`PASS ${cfg.label}: ${cfg.file}`);
  }
}

function main() {
  const [secArg, mode, arg3] = process.argv.slice(2);
  if (secArg === "--selftest") {
    selftest();
    return;
  }
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
  validateConfig(cfg);
  const text = extractSection(cfg);

  if (mode === "--verify") {
    if (!arg3 || !fs.existsSync(arg3)) {
      console.error(`generated workflow missing: ${arg3}`);
      process.exit(1);
    }
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
