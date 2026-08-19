# Changelog

All notable changes to Rune Deck are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Initial scaffold.
- BenchArtifact skill: benchmark any skill, rule, or agent against a baseline across models, with per-model aggregation and a self-contained comparison report (DECK-0001).
- The ReviewMarkers rule in core, adopted through the block-review ceremony.
- The UseSimplifiedTechnicalEnglish rule in core: all prose follows ASD-STE100, with a bad and good example pair.
- The SimplifiedTechnicalEnglish skill in core, adopted from two upstreams and merged: the STE rule set, the 39 recurring errors, worked examples, measured samples, and the ste-lint checker.
- The `ste` skill provides a short Claude command for `SimplifiedTechnicalEnglish`. It stays hidden from model invocation.

### Changed

- AdoptArtifact keeps block verdicts in temporary CLI sessions and commits only source-level provenance sidecars (DECK-0002).
- BuildSkill defers its evaluation step to BenchArtifact; the loop, agent templates, review viewer, and evaluation schemas moved there.
- The core skill schema now accepts `targets`, `disable-model-invocation`, and `user-invocable`.

### Fixed

- The meta module again includes its required empty defaults file.
- The current rune skill uses a directory-scoped schema until the Stable shell migration replaces it.
- The skill hook validates each entrypoint against its nearest `.mdschema`.

### Removed

- Legacy per-block review ledgers from BuildSkill and ReviewMarkers.
