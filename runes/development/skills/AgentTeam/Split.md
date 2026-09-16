# Split

Convert a task list into briefs that parallel agents execute without colliding. The split is the deliverable. Change no code.

## Constraints

- Read-only. Create no workspace, edit no file, run no version-control command.
- At most four packages. More exceed the run's concurrency and gain nothing.
- Cover only unchecked tasks. Never invent a task id.
- Two packages that write the same file are not independent. Merge them, or make one depend on the other.
- Every package names its workspace, its branch, its task ids, its owned files, its dependencies, and what it inherits as text.

## Procedure

Read the task list once. Extract each unchecked task with its full text. The implementing agent will not read this file.

Cut along file ownership, not topic. Two tasks belong in one package when they write the same file, when one reads an interface the other defines, or when one cannot be verified until the other lands.

Where a clean cut is impossible, declare a dependency instead of a parallel pair. A dependent package starts from its predecessor's integrated tree and runs after it. State the inherited interface as text in the dependent's brief, because it cannot see the predecessor's working copy.

Name the workspace after its work, not its number. Name the branch to match.

When the list yields one package, say so and recommend direct execution. A fan-out of one is overhead.

When a dependency chain makes every package serial, say so. The run still isolates each package, but the owner may prefer one session.

## Output

Packages with name, workspace, branch, task ids, files, dependsOn, inherits, and a self-contained brief. A `blocked` reason when no valid split exists.
