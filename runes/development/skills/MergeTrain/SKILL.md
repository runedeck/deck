---
name: MergeTrain
description: "Survey a repository's open pull requests read-only, clear the blockers an agent can clear in isolated workspaces, review each repair, and report to the owner with full URLs. USE WHEN what is ready to merge, sitrep on the queue, babysit the open pull requests, clear the blockers, merge train over a repo. NOT FOR merging (the owner merges), posting on pull requests, or a single pull request's review loop (VersionControl BabysitPR)."
compatibility: "Requires a workflow tool: the pi workflow extension or Claude Code Workflow. Requires gh authenticated read-only for the repository. Stops with one sentence where no workflow tool exists."
targets: [claude, agentskills]
metadata:
    version: 0.1.0
    decisions: DECK-0016
---

# MergeTrain

The name says train. The skill never merges. It surveys, repairs in isolation, reviews, and reports. The owner merges.

## Prerequisites

- A workflow tool. Without one, reply "MergeTrain needs a workflow tool" and stop.
- `owner/repo` from the user's sentence. Optional: a repair cap, default 8.
- The absolute path of this skill's directory, for the child briefs.

## Constraints

- RemoteWrites applies to every phase and every child. Children get the command list without the label exception.
- Survey and Report run `gh` read commands only.
- A repair child edits inside its own workspace and stops. It never commits, pushes, or opens anything.
- Every verdict is bound to the head SHA read at survey time. A moved head makes the verdict stale and the child stops.
- Caps: 1 survey, up to 8 repairs, up to 8 reviews, 1 report. Total 18 agents, one loop, no nested workflow.
- Every pull request in the report carries its full `https://` URL and every repair its absolute workspace path.

## Instructions

Read `workflow.js` from this skill's directory and pass it to the workflow tool verbatim. Set `args`:

```json
{ "repo": "owner/repo", "maxRepairs": 8, "skillDir": "/abs/path/to/MergeTrain",
  "changeId": "<id or omit>", "models": { "plan": "...", "code": "...", "review": "...", "cheap": "..." } }
```

`skillDir` is required and absolute. Fill `models` from the harness: in pi, `cliproxy/` ids only, code and plan on sol, review on grok, cheap on lumo. In Claude Code, omit `models` to inherit, or name Claude models. Never name an Anthropic model inside pi.

Phases, as the script runs them:

1. Survey: one child applies [Triage.md](Triage.md) and returns one blocker and one `actionable` verdict per pull request, with head SHA and URL.
2. Repair: one child per actionable blocker, capped, each in a workspace on the pull request head, per the VersionControl Jujutsu or GitWorktrees companion. It stops when the blocker is cleared, when the head moved, or when the blocker needs the owner.
3. Verify: one child per cleared repair applies [Review.md](Review.md) to the workspace diff and returns ranked findings with a blocking flag.
4. Report: one child writes the owner report from the structured results. Lead with what the owner must do now.

When Storyboard is installed, show its plan graph before the run and its result graph after.

## Verification

- No `gh pr` write command and no push appear in any child transcript.
- Every reported pull request has a URL, a head SHA, one blocker, and a verdict.
- Every repair names an absolute workspace path, or a reason it stopped.
- The script passed to the tool is byte-identical to `workflow.js`.

## References

- [workflow.js](workflow.js), [Triage.md](Triage.md), [Review.md](Review.md).
- Deck skill VersionControl, companion `BabysitPR.md`, for one pull request's active review-and-fix loop.
- Condensed from forge-dev `FixCI`, `CodeReviewer`, and forge-core `PullRequests`. Cut: the Python check inspector, the merge-approval step (a child cannot ask), and the pull request review posting surface (prohibited).
