## ADDED Requirements

### Requirement: Repository prose stays under the rune caps

Every requirement statement in the canonical specifications and in change directories MUST stay at or under 100 words, every scenario step at or under 30 words, and every `CHANGELOG.md` change line at or under 200 characters in the shape the validator enforces. The quality job MUST run a validator that carries both rules, so the caps hold in CI and not only on a contributor's machine.

#### Scenario: Requirement grows past the cap

- **WHEN** a change adds a requirement statement of 120 words
- **THEN** the validator fails the commit-stage checks and names the heading line

#### Scenario: Changelog entry becomes a paragraph

- **WHEN** a change adds a `CHANGELOG.md` line of 400 characters
- **THEN** the validator fails the check and reports a named diagnostic with the line number
