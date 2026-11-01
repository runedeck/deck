---
title: "A rune is one governed instruction"
description: "A rune is one governed instruction: a Markdown file with frontmatter, a skill, an agent, a rule, or a hook, with one canon, optional companions and variants, and a provenance sidecar."
type: adr
category: architecture
tags:
    - architecture
    - vocabulary
    - runes
status: proposed
created: 2026-09-23
updated: 2026-09-23
author: "@N4M3Z"
project: deck
related:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
    - "DECK-0014 Vocabulary Governance"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream:
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Is%20The%20System"
    - "instructions-stay-vendor-neutral#reusable-across-harnesses-and-models"
change: one-domain-one-plugin
---

# A rune is one governed instruction

## Context and Problem Statement

A *[rune][RUNE]* is the unit the deck is made of, and this record says what one is.
The foundations define the *[instruction][INSTRUCTION]*, the file a *[harness][HARNESS]* loads to steer a *[model][MODEL]*, and require that one source serves every [harness][HARNESS] and [model][MODEL].
A governed [instruction][INSTRUCTION] has three kinds of part: what is written once, what varies by [harness][HARNESS] and [model][MODEL], and what records where an *[instance][INSTANCE]* came from.
Anthropic's glossary calls rules [instruction][INSTRUCTION] files, and says that Claude Code is the [harness][HARNESS] and Claude the [model][MODEL] inside it ([Claude Code glossary][CC-GLOSSARY]).
Its hooks are settings entries, and a hook [rune][RUNE] is the Markdown source that *[assembly][ASSEMBLY]* renders into such an entry.

## Considered Options

1. Leave the term to the ontology comment. Then nothing records why a [rune][RUNE] has these parts and not others.
2. Write one record that defines the parts and the rule for each: one *[canon][CANON]*, *[companions][COMPANION]* for what one [harness][HARNESS] needs, *[variants][VARIANT]* for what one [harness][HARNESS] or [model][MODEL] needs, a *[sidecar][SIDECAR]* for provenance, and [assembly][ASSEMBLY] as the only way to make an [instance][INSTANCE].

## Decision Outcome

Option 2.

- A [rune][RUNE] MUST be one [instruction][INSTRUCTION]: a Markdown file with YAML frontmatter, of kind skill, agent, rule, or hook. A hook [rune][RUNE] is the source of a [harness][HARNESS]'s hook configuration. The rendered configuration is not a [rune][RUNE].
- A [rune][RUNE] MUST have exactly one [canon][CANON], the vendor-neutral entrypoint, and the [canon][CANON] MUST NOT contain a harness-specific [instruction][INSTRUCTION].
- A harness-specific [instruction][INSTRUCTION] MUST live in a [companion][COMPANION].
- A harness-, model-, or user-specific alternative MUST live in a [variant][VARIANT].
- An [instance][INSTANCE] MUST come from [assembly][ASSEMBLY], one for each [harness][HARNESS] and [model][MODEL], and MUST NOT be edited in its *[target][TARGET]*.
- Provenance MUST live in the [sidecar][SIDECAR] under `.provenance/`, the one exception to metadata inside the file (CORE-0002).

### Consequences

- [+] Every requirement that says [rune][RUNE] now points at one definition, and the term check refuses a prose use with no ontology entry.
- [+] A new [harness][HARNESS] costs [companions][COMPANION] and nothing in a [canon][CANON].
- [-] A [canon][CANON] that contains [harness][HARNESS] wording fails the rule, and that wording belongs in a [companion][COMPANION].
- [-] [Model][MODEL] is a second [assembly][ASSEMBLY] dimension, and resolving it needs the [harness][HARNESS] to say which [model][MODEL] runs.

[INSTRUCTION]: ../../specs/glossary/instruction.md
[CC-GLOSSARY]: https://code.claude.com/docs/en/glossary
[RUNE]: ../../specs/glossary/rune.md
[HARNESS]: ../../specs/glossary/harness.md
[MODEL]: ../../specs/glossary/model.md
[CANON]: ../../specs/glossary/canon.md
[COMPANION]: ../../specs/glossary/companion.md
[VARIANT]: ../../specs/glossary/variant.md
[ASSEMBLY]: ../../specs/glossary/assembly.md
[TARGET]: ../../specs/glossary/target.md
[SIDECAR]: ../../specs/glossary/sidecar.md
[INSTANCE]: ../../specs/glossary/instance.md
