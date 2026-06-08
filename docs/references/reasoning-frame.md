# Reasoning frame — Elon / Feynman / Naval

Not hero worship — a short name for a style of thought Erfan asks for. Use it when designing methods,
deciding what to build, or explaining why a change is worth it. (Domain-neutral rewrite of the Nexus
`elon-feynman-naval` reference, which was resume-specific.)

## Elon — first-principles reduction, constraint deletion

When drifting under inherited convention, ask:
- What is the real goal? (For us: produce one truthful, falsifiable result — not a tidy pipeline.)
- Which constraints are physically real, and which are leftovers from how it's usually done?
- What is the smallest intervention that gets the result?
- What should be **removed** instead of optimized?

Applied here: don't add a baseline, a loss term, or an artifact type because papers usually have it.
Add it only if a named bottleneck or confound requires it.

## Feynman — plain mechanism, honest limits

When deciding or explaining, ask:
- Can this be explained in plain language?
- Can we trace the mechanism step by step?
- **Where does the claim break?**
- What do we know, what do we infer, and what is still a guess?

Applied here: every claim is labeled by evidence status. State where a result would fail to
reproduce *before* running it. A number without a mechanism and a breaking point is not yet knowledge.

## Naval — leverage, compounding, elegant simplicity

When choosing between a local fix and a durable system, ask:
- What choice compounds across the rest of the thesis?
- What reduces repeated work later?
- What keeps the system simple enough to stay honest?
- Where is complexity pretending to be sophistication?

Applied here: prefer one reusable evaluation harness over bespoke per-experiment scripts; prefer the
`docs/` brain over reconstructing context in chat; delete machinery that isn't earning its keep.

## Combined operating rule

1. Reduce to the real goal; delete false constraints.
2. Inspect what already exists before inventing new work (the docs, brain-jepa, cached models).
3. Explain the gap mechanically and plainly.
4. Prefer the smallest durable change.
5. Use the deeper evidence bank only when the current state truly lacks the needed proof.

This frame is a guardrail against drift into duplicated work, fake sophistication, sprawl, and vague
justifications.
