---
status: proposed
---

# New branch checks from merge base

## Why

The quality workflow runs both check stages over one range of commits. A pull request gives it a base, and a later push gives it the earlier head of the branch. The first push of a new branch gives it neither, so both stages inspected every file in the repository. The idea snapshot check answers only while Obsidian runs on a desktop. It failed on every new branch with `REQUIRE_GATES` set, so the Draft Open workflow did not open the draft.

## What Changes

- The range for the first push of a branch starts at the branch's merge base with `main`. The stages then inspect the files the branch changes, the same files a pull request on that branch shows.
- A branch that jj rewrote and pushed again starts at the same merge base, because its earlier head no longer exists on the remote.
- A push to `main` with no earlier head still inspects every file. A later push and a pull request keep their ranges.

## Capabilities

### New Capabilities

- `quality-new-branch-base`: the validator checks the first push of a branch over the files the branch changes.

## Impact

- `.github/workflows/quality.yaml`, the range selection step only. Commit `d6ebd85d` on pull request #78 carries the fix, and this change records its rule.
- No hook, tool pin, or rune changes.
