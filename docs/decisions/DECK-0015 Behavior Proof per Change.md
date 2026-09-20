---
title: "Behavior Proof per Change"
description: "Every change with user-visible behavior carries a recorded end-to-end proof, one scene per specification scenario with expectations on the output, filed as the behavior proof"
type: adr
category: process
tags:
    - ceremony
    - evidence
    - acceptance
status: proposed
created: 2026-09-15
updated: 2026-09-15
author: "@N4M3Z"
project: deck
related:
    - "DECK-0013 Local Checks Before Publication"
    - "DECK-0014 Vocabulary Governance"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
---

# Behavior Proof per Change

## Context and Problem Statement

DECK-0013 made the check stages the proof that a candidate is clean. A clean candidate can still do the wrong thing: every check passes on a feature that does not behave as its specification says. Reviewers then read the diff and infer behavior, or trust the pull request's prose. The specification already states the behavior as scenarios, and DECK-0014 gave the prove stage a `rune:Proof` with a `behavior` kind that nothing produces yet. A terminal-recording skill was proposed as a README demo helper (#64). A demo that asserts nothing is not evidence.

## Decision Drivers

- The specification's scenarios are the acceptance criteria. A proof that walks them is a proof of the requirement, not of the implementation's self-image.
- A recording that a reviewer can watch, and a transcript a machine can grep, is evidence a diff is not.
- A demo without expectations passes when the feature is broken.

## Considered Options

1. AcceptanceTesting in core: one recorded scene per scenario, `expect` on every THEN, a failed expectation fails the recording, the GIF and transcript filed as the `behavior` proof, and VersionControl names it before every push.
2. The terminal-recording skill as proposed, a README demo helper with no assertions.
3. Rely on unit tests and reviewer reading.

## Decision Outcome

Chosen option: AcceptanceTesting, with the mandate in the `prove-each-scenario` delta.

A change with user-visible behavior carries one scene per scenario of its delta specification. Each scene runs the WHEN steps against the built candidate and asserts each THEN with `expect`. The driver exits nonzero on a miss and `asciinema rec --return` carries that out, so the recording itself fails. The GIF lives under `docs/proofs/<change>/`, the pull request's Testing section embeds it with the commit id, and the proof record carries the scenario list, the exit status, and the transcript digest. A scenario without a scene is listed as unproven.

Option 2 records what happened without saying what should have. Option 3 is the state this decision replaces.

## Consequences

- An implementation is not done until its scenes pass, which adds a recording pass to every change with behavior. A prose-only change carries no proof and says so.
- The proof is only as good as the scenarios. A specification without scenarios cannot be proven, which is a defect in the specification.
- The skill depends on asciinema, agg, and ffmpeg, which `scripts/install-tools` does not install. The skill's prerequisites name the Homebrew formulae.
- The `behavior` proof kind in `rune:proofKinds` gains its producer.
