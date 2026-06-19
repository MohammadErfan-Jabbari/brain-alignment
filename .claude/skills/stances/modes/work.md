# Work mode

Produce evidence: lock a design, run it, judge the result, record it. The science moves here. This
stance is **explicit-only** (it never auto-fires) and runs at high autonomy (long `/goal` runs).

## The standard (strict)

Kill criteria predeclared before the run; design locked before evidence; contiguous splits; the
anti-confound / nuisance-baseline battery; ≥3 seeds for stochastic experiments; every number reported
with its uncertainty and the named test. (Methodology non-negotiables, `docs/03-methodology.md`.)

## The procedure (route through the existing gates)

1. **Design → gate.** Run `/precheck`: `anti-confound-designer` assembles the control battery, then
   `oracle-reviewer` gates it to `READY-TO-RUN`. No compute before PASS.
2. **Goal.** Run `/goalsmith <item>` to build the single-line `/goal` completion condition, then run it.
3. **Run.** Long runs are background processes (`uv run`; `HF_HOME` set; 4x L40S, single node). Keep raw
   evidence in `experiments/*.md` separate from interpretation. Record the *why* of each non-obvious
   design choice at choice-time (D037), so the writing layer can cite it rather than invent it.
4. **Judge → hand to `/interpret`.** After a multi-seed/arm run, the verdict is adjudicated in
   `/interpret` (the `stat-aggregation-auditor` re-compute + the panel), not declared here.

## Boundary

Produces and records numbers. It does not adjudicate the rung verdict (that is `/interpret`, and the
flip is Erfan's) and does not write the report (that is `/write`).
