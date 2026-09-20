## ADDED Requirements

### Requirement: Remote writes belong to the owner

An agent MUST NOT run `gh pr merge`, `gh pr close`, `gh pr comment`, `gh pr review`, `gh pr edit --add-label`, `gh pr edit --remove-label`, `gh issue comment`, `gh issue close`, `git push`, `jj git push`, or a review-thread resolution call, and MUST NOT reach the same effects through the API. Two exceptions belong to the invoking agent only, never to a child: the single review label the prompt names, and the repository's correctness review label, applied once to a pull request the agent opened or babysits, after its required checks pass on the current head. The agent MUST NOT repeat a summon while a round is pending. The rule MUST load in every harness where rune installs core rules. Where rune has no rules path yet, the harness's `AGENTS.md` MUST carry the same list until the assembly target exists.

#### Scenario: Routine session finishes a fix

- **WHEN** a session with no workflow skill loaded finishes a code fix
- **THEN** it runs none of the listed commands and reports what the owner can push

#### Scenario: Prompt names a review label

- **WHEN** the prompt says to summon a reviewer with a named label
- **THEN** the invoking agent adds exactly that label and touches no other label

#### Scenario: Checks pass on a babysat pull request

- **WHEN** every required check passes on the current head of a pull request the agent opened or babysits, and no review round is pending
- **THEN** the agent adds the correctness review label once and reports the summon
