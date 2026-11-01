---
title: "A proof plays as a cast where a person reads it"
description: "A recorded proof on a page plays its asciinema cast through the html-tools player, with pause and the current scene, and the GIF remains for places that render images only."
type: adr
category: process
tags:
    - runedeck
    - proofs
    - skill
status: accepted
created: 2026-09-20
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0015 Behavior Proof per Change"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: playable-proof-recordings-page
---

# A proof plays as a cast where a person reads it

## Context and Problem Statement

The driver records a *[proof][PROOF]* as a cast and renders a GIF image from it. A pull request body can show the GIF, and the owner watched the GIF. The GIF loops, cannot pause, and never says which scene is on screen. The cast has the scene titles already.

## Considered Options

1. Render the GIF with a scene counter drawn into each frame.
2. Play the cast on the page with a player that pauses, scrubs, and names the scene.
3. Both: the player where a person reads, the GIF where only an image renders.

## Decision Outcome

Option 3. The player is one script in html-tools with no framework behind it. Its tests run without a browser. The player reads the scene titles from the driver's own `# Scenario:` lines. The GIF stays, because a pull request body renders only images.

The *[skill][SKILL]* MUST keep these rules:

- A page that shows a [proof][PROOF] MUST play the cast through the html-tools player.
- The GIF MUST remain beside the cast in the *[repository][REPOSITORY]*.

### Consequences

- [-] A page that shows a [proof][PROOF] has to include a copy of html-tools. The workshop's [proof][PROOF] page of 2026-09-20 inlines the script instead, because the page is one file with no [repository][REPOSITORY] of its own.
- [-] The driver's comment line is the scene marker. A recording made outside the driver has no scenes. The player then shows only a scrubber.

## More Information

- Recorded [proofs][PROOF] `docs/proofs/playable-proof-recordings-page/` (pause and scene label under node) and `docs/proofs/convenient-proof-page-viewer/` (the page generator on a five-scene cast), 2026-09-21.
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[PROOF]: ../specs/glossary/proof.md
[SKILL]: ../specs/glossary/skill.md
[REPOSITORY]: ../specs/glossary/repository.md
