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
updated: 2026-10-25
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

The BrowserbaseToolkit *[skill][SKILL]* came from forge-provision with four documents. Three are its own: the *[canon][CANON]* and two *[companions][COMPANION]*. The fourth is a copy of the vendor's own [skill][SKILL] file, sealed by a provenance *[sidecar][SIDECAR]*. In the *[deck][DECK]*, an imported file joins only after an adoption review, and every upstream change means a new review and a new seal. The vendor publishes the same file at one address, and its CLI installs a bundled copy of it. Does the [deck][DECK] keep that file, or point at it? A second question is the domain. A vendor domain of its own is what the Proton [skills][SKILL] have. The development domain is where a session that writes automation code looks.

## Considered Options

1. Adopt the vendor's file through the review state machine, with a sealed [sidecar][SIDECAR], and adopt it again on each upstream change.
2. Drop the copy. The [canon][CANON] links the published address for the full command reference and names the CLI command that prints the bundled copy.
3. Keep the copy without a review. This breaks the adoption rule and is listed only to say so.

## Decision Outcome

Option 2, in the development domain.

- The [skill][SKILL] MUST point at the vendor's published [skill][SKILL] file for the full command reference and MUST NOT hold a copy of it.
- The canonical [skill][SKILL] and its shared [companions][COMPANION] MUST name no *[harness][HARNESS]* tool, so every [harness][HARNESS] can load them. Claude Code runtime syntax goes only in the Claude variant, which other [harnesses][HARNESS] never receive.
- The [skill][SKILL] MUST carry no executable that changes the host. Its one script reads a page into a temporary directory and stops every browser session that it opens.
- The [skill][SKILL] lives in the development domain, beside the other [skills][SKILL] a session uses while it writes code. A vendor domain holds a [skill][SKILL] whose model or privacy constraints differ from the rest, as the Proton domain does. This [skill][SKILL] has no such constraint.

### Consequences

- [+] The [skill][SKILL] holds only its own files, and an upstream change needs no new adoption review or seal.
- [+] The link gives the session the current upstream text, and `browse skills show` prints the copy that matches the installed CLI.
- [-] The printed copy is as fresh as the installed CLI version.
- [-] A session that needs a command the [canon][CANON] does not list needs network access to the published address, or the CLI on the machine.
- [-] No digest pins what the session reads from upstream. The vendor can change the file under the link.
- [-] The [deck][DECK] has no recorded proof for the [skill][SKILL] yet. The bench result sits in the benchmark workspace, outside the [deck][DECK].

[SKILL]: ../../specs/glossary/skill.md
[CANON]: ../../specs/glossary/canon.md
[COMPANION]: ../../specs/glossary/companion.md
[SIDECAR]: ../../specs/glossary/sidecar.md
[DECK]: ../../specs/glossary/deck.md
[HARNESS]: ../../specs/glossary/harness.md
