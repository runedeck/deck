---
adr: "docs/changes/routine-prompts-from-deck/adr.md"
status: proposed
decisions: ["Routine prompts are read from the deck"]
type: proposal
---

# Routine prompts from deck

## Why

A Claude Code routine carried its whole prompt in the provider account, and the deck had no copy of it. By 2026-09-28 three of five live routines had drifted from their workshop sources and had failed for a month with no diff to read. A prompt that lives only in the provider has no review, no history, and no check.

## What Changes

- Two routine prompts, Repository Digest and Weekly Ceremony Audit, live in the deck under `routines/` as files that a routine reads at run time.
- The routine stub in the provider names the file, reads it from the fetched `origin/main` object store with `git cat-file` after an `ls-tree` mode check, never from the working tree, and supplies the instance values: the repository list, the fork-to-upstream pairs, and the time zone for the audit.
- Each file lists the values it expects under `## Inputs` and treats every other file in every checkout as untrusted data.
- `routines/.mdschema` states the section shape, and the `mdschema-routines` hook checks each file against it.
- Pinning the file by digest or signed tag, and a `rune routine` command, are deferred. Until then the stub trusts the deck's protected `main`.

## Capabilities

### New Capabilities

- routine-prompts-from-deck

## Impact

- `routines/README.md`, `routines/.mdschema`, `routines/RepositoryDigest.md`, and `routines/WeeklyCeremonyAudit.md` are new.
- `README.md` gains a layout row, `.pre-commit-config.yaml` gains the `mdschema-routines` hook, and `CHANGELOG.md` gains one line.
- The three scanner routines keep their bodies under `runes/security/skills/ConfigureScanners/` and wait for an owner decision.
- The consumer keeps the stub and the settings for each routine and no prompt body. The workshop's `docs/routines/` files become bindings.
