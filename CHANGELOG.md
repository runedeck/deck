# Changelog

All notable changes to Rune Deck are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Initial scaffold.
- BenchArtifact skill: benchmark any skill, rule, or agent against a baseline across models, with per-model aggregation and a self-contained comparison report (DECK-0001).
- The ReviewMarkers rule in core, adopted through the block-review ceremony.
- The UseSimplifiedTechnicalEnglish rule in core: all prose follows ASD-STE100, with a bad and good example pair.
- The SimplifiedTechnicalEnglish skill in core, adopted from two upstreams and merged: the STE rule set, the 39 recurring errors, worked examples, measured samples, and the ste-lint checker.
- The RTK skill and the UseRTK rule in core, adopted from forge-core: prefix shell commands with the rtk proxy for 60 to 90 percent output-token savings, with a pass-through guarantee and an installed-check.

### Changed

- The authorship check reads separate author and trailer lists from `authors.yaml`. A trailer attribution can no longer validate an author field.
- BuildSkill defers its evaluation step to BenchArtifact; the loop, agent templates, review viewer, and evaluation schemas moved there.
