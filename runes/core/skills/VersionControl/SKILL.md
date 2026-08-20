---
name: VersionControl
description: "Git and Jujutsu discipline for commits, staging, pushes, history rewrites, worktrees, and repo governance. USE WHEN committing, pushing, creating pull requests, squashing history, cleaning merged branches, setting branch protection or CODEOWNERS, or working in a jj colocated repo."
metadata:
    version: 0.1.0
    upstream: https://github.com/N4M3Z/forge-core
---

# VersionControl

Commit discipline, staging hygiene, push policy, and repo governance. In a jj colocated repo (`.jj/` at the root), the [Jujutsu.md](Jujutsu.md) companion replaces the git commit and push flow.

## Constraints

- Author every commit with an identity that `authors.yaml` lists. Use `make worktree BRANCH=<branch> IDENTITY=<model-id>` to create a worktree with the identity set. Do not export identity env variables for each command.
- Stage files by name. Never use `git add -A` or `git add .`.
- Commit with a pathspec (`git commit -- <path>...`), never a bare `git commit`. A bare commit snapshots the whole index and sweeps in the user's staged work. When unsure, run `git diff --cached --stat` first.
- Never commit files that contain secrets. The prek hooks run gitleaks at commit and at push; never bypass them with `--no-verify`.
- Do not push unless the user asks. A commit and a push are separate actions.
- Never force-push unless the user explicitly asks. When a force-push is sanctioned, use `--force-with-lease`, not `--force`.
- Use `git switch <branch>`, not `git checkout <branch>`.

## Instructions

### Write the commit message

Use a conventional prefix. Explain why, not what. Keep the first line under 72 characters.

- `feat:`: New feature or capability.
- `fix:`: Bug fix.
- `refactor:`: Restructure without a behavior change.
- `docs:`: Documentation only.
- `chore:`: Maintenance, such as dependencies, configuration, or CI.
- `test:`: Add or repair tests.

Name other model contributors with `Co-Authored-By` trailers in the `authors.yaml` format. Do not repeat the author as a trailer. Run `scripts/check-authorship` to verify the outgoing range; the prek pre-push hook runs it automatically.

### Open the pull request

- Keep the title under 70 characters.
- Write the body as `## Summary` bullets plus the sections the repository's checks require (deck requires `## Release Notes`).
- Create the pull request from a feature branch, never from main.

### Rewrite history

`git read-tree -u --reset <sha>` snaps the index and working tree to a commit's tree without a merge or a rebase. To squash or regroup a linear history:

```sh
test -z "$(git status --porcelain)" || {
    echo "The worktree must be clean before the rewrite." >&2
    exit 1
}
source_branch=$(git branch --show-current)
case "$source_branch" in
    ""|main|master)
        echo "Run this rewrite only on a named feature branch." >&2
        exit 1
        ;;
esac
git branch backup-pre-squash "$source_branch"
git switch --orphan squashed-tmp
git read-tree -u --reset <end-of-group-sha>
git commit -m "<new message>"
# Repeat read-tree and commit for each remaining group.
git branch -f "$source_branch" squashed-tmp
git switch "$source_branch"
git branch -d squashed-tmp
```

Group along the chronological spine. A tree snapshot inherits every earlier commit's content, so a theme-based group carries unrelated work. Create a backup branch before every destructive rewrite and diff the result against it before any push.

### Clean up merged branches

A squash-merge changes the commit hash, so `git branch -d` refuses with "not fully merged". Verify the merge state on the platform first, then force-delete:

```sh
gh pr list --head <branch> --state all --limit 1
git branch -D <branch>
git push origin --delete <branch>
```

For local branches whose remote is gone: `git fetch --prune`, then delete the branches that `git branch -vv` marks `: gone]`.

### Work in parallel

In git-only repos, use git worktrees; deck repos provide `make worktree`. In jj colocated repos, use jj workspaces instead. See [GitWorktrees.md](GitWorktrees.md).

### Govern the repository

Detect the platform from the remote origin URL and use its companion: [GitHub.md](GitHub.md) for `gh`, [GitLab.md](GitLab.md) for `glab`. Read the current rules before you change them. Prefer rulesets over legacy branch protection on GitHub. Document governance in the repository (CODEOWNERS, branch rules), not only in external settings.

### Sign commits

Model commits in runedeck repositories are unsigned by specification, and no branch rule requires signatures. For personal repositories with hardware-key signing (YubiKey GPG or FIDO2 SSH), see [CommitSigning.md](CommitSigning.md).

## Verification

- `scripts/check-authorship` passes on the outgoing range.
- The prek commit-stage and pre-push hooks pass.
- After a history rewrite, the rewritten tree matches the backup branch (`git diff backup-pre-<op> HEAD` is empty).

## References

- [Jujutsu.md](Jujutsu.md): the jj commit and push discipline for colocated repos.
- [CommitSigning.md](CommitSigning.md): hardware-key signing setup and batch re-signing.
- [GitWorktrees.md](GitWorktrees.md): worktree creation, safety checks, and cleanup.
- [GitHub.md](GitHub.md), [GitLab.md](GitLab.md): platform governance commands.
