---
name: ForgeCycle
description: "Route a spec-driven change to its next stage of the idea-to-merge loop and hand that stage to the skill that owns it. USE WHEN continue the change, where are we on a change, next step, run the loop, what stage is this in, resume work on a change directory, or after a review, lint, or CI result lands. NOT FOR intake of a raw idea (IntakeIdea), running a workflow yourself (MergeTrain, AgentTeam, AdversaryReview, ResearchGrid), or commits and pushes (VersionControl)."
compatibility: "Requires rune for `rune spec context`. Works in every harness. Stages owned by a skill absent from the harness end the turn with a report."
metadata:
    version: 0.1.0
    decisions: DECK-0008, DECK-0016
---

# ForgeCycle

One turn, one edge. Read where the change is, print the stage strip, name the next stage and the skill that owns it, and end the turn. The next turn invokes that skill. This skill never runs a stage itself.

## Prerequisites

- A change directory `docs/changes/<id>/` with `tasks.md`. Without one, route to IntakeIdea.
- `rune spec context <id>` for the work order, or `tasks.md` read directly when rune is absent.

## Constraints

- Never invoke a workflow tool or a workflow skill. Name it and stop.
- Never ready a draft, merge, comment, label, or resolve. The RemoteWrites rule applies to every stage. Pushing your own branch after the prek pipeline is allowed.
- Never nest: a stage that fans out (AgentTeam, MergeTrain) runs in its own turn with its own caps.
- Take exactly one edge per turn. A second edge waits for the next turn, even when it looks obvious.
- Keep no state of your own. `tasks.md` tick marks, the storyboard frames, and the pull request are the state.
- Stop and report when the owner closes the pull request, when the owning skill is not installed, or when the next edge needs an owner decision.

## Instructions

1. Read `rune spec context <id>` and `docs/changes/<id>/tasks.md`. Find the first unchecked task and the last storyboard frame under `docs/changes/<id>/storyboard/` if one exists. When a pull request URL is known, read its state with one `gh pr view` read call first. A closed, unmerged pull request stops the loop before any task-based routing.
2. Locate the change on the stage strip. The mapping from evidence to stage is in [Stages.md](Stages.md).
3. Print the strip with the current stage in brackets, then the next stage and its owner:

    ```text
    prompt · pushback · specify · isolate · [swarm] · gates · skim · lanes · babysit · approve · extract · recycle
    next: gates  owner: VersionControl (ContinuousIntegration)   change: agentic-merge-train  3/8 tasks
    ```

4. Pick the edge. Forward when the current stage's exit signal holds. Return edges: adversary findings, red gates, or requested changes go back to swarm, owner AgentTeam or the session. A fatal hit marked as a design flaw goes back to specify, owner ArchitectureDecision. A closed pull request stops.
5. Ask the extraction question at every exit, not only at the end: did this pass produce a rule, a skill, or a lesson. If yes, state the proposed extraction in one line of the reply so the owner or a later LearnFrom turn records it. Write nothing yourself, and do not name a second owner now.
6. End the turn with the owner named and the one sentence the next turn should start from. When Storyboard is installed, that next turn opens with a frame.

## Verification

- The reply contains exactly one stage in brackets and exactly one next owner.
- No tool call in the turn changed a file, a branch, or a remote.
- The named owner is installed in the harness, or the reply says it is not and stops.

## References

- [Stages.md](Stages.md): the twelve DECK-0008 stages, their owners, entry and exit signals, and return edges.
- Deck decisions DECK-0008 Idea-to-Merge Flywheel and DECK-0016 Forge Adoption.
- Condensed from forge-core `ExecutePlan`, `WorkSessionFlow`, and `VerifyCompletion`. Cut: the linear plan executor and the completion checklist, because the change's `tasks.md` and delta specs already carry both.
