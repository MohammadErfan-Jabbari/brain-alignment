# `claim-lattice.json` — the spine artifact (F15)

The single shared object every `/write` stage reads and writes. It carries the case (claims, evidence,
argument) from frame → gate → draft → audit so nothing drops between hands. The `lattice_integrity` check
(`scripts/lattice_integrity.py`) is the rigid DET floor over it.

## Top-level shape

```json
{
  "meta":        {"stage": <int 1-6>, "schema_version": "1"},
  "message":     "<one-sentence message of the paper>" | null,
  "frame":       "basic-science" | "technology" | null,
  "contribution_type": "<e.g. empirical-finding | methodological | conceptual>" | null,
  "reader_model": {"venue": "<named reader>", "old": [...], "new": [...],
                   "prior_beliefs": [...], "doubts": [...]} | null,
  "register":    {"venue": "<reader>", "exemplars": ["<section:paper>", ...]} | null,
  "claims":      [ <claim object>, ... ],
  "warrants":    [ {"from": "<claim_id>", "to": "<claim_id>", "warrant": "<text>"}, ... ],
  "figures":     [ {"figure_id": "<id>", "claim_id": "<claim_id>", "caption": "<one-line caption>", "shows": "<what the figure ACTUALLY plots — the reference F5 sizes the caption against, SC-XS-3>"}, ... ],
  "sections":    [ {"section_id": "<id>", "title": "<text>", "claim_ids": ["<claim_id>", ...]}, ... ],
  "deviation_log": [ {"functionality": "<F##>", "method": "<...>", "why": "<...>", "did": "<...>", "section_id": "<optional: the section/misfit this deviation covers — a logged entry excuses ONLY what it names>"}, ... ]
}
```

## Stage-1 fields (F2 + F1, written at stage 1; required by the gate — stage ≥ 3)

`message`, `frame`, `contribution_type` are the **F2** outputs; `reader_model` is the **F1** output. They are
optional before the gate and **required, well-formed, at stage ≥ 3** (the coupled package the human approves):
`message` is present (the *one-sentence* norm is gated by the human at F16, not a DET check — a sentence-counter
false-positives on "Sec."/"U.S."/ellipses, so it stays a judgment, per L060); `frame` ∈ {`basic-science`,
`technology`}; `contribution_type` is present; `reader_model` is an object carrying all of `venue, old, new,
prior_beliefs, doubts` (`venue` non-empty; the four term/belief fields are lists). Old-vs-new is
**reader-relative** — judged against `venue`, never absolute (Pinker's curse-of-knowledge). These four
content-bearing fields are also **append-safe under `diff`** (a later stage cannot silently empty them, even
across a stage regression). F2 only *sets and gates* the frame here; frame-consistency in the drafted prose is
audited by the F5 scope judge at stage 5.

`register` (F17, voice concern, also a stage-1 output) pins the venue's exemplar anchors `{venue, exemplars}`
from `references/F17-exemplars.md`. It is optional before the gate and **required non-empty at stage ≥ 4** — the
voice pass (F8b voice-realize, F12 audit) cannot run without a pinned exemplar set (`no-exemplar-pin`, SC-VOICE-10).
It is append-safe at both the top level and per sub-field (gutting `exemplars` while keeping `venue` is still caught).

## Claim object — required keys (always present after any stage write)

| Key | Type | Written at | Notes |
|---|---|---|---|
| `claim_id` | string | stage 2 (F3) | unique, e.g. `C1` |
| `text` | string | stage 2 (F3) | the claim itself |
| `bound_experiment` | string \| null | stage 2 (F3) | evidence key, e.g. `E008`; `null` → F3 raises a `\gap` |
| `evidence_status` | enum | stage 2 (F3) | `live` \| `demoted` \| `superseded` — F3 reads it; citing a demoted/superseded number as live is a DET flag |
| `strength` | enum | stage 2 (F3) | `unsupported` \| `observed` \| `supported` \| `strong` — bounds the wording; F9a asserts tag ≤ this |
| `scope` | string \| null | stage 2 (F3/F5) | e.g. `per-individual, n=9, LeBel, Qwen0.5B` |
| `is_central` | bool | stage 2 (F3) | a central contribution → needs a figure (F7) |
| `acknowledgments` | array | stage 2 (F18) | one limitation/rebuttal per **defended claim** (= bound + `strength ∈ {observed,supported,strong}`); F18 plans at stage 2, re-checks vs the F13 premortem at stage 5 |
| `section` | string \| null | stage 3 (F6) | section_id this claim is assigned to; `null` before F6 |
| `tags` | array | stage 4 (F8a) | `{"strength": <enum>, "sentence_ref": "<text>"}` — one per claim sentence as it is drafted |

**The key must be present even when the value is null/empty.** A *missing key* is a schema violation
(serialization bug — SC-TRUST-9, SC-PROC-6); a *null value* is a stage-appropriate not-yet-filled slot
(handled by the owning functionality, e.g. `bound_experiment: null` → F3's `\gap`).

## Enums
- `evidence_status`: `live` (current verdict, safe to cite) · `demoted` (overturned / artifact, e.g. E005's +0.0081) · `superseded` (replaced by a later experiment).
- `strength`: `unsupported` · `observed` · `supported` · `strong` (the claim-evidence contract ladder; lifted from the live skill).

## `lattice_integrity` rules (all pure-DET; the rigid floor)

Stage-aware via `meta.stage`. Two modes:

`validate <lattice>` — single snapshot:
1. **schema** — top-level keys present (incl. `deviation_log`); every claim has all required keys; enums
   valid; `claim_id` **and** `section_id` unique; `meta.schema_version == "1"`; `meta.stage` is an int in 1–6
   (a digit-string is coerced **and** flagged; an unparseable stage flags **and** fails safe to running all
   coverage, never silently disabling it); `is_central` is a bool; each `\evd` tag is
   `{strength: <enum>, sentence_ref: <text>}`; `message` is non-null at stage ≥ 3 (nothing to structure around). (always / as noted)
2. **orphan-claim** — every claim's `section` is non-null and names an existing section. (stage ≥ 3)
3. **empty-section / empty-skeleton** — every section has ≥1 *existing* claim; and a stage ≥ 3 lattice has ≥1
   claim and ≥1 section (an empty skeleton is malformed, not merely low-quality). (stage ≥ 3)
4. **node→section** — the claim↔section map agrees **both** directions: a claim's `section` exists *and* that
   section lists the claim; a section's `claim_ids` all resolve. (stage ≥ 3)
5. **central-claim-figure** — every `is_central` claim has ≥1 figure referencing it. **Dormant at stage 3**
   (skeleton, pre-figure); **mandatory at stage ≥ 4** (drafting). Gated on stage, not a self-reported flag, so
   it cannot die silently if F7 is skipped.
6. **warrant-ref / figure-ref** — every warrant `from`/`to` and every figure `claim_id` resolves to an
   existing claim (no dangling edges in the spine). (always)
7. **every-claim-tagged** — every claim has ≥1 well-formed `\evd` tag. (stage ≥ 4)

`diff <before> <after>` — append-safe / round-trip:
8. **round-trip / append-safe** — no claim dropped (`claim_id` is the stable identity — a rename reads as a
   drop); no key dropped from a claim; **no field that HAD content in `before` is emptied in `after`** —
   including a list whose members are gutted to empty strings (catches SC-PROC-7 acks-overwrite, the
   content-gutting bypass, scope-deletion = the mechanical half of SC-TRUST-10). Values may *change*; they may
   not be *cleared* by a later stage. `bound_experiment` and `section` are exempt (a `\gap` / re-skeleton may
   re-null them) but their **key** must still survive; `scope` is provenance and is **not** exempt.
   `diff` also composes in `validate(after)`, so a single `diff` call is self-sufficient.

Empty-warrant (F4) and lexical scope-words (F5) are separate hooks, **not** part of `lattice_integrity`.

## Draft output conventions (F8a → checked by `draft_check.py`)
The drafter writes a prose file alongside the lattice. Two literal conventions make the prose machine-checkable
without parsing natural language:
- **Section boundary:** a line by itself, `%%SECTION <section_id>`, before each section's prose. Every lattice
  section must have one (SC-PROC-3); the markers are stripped before final render.
- **Claim provenance:** `\evd{<claim-id>}{<strength>}` at the end of each claim sentence (SC-PROC-4). The same
  event is mirrored into that claim's `tags[]` (`{strength, sentence_ref}`); the two must agree (`tag-desync`).
`sentence_ref` is the claim sentence verbatim, so F9b can judge the prose against the tag.
