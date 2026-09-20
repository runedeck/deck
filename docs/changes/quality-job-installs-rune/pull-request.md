Install the pinned `rune` in the quality job so the `ontology-graph` hook runs instead of failing on an absent binary.

## Plan

The hook needs `rune graph export` under `REQUIRE_GATES`. The job installs rudof and openspec and never `rune`, so every push to `main` since `a0e89ea7` was red. A `cargo install` from the cli at a pinned commit, outside the tree, is the smallest fix that keeps the all-files hooks away from the cli checkout.

## Changes

- Add an `Install the pinned rune` step to `.github/workflows/quality.yaml` after `Install tools`: `cargo install --git https://github.com/runedeck/cli --rev 64fc7e85fbb9a3e65d95e45ad8825b5ee1cdbeaa rune-cli`.
- Raise the job timeout from 20 to 30 minutes in `.github/workflows/quality.yaml`.
- Add `docs/changes/quality-job-installs-rune/` with proposal, delta spec, tasks, and `adr.md`.

## Testing

- [x] `prek run --all-files` and `prek run --stage pre-push --all-files` with `REQUIRE_GATES=1` in an isolated clone of `f9134ce5`, both exit 0.
- [x] The `quality` check on this branch's head is green on GitHub and its log shows `declared world validates the real graph` passing.

## Release Notes

- N/A
