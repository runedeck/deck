# Changelog

All notable changes to Rune Deck are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- The VersionControl skill: the primary checkout stays on the default branch, and each work branch gets a worktree.
- The VersionControl skill: a landing checklist and a supersession check for dirty worktrees.
- The VersionControl skill: a jj colocated repository uses jj workspaces and the repository jj push alias.
- The VersionControl skill: no generation footer, tool badge, or session link in commit messages and pull request bodies.

### Added

- The check-provenance hook: a rune or sidecar edit fails when its provenance subject digest is stale, and `--fix` repairs it.
- BenchArtifact ships bench.py again: one config-driven driver for the quick, snapshot, plan, run, grade, judge, and report steps.
- The AnchorWorkingDirectory rule in core: each shell command chain starts from an absolute path.
- Benchmark tables carry an output-token column: corpus mean per arm and the delta, so efficiency artifacts can show their token effect.
- Initial scaffold.
- BenchArtifact skill: benchmark any skill, rule, or agent against a baseline across models, with per-model aggregation and a self-contained comparison report (DECK-0001).
- The ReviewMarkers rule in core, adopted through the block-review ceremony.
- The UseSimplifiedTechnicalEnglish rule in core: all prose follows ASD-STE100, with a bad and good example pair.
- The SimplifiedTechnicalEnglish skill in core, adopted from two upstreams and merged: the STE rule set, the 39 recurring errors, worked examples, measured samples, and the ste-lint checker.
- The VersionControl skill in core, adopted from forge-core and trimmed: commit and staging discipline, push policy, history rewrites, branch cleanup, worktrees, jj colocated flow, hardware-key signing, and platform governance companions.
- The `ste` skill provides a short Claude command for `SimplifiedTechnicalEnglish`. It stays hidden from model invocation.
- The RTK skill and the UseEfficientCLI rule in core: prefix shell commands with the rtk proxy for 60 to 90 percent output-token savings, and search selectively with fd, rg, ast-grep, and gh --json field selection.

### Changed

- The spec waiver label is `ignore:spec`, matching the `ignore:` family every runedeck repository uses. `spec:none` retires.
- AdoptArtifact keeps block verdicts in temporary CLI sessions and commits only source-level provenance sidecars (DECK-0002).
- The authorship check reads separate author and trailer lists from `authors.yaml`. A trailer attribution can no longer validate an author field.
- BuildSkill defers its evaluation step to BenchArtifact; the loop, agent templates, review viewer, and evaluation schemas moved there.
- The core skill schema now accepts `targets`, `disable-model-invocation`, and `user-invocable`.

### Fixed

- The RTK guidance preserves standard-input payloads through passthrough or file arguments.
- The meta module again includes its required empty defaults file.
- Stable shell now validates the `rune` skill with the shared meta skill schema.
- The skill hook validates each entrypoint against its nearest `.mdschema`.

### Removed

- Legacy per-block review ledgers from BuildSkill and ReviewMarkers.
