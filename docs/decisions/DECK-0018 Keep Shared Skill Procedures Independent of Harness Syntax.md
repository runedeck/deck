---
title: "Keep shared skill procedures independent of harness syntax"
description: "Align shared skill instructions and rules with layered validation."
type: adr
category: deck
tags: [skills, portability, authoring]
status: accepted
created: 2026-09-11
updated: 2026-10-19
author: "@N4M3Z"
project: runedeck
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["gpt-6-astra@codex"]
informed: []
upstream: []
change: skills-portable-across-harnesses
---

# Keep shared skill procedures independent of harness syntax

## Context and Problem Statement

The generic layer cannot give consistent *[instructions][INSTRUCTION]* when it requires tools from one *[harness][HARNESS]*.
The authoring guide must enforce the same boundary that the *[validator][VALIDATOR]* checks.

This *[architecture decision record][ARCHITECTUREDECISIONRECORD]* (ADR) remains an unnumbered proposal pending maintainer review.

## Considered Options

1. The author treats native commands as harmless text. What each command does when a [harness][HARNESS] runs it then remains unclear.
2. The author suppresses the [validator][VALIDATOR]'s findings. The contradiction between the authoring guide and the [validator][VALIDATOR] then remains.
3. The author duplicates all workflow text. Several places then repeat the same procedure, and each one needs maintenance.

## Decision Outcome

The author writes the generic entrypoint (the *[canon][CANON]*) and the generic *[companions][COMPANION]* as portable capability [instructions][INSTRUCTION].
The author keeps native scopes and procedures in an explicit entrypoint *[variant][VARIANT]* for that [harness][HARNESS].
The layer check must pass before the author declares authoring compliance.
The author keeps native evidence as a separate acceptance condition.

### Consequences

- [+] Shared [instructions][INSTRUCTION] remain usable without a fixed catalog of [harness][HARNESS] tools.
- [+] Metadata specific to one [harness][HARNESS] remains with that [harness][HARNESS].
- [+] The *[change][CHANGE]* does not need a new *[assembly][ASSEMBLY]* mechanism. It grants neither deployment nor approval authority.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[INSTRUCTION]: ../specs/glossary/instruction.md
[HARNESS]: ../specs/glossary/harness.md
[VALIDATOR]: ../specs/glossary/validator.md
[CANON]: ../specs/glossary/canon.md
[COMPANION]: ../specs/glossary/companion.md
[VARIANT]: ../specs/glossary/variant.md
[ARCHITECTUREDECISIONRECORD]: ../specs/glossary/architecture-decision-record.md
[CHANGE]: ../specs/glossary/change.md
[ASSEMBLY]: ../specs/glossary/assembly.md
