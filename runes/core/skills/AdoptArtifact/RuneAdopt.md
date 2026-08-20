# Rune adopt commands

> Drive the adoption state machine with the rune CLI: start or resume a session, record a verdict per block, and finalize concise source provenance.

The `rune` CLI owns adoption state in a Rune deck. The ceremony lives in the entrypoint; this workflow is its deck-side mechanics.

## OBJECTIVE

An adoption session driven from start to reviewed sidecars, with every block verdict enforced by the CLI.

## DONE WHEN

- `rune adopt status --json` shows no pending review for the artifact.
- Finalization reported reviewed provenance sidecars with final file digests.
- The artifact and its sidecars are staged without a review ledger.

## TODO

- [ ] List pending sessions, then resume or start one
- [ ] Record a verdict for every block
- [ ] Finalize, resolving each refusal
- [ ] Stage the artifact with its provenance evidence

## Step 1: Start or resume

Run every command from the deck root; adopt commands default to `--root .`. Re-run `rune adopt status --json` before acting, because invocation-time state becomes stale after each command. Empty or malformed status output means the deck has no adoption state here; stop and confirm the working directory with the user instead of starting a session.

```sh
rune adopt status --json
rune adopt start <source> --module runes/<domain> [--kind skill|agent|rule] [--name <artifact-name>] [--source-url <attribution>]
```

There is no resume command: `next`, `verdict`, and `finalize` continue the open session. When several sessions are open, pass `--artifact <path>` on each of them, using the artifact path that `status` reports. A commit-pinned GitHub URL imports one file. A local directory imports its complete tree, and `--source-url` records the upstream location.

## Step 2: Record verdicts

```sh
rune adopt next --count 4 --json
rune adopt verdict <block-id> keep
rune adopt verdict <block-id> adapt --note "<user rationale>"
rune adopt verdict <block-id> cut --note "<user rationale>"
```

The default `--count` is 1; batch up to 4 for flow, and fetch an oversized or whole-file block alone. `--note` is required for adapt and cut. Apply an approved adapt immediately; the temporary session stores the rationale until finalization writes the final file digest. Re-record a changed decision with `--force` only after explicit confirmation. If a block id is unknown, re-run `next` and synchronize with the current session.

## Step 3: Finalize or abandon

```sh
rune adopt finalize
rune adopt abandon --yes
```

Finalize refuses with reasons until the tree matches the session. The reviewer identity defaults to git config `user.name` and `user.email`; pass `--reviewer "Name <email>"` when needed. On success, inspect the reviewed sidecars and confirm that no review ledger entered the working tree. Abandon drops the session and imported artifact.

## Maintenance

```sh
rune adopt doctor
rune adopt reseal
```

`doctor` verifies open sessions and reviewed sidecar digests. It reports legacy `review.yaml` and `*.review.yaml` files for removal. `reseal` updates reviewed sidecar digests after the maintainer's own touch-ups; it does not review new content. Never use reseal to bless content the block verdicts did not cover.

## EXECUTE NOW

Work the TODO in order from the deck root, starting with `rune adopt status --json`.
