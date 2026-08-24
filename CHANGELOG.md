# Changelog

All notable changes to Rune Deck are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Three routine prompts under docs/routines: the nightly PR babysitter, the deck merge follow-up, and the weekly ceremony audit. Provider setup stays manual.
- Initial scaffold.
- BenchArtifact skill: benchmark any skill, rule, or agent against a baseline across models, with per-model aggregation and a self-contained comparison report (DECK-0001).
- The ReviewMarkers rule in core, adopted through the block-review ceremony.
- The UseSimplifiedTechnicalEnglish rule in core: all prose follows ASD-STE100, with a bad and good example pair.
- The SimplifiedTechnicalEnglish skill in core, adopted from two upstreams and merged: the STE rule set, the 39 recurring errors, worked examples, measured samples, and the ste-lint checker.
- The VersionControl skill in core, adopted from forge-core and trimmed: commit and staging discipline, push policy, history rewrites, branch cleanup, worktrees, jj colocated flow, hardware-key signing, and platform governance companions.
- The `ste` skill provides a short Claude command for `SimplifiedTechnicalEnglish`. It stays hidden from model invocation.
- The RTK skill and the UseEfficientCLI rule in core: prefix shell commands with the rtk proxy for 60 to 90 percent output-token savings, and search selectively with fd, rg, ast-grep, and gh --json field selection.

### Changed

- AdoptArtifact keeps block verdicts in temporary CLI sessions and commits only source-level provenance sidecars (DECK-0002).
- The authorship check reads separate author and trailer lists from `authors.yaml`. A trailer attribution can no longer validate an author field.
- BuildSkill defers its evaluation step to BenchArtifact; the loop, agent templates, review viewer, and evaluation schemas moved there.
- The core skill schema now accepts `targets`, `disable-model-invocation`, and `user-invocable`.

### Fixed

- The RTK guidance preserves standard-input payloads through passthrough or file arguments.
- The meta module again includes its required empty defaults file.
- The current rune skill uses a directory-scoped schema until the Stable shell migration replaces it.
- The skill hook validates each entrypoint against its nearest `.mdschema`.

### Removed

- Legacy per-block review ledgers from BuildSkill and ReviewMarkers.
