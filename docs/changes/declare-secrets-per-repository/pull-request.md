Adds the DeclareSecrets rule: declare each secret in `secretspec.toml`, read it only through secretspec, and keep values out of the conversation.

## Plan

Change `declare-secrets-per-repository`: proposal, one ADDED delta (`declare-secrets-per-repository`), and tasks under `docs/changes/declare-secrets-per-repository/`.

## Changes

- Adds `runes/core/rules/DeclareSecrets.md`: declare with `secretspec add`, read with `secretspec run` or `secretspec get`, pass values on stdin, give every call a `--reason`, and use `~/.config/rune/secretspec.toml` for harness credentials.
- Adds the rule to `casts/delivery.yaml`. The `core` cast selects it through `core/**`.

## Testing

- `rune validate`: 0 errors, `core/rules/DeclareSecrets.md` passes.
- `rune spec validate declare-secrets-per-repository` passes. The guarded push pipeline passed on this head.

## Release Notes

- New core rule DeclareSecrets for declaring and reading secrets through secretspec.
