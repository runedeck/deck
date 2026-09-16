---
name: AgentTeam
description: "Split a change's open tasks into work packages with disjoint file ownership, implement each in its own isolated workspace in parallel, review each against its task ids, and integrate the packages on trunk. USE WHEN implement the change with a team, fan out the tasks, do all the tasks at once, one workspace per task group, parallel implementation of a change directory. NOT FOR a single task (implement it directly), research fan-out (ResearchGrid), or review-only passes (AdversaryReview)."
compatibility: "Requires a workflow tool: the pi workflow extension or Claude Code Workflow. Requires a change directory with tasks.md and a repository with jj or git. Stops with one sentence where no workflow tool exists."
targets: [claude, agentskills]
metadata:
    version: 0.1.0
    decisions: DECK-0016
---

# AgentTeam

Replaces the hand-written brief per workspace. A planner cuts the task list into packages that own disjoint files, children implement in parallel, reviewers check each against its task ids, and an integrator applies the packages onto trunk in order and runs the suite. Nothing is committed or pushed.

## Prerequisites

- A workflow tool. Without one, reply "AgentTeam needs a workflow tool" and stop.
- The change id, from the user's sentence, and the repository root.
- The absolute path of this skill's directory, and of MergeTrain's, for [Split.md](Split.md) and `MergeTrain/Review.md`.

## Constraints

- RemoteWrites applies to every child. Children get the command list without the label exception.
- At most four packages. Packages that run in parallel own disjoint files. A package that depends on another starts from the integrated tree of its predecessor and runs after it.
- One child per package, each in its own workspace on trunk, per the VersionControl Jujutsu or GitWorktrees companion. Never on another session's working copy.
- The integrator applies packages in dependency order onto a fresh trunk workspace and runs the repository's own test and lint commands on the combined tree. It reports, it does not commit.
- Caps: 1 plan, up to 4 implement, up to 4 review, 1 integrate. Total 10 agents, one loop, no nested workflow. A `planOnly` run uses 1.

## Instructions

Read `workflow.js` from this skill's directory and pass it to the workflow tool verbatim. Set `args`:

```json
{ "change": "<id>", "root": "/abs/repo", "skillDir": "/abs/AgentTeam", "reviewDir": "/abs/MergeTrain",
  "planOnly": false, "plan": null, "models": { "plan": "...", "code": "...", "review": "...", "cheap": "..." } }
```

All four paths are required and absolute. Fill `models` from the harness: in pi, `cliproxy/` ids only, plan on astra or sol, code on sol, review on grok. In Claude Code, omit to inherit or name Claude models. Never name an Anthropic model inside pi.

Phases, as the script runs them:

1. Plan: one child applies [Split.md](Split.md) to `docs/changes/<id>/tasks.md` and returns packages with workspace, branch, task ids, owned files, dependencies, and a self-contained brief. The script rejects a plan with a dependency cycle, an unknown dependency, or two parallel packages owning one file.
2. Implement: one child per package, parallel among packages without dependencies, then dependency order. A package whose predecessor failed is blocked, not run. Each writes only its owned files.
3. Review: one child per implemented package applies `MergeTrain/Review.md` against the package's task text.
4. Integrate: runs only when every package built and no review blocks. One child applies each package's owned files onto a fresh trunk workspace in order, runs the suite, and reports the result or the first conflict. Otherwise the run returns `integrated: false` with the reason.

When Storyboard is installed, run twice: first with `planOnly: true`, draw the fan-out frame from the returned packages and get the owner's confirmation, then run again with `plan` set to the confirmed packages. A workflow cannot pause to ask, so the confirmation lives between the two runs.

## Verification

- No file is owned by two parallel packages.
- Every package reports its workspace path and its done and incomplete task ids.
- The integrate child reports the suite result on the combined tree, or the first conflict.
- No commit, push, or pull request exists that the run created.

## References

- [workflow.js](workflow.js), [Split.md](Split.md), `MergeTrain/Review.md`.
- Deck skill VersionControl, companions `Jujutsu.md` and `GitWorktrees.md`, for workspace mechanics.
- Condensed from forge-council `DeveloperSprint`, forge-dev `SubagentDrivenDevelopment` and `JujutsuToolkit`. Cut: TeamCreate and SendMessage (children cannot message), the architect chat (became the Plan phase), and the three-stage review (one review per package plus one integration check).
