---
title: "Behavior Proof per Change"
description: "Every change with user-visible behavior carries a recorded end-to-end proof, one scene per specification scenario with expectations on the output, filed as the behavior proof"
type: adr
category: process
tags:
    - ceremony
    - evidence
    - acceptance
status: accepted
created: 2026-09-15
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0013 Local Checks Before Publication"
    - "DECK-0014 Vocabulary Governance"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: record-proof-per-scenario
---

# Behavior Proof per Change

## Context and Problem Statement

A clean candidate can still do the wrong thing, and this record makes a recorded *[proof][PROOF]* of its behavior part of every *[change][CHANGE]*. DECK-0013 made the check stages the [proof][PROOF] that a candidate is clean. Every check passes on a feature that does not behave as its specification says. A reviewer then reads the diff and infers the behavior, or trusts the prose of the pull request. The specification already states the behavior as *[scenarios][SCENARIO]*, and DECK-0014 gave the prove stage a `rune:Proof` with a `behavior` kind that nothing produces yet. The proposal in #64 was a terminal-recording *[skill][SKILL]* as a README demo helper. A demo that asserts nothing is not evidence.

## Decision Drivers

- The [scenarios][SCENARIO] of the specification are the acceptance criteria. A [proof][PROOF] that walks them proves the *[requirement][REQUIREMENT]* instead of the self-image of the implementation.
- A recording that a reviewer watches, and a transcript that a machine searches, are evidence. A diff is not.
- A demo without expectations passes when the feature does not work.

## Considered Options

1. AcceptanceTesting in core. The author records one *[scene][SCENES]* per [scenario][SCENARIO], with `expect` on every THEN. A failed expectation fails the recording. The author files the GIF and the transcript as the `behavior` [proof][PROOF], and the VersionControl [skill][SKILL] lists the [proof][PROOF] as a step before every push.
2. The terminal-recording [skill][SKILL] as proposed. It is a README demo helper with no assertions.
3. Unit tests and a reviewer's reading.

## Decision Outcome

Option 1, AcceptanceTesting, with the mandate in the `record-proof-per-scenario` delta.

A [change][CHANGE] with user-visible behavior has one scene per [scenario][SCENARIO] of its *[delta specification][DELTASPECIFICATION]*. Each scene runs the WHEN steps against the built candidate and asserts each THEN with `expect`. The driver exits nonzero on a miss, and `asciinema rec --return` passes that exit status out. The recording itself then fails. The author stores the GIF under `docs/proofs/<change>/`. The Testing section of the pull request embeds the GIF with the commit id. The [proof][PROOF] record states the [scenario][SCENARIO] list, the exit status, and the transcript digest. The [proof][PROOF] lists a [scenario][SCENARIO] without a scene as unproven.

Option 2 records what happened without stating what the feature must do. Option 3 is the state this decision replaces.

### Consequences

- [-] An implementation is not done until its [scenes][SCENES] pass. This adds a recording pass to every [change][CHANGE] with behavior. A prose-only [change][CHANGE] has no [proof][PROOF] and says so.
- [-] The [proof][PROOF] is only as good as the [scenarios][SCENARIO]. Nobody can prove a specification without [scenarios][SCENARIO], and that is a defect in the specification.
- [-] The [skill][SKILL] depends on asciinema, agg, and ffmpeg, and `scripts/install-tools` does not install them. The prerequisites of the [skill][SKILL] list the Homebrew formulae.
- [+] The `behavior` [proof][PROOF] kind in `rune:proofKinds` gains its producer.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[PROOF]: ../specs/glossary/proof.md
[CHANGE]: ../specs/glossary/change.md
[SCENARIO]: ../specs/glossary/scenario.md
[SKILL]: ../specs/glossary/skill.md
[REQUIREMENT]: ../specs/glossary/requirement.md
[SCENES]: ../specs/glossary/scenes.md
[DELTASPECIFICATION]: ../specs/glossary/delta-specification.md
