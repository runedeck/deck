# proof-page-handover Specification

## Purpose

A finished proof is handed to the owner as a page that plays each cast and lists its scenes, never as a GIF path. This specification defines the handover and the page generator `scripts/proof-page.py` in the AcceptanceTesting skill.

## Requirements

### Requirement: A proof is handed over as a page

When a recorded proof is finished, the handover to the owner MUST be a page that plays each cast through the html-tools cast player and lists one scene per scenario. The message MUST contain the page's absolute path. A message with only the GIF path is an unfinished handover.

#### Scenario: Proof finished

- **WHEN** the recording exits with status 0 and the transcript check passes
- **THEN** the skill builds the page with `scripts/proof-page.py` and the handover states its absolute path

#### Scenario: Owner asks where the proof is

- **WHEN** the owner asks for the proof
- **THEN** the answer is the page's absolute path, and the GIF path is at most a second line

### Requirement: The page builds from the casts alone

`scripts/proof-page.py` MUST take the cast files, one caption and any number of short facts per proof, and the player script, and MUST write one self-contained file. The scene list MUST come from the `# Scenario:` lines in the cast, not from a hand-written list.

#### Scenario: Cast with five scenes

- **WHEN** the generator reads a cast whose driver printed five `# Scenario:` lines
- **THEN** the page lists those five titles in playback order beside the player
