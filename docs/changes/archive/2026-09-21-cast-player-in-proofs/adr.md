---
title: "A proof plays as a cast where a person reads it"
description: "A recorded proof on a page plays its asciinema cast through the html-tools player, with pause and the current scene, and the GIF stays for image-only surfaces."
type: adr
category: process
tags:
    - runedeck
    - proofs
    - skill
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0015 Recorded Behavior Proofs"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: cast-player-in-proofs
---

# A proof plays as a cast where a person reads it

## Context and Problem Statement

A proof is recorded as a cast and rendered as a GIF. The GIF is what a pull request body can show, and it is what the owner watched. It loops, cannot pause, and never says which scene is on screen. The cast has the scene titles already.

## Considered Options

1. Render the GIF with a scene counter burned into each frame.
2. Play the cast on the page with a player that pauses, scrubs, and names the scene.
3. Both: the player where a person reads, the GIF where only an image renders.

## Decision Outcome

Option 3. The player is one vanilla script in html-tools, tested without a browser, and reads the scene titles from the driver's own `# Scenario:` lines. The GIF stays because a pull request body renders images only.

The skill MUST keep these rules:

- A page that shows a proof MUST play the cast through the html-tools player.
- The GIF MUST stay committed beside the cast.

## Consequences

- A page that shows proofs vendors html-tools. The workshop's proof page of 2026-09-20 inlines the script instead, because it is one file with no repository of its own.
- The scene marker is the driver's comment line. A recording made outside the driver has no scenes, only a scrubber.
