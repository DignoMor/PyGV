# Repository guidance

## Development workflow

- `xp-dev` is the persistent integration branch and the base for new work.
- Develop changes on focused branches created from `xp-dev`, then merge them back into `xp-dev`.
- `main` contains releases. Changes enter `main` through a release pull request from `xp-dev`.
- Keep direct development commits off `main`.

## Specifications

For behavior, API, or architecture changes, read `specs/README.md`,
`specs/architecture.md`, and the relevant module specification before editing.
Update the affected specifications and obtain user approval before implementation.

Keep repository-related writes inside this repository unless the user explicitly
requests otherwise.

## Agent skills

### Issue tracker

Work is tracked in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the five canonical triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository. See `docs/agents/domain.md`.
