# Jujutsu (jj) workflow

When a repo is colocated with jj (`.jj/` at the root), there is no staging area, and this workflow replaces the git flow. Detect by the presence of `.jj/`. Drive mutations through jj and keep raw git read-only.

## The change workflow

1. `jj describe -m "feat: thing"` names the unit of work.
2. Edit. Every jj command auto-snapshots `@`. There is nothing to stage and nothing is lost.
3. Use `jj split` when `@` contains more than one logical change.
4. `jj new` creates an empty working-copy change after the described change.
5. `jj bookmark set <name> -r @-` points the bookmark at the described change. Bookmarks do not move automatically.
6. Run `jj push`. The `make install` alias runs the pre-push checks before `jj git push`.

After a squash-merged pull request, reconcile with `jj git fetch`, then `jj rebase -d main@origin --skip-emptied`.

## Auto-snapshot pulls in out-of-band drift

jj snapshots every non-gitignored file into `@`. A tool that writes into the tree out-of-band silently lands those files in whatever commit `@` is. Gitignore the tool's local files, or park `@` on a scratch commit (`jj new -m scratch`) so drift accumulates there. To pull drift out of a polluted commit, use `jj squash --from <commit> --into <scratch> <paths>`.

The same trap runs the other way: an edit intended for a parked change lands wherever `@` sits. Confirm the base with `jj status` before you edit files for a specific change. Relocate a misplaced edit with `jj squash --from @ --into <rev> <paths>`.

## Signing modes

Automated mode is the default. Use `signing.behavior=drop` with `git.sign-on-push=false`. This keeps snapshots and automated pushes unsigned.

Only the owner can start attended mode. Apply a separate overlay that sets `git.sign-on-push=true`. Put the base file first and the attended overlay last in `JJ_CONFIG`. On Unix, separate the paths with a colon. End attended mode when the owner exits its subshell. Do not change the base file to enter attended mode.

An agent launcher must ignore an inherited attended overlay. It must load the base file and an agent overlay. The agent overlay must set `git.sign-on-push=false`.

Attended mode changes signing only. It does not authorize a push. Do not create a raw `git commit -S` in a colocated repository.

## Secret scans run at push

jj runs no git hooks, so the commit-stage checks do not fire. `make install` relocates the scan: it wires a repo-local jj `push` alias to `.githooks/jj-push`, which runs the pre-push prek stage (gitleaks, semgrep) and only then `jj git push`. Push with `jj push`. If the alias is not wired, scan the outgoing commits by hand first:

```sh
from=$(jj log --no-graph -r 'trunk()' -T 'commit_id')
to=$(jj log --no-graph -r '@-' -T 'commit_id')
gitleaks git --log-opts "$from..$to"
```

CI re-runs the same pre-push checks as the backstop. Never weaken this to a post-push fixup. A public push that leaks a secret needs rotation plus history surgery.

## Parallel work uses workspaces, not git worktrees

In a colocated repo, `git worktree add` mutates refs behind jj's back. Use `jj workspace add ../repo-<name>`, one workspace per agent, based on a stable commit (`trunk()` or a described change), never another session's live `@`. "Working copy is stale" is routine: `jj workspace update-stale` re-syncs. Finish with `jj workspace forget <name>`; remove the directory separately.

## A change description is text, not a scratchpad

A described jj change is a reviewable git commit. A throwaway change can carry a review brief (`jj new -m "<brief>"`, then `jj abandon` after), but a real commit's message stays what-changed-and-why. Never put a review brief into the commit that carries the change.
