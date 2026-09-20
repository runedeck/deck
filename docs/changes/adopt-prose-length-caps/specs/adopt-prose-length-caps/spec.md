## ADDED Requirements

### Requirement: Deck prose stays under the rune caps

Every requirement statement in `docs/specs/` and `docs/changes/` MUST stay at or under 100 words, every scenario step at or under 30 words, and every `CHANGELOG.md` change line at or under 200 characters in the shape `rune docs check` enforces. The quality job MUST run a `rune` that carries both rules, so the caps hold in CI and not only on a contributor's machine.

#### Scenario: Requirement grows past the cap

- **WHEN** a change adds a requirement statement of 120 words
- **THEN** `rune spec validate` fails the commit-stage checks and names the heading line

#### Scenario: Changelog entry becomes a paragraph

- **WHEN** a change adds a `CHANGELOG.md` line of 400 characters
- **THEN** `rune docs check` fails with `entry-length` and the line number
