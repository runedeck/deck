---
adr: "docs/decisions/DECK-0005 Artifact Lifecycle and Evidence Tokens.md"
status: proposed
---

# Release Note Publishing

## Why

Pushback outcome: survivor.

This repository collects a `## Release Notes` list in each pull request. No specification or active change publishes those notes.

The `agentic-first-pipeline-rules` change lists `CHANGELOG.md` only as an affected file. The `lifecycle-stages-and-evidence` change defines ceremony delivery, not release publishing.

This change adds the missing release-publishing capability.

## What Changes

- Use merged pull request notes as release input.
- Compile the notes into one GitHub Release draft for owner review.
- Make release automation the only writer of repository changelog output.
- Preserve the current changelog history during the first release.
- Deliver the ceremony from Skeleton to this repository through Copier.

## Capabilities

- release-note-publishing-flow (new)

## Impact

- Skeleton release ceremony and template payload.
- The release ceremony of this repository after a Copier update.
- Release-note compiler and tests.
- `CHANGELOG.md` migration.
