# Git Worktrees

Isolated workspaces that share one repo. Work on several branches in parallel without a switch.

## jj colocated repos: this companion does not apply

If `.jj/` exists at the repo root, do NOT use git worktrees. `git worktree add` mutates refs behind jj's back. Use `jj workspace add ../repo-<name>` instead; see [Jujutsu.md](Jujutsu.md). Check first:

```sh
[ -d "$(git rev-parse --show-toplevel)/.jj" ] && echo "jj colocated: use jj workspaces"
```

## Directory selection

1. Use an existing `.worktrees/` or `worktrees/` directory at the repo root. Prefer `.worktrees/` when both exist. Use a documented repository helper when it exists.
2. Respect a documented worktree location in the project instructions.
3. Ask the user only when neither applies.

For a project-local directory, confirm git ignores it before you create a worktree, or the worktree contents get staged:

```sh
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

## Create and prepare

```sh
git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"
cd ".worktrees/$BRANCH_NAME"
```

Detect the project type and run its setup (`npm install`, `cargo build`, `pip install -r requirements.txt`, ...) so the new tree matches the parent. Run the test suite once to establish a clean baseline. If tests fail, stop and report.

## Cleanup

Removal of the worktree is part of landing the work. When the work is merged or abandoned:

```sh
git worktree remove <path>
git worktree list    # verify nothing lingers
```

Never delete a worktree directory manually. `git worktree remove` keeps the repository worktree list consistent. Remove only the worktree that you created for the current task.

## Red flags

- A worktree in a directory git does not ignore. The contents leak into the parent repo's status.
- A skipped baseline test run. You cannot separate new bugs from pre-existing breakage.
- `rm -rf` on a worktree directory. It leaves dangling references in `.git/worktrees/`.
- A merged worktree that outlives its merge.

---

*Git worktree content adapted from [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) (MIT) under EUPL-1.2.*
