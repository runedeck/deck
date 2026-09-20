## ADDED Requirements

### Requirement: New runes start as registered drafts

A session that starts a new skill, agent, or rule for a consumer MUST create it with `rune draft <kind> <name>` and MUST NOT write it by hand into a provider directory. The session MUST edit the draft where the harness loads it and MUST check it with `rune draft --list` or `rune doctor` before it decides to promote or drop it.

#### Scenario: Session starts a skill

- **WHEN** a session needs a skill that the deck does not carry
- **THEN** it runs `rune draft skill <Name>` at the consumer root and edits the file the command printed

#### Scenario: Session finds an unregistered file

- **WHEN** `rune doctor` reports a hand-written rune as an orphan
- **THEN** the session moves the file aside, runs `rune draft`, and puts the body into the registered copy

### Requirement: Promotion opens the change

A draft that earned its place MUST enter the deck through `rune promote <name> --domain <domain> --change <id>`, with a change id of at least three lowercase hyphenated words. The session MUST then continue in the deck with BuildSkill for the rune body and with the change's `proposal.md`, `tasks.md`, and `adr.md` for the record. A draft that did not earn its place MUST be removed with `rune draft --drop <name>`.

#### Scenario: Draft is promoted

- **WHEN** the session runs `rune promote ReviewSpec --domain core --change review-spec-interaction`
- **THEN** the deck holds `runes/core/skills/ReviewSpec/SKILL.md` and `docs/changes/review-spec-interaction/`, and `rune draft --list` in the consumer prints `no drafts`

#### Scenario: Draft is dropped

- **WHEN** the session runs `rune draft --drop <name>`
- **THEN** every provider copy and the `.drafts` entries are gone and `rune doctor --verify` exits 0
