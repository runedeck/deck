## ADDED Requirements

### Requirement: Storyboard frames precede writes

Before the first file write of a stage, Storyboard MUST show an ASCII frame and wait for the owner's confirmation. When a change directory exists, the first frame MUST be the change map with the current stage marked. A correction from the owner MUST produce a redrawn frame before any write. Each stage MUST end with a frame of what changed. Confirmed frames MUST be saved under `docs/changes/<id>/storyboard/` in order, after confirmation, and MUST use one glyph set at 78 columns or less. The question uses the harness's question tool when one exists and a plain question otherwise.

#### Scenario: Change directory exists

- **WHEN** a session starts work inside a change
- **THEN** the first frame is the change map with the current stage marked, and the session waits for confirmation

#### Scenario: Owner edits a box

- **WHEN** the owner answers with a correction to the frame
- **THEN** the frame is redrawn and shown again before any write

#### Scenario: Stage ends

- **WHEN** a stage finishes
- **THEN** a delta frame is shown and saved as the next numbered file
