## ADDED Requirements

### Requirement: Draft in the shared register

A drafted change MUST use Simplified Technical English and the repository's markdown schemas. The draft MUST define each term of art on first use or link the definition.

The [IntakeIdea skill](../../../../../runes/core/skills/IntakeIdea/SKILL.md#step-2-size-the-blast-radius) defines the blast-radius classes. A decision-bearing draft uses its Decision class.

The xlarge threshold is 1,000 added and deleted lines. Before push, the agent MUST calculate that total from the working-copy diff.

After pull request creation, the [PR lint workflow](../../../../../.github/workflows/pr-lint.yaml) assigns `size:xlarge` at the same threshold.

#### Scenario: A draft leaves the register

- **WHEN** a drafted document violates the STE style or its mdschema
- **THEN** the earliest available local lint reports the violation before owner review

#### Scenario: A harness has no post-edit hook

The [Deck provider list](../../../../../deck.yaml) defines the supported harness set. Codex has no post-edit hook and MUST use this fallback.

- **WHEN** a supported harness has no post-edit hook
- **THEN** the agent runs the Markdown and schema checks from the [Declared World gate ladder](../../../declared-world/design.md#the-gate-ladder) before owner review

### Requirement: Deterministic pass precedes review

Every deterministic check MUST run and pass before a human reads the draft. The owner reviews content, never formatting, spelling, schema, or link health.

#### Scenario: A draft reaches the owner

- **WHEN** a draft is presented for owner review
- **THEN** the local Markdown checks, `rune spec validate`, and `rune validate` have already passed on it

### Requirement: Review points by blast radius

A decision-bearing or xlarge change MUST get a draft review before its pull request. A smaller change MAY go straight to the pull request, where the ceremony provides the review.

The draft verdict MUST identify the reviewed planning-artifact content with a digest. A content change MUST invalidate the verdict and require a new owner review.

The pull request MUST carry the verdict only when its planning artifacts match the reviewed digest.

#### Scenario: A decision-bearing change is drafted

- **WHEN** IntakeIdea classifies a change as Decision or the working-copy diff reaches the xlarge threshold
- **THEN** the owner reviews the draft before any push, and the pull request carries the verdict for the same digest

#### Scenario: A reviewed draft changes before push

- **WHEN** planning-artifact content changes after owner review
- **THEN** the pipeline invalidates the verdict and stops the push until the owner reviews the new digest
