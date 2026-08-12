# Rune adopt commands

The `rune` CLI drives the adoption state machine in a Rune deck. Read this when adopting inside a deck; the ceremony itself lives in the entrypoint.

Run every command from the deck root; adopt commands default to `--root .`. Re-run `rune adopt status --json` before acting, because invocation-time state becomes stale after each command. When several sessions are pending, pass `--artifact` on every command.

## Session lifecycle

```sh
rune adopt status --json
rune adopt start <source> --module runes/<domain> [--kind skill|agent|rule] [--name <artifact-name>] [--source-url <attribution>]
```

A commit-pinned GitHub URL imports one file. A local directory imports its complete tree, and `--source-url` records the upstream location.

## Block review

```sh
rune adopt next --count 4 --json
rune adopt verdict <block-id> keep
rune adopt verdict <block-id> adapt --note "<maintainer rationale>"
rune adopt verdict <block-id> cut --note "<maintainer rationale>"
```

Re-record a changed decision with `--force` only after explicit confirmation. If a block id is unknown, re-run `next` and synchronize with the current ledger.

## Finalize or abandon

```sh
rune adopt finalize
rune adopt abandon --yes
```

Pass `--reviewer "Name <email>"` only when git configuration has no identity. On success, inspect the reported added entries and the record path; `rune adopt status --json` then shows no pending review. Abandon drops the session, the exit for an unresolvable name conflict with a first-party artifact.
