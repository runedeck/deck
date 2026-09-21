# proof-page-handover Specification

## Purpose

TBD - created by archiving change proof-page-handover. Update Purpose after archive.

## Requirements

### Requirement: A proof is handed over as a page

When a recorded proof is finished, the handover to the owner MUST be a page that plays each cast through the html-tools cast player and lists one scene per scenario. The message MUST carry the page's absolute path. A message that names only the GIF is an unfinished handover.

#### Scenario: Proof finished

- **WHEN** the recording exits with status 0 and the transcript check passes
- **THEN** the skill builds the page with `scripts/proof-page.py` and the handover names its absolute path

#### Scenario: Owner asks where the proof is

- **WHEN** the owner asks for the proof
- **THEN** the answer is the page's absolute path, and the GIF path is at most a second line

### Requirement: The page builds from the casts alone

`scripts/proof-page.py` MUST take the cast files, one caption and any number of short facts per proof, and the player script, and MUST write one self-contained file. The scene list MUST come from the `# Scenario:` lines in the cast, not from a hand-written list.

#### Scenario: Cast with five scenes

- **WHEN** the generator reads a cast whose driver printed five `# Scenario:` lines
- **THEN** the page lists those five titles in playback order beside the player
