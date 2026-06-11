# 2026-06-11 22:57 — graphify integration (tooling session, no science)

**Mode:** tooling / infrastructure. **Touched the science: NO.** `ladder.md` and `upspeed.md`
deliberately left untouched — no rung moved, no evidence produced. This log + `tasks.md` are the record.

## What was done

Integrated **graphify** (the knowledge-graph CLI, `github.com/safishamsi/graphify`) as a code/corpus
navigator for this repo. Cloned into gitignored `data/graphify/` for source reading.

- **Installed:** `graphifyy` via `uv tool` (Python 3.12, pinned so the Leiden/graspologic extra resolves),
  extras `[gemini,pdf,office,leiden]`. CLI = `graphify 0.8.37`.
- **Skill + hosts:** `/graphify` skill into `.claude/skills/graphify/`; Antigravity rules/workflow into
  `.agents/` + `~/.gemini/config/skills/graphify/`.
- **Stripped the nag hooks:** `graphify install` also wrote PreToolUse hooks (Bash-search + Read|Glob,
  "MANDATORY run graphify before reading files") into `.claude/settings.json` — removed them; they fight
  the docs-first session ritual.
- **`.graphifyignore`** (overrides `.gitignore` for graphify only, never touches git): whole-repo scope =
  code + docs + papers; excludes datasets (lebel/pereira/tuckute), `outputs/`, the graphify clone,
  video, course-material PDFs. Proven necessary — an explicit path into gitignored `data/` returns 0
  files (graphify walks up to the git root collecting ignore rules), so the override is the only way to
  graph `data/paper-repos/`.
- **`CLAUDE.md`:** added a `## graphify` section, explicitly **subordinate** to `docs/ladder.md` + gbrain
  (navigation aid, never a number source).
- Commits: `ea22aa4` (gitignore graphify-out/), `077eef2` (integration).

## How graphify works (the mechanism, for the deep-dive later)

- **Code → tree-sitter AST, local, free, deterministic** (EXTRACTED edges, 1.0 confidence). No LLM, no
  embeddings anywhere in the tool.
- **Docs/PDFs/images → an LLM** (Gemini API if `GEMINI_API_KEY`/`GOOGLE_API_KEY` set, else host-agent
  subagents). This is the only token-costing pass.
- **Clustering = Leiden/Louvain** on the graph; **query = lexical IDF + BFS/DFS traversal**, NOT vector
  search (wording-sensitive). Opposite design to gbrain (embedding-first).

## Evaluation — usefulness & accuracy

- **Code graph: useful + accurate.** scripts/ → 185 nodes/347 edges, free; `query`/`path`/`explain`
  returned correct nodes, real `file:line`, EXTRACTED tags; captured docstrings as linked rationale
  nodes. AST is deterministic ⇒ accurate by construction. Whole-repo AST parsed 5106 code files (cached).
- **Semantic doc-graph: works, cheap, but THIN/COARSE.** `docs/` via **Gemini 3.1 Flash-Lite** =
  57 nodes/37 edges from 79 files, **$0.13**, 198K in/11K out. But it extracted ~one node *per document*
  (a file-reference map), not sub-document concepts (noise ceiling, unique-R², rate-distortion never
  became nodes). God nodes = the obvious hub docs; "surprising connections" = generic INFERRED doc-doc
  links. Edges it *did* make were accurate (run_kd_alignment→E003 EXTRACTED; E006→Hadidi INFERRED).
  Community labeling silently failed (stayed "Community N").
- **Verdict:** the **code graph is the keeper** (free, accurate, real value for navigating the 21
  external `data/paper-repos/`). The **semantic doc-graph is redundant with gbrain and worse** (gbrain
  has these docs with embeddings + true concept relations). Did NOT run the full 2500-file semantic build.

## Backend notes (hard-won)

- NDS shared Ollama (`ollama.infra.nds`, gemma4:26b-a4b-it-qat) is **unreachable from centcom** (no DNS,
  IP not routable) and gemma4 is a reasoning model → the OpenAI-shim `think` trap (empty content). Local
  Ollama not installed. So Ollama is a separate setup project, not a switch.
- Gemini **free tier trains on inputs** ("don't send proprietary/confidential") → unsafe for unpublished
  thesis content. The subscription-covered **Antigravity** agent quota (30 RPM/200K TPM/1K RPD) or a
  billing-off API key are the only acceptable Gemini paths. Flash-Lite (4M TPM/150K RPD) is the fast one.

## Open thread

- **Get to the bottom of graphify later** (see `tasks.md`): if we revisit the doc-graph, the lever is
  `--mode deep` + a stronger model (3.1 Pro), and a clear use it serves that gbrain doesn't — else the
  code-graph-only conclusion stands.
