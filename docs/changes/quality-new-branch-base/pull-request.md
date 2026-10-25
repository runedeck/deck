Start a new branch's quality range at its merge base with `main`, so the idea snapshot check stops failing every first push.

## Plan

The first push of a branch carries no before commit, and a branch that jj rewrote carries one that no ref reaches. In both cases the quality job inspected every file, and `sync-idea` failed under `REQUIRE_GATES` because CI has no Obsidian, so Draft Open never opened a draft. Starting the range at the merge base inspects the files the branch changes, the same set a pull request shows. A push to `main` without a before commit still inspects every file.

## Changes

- Start the `Select check range` step in `.github/workflows/quality.yaml` at the merge base with `origin/main` when a branch push has no before commit, or one that `git cat-file -e` cannot find.
- Add `docs/changes/quality-new-branch-base/` with proposal, delta spec, design, tasks, and this body.
- Drop the `type: spec` frontmatter from the `routine-prompts-from-deck` and `scanner-routines-from-deck` delta specs, which openspec 1.15.0 rejects in strict mode.

## Testing

- [x] The range step, run locally with the inputs of a new branch, a rewritten branch, a later push, and a first push to `main`, starts at the merge base, the merge base, the before commit, and all files.
- [x] `jj push --dry-run` replays both prek stages with `REQUIRE_GATES=1` on the head and exits 0.
- [x] This branch's first push opened its draft through Draft Open, and `quality`, `spec/presence`, and `review/correctness` are green on GitHub.
- [x] `openspec validate --all --strict` with openspec 1.15.0 passes all 52 changes and specs.

## Release Notes

- N/A
