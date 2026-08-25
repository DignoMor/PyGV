# Issue tracker: GitHub

Issues and specs for this repository live as GitHub issues. Use the `gh` CLI for
all operations and infer the repository from `git remote -v`.

## Conventions

- Create: `gh issue create --title "..." --body "..."`
- Read: `gh issue view <number> --comments`
- List: `gh issue list --state open --json number,title,body,labels,comments`
- Comment: `gh issue comment <number> --body "..."`
- Label: `gh issue edit <number> --add-label "..."`
- Close: `gh issue close <number> --comment "..."`

Use a heredoc for multiline issue bodies. Fetch labels and comments when an
engineering skill needs the full ticket context.

## Pull requests as a triage surface

**PRs as a request surface: no.** Pull requests are delivery and release
artifacts, not incoming requests for the triage workflow.

GitHub shares one number space across issues and pull requests. Resolve an
ambiguous reference such as `#42` with `gh pr view 42`, falling back to
`gh issue view 42`.

## Skill operations

- When a skill says to publish to the issue tracker, create a GitHub issue.
- When a skill says to fetch a ticket, run `gh issue view <number> --comments`.
- For a wayfinding map, use one `wayfinder:map` issue with linked child issues.
- Represent blockers with GitHub issue dependencies when available; otherwise,
  use a `Blocked by: #<number>` line in the child issue.
- Claim an unblocked ticket by assigning it to the active developer.
