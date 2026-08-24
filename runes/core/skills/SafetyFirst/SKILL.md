---
name: SafetyFirst
description: "Work with command guards, never around them: prefer safe command forms, plan for guard intervention, and hand off what a guard rightly blocks. USE WHEN a command was blocked, a safety hook fired, dcg blocked a command, permission denied by a classifier, planning a destructive operation (reset, force-push, rm, restore, truncate), or a sandbox denial interrupts work. NOT FOR security review of code (GuardRails), sandbox or permission configuration (update-config), or debugging a broken hook."
metadata:
    version: 0.1.0
allowed-tools: Bash(command -v *) Bash(dcg *)
---

# SafetyFirst

Guard stack on this machine:

!`command -v dcg 2>/dev/null || echo "(dcg: not installed)"`
!`dcg --version 2>/dev/null || echo "(dcg: no version output)"`

Agent sessions run behind layered guards: safety hooks that match destructive commands, permission classifiers, sandbox rules, and the user's own review. The layers change over time and differ between machines. This skill is the discipline that holds for all of them: a block is information, not an obstacle. A bypass attempt enters the audit trail and costs trust. The guard usually catches a real mistake.

## Constraints

- Never bypass a guard: no cosmetic rewording of a blocked command, no alternate binary or wrapper, no environment tricks, no disabling the guard, no edits to guard configuration.
- Never ask another session or agent to run what this session was denied. That launders the user's permission decision.
- Never retry a blocked command verbatim. A denial means the user or their policy declined it.
- A guard is a net, not a boundary. The sandbox is the security control. Do not treat a guard as one.
- When a block catches a genuine mistake, take the safer path without complaint.

## Instructions

### Prefer the safe form first

The best interaction with a guard is none. Reach for the non-destructive form before the guard has anything to catch:

| Instead of | Use |
|---|---|
| `git reset --hard <ref>` | `git stash`, then a soft or mixed reset. When the tree is identical: `git checkout -B <branch> <ref>` |
| `git checkout <ref> -- <path>` | `git show <ref>:<path> >| <path>` |
| `git restore <path>` | `git restore --staged <path>` (keeps the worktree), or `git stash` |
| `git push --force` | `git push --force-with-lease=<branch>`, and only on your own branch |
| `git branch -D <branch>` | Verify the merge state on the platform first. Hand force-deletes to the user |
| `rm -rf <path>` | `trash <path>`, or `rm` named files inside the working directory |
| `> ~/<file>` truncation | Append with `>>`, write to a scratch path, or back up first |

### Design the sequence for intervention

Assume any step can be denied. Order work so a mid-sequence block leaves a consistent state:

- Do the reads and previews first (`git diff`, `--dry-run`, `-n`). Put the one mutating step last.
- Make steps idempotent, so the sequence can resume after a denial without redoing damage.
- Create the recovery point before the risky step (a backup branch, a stash, a copy), not after.
- Never chain a destructive command behind `&&` with unrelated work. A block mid-chain strands the rest.

### When a guard blocks

1. Read the whole block message. Guards state the rule, the rationale, and the safer alternative. The answer is usually in the message.
2. Take the suggested alternative. Worked examples: a blocked `checkout <ref> -- <path>` becomes `git show <ref>:<path>` into the file, and a blocked `reset --hard` becomes a stash plus a branch re-point.
3. When the guard offers an explain command (for example `dcg explain "<command>"`), use it to understand the rule before choosing a path.
4. When the intent is genuinely needed and no safe form exists, stop and hand the exact command to the user with one sentence on why the operation is required. The user runs it in their own terminal, or grants a narrow permission.
5. When the block looks like a false positive (a name collision, for example `jj restore` matched by a git rule), explain the mismatch to the user. Configuration changes belong to the user, never to the agent.

### Know the installed guards

Treat every layer with the same discipline. Known instances on this stack:

| Guard | Kind | On block |
|---|---|---|
| dcg (Destructive Command Guard) | Command-matching hook across harnesses | Follow its message and use `dcg explain` for the rule. Allowlist changes are the user's call |
| Permission classifier | AI-judged policy layer | Do not probe for phrasings that slip past. Route the action to the user |
| Sandbox | Filesystem and network boundary | Work inside the allowed paths. A denied write never justifies an invented location |
| Permission prompts | The user's live decision | A denial is an instruction. Adjust the approach |

New guards join this table on adoption. The discipline above does not change.

## Verification

- No blocked command was rerun verbatim, reworded, or routed through another tool or session.
- No guard configuration changed.
- Every handed-off command appears in the final report with its one-sentence reason.
- The task's destructive steps each had a recovery point created before them.

## References

- [dcg](https://github.com/Dicklesworthstone/destructive_command_guard): the destructive-command guard installed on this stack.
- forge-core GuardRails: the adjacent skill for security review and guard configuration detail.
