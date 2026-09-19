# Stages

The twelve stages of DECK-0008, in order. Each has one owner, one entry signal, and one exit signal. ForgeCycle names the owner and stops. The owner runs the stage in the next turn.

- **prompt**. Owner: the owner. Entry: a raw idea, transcript, or sketch arrives. Exit: text exists.
- **pushback**. Owner: IntakeIdea. Entry: text exists and no change directory does. Exit: a verdict of duplicate, extension, or survivor.
- **specify**. Owner: IntakeIdea, then ArchitectureDecision when alternatives exist. Entry: survivor. Exit: `rune spec validate <id>` passes and the ADR is linked when one exists.
- **isolate**. Owner: VersionControl, Jujutsu or GitWorktrees companion. Entry: tasks exist and no workspace does. Exit: a workspace on trunk named after the change.
- **swarm**. Owner: AgentTeam when the tasks split into packages, else the session itself. Entry: a workspace and unchecked tasks. Exit: every package reports done or blocked.
- **gates**. Owner: VersionControl through ContinuousIntegration, and AdversaryReview for prose and design. Entry: code or text changed. Exit: `rune validate`, tests, and lint green, and no open fatal hit.
- **skim**. Owner: Storyboard. Entry: gates green. Exit: the owner confirmed the delta frame.
- **lanes**. Owner: VersionControl for the push, the app for the draft, the owner's key for ready. Entry: owner confirmed. Exit: draft open, `rune sign open` run and touched, the controller's triage recorded.
- **babysit**. Owner: MergeTrain. Entry: pull request ready. Exit: every blocker cleared or handed to the owner, the ledger terminal, `rune sign submit` run.
- **approve**. Owner: the owner. Entry: a queue entry with its coverage state. Exit: `rune sign next` touched and merged, or closed.
- **extract**. Owner: LearnFrom. Entry: merged. Exit: a rule, a skill, or a lesson written, or "nothing to extract" recorded.
- **recycle**. Owner: `rune install`. Entry: the extraction landed. Exit: the next pass loads it.

## Return edges

- gates, on adversary findings or red checks: back to swarm.
- gates, on a fatal hit marked design flaw: back to specify, through ArchitectureDecision.
- skim, when the owner edits a box: back to swarm, or to specify when the box is a requirement.
- lanes or babysit, on changes requested: back to swarm.
- babysit, when the head moved under a verdict: stay in babysit and re-survey.
- approve, on closed without merge: stop, report, and ask whether to archive as abandoned.

## Locating the stage from evidence

- No `docs/changes/<id>` yet: pushback.
- Change exists but `rune spec validate` fails, or the proposal names an ADR that does not exist: specify.
- Spec valid and no workspace named after the change: isolate.
- Workspace exists and implementation tasks are unchecked: swarm.
- Implementation tasks ticked and verification tasks open: gates.
- Gates green and no confirmed delta frame: skim.
- Delta frame confirmed and no pull request URL in `tasks.md` or the transcript: lanes.
- Pull request open and not merged: babysit.
- Pull request closed and not merged: stop, report, and ask whether to archive as abandoned. Never route to swarm from here.
- Merged and the extraction task open: extract.
- Extraction ticked: recycle, then archive with `rune spec archive <id>`.

## Owner absent

When the owning skill is not installed in the harness, print the stage, name the skill, and stop. Do not substitute a prose imitation of the missing skill.
