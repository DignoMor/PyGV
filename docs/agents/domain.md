# Domain docs

This is a single-context repository. Domain language belongs in `CONTEXT.md`
at the repository root, and architectural decisions belong in `docs/adr/`.

## Before exploring

- Read `CONTEXT.md` when it exists.
- Read ADRs in `docs/adr/` that affect the area being changed.
- Proceed silently when either location does not yet exist. The domain-modeling
  flow creates these files lazily when terminology or decisions are resolved.

## Vocabulary

Use terms as defined in `CONTEXT.md` in issues, specifications, tests, and code.
When a needed concept is absent, reconsider whether existing vocabulary covers
it; otherwise record the gap for domain modeling.

## Decisions

Surface conflicts with an existing ADR explicitly. Do not silently override a
recorded decision.
