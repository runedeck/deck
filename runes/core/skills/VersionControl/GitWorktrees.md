# Git Worktrees

Isolated workspaces that share one repo. Work on several branches in parallel without a switch.

## jj colocated repos: this companion does not apply

If `.jj/` exists at the repo root, do NOT use git worktrees. `git worktree add` mutates refs behind jj's back. Use `jj workspace add ../repo-<name>` instead; see [Jujutsu.md](Jujutsu.md). Check first:

```sh
[ -d "$(git rev-parse --show-toplevel)/.jj" ] && echo "jj colocated: use jj workspaces"
```

## Primary checkout

Keep the primary checkout on the default branch. Create a worktree for each work branch. Do not create a worktree for the default branch. Do not leave the primary checkout on a work branch after the work merges. Tools that read merged state then read the primary checkout.

## Directory selection

1. Use an existing `.worktrees/` or `worktrees/` directory at the repo root. Prefer `.worktrees/` when both exist. Use a documented repository helper when it exists.
2. Respect a documented worktree location in the project instructions.
3. Ask the user only when neither applies.

For a project-local directory, confirm that Git ignores the selected directory before you create a worktree.

## Create and prepare

```sh
worktree_root=.worktrees # Set this to the selected directory.
git check-ignore -q -- "$worktree_root" || {
    echo "Git does not ignore $worktree_root." >&2
    exit 1
}
git worktree add "$worktree_root/$BRANCH_NAME" -b "$BRANCH_NAME"
cd "$worktree_root/$BRANCH_NAME"
```

Detect the project type and run its setup (`npm install`, `cargo build`, `pip install -r requirements.txt`, ...) so the new tree matches the parent. Run the test suite once to establish a clean baseline. If tests fail, stop and report.

## Cleanup

Removal of the worktree is part of landing the work. When the work is merged or abandoned:

```sh
git worktree remove <path>
git worktree list    # verify nothing lingers
```

A merge session ends clean. Check these two end conditions:

```sh
git worktree list                 # only live work remains
git branch --merged origin/main   # empty, except the default branch
```

Create at most one staging worktree for each pull request. Remove it in the session that merges the pull request.

Never delete a worktree directory manually. `git worktree remove` keeps the repository worktree list consistent. Remove only the worktree that you created for the current task.

## Supersession check

Check a dirty worktree before you delete it. Compare each touched file with the merged default branch:

```sh
git -C <worktree> status --porcelain | sed 's/^...//' | while read -r f; do
    git -C <worktree> diff origin/main --quiet -- "$f" || echo "differs: $f"
done
```

Delete the worktree only when no file differs. A file that differs holds unmerged work.

## Red flags

- A worktree in a directory git does not ignore. The contents leak into the parent repo's status.
- A skipped baseline test run. You cannot separate new bugs from pre-existing breakage.
- `rm -rf` on a worktree directory. It leaves dangling references in `.git/worktrees/`.
- A merged worktree that outlives its merge.
- A primary checkout that stays on a merged work branch.
- A separate worktree for the default branch.

---

*Git worktree content adapted from [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) (MIT) under EUPL-1.2.*
