# Changelog

All notable changes to Rune Deck are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Initial scaffold.
- BenchArtifact skill: benchmark any skill, rule, or agent against a baseline across models, with per-model aggregation and a self-contained comparison report (DECK-0001).
- The ReviewMarkers rule in core, adopted through the block-review ceremony.

### Changed

- AdoptArtifact keeps block verdicts in temporary CLI sessions and commits only source-level provenance sidecars (DECK-0002).
- BuildSkill defers its evaluation step to BenchArtifact; the loop, agent templates, review viewer, and evaluation schemas moved there.

### Removed

- Legacy per-block review ledgers from BuildSkill and ReviewMarkers.
