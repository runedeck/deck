---
adr: docs/changes/quality-job-installs-rune/adr.md
status: proposed
decisions: ["Quality job builds the pinned rune"]
---

# Quality job installs rune

## Why

The `ontology-graph` hook (declared-world-model, 2026-09-20) runs `rune graph export` and fails under `REQUIRE_GATES` when `rune` is absent. The quality job installs rudof and openspec through `scripts/install-tools.local` and never installs `rune`, so every push to `main` since `a0e89ea7` shows a red `quality` check while the hook passes locally.

## What Changes

- The quality job gains one step after `Install tools`: `cargo install --git https://github.com/runedeck/cli --rev <commit> rune-cli`, pinned to the cli main commit, into the runner's cargo bin. The checkout is not in the tree, so the all-files hooks never see it.
- The job timeout rises from 20 to 30 minutes for the build.

## Capabilities

### New Capabilities

- `quality-job-installs-rune`: the quality job carries the `rune` binary the real-graph hook needs, pinned by commit.

## Impact

- `.github/workflows/quality.yaml` only. The contract job keeps its own pin and its in-tree candidate build.
- The pin moves by hand when the deck needs a newer cli. A stale pin fails loud: the hook's export format is checked by the shapes.
