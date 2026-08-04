# Interpret mode

Turn recorded evidence into an adjudicated verdict. Enter on "is this verdict real", "digest this
result", "what does E0xx mean", or after a run produces numbers and before the verdict lands anywhere.
This is truth-producing: the strict standard applies, and re-judging a recorded number is `/work`-grade,
not casual reading.

## The hard line

`/interpret` proposes a verdict; it becomes settled only on the user's confirmation. It states only numbers a working session recorded: a needed-but-missing number
is a `\gap`, never invented.

## The loop

1. **Claim-Intent-Manifest first (pre-commitment).** Before adjudicating, pin three things in one block:
   - **claim**: the one-line verdict you expect to land,
   - **evidence**: the exact recorded pointer(s) that would support it (`E0nn`, a decision, a learning),
   - **overturn-if**: what result would falsify it (the kill-criterion echo).
   Write this before looking hard at the numbers. It is the one guard against drifting into an
   unsupported claim, the failure this repo keeps hitting (R06, the F1 reframes).
2. **SCR: predict the verdict before the recompute.** State what you expect the contrast to show and
   why, then compute or re-read it, then reconcile. A direct check on availability bias over a result
   the user may already have a hope about. Technique, not a gate; toggle off with "skip predictions".
3. **Re-compute the load-bearing contrast.** If the verdict rests on an aggregated statistic over
   seeds, folds, or subjects, run `stat-aggregation-auditor` to re-derive it independently (within-seed
   vs pooled, the bootstrap unit, paired vs unpaired, P-construction). Do not trust the run's own
   summary of its own number.
4. **Run the panel, reconcile to clean.** Spawn the thinking panel (`counter-argument`,
   `socratic-thinker`, `premortem-analyst`, `first-principles-grounder`) and `oracle-reviewer` in
   RESULT mode on the proposed verdict. Each emits a `PANEL-VERDICT` block. Verify each objection
   against the data, address the ones that hold, re-run until `PANEL-CLEAN:YES`. Add the Codex
   code-critic when the verdict rests on a script.
5. **Score against the manifest.** The landed verdict must match the manifest's claim and clear its
   overturn-if. If the evidence pushed the verdict off the manifest, that is a finding: say the claim
   moved and why, do not quietly keep the old framing.
6. **Hand off to `/write`.** Once the verdict is clean and confirmed, a paper-relevant finding goes directly into the canonical rewrite manuscript.

## Fresh-digest vs revision

- **Fresh-digest**: a queue question's first verdict. Builds.
- **Revision**: re-opening a settled question on new evidence or a found error. Corrects. This is the
  availability-bias danger zone: "we already concluded X" is the comfortable answer to defend, not
  necessarily the true one. Run the panel harder on a revision, and let the evidence move the claim.

## What this mode does not do

It does not write manuscript prose (that is `/write`) or run a new experiment (that is `/work`). It adjudicates a recorded result into a clean,
panel-survived, manifest-scored verdict.
