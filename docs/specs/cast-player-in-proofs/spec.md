# cast-player-in-proofs Specification

## Purpose

A recorded proof shown on a page plays its cast through the html-tools player, with pause, a scrubber, and the current scene. The GIF remains in the repository for a pull request body and other places that render images only. This specification defines that split.

## Requirements

### Requirement: A proof on a page plays its cast

When a recorded proof is shown on a page that a person reads, the page MUST play the cast through the html-tools cast player, with pause, resume, a scrubber, and the scene the playhead is in, taken from the driver's `# Scenario:` lines. The GIF MUST remain beside the cast in the repository, for a pull request body and any other place that renders images only.

#### Scenario: Reader pauses a proof

- **WHEN** a reader opens a page that shows a proof and presses Space during a scene
- **THEN** playback stops and the page names that scene by its number and title

#### Scenario: Pull request shows the proof

- **WHEN** the pull request body embeds the proof
- **THEN** it embeds the GIF, because the body renders images only
