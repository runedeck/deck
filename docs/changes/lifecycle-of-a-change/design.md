# Spec change lifecycle design

## Design

The change builds the lifecycle of a change. A change directory holds a proposal, a task list, and one delta specification for each capability. The validator rejects a change that lacks any of them. The name check refuses a change id or a capability name with fewer than four words. The archiver merges an accepted delta into the canonical tree once a record exists and the owner has reviewed each rule.

## Commands

A requirement names a role. This table names the path, program, and hook behind each row, so nothing is lost when a command moves out of a requirement.

| Requirement | Command | Notes |
|---|---|---|
| Change layout | `docs/changes/<id>/` | The change directory. It holds `proposal.md`, `tasks.md`, and `specs/<capability>/spec.md`. |
| Testable requirements | `openspec validate --all --strict`, `rune spec doctor` | The validator. Both run on `docs/` (tasks 1.2 and 2.1). |
| One canonical tree | `docs/specs/`, `docs/changes/archive/<date>-<id>/` | The canonical tree and the archive destination. `rune spec archive` performs the move (tasks 2.2 and 2.3). |
| Names have four words | `scripts/check-spec-names` | The name check, run as a prek hook. `docs/changes/local-checks/` is the two-word example the scenario describes. |
| Archive is acceptance | `rune spec archive` | Refuses a change with no `adr.md` and no entry under the `decisions` frontmatter key (task 2.4, cli). |
| Owner reviews each rule before archive | none | No program implements the review. The owner answers one scenario question with fixed options for each MUST statement. |
