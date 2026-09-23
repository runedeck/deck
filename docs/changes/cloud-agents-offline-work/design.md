# Cloud agents offline work design

## Approach

The cloud installer downloads and verifies every pinned release asset on each run and never trusts a binary already on the image. The specification names the installer and the files it places by role. This table names the paths that implement them.

## Commands

| Requirement | Command | Notes |
|---|---|---|
| Standalone schema validator | `/usr/local/bin/mdschema` | The installer places the verified `mdschema` release binary at this path so repository hooks can invoke it. The schema responsibilities stay in `runes/core/skills/BuildSkill/RuneDeck.md`. |
