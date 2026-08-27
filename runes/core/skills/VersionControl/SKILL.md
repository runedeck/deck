---
name: VersionControl
description: "Git and Jujutsu discipline for commits, pushes, pull-request review loops, history rewrites, worktrees, and repository governance. USE WHEN committing, pushing, creating or babysitting pull requests, responding to review bots, or changing Git history. Also use when cleaning branches, setting branch protection or CODEOWNERS, or working in a jj colocated repository. NOT FOR one-shot read-only pull-request audits, queue reports, or code review outside an active review-and-fix loop."
compatibility: "Requires Git. Jujutsu repositories require jj. GitHub and GitLab tasks require gh or glab and network access."
metadata:
    version: 0.3.0
    upstream: https://github.com/N4M3Z/forge-core
---

# VersionControl

Commit discipline, staging hygiene, push policy, and repo governance. In a jj colocated repo (`.jj/` at the root), the [Jujutsu.md](Jujutsu.md) companion replaces the git commit and push flow.

## Constraints

- Author every commit with an identity that `authors.yaml` lists. Use the repository worktree helper when available. Do not export identity env variables for each command.
- Stage files by name. Never use `git add -A` or `git add .`.
- Commit with a pathspec (`git commit -- <path>...`). A bare commit can include the user's staged work. Use a bare commit only after the history-rewrite procedure replaces the index with `git read-tree`. When unsure, run `git diff --cached --stat` first.
- Never commit files that contain secrets. The prek hooks run gitleaks at commit and at push. Never bypass them with `--no-verify`.
- Do not push unless the user asks. A commit and a push are separate actions.
- Never force-push unless the user explicitly asks. If the user approves a force-push, use `--force-with-lease`, not `--force`.
- Automated Jujutsu mode is the default. Keep automated pushes unsigned.
- Only the owner can start attended Jujutsu signing. An agent must not start or inherit attended mode.
- Open pull requests with the owner's existing `gh` authentication. Do not override it with an App token.
- Do not use Runewright for ordinary GitHub work. Reserve App identities for explicit CI or review automation.
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

Name other model contributors with `Co-Authored-By` trailers in the `authors.yaml` format. Do not repeat the author as a trailer. Attribution lives only in the author line and these trailers. Do not add a generation footer, a tool badge, or a session-link trailer. If the repository includes `scripts/check-authorship`, run it. The prek pre-push hook runs the repository check automatically.

### Open the pull request

- Keep the title under 70 characters.
- Write the body as `## Summary` bullets plus the sections the repository's checks require (deck requires `## Release Notes`).
- Create the pull request from a feature branch, never from main.
- When the user requests active babysitting, read [BabysitPR.md](BabysitPR.md) and use its review-and-fix loop.
- Do not append a generation footer, a tool badge, or a session link to the body.

### Manage rebase and summon economics

A review verdict binds to the head sha. Every rebase discards the standing verdict and costs one review round.

- Check the platform merge state before a rebase. Never rebase a MERGEABLE pull request. A stale but clean base merges free.
- Rebase a CONFLICTING pull request once, immediately before the merge, not after each movement of the default branch.
- Summon a review round only on a final head: no pushes planned, and the base checked against the default branch.
- Process a merge queue serially. Hand the owner every merge-ready pull request first. After the merges, rebase the survivors once, then summon once.
- Before a push, compare the remote head with the head this session last pushed. When another session moved it, stop and reconcile.

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
git branch backup-pre-squash "$source_branch" || {
    echo "Cannot create backup-pre-squash. Resolve the branch error before the rewrite." >&2
    exit 1
}
base=$(git merge-base "$source_branch" origin/main) || {
    echo "Cannot resolve the merge base with origin/main." >&2
    exit 1
}
git switch -c squashed-tmp "$base" || {
    echo "Cannot create squashed-tmp. Resolve the branch error before the rewrite." >&2
    exit 1
}
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

In git-only repos, use git worktrees. Keep the primary checkout on the default branch. Use a repository helper when it exists. In jj colocated repos, use jj workspaces instead. See [GitWorktrees.md](GitWorktrees.md).

### Govern the repository

Detect the platform from the remote origin URL and use its companion: [GitHub.md](GitHub.md) for `gh`, [GitLab.md](GitLab.md) for `glab`. Read the current rules before you change them. Prefer rulesets over legacy branch protection on GitHub. Document governance in the repository (CODEOWNERS, branch rules), not only in external settings.

### Sign commits

The runedeck specification requires unsigned model commits. Automated Jujutsu pushes also stay unsigned. Only an owner-established attended session enables Jujutsu push signing. The attended launcher must show a prompt marker and limit the mode to its subshell. Attended mode changes signing only. It does not authorize a commit or push.

See [Jujutsu.md](Jujutsu.md) for push signing. See [CommitSigning.md](CommitSigning.md) for repositories that require Git signing.

## Verification

- The repository authorship check passes on the outgoing range.
- The prek commit-stage and pre-push hooks pass.
- After a history rewrite, the rewritten tree matches the backup branch (`git diff backup-pre-<op> HEAD` is empty).

## References

- [Jujutsu.md](Jujutsu.md): the jj commit and push discipline for colocated repos.
- [CommitSigning.md](CommitSigning.md): hardware-key signing setup and batch re-signing.
- [GitWorktrees.md](GitWorktrees.md): worktree creation, safety checks, and cleanup.
- [BabysitPR.md](BabysitPR.md): the active review-and-fix loop for a pull request.
- [GitHub.md](GitHub.md), [GitLab.md](GitLab.md): platform governance commands.
