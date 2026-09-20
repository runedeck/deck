---
adr: docs/changes/adopt-prose-length-caps/adr.md
status: proposed
decisions: ["Deck prose keeps the cli caps"]
---

# Adopt prose length caps

## Why

The cli change `prose-length-caps` makes `rune spec validate` refuse a requirement statement over 100 words and `rune docs check` refuse a changelog entry over 200 characters. Six deck requirement statements and twelve changelog lines were over. The owner asked for the caps because both had grown into walls of text.

## What Changes

- Six requirement statements split into two or three each: `model-commit-attribution` (canonical), `pull-request-delivery-contract`, `release-note-publishing`, `restrict-remote-writes`. Every MUST and every scenario survives under its own heading.
- `CHANGELOG.md` rewritten to one line per change, verb first, groups in the Keep a Changelog order. 51 entries became 70 lines. No change dropped.
- The quality job's `RUNE_CLI_REV` moves to the cli commit that carries the caps, once that change is on cli `main`.

## Capabilities

### New Capabilities

- `adopt-prose-length-caps`: deck specs and the changelog stay under the caps the rune checkers enforce, in CI.

## Impact

- `docs/specs/model-commit-attribution/spec.md`, three change deltas, `CHANGELOG.md`, `.github/workflows/quality.yaml` (the pin).
- The `pull-request-delivery-contract` delta is now 170 lines, over the 150-line warning. Splitting that capability is its own change.
