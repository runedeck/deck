---
status: proposed
---

# Declare secrets per repository

## Why

The runedeck stack now declares secrets with SecretSpec ([SecretSpec][SECRETSPEC]). The skeleton gives each repository a `secretspec.toml`. Rune launch reads its credentials through `~/.config/rune/secretspec.toml`, and provision stores new keys in the Keychain. An agent that does not know this still reads `~/.env` or puts a key on a command line. A core rule tells every session how to declare, read, and pass a secret.

## What Changes

- `runes/core/rules/DeclareSecrets.md` tells an agent to declare each secret in the repository's `secretspec.toml` and to read it only through secretspec. Values stay out of the conversation and off argv, and every call gives a reason.
- The `delivery` cast selects the rule. The `core` cast selects it through `core/**`.

## Capabilities

- declare-secrets-per-repository (new)

## Impact

- One new rule and one cast entry. The rule enters without a provenance sidecar, because it is first-party content.

[SECRETSPEC]: https://github.com/cachix/secretspec
