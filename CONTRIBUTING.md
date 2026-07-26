# Contributing

## Getting Started

```sh
git clone https://github.com/N4M3Z/deck.git
cd deck
make install
```

## Conventions

See [README.md](README.md) for project-specific conventions.

## Git

Conventional Commits: `type: description`. Lowercase, no trailing period, no scope.

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.

## Pull Requests

1. Fork and create a branch
2. Make changes following the conventions above
3. `make validate`
4. Open a PR against `main` **as a draft**, and mark it ready when the tree is stable

CI runs validation on every PR. The `main` branch requires passing CI before merge. The body carries a `## Release Notes` section (`- N/A` when nothing is user-facing).

## Review etiquette

Reviews are billed and re-run on every push, so batch your responses: collect fixes locally while reviewers are working and push them together once the lanes settle, rather than one push per finding. A fix commit may name the review thread it answers with a `Resolves-Thread: <id>` trailer; the thread resolves automatically on push.

Billed reviewers are summoned, never ambient: the maintainer applies `summon:` labels (`summon:runeseer`, `summon:macroscope`, `summon:autofix`) to invoke them, and each summon is visible in the pull request timeline.
