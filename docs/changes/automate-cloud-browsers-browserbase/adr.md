---
title: "Point at the upstream reference instead of vendoring it"
description: "The BrowserbaseToolkit skill links the vendor's published skill file for the full command reference and holds no copy of it, so no new adoption review follows an upstream change."
type: adr
category: architecture
tags:
    - runedeck
    - domain
    - development
    - browserbase
status: proposed
created: 2026-10-22
updated: 2026-10-22
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream:
    - "automate-cloud-browsers-browserbase#command-reference-stays-upstream"
    - "https://browserbase.com/SKILL.md"
change: automate-cloud-browsers-browserbase
---

# Point at the upstream reference instead of vendoring it

## Context and Problem Statement

The BrowserbaseToolkit *[skill][SKILL]* came from forge-provision with four documents. Three are its own: the *[canon][CANON]* and two *[companions][COMPANION]*. The fourth is a copy of the vendor's own skill file, sealed by a provenance *[sidecar][SIDECAR]*. In the *[deck][DECK]*, an imported file joins only after an adoption review, and every upstream change means a new review and a new seal. The vendor publishes the same file at one address, and its CLI installs a bundled copy of it. Does the deck keep that file, or point at it? A second question is the domain. A vendor domain of its own is what the Proton skills have. The development domain is where a session that writes automation code looks.

## Considered Options

1. Adopt the vendor's file through the review state machine, with a sealed sidecar, and adopt it again on each upstream change.
2. Drop the copy. The canon links the published address for the full command reference and names the CLI command that installs the bundled copy.
3. Keep the copy without a review. This breaks the adoption rule and is listed only to say so.

## Decision Outcome

Option 2, in the development domain.

- The skill MUST point at the vendor's published skill file for the full command reference and MUST NOT hold a copy of it.
- The skill MUST consist of plain documents only and MUST name no *[harness][HARNESS]* tool, so every harness can load it.
- The skill lives in the development domain, beside the other skills a session uses while it writes code. A vendor domain holds a skill whose model or privacy constraints differ from the rest, as the Proton domain does. This skill has no such constraint.

### Consequences

- [+] The skill is three documents, and an upstream change needs no new adoption review or seal.
- [+] The link gives the session the current upstream text.
- [-] The install command copies the reference bundled with the installed CLI, so that copy is as fresh as the CLI version.
- [-] A session that needs a command the canon does not list needs network access to the published address, or the CLI on the machine.
- [-] No digest pins what the session reads from upstream. The vendor can change the file under the link.
- [-] The deck has no bench verdict and no proof for the skill yet. The measurement lives in the forge-provision bench workspace.

[SKILL]: ../../specs/glossary/skill.md
[CANON]: ../../specs/glossary/canon.md
[COMPANION]: ../../specs/glossary/companion.md
[SIDECAR]: ../../specs/glossary/sidecar.md
[DECK]: ../../specs/glossary/deck.md
[HARNESS]: ../../specs/glossary/harness.md
