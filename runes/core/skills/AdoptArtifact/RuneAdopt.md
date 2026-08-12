# Rune adopt commands

> Drive the adoption state machine with the rune CLI: start or resume a session, record a verdict per block, and finalize the sealed review record.

The `rune` CLI owns adoption state in a Rune deck. The ceremony lives in the entrypoint; this workflow is its deck-side mechanics.

## OBJECTIVE

An adoption session driven from start to sealed record, with every block verdict recorded through the CLI.

## DONE WHEN

- `rune adopt status --json` shows no pending review for the artifact.
- Finalization reported reviewed provenance sidecars and a sealed review record.
- The artifact, its sidecars, and the record are staged together.

## TODO

- [ ] List pending sessions, then resume or start one
- [ ] Record a verdict for every block
- [ ] Finalize, resolving each refusal
- [ ] Stage the artifact with its provenance evidence

## Step 1: Start or resume

Run every command from the deck root; adopt commands default to `--root .`. Re-run `rune adopt status --json` before acting, because invocation-time state becomes stale after each command. When several sessions are pending, pass `--artifact` on every command.

```sh
rune adopt status --json
rune adopt start <source> --module runes/<domain> [--kind skill|agent|rule] [--name <artifact-name>] [--source-url <attribution>]
```

A commit-pinned GitHub URL imports one file. A local directory imports its complete tree, and `--source-url` records the upstream location.

## Step 2: Record verdicts

```sh
rune adopt next --count 4 --json
rune adopt verdict <block-id> keep
rune adopt verdict <block-id> adapt --note "<user rationale>"
rune adopt verdict <block-id> cut --note "<user rationale>"
```

Re-record a changed decision with `--force` only after explicit confirmation. If a block id is unknown, re-run `next` and synchronize with the current ledger.

## Step 3: Finalize or abandon

```sh
rune adopt finalize
rune adopt abandon --yes
```

Pass `--reviewer "Name <email>"` only when git configuration has no identity. On success, inspect the reported added entries and the record path. Abandon drops the session, the exit for an unresolvable name conflict with a first-party artifact.

## EXECUTE NOW

Work the TODO in order from the deck root, starting with `rune adopt status --json`.
