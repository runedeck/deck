---
adr: docs/changes/cast-player-in-proofs/adr.md
status: proposed
decisions: ["A proof plays as a cast where a person reads it"]
---

# Cast player in proofs

## Why

The owner watched the three proofs of 2026-09-20 as GIFs and asked to pause, resume, and see which part was on screen. A GIF cannot do that. The asciinema cast beside every GIF carries the scene titles the driver prints, and html-tools now plays it in a page with those controls.

## What Changes

- AcceptanceTesting `Recording.md`: the Embed section says to play the cast through the html-tools cast player on a page a person reads, and to keep the GIF for image-only surfaces.

## Capabilities

### New Capabilities

- `cast-player-in-proofs`: a proof shown on a page plays its cast with pause, scrub, and the current scene.

## Impact

- One companion file of the AcceptanceTesting skill. The player lives in [html-tools](https://github.com/N4M3Z/html-tools) (`runtime/cast-player.js`, change `cast-player-runtime`).
