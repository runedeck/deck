# Consumers Copier Design

## Approach

Let Copier do the merge from the real baseline, then layer the deck's additions. The template side wins every conflicted file, and the deck's hooks, Makefile targets, lint excludes, and Quality steps are re-added by hand so the next update diffs against template bytes plus a known set of additions. Prose corrections are mechanical and position-bound: split at the reported semicolon, expand the reported contraction, and reseal whatever that touched.

The alternative was to keep the deck's copies and cherry-pick template hunks. That leaves Copier with no clean baseline and repeats the conflict on every update.

## Structure

- `answers.yaml`, `.pre-commit-config.yaml`, `Makefile`, `.github/workflows/quality.yaml`: template base plus deck additions.
- `.vale.ini`, `.rumdl.toml`, `typos.toml`: template base plus deck excludes and the Simplified Technical English sample overrides.
- `runes/**/.provenance/*.yaml`: resealed after the prose corrections.
- `docs/changes/consumers-copier`: this change.

## Risks

- The deck-only additions conflict again on the next template change to the same file. The additions are small and named in DECK-0012.
- A reseal endorses the corrected bytes without a new review. The corrections change punctuation only, and the diff is in the same commit.
