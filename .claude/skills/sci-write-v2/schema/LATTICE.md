# `claim-lattice.json` — the spine artifact (F15)

The single shared object every `/write` stage reads and writes. It carries the case (claims, evidence,
argument) from frame → gate → draft → audit so nothing drops between hands. The `lattice_integrity` check
(`scripts/lattice_integrity.py`) is the rigid DET floor over it.

## Top-level shape

```json
{
  "meta":        {"stage": <int 1-6>, "schema_version": "1"},
  "message":     "<one-sentence message of the paper>" | null,
  "reader_model": { ... } | null,
  "claims":      [ <claim object>, ... ],
  "warrants":    [ {"from": "<claim_id>", "to": "<claim_id>", "warrant": "<text>"}, ... ],
  "figures":     [ {"figure_id": "<id>", "claim_id": "<claim_id>"}, ... ],
  "sections":    [ {"section_id": "<id>", "title": "<text>", "claim_ids": ["<claim_id>", ...]}, ... ],
  "deviation_log": [ {"functionality": "<F##>", "method": "<...>", "why": "<...>", "did": "<...>"}, ... ]
}
```

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
| `acknowledgments` | array | stage 2 (F18) | one limitation/rebuttal per defended claim |
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
   valid; `claim_id` unique; `meta.schema_version == "1"`; `meta.stage` is an int in 1–6 (a digit-string is
   coerced **and** flagged; an unparseable stage flags **and** fails safe to running all coverage, never
   silently disabling it); `is_central` is a bool; each `\evd` tag is `{strength: <enum>, sentence_ref: <text>}`. (always)
2. **orphan-claim** — every claim's `section` is non-null and names an existing section. (stage ≥ 3)
3. **empty-section** — every section has ≥1 *existing* claim. (stage ≥ 3)
4. **node→section** — the claim↔section map agrees **both** directions: a claim's `section` exists *and* that
   section lists the claim; a section's `claim_ids` all resolve. (stage ≥ 3)
5. **central-claim-figure** — every `is_central` claim has ≥1 figure referencing it. (stage ≥ 3)
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
